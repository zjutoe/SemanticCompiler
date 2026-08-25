"""Fixed local-only E5 qwen3:14b interface smoke and offline verifier."""

# ruff: noqa: E402

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from urllib.parse import urlsplit

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Phase0.implementation.dialect import MANAGED_EFFECTS, TRAJECTORIES_BY_ID
from Phase0.implementation.fixture_loader import load_fixture_input
from Phase0.implementation.schema import CanonicalPayload
from Phase0.implementation.typed_paths import (
    ContractClause,
    ContractOpenArgument,
    ContractSurfaceState,
    IsomorphicOpenBinding,
    IsomorphicProposition,
    IsomorphicTerm,
    SemanticIsomorphicSurfaceState,
    alpha_A,
    alpha_B,
)


SCHEMA_VERSION = "phase0.e5.v1"
HANDOFF_PATH = "Phase0/handoffs/E5_local_qwen3_14b_smoke.md"
HANDOFF_BLOB = "ca8daecea42dcaf28c9d1de5cfc6a4988013be10"
RUNNER_PATH = "Phase0/run_e5_smoke.py"
FIXTURE_PATH = "Phase0/fixtures/F2_OPEN_UE_OWNER_BOUNDARY.json"
FIXTURE_CASE = "unresolved"

ENDPOINT = "http://127.0.0.1:11434"
CHAT_URL = f"{ENDPOINT}/api/chat"
OLLAMA_VERSION = "0.32.6"
MODEL = "qwen3:14b"
MODEL_LIST_ID = "bdbd181c33f2"
MODEL_BLOB_PATH = Path(
    "/data1/ollama/models/blobs/"
    "sha256-a8cc1361f3145dc01f6d77c6c82c9116b9ffe3c97b34716fe20418455876c40e"
)
MODEL_BLOB_BYTES = 9_276_184_896
MODEL_BLOB_SHA256 = "a8cc1361f3145dc01f6d77c6c82c9116b9ffe3c97b34716fe20418455876c40e"
MODELFILE_SHA256 = "f9490322d6987537a71e039fc188246336809f00bd5e3c472b83c4ff9f132414"

TIMEOUT_SECONDS = 600
RESPONSE_BODY_LIMIT_BYTES = 1024 * 1024
REQUEST_IDS = ("A__F2__unresolved", "B__F2__unresolved")
PACKAGE_FILES = (
    "manifest.json",
    "requests.json",
    "responses.json",
    "summary.json",
)

REPO_ROOT = Path(__file__).resolve().parents[1]
_COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")


class E5Error(ValueError):
    """Raised when the fixed E5 protocol or evidence is invalid."""


DECISION_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$defs": {
        "typed_value": {
            "type": "object",
            "additionalProperties": False,
            "required": ["type", "value"],
            "properties": {
                "type": {"type": "string", "minLength": 1},
                "value": {"type": "string", "minLength": 1},
            },
        },
        "resolution": {
            "type": "object",
            "additionalProperties": False,
            "required": ["semantic_slot_link", "value"],
            "properties": {
                "semantic_slot_link": {"type": "string", "minLength": 1},
                "value": {"$ref": "#/$defs/typed_value"},
            },
        },
        "clause_conflict_witness": {
            "type": "object",
            "additionalProperties": False,
            "required": ["kind", "clause_links"],
            "properties": {
                "kind": {"const": "ClauseConflictWitness"},
                "clause_links": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1},
                },
            },
        },
        "empty_domain_witness": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "kind",
                "semantic_slot_link",
                "excluding_constraint_links",
            ],
            "properties": {
                "kind": {"const": "EmptyDomainWitness"},
                "semantic_slot_link": {"type": "string", "minLength": 1},
                "excluding_constraint_links": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1},
                },
            },
        },
        "cross_constraint_witness": {
            "type": "object",
            "additionalProperties": False,
            "required": ["kind", "cross_constraint_links"],
            "properties": {
                "kind": {"const": "CrossConstraintWitness"},
                "cross_constraint_links": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1},
                },
            },
        },
        "excluded_action": {
            "type": "object",
            "additionalProperties": False,
            "required": ["action_id", "unauthorized_managed_effects"],
            "properties": {
                "action_id": {"type": "string", "minLength": 1},
                "unauthorized_managed_effects": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1},
                },
            },
        },
        "no_authorized_action_witness": {
            "type": "object",
            "additionalProperties": False,
            "required": ["kind", "excluded_actions"],
            "properties": {
                "kind": {"const": "NoAuthorizedActionWitness"},
                "excluded_actions": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"$ref": "#/$defs/excluded_action"},
                },
            },
        },
    },
    "oneOf": [
        {
            "type": "object",
            "additionalProperties": False,
            "required": ["kind", "semantic_slot_links"],
            "properties": {
                "kind": {"const": "ASK"},
                "semantic_slot_links": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1},
                },
            },
        },
        {
            "type": "object",
            "additionalProperties": False,
            "required": ["kind", "action_id", "executor_resolutions"],
            "properties": {
                "kind": {"const": "EXECUTE"},
                "action_id": {"type": "string", "minLength": 1},
                "executor_resolutions": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/resolution"},
                },
            },
        },
        {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "kind",
                "reason",
                "witness",
                "executor_resolutions",
            ],
            "properties": {
                "kind": {"const": "REJECT"},
                "reason": {"const": "HARD_UNSAT"},
                "witness": {
                    "oneOf": [
                        {"$ref": "#/$defs/clause_conflict_witness"},
                        {"$ref": "#/$defs/empty_domain_witness"},
                        {"$ref": "#/$defs/cross_constraint_witness"},
                    ]
                },
                "executor_resolutions": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/resolution"},
                },
            },
        },
        {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "kind",
                "reason",
                "witness",
                "executor_resolutions",
            ],
            "properties": {
                "kind": {"const": "REJECT"},
                "reason": {"const": "NO_AUTHORIZED_ACTION"},
                "witness": {"$ref": "#/$defs/no_authorized_action_witness"},
                "executor_resolutions": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/resolution"},
                },
            },
        },
    ],
}

SYSTEM_POLICY = """Interpret only the supplied semantic packet and apply these rules in order.
1. A normative proposition is active only when every claimed-authority support ref exists and resolves to a USER source. GOAL, REQUIRE, and PRESERVE are satisfied when their interpreted predicate is true; FORBID is satisfied when it is false. ALLOW authorizes its matching managed effect and is not a hard obligation. Ignore inactive propositions.
2. Enumerate typed joint completions in slot-declaration/domain order. Keep only completions consistent with resolved values, static exclusions, and cross-constraint allowed tuples. Pair a completion only with a candidate trajectory whose complete assignment equals it.
3. REJECT with HARD_UNSAT when a declared effective domain is empty, no legal completion exists, or no paired trajectory satisfies every active hard proposition. REJECT with NO_AUTHORIZED_ACTION when hard-valid pairs exist but every pair emits at least one managed effect not covered by an active matching ALLOW. Construct the corresponding witness only from supplied links, actions, and effects.
4. A safe EXECUTE choice is one action_id plus values for every EXECUTOR-owned OPEN slot such that choosing those executor values removes no currently legal projection of unresolved USER-owned values and an authorized hard-valid trajectory with that same action_id exists for every remaining USER-value projection. Choose safe choices by action_id, then by the supplied enum-domain order. EXECUTE with the chosen action and all executor resolutions when a safe choice exists.
5. Otherwise ASK only unresolved USER-owned links. List unresolved USER links in slot-declaration order. Enumerate their subsets by increasing cardinality and then combination order. A subset is sufficient only when, for every distinct legal answer projected onto that subset, treating that answer as resolved makes rules 3 or 4 produce REJECT or EXECUTE without another ASK. Return the first sufficient subset. Never ASK an EXECUTOR-owned link and never resolve a USER-owned link yourself.
6. Return exactly one Decision matching the supplied closed JSON schema, with no prose."""


def _compact_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


SYSTEM_MESSAGE = (
    SYSTEM_POLICY
    + "\nDecision JSON schema:\n"
    + _compact_json(DECISION_SCHEMA)
)


def _a_surface() -> ContractSurfaceState:
    return ContractSurfaceState(
        clauses=(
            ContractClause(
                clause_link="clause:000",
                modality="REQUIRE",
                predicate="world.error_handling_is",
                arguments=(
                    ContractOpenArgument(
                        semantic_slot_link="slot:clause:000:arg0",
                        type="ErrorPolicy",
                        owner="USER",
                        proposition_support=("u1",),
                    ),
                    ContractOpenArgument(
                        semantic_slot_link="slot:clause:000:arg1",
                        type="LogMode",
                        owner="EXECUTOR",
                        proposition_support=("u1",),
                    ),
                ),
                proposition_support=("u1",),
                claimed_authority_support=("u1",),
            ),
        ),
        knowledge_assertions=(),
    )


def _b_surface() -> SemanticIsomorphicSurfaceState:
    return SemanticIsomorphicSurfaceState(
        propositions=(
            IsomorphicProposition(
                proposition_index=0,
                force="REQUIRE",
                relation="world.error_handling_is",
                terms=(
                    IsomorphicTerm("OPEN", "ErrorPolicy", None),
                    IsomorphicTerm("OPEN", "LogMode", None),
                ),
                evidence=("u1",),
                authority_evidence=("u1",),
            ),
        ),
        facts=(),
        open_bindings=(
            IsomorphicOpenBinding(0, 0, "USER", ("u1",)),
            IsomorphicOpenBinding(0, 1, "EXECUTOR", ("u1",)),
        ),
    )


def build_packets() -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    """Build the exact expected-blind A/B model-visible packets."""

    fixture = load_fixture_input(REPO_ROOT / FIXTURE_PATH, FIXTURE_CASE)
    if not isinstance(fixture.entry_payload, CanonicalPayload):
        raise E5Error("F2 unresolved fixture is not canonical")
    a_surface = _a_surface()
    b_surface = _b_surface()
    canonical = fixture.entry_payload.canonical_state
    if alpha_A(a_surface) != canonical or alpha_B(b_surface) != canonical:
        raise E5Error("A/B surfaces do not equal the frozen F2 canonical state")

    if fixture.candidate_trajectory_ids != (
        "tau:f2:return_none_quiet",
        "tau:f2:raise_verbose",
    ):
        raise E5Error("F2 candidate trajectory order changed")
    trajectories = [
        asdict(TRAJECTORIES_BY_ID[trajectory_id])
        for trajectory_id in fixture.candidate_trajectory_ids
    ]
    shared = {
        "source_envelope": asdict(fixture.source_envelope),
        "visible_world_context": asdict(fixture.visible_world_context),
        "slot_declarations": [asdict(item) for item in fixture.slot_declarations],
        "static_constraints": [asdict(item) for item in fixture.static_constraints],
        "cross_constraints": [asdict(item) for item in fixture.cross_constraints],
        "dialect_interpretations": [
            {
                "predicate": "world.error_handling_is",
                "scope": "FINAL",
                "rule": (
                    "final observables error_policy and log_mode equal the two "
                    "typed arguments"
                ),
            }
        ],
        "managed_effect_universe": list(MANAGED_EFFECTS),
        "candidate_trajectories": trajectories,
    }
    packets = (
        {
            "encoding": "A",
            "semantic_serialization": asdict(a_surface),
            **shared,
        },
        {
            "encoding": "B",
            "semantic_serialization": asdict(b_surface),
            **shared,
        },
    )
    left = {key: value for key, value in packets[0].items() if key not in {"encoding", "semantic_serialization"}}
    right = {key: value for key, value in packets[1].items() if key not in {"encoding", "semantic_serialization"}}
    if left != right or packets[0]["semantic_serialization"] == packets[1]["semantic_serialization"]:
        raise E5Error("A/B packet isolation changed")
    return packets


def build_requests() -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    """Build the exact two Ollama request bodies without reading expected data."""

    packets = build_packets()
    return tuple(
        {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": _compact_json(packet)},
            ],
            "format": DECISION_SCHEMA,
            "stream": False,
            "think": False,
            "keep_alive": 0,
            "options": {
                "temperature": 0,
                "seed": 0,
                "num_predict": 256,
            },
        }
        for packet in packets
    )


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _validate_local_transport_binding() -> None:
    parts = urlsplit(CHAT_URL)
    if (
        parts.scheme != "http"
        or parts.hostname != "127.0.0.1"
        or parts.port != 11434
        or parts.path != "/api/chat"
        or parts.username is not None
        or parts.password is not None
        or parts.query
        or parts.fragment
    ):
        raise E5Error("chat transport is not the frozen localhost endpoint")


def _build_opener() -> urllib.request.OpenerDirector:
    _validate_local_transport_binding()
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        _NoRedirect(),
    )


def _reject_duplicate_pairs(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise E5Error(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise E5Error(f"invalid JSON constant: {value}")


def _decode_json(data: bytes, where: str) -> Any:
    try:
        return json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise E5Error(f"{where} is not valid UTF-8 JSON") from error


def _http_transport(request_body: Mapping[str, Any]) -> Mapping[str, Any]:
    data = _compact_json(request_body).encode("utf-8")
    request = urllib.request.Request(
        CHAT_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with _build_opener().open(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read(RESPONSE_BODY_LIMIT_BYTES + 1)
    except OSError as error:
        raise E5Error("localhost Ollama transport failed") from error
    if len(raw) > RESPONSE_BODY_LIMIT_BYTES:
        raise E5Error("Ollama response exceeds the 1 MiB limit")
    document = _decode_json(raw, "Ollama response")
    if not isinstance(document, dict):
        raise E5Error("Ollama response must be an object")
    return document


def _require_exact_keys(value: Any, keys: set[str], where: str) -> Mapping[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise E5Error(f"{where} has invalid fields")
    return value


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _valid_unique_strings(value: Any, *, nonempty: bool = True) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(_nonempty_string(item) for item in value)
        and len(value) == len(set(value))
    )


def _validate_typed_value(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and set(value) == {"type", "value"}
        and _nonempty_string(value["type"])
        and _nonempty_string(value["value"])
    )


def _validate_resolutions(value: Any) -> bool:
    return isinstance(value, list) and all(
        isinstance(item, dict)
        and set(item) == {"semantic_slot_link", "value"}
        and _nonempty_string(item["semantic_slot_link"])
        and _validate_typed_value(item["value"])
        for item in value
    )


def _validate_hard_unsat_witness(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    kind = value.get("kind")
    if kind == "ClauseConflictWitness":
        return set(value) == {"kind", "clause_links"} and _valid_unique_strings(value["clause_links"])
    if kind == "EmptyDomainWitness":
        return (
            set(value) == {"kind", "semantic_slot_link", "excluding_constraint_links"}
            and _nonempty_string(value["semantic_slot_link"])
            and _valid_unique_strings(value["excluding_constraint_links"])
        )
    if kind == "CrossConstraintWitness":
        return set(value) == {"kind", "cross_constraint_links"} and _valid_unique_strings(value["cross_constraint_links"])
    return False


def _validate_no_action_witness(value: Any) -> bool:
    if not isinstance(value, dict) or set(value) != {"kind", "excluded_actions"}:
        return False
    actions = value["excluded_actions"]
    return (
        value["kind"] == "NoAuthorizedActionWitness"
        and isinstance(actions, list)
        and bool(actions)
        and all(
            isinstance(action, dict)
            and set(action) == {"action_id", "unauthorized_managed_effects"}
            and _nonempty_string(action["action_id"])
            and _valid_unique_strings(action["unauthorized_managed_effects"])
            for action in actions
        )
    )


def _validate_decision(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    kind = value.get("kind")
    if kind == "ASK":
        return set(value) == {"kind", "semantic_slot_links"} and _valid_unique_strings(value["semantic_slot_links"])
    if kind == "EXECUTE":
        return (
            set(value) == {"kind", "action_id", "executor_resolutions"}
            and _nonempty_string(value["action_id"])
            and _validate_resolutions(value["executor_resolutions"])
        )
    if kind != "REJECT" or set(value) != {
        "kind",
        "reason",
        "witness",
        "executor_resolutions",
    } or not _validate_resolutions(value["executor_resolutions"]):
        return False
    if value["reason"] == "HARD_UNSAT":
        return _validate_hard_unsat_witness(value["witness"])
    if value["reason"] == "NO_AUTHORIZED_ACTION":
        return _validate_no_action_witness(value["witness"])
    return False


def _validate_service_envelope(value: Any) -> str:
    if not isinstance(value, dict):
        raise E5Error("service envelope must be an object")
    if value.get("model") != MODEL or value.get("done") is not True:
        raise E5Error("service envelope has wrong model identity or completion state")
    message = value.get("message")
    if not isinstance(message, dict) or message.get("role") != "assistant":
        raise E5Error("service envelope must contain one assistant message")
    content = message.get("content")
    if not _nonempty_string(content):
        raise E5Error("assistant message content must be non-empty")
    if "messages" in value:
        raise E5Error("service envelope contains additional messages")
    for container in (message, value):
        for field in ("tool_calls", "images"):
            if field in container and container[field] not in (None, []):
                raise E5Error(f"service envelope contains forbidden {field}")
    for container in (message, value):
        if "thinking" in container and container["thinking"] not in (None, ""):
            raise E5Error("service envelope contains non-empty thinking")
    return content


def _analyze_response(
    request_id: str,
    response: Mapping[str, Any],
    expected: Mapping[str, Any],
) -> Mapping[str, Any]:
    content = _validate_service_envelope(response)
    parsed: Any = None
    error: str | None = None
    try:
        parsed = json.loads(
            content,
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_json_constant,
        )
    except (json.JSONDecodeError, E5Error):
        error = "INVALID_JSON"
    if error is None and not _validate_decision(parsed):
        error = "INVALID_DECISION_SCHEMA"
        parsed = None
    if error is not None:
        outcome = "INVALID_OUTPUT"
    elif parsed == expected:
        outcome = "EXACT_MATCH"
    else:
        outcome = "DECISION_MISMATCH"
    return {
        "request_id": request_id,
        "service_response": response,
        "parsed_decision": parsed,
        "validation_error": error,
        "outcome": outcome,
    }


def _read_expected_decision() -> Mapping[str, Any]:
    raw = _decode_json((REPO_ROOT / FIXTURE_PATH).read_bytes(), "F2 fixture")
    if not isinstance(raw, dict) or not isinstance(raw.get("cases"), list):
        raise E5Error("F2 fixture document changed")
    matches = [item for item in raw["cases"] if item.get("case_id") == FIXTURE_CASE]
    if len(matches) != 1 or not isinstance(matches[0].get("expected"), dict):
        raise E5Error("F2 expected case changed")
    decision = matches[0]["expected"].get("decision")
    if not _validate_decision(decision):
        raise E5Error("F2 expected decision is invalid")
    return decision


def _build_summary(
    source_commit: str,
    records: Sequence[Mapping[str, Any]],
) -> Mapping[str, Any]:
    parsed = [record["parsed_decision"] for record in records]
    if all(item is not None for item in parsed):
        parity = "MATCH" if parsed[0] == parsed[1] else "MISMATCH"
    else:
        parity = "NOT_COMPARABLE"
    status = (
        "PASS"
        if [record["outcome"] for record in records] == ["EXACT_MATCH", "EXACT_MATCH"]
        and parity == "MATCH"
        else "FAIL"
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "implementation_source_commit": source_commit,
        "model": MODEL,
        "request_ids": list(REQUEST_IDS),
        "request_results": [
            {"request_id": record["request_id"], "outcome": record["outcome"]}
            for record in records
        ],
        "parsed_decision_parity": parity,
        "status": status,
        "scope_notice": (
            "Non-blocking local interface smoke only; non-scientific and not "
            "deployment evidence."
        ),
    }


def _manifest(source_commit: str, output_root: str) -> Mapping[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "implementation_source_commit": source_commit,
        "accepted_handoff_path": HANDOFF_PATH,
        "accepted_handoff_blob": HANDOFF_BLOB,
        "runner_path": RUNNER_PATH,
        "fixture_path": FIXTURE_PATH,
        "fixture_case": FIXTURE_CASE,
        "endpoint": ENDPOINT,
        "ollama_version": OLLAMA_VERSION,
        "model": MODEL,
        "model_list_id": MODEL_LIST_ID,
        "model_blob_path": str(MODEL_BLOB_PATH),
        "model_blob_bytes": MODEL_BLOB_BYTES,
        "model_blob_sha256": MODEL_BLOB_SHA256,
        "modelfile_sha256": MODELFILE_SHA256,
        "request_options": {
            "format": DECISION_SCHEMA,
            "stream": False,
            "think": False,
            "keep_alive": 0,
            "options": {"temperature": 0, "seed": 0, "num_predict": 256},
            "timeout_seconds": TIMEOUT_SECONDS,
            "response_body_limit_bytes": RESPONSE_BODY_LIMIT_BYTES,
        },
        "output_root": output_root,
        "request_ids": list(REQUEST_IDS),
    }


def _canonical_json_bytes(value: Any) -> bytes:
    return (_compact_json(value) + "\n").encode("utf-8")


def _serialize_package(
    source_commit: str,
    output_root: str,
    requests: Sequence[Mapping[str, Any]],
    records: Sequence[Mapping[str, Any]],
) -> Mapping[str, bytes]:
    return {
        "manifest.json": _canonical_json_bytes(_manifest(source_commit, output_root)),
        "requests.json": _canonical_json_bytes(list(requests)),
        "responses.json": _canonical_json_bytes(
            {"schema_version": SCHEMA_VERSION, "responses": list(records)}
        ),
        "summary.json": _canonical_json_bytes(_build_summary(source_commit, records)),
    }


def write_evidence_package(root: Path, files: Mapping[str, bytes]) -> None:
    """Atomically publish one exact, non-overwriting four-file package."""

    if set(files) != set(PACKAGE_FILES):
        raise E5Error("evidence package does not have the exact four-file set")
    if root.exists():
        raise E5Error(f"evidence root already exists: {root}")
    if not root.parent.is_dir():
        raise E5Error(f"evidence parent does not exist: {root.parent}")
    staging = Path(tempfile.mkdtemp(prefix=f".{root.name}.", dir=root.parent))
    try:
        for name in PACKAGE_FILES:
            (staging / name).write_bytes(files[name])
        if root.exists():
            raise E5Error(f"evidence root already exists: {root}")
        os.rename(staging, root)
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def _require_commit(source_commit: str) -> None:
    if not _COMMIT_RE.fullmatch(source_commit):
        raise E5Error("source commit must be 40 lowercase hexadecimal characters")


def _require_handoff(handoff_blob: str) -> None:
    if handoff_blob != HANDOFF_BLOB:
        raise E5Error("handoff blob does not match the embedded E5 contract")


def _output_path(source_commit: str, output_root: str) -> Path:
    expected = f"Phase0/evidence/E5_{source_commit}_qwen3_14b"
    if output_root != expected:
        raise E5Error(f"output root must be the normalized path {expected}")
    return REPO_ROOT / output_root


def _git_output(*arguments: str) -> str:
    completed = subprocess.run(
        ("git", *arguments),
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout.strip()


def _local_ollama_environment() -> Mapping[str, str]:
    environment = dict(os.environ)
    for key in tuple(environment):
        if key.lower() in {
            "http_proxy",
            "https_proxy",
            "all_proxy",
            "no_proxy",
        }:
            del environment[key]
    environment["OLLAMA_HOST"] = ENDPOINT
    return environment


def _ollama_output(*arguments: str) -> bytes:
    completed = subprocess.run(
        ("ollama", *arguments),
        cwd=REPO_ROOT,
        env=_local_ollama_environment(),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _preflight_model() -> None:
    version = _ollama_output("--version").decode("utf-8").strip()
    if version not in {OLLAMA_VERSION, f"ollama version is {OLLAMA_VERSION}"}:
        raise E5Error("Ollama version does not match the frozen binding")

    listing = _ollama_output("list").decode("utf-8").splitlines()
    matches = [line.split() for line in listing if line.split() and line.split()[0] == MODEL]
    if len(matches) != 1 or len(matches[0]) < 2 or matches[0][1] != MODEL_LIST_ID:
        raise E5Error("Ollama model tag/list ID does not match the frozen binding")

    modelfile = _ollama_output("show", MODEL, "--modelfile")
    if hashlib.sha256(modelfile).hexdigest() != MODELFILE_SHA256:
        raise E5Error("Ollama Modelfile checksum does not match the frozen binding")
    from_lines = [
        line.removeprefix("FROM ")
        for line in modelfile.decode("utf-8").splitlines()
        if line.startswith("FROM ")
    ]
    if from_lines != [str(MODEL_BLOB_PATH)]:
        raise E5Error("Ollama Modelfile FROM target does not match the frozen blob")
    try:
        size = MODEL_BLOB_PATH.stat().st_size
    except OSError as error:
        raise E5Error("frozen model blob is unavailable") from error
    if size != MODEL_BLOB_BYTES:
        raise E5Error("model blob size does not match the frozen binding")
    if _sha256_file(MODEL_BLOB_PATH) != MODEL_BLOB_SHA256:
        raise E5Error("model blob checksum does not match the frozen binding")


def _preflight_record(
    source_commit: str,
    handoff_blob: str,
    output_root: str,
) -> Path:
    _require_commit(source_commit)
    _require_handoff(handoff_blob)
    root = _output_path(source_commit, output_root)
    _validate_local_transport_binding()
    if _git_output("rev-parse", "HEAD") != source_commit:
        raise E5Error("source commit does not equal Git HEAD")
    if _git_output("status", "--porcelain", "--untracked-files=all"):
        raise E5Error("worktree or index is not clean")
    if _git_output("hash-object", HANDOFF_PATH) != HANDOFF_BLOB:
        raise E5Error("checked-out handoff blob does not match the accepted contract")
    if root.exists():
        raise E5Error(f"evidence root already exists: {output_root}")
    _preflight_model()
    return root


def record_evidence(
    source_commit: str,
    handoff_blob: str,
    output_root: str,
    transport: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None = None,
) -> Mapping[str, Any]:
    """Perform at most the fixed A/B calls and record one truthful package."""

    requests = build_requests()
    root = _preflight_record(source_commit, handoff_blob, output_root)
    send = _http_transport if transport is None else transport
    responses = []
    for request_id, request_body in zip(REQUEST_IDS, requests, strict=True):
        response = send(request_body)
        _validate_service_envelope(response)
        responses.append(response)
    expected = _read_expected_decision()
    records = [
        _analyze_response(request_id, response, expected)
        for request_id, response in zip(REQUEST_IDS, responses, strict=True)
    ]
    files = _serialize_package(
        source_commit,
        output_root,
        requests,
        records,
    )
    write_evidence_package(root, files)
    return _build_summary(source_commit, records)


def _read_canonical_json(path: Path) -> Any:
    raw = path.read_bytes()
    value = _decode_json(raw, str(path))
    if raw != _canonical_json_bytes(value):
        raise E5Error(f"{path.name} is not canonical JSON")
    return value


def verify_evidence_files(
    source_commit: str,
    output_root: str,
    root: Path,
) -> Mapping[str, Any]:
    """Offline-verify one package and recompute every derived response field."""

    if not root.is_dir():
        raise E5Error(f"missing evidence root: {root}")
    entries = {item.name: item for item in root.iterdir()}
    if set(entries) != set(PACKAGE_FILES) or any(not item.is_file() for item in entries.values()):
        raise E5Error("evidence root has missing, extra, or non-file entries")

    manifest = _read_canonical_json(entries["manifest.json"])
    if manifest != _manifest(source_commit, output_root):
        raise E5Error("manifest does not match the frozen E5 binding")
    requests = build_requests()
    if entries["requests.json"].read_bytes() != _canonical_json_bytes(list(requests)):
        raise E5Error("requests.json does not match the frozen requests")

    response_document = _read_canonical_json(entries["responses.json"])
    response_document = _require_exact_keys(
        response_document,
        {"schema_version", "responses"},
        "responses.json",
    )
    if response_document["schema_version"] != SCHEMA_VERSION:
        raise E5Error("responses.json has the wrong schema version")
    stored_records = response_document["responses"]
    if not isinstance(stored_records, list) or len(stored_records) != 2:
        raise E5Error("responses.json must contain exactly two responses")
    raw_responses = []
    for request_id, record in zip(REQUEST_IDS, stored_records, strict=True):
        record = _require_exact_keys(
            record,
            {
                "request_id",
                "service_response",
                "parsed_decision",
                "validation_error",
                "outcome",
            },
            request_id,
        )
        if record["request_id"] != request_id:
            raise E5Error("response request order changed")
        _validate_service_envelope(record["service_response"])
        raw_responses.append(record["service_response"])

    expected = _read_expected_decision()
    rebuilt_records = [
        _analyze_response(request_id, response, expected)
        for request_id, response in zip(REQUEST_IDS, raw_responses, strict=True)
    ]
    if stored_records != rebuilt_records:
        raise E5Error("responses.json derived fields do not match the raw responses")
    summary = _build_summary(source_commit, rebuilt_records)
    if entries["summary.json"].read_bytes() != _canonical_json_bytes(summary):
        raise E5Error("summary.json does not match the recomputed result")
    return summary


def verify_recorded_evidence(
    source_commit: str,
    handoff_blob: str,
    output_root: str,
) -> Mapping[str, Any]:
    """Offline verification that deliberately does not inspect current Git HEAD."""

    _require_commit(source_commit)
    _require_handoff(handoff_blob)
    root = _output_path(source_commit, output_root)
    return verify_evidence_files(source_commit, output_root, root)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("record", "verify"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--source-commit", required=True)
        subparser.add_argument("--handoff-blob", required=True)
        subparser.add_argument("--output-root", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "record":
            summary = record_evidence(
                arguments.source_commit,
                arguments.handoff_blob,
                arguments.output_root,
            )
        else:
            summary = verify_recorded_evidence(
                arguments.source_commit,
                arguments.handoff_blob,
                arguments.output_root,
            )
    except (E5Error, OSError, subprocess.CalledProcessError) as error:
        parser.error(str(error))
    print(_compact_json(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
