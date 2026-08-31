"""Literal finite K3-S packet and a separate assertion-only result map."""

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any

from .coding_plugin import (
    ArtifactContent,
    ArtifactProjection,
    ArtifactRole,
    ArtifactSelector,
    ArtifactTag,
    ByteSize,
    CodingEvidenceEntry,
    CodingEvidencePayload,
    ContentIdentity,
    Coverage,
    CoverageTag,
    EvidencePayloadTag,
    EvidenceRef,
    Eval,
    Format,
    ObservationEquals,
    ObservationResult,
    ObservationResultTag,
    ObservationSpec,
    ObservationSpecTag,
    ObservationValue,
    ObservationValueTag,
    Path,
    PathSegment,
    ProjectionTag,
    RepositorySnapshot,
    SelectorTag,
    TaskSpec,
    Truth,
    VerificationRecord,
    VerificationSpec,
    VerificationStatus,
    VERIFICATION_SCHEMA,
)
from .reference import (
    AbiRecord,
    CapabilityDescriptor,
    CertificateRecord,
    ChoiceBinding,
    Closure,
    Composition,
    CompositionReplay,
    CompositionRequest,
    ContractRole,
    ContractSpec,
    CoreReplay,
    DeclarationShape,
    DependencyEnvironment,
    Evaluability,
    EvolutionRecord,
    ExactKey,
    Formation,
    FormationRequest,
    GraphEvaluationRequest,
    InvocationReplayRequest,
    InvocationRequest,
    Judgment,
    Layer,
    LexicalBinding,
    LifecycleRecord,
    LogicalRecord,
    LookupReplay,
    LookupRequest,
    ModelContract,
    NamedCarrier,
    NodeOperation,
    ObservationEnvironment,
    ObservationEvaluation,
    ObservationKind,
    ObservationNode,
    ObservationQuery,
    PairBinding,
    PairDeclaration,
    PairReplay,
    PairReplayRequest,
    PairRequestData,
    PairValidationResult,
    PluginPackage,
    ProducerRecord,
    RecordIdentity,
    RecordKind,
    ResultRecord,
    SemanticBinding,
    SemanticEnvironment,
    ServiceIdentity,
    TrustEnvironment,
    TrustPolicyRecord,
    TrustRootRecord,
    TrustState,
    TypeDeclaration,
    Universe,
    Version,
)


class FixtureFamily(Enum):
    CORE_DEFINITIONAL = "CORE_DEFINITIONAL"
    PAIR_INDEPENDENT = "PAIR_INDEPENDENT"
    TRUST_BRANCH = "TRUST_BRANCH"
    MISSING_BASE = "MISSING_BASE"
    MISSING_VARIANT = "MISSING_VARIANT"
    CONFLUENCE_ORDER = "CONFLUENCE_ORDER"
    PROPER_CYCLE_REJECTION = "PROPER_CYCLE_REJECTION"
    PERMUTATION = "PERMUTATION"
    DUPLICATE_EQUAL = "DUPLICATE_EQUAL"
    DUPLICATE_CONFLICT = "DUPLICATE_CONFLICT"


class TrustFixtureTag(Enum):
    ADMITTED = "ADMITTED"
    ABSENT = "ABSENT"
    UNDECIDED = "UNDECIDED"
    INCOMPATIBLE = "INCOMPATIBLE"
    FAILED = "FAILED"


class MissingRowId(Enum):
    ABI = "ABI"
    PLUGIN = "PLUGIN"
    DECLARATION = "DECLARATION"
    SYMBOL = "SYMBOL"
    EVENT = "EVENT"
    PAIR_DECLARATION = "PAIR_DECLARATION"
    OUTCOME = "OUTCOME"
    BINDING = "BINDING"
    PROFILE_BINDING = "PROFILE_BINDING"
    PAIR_BINDING = "PAIR_BINDING"
    AUTHORITY_FACT = "AUTHORITY_FACT"
    CHOICE_BINDING = "CHOICE_BINDING"
    LEXICAL_BINDING = "LEXICAL_BINDING"
    EXTRANEOUS_LEXICAL_BINDING = "EXTRANEOUS_LEXICAL_BINDING"
    SERVICE = "SERVICE"
    CAPABILITY = "CAPABILITY"
    TRUST_POLICY = "TRUST_POLICY"
    TRUST_ROOT = "TRUST_ROOT"
    CERTIFICATE = "CERTIFICATE"
    MIGRATION = "MIGRATION"
    COMPATIBILITY_CLAIM = "COMPATIBILITY_CLAIM"
    EXTENSION_OPTIONAL = "EXTENSION_OPTIONAL"
    EXTENSION_REQUIRED = "EXTENSION_REQUIRED"
    MODEL_CONTRACT = "MODEL_CONTRACT"
    ALIAS_OPTIONAL = "ALIAS_OPTIONAL"
    ALIAS_REQUIRED = "ALIAS_REQUIRED"
    SIGMA_CONTRACT_SPEC = "SIGMA_CONTRACT_SPEC"
    SERVICE_CONTRACT_SPEC = "SERVICE_CONTRACT_SPEC"
    REQUEST = "REQUEST"
    RESULT = "RESULT"
    SEMANTIC_ENVIRONMENT = "SEMANTIC_ENVIRONMENT"
    TRUST_ENVIRONMENT = "TRUST_ENVIRONMENT"
    DEPENDENCY_ENVIRONMENT = "DEPENDENCY_ENVIRONMENT"
    OBSERVATION_ENVIRONMENT = "OBSERVATION_ENVIRONMENT"
    LIFECYCLE = "LIFECYCLE"
    EVENT_VALUE = "EVENT_VALUE"
    TRACE_EVENT = "TRACE_EVENT"
    SOURCE = "SOURCE"
    AUTHORITY_REF = "AUTHORITY_REF"
    EVIDENCE = "EVIDENCE"
    REASON = "REASON"
    CONFLICT = "CONFLICT"


class OrderTag(Enum):
    FORWARD = "FORWARD"
    REVERSE = "REVERSE"


class PackageOrderTag(Enum):
    PI1_PI2 = "PI1_PI2"
    PI2_PI1 = "PI2_PI1"


class RecordOrderTag(Enum):
    DECLARATION_THEN_SPEC = "DECLARATION_THEN_SPEC"
    SPEC_THEN_DECLARATION = "SPEC_THEN_DECLARATION"


@dataclass(frozen=True)
class FixtureId:
    family: FixtureFamily
    parameters: tuple[Any, ...] = ()

    def __post_init__(self) -> None:
        arities = {
            FixtureFamily.CORE_DEFINITIONAL: 0,
            FixtureFamily.PAIR_INDEPENDENT: 0,
            FixtureFamily.TRUST_BRANCH: 1,
            FixtureFamily.MISSING_BASE: 1,
            FixtureFamily.MISSING_VARIANT: 1,
            FixtureFamily.CONFLUENCE_ORDER: 1,
            FixtureFamily.PROPER_CYCLE_REJECTION: 0,
            FixtureFamily.PERMUTATION: 2,
            FixtureFamily.DUPLICATE_EQUAL: 1,
            FixtureFamily.DUPLICATE_CONFLICT: 1,
        }
        if len(self.parameters) != arities[self.family]:
            raise ValueError("invalid finite FixtureId")


ABI0 = Version((0,))
V1 = Version((1,))
V2 = Version((2,))


def key(local: str, owner: str = "capknow.semantic", namespace: str = "coding", version: Version = V1) -> ExactKey:
    return ExactKey(owner, namespace, local, version)


def rid(kind: RecordKind, local: str, owner: str = "capknow.semantic", namespace: str = "coding", version: Version = V1) -> RecordIdentity:
    return RecordIdentity(kind, key(local, owner, namespace, version))


def record(kind: RecordKind, local: str, value: Any, owner: str = "capknow.semantic", namespace: str = "coding", version: Version = V1) -> LogicalRecord:
    return LogicalRecord(rid(kind, local, owner, namespace, version), value)


def _authoritative(records: tuple[LogicalRecord, ...]) -> Composition:
    flat: list[LogicalRecord] = []
    def add(item: LogicalRecord) -> None:
        flat.append(item)
        if isinstance(item.value, PluginPackage):
            for member in item.value.members():
                add(member)
    for item in records:
        add(item)
    grouped: dict[RecordIdentity, set[LogicalRecord]] = {}
    for item in flat:
        grouped.setdefault(item.identity, set()).add(item)
    accepted = frozenset(next(iter(values)) for values in grouped.values() if len(values) == 1)
    from .reference import ConflictRef
    conflicts = tuple(ConflictRef(identity, frozenset(values)) for identity, values in sorted(grouped.items()) if len(values) > 1)
    return Composition(accepted, conflicts)


def _package(local: str, owner: str, *, declarations: tuple[LogicalRecord, ...] = (), bindings: tuple[LogicalRecord, ...] = (), models: tuple[LogicalRecord, ...] = (), specs: tuple[LogicalRecord, ...] = (), services: tuple[LogicalRecord, ...] = (), certificates: tuple[LogicalRecord, ...] = (), others: tuple[LogicalRecord, ...] = ()) -> LogicalRecord:
    plugin_key = key(local, owner, "plugin")
    return LogicalRecord(RecordIdentity(RecordKind.PACKAGE, plugin_key), PluginPackage(ABI0, plugin_key, owner, declarations, bindings, models, specs, services, certificates, others))


@dataclass(frozen=True)
class CoreConstruction:
    universe: Universe
    abi: RecordIdentity
    package: RecordIdentity
    declaration: RecordIdentity
    binding: RecordIdentity
    model: RecordIdentity
    capability: RecordIdentity
    service: RecordIdentity
    sigma_spec: RecordIdentity
    sound_spec: RecordIdentity
    semantic_environment: RecordIdentity
    dependency_environment: RecordIdentity
    trust_environment: RecordIdentity
    trust_root: RecordIdentity
    request: RecordIdentity
    snapshot: RepositorySnapshot
    task: TaskSpec
    evidence: frozenset[CodingEvidenceEntry]


def core_construction(trust_tag: TrustFixtureTag = TrustFixtureTag.ADMITTED) -> CoreConstruction:
    abi = record(RecordKind.ABI, "ABI0", AbiRecord(ABI0), namespace="abi", version=ABI0)
    task_type_id = rid(RecordKind.TYPE_DECLARATION, "TaskSpec", namespace="coding.type")
    snapshot_type_id = rid(RecordKind.TYPE_DECLARATION, "RepositorySnapshot", namespace="coding.type")
    task_type = LogicalRecord(task_type_id, TypeDeclaration(task_type_id.key, frozenset({"TASK"}), frozenset()))
    snapshot_type = LogicalRecord(snapshot_type_id, TypeDeclaration(snapshot_type_id.key, frozenset({"REPOSITORY_SNAPSHOT"}), frozenset()))
    declaration_id = rid(RecordKind.DECLARATION, "DP(task_accepts)", namespace="coding.declaration")
    declaration = LogicalRecord(declaration_id, DeclarationShape(declaration_id.key, key("SP(task_accepts)", namespace="coding.symbol"), "PREDICATE", (task_type_id.key, snapshot_type_id.key, key("EvidenceStore", namespace="carrier.type")), "BOOL", (frozenset(), frozenset({"final"}), frozenset({"evidence"})), frozenset({task_type_id, snapshot_type_id})))
    sigma_spec_id = rid(RecordKind.CONTRACT_SPEC, "CS(PREDICATE_MEANING,task_accepts)", namespace="coding.contract")
    sigma_spec = LogicalRecord(sigma_spec_id, ContractSpec(sigma_spec_id.key, Layer.SIGMA, ContractRole.PREDICATE_MEANING, ("TaskSpec", "RepositorySnapshot", "EvidenceStore"), frozenset({"Eval"}), (), frozenset(), "task_accepts"))
    binding_id = rid(RecordKind.BINDING, "BINDING(DP(task_accepts))", namespace="coding.binding")
    binding = LogicalRecord(binding_id, SemanticBinding(declaration_id, sigma_spec_id, frozenset({sigma_spec_id}), frozenset({sigma_spec_id})))
    service_id = rid(RecordKind.SERVICE, "SK(predicates)", namespace="coding.service")
    service = LogicalRecord(service_id, ServiceIdentity(service_id.key, "PREDICATE_EVALUATION"))
    sound_id = rid(RecordKind.CONTRACT_SPEC, "QSOUND(predicates)", namespace="coding.service.contract")
    sound = LogicalRecord(sound_id, ContractSpec(sound_id.key, Layer.SERVICE, ContractRole.SOUND_FRAGMENT, ("PredicateInvocationRequest",), frozenset({"Eval", "InterfaceFailure"}), (), frozenset(), "predicate_sound_fragment"))
    evidence_id = rid(RecordKind.CONTRACT_SPEC, "CS(EVIDENCE_SCHEMA,verification)", namespace="coding.contract")
    unknown_id = rid(RecordKind.CONTRACT_SPEC, "CS(UNKNOWN_BEHAVIOR,predicate)", namespace="coding.contract")
    error_id = rid(RecordKind.CONTRACT_SPEC, "CS(EVALUATION_ERROR_BEHAVIOR,predicate)", namespace="coding.contract")
    evidence_spec = LogicalRecord(evidence_id, ContractSpec(evidence_id.key, Layer.SIGMA, ContractRole.EVIDENCE_SCHEMA, ("EvidenceStore",), frozenset({"EvidenceMap", "InterfaceFailure"}), (), frozenset(), "verification_evidence_map"))
    unknown_spec = LogicalRecord(unknown_id, ContractSpec(unknown_id.key, Layer.SIGMA, ContractRole.UNKNOWN_BEHAVIOR, ("UnknownReasonSet",), frozenset({"Eval"}), (), frozenset(), "predicate_unknown"))
    error_spec = LogicalRecord(error_id, ContractSpec(error_id.key, Layer.SIGMA, ContractRole.EVALUATION_ERROR_BEHAVIOR, ("FailureReasonSet",), frozenset({"Eval"}), (), frozenset(), "predicate_error"))
    policy_id = rid(RecordKind.TRUST_POLICY, "TP", namespace="trust")
    policy = LogicalRecord(policy_id, TrustPolicyRecord(policy_id.key, "embedding-policy"))
    root_id = rid(RecordKind.TRUST_ROOT, "TR", namespace="trust")
    root = LogicalRecord(root_id, TrustRootRecord(root_id.key, policy_id, frozenset({"capknow.semantic"}), frozenset({service_id})))
    capability_id = rid(RecordKind.CAPABILITY, "CAP(predicates)", namespace="coding.capability")
    capability = LogicalRecord(capability_id, CapabilityDescriptor(capability_id.key, service_id, ABI0, key("coding-minimal", namespace="plugin"), frozenset({"PREDICATE_EVALUATION"}), frozenset({declaration_id}), sound_id, None, frozenset({binding_id}), frozenset({binding_id}), frozenset(), frozenset({root_id})))
    model_id = rid(RecordKind.MODEL_CONTRACT, "MODEL(task_accepts)", namespace="coding.model")
    model = LogicalRecord(model_id, ModelContract(model_id.key, binding_id, V1, declaration.value.symbol_key, declaration.value.argument_types, declaration.value.result_kind, declaration.value.facet_positions, evidence_id, unknown_id, error_id, sigma_spec_id, frozenset({capability_id})))
    package = _package("coding-minimal", "capknow.semantic", declarations=(task_type, snapshot_type, declaration), bindings=(binding,), models=(model,), specs=(sigma_spec, sound, evidence_spec, unknown_spec, error_spec), services=(service, capability))

    path = Path((PathSegment("src"), PathSegment("module.py")))
    artifact = ArtifactContent(ArtifactTag.TEXT, ArtifactRole.SOURCE, Format.TEXT, ByteSize(7), ContentIdentity("content-final"))
    snapshot = RepositorySnapshot(((path, artifact),))
    selector = ArtifactSelector(SelectorTag.PATHS_WITH_ROLE, frozenset({path}), ArtifactRole.SOURCE)
    observation_spec = ObservationSpec(ObservationSpecTag.ARTIFACT_VIEW, selector, ArtifactProjection(ProjectionTag.CONTENT))
    observation = ObservationResult(ObservationResultTag.ARTIFACT, observation_spec, Coverage(CoverageTag.COMPLETE), ((path, ObservationValue(ObservationValueTag.PRESENT_CONTENT, (artifact,))),))
    verification_spec = VerificationSpec("v_final", observation_spec, VERIFICATION_SCHEMA)
    evidence_ref = EvidenceRef("auditor", "coding", "verification/final", VERIFICATION_SCHEMA)
    verification = VerificationRecord(verification_spec, snapshot, VerificationStatus.PASS, observation, frozenset({evidence_ref}))
    evidence = frozenset({CodingEvidenceEntry(evidence_ref, CodingEvidencePayload(EvidencePayloadTag.VERIFICATION, verification))})
    task = TaskSpec(frozenset({ObservationEquals(observation_spec, observation)}), frozenset({verification_spec}))

    environment_id = rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_t", namespace="environment")
    refs = frozenset({declaration_id, binding_id})
    environment = LogicalRecord(environment_id, SemanticEnvironment((declaration_id,), (binding_id,), mechanically_extracted_dependencies=refs))
    dependency_id = rid(RecordKind.DEPENDENCY_ENVIRONMENT, "D_t", namespace="environment")
    dependency = LogicalRecord(dependency_id, DependencyEnvironment(environment_id, abi.identity, refs))
    trust_id = rid(RecordKind.TRUST_ENVIRONMENT, f"T_{trust_tag.value.lower()}", namespace="trust")
    if trust_tag is TrustFixtureTag.ADMITTED:
        trust_value = TrustEnvironment(policy_id, (root_id,), ((root_id, TrustState.ADMITTED),))
    elif trust_tag is TrustFixtureTag.ABSENT:
        trust_value = TrustEnvironment(policy_id, (), ())
    elif trust_tag is TrustFixtureTag.UNDECIDED:
        trust_value = TrustEnvironment(policy_id, (root_id,), ((root_id, TrustState.UNDECIDED),))
    elif trust_tag is TrustFixtureTag.INCOMPATIBLE:
        trust_value = TrustEnvironment(policy_id, (root_id,), ((root_id, TrustState.INCOMPATIBLE),))
    else:
        trust_value = TrustEnvironment(policy_id, (root_id,), ((root_id, TrustState.ADMITTED),), "TRANSPORT_FAILURE")
    trust = LogicalRecord(trust_id, trust_value)
    request_id = rid(RecordKind.REQUEST, f"Q_t[{trust_tag.value}]", namespace="request")
    request = LogicalRecord(request_id, InvocationRequest(declaration_id, environment_id, dependency_id, trust_id, V1, (task, snapshot, evidence)))
    records = (abi, package, policy, root, environment, dependency, trust, request)
    universe = Universe(records, InvocationReplayRequest(request_id))
    return CoreConstruction(universe, abi.identity, package.identity, declaration_id, binding_id, model_id, capability_id, service_id, sigma_spec_id, sound_id, environment_id, dependency_id, trust_id, root_id, request_id, snapshot, task, evidence)


def _core_expected(construction: CoreConstruction, tag: TrustFixtureTag) -> CoreReplay:
    composition = _authoritative(construction.universe.records)
    if tag is TrustFixtureTag.ADMITTED:
        return CoreReplay(composition, Formation.WELL_FORMED, Closure.CLOSED, Evaluability.AVAILABLE, f"INVOCABLE_FOR({construction.request.key.local})", Eval(Truth.TRUE, frozenset(next(iter(construction.evidence)).payload.value.evidence_refs)))
    if tag is TrustFixtureTag.UNDECIDED:
        return CoreReplay(composition, Formation.WELL_FORMED, Closure.CLOSED, Evaluability.UNKNOWN, "TRUST_ROOT_UNDECIDED", None)
    if tag is TrustFixtureTag.FAILED:
        return CoreReplay(composition, Formation.WELL_FORMED, Closure.CLOSED, Evaluability.UNKNOWN, "DISCOVERY_FAILED", None)
    lifecycle = "TRUST_ROOT_ABSENT" if tag is TrustFixtureTag.ABSENT else "TRUST_ROOT_INCOMPATIBLE"
    return CoreReplay(composition, Formation.WELL_FORMED, Closure.CLOSED, Evaluability.MISSING, lifecycle, None)


@dataclass(frozen=True)
class PairConstruction:
    universe: Universe
    request: RecordIdentity
    pair_binding: RecordIdentity
    certificate: RecordIdentity
    validation_references: frozenset[RecordIdentity]
    producer_records: tuple[LogicalRecord, ...]


def pair_construction() -> PairConstruction:
    abi = record(RecordKind.ABI, "ABI0.pair", AbiRecord(ABI0), namespace="abi", version=ABI0)
    spec_left_id = rid(RecordKind.CONTRACT_SPEC, "CS(refresh_scope)", namespace="pair.contract")
    spec_right_id = rid(RecordKind.CONTRACT_SPEC, "CS(refresh_occurred)", namespace="pair.contract")
    spec_left = LogicalRecord(spec_left_id, ContractSpec(spec_left_id.key, Layer.SIGMA, ContractRole.PREDICATE_MEANING, ("EventValue",), frozenset({"Eval"}), (), frozenset(), "refresh_scope"))
    spec_right = LogicalRecord(spec_right_id, ContractSpec(spec_right_id.key, Layer.SIGMA, ContractRole.PREDICATE_MEANING, ("Trace",), frozenset({"Eval"}), (), frozenset(), "refresh_occurred"))
    left_id = rid(RecordKind.BINDING, "B(refresh_scope)", namespace="pair.binding")
    right_id = rid(RecordKind.BINDING, "B(refresh_occurred)", namespace="pair.binding")
    left_decl_id = rid(RecordKind.DECLARATION, "DP(refresh_scope)", namespace="pair.declaration")
    right_decl_id = rid(RecordKind.DECLARATION, "DP(refresh_occurred)", namespace="pair.declaration")
    left_decl = LogicalRecord(left_decl_id, DeclarationShape(left_decl_id.key, key("SP(refresh_scope)", namespace="pair.symbol"), "PREDICATE", (), "BOOL", (), frozenset()))
    right_decl = LogicalRecord(right_decl_id, DeclarationShape(right_decl_id.key, key("SP(refresh_occurred)", namespace="pair.symbol"), "PREDICATE", (), "BOOL", (), frozenset()))
    left = LogicalRecord(left_id, SemanticBinding(left_decl_id, spec_left_id, frozenset({spec_left_id}), frozenset({spec_left_id})))
    right = LogicalRecord(right_id, SemanticBinding(right_decl_id, spec_right_id, frozenset({spec_right_id, left_id}), frozenset({spec_right_id, left_id})))
    pair_id = rid(RecordKind.PAIR_DECLARATION, "PAIR(refresh)", namespace="pair")
    pair = LogicalRecord(pair_id, PairDeclaration(pair_id.key, left_id, right_id))
    certificate_id = rid(RecordKind.CERTIFICATE, "PCERT", owner="capknow.audit.pair-proof", namespace="pair.certificate")
    certificate = LogicalRecord(certificate_id, CertificateRecord(certificate_id.key, pair_id, "PAIR_COHERENCE_ADMITTED", "capknow.audit.pair-proof"))
    validation_one = record(RecordKind.CERTIFICATE, "PAIR_PROOF_REF", CertificateRecord(key("PAIR_PROOF_REF", "capknow.audit.pair-validator", "pair.validation"), pair_id, "PAIR_FULL_EVAL", "capknow.audit.pair-validator"), owner="capknow.audit.pair-validator", namespace="pair.validation")
    validation_two = record(RecordKind.CERTIFICATE, "ROOT_p", CertificateRecord(key("ROOT_p", "capknow.audit.pair-root", "pair.validation"), pair_id, "PAIR_ROOT_ADMITTED", "capknow.audit.pair-root"), owner="capknow.audit.pair-root", namespace="pair.validation")
    pair_binding_id = rid(RecordKind.PAIR_BINDING, "PB_alt", namespace="pair.binding")
    validation_refs = frozenset({validation_one.identity, validation_two.identity})
    pair_binding = LogicalRecord(pair_binding_id, PairBinding(pair_id, certificate_id, frozenset({left_id, right_id}), validation_refs, validation_refs))
    policy_id = rid(RecordKind.TRUST_POLICY, "TP.pair", namespace="pair.trust")
    policy = LogicalRecord(policy_id, TrustPolicyRecord(policy_id.key, "embedding-policy"))
    root_id = rid(RecordKind.TRUST_ROOT, "TRP", namespace="pair.trust")
    root = LogicalRecord(root_id, TrustRootRecord(root_id.key, policy_id, frozenset({"capknow.semantic"}), frozenset({pair_id})))
    trust_id = rid(RecordKind.TRUST_ENVIRONMENT, "T_p", namespace="pair.trust")
    trust = LogicalRecord(trust_id, TrustEnvironment(policy_id, (root_id,), ((root_id, TrustState.ADMITTED),)))
    request_id = rid(RecordKind.REQUEST, "R_p", namespace="pair.request")
    request = LogicalRecord(request_id, PairRequestData(pair_binding_id, trust_id))
    producers = (
        record(RecordKind.PRODUCER, "producer.pair", ProducerRecord(pair_id, "capknow.semantic", "PAIR_OWNER"), namespace="pair.producer"),
        record(RecordKind.PRODUCER, "producer.certificate", ProducerRecord(certificate_id, "capknow.audit.pair-proof", "CERTIFICATE_OWNER"), namespace="pair.producer"),
        record(RecordKind.PRODUCER, "producer.validation.1", ProducerRecord(validation_one.identity, "capknow.audit.pair-validator", "VALIDATION_OWNER"), namespace="pair.producer"),
        record(RecordKind.PRODUCER, "producer.validation.2", ProducerRecord(validation_two.identity, "capknow.audit.pair-root", "VALIDATION_ROOT_OWNER"), namespace="pair.producer"),
        record(RecordKind.PRODUCER, "producer.trust", ProducerRecord(trust_id, "embedding-policy", "TRUST_OWNER"), namespace="pair.producer"),
        record(RecordKind.PRODUCER, "producer.trust.policy", ProducerRecord(policy_id, "embedding-policy", "TRUST_POLICY_OWNER"), namespace="pair.producer"),
        record(RecordKind.PRODUCER, "producer.trust.root", ProducerRecord(root_id, "embedding-policy", "TRUST_ROOT_OWNER"), namespace="pair.producer"),
    )
    package = _package("pair-coding", "capknow.semantic", declarations=(left_decl, right_decl, pair), bindings=(left, right, pair_binding), specs=(spec_left, spec_right))
    records = (abi, package, certificate, validation_one, validation_two, policy, root, trust, request, *producers)
    return PairConstruction(Universe(records, PairReplayRequest(request_id)), request_id, pair_binding_id, certificate_id, validation_refs, producers)


def _pair_expected(construction: PairConstruction) -> PairReplay:
    composition = _authoritative(construction.universe.records)
    certificate = composition.at(construction.certificate)
    binding = composition.at(construction.pair_binding)
    assert certificate is not None and isinstance(certificate.value, CertificateRecord)
    assert binding is not None and isinstance(binding.value, PairBinding)
    declaration = composition.at(binding.value.declaration)
    assert declaration is not None and isinstance(declaration.value, PairDeclaration)
    return PairReplay(composition, Formation.WELL_FORMED, Closure.CLOSED, PairValidationResult(declaration.value.pair_key, certificate.value.certificate_key, "PAIR_COHERENCE_ADMITTED"))


_ROW_KIND = {
    MissingRowId.ABI: RecordKind.ABI,
    MissingRowId.PLUGIN: RecordKind.PACKAGE,
    MissingRowId.DECLARATION: RecordKind.DECLARATION,
    MissingRowId.SYMBOL: RecordKind.DECLARATION,
    MissingRowId.EVENT: RecordKind.EVENT,
    MissingRowId.PAIR_DECLARATION: RecordKind.PAIR_DECLARATION,
    MissingRowId.OUTCOME: RecordKind.OUTCOME,
    MissingRowId.BINDING: RecordKind.BINDING,
    MissingRowId.PROFILE_BINDING: RecordKind.PROFILE_BINDING,
    MissingRowId.PAIR_BINDING: RecordKind.PAIR_BINDING,
    MissingRowId.AUTHORITY_FACT: RecordKind.AUTHORITY_FACT,
    MissingRowId.CHOICE_BINDING: RecordKind.CHOICE_BINDING,
    MissingRowId.LEXICAL_BINDING: RecordKind.LEXICAL_BINDING,
    MissingRowId.EXTRANEOUS_LEXICAL_BINDING: RecordKind.REQUEST,
    MissingRowId.SERVICE: RecordKind.SERVICE,
    MissingRowId.CAPABILITY: RecordKind.CAPABILITY,
    MissingRowId.TRUST_POLICY: RecordKind.TRUST_POLICY,
    MissingRowId.TRUST_ROOT: RecordKind.TRUST_ROOT,
    MissingRowId.CERTIFICATE: RecordKind.CERTIFICATE,
    MissingRowId.MIGRATION: RecordKind.MIGRATION,
    MissingRowId.COMPATIBILITY_CLAIM: RecordKind.COMPATIBILITY_CLAIM,
    MissingRowId.EXTENSION_OPTIONAL: RecordKind.SEMANTIC_EXTENSION,
    MissingRowId.EXTENSION_REQUIRED: RecordKind.SEMANTIC_EXTENSION,
    MissingRowId.MODEL_CONTRACT: RecordKind.MODEL_CONTRACT,
    MissingRowId.ALIAS_OPTIONAL: RecordKind.ALIAS,
    MissingRowId.ALIAS_REQUIRED: RecordKind.ALIAS,
    MissingRowId.SIGMA_CONTRACT_SPEC: RecordKind.CONTRACT_SPEC,
    MissingRowId.SERVICE_CONTRACT_SPEC: RecordKind.CONTRACT_SPEC,
    MissingRowId.REQUEST: RecordKind.REQUEST,
    MissingRowId.RESULT: RecordKind.RESULT,
    MissingRowId.SEMANTIC_ENVIRONMENT: RecordKind.SEMANTIC_ENVIRONMENT,
    MissingRowId.TRUST_ENVIRONMENT: RecordKind.TRUST_ENVIRONMENT,
    MissingRowId.DEPENDENCY_ENVIRONMENT: RecordKind.DEPENDENCY_ENVIRONMENT,
    MissingRowId.OBSERVATION_ENVIRONMENT: RecordKind.OBSERVATION_ENVIRONMENT,
    MissingRowId.LIFECYCLE: RecordKind.LIFECYCLE,
    MissingRowId.EVENT_VALUE: RecordKind.EVENT_VALUE,
    MissingRowId.TRACE_EVENT: RecordKind.TRACE_EVENT,
    MissingRowId.SOURCE: RecordKind.SOURCE,
    MissingRowId.AUTHORITY_REF: RecordKind.AUTHORITY_REF,
    MissingRowId.EVIDENCE: RecordKind.EVIDENCE,
    MissingRowId.REASON: RecordKind.REASON,
    MissingRowId.CONFLICT: RecordKind.CONFLICT,
}


_ROW_LOCAL = {
    MissingRowId.ABI: "ABI0",
    MissingRowId.PLUGIN: "PKG_CK",
    MissingRowId.DECLARATION: "DP(task_accepts)",
    MissingRowId.SYMBOL: "DP(task_accepts)",
    MissingRowId.EVENT: "DE(dependency_refresh)",
    MissingRowId.PAIR_DECLARATION: "PAIR(refresh)",
    MissingRowId.OUTCOME: "O_w",
    MissingRowId.BINDING: "BINDING(DP(task_accepts))",
    MissingRowId.PROFILE_BINDING: "PROFILE_BINDING(PK(implementation_evidence))",
    MissingRowId.PAIR_BINDING: "PAIR_BINDING(PAIR(refresh))",
    MissingRowId.AUTHORITY_FACT: "AF(choice,1)",
    MissingRowId.CHOICE_BINDING: "cb0",
    MissingRowId.LEXICAL_BINDING: "lk0",
    MissingRowId.EXTRANEOUS_LEXICAL_BINDING: "Q_t[T_admitted]",
    MissingRowId.SERVICE: "SK(predicates)",
    MissingRowId.CAPABILITY: "CAP(predicates)",
    MissingRowId.TRUST_POLICY: "TP",
    MissingRowId.TRUST_ROOT: "TR",
    MissingRowId.CERTIFICATE: "BCERT",
    MissingRowId.MIGRATION: "MK0",
    MissingRowId.COMPATIBILITY_CLAIM: "CCK0",
    MissingRowId.EXTENSION_OPTIONAL: "XK0",
    MissingRowId.EXTENSION_REQUIRED: "XK1",
    MissingRowId.MODEL_CONTRACT: "MODEL_task_accepts",
    MissingRowId.ALIAS_OPTIONAL: "AK0",
    MissingRowId.ALIAS_REQUIRED: "AK1",
    MissingRowId.SIGMA_CONTRACT_SPEC: "CS(PREDICATE_MEANING,task_accepts)",
    MissingRowId.SERVICE_CONTRACT_SPEC: "QSOUND",
    MissingRowId.REQUEST: "Q_t[T_admitted]",
    MissingRowId.RESULT: "RES_t",
    MissingRowId.SEMANTIC_ENVIRONMENT: "E_t",
    MissingRowId.TRUST_ENVIRONMENT: "T_admitted",
    MissingRowId.DEPENDENCY_ENVIRONMENT: "D_t",
    MissingRowId.OBSERVATION_ENVIRONMENT: "M_c",
    MissingRowId.LIFECYCLE: "L_c_final",
    MissingRowId.EVENT_VALUE: "ev0",
    MissingRowId.TRACE_EVENT: "te0",
    MissingRowId.SOURCE: "src0",
    MissingRowId.AUTHORITY_REF: "auth0",
    MissingRowId.EVIDENCE: "e0",
    MissingRowId.REASON: "u0",
    MissingRowId.CONFLICT: "conflict0",
}


_PACKAGED_ROWS = frozenset({
    MissingRowId.DECLARATION, MissingRowId.SYMBOL, MissingRowId.EVENT,
    MissingRowId.PAIR_DECLARATION, MissingRowId.BINDING,
    MissingRowId.PROFILE_BINDING, MissingRowId.PAIR_BINDING,
    MissingRowId.AUTHORITY_FACT, MissingRowId.SERVICE, MissingRowId.CAPABILITY,
    MissingRowId.CERTIFICATE, MissingRowId.MIGRATION,
    MissingRowId.COMPATIBILITY_CLAIM, MissingRowId.EXTENSION_OPTIONAL,
    MissingRowId.EXTENSION_REQUIRED, MissingRowId.MODEL_CONTRACT,
    MissingRowId.ALIAS_OPTIONAL, MissingRowId.ALIAS_REQUIRED,
    MissingRowId.SIGMA_CONTRACT_SPEC, MissingRowId.SERVICE_CONTRACT_SPEC,
})


def _row_identity(row: MissingRowId) -> RecordIdentity:
    kind = _ROW_KIND[row]
    namespace = f"missing.{row.value.lower()}"
    return rid(kind, _ROW_LOCAL[row], namespace=namespace, version=ABI0 if row is MissingRowId.ABI else V1)


def _row_value(row: MissingRowId, identity: RecordIdentity) -> Any:
    dummy_decl = rid(RecordKind.DECLARATION, f"decl.{row.value}", namespace=f"missing.{row.value.lower()}")
    dummy_spec = rid(RecordKind.CONTRACT_SPEC, f"spec.{row.value}", namespace=f"missing.{row.value.lower()}")
    if row is MissingRowId.ABI:
        return AbiRecord(ABI0)
    if row is MissingRowId.PLUGIN:
        return PluginPackage(ABI0, identity.key, identity.key.owner)
    if row in {MissingRowId.DECLARATION, MissingRowId.SYMBOL, MissingRowId.EVENT}:
        kind = "EVENT" if row is MissingRowId.EVENT else "PREDICATE"
        return DeclarationShape(identity.key, key(f"symbol.{row.value}", namespace=identity.key.namespace), kind, (), "BOOL", (), frozenset())
    if row is MissingRowId.PAIR_DECLARATION:
        return PairDeclaration(identity.key, dummy_decl, rid(RecordKind.DECLARATION, f"decl.right.{row.value}", namespace=identity.key.namespace))
    if row in {MissingRowId.BINDING, MissingRowId.PROFILE_BINDING}:
        return SemanticBinding(dummy_decl, dummy_spec, frozenset({dummy_spec}), frozenset({dummy_spec}))
    if row is MissingRowId.PAIR_BINDING:
        left = rid(RecordKind.BINDING, "B(refresh_scope)", namespace=identity.key.namespace)
        right = rid(RecordKind.BINDING, "B(refresh_occurred)", namespace=identity.key.namespace)
        validations = frozenset({rid(RecordKind.CERTIFICATE, "PAIR_PROOF_REF", namespace=identity.key.namespace), rid(RecordKind.CERTIFICATE, "ROOT_p", namespace=identity.key.namespace)})
        return PairBinding(rid(RecordKind.PAIR_DECLARATION, "PAIR(refresh)", namespace=identity.key.namespace), rid(RecordKind.CERTIFICATE, "PCERT", namespace=identity.key.namespace), frozenset({left, right}), validations, validations)
    if row is MissingRowId.CHOICE_BINDING:
        return ChoiceBinding(identity.key, rid(RecordKind.AUTHORITY_FACT, "AF(choice,1)", namespace=identity.key.namespace), "storage")
    if row is MissingRowId.LEXICAL_BINDING:
        return LexicalBinding(identity.key, dummy_decl, "scope_lex")
    if row is MissingRowId.SERVICE:
        return ServiceIdentity(identity.key, "PREDICATE_EVALUATION")
    if row is MissingRowId.CAPABILITY:
        return CapabilityDescriptor(identity.key, rid(RecordKind.SERVICE, "SK(predicates)", namespace=identity.key.namespace), ABI0, key(f"PKG.{row.value}", namespace="plugin"), frozenset({"PREDICATE_EVALUATION"}), frozenset({dummy_decl}), rid(RecordKind.CONTRACT_SPEC, "QSOUND", namespace=identity.key.namespace), None, frozenset(), frozenset(), frozenset(), frozenset())
    if row is MissingRowId.TRUST_POLICY:
        return TrustPolicyRecord(identity.key, "embedding-policy")
    if row is MissingRowId.TRUST_ROOT:
        return TrustRootRecord(identity.key, rid(RecordKind.TRUST_POLICY, "TP", namespace=identity.key.namespace), frozenset({"capknow.semantic"}), frozenset())
    if row is MissingRowId.CERTIFICATE:
        return CertificateRecord(identity.key, dummy_decl, "CONSISTENCY_UNSAT", identity.key.owner)
    if row in {MissingRowId.MIGRATION, MissingRowId.COMPATIBILITY_CLAIM, MissingRowId.EXTENSION_OPTIONAL, MissingRowId.EXTENSION_REQUIRED, MissingRowId.ALIAS_OPTIONAL, MissingRowId.ALIAS_REQUIRED}:
        return EvolutionRecord(identity.key, dummy_decl, row in {MissingRowId.EXTENSION_REQUIRED, MissingRowId.ALIAS_REQUIRED})
    if row is MissingRowId.MODEL_CONTRACT:
        binding = rid(RecordKind.BINDING, f"binding.{row.value}", namespace=identity.key.namespace)
        evidence = rid(RecordKind.CONTRACT_SPEC, f"evidence.{row.value}", namespace=identity.key.namespace)
        unknown = rid(RecordKind.CONTRACT_SPEC, f"unknown.{row.value}", namespace=identity.key.namespace)
        error = rid(RecordKind.CONTRACT_SPEC, f"error.{row.value}", namespace=identity.key.namespace)
        return ModelContract(identity.key, binding, V1, key(f"symbol.decl.binding.{row.value}", namespace=identity.key.namespace), (), "BOOL", (), evidence, unknown, error, dummy_spec, frozenset())
    if row in {MissingRowId.SIGMA_CONTRACT_SPEC, MissingRowId.SERVICE_CONTRACT_SPEC}:
        layer = Layer.SERVICE if row is MissingRowId.SERVICE_CONTRACT_SPEC else Layer.SIGMA
        role = ContractRole.SOUND_FRAGMENT if layer is Layer.SERVICE else ContractRole.PREDICATE_MEANING
        return ContractSpec(identity.key, layer, role, ("InvocationRequest",), frozenset({"Eval"}), (), frozenset(), "row-local-relation")
    if row in {MissingRowId.EXTRANEOUS_LEXICAL_BINDING, MissingRowId.REQUEST}:
        return InvocationRequest(dummy_decl, rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_t", namespace=identity.key.namespace), rid(RecordKind.DEPENDENCY_ENVIRONMENT, "D_t", namespace=identity.key.namespace), rid(RecordKind.TRUST_ENVIRONMENT, "T_admitted", namespace=identity.key.namespace), V1, (TaskSpec(), RepositorySnapshot(()), frozenset()))
    if row is MissingRowId.RESULT:
        return ResultRecord(rid(RecordKind.REQUEST, "Q_t[T_admitted]", namespace=identity.key.namespace), "Eval", Eval(Truth.TRUE))
    if row is MissingRowId.SEMANTIC_ENVIRONMENT:
        return SemanticEnvironment((), (), mechanically_extracted_dependencies=frozenset())
    if row is MissingRowId.TRUST_ENVIRONMENT:
        return TrustEnvironment(rid(RecordKind.TRUST_POLICY, "TP", namespace=identity.key.namespace), (), ())
    if row is MissingRowId.DEPENDENCY_ENVIRONMENT:
        return DependencyEnvironment(rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_t", namespace=identity.key.namespace), rid(RecordKind.ABI, "ABI0", namespace="abi", version=ABI0), frozenset())
    if row is MissingRowId.OBSERVATION_ENVIRONMENT:
        return ObservationEnvironment(())
    if row is MissingRowId.LIFECYCLE:
        return LifecycleRecord(rid(RecordKind.REQUEST, "R_c", namespace=identity.key.namespace), "COMPLETED")
    return NamedCarrier(_ROW_LOCAL[row])


def _package_category(target: LogicalRecord) -> dict[str, tuple[LogicalRecord, ...]]:
    kind = target.identity.kind
    if kind in {RecordKind.DECLARATION, RecordKind.SYMBOL, RecordKind.EVENT, RecordKind.PAIR_DECLARATION}:
        return {"declarations": (target,)}
    if kind in {RecordKind.BINDING, RecordKind.PROFILE_BINDING, RecordKind.PAIR_BINDING, RecordKind.AUTHORITY_FACT}:
        return {"bindings" if kind is not RecordKind.AUTHORITY_FACT else "others": (target,)}
    if kind is RecordKind.MODEL_CONTRACT:
        return {"models": (target,)}
    if kind is RecordKind.CONTRACT_SPEC:
        return {"specs": (target,)}
    if kind in {RecordKind.SERVICE, RecordKind.CAPABILITY}:
        return {"services": (target,)}
    if kind is RecordKind.CERTIFICATE:
        return {"certificates": (target,)}
    return {"others": (target,)}


def _value_references(value: Any) -> frozenset[RecordIdentity]:
    if isinstance(value, TypeDeclaration):
        return value.nested_type_dependencies
    if isinstance(value, DeclarationShape):
        return value.proper_type_dependencies
    if isinstance(value, ContractSpec):
        return value.support
    if isinstance(value, SemanticBinding):
        return frozenset({value.declaration, value.meaning_contract}) | value.dependency_closure
    if isinstance(value, PairDeclaration):
        return frozenset({value.left, value.right})
    if isinstance(value, PairBinding):
        return frozenset({value.declaration, value.certificate}) | value.proper_subjects | value.validation_references
    if isinstance(value, ChoiceBinding):
        return frozenset({value.authority_fact})
    if isinstance(value, LexicalBinding):
        return frozenset({value.declaration})
    if isinstance(value, CapabilityDescriptor):
        return frozenset({value.service, value.sound_fragment}) | value.supported_targets | value.dependency_closure | value.validation_references | value.required_trust_roots | (frozenset() if value.complete_fragment is None else frozenset({value.complete_fragment}))
    if isinstance(value, TrustRootRecord):
        return frozenset({value.policy}) | value.permitted_targets
    if isinstance(value, CertificateRecord):
        return frozenset({value.subject})
    if isinstance(value, ProducerRecord):
        return frozenset({value.subject})
    if isinstance(value, EvolutionRecord):
        return frozenset({value.subject})
    if isinstance(value, ModelContract):
        return frozenset({value.target_binding, value.evidence_contract, value.unknown_contract, value.error_contract, value.semantic_contract}) | value.capability_summaries
    if isinstance(value, InvocationRequest):
        return frozenset({value.target, value.semantic_environment, value.dependency_environment, value.trust_environment})
    if isinstance(value, ResultRecord):
        return frozenset({value.request})
    if isinstance(value, PairRequestData):
        return frozenset({value.pair_binding, value.trust_environment})
    if isinstance(value, SemanticEnvironment):
        return value.all_references()
    if isinstance(value, TrustEnvironment):
        return frozenset({value.policy, *value.roots})
    if isinstance(value, DependencyEnvironment):
        return frozenset({value.semantic_environment, value.abi}) | value.members
    if isinstance(value, LifecycleRecord):
        return frozenset({value.request})
    if isinstance(value, ObservationEnvironment):
        return frozenset(identity for identity, _ in value.values)
    if isinstance(value, ObservationNode):
        return frozenset({value.contract_spec})
    if isinstance(value, NamedCarrier):
        return value.references
    return frozenset()


def _support_value(identity: RecordIdentity) -> Any:
    namespace = identity.key.namespace
    if identity.kind is RecordKind.ABI:
        return AbiRecord(identity.key.version)
    if identity.kind in {RecordKind.DECLARATION, RecordKind.SYMBOL, RecordKind.EVENT}:
        declaration_kind = "EVENT" if identity.kind is RecordKind.EVENT else "PREDICATE"
        return DeclarationShape(identity.key, key(f"symbol.{identity.key.local}", identity.key.owner, namespace, identity.key.version), declaration_kind, (), "BOOL", (), frozenset())
    if identity.kind is RecordKind.CONTRACT_SPEC:
        role = ContractRole.PREDICATE_MEANING
        if identity.key.local.startswith("evidence."):
            role = ContractRole.EVIDENCE_SCHEMA
        elif identity.key.local.startswith("unknown."):
            role = ContractRole.UNKNOWN_BEHAVIOR
        elif identity.key.local.startswith("error."):
            role = ContractRole.EVALUATION_ERROR_BEHAVIOR
        return ContractSpec(identity.key, Layer.SIGMA, role, ("value",), frozenset({"Eval"}), (), frozenset(), f"meaning.{identity.key.local}")
    if identity.kind in {RecordKind.BINDING, RecordKind.PROFILE_BINDING}:
        declaration = rid(RecordKind.DECLARATION, f"decl.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        spec = rid(RecordKind.CONTRACT_SPEC, f"spec.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        return SemanticBinding(declaration, spec, frozenset({spec}), frozenset({spec}))
    if identity.kind is RecordKind.PAIR_DECLARATION:
        left = rid(RecordKind.BINDING, f"left.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        right = rid(RecordKind.BINDING, f"right.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        return PairDeclaration(identity.key, left, right)
    if identity.kind is RecordKind.CERTIFICATE:
        subject = rid(RecordKind.DECLARATION, f"subject.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        return CertificateRecord(identity.key, subject, "VALIDATION_ADMITTED", identity.key.owner)
    if identity.kind is RecordKind.AUTHORITY_FACT:
        return NamedCarrier(identity.key.local)
    if identity.kind is RecordKind.SERVICE:
        return ServiceIdentity(identity.key, "PREDICATE_EVALUATION")
    if identity.kind is RecordKind.TRUST_POLICY:
        return TrustPolicyRecord(identity.key, "embedding-policy")
    if identity.kind is RecordKind.TRUST_ROOT:
        policy = rid(RecordKind.TRUST_POLICY, f"policy.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        return TrustRootRecord(identity.key, policy, frozenset({identity.key.owner}), frozenset())
    if identity.kind is RecordKind.SEMANTIC_ENVIRONMENT:
        return SemanticEnvironment((), ())
    if identity.kind is RecordKind.DEPENDENCY_ENVIRONMENT:
        semantic = rid(RecordKind.SEMANTIC_ENVIRONMENT, f"semantic.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        abi = rid(RecordKind.ABI, f"abi.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        return DependencyEnvironment(semantic, abi, frozenset())
    if identity.kind is RecordKind.TRUST_ENVIRONMENT:
        policy = rid(RecordKind.TRUST_POLICY, f"policy.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        return TrustEnvironment(policy, (), ())
    if identity.kind is RecordKind.REQUEST:
        declaration = rid(RecordKind.DECLARATION, f"target.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        semantic = rid(RecordKind.SEMANTIC_ENVIRONMENT, f"semantic.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        dependency = rid(RecordKind.DEPENDENCY_ENVIRONMENT, f"dependency.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        trust = rid(RecordKind.TRUST_ENVIRONMENT, f"trust.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        return InvocationRequest(declaration, semantic, dependency, trust, identity.key.version, (TaskSpec(), RepositorySnapshot(()), frozenset()))
    if identity.kind is RecordKind.CAPABILITY:
        service = rid(RecordKind.SERVICE, f"service.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        sound = rid(RecordKind.CONTRACT_SPEC, f"sound.{identity.key.local}", identity.key.owner, namespace, identity.key.version)
        return CapabilityDescriptor(identity.key, service, ABI0, key(f"package.{identity.key.local}", identity.key.owner, "plugin"), frozenset({"PREDICATE_EVALUATION"}), frozenset(), sound, None, frozenset(), frozenset(), frozenset(), frozenset())
    return NamedCarrier(identity.key.local)


def _support_records(target: LogicalRecord) -> tuple[LogicalRecord, ...]:
    records: dict[RecordIdentity, LogicalRecord] = {}
    pending = list(_value_references(target.value))
    while pending:
        identity = pending.pop()
        if identity == target.identity or identity in records:
            continue
        value = _support_value(identity)
        item = LogicalRecord(identity, value)
        records[identity] = item
        pending.extend(_value_references(value))
    return tuple(records[identity] for identity in sorted(records))


def _complete_top_level(records: list[LogicalRecord], excluded: RecordIdentity | None) -> list[LogicalRecord]:
    def flattened(items: list[LogicalRecord] | tuple[LogicalRecord, ...]) -> tuple[LogicalRecord, ...]:
        result: list[LogicalRecord] = []
        for item in items:
            result.append(item)
            if isinstance(item.value, PluginPackage):
                result.extend(flattened(item.value.members()))
        return tuple(result)
    initial = flattened(records)
    present = {item.identity for item in initial}
    pending = [reference for item in initial for reference in _value_references(item.value)]
    while pending:
        identity = pending.pop()
        if identity == excluded or identity in present:
            continue
        item = LogicalRecord(identity, _support_value(identity))
        records.append(item)
        present.add(identity)
        pending.extend(_value_references(item.value))
    return records


def _package_members(records: tuple[LogicalRecord, ...]) -> dict[str, tuple[LogicalRecord, ...]]:
    result: dict[str, tuple[LogicalRecord, ...]] = {}
    for item in records:
        category = _package_category(item)
        for name, members in category.items():
            result[name] = result.get(name, ()) + members
    return result


@dataclass(frozen=True)
class MissingConstruction:
    row: MissingRowId
    target: RecordIdentity
    baseline: Universe
    variant: Universe
    baseline_container: RecordIdentity | None
    variant_container: RecordIdentity | None
    referring_record: RecordIdentity | None


def missing_construction(row: MissingRowId) -> MissingConstruction:
    target_id = _row_identity(row)
    target = LogicalRecord(target_id, _row_value(row, target_id))
    support = _support_records(target)
    abi = record(RecordKind.ABI, f"ABI0.{row.value}", AbiRecord(ABI0), namespace="abi", version=ABI0)
    baseline_records: list[LogicalRecord] = [abi]
    variant_records: list[LogicalRecord] = [abi]
    anchor = record(RecordKind.OUTCOME, f"ROW_CONTEXT({row.value})", NamedCarrier(f"ROW({row.value})"), namespace=f"missing.{row.value.lower()}.context")
    context_roots: tuple[RecordIdentity, ...] = (abi.identity, anchor.identity)
    baseline_container = None
    variant_container = None
    if row is MissingRowId.ABI:
        context_package = _package(f"PKG.CONTEXT.{row.value}", "capknow.semantic", others=(anchor,))
        baseline_records = [target, context_package]
        variant_records = [context_package]
        context_roots = (context_package.identity, anchor.identity)
    elif row is MissingRowId.PLUGIN:
        baseline_records.extend((target, anchor))
        variant_records.append(anchor)
    elif row in _PACKAGED_ROWS:
        kwargs = _package_members((target, *support))
        kwargs["others"] = kwargs.get("others", ()) + (anchor,)
        base_package = _package(f"PKG.{row.value}", "capknow.semantic", **kwargs)
        variant_kwargs = _package_members(support)
        variant_kwargs["others"] = variant_kwargs.get("others", ()) + (anchor,)
        variant_package = _package(f"PKG.{row.value}", "capknow.semantic", **variant_kwargs)
        baseline_records.append(base_package)
        variant_records.append(variant_package)
        baseline_container = base_package.identity
        variant_container = variant_package.identity
    else:
        baseline_records.extend((target, *support, anchor))
        variant_records.extend((*support, anchor))

    referring: LogicalRecord | None = None
    if row is MissingRowId.AUTHORITY_FACT:
        choice_id = rid(RecordKind.CHOICE_BINDING, "cb0", namespace=target_id.key.namespace)
        choice = LogicalRecord(choice_id, ChoiceBinding(choice_id.key, target_id, "storage"))
        env_id = rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_choice", namespace=target_id.key.namespace)
        env_base = LogicalRecord(env_id, SemanticEnvironment((), (), authority_facts=(target_id,), choice_bindings=(choice_id,), mechanically_extracted_dependencies=frozenset({target_id, choice_id})))
        env_variant = LogicalRecord(env_id, SemanticEnvironment((), (), choice_bindings=(choice_id,), mechanically_extracted_dependencies=frozenset({choice_id})))
        baseline_records.extend((choice, env_base))
        variant_records.extend((choice, env_variant))
        referring = choice
    elif row is MissingRowId.CHOICE_BINDING:
        env_id = rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_choice", namespace=target_id.key.namespace)
        env_base = LogicalRecord(env_id, SemanticEnvironment((), (), choice_bindings=(target_id,), mechanically_extracted_dependencies=frozenset({target_id})))
        env_variant = LogicalRecord(env_id, SemanticEnvironment((), (), mechanically_extracted_dependencies=frozenset()))
        baseline_records.append(env_base)
        variant_records.append(env_variant)
        referring = env_variant
    elif row is MissingRowId.LEXICAL_BINDING:
        env_id = rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_lex", namespace=target_id.key.namespace)
        env_base = LogicalRecord(env_id, SemanticEnvironment((), (), lexical_bindings=(target_id,), mechanically_extracted_dependencies=frozenset({target_id})))
        env_variant = LogicalRecord(env_id, SemanticEnvironment((), (), mechanically_extracted_dependencies=frozenset()))
        baseline_records.append(env_base)
        variant_records.append(env_variant)
        referring = env_variant
    elif row is MissingRowId.EXTRANEOUS_LEXICAL_BINDING:
        lexical_id = rid(RecordKind.LEXICAL_BINDING, "lk_extra", namespace=target_id.key.namespace)
        lexical = LogicalRecord(lexical_id, LexicalBinding(lexical_id.key, rid(RecordKind.DECLARATION, "x_task", namespace=target_id.key.namespace), "scope_extra"))
        env_id = rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_t", namespace=target_id.key.namespace)
        env_base = LogicalRecord(env_id, SemanticEnvironment((), ()))
        env = LogicalRecord(env_id, SemanticEnvironment((), (), lexical_bindings=(lexical_id,), mechanically_extracted_dependencies=frozenset({lexical_id})))
        replacement_id = rid(RecordKind.REQUEST, "Q_t_extra", namespace=target_id.key.namespace)
        replacement = LogicalRecord(replacement_id, replace(target.value, semantic_environment=env_id))
        baseline_records = [item for item in baseline_records if item.identity != env_id]
        variant_records = [item for item in variant_records if item.identity != env_id]
        baseline_records.append(env_base)
        variant_records.extend((lexical, env, replacement))
        referring = env
    elif row in {MissingRowId.EXTENSION_OPTIONAL, MissingRowId.EXTENSION_REQUIRED, MissingRowId.ALIAS_OPTIONAL, MissingRowId.ALIAS_REQUIRED}:
        requirement_id = rid(RecordKind.SEMANTIC_EXTENSION, f"requirement.{row.value}", namespace=target_id.key.namespace)
        referring = LogicalRecord(requirement_id, EvolutionRecord(requirement_id.key, target_id, row in {MissingRowId.EXTENSION_REQUIRED, MissingRowId.ALIAS_REQUIRED}))
        baseline_records.append(referring)
        variant_records.append(referring)
    elif row in {MissingRowId.SIGMA_CONTRACT_SPEC, MissingRowId.SERVICE_CONTRACT_SPEC}:
        if row is MissingRowId.SIGMA_CONTRACT_SPEC:
            ref_id = rid(RecordKind.BINDING, "B_task_wrong_meaning", namespace=target_id.key.namespace)
            referring = LogicalRecord(ref_id, SemanticBinding(rid(RecordKind.DECLARATION, "DP(task_accepts)", namespace=target_id.key.namespace), target_id, frozenset({target_id}), frozenset({target_id})))
        else:
            ref_id = rid(RecordKind.CAPABILITY, "CAP_pred_wrong_sound", namespace=target_id.key.namespace)
            referring = LogicalRecord(ref_id, CapabilityDescriptor(ref_id.key, rid(RecordKind.SERVICE, "SK(predicates)", namespace=target_id.key.namespace), ABI0, key(f"PKG.{row.value}", namespace="plugin"), frozenset({"PREDICATE_EVALUATION"}), frozenset(), target_id, None, frozenset(), frozenset(), frozenset(), frozenset()))
        baseline_records.append(referring)
        variant_records.append(referring)
    elif row in {MissingRowId.SEMANTIC_ENVIRONMENT, MissingRowId.TRUST_ENVIRONMENT, MissingRowId.DEPENDENCY_ENVIRONMENT}:
        request_id = rid(RecordKind.REQUEST, "Q_t_reconstructed", namespace=target_id.key.namespace)
        request_value = InvocationRequest(rid(RecordKind.DECLARATION, "DP(task_accepts)", namespace=target_id.key.namespace), target_id if row is MissingRowId.SEMANTIC_ENVIRONMENT else rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_t", namespace=target_id.key.namespace), target_id if row is MissingRowId.DEPENDENCY_ENVIRONMENT else rid(RecordKind.DEPENDENCY_ENVIRONMENT, "D_t", namespace=target_id.key.namespace), target_id if row is MissingRowId.TRUST_ENVIRONMENT else rid(RecordKind.TRUST_ENVIRONMENT, "T_admitted", namespace=target_id.key.namespace), V1, ())
        referring = LogicalRecord(request_id, request_value)
        baseline_records.append(referring)
        variant_records.append(referring)
    elif row is MissingRowId.OBSERVATION_ENVIRONMENT:
        ref_id = rid(RecordKind.RESULT, "F_c_missing", namespace=target_id.key.namespace)
        referring = LogicalRecord(ref_id, ResultRecord(rid(RecordKind.REQUEST, "R_c", namespace=target_id.key.namespace), "InterfaceFailure", "SEMANTIC_MISMATCH"))
        baseline_records.append(referring)
        variant_records.append(referring)
    elif row is MissingRowId.LIFECYCLE:
        ref_id = rid(RecordKind.LIFECYCLE, "L_life_after", namespace=target_id.key.namespace)
        referring = LogicalRecord(ref_id, LifecycleRecord(rid(RecordKind.REQUEST, "R_c_alt", namespace=target_id.key.namespace), "INVOCABLE_FOR"))
        baseline_records.append(referring)
        variant_records.append(referring)
    elif row is MissingRowId.CONFLICT:
        ref_id = rid(RecordKind.CONFLICT, "conflict1", namespace=target_id.key.namespace)
        replacement_conflict = LogicalRecord(ref_id, NamedCarrier("conflict1"))
        variant_records.append(replacement_conflict)

    query = LookupRequest(target_id, referring.identity if referring is not None else None, context_roots)
    baseline_records = _complete_top_level(baseline_records, None)
    variant_records = _complete_top_level(variant_records, target_id)
    baseline = Universe(tuple(baseline_records), query)
    variant = Universe(tuple(variant_records), query)
    return MissingConstruction(row, target_id, baseline, variant, baseline_container, variant_container, query.referring_record)


_MISSING_ASSERTIONS = {
    MissingRowId.ABI: Judgment("MALFORMED"),
    MissingRowId.PLUGIN: Judgment("MALFORMED"),
    MissingRowId.DECLARATION: Judgment("MALFORMED"),
    MissingRowId.SYMBOL: Judgment("MALFORMED"),
    MissingRowId.EVENT: Judgment("MALFORMED"),
    MissingRowId.PAIR_DECLARATION: Judgment("MALFORMED"),
    MissingRowId.OUTCOME: Judgment("MALFORMED"),
    MissingRowId.BINDING: Judgment("OPEN_BINDINGS"),
    MissingRowId.PROFILE_BINDING: Judgment("OPEN_BINDINGS"),
    MissingRowId.PAIR_BINDING: Judgment("OPEN_BINDINGS"),
    MissingRowId.AUTHORITY_FACT: Judgment("OPEN_BINDINGS", (_row_identity(MissingRowId.AUTHORITY_FACT),)),
    MissingRowId.CHOICE_BINDING: Judgment("OPEN_BINDINGS", (_row_identity(MissingRowId.CHOICE_BINDING),)),
    MissingRowId.LEXICAL_BINDING: Judgment("OPEN_BINDINGS", (_row_identity(MissingRowId.LEXICAL_BINDING),)),
    MissingRowId.EXTRANEOUS_LEXICAL_BINDING: Judgment("MALFORMED_REQUEST", ("EXTRANEOUS_LEXICAL_BINDING", rid(RecordKind.LEXICAL_BINDING, "lk_extra", namespace="missing.extraneous_lexical_binding"))),
    MissingRowId.SERVICE: Judgment("EVALUABILITY_MISSING"),
    MissingRowId.CAPABILITY: Judgment("EVALUABILITY_MISSING"),
    MissingRowId.TRUST_POLICY: Judgment("TRUST_ROOT_ABSENT"),
    MissingRowId.TRUST_ROOT: Judgment("TRUST_ROOT_ABSENT", (_row_identity(MissingRowId.TRUST_ROOT),)),
    MissingRowId.CERTIFICATE: Judgment("NO_CERTIFICATE_ADMISSION", ("CONSISTENCY_UNKNOWN",)),
    MissingRowId.MIGRATION: Judgment("NO_MIGRATION", ("MK0",)),
    MissingRowId.COMPATIBILITY_CLAIM: Judgment("NO_COMPATIBILITY", ("CCK0",)),
    MissingRowId.EXTENSION_OPTIONAL: Judgment("NO_EFFECT", ("XK0",)),
    MissingRowId.EXTENSION_REQUIRED: Judgment("INCOMPATIBLE", ("XK1",)),
    MissingRowId.MODEL_CONTRACT: Judgment("OPEN_BINDINGS", ("MODEL_CONTRACT",)),
    MissingRowId.ALIAS_OPTIONAL: Judgment("NO_ALIAS", ("AK0",)),
    MissingRowId.ALIAS_REQUIRED: Judgment("MALFORMED", ("MISSING_ALIAS", "AK1")),
    MissingRowId.SIGMA_CONTRACT_SPEC: Judgment("BINDING_INCOMPATIBLE", ("OPEN_BINDINGS",)),
    MissingRowId.SERVICE_CONTRACT_SPEC: Judgment("CAPABILITY_INCOMPATIBLE", ("EVALUABILITY_MISSING",)),
    MissingRowId.REQUEST: Judgment("MALFORMED_REQUEST"),
    MissingRowId.RESULT: Judgment("INVOCATION_FAILED", ("PROTOCOL", "NO_RESULT", "NO_TRUTH")),
    MissingRowId.SEMANTIC_ENVIRONMENT: Judgment("MALFORMED_REQUEST", (rid(RecordKind.REQUEST, "Q_t_reconstructed", namespace="missing.semantic_environment"),)),
    MissingRowId.TRUST_ENVIRONMENT: Judgment("MALFORMED_REQUEST", (rid(RecordKind.REQUEST, "Q_t_reconstructed", namespace="missing.trust_environment"),)),
    MissingRowId.DEPENDENCY_ENVIRONMENT: Judgment("MALFORMED_REQUEST", (rid(RecordKind.REQUEST, "Q_t_reconstructed", namespace="missing.dependency_environment"),)),
    MissingRowId.OBSERVATION_ENVIRONMENT: Judgment("MALFORMED_RESULT", ("SEMANTIC_MISMATCH",)),
    MissingRowId.LIFECYCLE: Judgment("LIFECYCLE_REPLACED", (rid(RecordKind.LIFECYCLE, "L_life_after", namespace="missing.lifecycle"), "INVOCABLE_FOR")),
    MissingRowId.EVENT_VALUE: Judgment("MALFORMED"),
    MissingRowId.TRACE_EVENT: Judgment("MALFORMED"),
    MissingRowId.SOURCE: Judgment("MALFORMED"),
    MissingRowId.AUTHORITY_REF: Judgment("MALFORMED"),
    MissingRowId.EVIDENCE: Judgment("TRUTH_UNKNOWN"),
    MissingRowId.REASON: Judgment("MALFORMED_RESULT", ("MALFORMED_CARRIER",)),
    MissingRowId.CONFLICT: Judgment("CONFLICT_REPLACED", (rid(RecordKind.CONFLICT, "conflict1", namespace="missing.conflict"), "MALFORMED")),
}


@dataclass(frozen=True)
class ConfluenceConstruction:
    universe: Universe
    node_one: RecordIdentity
    node_two: RecordIdentity


def confluence_construction(order: OrderTag) -> ConfluenceConstruction:
    path = Path((PathSegment("dependency.lock"),))
    old_artifact = ArtifactContent(ArtifactTag.TEXT, ArtifactRole.DEPENDENCY_LOCK, Format.TEXT, ByteSize(1), ContentIdentity("old"))
    new_artifact = ArtifactContent(ArtifactTag.TEXT, ArtifactRole.DEPENDENCY_LOCK, Format.TEXT, ByteSize(1), ContentIdentity("new"))
    old = RepositorySnapshot(((path, old_artifact),))
    new = RepositorySnapshot(((path, new_artifact),))
    selector = ArtifactSelector(SelectorTag.PATHS_WITH_ROLE, frozenset({path}), ArtifactRole.DEPENDENCY_LOCK)
    observed_spec = ObservationSpec(ObservationSpecTag.ARTIFACT_VIEW, selector, ArtifactProjection(ProjectionTag.CONTENT))
    node_one_id = rid(RecordKind.OBSERVATION_NODE, "N_o", namespace="confluence")
    node_two_id = rid(RecordKind.OBSERVATION_NODE, "N_d", namespace="confluence")
    spec_one_id = rid(RecordKind.CONTRACT_SPEC, "CS(N_o)", namespace="confluence.contract")
    spec_two_id = rid(RecordKind.CONTRACT_SPEC, "CS(N_d)", namespace="confluence.contract")
    spec_one = LogicalRecord(spec_one_id, ContractSpec(spec_one_id.key, Layer.SIGMA, ContractRole.PREDICATE_MEANING, ("RepositorySnapshot",), frozenset({"TermResult"}), (), frozenset(), "observe"))
    query = ObservationQuery(node_one_id, ObservationKind.TERM_RESULT, ("before", "after"))
    spec_two = LogicalRecord(spec_two_id, ContractSpec(spec_two_id.key, Layer.SIGMA, ContractRole.PREDICATE_MEANING, ("RepositorySnapshot", "RepositorySnapshot"), frozenset({"TermResult"}), (query,), frozenset({node_one_id}), "changes_between"))
    node_one = LogicalRecord(node_one_id, ObservationNode(NodeOperation.OBSERVE, (observed_spec, new), spec_one_id))
    node_two = LogicalRecord(node_two_id, ObservationNode(NodeOperation.CHANGES_BETWEEN, (old, new), spec_two_id))
    binding_one = record(RecordKind.BINDING, "B(N_o)", SemanticBinding(node_one_id, spec_one_id, frozenset({spec_one_id}), frozenset({spec_one_id})), namespace="confluence.binding")
    binding_two = record(RecordKind.BINDING, "B(N_d)", SemanticBinding(node_two_id, spec_two_id, frozenset({spec_two_id, node_one_id}), frozenset({spec_two_id, node_one_id})), namespace="confluence.binding")
    package = _package("confluence", "capknow.semantic", bindings=(binding_one, binding_two), specs=(spec_one, spec_two), others=(node_one, node_two))
    preferred = (node_one_id, node_two_id) if order is OrderTag.FORWARD else (node_two_id, node_one_id)
    return ConfluenceConstruction(Universe((package,), GraphEvaluationRequest((node_one_id, node_two_id), preferred)), node_one_id, node_two_id)


def _confluence_expected(construction: ConfluenceConstruction) -> ObservationEvaluation:
    composition = _authoritative(construction.universe.records)
    one = composition.at(construction.node_one)
    two = composition.at(construction.node_two)
    assert one is not None and two is not None and isinstance(one.value, ObservationNode) and isinstance(two.value, ObservationNode)
    spec, snapshot = one.value.arguments
    path = next(iter(spec.selector.paths))
    artifact = snapshot.as_map()[path]
    observed = ObservationResult(ObservationResultTag.ARTIFACT, spec, Coverage(CoverageTag.COMPLETE), ((path, ObservationValue(ObservationValueTag.PRESENT_CONTENT, (artifact,))),))
    from .coding_plugin import ChangeEntry, ChangeKind, ChangeSet, TermResult
    old, new = two.value.arguments
    changed = ChangeSet(((path, ChangeEntry(ChangeKind.MODIFIED, old.as_map()[path], new.as_map()[path])),))
    return ObservationEvaluation(tuple(sorted(((construction.node_one, TermResult(value=observed)), (construction.node_two, TermResult(value=changed))))), Judgment("COMPLETED_INCONCLUSIVE"), "COMPLETED", ("WELL_FORMED", "CLOSED", "EVALUABILITY_AVAILABLE", "COMPLETED", "CONSISTENCY_UNKNOWN"))


def cycle_universe() -> Universe:
    first_spec_id = rid(RecordKind.CONTRACT_SPEC, "CS(event_matches)", namespace="cycle.contract")
    second_spec_id = rid(RecordKind.CONTRACT_SPEC, "CS(event_occurred)", namespace="cycle.contract")
    first_spec = LogicalRecord(first_spec_id, ContractSpec(first_spec_id.key, Layer.SIGMA, ContractRole.PREDICATE_MEANING, ("pattern", "event"), frozenset({"Eval"}), (), frozenset(), "event_matches"))
    second_spec = LogicalRecord(second_spec_id, ContractSpec(second_spec_id.key, Layer.SIGMA, ContractRole.PREDICATE_MEANING, ("pattern", "trace"), frozenset({"Eval"}), (), frozenset(), "event_occurred"))
    first_id = rid(RecordKind.BINDING, "B(event_matches)", namespace="cycle.binding")
    second_id = rid(RecordKind.BINDING, "B(event_occurred)", namespace="cycle.binding")
    first_decl_id = rid(RecordKind.DECLARATION, "DP(event_matches)", namespace="cycle")
    second_decl_id = rid(RecordKind.DECLARATION, "DP(event_occurred)", namespace="cycle")
    first_decl = LogicalRecord(first_decl_id, DeclarationShape(first_decl_id.key, key("SP(event_matches)", namespace="cycle.symbol"), "PREDICATE", (), "BOOL", (), frozenset()))
    second_decl = LogicalRecord(second_decl_id, DeclarationShape(second_decl_id.key, key("SP(event_occurred)", namespace="cycle.symbol"), "PREDICATE", (), "BOOL", (), frozenset()))
    first = LogicalRecord(first_id, SemanticBinding(first_decl_id, first_spec_id, frozenset({first_spec_id, second_id}), frozenset({first_spec_id, second_id})))
    second = LogicalRecord(second_id, SemanticBinding(second_decl_id, second_spec_id, frozenset({second_spec_id, first_id}), frozenset({second_spec_id, first_id})))
    package = _package("cycle", "capknow.semantic", declarations=(first_decl, second_decl), bindings=(first, second), specs=(first_spec, second_spec))
    return Universe((package,), FormationRequest((first_id, second_id)))


def _presentation_records() -> tuple[LogicalRecord, LogicalRecord, LogicalRecord, LogicalRecord]:
    decl_one_id = rid(RecordKind.DECLARATION, "D_pi11", owner="capknow.pi1", namespace="permutation")
    decl_two_id = rid(RecordKind.DECLARATION, "D_pi21", owner="capknow.pi2", namespace="permutation")
    decl_one = LogicalRecord(decl_one_id, DeclarationShape(decl_one_id.key, key("S_pi11", "capknow.pi1", "permutation"), "PREDICATE", (), "BOOL", (), frozenset()))
    decl_two = LogicalRecord(decl_two_id, DeclarationShape(decl_two_id.key, key("S_pi21", "capknow.pi2", "permutation"), "PREDICATE", (), "BOOL", (), frozenset()))
    spec_one_id = rid(RecordKind.CONTRACT_SPEC, "A_pi11", owner="capknow.pi1", namespace="permutation")
    spec_two_id = rid(RecordKind.CONTRACT_SPEC, "A_pi21", owner="capknow.pi2", namespace="permutation")
    spec_one = LogicalRecord(spec_one_id, ContractSpec(spec_one_id.key, Layer.SIGMA, ContractRole.PREDICATE_MEANING, ("x",), frozenset({"Eval"}), (), frozenset(), "pi1"))
    spec_two = LogicalRecord(spec_two_id, ContractSpec(spec_two_id.key, Layer.SIGMA, ContractRole.PREDICATE_MEANING, ("x",), frozenset({"Eval"}), (), frozenset(), "pi2"))
    return decl_one, spec_one, decl_two, spec_two


def permutation_universe(package_order: PackageOrderTag, record_order: RecordOrderTag) -> Universe:
    d1, s1, d2, s2 = _presentation_records()
    p1 = (d1, s1) if record_order is RecordOrderTag.DECLARATION_THEN_SPEC else (s1, d1)
    p2 = (d2, s2) if record_order is RecordOrderTag.DECLARATION_THEN_SPEC else (s2, d2)
    presentations = (p1, p2) if package_order is PackageOrderTag.PI1_PI2 else (p2, p1)
    marker = record(RecordKind.PRESENTATION, f"permutation.{package_order.value}.{record_order.value}", NamedCarrier("permutation"), namespace="permutation")
    return Universe((marker,), CompositionRequest(presentations))


def duplicate_universe(conflict: bool, order: OrderTag) -> Universe:
    declaration_id = rid(RecordKind.DECLARATION, "DP(task_accepts)", namespace="duplicate")
    base = LogicalRecord(declaration_id, DeclarationShape(declaration_id.key, key("SP(task_accepts)", namespace="duplicate.symbol"), "PREDICATE", (), "BOOL", (), frozenset()))
    other = base if not conflict else LogicalRecord(declaration_id, replace(base.value, facet_positions=(frozenset({"final"}),)))
    pair = (base, other) if order is OrderTag.FORWARD else (other, base)
    marker = record(RecordKind.PRESENTATION, f"duplicate.{conflict}.{order.value}", NamedCarrier("duplicate"), namespace="duplicate")
    return Universe((marker,), CompositionRequest((pair,)))


def _composition_expected(universe: Universe) -> CompositionReplay:
    assert isinstance(universe.request, CompositionRequest)
    records = tuple(item for presentation in universe.request.presentations for item in presentation)
    composition = _authoritative(records)
    return CompositionReplay(composition, Formation.MALFORMED if composition.conflicts else Formation.WELL_FORMED, Closure.NOT_APPLICABLE if composition.conflicts else Closure.CLOSED)


def _build_packet() -> tuple[dict[FixtureId, Universe], dict[FixtureId, Any]]:
    packet: dict[FixtureId, Universe] = {}
    assertions: dict[FixtureId, Any] = {}
    core = core_construction()
    fid = FixtureId(FixtureFamily.CORE_DEFINITIONAL)
    packet[fid] = core.universe
    assertions[fid] = _core_expected(core, TrustFixtureTag.ADMITTED)
    pair = pair_construction()
    fid = FixtureId(FixtureFamily.PAIR_INDEPENDENT)
    packet[fid] = pair.universe
    assertions[fid] = _pair_expected(pair)
    for tag in TrustFixtureTag:
        construction = core_construction(tag)
        fid = FixtureId(FixtureFamily.TRUST_BRANCH, (tag,))
        packet[fid] = construction.universe
        assertions[fid] = _core_expected(construction, tag)
    for row in MissingRowId:
        construction = missing_construction(row)
        base_id = FixtureId(FixtureFamily.MISSING_BASE, (row,))
        variant_id = FixtureId(FixtureFamily.MISSING_VARIANT, (row,))
        packet[base_id] = construction.baseline
        packet[variant_id] = construction.variant
        base_composition = _authoritative(construction.baseline.records)
        target = base_composition.at(construction.target)
        assertions[base_id] = LookupReplay(base_composition, Judgment("PRESENT", (target,)))
        assertions[variant_id] = LookupReplay(_authoritative(construction.variant.records), _MISSING_ASSERTIONS[row])
    for order in OrderTag:
        construction = confluence_construction(order)
        fid = FixtureId(FixtureFamily.CONFLUENCE_ORDER, (order,))
        packet[fid] = construction.universe
        assertions[fid] = _confluence_expected(construction)
    cycle = cycle_universe()
    fid = FixtureId(FixtureFamily.PROPER_CYCLE_REJECTION)
    packet[fid] = cycle
    assertions[fid] = (Formation.MALFORMED, Closure.NOT_APPLICABLE, Judgment("MALFORMED", ("dependency cycle",)))
    for package_order in PackageOrderTag:
        for record_order in RecordOrderTag:
            fid = FixtureId(FixtureFamily.PERMUTATION, (package_order, record_order))
            packet[fid] = permutation_universe(package_order, record_order)
            assertions[fid] = _composition_expected(packet[fid])
    for order in OrderTag:
        equal_id = FixtureId(FixtureFamily.DUPLICATE_EQUAL, (order,))
        conflict_id = FixtureId(FixtureFamily.DUPLICATE_CONFLICT, (order,))
        packet[equal_id] = duplicate_universe(False, order)
        packet[conflict_id] = duplicate_universe(True, order)
        assertions[equal_id] = _composition_expected(packet[equal_id])
        assertions[conflict_id] = _composition_expected(packet[conflict_id])
    return packet, assertions


_FIXTURE_PACKET, _ASSERTION_RESULTS = _build_packet()


def fixture_packet() -> dict[FixtureId, Universe]:
    return dict(_FIXTURE_PACKET)


def assertion_results() -> dict[FixtureId, Any]:
    return dict(_ASSERTION_RESULTS)


def fixture_universe(fixture: FixtureId) -> Universe:
    return _FIXTURE_PACKET[fixture]
