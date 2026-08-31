"""Executable checks for the exact finite K3-X profile."""

from dataclasses import replace
import unittest

from . import coding_plugin as cp
from . import fixtures as fx
from . import reference as ref


def _rewrite(universe: ref.Universe, replacements: dict[ref.RecordIdentity, ref.LogicalRecord | None]) -> ref.Universe:
    def one(record: ref.LogicalRecord) -> ref.LogicalRecord | None:
        if record.identity in replacements:
            return replacements[record.identity]
        if not isinstance(record.value, ref.PluginPackage):
            return record
        package = record.value
        def members(values: tuple[ref.LogicalRecord, ...]) -> tuple[ref.LogicalRecord, ...]:
            return tuple(updated for item in values if (updated := one(item)) is not None)
        return replace(record, value=replace(
            package,
            declarations=members(package.declarations),
            bindings=members(package.bindings),
            model_contracts=members(package.model_contracts),
            contract_specs=members(package.contract_specs),
            services=members(package.services),
            certificates=members(package.certificates),
            other_records=members(package.other_records),
        ))
    return replace(universe, records=tuple(updated for item in universe.records if (updated := one(item)) is not None))


def _at(universe: ref.Universe, identity: ref.RecordIdentity) -> ref.LogicalRecord:
    item = ref.compose_records(universe.records).at(identity)
    if item is None:
        raise AssertionError(f"missing test construction record {identity}")
    return item


class K3XReferenceTests(unittest.TestCase):
    def test_k3x_01_core_definitional_and_closed_coding_values(self) -> None:
        construction = fx.core_construction()
        replayed = ref.replay(construction.universe)
        self.assertIsInstance(replayed, ref.CoreReplay)
        self.assertEqual((replayed.formation, replayed.closure, replayed.evaluability), (ref.Formation.WELL_FORMED, ref.Closure.CLOSED, ref.Evaluability.AVAILABLE))
        self.assertEqual(replayed.result.truth, cp.Truth.TRUE)

        empty_package = replace(_at(construction.universe, construction.package), value=replace(_at(construction.universe, construction.package).value, declarations=(), bindings=(), model_contracts=(), contract_specs=(), services=()))
        empty_result = ref.replay(_rewrite(construction.universe, {construction.package: empty_package}))
        self.assertNotEqual(empty_result, replayed)
        self.assertEqual(empty_result.formation, ref.Formation.MALFORMED)
        removed_result = ref.replay(_rewrite(construction.universe, {construction.package: None}))
        self.assertEqual(removed_result.formation, ref.Formation.MALFORMED)

        missing_path = cp.Path((cp.PathSegment("missing.py"),))
        missing_spec = cp.ObservationSpec(cp.ObservationSpecTag.ARTIFACT_VIEW, cp.ArtifactSelector(cp.SelectorTag.PATHS_WITH_ROLE, frozenset({missing_path}), cp.ArtifactRole.SOURCE), cp.ArtifactProjection(cp.ProjectionTag.CONTENT))
        absent = cp.observe(missing_spec, construction.snapshot).value
        self.assertEqual(absent.values[0][1].tag, cp.ObservationValueTag.ABSENT)
        wrong = cp.RepositorySnapshot(((missing_path, cp.ArtifactContent(cp.ArtifactTag.TEXT, cp.ArtifactRole.CONFIGURATION, cp.Format.TEXT, cp.ByteSize(1), cp.ContentIdentity("cfg"))),))
        self.assertEqual(cp.observe(missing_spec, wrong).value.values[0][1].tag, cp.ObservationValueTag.ROLE_MISMATCH)
        field_spec = replace(missing_spec, selector=cp.ArtifactSelector(cp.SelectorTag.PATHS, frozenset({missing_path})), projection=cp.ArtifactProjection(cp.ProjectionTag.STRUCTURED_FIELD, cp.FieldId("name")))
        self.assertEqual(cp.observe(field_spec, wrong).value.values[0][1].tag, cp.ObservationValueTag.PROJECTION_MISMATCH)

        verification = next(iter(construction.evidence)).payload.value
        fail_ref = cp.EvidenceRef("auditor", "coding", "verification/fail", cp.VERIFICATION_SCHEMA)
        fail_record = replace(verification, status=cp.VerificationStatus.FAIL, evidence_refs=frozenset({fail_ref}))
        conflict_evidence = construction.evidence | frozenset({cp.CodingEvidenceEntry(fail_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.VERIFICATION, fail_record))})
        conflict = cp.verification_passed(verification.spec, construction.snapshot, conflict_evidence)
        self.assertIsNone(conflict.truth)
        self.assertIn("OPPOSITE_DECISIVE_RECORD_CONFLICT", conflict.errors)
        wrong_snapshot_ref = cp.EvidenceRef("auditor", "coding", "verification/wrong-snapshot", cp.VERIFICATION_SCHEMA)
        wrong_snapshot_record = replace(verification, snapshot_identity=cp.RepositorySnapshot(()), evidence_refs=frozenset({wrong_snapshot_ref}))
        wrong_snapshot_entry = cp.CodingEvidenceEntry(wrong_snapshot_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.VERIFICATION, wrong_snapshot_record))
        self.assertEqual(cp.verification_passed(verification.spec, construction.snapshot, frozenset({wrong_snapshot_entry})).truth, cp.Truth.UNKNOWN)
        wrong_observation_ref = cp.EvidenceRef("auditor", "coding", "verification/wrong-observation", cp.VERIFICATION_SCHEMA)
        wrong_observation = replace(verification.observation, values=((next(iter(verification.observation.values))[0], cp.ObservationValue(cp.ObservationValueTag.ABSENT)),))
        wrong_observation_record = replace(verification, observation=wrong_observation, evidence_refs=frozenset({wrong_observation_ref}))
        wrong_observation_entry = cp.CodingEvidenceEntry(wrong_observation_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.VERIFICATION, wrong_observation_record))
        self.assertEqual(cp.verification_passed(verification.spec, construction.snapshot, frozenset({wrong_observation_entry})).truth, cp.Truth.UNKNOWN)
        inconclusive_ref = cp.EvidenceRef("auditor", "coding", "verification/inconclusive", cp.VERIFICATION_SCHEMA)
        inconclusive_record = replace(verification, status=cp.VerificationStatus.INCONCLUSIVE, evidence_refs=frozenset({inconclusive_ref}))
        inconclusive_entry = cp.CodingEvidenceEntry(inconclusive_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.VERIFICATION, inconclusive_record))
        self.assertEqual(cp.verification_passed(verification.spec, construction.snapshot, frozenset({inconclusive_entry})).truth, cp.Truth.UNKNOWN)

    def test_k3x_02_exact_identity_equal_coalescence_and_conflict(self) -> None:
        declaration_id = fx.rid(ref.RecordKind.DECLARATION, "d", namespace="identity")
        shape = ref.DeclarationShape(declaration_id.key, fx.key("s", namespace="identity"), "PREDICATE", (), "BOOL", (), frozenset())
        left = ref.LogicalRecord(declaration_id, shape)
        independently_equal = ref.LogicalRecord(ref.RecordIdentity(ref.RecordKind.DECLARATION, fx.key("d", namespace="identity")), replace(shape))
        coalesced = ref.compose_records((left, independently_equal))
        self.assertEqual(len(coalesced.records), 1)
        self.assertFalse(coalesced.conflicts)
        kind_distinct = ref.LogicalRecord(ref.RecordIdentity(ref.RecordKind.SYMBOL, declaration_id.key), shape)
        owner_distinct_id = fx.rid(ref.RecordKind.DECLARATION, "d", owner="other.owner", namespace="identity")
        owner_distinct = ref.LogicalRecord(owner_distinct_id, replace(shape, declaration_key=owner_distinct_id.key, symbol_key=fx.key("s", "other.owner", "identity")))
        separated = ref.compose_records((left, kind_distinct, owner_distinct))
        self.assertEqual(len(separated.records), 3)
        unequal = ref.LogicalRecord(declaration_id, replace(shape, facet_positions=(frozenset({"final"}),)))
        forward = ref.compose_records((left, unequal))
        reverse = ref.compose_records((unequal, left))
        self.assertEqual(forward, reverse)
        self.assertEqual(len(forward.conflicts), 1)
        with self.assertRaises(TypeError):
            ref.compose_records((ref.LogicalRecord(declaration_id, ref.NamedCarrier("wrong complete kind")),))

    def test_k3x_03_exact_versions_and_complete_descriptor_validation(self) -> None:
        self.assertTrue(ref.exact_version_agreement(fx.V1, fx.V1))
        self.assertFalse(ref.exact_version_agreement(fx.V1, fx.V2))
        construction = fx.core_construction()
        request = _at(construction.universe, construction.request)
        version_mismatch = _rewrite(construction.universe, {construction.request: replace(request, value=replace(request.value, requested_version=fx.V2))})
        replayed = ref.replay(version_mismatch)
        self.assertEqual((replayed.formation, replayed.lifecycle), (ref.Formation.MALFORMED, "VERSION_MISMATCH"))
        composition = ref.compose_records(construction.universe.records)
        model = _at(construction.universe, construction.model).value
        descriptor = _at(construction.universe, construction.capability).value
        mutations = (
            replace(descriptor, abi_version=fx.V2),
            replace(descriptor, plugin_key=fx.key("other-plugin", namespace="plugin")),
            replace(descriptor, supported_judgments=frozenset({"WRONG"})),
            replace(descriptor, supported_targets=frozenset()),
            replace(descriptor, sound_fragment=construction.sigma_spec),
            replace(descriptor, proper_dependencies=frozenset({construction.binding}), dependency_closure=frozenset()),
            replace(descriptor, validation_references=frozenset({construction.binding})),
            replace(descriptor, required_trust_roots=frozenset({construction.binding})),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assertEqual(ref.validate_model_descriptor(model, mutation, composition).tag, "MALFORMED")
        bad_model = replace(model, exact_version=fx.V2)
        self.assertEqual(ref.validate_model_descriptor(bad_model, descriptor, composition).tag, "MALFORMED")
        bad_summary = replace(model, capability_summaries=frozenset())
        self.assertEqual(ref.validate_model_descriptor(bad_summary, descriptor, composition).tag, "MALFORMED")
        model_mutations = (
            replace(model, exact_symbol_key=fx.key("wrong-symbol", namespace="coding.symbol")),
            replace(model, exact_argument_types=()),
            replace(model, exact_result_kind="TERM_RESULT"),
            replace(model, exact_facet_positions=(frozenset(),)),
            replace(model, evidence_contract=construction.sound_spec),
            replace(model, unknown_contract=construction.sound_spec),
            replace(model, error_contract=construction.sound_spec),
            replace(model, semantic_contract=construction.sound_spec),
        )
        for mutation in model_mutations:
            with self.subTest(model_mutation=mutation):
                self.assertEqual(ref.validate_model_descriptor(mutation, descriptor, composition).tag, "MALFORMED")
        with self.assertRaises(ValueError):
            replace(model, explanatory_text="invented prose")  # type: ignore[arg-type]
        descriptor_record = _at(construction.universe, construction.capability)
        bad_descriptor_record = replace(descriptor_record, value=replace(descriptor, abi_version=fx.V2))
        malformed_package = ref.replay(_rewrite(construction.universe, {construction.capability: bad_descriptor_record}))
        self.assertIsInstance(malformed_package, ref.CompositionReplay)
        self.assertEqual(malformed_package.formation, ref.Formation.MALFORMED)

    def test_k3x_04_declaration_binding_and_capability_are_derived(self) -> None:
        construction = fx.core_construction()
        environment_record = _at(construction.universe, construction.semantic_environment)
        dependency_record = _at(construction.universe, construction.dependency_environment)

        no_declaration_env = replace(environment_record, value=replace(environment_record.value, declarations=(), mechanically_extracted_dependencies=frozenset({construction.binding})))
        no_declaration_dep = replace(dependency_record, value=replace(dependency_record.value, members=frozenset({construction.binding})))
        no_declaration = _rewrite(construction.universe, {construction.declaration: None, construction.semantic_environment: no_declaration_env, construction.dependency_environment: no_declaration_dep})
        declaration_result = ref.replay(no_declaration)
        self.assertEqual((declaration_result.formation, declaration_result.lifecycle), (ref.Formation.MALFORMED, "DECLARATION_ABSENT"))

        no_binding_env = replace(environment_record, value=replace(environment_record.value, bindings=(), mechanically_extracted_dependencies=frozenset({construction.declaration})))
        no_binding_dep = replace(dependency_record, value=replace(dependency_record.value, members=frozenset({construction.declaration})))
        no_binding = _rewrite(construction.universe, {construction.binding: None, construction.semantic_environment: no_binding_env, construction.dependency_environment: no_binding_dep})
        binding_result = ref.replay(no_binding)
        self.assertEqual((binding_result.formation, binding_result.closure, binding_result.lifecycle), (ref.Formation.WELL_FORMED, ref.Closure.OPEN_BINDINGS, "BINDING_ABSENT"))

        model_record = _at(construction.universe, construction.model)
        no_capability_model = replace(model_record, value=replace(model_record.value, capability_summaries=frozenset()))
        no_capability = _rewrite(construction.universe, {construction.capability: None, construction.model: no_capability_model})
        capability_result = ref.replay(no_capability)
        self.assertEqual((capability_result.closure, capability_result.evaluability, capability_result.lifecycle), (ref.Closure.CLOSED, ref.Evaluability.MISSING, "CAPABILITY_ABSENT"))
        empty_environment = replace(environment_record, value=ref.SemanticEnvironment((), ()))
        self.assertEqual(ref.replay(_rewrite(construction.universe, {construction.semantic_environment: empty_environment})).formation, ref.Formation.MALFORMED)

    def test_k3x_05_pair_producers_validation_refs_and_proper_cycle(self) -> None:
        construction = fx.pair_construction()
        admitted = ref.replay(construction.universe)
        self.assertIsInstance(admitted, ref.PairReplay)
        self.assertEqual(admitted.result.result, "PAIR_COHERENCE_ADMITTED")
        binding = _at(construction.universe, construction.pair_binding)
        self.assertEqual(len(binding.value.validation_references), 2)
        self.assertFalse(binding.value.validation_references & binding.value.proper_subjects)

        removed_producer = _rewrite(construction.universe, {construction.producer_records[1].identity: None})
        self.assertEqual(ref.replay(removed_producer).details[0], "INCOMPLETE_PRODUCER_SET")
        cert_producer = construction.producer_records[1]
        self_trust = replace(cert_producer, value=replace(cert_producer.value, producer="capknow.semantic"))
        self.assertEqual(ref.replay(_rewrite(construction.universe, {cert_producer.identity: self_trust})).details[0], "PAIR_SELF_TRUST")
        equal_sets = replace(construction.producer_records[2], value=replace(construction.producer_records[2].value, producer="capknow.audit.pair-proof"))
        self.assertEqual(ref.replay(_rewrite(construction.universe, {construction.producer_records[2].identity: equal_sets})).details[0], "PAIR_SELF_TRUST")
        missing_validation = _rewrite(construction.universe, {next(iter(construction.validation_references)): None})
        self.assertEqual(ref.replay(missing_validation).details[0], "MISSING_VALIDATION_REFERENCE")
        certificate = _at(construction.universe, construction.certificate)
        wrong_subject = replace(certificate, value=replace(certificate.value, subject=construction.request))
        self.assertEqual(ref.replay(_rewrite(construction.universe, {construction.certificate: wrong_subject})).details[0], "PAIR_CERTIFICATE_SUBJECT_OR_JUDGMENT")
        empty_pair_package = next(record for record in construction.universe.records if isinstance(record.value, ref.PluginPackage))
        empty_pair_package = replace(empty_pair_package, value=replace(empty_pair_package.value, declarations=(), bindings=(), contract_specs=()))
        self.assertNotEqual(ref.replay(_rewrite(construction.universe, {empty_pair_package.identity: empty_pair_package})), admitted)

        cycle = ref.replay(fx.cycle_universe())
        self.assertEqual(cycle[:2], (ref.Formation.MALFORMED, ref.Closure.NOT_APPLICABLE))
        self.assertEqual(cycle[2], ref.Judgment("MALFORMED", ("dependency cycle",)))

    def test_k3x_06_five_trust_lifecycle_and_discovery_branches(self) -> None:
        projections = {}
        for tag in fx.TrustFixtureTag:
            construction = fx.core_construction(tag)
            projections[tag] = ref.replay(construction.universe)
        self.assertEqual(projections[fx.TrustFixtureTag.ADMITTED].evaluability, ref.Evaluability.AVAILABLE)
        self.assertEqual(projections[fx.TrustFixtureTag.ABSENT].evaluability, ref.Evaluability.MISSING)
        self.assertEqual(projections[fx.TrustFixtureTag.ABSENT].lifecycle, "TRUST_ROOT_ABSENT")
        self.assertEqual(projections[fx.TrustFixtureTag.UNDECIDED].evaluability, ref.Evaluability.UNKNOWN)
        self.assertEqual(projections[fx.TrustFixtureTag.INCOMPATIBLE].evaluability, ref.Evaluability.MISSING)
        self.assertEqual(projections[fx.TrustFixtureTag.FAILED].lifecycle, "DISCOVERY_FAILED")
        self.assertTrue(all(projections[tag].result is None for tag in fx.TrustFixtureTag if tag is not fx.TrustFixtureTag.ADMITTED))
        admitted = fx.core_construction()
        without_root = _rewrite(admitted.universe, {admitted.trust_root: None})
        self.assertEqual(ref.replay(without_root).lifecycle, "TRUST_ROOT_ABSENT")
        without_trust = _rewrite(admitted.universe, {admitted.trust_environment: None})
        self.assertEqual(ref.replay(without_trust).formation, ref.Formation.MALFORMED)

    def test_k3x_07_false_unknown_errors_malformed_and_profile_projection(self) -> None:
        construction = fx.core_construction()
        empty_selector = cp.ArtifactSelector(cp.SelectorTag.PATHS, frozenset({cp.Path((cp.PathSegment("absent"),))}))
        false_task = cp.TaskSpec(frozenset({cp.ArtifactsNonempty(empty_selector)}))
        self.assertEqual(cp.task_accepts(false_task, construction.snapshot, frozenset()).truth, cp.Truth.FALSE)
        verification = next(iter(construction.evidence)).payload.value.spec
        unknown = cp.task_accepts(cp.TaskSpec(required_verifications=frozenset({verification})), construction.snapshot, frozenset())
        self.assertEqual(unknown.truth, cp.Truth.UNKNOWN)
        self.assertFalse(unknown.errors)
        with self.assertRaises(ValueError):
            cp.Eval(cp.Truth.TRUE, errors=frozenset({"not both"}))
        self.assertEqual(ref.project_interface_failure(ref.InterfaceFailure(ref.FailureDomain.PREDICATE_EVALUATION, "BROKEN", frozenset({"r"}))).tag, "EVAL_ERROR")
        self.assertEqual(ref.project_interface_failure(ref.InterfaceFailure(ref.FailureDomain.REASONING, "BROKEN", frozenset({"r"}))).tag, "REASONING_ERROR")

        empty_task = cp.TaskSpec()
        task_result = cp.Eval(cp.Truth.TRUE)
        abstract = cp.AbstractCoverageResult(cp.AbstractCoverageTag.REASONING, cp.ReasoningResult(cp.ReasoningTag.ADMITTED_JUDGMENT, "cert", "CONSISTENCY_SAT"))
        abs_ref = cp.EvidenceRef("reasoner", "coding", "abstract", cp.IMPLEMENTATION_PROFILE_SCHEMA)
        conc_ref = cp.EvidenceRef("builder", "coding", "concrete", cp.IMPLEMENTATION_PROFILE_SCHEMA)
        abs_item = cp.ImplementationEvidence(cp.ImplementationEvidenceTag.ABSTRACT_ACCEPTANCE, "contract", construction.snapshot, certificate_key="cert")
        conc_item = cp.ImplementationEvidence(cp.ImplementationEvidenceTag.CONCRETE_IMPLEMENTATION, "contract", construction.snapshot, implementation_identity="implementation")
        entries = frozenset({cp.CodingEvidenceEntry(abs_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.IMPLEMENTATION_PROFILE, abs_item)), cp.CodingEvidenceEntry(conc_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.IMPLEMENTATION_PROFILE, conc_item))})
        subject = cp.ImplementationCoverageSubject("contract", empty_task, construction.snapshot, entries, task_result, abstract)
        self.assertEqual(cp.implementation_evidence_profile(subject).tag, cp.ProfileTag.COMPLETE)
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, evidence_store=frozenset())).tag, cp.ProfileTag.INCOMPLETE)
        pending_ref = cp.EvidenceRef("builder", "coding", "pending", cp.IMPLEMENTATION_PROFILE_SCHEMA)
        pending = cp.ImplementationEvidence(cp.ImplementationEvidenceTag.DIMENSION_PENDING, "contract", construction.snapshot, dimension="concrete_implementation_evidence", reason="PENDING")
        pending_entry = cp.CodingEvidenceEntry(pending_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.IMPLEMENTATION_PROFILE, pending))
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, evidence_store=frozenset({pending_entry}))).tag, cp.ProfileTag.UNKNOWN)
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, task_result=cp.Eval(cp.Truth.FALSE))).tag, cp.ProfileTag.EVALUATION_ERROR)
        reasoning_error = cp.AbstractCoverageResult(cp.AbstractCoverageTag.REASONING, cp.ReasoningResult(cp.ReasoningTag.REASONING_ERROR, reasons=frozenset({"REASONER_FAILED"})))
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, abstract_result=reasoning_error)).tag, cp.ProfileTag.INCOMPLETE)
        wrong_snapshot = cp.RepositorySnapshot(())
        wrong_item = replace(conc_item, snapshot_identity=wrong_snapshot)
        wrong_entry = cp.CodingEvidenceEntry(conc_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.IMPLEMENTATION_PROFILE, wrong_item))
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, evidence_store=frozenset({wrong_entry}))).tag, cp.ProfileTag.INCOMPLETE)
        wrong_contract = replace(conc_item, contract_identity="other")
        wrong_contract_entry = cp.CodingEvidenceEntry(conc_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.IMPLEMENTATION_PROFILE, wrong_contract))
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, evidence_store=frozenset({wrong_contract_entry}))).tag, cp.ProfileTag.INCOMPLETE)
        wrong_schema_ref = cp.EvidenceRef("builder", "coding", "bad-schema", cp.VERIFICATION_SCHEMA)
        wrong_schema_entry = cp.CodingEvidenceEntry(wrong_schema_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.IMPLEMENTATION_PROFILE, conc_item))
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, evidence_store=frozenset({wrong_schema_entry}))).tag, cp.ProfileTag.EVALUATION_ERROR)

    def test_k3x_08_trace_truth_event_admission_and_change_metadata(self) -> None:
        construction = fx.core_construction()
        command = cp.EventValue(cp.EventKind.COMMAND, cp.CommandEventPayload("build", "verification"))
        command_pattern = cp.EventPattern(cp.PatternKind.COMMAND_IS, command_id="build")
        self.assertEqual(cp.event_matches(command_pattern, command).truth, cp.Truth.TRUE)
        self.assertEqual(cp.event_matches(replace(command_pattern, command_id="deploy"), command).truth, cp.Truth.FALSE)
        self.assertEqual(cp.event_occurred(command_pattern, frozenset({cp.TraceEvent(command, "agent")})).truth, cp.Truth.TRUE)
        verification = next(iter(construction.evidence)).payload.value
        test_event = cp.EventValue(cp.EventKind.TEST, cp.TestEventPayload(verification.spec, construction.snapshot, cp.VerificationStatus.PASS, verification.evidence_refs))
        test_pattern = cp.EventPattern(cp.PatternKind.TEST_IS, verification_spec=verification.spec, statuses=frozenset({cp.VerificationStatus.PASS}))
        self.assertEqual(cp.event_matches(test_pattern, test_event).truth, cp.Truth.TRUE)
        with self.assertRaises(ValueError):
            cp.EventValue(cp.EventKind.COMMAND, ("command_id", "a", "command_id", "b"))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            cp.EventValue(cp.EventKind.RELEASE, cp.CommandEventPayload("x", "y"))

        path_created = cp.Path((cp.PathSegment("created"),))
        path_deleted = cp.Path((cp.PathSegment("deleted"),))
        path_modified = cp.Path((cp.PathSegment("modified"),))
        old = cp.ArtifactContent(cp.ArtifactTag.TEXT, cp.ArtifactRole.DEPENDENCY_METADATA, cp.Format.TEXT, cp.ByteSize(1), cp.ContentIdentity("old"))
        new = replace(old, content=cp.ContentIdentity("new"))
        before = cp.RepositorySnapshot(((path_deleted, old), (path_modified, old)))
        after = cp.RepositorySnapshot(((path_created, new), (path_modified, new)))
        changes = cp.changes_between(before, after).value
        kinds = {path: entry.kind for path, entry in changes.entries}
        self.assertEqual(kinds, {path_created: cp.ChangeKind.CREATED, path_deleted: cp.ChangeKind.DELETED, path_modified: cp.ChangeKind.MODIFIED})
        self.assertEqual(cp.dependency_metadata_changed(changes).truth, cp.Truth.TRUE)
        refresh_selector = cp.ArtifactSelector(cp.SelectorTag.ROLE, role=cp.ArtifactRole.DEPENDENCY_LOCK)
        refresh = cp.EventValue(cp.EventKind.DEPENDENCY_REFRESH, cp.DependencyRefreshEventPayload(refresh_selector, after))
        self.assertEqual(cp.refresh_scope(refresh).truth, cp.Truth.TRUE)
        source_refresh = replace(refresh, payload=replace(refresh.payload, selector=cp.ArtifactSelector(cp.SelectorTag.ROLE, role=cp.ArtifactRole.SOURCE)))
        self.assertEqual(cp.refresh_scope(source_refresh).truth, cp.Truth.FALSE)

    def test_k3x_09_confluence_contractspec_graph_errors_and_permutations(self) -> None:
        forward = fx.confluence_construction(fx.OrderTag.FORWARD)
        reverse = fx.confluence_construction(fx.OrderTag.REVERSE)
        forward_result = ref.replay(forward.universe)
        reverse_result = ref.replay(reverse.universe)
        self.assertEqual(forward_result, reverse_result)
        self.assertEqual(len(forward_result.observations), 2)
        absent_node = fx.rid(ref.RecordKind.OBSERVATION_NODE, "absent", namespace="confluence")
        with self.assertRaisesRegex(ValueError, "absent or wrong-kind"):
            ref.replay(replace(forward.universe, request=replace(forward.universe.request, nodes=(forward.node_one, absent_node))))
        wrong_kind_node = ref.RecordIdentity(ref.RecordKind.DECLARATION, forward.node_two.key)
        with self.assertRaisesRegex(ValueError, "absent or wrong-kind"):
            ref.replay(replace(forward.universe, request=replace(forward.universe.request, nodes=(forward.node_one, wrong_kind_node))))
        node_two = _at(forward.universe, forward.node_two)
        spec_two = _at(forward.universe, node_two.value.contract_spec)
        malformed_spec = replace(spec_two, value=replace(spec_two.value, support=frozenset()))
        with self.assertRaisesRegex(ValueError, "malformed ContractSpec"):
            ref.replay(_rewrite(forward.universe, {spec_two.identity: malformed_spec}))
        service_bad_kind = replace(spec_two.value, owner_layer=ref.Layer.SERVICE, role=ref.ContractRole.SOUND_FRAGMENT, observation_queries=(ref.ObservationQuery(forward.node_one, ref.ObservationKind.PROFILE_RESULT, ("input",)),), support=frozenset({forward.node_one}))
        self.assertEqual(ref.validate_contract_spec(service_bad_kind).tag, "WELL_FORMED")
        duplicate_query = replace(service_bad_kind, observation_queries=service_bad_kind.observation_queries * 2)
        self.assertEqual(ref.validate_contract_spec(duplicate_query).details[0], "DUPLICATE_OBSERVATION_QUERY")
        permutation_results = [ref.replay(fx.permutation_universe(package_order, record_order)) for package_order in fx.PackageOrderTag for record_order in fx.RecordOrderTag]
        self.assertTrue(all(result.composition == permutation_results[0].composition for result in permutation_results))

    def test_k3x_10_duplicate_equal_and_conflict_are_order_independent(self) -> None:
        equal_forward = ref.replay(fx.duplicate_universe(False, fx.OrderTag.FORWARD))
        equal_reverse = ref.replay(fx.duplicate_universe(False, fx.OrderTag.REVERSE))
        self.assertEqual(equal_forward, equal_reverse)
        self.assertFalse(equal_forward.composition.conflicts)
        conflict_forward = ref.replay(fx.duplicate_universe(True, fx.OrderTag.FORWARD))
        conflict_reverse = ref.replay(fx.duplicate_universe(True, fx.OrderTag.REVERSE))
        self.assertEqual(conflict_forward, conflict_reverse)
        self.assertEqual(conflict_forward.formation, ref.Formation.MALFORMED)
        self.assertEqual(len(conflict_forward.composition.conflicts), 1)
        self.assertEqual(len(conflict_forward.composition.conflicts[0].unequal_records), 2)

    def test_k3x_11_all_42_literal_missing_reconstructions(self) -> None:
        self.assertEqual(len(fx.MissingRowId), 42)
        for row in fx.MissingRowId:
            with self.subTest(row=row):
                construction = fx.missing_construction(row)
                baseline_composition = ref.compose_records(construction.baseline.records)
                variant_composition = ref.compose_records(construction.variant.records)
                self.assertIsNotNone(baseline_composition.at(construction.target))
                self.assertIsNone(variant_composition.at(construction.target))
                base = ref.replay(construction.baseline)
                variant = ref.replay(construction.variant)
                self.assertEqual(base.result.tag, "PRESENT")
                self.assertEqual(variant.result, fx._MISSING_ASSERTIONS[row])
                empty = ref.replay(replace(construction.variant, records=()))
                self.assertEqual(empty.result.tag, "MALFORMED_CONTEXT")
                if construction.variant_container is not None:
                    package = _at(construction.variant, construction.variant_container)
                    empty_package = replace(package, value=replace(package.value, declarations=(), bindings=(), model_contracts=(), contract_specs=(), services=(), certificates=(), other_records=()))
                    emptied = ref.replay(_rewrite(construction.variant, {construction.variant_container: empty_package}))
                    self.assertEqual(emptied.result.tag, "MALFORMED_CONTEXT")
        lexical = fx.missing_construction(fx.MissingRowId.EXTRANEOUS_LEXICAL_BINDING)
        self.assertEqual(ref.replay(lexical.variant).result.details[0], "EXTRANEOUS_LEXICAL_BINDING")

    def test_k3x_12_all_102_replays_without_identifier_or_assertion_input(self) -> None:
        packet = fx.fixture_packet()
        assertions = fx.assertion_results()
        self.assertEqual(set(packet), set(assertions))
        self.assertEqual(len(packet), 102)
        self.assertEqual(sum(identifier.family is fx.FixtureFamily.MISSING_BASE for identifier in packet), 42)
        self.assertEqual(sum(identifier.family is fx.FixtureFamily.MISSING_VARIANT for identifier in packet), 42)
        for identifier, universe in packet.items():
            with self.subTest(identifier=identifier):
                self.assertEqual(ref.replay(universe), assertions[identifier])
                self.assertFalse(any(isinstance(value, fx.FixtureId) for value in universe.records))

    def test_k3x_13_declared_access_and_static_oracle_exclusions(self) -> None:
        for requested in (frozenset({"repository"}), frozenset({"evidence"}), frozenset({"hidden_assertion"})):
            with self.subTest(requested=requested), self.assertRaises(cp.UndeclaredAccessError):
                cp.invoke_with_declared_access(requested, frozenset(), lambda: cp.Truth.TRUE, ())
        self.assertEqual(cp.invoke_with_declared_access(frozenset({"final"}), frozenset({"final"}), lambda value: value, (cp.Truth.TRUE,)), cp.Truth.TRUE)


if __name__ == "__main__":
    unittest.main()
