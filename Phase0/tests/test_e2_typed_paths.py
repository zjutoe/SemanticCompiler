"""E2 checks for the strict fixture-direct typed A/B adapters."""

from __future__ import annotations

import ast
import inspect
import json
import unittest
from dataclasses import replace
from pathlib import Path

from Phase0.implementation import typed_paths
from Phase0.implementation.backend import BackendOutcome, run_backend
from Phase0.implementation.elaboration import ElaborationFailure
from Phase0.implementation.fixture_loader import (
    _parse_canonical_state,
    load_fixture_input,
    load_fixture_inputs,
)
from Phase0.implementation.schema import (
    AdapterPayload,
    AssertionBasis,
    AssertionCommitment,
    CanonicalPayload,
    CanonicalSemanticState,
    KnowledgeAssertion,
    OpenTerm,
    TypedValue,
    ValueTerm,
)
from Phase0.implementation.typed_paths import (
    AdapterFailure,
    ContractClause,
    ContractKnowledgeAssertion,
    ContractOpenArgument,
    ContractSurfaceState,
    ContractValueArgument,
    IsomorphicFact,
    IsomorphicOpenBinding,
    IsomorphicProposition,
    IsomorphicTerm,
    SemanticIsomorphicSurfaceState,
    adapt_typed_surface,
    alpha_A,
    alpha_B,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures"
CANONICAL_FILES = (
    "F1_OPEN_UU_COUPLED_MIN_ASK.json",
    "F2_OPEN_UE_OWNER_BOUNDARY.json",
    "F3_EXECUTOR_COVERAGE_NONVACUOUS.json",
    "F4_EXECUTOR_JOINT_TRACE.json",
    "F5_AUTHORITY_ROLE_COUNTERFACTUAL.json",
    "F6_HARD_UNSAT_WITNESS.json",
    "F7_NO_AUTHORIZED_ACTION_WITNESS.json",
    "F8_NO_SILENT_INVALID_EXECUTION.json",
)
F9_FILE = "F9_C_NORMAL_END_TO_END_EXACT.json"


def _read_document(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _mention_for(state, clause_index: int, argument_index: int):
    clause_link = f"clause:{clause_index:03d}"
    matches = tuple(
        mention
        for mention in state.open_slot_mentions
        if mention.proposition_link == clause_link
        and mention.argument_position == argument_index
    )
    if len(matches) != 1:
        raise AssertionError((clause_link, argument_index, matches))
    return matches[0]


def _canonical_to_a(state: CanonicalSemanticState) -> ContractSurfaceState:
    clauses = []
    for clause_index, candidate in enumerate(state.normative_candidates):
        clause_link = f"clause:{clause_index:03d}"
        arguments = []
        for argument_index, term in enumerate(candidate.args):
            if type(term) is ValueTerm:
                arguments.append(ContractValueArgument(term.value))
            elif type(term) is OpenTerm:
                mention = _mention_for(state, clause_index, argument_index)
                arguments.append(
                    ContractOpenArgument(
                        semantic_slot_link=term.semantic_slot_link,
                        type=term.type,
                        owner=mention.owner,
                        proposition_support=mention.proposition_support,
                    )
                )
            else:
                raise AssertionError(term)
        clauses.append(
            ContractClause(
                clause_link=clause_link,
                modality=candidate.modality,
                predicate=candidate.predicate,
                arguments=tuple(arguments),
                proposition_support=candidate.proposition_support,
                claimed_authority_support=candidate.claimed_authority_support,
            )
        )
    knowledge = []
    for index, assertion in enumerate(state.knowledge_assertions):
        if any(type(term) is not ValueTerm for term in assertion.args):
            raise AssertionError(assertion)
        knowledge.append(
            ContractKnowledgeAssertion(
                knowledge_link=f"knowledge:{index:03d}",
                predicate=assertion.predicate,
                arguments=tuple(
                    ContractValueArgument(term.value) for term in assertion.args
                ),
                basis=assertion.basis,
                commitment=assertion.commitment,
                proposition_support=assertion.proposition_support,
            )
        )
    return ContractSurfaceState(tuple(clauses), tuple(knowledge))


def _canonical_to_b(
    state: CanonicalSemanticState,
) -> SemanticIsomorphicSurfaceState:
    propositions = []
    bindings = []
    for proposition_index, candidate in enumerate(state.normative_candidates):
        terms = []
        for argument_index, term in enumerate(candidate.args):
            if type(term) is ValueTerm:
                terms.append(IsomorphicTerm("VALUE", term.value.type, term.value.value))
            elif type(term) is OpenTerm:
                mention = _mention_for(state, proposition_index, argument_index)
                terms.append(IsomorphicTerm("OPEN", term.type, None))
                bindings.append(
                    IsomorphicOpenBinding(
                        proposition_index,
                        argument_index,
                        mention.owner,
                        mention.proposition_support,
                    )
                )
            else:
                raise AssertionError(term)
        propositions.append(
            IsomorphicProposition(
                proposition_index,
                candidate.modality,
                candidate.predicate,
                tuple(terms),
                candidate.proposition_support,
                candidate.claimed_authority_support,
            )
        )
    facts = []
    for fact_index, assertion in enumerate(state.knowledge_assertions):
        if any(type(term) is not ValueTerm for term in assertion.args):
            raise AssertionError(assertion)
        facts.append(
            IsomorphicFact(
                fact_index,
                assertion.predicate,
                tuple(
                    IsomorphicTerm("VALUE", term.value.type, term.value.value)
                    for term in assertion.args
                ),
                assertion.basis,
                assertion.commitment,
                assertion.proposition_support,
            )
        )
    return SemanticIsomorphicSurfaceState(
        tuple(propositions),
        tuple(facts),
        tuple(bindings),
    )


def _run_case(case, state):
    return run_backend(
        state,
        case.source_envelope,
        case.visible_world_context,
        case.slot_declarations,
        case.static_constraints,
        case.cross_constraints,
        case.candidate_trajectory_ids,
    )


def _canonical_cases():
    for file_name in CANONICAL_FILES:
        for case in load_fixture_inputs(FIXTURE_DIR / file_name):
            if isinstance(case.entry_payload, CanonicalPayload):
                yield case


def _f9_cases():
    cases = {
        case.case_id: case
        for case in load_fixture_inputs(FIXTURE_DIR / F9_FILE)
    }
    for raw_case in _read_document(FIXTURE_DIR / F9_FILE)["cases"]:
        case_id = raw_case["case_id"]
        state = _parse_canonical_state(
            raw_case["expected"]["canonical_state"],
            f"{case_id}.expected.canonical_state",
        )
        yield cases[case_id], state


class E2TypedPathsTest(unittest.TestCase):
    maxDiff = None

    def assert_adapter_failure(self, reason, function, *args):
        with self.assertRaises(AdapterFailure) as raised:
            function(*args)
        self.assertEqual(raised.exception.stage, "adapter_or_bridge")
        self.assertEqual(raised.exception.reason, reason)

    def test_fixture_gold_round_trip_for_both_typed_paths(self) -> None:
        for case in _canonical_cases():
            state = case.entry_payload.canonical_state
            with self.subTest(fixture=case.fixture_id, case=case.case_id):
                self.assertEqual(alpha_A(_canonical_to_a(state)), state)
                self.assertEqual(alpha_B(_canonical_to_b(state)), state)
        for case, state in _f9_cases():
            with self.subTest(fixture=case.fixture_id, case=case.case_id):
                self.assertEqual(alpha_A(_canonical_to_a(state)), state)
                self.assertEqual(alpha_B(_canonical_to_b(state)), state)

    def test_backend_outcomes_decisions_and_results_have_exact_a_b_parity(self) -> None:
        cases = tuple(
            case for case in _canonical_cases() if case.fixture_id != "F8_NO_SILENT_INVALID_EXECUTION"
        ) + tuple(case_and_state for case_and_state in _f9_cases())
        for item in cases:
            if type(item) is tuple:
                case, state = item
            else:
                case = item
                state = case.entry_payload.canonical_state
            with self.subTest(fixture=case.fixture_id, case=case.case_id):
                outcome_a = _run_case(case, alpha_A(_canonical_to_a(state)))
                outcome_b = _run_case(case, alpha_B(_canonical_to_b(state)))
                self.assertIsInstance(outcome_a, BackendOutcome)
                self.assertEqual(outcome_a, outcome_b)
                self.assertEqual(outcome_a.decision, outcome_b.decision)
                self.assertEqual(outcome_a.result, outcome_b.result)

    def test_f8_failures_stay_at_the_accepted_boundaries(self) -> None:
        expected = {
            raw_case["case_id"]: raw_case["expected"]["failure"]
            for raw_case in _read_document(
                FIXTURE_DIR / "F8_NO_SILENT_INVALID_EXECUTION.json"
            )["cases"]
        }
        for case_id in (
            "dangling_support",
            "wrong_enum_type",
            "malformed_domain",
            "declared_empty_domain",
        ):
            case = load_fixture_input(
                FIXTURE_DIR / "F8_NO_SILENT_INVALID_EXECUTION.json",
                case_id,
            )
            state = case.entry_payload.canonical_state
            for adapter, surface in (
                (alpha_A, _canonical_to_a(state)),
                (alpha_B, _canonical_to_b(state)),
            ):
                with self.subTest(case=case_id, adapter=adapter.__name__):
                    with self.assertRaises(ElaborationFailure) as raised:
                        _run_case(case, adapter(surface))
                    self.assertEqual(
                        {
                            "stage": raised.exception.stage,
                            "reason": raised.exception.reason,
                        },
                        expected[case_id],
                    )

        missing = load_fixture_input(
            FIXTURE_DIR / "F8_NO_SILENT_INVALID_EXECUTION.json",
            "missing_adapter_link",
        )
        self.assertIsInstance(missing.entry_payload, AdapterPayload)
        self.assert_adapter_failure(
            "MISSING_ADAPTER_LINK",
            adapt_typed_surface,
            missing.entry_payload.adapter_link,
            missing.entry_payload.surface,
        )

    def test_hand_authored_f1_and_joint_owner_f2_pairs(self) -> None:
        f1_expected = load_fixture_input(
            FIXTURE_DIR / "F1_OPEN_UU_COUPLED_MIN_ASK.json",
            "unresolved",
        ).entry_payload.canonical_state
        f1_a = ContractSurfaceState(
            clauses=(
                ContractClause(
                    "clause:000",
                    "REQUIRE",
                    "world.output_policy_is",
                    (
                        ContractOpenArgument(
                            "slot:clause:000:arg0", "OutputFormat", "USER", ("u1",)
                        ),
                        ContractOpenArgument(
                            "slot:clause:000:arg1", "Strictness", "USER", ("u1",)
                        ),
                    ),
                    ("u1",),
                    ("u1",),
                ),
            ),
            knowledge_assertions=(),
        )
        f1_b = SemanticIsomorphicSurfaceState(
            propositions=(
                IsomorphicProposition(
                    0,
                    "REQUIRE",
                    "world.output_policy_is",
                    (
                        IsomorphicTerm("OPEN", "OutputFormat", None),
                        IsomorphicTerm("OPEN", "Strictness", None),
                    ),
                    ("u1",),
                    ("u1",),
                ),
            ),
            facts=(),
            open_bindings=(
                IsomorphicOpenBinding(0, 0, "USER", ("u1",)),
                IsomorphicOpenBinding(0, 1, "USER", ("u1",)),
            ),
        )
        self.assertEqual(alpha_A(f1_a), f1_expected)
        self.assertEqual(alpha_B(f1_b), f1_expected)

        f2_expected = load_fixture_input(
            FIXTURE_DIR / "F2_OPEN_UE_OWNER_BOUNDARY.json",
            "unresolved",
        ).entry_payload.canonical_state
        f2_a = ContractSurfaceState(
            clauses=(
                ContractClause(
                    "clause:000",
                    "REQUIRE",
                    "world.error_handling_is",
                    (
                        ContractOpenArgument(
                            "slot:clause:000:arg0", "ErrorPolicy", "USER", ("u1",)
                        ),
                        ContractOpenArgument(
                            "slot:clause:000:arg1", "LogMode", "EXECUTOR", ("u1",)
                        ),
                    ),
                    ("u1",),
                    ("u1",),
                ),
            ),
            knowledge_assertions=(),
        )
        f2_b = SemanticIsomorphicSurfaceState(
            propositions=(
                IsomorphicProposition(
                    0,
                    "REQUIRE",
                    "world.error_handling_is",
                    (
                        IsomorphicTerm("OPEN", "ErrorPolicy", None),
                        IsomorphicTerm("OPEN", "LogMode", None),
                    ),
                    ("u1",),
                    ("u1",),
                ),
            ),
            facts=(),
            open_bindings=(
                IsomorphicOpenBinding(0, 0, "USER", ("u1",)),
                IsomorphicOpenBinding(0, 1, "EXECUTOR", ("u1",)),
            ),
        )
        self.assertEqual(alpha_A(f2_a), f2_expected)
        self.assertEqual(alpha_B(f2_b), f2_expected)

    def test_fixed_value_knowledge_round_trip_for_both_schemas(self) -> None:
        state = CanonicalSemanticState(
            normative_candidates=(),
            knowledge_assertions=(
                KnowledgeAssertion(
                    predicate="world.final_format_is",
                    args=(
                        ValueTerm(
                            "VALUE",
                            TypedValue("OutputFormat", "JSON"),
                        ),
                    ),
                    basis=AssertionBasis.OBSERVATION.value,
                    commitment=AssertionCommitment.ASSERTED.value,
                    proposition_support=("t1",),
                ),
            ),
            open_slot_mentions=(),
        )
        self.assertEqual(alpha_A(_canonical_to_a(state)), state)
        self.assertEqual(alpha_B(_canonical_to_b(state)), state)

    def test_contract_surface_rejects_malformed_records_containers_and_links(self) -> None:
        value = ContractValueArgument(TypedValue("OutputFormat", "JSON"))
        clause = ContractClause(
            "clause:000",
            "REQUIRE",
            "world.final_format_is",
            (value,),
            ("u1",),
            ("u1",),
        )
        surface = ContractSurfaceState((clause,), ())
        open_clause = replace(
            clause,
            arguments=(
                ContractOpenArgument(
                    "slot:clause:000:arg0", "OutputFormat", "USER", ("u1",)
                ),
            ),
        )
        bad_assertion = ContractKnowledgeAssertion(
            "knowledge:001",
            "world.final_format_is",
            (value,),
            "OBSERVATION",
            "ASSERTED",
            ("u1",),
        )
        malformed = (
            replace(surface, clauses=[clause]),
            replace(surface, clauses=(replace(clause, arguments=[value]),)),
            replace(surface, clauses=(replace(clause, proposition_support=("u1", 1)),)),
            replace(
                surface,
                clauses=(
                    replace(
                        clause,
                        arguments=(
                            ContractValueArgument(TypedValue("OutputFormat", "TOML")),
                        ),
                    ),
                ),
            ),
            replace(
                surface,
                clauses=(
                    replace(
                        clause,
                        arguments=(ContractValueArgument(("OutputFormat", "JSON")),),
                    ),
                ),
            ),
            ContractSurfaceState((clause, clause), ()),
            ContractSurfaceState((replace(clause, clause_link="clause:001"),), ()),
            ContractSurfaceState((replace(clause, clause_link="clause:0"),), ()),
            ContractSurfaceState(
                (
                    replace(
                        open_clause,
                        arguments=(
                            replace(
                                open_clause.arguments[0],
                                semantic_slot_link="slot:clause:000:arg1",
                            ),
                        ),
                    ),
                ),
                (),
            ),
            ContractSurfaceState((clause,), (bad_assertion,)),
        )
        for index, bad_surface in enumerate(malformed):
            with self.subTest(index=index):
                self.assert_adapter_failure(
                    "INVALID_CONTRACT_SURFACE", alpha_A, bad_surface
                )

    def test_isomorphic_surface_rejects_malformed_records_indices_and_terms(self) -> None:
        value_term = IsomorphicTerm("VALUE", "OutputFormat", "JSON")
        proposition = IsomorphicProposition(
            0,
            "REQUIRE",
            "world.final_format_is",
            (value_term,),
            ("u1",),
            ("u1",),
        )
        surface = SemanticIsomorphicSurfaceState((proposition,), (), ())
        fact = IsomorphicFact(
            1,
            "world.final_format_is",
            (value_term,),
            "OBSERVATION",
            "ASSERTED",
            ("u1",),
        )
        malformed = (
            replace(surface, propositions=[proposition]),
            replace(surface, propositions=(replace(proposition, terms=[value_term]),)),
            replace(surface, propositions=(replace(proposition, proposition_index=True),)),
            replace(surface, propositions=(replace(proposition, proposition_index="0"),)),
            replace(surface, propositions=(replace(proposition, proposition_index=1),)),
            replace(surface, propositions=(proposition, proposition)),
            replace(
                surface,
                propositions=(
                    replace(
                        proposition,
                        terms=(IsomorphicTerm("FIXED", "OutputFormat", "JSON"),),
                    ),
                ),
            ),
            replace(
                surface,
                propositions=(
                    replace(
                        proposition,
                        terms=(IsomorphicTerm("VALUE", "OutputFormat", "TOML"),),
                    ),
                ),
            ),
            replace(
                surface,
                propositions=(replace(proposition, evidence=("u1", 1)),),
            ),
            replace(surface, facts=(fact,)),
        )
        for index, bad_surface in enumerate(malformed):
            with self.subTest(index=index):
                self.assert_adapter_failure(
                    "INVALID_ISOMORPHIC_SURFACE", alpha_B, bad_surface
                )

    def test_isomorphic_open_bindings_are_an_exact_ordered_bijection(self) -> None:
        open_term = IsomorphicTerm("OPEN", "OutputFormat", None)
        open_proposition = IsomorphicProposition(
            0,
            "REQUIRE",
            "world.final_format_is",
            (open_term,),
            ("u1",),
            ("u1",),
        )
        binding = IsomorphicOpenBinding(0, 0, "USER", ("u1",))
        valid_open = SemanticIsomorphicSurfaceState(
            (open_proposition,), (), (binding,)
        )
        self.assertEqual(len(alpha_B(valid_open).open_slot_mentions), 1)

        value_proposition = replace(
            open_proposition,
            terms=(IsomorphicTerm("VALUE", "OutputFormat", "JSON"),),
        )
        two_open = replace(open_proposition, terms=(open_term, open_term))
        malformed = (
            replace(valid_open, open_bindings=()),
            replace(valid_open, open_bindings=(binding, binding)),
            SemanticIsomorphicSurfaceState(
                (value_proposition,), (), (binding,)
            ),
            replace(
                valid_open,
                open_bindings=(IsomorphicOpenBinding(0, 1, "USER", ("u1",)),),
            ),
            SemanticIsomorphicSurfaceState(
                (two_open,),
                (),
                (
                    IsomorphicOpenBinding(0, 1, "USER", ("u1",)),
                    IsomorphicOpenBinding(0, 0, "USER", ("u1",)),
                ),
            ),
            replace(
                valid_open,
                open_bindings=(IsomorphicOpenBinding(0, True, "USER", ("u1",)),),
            ),
        )
        for index, bad_surface in enumerate(malformed):
            with self.subTest(index=index):
                self.assert_adapter_failure(
                    "INVALID_ISOMORPHIC_SURFACE", alpha_B, bad_surface
                )

    def test_dispatcher_precedence_and_exact_surface_types(self) -> None:
        a = ContractSurfaceState((), ())
        b = SemanticIsomorphicSurfaceState((), (), ())
        cases = (
            ("MISSING_ADAPTER_LINK", None, object()),
            ("INVALID_ADAPTER_LINK", 1, object()),
            ("UNKNOWN_ADAPTER_LINK", "alpha_C", object()),
            ("ADAPTER_SURFACE_TYPE_MISMATCH", "alpha_A", b),
            ("ADAPTER_SURFACE_TYPE_MISMATCH", "alpha_B", a),
        )
        for reason, link, surface in cases:
            with self.subTest(reason=reason):
                self.assert_adapter_failure(reason, adapt_typed_surface, link, surface)
        self.assertEqual(adapt_typed_surface("alpha_A", a), alpha_A(a))
        self.assertEqual(adapt_typed_surface("alpha_B", b), alpha_B(b))

    def test_production_module_dependencies_are_expected_blind(self) -> None:
        source = inspect.getsource(typed_paths)
        tree = ast.parse(source)
        imports = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        self.assertEqual(
            set(imports),
            {"__future__", "dataclasses", "Phase0.implementation.schema"},
        )
        imported_modules = tuple(
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        )
        self.assertEqual(imported_modules, ())
        identifiers = {
            node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
        } | {
            node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
        }
        forbidden = {
            "open",
            "fixture_id",
            "case_id",
            "scenario_id",
            "expected",
            "candidate_trajectory_ids",
            "action_id",
            "ordered_effects",
            "final_observables",
            "run_backend",
            "BackendOutcome",
        }
        self.assertTrue(identifiers.isdisjoint(forbidden))
        self.assertNotIn("Phase0.tests", source)
        self.assertNotIn("fixture_loader", source)
        self.assertNotIn("import json", source)


if __name__ == "__main__":
    unittest.main()
