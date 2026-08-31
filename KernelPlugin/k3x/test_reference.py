"""Executable checks for the accepted finite K3-X packet."""

from dataclasses import replace
import unittest

from .coding_plugin import (
    ArtifactContent,
    ArtifactSelector,
    ChangeEntry,
    ChangeKind,
    ChangeSet,
    Criterion,
    CriterionKind,
    Eval,
    EventKind,
    EventPattern,
    EventValue,
    EvidenceEntry,
    FiniteCodingProfileError,
    ObservationResult,
    ObservationSpec,
    PatternKind,
    RepositorySnapshot,
    TaskSpec,
    Truth,
    UndeclaredAccessError,
    VerificationSpec,
    VerificationStatus,
    changes_between,
    dependency_metadata_changed,
    event_matches,
    event_occurred,
    implementation_evidence_profile,
    invoke_with_declared_access,
    observe,
    refresh_scope,
    snapshot_of,
    task_accepts,
    verification_passed,
)
from .fixtures import (
    FIXTURE_EXPECTED_X,
    FIXTURE_PACKET_X,
    FixtureFamily,
    FixtureId,
    OrderTag,
    PackageOrderTag,
    RecordOrderTag,
)
from .reference import (
    Closure,
    ContractRole,
    ContractSpec,
    DeclarationShape,
    DependencyGraph,
    Evaluability,
    FailureDomain,
    Formation,
    InterfaceFailure,
    Judgment,
    Layer,
    LogicalRecord,
    MissingKind,
    ObservationKind,
    ObservationQuery,
    PairValidationResult,
    SemanticBinding,
    TrustState,
    Version,
    admit_typed_value,
    compose_records,
    evaluate_contract,
    exact_version_agreement,
    project_interface_failure,
    project_trust,
    replay,
    topological_order,
    validate_contract_spec,
    validate_binding,
    validate_declaration_shape,
    validate_model_descriptor,
    validate_packages,
    validate_pair,
)


class K3XReferenceTests(unittest.TestCase):
    def test_k3x_01_closed_evaluable_coding_contract_true(self) -> None:
        fixture_id = FixtureId(FixtureFamily.CORE_DEFINITIONAL)
        universe = FIXTURE_PACKET_X[fixture_id]
        outcome = replay(universe)
        self.assertEqual(outcome, FIXTURE_EXPECTED_X[fixture_id])
        self.assertEqual(outcome.formation, Formation.WELL_FORMED)
        self.assertEqual(outcome.closure, Closure.CLOSED)
        self.assertEqual(outcome.evaluability, Evaluability.AVAILABLE)
        self.assertEqual(outcome.result.truth, Truth.TRUE)
        contract = universe.request.contract
        record_fields = {
            record.record_kind: record.field_map()
            for record in universe.records
            if record.record_kind in {"TYPE_DECLARATION", "LITERAL", "DECLARATION", "BINDING"}
        }
        declarations = [
            record.field_map()["declaration"]
            for record in universe.records
            if record.record_kind == "TYPE_DECLARATION"
        ]
        literal = record_fields["LITERAL"]["value"]
        self.assertEqual(admit_typed_value(declarations[0], literal), Judgment("ADMITTED"))
        declaration = record_fields["DECLARATION"]["declaration"]
        binding = record_fields["BINDING"]["binding"]
        self.assertEqual(validate_declaration_shape(declaration), Judgment("WELL_FORMED"))
        self.assertEqual(validate_binding(binding), Judgment("CLOSED"))
        self.assertEqual(snapshot_of(contract.final_snapshot).value, contract.final_snapshot)
        self.assertEqual(snapshot_of("ambient").error, "NOT_A_REPOSITORY_SNAPSHOT")
        empty = RepositorySnapshot(())
        self.assertEqual(
            changes_between(empty, contract.final_snapshot).value.entries[0].kind,
            ChangeKind.CREATED,
        )
        self.assertEqual(
            changes_between(contract.final_snapshot, empty).value.entries[0].kind,
            ChangeKind.DELETED,
        )
        observation_spec = contract.task.criteria[0].arguments[0]
        for projection in ("IDENTITY", "FORMAT", "SIZE", "CONTENT"):
            result = observe(
                replace(observation_spec, projection=projection),
                contract.final_snapshot,
            )
            self.assertTrue(result.is_value)
        with self.assertRaises(FiniteCodingProfileError):
            observe(
                replace(observation_spec, projection="UNDECLARED"),
                contract.final_snapshot,
            )
        self.assertEqual(
            task_accepts(contract.task, contract.final_snapshot, contract.evidence),
            outcome.result,
        )
        spec_key = contract.model_contract.semantic_contract_key
        spec = ContractSpec(
            spec_key,
            Layer.SIGMA,
            ContractRole.PREDICATE_MEANING,
            "(TaskSpec,RepositorySnapshot,EvidenceStore)",
            frozenset({"Eval"}),
            (),
            frozenset(),
            "task_accepts",
        )
        self.assertEqual(validate_contract_spec(spec), Judgment("WELL_FORMED"))
        query = ObservationQuery("lower", ObservationKind.TERM_RESULT, "total")
        duplicate_query = replace(
            spec,
            observation_queries=(query, query),
            support=frozenset({"lower"}),
        )
        support_mismatch = replace(spec, observation_queries=(query,))
        illegal_service_query = replace(
            spec,
            owner_layer=Layer.SERVICE,
            role=ContractRole.SOUND_FRAGMENT,
            observation_queries=(replace(query, expected_kind="MODEL_CONTRACT"),),
            support=frozenset({"lower"}),
        )
        incomplete = replace(spec, primary_input_domain="")
        for invalid in (duplicate_query, support_mismatch, illegal_service_query, incomplete):
            self.assertEqual(validate_contract_spec(invalid).tag, "MALFORMED")
        self.assertEqual(
            validate_contract_spec(replace(spec, owner_layer=Layer.SERVICE)).tag,
            "MALFORMED",
        )
        self.assertEqual(
            validate_declaration_shape(replace(declaration, facet_positions=())).tag,
            "MALFORMED",
        )
        self.assertEqual(
            validate_binding(replace(binding, proper_dependencies=frozenset())).tag,
            "OPEN_BINDINGS",
        )

    def test_k3x_02_structural_identity_and_kind_collision(self) -> None:
        base = next(iter(FIXTURE_PACKET_X.values())).records[1]
        independent_equal = LogicalRecord(base.identity, base.record_kind, base.fields)
        distinct_owner = replace(
            base,
            identity=replace(
                base.identity,
                key=replace(base.identity.key, owner="another.owner"),
            ),
        )
        distinct_plugin = replace(
            base,
            identity=replace(
                base.identity,
                key=replace(base.identity.key, local="another.plugin.member"),
            ),
        )
        distinct_kind_identity = replace(
            base,
            identity=replace(
                base.identity,
                key=replace(base.identity.key, namespace="coding.type"),
            ),
            record_kind="TYPE_DECLARATION",
        )
        composed = compose_records(
            (base, independent_equal, distinct_owner, distinct_plugin, distinct_kind_identity)
        )
        self.assertEqual(len(composed.records), 4)
        self.assertFalse(composed.conflicts)
        unequal_kind_same_key = replace(base, record_kind="CONTRACT_SPEC")
        collision = compose_records((base, unequal_kind_same_key))
        self.assertFalse(collision.records)
        self.assertEqual(len(collision.conflicts), 1)
        core = next(iter(FIXTURE_PACKET_X.values()))
        core_composition = compose_records(core.records)
        missing_member_package = replace(
            core.packages[0], members=frozenset({distinct_plugin.identity})
        )
        owner_package = replace(
            core.packages[0], members=frozenset({distinct_owner.identity})
        )
        self.assertEqual(
            validate_packages((missing_member_package,), core_composition).tag,
            "MALFORMED",
        )
        owner_composition = compose_records((*core.records, distinct_owner))
        self.assertEqual(validate_packages((owner_package,), owner_composition).tag, "MALFORMED")

    def test_k3x_03_exact_version_and_model_agreement_no_fallback(self) -> None:
        fixture_id = FixtureId(FixtureFamily.CORE_DEFINITIONAL)
        contract = FIXTURE_PACKET_X[fixture_id].request.contract
        self.assertTrue(exact_version_agreement(Version((1,)), Version((1,))))
        self.assertFalse(exact_version_agreement(Version((1,)), Version((2,))))
        self.assertEqual(
            validate_model_descriptor(contract.model_contract, contract.descriptor),
            Judgment("WELL_FORMED"),
        )
        mismatched = replace(contract, binding_version=Version((2,)))
        outcome = evaluate_contract(mismatched)
        self.assertEqual(outcome.formation, Formation.MALFORMED)
        self.assertEqual(outcome.lifecycle, "VERSION_MISMATCH")
        wrong_model = replace(contract.model_contract, capability_summaries=frozenset())
        self.assertEqual(
            validate_model_descriptor(wrong_model, contract.descriptor).tag,
            "MALFORMED",
        )
        wrong_target_version = replace(
            contract.model_contract,
            target_key=replace(contract.model_contract.target_key, version=Version((2,))),
        )
        wrong_owner = replace(
            contract.model_contract,
            key=replace(contract.model_contract.key, owner="another.owner"),
        )
        self.assertEqual(
            validate_model_descriptor(wrong_target_version, contract.descriptor).tag,
            "MALFORMED",
        )
        self.assertEqual(
            validate_model_descriptor(wrong_owner, contract.descriptor).tag,
            "MALFORMED",
        )

    def test_k3x_04_declaration_binding_and_capability_are_independent(self) -> None:
        fixture_id = FixtureId(FixtureFamily.CORE_DEFINITIONAL)
        contract = FIXTURE_PACKET_X[fixture_id].request.contract
        declaration_absent = evaluate_contract(replace(contract, declared=False))
        binding_absent = evaluate_contract(replace(contract, bound=False))
        capability_absent = evaluate_contract(replace(contract, capability_present=False))
        self.assertEqual(declaration_absent.formation, Formation.MALFORMED)
        self.assertEqual(binding_absent.closure, Closure.OPEN_BINDINGS)
        self.assertEqual(capability_absent.closure, Closure.CLOSED)
        self.assertEqual(capability_absent.evaluability, Evaluability.MISSING)
        self.assertEqual(
            {declaration_absent.lifecycle, binding_absent.lifecycle, capability_absent.lifecycle},
            {"DECLARATION_ABSENT", "BINDING_ABSENT", "CAPABILITY_ABSENT"},
        )

    def test_k3x_05_pair_validation_refs_independence_and_cycle(self) -> None:
        pair_id = FixtureId(FixtureFamily.PAIR_INDEPENDENT)
        universe = FIXTURE_PACKET_X[pair_id]
        pair = universe.request.pair
        self.assertEqual(
            pair.validation_references,
            frozenset({"VALIDATION_CERTIFICATE(PCERT)", "VALIDATION_CAPABILITY(PVC)"}),
        )
        self.assertTrue(pair.validation_references.isdisjoint(pair.proper_graph.nodes))
        pair_outcome = replay(universe)
        self.assertEqual(
            pair_outcome.result,
            PairValidationResult("PAIR(refresh)", "PCERT", "PAIR_COHERENCE_ADMITTED"),
        )
        self.assertEqual(pair_outcome, FIXTURE_EXPECTED_X[pair_id])
        producers = (
            pair.subject_producers,
            pair.certificate_producers,
            pair.validation_producers,
            pair.trust_producers,
        )
        for position, producer_set in enumerate(producers):
            self.assertTrue(producer_set)
            self.assertTrue(
                all(producer_set.isdisjoint(other) for other in producers[position + 1 :])
            )
        cycle_id = FixtureId(FixtureFamily.PROPER_CYCLE_REJECTION)
        cycle_outcome = replay(FIXTURE_PACKET_X[cycle_id])
        self.assertEqual(cycle_outcome, FIXTURE_EXPECTED_X[cycle_id])
        self.assertEqual(cycle_outcome[0], Formation.MALFORMED)
        self.assertEqual(cycle_outcome[1], Closure.NOT_APPLICABLE)
        with self.assertRaisesRegex(ValueError, "duplicate dependency node"):
            topological_order(DependencyGraph(("a", "a"), (("a", ()),)))
        with self.assertRaisesRegex(ValueError, "explicit proper-dependency"):
            topological_order(DependencyGraph(("a", "b"), (("a", ()),)))
        with self.assertRaisesRegex(ValueError, "absent node"):
            topological_order(DependencyGraph(("a",), (("a", ("b",)),)))
        self.assertEqual(
            validate_pair(replace(pair, validation_references=frozenset())).tag,
            "MALFORMED",
        )
        self.assertEqual(
            validate_pair(
                replace(
                    pair,
                    validation_references=frozenset({"refresh_scope"}),
                    required_validation_references=frozenset({"refresh_scope"}),
                )
            ).tag,
            "MALFORMED",
        )

    def test_k3x_06_five_trust_states_remain_distinct(self) -> None:
        projections = {}
        for state in TrustState:
            fixture_id = FixtureId(FixtureFamily.TRUST_BRANCH, (state,))
            universe = FIXTURE_PACKET_X[fixture_id]
            projections[state] = project_trust(universe.request)
            self.assertEqual(replay(universe), FIXTURE_EXPECTED_X[fixture_id])
        self.assertIsNotNone(projections[TrustState.ADMITTED].result)
        self.assertEqual(projections[TrustState.ABSENT].evaluability, Evaluability.MISSING)
        self.assertEqual(projections[TrustState.UNDECIDED].evaluability, Evaluability.UNKNOWN)
        self.assertEqual(projections[TrustState.INCOMPATIBLE].evaluability, Evaluability.MISSING)
        self.assertEqual(projections[TrustState.FAILED].discovery, "DISCOVERY_FAILED")
        for state in TrustState:
            if state is not TrustState.ADMITTED:
                self.assertIsNone(projections[state].result)

    def test_k3x_07_false_unknown_and_failure_families_do_not_collapse(self) -> None:
        snapshot = RepositorySnapshot(())
        selector = ArtifactSelector(role="SOURCE")
        false_task = TaskSpec((Criterion(CriterionKind.ARTIFACTS_NONEMPTY, (selector,)),))
        false_result = task_accepts(false_task, snapshot, ())
        verification = VerificationSpec("missing", ObservationSpec("s", selector, "IDENTITY"))
        unknown_result = verification_passed(verification, snapshot, ())
        first = EvidenceEntry("same", "abstract_acceptance", "one")
        second = EvidenceEntry("same", "abstract_acceptance", "two")
        evaluation_error = implementation_evidence_profile(
            Eval(Truth.TRUE), Eval(Truth.TRUE), (first, second)
        )
        reasoning_error = project_interface_failure(
            InterfaceFailure(FailureDomain.REASONING, "PROTOCOL_FAILURE", frozenset({"r"}))
        )
        malformed = project_interface_failure(
            InterfaceFailure(FailureDomain.REASONING, "PROTOCOL_FAILURE", frozenset())
        )
        artifact = ArtifactContent("SOURCE", "PYTHON", 5, "same")
        populated = RepositorySnapshot((("a", artifact), ("b", artifact)))
        identity_spec = ObservationSpec("identity", selector, "IDENTITY")
        identity_result = ObservationResult("identity", (("a", "same"), ("b", "same")))
        criteria = (
            Criterion(CriterionKind.OBSERVATION_EQUALS, (identity_spec, identity_result)),
            Criterion(CriterionKind.ONE_FORMAT_OF, (selector, frozenset({"PYTHON"}))),
            Criterion(CriterionKind.ARTIFACTS_NONEMPTY, (selector,)),
            Criterion(CriterionKind.ARTIFACT_SIZE_LT, (selector, 6)),
            Criterion(CriterionKind.ARTIFACT_SIZE_AT_LEAST, (selector, 5)),
            Criterion(CriterionKind.UNIVERSAL_OBSERVATION, (identity_spec, identity_result, "EQUAL")),
            Criterion(CriterionKind.DEPENDENCY_REPRODUCIBLE, (identity_spec,)),
            Criterion(CriterionKind.ADAPTER_CORRESPONDS, (identity_spec, "FIELD_CORRESPONDENCE")),
        )
        for criterion in criteria:
            self.assertEqual(task_accepts(TaskSpec((criterion,)), populated, ()).truth, Truth.TRUE)
        complete_profile = implementation_evidence_profile(
            Eval(Truth.TRUE),
            Eval(Truth.TRUE),
            (
                EvidenceEntry("abstract", "abstract_acceptance", "a"),
                EvidenceEntry("concrete", "concrete_implementation", "c"),
            ),
        )
        self.assertEqual(complete_profile.status, "PROFILE_COMPLETE")
        projected_failures = {
            domain: project_interface_failure(
                InterfaceFailure(domain, "PROTOCOL_FAILURE", frozenset({"r"}))
            ).tag
            for domain in FailureDomain
        }
        self.assertEqual(
            set(projected_failures.values()),
            {"TERM_ERROR", "EVAL_ERROR", "PROFILE_EVALUATION_ERROR", "REASONING_ERROR"},
        )
        self.assertEqual(false_result.truth, Truth.FALSE)
        self.assertEqual(unknown_result.truth, Truth.UNKNOWN)
        self.assertEqual(evaluation_error.status, "EVALUATION_ERROR")
        self.assertEqual(reasoning_error.tag, "REASONING_ERROR")
        self.assertEqual(malformed.tag, "MALFORMED_RESULT")
        self.assertEqual(len({false_result.truth.value, unknown_result.truth.value, evaluation_error.status, reasoning_error.tag, malformed.tag}), 5)

    def test_k3x_08_trace_truth_and_authority_are_independent(self) -> None:
        selector = ArtifactSelector(role="DEPENDENCY_LOCK")
        command = EventValue(
            EventKind.COMMAND,
            (("command_id", "build"), ("purpose", "VERIFY")),
        )
        test_event = EventValue(
            EventKind.TEST,
            (("spec", "v"), ("status", VerificationStatus.PASS)),
        )
        path_change = EventValue(
            EventKind.PATH_CHANGE,
            (("path", "src/a.py"), ("change_kind", ChangeKind.CREATED)),
        )
        refresh = EventValue(
            EventKind.DEPENDENCY_REFRESH,
            (("selector", selector), ("snapshot_identity", "F")),
        )
        network = EventValue(
            EventKind.NETWORK_CONTACT,
            (("contact_class", "PUBLIC_NETWORK"), ("purpose", "FETCH")),
        )
        release = EventValue(
            EventKind.RELEASE,
            (("release_id", "release-1"), ("snapshot_identity", "F")),
        )
        forbidden = EventPattern(PatternKind.NETWORK_CLASS, ("PUBLIC_NETWORK",))
        authorized = EventPattern(PatternKind.RELEASE_IS, ("release-1", "F"))
        matches = (
            (EventPattern(PatternKind.ANY_EVENT, (EventKind.COMMAND,)), command),
            (EventPattern(PatternKind.COMMAND_IS, ("build",)), command),
            (EventPattern(PatternKind.TEST_IS, ("v", frozenset({VerificationStatus.PASS}))), test_event),
            (EventPattern(PatternKind.PATH_CHANGE_IN, (frozenset({"src/a.py"}), frozenset({ChangeKind.CREATED}))), path_change),
            (forbidden, network),
            (authorized, release),
            (EventPattern(PatternKind.REFRESHES, (selector, "F")), refresh),
        )
        for pattern, event in matches:
            self.assertEqual(event_matches(pattern, event).truth, Truth.TRUE)
        self.assertEqual(event_matches(forbidden, network).truth, Truth.TRUE)
        self.assertEqual(event_occurred(forbidden, frozenset({network})).truth, Truth.TRUE)
        self.assertEqual(event_matches(authorized, release).truth, Truth.TRUE)
        self.assertEqual(refresh_scope(refresh).truth, Truth.TRUE)
        changes = ChangeSet((ChangeEntry("lock", ChangeKind.CREATED, None, ArtifactContent("DEPENDENCY_METADATA", "LOCK", 1, "x")),))
        self.assertEqual(dependency_metadata_changed(changes).truth, Truth.TRUE)
        ordinary = ArtifactContent("SOURCE", "PYTHON", 1, "ordinary")
        self.assertEqual(
            dependency_metadata_changed(
                ChangeSet((ChangeEntry("src", ChangeKind.MODIFIED, ordinary, ordinary),))
            ).truth,
            Truth.FALSE,
        )
        authority = Judgment("AUTHORIZED", ("AUTHORITY_FACT(release)",))
        self.assertNotEqual(authority.tag, Evaluability.AVAILABLE.value)
        self.assertNotEqual(event_matches(authorized, release), authority)

    def test_k3x_09_confluence_and_all_four_permutations(self) -> None:
        confluence = []
        for order in OrderTag:
            fixture_id = FixtureId(FixtureFamily.CONFLUENCE_ORDER, (order,))
            outcome = replay(FIXTURE_PACKET_X[fixture_id])
            self.assertEqual(outcome, FIXTURE_EXPECTED_X[fixture_id])
            confluence.append(outcome)
        self.assertEqual(confluence[0], confluence[1])
        permutations = []
        for package_order in PackageOrderTag:
            for record_order in RecordOrderTag:
                fixture_id = FixtureId(FixtureFamily.PERMUTATION, (package_order, record_order))
                outcome = replay(FIXTURE_PACKET_X[fixture_id])
                self.assertEqual(outcome, FIXTURE_EXPECTED_X[fixture_id])
                permutations.append(outcome)
        self.assertEqual(len(permutations), 4)
        self.assertTrue(all(outcome == permutations[0] for outcome in permutations))

    def test_k3x_10_equal_duplicates_and_conflicts_are_order_independent(self) -> None:
        equal_outcomes = []
        conflict_outcomes = []
        for order in OrderTag:
            equal_id = FixtureId(FixtureFamily.DUPLICATE_EQUAL, (order,))
            conflict_id = FixtureId(FixtureFamily.DUPLICATE_CONFLICT, (order,))
            equal_outcomes.append(replay(FIXTURE_PACKET_X[equal_id]))
            conflict_outcomes.append(replay(FIXTURE_PACKET_X[conflict_id]))
            self.assertEqual(equal_outcomes[-1], FIXTURE_EXPECTED_X[equal_id])
            self.assertEqual(conflict_outcomes[-1], FIXTURE_EXPECTED_X[conflict_id])
        self.assertEqual(equal_outcomes[0], equal_outcomes[1])
        self.assertEqual(conflict_outcomes[0], conflict_outcomes[1])
        self.assertEqual(equal_outcomes[0].formation, Formation.WELL_FORMED)
        self.assertEqual(conflict_outcomes[0].formation, Formation.MALFORMED)

    def test_k3x_11_all_42_missing_baselines_and_variants(self) -> None:
        self.assertEqual(len(MissingKind), 42)
        for kind in MissingKind:
            base_id = FixtureId(FixtureFamily.MISSING_BASE, (kind,))
            variant_id = FixtureId(FixtureFamily.MISSING_VARIANT, (kind,))
            baseline = FIXTURE_PACKET_X[base_id]
            variant = FIXTURE_PACKET_X[variant_id]
            target = baseline.request.target
            self.assertEqual(sum(record.identity == target for record in baseline.records), 1)
            self.assertEqual(sum(record.identity == target for record in variant.records), 0)
            self.assertEqual(replay(baseline), FIXTURE_EXPECTED_X[base_id])
            self.assertEqual(replay(variant), FIXTURE_EXPECTED_X[variant_id])
        lexical = FIXTURE_PACKET_X[
            FixtureId(FixtureFamily.MISSING_VARIANT, (MissingKind.EXTRANEOUS_LEXICAL_BINDING,))
        ]
        self.assertTrue(any(record.record_kind == "LEXICAL_BINDING" for record in lexical.records))
        for kind, replacement_kind in (
            (MissingKind.LIFECYCLE, "LIFECYCLE"),
            (MissingKind.CONFLICT, "CONFLICT"),
        ):
            variant = FIXTURE_PACKET_X[FixtureId(FixtureFamily.MISSING_VARIANT, (kind,))]
            self.assertEqual(sum(record.record_kind == replacement_kind for record in variant.records), 1)

    def test_k3x_12_every_tagged_universe_replays_independently(self) -> None:
        self.assertEqual(set(FIXTURE_PACKET_X), set(FIXTURE_EXPECTED_X))
        self.assertEqual(len(FIXTURE_PACKET_X), 102)
        self.assertEqual(len(FIXTURE_EXPECTED_X), 102)
        for fixture_id, universe in FIXTURE_PACKET_X.items():
            self.assertEqual(replay(universe), FIXTURE_EXPECTED_X[fixture_id], fixture_id)

    def test_k3x_13_undeclared_ambient_access_precedes_truth(self) -> None:
        calls: list[str] = []

        def meaning() -> Eval:
            calls.append("called")
            return Eval(Truth.TRUE)

        allowed = frozenset({"task", "final_snapshot"})
        for forbidden in ("repository", "evidence", "expected_answer"):
            with self.assertRaisesRegex(UndeclaredAccessError, forbidden):
                invoke_with_declared_access(
                    frozenset({"task", "final_snapshot", forbidden}),
                    allowed,
                    meaning,
                    (),
                )
        self.assertEqual(calls, [])
        self.assertEqual(
            invoke_with_declared_access(allowed, allowed, meaning, ()),
            Eval(Truth.TRUE),
        )
        self.assertEqual(calls, ["called"])
        with self.assertRaisesRegex(TypeError, "meaning must be callable"):
            invoke_with_declared_access(allowed, allowed, "not-callable", ())


if __name__ == "__main__":
    unittest.main()
