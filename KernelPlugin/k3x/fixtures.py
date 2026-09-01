"""Literal finite K3-S packet and independent assertion-only manifests."""

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any

from . import coding_plugin as cp

from .coding_plugin import (
    admission_type,
    ArtifactContent,
    ArtifactProjection,
    ArtifactRole,
    ArtifactSelector,
    ArtifactTag,
    ByteSize,
    ChangeEntry,
    ChangeKind,
    ChangeSet,
    CodingEvidenceEntry,
    CodingEvidencePayload,
    ContentIdentity,
    Coverage,
    CoverageTag,
    EvidencePayloadTag,
    EvidenceRef,
    EventKind,
    EventValue,
    TraceEvent,
    DependencyRefreshEventPayload,
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
    PairComparedFields,
    PairTraceDomain,
    ProjectionTag,
    RepositorySnapshot,
    SelectorTag,
    SnapshotIdentity,
    TaskSpec,
    TermResult,
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
    ConflictRef,
    PredicateFacetPositions,
    PredicateFacetPositionsConflict,
    CoreReplay,
    DeclarationShape,
    DependencyEnvironment,
    Evaluability,
    MigrationDeclaration,
    CompatibilityClaim,
    SemanticExtension,
    AliasBinding,
    ExactKey,
    Formation,
    FormationRequest,
    GraphEvaluationRequest,
    InvocationReplayRequest,
    InvocationRequest,
    ReasoningRequest,
    Judgment,
    Layer,
    LexicalBinding,
    LifecycleRecord,
    LogicalRecord,
    LookupReplay,
    LookupRequest,
    ModelContract,
    ModelCapabilitySummary,
    BindingTarget,
    ProfileBinding,
    ProfileDimensionKey,
    ProfileTarget,
    NamedCarrier,
    ConfluenceSubject,
    AttributedClause,
    ClauseAdoption,
    ConfluenceContract,
    EnvironmentUse,
    ReasoningTarget,
    ReasoningUnknown,
    ReasoningResultValue,
    ObservationEnvironment,
    ObservationEvaluation,
    ObservationKind,
    ObservationQuery,
    OccurrenceSemanticContractBundle,
    PairBinding,
    IndependentCoherenceProof,
    PairDeclaration,
    PairReplay,
    PairReplayRequest,
    PairAdmissionRequest,
    PairTarget,
    PairUse,
    ServiceUseTrustTarget,
    PairTrustTarget,
    PairCoherenceAdmission,
    PairCoherenceSubject,
    CertificateAdmission,
    EvolutionTarget,
    EvolutionTrustTarget,
    MigrationAdmissionSubject,
    CompatibilityAdmissionSubject,
    SemanticExtensionAdmissionSubject,
    MigrationAdmissionRequest,
    CompatibilityAdmissionRequest,
    SemanticExtensionAdmissionRequest,
    EvolutionProof,
    MigrationRelationAdmitted,
    CompatibilityClaimAdmitted,
    SemanticExtensionAdmitted,
    MigrationAdmissionResult,
    CompatibilityAdmissionResult,
    SemanticExtensionAdmissionResult,
    PairFullEvalProof,
    CertificateEnvelope,
    EvidenceRecord,
    OutcomeRecord,
    AuthorityFactRecord,
    SourceRecord,
    AuthorityRefRecord,
    EventValueRecord,
    TraceEventRecord,
    ReasonRecord,
    ConflictRecord,
    PairValidationResult,
    PluginPackage,
    ProducerRecord,
    RecordIdentity,
    RecordKind,
    ResolutionCoordinate,
    ResolutionRelation,
    ResultRecord,
    SemanticBinding,
    SemanticEnvironment,
    ServiceIdentity,
    TrustEnvironment,
    TrustPolicyRecord,
    TrustRootRecord,
    TrustRootJudgment,
    TrustState,
    TypeDeclaration,
    TypeAdmissionRelation,
    Universe,
    Version,
    compose_records,
    frozen_confluence_syntax_roots,
    frozen_task_syntax_roots,
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


IdentityLiteral = tuple[str, str, str, str, tuple[int, ...]]


@dataclass(frozen=True)
class ReplayAssertion:
    """Assertion-only literal projection of one public replay.

    The authoritative identities and semantic outcome are frozen separately
    from every fixture constructor.  This type is never imported by the
    reference evaluator or coding plugin.
    """

    authoritative_identities: tuple[IdentityLiteral, ...]
    conflicts: tuple[Any, ...]
    outcome: tuple[Any, ...]


ABI0 = Version((0,))
V1 = Version((1,))
V2 = Version((2,))


def key(
    local: str,
    owner: str = "capknow.semantic",
    namespace: str = "coding",
    version: Version = V1,
) -> ExactKey:
    return ExactKey(owner, namespace, local, version)


def rid(
    kind: RecordKind,
    local: str,
    owner: str = "capknow.semantic",
    namespace: str = "coding",
    version: Version = V1,
) -> RecordIdentity:
    return RecordIdentity(kind, key(local, owner, namespace, version))


def record(
    kind: RecordKind,
    local: str,
    value: Any,
    owner: str = "capknow.semantic",
    namespace: str = "coding",
    version: Version = V1,
) -> LogicalRecord:
    return LogicalRecord(rid(kind, local, owner, namespace, version), value)


def _package(
    local: str,
    owner: str,
    *,
    declarations: tuple[LogicalRecord, ...] = (),
    bindings: tuple[LogicalRecord, ...] = (),
    models: tuple[LogicalRecord, ...] = (),
    specs: tuple[LogicalRecord, ...] = (),
    services: tuple[LogicalRecord, ...] = (),
    certificates: tuple[LogicalRecord, ...] = (),
    others: tuple[LogicalRecord, ...] = (),
) -> LogicalRecord:
    plugin_key = key(local, owner, "plugin")
    pair_declarations = tuple(item for item in declarations if item.identity.kind is RecordKind.PAIR_DECLARATION)
    ordinary_declarations = tuple(item for item in declarations if item.identity.kind is not RecordKind.PAIR_DECLARATION)
    pair_bindings = tuple(item for item in bindings if item.identity.kind is RecordKind.PAIR_BINDING)
    profile_bindings = tuple(item for item in bindings if item.identity.kind is RecordKind.PROFILE_BINDING)
    ordinary_bindings = tuple(item for item in bindings if item.identity.kind is RecordKind.BINDING)
    value = PluginPackage(
        abi_version=ABI0,
        plugin_key=plugin_key,
        owner=owner,
        declarations=ordinary_declarations,
        pair_declarations=pair_declarations,
        bindings=ordinary_bindings,
        pair_bindings=pair_bindings,
        profile_bindings=profile_bindings,
        model_contracts=models,
        aliases=tuple(item for item in others if item.identity.kind is RecordKind.ALIAS),
        services=tuple(item for item in services if item.identity.kind is RecordKind.CAPABILITY),
        certificates=certificates,
        authority_facts=tuple(item for item in others if item.identity.kind is RecordKind.AUTHORITY_FACT),
        compatibility_claims=tuple(item for item in others if item.identity.kind is RecordKind.COMPATIBILITY_CLAIM),
        migrations=tuple(item for item in others if item.identity.kind is RecordKind.MIGRATION),
        semantic_extensions=tuple(item for item in others if item.identity.kind is RecordKind.SEMANTIC_EXTENSION),
    )
    return LogicalRecord(RecordIdentity(RecordKind.PACKAGE, plugin_key), value)


@dataclass(frozen=True)
class CoreConstruction:
    universe: Universe
    manifest: frozenset[LogicalRecord]
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
    result: RecordIdentity
    snapshot: RepositorySnapshot
    task: TaskSpec
    evidence: frozenset[CodingEvidenceEntry]


def _core_construction_local(
    trust_tag: TrustFixtureTag = TrustFixtureTag.ADMITTED,
) -> CoreConstruction:
    abi = record(
        RecordKind.ABI,
        "ABI0",
        AbiRecord(ABI0),
        namespace="abi",
        version=ABI0,
    )
    task_type_id = rid(
        RecordKind.TYPE_DECLARATION, "TaskSpec", namespace="coding.type"
    )
    snapshot_type_id = rid(
        RecordKind.TYPE_DECLARATION,
        "RepositorySnapshot",
        namespace="coding.type",
    )
    task_admission_id = rid(RecordKind.CONTRACT_SPEC, "ADMIT(TaskSpec)", namespace="coding.type.contract")
    snapshot_admission_id = rid(RecordKind.CONTRACT_SPEC, "ADMIT(RepositorySnapshot)", namespace="coding.type.contract")
    task_admission = LogicalRecord(task_admission_id, ContractSpec(
        task_admission_id.key, Layer.DELTA, ContractRole.TYPE_ADMISSION,
        ("TaskSpec",), frozenset({"ADMITTED", "NOT_ADMITTED"}), (), frozenset(),
        "admit_task_spec", TypeAdmissionRelation(admission_type("TaskSpec"))))
    snapshot_admission = LogicalRecord(snapshot_admission_id, ContractSpec(
        snapshot_admission_id.key, Layer.DELTA, ContractRole.TYPE_ADMISSION,
        ("RepositorySnapshot",), frozenset({"ADMITTED", "NOT_ADMITTED"}), (), frozenset(),
        "admit_repository_snapshot", TypeAdmissionRelation(admission_type("RepositorySnapshot"))))
    task_type = LogicalRecord(
        task_type_id,
        TypeDeclaration(task_type_id.key, task_admission.value, frozenset({task_admission_id})),
    )
    snapshot_type = LogicalRecord(
        snapshot_type_id,
        TypeDeclaration(
            snapshot_type_id.key,
            snapshot_admission.value,
            frozenset({snapshot_admission_id}),
        ),
    )
    declaration_id = rid(
        RecordKind.DECLARATION,
        "DP(task_accepts)",
        namespace="coding.declaration",
    )
    declaration = LogicalRecord(
        declaration_id,
        DeclarationShape(
            declaration_id.key,
            key("SP(task_accepts)", namespace="coding.symbol"),
            "PREDICATE",
            (
                task_type_id.key,
                snapshot_type_id.key,
                key("EvidenceStore", namespace="carrier.type"),
            ),
            "BOOL",
            (
                frozenset(),
                frozenset({"final"}),
                frozenset({"evidence"}),
            ),
            frozenset({task_type_id, snapshot_type_id}),
        ),
    )
    event_id = rid(
        RecordKind.EVENT,
        "DE(dependency_refresh)",
        namespace="coding.declaration",
    )
    event = LogicalRecord(
        event_id,
        DeclarationShape(
            event_id.key,
            key("EK(dependency_refresh)", namespace="coding.symbol"),
            "EVENT",
            (),
            "EVENT_VALUE",
            (),
            frozenset(),
        ),
    )
    sigma_spec_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(PREDICATE_MEANING,task_accepts)",
        namespace="coding.contract",
    )
    sigma_spec = LogicalRecord(
        sigma_spec_id,
        ContractSpec(
            sigma_spec_id.key,
            Layer.SIGMA,
            ContractRole.PREDICATE_MEANING,
            ("TaskSpec", "RepositorySnapshot", "EvidenceStore"),
            frozenset({"Eval"}),
            (),
            frozenset(),
            "task_accepts",
        ),
    )
    evidence_id = rid(RecordKind.CONTRACT_SPEC, "CS(EVIDENCE_SCHEMA,verification)", namespace="coding.contract")
    access_id = rid(RecordKind.CONTRACT_SPEC, "CS(ACCESS_BOUNDARY,task_final_evidence)", namespace="coding.contract")
    unknown_id = rid(RecordKind.CONTRACT_SPEC, "CS(UNKNOWN_BEHAVIOR,predicate)", namespace="coding.contract")
    error_id = rid(RecordKind.CONTRACT_SPEC, "CS(EVALUATION_ERROR_BEHAVIOR,predicate)", namespace="coding.contract")
    binding_id = rid(
        RecordKind.BINDING,
        "BINDING(DP(task_accepts))",
        namespace="coding.binding",
    )
    binding = LogicalRecord(
        binding_id,
        SemanticBinding(
            binding_id.key,
            declaration_id,
            "PREDICATE",
            sigma_spec_id,
            declaration.value.facet_positions,
            frozenset({declaration_id, sigma_spec_id, evidence_id, access_id, unknown_id, error_id}),
            frozenset({declaration_id, sigma_spec_id, evidence_id, access_id, unknown_id, error_id, task_type_id, snapshot_type_id, task_admission_id, snapshot_admission_id}),
            evidence_id,
            access_id,
            unknown_id,
            error_id,
            "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT",
        ),
    )
    profile_id = rid(
        RecordKind.PROFILE_BINDING,
        "PROFILE_BINDING(PK(implementation_evidence))",
        namespace="coding.binding",
    )
    profile = LogicalRecord(
        profile_id,
        ProfileBinding(
            key("PK(implementation_evidence)", namespace="coding.profile"),
            frozenset(), sigma_spec_id, evidence_id,
            frozenset(), frozenset(), unknown_id, error_id, error_id),
    )
    service_id = rid(
        RecordKind.SERVICE, "SK(predicates)", namespace="coding.service"
    )
    package_key = key("coding-minimal", namespace="plugin")
    service = LogicalRecord(
        service_id, ServiceIdentity(service_id.key, ABI0, package_key)
    )
    sound_id = rid(
        RecordKind.CONTRACT_SPEC,
        "QSOUND",
        namespace="coding.service.contract",
    )
    sound = LogicalRecord(
        sound_id,
        ContractSpec(
            sound_id.key,
            Layer.SERVICE,
            ContractRole.SOUND_FRAGMENT,
            ("ServiceAdmissionSubject",),
            frozenset({"IN_FRAGMENT", "OUTSIDE_FRAGMENT"}),
            (),
            frozenset(),
            "predicate_sound_fragment",
        ),
    )
    evidence_spec = LogicalRecord(
        evidence_id,
        ContractSpec(
            evidence_id.key,
            Layer.SIGMA,
            ContractRole.EVIDENCE_SCHEMA,
            ("EvidenceStore",),
            frozenset({"EvidenceMap", "InterfaceFailure"}),
            (),
            frozenset(),
            "verification_evidence_map",
        ),
    )
    unknown_spec = LogicalRecord(
        unknown_id,
        ContractSpec(
            unknown_id.key,
            Layer.SIGMA,
            ContractRole.UNKNOWN_BEHAVIOR,
            ("UnknownReasonSet",),
            frozenset({"Eval"}),
            (),
            frozenset(),
            "predicate_unknown",
        ),
    )
    error_spec = LogicalRecord(
        error_id,
        ContractSpec(
            error_id.key,
            Layer.SIGMA,
            ContractRole.EVALUATION_ERROR_BEHAVIOR,
            ("FailureReasonSet",),
            frozenset({"Eval"}),
            (),
            frozenset(),
            "predicate_error",
        ),
    )
    access_spec = LogicalRecord(access_id, ContractSpec(
        access_id.key, Layer.SIGMA, ContractRole.ACCESS_BOUNDARY,
        ("TaskSpec", "RepositorySnapshot", "EvidenceStore"),
        frozenset({"ADMITTED", "INADMISSIBLE"}), (), frozenset(),
        "task_final_evidence_access"))
    qreq_id = rid(RecordKind.CONTRACT_SPEC, "QREQ", namespace="coding.service.contract")
    qfail_id = rid(RecordKind.CONTRACT_SPEC, "QFAIL", namespace="coding.service.contract")
    qreq = LogicalRecord(qreq_id, ContractSpec(
        qreq_id.key, Layer.SERVICE, ContractRole.REQUIRED_EVIDENCE,
        ("ServiceAdmissionSubject", "EvidenceSet"), frozenset({"ADMISSIBLE", "INADMISSIBLE"}),
        (), frozenset(), "predicate_required_evidence"))
    qfail = LogicalRecord(qfail_id, ContractSpec(
        qfail_id.key, Layer.SERVICE, ContractRole.SERVICE_FAILURE_BEHAVIOR,
        ("InterfaceFailure",), frozenset({"EVAL_ERROR"}), (), frozenset(),
        "predicate_failure_projection"))
    policy_id = rid(RecordKind.TRUST_POLICY, "TP", namespace="trust")
    policy = LogicalRecord(
        policy_id, TrustPolicyRecord(policy_id.key, "embedding-policy")
    )
    root_id = rid(RecordKind.TRUST_ROOT, "TR", namespace="trust")
    root = LogicalRecord(
        root_id,
        TrustRootRecord(
            root_id.key,
            "embedding-policy",
            frozenset({rid(RecordKind.CAPABILITY, "CAP(predicates)", namespace="coding.capability")}),
            frozenset({"CONTRADICTION_PROOF"}),
            frozenset({service_id}),
            "V0_EXTERNAL_TRUST_PREMISE",
        ),
    )
    capability_id = rid(
        RecordKind.CAPABILITY,
        "CAP(predicates)",
        namespace="coding.capability",
    )
    capability = LogicalRecord(
        capability_id,
        CapabilityDescriptor(
            capability_id.key,
            service_id,
            ABI0,
            package_key,
            "PREDICATE_EVALUATION",
            "CONCRETE_EVALUATION_ONLY",
            frozenset({"PREDICATE_EVALUATION"}),
            frozenset({declaration_id}),
            sound_id,
            None,
            frozenset({binding_id}),
            frozenset({service_id, declaration_id, sound_id, qreq_id, qfail_id}),
            frozenset({service_id, declaration_id, sound_id, qreq_id, qfail_id, task_type_id, snapshot_type_id, task_admission_id, snapshot_admission_id}),
            qreq_id,
            frozenset({root_id}),
            qfail_id,
        ),
    )
    model_id = rid(
        RecordKind.MODEL_CONTRACT,
        "MODEL_task_accepts",
        namespace="coding.model",
    )
    model = LogicalRecord(
        model_id,
        ModelContract(
            model_id.key,
            binding_id,
            V1,
            declaration.value.symbol_key,
            declaration.value.argument_types,
            declaration.value.result_kind,
            declaration.value.facet_positions,
            evidence_id,
            unknown_id,
            error_id,
            sigma_spec_id,
            frozenset({ModelCapabilitySummary(
                capability_id, capability.value.service_role,
                capability.value.supported_judgments,
                capability.value.capability_class,
                capability.value.sound_fragment,
                capability.value.complete_fragment,
                capability.value.dependency_scope,
            )}),
        ),
    )
    package = _package(
        "coding-minimal",
        "capknow.semantic",
        declarations=(task_type, snapshot_type, declaration, event),
        bindings=(binding, profile),
        models=(model,),
        specs=(task_admission, snapshot_admission, sigma_spec, sound, evidence_spec, access_spec, unknown_spec, error_spec, qreq, qfail),
        services=(capability,),
    )

    path = Path((PathSegment("src"), PathSegment("module.py")))
    artifact = ArtifactContent(
        ArtifactTag.TEXT,
        ArtifactRole.SOURCE,
        Format.TEXT,
        ByteSize(7),
        ContentIdentity("content-final"),
    )
    snapshot = RepositorySnapshot(((path, artifact),))
    selector = ArtifactSelector(
        SelectorTag.PATHS_WITH_ROLE, frozenset({path}), ArtifactRole.SOURCE
    )
    observation_spec = ObservationSpec(
        ObservationSpecTag.ARTIFACT_VIEW,
        selector,
        ArtifactProjection(ProjectionTag.CONTENT),
    )
    observation = ObservationResult(
        ObservationResultTag.ARTIFACT,
        observation_spec,
        Coverage(CoverageTag.COMPLETE),
        (
            (
                path,
                ObservationValue(
                    ObservationValueTag.PRESENT_CONTENT, (artifact,)
                ),
            ),
        ),
    )
    verification_spec = VerificationSpec(
        "v_final", observation_spec, VERIFICATION_SCHEMA
    )
    evidence_ref = EvidenceRef(
        "auditor", "coding", "verification/final", VERIFICATION_SCHEMA
    )
    verification = VerificationRecord(
        verification_spec,
        SnapshotIdentity(snapshot),
        VerificationStatus.PASS,
        observation,
        frozenset({evidence_ref}),
    )
    evidence = frozenset(
        {
            CodingEvidenceEntry(
                evidence_ref,
                CodingEvidencePayload(
                    EvidencePayloadTag.VERIFICATION, verification
                ),
            )
        }
    )
    task = TaskSpec(
        frozenset({ObservationEquals(observation_spec, observation)}),
        frozenset({verification_spec}),
    )

    environment_id = rid(
        RecordKind.SEMANTIC_ENVIRONMENT, "E_t", namespace="environment"
    )
    required = frozen_task_syntax_roots()
    environment = LogicalRecord(
        environment_id,
        SemanticEnvironment(
            ABI0,
            (declaration_id,),
            (),
            (binding_id,),
            mechanically_extracted_dependencies=required,
        ),
    )
    dependency_id = rid(
        RecordKind.DEPENDENCY_ENVIRONMENT, "D_t", namespace="environment"
    )
    dependency = LogicalRecord(
        dependency_id,
        DependencyEnvironment(
            required,
            frozenset({binding_id}),
            frozenset({(declaration_id, binding_id)}),
            frozenset({declaration_id, binding_id}),
            binding.value.proper_semantic_dependencies,
            binding.value.dependency_closure,
            frozenset(),
        ),
    )
    trust_id = rid(
        RecordKind.TRUST_ENVIRONMENT,
        f"T_{trust_tag.value.lower()}",
        namespace="trust",
    )
    if trust_tag is TrustFixtureTag.ADMITTED:
        trust_value = TrustEnvironment(
            policy_id, "embedding-policy",
            ((root_id, TrustRootJudgment(TrustState.ADMITTED, root.value)),)
        )
    elif trust_tag is TrustFixtureTag.ABSENT:
        trust_value = TrustEnvironment(
            policy_id, "embedding-policy",
            ((root_id, TrustRootJudgment(TrustState.ABSENT)),))
    elif trust_tag is TrustFixtureTag.UNDECIDED:
        trust_value = TrustEnvironment(
            policy_id, "embedding-policy",
            ((root_id, TrustRootJudgment(TrustState.UNDECIDED, reasons=("ROOT_DISCOVERY_UNRESOLVED",))),)
        )
    elif trust_tag is TrustFixtureTag.INCOMPATIBLE:
        trust_value = TrustEnvironment(
            policy_id, "embedding-policy",
            ((root_id, TrustRootJudgment(TrustState.INCOMPATIBLE, reasons=("ROOT_TARGET_NOT_PERMITTED",))),)
        )
    else:
        trust_value = TrustEnvironment(
            policy_id,
            "embedding-policy",
            ((root_id, TrustRootJudgment(TrustState.FAILED, reasons=("ROOT_DISCOVERY_PROTOCOL_FAILURE",))),),
        )
    trust = LogicalRecord(trust_id, trust_value)
    request_id = rid(
        RecordKind.REQUEST,
        f"Q_t[{trust_tag.value}]",
        namespace="request",
    )
    request = LogicalRecord(
        request_id,
        InvocationRequest(
            declaration_id,
            environment_id,
            dependency_id,
            trust_id,
            V1,
            (task, snapshot, evidence),
        ),
    )
    result_id = rid(
        RecordKind.RESULT,
        f"RES_t[{trust_tag.value}]",
        namespace="result",
    )
    result = LogicalRecord(
        result_id,
        ResultRecord(
            request_id,
            "Eval",
            Eval(Truth.TRUE, frozenset({evidence_ref})),
        ),
    )
    result_records = (result,) if trust_tag is TrustFixtureTag.ADMITTED else ()
    top_level = (
        abi,
        package,
        task_admission,
        snapshot_admission,
        sigma_spec,
        sound,
        evidence_spec,
        access_spec,
        unknown_spec,
        error_spec,
        qreq,
        qfail,
        service,
        policy,
        root,
        environment,
        dependency,
        trust,
        request,
        *result_records,
    )
    manifest = frozenset(
        (
            abi,
            package,
            task_type,
            snapshot_type,
            task_admission,
            snapshot_admission,
            declaration,
            event,
            binding,
            profile,
            model,
            sigma_spec,
            sound,
            evidence_spec,
            access_spec,
            unknown_spec,
            error_spec,
            qreq,
            qfail,
            service,
            capability,
            policy,
            root,
            environment,
            dependency,
            trust,
            request,
            *result_records,
        )
    )
    return CoreConstruction(
        Universe(top_level, InvocationReplayRequest(request_id)),
        manifest,
        abi.identity,
        package.identity,
        declaration_id,
        binding_id,
        model_id,
        capability_id,
        service_id,
        sigma_spec_id,
        sound_id,
        environment_id,
        dependency_id,
        trust_id,
        root_id,
        request_id,
        result_id,
        snapshot,
        task,
        evidence,
    )


@dataclass(frozen=True)
class PairConstruction:
    universe: Universe
    manifest: frozenset[LogicalRecord]
    request: RecordIdentity
    pair_binding: RecordIdentity
    certificate: RecordIdentity
    validation_references: frozenset[RecordIdentity]
    producer_records: tuple[LogicalRecord, ...]


def pair_construction() -> PairConstruction:
    abi = record(
        RecordKind.ABI,
        "ABI0",
        AbiRecord(ABI0),
        namespace="abi",
        version=ABI0,
    )
    left_decl_id = rid(
        RecordKind.DECLARATION,
        "DP(refresh_scope)",
        namespace="coding.declaration",
    )
    right_decl_id = rid(
        RecordKind.DECLARATION,
        "DP(refresh_occurred)",
        namespace="coding.declaration",
    )
    left_decl = LogicalRecord(
        left_decl_id,
        DeclarationShape(
            left_decl_id.key,
            key("SP(refresh_scope)", namespace="coding.symbol"),
            "PREDICATE",
            (key("EventValue", namespace="carrier.type"),),
            "BOOL",
            (frozenset(),),
            frozenset(),
        ),
    )
    right_decl = LogicalRecord(
        right_decl_id,
        DeclarationShape(
            right_decl_id.key,
            key("SP(refresh_occurred)", namespace="coding.symbol"),
            "PREDICATE",
            (key("Trace", namespace="carrier.type"),),
            "BOOL",
            (frozenset({"trace"}),),
            frozenset(),
        ),
    )
    pair_event_id = rid(
        RecordKind.EVENT, "DE(dependency_refresh)", namespace="coding.declaration"
    )
    pair_event = LogicalRecord(
        pair_event_id,
        DeclarationShape(
            pair_event_id.key,
            key("EK(dependency_refresh)", namespace="coding.event"),
            "EVENT",
            (),
            "EVENT_VALUE",
            (),
            frozenset(),
        ),
    )
    left_spec_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(PREDICATE_MEANING,refresh_scope)",
        namespace="coding.contract",
    )
    right_spec_id = rid(
        RecordKind.CONTRACT_SPEC,
        "T3_A1_MEANING_LIFT(pd,sb)",
        namespace="coding.contract",
    )
    left_spec = LogicalRecord(
        left_spec_id,
        ContractSpec(
            left_spec_id.key,
            Layer.SIGMA,
            ContractRole.PREDICATE_MEANING,
            ("EventValue",),
            frozenset({"Eval"}),
            (),
            frozenset(),
            "refresh_scope",
        ),
    )
    right_spec = LogicalRecord(
        right_spec_id,
        ContractSpec(
            right_spec_id.key,
            Layer.SIGMA,
            ContractRole.OCCURRENCE_MEANING,
            ("Trace",),
            frozenset({"Eval"}),
            (),
            frozenset(),
            "T3_A1_MEANING_LIFT(pd,sb)",
        ),
    )
    pair_evidence_id = rid(RecordKind.CONTRACT_SPEC, "T3_A1_EVIDENCE_LIFT(pd,sb)", namespace="coding.contract")
    pair_access_id = rid(RecordKind.CONTRACT_SPEC, "T3_A1_ACCESS_LIFT(pd,sb)", namespace="coding.contract")
    pair_unknown_id = rid(RecordKind.CONTRACT_SPEC, "T3_A1_UNKNOWN_LIFT(pd,sb)", namespace="coding.contract")
    pair_error_id = rid(RecordKind.CONTRACT_SPEC, "T3_A1_ERROR_LIFT(pd,sb)", namespace="coding.contract")
    pair_aux_specs = (
        LogicalRecord(pair_evidence_id, ContractSpec(pair_evidence_id.key, Layer.SIGMA, ContractRole.EVIDENCE_SCHEMA, ("Trace",), frozenset({"EvidenceSet"}), (), frozenset(), "pair_evidence")),
        LogicalRecord(pair_access_id, ContractSpec(pair_access_id.key, Layer.SIGMA, ContractRole.ACCESS_BOUNDARY, ("Trace",), frozenset({"ADMITTED", "INADMISSIBLE"}), (), frozenset(), "pair_trace_access")),
        LogicalRecord(pair_unknown_id, ContractSpec(pair_unknown_id.key, Layer.SIGMA, ContractRole.UNKNOWN_BEHAVIOR, ("UnknownReasonSet",), frozenset({"Eval"}), (), frozenset(), "pair_unknown")),
        LogicalRecord(pair_error_id, ContractSpec(pair_error_id.key, Layer.SIGMA, ContractRole.EVALUATION_ERROR_BEHAVIOR, ("FailureReasonSet",), frozenset({"Eval"}), (), frozenset(), "pair_error")),
    )
    left_id = rid(
        RecordKind.BINDING,
        "B_alt(refresh_scope)",
        namespace="coding.binding",
    )
    right_id = rid(
        RecordKind.BINDING,
        "B_alt(refresh_occurred)",
        namespace="coding.binding",
    )
    occurrence_binding_id = RecordIdentity(RecordKind.BINDING, right_decl_id.key)
    left = LogicalRecord(
        left_id,
        SemanticBinding(
            left_id.key,
            left_decl_id,
            "PREDICATE",
            left_spec_id,
            (frozenset(),),
            frozenset({left_decl_id, left_spec_id, pair_evidence_id, pair_access_id, pair_unknown_id, pair_error_id}),
            frozenset({left_decl_id, left_spec_id, pair_evidence_id, pair_access_id, pair_unknown_id, pair_error_id}),
            pair_evidence_id,
            pair_access_id,
            pair_unknown_id,
            pair_error_id,
            "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT",
        ),
    )
    right = LogicalRecord(
        right_id,
        OccurrenceSemanticContractBundle(
            right_spec_id,
            (frozenset({"trace"}),),
            pair_evidence_id,
            pair_access_id,
            pair_unknown_id,
            pair_error_id,
            "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT",
            frozenset({right_decl_id, right_spec_id, pair_evidence_id, pair_access_id, pair_unknown_id, pair_error_id}),
            frozenset({right_decl_id, right_spec_id, pair_evidence_id, pair_access_id, pair_unknown_id, pair_error_id}),
        ),
    )
    pair_id = rid(
        RecordKind.PAIR_DECLARATION, "PAIR(refresh)", namespace="pair"
    )
    pair = LogicalRecord(
        pair_id, PairDeclaration(
            pair_id.key,
            left_decl.value.symbol_key,
            right_decl.value.symbol_key,
            frozenset({key("EK(dependency_refresh)", namespace="coding.event")}),
            frozenset({left_decl_id, right_decl_id, pair_event_id}),
        )
    )

    validator_owner = "capknow.audit.pair-validator"
    validator_service_id = rid(
        RecordKind.SERVICE,
        "refresh",
        owner=validator_owner,
        namespace="coding.validation",
    )
    validator_service = LogicalRecord(
        validator_service_id,
        ServiceIdentity(
            validator_service_id.key,
            ABI0,
            key("pair-validator", validator_owner, "plugin"),
        ),
    )
    psound_id = rid(
        RecordKind.CONTRACT_SPEC,
        "PSOUND",
        owner=validator_owner,
        namespace="pair.contract",
    )
    pcomplete_id = rid(
        RecordKind.CONTRACT_SPEC,
        "PCOMPLETE",
        owner=validator_owner,
        namespace="pair.contract",
    )
    pevidence_id = rid(
        RecordKind.CONTRACT_SPEC,
        "PEVIDENCE",
        owner=validator_owner,
        namespace="pair.contract",
    )
    pfailure_id = rid(
        RecordKind.CONTRACT_SPEC,
        "PFAILURE",
        owner=validator_owner,
        namespace="pair.contract",
    )
    psound = LogicalRecord(
        psound_id,
        ContractSpec(
            psound_id.key,
            Layer.SERVICE,
            ContractRole.SOUND_FRAGMENT,
            ("ServiceAdmissionSubject",),
            frozenset({"IN_FRAGMENT", "OUTSIDE_FRAGMENT"}),
            (),
            frozenset(),
            "pair_sound_fragment",
        ),
    )
    pcomplete = LogicalRecord(
        pcomplete_id,
        ContractSpec(
            pcomplete_id.key,
            Layer.SERVICE,
            ContractRole.COMPLETE_FRAGMENT,
            ("ServiceAdmissionSubject",),
            frozenset({"IN_FRAGMENT", "OUTSIDE_FRAGMENT"}),
            (),
            frozenset(),
            "pair_complete_fragment",
        ),
    )
    pevidence = LogicalRecord(
        pevidence_id,
        ContractSpec(
            pevidence_id.key,
            Layer.SERVICE,
            ContractRole.REQUIRED_EVIDENCE,
            ("ServiceAdmissionSubject", "PairFullEvalProof", "EvidenceSet"),
            frozenset({"ADMISSIBLE", "INADMISSIBLE"}),
            (),
            frozenset(),
            "pair_required_evidence",
        ),
    )
    pfailure = LogicalRecord(
        pfailure_id,
        ContractSpec(
            pfailure_id.key,
            Layer.SERVICE,
            ContractRole.SERVICE_FAILURE_BEHAVIOR,
            ("InterfaceFailure",),
            frozenset({"PairValidationResult.REASONING_ERROR"}),
            (),
            frozenset(),
            "pair_failure_projection",
        ),
    )
    validation_capability_id = rid(
        RecordKind.CAPABILITY,
        "refresh_full_eval",
        owner=validator_owner,
        namespace="coding.validation.capability",
    )
    pair_dependency_scope = frozenset({
        pair_id, left_id, right_id,
        left_decl_id, right_decl_id, pair_event_id,
        left_spec_id, right_spec_id, pair_evidence_id, pair_access_id,
        pair_unknown_id, pair_error_id,
        rid(RecordKind.MODEL_CONTRACT, "MODEL_refresh_occurred_pair", namespace="pair.model"),
    })
    capability_proper = frozenset({
        validator_service_id, pair_id, psound_id, pcomplete_id,
        pevidence_id, pfailure_id,
    })
    capability_closure = capability_proper | frozenset({
        left_decl_id, right_decl_id, pair_event_id,
    })
    validation_capability = LogicalRecord(
        validation_capability_id,
        CapabilityDescriptor(
            validation_capability_id.key,
            validator_service_id,
            ABI0,
            key("pair-validator", validator_owner, "plugin"),
            "PAIR_VALIDATION",
            "COMPLETE_FOR_DECLARED_FRAGMENT",
            frozenset({"EVENT_PAIR_COHERENCE_ADMISSION"}),
            frozenset({PairTarget(pair_id)}),
            psound_id,
            pcomplete_id,
            pair_dependency_scope,
            capability_proper,
            capability_closure,
            pevidence_id,
            frozenset({rid(RecordKind.TRUST_ROOT, "TRP", namespace="pair.trust")}),
            pfailure_id,
        ),
    )
    validator_package = _package(
        "pair-validator",
        validator_owner,
        specs=(psound, pcomplete, pevidence, pfailure),
        services=(validation_capability,),
    )

    proof_owner = "capknow.audit.pair-proof"
    certificate_id = rid(
        RecordKind.CERTIFICATE,
        "PCERT",
        owner=proof_owner,
        namespace="pair.certificate",
    )
    validation_owner = "capknow.audit.pair-validator"
    proof_id = rid(RecordKind.EVIDENCE, "PairFullEvalProof", owner=proof_owner, namespace="pair.proof")
    evidence_ref_id = rid(RecordKind.EVIDENCE, "PAIR_PROOF_REF", owner=proof_owner, namespace="pair.evidence")
    proof = LogicalRecord(proof_id, PairFullEvalProof(
        pair_id.key, right_id, right_spec_id,
        PairTraceDomain.ALL_ADMITTED_TRACES,
        PairComparedFields.COMPLETE_EVAL_RECORD))
    evidence_ref = LogicalRecord(evidence_ref_id, EvidenceRecord(
        proof_owner, "coding.pair-proof", "refresh_full_eval", psound_id))
    left_model_id = rid(RecordKind.MODEL_CONTRACT, "MODEL_refresh_scope_pair", namespace="pair.model")
    right_model_id = rid(RecordKind.MODEL_CONTRACT, "MODEL_refresh_occurred_pair", namespace="pair.model")
    left_model = LogicalRecord(left_model_id, ModelContract(
        left_model_id.key, left_id, V1, left_decl.value.symbol_key,
        left_decl.value.argument_types, left_decl.value.result_kind,
        left_decl.value.facet_positions, pair_evidence_id, pair_unknown_id,
        pair_error_id, left_spec_id, frozenset({ModelCapabilitySummary(
            validation_capability_id, validation_capability.value.service_role,
            validation_capability.value.supported_judgments,
            validation_capability.value.capability_class,
            validation_capability.value.sound_fragment,
            validation_capability.value.complete_fragment,
            validation_capability.value.dependency_scope)})))
    right_model = LogicalRecord(right_model_id, ModelContract(
        right_model_id.key, occurrence_binding_id, V1, right_decl.value.symbol_key,
        right_decl.value.argument_types, right_decl.value.result_kind,
        right_decl.value.facet_positions, pair_evidence_id, pair_unknown_id,
        pair_error_id, right_spec_id, frozenset({ModelCapabilitySummary(
            validation_capability_id, validation_capability.value.service_role,
            validation_capability.value.supported_judgments,
            validation_capability.value.capability_class,
            validation_capability.value.sound_fragment,
            validation_capability.value.complete_fragment,
            validation_capability.value.dependency_scope)})))
    validation_refs = frozenset({certificate_id, validation_capability_id})
    pair_binding_id = rid(
        RecordKind.PAIR_BINDING, "PB_alt", namespace="pair.binding"
    )
    pair_binding = LogicalRecord(
        pair_binding_id,
        PairBinding(
            pair_id.key,
            left_id,
            occurrence_binding_id,
            right_model_id,
            right_id,
            certificate_id,
            validation_capability_id,
            frozenset({pair_id, left_id, right_id, right_model_id}),
            frozenset({pair_id, left_id, right_id, right_model_id, left_decl_id, right_decl_id, pair_event_id, left_spec_id, right_spec_id, pair_evidence_id, pair_access_id, pair_unknown_id, pair_error_id}),
            validation_refs,
            IndependentCoherenceProof(right_id, certificate_id, validation_capability_id),
        ),
    )
    pair_subject = PairCoherenceSubject(
        pair_id, left_id, occurrence_binding_id,
        PairTraceDomain.ALL_ADMITTED_TRACES,
        PairComparedFields.COMPLETE_EVAL_RECORD,
    )
    pair_type_dependencies = {
        "PathSegment": (), "Path": ("PathSegment",), "PathSet": ("Path",),
        "ArtifactRole": (), "Format": (), "ByteSize": (),
        "ContentIdentity": (), "FieldId": (), "FieldValue": (),
        "SubjectId": (),
        "BehaviorValue": ("ContentIdentity", "FieldId", "FieldValue"),
        "ArtifactContent": ("ArtifactRole", "Format", "ByteSize", "ContentIdentity", "FieldId", "FieldValue", "SubjectId", "BehaviorValue"),
        "RepositorySnapshot": ("Path", "ArtifactContent"),
        "SnapshotIdentity": ("RepositorySnapshot",),
        "ArtifactSelector": ("PathSet", "ArtifactRole"),
        "DependencyRefreshEventPayload": ("ArtifactSelector", "SnapshotIdentity"),
        "PairTraceDomain": (), "PairComparedFields": (),
        "ServiceAdmissionSubject": ("PairTraceDomain", "PairComparedFields"),
    }
    pair_types: dict[str, LogicalRecord] = {}
    pair_admissions: dict[str, LogicalRecord] = {}
    for type_name, nested_names in pair_type_dependencies.items():
        type_identity = rid(RecordKind.TYPE_DECLARATION, f"T({type_name})", namespace="coding.type")
        admission_identity = rid(RecordKind.CONTRACT_SPEC, f"CS(TYPE_ADMISSION,type.{type_name})", namespace="coding.type-admission")
        nested = frozenset(
            rid(RecordKind.TYPE_DECLARATION, f"T({name})", namespace="coding.type")
            for name in nested_names
        )
        value_type = PairCoherenceSubject if type_name == "ServiceAdmissionSubject" else admission_type(type_name)
        admission = LogicalRecord(admission_identity, ContractSpec(
            admission_identity.key, Layer.DELTA, ContractRole.TYPE_ADMISSION,
            (type_name,), frozenset({"ADMITTED", "NOT_ADMITTED"}),
            tuple(ObservationQuery(item, ObservationKind.TYPE_ADMISSION_FACT, ("nested_value",)) for item in sorted(nested)),
            nested, f"admit_{type_name}", TypeAdmissionRelation(value_type),
        ))
        pair_admissions[type_name] = admission
        pair_types[type_name] = LogicalRecord(
            type_identity,
            TypeDeclaration(type_identity.key, admission.value,
                            nested | frozenset({admission_identity})),
        )
    literal_rows = (
        ("PairTraceDomain", PairTraceDomain.ALL_ADMITTED_TRACES),
        ("PairComparedFields", PairComparedFields.COMPLETE_EVAL_RECORD),
        ("ServiceAdmissionSubject", pair_subject),
    )
    literal_declarations: list[LogicalRecord] = []
    literal_bindings: list[LogicalRecord] = []
    literal_models: list[LogicalRecord] = []
    literal_specs: list[LogicalRecord] = []
    def nested_type_closure(type_name: str) -> frozenset[RecordIdentity]:
        nested_names = pair_type_dependencies[type_name]
        return frozenset({pair_types[type_name].identity,
                          pair_admissions[type_name].identity}) | frozenset().union(*(
            nested_type_closure(name) for name in nested_names
        ))
    for type_name, literal_value in literal_rows:
        type_identity = pair_types[type_name].identity
        local_suffix = type_name
        declaration_id = rid(RecordKind.DECLARATION, f"L({local_suffix})", namespace="coding.literal")
        declaration = LogicalRecord(declaration_id, DeclarationShape(
            declaration_id.key, key(f"LS({local_suffix})", namespace="coding.literal.symbol"),
            "LITERAL", (), type_identity.key.local, (), frozenset({type_identity}), literal_value,
        ))
        role_specs: dict[ContractRole, RecordIdentity] = {}
        for role in (ContractRole.LITERAL_MEANING, ContractRole.EVIDENCE_SCHEMA,
                     ContractRole.ACCESS_BOUNDARY, ContractRole.UNKNOWN_BEHAVIOR,
                     ContractRole.EVALUATION_ERROR_BEHAVIOR):
            spec_id = rid(RecordKind.CONTRACT_SPEC, f"CS({role.value},{local_suffix})", namespace="coding.literal.contract")
            spec = LogicalRecord(spec_id, ContractSpec(
                spec_id.key, Layer.SIGMA, role, (type_name,),
                frozenset({"VALUE"}) if role is ContractRole.LITERAL_MEANING else frozenset({"NONE"}),
                (), frozenset(), f"literal_{role.value.lower()}_{type_name}",
            ))
            role_specs[role] = spec_id
            literal_specs.append(spec)
        binding_id = rid(RecordKind.BINDING, f"BINDING(L({local_suffix}))", namespace="coding.literal.binding")
        direct = frozenset({declaration_id, *role_specs.values()})
        closure = direct | nested_type_closure(type_name)
        binding = LogicalRecord(binding_id, SemanticBinding(
            binding_id.key, declaration_id, "LITERAL", role_specs[ContractRole.LITERAL_MEANING],
            (), direct, closure, role_specs[ContractRole.EVIDENCE_SCHEMA],
            role_specs[ContractRole.ACCESS_BOUNDARY], role_specs[ContractRole.UNKNOWN_BEHAVIOR],
            role_specs[ContractRole.EVALUATION_ERROR_BEHAVIOR],
            "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT",
        ))
        model_id = rid(RecordKind.MODEL_CONTRACT, f"MODEL_LITERAL({local_suffix})", namespace="coding.literal.model")
        model = LogicalRecord(model_id, ModelContract(
            model_id.key, binding_id, V1, declaration.value.symbol_key, (),
            declaration.value.result_kind, (), role_specs[ContractRole.EVIDENCE_SCHEMA],
            role_specs[ContractRole.UNKNOWN_BEHAVIOR], role_specs[ContractRole.EVALUATION_ERROR_BEHAVIOR],
            role_specs[ContractRole.LITERAL_MEANING], frozenset(),
        ))
        literal_declarations.append(declaration)
        literal_bindings.append(binding)
        literal_models.append(model)
    pair_package = _package(
        "coding-minimal",
        "capknow.semantic",
        declarations=(*pair_types.values(), *literal_declarations,
                      left_decl, right_decl, pair_event, pair),
        bindings=(left, *literal_bindings, pair_binding),
        models=(left_model, right_model, *literal_models),
        specs=(*pair_admissions.values(), *literal_specs,
               left_spec, right_spec, *pair_aux_specs),
    )
    semantic_environment_id = rid(
        RecordKind.SEMANTIC_ENVIRONMENT, "E_p", namespace="pair.environment"
    )
    semantic_environment = LogicalRecord(
        semantic_environment_id,
        SemanticEnvironment(
            ABI0,
            (*tuple(item.identity for item in pair_types.values()),
             *tuple(item.identity for item in literal_declarations),
             left_decl_id, right_decl_id, pair_event_id),
            (pair_id,),
            (left_id, *tuple(item.identity for item in literal_bindings)),
            pair_bindings=(pair_binding_id,),
            mechanically_extracted_dependencies=frozenset(
                {pair_id}
            ),
        ),
    )
    dependency_environment_id = rid(
        RecordKind.DEPENDENCY_ENVIRONMENT,
        "D_p",
        namespace="pair.environment",
    )
    dependency_environment = LogicalRecord(
        dependency_environment_id,
        DependencyEnvironment(
            frozenset(semantic_environment.value.declarations + semantic_environment.value.pair_declarations),
            frozenset(semantic_environment.value.bindings + semantic_environment.value.pair_bindings),
            frozenset({(left_decl_id, left_id), *(
                (declaration.identity, binding.identity)
                for declaration, binding in zip(literal_declarations, literal_bindings, strict=True)
            )}),
            frozenset(semantic_environment.value.declarations + semantic_environment.value.pair_declarations + semantic_environment.value.bindings + semantic_environment.value.pair_bindings),
            pair_binding.value.proper_semantic_dependencies | left.value.proper_semantic_dependencies | frozenset().union(*(item.value.proper_semantic_dependencies for item in literal_bindings)),
            pair_binding.value.dependency_closure | left.value.dependency_closure | frozenset().union(*(item.value.dependency_closure for item in literal_bindings)),
            validation_refs,
        ),
    )
    updated_summary = ModelCapabilitySummary(
        validation_capability_id, validation_capability.value.service_role,
        validation_capability.value.supported_judgments,
        validation_capability.value.capability_class,
        validation_capability.value.sound_fragment,
        validation_capability.value.complete_fragment,
        dependency_environment.value.transitive_dependency_closure,
    )
    validation_capability = replace(
        validation_capability,
        value=replace(
            validation_capability.value,
            dependency_scope=dependency_environment.value.transitive_dependency_closure,
        ),
    )
    left_model = replace(left_model, value=replace(
        left_model.value, capability_summaries=frozenset({updated_summary})))
    right_model = replace(right_model, value=replace(
        right_model.value, capability_summaries=frozenset({updated_summary})))
    pair_package = replace(pair_package, value=replace(
        pair_package.value,
        model_contracts=(left_model, right_model, *literal_models),
    ))
    validator_package = replace(validator_package, value=replace(
        validator_package.value, services=(validation_capability,)))
    policy_id = rid(RecordKind.TRUST_POLICY, "TP", namespace="pair.trust")
    policy = LogicalRecord(
        policy_id, TrustPolicyRecord(policy_id.key, "embedding-policy")
    )
    root_id = rid(RecordKind.TRUST_ROOT, "TRP", namespace="pair.trust")
    root = LogicalRecord(
        root_id,
        TrustRootRecord(
            root_id.key,
            "embedding-policy",
            frozenset({validation_capability_id}),
            frozenset({"EVENT_PAIR_COHERENCE_PROOF"}),
            frozenset({
                ServiceUseTrustTarget(
                    validation_capability_id,
                    "EVENT_PAIR_COHERENCE_ADMISSION",
                    PairUse(pair_id),
                    semantic_environment_id,
                ),
                PairTrustTarget(pair_id),
            }),
            "V0_EXTERNAL_TRUST_PREMISE",
        ),
    )
    trust_id = rid(
        RecordKind.TRUST_ENVIRONMENT, "T_p", namespace="pair.trust"
    )
    trust = LogicalRecord(
        trust_id,
        TrustEnvironment(
            policy_id, "embedding-policy",
            ((root_id, TrustRootJudgment(TrustState.ADMITTED, root.value)),)
        ),
    )
    request_id = rid(RecordKind.REQUEST, "R_p", namespace="pair.request")
    conclusion = PairCoherenceAdmission(pair_id, certificate_id)
    request = LogicalRecord(
        request_id, PairAdmissionRequest(
            ABI0, pair_id, semantic_environment_id, trust_id,
            dependency_environment_id, PairTarget(pair_id), validation_capability_id)
    )
    envelope = LogicalRecord(
        certificate_id,
        CertificateEnvelope(
            certificate_id.key, "EVENT_PAIR_COHERENCE_PROOF", request_id,
            (pair_id, right_id), semantic_environment_id,
            validation_capability_id, psound_id, dependency_environment_id,
            conclusion, validation_capability_id, root_id,
            "SYMBOLIC", proof_id, frozenset({evidence_ref_id}),
        ),
    )
    proof_package = _package("pair-proof", proof_owner, certificates=(envelope,))
    admission = record(
        RecordKind.OUTCOME, "PADMIT", CertificateAdmission(certificate_id, conclusion),
        namespace="pair.admission",
    )
    validation_result = record(
        RecordKind.RESULT, "PRESULT",
        PairValidationResult(pair_id.key, certificate_id.key, conclusion),
        namespace="pair.result",
    )
    producers = (
        record(
            RecordKind.PRODUCER,
            "producer.pair",
            ProducerRecord(pair_id, "capknow.semantic", "PAIR_OWNER"),
            namespace="pair.producer",
        ),
        record(
            RecordKind.PRODUCER,
            "producer.certificate",
            ProducerRecord(
                certificate_id, proof_owner, "CERTIFICATE_OWNER"
            ),
            namespace="pair.producer",
        ),
        record(
            RecordKind.PRODUCER,
            "producer.validation.proof",
            ProducerRecord(
                evidence_ref_id, proof_owner, "EVIDENCE_OWNER"
            ),
            namespace="pair.producer",
        ),
        record(
            RecordKind.PRODUCER,
            "producer.full.eval.proof",
            ProducerRecord(proof_id, proof_owner, "PROOF_OWNER"),
            namespace="pair.producer",
        ),
        record(
            RecordKind.PRODUCER,
            "producer.validation.capability",
            ProducerRecord(
                validation_capability_id,
                validator_owner,
                "VALIDATION_CAPABILITY_OWNER",
            ),
            namespace="pair.producer",
        ),
        record(
            RecordKind.PRODUCER,
            "producer.validation.service",
            ProducerRecord(validator_service_id, validator_owner, "VALIDATION_SERVICE_OWNER"),
            namespace="pair.producer",
        ),
        record(
            RecordKind.PRODUCER,
            "producer.trust.environment",
            ProducerRecord(
                trust_id, "embedding-policy", "TRUST_ENVIRONMENT_OWNER"
            ),
            namespace="pair.producer",
        ),
        record(
            RecordKind.PRODUCER,
            "producer.trust.policy",
            ProducerRecord(
                policy_id, "embedding-policy", "TRUST_POLICY_OWNER"
            ),
            namespace="pair.producer",
        ),
        record(
            RecordKind.PRODUCER,
            "producer.trust.root",
            ProducerRecord(
                root_id, "embedding-policy", "TRUST_ROOT_OWNER"
            ),
            namespace="pair.producer",
        ),
    )
    top_level = (
        abi,
        pair_package,
        proof_package,
        validator_package,
        *pair_admissions.values(),
        *literal_specs,
        left_spec,
        right_spec,
        *pair_aux_specs,
        right,
        left_model,
        right_model,
        psound,
        pcomplete,
        pevidence,
        pfailure,
        validator_service,
        semantic_environment,
        dependency_environment,
        proof,
        evidence_ref,
        policy,
        root,
        trust,
        request,
        envelope,
        admission,
        validation_result,
        *producers,
    )
    manifest = frozenset(
        (
            abi,
            pair_package,
            *pair_types.values(),
            *pair_admissions.values(),
            *literal_declarations,
            *literal_bindings,
            *literal_models,
            *literal_specs,
            left_decl,
            right_decl,
            pair_event,
            pair,
            left,
            right,
            pair_binding,
            left_spec,
            right_spec,
            *pair_aux_specs,
            proof_package,
            proof,
            evidence_ref,
            left_model,
            right_model,
            validator_package,
            psound,
            pcomplete,
            pevidence,
            pfailure,
            validator_service,
            validation_capability,
            semantic_environment,
            dependency_environment,
            policy,
            root,
            trust,
            request,
            envelope,
            admission,
            validation_result,
            *producers,
        )
    )
    return PairConstruction(
        Universe(top_level, PairReplayRequest(request_id)),
        manifest,
        request_id,
        pair_binding_id,
        certificate_id,
        validation_refs,
        producers,
    )


@dataclass(frozen=True)
class LiteralMissingRow:
    row: MissingRowId
    target: RecordIdentity
    baseline_records: tuple[LogicalRecord, ...]
    variant_records: tuple[LogicalRecord, ...]
    baseline_manifest: frozenset[LogicalRecord]
    variant_manifest: frozenset[LogicalRecord]
    removed_records: frozenset[LogicalRecord]
    added_records: frozenset[LogicalRecord]
    baseline_coordinate: ResolutionCoordinate
    variant_coordinate: ResolutionCoordinate
    baseline_context: tuple[RecordIdentity, ...]
    variant_context: tuple[RecordIdentity, ...]
    expected: Judgment
    baseline_container: RecordIdentity | None = None
    variant_container: RecordIdentity | None = None


@dataclass(frozen=True)
class MissingConstruction:
    row: MissingRowId
    target: RecordIdentity
    baseline: Universe
    variant: Universe
    baseline_manifest: frozenset[LogicalRecord]
    variant_manifest: frozenset[LogicalRecord]
    removed_records: frozenset[LogicalRecord]
    added_records: frozenset[LogicalRecord]
    baseline_container: RecordIdentity | None
    variant_container: RecordIdentity | None


def _literal_missing_rows() -> tuple[LiteralMissingRow, ...]:
    """The 42 frozen row objects; no identity or status is synthesized."""

    core = core_construction()
    abi = next(item for item in core.universe.records if item.identity == core.abi)
    package = next(
        item for item in core.universe.records if item.identity == core.package
    )
    assert isinstance(package.value, PluginPackage)
    core_members = {item.identity: item for item in core.manifest}
    declaration = core_members[core.declaration]
    event = core_members[rid(
        RecordKind.EVENT, "DE(dependency_refresh)",
        namespace="coding.declaration")]
    binding = core_members[core.binding]
    profile = next(
        item
        for item in package.value.profile_bindings
        if item.identity.kind is RecordKind.PROFILE_BINDING
    )
    model = core_members[core.model]
    service = core_members[core.service]
    capability = core_members[core.capability]
    sigma_spec = core_members[core.sigma_spec]
    sound_spec = core_members[core.sound_spec]
    environment = next(
        item
        for item in core.universe.records
        if item.identity == core.semantic_environment
    )
    dependency = next(
        item
        for item in core.universe.records
        if item.identity == core.dependency_environment
    )
    trust = next(
        item
        for item in core.universe.records
        if item.identity == core.trust_environment
    )
    policy = next(
        item
        for item in core.universe.records
        if item.identity.kind is RecordKind.TRUST_POLICY
    )
    root = next(
        item for item in core.universe.records if item.identity == core.trust_root
    )
    request = next(
        item for item in core.universe.records if item.identity == core.request
    )
    result = next(
        item for item in core.universe.records if item.identity == core.result
    )

    package_no_declaration = replace(
        package,
        value=replace(
            package.value,
            declarations=tuple(
                item
                for item in package.value.declarations
                if item.identity != declaration.identity
            ),
        ),
    )
    package_no_event = replace(
        package,
        value=replace(
            package.value,
            declarations=tuple(
                item
                for item in package.value.declarations
                if item.identity != event.identity
            ),
        ),
    )
    package_no_binding = replace(
        package,
        value=replace(
            package.value,
            bindings=tuple(
                item
                for item in package.value.bindings
                if item.identity != binding.identity
            ),
        ),
    )
    package_no_profile = replace(
        package,
        value=replace(
            package.value,
            profile_bindings=tuple(
                item
                for item in package.value.profile_bindings
                if item.identity != profile.identity
            ),
        ),
    )
    package_no_service = replace(
        package,
        value=replace(
            package.value,
            services=package.value.services,
        ),
    )
    model_without_capability = replace(
        model, value=replace(model.value, capability_summaries=frozenset())
    )
    package_no_capability = replace(
        package,
        value=replace(
            package.value,
            model_contracts=(model_without_capability,),
            services=tuple(
                item
                for item in package.value.services
                if item.identity != capability.identity
            ),
        ),
    )
    package_no_model = replace(
        package, value=replace(package.value, model_contracts=())
    )

    pair = pair_construction()
    pair_package = next(
        item
        for item in pair.universe.records
        if isinstance(item.value, PluginPackage)
        and item.value.owner == "capknow.semantic"
    )
    pair_declaration = next(
        item
        for item in pair_package.value.pair_declarations
        if item.identity.kind is RecordKind.PAIR_DECLARATION
    )
    pair_binding = next(
        item
        for item in pair_package.value.pair_bindings
        if item.identity.kind is RecordKind.PAIR_BINDING
    )
    pair_package_no_declaration = replace(
        pair_package,
        value=replace(
            pair_package.value,
            pair_declarations=tuple(
                item
                for item in pair_package.value.pair_declarations
                if item.identity != pair_declaration.identity
            ),
        ),
    )
    pair_package_no_binding = replace(
        pair_package,
        value=replace(
            pair_package.value,
            pair_bindings=tuple(
                item
                for item in pair_package.value.pair_bindings
                if item.identity != pair_binding.identity
            ),
        ),
    )

    outcome = record(
        RecordKind.OUTCOME,
        "O_w",
        OutcomeRecord("ADAPTER_WITNESS_OUTCOME", "SATISFIED"),
        namespace="outcome",
    )
    authority = record(
        RecordKind.AUTHORITY_FACT,
        "AF(choice,1)",
        AuthorityFactRecord(
            key("AF(choice,1)", namespace="authority"),
            rid(RecordKind.AUTHORITY_REF, "AUTH(choice,1)", namespace="authority.ref"),
            rid(RecordKind.SOURCE, "SRC(choice,1)", namespace="authority.source"),
            "choice-controller", "LOCAL_STORAGE", frozenset(),
        ),
        namespace="authority",
    )
    choice_id = rid(
        RecordKind.CHOICE_BINDING, "cb0", namespace="authority.choice"
    )
    choice = LogicalRecord(
        choice_id, ChoiceBinding(choice_id.key, authority.identity, "LOCAL_STORAGE")
    )
    choice_environment_id = rid(
        RecordKind.SEMANTIC_ENVIRONMENT,
        "E_choice",
        namespace="authority.environment",
    )
    choice_environment = LogicalRecord(
        choice_environment_id,
        SemanticEnvironment(
            ABI0,
            (),
            (),
            (),
            authority_facts=(authority.identity,),
            choice_bindings=(choice_id,),
        ),
    )
    choice_environment_no_fact = replace(
        choice_environment,
        value=SemanticEnvironment(ABI0, (), (), (), authority_facts=(), choice_bindings=()),
    )
    choice_environment_no_binding = replace(
        choice_environment,
        value=SemanticEnvironment(
            ABI0, (), (), (), authority_facts=(authority.identity,), choice_bindings=()
        ),
    )
    authority_package = _package(
        "authority-owner",
        "capknow.semantic",
        bindings=(choice,),
        others=(authority,),
    )
    authority_package_no_fact = replace(
        authority_package,
        value=replace(authority_package.value, authority_facts=()),
    )

    lexical_id = rid(
        RecordKind.LEXICAL_BINDING, "lk0", namespace="lexical"
    )
    lexical = LogicalRecord(
        lexical_id,
        LexicalBinding(lexical_id.key, declaration.identity, "scope_lex"),
    )
    lexical_environment_id = rid(
        RecordKind.SEMANTIC_ENVIRONMENT,
        "E_lex",
        namespace="lexical.environment",
    )
    lexical_environment = LogicalRecord(
        lexical_environment_id,
        SemanticEnvironment(
            ABI0,
            (declaration.identity,),
            (),
            (binding.identity,),
            lexical_bindings=(lexical_id,),
        ),
    )
    lexical_environment_no_binding = replace(
        lexical_environment,
        value=SemanticEnvironment(
            ABI0, (declaration.identity,), (), (binding.identity,), lexical_bindings=()
        ),
    )
    lexical_dependency_id = rid(
        RecordKind.DEPENDENCY_ENVIRONMENT,
        "D_lex",
        namespace="lexical.environment",
    )
    lexical_dependency = LogicalRecord(
        lexical_dependency_id,
        DependencyEnvironment(
            frozenset({declaration.identity}),
            frozenset({binding.identity}),
            frozenset({(declaration.identity, binding.identity)}),
            frozenset({declaration.identity, binding.identity}),
            binding.value.proper_semantic_dependencies | frozenset({lexical_id}),
            binding.value.dependency_closure | frozenset({lexical_id}),
            frozenset(),
        ),
    )
    lexical_dependency_no_binding = replace(
        lexical_dependency,
        value=DependencyEnvironment(
            frozenset({declaration.identity}),
            frozenset({binding.identity}),
            frozenset({(declaration.identity, binding.identity)}),
            frozenset({declaration.identity, binding.identity}),
            binding.value.proper_semantic_dependencies,
            binding.value.dependency_closure,
            frozenset(),
        ),
    )
    lexical_request_id = rid(
        RecordKind.REQUEST, "R_lex", namespace="lexical.request"
    )
    lexical_request = LogicalRecord(
        lexical_request_id,
        InvocationRequest(
            declaration.identity,
            lexical_environment_id,
            lexical_dependency_id,
            trust.identity,
            V1,
            (core.task, core.snapshot, core.evidence),
        ),
    )

    extra_lexical_id = rid(
        RecordKind.LEXICAL_BINDING, "lk_extra", namespace="lexical"
    )
    extra_lexical = LogicalRecord(
        extra_lexical_id,
        LexicalBinding(
            extra_lexical_id.key, declaration.identity, "predicate_evaluation"
        ),
    )
    extra_environment_id = rid(
        RecordKind.SEMANTIC_ENVIRONMENT,
        "E_t_extra",
        namespace="environment",
    )
    extra_environment = LogicalRecord(
        extra_environment_id,
        SemanticEnvironment(
            ABI0,
            (declaration.identity,),
            (),
            (binding.identity,),
            lexical_bindings=(extra_lexical_id,),
            mechanically_extracted_dependencies=frozenset(
                {declaration.identity, binding.identity}
            ),
        ),
    )
    extra_dependency_id = rid(
        RecordKind.DEPENDENCY_ENVIRONMENT,
        "D_t_extra",
        namespace="environment",
    )
    extra_dependency = LogicalRecord(
        extra_dependency_id,
        DependencyEnvironment(
            frozenset({declaration.identity}),
            frozenset({binding.identity}),
            frozenset({(declaration.identity, binding.identity)}),
            frozenset({declaration.identity, binding.identity}),
            binding.value.proper_semantic_dependencies,
            binding.value.dependency_closure,
            frozenset(),
        ),
    )
    extra_request_id = rid(
        RecordKind.REQUEST, "Q_t_extra", namespace="request"
    )
    extra_request = LogicalRecord(
        extra_request_id,
        InvocationRequest(
            declaration.identity,
            extra_environment_id,
            extra_dependency_id,
            trust.identity,
            V1,
            (core.task, core.snapshot, core.evidence),
        ),
    )

    root_missing_environment = replace(
        trust,
        value=TrustEnvironment(policy.identity, "embedding-policy", ()),
    )

    proof_package = next(
        item
        for item in pair.universe.records
        if isinstance(item.value, PluginPackage)
        and item.value.owner == "capknow.audit.pair-proof"
    )
    pair_certificate = next(iter(proof_package.value.certificates))
    proof_package_no_certificate = replace(
        proof_package,
        value=replace(proof_package.value, certificates=()),
    )
    pair_request = next(
        item
        for item in pair.universe.records
        if item.identity == pair.request
    )
    pair_variant_records = tuple(
        proof_package_no_certificate
        if item.identity == proof_package.identity
        else item
        for item in pair.universe.records
    )
    pair_variant_manifest = (
        pair.manifest - frozenset({proof_package, pair_certificate})
    ) | frozenset({proof_package_no_certificate})

    evo_owner = "capknow.fixture.evolution-owner"
    migration_id = rid(
        RecordKind.MIGRATION,
        "MK0",
        owner=evo_owner,
        namespace="evolution",
    )
    compatibility_id = rid(
        RecordKind.COMPATIBILITY_CLAIM,
        "CCK0",
        owner=evo_owner,
        namespace="evolution",
    )
    optional_extension_id = rid(
        RecordKind.SEMANTIC_EXTENSION,
        "XK0",
        owner=evo_owner,
        namespace="evolution",
    )
    required_extension_id = rid(
        RecordKind.SEMANTIC_EXTENSION,
        "XK1",
        owner=evo_owner,
        namespace="evolution",
    )
    optional_alias_id = rid(
        RecordKind.ALIAS,
        "AK0",
        owner=evo_owner,
        namespace="evolution.alias",
    )
    required_alias_id = rid(
        RecordKind.ALIAS,
        "AK1",
        owner=evo_owner,
        namespace="evolution.alias",
    )
    migration_relation_id = rid(RecordKind.CONTRACT_SPEC, "MR0", owner=evo_owner, namespace="evolution.contract")
    compatibility_contract_id = rid(RecordKind.CONTRACT_SPEC, "CC0", owner=evo_owner, namespace="evolution.contract")
    extension_effect_id = rid(RecordKind.CONTRACT_SPEC, "XE0", owner=evo_owner, namespace="evolution.contract")
    extension_payload_id = rid(RecordKind.CONTRACT_SPEC, "XP0", owner=evo_owner, namespace="evolution.contract")
    evolution_root_id = rid(RecordKind.TRUST_ROOT, "TRE", namespace="evolution.trust")
    migration_certificate_id = rid(RecordKind.CERTIFICATE, "EC_m", owner="capknow.audit.evolution-proof", namespace="evolution.certificate")
    compatibility_certificate_id = rid(RecordKind.CERTIFICATE, "EC_c", owner="capknow.audit.evolution-proof", namespace="evolution.certificate")
    optional_extension_certificate_id = rid(RecordKind.CERTIFICATE, "EC_x0", owner="capknow.audit.evolution-proof", namespace="evolution.certificate")
    required_extension_certificate_id = rid(RecordKind.CERTIFICATE, "EC_x1", owner="capknow.audit.evolution-proof", namespace="evolution.certificate")
    migration_validator_id = rid(RecordKind.CAPABILITY, "EVC_m", owner="capknow.audit.evolution-validator", namespace="evolution.capability")
    compatibility_validator_id = rid(RecordKind.CAPABILITY, "EVC_c", owner="capknow.audit.evolution-validator", namespace="evolution.capability")
    optional_extension_validator_id = rid(RecordKind.CAPABILITY, "EVC_x0", owner="capknow.audit.evolution-validator", namespace="evolution.capability")
    required_extension_validator_id = rid(RecordKind.CAPABILITY, "EVC_x1", owner="capknow.audit.evolution-validator", namespace="evolution.capability")
    migration = LogicalRecord(
        migration_id,
        MigrationDeclaration(
            migration_id.key, environment.identity, environment.identity,
            "FULL_CONTRACT_EQUIVALENCE", migration_relation_id,
            migration_certificate_id, migration_validator_id, evolution_root_id,
        ),
    )
    compatibility = LogicalRecord(
        compatibility_id,
        CompatibilityClaim(
            compatibility_id.key, ABI0, ABI0, frozenset({migration_id}),
            frozenset({binding.identity}), compatibility_contract_id,
            compatibility_certificate_id, compatibility_validator_id,
            evolution_root_id,
        ),
    )
    optional_extension = LogicalRecord(
        optional_extension_id,
        SemanticExtension(
            optional_extension_id.key, optional_alias_id, Layer.SIGMA,
            extension_effect_id, extension_payload_id,
            optional_extension_certificate_id, optional_extension_validator_id,
            evolution_root_id,
        ),
    )
    required_extension = LogicalRecord(
        required_extension_id,
        SemanticExtension(
            required_extension_id.key, required_alias_id, Layer.SIGMA,
            extension_effect_id, extension_payload_id,
            required_extension_certificate_id, required_extension_validator_id,
            evolution_root_id,
        ),
    )
    optional_alias = LogicalRecord(
        optional_alias_id,
        AliasBinding(optional_alias_id.key, declaration.identity.key, "PREDICATE", V1),
    )
    required_alias = LogicalRecord(
        required_alias_id,
        AliasBinding(required_alias_id.key, declaration.identity.key, "PREDICATE", V1),
    )
    migration_relation = LogicalRecord(migration_relation_id, ContractSpec(
        migration_relation_id.key, Layer.SIGMA, ContractRole.MIGRATION_RELATION,
        ("EvolutionAdmissionSubject",), frozenset({"FULL_CONTRACT_EQUIVALENCE"}),
        (), frozenset(), "migration_relation_missing_fixture",
    ))
    compatibility_contract = LogicalRecord(compatibility_contract_id, ContractSpec(
        compatibility_contract_id.key, Layer.SERVICE, ContractRole.COMPATIBILITY_VALIDATION,
        ("EvolutionAdmissionSubject",), frozenset({"COMPATIBLE", "INCOMPATIBLE"}),
        (), frozenset(), "compatibility_missing_fixture",
    ))
    extension_effect = LogicalRecord(extension_effect_id, ContractSpec(
        extension_effect_id.key, Layer.SIGMA, ContractRole.SEMANTIC_EXTENSION_EFFECT,
        ("EvolutionAdmissionSubject",), frozenset({"PRESERVE_EXACT_TARGET"}),
        (), frozenset(), "extension_effect_missing_fixture",
    ))
    extension_payload = LogicalRecord(extension_payload_id, ContractSpec(
        extension_payload_id.key, Layer.SIGMA, ContractRole.SEMANTIC_EXTENSION_PAYLOAD,
        ("EvolutionAdmissionSubject",), frozenset({"NO_ADDITIONAL_MEANING"}),
        (), frozenset(), "extension_payload_missing_fixture",
    ))
    evolution_policy_id = rid(RecordKind.TRUST_POLICY, "TP", namespace="evolution.trust")
    evolution_policy = LogicalRecord(
        evolution_policy_id, TrustPolicyRecord(evolution_policy_id.key, "embedding-policy")
    )
    evolution_trust_id = rid(RecordKind.TRUST_ENVIRONMENT, "T_evo", namespace="evolution.trust")
    evolution_rows = (
        ("m", migration, migration_certificate_id, migration_validator_id,
         "MIGRATION_RELATION_ADMISSION", "MIGRATION_RELATION_PROOF", migration_relation_id),
        ("c", compatibility, compatibility_certificate_id, compatibility_validator_id,
         "COMPATIBILITY_CLAIM_ADMISSION", "COMPATIBILITY_CLAIM_PROOF", compatibility_contract_id),
        ("x0", optional_extension, optional_extension_certificate_id, optional_extension_validator_id,
         "SEMANTIC_EXTENSION_ADMISSION", "SEMANTIC_EXTENSION_VALIDATION", extension_effect_id),
        ("x1", required_extension, required_extension_certificate_id, required_extension_validator_id,
         "SEMANTIC_EXTENSION_ADMISSION", "SEMANTIC_EXTENSION_VALIDATION", extension_effect_id),
    )
    evolution_services: list[LogicalRecord] = []
    evolution_specs: list[LogicalRecord] = []
    evolution_dependencies: list[LogicalRecord] = []
    evolution_capabilities: list[LogicalRecord] = []
    evolution_requests: list[LogicalRecord] = []
    evolution_proofs: list[LogicalRecord] = []
    evolution_evidence: list[LogicalRecord] = []
    evolution_envelopes: list[LogicalRecord] = []
    evolution_admissions: list[LogicalRecord] = []
    evolution_results: list[LogicalRecord] = []
    evolution_producers: list[LogicalRecord] = []
    evolution_targets: list[EvolutionTarget] = []
    evolution_trust_targets: list[EvolutionTrustTarget] = []
    for row_name, candidate, certificate_identity, validator_identity, judgment_name, certificate_kind, relation_identity in evolution_rows:
        candidate_identity = candidate.identity
        if isinstance(candidate.value, MigrationDeclaration):
            subject = MigrationAdmissionSubject(
                candidate.value.migration_key, candidate.value.source_environment,
                candidate.value.target_environment, candidate.value.semantic_relation,
                candidate.value.relation_contract, candidate.identity.key.owner,
            )
            conclusion = MigrationRelationAdmitted(candidate.identity.key, certificate_identity)
            service_role = "MIGRATION_VALIDATION"
            request_type = MigrationAdmissionRequest
            result_type = MigrationAdmissionResult
        elif isinstance(candidate.value, CompatibilityClaim):
            subject = CompatibilityAdmissionSubject(
                candidate.value.claim_key, candidate.value.source_abi,
                candidate.value.target_abi, candidate.value.source_keys,
                candidate.value.target_keys, candidate.value.compatibility_contract,
                candidate.identity.key.owner,
            )
            conclusion = CompatibilityClaimAdmitted(candidate.identity.key, certificate_identity)
            service_role = "COMPATIBILITY_VALIDATION"
            request_type = CompatibilityAdmissionRequest
            result_type = CompatibilityAdmissionResult
        else:
            subject = SemanticExtensionAdmissionSubject(
                candidate.value.extension_key, candidate.value.target_record_identity,
                candidate.value.owner_layer, candidate.value.semantic_effect,
                candidate.value.payload, candidate.identity.key.owner,
            )
            conclusion = SemanticExtensionAdmitted(candidate.identity.key, certificate_identity)
            service_role = "SEMANTIC_EXTENSION_VALIDATION"
            request_type = SemanticExtensionAdmissionRequest
            result_type = SemanticExtensionAdmissionResult
        target = EvolutionTarget(judgment_name, subject, environment.identity)
        trust_target = EvolutionTrustTarget(judgment_name, subject)
        evolution_targets.append(target)
        evolution_trust_targets.append(trust_target)
        service_id = rid(RecordKind.SERVICE, f"EVSK_{row_name}", owner="capknow.audit.evolution-validator", namespace="evolution.service")
        evolution_service = LogicalRecord(service_id, ServiceIdentity(
            service_id.key, ABI0,
            key("evolution-validator", "capknow.audit.evolution-validator", "plugin"),
        ))
        spec_ids = {
            role: rid(RecordKind.CONTRACT_SPEC, f"{prefix}_{row_name}", owner="capknow.audit.evolution-validator", namespace="evolution.contract")
            for role, prefix in (
                (ContractRole.SOUND_FRAGMENT, "ES"),
                (ContractRole.COMPLETE_FRAGMENT, "ECOMP"),
                (ContractRole.REQUIRED_EVIDENCE, "EE"),
                (ContractRole.SERVICE_FAILURE_BEHAVIOR, "EF"),
            )
        }
        row_specs = (
            LogicalRecord(spec_ids[ContractRole.SOUND_FRAGMENT], ContractSpec(
                spec_ids[ContractRole.SOUND_FRAGMENT].key, Layer.SERVICE, ContractRole.SOUND_FRAGMENT,
                ("EvolutionAdmissionSubject",), frozenset({"IN_FRAGMENT", "OUTSIDE_FRAGMENT"}), (), frozenset(), "evolution_sound_fragment")),
            LogicalRecord(spec_ids[ContractRole.COMPLETE_FRAGMENT], ContractSpec(
                spec_ids[ContractRole.COMPLETE_FRAGMENT].key, Layer.SERVICE, ContractRole.COMPLETE_FRAGMENT,
                ("EvolutionAdmissionSubject",), frozenset({"IN_FRAGMENT", "OUTSIDE_FRAGMENT"}), (), frozenset(), "evolution_complete_fragment")),
            LogicalRecord(spec_ids[ContractRole.REQUIRED_EVIDENCE], ContractSpec(
                spec_ids[ContractRole.REQUIRED_EVIDENCE].key, Layer.SERVICE, ContractRole.REQUIRED_EVIDENCE,
                ("EvolutionAdmissionSubject", "EvolutionProof", "EvidenceSet"), frozenset({"ADMISSIBLE", "INADMISSIBLE"}), (), frozenset(), "evolution_required_evidence")),
            LogicalRecord(spec_ids[ContractRole.SERVICE_FAILURE_BEHAVIOR], ContractSpec(
                spec_ids[ContractRole.SERVICE_FAILURE_BEHAVIOR].key, Layer.SERVICE, ContractRole.SERVICE_FAILURE_BEHAVIOR,
                ("InterfaceFailure",), frozenset({f"{result_type.__name__}.REASONING_ERROR"}), (), frozenset(), "evolution_failure_projection")),
        )
        dependency_id = rid(RecordKind.DEPENDENCY_ENVIRONMENT, f"D_ev_{row_name}", namespace="evolution.environment")
        if isinstance(candidate.value, MigrationDeclaration):
            proper = frozenset({candidate_identity, candidate.value.source_environment,
                                candidate.value.target_environment, relation_identity})
        elif isinstance(candidate.value, CompatibilityClaim):
            proper = frozenset({candidate_identity, relation_identity,
                                *candidate.value.source_keys, *candidate.value.target_keys})
        else:
            proper = frozenset({candidate_identity, candidate.value.target_record_identity,
                                candidate.value.semantic_effect, candidate.value.payload})
        proper_closure = (proper | binding.value.dependency_closure
                          if isinstance(candidate.value, CompatibilityClaim)
                          else proper)
        validation_refs = frozenset({certificate_identity, validator_identity, evolution_root_id})
        dependency_record = LogicalRecord(dependency_id, DependencyEnvironment(
            frozenset({candidate_identity}), frozenset({candidate_identity}), frozenset(),
            frozenset({candidate_identity}), proper, proper_closure, validation_refs,
        ))
        descriptor_proper = frozenset({service_id, candidate_identity, *spec_ids.values()})
        evolution_capability = LogicalRecord(validator_identity, CapabilityDescriptor(
            validator_identity.key, service_id, ABI0,
            key("evolution-validator", "capknow.audit.evolution-validator", "plugin"),
            service_role,
            "COMPLETE_FOR_DECLARED_FRAGMENT", frozenset({judgment_name}),
            frozenset({target}), spec_ids[ContractRole.SOUND_FRAGMENT],
            spec_ids[ContractRole.COMPLETE_FRAGMENT], proper_closure, descriptor_proper,
            descriptor_proper, spec_ids[ContractRole.REQUIRED_EVIDENCE],
            frozenset({evolution_root_id}), spec_ids[ContractRole.SERVICE_FAILURE_BEHAVIOR],
        ))
        request_id = rid(RecordKind.REQUEST, f"R_{row_name}", namespace="evolution.request")
        request_record = LogicalRecord(request_id, request_type(
            ABI0, candidate_identity, environment.identity, evolution_trust_id,
            dependency_id, target, validator_identity,
        ))
        proof_id = rid(RecordKind.EVIDENCE, f"EVOLUTION_PROOF_{row_name}", owner="capknow.audit.evolution-proof", namespace="evolution.proof")
        evidence_id = rid(RecordKind.EVIDENCE, f"ER_{row_name}", owner="capknow.audit.evolution-proof", namespace="evolution.evidence")
        proof = LogicalRecord(proof_id, EvolutionProof(subject, candidate_identity, trust_target))
        evidence_item = LogicalRecord(evidence_id, EvidenceRecord(
            "capknow.audit.evolution-proof", "coding.evolution", row_name,
            spec_ids[ContractRole.REQUIRED_EVIDENCE],
        ))
        envelope = LogicalRecord(certificate_identity, CertificateEnvelope(
            certificate_identity.key, certificate_kind, request_id, (subject,),
            environment.identity, validator_identity, spec_ids[ContractRole.SOUND_FRAGMENT],
            dependency_id, conclusion, validator_identity, evolution_root_id,
            "SYMBOLIC", proof_id, frozenset({evidence_id}),
        ))
        admission_id = rid(RecordKind.OUTCOME, f"EADMIT_{row_name}", namespace="evolution.admission")
        result_id = rid(RecordKind.OUTCOME, f"ERESULT_{row_name}", namespace="evolution.result")
        evolution_services.append(evolution_service)
        evolution_specs.extend(row_specs)
        evolution_dependencies.append(dependency_record)
        evolution_capabilities.append(evolution_capability)
        evolution_requests.append(request_record)
        evolution_proofs.append(proof)
        evolution_evidence.append(evidence_item)
        evolution_envelopes.append(envelope)
        evolution_admissions.append(LogicalRecord(admission_id, CertificateAdmission(certificate_identity, conclusion)))
        evolution_results.append(LogicalRecord(result_id, result_type(conclusion)))
        for index, producer_name in enumerate((evo_owner, "capknow.semantic", "abi0")):
            evolution_producers.append(record(
                RecordKind.PRODUCER, f"producer.evolution.subject.{row_name}.{index}",
                ProducerRecord(candidate_identity, producer_name, "EVOLUTION_SUBJECT_PRODUCER"),
                namespace="evolution.producer",
            ))
        evolution_producers.extend((
            record(RecordKind.PRODUCER, f"producer.evolution.certificate.{row_name}",
                   ProducerRecord(certificate_identity, "capknow.audit.evolution-proof", "CERTIFICATE_OWNER"),
                   namespace="evolution.producer"),
            record(RecordKind.PRODUCER, f"producer.evolution.validator.{row_name}",
                   ProducerRecord(validator_identity, "capknow.audit.evolution-validator", "VALIDATOR_OWNER"),
                   namespace="evolution.producer"),
            record(RecordKind.PRODUCER, f"producer.evolution.service.{row_name}",
                   ProducerRecord(service_id, "capknow.audit.evolution-validator", "SERVICE_OWNER"),
                   namespace="evolution.producer"),
            record(RecordKind.PRODUCER, f"producer.evolution.proof.{row_name}",
                   ProducerRecord(proof_id, "capknow.audit.evolution-proof", "PROOF_OWNER"),
                   namespace="evolution.producer"),
            record(RecordKind.PRODUCER, f"producer.evolution.evidence.{row_name}",
                   ProducerRecord(evidence_id, "capknow.audit.evolution-proof", "EVIDENCE_OWNER"),
                   namespace="evolution.producer"),
        ))
    evolution_root = LogicalRecord(evolution_root_id, TrustRootRecord(
        evolution_root_id.key, "embedding-policy",
        frozenset(item.identity for item in evolution_capabilities),
        frozenset({"MIGRATION_RELATION_PROOF", "COMPATIBILITY_CLAIM_PROOF", "SEMANTIC_EXTENSION_VALIDATION"}),
        frozenset((*evolution_targets, *evolution_trust_targets)),
        "V0_EXTERNAL_TRUST_PREMISE",
    ))
    evolution_trust = LogicalRecord(evolution_trust_id, TrustEnvironment(
        evolution_policy_id, "embedding-policy",
        ((evolution_root_id, TrustRootJudgment(TrustState.ADMITTED, evolution_root.value)),),
    ))
    evolution_producers.append(record(
        RecordKind.PRODUCER, "producer.evolution.root",
        ProducerRecord(evolution_root_id, "embedding-policy", "TRUST_ROOT_OWNER"),
        namespace="evolution.producer",
    ))
    evolution_producers.extend((
        record(RecordKind.PRODUCER, "producer.evolution.policy",
               ProducerRecord(evolution_policy_id, "embedding-policy", "TRUST_POLICY_OWNER"),
               namespace="evolution.producer"),
        record(RecordKind.PRODUCER, "producer.evolution.trust_environment",
               ProducerRecord(evolution_trust_id, "embedding-policy", "TRUST_ENVIRONMENT_OWNER"),
               namespace="evolution.producer"),
    ))
    evolution_validator_package = _package(
        "evolution-validator", "capknow.audit.evolution-validator",
        specs=tuple(evolution_specs), services=tuple(evolution_capabilities),
    )
    evolution_proof_package = _package(
        "evolution-proof", "capknow.audit.evolution-proof",
        certificates=tuple(evolution_envelopes),
    )
    evolution_support = (
        environment,
        *(item for item in core.manifest
          if item.identity in {declaration.identity, binding.identity}
          or item.identity in binding.value.dependency_closure),
        migration_relation, compatibility_contract, extension_effect, extension_payload,
        evolution_policy, evolution_root, evolution_trust,
        evolution_validator_package, evolution_proof_package,
        *evolution_services, *evolution_specs, *evolution_dependencies,
        *evolution_requests, *evolution_proofs, *evolution_evidence,
        *evolution_admissions, *evolution_results,
        *evolution_producers,
    )
    evo_package = _package(
        "evolution-owner",
        evo_owner,
        others=(
            migration,
            compatibility,
            optional_extension,
            required_extension,
            optional_alias,
            required_alias,
        ),
    )
    evo_package_no_migration = replace(
        evo_package,
        value=replace(
            evo_package.value,
            migrations=(),
        ),
    )
    evo_package_no_compatibility = replace(
        evo_package,
        value=replace(
            evo_package.value,
            compatibility_claims=(),
        ),
    )
    evo_package_no_optional_extension = replace(
        evo_package,
        value=replace(
            evo_package.value,
            semantic_extensions=tuple(item for item in evo_package.value.semantic_extensions if item.identity != optional_extension_id),
        ),
    )
    evo_package_no_required_extension = replace(
        evo_package,
        value=replace(
            evo_package.value,
            semantic_extensions=tuple(item for item in evo_package.value.semantic_extensions if item.identity != required_extension_id),
        ),
    )
    evo_package_no_optional_alias = replace(
        evo_package,
        value=replace(
            evo_package.value,
            aliases=tuple(item for item in evo_package.value.aliases if item.identity != optional_alias_id),
        ),
    )
    evo_package_no_required_alias = replace(
        evo_package,
        value=replace(
            evo_package.value,
            aliases=tuple(item for item in evo_package.value.aliases if item.identity != required_alias_id),
        ),
    )

    wrong_sigma_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(PREDICATE_MEANING,task_accepts_wrong)",
        namespace="coding.contract",
    )
    wrong_sigma = LogicalRecord(
        wrong_sigma_id,
        replace(
            sigma_spec.value,
            contract_key=wrong_sigma_id.key,
            relation_name="task_accepts_wrong",
        ),
    )
    wrong_binding = replace(
        binding,
        value=replace(
            binding.value,
            meaning_contract=wrong_sigma_id,
            proper_semantic_dependencies=(binding.value.proper_semantic_dependencies - frozenset({sigma_spec.identity})) | frozenset({wrong_sigma_id}),
            dependency_closure=(binding.value.dependency_closure - frozenset({sigma_spec.identity})) | frozenset({wrong_sigma_id}),
        ),
    )
    wrong_model = replace(
        model, value=replace(model.value, semantic_contract=wrong_sigma_id)
    )
    package_wrong_sigma = replace(
        package,
        value=replace(
            package.value,
            bindings=tuple(
                wrong_binding if item.identity == binding.identity else item
                for item in package.value.bindings
            ),
            model_contracts=(wrong_model,),
        ),
    )
    wrong_sound_id = rid(
        RecordKind.CONTRACT_SPEC,
        "FSOUND",
        namespace="coding.service.contract",
    )
    wrong_sound = LogicalRecord(
        wrong_sound_id,
        replace(
            sound_spec.value,
            contract_key=wrong_sound_id.key,
            relation_name="function_sound_fragment",
        ),
    )
    wrong_capability = replace(
        capability,
        value=replace(capability.value, sound_fragment=wrong_sound_id),
    )
    package_wrong_service = replace(
        package,
        value=replace(
            package.value,
            services=tuple(
                wrong_capability if item.identity == capability.identity else item
                for item in package.value.services
            ),
        ),
    )

    no_result = replace(
        result,
        value=ResultRecord(request.identity, "InterfaceFailure", "NO_RESULT"),
    )
    empty_environment_id = rid(
        RecordKind.SEMANTIC_ENVIRONMENT, "E_t_empty", namespace="environment"
    )
    empty_environment = LogicalRecord(
        empty_environment_id, SemanticEnvironment(ABI0, (), (), ())
    )
    empty_dependency_id = rid(
        RecordKind.DEPENDENCY_ENVIRONMENT,
        "D_t_empty",
        namespace="environment",
    )
    empty_dependency = LogicalRecord(
        empty_dependency_id,
        DependencyEnvironment(frozenset(), frozenset(), frozenset(), frozenset(), frozenset(), frozenset(), frozenset()),
    )
    empty_request = replace(
        request,
        value=replace(
            request.value,
            semantic_environment=empty_environment_id,
            dependency_environment=empty_dependency_id,
        ),
    )
    absent_trust_id = rid(
        RecordKind.TRUST_ENVIRONMENT, "T_absent", namespace="trust"
    )
    absent_trust = LogicalRecord(
        absent_trust_id, TrustEnvironment(policy.identity, "embedding-policy", ())
    )
    no_trust_request = replace(
        request,
        value=replace(request.value, trust_environment=absent_trust_id),
    )
    incomplete_dependency_id = rid(
        RecordKind.DEPENDENCY_ENVIRONMENT,
        "D_t_incomplete",
        namespace="environment",
    )
    incomplete_dependency = LogicalRecord(
        incomplete_dependency_id,
        DependencyEnvironment(
            frozenset({declaration.identity}),
            frozenset({binding.identity}),
            frozenset({(declaration.identity, binding.identity)}),
            frozenset({declaration.identity, binding.identity}),
            frozenset(), frozenset(), frozenset(),
        ),
    )
    incomplete_request = replace(
        request,
        value=replace(
            request.value, dependency_environment=incomplete_dependency_id
        ),
    )

    observation_id = rid(
        RecordKind.OBSERVATION_ENVIRONMENT,
        "M_c",
        namespace="confluence.result",
    )
    n_o = rid(RecordKind.BINDING, "DF(observe)", namespace="coding.binding")
    n_d = rid(
        RecordKind.BINDING,
        "DF(changes_between)",
        namespace="coding.binding",
    )
    observation = LogicalRecord(
        observation_id,
        ObservationEnvironment(((n_o, "V_o"), (n_d, "V_d"))),
    )
    observation_missing_id = rid(
        RecordKind.OBSERVATION_ENVIRONMENT,
        "M_c_missing",
        namespace="confluence.result",
    )
    observation_missing = LogicalRecord(
        observation_missing_id, ObservationEnvironment(((n_o, "V_o"),))
    )
    reasoning_request_id = rid(
        RecordKind.REQUEST, "R_c", namespace="confluence.request"
    )
    reasoning_request = LogicalRecord(
        reasoning_request_id,
        InvocationRequest(
            declaration.identity,
            environment.identity,
            dependency.identity,
            trust.identity,
            V1,
            ("C_c",),
        ),
    )
    reasoning_result_id = rid(
        RecordKind.RESULT, "Y_c", namespace="confluence.result"
    )
    reasoning_result = LogicalRecord(
        reasoning_result_id,
        ResultRecord(reasoning_request_id, "ReasoningResult", "INCONCLUSIVE"),
    )
    malformed_reasoning_result = replace(
        reasoning_result,
        value=ResultRecord(
            reasoning_request_id, "InterfaceFailure", "SEMANTIC_MISMATCH"
        ),
    )
    lifecycle_id = rid(
        RecordKind.LIFECYCLE, "L_c_final", namespace="confluence.lifecycle"
    )
    lifecycle = LogicalRecord(
        lifecycle_id, LifecycleRecord(reasoning_request_id, "COMPLETED(Y_c)")
    )
    lifecycle_after_id = rid(
        RecordKind.LIFECYCLE,
        "L_life_after",
        namespace="confluence.lifecycle",
    )
    lifecycle_after = LogicalRecord(
        lifecycle_after_id,
        LifecycleRecord(reasoning_request_id, "INVOCABLE_FOR(R_c_alt)"),
    )

    event_value = record(
        RecordKind.EVENT_VALUE,
        "ev0",
        EventValueRecord(EventValue(
            EventKind.DEPENDENCY_REFRESH,
            DependencyRefreshEventPayload(
                ArtifactSelector(SelectorTag.ROLE, role=ArtifactRole.DEPENDENCY_LOCK),
                SnapshotIdentity(core.snapshot),
            ),
        )),
        namespace="event.value",
    )
    trace_event = record(
        RecordKind.TRACE_EVENT,
        "te0",
        TraceEventRecord(TraceEvent(event_value.value.event_value, "user")),
        namespace="event.trace",
    )
    source = record(
        RecordKind.SOURCE,
        "SRC(choice,1)",
        SourceRecord(
            "capknow.semantic", "coding.authority", "choice:1",
            frozenset({"AUTHENTICATED_BY(capknow.semantic)",
                       "CLAUSE_LOCAL_IDENTITY(choice:1)"})),
        namespace="authority.source",
    )
    authority_ref = record(
        RecordKind.AUTHORITY_REF,
        "AUTH(choice,1)",
        AuthorityRefRecord("capknow.semantic", "choice-controller", "STORAGE_SELECTION"),
        namespace="authority.ref",
    )
    evidence_record = record(
        RecordKind.EVIDENCE,
        "e0",
        EvidenceRecord("capknow.semantic", "coding.verification", "missing-matrix-record", core.sigma_spec),
        namespace="evidence",
    )
    evidence_subject = record(
        RecordKind.OUTCOME,
        "t_t_evidence_subject",
        OutcomeRecord("TASK_EVIDENCE_SUBJECT", frozenset(), frozenset({evidence_record.identity})),
        namespace="evidence",
    )
    evidence_subject_without_record = replace(
        evidence_subject,
        # The failed coordinate is still consumed by the outcome carrier; the
        # authoritative evidence record alone is absent from the variant.
        value=OutcomeRecord("TASK_EVIDENCE_SUBJECT", frozenset(), frozenset({evidence_record.identity})),
    )
    reason = record(
        RecordKind.REASON,
        "u0",
        ReasonRecord("UnknownReason", "capknow.semantic", "coding.missing-matrix", "DP(task_accepts)"),
        namespace="reason",
    )
    reason_carrier = record(
        RecordKind.OUTCOME,
        "VALUE(UNKNOWN)",
        OutcomeRecord("UNKNOWN_VALUE", None, frozenset({reason.identity})),
        namespace="reason",
    )
    reason_carrier_without_reason = replace(
        reason_carrier,
        # As above, retain the exact missing reference rather than erasing the
        # consumer edge that makes this a reason-carrier failure.
        value=OutcomeRecord("UNKNOWN_VALUE", None, frozenset({reason.identity})),
    )
    conflict = record(
        RecordKind.CONFLICT,
        "conflict0",
        ConflictRecord("PREDICATE_FACET_CONFLICT", frozenset({declaration.identity})),
        namespace="conflict",
    )
    conflict_replacement = record(
        RecordKind.CONFLICT,
        "conflict1",
        ConflictRecord("PREDICATE_FACET_CONFLICT", frozenset({declaration.identity})),
        namespace="conflict",
    )

    package_support = frozenset(
        item for item in core.manifest
        if item.identity.kind in {RecordKind.CONTRACT_SPEC, RecordKind.SERVICE}
    )
    package_manifest = frozenset((package, *package.value.members())) | package_support
    package_no_declaration_manifest = frozenset(
        (package_no_declaration, *package_no_declaration.value.members())
    ) | package_support
    package_no_event_manifest = frozenset(
        (package_no_event, *package_no_event.value.members())
    ) | package_support
    package_no_binding_manifest = frozenset(
        (package_no_binding, *package_no_binding.value.members())
    ) | package_support
    package_no_profile_manifest = frozenset(
        (package_no_profile, *package_no_profile.value.members())
    ) | package_support
    package_no_service_manifest = frozenset(
        (package_no_service, *package_no_service.value.members())
    ) | (package_support - frozenset({service}))
    package_no_capability_manifest = frozenset(
        (package_no_capability, *package_no_capability.value.members())
    ) | package_support
    package_no_model_manifest = frozenset(
        (package_no_model, *package_no_model.value.members())
    ) | package_support
    all_pair_package_members = frozenset(
        member
        for package_record in pair.manifest
        if isinstance(package_record.value, PluginPackage)
        for member in package_record.value.members()
    )
    pair_support = frozenset(
        item for item in pair.manifest
        if not isinstance(item.value, PluginPackage)
        and item not in all_pair_package_members
    )
    pair_package_manifest = frozenset(
        (pair_package, *pair_package.value.members())
    ) | pair_support
    pair_package_no_declaration_manifest = frozenset(
        (
            pair_package_no_declaration,
            *pair_package_no_declaration.value.members(),
        )
    ) | pair_support
    pair_package_no_binding_manifest = frozenset(
        (pair_package_no_binding, *pair_package_no_binding.value.members())
    ) | pair_support
    authority_package_manifest = frozenset(
        (authority_package, *authority_package.value.members())
    )
    authority_package_no_fact_manifest = frozenset(
        (authority_package_no_fact, *authority_package_no_fact.value.members())
    )
    proof_package_manifest = frozenset(
        (proof_package, *proof_package.value.members())
    )
    proof_package_no_certificate_manifest = frozenset(
        (
            proof_package_no_certificate,
            *proof_package_no_certificate.value.members(),
        )
    )
    evo_support_manifest = frozenset((
        *evolution_support, *evolution_capabilities, *evolution_envelopes,
    ))
    evo_manifest = frozenset((evo_package, *evo_package.value.members())) | evo_support_manifest
    evo_no_migration_manifest = frozenset(
        (evo_package_no_migration, *evo_package_no_migration.value.members())
    ) | evo_support_manifest
    evo_no_compatibility_manifest = frozenset(
        (
            evo_package_no_compatibility,
            *evo_package_no_compatibility.value.members(),
        )
    ) | evo_support_manifest
    evo_no_optional_extension_manifest = frozenset(
        (
            evo_package_no_optional_extension,
            *evo_package_no_optional_extension.value.members(),
        )
    ) | evo_support_manifest
    evo_no_required_extension_manifest = frozenset(
        (
            evo_package_no_required_extension,
            *evo_package_no_required_extension.value.members(),
        )
    ) | evo_support_manifest
    evo_no_optional_alias_manifest = frozenset(
        (
            evo_package_no_optional_alias,
            *evo_package_no_optional_alias.value.members(),
        )
    ) | evo_support_manifest
    evo_no_required_alias_manifest = frozenset(
        (
            evo_package_no_required_alias,
            *evo_package_no_required_alias.value.members(),
        )
    ) | evo_support_manifest
    wrong_sigma_manifest = frozenset(
        (package_wrong_sigma, *package_wrong_sigma.value.members())
    ) | (package_support - frozenset({sigma_spec})) | frozenset({wrong_sigma})
    wrong_service_manifest = frozenset(
        (package_wrong_service, *package_wrong_service.value.members())
    ) | (package_support - frozenset({sound_spec})) | frozenset({wrong_sound})

    formation_package = ResolutionCoordinate(
        ResolutionRelation.FORMATION_RECORD, package.identity
    )
    formation_pair_package = ResolutionCoordinate(
        ResolutionRelation.FORMATION_RECORD, pair_package.identity
    )
    formation_abi = ResolutionCoordinate(
        ResolutionRelation.FORMATION_RECORD, abi.identity
    )

    rows = (
        LiteralMissingRow(
            MissingRowId.ABI,
            abi.identity,
            (abi, package),
            (package,),
            frozenset({abi}) | package_manifest,
            package_manifest,
            frozenset({abi}),
            frozenset(),
            formation_package,
            formation_package,
            (package.identity,),
            (package.identity,),
            Judgment("MALFORMED"),
        ),
        LiteralMissingRow(
            MissingRowId.PLUGIN,
            package.identity,
            (abi, package),
            (abi,),
            frozenset({abi}) | package_manifest,
            frozenset({abi}),
            package_manifest,
            frozenset(),
            formation_abi,
            formation_abi,
            (abi.identity,),
            (abi.identity,),
            Judgment("MALFORMED"),
        ),
        LiteralMissingRow(
            MissingRowId.DECLARATION,
            declaration.identity,
            (abi, package),
            (abi, package_no_declaration),
            frozenset({abi}) | package_manifest,
            frozenset({abi}) | package_no_declaration_manifest,
            package_manifest - package_no_declaration_manifest,
            package_no_declaration_manifest - package_manifest,
            formation_package,
            ResolutionCoordinate(
                ResolutionRelation.FORMATION_RECORD,
                package_no_declaration.identity,
            ),
            (abi.identity, package.identity),
            (abi.identity, package_no_declaration.identity),
            Judgment("MALFORMED"),
            package.identity,
            package_no_declaration.identity,
        ),
        LiteralMissingRow(
            MissingRowId.SYMBOL,
            declaration.identity,
            (abi, package),
            (abi, package_no_declaration),
            frozenset({abi}) | package_manifest,
            frozenset({abi}) | package_no_declaration_manifest,
            package_manifest - package_no_declaration_manifest,
            package_no_declaration_manifest - package_manifest,
            formation_package,
            ResolutionCoordinate(
                ResolutionRelation.FORMATION_RECORD,
                package_no_declaration.identity,
            ),
            (abi.identity, package.identity),
            (abi.identity, package_no_declaration.identity),
            Judgment("MALFORMED"),
            package.identity,
            package_no_declaration.identity,
        ),
        LiteralMissingRow(
            MissingRowId.EVENT,
            event.identity,
            (abi, package),
            (abi, package_no_event),
            frozenset({abi}) | package_manifest,
            frozenset({abi}) | package_no_event_manifest,
            package_manifest - package_no_event_manifest,
            package_no_event_manifest - package_manifest,
            formation_package,
            ResolutionCoordinate(
                ResolutionRelation.FORMATION_RECORD, package_no_event.identity
            ),
            (abi.identity, package.identity),
            (abi.identity, package_no_event.identity),
            Judgment("MALFORMED"),
            package.identity,
            package_no_event.identity,
        ),
        LiteralMissingRow(
            MissingRowId.PAIR_DECLARATION,
            pair_declaration.identity,
            (abi, pair_package),
            (abi, pair_package_no_declaration),
            frozenset({abi}) | pair_package_manifest,
            frozenset({abi}) | pair_package_no_declaration_manifest,
            pair_package_manifest - pair_package_no_declaration_manifest,
            pair_package_no_declaration_manifest - pair_package_manifest,
            formation_pair_package,
            ResolutionCoordinate(
                ResolutionRelation.FORMATION_RECORD,
                pair_package_no_declaration.identity,
            ),
            (abi.identity, pair_package.identity),
            (abi.identity, pair_package_no_declaration.identity),
            Judgment("MALFORMED"),
            pair_package.identity,
            pair_package_no_declaration.identity,
        ),
        LiteralMissingRow(
            MissingRowId.OUTCOME,
            outcome.identity,
            (abi, outcome),
            (abi,),
            frozenset({abi, outcome}),
            frozenset({abi}),
            frozenset({outcome}),
            frozenset(),
            formation_abi,
            formation_abi,
            (abi.identity,),
            (abi.identity,),
            Judgment("MALFORMED"),
        ),
        LiteralMissingRow(
            MissingRowId.BINDING,
            binding.identity,
            (abi, package),
            (abi, package_no_binding),
            frozenset({abi}) | package_manifest,
            frozenset({abi}) | package_no_binding_manifest,
            package_manifest - package_no_binding_manifest,
            package_no_binding_manifest - package_manifest,
            ResolutionCoordinate(
                ResolutionRelation.BINDING_MEMBER, package.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.BINDING_MEMBER, package_no_binding.identity
            ),
            (abi.identity, package.identity),
            (abi.identity, package_no_binding.identity),
            Judgment("OPEN_BINDINGS"),
            package.identity,
            package_no_binding.identity,
        ),
        LiteralMissingRow(
            MissingRowId.PROFILE_BINDING,
            profile.identity,
            (abi, package),
            (abi, package_no_profile),
            frozenset({abi}) | package_manifest,
            frozenset({abi}) | package_no_profile_manifest,
            package_manifest - package_no_profile_manifest,
            package_no_profile_manifest - package_manifest,
            ResolutionCoordinate(
                ResolutionRelation.BINDING_MEMBER, package.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.BINDING_MEMBER, package_no_profile.identity
            ),
            (abi.identity, package.identity),
            (abi.identity, package_no_profile.identity),
            Judgment("OPEN_BINDINGS"),
            package.identity,
            package_no_profile.identity,
        ),
        LiteralMissingRow(
            MissingRowId.PAIR_BINDING,
            pair_binding.identity,
            (abi, pair_package),
            (abi, pair_package_no_binding),
            frozenset({abi}) | pair_package_manifest,
            frozenset({abi}) | pair_package_no_binding_manifest,
            pair_package_manifest - pair_package_no_binding_manifest,
            pair_package_no_binding_manifest - pair_package_manifest,
            ResolutionCoordinate(
                ResolutionRelation.BINDING_MEMBER, pair_package.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.BINDING_MEMBER,
                pair_package_no_binding.identity,
            ),
            (abi.identity, pair_package.identity),
            (abi.identity, pair_package_no_binding.identity),
            Judgment("OPEN_BINDINGS"),
            pair_package.identity,
            pair_package_no_binding.identity,
        ),
        LiteralMissingRow(
            MissingRowId.AUTHORITY_FACT,
            authority.identity,
            (abi, authority_package, choice_environment),
            (abi, authority_package_no_fact, choice_environment_no_fact),
            frozenset({abi, choice_environment}) | authority_package_manifest,
            frozenset({abi, choice_environment_no_fact})
            | authority_package_no_fact_manifest,
            (frozenset({choice_environment}) | authority_package_manifest)
            - (
                frozenset({choice_environment_no_fact})
                | authority_package_no_fact_manifest
            ),
            (
                frozenset({choice_environment_no_fact})
                | authority_package_no_fact_manifest
            )
            - (frozenset({choice_environment}) | authority_package_manifest),
            ResolutionCoordinate(
                ResolutionRelation.AUTHORITY_MEMBER,
                choice_environment.identity,
            ),
            ResolutionCoordinate(
                ResolutionRelation.AUTHORITY_MEMBER,
                choice_environment_no_fact.identity,
            ),
            (abi.identity, authority_package.identity, choice_environment.identity),
            (
                abi.identity,
                authority_package_no_fact.identity,
                choice_environment_no_fact.identity,
            ),
            Judgment("OPEN_BINDINGS", (authority.identity,)),
            authority_package.identity,
            authority_package_no_fact.identity,
        ),
        LiteralMissingRow(
            MissingRowId.CHOICE_BINDING,
            choice.identity,
            (abi, authority, choice, choice_environment),
            (abi, authority, choice_environment_no_binding),
            frozenset({abi, authority, choice, choice_environment}),
            frozenset({abi, authority, choice_environment_no_binding}),
            frozenset({choice, choice_environment}),
            frozenset({choice_environment_no_binding}),
            ResolutionCoordinate(
                ResolutionRelation.CHOICE_MEMBER, choice_environment.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.CHOICE_MEMBER,
                choice_environment_no_binding.identity,
            ),
            (abi.identity, choice_environment.identity),
            (abi.identity, choice_environment_no_binding.identity),
            Judgment("OPEN_BINDINGS", (choice.identity,)),
        ),
        LiteralMissingRow(
            MissingRowId.LEXICAL_BINDING,
            lexical.identity,
            (
                abi,
                lexical,
                lexical_environment,
                lexical_dependency,
                lexical_request,
            ),
            (
                abi,
                lexical_environment_no_binding,
                lexical_dependency_no_binding,
                lexical_request,
            ),
            frozenset(
                {
                    abi,
                    lexical,
                    lexical_environment,
                    lexical_dependency,
                    lexical_request,
                }
            ),
            frozenset(
                {
                    abi,
                    lexical_environment_no_binding,
                    lexical_dependency_no_binding,
                    lexical_request,
                }
            ),
            frozenset({lexical, lexical_environment, lexical_dependency}),
            frozenset(
                {lexical_environment_no_binding, lexical_dependency_no_binding}
            ),
            ResolutionCoordinate(
                ResolutionRelation.LEXICAL_MEMBER, lexical_environment.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.LEXICAL_MEMBER,
                lexical_environment_no_binding.identity,
            ),
            (abi.identity, lexical_environment.identity, lexical_request.identity),
            (
                abi.identity,
                lexical_environment_no_binding.identity,
                lexical_request.identity,
            ),
            Judgment("OPEN_BINDINGS", (lexical.identity,)),
        ),
        LiteralMissingRow(
            MissingRowId.EXTRANEOUS_LEXICAL_BINDING,
            request.identity,
            (abi, package, environment, dependency, trust, request),
            (
                abi,
                package,
                extra_lexical,
                extra_environment,
                extra_dependency,
                trust,
                extra_request,
            ),
            frozenset({abi, environment, dependency, trust, request})
            | package_manifest,
            frozenset(
                {
                    abi,
                    extra_lexical,
                    extra_environment,
                    extra_dependency,
                    trust,
                    extra_request,
                }
            )
            | package_manifest,
            frozenset({environment, dependency, request}),
            frozenset(
                {extra_lexical, extra_environment, extra_dependency, extra_request}
            ),
            ResolutionCoordinate(
                ResolutionRelation.EXTRANEOUS_LEXICAL, environment.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.EXTRANEOUS_LEXICAL,
                extra_environment.identity,
            ),
            (abi.identity, package.identity, environment.identity, request.identity),
            (
                abi.identity,
                package.identity,
                extra_environment.identity,
                extra_request.identity,
            ),
            Judgment(
                "MALFORMED_REQUEST",
                ("EXTRANEOUS_LEXICAL_BINDING", extra_lexical.identity),
            ),
        ),
        LiteralMissingRow(
            MissingRowId.SERVICE,
            service.identity,
            (abi, package, environment, dependency, trust, request),
            (abi, package_no_service, environment, dependency, trust, request),
            frozenset({abi, environment, dependency, trust, request})
            | package_manifest,
            frozenset({abi, environment, dependency, trust, request})
            | package_no_service_manifest,
            package_manifest - package_no_service_manifest,
            package_no_service_manifest - package_manifest,
            ResolutionCoordinate(
                ResolutionRelation.SERVICE_DISCOVERY, request.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.SERVICE_DISCOVERY, request.identity
            ),
            (abi.identity, package.identity, request.identity),
            (abi.identity, package_no_service.identity, request.identity),
            Judgment("EVALUABILITY_MISSING"),
            package.identity,
            package_no_service.identity,
        ),
        LiteralMissingRow(
            MissingRowId.CAPABILITY,
            capability.identity,
            (abi, package, environment, dependency, trust, request),
            (
                abi,
                package_no_capability,
                environment,
                dependency,
                trust,
                request,
            ),
            frozenset({abi, environment, dependency, trust, request})
            | package_manifest,
            frozenset({abi, environment, dependency, trust, request})
            | package_no_capability_manifest,
            package_manifest - package_no_capability_manifest,
            package_no_capability_manifest - package_manifest,
            ResolutionCoordinate(
                ResolutionRelation.SERVICE_DISCOVERY, request.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.SERVICE_DISCOVERY, request.identity
            ),
            (abi.identity, package.identity, request.identity),
            (abi.identity, package_no_capability.identity, request.identity),
            Judgment("EVALUABILITY_MISSING"),
            package.identity,
            package_no_capability.identity,
        ),
        LiteralMissingRow(
            MissingRowId.TRUST_POLICY,
            policy.identity,
            (abi, policy, trust),
            (abi, trust),
            frozenset({abi, policy, trust}),
            frozenset({abi, trust}),
            frozenset({policy}),
            frozenset(),
            ResolutionCoordinate(
                ResolutionRelation.TRUST_POLICY, trust.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.TRUST_POLICY, trust.identity
            ),
            (abi.identity, trust.identity),
            (abi.identity, trust.identity),
            Judgment("TRUST_ROOT_ABSENT"),
        ),
        LiteralMissingRow(
            MissingRowId.TRUST_ROOT,
            root.identity,
            (abi, policy, root, trust),
            (abi, policy, root_missing_environment),
            frozenset({abi, policy, root, trust}),
            frozenset({abi, policy, root_missing_environment}),
            frozenset({root, trust}),
            frozenset({root_missing_environment}),
            ResolutionCoordinate(
                ResolutionRelation.TRUST_ROOT, trust.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.TRUST_ROOT, root_missing_environment.identity
            ),
            (abi.identity, trust.identity),
            (abi.identity, root_missing_environment.identity),
            Judgment("TRUST_ROOT_ABSENT", (root.identity,)),
        ),
        LiteralMissingRow(
            MissingRowId.CERTIFICATE,
            pair_certificate.identity,
            pair.universe.records,
            pair_variant_records,
            pair.manifest,
            pair_variant_manifest,
            frozenset({proof_package, pair_certificate}),
            frozenset({proof_package_no_certificate}),
            ResolutionCoordinate(
                ResolutionRelation.CERTIFICATE_ADMISSION,
                pair_request.identity,
            ),
            ResolutionCoordinate(
                ResolutionRelation.CERTIFICATE_ADMISSION,
                pair_request.identity,
            ),
            (
                pair_request.identity,
                proof_package.identity,
                pair_binding.identity,
            ),
            (
                pair_request.identity,
                proof_package_no_certificate.identity,
                pair_binding.identity,
            ),
            Judgment(
                "NO_CERTIFICATE_ADMISSION", ("CONSISTENCY_UNKNOWN",)
            ),
            proof_package.identity,
            proof_package_no_certificate.identity,
        ),
        LiteralMissingRow(
            MissingRowId.MIGRATION,
            migration.identity,
            (abi, evo_package, compatibility, *evolution_support),
            (abi, evo_package_no_migration, compatibility, *evolution_support),
            frozenset({abi, compatibility}) | evo_manifest,
            frozenset({abi, compatibility}) | evo_no_migration_manifest,
            evo_manifest - evo_no_migration_manifest,
            evo_no_migration_manifest - evo_manifest,
            ResolutionCoordinate(
                ResolutionRelation.MIGRATION, compatibility.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.MIGRATION, compatibility.identity
            ),
            (abi.identity, evo_package.identity, compatibility.identity),
            (
                abi.identity,
                evo_package_no_migration.identity,
                compatibility.identity,
            ),
            Judgment("NO_MIGRATION", ("MK0",)),
            evo_package.identity,
            evo_package_no_migration.identity,
        ),
        LiteralMissingRow(
            MissingRowId.COMPATIBILITY_CLAIM,
            compatibility.identity,
            (abi, evo_package, required_extension, *evolution_support),
            (abi, evo_package_no_compatibility, required_extension, *evolution_support),
            frozenset({abi, required_extension}) | evo_manifest,
            frozenset({abi, required_extension})
            | evo_no_compatibility_manifest,
            evo_manifest - evo_no_compatibility_manifest,
            evo_no_compatibility_manifest - evo_manifest,
            ResolutionCoordinate(
                ResolutionRelation.COMPATIBILITY, required_extension.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.COMPATIBILITY, required_extension.identity
            ),
            (abi.identity, evo_package.identity, required_extension.identity),
            (
                abi.identity,
                evo_package_no_compatibility.identity,
                required_extension.identity,
            ),
            Judgment("NO_COMPATIBILITY", ("CCK0",)),
            evo_package.identity,
            evo_package_no_compatibility.identity,
        ),
        LiteralMissingRow(
            MissingRowId.EXTENSION_OPTIONAL,
            optional_extension.identity,
            (abi, evo_package, *evolution_support),
            (abi, evo_package_no_optional_extension, *evolution_support),
            frozenset({abi}) | evo_manifest,
            frozenset({abi}) | evo_no_optional_extension_manifest,
            evo_manifest - evo_no_optional_extension_manifest,
            evo_no_optional_extension_manifest - evo_manifest,
            ResolutionCoordinate(
                ResolutionRelation.OPTIONAL_EXTENSION,
                optional_alias.identity,
            ),
            ResolutionCoordinate(
                ResolutionRelation.OPTIONAL_EXTENSION,
                optional_alias.identity,
            ),
            (abi.identity, evo_package.identity, optional_alias.identity),
            (
                abi.identity,
                evo_package_no_optional_extension.identity,
                optional_alias.identity,
            ),
            Judgment("NO_EFFECT", ("XK0",)),
            evo_package.identity,
            evo_package_no_optional_extension.identity,
        ),
        LiteralMissingRow(
            MissingRowId.EXTENSION_REQUIRED,
            required_extension.identity,
            (abi, evo_package, *evolution_support),
            (abi, evo_package_no_required_extension, *evolution_support),
            frozenset({abi}) | evo_manifest,
            frozenset({abi}) | evo_no_required_extension_manifest,
            evo_manifest - evo_no_required_extension_manifest,
            evo_no_required_extension_manifest - evo_manifest,
            ResolutionCoordinate(
                ResolutionRelation.REQUIRED_EXTENSION,
                required_alias.identity,
            ),
            ResolutionCoordinate(
                ResolutionRelation.REQUIRED_EXTENSION,
                required_alias.identity,
            ),
            (abi.identity, evo_package.identity, required_alias.identity),
            (
                abi.identity,
                evo_package_no_required_extension.identity,
                required_alias.identity,
            ),
            Judgment("INCOMPATIBLE", ("XK1",)),
            evo_package.identity,
            evo_package_no_required_extension.identity,
        ),
        LiteralMissingRow(
            MissingRowId.MODEL_CONTRACT,
            model.identity,
            (abi, package),
            (abi, package_no_model),
            frozenset({abi}) | package_manifest,
            frozenset({abi}) | package_no_model_manifest,
            package_manifest - package_no_model_manifest,
            package_no_model_manifest - package_manifest,
            ResolutionCoordinate(
                ResolutionRelation.MODEL_BINDING, package.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.MODEL_BINDING, package_no_model.identity
            ),
            (abi.identity, package.identity),
            (abi.identity, package_no_model.identity),
            Judgment("OPEN_BINDINGS", ("MODEL_CONTRACT",)),
            package.identity,
            package_no_model.identity,
        ),
        LiteralMissingRow(
            MissingRowId.ALIAS_OPTIONAL,
            optional_alias.identity,
            (abi, evo_package, optional_extension, *evolution_support),
            (abi, evo_package_no_optional_alias, optional_extension, *evolution_support),
            frozenset({abi, optional_extension}) | evo_manifest,
            frozenset({abi, optional_extension}) | evo_no_optional_alias_manifest,
            evo_manifest - evo_no_optional_alias_manifest,
            evo_no_optional_alias_manifest - evo_manifest,
            ResolutionCoordinate(
                ResolutionRelation.OPTIONAL_ALIAS, optional_extension.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.OPTIONAL_ALIAS, optional_extension.identity
            ),
            (abi.identity, evo_package.identity, optional_extension.identity),
            (
                abi.identity,
                evo_package_no_optional_alias.identity,
                optional_extension.identity,
            ),
            Judgment("NO_ALIAS", ("AK0",)),
            evo_package.identity,
            evo_package_no_optional_alias.identity,
        ),
        LiteralMissingRow(
            MissingRowId.ALIAS_REQUIRED,
            required_alias.identity,
            (abi, evo_package, required_extension, *evolution_support),
            (abi, evo_package_no_required_alias, required_extension, *evolution_support),
            frozenset({abi, required_extension}) | evo_manifest,
            frozenset({abi, required_extension}) | evo_no_required_alias_manifest,
            evo_manifest - evo_no_required_alias_manifest,
            evo_no_required_alias_manifest - evo_manifest,
            ResolutionCoordinate(
                ResolutionRelation.REQUIRED_ALIAS, required_extension.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.REQUIRED_ALIAS, required_extension.identity
            ),
            (abi.identity, evo_package.identity, required_extension.identity),
            (
                abi.identity,
                evo_package_no_required_alias.identity,
                required_extension.identity,
            ),
            Judgment("MALFORMED", ("MISSING_ALIAS", "AK1")),
            evo_package.identity,
            evo_package_no_required_alias.identity,
        ),
        LiteralMissingRow(
            MissingRowId.SIGMA_CONTRACT_SPEC,
            sigma_spec.identity,
            (abi, package),
            (abi, package_wrong_sigma),
            frozenset({abi}) | package_manifest,
            frozenset({abi}) | wrong_sigma_manifest,
            package_manifest - wrong_sigma_manifest,
            wrong_sigma_manifest - package_manifest,
            ResolutionCoordinate(
                ResolutionRelation.SIGMA_CONTRACT, binding.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.SIGMA_CONTRACT, wrong_binding.identity
            ),
            (abi.identity, package.identity, binding.identity),
            (abi.identity, package_wrong_sigma.identity, wrong_binding.identity),
            Judgment("BINDING_INCOMPATIBLE", ("OPEN_BINDINGS",)),
            package.identity,
            package_wrong_sigma.identity,
        ),
        LiteralMissingRow(
            MissingRowId.SERVICE_CONTRACT_SPEC,
            sound_spec.identity,
            (abi, package),
            (abi, package_wrong_service),
            frozenset({abi}) | package_manifest,
            frozenset({abi}) | wrong_service_manifest,
            package_manifest - wrong_service_manifest,
            wrong_service_manifest - package_manifest,
            ResolutionCoordinate(
                ResolutionRelation.SERVICE_CONTRACT, capability.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.SERVICE_CONTRACT, wrong_capability.identity
            ),
            (abi.identity, package.identity, capability.identity),
            (
                abi.identity,
                package_wrong_service.identity,
                wrong_capability.identity,
            ),
            Judgment(
                "CAPABILITY_INCOMPATIBLE", ("EVALUABILITY_MISSING",)
            ),
            package.identity,
            package_wrong_service.identity,
        ),
        LiteralMissingRow(
            MissingRowId.REQUEST,
            request.identity,
            (abi, request, result),
            (abi, no_result),
            frozenset({abi, request, result}),
            frozenset({abi, no_result}),
            frozenset({request, result}),
            frozenset({no_result}),
            ResolutionCoordinate(
                ResolutionRelation.REQUEST_RECORD, result.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.REQUEST_RECORD, no_result.identity
            ),
            (abi.identity, result.identity),
            (abi.identity, no_result.identity),
            Judgment("MALFORMED_REQUEST"),
        ),
        LiteralMissingRow(
            MissingRowId.RESULT,
            result.identity,
            (abi, request, result),
            (abi, request),
            frozenset({abi, request, result}),
            frozenset({abi, request}),
            frozenset({result}),
            frozenset(),
            ResolutionCoordinate(
                ResolutionRelation.RESULT_PROTOCOL, request.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.RESULT_PROTOCOL, request.identity
            ),
            (abi.identity, request.identity),
            (abi.identity, request.identity),
            Judgment(
                "INVOCATION_FAILED", ("PROTOCOL", "NO_RESULT", "NO_TRUTH")
            ),
        ),
        LiteralMissingRow(
            MissingRowId.SEMANTIC_ENVIRONMENT,
            environment.identity,
            (abi, environment, dependency, request, result),
            (abi, empty_environment, empty_dependency, empty_request, result),
            frozenset({abi, environment, dependency, request, result}),
            frozenset(
                {abi, empty_environment, empty_dependency, empty_request, result}
            ),
            frozenset({environment, dependency, request}),
            frozenset({empty_environment, empty_dependency, empty_request}),
            ResolutionCoordinate(
                ResolutionRelation.REQUEST_ENVIRONMENT, request.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.REQUEST_ENVIRONMENT, empty_request.identity
            ),
            (abi.identity, request.identity),
            (abi.identity, empty_request.identity),
            Judgment("MALFORMED_REQUEST", (request.identity,)),
        ),
        LiteralMissingRow(
            MissingRowId.TRUST_ENVIRONMENT,
            trust.identity,
            (abi, trust, request, result),
            (abi, absent_trust, no_trust_request, result),
            frozenset({abi, trust, request, result}),
            frozenset({abi, absent_trust, no_trust_request, result}),
            frozenset({trust, request}),
            frozenset({absent_trust, no_trust_request}),
            ResolutionCoordinate(
                ResolutionRelation.REQUEST_ENVIRONMENT, request.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.REQUEST_ENVIRONMENT,
                no_trust_request.identity,
            ),
            (abi.identity, request.identity),
            (abi.identity, no_trust_request.identity),
            Judgment("MALFORMED_REQUEST", (request.identity,)),
        ),
        LiteralMissingRow(
            MissingRowId.DEPENDENCY_ENVIRONMENT,
            dependency.identity,
            (abi, dependency, request, result),
            (abi, incomplete_dependency, incomplete_request, result),
            frozenset({abi, dependency, request, result}),
            frozenset({abi, incomplete_dependency, incomplete_request, result}),
            frozenset({dependency, request}),
            frozenset({incomplete_dependency, incomplete_request}),
            ResolutionCoordinate(
                ResolutionRelation.REQUEST_ENVIRONMENT, request.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.REQUEST_ENVIRONMENT,
                incomplete_request.identity,
            ),
            (abi.identity, request.identity),
            (abi.identity, incomplete_request.identity),
            Judgment("MALFORMED_REQUEST", (request.identity,)),
        ),
        LiteralMissingRow(
            MissingRowId.OBSERVATION_ENVIRONMENT,
            observation.identity,
            (abi, reasoning_request, observation, reasoning_result, lifecycle),
            (
                abi,
                reasoning_request,
                observation_missing,
                malformed_reasoning_result,
                lifecycle,
            ),
            frozenset(
                {abi, reasoning_request, observation, reasoning_result, lifecycle}
            ),
            frozenset(
                {
                    abi,
                    reasoning_request,
                    observation_missing,
                    malformed_reasoning_result,
                    lifecycle,
                }
            ),
            frozenset({observation, reasoning_result}),
            frozenset({observation_missing, malformed_reasoning_result}),
            ResolutionCoordinate(
                ResolutionRelation.OBSERVATION_RESULT,
                reasoning_result.identity,
            ),
            ResolutionCoordinate(
                ResolutionRelation.OBSERVATION_RESULT,
                malformed_reasoning_result.identity,
            ),
            (abi.identity, reasoning_result.identity),
            (abi.identity, malformed_reasoning_result.identity),
            Judgment("MALFORMED_RESULT", ("SEMANTIC_MISMATCH",)),
        ),
        LiteralMissingRow(
            MissingRowId.LIFECYCLE,
            lifecycle.identity,
            (abi, reasoning_request, lifecycle),
            (abi, reasoning_request, lifecycle_after),
            frozenset({abi, reasoning_request, lifecycle}),
            frozenset({abi, reasoning_request, lifecycle_after}),
            frozenset({lifecycle}),
            frozenset({lifecycle_after}),
            ResolutionCoordinate(
                ResolutionRelation.LIFECYCLE_TRANSITION,
                replacement=lifecycle_after.identity,
            ),
            ResolutionCoordinate(
                ResolutionRelation.LIFECYCLE_TRANSITION,
                replacement=lifecycle_after.identity,
            ),
            (abi.identity, lifecycle.identity),
            (abi.identity, lifecycle_after.identity),
            Judgment(
                "LIFECYCLE_REPLACED",
                (lifecycle_after.identity, "INVOCABLE_FOR"),
            ),
        ),
        LiteralMissingRow(
            MissingRowId.EVENT_VALUE,
            event_value.identity,
            (abi, event, event_value, trace_event),
            (abi, event),
            frozenset({abi, event, event_value, trace_event}),
            frozenset({abi, event}),
            frozenset({event_value, trace_event}),
            frozenset(),
            formation_abi,
            formation_abi,
            (abi.identity,),
            (abi.identity,),
            Judgment("MALFORMED"),
        ),
        LiteralMissingRow(
            MissingRowId.TRACE_EVENT,
            trace_event.identity,
            (abi, event_value, trace_event),
            (abi, event_value),
            frozenset({abi, event_value, trace_event}),
            frozenset({abi, event_value}),
            frozenset({trace_event}),
            frozenset(),
            formation_abi,
            formation_abi,
            (abi.identity,),
            (abi.identity,),
            Judgment("MALFORMED"),
        ),
        LiteralMissingRow(
            MissingRowId.SOURCE,
            source.identity,
            (abi, source),
            (abi,),
            frozenset({abi, source}),
            frozenset({abi}),
            frozenset({source}),
            frozenset(),
            formation_abi,
            formation_abi,
            (abi.identity,),
            (abi.identity,),
            Judgment("MALFORMED"),
        ),
        LiteralMissingRow(
            MissingRowId.AUTHORITY_REF,
            authority_ref.identity,
            (abi, authority_ref),
            (abi,),
            frozenset({abi, authority_ref}),
            frozenset({abi}),
            frozenset({authority_ref}),
            frozenset(),
            formation_abi,
            formation_abi,
            (abi.identity,),
            (abi.identity,),
            Judgment("MALFORMED"),
        ),
        LiteralMissingRow(
            MissingRowId.EVIDENCE,
            evidence_record.identity,
            (abi, evidence_record, evidence_subject),
            (abi, evidence_subject_without_record),
            frozenset({abi, evidence_record, evidence_subject}),
            frozenset({abi, evidence_subject_without_record}),
            frozenset({evidence_record}),
            frozenset(),
            ResolutionCoordinate(
                ResolutionRelation.EVIDENCE_TRUTH, evidence_subject.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.EVIDENCE_TRUTH,
                evidence_subject_without_record.identity,
            ),
            (abi.identity, evidence_subject.identity),
            (abi.identity, evidence_subject_without_record.identity),
            Judgment("TRUTH_UNKNOWN"),
        ),
        LiteralMissingRow(
            MissingRowId.REASON,
            reason.identity,
            (abi, reason, reason_carrier),
            (abi, reason_carrier_without_reason),
            frozenset({abi, reason, reason_carrier}),
            frozenset({abi, reason_carrier_without_reason}),
            frozenset({reason}),
            frozenset(),
            ResolutionCoordinate(
                ResolutionRelation.REASON_CARRIER, reason_carrier.identity
            ),
            ResolutionCoordinate(
                ResolutionRelation.REASON_CARRIER,
                reason_carrier_without_reason.identity,
            ),
            (abi.identity, reason_carrier.identity),
            (abi.identity, reason_carrier_without_reason.identity),
            Judgment("MALFORMED_RESULT", ("MALFORMED_CARRIER",)),
        ),
        LiteralMissingRow(
            MissingRowId.CONFLICT,
            conflict.identity,
            (abi, declaration, conflict),
            (abi, declaration, conflict_replacement),
            frozenset({abi, declaration, conflict}),
            frozenset({abi, declaration, conflict_replacement}),
            frozenset({conflict}),
            frozenset({conflict_replacement}),
            ResolutionCoordinate(
                ResolutionRelation.CONFLICT_REPLACEMENT,
                replacement=conflict_replacement.identity,
            ),
            ResolutionCoordinate(
                ResolutionRelation.CONFLICT_REPLACEMENT,
                replacement=conflict_replacement.identity,
            ),
            (abi.identity, conflict.identity),
            (abi.identity, conflict_replacement.identity),
            Judgment(
                "CONFLICT_REPLACED",
                (conflict_replacement.identity, "MALFORMED"),
            ),
        ),
    )
    if len(rows) != 42 or {item.row for item in rows} != set(MissingRowId):
        raise AssertionError("literal missing-row tuple must be exactly exhaustive")
    # Every tagged universe carries its complete literal record presentation;
    # package membership is never treated as an implicit ContractSpec or
    # request/carrier closure.
    return tuple(
        replace(
            row,
            baseline_records=tuple(sorted(row.baseline_manifest, key=lambda item: item.identity)),
            variant_records=tuple(sorted(row.variant_manifest, key=lambda item: item.identity)),
        )
        for row in rows
    )


MISSING_EXPECTED_LITERAL = {
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
    MissingRowId.AUTHORITY_FACT: Judgment(
        "OPEN_BINDINGS",
        (("AUTHORITY_FACT_RECORD", "capknow.semantic", "authority", "AF(choice,1)", (1,)),),
    ),
    MissingRowId.CHOICE_BINDING: Judgment(
        "OPEN_BINDINGS",
        (("CHOICE_BINDING_RECORD", "capknow.semantic", "authority.choice", "cb0", (1,)),),
    ),
    MissingRowId.LEXICAL_BINDING: Judgment(
        "OPEN_BINDINGS",
        (("LEXICAL_BINDING_RECORD", "capknow.semantic", "lexical", "lk0", (1,)),),
    ),
    MissingRowId.EXTRANEOUS_LEXICAL_BINDING: Judgment(
        "MALFORMED_REQUEST",
        ("EXTRANEOUS_LEXICAL_BINDING", (
            "LEXICAL_BINDING_RECORD", "capknow.semantic", "lexical", "lk_extra", (1,)
        )),
    ),
    MissingRowId.SERVICE: Judgment("EVALUABILITY_MISSING"),
    MissingRowId.CAPABILITY: Judgment("EVALUABILITY_MISSING"),
    MissingRowId.TRUST_POLICY: Judgment("TRUST_ROOT_ABSENT"),
    MissingRowId.TRUST_ROOT: Judgment(
        "TRUST_ROOT_ABSENT",
        (("TRUST_ROOT_RECORD", "capknow.semantic", "trust", "TR", (1,)),),
    ),
    MissingRowId.CERTIFICATE: Judgment(
        "NO_CERTIFICATE_ADMISSION", ("CONSISTENCY_UNKNOWN",)
    ),
    MissingRowId.MIGRATION: Judgment("NO_MIGRATION", ("MK0",)),
    MissingRowId.COMPATIBILITY_CLAIM: Judgment("NO_COMPATIBILITY", ("CCK0",)),
    MissingRowId.EXTENSION_OPTIONAL: Judgment("NO_EFFECT", ("XK0",)),
    MissingRowId.EXTENSION_REQUIRED: Judgment("INCOMPATIBLE", ("XK1",)),
    MissingRowId.MODEL_CONTRACT: Judgment("OPEN_BINDINGS", ("MODEL_CONTRACT",)),
    MissingRowId.ALIAS_OPTIONAL: Judgment("NO_ALIAS", ("AK0",)),
    MissingRowId.ALIAS_REQUIRED: Judgment("MALFORMED", ("MISSING_ALIAS", "AK1")),
    MissingRowId.SIGMA_CONTRACT_SPEC: Judgment(
        "BINDING_INCOMPATIBLE", ("OPEN_BINDINGS",)
    ),
    MissingRowId.SERVICE_CONTRACT_SPEC: Judgment(
        "CAPABILITY_INCOMPATIBLE", ("EVALUABILITY_MISSING",)
    ),
    MissingRowId.REQUEST: Judgment("MALFORMED_REQUEST"),
    MissingRowId.RESULT: Judgment(
        "INVOCATION_FAILED", ("PROTOCOL", "NO_RESULT", "NO_TRUTH")
    ),
    MissingRowId.SEMANTIC_ENVIRONMENT: Judgment(
        "MALFORMED_REQUEST",
        (("REQUEST_RECORD", "capknow.semantic", "request", "Q_t[ADMITTED]", (1,)),),
    ),
    MissingRowId.TRUST_ENVIRONMENT: Judgment(
        "MALFORMED_REQUEST",
        (("REQUEST_RECORD", "capknow.semantic", "request", "Q_t[ADMITTED]", (1,)),),
    ),
    MissingRowId.DEPENDENCY_ENVIRONMENT: Judgment(
        "MALFORMED_REQUEST",
        (("REQUEST_RECORD", "capknow.semantic", "request", "Q_t[ADMITTED]", (1,)),),
    ),
    MissingRowId.OBSERVATION_ENVIRONMENT: Judgment(
        "MALFORMED_RESULT", ("SEMANTIC_MISMATCH",)
    ),
    MissingRowId.LIFECYCLE: Judgment(
        "LIFECYCLE_REPLACED",
        (("LIFECYCLE_RECORD", "capknow.semantic", "confluence.lifecycle", "L_life_after", (1,)), "INVOCABLE_FOR"),
    ),
    MissingRowId.EVENT_VALUE: Judgment("MALFORMED"),
    MissingRowId.TRACE_EVENT: Judgment("MALFORMED"),
    MissingRowId.SOURCE: Judgment("MALFORMED"),
    MissingRowId.AUTHORITY_REF: Judgment("MALFORMED"),
    MissingRowId.EVIDENCE: Judgment("TRUTH_UNKNOWN"),
    MissingRowId.REASON: Judgment(
        "MALFORMED_RESULT", ("MALFORMED_CARRIER",)
    ),
    MissingRowId.CONFLICT: Judgment(
        "CONFLICT_REPLACED",
        (("CONFLICT_RECORD", "capknow.semantic", "conflict", "conflict1", (1,)), "MALFORMED"),
    ),
}


def missing_construction(row: MissingRowId) -> MissingConstruction:
    spec = LITERAL_MISSING_BY_ID[row]
    baseline_request = LookupRequest(
        spec.target, spec.baseline_coordinate, spec.baseline_context
    )
    variant_request = LookupRequest(
        spec.target, spec.variant_coordinate, spec.variant_context
    )
    return MissingConstruction(
        row,
        spec.target,
        Universe(spec.baseline_records, baseline_request),
        Universe(spec.variant_records, variant_request),
        spec.baseline_manifest,
        spec.variant_manifest,
        spec.removed_records,
        spec.added_records,
        spec.baseline_container,
        spec.variant_container,
    )


@dataclass(frozen=True)
class ConfluenceConstruction:
    universe: Universe
    manifest: frozenset[LogicalRecord]
    node_one: RecordIdentity
    node_two: RecordIdentity


def _confluence_construction_local(order: OrderTag) -> ConfluenceConstruction:
    retained_core = _core_construction_local()
    retained_package = next(
        item for item in retained_core.manifest
        if item.identity == retained_core.package
    )
    assert isinstance(retained_package.value, PluginPackage)
    path = Path((PathSegment("dependency"), PathSegment("lock")))
    new_artifact = ArtifactContent(
        ArtifactTag.TEXT,
        ArtifactRole.DEPENDENCY_LOCK,
        Format.TEXT,
        ByteSize(150),
        ContentIdentity("lock_v1"),
    )
    old = RepositorySnapshot(())
    new = RepositorySnapshot(((path, new_artifact),))
    selector = ArtifactSelector(SelectorTag.PATHS, frozenset({path}))
    observed_spec = ObservationSpec(
        ObservationSpecTag.ARTIFACT_VIEW,
        selector,
        ArtifactProjection(ProjectionTag.CONTENT),
    )
    contract_id = rid(RecordKind.OUTCOME, "C_c", namespace="confluence.contract")
    source_one = record(
        RecordKind.SOURCE, "SRC(c,1)",
        SourceRecord("PLUGIN_ISSUER(APK)",
                     "AUTHENTICATED_FIXTURE_INSTRUCTION", "CODING_SOURCE(c,1)",
                     frozenset({"AUTHENTICATED_BY(APK)",
                                "CLAUSE_LOCAL_IDENTITY(coding.confluence.observation)"})),
        owner="PLUGIN_ISSUER(APK)", namespace="authenticated.fixture.source",
    )
    source_two = record(
        RecordKind.SOURCE, "SRC(c,2)",
        SourceRecord("PLUGIN_ISSUER(APK)",
                     "AUTHENTICATED_FIXTURE_INSTRUCTION", "CODING_SOURCE(c,2)",
                     frozenset({"AUTHENTICATED_BY(APK)",
                                "CLAUSE_LOCAL_IDENTITY(coding.confluence.change)"})),
        owner="PLUGIN_ISSUER(APK)", namespace="authenticated.fixture.source",
    )
    authority_one = record(
        RecordKind.AUTHORITY_REF, "AUTH(c,1)",
        AuthorityRefRecord(
            "PLUGIN_ISSUER(APK)", "coding.fixture", "CODING_AUTHORITY(c,1)"),
        owner="PLUGIN_ISSUER(APK)", namespace="coding.fixture",
    )
    authority_two = record(
        RecordKind.AUTHORITY_REF, "AUTH(c,2)",
        AuthorityRefRecord(
            "PLUGIN_ISSUER(APK)", "coding.fixture", "CODING_AUTHORITY(c,2)"),
        owner="PLUGIN_ISSUER(APK)", namespace="coding.fixture",
    )
    attestation_one = cp.AuthorityAttestationValue(
        authority_one.identity, source_one.identity, "fixture_principal", "REQUIRE",
        cp.AuthorityAttestationSubjectIdentity(
            cp.AuthoritySubjectTag.CLAUSE, contract_id,
            clause_tag=cp.AuthorityClauseTag.CONFLUENCE_OBSERVATION))
    attestation_two = cp.AuthorityAttestationValue(
        authority_two.identity, source_two.identity, "fixture_principal", "REQUIRE",
        cp.AuthorityAttestationSubjectIdentity(
            cp.AuthoritySubjectTag.CLAUSE, contract_id,
            clause_tag=cp.AuthorityClauseTag.CONFLUENCE_CHANGE))
    evidence_one = rid(RecordKind.EVIDENCE, "AUTHORITY_EVIDENCE_LOCAL(c,1)",
                       owner="PLUGIN_ISSUER(ATK)",
                       namespace="coding.authority.attestation")
    evidence_two = rid(RecordKind.EVIDENCE, "AUTHORITY_EVIDENCE_LOCAL(c,2)",
                       owner="PLUGIN_ISSUER(ATK)",
                       namespace="coding.authority.attestation")
    authority_fact_one = record(
        RecordKind.AUTHORITY_FACT, "AFB(c,1)",
        AuthorityFactRecord(
            key("AF(c,1)", namespace="confluence.authority.fact"),
            authority_one.identity, source_one.identity, "fixture_principal",
            attestation_one, frozenset({evidence_one})),
        namespace="confluence.authority.binding",
    )
    authority_fact_two = record(
        RecordKind.AUTHORITY_FACT, "AFB(c,2)",
        AuthorityFactRecord(
            key("AF(c,2)", namespace="confluence.authority.fact"),
            authority_two.identity, source_two.identity, "fixture_principal",
            attestation_two, frozenset({evidence_two})),
        namespace="confluence.authority.binding",
    )
    contract_value = ConfluenceContract(
        (
            AttributedClause(
                "coding.confluence.observation", source_one.identity,
                "REQUIRE(observations_equal(observe(s_c,F_c),O_c))"),
            AttributedClause(
                "coding.confluence.change", source_two.identity,
                "REQUIRE(dependency_metadata_changed(changes_between(P_c,F_c)))"),
        ),
        (
            ClauseAdoption(
                "coding.confluence.observation", authority_one.identity,
                "fixture_principal"),
            ClauseAdoption(
                "coding.confluence.change", authority_two.identity,
                "fixture_principal"),
        ),
    )
    contract = LogicalRecord(
        contract_id,
        OutcomeRecord(
            "CONTRACT_IDENTITY", contract_value,
            frozenset({
                source_one.identity, source_two.identity,
                authority_one.identity, authority_two.identity,
                authority_fact_one.identity, authority_fact_two.identity,
            }),
        ),
    )
    confluence_subject = ConfluenceSubject(contract_id, observed_spec, old, new)
    spec_one_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(CONFLUENCE,observe)",
        namespace="confluence.contract",
    )
    spec_two_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(CONFLUENCE,changes_between)",
        namespace="confluence.contract",
    )
    spec_one = LogicalRecord(
        spec_one_id,
        ContractSpec(
            spec_one_id.key,
            Layer.SIGMA,
            ContractRole.FUNCTION_MEANING,
            ("ObservationSpec", "RepositorySnapshot"),
            frozenset({"TermResult"}),
            (),
            frozenset(),
            "observe",
        ),
    )
    spec_two = LogicalRecord(
        spec_two_id,
        ContractSpec(
            spec_two_id.key,
            Layer.SIGMA,
            ContractRole.FUNCTION_MEANING,
            ("RepositorySnapshot", "RepositorySnapshot"),
            frozenset({"TermResult"}),
            (),
            frozenset(),
            "changes_between",
        ),
    )
    conf_evidence_id = rid(RecordKind.CONTRACT_SPEC, "CS(EVIDENCE_SCHEMA,none)", namespace="confluence.contract")
    conf_access_id = rid(RecordKind.CONTRACT_SPEC, "CS(ACCESS_BOUNDARY,snapshot_pair)", namespace="confluence.contract")
    conf_unknown_id = rid(RecordKind.CONTRACT_SPEC, "CS(UNKNOWN_BEHAVIOR,never)", namespace="confluence.contract")
    conf_error_id = rid(RecordKind.CONTRACT_SPEC, "CS(EVALUATION_ERROR_BEHAVIOR,term)", namespace="confluence.contract")
    conf_aux = (
        LogicalRecord(conf_evidence_id, ContractSpec(conf_evidence_id.key, Layer.SIGMA, ContractRole.EVIDENCE_SCHEMA, ("EvidenceStore",), frozenset({"EvidenceSet"}), (), frozenset(), "confluence_evidence")),
        LogicalRecord(conf_access_id, ContractSpec(conf_access_id.key, Layer.SIGMA, ContractRole.ACCESS_BOUNDARY, ("RepositorySnapshot",), frozenset({"ADMITTED", "INADMISSIBLE"}), (), frozenset(), "confluence_access")),
        LogicalRecord(conf_unknown_id, ContractSpec(conf_unknown_id.key, Layer.SIGMA, ContractRole.UNKNOWN_BEHAVIOR, ("UnknownReasonSet",), frozenset({"TermResult"}), (), frozenset(), "confluence_unknown")),
        LogicalRecord(conf_error_id, ContractSpec(conf_error_id.key, Layer.SIGMA, ContractRole.EVALUATION_ERROR_BEHAVIOR, ("FailureReasonSet",), frozenset({"TermResult"}), (), frozenset(), "confluence_error")),
    )
    observe_declaration_id = rid(
        RecordKind.DECLARATION, "DF(observe)", namespace="confluence.declaration"
    )
    changes_declaration_id = rid(
        RecordKind.DECLARATION, "DF(changes_between)", namespace="confluence.declaration"
    )
    observe_declaration = LogicalRecord(
        observe_declaration_id,
        DeclarationShape(
            observe_declaration_id.key,
            key("SF(observe)", namespace="confluence.symbol"),
            "FUNCTION",
            (key("ObservationSpec", namespace="carrier.type"), key("RepositorySnapshot", namespace="carrier.type")),
            "TERM_RESULT",
            (frozenset(), frozenset({"pre", "final"})),
            frozenset(),
        ),
    )
    changes_declaration = LogicalRecord(
        changes_declaration_id,
        DeclarationShape(
            changes_declaration_id.key,
            key("SF(changes_between)", namespace="confluence.symbol"),
            "FUNCTION",
            (key("RepositorySnapshot", namespace="carrier.type"), key("RepositorySnapshot", namespace="carrier.type")),
            "TERM_RESULT",
            (frozenset({"pre"}), frozenset({"final"})),
            frozenset(),
        ),
    )
    binding_one = record(
        RecordKind.BINDING,
        "BINDING(DF(observe))",
        SemanticBinding(
            rid(RecordKind.BINDING, "BINDING(DF(observe))", namespace="confluence.binding").key,
            observe_declaration_id,
            "FUNCTION",
            spec_one_id,
            observe_declaration.value.facet_positions,
            frozenset({observe_declaration_id, spec_one_id, conf_evidence_id, conf_access_id, conf_unknown_id, conf_error_id}),
            frozenset({observe_declaration_id, spec_one_id, conf_evidence_id, conf_access_id, conf_unknown_id, conf_error_id}),
            conf_evidence_id, conf_access_id, conf_unknown_id, conf_error_id,
            "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT",
        ),
        namespace="confluence.binding",
    )
    binding_two = record(
        RecordKind.BINDING,
        "BINDING(DF(changes_between))",
        SemanticBinding(
            rid(RecordKind.BINDING, "BINDING(DF(changes_between))", namespace="confluence.binding").key,
            changes_declaration_id,
            "FUNCTION",
            spec_two_id,
            changes_declaration.value.facet_positions,
            frozenset({changes_declaration_id, spec_two_id, conf_evidence_id, conf_access_id, conf_unknown_id, conf_error_id}),
            frozenset({changes_declaration_id, spec_two_id, conf_evidence_id, conf_access_id, conf_unknown_id, conf_error_id}),
            conf_evidence_id, conf_access_id, conf_unknown_id, conf_error_id,
            "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT",
        ),
        namespace="confluence.binding",
    )
    node_one_id = binding_one.identity
    node_two_id = binding_two.identity
    model_one_id = rid(RecordKind.MODEL_CONTRACT, "MODEL_observe_confluence", namespace="confluence.model")
    model_two_id = rid(RecordKind.MODEL_CONTRACT, "MODEL_changes_between_confluence", namespace="confluence.model")
    model_one = LogicalRecord(model_one_id, ModelContract(
        model_one_id.key, node_one_id, V1, observe_declaration.value.symbol_key,
        observe_declaration.value.argument_types, observe_declaration.value.result_kind,
        observe_declaration.value.facet_positions, conf_evidence_id, conf_unknown_id,
        conf_error_id, spec_one_id, frozenset(),
    ))
    model_two = LogicalRecord(model_two_id, ModelContract(
        model_two_id.key, node_two_id, V1, changes_declaration.value.symbol_key,
        changes_declaration.value.argument_types, changes_declaration.value.result_kind,
        changes_declaration.value.facet_positions, conf_evidence_id, conf_unknown_id,
        conf_error_id, spec_two_id, frozenset(),
    ))
    semantic_id = rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_c", namespace="confluence.environment")
    confluence_service_id = rid(RecordKind.SERVICE, "SK(confluence)", namespace="coding.service")
    confluence_capability_id = rid(RecordKind.CAPABILITY, "CAP(confluence)", namespace="coding.capability")
    csound_id = rid(RecordKind.CONTRACT_SPEC, "CSOUND", namespace="coding.service.contract")
    creq_id = rid(RecordKind.CONTRACT_SPEC, "CREQ", namespace="coding.service.contract")
    cfail_id = rid(RecordKind.CONTRACT_SPEC, "CFAIL", namespace="coding.service.contract")
    csound_queries = (
        ObservationQuery(node_one_id, ObservationKind.TERM_RESULT, ("observation_spec", "final_snapshot")),
        ObservationQuery(node_two_id, ObservationKind.TERM_RESULT, ("initial_snapshot", "final_snapshot")),
    )
    csound = LogicalRecord(csound_id, ContractSpec(
        csound_id.key, Layer.SERVICE, ContractRole.SOUND_FRAGMENT,
        ("ServiceAdmissionSubject",), frozenset({"IN_FRAGMENT", "OUTSIDE_FRAGMENT"}),
        csound_queries, frozenset({node_one_id, node_two_id}), "confluence_sound_fragment"))
    creq = LogicalRecord(creq_id, ContractSpec(
        creq_id.key, Layer.SERVICE, ContractRole.REQUIRED_EVIDENCE,
        ("ServiceAdmissionSubject", "EvidenceSet"), frozenset({"ADMISSIBLE", "INADMISSIBLE"}),
        (), frozenset(), "confluence_required_evidence"))
    cfail = LogicalRecord(cfail_id, ContractSpec(
        cfail_id.key, Layer.SERVICE, ContractRole.SERVICE_FAILURE_BEHAVIOR,
        ("InterfaceFailure",), frozenset({"REASONING_ERROR"}), (), frozenset(),
        "confluence_failure_projection"))
    confluence_service = LogicalRecord(confluence_service_id, ServiceIdentity(
        confluence_service_id.key, ABI0, key("coding-minimal", namespace="plugin")))
    confluence_proper = binding_one.value.proper_semantic_dependencies | binding_two.value.proper_semantic_dependencies
    confluence_closure = binding_one.value.dependency_closure | binding_two.value.dependency_closure
    confluence_root_id = rid(
        RecordKind.TRUST_ROOT, "ROOT_TR_c", namespace="confluence.trust")
    descriptor_proper = frozenset({
        confluence_service_id, csound_id, creq_id, cfail_id,
        confluence_root_id, semantic_id, contract_id}) | confluence_closure
    descriptor_closure = descriptor_proper | confluence_closure | frozenset({
        node_one_id, node_two_id,
    })
    confluence_capability = LogicalRecord(confluence_capability_id, CapabilityDescriptor(
        confluence_capability_id.key, confluence_service_id, ABI0,
        key("coding-minimal", namespace="plugin"), "REASONING",
        "PARTIAL_SYMBOLIC_REASONING", frozenset({"CONSISTENCY"}),
        frozenset({ReasoningTarget("CONSISTENCY", (confluence_subject,), semantic_id)}), csound_id, None,
        confluence_closure,
        descriptor_proper,
        descriptor_closure,
        creq_id, frozenset({rid(RecordKind.TRUST_ROOT, "ROOT_TR_c", namespace="confluence.trust")}), cfail_id))
    package = replace(retained_package, value=replace(
        retained_package.value,
        declarations=retained_package.value.declarations + (observe_declaration, changes_declaration),
        bindings=retained_package.value.bindings + (binding_one, binding_two),
        model_contracts=retained_package.value.model_contracts + (model_one, model_two),
        services=retained_package.value.services + (confluence_capability,),
    ))

    policy_id = rid(
        RecordKind.TRUST_POLICY, "TP", namespace="confluence.trust"
    )
    policy = LogicalRecord(
        policy_id, TrustPolicyRecord(policy_id.key, "embedding-policy")
    )
    root_id = rid(
        RecordKind.TRUST_ROOT, "ROOT_TR_c", namespace="confluence.trust"
    )
    capability_target = confluence_capability_id
    root = LogicalRecord(
        root_id,
        TrustRootRecord(
            root_id.key,
            "embedding-policy",
            frozenset({capability_target}),
            frozenset({"CONTRADICTION_PROOF"}),
            frozenset({ServiceUseTrustTarget(
                confluence_capability_id, "CONSISTENCY",
                EnvironmentUse("CONSISTENCY", (confluence_subject,)),
                semantic_id,
            )}),
            "V0_EXTERNAL_TRUST_PREMISE",
        ),
    )
    trust_id = rid(
        RecordKind.TRUST_ENVIRONMENT, "T_c", namespace="confluence.trust"
    )
    trust = LogicalRecord(
        trust_id,
        TrustEnvironment(
            policy_id, "embedding-policy",
            ((root_id, TrustRootJudgment(TrustState.ADMITTED, root.value)),)
        ),
    )
    semantic = LogicalRecord(
        semantic_id,
        SemanticEnvironment(
            ABI0,
            (observe_declaration_id, changes_declaration_id),
            (),
            (binding_one.identity, binding_two.identity),
            authority_facts=(authority_fact_one.identity, authority_fact_two.identity),
            mechanically_extracted_dependencies=frozen_confluence_syntax_roots(),
        ),
    )
    dependency_id = rid(
        RecordKind.DEPENDENCY_ENVIRONMENT,
        "D_c",
        namespace="confluence.environment",
    )
    abi_id = rid(
        RecordKind.ABI, "ABI0", namespace="abi", version=ABI0
    )
    dependency = LogicalRecord(
        dependency_id,
        DependencyEnvironment(
            frozen_confluence_syntax_roots(),
            frozenset({binding_one.identity, binding_two.identity}),
            frozenset({
                (observe_declaration_id, binding_one.identity),
                (changes_declaration_id, binding_two.identity),
            }),
            frozenset({observe_declaration_id, changes_declaration_id, binding_one.identity, binding_two.identity}),
            confluence_proper,
            confluence_closure,
            frozenset(),
        ),
    )
    request_id = rid(
        RecordKind.REQUEST, "R_c", namespace="confluence.request"
    )
    request_record = LogicalRecord(
        request_id,
        ReasoningRequest(
            ABI0, "CONSISTENCY", (confluence_subject,), semantic_id, trust_id,
            csound_id, dependency_id,
            ReasoningTarget("CONSISTENCY", (confluence_subject,), semantic_id),
            confluence_capability_id,
        ),
    )
    confluence_producers = tuple(
        record(
            RecordKind.PRODUCER, f"producer.confluence.subject.{index}",
            ProducerRecord(contract_id, producer, "REASONING_SUBJECT_PRODUCER"),
            namespace="confluence.producer",
        )
        for index, producer in enumerate((
            "capknow.semantic", "capknow.authority", "capknow.attestation",
            "capknow.validation", "embedding-authority-policy", "abi0",
        ))
    ) + (
        record(RecordKind.PRODUCER, "producer.confluence.capability",
               ProducerRecord(confluence_capability_id, "capknow.semantic", "CAPABILITY_OWNER"),
               namespace="confluence.producer"),
        record(RecordKind.PRODUCER, "producer.confluence.service",
               ProducerRecord(confluence_service_id, "capknow.semantic", "SERVICE_OWNER"),
               namespace="confluence.producer"),
        record(RecordKind.PRODUCER, "producer.confluence.root",
               ProducerRecord(root_id, "embedding-policy", "TRUST_ROOT_OWNER"),
               namespace="confluence.producer"),
        record(RecordKind.PRODUCER, "producer.confluence.policy",
               ProducerRecord(policy_id, "embedding-policy", "TRUST_POLICY_OWNER"),
               namespace="confluence.producer"),
        record(RecordKind.PRODUCER, "producer.confluence.trust_environment",
               ProducerRecord(trust_id, "embedding-policy", "TRUST_ENVIRONMENT_OWNER"),
               namespace="confluence.producer"),
    )
    observation = ObservationResult(
        ObservationResultTag.ARTIFACT,
        observed_spec,
        Coverage(CoverageTag.COMPLETE),
        (
            (
                path,
                ObservationValue(
                    ObservationValueTag.PRESENT_CONTENT, (new_artifact,)
                ),
            ),
        ),
    )
    changes = ChangeSet(((path, ChangeEntry(ChangeKind.CREATED, new=new_artifact)),))
    observations = tuple(
        sorted(
            (
                (node_one_id, TermResult(value=observation)),
                (node_two_id, TermResult(value=changes)),
            )
        )
    )
    observation_environment = record(
        RecordKind.OBSERVATION_ENVIRONMENT,
        "M_c",
        ObservationEnvironment(observations),
        namespace="confluence.result",
    )
    result_record = record(
        RecordKind.RESULT,
        "Y_c",
        ResultRecord(request_id, "ReasoningResult", ReasoningResultValue(
            "COMPLETED_INCONCLUSIVE",
            frozenset({ReasoningUnknown(
                "capknow.semantic", "coding.confluence", "fixture_inconclusive",
                (contract_id, observation_environment.identity),
            )}),
        )),
        namespace="confluence.result",
    )
    lifecycle_record = record(
        RecordKind.LIFECYCLE,
        "L_c_final",
        LifecycleRecord(request_id, "COMPLETED(Y_c)"),
        namespace="confluence.lifecycle",
    )
    status_record = record(
        RecordKind.OUTCOME,
        "K_c",
        OutcomeRecord(
            "CONFLUENCE_STATUS",
            (
                "WELL_FORMED",
                "CLOSED",
                "EVALUABILITY_AVAILABLE",
                "CONSISTENCY_UNKNOWN",
            ),
            frozenset(
                {
                    lifecycle_record.identity,
                    observation_environment.identity,
                    result_record.identity,
                }
            ),
        ),
        namespace="confluence.result",
    )
    abi = LogicalRecord(abi_id, AbiRecord(ABI0))
    preferred = (
        (node_one_id, node_two_id)
        if order is OrderTag.FORWARD
        else (node_two_id, node_one_id)
    )
    retained_support = tuple(
        item for item in retained_core.universe.records
        if item.identity not in {retained_core.abi, retained_core.package}
    )
    top_level = (
        abi,
        package,
        *retained_support,
        contract,
        source_one,
        source_two,
        authority_one,
        authority_two,
        authority_fact_one,
        authority_fact_two,
        observe_declaration,
        changes_declaration,
        spec_one,
        spec_two,
        model_one,
        model_two,
        *conf_aux,
        csound,
        creq,
        cfail,
        confluence_service,
        policy,
        root,
        trust,
        semantic,
        dependency,
        request_record,
        observation_environment,
        result_record,
        lifecycle_record,
        status_record,
        *confluence_producers,
    )
    manifest = frozenset(
        (
            abi,
            package,
            *retained_support,
            contract,
            source_one,
            source_two,
            authority_one,
            authority_two,
            authority_fact_one,
            authority_fact_two,
            observe_declaration,
            changes_declaration,
            binding_one,
            binding_two,
            spec_one,
            spec_two,
            model_one,
            model_two,
            *conf_aux,
            csound,
            creq,
            cfail,
            confluence_service,
            confluence_capability,
            policy,
            root,
            trust,
            semantic,
            dependency,
            request_record,
            observation_environment,
            result_record,
            lifecycle_record,
            status_record,
            *confluence_producers,
        )
    )
    return ConfluenceConstruction(
        Universe(
            top_level,
            GraphEvaluationRequest(
                (node_one_id, node_two_id), preferred,
                ((node_one_id, (observed_spec, new)), (node_two_id, (old, new))),
                request_id, trust_id,
                semantic_id, dependency_id, observation_environment.identity,
                result_record.identity, lifecycle_record.identity,
                status_record.identity,
            ),
        ),
        manifest,
        node_one_id,
        node_two_id,
    )


def _cycle_universe_local(cyclic: bool = True) -> Universe:
    retained_core = _core_construction_local()
    retained_package = next(
        item for item in retained_core.manifest
        if item.identity == retained_core.package
    )
    assert isinstance(retained_package.value, PluginPackage)
    cycle_type_dependencies = {
        "PathSegment": (),
        "Path": ("PathSegment",),
        "PathSet": ("Path",),
        "ArtifactRole": (),
        "Format": (),
        "ByteSize": (),
        "ContentIdentity": (),
        "FieldId": (),
        "FieldValue": (),
        "SubjectId": (),
        "BehaviorValue": ("ContentIdentity", "FieldId", "FieldValue"),
        "ArtifactContent": ("ArtifactRole", "Format", "ByteSize", "ContentIdentity", "FieldId", "FieldValue", "SubjectId", "BehaviorValue"),
        "RepositorySnapshot": ("Path", "ArtifactContent"),
        "SnapshotIdentity": ("RepositorySnapshot",),
        "ArtifactSelector": ("PathSet", "ArtifactRole"),
        "ArtifactProjection": ("FieldId",),
        "ObservationSpec": ("ArtifactSelector", "ArtifactProjection", "SubjectId", "FieldId"),
        "VerificationSpec": ("ObservationSpec",),
        "VerificationStatus": (),
        "ChangeKind": (),
        "CommandId": (),
        "ContactClass": (),
        "ReleaseId": (),
        "EventPattern": ("PathSet", "VerificationSpec", "VerificationStatus", "ChangeKind", "CommandId", "ContactClass", "ReleaseId", "SnapshotIdentity", "ArtifactSelector"),
    }
    cycle_types: dict[str, LogicalRecord] = {}
    cycle_admissions: dict[str, LogicalRecord] = {}
    for type_name, nested_names in cycle_type_dependencies.items():
        type_identity = rid(RecordKind.TYPE_DECLARATION, f"T({type_name})", namespace="coding.type")
        admission_identity = rid(RecordKind.CONTRACT_SPEC, f"CS(TYPE_ADMISSION,type.{type_name})", namespace="coding.type-admission")
        nested = frozenset(
            rid(RecordKind.TYPE_DECLARATION, f"T({name})", namespace="coding.type")
            for name in nested_names
        )
        admission = LogicalRecord(admission_identity, ContractSpec(
            admission_identity.key, Layer.DELTA, ContractRole.TYPE_ADMISSION,
            (type_name,), frozenset({"ADMITTED", "NOT_ADMITTED"}),
            tuple(ObservationQuery(item, ObservationKind.TYPE_ADMISSION_FACT, ("nested_value",)) for item in sorted(nested)),
            nested, f"admit_{type_name}", TypeAdmissionRelation(admission_type(type_name)),
        ))
        cycle_admissions[type_name] = admission
        cycle_types[type_name] = LogicalRecord(
            type_identity,
            TypeDeclaration(type_identity.key, admission.value, nested | frozenset({admission_identity})),
        )
    event_pattern_type = cycle_types["EventPattern"].identity
    first_spec_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(PREDICATE_MEANING,event_matches_cycle)",
        namespace="cycle.contract",
    )
    second_spec_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(PREDICATE_MEANING,event_occurred)",
        namespace="cycle.contract",
    )
    first_id = rid(
        RecordKind.BINDING,
        "BINDING(DP(event_matches))",
        namespace="cycle.binding",
    )
    second_id = rid(
        RecordKind.BINDING,
        "BINDING(DP(event_occurred))",
        namespace="cycle.binding",
    )
    first_query = ObservationQuery(
        second_id,
        ObservationKind.EVAL_RESULT,
        ("pattern", "singleton_trace(event)"),
    )
    second_query = ObservationQuery(
        first_id,
        ObservationKind.EVAL_RESULT_SEQUENCE,
        ("pattern", "trace"),
    )
    first_spec = LogicalRecord(
        first_spec_id,
        ContractSpec(
            first_spec_id.key,
            Layer.SIGMA,
            ContractRole.PREDICATE_MEANING,
            ("EventPattern", "EventValue"),
            frozenset({"Eval"}),
            (first_query,) if cyclic else (),
            frozenset({second_id}) if cyclic else frozenset(),
            "event_matches_cycle" if cyclic else "event_matches",
        ),
    )
    second_spec = LogicalRecord(
        second_spec_id,
        ContractSpec(
            second_spec_id.key,
            Layer.SIGMA,
            ContractRole.PREDICATE_MEANING,
            ("EventPattern", "Trace"),
            frozenset({"Eval"}),
            (second_query,),
            frozenset({first_id}),
            "event_occurred",
        ),
    )
    first_decl_id = rid(
        RecordKind.DECLARATION, "DP(event_matches)", namespace="cycle"
    )
    second_decl_id = rid(
        RecordKind.DECLARATION, "DP(event_occurred)", namespace="cycle"
    )
    first_decl = LogicalRecord(
        first_decl_id,
        DeclarationShape(
            first_decl_id.key,
            key("SP(event_matches)", namespace="cycle.symbol"),
            "PREDICATE",
            (event_pattern_type.key, key("EventValue", namespace="carrier.type")),
            "BOOL",
            (frozenset(), frozenset()),
            frozenset({event_pattern_type}),
        ),
    )
    second_decl = LogicalRecord(
        second_decl_id,
        DeclarationShape(
            second_decl_id.key,
            key("SP(event_occurred)", namespace="cycle.symbol"),
            "PREDICATE",
            (event_pattern_type.key, key("Trace", namespace="carrier.type")),
            "BOOL",
            (frozenset(), frozenset({"trace"})),
            frozenset({event_pattern_type}),
        ),
    )
    cycle_evidence_id = rid(RecordKind.CONTRACT_SPEC, "CS(EVIDENCE_SCHEMA,none)", namespace="cycle.contract")
    cycle_access_id = rid(RecordKind.CONTRACT_SPEC, "CS(ACCESS_BOUNDARY,pattern_trace)", namespace="cycle.contract")
    cycle_unknown_id = rid(RecordKind.CONTRACT_SPEC, "CS(UNKNOWN_BEHAVIOR,never)", namespace="cycle.contract")
    cycle_error_id = rid(RecordKind.CONTRACT_SPEC, "CS(EVALUATION_ERROR_BEHAVIOR,predicate)", namespace="cycle.contract")
    cycle_aux = (
        LogicalRecord(cycle_evidence_id, ContractSpec(cycle_evidence_id.key, Layer.SIGMA, ContractRole.EVIDENCE_SCHEMA, ("EvidenceStore",), frozenset({"EvidenceSet"}), (), frozenset(), "cycle_evidence")),
        LogicalRecord(cycle_access_id, ContractSpec(cycle_access_id.key, Layer.SIGMA, ContractRole.ACCESS_BOUNDARY, ("EventPattern", "Trace"), frozenset({"ADMITTED", "INADMISSIBLE"}), (), frozenset(), "cycle_access")),
        LogicalRecord(cycle_unknown_id, ContractSpec(cycle_unknown_id.key, Layer.SIGMA, ContractRole.UNKNOWN_BEHAVIOR, ("UnknownReasonSet",), frozenset({"Eval"}), (), frozenset(), "cycle_unknown")),
        LogicalRecord(cycle_error_id, ContractSpec(cycle_error_id.key, Layer.SIGMA, ContractRole.EVALUATION_ERROR_BEHAVIOR, ("FailureReasonSet",), frozenset({"Eval"}), (), frozenset(), "cycle_error")),
    )
    first_direct = frozenset({first_decl_id, first_spec_id, cycle_evidence_id, cycle_access_id, cycle_unknown_id, cycle_error_id}) | (frozenset({second_id}) if cyclic else frozenset())
    second_direct = frozenset({second_decl_id, second_spec_id, cycle_evidence_id, cycle_access_id, cycle_unknown_id, cycle_error_id, first_id})
    type_closure = frozenset(
        item.identity for item in (*cycle_types.values(), *cycle_admissions.values())
    )
    first_closure = first_direct | type_closure | (second_direct | frozenset({first_id, second_id}) if cyclic else frozenset())
    second_closure = second_direct | first_direct | type_closure | frozenset({first_id}) | (frozenset({second_id}) if cyclic else frozenset())
    first = LogicalRecord(
        first_id,
        SemanticBinding(
            first_id.key,
            first_decl_id,
            "PREDICATE",
            first_spec_id,
            (frozenset(), frozenset()), first_direct, first_closure,
            cycle_evidence_id, cycle_access_id, cycle_unknown_id, cycle_error_id,
            "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT",
        ),
    )
    second = LogicalRecord(
        second_id,
        SemanticBinding(
            second_id.key,
            second_decl_id,
            "PREDICATE",
            second_spec_id,
            (frozenset(), frozenset({"trace"})), second_direct, second_closure,
            cycle_evidence_id, cycle_access_id, cycle_unknown_id, cycle_error_id,
            "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT",
        ),
    )
    first_model_id = rid(RecordKind.MODEL_CONTRACT, "MODEL_event_matches_cycle", namespace="cycle.model")
    second_model_id = rid(RecordKind.MODEL_CONTRACT, "MODEL_event_occurred", namespace="cycle.model")
    first_model = LogicalRecord(first_model_id, ModelContract(
        first_model_id.key, first_id, V1, first_decl.value.symbol_key,
        first_decl.value.argument_types, first_decl.value.result_kind,
        first_decl.value.facet_positions, cycle_evidence_id, cycle_unknown_id,
        cycle_error_id, first_spec_id, frozenset(),
    ))
    second_model = LogicalRecord(second_model_id, ModelContract(
        second_model_id.key, second_id, V1, second_decl.value.symbol_key,
        second_decl.value.argument_types, second_decl.value.result_kind,
        second_decl.value.facet_positions, cycle_evidence_id, cycle_unknown_id,
        cycle_error_id, second_spec_id, frozenset(),
    ))
    snapshot_decl_id = rid(RecordKind.DECLARATION, "DF(snapshot_of)", namespace="cycle")
    changes_decl_id = rid(RecordKind.DECLARATION, "DF(changes_between)", namespace="cycle")
    observe_decl_id = rid(RecordKind.DECLARATION, "DF(observe)", namespace="cycle")
    snapshot_decl = LogicalRecord(snapshot_decl_id, DeclarationShape(
        snapshot_decl_id.key, key("SF(snapshot_of)", namespace="cycle.symbol"),
        "FUNCTION", (key("State", namespace="carrier.type"),), "TERM_RESULT",
        (frozenset({"pre", "final"}),), frozenset(),
    ))
    changes_decl = LogicalRecord(changes_decl_id, DeclarationShape(
        changes_decl_id.key, key("SF(changes_between)", namespace="cycle.symbol"),
        "FUNCTION", (cycle_types["RepositorySnapshot"].identity.key,) * 2,
        "TERM_RESULT", (frozenset({"pre"}), frozenset({"final"})),
        frozenset({cycle_types["RepositorySnapshot"].identity}),
    ))
    observe_decl = LogicalRecord(observe_decl_id, DeclarationShape(
        observe_decl_id.key, key("SF(observe)", namespace="cycle.symbol"),
        "FUNCTION", (cycle_types["ObservationSpec"].identity.key,
                     cycle_types["RepositorySnapshot"].identity.key),
        "TERM_RESULT", (frozenset(), frozenset({"pre", "final"})),
        frozenset({cycle_types["ObservationSpec"].identity,
                   cycle_types["RepositorySnapshot"].identity}),
    ))
    snapshot_spec_id = rid(RecordKind.CONTRACT_SPEC, "CS(FUNCTION_MEANING,snapshot_of)", namespace="cycle.contract")
    changes_spec_id = rid(RecordKind.CONTRACT_SPEC, "CS(FUNCTION_MEANING,changes_between)", namespace="cycle.contract")
    observe_spec_id = rid(RecordKind.CONTRACT_SPEC, "CS(FUNCTION_MEANING,observe)", namespace="cycle.contract")
    snapshot_spec = LogicalRecord(snapshot_spec_id, ContractSpec(
        snapshot_spec_id.key, Layer.SIGMA, ContractRole.FUNCTION_MEANING,
        ("State",), frozenset({"TermResult"}),
        (ObservationQuery(cycle_admissions["RepositorySnapshot"].identity,
                          ObservationKind.TYPE_ADMISSION_FACT, ("state",)),),
        frozenset({cycle_admissions["RepositorySnapshot"].identity}), "snapshot_of",
    ))
    changes_spec = LogicalRecord(changes_spec_id, ContractSpec(
        changes_spec_id.key, Layer.SIGMA, ContractRole.FUNCTION_MEANING,
        ("RepositorySnapshot", "RepositorySnapshot"), frozenset({"TermResult"}),
        (), frozenset(), "changes_between",
    ))
    observe_spec = LogicalRecord(observe_spec_id, ContractSpec(
        observe_spec_id.key, Layer.SIGMA, ContractRole.FUNCTION_MEANING,
        ("ObservationSpec", "RepositorySnapshot"), frozenset({"TermResult"}),
        (), frozenset(), "observe",
    ))
    snapshot_access_id = rid(RecordKind.CONTRACT_SPEC, "CS(ACCESS_BOUNDARY,state_only)", namespace="cycle.contract")
    changes_access_id = rid(RecordKind.CONTRACT_SPEC, "CS(ACCESS_BOUNDARY,snapshot_pair)", namespace="cycle.contract")
    observe_access_id = rid(RecordKind.CONTRACT_SPEC, "CS(ACCESS_BOUNDARY,observe)", namespace="cycle.contract")
    function_access_specs = (
        LogicalRecord(snapshot_access_id, ContractSpec(snapshot_access_id.key, Layer.SIGMA, ContractRole.ACCESS_BOUNDARY, ("State",), frozenset({"ADMITTED", "INADMISSIBLE"}), (), frozenset(), "state_only")),
        LogicalRecord(changes_access_id, ContractSpec(changes_access_id.key, Layer.SIGMA, ContractRole.ACCESS_BOUNDARY, ("RepositorySnapshot", "RepositorySnapshot"), frozenset({"ADMITTED", "INADMISSIBLE"}), (), frozenset(), "snapshot_pair")),
        LogicalRecord(observe_access_id, ContractSpec(observe_access_id.key, Layer.SIGMA, ContractRole.ACCESS_BOUNDARY, ("ObservationSpec", "RepositorySnapshot"), frozenset({"ADMITTED", "INADMISSIBLE"}), (), frozenset(), "observe")),
    )
    snapshot_id = rid(RecordKind.BINDING, "BINDING(DF(snapshot_of))", namespace="cycle.binding")
    changes_id = rid(RecordKind.BINDING, "BINDING(DF(changes_between))", namespace="cycle.binding")
    observe_id = rid(RecordKind.BINDING, "BINDING(DF(observe))", namespace="cycle.binding")
    function_rows = (
        (snapshot_id, snapshot_decl, snapshot_spec, snapshot_access_id),
        (changes_id, changes_decl, changes_spec, changes_access_id),
        (observe_id, observe_decl, observe_spec, observe_access_id),
    )
    function_bindings: list[LogicalRecord] = []
    function_models: list[LogicalRecord] = []
    for binding_id, declaration_record, spec_record, access_identity in function_rows:
        direct = frozenset({declaration_record.identity, spec_record.identity,
                            cycle_evidence_id, access_identity, cycle_unknown_id,
                            cycle_error_id})
        closure = direct | declaration_record.value.proper_type_dependencies | spec_record.value.support
        binding_record = LogicalRecord(binding_id, SemanticBinding(
            binding_id.key, declaration_record.identity, "FUNCTION", spec_record.identity,
            declaration_record.value.facet_positions, direct, closure,
            cycle_evidence_id, access_identity, cycle_unknown_id, cycle_error_id,
            "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT",
        ))
        model_id = rid(RecordKind.MODEL_CONTRACT,
                       f"MODEL_{binding_id.key.local[11:-2]}_cycle", namespace="cycle.model")
        function_bindings.append(binding_record)
        function_models.append(LogicalRecord(model_id, ModelContract(
            model_id.key, binding_id, V1, declaration_record.value.symbol_key,
            declaration_record.value.argument_types, declaration_record.value.result_kind,
            declaration_record.value.facet_positions, cycle_evidence_id,
            cycle_unknown_id, cycle_error_id, spec_record.identity, frozenset(),
        )))
    package = _package(
        "coding-minimal",
        "capknow.semantic",
        declarations=(*cycle_types.values(), first_decl, second_decl,
                      snapshot_decl, changes_decl, observe_decl),
        bindings=(first, second, *function_bindings),
        models=(first_model, second_model, *function_models),
        specs=(first_spec, second_spec, snapshot_spec, changes_spec, observe_spec,
               *function_access_specs),
    )
    package = replace(retained_package, value=replace(
        retained_package.value,
        declarations=retained_package.value.declarations + package.value.declarations,
        bindings=retained_package.value.bindings + package.value.bindings,
        profile_bindings=retained_package.value.profile_bindings,
        model_contracts=retained_package.value.model_contracts + package.value.model_contracts,
        services=(),
        certificates=(),
    ))
    environment = record(
        RecordKind.SEMANTIC_ENVIRONMENT,
        "E_PROPER_CYCLE",
        SemanticEnvironment(
            ABI0,
            tuple(item.identity for item in package.value.declarations),
            tuple(item.identity for item in package.value.pair_declarations),
            tuple(item.identity for item in package.value.bindings),
            profile_bindings=tuple(item.identity for item in package.value.profile_bindings),
            pair_bindings=tuple(item.identity for item in package.value.pair_bindings),
            authority_facts=tuple(item.identity for item in package.value.authority_facts),
            semantic_extensions=tuple(item.identity for item in package.value.semantic_extensions),
            mechanically_extracted_dependencies=frozenset(
                {first_id, second_id}
            ),
        ),
        namespace="cycle.environment",
    )
    abi = record(
        RecordKind.ABI,
        "ABI0",
        AbiRecord(ABI0),
        namespace="abi",
        version=ABI0,
    )
    retained_support = tuple(
        item for item in retained_core.universe.records
        if item.identity not in {retained_core.abi, retained_core.package}
        and item.identity.kind not in {RecordKind.SERVICE, RecordKind.CAPABILITY,
                                       RecordKind.CERTIFICATE}
    )
    return Universe(
        (abi, package, *retained_support,
         *cycle_admissions.values(), first_spec, second_spec,
         snapshot_spec, changes_spec, observe_spec, *function_access_specs,
         *cycle_aux, first_model, second_model, *function_models, environment),
        FormationRequest((first_id, second_id))
    )


_RETAINED_CK_CACHE: tuple[LogicalRecord, tuple[LogicalRecord, ...]] | None = None


_RETAINED_TYPE_DEPENDENCIES: dict[str, tuple[str, ...]] = {
    "PathSegment": (), "Path": ("PathSegment",), "PathSet": ("Path",),
    "ArtifactRole": (), "Format": (), "StorageBackend": (), "ByteSize": (),
    "ContentIdentity": (), "FieldId": (), "FieldValue": (), "SubjectId": (),
    "BehaviorValue": ("ContentIdentity", "FieldId", "FieldValue"),
    "ArtifactBody": ("ContentIdentity", "FieldId", "FieldValue", "SubjectId", "BehaviorValue"),
    "ArtifactBodyKind": (),
    "ArtifactContent": ("ArtifactRole", "Format", "ByteSize", "ContentIdentity", "FieldId", "FieldValue", "SubjectId", "BehaviorValue"),
    "RepositorySnapshot": ("Path", "ArtifactContent"),
    "SnapshotIdentity": ("RepositorySnapshot",),
    "ChangeEntry": ("ArtifactContent",), "ChangeSet": ("Path", "ChangeEntry"),
    "ArtifactSelector": ("PathSet", "ArtifactRole"),
    "ArtifactProjection": ("FieldId",), "Coverage": ("SubjectId",),
    "ObservationSpec": ("ArtifactSelector", "ArtifactProjection", "SubjectId", "FieldId"),
    "ObservationValue": ("ArtifactRole", "ArtifactBodyKind", "ArtifactProjection", "ArtifactContent", "BehaviorValue", "Format", "ByteSize", "FieldId", "FieldValue", "ContentIdentity"),
    "ObservationResult": ("Path", "SubjectId", "Coverage", "ObservationSpec", "ObservationValue"),
    "ObservationRelation": ("FieldId",),
    "VerificationStatus": (), "VerificationSpec": ("ObservationSpec",),
    "VerificationRecord": ("VerificationSpec", "SnapshotIdentity", "VerificationStatus", "ObservationResult"),
    "ImplementationEvidence": ("SnapshotIdentity",),
    "CodingEvidencePayload": ("VerificationRecord", "ImplementationEvidence"),
    "CodingEvidenceEntry": ("CodingEvidencePayload",),
    "AbstractCoverageResult": (),
    "ImplementationCoverageSubject": ("TaskSpec", "RepositorySnapshot", "AbstractCoverageResult"),
    "PairTraceDomain": (), "PairComparedFields": (), "AuthorityClauseTag": (),
    "AuthorityAttestationSubjectIdentity": ("AuthorityClauseTag",),
    "AuthorityAttestationValue": ("AuthorityAttestationSubjectIdentity",),
    "ServiceAdmissionSubject": ("TaskSpec", "RepositorySnapshot", "ObservationSpec", "ArtifactSelector", "ImplementationCoverageSubject", "PairTraceDomain", "PairComparedFields", "AuthorityAttestationValue"),
    "EvolutionAdmissionSubject": (),
    "Criterion": ("ObservationSpec", "ObservationResult", "ArtifactSelector", "ByteSize", "Format", "ObservationRelation"),
    "TaskSpec": ("Criterion", "VerificationSpec"),
    "ChangeKind": (), "CommandId": (), "ContactClass": (), "ReleaseId": (),
    "Purpose": (),
    "EventPattern": ("PathSet", "VerificationSpec", "VerificationStatus", "ChangeKind", "CommandId", "ContactClass", "ReleaseId", "SnapshotIdentity", "ArtifactSelector"),
    "CommandEventPayload": ("CommandId", "Purpose"),
    "TestEventPayload": ("VerificationSpec", "SnapshotIdentity", "VerificationStatus"),
    "PathChangeEventPayload": ("Path", "ArtifactContent"),
    "NetworkContactEventPayload": ("ContactClass", "Purpose"),
    "ReleaseEventPayload": ("ReleaseId", "SnapshotIdentity"),
    "DependencyRefreshEventPayload": ("ArtifactSelector", "SnapshotIdentity"),
}


def _retained_type_rows() -> tuple[tuple[LogicalRecord, ...], tuple[LogicalRecord, ...]]:
    declarations: list[LogicalRecord] = []
    admissions: list[LogicalRecord] = []
    for type_name, dependency_names in _RETAINED_TYPE_DEPENDENCIES.items():
        declaration_id = rid(
            RecordKind.TYPE_DECLARATION, f"T({type_name})", namespace="coding.type")
        admission_id = rid(
            RecordKind.CONTRACT_SPEC,
            f"CS(TYPE_ADMISSION,type.{type_name})",
            namespace="coding.type-admission",
        )
        dependencies = frozenset(
            rid(RecordKind.TYPE_DECLARATION, f"T({name})", namespace="coding.type")
            for name in dependency_names
        )
        admission = LogicalRecord(admission_id, ContractSpec(
            admission_id.key,
            Layer.DELTA,
            ContractRole.TYPE_ADMISSION,
            ("Value",),
            frozenset({"admitted", "not_admitted"}),
            tuple(ObservationQuery(
                dependency, ObservationKind.TYPE_ADMISSION_FACT, ("nested_value",))
                for dependency in sorted(dependencies)),
            dependencies,
            f"admit_{type_name}",
            TypeAdmissionRelation(admission_type(type_name)),
        ))
        admissions.append(admission)
        declarations.append(LogicalRecord(
            declaration_id,
            TypeDeclaration(
                declaration_id.key,
                admission.value,
                dependencies | frozenset({admission_id}),
            ),
        ))
    return tuple(declarations), tuple(admissions)


def _retained_literal_values() -> tuple[tuple[str, str, Any], ...]:
    # K3-S fixes p_b as two logical path segments.  It is logical data, not a
    # host path, and is shared literally by the bounds and confluence values.
    path = cp.Path((cp.PathSegment("dependency"), cp.PathSegment("lock")))
    selector = cp.ArtifactSelector(
        cp.SelectorTag.PATHS, frozenset({path}))
    artifact = cp.ArtifactContent(
        cp.ArtifactTag.TEXT, cp.ArtifactRole.DEPENDENCY_LOCK, cp.Format.TEXT,
        cp.ByteSize(150), cp.ContentIdentity("lock_v1"))
    pre = cp.RepositorySnapshot(())
    final = cp.RepositorySnapshot(((path, artifact),))
    spec_c = cp.ObservationSpec(
        cp.ObservationSpecTag.ARTIFACT_VIEW, selector,
        cp.ArtifactProjection(cp.ProjectionTag.CONTENT))
    result_c = cp.observe(spec_c, final).value
    field_left = cp.FieldId("request_field")
    field_right = cp.FieldId("client_field")
    accepted_shape = cp.FieldValue(cp.FieldValueTag.ATOM, "accepted_shape")
    client_pair = cp.SubjectId(cp.SubjectTag.CLIENT_PAIR, "adapter_pair")
    left_shape = ((field_left, accepted_shape),)
    right_shape = ((field_right, accepted_shape),)
    spec_w = cp.ObservationSpec(
        cp.ObservationSpecTag.CLIENT_ADAPTER_VIEW, domain=frozenset({client_pair}))
    adapter_relation = cp.ObservationRelation(
        cp.ObservationRelationTag.FIELD_CORRESPONDENCE,
        ((field_left, field_right),))
    adapter_path = cp.Path((cp.PathSegment("adapter"), cp.PathSegment("schema")))
    adapter_artifact = cp.ArtifactContent(
        cp.ArtifactTag.BEHAVIOR, cp.ArtifactRole.PUBLIC_SCHEMA, cp.Format.JSON,
        cp.ByteSize(1), observations=((client_pair, cp.BehaviorValue(
            cp.BehaviorTag.CORRESPONDENCE, left=left_shape, right=right_shape)),))
    witness_snapshot = cp.RepositorySnapshot(((adapter_path, adapter_artifact),))
    task_nonempty = cp.TaskSpec(frozenset({cp.ArtifactsNonempty(selector)}))
    task_lt = cp.TaskSpec(frozenset({cp.ArtifactSizeLt(selector, cp.ByteSize(100))}))
    task_ge = cp.TaskSpec(frozenset({cp.ArtifactSizeAtLeast(selector, cp.ByteSize(200))}))
    task_w = cp.TaskSpec(frozenset({cp.AdapterCorresponds(spec_w, adapter_relation)}))
    task_t = cp.TaskSpec(frozenset({cp.ObservationEquals(spec_c, result_c)}))
    contract_ids = {
        name: rid(RecordKind.OUTCOME, f"C_{name}", namespace="coding.contract")
        for name in ("b", "c", "w", "choice")
    }
    authority_rows = (
        ("b,1", contract_ids["b"], cp.AuthorityClauseTag.BOUNDS),
        ("c,1", contract_ids["c"], cp.AuthorityClauseTag.CONFLUENCE_OBSERVATION),
        ("c,2", contract_ids["c"], cp.AuthorityClauseTag.CONFLUENCE_CHANGE),
        ("w,1", contract_ids["w"], cp.AuthorityClauseTag.ADAPTER_PRESERVATION),
        ("w,2", contract_ids["w"], cp.AuthorityClauseTag.ADAPTER_ACCEPTANCE),
        ("choice,1", contract_ids["choice"], None),
    )


    authority_subjects = tuple(
        cp.AuthorityAttestationSubjectIdentity(
            cp.AuthoritySubjectTag.CHOICE if tag is None else cp.AuthoritySubjectTag.CLAUSE,
            contract_id, clause_tag=tag,
            choice_id="storage" if tag is None else None)
        for _, contract_id, tag in authority_rows
    )
    attestations = tuple(
        cp.AuthorityAttestationValue(
            rid(RecordKind.AUTHORITY_REF, f"AUTH({name})",
                owner="PLUGIN_ISSUER(APK)",
                namespace="coding.fixture"),
            rid(RecordKind.SOURCE, f"SRC({name})",
                owner="PLUGIN_ISSUER(APK)",
                namespace="authenticated.fixture.source"),
            ("user" if name == "choice,1" else "fixture_principal"),
            ("BIND_CHOICE(storage)" if name == "choice,1" else "REQUIRE"),
            subject)
        for (name, _, _), subject in zip(authority_rows, authority_subjects, strict=True)
    )
    profile_subject = cp.ImplementationCoverageSubject(
        contract_ids["w"], task_w, witness_snapshot, frozenset(),
        cp.Eval(cp.Truth.TRUE),
        cp.AbstractCoverageResult(cp.AbstractCoverageTag.NONE))
    pair_id = rid(RecordKind.PAIR_DECLARATION, "PAIR(refresh)", namespace="pair")
    scope_id = rid(RecordKind.BINDING, "BINDING(DP(refresh_scope))", namespace="coding.binding")
    occurrence_id = rid(RecordKind.BINDING, "BINDING(DP(refresh_occurred))", namespace="coding.binding")
    service_subjects = (
        ("bounds_subject_b", cp.ServiceAdmissionSubject(
            cp.ServiceSubjectTag.BOUNDS, selector=selector, nonempty_task=task_nonempty,
            upper_task=task_lt, lower_task=task_ge)),
        ("confluence_subject_c", cp.ServiceAdmissionSubject(
            cp.ServiceSubjectTag.CONFLUENCE, spec=spec_c, pre=pre, final=final)),
        ("witness_subject_w", cp.ServiceAdmissionSubject(
            cp.ServiceSubjectTag.ADAPTER_WITNESS, contract_identity=contract_ids["w"],
            spec=spec_w, task=task_w, pre=witness_snapshot, final=witness_snapshot)),
        ("predicate_subject_t", cp.ServiceAdmissionSubject(
            cp.ServiceSubjectTag.PREDICATE_CALL,
            binding=rid(RecordKind.BINDING, "BINDING(DP(task_accepts))", namespace="coding.binding"),
            arguments=(task_t, final, frozenset()))),
        ("profile_subject_w", cp.ServiceAdmissionSubject(
            cp.ServiceSubjectTag.PROFILE_CALL,
            profile=rid(RecordKind.PROFILE_BINDING, "PROFILE_impl", namespace="coding.profile"),
            profile_subject=profile_subject)),
        ("pair_subject", cp.ServiceAdmissionSubject(
            cp.ServiceSubjectTag.PAIR_COHERENCE, pair=pair_id,
            scope_binding=scope_id, occurrence_binding=occurrence_id,
            trace_domain=cp.PairTraceDomain.ALL_ADMITTED_TRACES,
            compared_fields=cp.PairComparedFields.COMPLETE_EVAL_RECORD)),
        *((f"authority_subject({name})", cp.ServiceAdmissionSubject(
            cp.ServiceSubjectTag.AUTHORITY_ATTESTATION,
            authority_fact_key=rid(RecordKind.AUTHORITY_FACT, f"AF({name})", namespace="authority.fact"),
            attestation=attestation,
            offered_evidence_refs=frozenset({cp.EvidenceRef(
                "PLUGIN_ISSUER(ATK)", "coding.authority.attestation",
                f"AUTHORITY_EVIDENCE_LOCAL({name})", "AREQUIRED")})))
          for (name, _, _), attestation in zip(authority_rows, attestations, strict=True)),
    )
    environment_one = rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_t", namespace="environment")
    evolution_owner = "capknow.fixture.evolution-owner"
    candidate_ids = (
        rid(RecordKind.MIGRATION, "MK0", owner=evolution_owner,
            namespace="evolution"),
        rid(RecordKind.COMPATIBILITY_CLAIM, "CCK0", owner=evolution_owner,
            namespace="evolution"),
        rid(RecordKind.SEMANTIC_EXTENSION, "XK0", owner=evolution_owner,
            namespace="evolution"),
        rid(RecordKind.SEMANTIC_EXTENSION, "XK1", owner=evolution_owner,
            namespace="evolution"),
    )
    optional_alias = rid(RecordKind.ALIAS, "AK0", owner=evolution_owner,
                         namespace="evolution.alias")
    required_alias = rid(RecordKind.ALIAS, "AK1", owner=evolution_owner,
                         namespace="evolution.alias")
    task_binding = rid(RecordKind.BINDING, "BINDING(DP(task_accepts))",
                       namespace="coding.binding")
    evolution_subjects = (
        cp.EvolutionAdmissionSubject(
            cp.EvolutionSubjectTag.MIGRATION_RELATION, candidate_ids[0],
            source_identity=environment_one, target_identity=environment_one,
            relation=cp.EvolutionRelation.FULL_CONTRACT_EQUIVALENCE),
        cp.EvolutionAdmissionSubject(
            cp.EvolutionSubjectTag.COMPATIBILITY_CLAIM, candidate_ids[1],
            source_abi=ABI0, target_abi=ABI0,
            source_keys=frozenset({candidate_ids[0]}),
            target_keys=frozenset({task_binding})),
        cp.EvolutionAdmissionSubject(
            cp.EvolutionSubjectTag.SEMANTIC_EXTENSION, candidate_ids[2],
            target_record_identity=optional_alias,
            owner_layer=cp.EvolutionOwnerLayer.SIGMA),
        cp.EvolutionAdmissionSubject(
            cp.EvolutionSubjectTag.SEMANTIC_EXTENSION, candidate_ids[3],
            target_record_identity=required_alias,
            owner_layer=cp.EvolutionOwnerLayer.SIGMA),
    )
    return (
        ("TaskSpec", "ts_nonempty", task_nonempty),
        ("TaskSpec", "ts_lt_100", task_lt),
        ("TaskSpec", "ts_ge_200", task_ge),
        ("ObservationSpec", "s_c", spec_c),
        ("RepositorySnapshot", "P_c", pre),
        ("RepositorySnapshot", "F_c", final),
        ("ObservationResult", "O_c", result_c),
        ("ObservationSpec", "s_w", spec_w),
        ("TaskSpec", "t_w", task_w), ("TaskSpec", "t_t", task_t),
        ("StorageBackend", "LOCAL_STORAGE", cp.StorageBackend.LOCAL),
        ("StorageBackend", "HOSTED_STORAGE", cp.StorageBackend.HOSTED),
        ("PairTraceDomain", "ALL_ADMITTED_TRACES", cp.PairTraceDomain.ALL_ADMITTED_TRACES),
        ("PairComparedFields", "COMPLETE_EVAL_RECORD", cp.PairComparedFields.COMPLETE_EVAL_RECORD),
        *(("AuthorityClauseTag", tag.value, tag) for tag in cp.AuthorityClauseTag),
        *(("AuthorityAttestationSubjectIdentity", f"attestation_subject_identity({name})", value)
          for (name, _, _), value in zip(authority_rows, authority_subjects, strict=True)),
        *(("AuthorityAttestationValue", f"ATTEST({name})", value)
          for (name, _, _), value in zip(authority_rows, attestations, strict=True)),
        *(("ServiceAdmissionSubject", name, value) for name, value in service_subjects),
        *(("EvolutionAdmissionSubject", name, value) for name, value in zip(
            ("mr_subject", "cc_subject", "x0_subject", "x1_subject"),
            evolution_subjects, strict=True)),
    )


def _retained_literal_rows(
    type_declarations: tuple[LogicalRecord, ...],
    type_admissions: tuple[LogicalRecord, ...],
) -> tuple[
    tuple[LogicalRecord, ...], tuple[LogicalRecord, ...],
    tuple[LogicalRecord, ...], tuple[LogicalRecord, ...],
]:
    type_by_name = {
        item.identity.key.local[2:-1]: item for item in type_declarations
    }
    admission_by_name = {
        item.identity.key.local.removeprefix("CS(TYPE_ADMISSION,type.")[:-1]: item
        for item in type_admissions
    }

    def type_closure(name: str) -> frozenset[RecordIdentity]:
        return frozenset({
            type_by_name[name].identity, admission_by_name[name].identity,
        }) | frozenset().union(*(
            type_closure(dependency)
            for dependency in _RETAINED_TYPE_DEPENDENCIES[name]
        ))

    evidence_id = rid(RecordKind.CONTRACT_SPEC, "CS(EVIDENCE_SCHEMA,none)", namespace="coding.contract")
    access_id = rid(RecordKind.CONTRACT_SPEC, "CS(ACCESS_BOUNDARY,literal)", namespace="coding.contract")
    unknown_id = rid(RecordKind.CONTRACT_SPEC, "CS(UNKNOWN_BEHAVIOR,not_applicable)", namespace="coding.contract")
    error_id = rid(RecordKind.CONTRACT_SPEC, "CS(EVALUATION_ERROR_BEHAVIOR,literal)", namespace="coding.contract")
    shared_specs = (
        LogicalRecord(evidence_id, ContractSpec(evidence_id.key, Layer.SIGMA, ContractRole.EVIDENCE_SCHEMA, ("ExplicitInputs",), frozenset({"EvidenceSet"}), (), frozenset(), "evidence_none")),
        LogicalRecord(access_id, ContractSpec(access_id.key, Layer.SIGMA, ContractRole.ACCESS_BOUNDARY, ("LiteralIdentity",), frozenset({"ADMITTED", "INADMISSIBLE"}), (), frozenset(), "access_literal")),
        LogicalRecord(unknown_id, ContractSpec(unknown_id.key, Layer.SIGMA, ContractRole.UNKNOWN_BEHAVIOR, ("LiteralOrFunctionInput",), frozenset({"NOT_APPLICABLE"}), (), frozenset(), "unknown_not_applicable")),
        LogicalRecord(error_id, ContractSpec(error_id.key, Layer.SIGMA, ContractRole.EVALUATION_ERROR_BEHAVIOR, ("LiteralIdentity",), frozenset({"TermResult"}), (), frozenset(), "error_literal")),
    )
    declarations: list[LogicalRecord] = []
    bindings: list[LogicalRecord] = []
    models: list[LogicalRecord] = []
    meaning_specs: list[LogicalRecord] = []
    for type_name, local, literal_value in _retained_literal_values():
        declaration_id = rid(RecordKind.DECLARATION, f"L(T({type_name}),{local})", namespace="coding.declaration")
        declaration = LogicalRecord(declaration_id, DeclarationShape(
            declaration_id.key, key("NO_SYMBOL_LITERAL", namespace="coding.symbol"),
            "LITERAL", (), f"T({type_name})", (),
            frozenset({type_by_name[type_name].identity}), literal_value))
        meaning_id = rid(
            RecordKind.CONTRACT_SPEC,
            f"CS(LITERAL_MEANING,literal.T({type_name}).{local})",
            namespace="coding.contract",
        )
        meaning = LogicalRecord(meaning_id, ContractSpec(
            meaning_id.key, Layer.SIGMA, ContractRole.LITERAL_MEANING,
            ("LiteralIdentity",), frozenset({"TERM_VALUE"}), (), frozenset(),
            f"literal_meaning_{local}"))
        binding_id = rid(RecordKind.BINDING, f"BINDING(L(T({type_name}),{local}))", namespace="coding.binding")
        proper = frozenset({declaration_id, meaning_id, evidence_id, access_id, unknown_id, error_id})
        binding = LogicalRecord(binding_id, SemanticBinding(
            binding_id.key, declaration_id, "LITERAL", meaning_id, (), proper,
            proper | type_closure(type_name), evidence_id, access_id, unknown_id,
            error_id, "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT"))
        model_id = rid(RecordKind.MODEL_CONTRACT, f"MODEL_LITERAL(T({type_name}),{local})", namespace="coding.model")
        model = LogicalRecord(model_id, ModelContract(
            model_id.key, binding_id, V1, declaration.value.symbol_key, (),
            declaration.value.result_kind, (), evidence_id, unknown_id, error_id,
            meaning_id, frozenset()))
        declarations.append(declaration)
        meaning_specs.append(meaning)
        bindings.append(binding)
        models.append(model)
    return tuple(declarations), tuple(bindings), tuple(models), (*shared_specs, *meaning_specs)


def _identity_union(*groups: tuple[LogicalRecord, ...]) -> tuple[LogicalRecord, ...]:
    by_identity: dict[RecordIdentity, LogicalRecord] = {}
    for group in groups:
        for item in group:
            previous = by_identity.get(item.identity)
            if previous is not None and previous != item:
                raise ValueError(f"unequal retained PKG_CK member: {item.identity}")
            by_identity[item.identity] = item
    return tuple(sorted(by_identity.values(), key=lambda item: item.identity))


def _retained_symbol_rows(
    type_declarations: tuple[LogicalRecord, ...],
    type_admissions: tuple[LogicalRecord, ...],
) -> tuple[
    tuple[LogicalRecord, ...], tuple[LogicalRecord, ...],
    tuple[LogicalRecord, ...], tuple[LogicalRecord, ...],
    tuple[LogicalRecord, ...], tuple[LogicalRecord, ...],
]:
    """Build the literal DELTA_SYMBOL_X/BIND_ORDINARY_X/DELTA_PAIR_X slice."""
    core = _core_construction_local()
    core_records = compose_records(core.universe.records)
    core_declaration = core_records.at(core.declaration)
    core_binding = core_records.at(core.binding)
    core_model = core_records.at(core.model)
    core_profile = next(
        item for item in core_records.records
        if item.identity.kind is RecordKind.PROFILE_BINDING)
    assert core_declaration and core_binding and core_model

    type_by_name = {
        item.identity.key.local[2:-1]: item for item in type_declarations
    }
    admission_by_name = {
        item.identity.key.local.removeprefix("CS(TYPE_ADMISSION,type.")[:-1]: item
        for item in type_admissions
    }

    def type_closure(*names: str) -> frozenset[RecordIdentity]:
        reached: set[RecordIdentity] = set()
        pending = list(names)
        while pending:
            name = pending.pop()
            reached.update((type_by_name[name].identity, admission_by_name[name].identity))
            pending.extend(_RETAINED_TYPE_DEPENDENCIES[name])
        return frozenset(reached)

    declarations: list[LogicalRecord] = []
    bindings: list[LogicalRecord] = []
    models: list[LogicalRecord] = []
    specs: dict[RecordIdentity, LogicalRecord] = {}
    by_name: dict[str, LogicalRecord] = {}
    binding_by_name: dict[str, LogicalRecord] = {}

    callable_rows = (
        ("FUNCTION", "snapshot_of", ("State",), "T(RepositorySnapshot)", (frozenset({"pre", "final"}),), "state_only", "not_applicable", "none"),
        ("FUNCTION", "changes_between", ("RepositorySnapshot", "RepositorySnapshot"), "T(ChangeSet)", (frozenset({"pre"}), frozenset({"final"})), "snapshot_pair", "not_applicable", "none"),
        ("FUNCTION", "observe", ("ObservationSpec", "RepositorySnapshot"), "T(ObservationResult)", (frozenset(), frozenset({"pre", "final"})), "spec_snapshot", "not_applicable", "none"),
        ("PREDICATE", "observations_equal", ("ObservationResult", "ObservationResult"), "Bool", (frozenset({"pre"}), frozenset({"final"})), "result_pair", "never", "none"),
        ("PREDICATE", "task_accepts", ("TaskSpec", "RepositorySnapshot", "EvidenceStore"), "Bool", (frozenset(), frozenset({"final"}), frozenset({"evidence"})), "task_final_evidence", "task", "verification"),
        ("PREDICATE", "dependency_metadata_changed", ("ChangeSet",), "Bool", (frozenset({"pre", "final"}),), "change_set_only", "never", "none"),
        ("PREDICATE", "verification_passed", ("VerificationSpec", "RepositorySnapshot", "EvidenceStore"), "Bool", (frozenset(), frozenset({"final"}), frozenset({"evidence"})), "verification_snapshot_evidence", "evidence_pending", "verification"),
        ("PREDICATE", "event_matches", ("EventPattern", "EventValue"), "Bool", (frozenset(), frozenset()), "pattern_event", "never", "none"),
        ("PREDICATE", "event_occurred", ("EventPattern", "Trace"), "Bool", (frozenset(), frozenset({"trace"})), "pattern_trace", "never", "none"),
        ("PREDICATE", "refresh_scope", ("EventValue",), "Bool", (frozenset(),), "event_only", "never", "none"),
        ("PREDICATE", "refresh_occurred", ("Trace",), "Bool", (frozenset({"trace"}),), "event_only", "never", "none"),
    )

    def contract(role: ContractRole, local: str, domain: tuple[str, ...],
                 relation: str, support: frozenset[RecordIdentity] = frozenset(),
                 queries: tuple[ObservationQuery, ...] = ()) -> LogicalRecord:
        identity = rid(RecordKind.CONTRACT_SPEC, f"CS({role.value},{local})",
                       namespace="coding.contract")
        existing = specs.get(identity)
        if existing is not None:
            return existing
        codomain = (
            frozenset({"TermResult"})
            if role is ContractRole.FUNCTION_MEANING
            else frozenset({"Eval"})
            if role is ContractRole.PREDICATE_MEANING
            else frozenset({"EvidenceSet"})
            if role is ContractRole.EVIDENCE_SCHEMA
            else frozenset({"ADMITTED", "INADMISSIBLE"})
            if role is ContractRole.ACCESS_BOUNDARY
            else frozenset({"NOT_APPLICABLE"})
            if role is ContractRole.UNKNOWN_BEHAVIOR and local == "not_applicable"
            else frozenset({"Eval"})
            if role is ContractRole.UNKNOWN_BEHAVIOR
            else frozenset({"TermResult"})
            if role is ContractRole.EVALUATION_ERROR_BEHAVIOR and local == "term"
            else frozenset({"ProfileResult"})
            if role in {ContractRole.EVALUATION_ERROR_BEHAVIOR,
                        ContractRole.REASONING_ERROR_BEHAVIOR}
            and local == "profile"
            else frozenset({"Eval"})
        )
        result = LogicalRecord(identity, ContractSpec(
            identity.key, Layer.SIGMA, role, domain, codomain,
            queries, support, relation))
        specs[identity] = result
        return result

    for kind, name, argument_types, result_kind, facets, access_name, unknown_name, evidence_name in callable_rows:
        declaration_id = rid(RecordKind.DECLARATION,
                             f"D{'F' if kind == 'FUNCTION' else 'P'}({name})",
                             namespace="coding.declaration")
        dependencies = tuple(item for item in argument_types if item in type_by_name)
        exact_argument_types = tuple(
            type_by_name[item].identity.key
            if item in type_by_name else key(item, namespace="carrier.type")
            for item in argument_types)
        declaration = LogicalRecord(declaration_id, DeclarationShape(
            declaration_id.key,
            key(f"S{'F' if kind == 'FUNCTION' else 'P'}({name})", namespace="coding.symbol"),
            kind, exact_argument_types, result_kind, facets,
            frozenset(type_by_name[item].identity for item in dependencies)))
        declarations.append(declaration)
        by_name[name] = declaration
        if name == "refresh_occurred":
            continue
        meaning_support = (frozenset({rid(RecordKind.BINDING,
                                             "BINDING(DP(event_matches))",
                                             namespace="coding.binding")})
                           if name == "event_occurred" else frozenset())
        if name == "snapshot_of":
            meaning_support = frozenset({type_by_name["RepositorySnapshot"].identity})
        queries = (
            (ObservationQuery(
                next(iter(meaning_support)),
                ObservationKind.TYPE_ADMISSION_FACT,
                ("snapshot",)),)
            if name == "snapshot_of"
            else (ObservationQuery(
                next(iter(meaning_support)),
                ObservationKind.EVAL_RESULT_SEQUENCE,
                ("pattern", "trace")),)
            if meaning_support else ()
        )
        meaning_domain = tuple(
            f"T({item})" if item in type_by_name else item
            for item in argument_types)
        meaning = contract(
            ContractRole.FUNCTION_MEANING if kind == "FUNCTION" else ContractRole.PREDICATE_MEANING,
            name, meaning_domain, name, meaning_support, queries)
        evidence_support = (
            frozenset({type_by_name["CodingEvidenceEntry"].identity})
            if evidence_name == "verification" else frozenset())
        evidence_queries = (() if not evidence_support else (
            ObservationQuery(next(iter(evidence_support)),
                             ObservationKind.TYPE_ADMISSION_FACT,
                             ("evidence_entry",)),))
        evidence = contract(ContractRole.EVIDENCE_SCHEMA, evidence_name,
                            (("ExplicitInputs",) if evidence_name == "none"
                             else ("EvidenceStore",)),
                            f"evidence_{evidence_name}", evidence_support,
                            evidence_queries)
        access = contract(ContractRole.ACCESS_BOUNDARY, access_name,
                          meaning_domain or ("Trace",), f"access_{access_name}",
                          meaning_support, queries)
        unknown = contract(ContractRole.UNKNOWN_BEHAVIOR, unknown_name,
                           (("LiteralOrFunctionInput",)
                            if unknown_name == "not_applicable"
                            else ("PredicateInput",)),
                           f"unknown_{unknown_name}")
        error_name = "term" if kind == "FUNCTION" else "predicate"
        error = contract(ContractRole.EVALUATION_ERROR_BEHAVIOR, error_name,
                         (("TermInput",) if kind == "FUNCTION"
                          else ("PredicateInput",)), f"error_{error_name}")
        binding_id = rid(RecordKind.BINDING,
                         f"BINDING(D{'F' if kind == 'FUNCTION' else 'P'}({name}))",
                         namespace="coding.binding")
        proper = frozenset({declaration.identity, meaning.identity,
                            evidence.identity, access.identity,
                            unknown.identity, error.identity}) | meaning_support | evidence_support
        closure = proper | type_closure(*(item for item in argument_types if item in type_by_name))
        if evidence_name == "verification":
            closure |= type_closure("CodingEvidenceEntry")
        if name == "snapshot_of":
            closure |= type_closure("RepositorySnapshot")
        if name == "event_occurred":
            lower = binding_by_name["event_matches"]
            closure |= lower.value.dependency_closure | frozenset({lower.identity})
        binding = LogicalRecord(binding_id, SemanticBinding(
            binding_id.key, declaration.identity, kind, meaning.identity,
            facets, proper, closure, evidence.identity, access.identity,
            unknown.identity, error.identity,
            "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT"))
        model_id = rid(RecordKind.MODEL_CONTRACT, f"MODEL_{name}", namespace="coding.model")
        model = LogicalRecord(model_id, ModelContract(
            model_id.key, binding_id, V1, declaration.value.symbol_key,
            declaration.value.argument_types, declaration.value.result_kind,
            declaration.value.facet_positions, evidence.identity, unknown.identity,
            error.identity, meaning.identity,
            core_model.value.capability_summaries if name == "task_accepts" else frozenset()))
        bindings.append(binding)
        binding_by_name[name] = binding
        models.append(model)

    event_rows = (
        ("command", "CommandEventPayload", "CONTROLLED"),
        ("test", "TestEventPayload", "OBSERVATIONAL"),
        ("path_change", "PathChangeEventPayload", "CONTROLLED"),
        ("network_contact", "NetworkContactEventPayload", "CONTROLLED"),
        ("release", "ReleaseEventPayload", "CONTROLLED"),
        ("dependency_refresh", "DependencyRefreshEventPayload", "CONTROLLED"),
    )
    for name, payload_type, event_class in event_rows:
        event_id = rid(RecordKind.EVENT, f"DE({name})", namespace="coding.declaration")
        declarations.append(LogicalRecord(event_id, DeclarationShape(
            event_id.key, key(f"EK({name})", namespace="coding.event"),
            "EVENT", (type_by_name[payload_type].identity.key,), "EventValue",
            (frozenset(),), frozenset({type_by_name[payload_type].identity}))))

    pair_id = rid(RecordKind.PAIR_DECLARATION, "PAIR(refresh)", namespace="pair")
    scope = binding_by_name["refresh_scope"]
    occurrence_decl = by_name["refresh_occurred"]
    occurrence_meaning = contract(ContractRole.OCCURRENCE_MEANING,
                                  "refresh_occurred", ("Trace",),
                                  "T3_A1_MEANING_LIFT")
    occurrence_id = rid(RecordKind.BINDING, "BINDING(DP(refresh_occurred))",
                        namespace="coding.binding")
    occurrence_direct = frozenset({occurrence_decl.identity, occurrence_meaning.identity})
    occurrence = LogicalRecord(occurrence_id, OccurrenceSemanticContractBundle(
        occurrence_meaning.identity, occurrence_decl.value.facet_positions,
        contract(ContractRole.EVIDENCE_SCHEMA, "none", ("EvidenceStore",), "evidence_none").identity,
        contract(ContractRole.ACCESS_BOUNDARY, "event_only", ("Trace",), "access_event_only").identity,
        contract(ContractRole.UNKNOWN_BEHAVIOR, "never", ("UnknownReasonSet",), "unknown_never").identity,
        contract(ContractRole.EVALUATION_ERROR_BEHAVIOR, "predicate", ("FailureReasonSet",), "error_predicate").identity,
        "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT", occurrence_direct,
        occurrence_direct))
    occurrence_model_id = rid(RecordKind.MODEL_CONTRACT, "MODEL_refresh_occurred", namespace="coding.model")
    occurrence_model = LogicalRecord(occurrence_model_id, ModelContract(
        occurrence_model_id.key, occurrence_id, V1, occurrence_decl.value.symbol_key,
        occurrence_decl.value.argument_types, occurrence_decl.value.result_kind,
        occurrence_decl.value.facet_positions, occurrence.value.evidence_schema,
        occurrence.value.unknown_contract, occurrence.value.evaluation_error_contract,
        occurrence.value.meaning_contract, frozenset()))
    pair = LogicalRecord(pair_id, PairDeclaration(
        pair_id.key, by_name["refresh_scope"].value.symbol_key,
        occurrence_decl.value.symbol_key,
        frozenset({key("EK(dependency_refresh)", namespace="coding.event")}),
        frozenset({by_name["refresh_scope"].identity, occurrence_decl.identity,
                   rid(RecordKind.EVENT, "DE(dependency_refresh)", namespace="coding.declaration")})))
    pair_binding_id = rid(RecordKind.PAIR_BINDING, "PB_refresh", namespace="pair.binding")
    pair_roots = frozenset({pair_id, scope.identity, occurrence_id, occurrence_model_id})
    pair_binding = LogicalRecord(pair_binding_id, PairBinding(
        pair_id.key, scope.identity, occurrence_id, occurrence_model_id,
        occurrence_id, rid(RecordKind.CERTIFICATE, "NONE", namespace="pair"),
        rid(RecordKind.CAPABILITY, "NONE", namespace="pair"),
        pair_roots, pair_roots | scope.value.dependency_closure | occurrence.value.dependency_closure,
        frozenset(), IndependentCoherenceProof(
            occurrence_id, rid(RecordKind.CERTIFICATE, "NONE", namespace="pair"),
            rid(RecordKind.CAPABILITY, "NONE", namespace="pair"))))
    profile_key = key("PK(implementation_evidence)", namespace="coding.profile")
    profile_id = rid(
        RecordKind.PROFILE_BINDING,
        "PROFILE_BINDING(PK(implementation_evidence))",
        namespace="coding.binding")
    coverage = contract(
        ContractRole.PROFILE_COVERAGE, "implementation_evidence",
        ("ImplementationCoverageSubject",), "implementation_evidence_profile",
        frozenset({binding_by_name["task_accepts"].identity}),
        (ObservationQuery(binding_by_name["task_accepts"].identity,
                          ObservationKind.EVAL_RESULT,
                          ("task", "final_snapshot", "evidence_store")),))
    profile_evidence = contract(
        ContractRole.EVIDENCE_SCHEMA, "implementation_profile",
        ("EvidenceStore",), "evidence_implementation_profile",
        frozenset({type_by_name["CodingEvidenceEntry"].identity}),
        (ObservationQuery(type_by_name["CodingEvidenceEntry"].identity,
                          ObservationKind.TYPE_ADMISSION_FACT,
                          ("evidence_entry",)),))
    profile_unknown = contract(
        ContractRole.UNKNOWN_BEHAVIOR, "evidence_pending",
        ("ProfileInput",), "unknown_evidence_pending")
    profile_evaluation_error = contract(
        ContractRole.EVALUATION_ERROR_BEHAVIOR, "profile",
        ("ProfileInput",), "error_profile")
    profile_reasoning_error = contract(
        ContractRole.REASONING_ERROR_BEHAVIOR, "profile",
        ("ProfileRequest",), "reasoning_error_profile")
    profile_proper = frozenset({
        coverage.identity, profile_evidence.identity, profile_unknown.identity,
        profile_evaluation_error.identity, profile_reasoning_error.identity,
    })
    profile_closure = (profile_proper
                       | frozenset({binding_by_name["task_accepts"].identity})
                       | binding_by_name["task_accepts"].value.dependency_closure
                       | type_closure("CodingEvidenceEntry"))
    profile = LogicalRecord(profile_id, ProfileBinding(
        profile_key,
        frozenset({
            ProfileDimensionKey(profile_key, "abstract_acceptance_evidence"),
            ProfileDimensionKey(profile_key,
                                "concrete_implementation_evidence"),
        }),
        coverage.identity, profile_evidence.identity, profile_proper,
        profile_closure, profile_unknown.identity,
        profile_evaluation_error.identity, profile_reasoning_error.identity))
    models.append(occurrence_model)
    return (tuple(declarations), tuple(bindings), tuple(models),
            tuple(specs.values()), (pair,), (occurrence, pair_binding, profile))


def _retained_ck() -> tuple[LogicalRecord, tuple[LogicalRecord, ...]]:
    """Construct the one literal K3-S PKG_CK and its external records once."""
    global _RETAINED_CK_CACHE
    if _RETAINED_CK_CACHE is not None:
        return _RETAINED_CK_CACHE
    core = _core_construction_local()
    package = next(item for item in core.universe.records
                   if isinstance(item.value, PluginPackage))
    retained_types, retained_admissions = _retained_type_rows()
    retained_literals, retained_literal_bindings, retained_literal_models, retained_literal_specs = (
        _retained_literal_rows(retained_types, retained_admissions))
    (symbols, ordinary_bindings, ordinary_models, ordinary_specs,
     pair_declarations, special_bindings) = _retained_symbol_rows(
         retained_types, retained_admissions)
    occurrence, pair_binding, profile = special_bindings

    declaration_records = {
        item.identity: item for item in (*retained_types, *symbols)
    }
    def declaration_dependency_closure(
        declaration_identity: RecordIdentity,
    ) -> frozenset[RecordIdentity]:
        reached: set[RecordIdentity] = {declaration_identity}
        pending = [declaration_identity]
        while pending:
            current = declaration_records.get(pending.pop())
            if current is None:
                continue
            dependencies = (
                current.value.proper_declaration_dependencies
                if isinstance(current.value, TypeDeclaration)
                else current.value.proper_type_dependencies
                if isinstance(current.value, DeclarationShape)
                else frozenset())
            for dependency in dependencies:
                if dependency not in reached:
                    reached.add(dependency)
                    pending.append(dependency)
        return frozenset(reached)

    # K3-S §6.2/§8.2 fixes exactly these six CK descriptors and BENV.
    core_records = compose_records(core.universe.records)
    predicate_capability = core_records.at(core.capability)
    assert predicate_capability is not None
    confluence = _confluence_construction_local(OrderTag.FORWARD)
    confluence_capability = next(
        item for item in confluence.manifest
        if item.identity.kind is RecordKind.CAPABILITY
        and item.identity.key.local == "CAP(confluence)")
    retained_observe = next(item for item in ordinary_bindings
                            if item.identity.key.local == "BINDING(DF(observe))")
    retained_changes = next(item for item in ordinary_bindings
                            if item.identity.key.local == "BINDING(DF(changes_between))")
    confluence_nodes = (retained_observe.identity, retained_changes.identity)
    confluence_scope = (retained_observe.value.dependency_closure
                        | retained_changes.value.dependency_closure)
    confluence_target = next(iter(confluence_capability.value.supported_targets))
    confluence_descriptor_proper = frozenset({
        confluence_capability.value.service,
        confluence_capability.value.sound_fragment,
        confluence_capability.value.required_evidence,
        confluence_capability.value.failure_contract,
        *confluence_capability.value.required_trust_roots,
        confluence_target.semantic_environment,
        confluence_target.subjects[0].contract_identity,
    })
    confluence_capability = replace(
        confluence_capability,
        value=replace(
            confluence_capability.value,
            dependency_scope=confluence_scope,
            proper_semantic_dependencies=confluence_descriptor_proper,
            dependency_closure=(confluence_descriptor_proper
                                | confluence_scope
                                | frozenset(confluence_nodes))))
    canonical_task_binding = next(
        item for item in ordinary_bindings
        if item.identity.key.local == "BINDING(DP(task_accepts))")
    predicate_bindings = tuple(
        item for item in ordinary_bindings
        if item.value.binding_kind == "PREDICATE") + (occurrence,)
    occurrence_declaration = next(
        item.identity for item in symbols
        if item.identity.key.local == "DP(refresh_occurred)")
    predicate_targets = frozenset(
        BindingTarget(item.identity) for item in predicate_bindings)
    predicate_scope = frozenset().union(*(
        item.value.dependency_closure for item in predicate_bindings))
    predicate_roots = predicate_capability.value.required_trust_roots
    predicate_target_roots = frozenset(
        target.binding for target in predicate_targets)
    predicate_proper = frozenset({
        predicate_capability.value.service,
        predicate_capability.value.sound_fragment,
        predicate_capability.value.required_evidence,
        predicate_capability.value.failure_contract,
    }) | predicate_roots | predicate_target_roots
    predicate_descriptor_closure = predicate_proper | predicate_scope
    predicate_capability = replace(
        predicate_capability,
        value=replace(
            predicate_capability.value,
            supported_targets=predicate_targets,
            dependency_scope=predicate_scope,
            proper_semantic_dependencies=predicate_proper,
            dependency_closure=predicate_descriptor_closure))
    service_rows = (
        ("functions", "FSOUND", None, "FREQ", "FFAIL"),
        ("profile", "PROFSOUND", None, "PROFREQ", "PROFFAIL"),
        ("bounds", "BSOUND", "BCOMPLETE", "BREQ", "BFAIL"),
    )
    service_capabilities: list[LogicalRecord] = []
    service_support: list[LogicalRecord] = []
    for name, sound_local, complete_local, required_local, failure_local in service_rows:
        service_id = rid(RecordKind.SERVICE, f"SK({name})", namespace="coding.service")
        capability_id = rid(RecordKind.CAPABILITY, f"CAP({name})", namespace="coding.capability")
        sound_id = rid(RecordKind.CONTRACT_SPEC, sound_local, namespace="coding.service.contract")
        complete_id = (rid(RecordKind.CONTRACT_SPEC, complete_local,
                           namespace="coding.service.contract")
                       if complete_local is not None else None)
        required_id = rid(RecordKind.CONTRACT_SPEC, required_local, namespace="coding.service.contract")
        failure_id = rid(RecordKind.CONTRACT_SPEC, failure_local, namespace="coding.service.contract")
        service = LogicalRecord(service_id, ServiceIdentity(service_id.key, ABI0, package.value.plugin_key))
        sound_relation = ("function_sound_fragment"
                          if name == "functions" else f"{name}_sound_fragment")
        sound = LogicalRecord(sound_id, ContractSpec(sound_id.key, Layer.SERVICE, ContractRole.SOUND_FRAGMENT, ("ServiceAdmissionSubject",), frozenset({"IN_FRAGMENT", "OUTSIDE_FRAGMENT"}), (), frozenset(), sound_relation))
        required = LogicalRecord(required_id, ContractSpec(required_id.key, Layer.SERVICE, ContractRole.REQUIRED_EVIDENCE, ("ServiceAdmissionSubject", "EvidenceSet"), frozenset({"ADMISSIBLE", "INADMISSIBLE"}), (), frozenset(), f"{name}_required_evidence"))
        failure_codomain = {
            "functions": frozenset({"TermResult.TERM_ERROR"}),
            "profile": frozenset({"ProfileResult.EVALUATION_ERROR"}),
            "bounds": frozenset({"ReasoningResult.REASONING_ERROR"}),
        }[name]
        failure = LogicalRecord(failure_id, ContractSpec(failure_id.key, Layer.SERVICE, ContractRole.SERVICE_FAILURE_BEHAVIOR, ("InterfaceFailure",), failure_codomain, (), frozenset(), f"{name}_failure_projection"))
        proper = frozenset({service_id, sound_id, required_id, failure_id}
                           | ({complete_id} if complete_id is not None else set()))
        if name == "functions":
            targeted = tuple(item for item in ordinary_bindings
                             if item.identity.key.local in {
                                 "BINDING(DF(snapshot_of))",
                                 "BINDING(DF(changes_between))",
                                 "BINDING(DF(observe))"})
            service_role = "FUNCTION_EVALUATION"
            capability_class = "CONCRETE_EVALUATION_ONLY"
            judgments = frozenset({"FUNCTION_EVALUATION"})
            targets = frozenset(BindingTarget(item.identity) for item in targeted)
            dependency_scope = frozenset().union(
                *(item.value.dependency_closure for item in targeted))
            roots = frozenset({rid(RecordKind.TRUST_ROOT, "TR", namespace="trust")})
        elif name == "profile":
            service_role = "PROFILE_CONCRETE"
            capability_class = "CONCRETE_EVALUATION_ONLY"
            judgments = frozenset({"PROFILE_COVERAGE"})
            targets = frozenset({ProfileTarget(profile.value.profile_key)})
            dependency_scope = profile.value.dependency_closure
            roots = frozenset({rid(RecordKind.TRUST_ROOT, "TR", namespace="trust")})
        else:
            service_role = "REASONING"
            capability_class = "COMPLETE_FOR_DECLARED_FRAGMENT"
            judgments = frozenset({"CONSISTENCY"})
            targets = frozenset({ReasoningTarget(
                "CONSISTENCY",
                (rid(RecordKind.OUTCOME, "C_b", namespace="bounds.contract"),),
                rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_b",
                    namespace="bounds.environment"))})
            bounds_subjects = tuple(
                item for item in (*ordinary_bindings,
                                  *retained_literal_bindings)
                if item.identity.key.local in {
                    "BINDING(DF(snapshot_of))",
                    "BINDING(DP(task_accepts))",
                    "BINDING(L(T(TaskSpec),ts_nonempty))",
                    "BINDING(L(T(TaskSpec),ts_lt_100))",
                    "BINDING(L(T(TaskSpec),ts_ge_200))",
                })
            dependency_scope = frozenset().union(*(
                item.value.dependency_closure for item in bounds_subjects))
            roots = frozenset({rid(RecordKind.TRUST_ROOT, "TRB",
                                   namespace="bounds.trust")})
        target_roots = (frozenset(target.binding for target in targets)
                        if name == "functions"
                        else frozenset({profile.identity})
                        if name == "profile"
                        else frozenset({
                            next(iter(targets)).semantic_environment,
                            *next(iter(targets)).subjects,
                        }))
        descriptor_proper = proper | roots | target_roots
        descriptor_closure = (descriptor_proper | dependency_scope
                              if name != "bounds" else descriptor_proper)
        service_capabilities.append(LogicalRecord(capability_id, CapabilityDescriptor(
            capability_id.key, service_id, ABI0, package.value.plugin_key,
            service_role, capability_class, judgments,
            targets, sound_id, complete_id, dependency_scope,
            descriptor_proper, descriptor_closure,
            required_id, roots, failure_id)))
        service_support.extend((service, sound, required, failure))
        if complete_id is not None:
            service_support.append(LogicalRecord(complete_id, ContractSpec(
                complete_id.key, Layer.SERVICE, ContractRole.COMPLETE_FRAGMENT,
                ("ServiceAdmissionSubject",),
                frozenset({"IN_FRAGMENT", "OUTSIDE_FRAGMENT"}), (),
                frozenset(), f"{name}_complete")))
    lexical_service_id = rid(RecordKind.SERVICE, "LEXSK", namespace="coding.service")
    lexical_capability_id = rid(RecordKind.CAPABILITY, "LEX_CAP", namespace="coding.capability")
    lexical_spec_ids = tuple(
        rid(RecordKind.CONTRACT_SPEC, local, namespace="coding.service.contract")
        for local in ("LEX_SOUND", "LEX_REQ", "LEX_FAIL"))
    lexical_root = rid(RecordKind.TRUST_ROOT, "TR", namespace="trust")
    lexical_target = ReasoningTarget(
        "FORMULA_ENTAILMENT", ("f_lex", "g_lex"),
        rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_lex",
            namespace="lexical.environment"))
    lexical_scope = canonical_task_binding.value.dependency_closure
    lexical_proper = frozenset({
        lexical_service_id, *lexical_spec_ids, lexical_root,
        lexical_target.semantic_environment})
    lexical = LogicalRecord(lexical_capability_id, CapabilityDescriptor(
        lexical_capability_id.key, lexical_service_id, ABI0, package.value.plugin_key,
        "REASONING", "PARTIAL_SYMBOLIC_REASONING",
        frozenset({"FORMULA_ENTAILMENT"}), frozenset({lexical_target}), lexical_spec_ids[0],
        None, lexical_scope,
        lexical_proper, lexical_proper,
        lexical_spec_ids[1], frozenset({lexical_root}),
        lexical_spec_ids[2]))
    service_support.append(LogicalRecord(
        lexical_service_id, ServiceIdentity(lexical_service_id.key, ABI0, package.value.plugin_key)))
    lexical_shapes = (
        (ContractRole.SOUND_FRAGMENT, ("Formula", "Formula"),
         frozenset({"IN_FRAGMENT", "OUTSIDE_FRAGMENT"}),
         "formula_entailment_sound_fragment"),
        (ContractRole.REQUIRED_EVIDENCE, ("FormulaPair", "EvidenceSet"),
         frozenset({"ADMISSIBLE", "INADMISSIBLE"}),
         "formula_entailment_required_evidence"),
        (ContractRole.SERVICE_FAILURE_BEHAVIOR, ("InterfaceFailure",),
         frozenset({"ReasoningResult.REASONING_ERROR"}),
         "formula_entailment_failure_projection"),
    )
    for identity, (role, domain, codomain, relation) in zip(
            lexical_spec_ids, lexical_shapes, strict=True):
        service_support.append(LogicalRecord(identity, ContractSpec(
            identity.key, Layer.SERVICE, role, domain, codomain, (),
            frozenset(), relation)))
    function_capability = next(
        item for item in service_capabilities
        if item.identity.key.local == "CAP(functions)")
    function_targets = frozenset(
        item.identity for item in ordinary_bindings
        if item.value.binding_kind == "FUNCTION")
    predicate_binding_targets = frozenset(
        item.identity for item in predicate_bindings)
    def descriptor_summary(item: LogicalRecord) -> ModelCapabilitySummary:
        value = item.value
        assert isinstance(value, CapabilityDescriptor)
        return ModelCapabilitySummary(
            item.identity, value.service_role, value.supported_judgments,
            value.capability_class, value.sound_fragment,
            value.complete_fragment, value.dependency_scope)
    function_summary = descriptor_summary(function_capability)
    predicate_summary = descriptor_summary(predicate_capability)
    ordinary_models = tuple(
        replace(model, value=replace(
            model.value,
            capability_summaries=frozenset({
                function_summary if model.value.target_binding in function_targets
                else predicate_summary})))
        if model.value.target_binding in function_targets | predicate_binding_targets
        else model
        for model in ordinary_models)
    bcert_key = key("bundle_bounds_unsat",
                    owner="PLUGIN_CERTIFICATE_ISSUER(CK)",
                    namespace="coding.certificate")
    # A CertificateEnvelope is stored at its certificate key.  BENV is the
    # specification name of this value, not a second record identity.
    benv_id = RecordIdentity(RecordKind.CERTIFICATE, bcert_key)
    benv = LogicalRecord(benv_id, CertificateEnvelope(
        bcert_key, "CONTRADICTION_PROOF",
        rid(RecordKind.REQUEST, "R_b", namespace="bounds.request"),
        (rid(RecordKind.OUTCOME, "C_b", namespace="bounds.contract"),),
        rid(RecordKind.SEMANTIC_ENVIRONMENT, "E_b", namespace="bounds.environment"),
        rid(RecordKind.CAPABILITY, "CAP(bounds)", namespace="coding.capability"),
        rid(RecordKind.CONTRACT_SPEC, "BSOUND", namespace="coding.service.contract"),
        rid(RecordKind.DEPENDENCY_ENVIRONMENT, "D_b", namespace="bounds.environment"),
        "CONSISTENCY_UNSAT",
        rid(RecordKind.CAPABILITY, "CAP(validate_bounds)", namespace="coding.capability"),
        rid(RecordKind.TRUST_ROOT, "TRB", namespace="bounds.trust"),
        "SYMBOLIC", rid(RecordKind.EVIDENCE, "BundleBoundsProof", namespace="bounds.proof"),
        frozenset({rid(RecordKind.EVIDENCE, "BPROOF_REF", namespace="bounds.evidence")})))
    package_value = PluginPackage(
        abi_version=ABI0,
        plugin_key=package.value.plugin_key,
        owner=package.value.owner,
        declarations=_identity_union(retained_types, retained_literals, symbols),
        pair_declarations=pair_declarations,
        bindings=_identity_union(retained_literal_bindings, ordinary_bindings),
        pair_bindings=(pair_binding,),
        profile_bindings=(profile,),
        model_contracts=_identity_union(retained_literal_models, ordinary_models),
        aliases=(),
        services=_identity_union((predicate_capability, confluence_capability),
                                 tuple(service_capabilities), (lexical,)),
        certificates=(benv,),
        authority_facts=(), compatibility_claims=(), migrations=(),
        semantic_extensions=(),
    )
    retained_package = LogicalRecord(package.identity, package_value)
    literal_spec_ids = frozenset(item.identity for item in retained_literal_specs)
    ordinary_specs = tuple(item for item in ordinary_specs
                           if item.identity not in literal_spec_ids)
    ordinary_spec_ids = frozenset(item.identity for item in ordinary_specs)
    retained_csound = LogicalRecord(
        confluence_capability.value.sound_fragment,
        ContractSpec(
            confluence_capability.value.sound_fragment.key,
            Layer.SERVICE, ContractRole.SOUND_FRAGMENT,
            ("ServiceAdmissionSubject",),
            frozenset({"IN_FRAGMENT", "OUTSIDE_FRAGMENT"}),
            (
                ObservationQuery(retained_observe.identity,
                                 ObservationKind.TERM_RESULT,
                                 ("observation_spec", "final_snapshot")),
                ObservationQuery(retained_changes.identity,
                                 ObservationKind.TERM_RESULT,
                                 ("initial_snapshot", "final_snapshot")),
            ),
            frozenset(confluence_nodes), "confluence_sound_fragment"))
    support = _identity_union(
        retained_admissions, retained_literal_specs, ordinary_specs,
        tuple(service_support), (occurrence, retained_csound), tuple(
            item for item in core_records.records
            if (item.identity.kind is RecordKind.SERVICE
                or (item.identity.kind is RecordKind.CONTRACT_SPEC
                    and item.identity.key.namespace != "coding.type.contract"
                    and item.identity not in literal_spec_ids | ordinary_spec_ids))
        ), tuple(
            item for item in confluence.manifest
            if (item.identity.kind is RecordKind.SERVICE
                or (item.identity.kind is RecordKind.CONTRACT_SPEC
                    and item.identity.key.namespace != "coding.type.contract"
                    and item.identity not in literal_spec_ids | ordinary_spec_ids
                    and item.identity != retained_csound.identity))
        ))
    if (len(package_value.declarations), len(retained_literals), len(symbols),
            len(package_value.bindings), len(package_value.model_contracts),
            len(package_value.services)) != (119, 47, 17, 57, 58, 6):
        raise ValueError("literal PKG_CK cardinality disagreement")
    _RETAINED_CK_CACHE = retained_package, support
    return _RETAINED_CK_CACHE


def _install_retained_package(
    universe: Universe,
    package: LogicalRecord,
    support: tuple[LogicalRecord, ...],
) -> Universe:
    local_package = next(
        item for item in universe.records if isinstance(item.value, PluginPackage))
    canonical_identities = frozenset(
        {package.identity, *(item.identity for item in package.value.members()),
         *(item.identity for item in support)})
    retained_records = tuple(
        item for item in universe.records
        if item.identity != local_package.identity
        and item.identity not in canonical_identities)
    retained_records = tuple(
        item for item in retained_records
        if item.identity.key.namespace != "coding.type.contract"
        and not (item.identity.kind is RecordKind.TYPE_DECLARATION
                 and item.identity.key.local in {"TaskSpec", "RepositorySnapshot"}))
    records = _identity_union(retained_records, (package,), support)
    return replace(universe, records=records)


def core_construction(
    trust_tag: TrustFixtureTag = TrustFixtureTag.ADMITTED,
) -> CoreConstruction:
    local = _core_construction_local(trust_tag)
    package, support = _retained_ck()
    universe = _install_retained_package(local.universe, package, support)
    composition = compose_records(universe.records)
    frozen_values = {
        local_name: value
        for _, local_name, value in _retained_literal_values()
    }
    frozen_task = frozen_values["t_t"]
    frozen_snapshot = frozen_values["F_c"]
    frozen_evidence: frozenset[CodingEvidenceEntry] = frozenset()
    frozen_observation_spec = next(iter(frozen_task.criteria)).spec
    frozen_observation = cp.observe(
        frozen_observation_spec, frozen_snapshot).value
    diagnostic_verification_spec = cp.VerificationSpec(
        "v_final", frozen_observation_spec, cp.VERIFICATION_SCHEMA)
    diagnostic_evidence_ref = cp.EvidenceRef(
        "auditor", "coding", "verification/final", cp.VERIFICATION_SCHEMA)
    diagnostic_verification = cp.VerificationRecord(
        diagnostic_verification_spec, cp.SnapshotIdentity(frozen_snapshot),
        cp.VerificationStatus.PASS, frozen_observation,
        frozenset({diagnostic_evidence_ref}))
    diagnostic_evidence = frozenset({cp.CodingEvidenceEntry(
        diagnostic_evidence_ref, cp.CodingEvidencePayload(
            cp.EvidencePayloadTag.VERIFICATION, diagnostic_verification))})
    semantic_record = composition.at(local.semantic_environment)
    dependency_record = composition.at(local.dependency_environment)
    assert semantic_record is not None and dependency_record is not None
    binding_record = next(
        item for item in package.value.bindings
        if item.identity.key.local == "BINDING(DP(task_accepts))")
    declaration_record = next(
        item for item in package.value.declarations
        if item.identity.key.local == "DP(task_accepts)")
    required_type_names = {
        "TaskSpec", "RepositorySnapshot", "CodingEvidenceEntry"}
    pending = list(required_type_names)
    while pending:
        for name in _RETAINED_TYPE_DEPENDENCIES[pending.pop()]:
            if name not in required_type_names:
                required_type_names.add(name)
                pending.append(name)
    delta_declarations = tuple(sorted((
        *(item.identity for item in package.value.declarations
          if item.identity.kind is RecordKind.TYPE_DECLARATION
          and item.identity.key.local[2:-1] in required_type_names),
        declaration_record.identity,
    )))
    frozen_required = frozen_task_syntax_roots()
    rebuilt_semantic = replace(
        semantic_record,
        value=SemanticEnvironment(
            ABI0, delta_declarations, (), (binding_record.identity,),
            mechanically_extracted_dependencies=frozen_required))
    syntax = frozen_task_syntax_roots()
    subjects = frozenset({binding_record.identity})
    associations = frozenset({(declaration_record.identity,
                                binding_record.identity)})
    proper = binding_record.value.proper_semantic_dependencies
    from .reference import _reachable_closure
    rebuilt_dependency = replace(
        dependency_record,
        value=DependencyEnvironment(
            syntax, subjects, associations, syntax | subjects, proper,
            _reachable_closure(proper, composition),
            dependency_record.value.validation_references))
    request_record = composition.at(local.request)
    assert request_record is not None and isinstance(request_record.value, InvocationRequest)
    rebuilt_request = replace(
        request_record,
        value=replace(request_record.value,
                      target=declaration_record.identity,
                      arguments=(frozen_task, frozen_snapshot, frozen_evidence)))
    result_record = composition.at(local.result)
    rebuilt_result = None if result_record is None else replace(
        result_record,
        value=ResultRecord(local.request, "Eval", Eval(Truth.TRUE)))
    capability_record = composition.at(local.capability)
    root_record = composition.at(local.trust_root)
    trust_record = composition.at(local.trust_environment)
    assert capability_record is not None and root_record is not None and trust_record is not None
    frozen_use = ServiceUseTrustTarget(
        capability_record.identity, "PREDICATE_EVALUATION",
        binding_record.identity, rebuilt_semantic.identity)
    rebuilt_root = replace(
        root_record,
        value=replace(root_record.value, permitted_targets=frozenset({frozen_use})))
    judgments = tuple(
        (root, TrustRootJudgment(judgment.state,
             rebuilt_root.value if judgment.state is TrustState.ADMITTED else None,
             judgment.reasons))
        for root, judgment in trust_record.value.root_judgments)
    rebuilt_trust = replace(
        trust_record, value=replace(trust_record.value, root_judgments=judgments))
    replacements = {
        rebuilt_semantic.identity: rebuilt_semantic,
        rebuilt_dependency.identity: rebuilt_dependency,
        rebuilt_request.identity: rebuilt_request,
        rebuilt_root.identity: rebuilt_root,
        rebuilt_trust.identity: rebuilt_trust,
    }
    if rebuilt_result is not None:
        replacements[rebuilt_result.identity] = rebuilt_result
    universe = replace(
        universe,
        records=tuple(replacements.get(item.identity, item)
                      for item in universe.records))
    manifest = frozenset(compose_records(universe.records).records)
    return replace(
        local, universe=universe, manifest=manifest,
        snapshot=frozen_snapshot, task=frozen_task, evidence=diagnostic_evidence)


def confluence_construction(order: OrderTag) -> ConfluenceConstruction:
    local = _confluence_construction_local(order)
    package, support = _retained_ck()
    universe = _install_retained_package(local.universe, package, support)
    composition = compose_records(universe.records)
    retained_nodes = tuple(
        next(item.identity for item in package.value.bindings
             if item.identity.key.local == local_id.key.local)
        for local_id in (local.node_one, local.node_two))
    retained_predicates = tuple(
        next(item.identity for item in package.value.bindings
             if item.identity.key.local == local)
        for local in (
            "BINDING(DP(observations_equal))",
            "BINDING(DP(dependency_metadata_changed))",
        ))
    retained_subjects = retained_nodes + retained_predicates
    graph_request = universe.request
    assert isinstance(graph_request, GraphEvaluationRequest)
    reasoning = composition.at(graph_request.reasoning_request)
    assert reasoning is not None and isinstance(reasoning.value, ReasoningRequest)
    subject = reasoning.value.subjects[0]
    assert isinstance(subject, ConfluenceSubject)
    literal_values = (subject.observation_spec, subject.prior_snapshot,
                      subject.final_snapshot,
                      cp.observe(subject.observation_spec,
                                 subject.final_snapshot).value)
    literal_declarations = tuple(
        item for item in package.value.declarations
        if isinstance(item.value, DeclarationShape)
        and item.value.declaration_kind == "LITERAL"
        and any(item.value.literal_value == value for value in literal_values))
    selected_declaration_ids = {
        item.value.declaration for item in package.value.bindings
        if item.identity in retained_subjects
    } | {item.identity for item in literal_declarations}
    pending = list(selected_declaration_ids)
    while pending:
        declaration_identity = pending.pop()
        declaration_record = composition.at(declaration_identity)
        if declaration_record is None:
            continue
        dependencies = (
            declaration_record.value.proper_declaration_dependencies
            if isinstance(declaration_record.value, TypeDeclaration)
            else declaration_record.value.proper_type_dependencies
            if isinstance(declaration_record.value, DeclarationShape)
            else frozenset())
        for dependency_identity in dependencies:
            dependency_record = composition.at(dependency_identity)
            if (dependency_record is not None
                    and isinstance(dependency_record.value, TypeDeclaration)
                    and dependency_identity not in selected_declaration_ids):
                selected_declaration_ids.add(dependency_identity)
                pending.append(dependency_identity)
    selected_bindings = tuple(
        item for item in package.value.bindings
        if item.identity in retained_subjects
        or (isinstance(item.value, SemanticBinding)
            and item.value.declaration in {row.identity for row in literal_declarations}))
    selected_binding_ids = tuple(item.identity for item in selected_bindings)
    selected_declarations = tuple(sorted(selected_declaration_ids))
    semantic_record = composition.at(graph_request.semantic_environment)
    dependency_record = composition.at(graph_request.dependency_environment)
    observation_record = composition.at(graph_request.observation_environment)
    assert semantic_record and dependency_record and observation_record
    semantic_value = semantic_record.value
    assert isinstance(semantic_value, SemanticEnvironment)
    rebuilt_semantic = replace(
        semantic_record,
        value=SemanticEnvironment(
            ABI0, selected_declarations, (), selected_binding_ids,
            authority_facts=semantic_value.authority_facts,
            mechanically_extracted_dependencies=frozen_confluence_syntax_roots()))
    associations = frozenset(
        (item.value.declaration, item.identity) for item in selected_bindings)
    proper = frozenset().union(*(
        item.value.proper_semantic_dependencies for item in selected_bindings))
    from .reference import _reachable_closure
    rebuilt_dependency = replace(
        dependency_record,
        value=DependencyEnvironment(
            frozen_confluence_syntax_roots(), frozenset(selected_binding_ids),
            associations,
            frozen_confluence_syntax_roots() | frozenset(selected_binding_ids),
            proper, _reachable_closure(proper, composition), frozenset()))
    observation_values = dict(observation_record.value.values)
    rebuilt_observation = replace(
        observation_record,
        value=ObservationEnvironment(tuple(sorted(
            (new, observation_values[old])
            for old, new in zip((local.node_one, local.node_two),
                                retained_nodes, strict=True)))))
    rewritten_records = tuple(
        rebuilt_semantic if item.identity == rebuilt_semantic.identity
        else rebuilt_dependency if item.identity == rebuilt_dependency.identity
        else rebuilt_observation if item.identity == rebuilt_observation.identity
        else item
        for item in universe.records
        if not (item.identity.key.namespace in {
            "confluence.binding", "confluence.declaration", "confluence.model"}
            or (isinstance(item.value, ContractSpec)
                and item.identity.key.namespace == "confluence.contract")))
    preliminary = replace(universe, records=rewritten_records)
    preliminary_composition = compose_records(preliminary.records)
    package_record = next(
        item for item in preliminary.records
        if isinstance(item.value, PluginPackage))
    confluence_descriptor = next(
        item for item in package_record.value.services
        if item.identity.key.local == "CAP(confluence)")
    exact_descriptor = replace(
        confluence_descriptor,
        value=replace(
            confluence_descriptor.value,
            dependency_closure=_reachable_closure(
                confluence_descriptor.value.proper_semantic_dependencies,
                preliminary_composition)))
    exact_package = replace(
        package_record,
        value=replace(
            package_record.value,
            services=tuple(
                exact_descriptor if item.identity == exact_descriptor.identity
                else item
                for item in package_record.value.services)))
    rewritten_records = tuple(
        exact_package if item.identity == exact_package.identity else item
        for item in rewritten_records)
    observation_inputs = tuple(
        (new, arguments) for (old, arguments), new in zip(
            graph_request.observation_inputs, retained_nodes, strict=True))
    preferred = retained_nodes if order is OrderTag.FORWARD else retained_nodes[::-1]
    rebuilt_request = replace(
        graph_request, nodes=retained_nodes, preferred_order=preferred,
        observation_inputs=observation_inputs)
    universe = replace(universe, records=rewritten_records, request=rebuilt_request)
    return replace(
        local, universe=universe,
        manifest=frozenset(compose_records(universe.records).records),
        node_one=retained_nodes[0], node_two=retained_nodes[1])


def cycle_universe(cyclic: bool = True) -> Universe:
    retained_package, retained_support = _retained_ck()
    matches = next(item for item in retained_package.value.bindings
                   if item.identity.key.local == "BINDING(DP(event_matches))")
    occurred = next(item for item in retained_package.value.bindings
                    if item.identity.key.local == "BINDING(DP(event_occurred))")
    abi = record(RecordKind.ABI, "ABI0", AbiRecord(ABI0), namespace="abi", version=ABI0)
    package = retained_package
    support = retained_support
    if cyclic:
        cycle_spec_id = rid(
            RecordKind.CONTRACT_SPEC,
            "CS(PREDICATE_MEANING,event_matches_cycle)",
            namespace="coding.contract")
        cycle_spec = LogicalRecord(cycle_spec_id, ContractSpec(
            cycle_spec_id.key, Layer.SIGMA, ContractRole.PREDICATE_MEANING,
            ("T(EventPattern)", "EventValue"), frozenset({"Eval"}),
            (ObservationQuery(occurred.identity, ObservationKind.EVAL_RESULT,
                              ("pattern", "singleton_trace(event)")),),
            frozenset({occurred.identity}), "event_matches_cycle"))
        cycle_access = next(
            item for item in retained_support
            if item.identity == matches.value.access_boundary)
        cycle_access = replace(
            cycle_access,
            value=replace(
                cycle_access.value,
                observation_queries=(ObservationQuery(
                    occurred.identity, ObservationKind.EVAL_RESULT,
                    ("pattern", "singleton_trace(event)")),),
                support=frozenset({occurred.identity})))
        direct = ((matches.value.proper_semantic_dependencies
                   - frozenset({matches.value.meaning_contract}))
                  | frozenset({cycle_spec_id, occurred.identity}))
        reachability = (direct | occurred.value.proper_semantic_dependencies
                        | matches.value.dependency_closure
                        | frozenset({matches.identity, occurred.identity,
                                     cycle_spec_id})) - frozenset({
                                         matches.value.meaning_contract})
        changed_matches = replace(
            matches, value=replace(matches.value, meaning_contract=cycle_spec_id,
                                   proper_semantic_dependencies=direct,
                                   dependency_closure=reachability))
        changed_models = tuple(
            replace(
                model,
                value=replace(
                    model.value,
                    semantic_contract=(
                        cycle_spec_id
                        if model.value.target_binding == matches.identity
                        else model.value.semantic_contract),
                    capability_summaries=frozenset()))
            if (model.value.target_binding == matches.identity
                or (model.identity.key.namespace == "coding.model"
                    and not model.identity.key.local.startswith("MODEL_LITERAL(")))
            else model
            for model in retained_package.value.model_contracts)
        package = replace(
            retained_package,
            value=replace(
                retained_package.value,
                bindings=tuple(
                    changed_matches if item.identity == matches.identity
                    else item for item in retained_package.value.bindings),
                model_contracts=changed_models, services=(), certificates=()))
        support = tuple(
            item for item in retained_support
            if item.identity not in {
                matches.value.meaning_contract, matches.value.access_boundary
            }) + (cycle_spec, cycle_access)
    environment = record(
        RecordKind.SEMANTIC_ENVIRONMENT,
        "E_PROPER_CYCLE",
        SemanticEnvironment(
            ABI0,
            tuple(item.identity for item in package.value.declarations),
            tuple(item.identity for item in package.value.pair_declarations),
            tuple(item.identity for item in package.value.bindings),
            profile_bindings=tuple(item.identity for item in package.value.profile_bindings),
            pair_bindings=tuple(item.identity for item in package.value.pair_bindings),
            authority_facts=tuple(item.identity for item in package.value.authority_facts),
            semantic_extensions=tuple(item.identity for item in package.value.semantic_extensions),
            mechanically_extracted_dependencies=frozenset({matches.identity}),
        ), namespace="cycle.environment")
    return Universe(
        _identity_union((abi, package, environment), support),
        FormationRequest((matches.identity, occurred.identity)))


LITERAL_MISSING_ROWS = _literal_missing_rows()
LITERAL_MISSING_BY_ID = {item.row: item for item in LITERAL_MISSING_ROWS}
MISSING_LITERAL_IDENTITIES = {
    item.row: item.target for item in LITERAL_MISSING_ROWS
}


PERMUTATION_TYPE_NAMES = (
    "fixture_unit_one",
    "fixture_unit_two",
    "fixture_unit_three",
    "fixture_unit_four",
)


def _literal_permutation_records() -> tuple[
    LogicalRecord,
    LogicalRecord,
    tuple[LogicalRecord, LogicalRecord],
    tuple[LogicalRecord, LogicalRecord],
    tuple[LogicalRecord, LogicalRecord],
    tuple[LogicalRecord, LogicalRecord],
]:
    abi = record(
        RecordKind.ABI,
        "ABI0",
        AbiRecord(ABI0),
        namespace="abi",
        version=ABI0,
    )
    owners = (
        "capknow.fixture.permutation-one",
        "capknow.fixture.permutation-one",
        "capknow.fixture.permutation-two",
        "capknow.fixture.permutation-two",
    )
    pairs: list[tuple[LogicalRecord, LogicalRecord]] = []
    for name, owner in zip(PERMUTATION_TYPE_NAMES, owners, strict=True):
        type_id = rid(
            RecordKind.TYPE_DECLARATION,
            f"T({name})",
            owner=owner,
            namespace="coding.fixture.type",
        )
        admission_id = rid(
            RecordKind.CONTRACT_SPEC,
            f"A({name})",
            owner=owner,
            namespace="coding.fixture.type-admission",
        )
        admission = LogicalRecord(
            admission_id,
            ContractSpec(
                admission_id.key,
                Layer.DELTA,
                ContractRole.TYPE_ADMISSION,
                ("Value",),
                frozenset({"admitted", "not_admitted"}),
                (),
                frozenset(),
                f"admit_UNIT_{name}",
                TypeAdmissionRelation(str),
            ),
        )
        declaration = LogicalRecord(
            type_id,
            TypeDeclaration(
                type_id.key,
                admission.value,
                frozenset({admission_id}),
            ),
        )
        pairs.append((declaration, admission))
    package_one = _package(
        "permutation-one",
        "capknow.fixture.permutation-one",
        declarations=(pairs[0][0], pairs[1][0]),
        specs=(pairs[0][1], pairs[1][1]),
    )
    package_two = _package(
        "permutation-two",
        "capknow.fixture.permutation-two",
        declarations=(pairs[2][0], pairs[3][0]),
        specs=(pairs[2][1], pairs[3][1]),
    )
    return abi, package_one, package_two, pairs[0], pairs[1], pairs[2], pairs[3]


(
    PI_ABI,
    PI_PACKAGE_ONE,
    PI_PACKAGE_TWO,
    PI_PAIR_11,
    PI_PAIR_12,
    PI_PAIR_21,
    PI_PAIR_22,
) = _literal_permutation_records()


def permutation_universe(
    package_order: PackageOrderTag, record_order: RecordOrderTag
) -> Universe:
    package_sequence = (
        (PI_PACKAGE_ONE, PI_PACKAGE_TWO)
        if package_order is PackageOrderTag.PI1_PI2
        else (PI_PACKAGE_TWO, PI_PACKAGE_ONE)
    )
    first_members = (
        (*PI_PAIR_11, *PI_PAIR_12)
        if record_order is RecordOrderTag.DECLARATION_THEN_SPEC
        else (
            PI_PAIR_12[1],
            PI_PAIR_12[0],
            PI_PAIR_11[1],
            PI_PAIR_11[0],
        )
    )
    second_members = (
        (*PI_PAIR_21, *PI_PAIR_22)
        if record_order is RecordOrderTag.DECLARATION_THEN_SPEC
        else (
            PI_PAIR_22[1],
            PI_PAIR_22[0],
            PI_PAIR_21[1],
            PI_PAIR_21[0],
        )
    )
    first_presentation = (
        PI_ABI,
        PI_PACKAGE_ONE,
        *first_members,
    )
    second_presentation = (
        PI_ABI,
        PI_PACKAGE_TWO,
        *second_members,
    )
    record_presentations = (
        (first_presentation, second_presentation)
        if package_order is PackageOrderTag.PI1_PI2
        else (second_presentation, first_presentation)
    )
    package_presentation = (PI_ABI, *package_sequence)
    marker = record(
        RecordKind.PRESENTATION,
        f"PERMUTATION({package_order.value},{record_order.value})",
        NamedCarrier("PERMUTATION_PRESENTATION"),
        namespace="permutation",
    )
    return Universe(
        (marker,),
        CompositionRequest((package_presentation, *record_presentations)),
    )


DUPLICATE_TYPE_NAMES = (
    "PathSegment",
    "Path",
    "PathSet",
    "ArtifactRole",
    "Format",
    "ByteSize",
    "ContentIdentity",
    "FieldId",
    "FieldValue",
    "SubjectId",
    "BehaviorValue",
    "ArtifactBodyKind",
    "ArtifactContent",
    "ArtifactSelector",
    "ArtifactProjection",
    "Coverage",
    "ObservationSpec",
    "ObservationValue",
    "ObservationResult",
    "ObservationRelation",
    "VerificationSpec",
    "Criterion",
    "TaskSpec",
    "RepositorySnapshot",
)

DUPLICATE_TYPE_DEPENDENCIES = {
    "PathSegment": (), "Path": ("PathSegment",), "PathSet": ("Path",),
    "ArtifactRole": (), "Format": (), "ByteSize": (), "ContentIdentity": (),
    "FieldId": (), "FieldValue": (), "SubjectId": (),
    "BehaviorValue": ("ContentIdentity", "FieldId", "FieldValue"),
    "ArtifactBodyKind": (),
    "ArtifactContent": ("ArtifactRole", "Format", "ByteSize", "ContentIdentity", "FieldId", "FieldValue", "SubjectId", "BehaviorValue"),
    "ArtifactSelector": ("PathSet", "ArtifactRole"),
    "ArtifactProjection": ("FieldId",), "Coverage": ("SubjectId",),
    "ObservationSpec": ("ArtifactSelector", "ArtifactProjection", "SubjectId", "FieldId"),
    "ObservationValue": ("ArtifactRole", "ArtifactBodyKind", "ArtifactProjection", "ArtifactContent", "BehaviorValue", "Format", "ByteSize", "FieldId", "FieldValue", "ContentIdentity"),
    "ObservationResult": ("Path", "SubjectId", "Coverage", "ObservationSpec", "ObservationValue"),
    "ObservationRelation": ("FieldId",),
    "VerificationSpec": ("ObservationSpec",),
    "Criterion": ("ObservationSpec", "ObservationResult", "ArtifactSelector", "ByteSize", "Format", "ObservationRelation"),
    "TaskSpec": ("Criterion", "VerificationSpec"),
    "RepositorySnapshot": ("Path", "ArtifactContent"),
}


def _literal_duplicate_context() -> tuple[
    LogicalRecord,
    LogicalRecord,
    tuple[LogicalRecord, ...],
    tuple[LogicalRecord, ...],
    LogicalRecord,
    LogicalRecord,
]:
    abi = record(
        RecordKind.ABI,
        "ABI0",
        AbiRecord(ABI0),
        namespace="abi",
        version=ABI0,
    )
    declarations: list[LogicalRecord] = []
    admissions: list[LogicalRecord] = []
    for name in DUPLICATE_TYPE_NAMES:
        type_id = rid(
            RecordKind.TYPE_DECLARATION,
            f"T({name})",
            namespace="coding.type",
        )
        admission_id = rid(
            RecordKind.CONTRACT_SPEC,
            f"CS(TYPE_ADMISSION,type.{name})",
            namespace="coding.type-admission",
        )
        nested = frozenset(
            rid(RecordKind.TYPE_DECLARATION, f"T({dependency})", namespace="coding.type")
            for dependency in DUPLICATE_TYPE_DEPENDENCIES[name]
        )
        admissions.append(
            LogicalRecord(
                admission_id,
                ContractSpec(
                    admission_id.key,
                    Layer.DELTA,
                    ContractRole.TYPE_ADMISSION,
                    ("Value",),
                    frozenset({"admitted", "not_admitted"}),
                    tuple(
                        ObservationQuery(dependency, ObservationKind.TYPE_ADMISSION_FACT, ("nested_value",))
                        for dependency in sorted(nested)
                    ),
                    nested,
                    f"admit_{name}",
                    TypeAdmissionRelation(admission_type(name)),
                ),
            )
        )
        declarations.append(
            LogicalRecord(
                type_id,
                TypeDeclaration(
                    type_id.key,
                    admissions[-1].value,
                    nested | frozenset({admission_id}),
                ),
            )
        )
    package = _package(
        "coding-minimal",
        "capknow.semantic",
        declarations=tuple(declarations),
        specs=tuple(admissions),
    )
    task_type = next(
        item for item in declarations if item.identity.key.local == "T(TaskSpec)"
    )
    snapshot_type = next(
        item
        for item in declarations
        if item.identity.key.local == "T(RepositorySnapshot)"
    )
    declaration_id = rid(
        RecordKind.DECLARATION,
        "DP(task_accepts)",
        namespace="coding.declaration",
    )
    declaration = LogicalRecord(
        declaration_id,
        DeclarationShape(
            declaration_id.key,
            key("SP(task_accepts)", namespace="coding.symbol"),
            "PREDICATE",
            (
                task_type.identity.key,
                snapshot_type.identity.key,
                key("EvidenceStore", namespace="carrier.type"),
            ),
            "BOOL",
            (
                frozenset(),
                frozenset({"final"}),
                frozenset({"evidence"}),
            ),
            frozenset({task_type.identity, snapshot_type.identity}),
        ),
    )
    bad = replace(
        declaration,
        value=replace(
            declaration.value,
            facet_positions=(
                frozenset(),
                frozenset({"final"}),
                frozenset(),
            ),
        ),
    )
    return (
        abi,
        package,
        tuple(declarations),
        tuple(admissions),
        declaration,
        bad,
    )


(
    DUPLICATE_ABI,
    DUPLICATE_PACKAGE,
    DUPLICATE_TYPE_DECLARATIONS,
    DUPLICATE_TYPE_ADMISSIONS,
    DUPLICATE_DECLARATION,
    DUPLICATE_BAD_DECLARATION,
) = _literal_duplicate_context()
DUPLICATE_DECLARATION_COPY = replace(
    DUPLICATE_DECLARATION,
    value=replace(DUPLICATE_DECLARATION.value),
)


def duplicate_universe(conflict: bool, order: OrderTag) -> Universe:
    context = (
        DUPLICATE_ABI,
        DUPLICATE_PACKAGE,
        *DUPLICATE_TYPE_DECLARATIONS,
        *DUPLICATE_TYPE_ADMISSIONS,
    )
    second = (
        DUPLICATE_BAD_DECLARATION
        if conflict
        else DUPLICATE_DECLARATION_COPY
    )
    pair = (
        (DUPLICATE_DECLARATION, second)
        if order is OrderTag.FORWARD
        else (second, DUPLICATE_DECLARATION)
    )
    presentation = (
        (*context, *pair)
        if order is OrderTag.FORWARD
        else (*pair, *tuple(reversed(context)))
    )
    marker = record(
        RecordKind.PRESENTATION,
        f"DUPLICATE({conflict},{order.value})",
        NamedCarrier("DUPLICATE_PRESENTATION"),
        namespace="duplicate",
    )
    return Universe((marker,), CompositionRequest((presentation,)))


def _build_fixture_packet() -> dict[FixtureId, Universe]:
    packet: dict[FixtureId, Universe] = {}

    core = core_construction()
    core_id = FixtureId(FixtureFamily.CORE_DEFINITIONAL)
    packet[core_id] = core.universe

    pair = pair_construction()
    pair_id = FixtureId(FixtureFamily.PAIR_INDEPENDENT)
    packet[pair_id] = pair.universe

    for tag in TrustFixtureTag:
        construction = core_construction(tag)
        fixture_id = FixtureId(FixtureFamily.TRUST_BRANCH, (tag,))
        packet[fixture_id] = construction.universe

    for spec in LITERAL_MISSING_ROWS:
        construction = missing_construction(spec.row)
        base_id = FixtureId(FixtureFamily.MISSING_BASE, (spec.row,))
        variant_id = FixtureId(FixtureFamily.MISSING_VARIANT, (spec.row,))
        packet[base_id] = construction.baseline
        packet[variant_id] = construction.variant

    for order in OrderTag:
        construction = confluence_construction(order)
        fixture_id = FixtureId(FixtureFamily.CONFLUENCE_ORDER, (order,))
        packet[fixture_id] = construction.universe

    cycle_id = FixtureId(FixtureFamily.PROPER_CYCLE_REJECTION)
    packet[cycle_id] = cycle_universe()

    for package_order in PackageOrderTag:
        for record_order in RecordOrderTag:
            fixture_id = FixtureId(
                FixtureFamily.PERMUTATION, (package_order, record_order)
            )
            packet[fixture_id] = permutation_universe(
                package_order, record_order
            )

    for order in OrderTag:
        equal_id = FixtureId(FixtureFamily.DUPLICATE_EQUAL, (order,))
        conflict_id = FixtureId(FixtureFamily.DUPLICATE_CONFLICT, (order,))
        packet[equal_id] = duplicate_universe(False, order)
        packet[conflict_id] = duplicate_universe(True, order)

    return packet


_FIXTURE_PACKET = _build_fixture_packet()
# Independently frozen assertion-only identity catalog.  None of these
# atoms is obtained from a fixture, manifest, request, result, or replay.
_EI_000_ABI0: IdentityLiteral = ('ABI_RECORD', 'capknow.semantic', 'abi', 'ABI0', (0,))
_EI_001_AK0: IdentityLiteral = ('ALIAS_RECORD', 'capknow.fixture.evolution-owner', 'evolution.alias', 'AK0', (1,))
_EI_002_AK1: IdentityLiteral = ('ALIAS_RECORD', 'capknow.fixture.evolution-owner', 'evolution.alias', 'AK1', (1,))
_EI_003_AF_choice_1: IdentityLiteral = ('AUTHORITY_FACT_RECORD', 'capknow.semantic', 'authority', 'AF(choice,1)', (1,))
_EI_004_AUTH_choice_1: IdentityLiteral = ('AUTHORITY_REF_RECORD', 'capknow.semantic', 'authority.ref', 'AUTH(choice,1)', (1,))
_EI_005_BINDING_DP_task_accepts: IdentityLiteral = ('BINDING_RECORD', 'capknow.semantic', 'coding.binding', 'BINDING(DP(task_accepts))', (1,))
_EI_006_B_alt_refresh_occurred: IdentityLiteral = ('BINDING_RECORD', 'capknow.semantic', 'coding.binding', 'B_alt(refresh_occurred)', (1,))
_EI_007_B_alt_refresh_scope: IdentityLiteral = ('BINDING_RECORD', 'capknow.semantic', 'coding.binding', 'B_alt(refresh_scope)', (1,))
_EI_008_BINDING_DF_changes_between: IdentityLiteral = ('BINDING_RECORD', 'capknow.semantic', 'confluence.binding', 'BINDING(DF(changes_between))', (1,))
_EI_009_BINDING_DF_observe: IdentityLiteral = ('BINDING_RECORD', 'capknow.semantic', 'confluence.binding', 'BINDING(DF(observe))', (1,))
_EI_010_BINDING_DP_event_matches: IdentityLiteral = ('BINDING_RECORD', 'capknow.semantic', 'cycle.binding', 'BINDING(DP(event_matches))', (1,))
_EI_011_BINDING_DP_event_occurred: IdentityLiteral = ('BINDING_RECORD', 'capknow.semantic', 'cycle.binding', 'BINDING(DP(event_occurred))', (1,))
_EI_012_PVC: IdentityLiteral = ('CAPABILITY_RECORD', 'capknow.audit.pair-validator', 'coding.validation.capability', 'refresh_full_eval', (1,))
_EI_013_CAP_confluence: IdentityLiteral = ('CAPABILITY_RECORD', 'capknow.semantic', 'coding.capability', 'CAP(confluence)', (1,))
_EI_014_CAP_predicates: IdentityLiteral = ('CAPABILITY_RECORD', 'capknow.semantic', 'coding.capability', 'CAP(predicates)', (1,))
_EI_015_PCERT: IdentityLiteral = ('CERTIFICATE_RECORD', 'capknow.audit.pair-proof', 'pair.certificate', 'PCERT', (1,))
_EI_016_cb0: IdentityLiteral = ('CHOICE_BINDING_RECORD', 'capknow.semantic', 'authority.choice', 'cb0', (1,))
_EI_017_CCK0: IdentityLiteral = ('COMPATIBILITY_RECORD', 'capknow.fixture.evolution-owner', 'evolution', 'CCK0', (1,))
_EI_018_conflict0: IdentityLiteral = ('CONFLICT_RECORD', 'capknow.semantic', 'conflict', 'conflict0', (1,))
_EI_019_conflict1: IdentityLiteral = ('CONFLICT_RECORD', 'capknow.semantic', 'conflict', 'conflict1', (1,))
_EI_020_PCOMPLETE: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.audit.pair-validator', 'pair.contract', 'PCOMPLETE', (1,))
_EI_021_PEVIDENCE: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.audit.pair-validator', 'pair.contract', 'PEVIDENCE', (1,))
_EI_022_PFAILURE: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.audit.pair-validator', 'pair.contract', 'PFAILURE', (1,))
_EI_023_PSOUND: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.audit.pair-validator', 'pair.contract', 'PSOUND', (1,))
_EI_024_A_fixture_unit_one: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.fixture.permutation-one', 'coding.fixture.type-admission', 'A(fixture_unit_one)', (1,))
_EI_025_A_fixture_unit_two: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.fixture.permutation-one', 'coding.fixture.type-admission', 'A(fixture_unit_two)', (1,))
_EI_026_A_fixture_unit_four: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.fixture.permutation-two', 'coding.fixture.type-admission', 'A(fixture_unit_four)', (1,))
_EI_027_A_fixture_unit_three: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.fixture.permutation-two', 'coding.fixture.type-admission', 'A(fixture_unit_three)', (1,))
_EI_028_CS_ACCESS_BOUNDARY_task_final_evidence: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'CS(ACCESS_BOUNDARY,task_final_evidence)', (1,))
_EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'CS(EVALUATION_ERROR_BEHAVIOR,predicate)', (1,))
_EI_030_CS_EVIDENCE_SCHEMA_verification: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'CS(EVIDENCE_SCHEMA,verification)', (1,))
_EI_031_CS_PREDICATE_MEANING_observations_equal: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'CS(PREDICATE_MEANING,task_accepts_wrong)', (1,))
_EI_032_CS_PREDICATE_MEANING_refresh_occurred: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'T3_A1_MEANING_LIFT(pd,sb)', (1,))
_EI_033_CS_PREDICATE_MEANING_refresh_scope: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'CS(PREDICATE_MEANING,refresh_scope)', (1,))
_EI_034_CS_PREDICATE_MEANING_task_accepts: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'CS(PREDICATE_MEANING,task_accepts)', (1,))
_EI_035_CS_UNKNOWN_BEHAVIOR_predicate: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'CS(UNKNOWN_BEHAVIOR,predicate)', (1,))
_EI_036_T3_A1_ACCESS_LIFT: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'T3_A1_ACCESS_LIFT(pd,sb)', (1,))
_EI_037_T3_A1_ERROR_LIFT: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'T3_A1_ERROR_LIFT(pd,sb)', (1,))
_EI_038_T3_A1_EVIDENCE_LIFT: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'T3_A1_EVIDENCE_LIFT(pd,sb)', (1,))
_EI_039_T3_A1_UNKNOWN_LIFT: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'T3_A1_UNKNOWN_LIFT(pd,sb)', (1,))
_EI_040_CFAIL: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.service.contract', 'CFAIL', (1,))
_EI_041_CREQ: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.service.contract', 'CREQ', (1,))
_EI_042_CSOUND: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.service.contract', 'CSOUND', (1,))
_EI_043_FSOUND: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.service.contract', 'FSOUND', (1,))
_EI_044_QFAIL: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.service.contract', 'QFAIL', (1,))
_EI_045_QREQ: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.service.contract', 'QREQ', (1,))
_EI_046_QSOUND: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.service.contract', 'QSOUND', (1,))
_EI_047_CS_TYPE_ADMISSION_type_ArtifactBodyKind: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ArtifactBodyKind)', (1,))
_EI_048_CS_TYPE_ADMISSION_type_ArtifactContent: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ArtifactContent)', (1,))
_EI_049_CS_TYPE_ADMISSION_type_ArtifactProjection: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ArtifactProjection)', (1,))
_EI_050_CS_TYPE_ADMISSION_type_ArtifactRole: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ArtifactRole)', (1,))
_EI_051_CS_TYPE_ADMISSION_type_ArtifactSelector: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ArtifactSelector)', (1,))
_EI_052_CS_TYPE_ADMISSION_type_BehaviorValue: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.BehaviorValue)', (1,))
_EI_053_CS_TYPE_ADMISSION_type_ByteSize: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ByteSize)', (1,))
_EI_054_CS_TYPE_ADMISSION_type_ContentIdentity: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ContentIdentity)', (1,))
_EI_055_CS_TYPE_ADMISSION_type_Coverage: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.Coverage)', (1,))
_EI_056_CS_TYPE_ADMISSION_type_Criterion: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.Criterion)', (1,))
_EI_057_CS_TYPE_ADMISSION_type_FieldId: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.FieldId)', (1,))
_EI_058_CS_TYPE_ADMISSION_type_FieldValue: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.FieldValue)', (1,))
_EI_059_CS_TYPE_ADMISSION_type_Format: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.Format)', (1,))
_EI_060_CS_TYPE_ADMISSION_type_ObservationRelation: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ObservationRelation)', (1,))
_EI_061_CS_TYPE_ADMISSION_type_ObservationResult: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ObservationResult)', (1,))
_EI_062_CS_TYPE_ADMISSION_type_ObservationSpec: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ObservationSpec)', (1,))
_EI_063_CS_TYPE_ADMISSION_type_ObservationValue: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.ObservationValue)', (1,))
_EI_064_CS_TYPE_ADMISSION_type_Path: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.Path)', (1,))
_EI_065_CS_TYPE_ADMISSION_type_PathSegment: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.PathSegment)', (1,))
_EI_066_CS_TYPE_ADMISSION_type_PathSet: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.PathSet)', (1,))
_EI_067_CS_TYPE_ADMISSION_type_RepositorySnapshot: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.RepositorySnapshot)', (1,))
_EI_068_CS_TYPE_ADMISSION_type_SubjectId: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.SubjectId)', (1,))
_EI_069_CS_TYPE_ADMISSION_type_TaskSpec: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.TaskSpec)', (1,))
_EI_070_CS_TYPE_ADMISSION_type_VerificationSpec: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type-admission', 'CS(TYPE_ADMISSION,type.VerificationSpec)', (1,))
_EI_071_ADMIT_RepositorySnapshot: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type.contract', 'ADMIT(RepositorySnapshot)', (1,))
_EI_072_ADMIT_TaskSpec: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.type.contract', 'ADMIT(TaskSpec)', (1,))
_EI_073_CS_ACCESS_BOUNDARY_snapshot_pair: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'confluence.contract', 'CS(ACCESS_BOUNDARY,snapshot_pair)', (1,))
_EI_074_CS_CONFLUENCE_changes_between: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'confluence.contract', 'CS(CONFLUENCE,changes_between)', (1,))
_EI_075_CS_CONFLUENCE_observe: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'confluence.contract', 'CS(CONFLUENCE,observe)', (1,))
_EI_076_CS_EVALUATION_ERROR_BEHAVIOR_term: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'confluence.contract', 'CS(EVALUATION_ERROR_BEHAVIOR,term)', (1,))
_EI_077_CS_EVIDENCE_SCHEMA_none: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'confluence.contract', 'CS(EVIDENCE_SCHEMA,none)', (1,))
_EI_078_CS_UNKNOWN_BEHAVIOR_never: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'confluence.contract', 'CS(UNKNOWN_BEHAVIOR,never)', (1,))
_EI_079_CS_ACCESS_BOUNDARY_pattern_trace: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'cycle.contract', 'CS(ACCESS_BOUNDARY,pattern_trace)', (1,))
_EI_080_CS_EVALUATION_ERROR_BEHAVIOR_predicate: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'cycle.contract', 'CS(EVALUATION_ERROR_BEHAVIOR,predicate)', (1,))
_EI_081_CS_EVIDENCE_SCHEMA_none: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'cycle.contract', 'CS(EVIDENCE_SCHEMA,none)', (1,))
_EI_082_CS_PREDICATE_MEANING_event_matches_cycle: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'cycle.contract', 'CS(PREDICATE_MEANING,event_matches_cycle)', (1,))
_EI_083_CS_PREDICATE_MEANING_event_occurred: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'cycle.contract', 'CS(PREDICATE_MEANING,event_occurred)', (1,))
_EI_084_CS_UNKNOWN_BEHAVIOR_never: IdentityLiteral = ('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'cycle.contract', 'CS(UNKNOWN_BEHAVIOR,never)', (1,))
_EI_085_DP_refresh_occurred: IdentityLiteral = ('DECLARATION_RECORD', 'capknow.semantic', 'coding.declaration', 'DP(refresh_occurred)', (1,))
_EI_086_DP_refresh_scope: IdentityLiteral = ('DECLARATION_RECORD', 'capknow.semantic', 'coding.declaration', 'DP(refresh_scope)', (1,))
_EI_087_DP_task_accepts: IdentityLiteral = ('DECLARATION_RECORD', 'capknow.semantic', 'coding.declaration', 'DP(task_accepts)', (1,))
_EI_088_DP_event_matches: IdentityLiteral = ('DECLARATION_RECORD', 'capknow.semantic', 'cycle', 'DP(event_matches)', (1,))
_EI_089_DP_event_occurred: IdentityLiteral = ('DECLARATION_RECORD', 'capknow.semantic', 'cycle', 'DP(event_occurred)', (1,))
_EI_090_D_c: IdentityLiteral = ('DEPENDENCY_ENVIRONMENT_RECORD', 'capknow.semantic', 'confluence.environment', 'D_c', (1,))
_EI_091_D_t: IdentityLiteral = ('DEPENDENCY_ENVIRONMENT_RECORD', 'capknow.semantic', 'environment', 'D_t', (1,))
_EI_092_D_t_empty: IdentityLiteral = ('DEPENDENCY_ENVIRONMENT_RECORD', 'capknow.semantic', 'environment', 'D_t_empty', (1,))
_EI_093_D_t_extra: IdentityLiteral = ('DEPENDENCY_ENVIRONMENT_RECORD', 'capknow.semantic', 'environment', 'D_t_extra', (1,))
_EI_094_D_t_incomplete: IdentityLiteral = ('DEPENDENCY_ENVIRONMENT_RECORD', 'capknow.semantic', 'environment', 'D_t_incomplete', (1,))
_EI_095_D_lex: IdentityLiteral = ('DEPENDENCY_ENVIRONMENT_RECORD', 'capknow.semantic', 'lexical.environment', 'D_lex', (1,))
_EI_096_D_p: IdentityLiteral = ('DEPENDENCY_ENVIRONMENT_RECORD', 'capknow.semantic', 'pair.environment', 'D_p', (1,))
_EI_097_DE_dependency_refresh: IdentityLiteral = ('EVENT_DECLARATION_RECORD', 'capknow.semantic', 'coding.declaration', 'DE(dependency_refresh)', (1,))
_EI_098_ev0: IdentityLiteral = ('EVENT_VALUE_RECORD', 'capknow.semantic', 'event.value', 'ev0', (1,))
_EI_099_PAIR_PROOF_REF: IdentityLiteral = ('EVIDENCE_RECORD', 'capknow.audit.pair-proof', 'pair.evidence', 'PAIR_PROOF_REF', (1,))
_EI_100_PairFullEvalProof: IdentityLiteral = ('EVIDENCE_RECORD', 'capknow.audit.pair-proof', 'pair.proof', 'PairFullEvalProof', (1,))
_EI_101_e0: IdentityLiteral = ('EVIDENCE_RECORD', 'capknow.semantic', 'evidence', 'e0', (1,))
_EI_102_lk0: IdentityLiteral = ('LEXICAL_BINDING_RECORD', 'capknow.semantic', 'lexical', 'lk0', (1,))
_EI_103_lk_extra: IdentityLiteral = ('LEXICAL_BINDING_RECORD', 'capknow.semantic', 'lexical', 'lk_extra', (1,))
_EI_104_L_c_final: IdentityLiteral = ('LIFECYCLE_RECORD', 'capknow.semantic', 'confluence.lifecycle', 'L_c_final', (1,))
_EI_105_L_life_after: IdentityLiteral = ('LIFECYCLE_RECORD', 'capknow.semantic', 'confluence.lifecycle', 'L_life_after', (1,))
_EI_106_MK0: IdentityLiteral = ('MIGRATION_RECORD', 'capknow.fixture.evolution-owner', 'evolution', 'MK0', (1,))
_EI_107_MODEL_task_accepts: IdentityLiteral = ('MODEL_CONTRACT_RECORD', 'capknow.semantic', 'coding.model', 'MODEL_task_accepts', (1,))
_EI_108_MODEL_refresh_occurred_pair: IdentityLiteral = ('MODEL_CONTRACT_RECORD', 'capknow.semantic', 'pair.model', 'MODEL_refresh_occurred_pair', (1,))
_EI_109_MODEL_refresh_scope_pair: IdentityLiteral = ('MODEL_CONTRACT_RECORD', 'capknow.semantic', 'pair.model', 'MODEL_refresh_scope_pair', (1,))
_EI_110_M_c: IdentityLiteral = ('OBSERVATION_ENVIRONMENT_RECORD', 'capknow.semantic', 'confluence.result', 'M_c', (1,))
_EI_111_M_c_missing: IdentityLiteral = ('OBSERVATION_ENVIRONMENT_RECORD', 'capknow.semantic', 'confluence.result', 'M_c_missing', (1,))
_EI_114_K_c: IdentityLiteral = ('OUTCOME_RECORD', 'capknow.semantic', 'confluence.result', 'K_c', (1,))
_EI_115_t_t_evidence_subject: IdentityLiteral = ('OUTCOME_RECORD', 'capknow.semantic', 'evidence', 't_t_evidence_subject', (1,))
_EI_116_O_w: IdentityLiteral = ('OUTCOME_RECORD', 'capknow.semantic', 'outcome', 'O_w', (1,))
_EI_117_VALUE_UNKNOWN: IdentityLiteral = ('OUTCOME_RECORD', 'capknow.semantic', 'reason', 'VALUE(UNKNOWN)', (1,))
_EI_118_pair_validator: IdentityLiteral = ('PACKAGE_RECORD', 'capknow.audit.pair-validator', 'plugin', 'pair-validator', (1,))
_EI_119_pair_proof: IdentityLiteral = ('PACKAGE_RECORD', 'capknow.audit.pair-proof', 'plugin', 'pair-proof', (1,))
_EI_120_evolution_owner: IdentityLiteral = ('PACKAGE_RECORD', 'capknow.fixture.evolution-owner', 'plugin', 'evolution-owner', (1,))
_EI_121_permutation_one: IdentityLiteral = ('PACKAGE_RECORD', 'capknow.fixture.permutation-one', 'plugin', 'permutation-one', (1,))
_EI_122_permutation_two: IdentityLiteral = ('PACKAGE_RECORD', 'capknow.fixture.permutation-two', 'plugin', 'permutation-two', (1,))
_EI_123_authority_owner: IdentityLiteral = ('PACKAGE_RECORD', 'capknow.semantic', 'plugin', 'authority-owner', (1,))
_EI_124_coding_minimal: IdentityLiteral = ('PACKAGE_RECORD', 'capknow.semantic', 'plugin', 'coding-minimal', (1,))
_EI_125_PB_alt: IdentityLiteral = ('PAIR_BINDING_RECORD', 'capknow.semantic', 'pair.binding', 'PB_alt', (1,))
_EI_126_PAIR_refresh: IdentityLiteral = ('PAIR_DECLARATION_RECORD', 'capknow.semantic', 'pair', 'PAIR(refresh)', (1,))
_EI_127_producer_certificate: IdentityLiteral = ('PRODUCER_RECORD', 'capknow.semantic', 'pair.producer', 'producer.certificate', (1,))
_EI_128_producer_pair: IdentityLiteral = ('PRODUCER_RECORD', 'capknow.semantic', 'pair.producer', 'producer.pair', (1,))
_EI_129_producer_trust_environment: IdentityLiteral = ('PRODUCER_RECORD', 'capknow.semantic', 'pair.producer', 'producer.trust.environment', (1,))
_EI_130_producer_trust_policy: IdentityLiteral = ('PRODUCER_RECORD', 'capknow.semantic', 'pair.producer', 'producer.trust.policy', (1,))
_EI_131_producer_trust_root: IdentityLiteral = ('PRODUCER_RECORD', 'capknow.semantic', 'pair.producer', 'producer.trust.root', (1,))
_EI_132_producer_validation_capability: IdentityLiteral = ('PRODUCER_RECORD', 'capknow.semantic', 'pair.producer', 'producer.validation.capability', (1,))
_EI_133_producer_validation_proof: IdentityLiteral = ('PRODUCER_RECORD', 'capknow.semantic', 'pair.producer', 'producer.validation.proof', (1,))
_EI_134_PROFILE_BINDING_PK_implementation_evidence: IdentityLiteral = ('PROFILE_BINDING_RECORD', 'capknow.semantic', 'coding.binding', 'PROFILE_BINDING(PK(implementation_evidence))', (1,))
_EI_135_u0: IdentityLiteral = ('REASON_RECORD', 'capknow.semantic', 'reason', 'u0', (1,))
_EI_136_R_c: IdentityLiteral = ('REQUEST_RECORD', 'capknow.semantic', 'confluence.request', 'R_c', (1,))
_EI_137_R_lex: IdentityLiteral = ('REQUEST_RECORD', 'capknow.semantic', 'lexical.request', 'R_lex', (1,))
_EI_138_R_p: IdentityLiteral = ('REQUEST_RECORD', 'capknow.semantic', 'pair.request', 'R_p', (1,))
_EI_139_Q_t_ABSENT: IdentityLiteral = ('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t[ABSENT]', (1,))
_EI_140_Q_t_ADMITTED: IdentityLiteral = ('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t[ADMITTED]', (1,))
_EI_141_Q_t_FAILED: IdentityLiteral = ('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t[FAILED]', (1,))
_EI_142_Q_t_INCOMPATIBLE: IdentityLiteral = ('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t[INCOMPATIBLE]', (1,))
_EI_143_Q_t_UNDECIDED: IdentityLiteral = ('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t[UNDECIDED]', (1,))
_EI_144_Q_t_extra: IdentityLiteral = ('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t_extra', (1,))
_EI_145_Y_c: IdentityLiteral = ('RESULT_RECORD', 'capknow.semantic', 'confluence.result', 'Y_c', (1,))
_EI_146_RES_t_ADMITTED: IdentityLiteral = ('RESULT_RECORD', 'capknow.semantic', 'result', 'RES_t[ADMITTED]', (1,))
_EI_147_E_choice: IdentityLiteral = ('SEMANTIC_ENVIRONMENT_RECORD', 'capknow.semantic', 'authority.environment', 'E_choice', (1,))
_EI_148_E_c: IdentityLiteral = ('SEMANTIC_ENVIRONMENT_RECORD', 'capknow.semantic', 'confluence.environment', 'E_c', (1,))
_EI_149_E_PROPER_CYCLE: IdentityLiteral = ('SEMANTIC_ENVIRONMENT_RECORD', 'capknow.semantic', 'cycle.environment', 'E_PROPER_CYCLE', (1,))
_EI_150_E_t: IdentityLiteral = ('SEMANTIC_ENVIRONMENT_RECORD', 'capknow.semantic', 'environment', 'E_t', (1,))
_EI_151_E_t_empty: IdentityLiteral = ('SEMANTIC_ENVIRONMENT_RECORD', 'capknow.semantic', 'environment', 'E_t_empty', (1,))
_EI_152_E_t_extra: IdentityLiteral = ('SEMANTIC_ENVIRONMENT_RECORD', 'capknow.semantic', 'environment', 'E_t_extra', (1,))
_EI_153_E_lex: IdentityLiteral = ('SEMANTIC_ENVIRONMENT_RECORD', 'capknow.semantic', 'lexical.environment', 'E_lex', (1,))
_EI_154_E_p: IdentityLiteral = ('SEMANTIC_ENVIRONMENT_RECORD', 'capknow.semantic', 'pair.environment', 'E_p', (1,))
_EI_155_XK0: IdentityLiteral = ('SEMANTIC_EXTENSION_RECORD', 'capknow.fixture.evolution-owner', 'evolution', 'XK0', (1,))
_EI_156_XK1: IdentityLiteral = ('SEMANTIC_EXTENSION_RECORD', 'capknow.fixture.evolution-owner', 'evolution', 'XK1', (1,))
_EI_157_PVSK: IdentityLiteral = ('SERVICE_RECORD', 'capknow.audit.pair-validator', 'coding.validation', 'refresh', (1,))
_EI_158_SK_confluence: IdentityLiteral = ('SERVICE_RECORD', 'capknow.semantic', 'coding.service', 'SK(confluence)', (1,))
_EI_159_SK_predicates: IdentityLiteral = ('SERVICE_RECORD', 'capknow.semantic', 'coding.service', 'SK(predicates)', (1,))
_EI_160_SRC_choice_1: IdentityLiteral = ('SOURCE_RECORD', 'capknow.semantic', 'authority.source', 'SRC(choice,1)', (1,))
_EI_161_te0: IdentityLiteral = ('TRACE_EVENT_RECORD', 'capknow.semantic', 'event.trace', 'te0', (1,))
_EI_162_T_c: IdentityLiteral = ('TRUST_ENVIRONMENT_RECORD', 'capknow.semantic', 'confluence.trust', 'T_c', (1,))
_EI_163_T_p: IdentityLiteral = ('TRUST_ENVIRONMENT_RECORD', 'capknow.semantic', 'pair.trust', 'T_p', (1,))
_EI_164_T_absent: IdentityLiteral = ('TRUST_ENVIRONMENT_RECORD', 'capknow.semantic', 'trust', 'T_absent', (1,))
_EI_165_T_admitted: IdentityLiteral = ('TRUST_ENVIRONMENT_RECORD', 'capknow.semantic', 'trust', 'T_admitted', (1,))
_EI_166_T_failed: IdentityLiteral = ('TRUST_ENVIRONMENT_RECORD', 'capknow.semantic', 'trust', 'T_failed', (1,))
_EI_167_T_incompatible: IdentityLiteral = ('TRUST_ENVIRONMENT_RECORD', 'capknow.semantic', 'trust', 'T_incompatible', (1,))
_EI_168_T_undecided: IdentityLiteral = ('TRUST_ENVIRONMENT_RECORD', 'capknow.semantic', 'trust', 'T_undecided', (1,))
_EI_169_TP: IdentityLiteral = ('TRUST_POLICY_RECORD', 'capknow.semantic', 'confluence.trust', 'TP', (1,))
_EI_170_TP: IdentityLiteral = ('TRUST_POLICY_RECORD', 'capknow.semantic', 'pair.trust', 'TP', (1,))
_EI_171_TP: IdentityLiteral = ('TRUST_POLICY_RECORD', 'capknow.semantic', 'trust', 'TP', (1,))
_EI_172_ROOT_TR_c: IdentityLiteral = ('TRUST_ROOT_RECORD', 'capknow.semantic', 'confluence.trust', 'ROOT_TR_c', (1,))
_EI_173_TRP: IdentityLiteral = ('TRUST_ROOT_RECORD', 'capknow.semantic', 'pair.trust', 'TRP', (1,))
_EI_174_TR: IdentityLiteral = ('TRUST_ROOT_RECORD', 'capknow.semantic', 'trust', 'TR', (1,))
_EI_175_T_fixture_unit_one: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.fixture.permutation-one', 'coding.fixture.type', 'T(fixture_unit_one)', (1,))
_EI_176_T_fixture_unit_two: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.fixture.permutation-one', 'coding.fixture.type', 'T(fixture_unit_two)', (1,))
_EI_177_T_fixture_unit_four: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.fixture.permutation-two', 'coding.fixture.type', 'T(fixture_unit_four)', (1,))
_EI_178_T_fixture_unit_three: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.fixture.permutation-two', 'coding.fixture.type', 'T(fixture_unit_three)', (1,))
_EI_179_RepositorySnapshot: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'RepositorySnapshot', (1,))
_EI_180_T_ArtifactBodyKind: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ArtifactBodyKind)', (1,))
_EI_181_T_ArtifactContent: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ArtifactContent)', (1,))
_EI_182_T_ArtifactProjection: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ArtifactProjection)', (1,))
_EI_183_T_ArtifactRole: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ArtifactRole)', (1,))
_EI_184_T_ArtifactSelector: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ArtifactSelector)', (1,))
_EI_185_T_BehaviorValue: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(BehaviorValue)', (1,))
_EI_186_T_ByteSize: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ByteSize)', (1,))
_EI_187_T_ContentIdentity: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ContentIdentity)', (1,))
_EI_188_T_Coverage: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(Coverage)', (1,))
_EI_189_T_Criterion: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(Criterion)', (1,))
_EI_190_T_FieldId: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(FieldId)', (1,))
_EI_191_T_FieldValue: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(FieldValue)', (1,))
_EI_192_T_Format: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(Format)', (1,))
_EI_193_T_ObservationRelation: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ObservationRelation)', (1,))
_EI_194_T_ObservationResult: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ObservationResult)', (1,))
_EI_195_T_ObservationSpec: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ObservationSpec)', (1,))
_EI_196_T_ObservationValue: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(ObservationValue)', (1,))
_EI_197_T_Path: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(Path)', (1,))
_EI_198_T_PathSegment: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(PathSegment)', (1,))
_EI_199_T_PathSet: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(PathSet)', (1,))
_EI_200_T_RepositorySnapshot: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(RepositorySnapshot)', (1,))
_EI_201_T_SubjectId: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(SubjectId)', (1,))
_EI_202_T_TaskSpec: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(TaskSpec)', (1,))
_EI_203_T_VerificationSpec: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'T(VerificationSpec)', (1,))
_EI_204_TaskSpec: IdentityLiteral = ('TYPE_DECLARATION_RECORD', 'capknow.semantic', 'coding.type', 'TaskSpec', (1,))

_EXPECTED_C_PATH = Path((PathSegment("dependency"), PathSegment("lock")))
_EXPECTED_C_NEW = ArtifactContent(
    ArtifactTag.TEXT, ArtifactRole.DEPENDENCY_LOCK, Format.TEXT,
    ByteSize(150), ContentIdentity("lock_v1"),
)
_EXPECTED_C_SELECTOR = ArtifactSelector(
    SelectorTag.PATHS, frozenset({_EXPECTED_C_PATH}),
)
_EXPECTED_C_SPEC = ObservationSpec(
    ObservationSpecTag.ARTIFACT_VIEW, _EXPECTED_C_SELECTOR,
    ArtifactProjection(ProjectionTag.CONTENT),
)
_EXPECTED_C_OBSERVATION = ObservationResult(
    ObservationResultTag.ARTIFACT, _EXPECTED_C_SPEC, Coverage(CoverageTag.COMPLETE),
    ((_EXPECTED_C_PATH, ObservationValue(
        ObservationValueTag.PRESENT_CONTENT, (_EXPECTED_C_NEW,),
    )),),
)
_EXPECTED_CONFLUENCE_OUTCOME = (
    "OBSERVATION",
    (
        (("BINDING_RECORD", "capknow.semantic", "coding.binding",
          "BINDING(DF(changes_between))", (1,)), TermResult(value=ChangeSet(((_EXPECTED_C_PATH, ChangeEntry(
            ChangeKind.CREATED, new=_EXPECTED_C_NEW,
        )),)))),
        (("BINDING_RECORD", "capknow.semantic", "coding.binding",
          "BINDING(DF(observe))", (1,)), TermResult(value=_EXPECTED_C_OBSERVATION)),
    ),
    ("COMPLETED_INCONCLUSIVE", ()),
    "COMPLETED",
    ("WELL_FORMED", "CLOSED", "EVALUABILITY_AVAILABLE", "COMPLETED", "CONSISTENCY_UNKNOWN"),
)

_EXPECTED_CYCLE_TYPE_NAMES = (
    "PathSegment", "Path", "PathSet", "ArtifactRole", "Format", "ByteSize",
    "ContentIdentity", "FieldId", "FieldValue", "SubjectId", "BehaviorValue",
    "ArtifactContent", "RepositorySnapshot", "SnapshotIdentity",
    "ArtifactSelector", "ArtifactProjection", "ObservationSpec",
    "VerificationSpec", "VerificationStatus", "ChangeKind", "CommandId",
    "ContactClass", "ReleaseId", "EventPattern",
)
_EXPECTED_CYCLE_ADDITIONS: tuple[IdentityLiteral, ...] = tuple(
    ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.type-admission",
     f"CS(TYPE_ADMISSION,type.{name})", (1,))
    for name in _EXPECTED_CYCLE_TYPE_NAMES
) + tuple(
    ("TYPE_DECLARATION_RECORD", "capknow.semantic", "coding.type",
     f"T({name})", (1,))
    for name in _EXPECTED_CYCLE_TYPE_NAMES
) + (
    ("MODEL_CONTRACT_RECORD", "capknow.semantic", "cycle.model", "MODEL_event_matches_cycle", (1,)),
    ("MODEL_CONTRACT_RECORD", "capknow.semantic", "cycle.model", "MODEL_event_occurred", (1,)),
    ("DECLARATION_RECORD", "capknow.semantic", "cycle", "DF(snapshot_of)", (1,)),
    ("DECLARATION_RECORD", "capknow.semantic", "cycle", "DF(changes_between)", (1,)),
    ("DECLARATION_RECORD", "capknow.semantic", "cycle", "DF(observe)", (1,)),
    ("BINDING_RECORD", "capknow.semantic", "cycle.binding", "BINDING(DF(snapshot_of))", (1,)),
    ("BINDING_RECORD", "capknow.semantic", "cycle.binding", "BINDING(DF(changes_between))", (1,)),
    ("BINDING_RECORD", "capknow.semantic", "cycle.binding", "BINDING(DF(observe))", (1,)),
    ("CONTRACT_SPEC_RECORD", "capknow.semantic", "cycle.contract", "CS(FUNCTION_MEANING,snapshot_of)", (1,)),
    ("CONTRACT_SPEC_RECORD", "capknow.semantic", "cycle.contract", "CS(FUNCTION_MEANING,changes_between)", (1,)),
    ("CONTRACT_SPEC_RECORD", "capknow.semantic", "cycle.contract", "CS(FUNCTION_MEANING,observe)", (1,)),
    ("CONTRACT_SPEC_RECORD", "capknow.semantic", "cycle.contract", "CS(ACCESS_BOUNDARY,state_only)", (1,)),
    ("CONTRACT_SPEC_RECORD", "capknow.semantic", "cycle.contract", "CS(ACCESS_BOUNDARY,snapshot_pair)", (1,)),
    ("CONTRACT_SPEC_RECORD", "capknow.semantic", "cycle.contract", "CS(ACCESS_BOUNDARY,observe)", (1,)),
    ("MODEL_CONTRACT_RECORD", "capknow.semantic", "cycle.model", "MODEL_snapshot_of_cycle", (1,)),
    ("MODEL_CONTRACT_RECORD", "capknow.semantic", "cycle.model", "MODEL_changes_between_cycle", (1,)),
    ("MODEL_CONTRACT_RECORD", "capknow.semantic", "cycle.model", "MODEL_observe_cycle", (1,)),
)

_EXPECTED_EVOLUTION_ROW_NAMES = ("m", "c", "x0", "x1")
_EXPECTED_EVOLUTION_ADDITIONS: tuple[IdentityLiteral, ...] = (
    ("CONTRACT_SPEC_RECORD", "capknow.fixture.evolution-owner", "evolution.contract", "MR0", (1,)),
    ("CONTRACT_SPEC_RECORD", "capknow.fixture.evolution-owner", "evolution.contract", "CC0", (1,)),
    ("CONTRACT_SPEC_RECORD", "capknow.fixture.evolution-owner", "evolution.contract", "XE0", (1,)),
    ("CONTRACT_SPEC_RECORD", "capknow.fixture.evolution-owner", "evolution.contract", "XP0", (1,)),
    ("TRUST_POLICY_RECORD", "capknow.semantic", "evolution.trust", "TP", (1,)),
    ("TRUST_ROOT_RECORD", "capknow.semantic", "evolution.trust", "TRE", (1,)),
    ("TRUST_ENVIRONMENT_RECORD", "capknow.semantic", "evolution.trust", "T_evo", (1,)),
    ("PACKAGE_RECORD", "capknow.audit.evolution-validator", "plugin", "evolution-validator", (1,)),
    ("PACKAGE_RECORD", "capknow.audit.evolution-proof", "plugin", "evolution-proof", (1,)),
) + tuple(
    identity
    for name in _EXPECTED_EVOLUTION_ROW_NAMES
    for identity in (
        ("SERVICE_RECORD", "capknow.audit.evolution-validator", "evolution.service", f"EVSK_{name}", (1,)),
        ("CAPABILITY_RECORD", "capknow.audit.evolution-validator", "evolution.capability", f"EVC_{name}", (1,)),
        ("CONTRACT_SPEC_RECORD", "capknow.audit.evolution-validator", "evolution.contract", f"ES_{name}", (1,)),
        ("CONTRACT_SPEC_RECORD", "capknow.audit.evolution-validator", "evolution.contract", f"ECOMP_{name}", (1,)),
        ("CONTRACT_SPEC_RECORD", "capknow.audit.evolution-validator", "evolution.contract", f"EE_{name}", (1,)),
        ("CONTRACT_SPEC_RECORD", "capknow.audit.evolution-validator", "evolution.contract", f"EF_{name}", (1,)),
        ("DEPENDENCY_ENVIRONMENT_RECORD", "capknow.semantic", "evolution.environment", f"D_ev_{name}", (1,)),
        ("REQUEST_RECORD", "capknow.semantic", "evolution.request", f"R_{name}", (1,)),
        ("EVIDENCE_RECORD", "capknow.audit.evolution-proof", "evolution.proof", f"EVOLUTION_PROOF_{name}", (1,)),
        ("EVIDENCE_RECORD", "capknow.audit.evolution-proof", "evolution.evidence", f"ER_{name}", (1,)),
        ("OUTCOME_RECORD", "capknow.semantic", "evolution.admission", f"EADMIT_{name}", (1,)),
        ("OUTCOME_RECORD", "capknow.semantic", "evolution.result", f"ERESULT_{name}", (1,)),
    )
) + (
    ("CERTIFICATE_RECORD", "capknow.audit.evolution-proof", "evolution.certificate", "EC_m", (1,)),
    ("CERTIFICATE_RECORD", "capknow.audit.evolution-proof", "evolution.certificate", "EC_c", (1,)),
    ("CERTIFICATE_RECORD", "capknow.audit.evolution-proof", "evolution.certificate", "EC_x0", (1,)),
    ("CERTIFICATE_RECORD", "capknow.audit.evolution-proof", "evolution.certificate", "EC_x1", (1,)),
) + tuple(
    identity
    for name in _EXPECTED_EVOLUTION_ROW_NAMES
    for identity in (
        *(('PRODUCER_RECORD', 'capknow.semantic', 'evolution.producer', f'producer.evolution.subject.{name}.{index}', (1,)) for index in range(3)),
        ('PRODUCER_RECORD', 'capknow.semantic', 'evolution.producer', f'producer.evolution.certificate.{name}', (1,)),
        ('PRODUCER_RECORD', 'capknow.semantic', 'evolution.producer', f'producer.evolution.validator.{name}', (1,)),
        ('PRODUCER_RECORD', 'capknow.semantic', 'evolution.producer', f'producer.evolution.service.{name}', (1,)),
    )
) + (
    ('PRODUCER_RECORD', 'capknow.semantic', 'evolution.producer', 'producer.evolution.root', (1,)),
)

_EXPECTED_CONFLUENCE_DECLARATIONS: tuple[IdentityLiteral, ...] = (
    ("DECLARATION_RECORD", "capknow.semantic", "confluence.declaration", "DF(observe)", (1,)),
    ("DECLARATION_RECORD", "capknow.semantic", "confluence.declaration", "DF(changes_between)", (1,)),
) + tuple(
    ('PRODUCER_RECORD', 'capknow.semantic', 'confluence.producer',
     f'producer.confluence.subject.{index}', (1,))
    for index in range(6)
) + (
    ('PRODUCER_RECORD', 'capknow.semantic', 'confluence.producer', 'producer.confluence.capability', (1,)),
    ('PRODUCER_RECORD', 'capknow.semantic', 'confluence.producer', 'producer.confluence.service', (1,)),
    ('PRODUCER_RECORD', 'capknow.semantic', 'confluence.producer', 'producer.confluence.root', (1,)),
    ('PRODUCER_RECORD', 'capknow.semantic', 'confluence.producer', 'producer.confluence.policy', (1,)),
    ('PRODUCER_RECORD', 'capknow.semantic', 'confluence.producer', 'producer.confluence.trust_environment', (1,)),
)
_EXPECTED_CONFLUENCE_AUTHORITY_ADDITIONS: tuple[IdentityLiteral, ...] = (
    ('SOURCE_RECORD', 'PLUGIN_ISSUER(APK)', 'authenticated.fixture.source', 'SRC(c,1)', (1,)),
    ('SOURCE_RECORD', 'PLUGIN_ISSUER(APK)', 'authenticated.fixture.source', 'SRC(c,2)', (1,)),
    ('AUTHORITY_REF_RECORD', 'PLUGIN_ISSUER(APK)', 'coding.fixture', 'AUTH(c,1)', (1,)),
    ('AUTHORITY_REF_RECORD', 'PLUGIN_ISSUER(APK)', 'coding.fixture', 'AUTH(c,2)', (1,)),
    ('AUTHORITY_FACT_RECORD', 'capknow.semantic', 'confluence.authority.binding', 'AFB(c,1)', (1,)),
    ('AUTHORITY_FACT_RECORD', 'capknow.semantic', 'confluence.authority.binding', 'AFB(c,2)', (1,)),
)

_EXPECTED_PAIR_REPAIR5_ADDITIONS: tuple[IdentityLiteral, ...] = (
    ('OUTCOME_RECORD', 'capknow.semantic', 'pair.admission', 'PADMIT', (1,)),
    ('RESULT_RECORD', 'capknow.semantic', 'pair.result', 'PRESULT', (1,)),
)
_EXPECTED_PAIR_REPAIR6_TYPE_NAMES = tuple(pair_type_dependencies for pair_type_dependencies in (
    "PathSegment", "Path", "PathSet", "ArtifactRole", "Format", "ByteSize",
    "ContentIdentity", "FieldId", "FieldValue", "SubjectId", "BehaviorValue",
    "ArtifactContent", "RepositorySnapshot", "SnapshotIdentity",
    "ArtifactSelector", "DependencyRefreshEventPayload", "PairTraceDomain",
    "PairComparedFields", "ServiceAdmissionSubject",
))
_EXPECTED_PAIR_REPAIR6_LITERAL_NAMES = (
    "PairTraceDomain", "PairComparedFields", "ServiceAdmissionSubject",
)
_EXPECTED_PAIR_REPAIR6_ADDITIONS: tuple[IdentityLiteral, ...] = tuple(
    identity
    for name in _EXPECTED_PAIR_REPAIR6_TYPE_NAMES
    for identity in (
        ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.type-admission", f"CS(TYPE_ADMISSION,type.{name})", (1,)),
        ("TYPE_DECLARATION_RECORD", "capknow.semantic", "coding.type", f"T({name})", (1,)),
    )
) + tuple(
    identity
    for name in _EXPECTED_PAIR_REPAIR6_LITERAL_NAMES
    for identity in (
        ("DECLARATION_RECORD", "capknow.semantic", "coding.literal", f"L({name})", (1,)),
        ("BINDING_RECORD", "capknow.semantic", "coding.literal.binding", f"BINDING(L({name}))", (1,)),
        ("MODEL_CONTRACT_RECORD", "capknow.semantic", "coding.literal.model", f"MODEL_LITERAL({name})", (1,)),
        *(("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.literal.contract", f"CS({role},{name})", (1,))
          for role in ("LITERAL_MEANING", "EVIDENCE_SCHEMA", "ACCESS_BOUNDARY",
                       "UNKNOWN_BEHAVIOR", "EVALUATION_ERROR_BEHAVIOR")),
    )
) + (
    ("PRODUCER_RECORD", "capknow.semantic", "pair.producer", "producer.full.eval.proof", (1,)),
    ("PRODUCER_RECORD", "capknow.semantic", "pair.producer", "producer.validation.service", (1,)),
)
_EXPECTED_EVOLUTION_REPAIR6_ADDITIONS: tuple[IdentityLiteral, ...] = tuple(
    identity
    for name in _EXPECTED_EVOLUTION_ROW_NAMES
    for identity in (
        ("PRODUCER_RECORD", "capknow.semantic", "evolution.producer", f"producer.evolution.proof.{name}", (1,)),
        ("PRODUCER_RECORD", "capknow.semantic", "evolution.producer", f"producer.evolution.evidence.{name}", (1,)),
    )
) + (
    ("PRODUCER_RECORD", "capknow.semantic", "evolution.producer", "producer.evolution.policy", (1,)),
    ("PRODUCER_RECORD", "capknow.semantic", "evolution.producer", "producer.evolution.trust_environment", (1,)),
)
_EXPECTED_EVOLUTION_REPAIR7_ADDITIONS: tuple[IdentityLiteral, ...] = (
    _EI_005_BINDING_DP_task_accepts,
    _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence,
    _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate,
    _EI_030_CS_EVIDENCE_SCHEMA_verification,
    _EI_034_CS_PREDICATE_MEANING_task_accepts,
    _EI_087_DP_task_accepts, _EI_150_E_t,
    ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.contract", "CS(UNKNOWN_BEHAVIOR,task)", (1,)),
) + tuple(
    identity
    for name in (
        "ArtifactBodyKind", "ArtifactContent", "ArtifactProjection", "ArtifactRole",
        "ArtifactSelector", "BehaviorValue", "ByteSize", "ContentIdentity",
        "Coverage", "Criterion", "FieldId", "FieldValue", "Format",
        "ObservationRelation", "ObservationResult", "ObservationSpec",
        "ObservationValue", "Path", "PathSegment", "PathSet",
        "RepositorySnapshot", "SubjectId", "TaskSpec", "VerificationSpec",
    )
    for identity in (
        ("TYPE_DECLARATION_RECORD", "capknow.semantic", "coding.type", f"T({name})", (1,)),
        ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.type-admission", f"CS(TYPE_ADMISSION,type.{name})", (1,)),
    )
)
_EXPECTED_RETAINED_CORE_ADDITIONS: tuple[IdentityLiteral, ...] = (
    _EI_005_BINDING_DP_task_accepts, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence,
    _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification,
    _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate,
    _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND,
    _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec,
    _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh,
    _EI_107_MODEL_task_accepts, _EI_134_PROFILE_BINDING_PK_implementation_evidence,
    _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED, _EI_150_E_t,
    _EI_165_T_admitted, _EI_171_TP, _EI_174_TR,
    _EI_179_RepositorySnapshot, _EI_204_TaskSpec,
)
_EXPECTED_RETAINED_TYPE_NAMES = (
    "PathSegment", "Path", "PathSet", "ArtifactRole", "Format",
    "StorageBackend", "ByteSize", "ContentIdentity", "FieldId", "FieldValue",
    "SubjectId", "BehaviorValue", "ArtifactBody", "ArtifactBodyKind",
    "ArtifactContent", "RepositorySnapshot", "SnapshotIdentity", "ChangeEntry",
    "ChangeSet", "ArtifactSelector", "ArtifactProjection", "Coverage",
    "ObservationSpec", "ObservationValue", "ObservationResult",
    "ObservationRelation", "VerificationStatus", "VerificationSpec",
    "VerificationRecord", "ImplementationEvidence", "CodingEvidencePayload",
    "CodingEvidenceEntry", "AbstractCoverageResult",
    "ImplementationCoverageSubject", "PairTraceDomain", "PairComparedFields",
    "AuthorityClauseTag", "AuthorityAttestationSubjectIdentity",
    "AuthorityAttestationValue", "ServiceAdmissionSubject",
    "EvolutionAdmissionSubject", "Criterion", "TaskSpec", "ChangeKind",
    "CommandId", "ContactClass", "ReleaseId", "Purpose", "EventPattern",
    "CommandEventPayload", "TestEventPayload", "PathChangeEventPayload",
    "NetworkContactEventPayload", "ReleaseEventPayload",
    "DependencyRefreshEventPayload",
)
_EXPECTED_RETAINED_TYPE_IDENTITIES: tuple[IdentityLiteral, ...] = tuple(
    identity
    for name in _EXPECTED_RETAINED_TYPE_NAMES
    for identity in (
        ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.type-admission",
         f"CS(TYPE_ADMISSION,type.{name})", (1,)),
        ("TYPE_DECLARATION_RECORD", "capknow.semantic", "coding.type",
         f"T({name})", (1,)),
    )
)
_EXPECTED_RETAINED_LITERAL_ROWS = (
    ("TaskSpec", "ts_nonempty"), ("TaskSpec", "ts_lt_100"),
    ("TaskSpec", "ts_ge_200"), ("ObservationSpec", "s_c"),
    ("RepositorySnapshot", "P_c"), ("RepositorySnapshot", "F_c"),
    ("ObservationResult", "O_c"), ("ObservationSpec", "s_w"),
    ("TaskSpec", "t_w"), ("TaskSpec", "t_t"),
    ("StorageBackend", "LOCAL_STORAGE"), ("StorageBackend", "HOSTED_STORAGE"),
    ("PairTraceDomain", "ALL_ADMITTED_TRACES"),
    ("PairComparedFields", "COMPLETE_EVAL_RECORD"),
    *(("AuthorityClauseTag", name) for name in (
        "BOUNDS_CLAUSE", "CONFLUENCE_OBSERVATION_CLAUSE",
        "CONFLUENCE_CHANGE_CLAUSE", "ADAPTER_PRESERVATION_CLAUSE",
        "ADAPTER_ACCEPTANCE_CLAUSE")),
    *(("AuthorityAttestationSubjectIdentity", f"attestation_subject_identity({name})")
      for name in ("b,1", "c,1", "c,2", "w,1", "w,2", "choice,1")),
    *(("AuthorityAttestationValue", f"ATTEST({name})")
      for name in ("b,1", "c,1", "c,2", "w,1", "w,2", "choice,1")),
    *(("ServiceAdmissionSubject", name) for name in (
        "bounds_subject_b", "confluence_subject_c", "witness_subject_w",
        "predicate_subject_t", "profile_subject_w", "pair_subject",
        "authority_subject(b,1)", "authority_subject(c,1)",
        "authority_subject(c,2)", "authority_subject(w,1)",
        "authority_subject(w,2)", "authority_subject(choice,1)")),
    *(("EvolutionAdmissionSubject", name)
      for name in ("mr_subject", "cc_subject", "x0_subject", "x1_subject")),
)
_EXPECTED_RETAINED_LITERAL_IDENTITIES: tuple[IdentityLiteral, ...] = (
    tuple(
        identity
        for type_name, local in _EXPECTED_RETAINED_LITERAL_ROWS
        for identity in (
            ("DECLARATION_RECORD", "capknow.semantic", "coding.declaration", f"L(T({type_name}),{local})", (1,)),
            ("BINDING_RECORD", "capknow.semantic", "coding.binding", f"BINDING(L(T({type_name}),{local}))", (1,)),
            ("MODEL_CONTRACT_RECORD", "capknow.semantic", "coding.model", f"MODEL_LITERAL(T({type_name}),{local})", (1,)),
            ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.contract",
             f"CS(LITERAL_MEANING,literal.T({type_name}).{local})", (1,)),
        )
    ) + (
        ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.contract", "CS(EVIDENCE_SCHEMA,none)", (1,)),
        ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.contract", "CS(ACCESS_BOUNDARY,literal)", (1,)),
        ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.contract", "CS(UNKNOWN_BEHAVIOR,never)", (1,)),
        ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.contract", "CS(EVALUATION_ERROR_BEHAVIOR,literal)", (1,)),
    )
)
_EXPECTED_ORDINARY_FUNCTIONS = ("snapshot_of", "changes_between", "observe")
_EXPECTED_ORDINARY_PREDICATES = (
    "observations_equal", "task_accepts", "dependency_metadata_changed",
    "verification_passed", "event_matches", "event_occurred", "refresh_scope",
)
_EXPECTED_RETAINED_SYMBOL_IDENTITIES: tuple[IdentityLiteral, ...] = tuple(
    identity
    for prefix, names in (("DF", _EXPECTED_ORDINARY_FUNCTIONS),
                          ("DP", _EXPECTED_ORDINARY_PREDICATES))
    for name in names
    for identity in (
        ("DECLARATION_RECORD", "capknow.semantic", "coding.declaration", f"{prefix}({name})", (1,)),
        ("BINDING_RECORD", "capknow.semantic", "coding.binding", f"BINDING({prefix}({name}))", (1,)),
        ("MODEL_CONTRACT_RECORD", "capknow.semantic", "coding.model", f"MODEL_{name}", (1,)),
    )
) + tuple(
    ("EVENT_DECLARATION_RECORD", "capknow.semantic", "coding.declaration", f"DE({name})", (1,))
    for name in ("command", "test", "path_change", "network_contact", "release", "dependency_refresh")
) + (
    ("DECLARATION_RECORD", "capknow.semantic", "coding.declaration", "DP(refresh_occurred)", (1,)),
    ("BINDING_RECORD", "capknow.semantic", "coding.binding", "BINDING(DP(refresh_occurred))", (1,)),
    ("MODEL_CONTRACT_RECORD", "capknow.semantic", "coding.model", "MODEL_refresh_occurred", (1,)),
    ("PAIR_DECLARATION_RECORD", "capknow.semantic", "pair", "PAIR(refresh)", (1,)),
    ("PAIR_BINDING_RECORD", "capknow.semantic", "pair.binding", "PB_refresh", (1,)),
)
_EXPECTED_ORDINARY_SPEC_LOCALS = (
    "CS(FUNCTION_MEANING,snapshot_of)", "CS(FUNCTION_MEANING,changes_between)",
    "CS(FUNCTION_MEANING,observe)", "CS(PREDICATE_MEANING,observations_equal)",
    "CS(PREDICATE_MEANING,task_accepts)",
    "CS(PREDICATE_MEANING,dependency_metadata_changed)",
    "CS(PREDICATE_MEANING,verification_passed)",
    "CS(PREDICATE_MEANING,event_matches)", "CS(PREDICATE_MEANING,event_occurred)",
    "CS(PREDICATE_MEANING,refresh_scope)", "CS(OCCURRENCE_MEANING,refresh_occurred)",
    "CS(EVIDENCE_SCHEMA,verification)", "CS(ACCESS_BOUNDARY,state_only)",
    "CS(ACCESS_BOUNDARY,snapshot_pair)", "CS(ACCESS_BOUNDARY,spec_snapshot)",
    "CS(ACCESS_BOUNDARY,result_pair)", "CS(ACCESS_BOUNDARY,task_final_evidence)",
    "CS(ACCESS_BOUNDARY,change_set_only)",
    "CS(ACCESS_BOUNDARY,verification_snapshot_evidence)",
    "CS(ACCESS_BOUNDARY,pattern_event)", "CS(ACCESS_BOUNDARY,pattern_trace)",
    "CS(ACCESS_BOUNDARY,event_only)", "CS(UNKNOWN_BEHAVIOR,not_applicable)",
    "CS(UNKNOWN_BEHAVIOR,never)", "CS(UNKNOWN_BEHAVIOR,evidence_pending)",
    "CS(UNKNOWN_BEHAVIOR,task)", "CS(EVALUATION_ERROR_BEHAVIOR,term)",
)
_EXPECTED_RETAINED_SERVICE_MEMBERS: tuple[IdentityLiteral, ...] = tuple(
    ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.contract", local, (1,))
    for local in _EXPECTED_ORDINARY_SPEC_LOCALS
) + tuple(
    (kind, "capknow.semantic", namespace, local, (1,))
    for kind, namespace, local in (
        *(("CAPABILITY_RECORD", "coding.capability", f"CAP({name})")
          for name in ("functions", "predicates", "profile", "bounds", "confluence")),
        ("CAPABILITY_RECORD", "coding.capability", "LEX_CAP"),
        *(("SERVICE_RECORD", "coding.service", f"SK({name})")
          for name in ("functions", "predicates", "profile", "bounds", "confluence")),
        ("SERVICE_RECORD", "coding.service", "LEXSK"),
        *(("CONTRACT_SPEC_RECORD", "coding.service.contract", local)
          for local in ("FSOUND", "FREQ", "FFAIL",
                        "PROFSOUND", "PROFREQ", "PROFFAIL",
                        "BSOUND", "BCOMPLETE", "BREQ", "BFAIL",
                        "LEX_SOUND", "LEX_REQ", "LEX_FAIL",
                        "CSOUND", "CREQ", "CFAIL")),
        *(("CONTRACT_SPEC_RECORD", "confluence.contract", local)
          for local in ("CS(ACCESS_BOUNDARY,snapshot_pair)",
                        "CS(CONFLUENCE,changes_between)", "CS(CONFLUENCE,observe)",
                        "CS(EVALUATION_ERROR_BEHAVIOR,term)",
                        "CS(EVIDENCE_SCHEMA,none)", "CS(UNKNOWN_BEHAVIOR,never)")),
    )
) + (
    ("CERTIFICATE_RECORD", "PLUGIN_CERTIFICATE_ISSUER(CK)",
     "coding.certificate", "bundle_bounds_unsat", (1,)),
)
_EXPECTED_RETAINED_CONFLUENCE_MEMBERS = (
    _EXPECTED_RETAINED_SYMBOL_IDENTITIES + _EXPECTED_RETAINED_SERVICE_MEMBERS)
_EXPECTED_RETAINED_CYCLE_MEMBERS: tuple[IdentityLiteral, ...] = ()
_EXPECTED_PROFILE_IMPL_SPECS: tuple[IdentityLiteral, ...] = tuple(
    ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.contract", local, (1,))
    for local in (
        "CS(PROFILE_COVERAGE,implementation_evidence)",
        "CS(EVIDENCE_SCHEMA,implementation_profile)",
        "CS(EVALUATION_ERROR_BEHAVIOR,profile)",
        "CS(REASONING_ERROR_BEHAVIOR,profile)",
    ))
_EXPECTED_RETAINED_CORE_UNIVERSE_ADDITIONS = (
    _EXPECTED_RETAINED_TYPE_IDENTITIES
    + _EXPECTED_RETAINED_LITERAL_IDENTITIES
    + _EXPECTED_RETAINED_CONFLUENCE_MEMBERS
    + _EXPECTED_PROFILE_IMPL_SPECS
)
_EXPECTED_RETAINED_CORE_WITHOUT_MODELS = tuple(
    identity for identity in _EXPECTED_RETAINED_CORE_UNIVERSE_ADDITIONS
    if identity[0] != "MODEL_CONTRACT_RECORD"
)
_EXPECTED_RETAINED_CYCLE_UNIVERSE_ADDITIONS = (
    _EXPECTED_RETAINED_TYPE_IDENTITIES
    + _EXPECTED_RETAINED_LITERAL_IDENTITIES
    + tuple(identity for identity in _EXPECTED_RETAINED_CONFLUENCE_MEMBERS
            if identity[0] != "CAPABILITY_RECORD" and identity[0] != "SERVICE_RECORD")
    + _EXPECTED_PROFILE_IMPL_SPECS
)
_EXPECTED_CONFLUENCE_REPAIR6_ADDITIONS: tuple[IdentityLiteral, ...] = (
    *_EXPECTED_RETAINED_CORE_ADDITIONS,
    _EI_014_CAP_predicates, _EI_159_SK_predicates,
    ("MODEL_CONTRACT_RECORD", "capknow.semantic", "confluence.model", "MODEL_changes_between_confluence", (1,)),
    ("MODEL_CONTRACT_RECORD", "capknow.semantic", "confluence.model", "MODEL_observe_confluence", (1,)),
    ("OUTCOME_RECORD", "capknow.semantic", "confluence.contract", "C_c", (1,)),
)
_EVOLUTION_MISSING_ROWS = frozenset({
    MissingRowId.MIGRATION, MissingRowId.COMPATIBILITY_CLAIM,
    MissingRowId.EXTENSION_OPTIONAL, MissingRowId.EXTENSION_REQUIRED,
    MissingRowId.ALIAS_OPTIONAL, MissingRowId.ALIAS_REQUIRED,
})
_EXPECTED_EVOLUTION_REPAIR10_ADDITIONS: tuple[IdentityLiteral, ...] = tuple(
    identity
    for name in (
        "CodingEvidenceEntry", "CodingEvidencePayload",
        "ImplementationEvidence", "SnapshotIdentity",
        "VerificationRecord", "VerificationStatus",
    )
    for identity in (
        ("TYPE_DECLARATION_RECORD", "capknow.semantic", "coding.type",
         f"T({name})", (1,)),
        ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.type-admission",
         f"CS(TYPE_ADMISSION,type.{name})", (1,)),
    ))

_EXPECTED_REPLAY_ASSERTIONS_LITERAL: dict[FixtureId, ReplayAssertion] = {
    FixtureId(FixtureFamily.CORE_DEFINITIONAL): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED, _EI_150_E_t, _EI_159_SK_predicates, _EI_165_T_admitted, _EI_171_TP, _EI_174_TR, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ("CORE", Formation.WELL_FORMED, Closure.CLOSED, Evaluability.AVAILABLE,
         'INVOCABLE_FOR(Q_t[ADMITTED])', Eval(Truth.TRUE)),
    ),
    FixtureId(FixtureFamily.PAIR_INDEPENDENT): ReplayAssertion(
        (_EI_000_ABI0, _EI_006_B_alt_refresh_occurred, _EI_007_B_alt_refresh_scope, _EI_012_PVC, _EI_015_PCERT, _EI_020_PCOMPLETE, _EI_021_PEVIDENCE, _EI_022_PFAILURE, _EI_023_PSOUND, _EI_032_CS_PREDICATE_MEANING_refresh_occurred, _EI_033_CS_PREDICATE_MEANING_refresh_scope, _EI_036_T3_A1_ACCESS_LIFT, _EI_037_T3_A1_ERROR_LIFT, _EI_038_T3_A1_EVIDENCE_LIFT, _EI_039_T3_A1_UNKNOWN_LIFT, _EI_085_DP_refresh_occurred, _EI_086_DP_refresh_scope, _EI_096_D_p, _EI_097_DE_dependency_refresh, _EI_099_PAIR_PROOF_REF, _EI_100_PairFullEvalProof, _EI_108_MODEL_refresh_occurred_pair, _EI_109_MODEL_refresh_scope_pair, _EI_118_pair_validator, _EI_119_pair_proof, _EI_124_coding_minimal, _EI_125_PB_alt, _EI_126_PAIR_refresh, _EI_127_producer_certificate, _EI_128_producer_pair, _EI_129_producer_trust_environment, _EI_130_producer_trust_policy, _EI_131_producer_trust_root, _EI_132_producer_validation_capability, _EI_133_producer_validation_proof, _EI_138_R_p, _EI_154_E_p, _EI_157_PVSK, _EI_163_T_p, _EI_170_TP, _EI_173_TRP),
        (),
        ("PAIR", Formation.WELL_FORMED, Closure.CLOSED, ('capknow.semantic', 'pair', 'PAIR(refresh)', (1,)), ('capknow.audit.pair-proof', 'pair.certificate', 'PCERT', (1,)), 'PAIR_COHERENCE_ADMITTED'),
    ),
    FixtureId(FixtureFamily.TRUST_BRANCH, (TrustFixtureTag.ADMITTED,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED, _EI_150_E_t, _EI_159_SK_predicates, _EI_165_T_admitted, _EI_171_TP, _EI_174_TR, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ("CORE", Formation.WELL_FORMED, Closure.CLOSED, Evaluability.AVAILABLE,
         'INVOCABLE_FOR(Q_t[ADMITTED])', Eval(Truth.TRUE)),
    ),
    FixtureId(FixtureFamily.TRUST_BRANCH, (TrustFixtureTag.ABSENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_139_Q_t_ABSENT, _EI_150_E_t, _EI_159_SK_predicates, _EI_164_T_absent, _EI_171_TP, _EI_174_TR, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ("CORE", Formation.WELL_FORMED, Closure.CLOSED, Evaluability.MISSING, 'TRUST_ROOT_ABSENT', None),
    ),
    FixtureId(FixtureFamily.TRUST_BRANCH, (TrustFixtureTag.UNDECIDED,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_143_Q_t_UNDECIDED, _EI_150_E_t, _EI_159_SK_predicates, _EI_168_T_undecided, _EI_171_TP, _EI_174_TR, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ("CORE", Formation.WELL_FORMED, Closure.CLOSED, Evaluability.UNKNOWN, 'TRUST_ROOT_UNDECIDED', None),
    ),
    FixtureId(FixtureFamily.TRUST_BRANCH, (TrustFixtureTag.INCOMPATIBLE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_142_Q_t_INCOMPATIBLE, _EI_150_E_t, _EI_159_SK_predicates, _EI_167_T_incompatible, _EI_171_TP, _EI_174_TR, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ("CORE", Formation.WELL_FORMED, Closure.CLOSED, Evaluability.MISSING, 'TRUST_ROOT_INCOMPATIBLE', None),
    ),
    FixtureId(FixtureFamily.TRUST_BRANCH, (TrustFixtureTag.FAILED,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_141_Q_t_FAILED, _EI_150_E_t, _EI_159_SK_predicates, _EI_166_T_failed, _EI_171_TP, _EI_174_TR, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ("CORE", Formation.WELL_FORMED, Closure.CLOSED, Evaluability.UNKNOWN, 'DISCOVERY_FAILED', None),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.ABI,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('ABI_RECORD', 'capknow.semantic', 'abi', 'ABI0', (0,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.ABI,)): ReplayAssertion(
        (_EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.PLUGIN,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('PACKAGE_RECORD', 'capknow.semantic', 'plugin', 'coding-minimal', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.PLUGIN,)): ReplayAssertion(
        (_EI_000_ABI0,),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.DECLARATION,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('DECLARATION_RECORD', 'capknow.semantic', 'coding.declaration', 'DP(task_accepts)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.DECLARATION,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.SYMBOL,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('DECLARATION_RECORD', 'capknow.semantic', 'coding.declaration', 'DP(task_accepts)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.SYMBOL,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.EVENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('EVENT_DECLARATION_RECORD', 'capknow.semantic', 'coding.declaration', 'DE(dependency_refresh)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.EVENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.PAIR_DECLARATION,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_006_B_alt_refresh_occurred, _EI_007_B_alt_refresh_scope, _EI_020_PCOMPLETE, _EI_021_PEVIDENCE, _EI_022_PFAILURE, _EI_023_PSOUND, _EI_032_CS_PREDICATE_MEANING_refresh_occurred, _EI_033_CS_PREDICATE_MEANING_refresh_scope, _EI_036_T3_A1_ACCESS_LIFT, _EI_037_T3_A1_ERROR_LIFT, _EI_038_T3_A1_EVIDENCE_LIFT, _EI_039_T3_A1_UNKNOWN_LIFT, _EI_085_DP_refresh_occurred, _EI_086_DP_refresh_scope, _EI_096_D_p, _EI_099_PAIR_PROOF_REF, _EI_100_PairFullEvalProof, _EI_108_MODEL_refresh_occurred_pair, _EI_109_MODEL_refresh_scope_pair, _EI_124_coding_minimal, _EI_125_PB_alt, _EI_126_PAIR_refresh, _EI_127_producer_certificate, _EI_128_producer_pair, _EI_129_producer_trust_environment, _EI_130_producer_trust_policy, _EI_131_producer_trust_root, _EI_132_producer_validation_capability, _EI_133_producer_validation_proof, _EI_138_R_p, _EI_154_E_p, _EI_157_PVSK, _EI_163_T_p, _EI_170_TP, _EI_173_TRP),
        (),
        ('LOOKUP', 'PRESENT', (('PAIR_DECLARATION_RECORD', 'capknow.semantic', 'pair', 'PAIR(refresh)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.PAIR_DECLARATION,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_006_B_alt_refresh_occurred, _EI_007_B_alt_refresh_scope, _EI_020_PCOMPLETE, _EI_021_PEVIDENCE, _EI_022_PFAILURE, _EI_023_PSOUND, _EI_032_CS_PREDICATE_MEANING_refresh_occurred, _EI_033_CS_PREDICATE_MEANING_refresh_scope, _EI_036_T3_A1_ACCESS_LIFT, _EI_037_T3_A1_ERROR_LIFT, _EI_038_T3_A1_EVIDENCE_LIFT, _EI_039_T3_A1_UNKNOWN_LIFT, _EI_085_DP_refresh_occurred, _EI_086_DP_refresh_scope, _EI_096_D_p, _EI_099_PAIR_PROOF_REF, _EI_100_PairFullEvalProof, _EI_108_MODEL_refresh_occurred_pair, _EI_109_MODEL_refresh_scope_pair, _EI_124_coding_minimal, _EI_125_PB_alt, _EI_127_producer_certificate, _EI_128_producer_pair, _EI_129_producer_trust_environment, _EI_130_producer_trust_policy, _EI_131_producer_trust_root, _EI_132_producer_validation_capability, _EI_133_producer_validation_proof, _EI_138_R_p, _EI_154_E_p, _EI_157_PVSK, _EI_163_T_p, _EI_170_TP, _EI_173_TRP),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.OUTCOME,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_116_O_w),
        (),
        ('LOOKUP', 'PRESENT', (('OUTCOME_RECORD', 'capknow.semantic', 'outcome', 'O_w', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.OUTCOME,)): ReplayAssertion(
        (_EI_000_ABI0,),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('BINDING_RECORD', 'capknow.semantic', 'coding.binding', 'BINDING(DP(task_accepts))', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'OPEN_BINDINGS', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.PROFILE_BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('PROFILE_BINDING_RECORD', 'capknow.semantic', 'coding.binding', 'PROFILE_BINDING(PK(implementation_evidence))', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.PROFILE_BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'OPEN_BINDINGS', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.PAIR_BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_006_B_alt_refresh_occurred, _EI_007_B_alt_refresh_scope, _EI_020_PCOMPLETE, _EI_021_PEVIDENCE, _EI_022_PFAILURE, _EI_023_PSOUND, _EI_032_CS_PREDICATE_MEANING_refresh_occurred, _EI_033_CS_PREDICATE_MEANING_refresh_scope, _EI_036_T3_A1_ACCESS_LIFT, _EI_037_T3_A1_ERROR_LIFT, _EI_038_T3_A1_EVIDENCE_LIFT, _EI_039_T3_A1_UNKNOWN_LIFT, _EI_085_DP_refresh_occurred, _EI_086_DP_refresh_scope, _EI_096_D_p, _EI_099_PAIR_PROOF_REF, _EI_100_PairFullEvalProof, _EI_108_MODEL_refresh_occurred_pair, _EI_109_MODEL_refresh_scope_pair, _EI_124_coding_minimal, _EI_125_PB_alt, _EI_126_PAIR_refresh, _EI_127_producer_certificate, _EI_128_producer_pair, _EI_129_producer_trust_environment, _EI_130_producer_trust_policy, _EI_131_producer_trust_root, _EI_132_producer_validation_capability, _EI_133_producer_validation_proof, _EI_138_R_p, _EI_154_E_p, _EI_157_PVSK, _EI_163_T_p, _EI_170_TP, _EI_173_TRP),
        (),
        ('LOOKUP', 'PRESENT', (('PAIR_BINDING_RECORD', 'capknow.semantic', 'pair.binding', 'PB_alt', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.PAIR_BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_006_B_alt_refresh_occurred, _EI_007_B_alt_refresh_scope, _EI_020_PCOMPLETE, _EI_021_PEVIDENCE, _EI_022_PFAILURE, _EI_023_PSOUND, _EI_032_CS_PREDICATE_MEANING_refresh_occurred, _EI_033_CS_PREDICATE_MEANING_refresh_scope, _EI_036_T3_A1_ACCESS_LIFT, _EI_037_T3_A1_ERROR_LIFT, _EI_038_T3_A1_EVIDENCE_LIFT, _EI_039_T3_A1_UNKNOWN_LIFT, _EI_085_DP_refresh_occurred, _EI_086_DP_refresh_scope, _EI_096_D_p, _EI_099_PAIR_PROOF_REF, _EI_100_PairFullEvalProof, _EI_108_MODEL_refresh_occurred_pair, _EI_109_MODEL_refresh_scope_pair, _EI_124_coding_minimal, _EI_126_PAIR_refresh, _EI_127_producer_certificate, _EI_128_producer_pair, _EI_129_producer_trust_environment, _EI_130_producer_trust_policy, _EI_131_producer_trust_root, _EI_132_producer_validation_capability, _EI_133_producer_validation_proof, _EI_138_R_p, _EI_154_E_p, _EI_157_PVSK, _EI_163_T_p, _EI_170_TP, _EI_173_TRP),
        (),
        ('LOOKUP', 'OPEN_BINDINGS', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.AUTHORITY_FACT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_003_AF_choice_1, _EI_123_authority_owner, _EI_147_E_choice),
        (),
        ('LOOKUP', 'PRESENT', (('AUTHORITY_FACT_RECORD', 'capknow.semantic', 'authority', 'AF(choice,1)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.AUTHORITY_FACT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_123_authority_owner, _EI_147_E_choice),
        (),
        ('LOOKUP', 'OPEN_BINDINGS', (('AUTHORITY_FACT_RECORD', 'capknow.semantic', 'authority', 'AF(choice,1)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.CHOICE_BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_003_AF_choice_1, _EI_016_cb0, _EI_147_E_choice),
        (),
        ('LOOKUP', 'PRESENT', (('CHOICE_BINDING_RECORD', 'capknow.semantic', 'authority.choice', 'cb0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.CHOICE_BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_003_AF_choice_1, _EI_147_E_choice),
        (),
        ('LOOKUP', 'OPEN_BINDINGS', (('CHOICE_BINDING_RECORD', 'capknow.semantic', 'authority.choice', 'cb0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.LEXICAL_BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_095_D_lex, _EI_102_lk0, _EI_137_R_lex, _EI_153_E_lex),
        (),
        ('LOOKUP', 'PRESENT', (('LEXICAL_BINDING_RECORD', 'capknow.semantic', 'lexical', 'lk0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.LEXICAL_BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_095_D_lex, _EI_137_R_lex, _EI_153_E_lex),
        (),
        ('LOOKUP', 'OPEN_BINDINGS', (('LEXICAL_BINDING_RECORD', 'capknow.semantic', 'lexical', 'lk0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.EXTRANEOUS_LEXICAL_BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_140_Q_t_ADMITTED, _EI_150_E_t, _EI_159_SK_predicates, _EI_165_T_admitted, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t[ADMITTED]', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.EXTRANEOUS_LEXICAL_BINDING,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_093_D_t_extra, _EI_097_DE_dependency_refresh, _EI_103_lk_extra, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_144_Q_t_extra, _EI_152_E_t_extra, _EI_159_SK_predicates, _EI_165_T_admitted, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'MALFORMED_REQUEST', ('EXTRANEOUS_LEXICAL_BINDING', ('LEXICAL_BINDING_RECORD', 'capknow.semantic', 'lexical', 'lk_extra', (1,)))),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.SERVICE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_140_Q_t_ADMITTED, _EI_150_E_t, _EI_159_SK_predicates, _EI_165_T_admitted, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('SERVICE_RECORD', 'capknow.semantic', 'coding.service', 'SK(predicates)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.SERVICE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_140_Q_t_ADMITTED, _EI_150_E_t, _EI_165_T_admitted, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'EVALUABILITY_MISSING', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.CAPABILITY,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_140_Q_t_ADMITTED, _EI_150_E_t, _EI_159_SK_predicates, _EI_165_T_admitted, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('CAPABILITY_RECORD', 'capknow.semantic', 'coding.capability', 'CAP(predicates)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.CAPABILITY,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_091_D_t, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_140_Q_t_ADMITTED, _EI_150_E_t, _EI_159_SK_predicates, _EI_165_T_admitted, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'EVALUABILITY_MISSING', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.TRUST_POLICY,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_165_T_admitted, _EI_171_TP),
        (),
        ('LOOKUP', 'PRESENT', (('TRUST_POLICY_RECORD', 'capknow.semantic', 'trust', 'TP', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.TRUST_POLICY,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_165_T_admitted),
        (),
        ('LOOKUP', 'TRUST_ROOT_ABSENT', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.TRUST_ROOT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_165_T_admitted, _EI_171_TP, _EI_174_TR),
        (),
        ('LOOKUP', 'PRESENT', (('TRUST_ROOT_RECORD', 'capknow.semantic', 'trust', 'TR', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.TRUST_ROOT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_165_T_admitted, _EI_171_TP),
        (),
        ('LOOKUP', 'TRUST_ROOT_ABSENT', (('TRUST_ROOT_RECORD', 'capknow.semantic', 'trust', 'TR', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.CERTIFICATE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_006_B_alt_refresh_occurred, _EI_007_B_alt_refresh_scope, _EI_012_PVC, _EI_015_PCERT, _EI_020_PCOMPLETE, _EI_021_PEVIDENCE, _EI_022_PFAILURE, _EI_023_PSOUND, _EI_032_CS_PREDICATE_MEANING_refresh_occurred, _EI_033_CS_PREDICATE_MEANING_refresh_scope, _EI_036_T3_A1_ACCESS_LIFT, _EI_037_T3_A1_ERROR_LIFT, _EI_038_T3_A1_EVIDENCE_LIFT, _EI_039_T3_A1_UNKNOWN_LIFT, _EI_085_DP_refresh_occurred, _EI_086_DP_refresh_scope, _EI_096_D_p, _EI_099_PAIR_PROOF_REF, _EI_100_PairFullEvalProof, _EI_108_MODEL_refresh_occurred_pair, _EI_109_MODEL_refresh_scope_pair, _EI_118_pair_validator, _EI_119_pair_proof, _EI_124_coding_minimal, _EI_125_PB_alt, _EI_126_PAIR_refresh, _EI_127_producer_certificate, _EI_128_producer_pair, _EI_129_producer_trust_environment, _EI_130_producer_trust_policy, _EI_131_producer_trust_root, _EI_132_producer_validation_capability, _EI_133_producer_validation_proof, _EI_138_R_p, _EI_154_E_p, _EI_157_PVSK, _EI_163_T_p, _EI_170_TP, _EI_173_TRP),
        (),
        ('LOOKUP', 'PRESENT', (('CERTIFICATE_RECORD', 'capknow.audit.pair-proof', 'pair.certificate', 'PCERT', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.CERTIFICATE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_006_B_alt_refresh_occurred, _EI_007_B_alt_refresh_scope, _EI_012_PVC, _EI_020_PCOMPLETE, _EI_021_PEVIDENCE, _EI_022_PFAILURE, _EI_023_PSOUND, _EI_032_CS_PREDICATE_MEANING_refresh_occurred, _EI_033_CS_PREDICATE_MEANING_refresh_scope, _EI_036_T3_A1_ACCESS_LIFT, _EI_037_T3_A1_ERROR_LIFT, _EI_038_T3_A1_EVIDENCE_LIFT, _EI_039_T3_A1_UNKNOWN_LIFT, _EI_085_DP_refresh_occurred, _EI_086_DP_refresh_scope, _EI_096_D_p, _EI_099_PAIR_PROOF_REF, _EI_100_PairFullEvalProof, _EI_108_MODEL_refresh_occurred_pair, _EI_109_MODEL_refresh_scope_pair, _EI_118_pair_validator, _EI_119_pair_proof, _EI_124_coding_minimal, _EI_125_PB_alt, _EI_126_PAIR_refresh, _EI_127_producer_certificate, _EI_128_producer_pair, _EI_129_producer_trust_environment, _EI_130_producer_trust_policy, _EI_131_producer_trust_root, _EI_132_producer_validation_capability, _EI_133_producer_validation_proof, _EI_138_R_p, _EI_154_E_p, _EI_157_PVSK, _EI_163_T_p, _EI_170_TP, _EI_173_TRP),
        (),
        ('LOOKUP', 'NO_CERTIFICATE_ADMISSION', ('CONSISTENCY_UNKNOWN',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.MIGRATION,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_002_AK1, _EI_017_CCK0, _EI_106_MK0, _EI_120_evolution_owner, _EI_155_XK0, _EI_156_XK1),
        (),
        ('LOOKUP', 'PRESENT', (('MIGRATION_RECORD', 'capknow.fixture.evolution-owner', 'evolution', 'MK0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.MIGRATION,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_002_AK1, _EI_017_CCK0, _EI_120_evolution_owner, _EI_155_XK0, _EI_156_XK1),
        (),
        ('LOOKUP', 'NO_MIGRATION', ('MK0',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.COMPATIBILITY_CLAIM,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_002_AK1, _EI_017_CCK0, _EI_106_MK0, _EI_120_evolution_owner, _EI_155_XK0, _EI_156_XK1),
        (),
        ('LOOKUP', 'PRESENT', (('COMPATIBILITY_RECORD', 'capknow.fixture.evolution-owner', 'evolution', 'CCK0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.COMPATIBILITY_CLAIM,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_002_AK1, _EI_106_MK0, _EI_120_evolution_owner, _EI_155_XK0, _EI_156_XK1),
        (),
        ('LOOKUP', 'NO_COMPATIBILITY', ('CCK0',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.EXTENSION_OPTIONAL,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_002_AK1, _EI_017_CCK0, _EI_106_MK0, _EI_120_evolution_owner, _EI_155_XK0, _EI_156_XK1),
        (),
        ('LOOKUP', 'PRESENT', (('SEMANTIC_EXTENSION_RECORD', 'capknow.fixture.evolution-owner', 'evolution', 'XK0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.EXTENSION_OPTIONAL,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_002_AK1, _EI_017_CCK0, _EI_106_MK0, _EI_120_evolution_owner, _EI_156_XK1),
        (),
        ('LOOKUP', 'NO_EFFECT', ('XK0',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.EXTENSION_REQUIRED,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_002_AK1, _EI_017_CCK0, _EI_106_MK0, _EI_120_evolution_owner, _EI_155_XK0, _EI_156_XK1),
        (),
        ('LOOKUP', 'PRESENT', (('SEMANTIC_EXTENSION_RECORD', 'capknow.fixture.evolution-owner', 'evolution', 'XK1', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.EXTENSION_REQUIRED,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_002_AK1, _EI_017_CCK0, _EI_106_MK0, _EI_120_evolution_owner, _EI_155_XK0),
        (),
        ('LOOKUP', 'INCOMPATIBLE', ('XK1',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.MODEL_CONTRACT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('MODEL_CONTRACT_RECORD', 'capknow.semantic', 'coding.model', 'MODEL_task_accepts', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.MODEL_CONTRACT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'OPEN_BINDINGS', ('MODEL_CONTRACT',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.ALIAS_OPTIONAL,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_002_AK1, _EI_017_CCK0, _EI_106_MK0, _EI_120_evolution_owner, _EI_155_XK0, _EI_156_XK1),
        (),
        ('LOOKUP', 'PRESENT', (('ALIAS_RECORD', 'capknow.fixture.evolution-owner', 'evolution.alias', 'AK0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.ALIAS_OPTIONAL,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_002_AK1, _EI_017_CCK0, _EI_106_MK0, _EI_120_evolution_owner, _EI_155_XK0, _EI_156_XK1),
        (),
        ('LOOKUP', 'NO_ALIAS', ('AK0',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.ALIAS_REQUIRED,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_002_AK1, _EI_017_CCK0, _EI_106_MK0, _EI_120_evolution_owner, _EI_155_XK0, _EI_156_XK1),
        (),
        ('LOOKUP', 'PRESENT', (('ALIAS_RECORD', 'capknow.fixture.evolution-owner', 'evolution.alias', 'AK1', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.ALIAS_REQUIRED,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_001_AK0, _EI_017_CCK0, _EI_106_MK0, _EI_120_evolution_owner, _EI_155_XK0, _EI_156_XK1),
        (),
        ('LOOKUP', 'MALFORMED', ('MISSING_ALIAS', 'AK1')),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.SIGMA_CONTRACT_SPEC,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.contract', 'CS(PREDICATE_MEANING,task_accepts)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.SIGMA_CONTRACT_SPEC,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_031_CS_PREDICATE_MEANING_observations_equal, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'BINDING_INCOMPATIBLE', ('OPEN_BINDINGS',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.SERVICE_CONTRACT_SPEC,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_044_QFAIL, _EI_045_QREQ, _EI_046_QSOUND, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'PRESENT', (('CONTRACT_SPEC_RECORD', 'capknow.semantic', 'coding.service.contract', 'QSOUND', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.SERVICE_CONTRACT_SPEC,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_005_BINDING_DP_task_accepts, _EI_014_CAP_predicates, _EI_028_CS_ACCESS_BOUNDARY_task_final_evidence, _EI_029_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_030_CS_EVIDENCE_SCHEMA_verification, _EI_034_CS_PREDICATE_MEANING_task_accepts, _EI_035_CS_UNKNOWN_BEHAVIOR_predicate, _EI_043_FSOUND, _EI_044_QFAIL, _EI_045_QREQ, _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec, _EI_087_DP_task_accepts, _EI_097_DE_dependency_refresh, _EI_107_MODEL_task_accepts, _EI_124_coding_minimal, _EI_134_PROFILE_BINDING_PK_implementation_evidence, _EI_159_SK_predicates, _EI_179_RepositorySnapshot, _EI_204_TaskSpec),
        (),
        ('LOOKUP', 'CAPABILITY_INCOMPATIBLE', ('EVALUABILITY_MISSING',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.REQUEST,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED),
        (),
        ('LOOKUP', 'PRESENT', (('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t[ADMITTED]', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.REQUEST,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_146_RES_t_ADMITTED),
        (),
        ('LOOKUP', 'MALFORMED_REQUEST', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.RESULT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED),
        (),
        ('LOOKUP', 'PRESENT', (('RESULT_RECORD', 'capknow.semantic', 'result', 'RES_t[ADMITTED]', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.RESULT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_140_Q_t_ADMITTED),
        (),
        ('LOOKUP', 'INVOCATION_FAILED', ('PROTOCOL', 'NO_RESULT', 'NO_TRUTH')),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.SEMANTIC_ENVIRONMENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_091_D_t, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED, _EI_150_E_t),
        (),
        ('LOOKUP', 'PRESENT', (('SEMANTIC_ENVIRONMENT_RECORD', 'capknow.semantic', 'environment', 'E_t', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.SEMANTIC_ENVIRONMENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_092_D_t_empty, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED, _EI_151_E_t_empty),
        (),
        ('LOOKUP', 'MALFORMED_REQUEST', (('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t[ADMITTED]', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.TRUST_ENVIRONMENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED, _EI_165_T_admitted),
        (),
        ('LOOKUP', 'PRESENT', (('TRUST_ENVIRONMENT_RECORD', 'capknow.semantic', 'trust', 'T_admitted', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.TRUST_ENVIRONMENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED, _EI_164_T_absent),
        (),
        ('LOOKUP', 'MALFORMED_REQUEST', (('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t[ADMITTED]', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.DEPENDENCY_ENVIRONMENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_091_D_t, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED),
        (),
        ('LOOKUP', 'PRESENT', (('DEPENDENCY_ENVIRONMENT_RECORD', 'capknow.semantic', 'environment', 'D_t', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.DEPENDENCY_ENVIRONMENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_094_D_t_incomplete, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED),
        (),
        ('LOOKUP', 'MALFORMED_REQUEST', (('REQUEST_RECORD', 'capknow.semantic', 'request', 'Q_t[ADMITTED]', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.OBSERVATION_ENVIRONMENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_104_L_c_final, _EI_110_M_c, _EI_136_R_c, _EI_145_Y_c),
        (),
        ('LOOKUP', 'PRESENT', (('OBSERVATION_ENVIRONMENT_RECORD', 'capknow.semantic', 'confluence.result', 'M_c', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.OBSERVATION_ENVIRONMENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_104_L_c_final, _EI_111_M_c_missing, _EI_136_R_c, _EI_145_Y_c),
        (),
        ('LOOKUP', 'MALFORMED_RESULT', ('SEMANTIC_MISMATCH',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.LIFECYCLE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_104_L_c_final, _EI_136_R_c),
        (),
        ('LOOKUP', 'PRESENT', (('LIFECYCLE_RECORD', 'capknow.semantic', 'confluence.lifecycle', 'L_c_final', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.LIFECYCLE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_105_L_life_after, _EI_136_R_c),
        (),
        ('LOOKUP', 'LIFECYCLE_REPLACED', (('LIFECYCLE_RECORD', 'capknow.semantic', 'confluence.lifecycle', 'L_life_after', (1,)), 'INVOCABLE_FOR')),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.EVENT_VALUE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_097_DE_dependency_refresh, _EI_098_ev0, _EI_161_te0),
        (),
        ('LOOKUP', 'PRESENT', (('EVENT_VALUE_RECORD', 'capknow.semantic', 'event.value', 'ev0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.EVENT_VALUE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_097_DE_dependency_refresh),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.TRACE_EVENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_098_ev0, _EI_161_te0),
        (),
        ('LOOKUP', 'PRESENT', (('TRACE_EVENT_RECORD', 'capknow.semantic', 'event.trace', 'te0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.TRACE_EVENT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_098_ev0),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.SOURCE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_160_SRC_choice_1),
        (),
        ('LOOKUP', 'PRESENT', (('SOURCE_RECORD', 'capknow.semantic', 'authority.source', 'SRC(choice,1)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.SOURCE,)): ReplayAssertion(
        (_EI_000_ABI0,),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.AUTHORITY_REF,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_004_AUTH_choice_1),
        (),
        ('LOOKUP', 'PRESENT', (('AUTHORITY_REF_RECORD', 'capknow.semantic', 'authority.ref', 'AUTH(choice,1)', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.AUTHORITY_REF,)): ReplayAssertion(
        (_EI_000_ABI0,),
        (),
        ('LOOKUP', 'MALFORMED', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.EVIDENCE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_101_e0, _EI_115_t_t_evidence_subject),
        (),
        ('LOOKUP', 'PRESENT', (('EVIDENCE_RECORD', 'capknow.semantic', 'evidence', 'e0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.EVIDENCE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_115_t_t_evidence_subject),
        (),
        ('LOOKUP', 'TRUTH_UNKNOWN', ()),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.REASON,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_117_VALUE_UNKNOWN, _EI_135_u0),
        (),
        ('LOOKUP', 'PRESENT', (('REASON_RECORD', 'capknow.semantic', 'reason', 'u0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.REASON,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_117_VALUE_UNKNOWN),
        (),
        ('LOOKUP', 'MALFORMED_RESULT', ('MALFORMED_CARRIER',)),
    ),
    FixtureId(FixtureFamily.MISSING_BASE, (MissingRowId.CONFLICT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_018_conflict0, _EI_087_DP_task_accepts),
        (),
        ('LOOKUP', 'PRESENT', (('CONFLICT_RECORD', 'capknow.semantic', 'conflict', 'conflict0', (1,)),)),
    ),
    FixtureId(FixtureFamily.MISSING_VARIANT, (MissingRowId.CONFLICT,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_019_conflict1, _EI_087_DP_task_accepts),
        (),
        ('LOOKUP', 'CONFLICT_REPLACED', (('CONFLICT_RECORD', 'capknow.semantic', 'conflict', 'conflict1', (1,)), 'MALFORMED')),
    ),
    FixtureId(FixtureFamily.CONFLUENCE_ORDER, (OrderTag.FORWARD,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_008_BINDING_DF_changes_between, _EI_009_BINDING_DF_observe, _EI_013_CAP_confluence, _EI_040_CFAIL, _EI_041_CREQ, _EI_042_CSOUND, _EI_073_CS_ACCESS_BOUNDARY_snapshot_pair, _EI_074_CS_CONFLUENCE_changes_between, _EI_075_CS_CONFLUENCE_observe, _EI_076_CS_EVALUATION_ERROR_BEHAVIOR_term, _EI_077_CS_EVIDENCE_SCHEMA_none, _EI_078_CS_UNKNOWN_BEHAVIOR_never, _EI_090_D_c, _EI_104_L_c_final, _EI_110_M_c, _EI_114_K_c, _EI_124_coding_minimal, _EI_136_R_c, _EI_145_Y_c, _EI_148_E_c, _EI_158_SK_confluence, _EI_162_T_c, _EI_169_TP, _EI_172_ROOT_TR_c),
        (),
        _EXPECTED_CONFLUENCE_OUTCOME,
    ),
    FixtureId(FixtureFamily.CONFLUENCE_ORDER, (OrderTag.REVERSE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_008_BINDING_DF_changes_between, _EI_009_BINDING_DF_observe, _EI_013_CAP_confluence, _EI_040_CFAIL, _EI_041_CREQ, _EI_042_CSOUND, _EI_073_CS_ACCESS_BOUNDARY_snapshot_pair, _EI_074_CS_CONFLUENCE_changes_between, _EI_075_CS_CONFLUENCE_observe, _EI_076_CS_EVALUATION_ERROR_BEHAVIOR_term, _EI_077_CS_EVIDENCE_SCHEMA_none, _EI_078_CS_UNKNOWN_BEHAVIOR_never, _EI_090_D_c, _EI_104_L_c_final, _EI_110_M_c, _EI_114_K_c, _EI_124_coding_minimal, _EI_136_R_c, _EI_145_Y_c, _EI_148_E_c, _EI_158_SK_confluence, _EI_162_T_c, _EI_169_TP, _EI_172_ROOT_TR_c),
        (),
        _EXPECTED_CONFLUENCE_OUTCOME,
    ),
    FixtureId(FixtureFamily.PROPER_CYCLE_REJECTION): ReplayAssertion(
        (_EI_000_ABI0, _EI_010_BINDING_DP_event_matches, _EI_011_BINDING_DP_event_occurred, _EI_079_CS_ACCESS_BOUNDARY_pattern_trace, _EI_080_CS_EVALUATION_ERROR_BEHAVIOR_predicate, _EI_081_CS_EVIDENCE_SCHEMA_none, _EI_082_CS_PREDICATE_MEANING_event_matches_cycle, _EI_083_CS_PREDICATE_MEANING_event_occurred, _EI_084_CS_UNKNOWN_BEHAVIOR_never, _EI_088_DP_event_matches, _EI_089_DP_event_occurred, _EI_124_coding_minimal, _EI_149_E_PROPER_CYCLE) + _EXPECTED_CYCLE_ADDITIONS,
        (),
        ("FORMATION", (Formation.MALFORMED, Closure.NOT_APPLICABLE, Judgment("MALFORMED", ("dependency cycle",)))),
    ),
    FixtureId(FixtureFamily.PERMUTATION, (PackageOrderTag.PI1_PI2, RecordOrderTag.DECLARATION_THEN_SPEC,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_024_A_fixture_unit_one, _EI_025_A_fixture_unit_two, _EI_026_A_fixture_unit_four, _EI_027_A_fixture_unit_three, _EI_121_permutation_one, _EI_122_permutation_two, _EI_175_T_fixture_unit_one, _EI_176_T_fixture_unit_two, _EI_177_T_fixture_unit_four, _EI_178_T_fixture_unit_three),
        (),
        ("COMPOSITION", Formation.WELL_FORMED, Closure.CLOSED),
    ),
    FixtureId(FixtureFamily.PERMUTATION, (PackageOrderTag.PI1_PI2, RecordOrderTag.SPEC_THEN_DECLARATION,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_024_A_fixture_unit_one, _EI_025_A_fixture_unit_two, _EI_026_A_fixture_unit_four, _EI_027_A_fixture_unit_three, _EI_121_permutation_one, _EI_122_permutation_two, _EI_175_T_fixture_unit_one, _EI_176_T_fixture_unit_two, _EI_177_T_fixture_unit_four, _EI_178_T_fixture_unit_three),
        (),
        ("COMPOSITION", Formation.WELL_FORMED, Closure.CLOSED),
    ),
    FixtureId(FixtureFamily.PERMUTATION, (PackageOrderTag.PI2_PI1, RecordOrderTag.DECLARATION_THEN_SPEC,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_024_A_fixture_unit_one, _EI_025_A_fixture_unit_two, _EI_026_A_fixture_unit_four, _EI_027_A_fixture_unit_three, _EI_121_permutation_one, _EI_122_permutation_two, _EI_175_T_fixture_unit_one, _EI_176_T_fixture_unit_two, _EI_177_T_fixture_unit_four, _EI_178_T_fixture_unit_three),
        (),
        ("COMPOSITION", Formation.WELL_FORMED, Closure.CLOSED),
    ),
    FixtureId(FixtureFamily.PERMUTATION, (PackageOrderTag.PI2_PI1, RecordOrderTag.SPEC_THEN_DECLARATION,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_024_A_fixture_unit_one, _EI_025_A_fixture_unit_two, _EI_026_A_fixture_unit_four, _EI_027_A_fixture_unit_three, _EI_121_permutation_one, _EI_122_permutation_two, _EI_175_T_fixture_unit_one, _EI_176_T_fixture_unit_two, _EI_177_T_fixture_unit_four, _EI_178_T_fixture_unit_three),
        (),
        ("COMPOSITION", Formation.WELL_FORMED, Closure.CLOSED),
    ),
    FixtureId(FixtureFamily.DUPLICATE_EQUAL, (OrderTag.FORWARD,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_047_CS_TYPE_ADMISSION_type_ArtifactBodyKind, _EI_048_CS_TYPE_ADMISSION_type_ArtifactContent, _EI_049_CS_TYPE_ADMISSION_type_ArtifactProjection, _EI_050_CS_TYPE_ADMISSION_type_ArtifactRole, _EI_051_CS_TYPE_ADMISSION_type_ArtifactSelector, _EI_052_CS_TYPE_ADMISSION_type_BehaviorValue, _EI_053_CS_TYPE_ADMISSION_type_ByteSize, _EI_054_CS_TYPE_ADMISSION_type_ContentIdentity, _EI_055_CS_TYPE_ADMISSION_type_Coverage, _EI_056_CS_TYPE_ADMISSION_type_Criterion, _EI_057_CS_TYPE_ADMISSION_type_FieldId, _EI_058_CS_TYPE_ADMISSION_type_FieldValue, _EI_059_CS_TYPE_ADMISSION_type_Format, _EI_060_CS_TYPE_ADMISSION_type_ObservationRelation, _EI_061_CS_TYPE_ADMISSION_type_ObservationResult, _EI_062_CS_TYPE_ADMISSION_type_ObservationSpec, _EI_063_CS_TYPE_ADMISSION_type_ObservationValue, _EI_064_CS_TYPE_ADMISSION_type_Path, _EI_065_CS_TYPE_ADMISSION_type_PathSegment, _EI_066_CS_TYPE_ADMISSION_type_PathSet, _EI_067_CS_TYPE_ADMISSION_type_RepositorySnapshot, _EI_068_CS_TYPE_ADMISSION_type_SubjectId, _EI_069_CS_TYPE_ADMISSION_type_TaskSpec, _EI_070_CS_TYPE_ADMISSION_type_VerificationSpec, _EI_087_DP_task_accepts, _EI_124_coding_minimal, _EI_180_T_ArtifactBodyKind, _EI_181_T_ArtifactContent, _EI_182_T_ArtifactProjection, _EI_183_T_ArtifactRole, _EI_184_T_ArtifactSelector, _EI_185_T_BehaviorValue, _EI_186_T_ByteSize, _EI_187_T_ContentIdentity, _EI_188_T_Coverage, _EI_189_T_Criterion, _EI_190_T_FieldId, _EI_191_T_FieldValue, _EI_192_T_Format, _EI_193_T_ObservationRelation, _EI_194_T_ObservationResult, _EI_195_T_ObservationSpec, _EI_196_T_ObservationValue, _EI_197_T_Path, _EI_198_T_PathSegment, _EI_199_T_PathSet, _EI_200_T_RepositorySnapshot, _EI_201_T_SubjectId, _EI_202_T_TaskSpec, _EI_203_T_VerificationSpec),
        (),
        ("COMPOSITION", Formation.WELL_FORMED, Closure.CLOSED),
    ),
    FixtureId(FixtureFamily.DUPLICATE_CONFLICT, (OrderTag.FORWARD,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_047_CS_TYPE_ADMISSION_type_ArtifactBodyKind, _EI_048_CS_TYPE_ADMISSION_type_ArtifactContent, _EI_049_CS_TYPE_ADMISSION_type_ArtifactProjection, _EI_050_CS_TYPE_ADMISSION_type_ArtifactRole, _EI_051_CS_TYPE_ADMISSION_type_ArtifactSelector, _EI_052_CS_TYPE_ADMISSION_type_BehaviorValue, _EI_053_CS_TYPE_ADMISSION_type_ByteSize, _EI_054_CS_TYPE_ADMISSION_type_ContentIdentity, _EI_055_CS_TYPE_ADMISSION_type_Coverage, _EI_056_CS_TYPE_ADMISSION_type_Criterion, _EI_057_CS_TYPE_ADMISSION_type_FieldId, _EI_058_CS_TYPE_ADMISSION_type_FieldValue, _EI_059_CS_TYPE_ADMISSION_type_Format, _EI_060_CS_TYPE_ADMISSION_type_ObservationRelation, _EI_061_CS_TYPE_ADMISSION_type_ObservationResult, _EI_062_CS_TYPE_ADMISSION_type_ObservationSpec, _EI_063_CS_TYPE_ADMISSION_type_ObservationValue, _EI_064_CS_TYPE_ADMISSION_type_Path, _EI_065_CS_TYPE_ADMISSION_type_PathSegment, _EI_066_CS_TYPE_ADMISSION_type_PathSet, _EI_067_CS_TYPE_ADMISSION_type_RepositorySnapshot, _EI_068_CS_TYPE_ADMISSION_type_SubjectId, _EI_069_CS_TYPE_ADMISSION_type_TaskSpec, _EI_070_CS_TYPE_ADMISSION_type_VerificationSpec, _EI_124_coding_minimal, _EI_180_T_ArtifactBodyKind, _EI_181_T_ArtifactContent, _EI_182_T_ArtifactProjection, _EI_183_T_ArtifactRole, _EI_184_T_ArtifactSelector, _EI_185_T_BehaviorValue, _EI_186_T_ByteSize, _EI_187_T_ContentIdentity, _EI_188_T_Coverage, _EI_189_T_Criterion, _EI_190_T_FieldId, _EI_191_T_FieldValue, _EI_192_T_Format, _EI_193_T_ObservationRelation, _EI_194_T_ObservationResult, _EI_195_T_ObservationSpec, _EI_196_T_ObservationValue, _EI_197_T_Path, _EI_198_T_PathSegment, _EI_199_T_PathSet, _EI_200_T_RepositorySnapshot, _EI_201_T_SubjectId, _EI_202_T_TaskSpec, _EI_203_T_VerificationSpec),
        (('PREDICATE_FACET_POSITIONS_CONFLICT', ('capknow.semantic', 'coding.declaration', 'DP(task_accepts)', (1,)), (((), ('final',), ()), ((), ('final',), ('evidence',))), (('DECLARATION_RECORD', 'capknow.semantic', 'coding.declaration', 'DP(task_accepts)', (1,)),)),),
        ("COMPOSITION", Formation.MALFORMED, Closure.NOT_APPLICABLE),
    ),
    FixtureId(FixtureFamily.DUPLICATE_EQUAL, (OrderTag.REVERSE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_047_CS_TYPE_ADMISSION_type_ArtifactBodyKind, _EI_048_CS_TYPE_ADMISSION_type_ArtifactContent, _EI_049_CS_TYPE_ADMISSION_type_ArtifactProjection, _EI_050_CS_TYPE_ADMISSION_type_ArtifactRole, _EI_051_CS_TYPE_ADMISSION_type_ArtifactSelector, _EI_052_CS_TYPE_ADMISSION_type_BehaviorValue, _EI_053_CS_TYPE_ADMISSION_type_ByteSize, _EI_054_CS_TYPE_ADMISSION_type_ContentIdentity, _EI_055_CS_TYPE_ADMISSION_type_Coverage, _EI_056_CS_TYPE_ADMISSION_type_Criterion, _EI_057_CS_TYPE_ADMISSION_type_FieldId, _EI_058_CS_TYPE_ADMISSION_type_FieldValue, _EI_059_CS_TYPE_ADMISSION_type_Format, _EI_060_CS_TYPE_ADMISSION_type_ObservationRelation, _EI_061_CS_TYPE_ADMISSION_type_ObservationResult, _EI_062_CS_TYPE_ADMISSION_type_ObservationSpec, _EI_063_CS_TYPE_ADMISSION_type_ObservationValue, _EI_064_CS_TYPE_ADMISSION_type_Path, _EI_065_CS_TYPE_ADMISSION_type_PathSegment, _EI_066_CS_TYPE_ADMISSION_type_PathSet, _EI_067_CS_TYPE_ADMISSION_type_RepositorySnapshot, _EI_068_CS_TYPE_ADMISSION_type_SubjectId, _EI_069_CS_TYPE_ADMISSION_type_TaskSpec, _EI_070_CS_TYPE_ADMISSION_type_VerificationSpec, _EI_087_DP_task_accepts, _EI_124_coding_minimal, _EI_180_T_ArtifactBodyKind, _EI_181_T_ArtifactContent, _EI_182_T_ArtifactProjection, _EI_183_T_ArtifactRole, _EI_184_T_ArtifactSelector, _EI_185_T_BehaviorValue, _EI_186_T_ByteSize, _EI_187_T_ContentIdentity, _EI_188_T_Coverage, _EI_189_T_Criterion, _EI_190_T_FieldId, _EI_191_T_FieldValue, _EI_192_T_Format, _EI_193_T_ObservationRelation, _EI_194_T_ObservationResult, _EI_195_T_ObservationSpec, _EI_196_T_ObservationValue, _EI_197_T_Path, _EI_198_T_PathSegment, _EI_199_T_PathSet, _EI_200_T_RepositorySnapshot, _EI_201_T_SubjectId, _EI_202_T_TaskSpec, _EI_203_T_VerificationSpec),
        (),
        ("COMPOSITION", Formation.WELL_FORMED, Closure.CLOSED),
    ),
    FixtureId(FixtureFamily.DUPLICATE_CONFLICT, (OrderTag.REVERSE,)): ReplayAssertion(
        (_EI_000_ABI0, _EI_047_CS_TYPE_ADMISSION_type_ArtifactBodyKind, _EI_048_CS_TYPE_ADMISSION_type_ArtifactContent, _EI_049_CS_TYPE_ADMISSION_type_ArtifactProjection, _EI_050_CS_TYPE_ADMISSION_type_ArtifactRole, _EI_051_CS_TYPE_ADMISSION_type_ArtifactSelector, _EI_052_CS_TYPE_ADMISSION_type_BehaviorValue, _EI_053_CS_TYPE_ADMISSION_type_ByteSize, _EI_054_CS_TYPE_ADMISSION_type_ContentIdentity, _EI_055_CS_TYPE_ADMISSION_type_Coverage, _EI_056_CS_TYPE_ADMISSION_type_Criterion, _EI_057_CS_TYPE_ADMISSION_type_FieldId, _EI_058_CS_TYPE_ADMISSION_type_FieldValue, _EI_059_CS_TYPE_ADMISSION_type_Format, _EI_060_CS_TYPE_ADMISSION_type_ObservationRelation, _EI_061_CS_TYPE_ADMISSION_type_ObservationResult, _EI_062_CS_TYPE_ADMISSION_type_ObservationSpec, _EI_063_CS_TYPE_ADMISSION_type_ObservationValue, _EI_064_CS_TYPE_ADMISSION_type_Path, _EI_065_CS_TYPE_ADMISSION_type_PathSegment, _EI_066_CS_TYPE_ADMISSION_type_PathSet, _EI_067_CS_TYPE_ADMISSION_type_RepositorySnapshot, _EI_068_CS_TYPE_ADMISSION_type_SubjectId, _EI_069_CS_TYPE_ADMISSION_type_TaskSpec, _EI_070_CS_TYPE_ADMISSION_type_VerificationSpec, _EI_124_coding_minimal, _EI_180_T_ArtifactBodyKind, _EI_181_T_ArtifactContent, _EI_182_T_ArtifactProjection, _EI_183_T_ArtifactRole, _EI_184_T_ArtifactSelector, _EI_185_T_BehaviorValue, _EI_186_T_ByteSize, _EI_187_T_ContentIdentity, _EI_188_T_Coverage, _EI_189_T_Criterion, _EI_190_T_FieldId, _EI_191_T_FieldValue, _EI_192_T_Format, _EI_193_T_ObservationRelation, _EI_194_T_ObservationResult, _EI_195_T_ObservationSpec, _EI_196_T_ObservationValue, _EI_197_T_Path, _EI_198_T_PathSegment, _EI_199_T_PathSet, _EI_200_T_RepositorySnapshot, _EI_201_T_SubjectId, _EI_202_T_TaskSpec, _EI_203_T_VerificationSpec),
        (('PREDICATE_FACET_POSITIONS_CONFLICT', ('capknow.semantic', 'coding.declaration', 'DP(task_accepts)', (1,)), (((), ('final',), ()), ((), ('final',), ('evidence',))), (('DECLARATION_RECORD', 'capknow.semantic', 'coding.declaration', 'DP(task_accepts)', (1,)),)),),
        ("COMPOSITION", Formation.MALFORMED, Closure.NOT_APPLICABLE),
    ),
}

def _build_expected_assertions() -> dict[FixtureId, ReplayAssertion]:
    pair_missing_rows = {
        MissingRowId.PAIR_DECLARATION,
        MissingRowId.PAIR_BINDING,
        MissingRowId.CERTIFICATE,
    }
    retained_core_missing_rows = {
        MissingRowId.ABI,
        MissingRowId.DECLARATION,
        MissingRowId.SYMBOL,
        MissingRowId.EVENT,
        MissingRowId.BINDING,
        MissingRowId.PROFILE_BINDING,
        MissingRowId.EXTRANEOUS_LEXICAL_BINDING,
        MissingRowId.SERVICE,
        MissingRowId.CAPABILITY,
        MissingRowId.MODEL_CONTRACT,
        MissingRowId.SIGMA_CONTRACT_SPEC,
        MissingRowId.SERVICE_CONTRACT_SPEC,
    }
    retained_core_without_models_rows = {
        MissingRowId.CAPABILITY,
        MissingRowId.MODEL_CONTRACT,
        MissingRowId.SIGMA_CONTRACT_SPEC,
    }
    obsolete_retained_core_identities = frozenset({
        _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec,
        _EI_179_RepositorySnapshot, _EI_204_TaskSpec,
    })
    obsolete_confluence_parallel = frozenset({
        _EI_008_BINDING_DF_changes_between, _EI_009_BINDING_DF_observe,
        _EI_073_CS_ACCESS_BOUNDARY_snapshot_pair,
        _EI_074_CS_CONFLUENCE_changes_between, _EI_075_CS_CONFLUENCE_observe,
        _EI_076_CS_EVALUATION_ERROR_BEHAVIOR_term,
        _EI_077_CS_EVIDENCE_SCHEMA_none, _EI_078_CS_UNKNOWN_BEHAVIOR_never,
        ("DECLARATION_RECORD", "capknow.semantic", "confluence.declaration", "DF(observe)", (1,)),
        ("DECLARATION_RECORD", "capknow.semantic", "confluence.declaration", "DF(changes_between)", (1,)),
        ("MODEL_CONTRACT_RECORD", "capknow.semantic", "confluence.model", "MODEL_observe_confluence", (1,)),
        ("MODEL_CONTRACT_RECORD", "capknow.semantic", "confluence.model", "MODEL_changes_between_confluence", (1,)),
    })
    occurrence_projection_identity: IdentityLiteral = (
        "BINDING_RECORD", "capknow.semantic", "coding.binding",
        "BINDING(DP(refresh_occurred))", (1,))
    retained_variant_targets: dict[MissingRowId, IdentityLiteral] = {
        MissingRowId.DECLARATION: _EI_087_DP_task_accepts,
        MissingRowId.SYMBOL: _EI_087_DP_task_accepts,
        MissingRowId.EVENT: _EI_097_DE_dependency_refresh,
        MissingRowId.BINDING: _EI_005_BINDING_DP_task_accepts,
        MissingRowId.SERVICE: _EI_159_SK_predicates,
        MissingRowId.CAPABILITY: _EI_014_CAP_predicates,
        MissingRowId.MODEL_CONTRACT: _EI_107_MODEL_task_accepts,
        MissingRowId.SIGMA_CONTRACT_SPEC: _EI_034_CS_PREDICATE_MEANING_task_accepts,
    }
    cycle_obsolete = frozenset(
        identity for identity in (
            _EXPECTED_REPLAY_ASSERTIONS_LITERAL[
                FixtureId(FixtureFamily.PROPER_CYCLE_REJECTION)
            ].authoritative_identities
            + _EXPECTED_RETAINED_CORE_ADDITIONS
            + _EXPECTED_RETAINED_CYCLE_UNIVERSE_ADDITIONS)
        if identity[2].startswith("cycle")
        or identity in {
            _EI_091_D_t, _EI_140_Q_t_ADMITTED, _EI_146_RES_t_ADMITTED,
            _EI_150_E_t, _EI_165_T_admitted, _EI_171_TP, _EI_174_TR,
            _EI_179_RepositorySnapshot, _EI_204_TaskSpec,
            _EI_071_ADMIT_RepositorySnapshot, _EI_072_ADMIT_TaskSpec,
            ("CERTIFICATE_RECORD", "PLUGIN_CERTIFICATE_ISSUER(CK)",
             "coding.certificate", "bundle_bounds_unsat", (1,)),
            ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.contract", "CS(PREDICATE_MEANING,event_matches)", (1,)),
        })
    cycle_exact_additions: frozenset[IdentityLiteral] = frozenset({
        ("CONTRACT_SPEC_RECORD", "capknow.semantic", "coding.contract", "CS(PREDICATE_MEANING,event_matches_cycle)", (1,)),
        ("SEMANTIC_ENVIRONMENT_RECORD", "capknow.semantic", "cycle.environment", "E_PROPER_CYCLE", (1,)),
        *(("SERVICE_RECORD", "capknow.semantic", "coding.service", f"SK({name})", (1,))
          for name in ("functions", "predicates", "profile", "bounds", "confluence")),
        ("SERVICE_RECORD", "capknow.semantic", "coding.service", "LEXSK", (1,)),
    })
    return {
        identifier: ReplayAssertion(
            tuple(sorted(
                (frozenset(assertion.authoritative_identities
                + (_EXPECTED_EVOLUTION_ADDITIONS
                   if identifier.family in {FixtureFamily.MISSING_BASE, FixtureFamily.MISSING_VARIANT}
                   and identifier.parameters[0] in _EVOLUTION_MISSING_ROWS
                   else ())
                + (_EXPECTED_EVOLUTION_REPAIR6_ADDITIONS
                   if identifier.family in {FixtureFamily.MISSING_BASE, FixtureFamily.MISSING_VARIANT}
                   and identifier.parameters[0] in _EVOLUTION_MISSING_ROWS
                   else ())
                + (_EXPECTED_EVOLUTION_REPAIR7_ADDITIONS
                   if identifier.family in {FixtureFamily.MISSING_BASE, FixtureFamily.MISSING_VARIANT}
                   and identifier.parameters[0] in _EVOLUTION_MISSING_ROWS
                   else ())
                + (_EXPECTED_EVOLUTION_REPAIR10_ADDITIONS
                   if identifier.family in {FixtureFamily.MISSING_BASE, FixtureFamily.MISSING_VARIANT}
                   and identifier.parameters[0] in _EVOLUTION_MISSING_ROWS
                   else ())
                + ((_EI_097_DE_dependency_refresh,)
                   if identifier.family in {FixtureFamily.MISSING_BASE, FixtureFamily.MISSING_VARIANT}
                   and identifier.parameters[0] in pair_missing_rows
                   else ())
                + (_EXPECTED_CONFLUENCE_DECLARATIONS
                   if identifier.family is FixtureFamily.CONFLUENCE_ORDER
                   else ())
                + (_EXPECTED_CONFLUENCE_REPAIR6_ADDITIONS
                   if identifier.family is FixtureFamily.CONFLUENCE_ORDER
                   else ())
                + (_EXPECTED_CONFLUENCE_AUTHORITY_ADDITIONS
                   if identifier.family is FixtureFamily.CONFLUENCE_ORDER
                   else ())
                + (_EXPECTED_PAIR_REPAIR5_ADDITIONS
                   if identifier.family is FixtureFamily.PAIR_INDEPENDENT
                   or (identifier.family in {FixtureFamily.MISSING_BASE, FixtureFamily.MISSING_VARIANT}
                       and identifier.parameters[0] in pair_missing_rows)
                   else ())
                + (_EXPECTED_PAIR_REPAIR6_ADDITIONS
                   if identifier.family is FixtureFamily.PAIR_INDEPENDENT
                   or (identifier.family in {FixtureFamily.MISSING_BASE, FixtureFamily.MISSING_VARIANT}
                       and identifier.parameters[0] in pair_missing_rows)
                   else ())
                + (_EXPECTED_RETAINED_CORE_ADDITIONS
                   if identifier.family is FixtureFamily.PROPER_CYCLE_REJECTION
                   else ())
                + ((_EXPECTED_RETAINED_CORE_WITHOUT_MODELS
                    if identifier.family is FixtureFamily.MISSING_VARIANT
                    and identifier.parameters[0] in retained_core_without_models_rows
                    else _EXPECTED_RETAINED_CORE_UNIVERSE_ADDITIONS)
                   if identifier.family in {
                       FixtureFamily.CORE_DEFINITIONAL,
                       FixtureFamily.TRUST_BRANCH,
                       FixtureFamily.CONFLUENCE_ORDER,
                   }
                   or (identifier.family in {
                       FixtureFamily.MISSING_BASE, FixtureFamily.MISSING_VARIANT}
                       and identifier.parameters[0] in retained_core_missing_rows)
                   or (identifier.family is FixtureFamily.MISSING_BASE
                       and identifier.parameters[0] is MissingRowId.PLUGIN)
                   else ())
                + (_EXPECTED_RETAINED_CYCLE_UNIVERSE_ADDITIONS
                   if identifier.family is FixtureFamily.PROPER_CYCLE_REJECTION
                   else ()))
                - (obsolete_retained_core_identities
                   if identifier.family in {
                       FixtureFamily.CORE_DEFINITIONAL, FixtureFamily.TRUST_BRANCH,
                       FixtureFamily.CONFLUENCE_ORDER,
                   } or (identifier.family in {
                       FixtureFamily.MISSING_BASE, FixtureFamily.MISSING_VARIANT}
                       and identifier.parameters[0] in retained_core_missing_rows)
                   or (identifier.family is FixtureFamily.MISSING_BASE
                       and identifier.parameters[0] is MissingRowId.PLUGIN)
                   else frozenset())
                - (obsolete_confluence_parallel
                   if identifier.family is FixtureFamily.CONFLUENCE_ORDER
                   else frozenset())
                - ({occurrence_projection_identity}
                   if identifier.family in {
                       FixtureFamily.MISSING_BASE, FixtureFamily.MISSING_VARIANT}
                   else set())
                - ({retained_variant_targets[identifier.parameters[0]]}
                   if identifier.family is FixtureFamily.MISSING_VARIANT
                   and identifier.parameters[0] in retained_variant_targets
                   else set())
                - (cycle_obsolete
                   if identifier.family is FixtureFamily.PROPER_CYCLE_REJECTION
                   else frozenset())
                | (cycle_exact_additions
                   if identifier.family is FixtureFamily.PROPER_CYCLE_REJECTION
                   else frozenset()))
            )),
            assertion.conflicts,
            assertion.outcome,
        )
        for identifier, assertion in _EXPECTED_REPLAY_ASSERTIONS_LITERAL.items()
    }

_ASSERTION_RESULTS = _build_expected_assertions()


def fixture_packet() -> dict[FixtureId, Universe]:
    return dict(_FIXTURE_PACKET)


def assertion_results() -> dict[FixtureId, Any]:
    return dict(_ASSERTION_RESULTS)


def fixture_universe(fixture: FixtureId) -> Universe:
    return _FIXTURE_PACKET[fixture]
