"""E1 checks for shared elaboration, runtime decisions, and backend results."""

from __future__ import annotations

import inspect
import json
import unittest
from dataclasses import replace
from pathlib import Path
from typing import Any

from Phase0.implementation import backend, elaboration, runtime
from Phase0.implementation.backend import run_backend
from Phase0.implementation.elaboration import ElaborationFailure
from Phase0.implementation.fixture_loader import (
    _parse_canonical_state,
    load_fixture_input,
    load_fixture_inputs,
)
from Phase0.implementation.runtime import (
    AskDecision,
    ClauseConflictWitness,
    CrossConstraintWitness,
    EmptyDomainWitness,
    ExecuteDecision,
    NoAuthorizedActionWitness,
    RejectDecision,
    RuntimeFailure,
)
from Phase0.implementation.schema import (
    AssertionBasis,
    AssertionCommitment,
    AdapterPayload,
    CanonicalPayload,
    CanonicalSemanticState,
    KnowledgeAssertion,
    Modality,
    NormativeCandidate,
    OpenTerm,
    SourceEnvelope,
    SourceRole,
    SourceSpan,
    StaticConstraint,
    TypedValue,
    ValueTerm,
    VisibleWorldContext,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures"
CANONICAL_FIXTURES = (
    "F1_OPEN_UU_COUPLED_MIN_ASK.json",
    "F2_OPEN_UE_OWNER_BOUNDARY.json",
    "F3_EXECUTOR_COVERAGE_NONVACUOUS.json",
    "F4_EXECUTOR_JOINT_TRACE.json",
    "F5_AUTHORITY_ROLE_COUNTERFACTUAL.json",
    "F6_HARD_UNSAT_WITNESS.json",
    "F7_NO_AUTHORIZED_ACTION_WITNESS.json",
)


def _read_document(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _expected_by_case(path: Path) -> dict[str, dict[str, Any]]:
    document = _read_document(path)
    return {case["case_id"]: case["expected"] for case in document["cases"]}


def _typed_value(value) -> dict[str, str]:
    return {"type": value.type, "value": value.value}


def _maybe_typed_value(value) -> dict[str, str] | None:
    if value is None:
        return None
    return _typed_value(value)


def _assignment(value) -> list[dict[str, Any]]:
    return [
        {
            "semantic_slot_link": item.semantic_slot_link,
            "value": _typed_value(item.value),
        }
        for item in value
    ]


def _project_elaboration(value) -> dict[str, Any]:
    return {
        "candidates": [
            {
                "clause_link": candidate.clause_link,
                "authority": candidate.authority,
                "active": candidate.active,
            }
            for candidate in value.candidates
        ],
        "active_clause_links": list(value.active_clause_links),
        "knowledge_assertions": [],
        "open_slots": [
            {
                "semantic_slot_link": slot.semantic_slot_link,
                "type": slot.type,
                "owner": slot.owner,
                "resolved_value": _maybe_typed_value(slot.resolved_value),
            }
            for slot in value.open_slots
        ],
        "slot_domains": [
            {
                "semantic_slot_link": domain.semantic_slot_link,
                "values": [_typed_value(item) for item in domain.values],
            }
            for domain in value.slot_domains
        ],
        "constraint_links": list(value.constraint_links),
    }


def _project_witness(value) -> dict[str, Any]:
    if isinstance(value, ClauseConflictWitness):
        return {"kind": value.kind, "clause_links": list(value.clause_links)}
    if isinstance(value, EmptyDomainWitness):
        return {
            "kind": value.kind,
            "semantic_slot_link": value.semantic_slot_link,
            "excluding_constraint_links": list(value.excluding_constraint_links),
        }
    if isinstance(value, CrossConstraintWitness):
        return {
            "kind": value.kind,
            "cross_constraint_links": list(value.cross_constraint_links),
        }
    if isinstance(value, NoAuthorizedActionWitness):
        return {
            "kind": value.kind,
            "excluded_actions": [
                {
                    "action_id": action.action_id,
                    "unauthorized_managed_effects": list(
                        action.unauthorized_managed_effects
                    ),
                }
                for action in value.excluded_actions
            ],
        }
    raise AssertionError(value)


def _project_decision(value) -> dict[str, Any]:
    if isinstance(value, AskDecision):
        return {
            "kind": value.kind,
            "semantic_slot_links": list(value.semantic_slot_links),
        }
    if isinstance(value, ExecuteDecision):
        return {
            "kind": value.kind,
            "action_id": value.action_id,
            "executor_resolutions": _assignment(value.executor_resolutions),
        }
    if isinstance(value, RejectDecision):
        return {
            "kind": value.kind,
            "reason": value.reason,
            "witness": _project_witness(value.witness),
            "executor_resolutions": _assignment(value.executor_resolutions),
        }
    raise AssertionError(value)


def _project_result(value) -> dict[str, Any] | None:
    if value is None:
        return None
    return {
        "kind": value.kind,
        "action_id": value.action_id,
        "final_observables": {
            observable.name: _typed_value(observable.value)
            for observable in value.final_observables
        },
        "ordered_effects": list(value.ordered_effects),
    }


def _run_case(case, canonical_state=None):
    if canonical_state is None:
        if not isinstance(case.entry_payload, CanonicalPayload):
            raise AssertionError(case)
        canonical_state = case.entry_payload.canonical_state
    return run_backend(
        canonical_state,
        case.source_envelope,
        case.visible_world_context,
        case.slot_declarations,
        case.static_constraints,
        case.cross_constraints,
        case.candidate_trajectory_ids,
    )


class E1ElaborationAndRuntimeTest(unittest.TestCase):
    maxDiff = None

    def test_f1_f7_canonical_routes_match_expected_backend_projections(self) -> None:
        for file_name in CANONICAL_FIXTURES:
            path = FIXTURE_DIR / file_name
            expected = _expected_by_case(path)
            for case in load_fixture_inputs(path):
                with self.subTest(fixture=case.fixture_id, case=case.case_id):
                    outcome = _run_case(case)
                    self.assertEqual(
                        _project_elaboration(outcome.elaborated),
                        expected[case.case_id]["elaboration"],
                    )
                    self.assertEqual(
                        [_assignment(item) for item in outcome.legal_joint_completions],
                        expected[case.case_id]["legal_joint_completions"],
                    )
                    self.assertEqual(
                        _project_decision(outcome.decision),
                        expected[case.case_id]["decision"],
                    )
                    if not isinstance(outcome.decision, ExecuteDecision):
                        self.assertIsNone(outcome.result)

    def test_authority_coverage_witness_and_result_routes_are_distinct(self) -> None:
        assistant_case = load_fixture_input(
            FIXTURE_DIR / "F5_AUTHORITY_ROLE_COUNTERFACTUAL.json",
            "assistant_fixed",
        )
        assistant_outcome = _run_case(assistant_case)
        self.assertEqual(assistant_outcome.elaborated.candidates[0].authority, "NONE")
        self.assertFalse(assistant_outcome.elaborated.candidates[0].active)
        self.assertEqual(_project_decision(assistant_outcome.decision)["action_id"], "f5_a_yaml")

        executor_case = load_fixture_input(
            FIXTURE_DIR / "F3_EXECUTOR_COVERAGE_NONVACUOUS.json",
            "unresolved",
        )
        executor_outcome = _run_case(executor_case)
        self.assertEqual(
            _project_decision(executor_outcome.decision),
            {
                "kind": "EXECUTE",
                "action_id": "f3_use_local",
                "executor_resolutions": [
                    {
                        "semantic_slot_link": "slot:clause:000:arg1",
                        "value": {"type": "Backend", "value": "LOCAL"},
                    }
                ],
            },
        )
        self.assertIsNone(executor_outcome.result)

        expected_witness_types = {
            "clause_conflict": ClauseConflictWitness,
            "static_empty": EmptyDomainWitness,
            "cross_empty": CrossConstraintWitness,
        }
        for case_id, witness_type in expected_witness_types.items():
            with self.subTest(case=case_id):
                case = load_fixture_input(
                    FIXTURE_DIR / "F6_HARD_UNSAT_WITNESS.json",
                    case_id,
                )
                outcome = _run_case(case)
                self.assertIsInstance(outcome.decision, RejectDecision)
                self.assertIsInstance(outcome.decision.witness, witness_type)
                self.assertIsNone(outcome.result)

        no_auth_case = load_fixture_input(
            FIXTURE_DIR / "F7_NO_AUTHORIZED_ACTION_WITNESS.json",
            "missing_allow",
        )
        no_auth_outcome = _run_case(no_auth_case)
        self.assertIsInstance(no_auth_outcome.decision, RejectDecision)
        self.assertEqual(no_auth_outcome.decision.reason, "NO_AUTHORIZED_ACTION")
        self.assertIsInstance(no_auth_outcome.decision.witness, NoAuthorizedActionWitness)

    def test_f8_elaboration_failures_are_loud_and_adapter_case_stays_out_of_e1(self) -> None:
        path = FIXTURE_DIR / "F8_NO_SILENT_INVALID_EXECUTION.json"
        expected = _expected_by_case(path)
        for case in load_fixture_inputs(path):
            if case.case_id == "missing_adapter_link":
                self.assertIsInstance(case.entry_payload, AdapterPayload)
                self.assertEqual(
                    expected[case.case_id]["failure"],
                    {"stage": "adapter_or_bridge", "reason": "MISSING_ADAPTER_LINK"},
                )
                continue
            with self.subTest(case=case.case_id):
                with self.assertRaises(ElaborationFailure) as raised:
                    _run_case(case)
                self.assertEqual(
                    {
                        "stage": raised.exception.stage,
                        "reason": raised.exception.reason,
                    },
                    expected[case.case_id]["failure"],
                )

    def test_f9_expected_canonical_values_use_same_backend_and_exact_result(self) -> None:
        path = FIXTURE_DIR / "F9_C_NORMAL_END_TO_END_EXACT.json"
        cases = {case.case_id: case for case in load_fixture_inputs(path)}
        document = _read_document(path)
        for raw_case in document["cases"]:
            case_id = raw_case["case_id"]
            expected = raw_case["expected"]
            canonical_state = _parse_canonical_state(
                expected["canonical_state"],
                f"{case_id}.expected.canonical_state",
            )
            with self.subTest(case=case_id):
                outcome = _run_case(cases[case_id], canonical_state)
                self.assertEqual(
                    _project_elaboration(outcome.elaborated),
                    expected["elaboration"],
                )
                self.assertEqual(
                    [_assignment(item) for item in outcome.legal_joint_completions],
                    expected["legal_joint_completions"],
                )
                self.assertEqual(_project_decision(outcome.decision), expected["decision"])
                self.assertEqual(_project_result(outcome.result), expected["result"])

    def test_same_support_semantic_order_is_independent_of_input_order(self) -> None:
        source = SourceEnvelope(
            spans=(SourceSpan(ref="u1", role=SourceRole.USER.value, text="same"),)
        )
        visible = VisibleWorldContext(entities=(), observable_values=())
        goal_yaml = NormativeCandidate(
            modality=Modality.GOAL.value,
            predicate="world.final_format_is",
            args=(ValueTerm("VALUE", TypedValue("OutputFormat", "YAML")),),
            proposition_support=("u1",),
            claimed_authority_support=("u1",),
        )
        require_json = NormativeCandidate(
            modality=Modality.REQUIRE.value,
            predicate="world.final_format_is",
            args=(ValueTerm("VALUE", TypedValue("OutputFormat", "JSON")),),
            proposition_support=("u1",),
            claimed_authority_support=("u1",),
        )
        knowledge_yaml = KnowledgeAssertion(
            predicate="world.final_format_is",
            args=(ValueTerm("VALUE", TypedValue("OutputFormat", "YAML")),),
            basis=AssertionBasis.EXPLICIT_STATEMENT.value,
            commitment=AssertionCommitment.ASSERTED.value,
            proposition_support=("u1",),
        )
        knowledge_json = KnowledgeAssertion(
            predicate="world.final_format_is",
            args=(ValueTerm("VALUE", TypedValue("OutputFormat", "JSON")),),
            basis=AssertionBasis.EXPLICIT_STATEMENT.value,
            commitment=AssertionCommitment.ASSERTED.value,
            proposition_support=("u1",),
        )
        states = (
            CanonicalSemanticState(
                normative_candidates=(require_json, goal_yaml),
                knowledge_assertions=(knowledge_yaml, knowledge_json),
                open_slot_mentions=(),
            ),
            CanonicalSemanticState(
                normative_candidates=(goal_yaml, require_json),
                knowledge_assertions=(knowledge_json, knowledge_yaml),
                open_slot_mentions=(),
            ),
        )
        projections = []
        for state in states:
            elaborated = elaboration.elaborate(
                state,
                source,
                visible,
                (),
                (),
                (),
            )
            projections.append(
                (
                    [
                        (
                            candidate.clause_link,
                            candidate.original.modality,
                            candidate.original.args[0].value.value,
                        )
                        for candidate in elaborated.candidates
                    ],
                    [
                        assertion.args[0].value.value
                        for assertion in elaborated.knowledge_assertions
                    ],
                )
            )
        self.assertEqual(projections[0], projections[1])
        self.assertEqual(
            projections[0],
            (
                [
                    ("clause:000", "GOAL", "YAML"),
                    ("clause:001", "REQUIRE", "JSON"),
                ],
                ["JSON", "YAML"],
            ),
        )

        missing_support = CanonicalSemanticState(
            normative_candidates=(replace(goal_yaml, proposition_support=()),),
            knowledge_assertions=(),
            open_slot_mentions=(),
        )
        with self.assertRaises(ElaborationFailure) as missing:
            elaboration.elaborate(missing_support, source, visible, (), (), ())
        self.assertEqual(missing.exception.reason, "MISSING_PROPOSITION_SUPPORT")

        unknown_modality = CanonicalSemanticState(
            normative_candidates=(replace(goal_yaml, modality="MUST"),),
            knowledge_assertions=(),
            open_slot_mentions=(),
        )
        with self.assertRaises(ElaborationFailure) as unknown:
            elaboration.elaborate(unknown_modality, source, visible, (), (), ())
        self.assertEqual(unknown.exception.reason, "UNKNOWN_MODALITY")

    def test_direct_dataclass_record_semantics_fail_at_elaboration_boundary(self) -> None:
        source = SourceEnvelope(
            spans=(SourceSpan(ref="u1", role=SourceRole.USER.value, text="same"),)
        )
        visible = VisibleWorldContext(entities=(), observable_values=())
        valid_candidate = NormativeCandidate(
            modality=Modality.REQUIRE.value,
            predicate="world.final_format_is",
            args=(ValueTerm("VALUE", TypedValue("OutputFormat", "JSON")),),
            proposition_support=("u1",),
            claimed_authority_support=("u1",),
        )
        malformed_value_tag = replace(
            valid_candidate,
            args=(ValueTerm("OPEN", TypedValue("OutputFormat", "JSON")),),
        )
        malformed_open_tag = replace(
            valid_candidate,
            args=(OpenTerm("VALUE", "OutputFormat", "slot:clause:000:arg0"),),
        )
        unknown_enum_value = replace(
            valid_candidate,
            args=(ValueTerm("VALUE", TypedValue("OutputFormat", "TOML")),),
        )
        cases = (
            (malformed_value_tag, source, "INVALID_VALUE_TERM_KIND"),
            (malformed_open_tag, source, "INVALID_OPEN_TERM_KIND"),
            (unknown_enum_value, source, "UNKNOWN_ENUM_VALUE"),
            (
                valid_candidate,
                SourceEnvelope(
                    spans=(SourceSpan(ref="u1", role="SYSTEM", text="bad"),)
                ),
                "INVALID_SOURCE_ROLE",
            ),
        )
        for candidate, envelope, reason in cases:
            with self.subTest(reason=reason):
                state = CanonicalSemanticState(
                    normative_candidates=(candidate,),
                    knowledge_assertions=(),
                    open_slot_mentions=(),
                )
                with self.assertRaises(ElaborationFailure) as raised:
                    elaboration.elaborate(state, envelope, visible, (), (), ())
                self.assertEqual(raised.exception.reason, reason)

        valid_knowledge = KnowledgeAssertion(
            predicate="world.final_format_is",
            args=(ValueTerm("VALUE", TypedValue("OutputFormat", "JSON")),),
            basis=AssertionBasis.EXPLICIT_STATEMENT.value,
            commitment=AssertionCommitment.ASSERTED.value,
            proposition_support=("u1",),
        )
        invalid_knowledge_records = (
            (replace(valid_knowledge, basis="GUESS"), "INVALID_KNOWLEDGE_BASIS"),
            (
                replace(valid_knowledge, commitment="MAYBE"),
                "INVALID_KNOWLEDGE_COMMITMENT",
            ),
        )
        for assertion, reason in invalid_knowledge_records:
            with self.subTest(reason=reason):
                state = CanonicalSemanticState(
                    normative_candidates=(),
                    knowledge_assertions=(assertion,),
                    open_slot_mentions=(),
                )
                with self.assertRaises(ElaborationFailure) as raised:
                    elaboration.elaborate(state, source, visible, (), (), ())
                self.assertEqual(raised.exception.reason, reason)

    def test_empty_domain_witness_uses_minimal_redundant_exclusions(self) -> None:
        case = load_fixture_input(
            FIXTURE_DIR / "F6_HARD_UNSAT_WITNESS.json",
            "static_empty",
        )
        slot = case.slot_declarations[0]
        json_value = TypedValue("OutputFormat", "JSON")
        yaml_value = TypedValue("OutputFormat", "YAML")
        redundant_constraints = (
            StaticConstraint(
                constraint_link="constraint:f6:aaa_json_duplicate",
                semantic_slot_link=slot.semantic_slot_link,
                candidate_value=json_value,
                context_predicate="world.format_supported",
                required_context_value=True,
            ),
            StaticConstraint(
                constraint_link="constraint:f6:zzz_yaml_duplicate",
                semantic_slot_link=slot.semantic_slot_link,
                candidate_value=yaml_value,
                context_predicate="world.format_supported",
                required_context_value=True,
            ),
        )
        unresolved_outcome = run_backend(
            case.entry_payload.canonical_state,
            case.source_envelope,
            case.visible_world_context,
            case.slot_declarations,
            case.static_constraints + redundant_constraints,
            case.cross_constraints,
            case.candidate_trajectory_ids,
        )
        self.assertEqual(
            unresolved_outcome.decision.witness.excluding_constraint_links,
            (
                "constraint:f6:aaa_json_duplicate",
                "constraint:f6:format_not_yaml",
            ),
        )

        resolved_slot = replace(slot, resolved_value=json_value)
        resolved_outcome = run_backend(
            case.entry_payload.canonical_state,
            case.source_envelope,
            case.visible_world_context,
            (resolved_slot,),
            case.static_constraints + redundant_constraints,
            case.cross_constraints,
            case.candidate_trajectory_ids,
        )
        self.assertEqual(
            resolved_outcome.decision.witness.excluding_constraint_links,
            ("constraint:f6:aaa_json_duplicate",),
        )

    def test_static_constraints_reject_non_initial_manifest_predicates(self) -> None:
        case = load_fixture_input(
            FIXTURE_DIR / "F6_HARD_UNSAT_WITNESS.json",
            "static_empty",
        )
        bad_constraints = tuple(
            replace(constraint, context_predicate="world.final_format_is")
            for constraint in case.static_constraints
        )
        bad_context = VisibleWorldContext(
            entities=case.visible_world_context.entities,
            observable_values=tuple(
                replace(observation, predicate="world.final_format_is")
                for observation in case.visible_world_context.observable_values
            ),
        )
        with self.assertRaises(ElaborationFailure) as raised:
            run_backend(
                case.entry_payload.canonical_state,
                case.source_envelope,
                bad_context,
                case.slot_declarations,
                bad_constraints,
                case.cross_constraints,
                case.candidate_trajectory_ids,
            )
        self.assertEqual(
            raised.exception.reason,
            "STATIC_CONSTRAINT_PREDICATE_SCOPE_MISMATCH",
        )

    def test_runtime_contract_violations_have_distinct_stable_reasons(self) -> None:
        base_case = load_fixture_input(
            FIXTURE_DIR / "F5_AUTHORITY_ROLE_COUNTERFACTUAL.json",
            "user_fixed",
        )
        with self.assertRaises(RuntimeFailure) as unknown:
            run_backend(
                base_case.entry_payload.canonical_state,
                base_case.source_envelope,
                base_case.visible_world_context,
                base_case.slot_declarations,
                base_case.static_constraints,
                base_case.cross_constraints,
                ("tau:unknown",),
            )
        self.assertEqual(unknown.exception.reason, "UNKNOWN_TRAJECTORY_ID")

        structural_case = load_fixture_input(
            FIXTURE_DIR / "F1_OPEN_UU_COUPLED_MIN_ASK.json",
            "unresolved",
        )
        with self.assertRaises(RuntimeFailure) as structural:
            run_backend(
                structural_case.entry_payload.canonical_state,
                structural_case.source_envelope,
                structural_case.visible_world_context,
                structural_case.slot_declarations,
                structural_case.static_constraints,
                structural_case.cross_constraints,
                ("tau:f5:fixed_json",),
            )
        self.assertEqual(
            structural.exception.reason,
            "STRUCTURALLY_INCOMPATIBLE_TRAJECTORY",
        )

        empty_witness_case = load_fixture_input(
            FIXTURE_DIR / "F5_AUTHORITY_ROLE_COUNTERFACTUAL.json",
            "assistant_fixed",
        )
        with self.assertRaises(RuntimeFailure) as empty_witness:
            run_backend(
                empty_witness_case.entry_payload.canonical_state,
                empty_witness_case.source_envelope,
                empty_witness_case.visible_world_context,
                empty_witness_case.slot_declarations,
                empty_witness_case.static_constraints,
                empty_witness_case.cross_constraints,
                (),
            )
        self.assertEqual(
            empty_witness.exception.reason,
            "EMPTY_TRAJECTORY_FIBER",
        )

        out_of_omega_case = load_fixture_input(
            FIXTURE_DIR / "F2_OPEN_UE_OWNER_BOUNDARY.json",
            "resolved_return_none",
        )
        with self.assertRaises(RuntimeFailure) as out_of_omega:
            run_backend(
                out_of_omega_case.entry_payload.canonical_state,
                out_of_omega_case.source_envelope,
                out_of_omega_case.visible_world_context,
                out_of_omega_case.slot_declarations,
                out_of_omega_case.static_constraints,
                out_of_omega_case.cross_constraints,
                ("tau:f2:raise_verbose",),
            )
        self.assertEqual(out_of_omega.exception.reason, "EMPTY_TRAJECTORY_FIBER")

        f1_case = load_fixture_input(
            FIXTURE_DIR / "F1_OPEN_UU_COUPLED_MIN_ASK.json",
            "unresolved",
        )
        with self.assertRaises(RuntimeFailure) as no_query:
            run_backend(
                f1_case.entry_payload.canonical_state,
                f1_case.source_envelope,
                f1_case.visible_world_context,
                f1_case.slot_declarations,
                f1_case.static_constraints,
                f1_case.cross_constraints,
                ("tau:f1:json_strict",),
            )
        self.assertEqual(no_query.exception.reason, "NO_SUFFICIENT_USER_QUERY")

    def test_public_backend_api_and_production_dependencies_are_expected_blind(self) -> None:
        self.assertEqual(
            tuple(inspect.signature(backend.run_backend).parameters),
            (
                "canonical_state",
                "source_envelope",
                "visible_world_context",
                "slot_declarations",
                "static_constraints",
                "cross_constraints",
                "candidate_trajectory_ids",
            ),
        )
        self.assertEqual(
            tuple(inspect.signature(elaboration.elaborate).parameters),
            (
                "canonical_state",
                "source_envelope",
                "visible_world_context",
                "slot_declarations",
                "static_constraints",
                "cross_constraints",
            ),
        )
        self.assertEqual(
            tuple(inspect.signature(runtime.decide).parameters),
            ("elaborated", "candidate_trajectory_ids"),
        )
        forbidden_source_tokens = (
            "fixture_loader",
            "load_fixture",
            "Phase0.tests",
            "json.load",
            ".json",
            "fixture_id",
            "case_id",
            "scenario_id",
            "entry_stage",
        )
        for module in (backend, elaboration, runtime):
            source = inspect.getsource(module)
            for token in forbidden_source_tokens:
                with self.subTest(module=module.__name__, token=token):
                    self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
