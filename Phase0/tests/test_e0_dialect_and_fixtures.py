"""E0-only checks for the finite dialect, fixture inputs, and test-local expected data."""

from __future__ import annotations

import json
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


def _validate_expected_shape(expected: dict[str, Any]) -> None:
    assert tuple(expected.keys()) == EXPECTED_KEYS
    if expected["canonical_state"] is not None:
        _validate_canonical_state_shape(expected["canonical_state"])
    if expected["elaboration"] is not None:
        assert tuple(expected["elaboration"].keys()) == ("candidates", "active_clause_links", "knowledge_assertions", "open_slots", "slot_domains", "constraint_links")
    if expected["legal_joint_completions"] is not None:
        assert isinstance(expected["legal_joint_completions"], list)
        for assignment in expected["legal_joint_completions"]:
            _validate_assignment(assignment)
    decision = expected["decision"]
    if decision is not None:
        if decision["kind"] == "ASK":
            assert tuple(decision.keys()) == ("kind", "semantic_slot_links")
        elif decision["kind"] == "EXECUTE":
            assert tuple(decision.keys()) == ("kind", "action_id", "executor_resolutions")
            _validate_assignment(decision["executor_resolutions"])
        elif decision["kind"] == "REJECT":
            assert tuple(decision.keys()) == ("kind", "reason", "witness", "executor_resolutions")
            assert decision["reason"] in ("HARD_UNSAT", "NO_AUTHORIZED_ACTION")
            _validate_assignment(decision["executor_resolutions"])
        else:
            raise AssertionError(decision)
    if expected["result"] is not None:
        assert tuple(expected["result"].keys()) == ("kind", "action_id", "final_observables", "ordered_effects")
    if expected["failure"] is not None:
        assert tuple(expected["failure"].keys()) == ("stage", "reason")
    if expected["dependency_assertions"] is not None:
        assert tuple(expected["dependency_assertions"].keys()) == ("normal_content_refs", "referenced_support_view", "canonical_equals_case")


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
        self.assertEqual(
            tuple(dialect.TRAJECTORIES_BY_ID),
            (
                "tau:f1:json_strict",
                "tau:f1:yaml_lenient",
                "tau:f2:return_none_quiet",
                "tau:f2:raise_verbose",
                "tau:f3:safe_local",
                "tau:f3:fast_local",
                "tau:f3:fast_remote",
                "tau:f4:yaml_lenient",
                "tau:f4:json_strict",
                "tau:f5:fixed_yaml",
                "tau:f5:fixed_json",
                "tau:f5:open_yaml",
                "tau:f5:open_json",
                "tau:f6:json",
                "tau:f6:yaml",
                "tau:f7:write_json",
                "tau:f9:write_json",
            ),
        )
        effectful = [item.trajectory_id for item in dialect.TRAJECTORIES if item.ordered_effects]
        self.assertEqual(effectful, ["tau:f7:write_json", "tau:f9:write_json"])
        self.assertEqual(dialect.TRAJECTORIES_BY_ID["tau:f4:json_strict"].action_id, "f4_b_json_strict")
        self.assertEqual(_freeze(dialect.TRAJECTORIES_BY_ID["tau:f2:return_none_quiet"].initial_observables), [])

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

    def test_exact_decisions_and_witness_routes_are_frozen(self) -> None:
        expected = _read_expected(FIXTURE_DIR / "F1_OPEN_UU_COUPLED_MIN_ASK.json")["unresolved"]
        self.assertEqual(expected["decision"], {"kind": "ASK", "semantic_slot_links": [S0]})
        expected = _read_expected(FIXTURE_DIR / "F2_OPEN_UE_OWNER_BOUNDARY.json")
        self.assertEqual(expected["resolved_return_none"]["decision"], {"kind": "EXECUTE", "action_id": "f2_return_none_quiet", "executor_resolutions": _assignment((S1, _tv("LogMode", "QUIET")))})
        expected = _read_expected(FIXTURE_DIR / "F3_EXECUTOR_COVERAGE_NONVACUOUS.json")["unresolved"]
        self.assertEqual(expected["decision"], {"kind": "EXECUTE", "action_id": "f3_use_local", "executor_resolutions": _assignment((S1, _tv("Backend", "LOCAL")))})
        expected = _read_expected(FIXTURE_DIR / "F4_EXECUTOR_JOINT_TRACE.json")["unresolved"]
        self.assertEqual(expected["decision"], {"kind": "EXECUTE", "action_id": "f4_b_json_strict", "executor_resolutions": _assignment((S0, _tv("OutputFormat", "JSON")), (S1, _tv("Strictness", "STRICT")))})
        expected = _read_expected(FIXTURE_DIR / "F6_HARD_UNSAT_WITNESS.json")
        self.assertEqual(expected["clause_conflict"]["decision"]["witness"]["kind"], "ClauseConflictWitness")
        self.assertEqual(expected["static_empty"]["decision"]["witness"]["kind"], "EmptyDomainWitness")
        self.assertEqual(expected["cross_empty"]["decision"]["witness"]["kind"], "CrossConstraintWitness")
        expected = _read_expected(FIXTURE_DIR / "F7_NO_AUTHORIZED_ACTION_WITNESS.json")["missing_allow"]
        self.assertEqual(expected["decision"]["reason"], "NO_AUTHORIZED_ACTION")
        self.assertEqual(expected["decision"]["witness"], {"kind": "NoAuthorizedActionWitness", "excluded_actions": [{"action_id": "f7_write_json", "unauthorized_managed_effects": ["WRITE_OUTPUT"]}]})

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
