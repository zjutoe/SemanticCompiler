"""Literal finite K3-S packet and independent assertion-only manifests."""

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
    ResolutionCoordinate,
    ResolutionRelation,
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
    value = PluginPackage(
        ABI0,
        plugin_key,
        owner,
        declarations,
        bindings,
        models,
        specs,
        services,
        certificates,
        others,
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


def core_construction(
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
    task_type = LogicalRecord(
        task_type_id,
        TypeDeclaration(task_type_id.key, frozenset({"TASK"}), frozenset()),
    )
    snapshot_type = LogicalRecord(
        snapshot_type_id,
        TypeDeclaration(
            snapshot_type_id.key,
            frozenset({"REPOSITORY_SNAPSHOT"}),
            frozenset(),
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
    binding_id = rid(
        RecordKind.BINDING,
        "BINDING(DP(task_accepts))",
        namespace="coding.binding",
    )
    binding = LogicalRecord(
        binding_id,
        SemanticBinding(
            declaration_id,
            sigma_spec_id,
            frozenset({sigma_spec_id}),
            frozenset({sigma_spec_id}),
        ),
    )
    profile_id = rid(
        RecordKind.PROFILE_BINDING,
        "PROFILE_BINDING(PK(implementation_evidence))",
        namespace="coding.binding",
    )
    profile = LogicalRecord(
        profile_id,
        SemanticBinding(
            declaration_id,
            sigma_spec_id,
            frozenset({sigma_spec_id}),
            frozenset({sigma_spec_id}),
        ),
    )
    service_id = rid(
        RecordKind.SERVICE, "SK(predicates)", namespace="coding.service"
    )
    service = LogicalRecord(
        service_id, ServiceIdentity(service_id.key, "PREDICATE_EVALUATION")
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
    evidence_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(EVIDENCE_SCHEMA,verification)",
        namespace="coding.contract",
    )
    unknown_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(UNKNOWN_BEHAVIOR,predicate)",
        namespace="coding.contract",
    )
    error_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(EVALUATION_ERROR_BEHAVIOR,predicate)",
        namespace="coding.contract",
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
    policy_id = rid(RecordKind.TRUST_POLICY, "TP", namespace="trust")
    policy = LogicalRecord(
        policy_id, TrustPolicyRecord(policy_id.key, "embedding-policy")
    )
    root_id = rid(RecordKind.TRUST_ROOT, "TR", namespace="trust")
    root = LogicalRecord(
        root_id,
        TrustRootRecord(
            root_id.key,
            policy_id,
            frozenset({"capknow.semantic"}),
            frozenset({service_id}),
        ),
    )
    capability_id = rid(
        RecordKind.CAPABILITY,
        "CAP(predicates)",
        namespace="coding.capability",
    )
    package_key = key("coding-minimal", namespace="plugin")
    capability = LogicalRecord(
        capability_id,
        CapabilityDescriptor(
            capability_id.key,
            service_id,
            ABI0,
            package_key,
            frozenset({"PREDICATE_EVALUATION"}),
            frozenset({declaration_id}),
            sound_id,
            None,
            frozenset({binding_id}),
            frozenset({binding_id}),
            frozenset(),
            frozenset({root_id}),
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
            frozenset({capability_id}),
        ),
    )
    package = _package(
        "coding-minimal",
        "capknow.semantic",
        declarations=(task_type, snapshot_type, declaration, event),
        bindings=(binding, profile),
        models=(model,),
        specs=(sigma_spec, sound, evidence_spec, unknown_spec, error_spec),
        services=(service, capability),
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
        snapshot,
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
    required = frozenset({declaration_id, binding_id})
    environment = LogicalRecord(
        environment_id,
        SemanticEnvironment(
            (declaration_id,),
            (binding_id,),
            mechanically_extracted_dependencies=required,
        ),
    )
    dependency_id = rid(
        RecordKind.DEPENDENCY_ENVIRONMENT, "D_t", namespace="environment"
    )
    dependency = LogicalRecord(
        dependency_id,
        DependencyEnvironment(environment_id, abi.identity, required),
    )
    trust_id = rid(
        RecordKind.TRUST_ENVIRONMENT,
        f"T_{trust_tag.value.lower()}",
        namespace="trust",
    )
    if trust_tag is TrustFixtureTag.ADMITTED:
        trust_value = TrustEnvironment(
            policy_id, (root_id,), ((root_id, TrustState.ADMITTED),)
        )
    elif trust_tag is TrustFixtureTag.ABSENT:
        trust_value = TrustEnvironment(policy_id, (), ())
    elif trust_tag is TrustFixtureTag.UNDECIDED:
        trust_value = TrustEnvironment(
            policy_id, (root_id,), ((root_id, TrustState.UNDECIDED),)
        )
    elif trust_tag is TrustFixtureTag.INCOMPATIBLE:
        trust_value = TrustEnvironment(
            policy_id, (root_id,), ((root_id, TrustState.INCOMPATIBLE),)
        )
    else:
        trust_value = TrustEnvironment(
            policy_id,
            (root_id,),
            ((root_id, TrustState.ADMITTED),),
            "TRANSPORT_FAILURE",
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
    top_level = (
        abi,
        package,
        policy,
        root,
        environment,
        dependency,
        trust,
        request,
        result,
    )
    manifest = frozenset(
        (
            abi,
            package,
            task_type,
            snapshot_type,
            declaration,
            event,
            binding,
            profile,
            model,
            sigma_spec,
            sound,
            evidence_spec,
            unknown_spec,
            error_spec,
            service,
            capability,
            policy,
            root,
            environment,
            dependency,
            trust,
            request,
            result,
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
            (),
            "BOOL",
            (),
            frozenset(),
        ),
    )
    right_decl = LogicalRecord(
        right_decl_id,
        DeclarationShape(
            right_decl_id.key,
            key("SP(refresh_occurred)", namespace="coding.symbol"),
            "PREDICATE",
            (),
            "BOOL",
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
        "CS(PREDICATE_MEANING,refresh_occurred)",
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
            ContractRole.PREDICATE_MEANING,
            ("Trace",),
            frozenset({"Eval"}),
            (),
            frozenset(),
            "refresh_occurred",
        ),
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
    left = LogicalRecord(
        left_id,
        SemanticBinding(
            left_decl_id,
            left_spec_id,
            frozenset({left_spec_id}),
            frozenset({left_spec_id}),
        ),
    )
    right = LogicalRecord(
        right_id,
        SemanticBinding(
            right_decl_id,
            right_spec_id,
            frozenset({right_spec_id, left_id}),
            frozenset({right_spec_id, left_id}),
        ),
    )
    pair_id = rid(
        RecordKind.PAIR_DECLARATION, "PAIR(refresh)", namespace="pair"
    )
    pair = LogicalRecord(
        pair_id, PairDeclaration(pair_id.key, left_id, right_id)
    )

    validator_owner = "capknow.audit.pair-capability"
    validator_service_id = rid(
        RecordKind.SERVICE,
        "PVSK",
        owner=validator_owner,
        namespace="pair.service",
    )
    validator_service = LogicalRecord(
        validator_service_id,
        ServiceIdentity(validator_service_id.key, "PAIR_VALIDATION"),
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
            frozenset({"PAIR_VALIDATION_ERROR"}),
            (),
            frozenset(),
            "pair_failure_projection",
        ),
    )
    validation_capability_id = rid(
        RecordKind.CAPABILITY,
        "PVC",
        owner=validator_owner,
        namespace="pair.capability",
    )
    validation_capability = LogicalRecord(
        validation_capability_id,
        CapabilityDescriptor(
            validation_capability_id.key,
            validator_service_id,
            ABI0,
            key("pair-validator", validator_owner, "plugin"),
            frozenset({"PAIR_VALIDATION"}),
            frozenset({pair_id}),
            psound_id,
            pcomplete_id,
            frozenset({left_id, right_id}),
            frozenset({left_id, right_id}),
            frozenset(),
            frozenset(),
        ),
    )
    validator_package = _package(
        "pair-validator",
        validator_owner,
        specs=(psound, pcomplete, pevidence, pfailure),
        services=(validator_service, validation_capability),
    )

    proof_owner = "capknow.audit.pair-proof"
    certificate_id = rid(
        RecordKind.CERTIFICATE,
        "PCERT",
        owner=proof_owner,
        namespace="pair.certificate",
    )
    certificate = LogicalRecord(
        certificate_id,
        CertificateRecord(
            certificate_id.key,
            pair_id,
            "PAIR_COHERENCE_ADMITTED",
            proof_owner,
        ),
    )
    proof_package = _package(
        "pair-proof", proof_owner, certificates=(certificate,)
    )
    validation_owner = "capknow.audit.pair-validator"
    validation_proof_id = rid(
        RecordKind.CERTIFICATE,
        "PAIR_PROOF_REF",
        owner=validation_owner,
        namespace="pair.validation",
    )
    validation_proof = LogicalRecord(
        validation_proof_id,
        CertificateRecord(
            validation_proof_id.key,
            pair_id,
            "PAIR_FULL_EVAL",
            validation_owner,
        ),
    )
    validation_package = _package(
        "pair-validation-proof",
        validation_owner,
        certificates=(validation_proof,),
    )
    validation_refs = frozenset(
        {validation_proof_id, validation_capability_id}
    )
    pair_binding_id = rid(
        RecordKind.PAIR_BINDING, "PB_alt", namespace="pair.binding"
    )
    pair_binding = LogicalRecord(
        pair_binding_id,
        PairBinding(
            pair_id,
            certificate_id,
            frozenset({left_id, right_id}),
            validation_refs,
            validation_refs,
        ),
    )
    pair_package = _package(
        "coding-minimal",
        "capknow.semantic",
        declarations=(left_decl, right_decl, pair),
        bindings=(left, right, pair_binding),
        specs=(left_spec, right_spec),
    )
    semantic_environment_id = rid(
        RecordKind.SEMANTIC_ENVIRONMENT, "E_p", namespace="pair.environment"
    )
    semantic_environment = LogicalRecord(
        semantic_environment_id,
        SemanticEnvironment(
            (left_decl_id, right_decl_id),
            (left_id, right_id),
            pair_bindings=(pair_binding_id,),
            mechanically_extracted_dependencies=frozenset(
                {left_id, right_id}
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
            semantic_environment_id,
            abi.identity,
            frozenset({left_id, right_id}),
        ),
    )
    evidence = record(
        RecordKind.EVIDENCE,
        "PAIR_FULL_EVAL_EVIDENCE",
        NamedCarrier(
            "PAIR_FULL_EVAL_PROOF",
            frozenset({pair_id, left_id, right_id}),
            "COMPLETE_EVAL_RECORD",
        ),
        owner=validation_owner,
        namespace="pair.evidence",
    )
    policy_id = rid(RecordKind.TRUST_POLICY, "TP", namespace="pair.trust")
    policy = LogicalRecord(
        policy_id, TrustPolicyRecord(policy_id.key, "embedding-policy")
    )
    root_id = rid(RecordKind.TRUST_ROOT, "TRP", namespace="pair.trust")
    root = LogicalRecord(
        root_id,
        TrustRootRecord(
            root_id.key,
            policy_id,
            frozenset({"capknow.semantic"}),
            frozenset({pair_id}),
        ),
    )
    trust_id = rid(
        RecordKind.TRUST_ENVIRONMENT, "T_p", namespace="pair.trust"
    )
    trust = LogicalRecord(
        trust_id,
        TrustEnvironment(
            policy_id, (root_id,), ((root_id, TrustState.ADMITTED),)
        ),
    )
    request_id = rid(RecordKind.REQUEST, "R_p", namespace="pair.request")
    request = LogicalRecord(
        request_id, PairRequestData(pair_binding_id, trust_id)
    )
    envelope = record(
        RecordKind.EVIDENCE,
        "PENV",
        NamedCarrier(
            "PAIR_CERTIFICATE_ENVELOPE",
            frozenset(
                {
                    request_id,
                    pair_id,
                    semantic_environment_id,
                    dependency_environment_id,
                    validation_capability_id,
                    psound_id,
                    root_id,
                    evidence.identity,
                }
            ),
            "PAIR_COHERENCE_ADMITTED",
        ),
        owner=proof_owner,
        namespace="pair.envelope",
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
                validation_proof_id, validation_owner, "VALIDATION_OWNER"
            ),
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
        validation_package,
        validator_package,
        semantic_environment,
        dependency_environment,
        evidence,
        policy,
        root,
        trust,
        request,
        envelope,
        *producers,
    )
    manifest = frozenset(
        (
            abi,
            pair_package,
            left_decl,
            right_decl,
            pair,
            left,
            right,
            pair_binding,
            left_spec,
            right_spec,
            proof_package,
            certificate,
            validation_package,
            validation_proof,
            validator_package,
            psound,
            pcomplete,
            pevidence,
            pfailure,
            validator_service,
            validation_capability,
            semantic_environment,
            dependency_environment,
            evidence,
            policy,
            root,
            trust,
            request,
            envelope,
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
    core_members = {item.identity: item for item in package.value.members()}
    declaration = core_members[core.declaration]
    event = next(
        item
        for item in package.value.declarations
        if item.identity.kind is RecordKind.EVENT
    )
    binding = core_members[core.binding]
    profile = next(
        item
        for item in package.value.bindings
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
            bindings=tuple(
                item
                for item in package.value.bindings
                if item.identity != profile.identity
            ),
        ),
    )
    package_no_service = replace(
        package,
        value=replace(
            package.value,
            services=tuple(
                item
                for item in package.value.services
                if item.identity != service.identity
            ),
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
        for item in pair_package.value.declarations
        if item.identity.kind is RecordKind.PAIR_DECLARATION
    )
    pair_binding = next(
        item
        for item in pair_package.value.bindings
        if item.identity.kind is RecordKind.PAIR_BINDING
    )
    pair_package_no_declaration = replace(
        pair_package,
        value=replace(
            pair_package.value,
            declarations=tuple(
                item
                for item in pair_package.value.declarations
                if item.identity != pair_declaration.identity
            ),
        ),
    )
    pair_package_no_binding = replace(
        pair_package,
        value=replace(
            pair_package.value,
            bindings=tuple(
                item
                for item in pair_package.value.bindings
                if item.identity != pair_binding.identity
            ),
        ),
    )

    outcome = record(
        RecordKind.OUTCOME,
        "O_w",
        NamedCarrier("ADAPTER_WITNESS_OUTCOME", value="SATISFIED"),
        namespace="outcome",
    )
    authority = record(
        RecordKind.AUTHORITY_FACT,
        "AF(choice,1)",
        NamedCarrier("AUTHORITY_FACT", value="LOCAL_STORAGE"),
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
            (),
            (),
            authority_facts=(authority.identity,),
            choice_bindings=(choice_id,),
        ),
    )
    choice_environment_no_fact = replace(
        choice_environment,
        value=SemanticEnvironment((), (), authority_facts=(), choice_bindings=()),
    )
    choice_environment_no_binding = replace(
        choice_environment,
        value=SemanticEnvironment(
            (), (), authority_facts=(authority.identity,), choice_bindings=()
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
        value=replace(authority_package.value, other_records=()),
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
            (declaration.identity,),
            (binding.identity,),
            lexical_bindings=(lexical_id,),
        ),
    )
    lexical_environment_no_binding = replace(
        lexical_environment,
        value=SemanticEnvironment(
            (declaration.identity,), (binding.identity,), lexical_bindings=()
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
            lexical_environment_id,
            abi.identity,
            frozenset({declaration.identity, binding.identity, lexical_id}),
        ),
    )
    lexical_dependency_no_binding = replace(
        lexical_dependency,
        value=DependencyEnvironment(
            lexical_environment_id,
            abi.identity,
            frozenset({declaration.identity, binding.identity}),
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
            (declaration.identity,),
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
            extra_environment_id,
            abi.identity,
            frozenset({declaration.identity, binding.identity}),
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
        value=TrustEnvironment(policy.identity, (), ()),
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
    migration = LogicalRecord(
        migration_id,
        EvolutionRecord(migration_id.key, environment.identity, True),
    )
    compatibility = LogicalRecord(
        compatibility_id,
        EvolutionRecord(compatibility_id.key, migration_id, True),
    )
    optional_extension = LogicalRecord(
        optional_extension_id,
        EvolutionRecord(optional_extension_id.key, optional_alias_id, False),
    )
    required_extension = LogicalRecord(
        required_extension_id,
        EvolutionRecord(required_extension_id.key, required_alias_id, True),
    )
    optional_alias = LogicalRecord(
        optional_alias_id,
        EvolutionRecord(optional_alias_id.key, declaration.identity, False),
    )
    required_alias = LogicalRecord(
        required_alias_id,
        EvolutionRecord(required_alias_id.key, declaration.identity, True),
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
            other_records=tuple(
                item
                for item in evo_package.value.other_records
                if item.identity != migration_id
            ),
        ),
    )
    evo_package_no_compatibility = replace(
        evo_package,
        value=replace(
            evo_package.value,
            other_records=tuple(
                item
                for item in evo_package.value.other_records
                if item.identity != compatibility_id
            ),
        ),
    )
    evo_package_no_optional_extension = replace(
        evo_package,
        value=replace(
            evo_package.value,
            other_records=tuple(
                item
                for item in evo_package.value.other_records
                if item.identity != optional_extension_id
            ),
        ),
    )
    evo_package_no_required_extension = replace(
        evo_package,
        value=replace(
            evo_package.value,
            other_records=tuple(
                item
                for item in evo_package.value.other_records
                if item.identity != required_extension_id
            ),
        ),
    )
    evo_package_no_optional_alias = replace(
        evo_package,
        value=replace(
            evo_package.value,
            other_records=tuple(
                item
                for item in evo_package.value.other_records
                if item.identity != optional_alias_id
            ),
        ),
    )
    evo_package_no_required_alias = replace(
        evo_package,
        value=replace(
            evo_package.value,
            other_records=tuple(
                item
                for item in evo_package.value.other_records
                if item.identity != required_alias_id
            ),
        ),
    )

    wrong_sigma_id = rid(
        RecordKind.CONTRACT_SPEC,
        "CS(PREDICATE_MEANING,observations_equal)",
        namespace="coding.contract",
    )
    wrong_sigma = LogicalRecord(
        wrong_sigma_id,
        replace(
            sigma_spec.value,
            contract_key=wrong_sigma_id.key,
            relation_name="observations_equal",
        ),
    )
    wrong_binding = replace(
        binding,
        value=replace(
            binding.value,
            meaning_contract=wrong_sigma_id,
            proper_dependencies=frozenset({wrong_sigma_id}),
            dependency_closure=frozenset({wrong_sigma_id}),
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
            contract_specs=tuple(
                wrong_sigma if item.identity == sigma_spec.identity else item
                for item in package.value.contract_specs
            ),
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
            contract_specs=tuple(
                wrong_sound if item.identity == sound_spec.identity else item
                for item in package.value.contract_specs
            ),
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
        empty_environment_id, SemanticEnvironment((), ())
    )
    empty_dependency_id = rid(
        RecordKind.DEPENDENCY_ENVIRONMENT,
        "D_t_empty",
        namespace="environment",
    )
    empty_dependency = LogicalRecord(
        empty_dependency_id,
        DependencyEnvironment(empty_environment_id, abi.identity, frozenset()),
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
        absent_trust_id, TrustEnvironment(policy.identity, (), ())
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
            environment.identity, abi.identity, frozenset({declaration.identity})
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
        NamedCarrier(
            "DEPENDENCY_REFRESH",
            frozenset({event.identity}),
            "SNAPSHOT_IDENTITY(F_c)",
        ),
        namespace="event.value",
    )
    trace_event = record(
        RecordKind.TRACE_EVENT,
        "te0",
        NamedCarrier(
            "TRACE_EVENT", frozenset({event_value.identity}), "user"
        ),
        namespace="event.trace",
    )
    source = record(
        RecordKind.SOURCE,
        "SRC(choice,1)",
        NamedCarrier("SOURCE", value="choice:1"),
        namespace="authority.source",
    )
    authority_ref = record(
        RecordKind.AUTHORITY_REF,
        "AUTH(choice,1)",
        NamedCarrier("AUTHORITY_REF", value="choice:1"),
        namespace="authority.ref",
    )
    evidence_record = record(
        RecordKind.EVIDENCE,
        "e0",
        NamedCarrier("EVIDENCE_REF", value="missing-matrix-record"),
        namespace="evidence",
    )
    evidence_subject = record(
        RecordKind.OUTCOME,
        "t_t_evidence_subject",
        NamedCarrier(
            "TASK_EVIDENCE_SUBJECT", frozenset({evidence_record.identity})
        ),
        namespace="evidence",
    )
    evidence_subject_without_record = replace(
        evidence_subject,
        value=NamedCarrier("TASK_EVIDENCE_SUBJECT", frozenset()),
    )
    reason = record(
        RecordKind.REASON,
        "u0",
        NamedCarrier("UNKNOWN_REASON", value="DP(task_accepts)"),
        namespace="reason",
    )
    reason_carrier = record(
        RecordKind.OUTCOME,
        "VALUE(UNKNOWN)",
        NamedCarrier("UNKNOWN_VALUE", frozenset({reason.identity})),
        namespace="reason",
    )
    reason_carrier_without_reason = replace(
        reason_carrier,
        value=NamedCarrier("UNKNOWN_VALUE", frozenset()),
    )
    conflict = record(
        RecordKind.CONFLICT,
        "conflict0",
        NamedCarrier(
            "PREDICATE_FACET_POSITIONS_CONFLICT",
            frozenset({declaration.identity}),
            ((frozenset(), frozenset({"final"}), frozenset({"evidence"})),
             (frozenset(), frozenset({"final"}), frozenset())),
        ),
        namespace="conflict",
    )
    conflict_replacement = record(
        RecordKind.CONFLICT,
        "conflict1",
        NamedCarrier(
            "PREDICATE_FACET_POSITIONS_CONFLICT",
            frozenset({declaration.identity}),
            ((frozenset(), frozenset({"final"}), frozenset({"evidence"})),
             (frozenset(), frozenset(), frozenset({"evidence"}))),
        ),
        namespace="conflict",
    )

    package_manifest = frozenset((package, *package.value.members()))
    package_no_declaration_manifest = frozenset(
        (package_no_declaration, *package_no_declaration.value.members())
    )
    package_no_event_manifest = frozenset(
        (package_no_event, *package_no_event.value.members())
    )
    package_no_binding_manifest = frozenset(
        (package_no_binding, *package_no_binding.value.members())
    )
    package_no_profile_manifest = frozenset(
        (package_no_profile, *package_no_profile.value.members())
    )
    package_no_service_manifest = frozenset(
        (package_no_service, *package_no_service.value.members())
    )
    package_no_capability_manifest = frozenset(
        (package_no_capability, *package_no_capability.value.members())
    )
    package_no_model_manifest = frozenset(
        (package_no_model, *package_no_model.value.members())
    )
    pair_package_manifest = frozenset(
        (pair_package, *pair_package.value.members())
    )
    pair_package_no_declaration_manifest = frozenset(
        (
            pair_package_no_declaration,
            *pair_package_no_declaration.value.members(),
        )
    )
    pair_package_no_binding_manifest = frozenset(
        (pair_package_no_binding, *pair_package_no_binding.value.members())
    )
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
    evo_manifest = frozenset((evo_package, *evo_package.value.members()))
    evo_no_migration_manifest = frozenset(
        (evo_package_no_migration, *evo_package_no_migration.value.members())
    )
    evo_no_compatibility_manifest = frozenset(
        (
            evo_package_no_compatibility,
            *evo_package_no_compatibility.value.members(),
        )
    )
    evo_no_optional_extension_manifest = frozenset(
        (
            evo_package_no_optional_extension,
            *evo_package_no_optional_extension.value.members(),
        )
    )
    evo_no_required_extension_manifest = frozenset(
        (
            evo_package_no_required_extension,
            *evo_package_no_required_extension.value.members(),
        )
    )
    evo_no_optional_alias_manifest = frozenset(
        (
            evo_package_no_optional_alias,
            *evo_package_no_optional_alias.value.members(),
        )
    )
    evo_no_required_alias_manifest = frozenset(
        (
            evo_package_no_required_alias,
            *evo_package_no_required_alias.value.members(),
        )
    )
    wrong_sigma_manifest = frozenset(
        (package_wrong_sigma, *package_wrong_sigma.value.members())
    )
    wrong_service_manifest = frozenset(
        (package_wrong_service, *package_wrong_service.value.members())
    )

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
            (abi, evo_package, compatibility),
            (abi, evo_package_no_migration, compatibility),
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
            (abi, evo_package, required_extension),
            (abi, evo_package_no_compatibility, required_extension),
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
            (abi, evo_package),
            (abi, evo_package_no_optional_extension),
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
            (abi, evo_package),
            (abi, evo_package_no_required_extension),
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
            (abi, evo_package, optional_extension),
            (abi, evo_package_no_optional_alias, optional_extension),
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
            (abi, evo_package, required_extension),
            (abi, evo_package_no_required_alias, required_extension),
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
            frozenset({evidence_record, evidence_subject}),
            frozenset({evidence_subject_without_record}),
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
            frozenset({reason, reason_carrier}),
            frozenset({reason_carrier_without_reason}),
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
    return rows


LITERAL_MISSING_ROWS = _literal_missing_rows()
LITERAL_MISSING_BY_ID = {item.row: item for item in LITERAL_MISSING_ROWS}
MISSING_LITERAL_IDENTITIES = {
    item.row: item.target for item in LITERAL_MISSING_ROWS
}
MISSING_EXPECTED_LITERAL = {
    item.row: item.expected for item in LITERAL_MISSING_ROWS
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
    expected: ObservationEvaluation
    node_one: RecordIdentity
    node_two: RecordIdentity


def confluence_construction(order: OrderTag) -> ConfluenceConstruction:
    path = Path((PathSegment("dependency.lock"),))
    old_artifact = ArtifactContent(
        ArtifactTag.TEXT,
        ArtifactRole.DEPENDENCY_LOCK,
        Format.TEXT,
        ByteSize(1),
        ContentIdentity("old"),
    )
    new_artifact = ArtifactContent(
        ArtifactTag.TEXT,
        ArtifactRole.DEPENDENCY_LOCK,
        Format.TEXT,
        ByteSize(1),
        ContentIdentity("new"),
    )
    old = RepositorySnapshot(((path, old_artifact),))
    new = RepositorySnapshot(((path, new_artifact),))
    selector = ArtifactSelector(
        SelectorTag.PATHS_WITH_ROLE,
        frozenset({path}),
        ArtifactRole.DEPENDENCY_LOCK,
    )
    observed_spec = ObservationSpec(
        ObservationSpecTag.ARTIFACT_VIEW,
        selector,
        ArtifactProjection(ProjectionTag.CONTENT),
    )
    node_one_id = rid(
        RecordKind.OBSERVATION_NODE, "N_o", namespace="confluence"
    )
    node_two_id = rid(
        RecordKind.OBSERVATION_NODE, "N_d", namespace="confluence"
    )
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
            ContractRole.PREDICATE_MEANING,
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
            ContractRole.PREDICATE_MEANING,
            ("RepositorySnapshot", "RepositorySnapshot"),
            frozenset({"TermResult"}),
            (),
            frozenset(),
            "changes_between",
        ),
    )
    node_one = LogicalRecord(
        node_one_id,
        ObservationNode(
            NodeOperation.OBSERVE, (observed_spec, new), spec_one_id
        ),
    )
    node_two = LogicalRecord(
        node_two_id,
        ObservationNode(
            NodeOperation.CHANGES_BETWEEN, (old, new), spec_two_id
        ),
    )
    binding_one = record(
        RecordKind.BINDING,
        "BINDING(DF(observe))",
        SemanticBinding(
            node_one_id,
            spec_one_id,
            frozenset({spec_one_id}),
            frozenset({spec_one_id}),
        ),
        namespace="confluence.binding",
    )
    binding_two = record(
        RecordKind.BINDING,
        "BINDING(DF(changes_between))",
        SemanticBinding(
            node_two_id,
            spec_two_id,
            frozenset({spec_two_id}),
            frozenset({spec_two_id}),
        ),
        namespace="confluence.binding",
    )
    package = _package(
        "coding-minimal",
        "capknow.semantic",
        bindings=(binding_one, binding_two),
        specs=(spec_one, spec_two),
        others=(node_one, node_two),
    )

    policy_id = rid(
        RecordKind.TRUST_POLICY, "TP", namespace="confluence.trust"
    )
    policy = LogicalRecord(
        policy_id, TrustPolicyRecord(policy_id.key, "embedding-policy")
    )
    root_id = rid(
        RecordKind.TRUST_ROOT, "ROOT_TR_c", namespace="confluence.trust"
    )
    capability_target = rid(
        RecordKind.CAPABILITY, "CAP(confluence)", namespace="coding.capability"
    )
    root = LogicalRecord(
        root_id,
        TrustRootRecord(
            root_id.key,
            policy_id,
            frozenset({"capknow.semantic"}),
            frozenset({capability_target}),
        ),
    )
    trust_id = rid(
        RecordKind.TRUST_ENVIRONMENT, "T_c", namespace="confluence.trust"
    )
    trust = LogicalRecord(
        trust_id,
        TrustEnvironment(
            policy_id, (root_id,), ((root_id, TrustState.ADMITTED),)
        ),
    )
    semantic_id = rid(
        RecordKind.SEMANTIC_ENVIRONMENT,
        "E_c",
        namespace="confluence.environment",
    )
    semantic = LogicalRecord(
        semantic_id,
        SemanticEnvironment(
            (),
            (binding_one.identity, binding_two.identity),
            mechanically_extracted_dependencies=frozenset(
                {binding_one.identity, binding_two.identity}
            ),
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
            semantic_id,
            abi_id,
            frozenset({binding_one.identity, binding_two.identity}),
        ),
    )
    request_id = rid(
        RecordKind.REQUEST, "R_c", namespace="confluence.request"
    )
    request_record = LogicalRecord(
        request_id,
        InvocationRequest(
            node_one_id,
            semantic_id,
            dependency_id,
            trust_id,
            V1,
            ("C_c",),
        ),
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
    changes = ChangeSet(
        ((path, ChangeEntry(ChangeKind.MODIFIED, old_artifact, new_artifact)),)
    )
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
        ResultRecord(request_id, "ReasoningResult", "COMPLETED_INCONCLUSIVE"),
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
        NamedCarrier(
            "CONFLUENCE_STATUS",
            frozenset(
                {
                    lifecycle_record.identity,
                    observation_environment.identity,
                    result_record.identity,
                }
            ),
            (
                "WELL_FORMED",
                "CLOSED",
                "EVALUABILITY_AVAILABLE",
                "CONSISTENCY_UNKNOWN",
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
    top_level = (
        abi,
        package,
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
    )
    manifest = frozenset(
        (
            abi,
            package,
            binding_one,
            binding_two,
            spec_one,
            spec_two,
            node_one,
            node_two,
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
        )
    )
    expected = ObservationEvaluation(
        observations,
        Judgment("COMPLETED_INCONCLUSIVE"),
        "COMPLETED",
        (
            "WELL_FORMED",
            "CLOSED",
            "EVALUABILITY_AVAILABLE",
            "COMPLETED",
            "CONSISTENCY_UNKNOWN",
        ),
    )
    return ConfluenceConstruction(
        Universe(
            top_level,
            GraphEvaluationRequest((node_one_id, node_two_id), preferred),
        ),
        manifest,
        expected,
        node_one_id,
        node_two_id,
    )


def cycle_universe() -> Universe:
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
            (first_query,),
            frozenset({second_id}),
            "event_matches_cycle",
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
            (),
            "BOOL",
            (),
            frozenset(),
        ),
    )
    second_decl = LogicalRecord(
        second_decl_id,
        DeclarationShape(
            second_decl_id.key,
            key("SP(event_occurred)", namespace="cycle.symbol"),
            "PREDICATE",
            (),
            "BOOL",
            (),
            frozenset(),
        ),
    )
    first = LogicalRecord(
        first_id,
        SemanticBinding(
            first_decl_id,
            first_spec_id,
            frozenset({first_spec_id}),
            frozenset({first_spec_id, second_id}),
        ),
    )
    second = LogicalRecord(
        second_id,
        SemanticBinding(
            second_decl_id,
            second_spec_id,
            frozenset({second_spec_id}),
            frozenset({second_spec_id, first_id}),
        ),
    )
    package = _package(
        "coding-minimal",
        "capknow.semantic",
        declarations=(first_decl, second_decl),
        bindings=(first, second),
        specs=(first_spec, second_spec),
    )
    environment = record(
        RecordKind.SEMANTIC_ENVIRONMENT,
        "E_PROPER_CYCLE",
        SemanticEnvironment(
            (first_decl_id, second_decl_id),
            (first_id, second_id),
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
    return Universe(
        (abi, package, environment), FormationRequest((first_id, second_id))
    )


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
            ),
        )
        declaration = LogicalRecord(
            type_id,
            TypeDeclaration(
                type_id.key,
                frozenset({f"UNIT_{name}"}),
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
PI_LITERAL_MANIFEST = frozenset(
    {
        PI_ABI,
        PI_PACKAGE_ONE,
        PI_PACKAGE_TWO,
        *PI_PAIR_11,
        *PI_PAIR_12,
        *PI_PAIR_21,
        *PI_PAIR_22,
    }
)
PI_EXPECTED_LITERAL = CompositionReplay(
    Composition(PI_LITERAL_MANIFEST, ()),
    Formation.WELL_FORMED,
    Closure.CLOSED,
)


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
        admissions.append(
            LogicalRecord(
                admission_id,
                ContractSpec(
                    admission_id.key,
                    Layer.DELTA,
                    ContractRole.TYPE_ADMISSION,
                    ("Value",),
                    frozenset({"admitted", "not_admitted"}),
                    (),
                    frozenset(),
                    f"admit_{name}",
                ),
            )
        )
        declarations.append(
            LogicalRecord(
                type_id,
                TypeDeclaration(
                    type_id.key,
                    frozenset({name.upper()}),
                    frozenset({admission_id}),
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
DUPLICATE_BASE_MANIFEST = frozenset(
    {
        DUPLICATE_ABI,
        DUPLICATE_PACKAGE,
        *DUPLICATE_TYPE_DECLARATIONS,
        *DUPLICATE_TYPE_ADMISSIONS,
        DUPLICATE_DECLARATION,
    }
)
DUPLICATE_EQUAL_EXPECTED_LITERAL = CompositionReplay(
    Composition(DUPLICATE_BASE_MANIFEST, ()),
    Formation.WELL_FORMED,
    Closure.CLOSED,
)
DUPLICATE_CONFLICT = ConflictRef(
    DUPLICATE_DECLARATION.identity,
    frozenset({DUPLICATE_DECLARATION, DUPLICATE_BAD_DECLARATION}),
)
DUPLICATE_CONFLICT_EXPECTED_LITERAL = CompositionReplay(
    Composition(
        DUPLICATE_BASE_MANIFEST - frozenset({DUPLICATE_DECLARATION}),
        (DUPLICATE_CONFLICT,),
    ),
    Formation.MALFORMED,
    Closure.NOT_APPLICABLE,
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


TRUST_EXPECTED_LITERAL = {
    TrustFixtureTag.ADMITTED: (
        Evaluability.AVAILABLE,
        "INVOCABLE",
        True,
    ),
    TrustFixtureTag.ABSENT: (
        Evaluability.MISSING,
        "TRUST_ROOT_ABSENT",
        False,
    ),
    TrustFixtureTag.UNDECIDED: (
        Evaluability.UNKNOWN,
        "TRUST_ROOT_UNDECIDED",
        False,
    ),
    TrustFixtureTag.INCOMPATIBLE: (
        Evaluability.MISSING,
        "TRUST_ROOT_INCOMPATIBLE",
        False,
    ),
    TrustFixtureTag.FAILED: (
        Evaluability.UNKNOWN,
        "DISCOVERY_FAILED",
        False,
    ),
}


def _build_packet() -> tuple[dict[FixtureId, Universe], dict[FixtureId, Any]]:
    packet: dict[FixtureId, Universe] = {}
    assertions: dict[FixtureId, Any] = {}

    core = core_construction()
    core_id = FixtureId(FixtureFamily.CORE_DEFINITIONAL)
    packet[core_id] = core.universe
    assertions[core_id] = CoreReplay(
        Composition(core.manifest, ()),
        Formation.WELL_FORMED,
        Closure.CLOSED,
        Evaluability.AVAILABLE,
        f"INVOCABLE_FOR({core.request.key.local})",
        Eval(
            Truth.TRUE,
            frozenset(
                next(iter(core.evidence)).payload.value.evidence_refs
            ),
        ),
    )

    pair = pair_construction()
    pair_id = FixtureId(FixtureFamily.PAIR_INDEPENDENT)
    packet[pair_id] = pair.universe
    pair_declaration = next(
        item
        for item in pair.manifest
        if item.identity.kind is RecordKind.PAIR_DECLARATION
    )
    pair_certificate = next(
        item for item in pair.manifest if item.identity == pair.certificate
    )
    assertions[pair_id] = PairReplay(
        Composition(pair.manifest, ()),
        Formation.WELL_FORMED,
        Closure.CLOSED,
        PairValidationResult(
            pair_declaration.value.pair_key,
            pair_certificate.value.certificate_key,
            "PAIR_COHERENCE_ADMITTED",
        ),
    )

    for tag in TrustFixtureTag:
        construction = core_construction(tag)
        fixture_id = FixtureId(FixtureFamily.TRUST_BRANCH, (tag,))
        packet[fixture_id] = construction.universe
        evaluability, lifecycle, has_result = TRUST_EXPECTED_LITERAL[tag]
        exact_lifecycle = (
            f"INVOCABLE_FOR({construction.request.key.local})"
            if lifecycle == "INVOCABLE"
            else lifecycle
        )
        exact_result = (
            Eval(
                Truth.TRUE,
                frozenset(
                    next(iter(construction.evidence)).payload.value.evidence_refs
                ),
            )
            if has_result
            else None
        )
        assertions[fixture_id] = CoreReplay(
            Composition(construction.manifest, ()),
            Formation.WELL_FORMED,
            Closure.CLOSED,
            evaluability,
            exact_lifecycle,
            exact_result,
        )

    for spec in LITERAL_MISSING_ROWS:
        construction = missing_construction(spec.row)
        base_id = FixtureId(FixtureFamily.MISSING_BASE, (spec.row,))
        variant_id = FixtureId(FixtureFamily.MISSING_VARIANT, (spec.row,))
        packet[base_id] = construction.baseline
        packet[variant_id] = construction.variant
        target = next(
            item
            for item in spec.baseline_manifest
            if item.identity == spec.target
        )
        assertions[base_id] = LookupReplay(
            Composition(spec.baseline_manifest, ()),
            Judgment("PRESENT", (target,)),
        )
        assertions[variant_id] = LookupReplay(
            Composition(spec.variant_manifest, ()), spec.expected
        )

    for order in OrderTag:
        construction = confluence_construction(order)
        fixture_id = FixtureId(FixtureFamily.CONFLUENCE_ORDER, (order,))
        packet[fixture_id] = construction.universe
        assertions[fixture_id] = construction.expected

    cycle_id = FixtureId(FixtureFamily.PROPER_CYCLE_REJECTION)
    packet[cycle_id] = cycle_universe()
    assertions[cycle_id] = (
        Formation.MALFORMED,
        Closure.NOT_APPLICABLE,
        Judgment("MALFORMED", ("dependency cycle",)),
    )

    for package_order in PackageOrderTag:
        for record_order in RecordOrderTag:
            fixture_id = FixtureId(
                FixtureFamily.PERMUTATION, (package_order, record_order)
            )
            packet[fixture_id] = permutation_universe(
                package_order, record_order
            )
            assertions[fixture_id] = PI_EXPECTED_LITERAL

    for order in OrderTag:
        equal_id = FixtureId(FixtureFamily.DUPLICATE_EQUAL, (order,))
        conflict_id = FixtureId(FixtureFamily.DUPLICATE_CONFLICT, (order,))
        packet[equal_id] = duplicate_universe(False, order)
        packet[conflict_id] = duplicate_universe(True, order)
        assertions[equal_id] = DUPLICATE_EQUAL_EXPECTED_LITERAL
        assertions[conflict_id] = DUPLICATE_CONFLICT_EXPECTED_LITERAL

    return packet, assertions


_FIXTURE_PACKET, _ASSERTION_RESULTS = _build_packet()


def fixture_packet() -> dict[FixtureId, Universe]:
    return dict(_FIXTURE_PACKET)


def assertion_results() -> dict[FixtureId, Any]:
    return dict(_ASSERTION_RESULTS)


def fixture_universe(fixture: FixtureId) -> Universe:
    return _FIXTURE_PACKET[fixture]
