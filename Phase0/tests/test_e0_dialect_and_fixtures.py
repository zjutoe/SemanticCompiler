"""E0-only checks for the finite dialect, fixture inputs, and test-local expected data."""

from __future__ import annotations

import json
import hashlib
import unittest
from dataclasses import asdict, is_dataclass
from itertools import product
from pathlib import Path
from typing import Any

from Phase0.implementation import dialect
from Phase0.implementation.fixture_loader import load_fixture_input, load_fixture_inputs
from Phase0.implementation.schema import (
    AdapterPayload,
    CanonicalPayload,
    ExtractiveContentPayload,
    OpenTerm,
    SourcePayload,
    TYPE_VALUE_ORDER,
    ValueTerm,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures"
FIXTURE_FILES = (
    "F1_OPEN_UU_COUPLED_MIN_ASK.json",
    "F2_OPEN_UE_OWNER_BOUNDARY.json",
    "F3_EXECUTOR_COVERAGE_NONVACUOUS.json",
    "F4_EXECUTOR_JOINT_TRACE.json",
    "F5_AUTHORITY_ROLE_COUNTERFACTUAL.json",
    "F6_HARD_UNSAT_WITNESS.json",
    "F7_NO_AUTHORIZED_ACTION_WITNESS.json",
    "F8_NO_SILENT_INVALID_EXECUTION.json",
    "F9_C_NORMAL_END_TO_END_EXACT.json",
)
EXPECTED_CASE_IDS = {
    "F1_OPEN_UU_COUPLED_MIN_ASK": ("unresolved",),
    "F2_OPEN_UE_OWNER_BOUNDARY": ("unresolved", "resolved_return_none"),
    "F3_EXECUTOR_COVERAGE_NONVACUOUS": ("unresolved",),
    "F4_EXECUTOR_JOINT_TRACE": ("unresolved",),
    "F5_AUTHORITY_ROLE_COUNTERFACTUAL": ("user_fixed", "assistant_fixed", "tool_fixed", "user_executor_open"),
    "F6_HARD_UNSAT_WITNESS": ("clause_conflict", "static_empty", "cross_empty"),
    "F7_NO_AUTHORIZED_ACTION_WITNESS": ("missing_allow",),
    "F8_NO_SILENT_INVALID_EXECUTION": ("dangling_support", "wrong_enum_type", "missing_adapter_link", "malformed_domain", "declared_empty_domain"),
    "F9_C_NORMAL_END_TO_END_EXACT": ("normal", "gold_c_original", "gold_c_distractor_variant"),
}
DOCUMENT_KEYS = ("fixture_id", "schema_version", "dialect_version", "cases")
CASE_KEYS = ("case_id", "entry_stage", "input", "expected")
INPUT_KEYS = ("source_envelope", "entry_payload", "visible_world_context", "slot_declarations", "static_constraints", "cross_constraints", "candidate_trajectory_ids")
EXPECTED_KEYS = ("canonical_state", "elaboration", "legal_joint_completions", "decision", "result", "failure", "dependency_assertions")
S0 = "slot:clause:000:arg0"
S1 = "slot:clause:000:arg1"
EXPECTED_FIXTURE_SHA256S = {
    "F1_OPEN_UU_COUPLED_MIN_ASK.json": "fb4c6e49c76645cbd4b91735207a98986aa983c4a86a85c08a4a8e23f44d92f3",
    "F2_OPEN_UE_OWNER_BOUNDARY.json": "7864518319a776b256413e8507798a64888bd4efa136c9f1bde1b470ad1e9f81",
    "F3_EXECUTOR_COVERAGE_NONVACUOUS.json": "645e801041a5f8c95f697cf11cb9f7ac729c3cfdef7085fd144f703327ddd8c6",
    "F4_EXECUTOR_JOINT_TRACE.json": "3c8edea79e912af00ea3f073fc2b49e28de30ff1344ccd68dccf3a2946183959",
    "F5_AUTHORITY_ROLE_COUNTERFACTUAL.json": "41a35d35fb991b3ae9634cf005303c22f2d0358361a345c1c81adcc72ac3e9dc",
    "F6_HARD_UNSAT_WITNESS.json": "dc6ccceca0a4eb2a4d9f78a25487d92e0b668726a44ae521b5138ea21433d627",
    "F7_NO_AUTHORIZED_ACTION_WITNESS.json": "78c244fb3e8830c8bc46591826b859e72d773f3ccdbecba6373669d61338f9df",
    "F8_NO_SILENT_INVALID_EXECUTION.json": "8c13656f690e92bd2541b0821c8222d95dc2a391716fb68e5f1c2f4b07d5aedb",
    "F9_C_NORMAL_END_TO_END_EXACT.json": "82204b6ce26d829917d43b88f071864d9b5a21e11e66bef173897f53f39a54fa",
}


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_expected(path: Path) -> dict[str, Any]:
    document = _read_json(path)
    return {case["case_id"]: case["expected"] for case in document["cases"]}


def _freeze(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _freeze(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [_freeze(item) for item in value]
    return value


def _tv(type_id: str, value_id: str) -> dict[str, str]:
    return {"type": type_id, "value": value_id}


def _assignment(*items: tuple[str, dict[str, str]]) -> list[dict[str, Any]]:
    return [{"semantic_slot_link": link, "value": value} for link, value in items]


def _obs(name: str, value: dict[str, str]) -> dict[str, Any]:
    return {"name": name, "value": value}


def _value_term(type_id: str, value_id: str) -> dict[str, Any]:
    return {"kind": "VALUE", "value": _tv(type_id, value_id)}


def _candidate(modality: str, predicate: str, args: list[dict[str, Any]], support: list[str]) -> dict[str, Any]:
    return {
        "modality": modality,
        "predicate": predicate,
        "args": args,
        "proposition_support": support,
        "claimed_authority_support": support,
    }


def _canonical(*candidates: dict[str, Any]) -> dict[str, Any]:
    return {"normative_candidates": list(candidates), "knowledge_assertions": [], "open_slot_mentions": []}


def _validate_typed_value(value: Any) -> None:
    assert tuple(value.keys()) == ("type", "value")
    assert value["type"] in TYPE_VALUE_ORDER
    assert value["value"] in TYPE_VALUE_ORDER[value["type"]]


def _validate_assignment(value: Any) -> None:
    assert isinstance(value, list)
    for item in value:
        assert tuple(item.keys()) == ("semantic_slot_link", "value")
        assert isinstance(item["semantic_slot_link"], str)
        _validate_typed_value(item["value"])


def _validate_source_span_shape(value: Any) -> None:
    assert tuple(value.keys()) == ("ref", "role", "text")
    assert isinstance(value["ref"], str)
    assert value["role"] in ("USER", "ASSISTANT", "TOOL")
    assert isinstance(value["text"], str)


def _validate_elaboration_shape(value: Any) -> None:
    assert tuple(value.keys()) == ("candidates", "active_clause_links", "knowledge_assertions", "open_slots", "slot_domains", "constraint_links")
    for candidate in value["candidates"]:
        assert tuple(candidate.keys()) == ("clause_link", "authority", "active")
        assert isinstance(candidate["clause_link"], str)
        assert candidate["authority"] in ("USER", "NONE")
        assert isinstance(candidate["active"], bool)
    assert all(isinstance(item, str) for item in value["active_clause_links"])
    assert value["knowledge_assertions"] == []
    for slot in value["open_slots"]:
        assert tuple(slot.keys()) == ("semantic_slot_link", "type", "owner", "resolved_value")
        assert isinstance(slot["semantic_slot_link"], str)
        assert slot["type"] in TYPE_VALUE_ORDER
        assert slot["owner"] in ("USER", "EXECUTOR")
        if slot["resolved_value"] is not None:
            _validate_typed_value(slot["resolved_value"])
    for domain in value["slot_domains"]:
        assert tuple(domain.keys()) == ("semantic_slot_link", "values")
        assert isinstance(domain["semantic_slot_link"], str)
        assert isinstance(domain["values"], list)
        for item in domain["values"]:
            _validate_typed_value(item)
    assert all(isinstance(item, str) for item in value["constraint_links"])


def _validate_witness_shape(value: Any) -> None:
    kind = value["kind"]
    if kind == "ClauseConflictWitness":
        assert tuple(value.keys()) == ("kind", "clause_links")
        assert all(isinstance(item, str) for item in value["clause_links"])
    elif kind == "EmptyDomainWitness":
        assert tuple(value.keys()) == ("kind", "semantic_slot_link", "excluding_constraint_links")
        assert isinstance(value["semantic_slot_link"], str)
        assert all(isinstance(item, str) for item in value["excluding_constraint_links"])
    elif kind == "CrossConstraintWitness":
        assert tuple(value.keys()) == ("kind", "cross_constraint_links")
        assert all(isinstance(item, str) for item in value["cross_constraint_links"])
    elif kind == "NoAuthorizedActionWitness":
        assert tuple(value.keys()) == ("kind", "excluded_actions")
        for action in value["excluded_actions"]:
            assert tuple(action.keys()) == ("action_id", "unauthorized_managed_effects")
            assert isinstance(action["action_id"], str)
            assert all(effect in dialect.MANAGED_EFFECTS for effect in action["unauthorized_managed_effects"])
    else:
        raise AssertionError(value)


def _validate_decision_shape(value: Any) -> None:
    if value["kind"] == "ASK":
        assert tuple(value.keys()) == ("kind", "semantic_slot_links")
        assert all(isinstance(item, str) for item in value["semantic_slot_links"])
    elif value["kind"] == "EXECUTE":
        assert tuple(value.keys()) == ("kind", "action_id", "executor_resolutions")
        assert isinstance(value["action_id"], str)
        _validate_assignment(value["executor_resolutions"])
    elif value["kind"] == "REJECT":
        assert tuple(value.keys()) == ("kind", "reason", "witness", "executor_resolutions")
        assert value["reason"] in ("HARD_UNSAT", "NO_AUTHORIZED_ACTION")
        _validate_witness_shape(value["witness"])
        _validate_assignment(value["executor_resolutions"])
    else:
        raise AssertionError(value)


def _validate_result_shape(value: Any) -> None:
    assert tuple(value.keys()) == ("kind", "action_id", "final_observables", "ordered_effects")
    assert value["kind"] == "EXECUTED"
    assert isinstance(value["action_id"], str)
    assert tuple(value["final_observables"].keys()) == ("format",)
    _validate_typed_value(value["final_observables"]["format"])
    assert all(effect in dialect.MANAGED_EFFECTS for effect in value["ordered_effects"])


def _validate_dependency_assertions_shape(value: Any) -> None:
    assert tuple(value.keys()) == ("normal_content_refs", "referenced_support_view", "canonical_equals_case")
    assert all(isinstance(item, str) for item in value["normal_content_refs"])
    for span in value["referenced_support_view"]:
        _validate_source_span_shape(span)
    assert value["canonical_equals_case"] is None or isinstance(value["canonical_equals_case"], str)


def _validate_expected_shape(expected: dict[str, Any]) -> None:
    assert tuple(expected.keys()) == EXPECTED_KEYS
    if expected["canonical_state"] is not None:
        _validate_canonical_state_shape(expected["canonical_state"])
    if expected["elaboration"] is not None:
        _validate_elaboration_shape(expected["elaboration"])
    if expected["legal_joint_completions"] is not None:
        assert isinstance(expected["legal_joint_completions"], list)
        for assignment in expected["legal_joint_completions"]:
            _validate_assignment(assignment)
    decision = expected["decision"]
    if decision is not None:
        _validate_decision_shape(decision)
    if expected["result"] is not None:
        _validate_result_shape(expected["result"])
    if expected["failure"] is not None:
        assert tuple(expected["failure"].keys()) == ("stage", "reason")
        assert isinstance(expected["failure"]["stage"], str)
        assert isinstance(expected["failure"]["reason"], str)
    if expected["dependency_assertions"] is not None:
        _validate_dependency_assertions_shape(expected["dependency_assertions"])


def _validate_canonical_state_shape(state: dict[str, Any]) -> None:
    assert tuple(state.keys()) == ("normative_candidates", "knowledge_assertions", "open_slot_mentions")
    for candidate in state["normative_candidates"]:
        assert tuple(candidate.keys()) == ("modality", "predicate", "args", "proposition_support", "claimed_authority_support")
        for term in candidate["args"]:
            if term["kind"] == "VALUE":
                assert tuple(term.keys()) == ("kind", "value")
                _validate_typed_value(term["value"])
            elif term["kind"] == "OPEN":
                assert tuple(term.keys()) == ("kind", "type", "semantic_slot_link")
            else:
                raise AssertionError(term)
    for mention in state["open_slot_mentions"]:
        assert tuple(mention.keys()) == ("type", "owner", "proposition_link", "argument_position", "proposition_support")
        assert mention["type"] in TYPE_VALUE_ORDER
        assert mention["owner"] in ("USER", "EXECUTOR")
        assert isinstance(mention["proposition_link"], str)
        assert isinstance(mention["argument_position"], int)
        assert all(isinstance(item, str) for item in mention["proposition_support"])


def _slot_domains(case_input) -> dict[str, list[dict[str, str]]]:
    domains: dict[str, list[dict[str, str]]] = {}
    for slot in case_input.slot_declarations:
        if isinstance(slot.schema_domain, tuple):
            domains[slot.semantic_slot_link] = [_freeze(value) for value in slot.schema_domain]
        else:
            domains[slot.semantic_slot_link] = []
        if slot.resolved_value is not None:
            domains[slot.semantic_slot_link] = [_freeze(slot.resolved_value)]
    context = {
        (item.predicate, tuple((arg.type, arg.value) for arg in item.args)): item.value
        for item in case_input.visible_world_context.observable_values
    }
    for constraint in case_input.static_constraints:
        key = (constraint.context_predicate, ((constraint.candidate_value.type, constraint.candidate_value.value),))
        if context.get(key) != constraint.required_context_value:
            candidate = _freeze(constraint.candidate_value)
            domains[constraint.semantic_slot_link] = [value for value in domains[constraint.semantic_slot_link] if value != candidate]
    return domains


def _oracle_legal_completions(case_input) -> list[list[dict[str, Any]]]:
    slot_links = sorted((slot.semantic_slot_link for slot in case_input.slot_declarations))
    if not slot_links:
        return [[]]
    domains = _slot_domains(case_input)
    completions = []
    for values in product(*(domains[link] for link in slot_links)):
        assignment = dict(zip(slot_links, values))
        allowed = True
        for constraint in case_input.cross_constraints:
            pair = tuple(assignment[link] for link in constraint.semantic_slot_links)
            allowed_pairs = tuple(tuple(_freeze(value) for value in pair_values) for pair_values in constraint.allowed_tuples)
            if pair not in allowed_pairs:
                allowed = False
                break
        if allowed:
            completions.append(_assignment(*tuple((link, assignment[link]) for link in slot_links)))
    return completions


EXPECTED_TRAJECTORIES = [
    {"trajectory_id": "tau:f1:json_strict", "action_id": "f1_render_json_strict", "assignment": _assignment((S0, _tv("OutputFormat", "JSON")), (S1, _tv("Strictness", "STRICT"))), "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "JSON")), _obs("strictness", _tv("Strictness", "STRICT"))], "ordered_effects": []},
    {"trajectory_id": "tau:f1:yaml_lenient", "action_id": "f1_render_yaml_lenient", "assignment": _assignment((S0, _tv("OutputFormat", "YAML")), (S1, _tv("Strictness", "LENIENT"))), "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "YAML")), _obs("strictness", _tv("Strictness", "LENIENT"))], "ordered_effects": []},
    {"trajectory_id": "tau:f2:return_none_quiet", "action_id": "f2_return_none_quiet", "assignment": _assignment((S0, _tv("ErrorPolicy", "RETURN_NONE")), (S1, _tv("LogMode", "QUIET"))), "initial_observables": [], "final_observables": [_obs("error_policy", _tv("ErrorPolicy", "RETURN_NONE")), _obs("log_mode", _tv("LogMode", "QUIET"))], "ordered_effects": []},
    {"trajectory_id": "tau:f2:raise_verbose", "action_id": "f2_raise_verbose", "assignment": _assignment((S0, _tv("ErrorPolicy", "RAISE")), (S1, _tv("LogMode", "VERBOSE"))), "initial_observables": [], "final_observables": [_obs("error_policy", _tv("ErrorPolicy", "RAISE")), _obs("log_mode", _tv("LogMode", "VERBOSE"))], "ordered_effects": []},
    {"trajectory_id": "tau:f3:safe_local", "action_id": "f3_use_local", "assignment": _assignment((S0, _tv("ServiceMode", "SAFE")), (S1, _tv("Backend", "LOCAL"))), "initial_observables": [], "final_observables": [_obs("service_mode", _tv("ServiceMode", "SAFE")), _obs("backend", _tv("Backend", "LOCAL"))], "ordered_effects": []},
    {"trajectory_id": "tau:f3:fast_local", "action_id": "f3_use_local", "assignment": _assignment((S0, _tv("ServiceMode", "FAST")), (S1, _tv("Backend", "LOCAL"))), "initial_observables": [], "final_observables": [_obs("service_mode", _tv("ServiceMode", "FAST")), _obs("backend", _tv("Backend", "LOCAL"))], "ordered_effects": []},
    {"trajectory_id": "tau:f3:fast_remote", "action_id": "f3_use_remote", "assignment": _assignment((S0, _tv("ServiceMode", "FAST")), (S1, _tv("Backend", "REMOTE"))), "initial_observables": [], "final_observables": [_obs("service_mode", _tv("ServiceMode", "FAST")), _obs("backend", _tv("Backend", "REMOTE"))], "ordered_effects": []},
    {"trajectory_id": "tau:f4:yaml_lenient", "action_id": "f4_a_yaml_lenient", "assignment": _assignment((S0, _tv("OutputFormat", "YAML")), (S1, _tv("Strictness", "LENIENT"))), "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "YAML")), _obs("strictness", _tv("Strictness", "LENIENT"))], "ordered_effects": []},
    {"trajectory_id": "tau:f4:json_strict", "action_id": "f4_b_json_strict", "assignment": _assignment((S0, _tv("OutputFormat", "JSON")), (S1, _tv("Strictness", "STRICT"))), "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "JSON")), _obs("strictness", _tv("Strictness", "STRICT"))], "ordered_effects": []},
    {"trajectory_id": "tau:f5:fixed_yaml", "action_id": "f5_a_yaml", "assignment": [], "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "YAML"))], "ordered_effects": []},
    {"trajectory_id": "tau:f5:fixed_json", "action_id": "f5_b_json", "assignment": [], "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "JSON"))], "ordered_effects": []},
    {"trajectory_id": "tau:f5:open_yaml", "action_id": "f5_a_yaml", "assignment": _assignment((S0, _tv("OutputFormat", "YAML"))), "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "YAML"))], "ordered_effects": []},
    {"trajectory_id": "tau:f5:open_json", "action_id": "f5_b_json", "assignment": _assignment((S0, _tv("OutputFormat", "JSON"))), "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "JSON"))], "ordered_effects": []},
    {"trajectory_id": "tau:f6:json", "action_id": "f6_render_json", "assignment": [], "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "JSON"))], "ordered_effects": []},
    {"trajectory_id": "tau:f6:yaml", "action_id": "f6_render_yaml", "assignment": [], "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "YAML"))], "ordered_effects": []},
    {"trajectory_id": "tau:f7:write_json", "action_id": "f7_write_json", "assignment": [], "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "JSON"))], "ordered_effects": ["WRITE_OUTPUT"]},
    {"trajectory_id": "tau:f9:write_json", "action_id": "write_json", "assignment": [], "initial_observables": [_obs("format", _tv("OutputFormat", "UNSET"))], "final_observables": [_obs("format", _tv("OutputFormat", "JSON"))], "ordered_effects": ["WRITE_OUTPUT"]},
]
EXPECTED_DECISIONS = {
    ("F1_OPEN_UU_COUPLED_MIN_ASK", "unresolved"): {"kind": "ASK", "semantic_slot_links": [S0]},
    ("F2_OPEN_UE_OWNER_BOUNDARY", "unresolved"): {"kind": "ASK", "semantic_slot_links": [S0]},
    ("F2_OPEN_UE_OWNER_BOUNDARY", "resolved_return_none"): {"kind": "EXECUTE", "action_id": "f2_return_none_quiet", "executor_resolutions": _assignment((S1, _tv("LogMode", "QUIET")))},
    ("F3_EXECUTOR_COVERAGE_NONVACUOUS", "unresolved"): {"kind": "EXECUTE", "action_id": "f3_use_local", "executor_resolutions": _assignment((S1, _tv("Backend", "LOCAL")))},
    ("F4_EXECUTOR_JOINT_TRACE", "unresolved"): {"kind": "EXECUTE", "action_id": "f4_b_json_strict", "executor_resolutions": _assignment((S0, _tv("OutputFormat", "JSON")), (S1, _tv("Strictness", "STRICT")))},
    ("F5_AUTHORITY_ROLE_COUNTERFACTUAL", "user_fixed"): {"kind": "EXECUTE", "action_id": "f5_b_json", "executor_resolutions": []},
    ("F5_AUTHORITY_ROLE_COUNTERFACTUAL", "assistant_fixed"): {"kind": "EXECUTE", "action_id": "f5_a_yaml", "executor_resolutions": []},
    ("F5_AUTHORITY_ROLE_COUNTERFACTUAL", "tool_fixed"): {"kind": "EXECUTE", "action_id": "f5_a_yaml", "executor_resolutions": []},
    ("F5_AUTHORITY_ROLE_COUNTERFACTUAL", "user_executor_open"): {"kind": "EXECUTE", "action_id": "f5_a_yaml", "executor_resolutions": _assignment((S0, _tv("OutputFormat", "YAML")))},
    ("F6_HARD_UNSAT_WITNESS", "clause_conflict"): {"kind": "REJECT", "reason": "HARD_UNSAT", "witness": {"kind": "ClauseConflictWitness", "clause_links": ["clause:000", "clause:001"]}, "executor_resolutions": []},
    ("F6_HARD_UNSAT_WITNESS", "static_empty"): {"kind": "REJECT", "reason": "HARD_UNSAT", "witness": {"kind": "EmptyDomainWitness", "semantic_slot_link": S0, "excluding_constraint_links": ["constraint:f6:format_not_json", "constraint:f6:format_not_yaml"]}, "executor_resolutions": []},
    ("F6_HARD_UNSAT_WITNESS", "cross_empty"): {"kind": "REJECT", "reason": "HARD_UNSAT", "witness": {"kind": "CrossConstraintWitness", "cross_constraint_links": ["constraint:f6:no_output_policy_pair"]}, "executor_resolutions": []},
    ("F7_NO_AUTHORIZED_ACTION_WITNESS", "missing_allow"): {"kind": "REJECT", "reason": "NO_AUTHORIZED_ACTION", "witness": {"kind": "NoAuthorizedActionWitness", "excluded_actions": [{"action_id": "f7_write_json", "unauthorized_managed_effects": ["WRITE_OUTPUT"]}]}, "executor_resolutions": []},
    ("F8_NO_SILENT_INVALID_EXECUTION", "dangling_support"): None,
    ("F8_NO_SILENT_INVALID_EXECUTION", "wrong_enum_type"): None,
    ("F8_NO_SILENT_INVALID_EXECUTION", "missing_adapter_link"): None,
    ("F8_NO_SILENT_INVALID_EXECUTION", "malformed_domain"): None,
    ("F8_NO_SILENT_INVALID_EXECUTION", "declared_empty_domain"): None,
    ("F9_C_NORMAL_END_TO_END_EXACT", "normal"): {"kind": "EXECUTE", "action_id": "write_json", "executor_resolutions": []},
    ("F9_C_NORMAL_END_TO_END_EXACT", "gold_c_original"): {"kind": "EXECUTE", "action_id": "write_json", "executor_resolutions": []},
    ("F9_C_NORMAL_END_TO_END_EXACT", "gold_c_distractor_variant"): {"kind": "EXECUTE", "action_id": "write_json", "executor_resolutions": []},
}
EXPECTED_FAILURES = {
    ("F8_NO_SILENT_INVALID_EXECUTION", "dangling_support"): {"stage": "elaboration", "reason": "DANGLING_SUPPORT_REF"},
    ("F8_NO_SILENT_INVALID_EXECUTION", "wrong_enum_type"): {"stage": "elaboration", "reason": "TYPE_MISMATCH"},
    ("F8_NO_SILENT_INVALID_EXECUTION", "missing_adapter_link"): {"stage": "adapter_or_bridge", "reason": "MISSING_ADAPTER_LINK"},
    ("F8_NO_SILENT_INVALID_EXECUTION", "malformed_domain"): {"stage": "elaboration", "reason": "MALFORMED_DOMAIN_DECLARATION"},
    ("F8_NO_SILENT_INVALID_EXECUTION", "declared_empty_domain"): {"stage": "elaboration", "reason": "DECLARED_EMPTY_DOMAIN"},
}
EXPECTED_WRITE_JSON_RESULT = {"kind": "EXECUTED", "action_id": "write_json", "final_observables": {"format": _tv("OutputFormat", "JSON")}, "ordered_effects": ["WRITE_OUTPUT"]}
EXPECTED_F9_DEPENDENCIES = {
    "normal": {"normal_content_refs": ["u1", "u2", "a1"], "referenced_support_view": [{"ref": "u1", "role": "USER", "text": "Require final format JSON."}, {"ref": "u2", "role": "USER", "text": "Allow managed effect WRITE_OUTPUT."}, {"ref": "a1", "role": "ASSISTANT", "text": "Use YAML."}], "canonical_equals_case": None},
    "gold_c_original": {"normal_content_refs": [], "referenced_support_view": [{"ref": "u1", "role": "USER", "text": "Require final format JSON."}, {"ref": "u2", "role": "USER", "text": "Allow managed effect WRITE_OUTPUT."}], "canonical_equals_case": None},
    "gold_c_distractor_variant": {"normal_content_refs": [], "referenced_support_view": [{"ref": "u1", "role": "USER", "text": "Require final format JSON."}, {"ref": "u2", "role": "USER", "text": "Allow managed effect WRITE_OUTPUT."}], "canonical_equals_case": "gold_c_original"},
}
EXPECTED_F9_CANONICAL = {
    "normal": _canonical(
        _candidate("REQUIRE", "world.final_format_is", [_value_term("OutputFormat", "JSON")], ["u1"]),
        _candidate("ALLOW", "effect.WRITE_OUTPUT", [], ["u2"]),
        _candidate("REQUIRE", "world.final_format_is", [_value_term("OutputFormat", "YAML")], ["a1"]),
    ),
    "gold_c_original": _canonical(
        _candidate("REQUIRE", "world.final_format_is", [_value_term("OutputFormat", "JSON")], ["u1"]),
        _candidate("ALLOW", "effect.WRITE_OUTPUT", [], ["u2"]),
    ),
    "gold_c_distractor_variant": _canonical(
        _candidate("REQUIRE", "world.final_format_is", [_value_term("OutputFormat", "JSON")], ["u1"]),
        _candidate("ALLOW", "effect.WRITE_OUTPUT", [], ["u2"]),
    ),
}
EXPECTED_ELABORATION_CANDIDATES = {
    ("F1_OPEN_UU_COUPLED_MIN_ASK", "unresolved"): [("clause:000", "USER", True)],
    ("F2_OPEN_UE_OWNER_BOUNDARY", "unresolved"): [("clause:000", "USER", True)],
    ("F2_OPEN_UE_OWNER_BOUNDARY", "resolved_return_none"): [("clause:000", "USER", True)],
    ("F3_EXECUTOR_COVERAGE_NONVACUOUS", "unresolved"): [("clause:000", "USER", True)],
    ("F4_EXECUTOR_JOINT_TRACE", "unresolved"): [("clause:000", "USER", True), ("clause:001", "USER", True)],
    ("F5_AUTHORITY_ROLE_COUNTERFACTUAL", "user_fixed"): [("clause:000", "USER", True)],
    ("F5_AUTHORITY_ROLE_COUNTERFACTUAL", "assistant_fixed"): [("clause:000", "NONE", False)],
    ("F5_AUTHORITY_ROLE_COUNTERFACTUAL", "tool_fixed"): [("clause:000", "NONE", False)],
    ("F5_AUTHORITY_ROLE_COUNTERFACTUAL", "user_executor_open"): [("clause:000", "USER", True)],
    ("F6_HARD_UNSAT_WITNESS", "clause_conflict"): [("clause:000", "USER", True), ("clause:001", "USER", True)],
    ("F6_HARD_UNSAT_WITNESS", "static_empty"): [("clause:000", "USER", True)],
    ("F6_HARD_UNSAT_WITNESS", "cross_empty"): [("clause:000", "USER", True)],
    ("F7_NO_AUTHORIZED_ACTION_WITNESS", "missing_allow"): [("clause:000", "USER", True)],
    ("F9_C_NORMAL_END_TO_END_EXACT", "normal"): [("clause:000", "USER", True), ("clause:001", "USER", True), ("clause:002", "NONE", False)],
    ("F9_C_NORMAL_END_TO_END_EXACT", "gold_c_original"): [("clause:000", "USER", True), ("clause:001", "USER", True)],
    ("F9_C_NORMAL_END_TO_END_EXACT", "gold_c_distractor_variant"): [("clause:000", "USER", True), ("clause:001", "USER", True)],
}


class E0DialectAndFixturesTest(unittest.TestCase):
    maxDiff = None

    def test_manifest_versions_enums_predicates_and_effects_are_exact(self) -> None:
        self.assertEqual(dialect.FIXTURE_SCHEMA_VERSION, "phase0.e0.v1")
        self.assertEqual(dialect.DIALECT_VERSION, "contract-ir.phase0.v0")
        self.assertEqual(dialect.MANAGED_EFFECTS, ("WRITE_OUTPUT",))
        self.assertEqual(tuple(dialect.PREDICATE_BY_ID), tuple(item.predicate for item in dialect.PREDICATES))
        self.assertEqual(
            [(item.predicate, item.signature, item.scope) for item in dialect.PREDICATES],
            [
                ("world.final_format_is", ("OutputFormat",), "FINAL"),
                ("world.output_policy_is", ("OutputFormat", "Strictness"), "FINAL"),
                ("world.error_handling_is", ("ErrorPolicy", "LogMode"), "FINAL"),
                ("world.service_route_is", ("ServiceMode", "Backend"), "FINAL"),
                ("world.format_supported", ("OutputFormat",), "INITIAL"),
                ("effect.WRITE_OUTPUT", (), "EVENT"),
            ],
        )
        self.assertEqual(TYPE_VALUE_ORDER["OutputFormat"], ("UNSET", "JSON", "YAML"))
        self.assertEqual(TYPE_VALUE_ORDER["Strictness"], ("STRICT", "LENIENT"))
        self.assertEqual(TYPE_VALUE_ORDER["ErrorPolicy"], ("RETURN_NONE", "RAISE"))
        self.assertEqual(TYPE_VALUE_ORDER["LogMode"], ("QUIET", "VERBOSE"))
        self.assertEqual(TYPE_VALUE_ORDER["ServiceMode"], ("SAFE", "FAST"))
        self.assertEqual(TYPE_VALUE_ORDER["Backend"], ("LOCAL", "REMOTE"))

    def test_trajectory_catalog_is_exact_and_only_f7_f9_emit_write_output(self) -> None:
        self.assertEqual([_freeze(item) for item in dialect.TRAJECTORIES], EXPECTED_TRAJECTORIES)
        self.assertEqual(tuple(dialect.TRAJECTORIES_BY_ID), tuple(item["trajectory_id"] for item in EXPECTED_TRAJECTORIES))
        effectful = [item.trajectory_id for item in dialect.TRAJECTORIES if item.ordered_effects]
        self.assertEqual(effectful, ["tau:f7:write_json", "tau:f9:write_json"])

    def test_fixture_documents_have_exact_catalog_and_strict_envelope(self) -> None:
        found_fixture_ids = []
        for file_name in FIXTURE_FILES:
            document = _read_json(FIXTURE_DIR / file_name)
            self.assertEqual(tuple(document.keys()), DOCUMENT_KEYS)
            fixture_id = document["fixture_id"]
            found_fixture_ids.append(fixture_id)
            self.assertEqual(document["schema_version"], "phase0.e0.v1")
            self.assertEqual(document["dialect_version"], "contract-ir.phase0.v0")
            self.assertEqual(tuple(case["case_id"] for case in document["cases"]), EXPECTED_CASE_IDS[fixture_id])
            for case in document["cases"]:
                self.assertEqual(tuple(case.keys()), CASE_KEYS)
                self.assertEqual(tuple(case["input"].keys()), INPUT_KEYS)
                _validate_expected_shape(case["expected"])
        self.assertEqual(tuple(found_fixture_ids), tuple(EXPECTED_CASE_IDS))

    def test_fixture_files_are_byte_exact(self) -> None:
        self.assertEqual(tuple(EXPECTED_FIXTURE_SHA256S), FIXTURE_FILES)
        for file_name in FIXTURE_FILES:
            data = (FIXTURE_DIR / file_name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), EXPECTED_FIXTURE_SHA256S[file_name])

    def test_loader_is_expected_blind_and_loads_all_cases_losslessly(self) -> None:
        total = 0
        for file_name in FIXTURE_FILES:
            path = FIXTURE_DIR / file_name
            document = _read_json(path)
            cases = load_fixture_inputs(path)
            self.assertEqual(tuple(case.case_id for case in cases), tuple(case["case_id"] for case in document["cases"]))
            for loaded, raw_case in zip(cases, document["cases"], strict=True):
                self.assertFalse(hasattr(loaded, "expected"))
                self.assertEqual(loaded.fixture_id, document["fixture_id"])
                self.assertEqual(loaded.case_id, raw_case["case_id"])
                self.assertEqual(loaded.entry_stage, raw_case["entry_stage"])
                selected = load_fixture_input(path, loaded.case_id)
                self.assertEqual(selected, loaded)
            total += len(cases)
        self.assertEqual(total, 21)

    def test_canonical_open_mentions_are_exhaustive_and_linked(self) -> None:
        for file_name in FIXTURE_FILES:
            for case in load_fixture_inputs(FIXTURE_DIR / file_name):
                if not isinstance(case.entry_payload, CanonicalPayload):
                    continue
                state = case.entry_payload.canonical_state
                mentions = {
                    (mention.proposition_link, mention.argument_position): mention
                    for mention in state.open_slot_mentions
                }
                expected_mentions = {}
                for candidate_index, candidate in enumerate(state.normative_candidates):
                    clause_link = f"clause:{candidate_index:03d}"
                    for arg_index, term in enumerate(candidate.args):
                        if isinstance(term, OpenTerm):
                            self.assertEqual(term.semantic_slot_link, f"slot:{clause_link}:arg{arg_index}")
                            expected_mentions[(clause_link, arg_index)] = (term.type, candidate.proposition_support)
                        elif isinstance(term, ValueTerm):
                            continue
                        else:
                            self.fail(term)
                self.assertEqual(set(mentions), set(expected_mentions))
                slot_by_link = {slot.semantic_slot_link: slot for slot in case.slot_declarations}
                for (clause_link, arg_index), (type_id, support) in expected_mentions.items():
                    mention = mentions[(clause_link, arg_index)]
                    slot = slot_by_link[f"slot:{clause_link}:arg{arg_index}"]
                    self.assertEqual((mention.type, mention.owner, mention.proposition_support), (type_id, slot.owner, support))

    def test_test_local_expected_legal_completions_match_fixture_constraints(self) -> None:
        for file_name in FIXTURE_FILES:
            expected_by_case = _read_expected(FIXTURE_DIR / file_name)
            for case in load_fixture_inputs(FIXTURE_DIR / file_name):
                expected = expected_by_case[case.case_id]
                if expected["legal_joint_completions"] is None:
                    continue
                self.assertEqual(expected["legal_joint_completions"], _oracle_legal_completions(case), (case.fixture_id, case.case_id))

    def test_exact_expected_case_contracts_are_frozen(self) -> None:
        seen_keys = []
        for file_name in FIXTURE_FILES:
            document = _read_json(FIXTURE_DIR / file_name)
            for case in document["cases"]:
                key = (document["fixture_id"], case["case_id"])
                expected = case["expected"]
                seen_keys.append(key)
                self.assertEqual(expected["decision"], EXPECTED_DECISIONS[key], key)
                self.assertEqual(expected["failure"], EXPECTED_FAILURES.get(key), key)
                self.assertEqual(expected["result"], EXPECTED_WRITE_JSON_RESULT if key[0] == "F9_C_NORMAL_END_TO_END_EXACT" else None, key)
                self.assertEqual(expected["dependency_assertions"], EXPECTED_F9_DEPENDENCIES.get(key[1]) if key[0] == "F9_C_NORMAL_END_TO_END_EXACT" else None, key)
                if key[0] == "F9_C_NORMAL_END_TO_END_EXACT":
                    self.assertEqual(expected["canonical_state"], EXPECTED_F9_CANONICAL[key[1]], key)
                else:
                    self.assertIsNone(expected["canonical_state"], key)
                if key[0] == "F8_NO_SILENT_INVALID_EXECUTION":
                    self.assertIsNone(expected["elaboration"], key)
                    self.assertIsNone(expected["legal_joint_completions"], key)
                else:
                    actual_candidates = [
                        (item["clause_link"], item["authority"], item["active"])
                        for item in expected["elaboration"]["candidates"]
                    ]
                    self.assertEqual(actual_candidates, EXPECTED_ELABORATION_CANDIDATES[key], key)
        self.assertEqual(tuple(seen_keys), tuple(EXPECTED_DECISIONS))
        self.assertEqual(set(EXPECTED_FAILURES), {key for key in seen_keys if key[0] == "F8_NO_SILENT_INVALID_EXECUTION"})

    def test_f8_invalid_inputs_are_preserved_without_execution_or_expected_exposure(self) -> None:
        path = FIXTURE_DIR / "F8_NO_SILENT_INVALID_EXECUTION.json"
        cases = {case.case_id: case for case in load_fixture_inputs(path)}
        expected = _read_expected(path)
        self.assertEqual(cases["dangling_support"].entry_payload.canonical_state.normative_candidates[0].proposition_support, ("missing_ref",))
        wrong_term = cases["wrong_enum_type"].entry_payload.canonical_state.normative_candidates[0].args[0]
        self.assertEqual((wrong_term.value.type, wrong_term.value.value), ("Strictness", "STRICT"))
        self.assertIsInstance(cases["missing_adapter_link"].entry_payload, AdapterPayload)
        self.assertIsNone(cases["missing_adapter_link"].entry_payload.adapter_link)
        self.assertEqual(cases["malformed_domain"].slot_declarations[0].schema_domain, "JSON,YAML")
        self.assertEqual(cases["declared_empty_domain"].slot_declarations[0].schema_domain, ())
        self.assertEqual([expected[case_id]["failure"]["reason"] for case_id in EXPECTED_CASE_IDS["F8_NO_SILENT_INVALID_EXECUTION"]], ["DANGLING_SUPPORT_REF", "TYPE_MISMATCH", "MISSING_ADAPTER_LINK", "MALFORMED_DOMAIN_DECLARATION", "DECLARED_EMPTY_DOMAIN"])
        for case in cases.values():
            self.assertEqual(case.candidate_trajectory_ids, ())

    def test_f9_source_and_gold_c_expected_values_are_exact_and_isolated(self) -> None:
        path = FIXTURE_DIR / "F9_C_NORMAL_END_TO_END_EXACT.json"
        cases = {case.case_id: case for case in load_fixture_inputs(path)}
        self.assertIsInstance(cases["normal"].entry_payload, SourcePayload)
        self.assertIsInstance(cases["gold_c_original"].entry_payload, ExtractiveContentPayload)
        self.assertEqual(cases["gold_c_original"].entry_payload.content_refs, ("u1", "u2"))
        expected = _read_expected(path)
        self.assertEqual(expected["normal"]["dependency_assertions"]["normal_content_refs"], ["u1", "u2", "a1"])
        self.assertEqual(expected["gold_c_original"]["dependency_assertions"]["referenced_support_view"], expected["gold_c_distractor_variant"]["dependency_assertions"]["referenced_support_view"])
        self.assertEqual(expected["gold_c_original"]["canonical_state"], expected["gold_c_distractor_variant"]["canonical_state"])
        self.assertEqual(expected["gold_c_distractor_variant"]["dependency_assertions"]["canonical_equals_case"], "gold_c_original")
        for case_id in ("normal", "gold_c_original", "gold_c_distractor_variant"):
            self.assertEqual(expected[case_id]["decision"], {"kind": "EXECUTE", "action_id": "write_json", "executor_resolutions": []})
            self.assertEqual(expected[case_id]["result"], {"kind": "EXECUTED", "action_id": "write_json", "final_observables": {"format": {"type": "OutputFormat", "value": "JSON"}}, "ordered_effects": ["WRITE_OUTPUT"]})

    def test_loader_public_api_is_limited_to_the_two_expected_blind_entrypoints(self) -> None:
        import Phase0.implementation.fixture_loader as fixture_loader

        self.assertEqual(fixture_loader.__all__, ("load_fixture_inputs", "load_fixture_input"))
        for name in ("expected", "decision", "result"):
            self.assertFalse(any(public_name.lower().find(name) >= 0 for public_name in fixture_loader.__all__))


if __name__ == "__main__":
    unittest.main()
