"""Strict, expected-blind loader for Phase 0 E0 fixture inputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from Phase0.implementation.dialect import DIALECT_VERSION, FIXTURE_SCHEMA_VERSION, PREDICATE_BY_ID
from Phase0.implementation.schema import (
    AdapterPayload,
    AdapterSurface,
    AssertionBasis,
    AssertionCommitment,
    CanonicalPayload,
    CanonicalSemanticState,
    ContextAvailability,
    ContextValue,
    CrossConstraint,
    EntryStage,
    ExtractiveContentPayload,
    FixtureInput,
    KnowledgeAssertion,
    Modality,
    NormativeCandidate,
    OpenOwner,
    OpenSlotMention,
    SlotDeclaration,
    SourceEnvelope,
    SourcePayload,
    SourceRole,
    SourceSpan,
    StaticConstraint,
    StrictSchemaError,
    TYPE_VALUE_ORDER,
    TypedValue,
    VisibleWorldContext,
    parse_ref_list,
    parse_term,
    parse_typed_value,
    require_bool,
    require_enum,
    require_exact_keys,
    require_list,
    require_mapping,
    require_string,
)


_DOCUMENT_KEYS = ("fixture_id", "schema_version", "dialect_version", "cases")
_CASE_KEYS = ("case_id", "entry_stage", "input", "expected")
_INPUT_KEYS = (
    "source_envelope",
    "entry_payload",
    "visible_world_context",
    "slot_declarations",
    "static_constraints",
    "cross_constraints",
    "candidate_trajectory_ids",
)
_EXPECTED_KEYS = (
    "canonical_state",
    "elaboration",
    "legal_joint_completions",
    "decision",
    "result",
    "failure",
    "dependency_assertions",
)

__all__ = ("load_fixture_inputs", "load_fixture_input")


def _reject_duplicate_pairs(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise StrictSchemaError(f"duplicate key {key!r}")
        obj[key] = value
    return obj


def _load_raw_document(path: str | Path) -> Mapping[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return require_mapping(json.load(handle, object_pairs_hook=_reject_duplicate_pairs), "document")


def _parse_source_envelope(value: Any, where: str) -> SourceEnvelope | None:
    if value is None:
        return None
    obj = require_mapping(value, where)
    require_exact_keys(obj, ("spans",), where)
    spans = []
    seen: set[str] = set()
    for index, item in enumerate(require_list(obj["spans"], f"{where}.spans")):
        span = require_mapping(item, f"{where}.spans[{index}]")
        require_exact_keys(span, ("ref", "role", "text"), f"{where}.spans[{index}]")
        ref = require_string(span["ref"], f"{where}.spans[{index}].ref")
        if ref in seen:
            raise StrictSchemaError(f"{where}.spans has duplicate ref {ref!r}")
        seen.add(ref)
        spans.append(
            SourceSpan(
                ref=ref,
                role=require_enum(span["role"], SourceRole, f"{where}.spans[{index}].role"),
                text=require_string(span["text"], f"{where}.spans[{index}].text"),
            )
        )
    return SourceEnvelope(spans=tuple(spans))


def _parse_candidate(value: Any, where: str) -> NormativeCandidate:
    obj = require_mapping(value, where)
    require_exact_keys(
        obj,
        ("modality", "predicate", "args", "proposition_support", "claimed_authority_support"),
        where,
    )
    predicate = require_string(obj["predicate"], f"{where}.predicate")
    if predicate not in PREDICATE_BY_ID:
        raise StrictSchemaError(f"{where}.predicate is unknown: {predicate!r}")
    return NormativeCandidate(
        modality=require_enum(obj["modality"], Modality, f"{where}.modality"),
        predicate=predicate,
        args=tuple(parse_term(item, f"{where}.args[{index}]") for index, item in enumerate(require_list(obj["args"], f"{where}.args"))),
        proposition_support=parse_ref_list(obj["proposition_support"], f"{where}.proposition_support"),
        claimed_authority_support=parse_ref_list(obj["claimed_authority_support"], f"{where}.claimed_authority_support"),
    )


def _parse_knowledge_assertion(value: Any, where: str) -> KnowledgeAssertion:
    obj = require_mapping(value, where)
    require_exact_keys(obj, ("predicate", "args", "basis", "commitment", "proposition_support"), where)
    predicate = require_string(obj["predicate"], f"{where}.predicate")
    if predicate not in PREDICATE_BY_ID:
        raise StrictSchemaError(f"{where}.predicate is unknown: {predicate!r}")
    return KnowledgeAssertion(
        predicate=predicate,
        args=tuple(parse_term(item, f"{where}.args[{index}]") for index, item in enumerate(require_list(obj["args"], f"{where}.args"))),
        basis=require_enum(obj["basis"], AssertionBasis, f"{where}.basis"),
        commitment=require_enum(obj["commitment"], AssertionCommitment, f"{where}.commitment"),
        proposition_support=parse_ref_list(obj["proposition_support"], f"{where}.proposition_support"),
    )


def _parse_open_slot_mention(value: Any, where: str) -> OpenSlotMention:
    obj = require_mapping(value, where)
    require_exact_keys(obj, ("type", "owner", "proposition_link", "argument_position", "proposition_support"), where)
    position = obj["argument_position"]
    if not isinstance(position, int) or position < 0:
        raise StrictSchemaError(f"{where}.argument_position must be a nonnegative integer")
    type_id = require_string(obj["type"], f"{where}.type")
    if type_id not in TYPE_VALUE_ORDER:
        raise StrictSchemaError(f"{where}.type has unknown open enum type {type_id!r}")
    return OpenSlotMention(
        type=type_id,
        owner=require_enum(obj["owner"], OpenOwner, f"{where}.owner"),
        proposition_link=require_string(obj["proposition_link"], f"{where}.proposition_link"),
        argument_position=position,
        proposition_support=parse_ref_list(obj["proposition_support"], f"{where}.proposition_support"),
    )


def _parse_canonical_state(value: Any, where: str) -> CanonicalSemanticState:
    obj = require_mapping(value, where)
    require_exact_keys(obj, ("normative_candidates", "knowledge_assertions", "open_slot_mentions"), where)
    return CanonicalSemanticState(
        normative_candidates=tuple(_parse_candidate(item, f"{where}.normative_candidates[{index}]") for index, item in enumerate(require_list(obj["normative_candidates"], f"{where}.normative_candidates"))),
        knowledge_assertions=tuple(_parse_knowledge_assertion(item, f"{where}.knowledge_assertions[{index}]") for index, item in enumerate(require_list(obj["knowledge_assertions"], f"{where}.knowledge_assertions"))),
        open_slot_mentions=tuple(_parse_open_slot_mention(item, f"{where}.open_slot_mentions[{index}]") for index, item in enumerate(require_list(obj["open_slot_mentions"], f"{where}.open_slot_mentions"))),
    )


def _parse_entry_payload(value: Any, where: str):
    obj = require_mapping(value, where)
    kind = require_string(obj.get("kind"), f"{where}.kind")
    if kind == "CANONICAL":
        require_exact_keys(obj, ("kind", "canonical_state"), where)
        return CanonicalPayload(kind=kind, canonical_state=_parse_canonical_state(obj["canonical_state"], f"{where}.canonical_state"))
    if kind == "SOURCE":
        require_exact_keys(obj, ("kind",), where)
        return SourcePayload(kind=kind)
    if kind == "EXTRACTIVE_CONTENT":
        require_exact_keys(obj, ("kind", "content_refs"), where)
        return ExtractiveContentPayload(kind=kind, content_refs=parse_ref_list(obj["content_refs"], f"{where}.content_refs"))
    if kind == "ADAPTER":
        require_exact_keys(obj, ("kind", "adapter_link", "surface"), where)
        if obj["adapter_link"] is not None:
            require_string(obj["adapter_link"], f"{where}.adapter_link")
        surface = require_mapping(obj["surface"], f"{where}.surface")
        require_exact_keys(surface, ("normative_candidates",), f"{where}.surface")
        return AdapterPayload(
            kind=kind,
            adapter_link=obj["adapter_link"],
            surface=AdapterSurface(
                normative_candidates=tuple(_parse_candidate(item, f"{where}.surface.normative_candidates[{index}]") for index, item in enumerate(require_list(surface["normative_candidates"], f"{where}.surface.normative_candidates")))
            ),
        )
    raise StrictSchemaError(f"{where}.kind has unknown payload kind {kind!r}")


def _parse_domain(value: Any, slot_type: str, where: str) -> tuple[TypedValue, ...] | Any:
    if isinstance(value, list):
        domain = tuple(parse_typed_value(item, f"{where}[{index}]") for index, item in enumerate(value))
        for item in domain:
            if item.type != slot_type:
                raise StrictSchemaError(f"{where} contains {item.type!r}, expected {slot_type!r}")
        return domain
    if isinstance(value, (str, int, float, bool, dict)) or value is None:
        return value
    raise StrictSchemaError(f"{where} is an unsupported raw invalid domain")


def _parse_slot_declaration(value: Any, where: str) -> SlotDeclaration:
    obj = require_mapping(value, where)
    require_exact_keys(obj, ("semantic_slot_link", "type", "owner", "schema_domain", "resolved_value"), where)
    type_id = require_string(obj["type"], f"{where}.type")
    if type_id not in TYPE_VALUE_ORDER:
        raise StrictSchemaError(f"{where}.type has unknown slot enum type {type_id!r}")
    domain = _parse_domain(obj["schema_domain"], type_id, f"{where}.schema_domain")
    resolved = None if obj["resolved_value"] is None else parse_typed_value(obj["resolved_value"], f"{where}.resolved_value")
    if resolved is not None and resolved.type != type_id:
        raise StrictSchemaError(f"{where}.resolved_value type mismatch")
    if isinstance(domain, tuple) and resolved is not None and resolved not in domain:
        raise StrictSchemaError(f"{where}.resolved_value is not a domain member")
    return SlotDeclaration(
        semantic_slot_link=require_string(obj["semantic_slot_link"], f"{where}.semantic_slot_link"),
        type=type_id,
        owner=require_enum(obj["owner"], OpenOwner, f"{where}.owner"),
        schema_domain=domain,
        resolved_value=resolved,
    )


def _parse_context_value(value: Any, where: str) -> ContextValue:
    obj = require_mapping(value, where)
    require_exact_keys(obj, ("predicate", "scope", "args", "value"), where)
    predicate = require_string(obj["predicate"], f"{where}.predicate")
    if predicate not in PREDICATE_BY_ID:
        raise StrictSchemaError(f"{where}.predicate is unknown: {predicate!r}")
    return ContextValue(
        predicate=predicate,
        scope=require_enum(obj["scope"], ContextAvailability, f"{where}.scope"),
        args=tuple(parse_typed_value(item, f"{where}.args[{index}]") for index, item in enumerate(require_list(obj["args"], f"{where}.args"))),
        value=require_bool(obj["value"], f"{where}.value"),
    )


def _parse_visible_world_context(value: Any, where: str) -> VisibleWorldContext:
    obj = require_mapping(value, where)
    require_exact_keys(obj, ("entities", "observable_values"), where)
    entities = tuple(require_list(obj["entities"], f"{where}.entities"))
    if entities:
        raise StrictSchemaError(f"{where}.entities must be [] in E0")
    return VisibleWorldContext(
        entities=entities,
        observable_values=tuple(_parse_context_value(item, f"{where}.observable_values[{index}]") for index, item in enumerate(require_list(obj["observable_values"], f"{where}.observable_values"))),
    )


def _parse_static_constraint(value: Any, where: str) -> StaticConstraint:
    obj = require_mapping(value, where)
    require_exact_keys(obj, ("constraint_link", "semantic_slot_link", "candidate_value", "context_predicate", "required_context_value"), where)
    predicate = require_string(obj["context_predicate"], f"{where}.context_predicate")
    if predicate not in PREDICATE_BY_ID:
        raise StrictSchemaError(f"{where}.context_predicate is unknown: {predicate!r}")
    return StaticConstraint(
        constraint_link=require_string(obj["constraint_link"], f"{where}.constraint_link"),
        semantic_slot_link=require_string(obj["semantic_slot_link"], f"{where}.semantic_slot_link"),
        candidate_value=parse_typed_value(obj["candidate_value"], f"{where}.candidate_value"),
        context_predicate=predicate,
        required_context_value=require_bool(obj["required_context_value"], f"{where}.required_context_value"),
    )


def _parse_cross_constraint(value: Any, where: str) -> CrossConstraint:
    obj = require_mapping(value, where)
    require_exact_keys(obj, ("constraint_link", "semantic_slot_links", "allowed_tuples"), where)
    links = tuple(require_string(item, f"{where}.semantic_slot_links[]") for item in require_list(obj["semantic_slot_links"], f"{where}.semantic_slot_links"))
    if len(links) != 2:
        raise StrictSchemaError(f"{where}.semantic_slot_links must have length 2")
    allowed = []
    for tuple_index, raw_tuple in enumerate(require_list(obj["allowed_tuples"], f"{where}.allowed_tuples")):
        items = tuple(parse_typed_value(item, f"{where}.allowed_tuples[{tuple_index}][]") for item in require_list(raw_tuple, f"{where}.allowed_tuples[{tuple_index}]"))
        if len(items) != 2:
            raise StrictSchemaError(f"{where}.allowed_tuples[{tuple_index}] must have length 2")
        allowed.append((items[0], items[1]))
    return CrossConstraint(
        constraint_link=require_string(obj["constraint_link"], f"{where}.constraint_link"),
        semantic_slot_links=(links[0], links[1]),
        allowed_tuples=tuple(allowed),
    )


def _ensure_unique(values: tuple[str, ...], where: str) -> None:
    if len(set(values)) != len(values):
        raise StrictSchemaError(f"{where} has duplicate IDs")


def _parse_input(fixture_id: str, case_id: str, entry_stage: str, value: Any, where: str) -> FixtureInput:
    obj = require_mapping(value, where)
    require_exact_keys(obj, _INPUT_KEYS, where)
    slots = tuple(_parse_slot_declaration(item, f"{where}.slot_declarations[{index}]") for index, item in enumerate(require_list(obj["slot_declarations"], f"{where}.slot_declarations")))
    static_constraints = tuple(_parse_static_constraint(item, f"{where}.static_constraints[{index}]") for index, item in enumerate(require_list(obj["static_constraints"], f"{where}.static_constraints")))
    cross_constraints = tuple(_parse_cross_constraint(item, f"{where}.cross_constraints[{index}]") for index, item in enumerate(require_list(obj["cross_constraints"], f"{where}.cross_constraints")))
    trajectory_ids = tuple(require_string(item, f"{where}.candidate_trajectory_ids[]") for item in require_list(obj["candidate_trajectory_ids"], f"{where}.candidate_trajectory_ids"))
    _ensure_unique(tuple(slot.semantic_slot_link for slot in slots), f"{where}.slot_declarations")
    _ensure_unique(tuple(item.constraint_link for item in static_constraints) + tuple(item.constraint_link for item in cross_constraints), f"{where}.constraints")
    _ensure_unique(trajectory_ids, f"{where}.candidate_trajectory_ids")
    return FixtureInput(
        fixture_id=fixture_id,
        case_id=case_id,
        entry_stage=entry_stage,
        source_envelope=_parse_source_envelope(obj["source_envelope"], f"{where}.source_envelope"),
        entry_payload=_parse_entry_payload(obj["entry_payload"], f"{where}.entry_payload"),
        visible_world_context=_parse_visible_world_context(obj["visible_world_context"], f"{where}.visible_world_context"),
        slot_declarations=slots,
        static_constraints=static_constraints,
        cross_constraints=cross_constraints,
        candidate_trajectory_ids=trajectory_ids,
    )


def load_fixture_inputs(path: str | Path) -> tuple[FixtureInput, ...]:
    """Load all fixture inputs from one E0 JSON file without parsing expected values."""
    document = _load_raw_document(path)
    require_exact_keys(document, _DOCUMENT_KEYS, "document")
    fixture_id = require_string(document["fixture_id"], "document.fixture_id")
    if document["schema_version"] != FIXTURE_SCHEMA_VERSION:
        raise StrictSchemaError("wrong fixture schema version")
    if document["dialect_version"] != DIALECT_VERSION:
        raise StrictSchemaError("wrong dialect version")
    cases = []
    seen_cases: set[str] = set()
    for index, raw_case in enumerate(require_list(document["cases"], "document.cases")):
        case = require_mapping(raw_case, f"document.cases[{index}]")
        require_exact_keys(case, _CASE_KEYS, f"document.cases[{index}]")
        case_id = require_string(case["case_id"], f"document.cases[{index}].case_id")
        if case_id in seen_cases:
            raise StrictSchemaError(f"duplicate case_id {case_id!r}")
        seen_cases.add(case_id)
        entry_stage = require_enum(case["entry_stage"], EntryStage, f"document.cases[{index}].entry_stage")
        expected = require_mapping(case["expected"], f"document.cases[{index}].expected")
        require_exact_keys(expected, _EXPECTED_KEYS, f"document.cases[{index}].expected")
        cases.append(_parse_input(fixture_id, case_id, entry_stage, case["input"], f"document.cases[{index}].input"))
    return tuple(cases)


def load_fixture_input(path: str | Path, case_id: str) -> FixtureInput:
    """Load exactly one fixture input by case ID without exposing expected values."""
    matches = tuple(case for case in load_fixture_inputs(path) if case.case_id == case_id)
    if len(matches) != 1:
        raise StrictSchemaError(f"expected exactly one case_id {case_id!r}, found {len(matches)}")
    return matches[0]
