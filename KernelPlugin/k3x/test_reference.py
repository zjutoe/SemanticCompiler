"""Executable checks for the exact finite K3-X profile."""

import ast
from dataclasses import fields, is_dataclass, replace
import inspect
import unittest

from . import coding_plugin as cp
from . import fixtures as fx
from . import reference as ref


_ASSERTED_TASK_TYPES = frozenset({
    "ArtifactBodyKind", "ArtifactContent", "ArtifactProjection",
    "ArtifactRole", "ArtifactSelector", "BehaviorValue", "ByteSize",
    "ContentIdentity", "Coverage", "Criterion", "FieldId", "FieldValue",
    "Format", "ObservationRelation", "ObservationResult", "ObservationSpec",
    "ObservationValue", "Path", "PathSegment", "PathSet",
    "RepositorySnapshot", "SubjectId", "TaskSpec", "VerificationSpec",
})
_ASSERTED_CONFLUENCE_TYPES = frozenset({
    "ArtifactBodyKind", "ArtifactContent", "ArtifactProjection",
    "ArtifactRole", "ArtifactSelector", "BehaviorValue", "ByteSize",
    "ChangeEntry", "ChangeSet", "ContentIdentity", "Coverage", "FieldId",
    "FieldValue", "Format", "ObservationResult", "ObservationSpec",
    "ObservationValue", "Path", "PathSegment", "PathSet",
    "RepositorySnapshot", "SubjectId",
})


def _asserted_syntax_keys(kind: str) -> frozenset[ref.K1SyntaxKey]:
    type_names = (_ASSERTED_CONFLUENCE_TYPES
                  if kind == "confluence" else _ASSERTED_TASK_TYPES)
    symbols = {
        "task": {"SP(task_accepts)"},
        "bounds": {"SP(task_accepts)", "SF(snapshot_of)"},
        "lexical": {"SP(task_accepts)", "SF(snapshot_of)"},
        "confluence": {"SF(observe)", "SF(changes_between)",
                        "SP(observations_equal)",
                        "SP(dependency_metadata_changed)"},
    }[kind]
    def exact(local: str, namespace: str) -> ref.ExactKey:
        return ref.ExactKey(
            "capknow.semantic", namespace, local, ref.Version((1,)))
    return frozenset({
        ref.K1SyntaxKey(ref.K1SyntaxTag.PLUGIN,
                        exact("coding-minimal", "plugin")),
        *(ref.K1SyntaxKey(ref.K1SyntaxTag.SYMBOL,
                          exact(local, "coding.symbol"))
          for local in symbols),
        *(ref.K1SyntaxKey(ref.K1SyntaxTag.DECLARATION,
                          exact(f"T({name})", "coding.type"))
          for name in type_names),
    })


def _asserted_reasoning_roots(
    target: ref.ReasoningTarget, kind: str,
) -> frozenset[ref.DependencyKey]:
    syntax = _asserted_syntax_keys(kind)
    return frozenset({_asserted_dependency_key(
        target.semantic_environment)}) | frozenset(
            _asserted_lift(item) for item in syntax)


def _asserted_dependency_key(identity: ref.RecordIdentity) -> ref.DependencyKey:
    tags = {
        ref.RecordKind.PACKAGE: ref.DependencyTag.PLUGIN,
        ref.RecordKind.TYPE_DECLARATION: ref.DependencyTag.DECLARATION,
        ref.RecordKind.DECLARATION: ref.DependencyTag.DECLARATION,
        ref.RecordKind.EVENT: ref.DependencyTag.EVENT,
        ref.RecordKind.BINDING: ref.DependencyTag.BINDING,
        ref.RecordKind.PAIR_BINDING: ref.DependencyTag.PAIR_BINDING,
        ref.RecordKind.PROFILE_BINDING: ref.DependencyTag.PROFILE_BINDING,
        ref.RecordKind.PAIR_DECLARATION: ref.DependencyTag.PAIR_DECLARATION,
        ref.RecordKind.CONTRACT_SPEC: ref.DependencyTag.CONTRACT_SPEC,
        ref.RecordKind.SERVICE: ref.DependencyTag.SERVICE,
        ref.RecordKind.CAPABILITY: ref.DependencyTag.CAPABILITY,
        ref.RecordKind.CERTIFICATE: ref.DependencyTag.CERTIFICATE,
        ref.RecordKind.MODEL_CONTRACT: ref.DependencyTag.MODEL_CONTRACT,
        ref.RecordKind.TRUST_ROOT: ref.DependencyTag.TRUST_ROOT,
        ref.RecordKind.SEMANTIC_ENVIRONMENT: ref.DependencyTag.CARRIER,
        ref.RecordKind.SEMANTIC_ENVIRONMENT: ref.DependencyTag.CARRIER,
    }
    tag = tags.get(identity.kind, ref.DependencyTag.CARRIER)
    return ref.DependencyKey(
        tag, identity.key,
        identity.kind if tag is ref.DependencyTag.CARRIER else None)


def _asserted_lift(key: ref.K1SyntaxKey) -> ref.DependencyKey:
    tags = {
        ref.K1SyntaxTag.PLUGIN: (ref.DependencyTag.PLUGIN,
                                 ref.RecordKind.PACKAGE),
        ref.K1SyntaxTag.DECLARATION: (ref.DependencyTag.DECLARATION,
                                      ref.RecordKind.DECLARATION),
        ref.K1SyntaxTag.SYMBOL: (ref.DependencyTag.SYMBOL,
                                 ref.RecordKind.SYMBOL),
        ref.K1SyntaxTag.EVENT: (ref.DependencyTag.EVENT,
                                ref.RecordKind.EVENT),
        ref.K1SyntaxTag.PROFILE: (ref.DependencyTag.PROFILE,
                                  ref.RecordKind.PROFILE_BINDING),
        ref.K1SyntaxTag.PAIR: (ref.DependencyTag.PAIR,
                               ref.RecordKind.PAIR_DECLARATION),
    }
    tag, _ = tags[key.tag]
    return ref.DependencyKey(tag, key.exact_key)


def _asserted_dependency_environment(
    syntax: frozenset[ref.K1SyntaxKey],
    semantic_roots: frozenset[ref.RecordIdentity],
    composition: ref.Composition,
) -> ref.DependencyEnvironment:
    associations: set[tuple[ref.DependencyKey, ref.DependencyKey]] = set()
    for root in syntax:
        if root.tag is not ref.K1SyntaxTag.SYMBOL:
            continue
        declarations = tuple(
            item for item in composition.records
            if isinstance(item.value, ref.DeclarationShape)
            and item.value.symbol_key == root.exact_key)
        if len(declarations) != 1:
            raise AssertionError("independent symbol declaration is not unique")
        declaration = declarations[0]
        ordinary = tuple(
            item for item in composition.records
            if isinstance(item.value, ref.SemanticBinding)
            and item.value.declaration == declaration.identity)
        pair_owned = tuple(
            occurrence for pair_binding in composition.records
            if isinstance(pair_binding.value, ref.PairBinding)
            and (pair_declaration := composition.at(ref.RecordIdentity(
                ref.RecordKind.PAIR_DECLARATION,
                pair_binding.value.pair_key))) is not None
            and isinstance(pair_declaration.value, ref.PairDeclaration)
            and pair_declaration.value.occurrence_symbol
                == declaration.value.symbol_key
            and (occurrence := composition.at(
                pair_binding.value.occurrence_bundle)) is not None
            and isinstance(occurrence.value,
                           ref.OccurrenceSemanticContractBundle))
        bindings = ordinary + pair_owned
        if len(bindings) != 1:
            raise AssertionError("independent symbol binding is not unique")
        source = _asserted_lift(root)
        associations.update({
            (source, _asserted_dependency_key(declaration.identity)),
            (source, _asserted_dependency_key(bindings[0].identity)),
        })
    roots = frozenset(_asserted_lift(item) for item in syntax) | frozenset(
        _asserted_dependency_key(item) for item in semantic_roots)
    association_map: dict[ref.DependencyKey, set[ref.DependencyKey]] = {}
    for source, target in associations:
        association_map.setdefault(source, set()).add(target)
    reached = set(roots)
    pending = list(roots)
    proper: set[ref.DependencyKey] = set()
    while pending:
        current = pending.pop()
        candidates = tuple(
            item for item in composition.records
            if item.identity.key == current.exact_key
            and (item.identity.kind == current.record_kind
                 or current.tag is ref.DependencyTag.DECLARATION
                 and item.identity.kind is ref.RecordKind.TYPE_DECLARATION))
        value = candidates[0].value if len(candidates) == 1 else None
        direct = (
            value.proper_declaration_dependencies
            if isinstance(value, ref.TypeDeclaration)
            else value.proper_declaration_dependencies
            if isinstance(value, ref.PairDeclaration)
            else value.proper_type_dependencies
            if isinstance(value, ref.DeclarationShape)
            else value.support
            if isinstance(value, ref.ContractSpec)
            else value.proper_semantic_dependencies
            if isinstance(value, (ref.SemanticBinding, ref.ProfileBinding,
                                  ref.OccurrenceSemanticContractBundle,
                                  ref.PairBinding))
            else frozenset())
        direct_keys = {_asserted_dependency_key(item) for item in direct}
        proper.update(direct_keys)
        for target in association_map.get(current, set()) | direct_keys:
            if target not in reached:
                reached.add(target)
                pending.append(target)
    expanded = roots | frozenset(target for _, target in associations)
    return ref.DependencyEnvironment(
        syntax, roots, frozenset(associations), expanded, frozenset(proper),
        frozenset(reached - roots), frozenset())


def _asserted_dependency_resolves(
    key: ref.DependencyKey, composition: ref.Composition,
) -> bool:
    direct = composition.at(ref.RecordIdentity(key.record_kind, key.exact_key))
    if direct is not None:
        return True
    if key.tag is ref.DependencyTag.DECLARATION:
        return composition.at(ref.RecordIdentity(
            ref.RecordKind.TYPE_DECLARATION, key.exact_key)) is not None
    if key.tag is not ref.DependencyTag.SYMBOL:
        return False
    declarations = tuple(
        item for item in composition.records
        if isinstance(item.value, ref.DeclarationShape)
        and item.value.symbol_key == key.exact_key)
    if len(declarations) != 1:
        return False
    ordinary = tuple(
        item for item in composition.records
        if isinstance(item.value, ref.SemanticBinding)
        and item.value.declaration == declarations[0].identity)
    pair_owned = tuple(
        item for item in composition.records
        if isinstance(item.value, ref.OccurrenceSemanticContractBundle)
        and any(
            isinstance(pair.value, ref.PairBinding)
            and pair.value.occurrence_bundle == item.identity
            and (pair_declaration := composition.at(ref.RecordIdentity(
                ref.RecordKind.PAIR_DECLARATION,
                pair.value.pair_key))) is not None
            and isinstance(pair_declaration.value, ref.PairDeclaration)
            and pair_declaration.value.occurrence_symbol
                == declarations[0].value.symbol_key
            for pair in composition.records))
    return len(ordinary + pair_owned) == 1


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
            pair_declarations=members(package.pair_declarations),
            bindings=members(package.bindings),
            pair_bindings=members(package.pair_bindings),
            profile_bindings=members(package.profile_bindings),
            model_contracts=members(package.model_contracts),
            aliases=members(package.aliases),
            services=members(package.services),
            certificates=members(package.certificates),
            authority_facts=members(package.authority_facts),
            compatibility_claims=members(package.compatibility_claims),
            migrations=members(package.migrations),
            semantic_extensions=members(package.semantic_extensions),
        ))
    return replace(universe, records=tuple(updated for item in universe.records if (updated := one(item)) is not None))


def _at(universe: ref.Universe, identity: ref.RecordIdentity) -> ref.LogicalRecord:
    item = ref.compose_records(universe.records).at(identity)
    if item is None:
        raise AssertionError(f"missing test construction record {identity}")
    return item


def _identity_literal(identity: ref.RecordIdentity) -> fx.IdentityLiteral:
    return (
        identity.kind.value,
        identity.key.owner,
        identity.key.namespace,
        identity.key.local,
        identity.key.version.components,
    )


def _key_literal(value: ref.ExactKey) -> tuple[str, str, str, tuple[int, ...]]:
    return (value.owner, value.namespace, value.local, value.version.components)


def _detail_literal(value: object) -> object:
    if isinstance(value, ref.LogicalRecord):
        return _identity_literal(value.identity)
    if isinstance(value, ref.RecordIdentity):
        return _identity_literal(value)
    if isinstance(value, tuple):
        return tuple(_detail_literal(item) for item in value)
    if isinstance(value, frozenset):
        return frozenset(_detail_literal(item) for item in value)
    return value


def _judgment_literal(value: ref.Judgment) -> tuple[object, ...]:
    return (value.tag, _detail_literal(value.details))


def _conflict_literal(value: ref.ConflictRef) -> tuple[object, ...]:
    positions = tuple(sorted(
        tuple(tuple(sorted(facets)) for facets in item.positions)
        for item in value.conflict_kind.unequal_positions
    ))
    return (
        "PREDICATE_FACET_POSITIONS_CONFLICT",
        _key_literal(value.conflict_kind.declaration_key),
        positions,
        tuple(sorted(_identity_literal(item) for item in value.involved_identity_set)),
    )


def _replay_assertion(universe: ref.Universe, replayed: object) -> fx.ReplayAssertion:
    if isinstance(replayed, (ref.CoreReplay, ref.PairReplay, ref.LookupReplay)):
        composition = replayed.authoritative
    elif isinstance(replayed, ref.CompositionReplay):
        composition = replayed.composition
    else:
        composition = ref.compose_records(universe.records)
    identities = tuple(sorted(_identity_literal(item.identity) for item in composition.records))
    conflicts = tuple(_conflict_literal(item) for item in composition.conflicts)
    if isinstance(replayed, ref.CoreReplay):
        outcome = (
            "CORE", replayed.formation, replayed.closure, replayed.evaluability,
            replayed.lifecycle, replayed.result,
        )
    elif isinstance(replayed, ref.PairReplay):
        outcome = (
            "PAIR", replayed.formation, replayed.closure,
            _key_literal(replayed.result.pair_key),
            _key_literal(replayed.result.certificate_key), replayed.result.result.tag,
        )
    elif isinstance(replayed, ref.LookupReplay):
        outcome = ("LOOKUP", *_judgment_literal(replayed.result))
    elif isinstance(replayed, ref.ObservationEvaluation):
        outcome = (
            "OBSERVATION",
            tuple((_identity_literal(identity), value) for identity, value in replayed.observations),
            _judgment_literal(replayed.reasoning_result),
            replayed.lifecycle,
            replayed.status,
        )
    elif isinstance(replayed, ref.CompositionReplay):
        outcome = ("COMPOSITION", replayed.formation, replayed.closure)
    elif isinstance(replayed, tuple):
        outcome = ("FORMATION", replayed)
    else:
        raise AssertionError(f"unsupported test replay projection: {type(replayed).__name__}")
    return fx.ReplayAssertion(identities, conflicts, outcome)


def _contains_fixture_id(value: object) -> bool:
    if isinstance(value, fx.FixtureId):
        return True
    if isinstance(value, str) and any(
        token in value.casefold() for token in ("challenge", "expected")
    ):
        return True
    if isinstance(value, dict):
        return any(_contains_fixture_id(item) for pair in value.items() for item in pair)
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_fixture_id(item) for item in value)
    if is_dataclass(value) and not isinstance(value, type):
        return any(_contains_fixture_id(getattr(value, item.name)) for item in fields(value))
    return False


class K3XReferenceTests(unittest.TestCase):
    def test_k3x_01_core_definitional_and_closed_coding_values(self) -> None:
        construction = fx.core_construction()
        replayed = ref.replay(construction.universe)
        self.assertIsInstance(replayed, ref.CoreReplay)
        self.assertEqual((replayed.formation, replayed.closure, replayed.evaluability), (ref.Formation.WELL_FORMED, ref.Closure.CLOSED, ref.Evaluability.AVAILABLE))
        self.assertEqual(replayed.result.truth, cp.Truth.TRUE)
        result_record = _at(construction.universe, construction.result)
        self.assertEqual((result_record.value.request, result_record.value.result_kind, result_record.value.result), (construction.request, "Eval", replayed.result))
        package = _at(construction.universe, construction.package).value
        composition = ref.compose_records(construction.universe.records)
        self.assertEqual(
            (len(package.declarations), len(package.pair_declarations),
             len(package.bindings), len(package.pair_bindings),
             len(package.profile_bindings), len(package.model_contracts),
             len(package.services), len(package.certificates)),
            (119, 1, 57, 1, 1, 58, 6, 1),
        )
        self.assertEqual(
            (sum(isinstance(item.value, ref.TypeDeclaration)
                 for item in package.declarations),
             sum(isinstance(item.value, ref.DeclarationShape)
                 and item.value.declaration_kind == "LITERAL"
                 for item in package.declarations)),
            (55, 47),
        )
        type_rows = tuple(
            item for item in package.declarations
            if isinstance(item.value, ref.TypeDeclaration))
        self.assertEqual(
            {item.identity.key.local for item in type_rows},
            {f"T({name})" for name in cp._ADMISSION_TYPES})
        for declaration_record in type_rows:
            spec = declaration_record.value.admitted_value_domain
            type_name = declaration_record.identity.key.local[2:-1]
            with self.subTest(exact_type_admission=type_name):
                self.assertEqual(spec.primary_input_domain, ("Value",))
                self.assertEqual(spec.codomain,
                                 frozenset({"admitted", "not_admitted"}))
                self.assertEqual(spec.type_admission_relation,
                                 ref.TypeAdmissionRelation(cp.admission_type(type_name)))
                self.assertEqual(
                    frozenset(query.dependency
                              for query in spec.observation_queries),
                    spec.support)
                self.assertEqual(
                    declaration_record.value.proper_declaration_dependencies,
                    spec.support | frozenset({ref.RecordIdentity(
                        ref.RecordKind.CONTRACT_SPEC, spec.contract_key)}))
        literal_rows = tuple(
            item for item in package.declarations
            if isinstance(item.value, ref.DeclarationShape)
            and item.value.declaration_kind == "LITERAL")
        literal_bindings = {
            item.value.declaration: item for item in package.bindings
            if isinstance(item.value, ref.SemanticBinding)
            and item.value.binding_kind == "LITERAL"}
        literal_models = {
            item.value.target_binding: item for item in package.model_contracts}
        self.assertEqual(set(literal_bindings),
                         {item.identity for item in literal_rows})
        for declaration_record in literal_rows:
            binding_record = literal_bindings[declaration_record.identity]
            model_record = literal_models[binding_record.identity]
            with self.subTest(exact_literal=declaration_record.identity.key.local):
                self.assertEqual(declaration_record.value.argument_types, ())
                self.assertEqual(declaration_record.value.facet_positions, ())
                self.assertEqual(len(declaration_record.value.proper_type_dependencies), 1)
                self.assertIsNotNone(declaration_record.value.literal_value)
                self.assertEqual(binding_record.value.declaration,
                                 declaration_record.identity)
                self.assertEqual(binding_record.value.binding_kind, "LITERAL")
                self.assertEqual(binding_record.value.unknown_contract.key.local,
                                 "CS(UNKNOWN_BEHAVIOR,not_applicable)")
                self.assertEqual(binding_record.value.permitted_facet_inputs, ())
                self.assertEqual(
                    binding_record.value.proper_semantic_dependencies,
                    frozenset({declaration_record.identity,
                               binding_record.value.meaning_contract,
                               binding_record.value.evidence_schema,
                               binding_record.value.access_boundary,
                               binding_record.value.unknown_contract,
                               binding_record.value.evaluation_error_contract}))
                self.assertEqual(model_record.value.target_binding,
                                 binding_record.identity)
                self.assertEqual(model_record.value.exact_symbol_key,
                                 declaration_record.value.symbol_key)
                self.assertEqual(model_record.value.exact_argument_types, ())
                self.assertEqual(model_record.value.exact_result_kind,
                                 declaration_record.value.result_kind)
                self.assertEqual(model_record.value.exact_facet_positions, ())
                self.assertEqual(model_record.value.evidence_contract,
                                 binding_record.value.evidence_schema)
                self.assertEqual(model_record.value.unknown_contract,
                                 binding_record.value.unknown_contract)
                self.assertEqual(model_record.value.error_contract,
                                 binding_record.value.evaluation_error_contract)
                self.assertEqual(model_record.value.semantic_contract,
                                 binding_record.value.meaning_contract)
                self.assertEqual(model_record.value.capability_summaries,
                                 frozenset())
        callable_declarations = {
            item.identity.key.local: item.value for item in package.declarations
            if isinstance(item.value, ref.DeclarationShape)
            and item.value.declaration_kind in {"FUNCTION", "PREDICATE"}}
        expected_callable_fields = {
            "DF(snapshot_of)": (("State",), "T(RepositorySnapshot)",
                                (frozenset({"pre", "final"}),)),
            "DF(changes_between)": (("RepositorySnapshot", "RepositorySnapshot"),
                                    "T(ChangeSet)",
                                    (frozenset({"pre"}), frozenset({"final"}))),
            "DF(observe)": (("ObservationSpec", "RepositorySnapshot"),
                            "T(ObservationResult)",
                            (frozenset(), frozenset({"pre", "final"}))),
            "DP(observations_equal)": (("ObservationResult", "ObservationResult"),
                                       "Bool",
                                       (frozenset({"pre"}), frozenset({"final"}))),
            "DP(task_accepts)": (("TaskSpec", "RepositorySnapshot", "EvidenceStore"),
                                 "Bool", (frozenset(), frozenset({"final"}),
                                          frozenset({"evidence"}))),
            "DP(dependency_metadata_changed)": (("ChangeSet",), "Bool",
                                                (frozenset({"pre", "final"}),)),
            "DP(verification_passed)": (("VerificationSpec", "RepositorySnapshot",
                                         "EvidenceStore"), "Bool",
                                        (frozenset(), frozenset({"final"}),
                                         frozenset({"evidence"}))),
            "DP(event_matches)": (("EventPattern", "EventValue"), "Bool",
                                  (frozenset(), frozenset())),
            "DP(event_occurred)": (("EventPattern", "Trace"), "Bool",
                                   (frozenset(), frozenset({"trace"}))),
            "DP(refresh_scope)": (("EventValue",), "Bool", (frozenset(),)),
            "DP(refresh_occurred)": (("Trace",), "Bool",
                                     (frozenset({"trace"}),)),
        }
        self.assertEqual(set(callable_declarations), set(expected_callable_fields))
        for local, (argument_names, result_kind, facets) in expected_callable_fields.items():
            declaration = callable_declarations[local]
            self.assertEqual(
                tuple(item.local[2:-1] if item.local.startswith("T(")
                      else item.local for item in declaration.argument_types),
                argument_names)
            self.assertEqual(declaration.result_kind, result_kind)
            self.assertEqual(declaration.facet_positions, facets)
        attestation_values = tuple(
            item.value.literal_value for item in literal_rows
            if isinstance(item.value.literal_value,
                          cp.AuthorityAttestationValue))
        self.assertEqual(len(attestation_values), 6)
        frozen_core_assertion = fx.assertion_results()[
            fx.FixtureId(fx.FixtureFamily.CORE_DEFINITIONAL)]
        self.assertEqual(
            [item.normative_role for item in attestation_values].count("REQUIRE"),
            5)
        choice_attestation = next(
            item for item in attestation_values
            if item.normative_role == "BIND_CHOICE(storage)")
        self.assertEqual(choice_attestation.principal, "user")
        self.assertEqual(choice_attestation.subject_identity.choice_id,
                         "storage")
        for item in attestation_values:
            with self.subTest(authority_attestation=item.subject_identity):
                self.assertEqual(item.authority_ref.key.owner,
                                 "PLUGIN_ISSUER(APK)")
                self.assertEqual(item.source_ref.key.owner,
                                 "PLUGIN_ISSUER(APK)")
                if item is not choice_attestation:
                    self.assertEqual(item.principal, "fixture_principal")
                    self.assertEqual(item.normative_role, "REQUIRE")
        authority_subject_values = tuple(
            item.value.literal_value for item in literal_rows
            if isinstance(item.value.literal_value,
                          cp.ServiceAdmissionSubject)
            and item.value.literal_value.tag
                is cp.ServiceSubjectTag.AUTHORITY_ATTESTATION)
        self.assertEqual(len(authority_subject_values), 6)
        for subject_value in authority_subject_values:
            self.assertIn(subject_value.attestation, attestation_values)
            self.assertEqual(len(subject_value.offered_evidence_refs), 1)
            evidence_ref = next(iter(subject_value.offered_evidence_refs))
            self.assertEqual((evidence_ref.issuer_scope, evidence_ref.namespace,
                              evidence_ref.schema_binding),
                             ("PLUGIN_ISSUER(ATK)",
                              "coding.authority.attestation", "AREQUIRED"))
        authority_literal_rows = tuple(
            item for item in literal_rows
            if isinstance(item.value.literal_value, (
                cp.AuthorityAttestationSubjectIdentity,
                cp.AuthorityAttestationValue))
            or (isinstance(item.value.literal_value,
                          cp.ServiceAdmissionSubject)
                and item.value.literal_value.tag
                    is cp.ServiceSubjectTag.AUTHORITY_ATTESTATION))
        authority_by_type: dict[type[object], list[ref.LogicalRecord]] = {}
        for item in authority_literal_rows:
            authority_by_type.setdefault(
                type(item.value.literal_value), []).append(item)
        for rows in authority_by_type.values():
            self.assertEqual(len(rows), 6)
            for index, declaration_record in enumerate(rows):
                replacement_value = rows[(index + 1) % len(rows)].value.literal_value
                changed_declaration = replace(
                    declaration_record,
                    value=replace(declaration_record.value,
                                  literal_value=replacement_value))
                changed = _rewrite(
                    construction.universe,
                    {declaration_record.identity: changed_declaration})
                with self.subTest(
                        frozen_authority_literal=declaration_record.identity):
                    self.assertNotEqual(
                        _replay_assertion(changed, ref.replay(changed)),
                        frozen_core_assertion)
        self.assertEqual(
            {item.identity.key.local for item in package.services},
            {"CAP(functions)", "CAP(predicates)", "CAP(profile)",
             "CAP(bounds)", "CAP(confluence)", "LEX_CAP"},
        )
        descriptor_coordinates = {
            item.identity.key.local: (
                item.value.service_role, item.value.capability_class,
                item.value.supported_judgments,
                item.value.sound_fragment.key.local,
                None if item.value.complete_fragment is None
                else item.value.complete_fragment.key.local,
                item.value.required_evidence.key.local,
                item.value.failure_contract.key.local)
            for item in package.services}
        self.assertEqual(descriptor_coordinates, {
            "CAP(functions)": ("FUNCTION_EVALUATION", "CONCRETE_EVALUATION_ONLY", frozenset({"FUNCTION_EVALUATION"}), "FSOUND", None, "FREQ", "FFAIL"),
            "CAP(predicates)": ("PREDICATE_EVALUATION", "CONCRETE_EVALUATION_ONLY", frozenset({"PREDICATE_EVALUATION"}), "QSOUND", None, "QREQ", "QFAIL"),
            "CAP(profile)": ("PROFILE_CONCRETE", "CONCRETE_EVALUATION_ONLY", frozenset({"PROFILE_COVERAGE"}), "PROFSOUND", None, "PROFREQ", "PROFFAIL"),
            "CAP(bounds)": ("REASONING", "COMPLETE_FOR_DECLARED_FRAGMENT", frozenset({"CONSISTENCY"}), "BSOUND", "BCOMPLETE", "BREQ", "BFAIL"),
            "CAP(confluence)": ("REASONING", "PARTIAL_SYMBOLIC_REASONING", frozenset({"CONSISTENCY"}), "CSOUND", None, "CREQ", "CFAIL"),
            "LEX_CAP": ("REASONING", "PARTIAL_SYMBOLIC_REASONING", frozenset({"FORMULA_ENTAILMENT"}), "LEX_SOUND", None, "LEX_REQ", "LEX_FAIL"),
        })
        def asserted_target_roots(
            target: object, reasoning_kind: str = "",
        ) -> frozenset[ref.DependencyKey]:
            if isinstance(target, ref.BindingTarget):
                return frozenset({_asserted_dependency_key(target.binding)})
            if isinstance(target, ref.ProfileTarget):
                return frozenset(
                    _asserted_dependency_key(item.identity)
                    for item in package.profile_bindings
                    if item.value.profile_key == target.profile_key)
            if isinstance(target, ref.ReasoningTarget):
                return _asserted_reasoning_roots(target, reasoning_kind)
            self.fail(f"unexpected typed capability target: {target!r}")
        for descriptor_record in package.services:
            descriptor_local = descriptor_record.identity.key.local
            with self.subTest(exact_descriptor=descriptor_record.identity.key.local):
                self.assertTrue(descriptor_record.value.supported_targets)
                self.assertTrue(descriptor_record.value.dependency_scope)
                self.assertTrue(descriptor_record.value.required_trust_roots)
                self.assertTrue(
                    frozenset(_asserted_dependency_key(item) for item in
                              descriptor_record.value.required_trust_roots)
                    <= descriptor_record.value.proper_semantic_dependencies)
                self.assertEqual(
                    descriptor_record.value.proper_semantic_dependencies,
                    frozenset(_asserted_dependency_key(item) for item in {
                        descriptor_record.value.service,
                        descriptor_record.value.sound_fragment,
                        descriptor_record.value.required_evidence,
                        descriptor_record.value.failure_contract,
                        *descriptor_record.value.required_trust_roots,
                        *(tuple() if descriptor_record.value.complete_fragment is None
                          else (descriptor_record.value.complete_fragment,)),
                    }) | frozenset().union(*(
                        asserted_target_roots(target)
                        if descriptor_local not in {
                            "CAP(bounds)", "CAP(confluence)", "LEX_CAP"}
                        else asserted_target_roots(target, {
                            "CAP(bounds)": "bounds",
                            "CAP(confluence)": "confluence",
                            "LEX_CAP": "lexical",
                        }[descriptor_local])
                        for target in descriptor_record.value.supported_targets)))
        descriptors = {
            item.identity.key.local: item.value for item in package.services}
        asserted_binding_targets = {
            "CAP(functions)": {
                "BINDING(DF(snapshot_of))", "BINDING(DF(changes_between))",
                "BINDING(DF(observe))"},
            "CAP(predicates)": {
                "BINDING(DP(task_accepts))",
                "BINDING(DP(observations_equal))",
                "BINDING(DP(verification_passed))",
                "BINDING(DP(event_matches))",
                "BINDING(DP(event_occurred))",
                "BINDING(DP(refresh_scope))",
                "BINDING(DP(refresh_occurred))",
                "BINDING(DP(dependency_metadata_changed))"},
        }
        for local, expected in asserted_binding_targets.items():
            self.assertEqual(
                {target.binding.key.local
                 for target in descriptors[local].supported_targets
                 if isinstance(target, ref.BindingTarget)},
                expected)
            self.assertTrue(all(
                isinstance(target, ref.BindingTarget)
                for target in descriptors[local].supported_targets))
        self.assertEqual(
            descriptors["CAP(profile)"].supported_targets,
            frozenset({ref.ProfileTarget(fx.key(
                "PK(implementation_evidence)", namespace="coding.profile"))}))
        asserted_reasoning_targets = {
            "CAP(bounds)": ("CONSISTENCY", (
                ref.ContractSubject(ref.frozen_bounds_contract()),), "E_b"),
            "CAP(confluence)": ("CONSISTENCY", (
                ref.ContractSubject(ref.frozen_confluence_contract()),), "E_c"),
            "LEX_CAP": ("FORMULA_ENTAILMENT", (ref.FormulaSubject(
                frozenset(ref.frozen_lexical_formulas()),
                ref.frozen_lexical_scope()),), "E_lex"),
        }
        for local, (judgment, subjects, environment) in asserted_reasoning_targets.items():
            self.assertEqual(len(descriptors[local].supported_targets), 1)
            target = next(iter(descriptors[local].supported_targets))
            self.assertIsInstance(target, ref.ReasoningTarget)
            self.assertEqual(target.judgment, judgment)
            self.assertEqual(target.semantic_environment.key.local, environment)
            self.assertEqual(target.subjects, subjects)
            self.assertTrue(all(
                isinstance(root, ref.DependencyKey)
                and _asserted_dependency_resolves(root, composition)
                for root in _asserted_reasoning_roots(target, {
                    "CAP(bounds)": "bounds",
                    "CAP(confluence)": "confluence",
                    "LEX_CAP": "lexical",
                }[local])))
        bounds_target = next(iter(descriptors["CAP(bounds)"].supported_targets))
        assert isinstance(bounds_target, ref.ReasoningTarget)
        bounds_subject = bounds_target.subjects[0]
        assert isinstance(bounds_subject, ref.ContractSubject)
        clause = bounds_subject.contract.attributed_clauses[0]
        formula = next(iter(clause.requirement.members))
        assert formula.symbol is not None
        foreign_formula = replace(
            formula, symbol=replace(formula.symbol, owner="foreign.owner"))
        foreign_contract = replace(
            bounds_subject.contract,
            attributed_clauses=(replace(
                clause, requirement=replace(
                    clause.requirement,
                    members=(clause.requirement.members - {formula})
                    | {foreign_formula})),))
        self.assertNotEqual(
            ref.required_subject(bounds_subject),
            ref.required_subject(ref.ContractSubject(foreign_contract)))
        lexical_subject = next(iter(
            descriptors["LEX_CAP"].supported_targets)).subjects[0]
        assert isinstance(lexical_subject, ref.FormulaSubject)
        foreign_scope_subject = replace(
            lexical_subject,
            lexical_scope=replace(
                lexical_subject.lexical_scope,
                judgment_or_binder_kind="PREDICATE_EVALUATION"))
        self.assertNotEqual(lexical_subject, foreign_scope_subject)
        for descriptor_local, changed_target in (
            ("CAP(bounds)", replace(
                bounds_target,
                subjects=(ref.ContractSubject(foreign_contract),))),
            ("LEX_CAP", replace(
                next(iter(descriptors["LEX_CAP"].supported_targets)),
                subjects=(foreign_scope_subject,))),
        ):
            descriptor_record = next(
                item for item in package.services
                if item.identity.key.local == descriptor_local)
            changed_descriptor = replace(
                descriptor_record,
                value=replace(
                    descriptor_record.value,
                    supported_targets=frozenset({changed_target})))
            self.assertIsInstance(ref.replay(_rewrite(
                construction.universe,
                {descriptor_record.identity: changed_descriptor})),
                ref.CompositionReplay)
        unresolved = ref.DependencyKey(
            ref.DependencyTag.SYMBOL,
            replace(formula.symbol, owner="foreign.owner"))
        with self.assertRaises(ValueError):
            ref.dependency_reachability(frozenset({unresolved}), composition)
        with self.assertRaises(TypeError):
            ref.ReasoningTarget(
                "FORMULA_ENTAILMENT", ("f_lex", "g_lex"),  # type: ignore[arg-type]
                fx.rid(ref.RecordKind.SEMANTIC_ENVIRONMENT, "E_lex",
                       namespace="lexical.environment"))
        lexical_target = next(iter(descriptors["LEX_CAP"].supported_targets))
        assert isinstance(lexical_target, ref.ReasoningTarget)
        omitted_subject = replace(
            lexical_target, subjects=(replace(
                lexical_target.subjects[0], formulas=frozenset({
                    ref.frozen_lexical_formulas()[0]}),
                lexical_scope=ref.LexicalScopeIdentity(
                    "FORMULA_ENTAILMENT",
                    (ref.frozen_lexical_formulas()[0],))),))
        lexical_descriptor_record = next(
            item for item in package.services
            if item.identity.key.local == "LEX_CAP")
        omitted_descriptor = replace(
            lexical_descriptor_record,
            value=replace(lexical_descriptor_record.value,
                          supported_targets=frozenset({omitted_subject})))
        omitted_replay = ref.replay(_rewrite(
            construction.universe,
            {lexical_descriptor_record.identity: omitted_descriptor}))
        self.assertIsInstance(omitted_replay, ref.CompositionReplay)
        self.assertEqual(omitted_replay.formation, ref.Formation.MALFORMED)
        with self.assertRaises(TypeError):
            replace(lexical_target, semantic_environment=fx.rid(
                ref.RecordKind.TRUST_ENVIRONMENT, "E_lex",
                namespace="lexical.environment"))
        self.assertEqual(
            {local: (descriptor.service.key.local,
                     {root.key.local for root in descriptor.required_trust_roots})
             for local, descriptor in descriptors.items()},
            {
                "CAP(functions)": ("SK(functions)", {"TR"}),
                "CAP(predicates)": ("SK(predicates)", {"TR"}),
                "CAP(profile)": ("SK(profile)", {"TR"}),
                "CAP(bounds)": ("SK(bounds)", {"TRB"}),
                "CAP(confluence)": ("SK(confluence)", {"ROOT_TR_c"}),
                "LEX_CAP": ("LEXSK", {"TR"}),
            })

        profile_record = next(
            item for item in package.profile_bindings
            if item.identity.key.local
            == "PROFILE_BINDING(PK(implementation_evidence))")
        self.assertIsInstance(profile_record.value, ref.ProfileBinding)
        self.assertEqual(
            {item.dimension for item in profile_record.value.dimensions},
            {"abstract_acceptance_evidence",
             "concrete_implementation_evidence"})
        self.assertEqual(
            profile_record.value.coverage_meaning.key.local,
            "CS(PROFILE_COVERAGE,implementation_evidence)")
        self.assertEqual(
            profile_record.value.evidence_schema.key.local,
            "CS(EVIDENCE_SCHEMA,implementation_profile)")
        self.assertEqual(
            profile_record.value.unknown_contract.key.local,
            "CS(UNKNOWN_BEHAVIOR,evidence_pending)")
        self.assertEqual(
            profile_record.value.evaluation_error_contract.key.local,
            "CS(EVALUATION_ERROR_BEHAVIOR,profile)")
        self.assertEqual(
            profile_record.value.reasoning_error_contract.key.local,
            "CS(REASONING_ERROR_BEHAVIOR,profile)")
        self.assertEqual(
            ref.validate_profile_binding(profile_record.value, composition).tag,
            "CLOSED")
        binding_closures = {
            item.identity.key.local: item.value.dependency_closure
            for item in composition.records
            if item.identity.kind is ref.RecordKind.BINDING
            and hasattr(item.value, "dependency_closure")}
        def combined_scope(*locals_: str) -> frozenset[ref.DependencyKey]:
            return frozenset().union(*(
                frozenset(_asserted_dependency_key(root)
                          for root in binding_closures[local])
                for local in locals_))
        self.assertEqual(
            {local: descriptor.dependency_scope
             for local, descriptor in descriptors.items()},
            {
                "CAP(functions)": combined_scope(
                    "BINDING(DF(snapshot_of))",
                    "BINDING(DF(changes_between))",
                    "BINDING(DF(observe))"),
                "CAP(predicates)": combined_scope(
                    *sorted(asserted_binding_targets["CAP(predicates)"])),
                "CAP(profile)": frozenset(
                    _asserted_dependency_key(root)
                    for root in profile_record.value.dependency_closure),
                "CAP(bounds)": combined_scope(
                    "BINDING(DF(snapshot_of))",
                    "BINDING(DP(task_accepts))",
                    "BINDING(L(T(TaskSpec),ts_nonempty))",
                    "BINDING(L(T(TaskSpec),ts_lt_100))",
                    "BINDING(L(T(TaskSpec),ts_ge_200))"),
                "CAP(confluence)": combined_scope(
                    "BINDING(DF(observe))",
                    "BINDING(DF(changes_between))"),
                "LEX_CAP": combined_scope("BINDING(DP(task_accepts))"),
            })

        spec_by_local = {
            item.identity.key.local: item for item in composition.records
            if isinstance(item.value, ref.ContractSpec)}
        snapshot_meaning = spec_by_local[
            "CS(FUNCTION_MEANING,snapshot_of)"].value
        state_access = spec_by_local["CS(ACCESS_BOUNDARY,state_only)"].value
        occurred_meaning = spec_by_local[
            "CS(PREDICATE_MEANING,event_occurred)"].value
        trace_access = spec_by_local["CS(ACCESS_BOUNDARY,pattern_trace)"].value
        self.assertEqual(
            (state_access.support, state_access.observation_queries),
            (snapshot_meaning.support, snapshot_meaning.observation_queries))
        self.assertEqual(
            (trace_access.support, trace_access.observation_queries),
            (occurred_meaning.support, occurred_meaning.observation_queries))
        verification_schema = spec_by_local[
            "CS(EVIDENCE_SCHEMA,verification)"].value
        self.assertEqual(
            {item.key.local for item in verification_schema.support},
            {"T(CodingEvidenceEntry)"})

        expected_task_syntax = _asserted_syntax_keys("task")
        task_environment = _at(
            construction.universe, construction.semantic_environment).value
        task_dependencies = _at(
            construction.universe, construction.dependency_environment).value
        self.assertEqual(
            task_environment.mechanically_extracted_dependencies,
            expected_task_syntax)
        self.assertEqual(task_dependencies.syntax_root_keys,
                         expected_task_syntax)
        self.assertEqual(
            task_dependencies,
            _asserted_dependency_environment(
                expected_task_syntax, frozenset({construction.binding}),
                composition))
        rogue_syntax = ref.K1SyntaxKey(
            ref.K1SyntaxTag.DECLARATION,
            fx.key("T(rogue)", namespace="coding.type"))
        changed_environment = replace(
            _at(construction.universe, construction.semantic_environment),
            value=replace(task_environment,
                          mechanically_extracted_dependencies=
                          expected_task_syntax | {rogue_syntax}))
        changed_dependencies = replace(
            _at(construction.universe, construction.dependency_environment),
            value=replace(task_dependencies,
                          syntax_root_keys=expected_task_syntax | {rogue_syntax},
                          expanded_root_keys=(task_dependencies.expanded_root_keys
                                              | {ref.lift_syntax_key(
                                                  rogue_syntax)})))
        changed_syntax = _rewrite(construction.universe, {
            construction.semantic_environment: changed_environment,
            construction.dependency_environment: changed_dependencies})
        self.assertEqual(ref.replay(changed_syntax).formation,
                         ref.Formation.MALFORMED)

        emptied_access = replace(
            spec_by_local["CS(ACCESS_BOUNDARY,state_only)"],
            value=replace(state_access, observation_queries=(),
                          support=frozenset()))
        self.assertIsInstance(ref.replay(_rewrite(
            construction.universe,
            {emptied_access.identity: emptied_access})),
            ref.CompositionReplay)
        empty_profile = replace(
            profile_record, value=replace(profile_record.value,
                                          dimensions=frozenset()))
        self.assertIsInstance(ref.replay(_rewrite(
            construction.universe,
            {profile_record.identity: empty_profile})),
            ref.CompositionReplay)
        # Every field of every retained descriptor is executable data.  These
        # mutations are compared with the separately frozen packet assertion;
        # no expected value is obtained from replay.
        foreign_identity = fx.rid(
            ref.RecordKind.DECLARATION, "foreign-complete-value",
            namespace="assertion.falsifier")

        def changed_field(value: object) -> object:
            if isinstance(value, ref.ExactKey):
                return fx.key("foreign-complete-value",
                              namespace="assertion.falsifier")
            if isinstance(value, ref.Version):
                return fx.V2
            if isinstance(value, ref.RecordIdentity):
                return ref.RecordIdentity(value.kind, fx.key(
                    "foreign-complete-value",
                    namespace="assertion.falsifier"))
            if isinstance(value, str):
                return f"{value}.wrong"
            if isinstance(value, frozenset):
                return (frozenset() if value
                        else frozenset({foreign_identity}))
            if isinstance(value, tuple):
                return () if value else (foreign_identity,)
            if value is None:
                return foreign_identity
            raise AssertionError(f"unhandled frozen field type: {type(value)}")

        for descriptor_record in package.services:
            for field_name in descriptor_record.value.__dataclass_fields__:
                mutation = replace(
                    descriptor_record.value,
                    **{field_name: changed_field(
                        getattr(descriptor_record.value, field_name))})
                changed = _rewrite(
                    construction.universe,
                    {descriptor_record.identity: replace(
                        descriptor_record, value=mutation)})
                with self.subTest(
                        descriptor_complete_field=(
                            descriptor_record.identity.key.local, field_name)):
                    self.assertNotEqual(
                        _replay_assertion(changed, ref.replay(changed)),
                        frozen_core_assertion)

        retained_contracts = tuple(
            item for item in ref.compose_records(
                construction.universe.records).records
            if isinstance(item.value, ref.ContractSpec)
            and item.identity.key.namespace == "coding.contract"
            and (item.identity.key.local.startswith("CS(FUNCTION_MEANING,")
                 or item.identity.key.local.startswith(
                     "CS(PREDICATE_MEANING,")
                 or item.identity.key.local in {
                     "CS(EVIDENCE_SCHEMA,none)",
                     "CS(EVIDENCE_SCHEMA,verification)",
                     "CS(ACCESS_BOUNDARY,literal)",
                     "CS(ACCESS_BOUNDARY,task_final_evidence)",
                     "CS(UNKNOWN_BEHAVIOR,not_applicable)",
                     "CS(UNKNOWN_BEHAVIOR,task)",
                     "CS(EVALUATION_ERROR_BEHAVIOR,literal)",
                     "CS(EVALUATION_ERROR_BEHAVIOR,predicate)",
                     "CS(EVALUATION_ERROR_BEHAVIOR,term)",
                 }))
        for contract_record in retained_contracts:
            for field_name in contract_record.value.__dataclass_fields__:
                current = getattr(contract_record.value, field_name)
                if field_name == "owner_layer":
                    replacement_value = (
                        ref.Layer.SERVICE
                        if current is not ref.Layer.SERVICE else ref.Layer.SIGMA)
                elif field_name == "role":
                    replacement_value = ref.ContractRole.SEMANTIC_EXTENSION_PAYLOAD
                elif field_name == "type_admission_relation":
                    replacement_value = ref.TypeAdmissionRelation(str)
                else:
                    replacement_value = changed_field(current)
                mutation = replace(
                    contract_record.value, **{field_name: replacement_value})
                changed = _rewrite(
                    construction.universe,
                    {contract_record.identity: replace(
                        contract_record, value=mutation)})
                with self.subTest(
                        contract_complete_field=(
                            contract_record.identity.key.local, field_name)):
                    self.assertNotEqual(
                        _replay_assertion(changed, ref.replay(changed)),
                        frozen_core_assertion)
        self.assertEqual(
            {item.identity.key.local: len(item.value.supported_targets)
             for item in package.services},
            {"CAP(functions)": 3, "CAP(predicates)": 8,
             "CAP(profile)": 1, "CAP(bounds)": 1,
             "CAP(confluence)": 1, "LEX_CAP": 1})
        benv = package.certificates[0]
        self.assertEqual(benv.identity.key, benv.value.certificate_key)
        self.assertEqual(
            (benv.value.certificate_key.owner,
             benv.value.certificate_key.namespace,
             benv.value.certificate_key.local),
            ("PLUGIN_CERTIFICATE_ISSUER(CK)", "coding.certificate",
             "bundle_bounds_unsat"),
        )
        self.assertEqual(
            (benv.value.certificate_kind,
             benv.value.request_binding.key.local,
             tuple(item.key.local for item in benv.value.subjects),
             benv.value.environment.key.local,
             benv.value.capability_key.key.local,
             benv.value.fragment.key.local,
             benv.value.dependencies.key.local,
             benv.value.claimed_conclusion,
             benv.value.validator_key.key.local,
             benv.value.trust_root_key.key.local,
             benv.value.abstraction_class),
            ("CONTRADICTION_PROOF", "R_b", ("C_b",), "E_b",
             "CAP(bounds)", "BSOUND", "D_b", "CONSISTENCY_UNSAT",
             "CAP(validate_bounds)", "TRB", "SYMBOLIC"))
        for field_name in benv.value.__dataclass_fields__:
            mutation = replace(
                benv.value,
                **{field_name: changed_field(
                    getattr(benv.value, field_name))})
            changed = _rewrite(
                construction.universe,
                {benv.identity: replace(benv, value=mutation)})
            with self.subTest(benv_complete_field=field_name):
                self.assertNotEqual(
                    _replay_assertion(changed, ref.replay(changed)),
                    frozen_core_assertion)

        empty_package = replace(_at(construction.universe, construction.package), value=replace(_at(construction.universe, construction.package).value, declarations=(), pair_declarations=(), bindings=(), pair_bindings=(), profile_bindings=(), model_contracts=(), aliases=(), services=(), certificates=(), authority_facts=(), compatibility_claims=(), migrations=(), semantic_extensions=()))
        empty_result = ref.replay(_rewrite(construction.universe, {construction.package: empty_package}))
        self.assertNotEqual(empty_result, replayed)
        self.assertEqual(empty_result.formation, ref.Formation.MALFORMED)
        removed_result = ref.replay(_rewrite(construction.universe, {construction.package: None}))
        self.assertEqual(removed_result.formation, ref.Formation.MALFORMED)

        task_type = next(
            item for item in ref.compose_records(construction.universe.records).records
            if isinstance(item.value, ref.TypeDeclaration)
            and item.identity.key.local == "T(TaskSpec)"
        )
        reduced_type = replace(
            task_type,
            value=replace(task_type.value, proper_declaration_dependencies=frozenset()),
        )
        self.assertEqual(
            ref.replay(_rewrite(construction.universe, {task_type.identity: reduced_type})).formation,
            ref.Formation.MALFORMED,
        )
        changed_domain = replace(
            task_type,
            value=replace(
                task_type.value,
                admitted_value_domain=replace(
                    task_type.value.admitted_value_domain,
                    type_admission_relation=ref.TypeAdmissionRelation(str),
                ),
            ),
        )
        self.assertEqual(
            ref.replay(_rewrite(construction.universe, {task_type.identity: changed_domain})).formation,
            ref.Formation.MALFORMED,
        )
        admitted = ref.TypedValue(task_type.value.type_key, construction.task)
        self.assertEqual(ref.admit_typed_value(task_type.value, admitted).tag, "ADMITTED")
        forged = object.__new__(cp.TaskSpec)
        object.__setattr__(forged, "criteria", frozenset({object()}))
        object.__setattr__(forged, "required_verifications", frozenset())
        rejected = ref.TypedValue(task_type.value.type_key, forged)
        self.assertEqual(ref.admit_typed_value(task_type.value, rejected).tag, "NOT_ADMITTED")
        forged_size = object.__new__(cp.ByteSize)
        object.__setattr__(forged_size, "kib", True)
        self.assertFalse(cp.admitted_closed_value(cp.ByteSize, forged_size))
        self.assertFalse(cp.admitted_closed_value(frozenset, frozenset({cp.FieldId("not-a-path")})))
        self.assertTrue(cp.admitted_closed_value(
            cp.admission_type("ArtifactRole"), cp.OtherArtifactRole("private")))
        self.assertTrue(cp.admitted_closed_value(
            cp.admission_type("Format"), cp.OtherFormat("custom")))
        forged_subject = object.__new__(cp.SubjectId)
        object.__setattr__(forged_subject, "tag", "REQUEST_SUBJECT")
        object.__setattr__(forged_subject, "atom", "request")
        self.assertFalse(cp.admitted_closed_value(cp.SubjectId, forged_subject))
        with self.assertRaises(ValueError):
            cp.ObservationValue(cp.ObservationValueTag.BEHAVIOR_CONFLICT, (frozenset(),))
        with self.assertRaises(ValueError):
            cp.ObservationValue(
                cp.ObservationValueTag.CORRESPONDENCE_VALUE,
                (((cp.FieldId("field"), 1),), ()),
            )
        self.assertNotEqual(cp.CommandId("same"), cp.ContactClass("same"))
        self.assertNotEqual(cp.ContactClass("same"), cp.ReleaseId("same"))
        self.assertNotEqual(cp.SnapshotIdentity(construction.snapshot), construction.snapshot)

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
        wrong_snapshot_record = replace(verification, snapshot_identity=cp.SnapshotIdentity(cp.RepositorySnapshot(())), evidence_refs=frozenset({wrong_snapshot_ref}))
        wrong_snapshot_entry = cp.CodingEvidenceEntry(wrong_snapshot_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.VERIFICATION, wrong_snapshot_record))
        self.assertEqual(cp.verification_passed(verification.spec, construction.snapshot, frozenset({wrong_snapshot_entry})).truth, cp.Truth.UNKNOWN)
        wrong_observation_ref = cp.EvidenceRef("auditor", "coding", "verification/wrong-observation", cp.VERIFICATION_SCHEMA)
        wrong_observation = replace(verification.observation, values=((next(iter(verification.observation.values))[0], cp.ObservationValue(cp.ObservationValueTag.ABSENT)),))
        wrong_observation_record = replace(verification, observation=wrong_observation, evidence_refs=frozenset({wrong_observation_ref}))
        wrong_observation_entry = cp.CodingEvidenceEntry(wrong_observation_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.VERIFICATION, wrong_observation_record))
        # The four K3-S verification equations do not compare a payload value
        # to a direct re-observation: matching spec/snapshot/subject/evidence
        # membership is sufficient even for another admitted observation value.
        self.assertEqual(cp.verification_passed(verification.spec, construction.snapshot, frozenset({wrong_observation_entry})).truth, cp.Truth.TRUE)
        inconclusive_ref = cp.EvidenceRef("auditor", "coding", "verification/inconclusive", cp.VERIFICATION_SCHEMA)
        inconclusive_record = replace(verification, status=cp.VerificationStatus.INCONCLUSIVE, evidence_refs=frozenset({inconclusive_ref}))
        inconclusive_entry = cp.CodingEvidenceEntry(inconclusive_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.VERIFICATION, inconclusive_record))
        self.assertEqual(cp.verification_passed(verification.spec, construction.snapshot, frozenset({inconclusive_entry})).truth, cp.Truth.UNKNOWN)
        self.assertEqual(cp.OtherArtifactRole("private"), cp.OtherArtifactRole("private"))
        self.assertNotEqual(cp.OtherArtifactRole("private"), cp.ArtifactRole.SOURCE)
        self.assertEqual(cp.OtherFormat("custom"), cp.OtherFormat("custom"))
        with self.assertRaises(ValueError):
            cp.FieldValue(cp.FieldValueTag.BOOL, 1)
        first = cp.Path((cp.PathSegment("a"),))
        second = cp.Path((cp.PathSegment("b"),))
        artifact_a = cp.ArtifactContent(cp.ArtifactTag.TEXT, cp.OtherArtifactRole("private"), cp.OtherFormat("custom"), cp.ByteSize(1), cp.ContentIdentity("a"))
        artifact_b = cp.ArtifactContent(cp.ArtifactTag.TEXT, cp.ArtifactRole.SOURCE, cp.Format.TEXT, cp.ByteSize(2), cp.ContentIdentity("b"))
        self.assertEqual(cp.RepositorySnapshot(((first, artifact_a), (second, artifact_b))), cp.RepositorySnapshot(((second, artifact_b), (first, artifact_a))))

        # The retained K3-S TYPE_X table is closed and every row has an
        # independently admitted positive witness.
        subject_id = cp.SubjectId(cp.SubjectTag.REQUEST, "request")
        behavior = cp.BehaviorValue(cp.BehaviorTag.ACCEPTED)
        body = cp.ArtifactBody(cp.ArtifactBodyTag.TEXT, cp.ContentIdentity("body"))
        change = cp.ChangeEntry(cp.ChangeKind.CREATED, new=artifact_b)
        change_set = cp.ChangeSet(((first, change),))
        implementation = cp.ImplementationEvidence(
            cp.ImplementationEvidenceTag.CONCRETE_IMPLEMENTATION,
            "contract", cp.SnapshotIdentity(construction.snapshot),
            implementation_identity="implementation")
        implementation_ref = cp.EvidenceRef(
            "builder", "coding", "implementation",
            cp.IMPLEMENTATION_PROFILE_SCHEMA)
        implementation_payload = cp.CodingEvidencePayload(
            cp.EvidencePayloadTag.IMPLEMENTATION_PROFILE, implementation)
        implementation_entry = cp.CodingEvidenceEntry(
            implementation_ref, implementation_payload)
        abstract = cp.AbstractCoverageResult(cp.AbstractCoverageTag.NONE)
        profile_subject = cp.ImplementationCoverageSubject(
            "contract", construction.task, construction.snapshot,
            frozenset({implementation_entry}), cp.Eval(cp.Truth.TRUE), abstract)
        clause_subject = cp.AuthorityAttestationSubjectIdentity(
            cp.AuthoritySubjectTag.CLAUSE, construction.declaration,
            clause_tag=cp.AuthorityClauseTag.BOUNDS)
        attestation = cp.AuthorityAttestationValue(
            construction.declaration, construction.binding, "principal",
            "NORMATIVE", clause_subject)
        service_subject = cp.ServiceAdmissionSubject(
            cp.ServiceSubjectTag.PAIR_COHERENCE,
            pair=construction.declaration,
            scope_binding=construction.binding,
            occurrence_binding=construction.binding,
            trace_domain=cp.PairTraceDomain.ALL_ADMITTED_TRACES,
            compared_fields=cp.PairComparedFields.COMPLETE_EVAL_RECORD)
        evolution_subject = cp.EvolutionAdmissionSubject(
            cp.EvolutionSubjectTag.COMPATIBILITY_CLAIM,
            construction.declaration, source_abi=fx.V1, target_abi=fx.V1,
            source_keys=frozenset({construction.declaration}),
            target_keys=frozenset({construction.binding}))
        test_payload = cp.TestEventPayload(
            verification.spec, verification.snapshot_identity,
            verification.status, verification.evidence_refs)
        selector = verification.spec.subject.selector
        assert selector is not None
        samples = {
            "PathSegment": first.segments[0], "Path": first,
            "PathSet": frozenset({first}), "ArtifactRole": cp.ArtifactRole.SOURCE,
            "Format": cp.Format.TEXT, "StorageBackend": cp.StorageBackend.LOCAL,
            "ByteSize": cp.ByteSize(1), "ContentIdentity": cp.ContentIdentity("c"),
            "FieldId": cp.FieldId("f"),
            "FieldValue": cp.FieldValue(cp.FieldValueTag.INT, 1),
            "SubjectId": subject_id, "BehaviorValue": behavior,
            "ArtifactBody": body, "ArtifactBodyKind": cp.ArtifactBodyKind.TEXT,
            "ArtifactContent": artifact_b,
            "ObservationValue": cp.ObservationValue(cp.ObservationValueTag.PRESENT),
            "RepositorySnapshot": construction.snapshot,
            "SnapshotIdentity": cp.SnapshotIdentity(construction.snapshot),
            "ChangeEntry": change, "ChangeSet": change_set,
            "ArtifactSelector": selector, "ArtifactProjection": cp.ArtifactProjection(cp.ProjectionTag.CONTENT),
            "Coverage": cp.Coverage(cp.CoverageTag.COMPLETE),
            "ObservationSpec": verification.spec.subject,
            "ObservationResult": verification.observation,
            "ObservationRelation": cp.ObservationRelation(cp.ObservationRelationTag.EQUAL),
            "VerificationStatus": cp.VerificationStatus.PASS,
            "VerificationSpec": verification.spec, "VerificationRecord": verification,
            "ImplementationEvidence": implementation,
            "CodingEvidencePayload": implementation_payload,
            "CodingEvidenceEntry": implementation_entry,
            "AbstractCoverageResult": abstract,
            "ImplementationCoverageSubject": profile_subject,
            "PairTraceDomain": cp.PairTraceDomain.ALL_ADMITTED_TRACES,
            "PairComparedFields": cp.PairComparedFields.COMPLETE_EVAL_RECORD,
            "AuthorityClauseTag": cp.AuthorityClauseTag.BOUNDS,
            "AuthorityAttestationSubjectIdentity": clause_subject,
            "AuthorityAttestationValue": attestation,
            "ServiceAdmissionSubject": service_subject,
            "EvolutionAdmissionSubject": evolution_subject,
            "Criterion": next(iter(construction.task.criteria)),
            "TaskSpec": construction.task, "ChangeKind": cp.ChangeKind.CREATED,
            "CommandId": cp.CommandId("command"),
            "ContactClass": cp.ContactClass("contact"),
            "ReleaseId": cp.ReleaseId("release"), "Purpose": cp.Purpose("purpose"),
            "EventPattern": cp.EventPattern(cp.PatternKind.ANY_EVENT, event_key=cp.EventKind.TEST),
            "CommandEventPayload": cp.CommandEventPayload(cp.CommandId("command"), cp.Purpose("purpose")),
            "TestEventPayload": test_payload,
            "PathChangeEventPayload": cp.PathChangeEventPayload(first, change),
            "NetworkContactEventPayload": cp.NetworkContactEventPayload(cp.ContactClass("contact"), cp.Purpose("purpose")),
            "ReleaseEventPayload": cp.ReleaseEventPayload(cp.ReleaseId("release"), cp.SnapshotIdentity(construction.snapshot)),
            "DependencyRefreshEventPayload": cp.DependencyRefreshEventPayload(selector, cp.SnapshotIdentity(construction.snapshot)),
        }
        self.assertEqual(set(samples), set(cp._ADMISSION_TYPES))
        for type_name, sample in samples.items():
            with self.subTest(retained_type=type_name):
                self.assertTrue(cp.admitted_closed_value(cp.admission_type(type_name), sample))
        forged_change = object.__new__(cp.ChangeEntry)
        object.__setattr__(forged_change, "kind", cp.ChangeKind.CREATED)
        object.__setattr__(forged_change, "old", artifact_b)
        object.__setattr__(forged_change, "new", artifact_b)
        self.assertFalse(cp.admitted_closed_value(cp.ChangeEntry, forged_change))
        forged_verification = object.__new__(cp.VerificationRecord)
        for name, value in vars(verification).items():
            object.__setattr__(forged_verification, name, value)
        object.__setattr__(forged_verification, "evidence_refs", frozenset({implementation_ref}))
        self.assertFalse(cp.admitted_closed_value(cp.VerificationRecord, forged_verification))
        forged_entry = replace(
            implementation_entry, reference=next(iter(verification.evidence_refs)))
        self.assertFalse(cp.admitted_closed_value(cp.CodingEvidenceEntry, forged_entry))
        forged_service = replace(service_subject, trace_domain="ALL_ADMITTED_TRACES")
        self.assertFalse(cp.admitted_closed_value(cp.admission_type("ServiceAdmissionSubject"), forged_service))
        forged_evolution = replace(evolution_subject, source_keys=frozenset({"raw-key"}))
        self.assertFalse(cp.admitted_closed_value(cp.EvolutionAdmissionSubject, forged_evolution))

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
            replace(descriptor, proper_semantic_dependencies=frozenset({construction.binding}), dependency_closure=frozenset()),
            replace(descriptor, required_evidence=construction.binding),
            replace(descriptor, required_trust_roots=frozenset({construction.binding})),
            replace(descriptor, supported_targets=frozenset({
                ref.BindingTarget(fx.rid(
                    ref.RecordKind.BINDING, "rogue",
                    namespace="assertion.falsifier"))})),
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
        sigma = _at(construction.universe, construction.sigma_spec)
        renamed = replace(sigma, value=replace(sigma.value, relation_name="not_a_frozen_relation"))
        with self.assertRaises(ref.FiniteProfileError):
            ref.evaluate_invocation(construction.request, ref.compose_records(_rewrite(construction.universe, {sigma.identity: renamed}).records))

        descriptors = {
            item.identity.key.local: item.value
            for item in _at(construction.universe, construction.package).value.services
        }
        authoritative_roots = {
            "CAP(bounds)": ref.RecordIdentity(
                ref.RecordKind.SEMANTIC_ENVIRONMENT,
                ref.ExactKey("capknow.semantic", "bounds.environment",
                             "E_b", ref.Version((1,)))),
            "CAP(confluence)": ref.RecordIdentity(
                ref.RecordKind.SEMANTIC_ENVIRONMENT,
                ref.ExactKey("capknow.semantic", "confluence.environment",
                             "E_c", ref.Version((1,)))),
            "LEX_CAP": ref.RecordIdentity(
                ref.RecordKind.SEMANTIC_ENVIRONMENT,
                ref.ExactKey("capknow.semantic", "lexical.environment",
                             "E_lex", ref.Version((1,)))),
        }
        for local, identity in authoritative_roots.items():
            carrier = composition.at(identity)
            self.assertIsNotNone(carrier)
            assert carrier is not None
            expected_authority = {
                "CAP(bounds)": {"AFB(b,1)"},
                "CAP(confluence)": {"AFB(c,1)", "AFB(c,2)"},
                "LEX_CAP": set(),
            }[local]
            self.assertEqual(
                {item.key.local for item in carrier.value.authority_facts},
                expected_authority)
            missing = ref.compose_records(tuple(
                item for item in composition.records
                if item.identity != identity))
            with self.subTest(missing_environment=identity.key.local):
                with self.assertRaisesRegex(ValueError, "unresolved"):
                    ref.dependency_reachability(
                        descriptors[local].proper_semantic_dependencies,
                        missing)
        for local, identity in (
            ("CAP(bounds)", ref.RecordIdentity(
                ref.RecordKind.TRUST_ROOT,
                ref.ExactKey("capknow.semantic", "bounds.trust", "TRB",
                             ref.Version((1,))))),
            ("CAP(confluence)", ref.RecordIdentity(
                ref.RecordKind.TRUST_ROOT,
                ref.ExactKey("capknow.semantic", "confluence.trust",
                             "ROOT_TR_c", ref.Version((1,))))),
        ):
            missing = ref.compose_records(tuple(
                item for item in composition.records
                if item.identity != identity))
            with self.subTest(missing_trust_root=identity.key.local):
                with self.assertRaisesRegex(ValueError, "unresolved"):
                    ref.dependency_reachability(
                        descriptors[local].proper_semantic_dependencies,
                        missing)
        foreign_root = ref.DependencyKey(
            ref.DependencyTag.TRUST_ROOT,
            ref.ExactKey("foreign.owner", "foreign.trust", "TR",
                         ref.Version((1,))))
        with self.assertRaisesRegex(ValueError, "unresolved"):
            ref.dependency_reachability(frozenset({foreign_root}), composition)
        foreign_environment = ref.RecordIdentity(
            ref.RecordKind.SEMANTIC_ENVIRONMENT,
            ref.ExactKey("foreign.owner", "foreign.environment", "E",
                         ref.Version((1,))))
        with self.assertRaisesRegex(ValueError, "unresolved"):
            ref.derive_dependency_environment(
                frozenset(), frozenset({foreign_environment}), composition)
        bounds_root = composition.at(ref.RecordIdentity(
            ref.RecordKind.TRUST_ROOT,
            ref.ExactKey("capknow.semantic", "bounds.trust", "TRB",
                         ref.Version((1,)))))
        assert bounds_root is not None
        self.assertEqual(
            {item.key.local for item in bounds_root.value.trusted_validators},
            {"CAP(bounds)", "CAP(validate_bounds)"})
        self.assertEqual(len(bounds_root.value.permitted_targets), 3)
        summary = next(iter(model.capability_summaries))
        with self.assertRaisesRegex(TypeError, "DependencyKey"):
            replace(summary, dependency_scope=frozenset({construction.binding}))

    def test_k3x_04_declaration_binding_and_capability_are_derived(self) -> None:
        construction = fx.core_construction()
        environment_record = _at(construction.universe, construction.semantic_environment)
        dependency_record = _at(construction.universe, construction.dependency_environment)

        no_declaration_env = replace(environment_record, value=replace(environment_record.value, declarations=(), mechanically_extracted_dependencies=frozenset()))
        no_declaration_dep = replace(dependency_record, value=replace(
            dependency_record.value, syntax_root_keys=frozenset(),
            expanded_root_keys=frozenset({ref.dependency_key(
                construction.binding)})))
        no_declaration = _rewrite(construction.universe, {construction.declaration: None, construction.semantic_environment: no_declaration_env, construction.dependency_environment: no_declaration_dep})
        declaration_result = ref.replay(no_declaration)
        self.assertEqual(declaration_result.formation, ref.Formation.MALFORMED)

        no_binding_env = replace(environment_record, value=replace(
            environment_record.value, bindings=(),
            mechanically_extracted_dependencies=_asserted_syntax_keys("task")))
        no_binding_dep = replace(dependency_record, value=replace(
            dependency_record.value, subject_root_keys=frozenset(),
            expanded_root_keys=frozenset({ref.dependency_key(
                construction.declaration)})))
        no_binding = _rewrite(construction.universe, {construction.binding: None, construction.semantic_environment: no_binding_env, construction.dependency_environment: no_binding_dep})
        binding_result = ref.replay(no_binding)
        self.assertEqual(binding_result.formation, ref.Formation.MALFORMED)

        model_record = _at(construction.universe, construction.model)
        no_capability_model = replace(model_record, value=replace(model_record.value, capability_summaries=frozenset()))
        no_capability = _rewrite(construction.universe, {construction.capability: None, construction.model: no_capability_model})
        capability_result = ref.replay(no_capability)
        self.assertEqual((capability_result.closure, capability_result.evaluability, capability_result.lifecycle), (ref.Closure.CLOSED, ref.Evaluability.MISSING, "CAPABILITY_ABSENT"))
        empty_environment = replace(environment_record, value=ref.SemanticEnvironment(fx.V1, (), (), ()))
        self.assertEqual(ref.replay(_rewrite(construction.universe, {construction.semantic_environment: empty_environment})).formation, ref.Formation.MALFORMED)

    def test_k3x_05_pair_producers_validation_refs_and_proper_cycle(self) -> None:
        construction = fx.pair_construction()
        admitted = ref.replay(construction.universe)
        self.assertIsInstance(admitted, ref.PairReplay)
        self.assertEqual(admitted.result.result.tag, "PAIR_COHERENCE_ADMITTED")
        binding = _at(construction.universe, construction.pair_binding)
        without_pair_binding = _rewrite(
            construction.universe, {binding.identity: None})
        self.assertNotIsInstance(ref.replay(without_pair_binding), ref.PairReplay)
        pair_composition = ref.compose_records(construction.universe.records)
        pair_declaration = pair_composition.at(ref.RecordIdentity(
            ref.RecordKind.PAIR_DECLARATION, binding.value.pair_key))
        assert pair_declaration is not None
        pair_target_roots = ref._capability_target_roots(
            ref.PairTarget(pair_declaration.identity), pair_composition)
        self.assertEqual(pair_target_roots, frozenset({
            _asserted_dependency_key(pair_declaration.identity),
            _asserted_dependency_key(binding.identity),
            _asserted_dependency_key(binding.value.occurrence_bundle),
        }))
        occurrence_bundle = _at(
            construction.universe, binding.value.occurrence_bundle)
        occurrence_symbol = ref.K1SyntaxKey(
            ref.K1SyntaxTag.SYMBOL,
            ref.ExactKey("capknow.semantic", "coding.symbol",
                         "SP(refresh_occurred)", ref.Version((1,))))
        occurrence_syntax = frozenset({occurrence_symbol})
        derived_occurrence = ref.derive_dependency_environment(
            occurrence_syntax, frozenset({binding.identity}),
            pair_composition)
        asserted_occurrence = _asserted_dependency_environment(
            occurrence_syntax, frozenset({binding.identity}),
            pair_composition)
        self.assertEqual(derived_occurrence, asserted_occurrence)
        self.assertIn(
            _asserted_dependency_key(occurrence_bundle.identity),
            derived_occurrence.expanded_root_keys)
        self.assertEqual(len(binding.value.validation_references), 2)
        self.assertFalse(binding.value.validation_references & binding.value.proper_semantic_dependencies)
        manifest = construction.manifest
        self.assertEqual({item.identity.key.local for item in manifest if isinstance(item.value, ref.ContractSpec) and item.value.owner_layer is ref.Layer.SERVICE}, {"PSOUND", "PCOMPLETE", "PEVIDENCE", "PFAILURE"})
        self.assertTrue({"E_p", "D_p", "PairFullEvalProof", "refresh_full_eval", "R_p", "TRP", "PCERT"} <= {item.identity.key.local for item in manifest})

        removed_producer = _rewrite(construction.universe, {construction.producer_records[1].identity: None})
        self.assertEqual(ref.replay(removed_producer).details[0], "INCOMPLETE_PRODUCER_SET")
        cert_producer = construction.producer_records[1]
        self_trust = replace(cert_producer, value=replace(cert_producer.value, producer="capknow.semantic"))
        self.assertEqual(ref.replay(_rewrite(construction.universe, {cert_producer.identity: self_trust})).details[0], "PAIR_PRODUCER_MISMATCH")
        capability_producer = next(
            item for item in construction.producer_records
            if item.value.subject == binding.value.validator
        )
        equal_sets = replace(capability_producer, value=replace(capability_producer.value, producer="capknow.audit.pair-proof"))
        self.assertEqual(ref.replay(_rewrite(construction.universe, {capability_producer.identity: equal_sets})).details[0], "PAIR_PRODUCER_MISMATCH")
        for index, producer_record in enumerate(construction.producer_records):
            rogue = fx.record(
                ref.RecordKind.PRODUCER, f"rogue.{index}",
                ref.ProducerRecord(
                    producer_record.value.subject, "rogue.producer",
                    producer_record.value.producer_role),
                namespace="pair.rogue-producer")
            changed = replace(
                construction.universe,
                records=(*construction.universe.records, rogue))
            with self.subTest(rogue_pair_producer=producer_record.value.subject):
                rejected = ref.replay(changed)
                self.assertIsInstance(rejected, ref.Judgment)
                self.assertEqual(rejected.details[0], "PAIR_PRODUCER_MISMATCH")
        missing_validation = _rewrite(construction.universe, {next(iter(construction.validation_references)): None})
        self.assertNotEqual(ref.replay(missing_validation), admitted)
        pair_request = _at(construction.universe, construction.request)
        pair_trust = _at(construction.universe, pair_request.value.trust_environment)
        incompatible_trust = replace(pair_trust, value=replace(pair_trust.value, root_judgments=((pair_trust.value.roots[0], ref.TrustRootJudgment(ref.TrustState.INCOMPATIBLE, reasons=("TEST",))),)))
        self.assertEqual(ref.replay(_rewrite(construction.universe, {pair_trust.identity: incompatible_trust})).tag, "INCOMPATIBLE")
        certificate = _at(construction.universe, construction.certificate)
        wrong_subject = replace(certificate, value=replace(certificate.value, subjects=(construction.request,)))
        self.assertEqual(ref.replay(_rewrite(construction.universe, {construction.certificate: wrong_subject})).details[0], "PAIR_CERTIFICATE_ENVELOPE")
        empty_pair_package = next(record for record in construction.universe.records if isinstance(record.value, ref.PluginPackage))
        empty_pair_package = replace(empty_pair_package, value=replace(empty_pair_package.value, declarations=(), pair_declarations=(), bindings=(), pair_bindings=(), profile_bindings=(), model_contracts=(), aliases=(), services=(), certificates=(), authority_facts=(), compatibility_claims=(), migrations=(), semantic_extensions=()))
        self.assertNotEqual(ref.replay(_rewrite(construction.universe, {empty_pair_package.identity: empty_pair_package})), admitted)

        foreign_pair = fx.rid(ref.RecordKind.PAIR_DECLARATION, "PAIR(foreign)", namespace="pair")
        request_mutations = (
            replace(pair_request.value, abi_version=fx.V2),
            replace(pair_request.value, pair_key=foreign_pair),
            replace(pair_request.value, semantic_environment=pair_request.value.trust_environment),
            replace(pair_request.value, trust_environment=pair_request.value.semantic_environment),
            replace(pair_request.value, complete_dependencies=pair_request.value.semantic_environment),
            replace(pair_request.value, capability_target=ref.PairTarget(foreign_pair)),
            replace(pair_request.value, capability_key=construction.certificate),
        )
        for mutation in request_mutations:
            with self.subTest(pair_request_field=mutation):
                changed = replace(pair_request, value=mutation)
                self.assertNotIsInstance(
                    ref.replay(_rewrite(construction.universe, {pair_request.identity: changed})),
                    ref.PairReplay,
                )

        pair_environment = _at(
            construction.universe, pair_request.value.semantic_environment)
        for mutation in (
            replace(pair_environment.value, abi_version=fx.V2),
            replace(pair_environment.value, chi_c=(("rogue", True),)),
            replace(pair_environment.value,
                    mechanically_extracted_dependencies=frozenset()),
        ):
            with self.subTest(pair_environment_field=mutation):
                rejected = ref.replay(_rewrite(
                    construction.universe,
                    {pair_environment.identity:
                     replace(pair_environment, value=mutation)}))
                self.assertIsInstance(rejected, ref.Judgment)
                self.assertEqual(rejected.details[0], "PAIR_SEMANTIC_ENVIRONMENT")
        pair_dependency = _at(
            construction.universe, pair_request.value.complete_dependencies)
        dependency_mutations = (
            replace(pair_dependency.value, syntax_root_keys=frozenset()),
            replace(pair_dependency.value, subject_root_keys=frozenset()),
            replace(pair_dependency.value, binding_association_edges=frozenset()),
            replace(pair_dependency.value, expanded_root_keys=frozenset()),
            replace(pair_dependency.value, proper_dependencies=frozenset()),
            replace(pair_dependency.value, transitive_dependency_closure=frozenset()),
        )
        for mutation in dependency_mutations:
            with self.subTest(pair_dependency_field=mutation):
                rejected = ref.replay(_rewrite(
                    construction.universe,
                    {pair_dependency.identity:
                     replace(pair_dependency, value=mutation)}))
                self.assertNotIsInstance(rejected, ref.PairReplay)

        bundle = _at(construction.universe, binding.value.occurrence_bundle)
        binding_mutations = (
            replace(binding.value, pair_key=foreign_pair.key),
            replace(binding.value, scope_binding_key=binding.value.occurrence_bundle),
            replace(binding.value, occurrence_binding_key=binding.value.occurrence_bundle),
            replace(binding.value, occurrence_model_contract_key=binding.value.scope_binding_key),
            replace(binding.value, occurrence_bundle=binding.value.scope_binding_key),
            replace(binding.value, certificate=binding.value.validator),
            replace(binding.value, validator=binding.value.certificate),
            replace(binding.value, proper_semantic_dependencies=frozenset()),
            replace(binding.value, dependency_closure=frozenset()),
            replace(binding.value, validation_references=frozenset()),
            replace(binding.value, admission=ref.IndependentCoherenceProof(
                binding.value.occurrence_bundle,
                binding.value.validator, binding.value.certificate)),
        )
        for mutation in binding_mutations:
            with self.subTest(pair_binding_field=mutation):
                changed = replace(binding, value=mutation)
                self.assertNotIsInstance(
                    ref.replay(_rewrite(construction.universe, {binding.identity: changed})),
                    ref.PairReplay,
                )
        scope = _at(construction.universe, binding.value.scope_binding_key)
        scope_mutations = (
            replace(scope.value, binding_key=fx.key("wrong", namespace="pair.binding")),
            replace(scope.value, declaration=foreign_pair),
            replace(scope.value, binding_kind="FUNCTION"),
            replace(scope.value, meaning_contract=construction.request),
            replace(scope.value, permitted_facet_inputs=()),
            replace(scope.value, proper_semantic_dependencies=frozenset()),
            replace(scope.value, dependency_closure=frozenset()),
            replace(scope.value, evidence_schema=construction.request),
            replace(scope.value, access_boundary=construction.request),
            replace(scope.value, unknown_contract=construction.request),
            replace(scope.value, evaluation_error_contract=construction.request),
            replace(scope.value, determinism_rule="WRONG"),
        )
        for mutation in scope_mutations:
            with self.subTest(pair_scope_field=mutation):
                changed = replace(scope, value=mutation)
                self.assertNotIsInstance(
                    ref.replay(_rewrite(construction.universe, {scope.identity: changed})),
                    ref.PairReplay,
                )
        changed_bundle = replace(bundle, value=replace(bundle.value, permitted_facet_inputs=(frozenset(),)))
        self.assertNotIsInstance(
            ref.replay(_rewrite(construction.universe, {bundle.identity: changed_bundle})),
            ref.PairReplay,
        )
        pair_composition = ref.compose_records(construction.universe.records)
        pair_evidence = next(
            item for item in pair_composition.records
            if isinstance(item.value, ref.EvidenceRecord)
            and item.identity.key.local == "PAIR_PROOF_REF"
        )
        for mutation in (
            replace(pair_evidence.value, issuer="foreign"),
            replace(pair_evidence.value, namespace="foreign"),
            replace(pair_evidence.value, local="foreign"),
            replace(pair_evidence.value, schema_contract=construction.request),
        ):
            self.assertNotIsInstance(
                ref.replay(_rewrite(construction.universe, {
                    pair_evidence.identity: replace(pair_evidence, value=mutation)
                })), ref.PairReplay,
            )
        for producer_record in construction.producer_records:
            with self.subTest(removed_exact_pair_producer=producer_record.identity):
                self.assertNotIsInstance(
                    ref.replay(_rewrite(construction.universe, {producer_record.identity: None})),
                    ref.PairReplay,
                )
        literal_records = tuple(
            item for item in pair_composition.records
            if item.identity.key.namespace in {
                "coding.literal", "coding.literal.binding", "coding.literal.model"
            }
        )
        self.assertEqual(len(literal_records), 9)
        for literal_record in literal_records:
            with self.subTest(removed_pair_literal_record=literal_record.identity):
                self.assertNotIsInstance(
                    ref.replay(_rewrite(construction.universe, {literal_record.identity: None})),
                    ref.PairReplay,
                )

        pair_models = tuple(
            item for item in ref.compose_records(construction.universe.records).records
            if isinstance(item.value, ref.ModelContract)
            and item.value.target_binding in {
                binding.value.scope_binding_key,
                binding.value.occurrence_binding_key,
            }
        )
        self.assertEqual(len(pair_models), 2)
        literal_models = tuple(
            item for item in ref.compose_records(construction.universe.records).records
            if isinstance(item.value, ref.ModelContract)
            and item.identity.key.namespace == "coding.literal.model"
        )
        self.assertEqual(len(literal_models), 3)
        for model in pair_models:
            with self.subTest(removed_pair_model=model.identity):
                self.assertNotIsInstance(
                    ref.replay(_rewrite(construction.universe, {model.identity: None})),
                    ref.PairReplay,
                )
            model_mutations = (
                replace(model.value, model_key=fx.key("wrong", namespace="pair.model")),
                replace(model.value, target_binding=foreign_pair),
                replace(model.value, exact_version=fx.V2),
                replace(model.value, exact_symbol_key=fx.key("wrong", namespace="pair.symbol")),
                replace(model.value, exact_argument_types=()),
                replace(model.value, exact_result_kind="TERM_RESULT"),
                replace(model.value, exact_facet_positions=()),
                replace(model.value, evidence_contract=construction.request),
                replace(model.value, unknown_contract=construction.request),
                replace(model.value, error_contract=construction.request),
                replace(model.value, semantic_contract=construction.request),
                replace(model.value, capability_summaries=frozenset()),
            )
            for mutation in model_mutations:
                with self.subTest(pair_model_field=model.identity, mutation=mutation):
                    changed = replace(model, value=mutation)
                    self.assertNotIsInstance(
                        ref.replay(_rewrite(construction.universe, {model.identity: changed})),
                        ref.PairReplay,
                    )

        admission_record = next(item for item in construction.manifest if isinstance(item.value, ref.CertificateAdmission))
        result_carrier = next(item for item in construction.manifest if isinstance(item.value, ref.PairValidationResult))
        standalone_mutations = (
            replace(admission_record, value=replace(admission_record.value, certificate=construction.request)),
            replace(admission_record, value=replace(admission_record.value, admitted_conclusion=ref.PairCoherenceAdmission(foreign_pair, construction.certificate))),
            replace(admission_record, identity=fx.rid(ref.RecordKind.OUTCOME, "PADMIT_WRONG", namespace="pair.admission")),
            replace(result_carrier, value=replace(result_carrier.value, pair_key=foreign_pair.key)),
            replace(result_carrier, value=replace(result_carrier.value, certificate_key=construction.request.key)),
            replace(result_carrier, value=replace(result_carrier.value, result=ref.PairCoherenceAdmission(foreign_pair, construction.certificate))),
            replace(result_carrier, identity=fx.rid(ref.RecordKind.RESULT, "PRESULT_WRONG", namespace="pair.result")),
        )
        for changed in standalone_mutations:
            self.assertNotIsInstance(
                ref.replay(_rewrite(construction.universe, {
                    admission_record.identity if isinstance(changed.value, ref.CertificateAdmission) else result_carrier.identity: changed
                })),
                ref.PairReplay,
            )
        dependency = _at(construction.universe, pair_request.value.complete_dependencies)
        for field_name in (
            "syntax_root_keys", "subject_root_keys", "binding_association_edges",
            "expanded_root_keys", "proper_dependencies",
            "transitive_dependency_closure", "validation_references",
        ):
            changed = replace(
                dependency,
                value=replace(dependency.value, **{field_name: frozenset()}),
            )
            with self.subTest(pair_dependency_field=field_name):
                self.assertNotIsInstance(
                    ref.replay(_rewrite(construction.universe, {dependency.identity: changed})),
                    ref.PairReplay,
                )

        baseline_cycle = fx.cycle_universe(False)
        self.assertEqual(
            ref.replay(baseline_cycle),
            (ref.Formation.WELL_FORMED, ref.Closure.CLOSED),
        )
        cycle_universe = fx.cycle_universe(True)
        cycle = ref.replay(cycle_universe)
        self.assertEqual(cycle[:2], (ref.Formation.MALFORMED, ref.Closure.NOT_APPLICABLE))
        self.assertEqual(cycle[2], ref.Judgment("MALFORMED", ("dependency cycle",)))
        baseline_records = {item.identity: item for item in ref.compose_records(baseline_cycle.records).records}
        cycle_records = {item.identity: item for item in ref.compose_records(cycle_universe.records).records}
        removed = frozenset(baseline_records) - frozenset(cycle_records)
        added = frozenset(cycle_records) - frozenset(baseline_records)
        self.assertEqual(
            {identity.key.local for identity in removed},
            {"CAP(functions)", "CAP(predicates)", "CAP(profile)",
             "CAP(bounds)", "CAP(confluence)", "LEX_CAP",
             "bundle_bounds_unsat",
             "CS(PREDICATE_MEANING,event_matches)"},
        )
        self.assertEqual(
            {identity.key.local for identity in added},
            {"CS(PREDICATE_MEANING,event_matches_cycle)"},
        )
        changed = {identity for identity in frozenset(baseline_records) & frozenset(cycle_records)
                   if baseline_records[identity] != cycle_records[identity]}
        self.assertEqual(
            {identity.key.local for identity in changed},
            {"coding-minimal", "BINDING(DP(event_matches))",
             "CS(ACCESS_BOUNDARY,pattern_event)",
             "MODEL_snapshot_of", "MODEL_changes_between", "MODEL_observe",
             "MODEL_observations_equal", "MODEL_task_accepts",
             "MODEL_dependency_metadata_changed", "MODEL_verification_passed",
             "MODEL_event_matches", "MODEL_event_occurred",
             "MODEL_refresh_scope", "MODEL_refresh_occurred"},
        )
        occurred_identity = next(
            identity for identity in baseline_records
            if identity.key.local == "BINDING(DP(event_occurred))")
        self.assertEqual(baseline_records[occurred_identity],
                         cycle_records[occurred_identity])
        for identity in frozenset(baseline_records) & frozenset(cycle_records) - changed:
            self.assertEqual(baseline_records[identity], cycle_records[identity])
        self.assertEqual(
            {item.identity.key.local for item in cycle_records.values()
             if isinstance(item.value, ref.ModelContract)
             and not item.identity.key.local.startswith("MODEL_LITERAL(")},
            {"MODEL_snapshot_of", "MODEL_changes_between", "MODEL_observe",
             "MODEL_observations_equal", "MODEL_task_accepts",
             "MODEL_dependency_metadata_changed", "MODEL_verification_passed",
             "MODEL_event_matches", "MODEL_event_occurred", "MODEL_refresh_scope",
             "MODEL_refresh_occurred"},
        )
        retained_core = fx.core_construction()
        retained_package = _at(retained_core.universe, retained_core.package).value
        baseline_package = next(
            item.value for item in baseline_records.values()
            if isinstance(item.value, ref.PluginPackage)
        )
        self.assertEqual(baseline_package, retained_package)
        for member in (
            *retained_package.declarations, *retained_package.pair_declarations,
            *retained_package.bindings, *retained_package.pair_bindings,
            *retained_package.profile_bindings, *retained_package.model_contracts,
            *retained_package.aliases, *retained_package.authority_facts,
            *retained_package.compatibility_claims, *retained_package.migrations,
            *retained_package.semantic_extensions,
        ):
            self.assertEqual(baseline_records[member.identity], member)

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
        missing_root = ref.replay(without_root)
        self.assertIsInstance(missing_root, ref.CompositionReplay)
        self.assertEqual(missing_root.formation, ref.Formation.MALFORMED)
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
        abs_item = cp.ImplementationEvidence(cp.ImplementationEvidenceTag.ABSTRACT_ACCEPTANCE, "contract", cp.SnapshotIdentity(construction.snapshot), certificate_key="cert")
        conc_item = cp.ImplementationEvidence(cp.ImplementationEvidenceTag.CONCRETE_IMPLEMENTATION, "contract", cp.SnapshotIdentity(construction.snapshot), implementation_identity="implementation")
        entries = frozenset({cp.CodingEvidenceEntry(abs_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.IMPLEMENTATION_PROFILE, abs_item)), cp.CodingEvidenceEntry(conc_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.IMPLEMENTATION_PROFILE, conc_item))})
        subject = cp.ImplementationCoverageSubject("contract", empty_task, construction.snapshot, entries, task_result, abstract)
        self.assertEqual(cp.implementation_evidence_profile(subject).tag, cp.ProfileTag.COMPLETE)
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, evidence_store=frozenset())).tag, cp.ProfileTag.INCOMPLETE)
        pending_ref = cp.EvidenceRef("builder", "coding", "pending", cp.IMPLEMENTATION_PROFILE_SCHEMA)
        pending = cp.ImplementationEvidence(cp.ImplementationEvidenceTag.DIMENSION_PENDING, "contract", cp.SnapshotIdentity(construction.snapshot), dimension="concrete_implementation_evidence", reason="PENDING")
        pending_entry = cp.CodingEvidenceEntry(pending_ref, cp.CodingEvidencePayload(cp.EvidencePayloadTag.IMPLEMENTATION_PROFILE, pending))
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, evidence_store=frozenset({pending_entry}))).tag, cp.ProfileTag.UNKNOWN)
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, task_result=cp.Eval(cp.Truth.FALSE))).tag, cp.ProfileTag.EVALUATION_ERROR)
        reasoning_error = cp.AbstractCoverageResult(cp.AbstractCoverageTag.REASONING, cp.ReasoningResult(cp.ReasoningTag.REASONING_ERROR, reasons=frozenset({"REASONER_FAILED"})))
        self.assertEqual(cp.implementation_evidence_profile(replace(subject, abstract_result=reasoning_error)).tag, cp.ProfileTag.INCOMPLETE)
        wrong_snapshot = cp.RepositorySnapshot(())
        wrong_item = replace(conc_item, snapshot_identity=cp.SnapshotIdentity(wrong_snapshot))
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
        command = cp.EventValue(cp.EventKind.COMMAND, cp.CommandEventPayload(cp.CommandId("build"), cp.Purpose("verification")))
        command_pattern = cp.EventPattern(cp.PatternKind.COMMAND_IS, command_id=cp.CommandId("build"))
        self.assertEqual(cp.event_matches(command_pattern, command).truth, cp.Truth.TRUE)
        self.assertEqual(cp.event_matches(replace(command_pattern, command_id=cp.CommandId("deploy")), command).truth, cp.Truth.FALSE)
        self.assertEqual(cp.event_occurred(command_pattern, frozenset({cp.TraceEvent(command, "agent")})).truth, cp.Truth.TRUE)
        verification = next(iter(construction.evidence)).payload.value
        test_event = cp.EventValue(cp.EventKind.TEST, cp.TestEventPayload(verification.spec, cp.SnapshotIdentity(construction.snapshot), cp.VerificationStatus.PASS, verification.evidence_refs))
        test_pattern = cp.EventPattern(cp.PatternKind.TEST_IS, verification_spec=verification.spec, statuses=frozenset({cp.VerificationStatus.PASS}))
        self.assertEqual(cp.event_matches(test_pattern, test_event).truth, cp.Truth.TRUE)
        with self.assertRaises(ValueError):
            cp.EventValue(cp.EventKind.COMMAND, ("command_id", "a", "command_id", "b"))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            cp.EventValue(cp.EventKind.RELEASE, cp.CommandEventPayload(cp.CommandId("x"), cp.Purpose("y")))

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
        refresh = cp.EventValue(cp.EventKind.DEPENDENCY_REFRESH, cp.DependencyRefreshEventPayload(refresh_selector, cp.SnapshotIdentity(after)))
        self.assertEqual(cp.refresh_scope(refresh).truth, cp.Truth.TRUE)
        source_refresh = replace(refresh, payload=replace(refresh.payload, selector=cp.ArtifactSelector(cp.SelectorTag.ROLE, role=cp.ArtifactRole.SOURCE)))
        self.assertEqual(cp.refresh_scope(source_refresh).truth, cp.Truth.FALSE)

    def test_k3x_09_confluence_contractspec_graph_errors_and_permutations(self) -> None:
        forward = fx.confluence_construction(fx.OrderTag.FORWARD)
        reverse = fx.confluence_construction(fx.OrderTag.REVERSE)
        forward_result = ref.replay(forward.universe)
        reverse_result = ref.replay(reverse.universe)
        self.assertEqual(forward_result, reverse_result)
        retained = fx.core_construction()
        retained_package = _at(retained.universe, retained.package)
        forward_package = next(
            item for item in forward.universe.records
            if isinstance(item.value, ref.PluginPackage)
        )
        reverse_package = next(
            item for item in reverse.universe.records
            if isinstance(item.value, ref.PluginPackage)
        )
        self.assertEqual(forward_package, retained_package)
        self.assertEqual(reverse_package, retained_package)
        retained_authority_literal = next(
            item for item in forward_package.value.declarations
            if isinstance(item.value, ref.DeclarationShape)
            and isinstance(item.value.literal_value,
                           cp.AuthorityAttestationValue))
        package_without_authority_literal = replace(
            forward_package, value=replace(
                forward_package.value,
                declarations=tuple(
                    item for item in forward_package.value.declarations
                    if item.identity != retained_authority_literal.identity)))
        self.assertNotIsInstance(
            ref.replay(_rewrite(
                forward.universe,
                {forward_package.identity: package_without_authority_literal})),
            ref.ObservationEvaluation)
        retained_confluence_literal_binding = next(
            item for item in forward_package.value.bindings
            if isinstance(item.value, ref.SemanticBinding)
            and item.value.binding_kind == "LITERAL"
            and item.identity in _at(
                forward.universe,
                forward.universe.request.semantic_environment).value.bindings)
        package_without_confluence_literal = replace(
            forward_package, value=replace(
                forward_package.value,
                bindings=tuple(
                    item for item in forward_package.value.bindings
                    if item.identity != retained_confluence_literal_binding.identity)))
        self.assertNotIsInstance(
            ref.replay(_rewrite(
                forward.universe,
                {forward_package.identity: package_without_confluence_literal})),
            ref.ObservationEvaluation)
        self.assertEqual(len(forward_result.observations), 2)
        absent_node = fx.rid(ref.RecordKind.BINDING, "absent", namespace="confluence.binding")
        with self.assertRaisesRegex(ValueError, "confluence capability/fragment"):
            ref.replay(replace(forward.universe, request=replace(forward.universe.request, nodes=(forward.node_one, absent_node))))
        wrong_kind_node = ref.RecordIdentity(ref.RecordKind.DECLARATION, forward.node_two.key)
        with self.assertRaisesRegex(ValueError, "confluence capability/fragment"):
            ref.replay(replace(forward.universe, request=replace(forward.universe.request, nodes=(forward.node_one, wrong_kind_node))))
        node_two = _at(forward.universe, forward.node_two)
        spec_two = _at(forward.universe, node_two.value.meaning_contract)
        malformed_query = ref.ObservationQuery(forward.node_one, ref.ObservationKind.TERM_RESULT, ("before", "after"))
        malformed_spec = replace(spec_two, value=replace(spec_two.value, observation_queries=(malformed_query,)))
        self.assertNotIsInstance(
            ref.replay(_rewrite(
                forward.universe, {spec_two.identity: malformed_spec})),
            ref.ObservationEvaluation,
        )
        service_bad_kind = replace(spec_two.value, owner_layer=ref.Layer.SERVICE, role=ref.ContractRole.SOUND_FRAGMENT, observation_queries=(ref.ObservationQuery(forward.node_one, ref.ObservationKind.PROFILE_RESULT, ("input",)),), support=frozenset({forward.node_one}))
        self.assertEqual(ref.validate_contract_spec(service_bad_kind).tag, "WELL_FORMED")
        duplicate_query = replace(service_bad_kind, observation_queries=service_bad_kind.observation_queries * 2)
        self.assertEqual(ref.validate_contract_spec(duplicate_query).details[0], "DUPLICATE_OBSERVATION_QUERY")
        dependency = _at(forward.universe, forward.universe.request.dependency_environment)
        expected_confluence_syntax = _asserted_syntax_keys("confluence")
        self.assertEqual(dependency.value.syntax_root_keys,
                         expected_confluence_syntax)
        semantic = _at(
            forward.universe, forward.universe.request.semantic_environment)
        self.assertEqual(semantic.value.mechanically_extracted_dependencies,
                         expected_confluence_syntax)
        self.assertEqual(
            dependency.value,
            _asserted_dependency_environment(
                expected_confluence_syntax, frozenset(),
                ref.compose_records(forward.universe.records)))
        with self.assertRaises(ValueError):
            ref.K1SyntaxKey(  # type: ignore[arg-type]
                "K1_FORMULA", fx.key("rogue", namespace="confluence"))
        rogue_root = ref.K1SyntaxKey(
            ref.K1SyntaxTag.DECLARATION,
            fx.key("T(rogue)", namespace="coding.type"))
        rogue_dependency = ref.lift_syntax_key(rogue_root)
        coherent_semantic = replace(
            semantic, value=replace(
                semantic.value,
                mechanically_extracted_dependencies=(
                    semantic.value.mechanically_extracted_dependencies
                    | {rogue_root})))
        coherent_dependency = replace(
            dependency, value=replace(
                dependency.value,
                syntax_root_keys=dependency.value.syntax_root_keys | {rogue_root},
                expanded_root_keys=dependency.value.expanded_root_keys
                | {rogue_dependency}))
        with self.assertRaises(ValueError):
            ref.replay(_rewrite(forward.universe, {
                semantic.identity: coherent_semantic,
                dependency.identity: coherent_dependency}))
        foreign = fx.rid(ref.RecordKind.DECLARATION, "foreign", namespace="confluence")
        foreign_dependency = ref.dependency_key(foreign)
        with self.assertRaises(TypeError):
            replace(dependency.value, expanded_root_keys=
                    dependency.value.expanded_root_keys | {foreign})
        dependency_mutations = {
            "syntax_root_keys": dependency.value.syntax_root_keys | frozenset({rogue_root}),
            "subject_root_keys": frozenset(),
            "binding_association_edges": frozenset({(foreign_dependency, foreign_dependency)}),
            "expanded_root_keys": dependency.value.expanded_root_keys | frozenset({foreign_dependency}),
            "proper_dependencies": frozenset(),
            "transitive_dependency_closure": frozenset(),
            "validation_references": frozenset({foreign}),
        }
        for field_name, value in dependency_mutations.items():
            changed = replace(
                dependency,
                value=replace(dependency.value, **{field_name: value}),
            )
            with self.subTest(confluence_dependency_field=field_name), self.assertRaises(ValueError):
                ref.replay(_rewrite(forward.universe, {dependency.identity: changed}))
        def assert_confluence_rejected(changed: ref.LogicalRecord) -> None:
            try:
                changed_result = ref.replay(_rewrite(forward.universe, {changed.identity: changed}))
            except ValueError:
                return
            self.assertNotEqual(changed_result, forward_result)

        composition = ref.compose_records(forward.universe.records)
        for node_identity in (forward.node_one, forward.node_two):
            node_binding = composition.at(node_identity)
            assert node_binding is not None and isinstance(node_binding.value, ref.SemanticBinding)
            self.assertEqual(ref.validate_binding(node_binding.value, composition).tag, "CLOSED")
            assert_confluence_rejected(replace(
                node_binding,
                value=replace(node_binding.value, permitted_facet_inputs=()),
            ))
            node_model = next(
                item for item in composition.records
                if isinstance(item.value, ref.ModelContract)
                and item.value.target_binding == node_identity
            )
            package_without_model = replace(
                forward_package,
                value=replace(
                    forward_package.value,
                    model_contracts=tuple(
                        item for item in forward_package.value.model_contracts
                        if item.identity != node_model.identity)))
            self.assertNotIsInstance(
                ref.replay(_rewrite(
                    forward.universe,
                    {forward_package.identity: package_without_model})),
                ref.ObservationEvaluation)
        confluence_service = next(item for item in composition.records if isinstance(item.value, ref.ServiceIdentity) and item.identity.key.local == "SK(confluence)")
        assert_confluence_rejected(replace(confluence_service, value=replace(confluence_service.value, abi_version=fx.V2)))
        assert_confluence_rejected(replace(confluence_service, value=replace(confluence_service.value, plugin_key=fx.key("foreign", namespace="plugin"))))
        confluence_root = next(item for item in composition.records if isinstance(item.value, ref.TrustRootRecord) and item.identity.key.local == "ROOT_TR_c")
        root_mutations = (
            replace(confluence_root.value, owner="foreign-policy"),
            replace(confluence_root.value, trusted_validators=frozenset()),
            replace(confluence_root.value, permitted_certificate_kinds=frozenset()),
            replace(confluence_root.value, permitted_targets=frozenset()),
            replace(confluence_root.value, adoption="IMPLICIT"),
        )
        for mutation in root_mutations:
            assert_confluence_rejected(replace(confluence_root, value=mutation))
        confluence_result = _at(forward.universe, forward.universe.request.result_record)
        bad_reason = ref.ReasoningUnknown("foreign", "coding.confluence", "fixture_inconclusive", (forward.universe.request.reasoning_request, forward.universe.request.observation_environment))
        assert_confluence_rejected(replace(confluence_result, value=replace(
            confluence_result.value,
            result=ref.ReasoningResultValue("COMPLETED_INCONCLUSIVE", frozenset({bad_reason})),
        )))
        producer = next(item for item in composition.records if isinstance(item.value, ref.ProducerRecord) and item.identity.key.local == "producer.confluence.root")
        assert_confluence_rejected(replace(producer, value=replace(producer.value, producer="capknow.semantic")))
        for local in ("producer.confluence.policy", "producer.confluence.trust_environment"):
            exact_producer = next(item for item in composition.records if isinstance(item.value, ref.ProducerRecord) and item.identity.key.local == local)
            with self.assertRaises(ValueError):
                ref.replay(_rewrite(forward.universe, {exact_producer.identity: None}))
        contract = next(item for item in composition.records if isinstance(item.value, ref.OutcomeRecord) and item.identity.key.local == "C_c")
        assert_confluence_rejected(replace(contract, value=replace(contract.value, value="foreign")))
        contract_value = contract.value.value
        self.assertIsInstance(contract_value, ref.ConfluenceContract)
        assert isinstance(contract_value, ref.ConfluenceContract)
        contract_mutations = (
            replace(contract_value, attributed_clauses=contract_value.attributed_clauses[:1]),
            replace(contract_value, attributed_clauses=(
                replace(contract_value.attributed_clauses[0], requirement="foreign"),
                contract_value.attributed_clauses[1],
            )),
            replace(contract_value, adoptions=contract_value.adoptions[:1]),
            replace(contract_value, adoptions=(
                replace(contract_value.adoptions[0], principal="foreign"),
                contract_value.adoptions[1],
            )),
            replace(contract_value, choices=("foreign",)),
            replace(contract_value, profile_requirements=("foreign",)),
            replace(contract_value, pair_requirements=("foreign",)),
        )
        for mutation in contract_mutations:
            assert_confluence_rejected(replace(
                contract, value=replace(contract.value, value=mutation)))
        confluence_authority_records = tuple(
            item for item in composition.records
            if item.identity.key.local in {
                "SRC(c,1)", "SRC(c,2)", "AUTH(c,1)", "AUTH(c,2)",
                "AFB(c,1)", "AFB(c,2)",
            }
        )
        self.assertEqual(len(confluence_authority_records), 6)
        for authority_record in confluence_authority_records:
            with self.subTest(confluence_authority_record=authority_record.identity):
                with self.assertRaises(ValueError):
                    ref.replay(_rewrite(
                        forward.universe, {authority_record.identity: None}))
        confluence_sources = tuple(
            item.value for item in confluence_authority_records
            if isinstance(item.value, ref.SourceRecord))
        self.assertEqual(
            {(item.issuer, item.source_kind, item.stable_source_identity)
             for item in confluence_sources},
            {("PLUGIN_ISSUER(APK)", "AUTHENTICATED_FIXTURE_INSTRUCTION",
              "CODING_SOURCE(c,1)"),
             ("PLUGIN_ISSUER(APK)", "AUTHENTICATED_FIXTURE_INSTRUCTION",
              "CODING_SOURCE(c,2)")})
        confluence_facts = tuple(
            item.value for item in confluence_authority_records
            if isinstance(item.value, ref.AuthorityFactRecord))
        self.assertEqual(len(confluence_facts), 2)
        for fact in confluence_facts:
            self.assertEqual(fact.principal, "fixture_principal")
            self.assertEqual(fact.admission_subject_data.normative_role,
                             "REQUIRE")
            self.assertEqual(len(fact.evidence_refs), 1)
            evidence = next(iter(fact.evidence_refs))
            self.assertEqual(
                (evidence.key.owner, evidence.key.namespace),
                ("PLUGIN_ISSUER(ATK)", "coding.authority.attestation"))
        semantic = _at(forward.universe, forward.universe.request.semantic_environment)
        semantic_mutations = (
            replace(semantic.value, abi_version=fx.V2),
            replace(semantic.value, declarations=semantic.value.declarations * 2),
            replace(semantic.value, bindings=semantic.value.bindings * 2),
            replace(semantic.value, authority_facts=()),
            replace(semantic.value, mechanically_extracted_dependencies=frozenset()),
            replace(semantic.value, chi_c=(("foreign", "foreign"),)),
        )
        for mutation in semantic_mutations:
            with self.assertRaises(ValueError):
                ref.replay(_rewrite(
                    forward.universe, {semantic.identity: replace(semantic, value=mutation)}))
        bad_inputs = replace(
            forward.universe.request,
            observation_inputs=((forward.node_one, forward.universe.request.observation_inputs[1][1]),
                                forward.universe.request.observation_inputs[1]),
        )
        with self.assertRaises(ValueError):
            ref.replay(replace(forward.universe, request=bad_inputs))
        permutation_results = [ref.replay(fx.permutation_universe(package_order, record_order)) for package_order in fx.PackageOrderTag for record_order in fx.RecordOrderTag]
        self.assertTrue(all(result.composition == permutation_results[0].composition for result in permutation_results))
        permutation_records = permutation_results[0].composition.records
        self.assertEqual(len(permutation_records), 11)
        self.assertEqual(sum(isinstance(item.value, ref.PluginPackage) for item in permutation_records), 2)
        self.assertEqual(sum(isinstance(item.value, ref.TypeDeclaration) for item in permutation_records), 4)
        self.assertEqual(sum(isinstance(item.value, ref.ContractSpec) and item.value.owner_layer is ref.Layer.DELTA for item in permutation_records), 4)
        self.assertTrue(all(len(item.value.declarations) == 2 for item in permutation_records if isinstance(item.value, ref.PluginPackage)))

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
        conflict = conflict_forward.composition.conflicts[0]
        self.assertEqual(conflict.involved_identity_set, frozenset({fx.DUPLICATE_DECLARATION.identity}))
        self.assertEqual(len(conflict.conflict_kind.unequal_positions), 2)
        self.assertEqual((len(fx.DUPLICATE_TYPE_DECLARATIONS), len(fx.DUPLICATE_TYPE_ADMISSIONS)), (24, 24))
        self.assertEqual(len(fx.DUPLICATE_PACKAGE.value.declarations), 24)
        self.assertEqual(len(fx.DUPLICATE_PACKAGE.value.model_contracts), 0)
        self.assertEqual(len(fx.DUPLICATE_DECLARATION.value.argument_types), 3)
        self.assertEqual(len(fx.DUPLICATE_BAD_DECLARATION.value.argument_types), 3)

    def test_k3x_11_all_42_literal_missing_reconstructions(self) -> None:
        self.assertEqual(len(fx.MissingRowId), 42)
        literal_identity_fields = (
            (fx.MissingRowId.ABI, ref.RecordKind.ABI, "capknow.semantic", "abi", "ABI0", fx.ABI0),
            (fx.MissingRowId.PLUGIN, ref.RecordKind.PACKAGE, "capknow.semantic", "plugin", "coding-minimal", fx.V1),
            (fx.MissingRowId.DECLARATION, ref.RecordKind.DECLARATION, "capknow.semantic", "coding.declaration", "DP(task_accepts)", fx.V1),
            (fx.MissingRowId.SYMBOL, ref.RecordKind.DECLARATION, "capknow.semantic", "coding.declaration", "DP(task_accepts)", fx.V1),
            (fx.MissingRowId.EVENT, ref.RecordKind.EVENT, "capknow.semantic", "coding.declaration", "DE(dependency_refresh)", fx.V1),
            (fx.MissingRowId.PAIR_DECLARATION, ref.RecordKind.PAIR_DECLARATION, "capknow.semantic", "pair", "PAIR(refresh)", fx.V1),
            (fx.MissingRowId.OUTCOME, ref.RecordKind.OUTCOME, "capknow.semantic", "outcome", "O_w", fx.V1),
            (fx.MissingRowId.BINDING, ref.RecordKind.BINDING, "capknow.semantic", "coding.binding", "BINDING(DP(task_accepts))", fx.V1),
            (fx.MissingRowId.PROFILE_BINDING, ref.RecordKind.PROFILE_BINDING, "capknow.semantic", "coding.binding", "PROFILE_BINDING(PK(implementation_evidence))", fx.V1),
            (fx.MissingRowId.PAIR_BINDING, ref.RecordKind.PAIR_BINDING, "capknow.semantic", "pair.binding", "PB_alt", fx.V1),
            (fx.MissingRowId.AUTHORITY_FACT, ref.RecordKind.AUTHORITY_FACT, "capknow.semantic", "authority", "AF(choice,1)", fx.V1),
            (fx.MissingRowId.CHOICE_BINDING, ref.RecordKind.CHOICE_BINDING, "capknow.semantic", "authority.choice", "cb0", fx.V1),
            (fx.MissingRowId.LEXICAL_BINDING, ref.RecordKind.LEXICAL_BINDING, "capknow.semantic", "lexical", "lk0", fx.V1),
            (fx.MissingRowId.EXTRANEOUS_LEXICAL_BINDING, ref.RecordKind.REQUEST, "capknow.semantic", "request", "Q_t[ADMITTED]", fx.V1),
            (fx.MissingRowId.SERVICE, ref.RecordKind.SERVICE, "capknow.semantic", "coding.service", "SK(predicates)", fx.V1),
            (fx.MissingRowId.CAPABILITY, ref.RecordKind.CAPABILITY, "capknow.semantic", "coding.capability", "CAP(predicates)", fx.V1),
            (fx.MissingRowId.TRUST_POLICY, ref.RecordKind.TRUST_POLICY, "capknow.semantic", "trust", "TP", fx.V1),
            (fx.MissingRowId.TRUST_ROOT, ref.RecordKind.TRUST_ROOT, "capknow.semantic", "trust", "TR", fx.V1),
            (fx.MissingRowId.CERTIFICATE, ref.RecordKind.CERTIFICATE, "capknow.audit.pair-proof", "pair.certificate", "PCERT", fx.V1),
            (fx.MissingRowId.MIGRATION, ref.RecordKind.MIGRATION, "capknow.fixture.evolution-owner", "evolution", "MK0", fx.V1),
            (fx.MissingRowId.COMPATIBILITY_CLAIM, ref.RecordKind.COMPATIBILITY_CLAIM, "capknow.fixture.evolution-owner", "evolution", "CCK0", fx.V1),
            (fx.MissingRowId.EXTENSION_OPTIONAL, ref.RecordKind.SEMANTIC_EXTENSION, "capknow.fixture.evolution-owner", "evolution", "XK0", fx.V1),
            (fx.MissingRowId.EXTENSION_REQUIRED, ref.RecordKind.SEMANTIC_EXTENSION, "capknow.fixture.evolution-owner", "evolution", "XK1", fx.V1),
            (fx.MissingRowId.MODEL_CONTRACT, ref.RecordKind.MODEL_CONTRACT, "capknow.semantic", "coding.model", "MODEL_task_accepts", fx.V1),
            (fx.MissingRowId.ALIAS_OPTIONAL, ref.RecordKind.ALIAS, "capknow.fixture.evolution-owner", "evolution.alias", "AK0", fx.V1),
            (fx.MissingRowId.ALIAS_REQUIRED, ref.RecordKind.ALIAS, "capknow.fixture.evolution-owner", "evolution.alias", "AK1", fx.V1),
            (fx.MissingRowId.SIGMA_CONTRACT_SPEC, ref.RecordKind.CONTRACT_SPEC, "capknow.semantic", "coding.contract", "CS(PREDICATE_MEANING,task_accepts)", fx.V1),
            (fx.MissingRowId.SERVICE_CONTRACT_SPEC, ref.RecordKind.CONTRACT_SPEC, "capknow.semantic", "coding.service.contract", "QSOUND", fx.V1),
            (fx.MissingRowId.REQUEST, ref.RecordKind.REQUEST, "capknow.semantic", "request", "Q_t[ADMITTED]", fx.V1),
            (fx.MissingRowId.RESULT, ref.RecordKind.RESULT, "capknow.semantic", "result", "RES_t[ADMITTED]", fx.V1),
            (fx.MissingRowId.SEMANTIC_ENVIRONMENT, ref.RecordKind.SEMANTIC_ENVIRONMENT, "capknow.semantic", "environment", "E_t", fx.V1),
            (fx.MissingRowId.TRUST_ENVIRONMENT, ref.RecordKind.TRUST_ENVIRONMENT, "capknow.semantic", "trust", "T_admitted", fx.V1),
            (fx.MissingRowId.DEPENDENCY_ENVIRONMENT, ref.RecordKind.DEPENDENCY_ENVIRONMENT, "capknow.semantic", "environment", "D_t", fx.V1),
            (fx.MissingRowId.OBSERVATION_ENVIRONMENT, ref.RecordKind.OBSERVATION_ENVIRONMENT, "capknow.semantic", "confluence.result", "M_c", fx.V1),
            (fx.MissingRowId.LIFECYCLE, ref.RecordKind.LIFECYCLE, "capknow.semantic", "confluence.lifecycle", "L_c_final", fx.V1),
            (fx.MissingRowId.EVENT_VALUE, ref.RecordKind.EVENT_VALUE, "capknow.semantic", "event.value", "ev0", fx.V1),
            (fx.MissingRowId.TRACE_EVENT, ref.RecordKind.TRACE_EVENT, "capknow.semantic", "event.trace", "te0", fx.V1),
            (fx.MissingRowId.SOURCE, ref.RecordKind.SOURCE, "capknow.semantic", "authority.source", "SRC(choice,1)", fx.V1),
            (fx.MissingRowId.AUTHORITY_REF, ref.RecordKind.AUTHORITY_REF, "capknow.semantic", "authority.ref", "AUTH(choice,1)", fx.V1),
            (fx.MissingRowId.EVIDENCE, ref.RecordKind.EVIDENCE, "capknow.semantic", "evidence", "e0", fx.V1),
            (fx.MissingRowId.REASON, ref.RecordKind.REASON, "capknow.semantic", "reason", "u0", fx.V1),
            (fx.MissingRowId.CONFLICT, ref.RecordKind.CONFLICT, "capknow.semantic", "conflict", "conflict0", fx.V1),
        )
        self.assertEqual(len(literal_identity_fields), 42)
        for row, kind, owner, namespace, local, version in literal_identity_fields:
            target = fx.missing_construction(row).target
            self.assertEqual(target, ref.RecordIdentity(kind, ref.ExactKey(owner, namespace, local, version)))
        for row in fx.MissingRowId:
            with self.subTest(row=row):
                construction = fx.missing_construction(row)
                baseline_composition = ref.compose_records(construction.baseline.records)
                variant_composition = ref.compose_records(construction.variant.records)
                self.assertEqual(baseline_composition.records, construction.baseline_manifest)
                self.assertEqual(variant_composition.records, construction.variant_manifest)
                self.assertEqual(construction.baseline_manifest - construction.variant_manifest, construction.removed_records)
                self.assertEqual(construction.variant_manifest - construction.baseline_manifest, construction.added_records)
                self.assertIsNotNone(baseline_composition.at(construction.target))
                self.assertIsNone(variant_composition.at(construction.target))
                base = ref.replay(construction.baseline)
                variant = ref.replay(construction.variant)
                self.assertEqual(base.result.tag, "PRESENT")
                independent = fx.MISSING_EXPECTED_LITERAL[row]
                self.assertEqual(
                    _judgment_literal(variant.result),
                    (independent.tag, independent.details),
                )
                empty = ref.replay(replace(construction.variant, records=()))
                self.assertEqual(empty.result.tag, "MALFORMED_CONTEXT")
                if construction.variant_container is not None:
                    package = _at(construction.variant, construction.variant_container)
                    empty_package = replace(package, value=replace(package.value, declarations=(), pair_declarations=(), bindings=(), pair_bindings=(), profile_bindings=(), model_contracts=(), aliases=(), services=(), certificates=(), authority_facts=(), compatibility_claims=(), migrations=(), semantic_extensions=()))
                    if package != empty_package:
                        emptied = ref.replay(_rewrite(construction.variant, {construction.variant_container: empty_package}))
                        self.assertNotEqual(emptied, variant)
        lexical = fx.missing_construction(fx.MissingRowId.EXTRANEOUS_LEXICAL_BINDING)
        self.assertEqual(ref.replay(lexical.variant).result.details[0], "EXTRANEOUS_LEXICAL_BINDING")
        arbitrary = ref.LookupRequest(
            fx.rid(ref.RecordKind.CAPABILITY, "unsupported", namespace="unsupported"),
            ref.ResolutionCoordinate(ref.ResolutionRelation.SERVICE_DISCOVERY, lexical.variant.request.context_roots[0]),
            lexical.variant.request.context_roots,
        )
        with self.assertRaises(ref.FiniteProfileError):
            ref.replay(replace(lexical.variant, request=arbitrary))
        trust = fx.missing_construction(fx.MissingRowId.TRUST_ROOT)
        original_consumer = trust.variant.request.coordinate.consumer
        assert original_consumer is not None
        foreign_consumer = replace(
            original_consumer,
            key=replace(original_consumer.key, owner="foreign.owner"),
        )
        foreign_coordinate = replace(
            trust.variant.request.coordinate, consumer=foreign_consumer
        )
        foreign_context = tuple(
            foreign_consumer if item == original_consumer else item
            for item in trust.variant.request.context_roots
        )
        consumer_record = _at(trust.variant, original_consumer)
        foreign_record = replace(consumer_record, identity=foreign_consumer)
        with self.assertRaises(ref.FiniteProfileError):
            ref.replay(replace(
                trust.variant,
                records=(*trust.variant.records, foreign_record),
                request=replace(
                    trust.variant.request,
                    coordinate=foreign_coordinate,
                    context_roots=foreign_context,
                ),
            ))

        evolution = fx.missing_construction(fx.MissingRowId.MIGRATION).baseline
        evolution_expected = ref.replay(evolution)
        self.assertIsInstance(evolution_expected, ref.LookupReplay)
        evolution_composition = ref.compose_records(evolution.records)

        def assert_evolution_rejected(changed: ref.LogicalRecord) -> None:
            replayed = ref.replay(_rewrite(evolution, {changed.identity: changed}))
            self.assertFalse(
                isinstance(replayed, ref.LookupReplay)
                and replayed.result.tag == "PRESENT"
            )

        evolution_root = next(item for item in evolution_composition.records if isinstance(item.value, ref.TrustRootRecord) and item.identity.key.local == "TRE")
        for mutation in (
            replace(evolution_root.value, owner="foreign"),
            replace(evolution_root.value, trusted_validators=frozenset()),
            replace(evolution_root.value, permitted_certificate_kinds=frozenset()),
            replace(evolution_root.value, permitted_targets=frozenset()),
            replace(evolution_root.value, adoption="IMPLICIT"),
        ):
            assert_evolution_rejected(replace(evolution_root, value=mutation))
        evolution_service = next(item for item in evolution_composition.records if isinstance(item.value, ref.ServiceIdentity) and item.identity.key.local == "EVSK_m")
        assert_evolution_rejected(replace(evolution_service, value=replace(evolution_service.value, abi_version=fx.V2)))
        evolution_proof = next(item for item in evolution_composition.records if isinstance(item.value, ref.EvolutionProof) and item.identity.key.local == "EVOLUTION_PROOF_m")
        assert_evolution_rejected(replace(evolution_proof, value=replace(evolution_proof.value, record_identity=fx.rid(ref.RecordKind.MIGRATION, "foreign", namespace="evolution"))))
        evolution_capability = next(item for item in evolution_composition.records if isinstance(item.value, ref.CapabilityDescriptor) and item.identity.key.local == "EVC_m")
        for mutation in (
            replace(evolution_capability.value, supported_targets=frozenset()),
            replace(evolution_capability.value, dependency_scope=frozenset()),
            replace(evolution_capability.value, required_trust_roots=frozenset()),
            replace(evolution_capability.value, complete_fragment=None),
        ):
            assert_evolution_rejected(replace(evolution_capability, value=mutation))
        evolution_fragment = next(item for item in evolution_composition.records if isinstance(item.value, ref.ContractSpec) and item.identity.key.local == "ES_m")
        assert_evolution_rejected(replace(evolution_fragment, value=replace(evolution_fragment.value, relation_name="foreign")))
        evolution_envelope = next(item for item in evolution_composition.records if isinstance(item.value, ref.CertificateEnvelope) and item.identity.key.local == "EC_m")
        assert_evolution_rejected(replace(evolution_envelope, value=replace(evolution_envelope.value, fragment=evolution_envelope.value.dependencies)))
        assert_evolution_rejected(replace(evolution_envelope, value=replace(evolution_envelope.value, abstraction_class="CONCRETE")))
        assert_evolution_rejected(replace(
            evolution_envelope,
            value=replace(
                evolution_envelope.value,
                certificate_key=fx.key(
                    "EC_wrong", owner="capknow.audit.evolution-proof",
                    namespace="evolution.certificate"))))
        evolution_evidence = next(item for item in evolution_composition.records if isinstance(item.value, ref.EvidenceRecord) and item.identity.key.local == "ER_m")
        for mutation in (
            replace(evolution_evidence.value, issuer="foreign"),
            replace(evolution_evidence.value, namespace="foreign"),
            replace(evolution_evidence.value, local="foreign"),
            replace(evolution_evidence.value, schema_contract=evolution_envelope.value.fragment),
        ):
            assert_evolution_rejected(replace(evolution_evidence, value=mutation))
        evolution_policy = next(item for item in evolution_composition.records if isinstance(item.value, ref.TrustPolicyRecord) and item.identity.key.local == "TP" and item.identity.key.namespace == "evolution.trust")
        assert_evolution_rejected(replace(evolution_policy, value=replace(evolution_policy.value, policy_owner="foreign")))
        evolution_request = next(item for item in evolution_composition.records if isinstance(item.value, ref.MigrationAdmissionRequest))
        assert_evolution_rejected(replace(evolution_request, value=ref.CompatibilityAdmissionRequest(
            evolution_request.value.abi_version, evolution_request.value.candidate,
            evolution_request.value.semantic_environment, evolution_request.value.trust_environment,
            evolution_request.value.complete_dependencies, evolution_request.value.capability_target,
            evolution_request.value.capability_key,
        )))
        evolution_admission = next(item for item in evolution_composition.records if isinstance(item.value, ref.CertificateAdmission) and item.identity.key.local == "EADMIT_m")
        assert_evolution_rejected(replace(evolution_admission, value=replace(evolution_admission.value, admitted_conclusion=ref.MigrationRelationAdmitted(evolution_admission.value.certificate.key, evolution_admission.value.certificate))))
        evolution_result = next(item for item in evolution_composition.records if isinstance(item.value, ref.EvolutionAdmissionResult) and item.identity.key.local == "ERESULT_m")
        assert_evolution_rejected(replace(evolution_result, value=replace(evolution_result.value, conclusion=ref.MigrationRelationAdmitted(fx.key("foreign", namespace="evolution"), evolution_admission.value.certificate))))
        assert_evolution_rejected(replace(evolution_result, value=ref.CompatibilityAdmissionResult(evolution_result.value.conclusion)))
        migration_envelope = next(
            item for item in evolution_composition.records
            if isinstance(item.value, ref.CertificateEnvelope)
            and item.identity.key.local == "EC_m")
        migration_validator = next(
            item for item in evolution_composition.records
            if isinstance(item.value, ref.CapabilityDescriptor)
            and item.identity.key.local == "EVC_m")
        evolution_trust = _at(
            evolution, evolution_request.value.trust_environment)
        relevant_producer_subjects = frozenset({
            migration_record.identity if 'migration_record' in locals()
            else evolution_request.value.candidate,
            migration_envelope.identity,
            migration_validator.identity,
            migration_validator.value.service,
            migration_envelope.value.payload,
            *migration_envelope.value.evidence_refs,
            evolution_request.value.trust_environment,
            evolution_trust.value.policy,
            *evolution_trust.value.roots,
        })
        evolution_producers = tuple(
            item for item in evolution_composition.records
            if isinstance(item.value, ref.ProducerRecord)
            and item.identity.key.namespace == "evolution.producer"
            and item.value.subject in relevant_producer_subjects)
        for producer_record in evolution_producers:
            with self.subTest(removed_evolution_producer=producer_record.identity):
                replayed = ref.replay(_rewrite(evolution, {producer_record.identity: None}))
                self.assertFalse(isinstance(replayed, ref.LookupReplay) and replayed.result.tag == "PRESENT")
        evolution_environment = next(
            item for item in evolution_composition.records
            if isinstance(item.value, ref.SemanticEnvironment)
            and item.identity == evolution_request.value.semantic_environment)
        self.assertFalse(isinstance(
            ref.replay(_rewrite(
                evolution, {evolution_environment.identity: None})),
            ref.LookupReplay))
        rogue_environment_id = fx.rid(
            ref.RecordKind.SEMANTIC_ENVIRONMENT, "E_rogue",
            namespace="evolution.environment")
        rogue_environment = ref.LogicalRecord(
            rogue_environment_id, evolution_environment.value)
        wrong_environment_request = replace(
            evolution_request,
            value=replace(evolution_request.value,
                          semantic_environment=rogue_environment_id,
                          capability_target=replace(
                              evolution_request.value.capability_target,
                              semantic_environment=rogue_environment_id)))
        rewritten_wrong_environment = _rewrite(
            evolution,
            {evolution_request.identity: wrong_environment_request})
        wrong_environment_universe = replace(
            rewritten_wrong_environment,
            records=(*rewritten_wrong_environment.records, rogue_environment))
        self.assertFalse(isinstance(
            ref.replay(wrong_environment_universe), ref.LookupReplay))
        for field_name, changed_value in (
            ("chi_c", (("rogue", "value"),)),
            ("mechanically_extracted_dependencies", frozenset({
                fx.rid(ref.RecordKind.MIGRATION, "MK0",
                       owner="capknow.fixture.evolution-owner",
                       namespace="evolution")})),
            ("authority_facts", (fx.rid(
                ref.RecordKind.MIGRATION, "MK0",
                owner="capknow.fixture.evolution-owner",
                namespace="evolution"),)),
        ):
            with self.subTest(evolution_environment_field=field_name):
                assert_evolution_rejected(replace(
                    evolution_environment,
                    value=replace(evolution_environment.value,
                                  **{field_name: changed_value})))
        migration_record = next(
            item for item in evolution_composition.records
            if isinstance(item.value, ref.MigrationDeclaration))
        dangling_environment = fx.rid(
            ref.RecordKind.SEMANTIC_ENVIRONMENT, "E_dangling",
            namespace="evolution.environment")
        for mutation in (
            replace(migration_record.value,
                    source_environment=dangling_environment),
            replace(migration_record.value,
                    target_environment=dangling_environment),
        ):
            assert_evolution_rejected(
                replace(migration_record, value=mutation))
        dangling_dependency = fx.rid(
            ref.RecordKind.BINDING, "dangling", namespace="evolution")
        dangling_dependency_key = ref.dependency_key(dangling_dependency)
        evolution_dependency = next(
            item for item in evolution_composition.records
            if isinstance(item.value, ref.DependencyEnvironment)
            and item.identity == evolution_request.value.complete_dependencies)
        assert_evolution_rejected(replace(
            evolution_dependency,
            value=replace(
                evolution_dependency.value,
                proper_dependencies=(
                    evolution_dependency.value.proper_dependencies
                    | frozenset({dangling_dependency_key})),
                transitive_dependency_closure=(
                    evolution_dependency.value.transitive_dependency_closure
                    | frozenset({dangling_dependency_key})))))
        for index, producer_record in enumerate(evolution_producers):
            rogue = fx.record(
                ref.RecordKind.PRODUCER, f"rogue.evolution.{index}",
                ref.ProducerRecord(
                    producer_record.value.subject, "rogue.producer",
                    producer_record.value.producer_role),
                namespace="evolution.rogue-producer")
            replayed = ref.replay(replace(
                evolution, records=(*evolution.records, rogue)))
            with self.subTest(rogue_evolution_producer=producer_record.value.subject):
                self.assertFalse(
                    isinstance(replayed, ref.LookupReplay)
                    and replayed.result.tag == "PRESENT")

    def test_k3x_12_all_102_replays_without_identifier_or_assertion_input(self) -> None:
        packet = fx.fixture_packet()
        assertions = fx.assertion_results()
        self.assertEqual(set(packet), set(assertions))
        self.assertEqual(len(packet), 102)
        self.assertEqual(sum(identifier.family is fx.FixtureFamily.MISSING_BASE for identifier in packet), 42)
        self.assertEqual(sum(identifier.family is fx.FixtureFamily.MISSING_VARIANT for identifier in packet), 42)
        for identifier, universe in packet.items():
            with self.subTest(identifier=identifier):
                replayed = ref.replay(universe)
                self.assertEqual(_replay_assertion(universe, replayed), assertions[identifier])
                self.assertFalse(_contains_fixture_id(universe))

        core_id = fx.FixtureId(fx.FixtureFamily.CORE_DEFINITIONAL)
        core = packet[core_id]
        frozen = assertions[core_id]
        extra_identity = ref.RecordIdentity(
            ref.RecordKind.PRESENTATION,
            ref.ExactKey(
                "capknow.semantic", "assertion.falsifier", "extra-record",
                ref.Version((1,)),
            ),
        )
        extra = ref.LogicalRecord(extra_identity, ref.NamedCarrier("EXTRA_RECORD"))
        changed_manifest = replace(core, records=(*core.records, extra))
        self.assertNotEqual(
            _replay_assertion(changed_manifest, ref.replay(changed_manifest)), frozen
        )

        request_identity = ref.RecordIdentity(
            ref.RecordKind.REQUEST,
            ref.ExactKey(
                "capknow.semantic", "request", "Q_t[ADMITTED]", ref.Version((1,))
            ),
        )
        request = _at(core, request_identity)
        changed_request = replace(
            request,
            value=replace(
                request.value,
                arguments=(*request.value.arguments[:-1], frozenset({object()}))),
        )
        changed_evidence = _rewrite(core, {request_identity: changed_request})
        self.assertNotEqual(
            _replay_assertion(changed_evidence, ref.replay(changed_evidence)), frozen
        )

        result_identity = ref.RecordIdentity(
            ref.RecordKind.RESULT,
            ref.ExactKey(
                "capknow.semantic", "result", "RES_t[ADMITTED]", ref.Version((1,))
            ),
        )
        result = _at(core, result_identity)
        changed_result_record = replace(
            result, value=replace(result.value, result=cp.Eval(cp.Truth.FALSE))
        )
        changed_result = _rewrite(core, {result_identity: changed_result_record})
        self.assertNotEqual(
            _replay_assertion(changed_result, ref.replay(changed_result)), frozen
        )

    def test_k3x_13_declared_access_and_static_oracle_exclusions(self) -> None:
        for requested in (frozenset({"repository"}), frozenset({"evidence"}), frozenset({"hidden_assertion"})):
            with self.subTest(requested=requested), self.assertRaises(cp.UndeclaredAccessError):
                cp.invoke_with_declared_access(requested, frozenset(), lambda: cp.Truth.TRUE, ())
        self.assertEqual(cp.invoke_with_declared_access(frozenset({"final"}), frozenset({"final"}), lambda value: value, (cp.Truth.TRUE,)), cp.Truth.TRUE)

        builder_source = inspect.getsource(fx._build_expected_assertions)
        builder_tree = ast.parse(builder_source)
        attributes = {
            item.attr for item in ast.walk(builder_tree) if isinstance(item, ast.Attribute)
        }
        calls = {
            item.func.id
            for item in ast.walk(builder_tree)
            if isinstance(item, ast.Call) and isinstance(item.func, ast.Name)
        }
        self.assertFalse(
            attributes
            & {
                "manifest", "baseline_manifest", "variant_manifest",
                "universe", "evidence", "result", "expected",
            }
        )
        self.assertFalse(
            calls
            & {
                "compose_records", "validate_packages", "validate_binding",
                "validate_model_descriptor", "validate_pair", "replay",
            }
        )
        self.assertNotIn("next(iter(", builder_source)
        self.assertEqual(len(fx._EXPECTED_REPLAY_ASSERTIONS_LITERAL), 102)


if __name__ == "__main__":
    unittest.main()
