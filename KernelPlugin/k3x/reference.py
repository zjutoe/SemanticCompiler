"""Pure reference evaluator for the finite K2/K3-S construction.

Every judgment below is reconstructed from complete authoritative records.  A
replay request carries identities and runtime inputs only; it never carries a
formation, closure, trust, producer, graph, lifecycle, or result decision.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable


class FiniteProfileError(NotImplementedError):
    """The supplied constructor is outside the accepted finite profile."""


class Formation(Enum):
    WELL_FORMED = "WELL_FORMED"
    MALFORMED = "MALFORMED"


class Closure(Enum):
    CLOSED = "CLOSED"
    OPEN_BINDINGS = "OPEN_BINDINGS"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Evaluability(Enum):
    AVAILABLE = "EVALUABILITY_AVAILABLE"
    MISSING = "EVALUABILITY_MISSING"
    UNKNOWN = "EVALUABILITY_UNKNOWN"


class TrustState(Enum):
    ADMITTED = "ADMITTED"
    ABSENT = "ABSENT"
    UNDECIDED = "UNDECIDED"
    INCOMPATIBLE = "INCOMPATIBLE"
    FAILED = "FAILED"


class FailureDomain(Enum):
    FUNCTION_EVALUATION = "FUNCTION_EVALUATION"
    PREDICATE_EVALUATION = "PREDICATE_EVALUATION"
    PROFILE_CONCRETE = "PROFILE_CONCRETE"
    REASONING = "REASONING"


class Layer(Enum):
    DELTA = "Delta"
    SIGMA = "Sigma"
    SERVICE = "Service"


class ContractRole(Enum):
    TYPE_ADMISSION = "TYPE_ADMISSION"
    LITERAL_MEANING = "LITERAL_MEANING"
    FUNCTION_MEANING = "FUNCTION_MEANING"
    PREDICATE_MEANING = "PREDICATE_MEANING"
    PROFILE_COVERAGE = "PROFILE_COVERAGE"
    EVIDENCE_SCHEMA = "EVIDENCE_SCHEMA"
    ACCESS_BOUNDARY = "ACCESS_BOUNDARY"
    UNKNOWN_BEHAVIOR = "UNKNOWN_BEHAVIOR"
    EVALUATION_ERROR_BEHAVIOR = "EVALUATION_ERROR_BEHAVIOR"
    REASONING_ERROR_BEHAVIOR = "REASONING_ERROR_BEHAVIOR"
    SOUND_FRAGMENT = "SOUND_FRAGMENT"
    COMPLETE_FRAGMENT = "COMPLETE_FRAGMENT"
    REQUIRED_EVIDENCE = "REQUIRED_EVIDENCE"
    SERVICE_FAILURE_BEHAVIOR = "SERVICE_FAILURE_BEHAVIOR"


class ObservationKind(Enum):
    IDENTITY_PRESENCE = "IDENTITY_PRESENCE"
    DECLARATION_SHAPE = "DECLARATION_SHAPE"
    TYPE_ADMISSION_FACT = "TYPE_ADMISSION_FACT"
    VALUE_RESULT = "VALUE_RESULT"
    TERM_RESULT = "TERM_RESULT"
    EVAL_RESULT = "EVAL_RESULT"
    EVAL_RESULT_SEQUENCE = "EVAL_RESULT_SEQUENCE"
    PROFILE_RESULT = "PROFILE_RESULT"


class NodeOperation(Enum):
    OBSERVE = "observe"
    CHANGES_BETWEEN = "changes_between"


class ResolutionRelation(Enum):
    """Closed K2 coordinates at which an authoritative record is required."""

    FORMATION_RECORD = "FORMATION_RECORD"
    BINDING_MEMBER = "BINDING_MEMBER"
    AUTHORITY_MEMBER = "AUTHORITY_MEMBER"
    CHOICE_MEMBER = "CHOICE_MEMBER"
    LEXICAL_MEMBER = "LEXICAL_MEMBER"
    EXTRANEOUS_LEXICAL = "EXTRANEOUS_LEXICAL"
    SERVICE_DISCOVERY = "SERVICE_DISCOVERY"
    TRUST_POLICY = "TRUST_POLICY"
    TRUST_ROOT = "TRUST_ROOT"
    CERTIFICATE_ADMISSION = "CERTIFICATE_ADMISSION"
    MIGRATION = "MIGRATION"
    COMPATIBILITY = "COMPATIBILITY"
    OPTIONAL_EXTENSION = "OPTIONAL_EXTENSION"
    REQUIRED_EXTENSION = "REQUIRED_EXTENSION"
    MODEL_BINDING = "MODEL_BINDING"
    OPTIONAL_ALIAS = "OPTIONAL_ALIAS"
    REQUIRED_ALIAS = "REQUIRED_ALIAS"
    SIGMA_CONTRACT = "SIGMA_CONTRACT"
    SERVICE_CONTRACT = "SERVICE_CONTRACT"
    REQUEST_RECORD = "REQUEST_RECORD"
    RESULT_PROTOCOL = "RESULT_PROTOCOL"
    REQUEST_ENVIRONMENT = "REQUEST_ENVIRONMENT"
    OBSERVATION_RESULT = "OBSERVATION_RESULT"
    LIFECYCLE_TRANSITION = "LIFECYCLE_TRANSITION"
    EVIDENCE_TRUTH = "EVIDENCE_TRUTH"
    REASON_CARRIER = "REASON_CARRIER"
    CONFLICT_REPLACEMENT = "CONFLICT_REPLACEMENT"


class RecordKind(str, Enum):
    ABI = "ABI_RECORD"
    PACKAGE = "PACKAGE_RECORD"
    TYPE_DECLARATION = "TYPE_DECLARATION_RECORD"
    DECLARATION = "DECLARATION_RECORD"
    SYMBOL = "SYMBOL_RECORD"
    EVENT = "EVENT_DECLARATION_RECORD"
    PAIR_DECLARATION = "PAIR_DECLARATION_RECORD"
    OUTCOME = "OUTCOME_RECORD"
    BINDING = "BINDING_RECORD"
    PROFILE_BINDING = "PROFILE_BINDING_RECORD"
    PAIR_BINDING = "PAIR_BINDING_RECORD"
    AUTHORITY_FACT = "AUTHORITY_FACT_RECORD"
    CHOICE_BINDING = "CHOICE_BINDING_RECORD"
    LEXICAL_BINDING = "LEXICAL_BINDING_RECORD"
    SERVICE = "SERVICE_RECORD"
    CAPABILITY = "CAPABILITY_RECORD"
    TRUST_POLICY = "TRUST_POLICY_RECORD"
    TRUST_ROOT = "TRUST_ROOT_RECORD"
    CERTIFICATE = "CERTIFICATE_RECORD"
    MIGRATION = "MIGRATION_RECORD"
    COMPATIBILITY_CLAIM = "COMPATIBILITY_RECORD"
    SEMANTIC_EXTENSION = "SEMANTIC_EXTENSION_RECORD"
    MODEL_CONTRACT = "MODEL_CONTRACT_RECORD"
    ALIAS = "ALIAS_RECORD"
    CONTRACT_SPEC = "CONTRACT_SPEC_RECORD"
    REQUEST = "REQUEST_RECORD"
    RESULT = "RESULT_RECORD"
    SEMANTIC_ENVIRONMENT = "SEMANTIC_ENVIRONMENT_RECORD"
    TRUST_ENVIRONMENT = "TRUST_ENVIRONMENT_RECORD"
    DEPENDENCY_ENVIRONMENT = "DEPENDENCY_ENVIRONMENT_RECORD"
    OBSERVATION_ENVIRONMENT = "OBSERVATION_ENVIRONMENT_RECORD"
    LIFECYCLE = "LIFECYCLE_RECORD"
    EVENT_VALUE = "EVENT_VALUE_RECORD"
    TRACE_EVENT = "TRACE_EVENT_RECORD"
    SOURCE = "SOURCE_RECORD"
    AUTHORITY_REF = "AUTHORITY_REF_RECORD"
    EVIDENCE = "EVIDENCE_RECORD"
    REASON = "REASON_RECORD"
    CONFLICT = "CONFLICT_RECORD"
    PRODUCER = "PRODUCER_RECORD"
    OBSERVATION_NODE = "OBSERVATION_NODE_RECORD"
    PRESENTATION = "PRESENTATION_RECORD"


@dataclass(frozen=True, order=True)
class Version:
    components: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.components or any(value < 0 for value in self.components):
            raise ValueError("an exact version is a nonempty natural tuple")


@dataclass(frozen=True, order=True)
class ExactKey:
    owner: str
    namespace: str
    local: str
    version: Version

    def __post_init__(self) -> None:
        if not self.owner or not self.namespace or not self.local:
            raise ValueError("exact-key atoms are nonempty")


@dataclass(frozen=True, order=True)
class RecordIdentity:
    kind: RecordKind
    key: ExactKey


@dataclass(frozen=True)
class AbiRecord:
    version: Version


@dataclass(frozen=True)
class TypeDeclaration:
    type_key: ExactKey
    admitted_value_domain: RecordIdentity
    admitted_constructor_tags: frozenset[str]
    proper_declaration_dependencies: frozenset[RecordIdentity]

    def __post_init__(self) -> None:
        if not self.admitted_constructor_tags:
            raise ValueError("type declaration admits a nonempty closed tag set")


@dataclass(frozen=True)
class TypedValue:
    type_key: ExactKey
    constructor_tag: str
    value: Any


@dataclass(frozen=True)
class DeclarationShape:
    declaration_key: ExactKey
    symbol_key: ExactKey
    declaration_kind: str
    argument_types: tuple[ExactKey, ...]
    result_kind: str
    facet_positions: tuple[frozenset[str], ...]
    proper_type_dependencies: frozenset[RecordIdentity]


@dataclass(frozen=True)
class ObservationQuery:
    dependency: RecordIdentity
    expected_kind: ObservationKind
    input_projection: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.input_projection:
            raise ValueError("observation input projection is explicit and total")


@dataclass(frozen=True)
class ContractSpec:
    contract_key: ExactKey
    owner_layer: Layer
    role: ContractRole
    primary_input_domain: tuple[str, ...]
    codomain: frozenset[str]
    observation_queries: tuple[ObservationQuery, ...]
    support: frozenset[RecordIdentity]
    relation_name: str


@dataclass(frozen=True)
class SemanticBinding:
    binding_key: ExactKey
    declaration: RecordIdentity
    binding_kind: str
    meaning_contract: RecordIdentity
    permitted_facet_inputs: tuple[frozenset[str], ...]
    proper_semantic_dependencies: frozenset[RecordIdentity]
    dependency_closure: frozenset[RecordIdentity]
    evidence_schema: RecordIdentity
    access_boundary: RecordIdentity
    unknown_contract: RecordIdentity
    evaluation_error_contract: RecordIdentity
    determinism_rule: str

    @property
    def proper_dependencies(self) -> frozenset[RecordIdentity]:
        return self.proper_semantic_dependencies


@dataclass(frozen=True)
class ModelCapabilitySummary:
    capability_key: RecordIdentity
    service_role: str
    supported_judgments: frozenset[str]
    capability_class: str
    sound_fragment_key: RecordIdentity
    complete_fragment_key: RecordIdentity | None
    dependency_scope: frozenset[RecordIdentity]


@dataclass(frozen=True)
class ModelContract:
    model_key: ExactKey
    target_binding: RecordIdentity
    exact_version: Version
    exact_symbol_key: ExactKey
    exact_argument_types: tuple[ExactKey, ...]
    exact_result_kind: str
    exact_facet_positions: tuple[frozenset[str], ...]
    evidence_contract: RecordIdentity
    unknown_contract: RecordIdentity
    error_contract: RecordIdentity
    semantic_contract: RecordIdentity
    capability_summaries: frozenset[ModelCapabilitySummary]
    explanatory_text: None = None

    def __post_init__(self) -> None:
        if self.explanatory_text is not None:
            raise ValueError("finite model explanatory_text is exactly ABSENT")


@dataclass(frozen=True)
class ServiceIdentity:
    service_key: ExactKey
    abi_version: Version
    plugin_key: ExactKey


@dataclass(frozen=True)
class CapabilityDescriptor:
    capability_key: ExactKey
    service: RecordIdentity
    abi_version: Version
    plugin_key: ExactKey
    service_role: str
    capability_class: str
    supported_judgments: frozenset[str]
    supported_targets: frozenset[RecordIdentity]
    sound_fragment: RecordIdentity
    complete_fragment: RecordIdentity | None
    dependency_scope: frozenset[RecordIdentity]
    proper_semantic_dependencies: frozenset[RecordIdentity]
    dependency_closure: frozenset[RecordIdentity]
    required_evidence: RecordIdentity
    required_trust_roots: frozenset[RecordIdentity]
    failure_contract: RecordIdentity

    @property
    def proper_dependencies(self) -> frozenset[RecordIdentity]:
        return self.proper_semantic_dependencies


@dataclass(frozen=True)
class CertificateRecord:
    certificate_key: ExactKey
    subject: RecordIdentity
    judgment: str
    issuer: str


@dataclass(frozen=True)
class ProducerRecord:
    subject: RecordIdentity
    producer: str
    producer_role: str


@dataclass(frozen=True)
class TrustPolicyRecord:
    policy_key: ExactKey
    policy_owner: str


@dataclass(frozen=True)
class TrustRootRecord:
    root_key: ExactKey
    owner: str
    trusted_validators: frozenset[RecordIdentity]
    permitted_certificate_kinds: frozenset[str]
    permitted_targets: frozenset[RecordIdentity]
    adoption: str


@dataclass(frozen=True)
class TrustRootJudgment:
    state: TrustState
    admitted_root: TrustRootRecord | None = None
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.state is TrustState.ADMITTED:
            if self.admitted_root is None or self.reasons:
                raise ValueError("admitted trust judgment carries the exact root only")
        elif self.admitted_root is not None:
            raise ValueError("non-admitted trust judgment carries no root")


@dataclass(frozen=True)
class TrustEnvironment:
    policy: RecordIdentity
    policy_owner: str
    root_judgments: tuple[tuple[RecordIdentity, TrustRootJudgment], ...]
    discovery_failure: str | None = None

    def __post_init__(self) -> None:
        if len({root for root, _ in self.root_judgments}) != len(self.root_judgments):
            raise ValueError("duplicate trust-root judgment")

    @property
    def roots(self) -> tuple[RecordIdentity, ...]:
        return tuple(root for root, _ in self.root_judgments)


@dataclass(frozen=True)
class SemanticEnvironment:
    abi_version: Version
    declarations: tuple[RecordIdentity, ...]
    pair_declarations: tuple[RecordIdentity, ...]
    bindings: tuple[RecordIdentity, ...]
    profile_bindings: tuple[RecordIdentity, ...] = ()
    pair_bindings: tuple[RecordIdentity, ...] = ()
    authority_facts: tuple[RecordIdentity, ...] = ()
    semantic_extensions: tuple[RecordIdentity, ...] = ()
    lexical_bindings: tuple[RecordIdentity, ...] = ()
    choice_bindings: tuple[RecordIdentity, ...] = ()
    mechanically_extracted_dependencies: frozenset[RecordIdentity] = frozenset()
    chi_c: tuple[tuple[str, Any], ...] = ()

    def all_references(self) -> frozenset[RecordIdentity]:
        return frozenset(
            self.declarations
            + self.pair_declarations
            + self.bindings
            + self.profile_bindings
            + self.pair_bindings
            + self.authority_facts
            + self.semantic_extensions
            + self.lexical_bindings
            + self.choice_bindings
        )


@dataclass(frozen=True)
class DependencyEnvironment:
    syntax_root_keys: frozenset[RecordIdentity]
    subject_root_keys: frozenset[RecordIdentity]
    binding_association_edges: frozenset[tuple[RecordIdentity, RecordIdentity]]
    expanded_root_keys: frozenset[RecordIdentity]
    proper_dependencies: frozenset[RecordIdentity]
    transitive_dependency_closure: frozenset[RecordIdentity]
    validation_references: frozenset[RecordIdentity]


@dataclass(frozen=True)
class InvocationRequest:
    target: RecordIdentity
    semantic_environment: RecordIdentity
    dependency_environment: RecordIdentity
    trust_environment: RecordIdentity
    requested_version: Version
    arguments: tuple[Any, ...]


@dataclass(frozen=True)
class ReasoningRequest:
    abi_version: Version
    judgment: str
    subjects: tuple[Any, ...]
    semantic_environment: RecordIdentity
    trust_environment: RecordIdentity
    required_fragment: RecordIdentity
    complete_dependencies: RecordIdentity
    capability_target: RecordIdentity
    capability_key: RecordIdentity


@dataclass(frozen=True)
class ResultRecord:
    request: RecordIdentity
    result_kind: str
    result: Any


@dataclass(frozen=True)
class LifecycleRecord:
    request: RecordIdentity
    judgment: str


@dataclass(frozen=True)
class ObservationEnvironment:
    values: tuple[tuple[RecordIdentity, Any], ...]


@dataclass(frozen=True)
class PairDeclaration:
    pair_key: ExactKey
    scope_symbol: ExactKey
    occurrence_symbol: ExactKey
    controlled_keys: frozenset[ExactKey]
    proper_declaration_dependencies: frozenset[RecordIdentity]


@dataclass(frozen=True)
class OccurrenceSemanticContractBundle:
    meaning_contract: RecordIdentity
    permitted_facet_inputs: tuple[frozenset[str], ...]
    evidence_schema: RecordIdentity
    access_boundary: RecordIdentity
    unknown_contract: RecordIdentity
    evaluation_error_contract: RecordIdentity
    determinism_rule: str
    proper_semantic_dependencies: frozenset[RecordIdentity]
    dependency_closure: frozenset[RecordIdentity]


@dataclass(frozen=True)
class PairBinding:
    pair_key: ExactKey
    scope_binding_key: RecordIdentity
    occurrence_binding_key: RecordIdentity
    occurrence_model_contract_key: RecordIdentity
    occurrence_bundle: RecordIdentity
    certificate: RecordIdentity
    validator: RecordIdentity
    proper_semantic_dependencies: frozenset[RecordIdentity]
    dependency_closure: frozenset[RecordIdentity]
    validation_references: frozenset[RecordIdentity]


@dataclass(frozen=True)
class PairRequestData:
    abi_version: Version
    pair_binding: RecordIdentity
    semantic_environment: RecordIdentity
    trust_environment: RecordIdentity
    complete_dependencies: RecordIdentity
    capability_target: RecordIdentity
    capability_key: RecordIdentity


@dataclass(frozen=True)
class PairFullEvalProof:
    pair_key: ExactKey
    bundle: RecordIdentity
    reference_contract: RecordIdentity
    trace_domain: str
    compared_fields: str


@dataclass(frozen=True)
class EvidenceRecord:
    issuer: str
    namespace: str
    local: str
    schema_contract: RecordIdentity


@dataclass(frozen=True)
class CertificateEnvelope:
    certificate_key: ExactKey
    certificate_kind: str
    request_binding: RecordIdentity
    subjects: tuple[RecordIdentity, ...]
    environment: RecordIdentity
    capability_key: RecordIdentity
    fragment: RecordIdentity
    dependencies: RecordIdentity
    claimed_conclusion: str
    validator_key: RecordIdentity
    trust_root_key: RecordIdentity
    abstraction_class: str
    payload: RecordIdentity
    evidence_refs: frozenset[RecordIdentity]


@dataclass(frozen=True)
class ChoiceBinding:
    choice_key: ExactKey
    authority_fact: RecordIdentity
    selected_value: str


@dataclass(frozen=True)
class LexicalBinding:
    lexical_key: ExactKey
    declaration: RecordIdentity
    source_scope: str


@dataclass(frozen=True)
class EvolutionRecord:
    evolution_key: ExactKey
    subject: RecordIdentity
    required: bool


@dataclass(frozen=True)
class OutcomeRecord:
    outcome_kind: str
    value: Any
    references: frozenset[RecordIdentity] = frozenset()


@dataclass(frozen=True)
class AuthorityFactRecord:
    authority_fact_key: ExactKey
    authority_ref: RecordIdentity
    source_ref: RecordIdentity
    principal: str
    admission_subject_data: Any
    evidence_refs: frozenset[RecordIdentity]


@dataclass(frozen=True)
class SourceRecord:
    issuer: str
    namespace: str
    stable_identity: str


@dataclass(frozen=True)
class AuthorityRefRecord:
    owner: str
    principal: str
    authority_kind: str


@dataclass(frozen=True)
class EventValueRecord:
    event_value: Any


@dataclass(frozen=True)
class TraceEventRecord:
    trace_event: Any


@dataclass(frozen=True)
class ReasonRecord:
    reason_sort: str
    issuer: str
    code: str
    subject_identity: Any


@dataclass(frozen=True)
class ConflictRecord:
    conflict_kind: str
    involved_identity_set: frozenset[RecordIdentity]


@dataclass(frozen=True)
class NamedCarrier:
    name: str
    references: frozenset[RecordIdentity] = frozenset()
    value: Any = None


@dataclass(frozen=True)
class ObservationNode:
    operation: NodeOperation
    arguments: tuple[Any, ...]
    contract_spec: RecordIdentity


@dataclass(frozen=True)
class PluginPackage:
    abi_version: Version
    plugin_key: ExactKey
    owner: str
    declarations: tuple["LogicalRecord", ...] = ()
    pair_declarations: tuple["LogicalRecord", ...] = ()
    bindings: tuple["LogicalRecord", ...] = ()
    pair_bindings: tuple["LogicalRecord", ...] = ()
    profile_bindings: tuple["LogicalRecord", ...] = ()
    model_contracts: tuple["LogicalRecord", ...] = ()
    aliases: tuple["LogicalRecord", ...] = ()
    services: tuple["LogicalRecord", ...] = ()
    certificates: tuple["LogicalRecord", ...] = ()
    authority_facts: tuple["LogicalRecord", ...] = ()
    compatibility_claims: tuple["LogicalRecord", ...] = ()
    migrations: tuple["LogicalRecord", ...] = ()
    semantic_extensions: tuple["LogicalRecord", ...] = ()
    diagnostics: None = None

    def members(self) -> tuple["LogicalRecord", ...]:
        return (self.declarations + self.pair_declarations + self.bindings
                + self.pair_bindings + self.profile_bindings
                + self.model_contracts + self.aliases + self.services
                + self.certificates + self.authority_facts
                + self.compatibility_claims + self.migrations
                + self.semantic_extensions)


RecordValue = AbiRecord | TypeDeclaration | TypedValue | DeclarationShape | ContractSpec | SemanticBinding | ModelContract | ServiceIdentity | CapabilityDescriptor | CertificateRecord | ProducerRecord | TrustPolicyRecord | TrustRootRecord | TrustEnvironment | SemanticEnvironment | DependencyEnvironment | InvocationRequest | ReasoningRequest | ResultRecord | LifecycleRecord | ObservationEnvironment | PairDeclaration | OccurrenceSemanticContractBundle | PairBinding | PairRequestData | PairFullEvalProof | EvidenceRecord | CertificateEnvelope | ChoiceBinding | LexicalBinding | EvolutionRecord | OutcomeRecord | AuthorityFactRecord | SourceRecord | AuthorityRefRecord | EventValueRecord | TraceEventRecord | ReasonRecord | ConflictRecord | NamedCarrier | ObservationNode | PluginPackage


@dataclass(frozen=True)
class LogicalRecord:
    identity: RecordIdentity
    value: RecordValue


@dataclass(frozen=True)
class PredicateFacetPositions:
    """The admitted three-position predicate facet sequence."""
    positions: tuple[frozenset[str], frozenset[str], frozenset[str]]


@dataclass(frozen=True)
class PredicateFacetPositionsConflict:
    declaration_key: ExactKey
    unequal_positions: frozenset[PredicateFacetPositions]

    def __post_init__(self) -> None:
        if len(self.unequal_positions) != 2:
            raise ValueError("predicate facet conflict has exactly two admitted positions")


@dataclass(frozen=True)
class ConflictRef:
    conflict_kind: PredicateFacetPositionsConflict
    involved_identity_set: frozenset[RecordIdentity]


@dataclass(frozen=True)
class Composition:
    records: frozenset[LogicalRecord]
    conflicts: tuple[ConflictRef, ...]

    def at(self, identity: RecordIdentity) -> LogicalRecord | None:
        matches = tuple(record for record in self.records if record.identity == identity)
        return matches[0] if matches else None


@dataclass(frozen=True)
class Judgment:
    tag: str
    details: tuple[Any, ...] = ()


@dataclass(frozen=True)
class InterfaceFailure:
    domain: FailureDomain
    kind: str
    reasons: frozenset[str]


@dataclass(frozen=True)
class ContractReplay:
    formation: Formation
    closure: Closure
    evaluability: Evaluability
    lifecycle: str
    result: Any | None


@dataclass(frozen=True)
class CoreReplay:
    authoritative: Composition
    formation: Formation
    closure: Closure
    evaluability: Evaluability
    lifecycle: str
    result: Any | None


@dataclass(frozen=True)
class PairValidationResult:
    pair_key: ExactKey
    certificate_key: ExactKey
    result: str


@dataclass(frozen=True)
class PairReplay:
    authoritative: Composition
    formation: Formation
    closure: Closure
    result: PairValidationResult


@dataclass(frozen=True)
class LookupReplay:
    authoritative: Composition
    result: Judgment


@dataclass(frozen=True)
class ObservationEvaluation:
    observations: tuple[tuple[RecordIdentity, Any], ...]
    reasoning_result: Judgment
    lifecycle: str
    status: tuple[str, ...]


@dataclass(frozen=True)
class CompositionReplay:
    composition: Composition
    formation: Formation
    closure: Closure


@dataclass(frozen=True)
class InvocationReplayRequest:
    request: RecordIdentity


@dataclass(frozen=True)
class PairReplayRequest:
    request: RecordIdentity


@dataclass(frozen=True)
class ResolutionCoordinate:
    """A structural consumer/slot, never a precomputed missing judgment."""

    relation: ResolutionRelation
    consumer: RecordIdentity | None = None
    replacement: RecordIdentity | None = None


@dataclass(frozen=True)
class LookupRequest:
    target: RecordIdentity
    coordinate: ResolutionCoordinate
    context_roots: tuple[RecordIdentity, ...] = ()

    def __post_init__(self) -> None:
        if not self.context_roots:
            raise ValueError("lookup requires its literal row-local context roots")


@dataclass(frozen=True)
class GraphEvaluationRequest:
    nodes: tuple[RecordIdentity, ...]
    preferred_order: tuple[RecordIdentity, ...]
    reasoning_request: RecordIdentity
    trust_environment: RecordIdentity
    semantic_environment: RecordIdentity
    dependency_environment: RecordIdentity
    observation_environment: RecordIdentity
    result_record: RecordIdentity
    lifecycle_record: RecordIdentity
    status_record: RecordIdentity


@dataclass(frozen=True)
class FormationRequest:
    bindings: tuple[RecordIdentity, ...]


@dataclass(frozen=True)
class CompositionRequest:
    presentations: tuple[tuple[LogicalRecord, ...], ...]


ReplayRequest = InvocationReplayRequest | PairReplayRequest | LookupRequest | GraphEvaluationRequest | FormationRequest | CompositionRequest


@dataclass(frozen=True)
class Universe:
    records: tuple[LogicalRecord, ...]
    request: ReplayRequest


_VALUE_KIND = {
    AbiRecord: {RecordKind.ABI},
    TypeDeclaration: {RecordKind.TYPE_DECLARATION},
    DeclarationShape: {RecordKind.DECLARATION, RecordKind.SYMBOL, RecordKind.EVENT},
    ContractSpec: {RecordKind.CONTRACT_SPEC},
    SemanticBinding: {RecordKind.BINDING, RecordKind.PROFILE_BINDING},
    ModelContract: {RecordKind.MODEL_CONTRACT},
    ServiceIdentity: {RecordKind.SERVICE},
    CapabilityDescriptor: {RecordKind.CAPABILITY},
    CertificateRecord: {RecordKind.CERTIFICATE},
    ProducerRecord: {RecordKind.PRODUCER},
    TrustPolicyRecord: {RecordKind.TRUST_POLICY},
    TrustRootRecord: {RecordKind.TRUST_ROOT},
    TrustEnvironment: {RecordKind.TRUST_ENVIRONMENT},
    SemanticEnvironment: {RecordKind.SEMANTIC_ENVIRONMENT},
    DependencyEnvironment: {RecordKind.DEPENDENCY_ENVIRONMENT},
    InvocationRequest: {RecordKind.REQUEST},
    ReasoningRequest: {RecordKind.REQUEST},
    ResultRecord: {RecordKind.RESULT},
    LifecycleRecord: {RecordKind.LIFECYCLE},
    ObservationEnvironment: {RecordKind.OBSERVATION_ENVIRONMENT},
    PairDeclaration: {RecordKind.PAIR_DECLARATION},
    OccurrenceSemanticContractBundle: {RecordKind.BINDING},
    PairBinding: {RecordKind.PAIR_BINDING},
    PairRequestData: {RecordKind.REQUEST},
    PairFullEvalProof: {RecordKind.EVIDENCE},
    EvidenceRecord: {RecordKind.EVIDENCE},
    CertificateEnvelope: {RecordKind.CERTIFICATE},
    ChoiceBinding: {RecordKind.CHOICE_BINDING},
    LexicalBinding: {RecordKind.LEXICAL_BINDING},
    EvolutionRecord: {RecordKind.MIGRATION, RecordKind.COMPATIBILITY_CLAIM, RecordKind.SEMANTIC_EXTENSION, RecordKind.ALIAS},
    OutcomeRecord: {RecordKind.OUTCOME},
    AuthorityFactRecord: {RecordKind.AUTHORITY_FACT},
    SourceRecord: {RecordKind.SOURCE},
    AuthorityRefRecord: {RecordKind.AUTHORITY_REF},
    EventValueRecord: {RecordKind.EVENT_VALUE},
    TraceEventRecord: {RecordKind.TRACE_EVENT},
    ReasonRecord: {RecordKind.REASON},
    ConflictRecord: {RecordKind.CONFLICT},
    ObservationNode: {RecordKind.OBSERVATION_NODE},
    PluginPackage: {RecordKind.PACKAGE},
}


def _record_shape(record: LogicalRecord) -> bool:
    allowed = _VALUE_KIND.get(type(record.value))
    if allowed is not None:
        return record.identity.kind in allowed
    return isinstance(record.value, TypedValue) or (
        isinstance(record.value, NamedCarrier)
        and record.identity.kind is RecordKind.PRESENTATION
    )


def exact_version_agreement(requested: Version, supplied: Version) -> bool:
    return requested == supplied


def admit_typed_value(declaration: TypeDeclaration, value: TypedValue) -> Judgment:
    if value.type_key != declaration.type_key:
        return Judgment("NOT_ADMITTED", ("TYPE_KEY_MISMATCH",))
    if value.constructor_tag not in declaration.admitted_constructor_tags:
        return Judgment("NOT_ADMITTED", ("CONSTRUCTOR_TAG", value.constructor_tag))
    return Judgment("ADMITTED")


def validate_declaration_shape(declaration: DeclarationShape) -> Judgment:
    if declaration.declaration_kind not in {"FUNCTION", "PREDICATE", "EVENT"}:
        return Judgment("MALFORMED", ("DECLARATION_KIND",))
    if declaration.declaration_key.owner != declaration.symbol_key.owner:
        return Judgment("MALFORMED", ("DECLARATION_SYMBOL_OWNER",))
    if declaration.declaration_key.version != declaration.symbol_key.version:
        return Judgment("MALFORMED", ("DECLARATION_SYMBOL_VERSION",))
    if len(declaration.facet_positions) != len(declaration.argument_types):
        return Judgment("MALFORMED", ("FACET_ARITY",))
    if any(item.kind is not RecordKind.TYPE_DECLARATION for item in declaration.proper_type_dependencies):
        return Judgment("MALFORMED", ("TYPE_DEPENDENCY_KIND",))
    return Judgment("WELL_FORMED")


def validate_contract_spec(spec: ContractSpec) -> Judgment:
    keys = tuple(query.dependency for query in spec.observation_queries)
    if len(keys) != len(set(keys)):
        return Judgment("MALFORMED", ("DUPLICATE_OBSERVATION_QUERY",))
    if frozenset(keys) != spec.support:
        return Judgment("MALFORMED", ("SUPPORT_QUERY_MISMATCH",))
    delta = {ContractRole.TYPE_ADMISSION}
    service = {ContractRole.SOUND_FRAGMENT, ContractRole.COMPLETE_FRAGMENT, ContractRole.REQUIRED_EVIDENCE, ContractRole.SERVICE_FAILURE_BEHAVIOR}
    if spec.owner_layer is Layer.DELTA and spec.role not in delta:
        return Judgment("MALFORMED", ("DELTA_ROLE",))
    if spec.owner_layer is Layer.SERVICE and spec.role not in service:
        return Judgment("MALFORMED", ("SERVICE_ROLE",))
    if spec.owner_layer is Layer.SIGMA and spec.role in delta | service:
        return Judgment("MALFORMED", ("SIGMA_ROLE",))
    if spec.owner_layer is Layer.SERVICE:
        legal = {ObservationKind.TERM_RESULT, ObservationKind.EVAL_RESULT, ObservationKind.EVAL_RESULT_SEQUENCE, ObservationKind.PROFILE_RESULT}
        if any(query.expected_kind not in legal for query in spec.observation_queries):
            return Judgment("MALFORMED", ("SERVICE_OBSERVATION_KIND",))
    if not spec.primary_input_domain or not spec.codomain or not spec.relation_name:
        return Judgment("MALFORMED", ("INCOMPLETE_CONTRACT_SPEC",))
    return Judgment("WELL_FORMED")


def _expand(records: Iterable[LogicalRecord]) -> tuple[LogicalRecord, ...]:
    expanded: list[LogicalRecord] = []
    for record in records:
        expanded.append(record)
        if isinstance(record.value, PluginPackage):
            expanded.extend(_expand(record.value.members()))
    return tuple(expanded)


def compose_records(records: tuple[LogicalRecord, ...]) -> Composition:
    grouped: dict[RecordIdentity, set[LogicalRecord]] = {}
    for record in _expand(records):
        if not isinstance(record, LogicalRecord) or not _record_shape(record):
            raise TypeError("composition accepts field-complete kind-conformant records")
        grouped.setdefault(record.identity, set()).add(record)
    accepted: set[LogicalRecord] = set()
    conflicts: list[ConflictRef] = []
    for identity in sorted(grouped):
        alternatives = grouped[identity]
        if len(alternatives) == 1:
            accepted.add(next(iter(alternatives)))
        else:
            if (identity.kind is not RecordKind.DECLARATION
                    or not all(isinstance(item.value, DeclarationShape) for item in alternatives)):
                raise TypeError("finite conflicts are only predicate-facet conflicts")
            positions = frozenset(PredicateFacetPositions(item.value.facet_positions) for item in alternatives)
            conflicts.append(ConflictRef(PredicateFacetPositionsConflict(identity.key, positions), frozenset({identity})))
    return Composition(frozenset(accepted), tuple(conflicts))


def _resolve(composition: Composition, identity: RecordIdentity, value_type: type[Any] | tuple[type[Any], ...] | None = None) -> LogicalRecord | None:
    record = composition.at(identity)
    if record is None or (value_type is not None and not isinstance(record.value, value_type)):
        return None
    return record


def validate_packages(composition: Composition) -> Judgment:
    if composition.conflicts:
        return Judgment("MALFORMED", ("CONFLICT", composition.conflicts))
    keyed_values = (
        (TypeDeclaration, "type_key"),
        (DeclarationShape, "declaration_key"),
        (ContractSpec, "contract_key"),
        (ModelContract, "model_key"),
        (ServiceIdentity, "service_key"),
        (CapabilityDescriptor, "capability_key"),
        (CertificateRecord, "certificate_key"),
        (CertificateEnvelope, "certificate_key"),
        (TrustPolicyRecord, "policy_key"),
        (TrustRootRecord, "root_key"),
        (ChoiceBinding, "choice_key"),
        (LexicalBinding, "lexical_key"),
        (EvolutionRecord, "evolution_key"),
    )
    for record in composition.records:
        if isinstance(record.value, AbiRecord) and record.identity.key.version != record.value.version:
            return Judgment("MALFORMED", ("ABI_RECORD_IDENTITY", record.identity))
        for value_type, field in keyed_values:
            if isinstance(record.value, value_type) and getattr(record.value, field) != record.identity.key:
                return Judgment("MALFORMED", ("RECORD_FIELD_IDENTITY", record.identity))
        if isinstance(record.value, CertificateRecord) and record.value.issuer != record.value.certificate_key.owner:
            return Judgment("MALFORMED", ("CERTIFICATE_ISSUER_OWNER", record.identity))
        if isinstance(record.value, TypeDeclaration):
            admission = _resolve(composition, record.value.admitted_value_domain, ContractSpec)
            if admission is None or admission.value.owner_layer is not Layer.DELTA or admission.value.role is not ContractRole.TYPE_ADMISSION:
                return Judgment("MALFORMED", ("TYPE_ADMISSION_CONTRACT", record.identity))
            expected = admission.value.support
            if record.value.proper_declaration_dependencies != expected:
                return Judgment("MALFORMED", ("TYPE_DEPENDENCY_PROJECTION", record.identity))
        if isinstance(record.value, ServiceIdentity):
            if record.value.abi_version != record.identity.key.version and record.value.abi_version.components != (0,):
                return Judgment("MALFORMED", ("SERVICE_ABI", record.identity))
            if record.value.service_key.owner != record.value.plugin_key.owner:
                return Judgment("MALFORMED", ("SERVICE_PLUGIN", record.identity))
        if not isinstance(record.value, PluginPackage):
            continue
        package = record.value
        if record.identity.key != package.plugin_key or package.owner != package.plugin_key.owner:
            return Judgment("MALFORMED", ("PACKAGE_IDENTITY", record.identity))
        for member in package.members():
            if member.identity.key.owner != package.owner:
                return Judgment("MALFORMED", ("PACKAGE_OWNER", member.identity))
            if composition.at(member.identity) != member:
                return Judgment("MALFORMED", ("PACKAGE_MEMBER_MISMATCH", member.identity))
        categories = (
            (package.declarations, {RecordKind.TYPE_DECLARATION, RecordKind.DECLARATION, RecordKind.SYMBOL, RecordKind.EVENT}),
            (package.pair_declarations, {RecordKind.PAIR_DECLARATION}),
            (package.bindings, {RecordKind.BINDING}),
            (package.pair_bindings, {RecordKind.PAIR_BINDING}),
            (package.profile_bindings, {RecordKind.PROFILE_BINDING}),
            (package.model_contracts, {RecordKind.MODEL_CONTRACT}),
            (package.aliases, {RecordKind.ALIAS}),
            (package.services, {RecordKind.CAPABILITY}),
            (package.certificates, {RecordKind.CERTIFICATE}),
            (package.authority_facts, {RecordKind.AUTHORITY_FACT}),
            (package.compatibility_claims, {RecordKind.COMPATIBILITY_CLAIM}),
            (package.migrations, {RecordKind.MIGRATION}),
            (package.semantic_extensions, {RecordKind.SEMANTIC_EXTENSION}),
        )
        for members, kinds in categories:
            if any(member.identity.kind not in kinds for member in members):
                return Judgment("MALFORMED", ("PACKAGE_MEMBER_CATEGORY", record.identity))
        if any(isinstance(member.value, CapabilityDescriptor) and (member.value.abi_version != package.abi_version or member.value.plugin_key != package.plugin_key) for member in package.services):
            return Judgment("MALFORMED", ("DESCRIPTOR_PACKAGE_ABI_OR_PLUGIN", record.identity))
    return Judgment("WELL_FORMED")


def validate_binding(binding: SemanticBinding, composition: Composition) -> Judgment:
    if binding.binding_key.owner != binding.declaration.key.owner:
        return Judgment("MALFORMED", ("BINDING_OWNER",))
    declaration = _resolve(composition, binding.declaration, DeclarationShape)
    fields = (
        (binding.meaning_contract, {
            "LITERAL": ContractRole.LITERAL_MEANING,
            "FUNCTION": ContractRole.FUNCTION_MEANING,
            "PREDICATE": ContractRole.PREDICATE_MEANING,
            "PROFILE": ContractRole.PREDICATE_MEANING,
        }.get(binding.binding_kind)),
        (binding.evidence_schema, ContractRole.EVIDENCE_SCHEMA),
        (binding.access_boundary, ContractRole.ACCESS_BOUNDARY),
        (binding.unknown_contract, ContractRole.UNKNOWN_BEHAVIOR),
        (binding.evaluation_error_contract, ContractRole.EVALUATION_ERROR_BEHAVIOR),
    )
    resolved = tuple((_resolve(composition, identity, ContractSpec), role) for identity, role in fields)
    if declaration is None or any(record is None for record, _ in resolved):
        return Judgment("OPEN_BINDINGS", tuple(identity for (identity, _), (record, _) in zip(fields, resolved) if record is None))
    if (binding.binding_key.owner != binding.declaration.key.owner
            or binding.binding_key.version != binding.declaration.key.version
            or binding.binding_kind != declaration.value.declaration_kind):
        return Judgment("MALFORMED", ("BINDING_IDENTITY_OR_KIND",))
    if binding.permitted_facet_inputs != declaration.value.facet_positions:
        return Judgment("MALFORMED", ("BINDING_FACETS",))
    if any(record.value.owner_layer is not Layer.SIGMA or record.value.role is not role or validate_contract_spec(record.value).tag != "WELL_FORMED" for record, role in resolved):
        return Judgment("MALFORMED", ("BINDING_CONTRACT_ROLE",))
    if binding.determinism_rule != "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT":
        return Judgment("MALFORMED", ("BINDING_DETERMINISM",))
    expected = frozenset({binding.declaration, *(identity for identity, _ in fields)}) | resolved[0][0].value.support
    if binding.proper_semantic_dependencies != expected:
        return Judgment("MALFORMED", ("BINDING_SUPPORT_PROJECTION", expected, binding.proper_semantic_dependencies))
    expected_closure = _reachable_closure(expected, composition)
    if binding.dependency_closure != expected_closure:
        return Judgment("MALFORMED", ("DEPENDENCY_CLOSURE", expected_closure, binding.dependency_closure))
    if any(_resolve(composition, item) is None for item in binding.dependency_closure):
        return Judgment("OPEN_BINDINGS", tuple(item for item in binding.dependency_closure if _resolve(composition, item) is None))
    return Judgment("CLOSED")


def _direct_dependencies(identity: RecordIdentity, composition: Composition) -> frozenset[RecordIdentity]:
    record = composition.at(identity)
    if record is None:
        return frozenset()
    value = record.value
    if isinstance(value, TypeDeclaration):
        return frozenset({value.admitted_value_domain}) | value.proper_declaration_dependencies
    if isinstance(value, DeclarationShape):
        return value.proper_type_dependencies
    if isinstance(value, ContractSpec):
        return value.support
    if isinstance(value, SemanticBinding):
        return value.proper_semantic_dependencies
    if isinstance(value, OccurrenceSemanticContractBundle):
        return value.proper_semantic_dependencies
    return frozenset()


def _reachable_closure(roots: frozenset[RecordIdentity], composition: Composition) -> frozenset[RecordIdentity]:
    reached = set(roots)
    pending = list(roots)
    while pending:
        current = pending.pop()
        for dependency in _direct_dependencies(current, composition):
            if dependency not in reached:
                reached.add(dependency)
                pending.append(dependency)
    return frozenset(reached)


def validate_model_descriptor(model: ModelContract, descriptor: CapabilityDescriptor, composition: Composition) -> Judgment:
    descriptor_identity = RecordIdentity(RecordKind.CAPABILITY, descriptor.capability_key)
    owning_packages = tuple(record.value for record in composition.records if isinstance(record.value, PluginPackage) and any(member.identity == descriptor_identity for member in record.value.services))
    if len(owning_packages) != 1 or owning_packages[0].abi_version != descriptor.abi_version or owning_packages[0].plugin_key != descriptor.plugin_key:
        return Judgment("MALFORMED", ("DESCRIPTOR_PACKAGE_ABI_OR_PLUGIN",))
    target_binding = _resolve(composition, model.target_binding, SemanticBinding)
    target = None if target_binding is None else _resolve(composition, target_binding.value.declaration, DeclarationShape)
    semantic = _resolve(composition, model.semantic_contract, ContractSpec)
    service = _resolve(composition, descriptor.service, ServiceIdentity)
    sound = _resolve(composition, descriptor.sound_fragment, ContractSpec)
    complete = None if descriptor.complete_fragment is None else _resolve(composition, descriptor.complete_fragment, ContractSpec)
    if target is None or semantic is None:
        return Judgment("MALFORMED", ("MODEL_TARGET_OR_CONTRACT",))
    declaration = target.value
    if model.exact_version != model.target_binding.key.version or model.model_key.owner != model.target_binding.key.owner:
        return Judgment("MALFORMED", ("MODEL_VERSION_OR_OWNER",))
    if target_binding is None or target_binding.value.meaning_contract != model.semantic_contract:
        return Judgment("MALFORMED", ("MODEL_BINDING_CONTRACT",))
    if (model.exact_symbol_key, model.exact_argument_types, model.exact_result_kind, model.exact_facet_positions) != (declaration.symbol_key, declaration.argument_types, declaration.result_kind, declaration.facet_positions):
        return Judgment("MALFORMED", ("MODEL_DECLARATION_SHAPE",))
    role_checks = (
        (model.evidence_contract, ContractRole.EVIDENCE_SCHEMA),
        (model.unknown_contract, ContractRole.UNKNOWN_BEHAVIOR),
        (model.error_contract, ContractRole.EVALUATION_ERROR_BEHAVIOR),
    )
    if any((record := _resolve(composition, identity, ContractSpec)) is None or record.value.role is not role for identity, role in role_checks):
        return Judgment("MALFORMED", ("MODEL_AUXILIARY_CONTRACT",))
    if service is None or sound is None or (descriptor.complete_fragment is not None and complete is None):
        return Judgment("MALFORMED", ("DESCRIPTOR_SERVICE_OR_FRAGMENT",))
    if (service.value.abi_version != descriptor.abi_version
            or service.value.plugin_key != descriptor.plugin_key
            or descriptor.service_role not in descriptor.supported_judgments
            or not descriptor.supported_judgments):
        return Judgment("MALFORMED", ("DESCRIPTOR_JUDGMENT",))
    if sound is not None and (sound.value.owner_layer is not Layer.SERVICE or sound.value.role is not ContractRole.SOUND_FRAGMENT):
        return Judgment("MALFORMED", ("DESCRIPTOR_SOUND_ROLE",))
    if complete is not None and (complete.value.owner_layer is not Layer.SERVICE or complete.value.role is not ContractRole.COMPLETE_FRAGMENT):
        return Judgment("MALFORMED", ("DESCRIPTOR_COMPLETE_ROLE",))
    expected_summary = ModelCapabilitySummary(
        descriptor_identity, descriptor.service_role,
        descriptor.supported_judgments, descriptor.capability_class,
        descriptor.sound_fragment, descriptor.complete_fragment,
        descriptor.dependency_scope,
    )
    if model.capability_summaries != frozenset({expected_summary}):
        return Judgment("MALFORMED", ("MODEL_DESCRIPTOR_MISMATCH",))
    evidence = _resolve(composition, descriptor.required_evidence, ContractSpec)
    failure = _resolve(composition, descriptor.failure_contract, ContractSpec)
    if evidence is None or evidence.value.role is not ContractRole.REQUIRED_EVIDENCE or failure is None or failure.value.role is not ContractRole.SERVICE_FAILURE_BEHAVIOR:
        return Judgment("MALFORMED", ("DESCRIPTOR_EVIDENCE_OR_FAILURE",))
    expected_dependencies = frozenset({descriptor.service, *descriptor.supported_targets, descriptor.sound_fragment, descriptor.required_evidence, descriptor.failure_contract})
    if descriptor.complete_fragment is not None:
        expected_dependencies |= frozenset({descriptor.complete_fragment})
    if descriptor.proper_semantic_dependencies != expected_dependencies:
        return Judgment("MALFORMED", ("DESCRIPTOR_DEPENDENCY_PROJECTION",))
    if descriptor.dependency_closure != _reachable_closure(expected_dependencies, composition):
        return Judgment("MALFORMED", ("DESCRIPTOR_DEPENDENCY_CLOSURE",))
    if any(item.kind is not RecordKind.TRUST_ROOT for item in descriptor.required_trust_roots):
        return Judgment("MALFORMED", ("DESCRIPTOR_TRUST_ROOT_KIND",))
    if any(_resolve(composition, item) is None for item in descriptor.dependency_closure):
        return Judgment("MALFORMED", ("DESCRIPTOR_DANGLING_REFERENCE",))
    if target_binding.value.declaration not in descriptor.supported_targets:
        return Judgment("MALFORMED", ("DESCRIPTOR_TARGET",))
    return Judgment("WELL_FORMED")


def _proper_graph(bindings: tuple[RecordIdentity, ...], composition: Composition) -> dict[RecordIdentity, set[RecordIdentity]]:
    """Derive proper binding edges only from resolved ContractSpec queries.

    A fixture cannot create a semantic edge by filling a binding field.  The
    declaration/contract roots remain validation/closure data; only a query
    whose dependency resolves to another binding contributes a graph edge.
    """
    domain = set(bindings)
    graph: dict[RecordIdentity, set[RecordIdentity]] = {}
    for identity in bindings:
        record = _resolve(composition, identity, SemanticBinding)
        if record is None:
            raise ValueError("missing graph binding")
        meaning = _resolve(composition, record.value.meaning_contract, ContractSpec)
        if meaning is None or validate_contract_spec(meaning.value).tag != "WELL_FORMED":
            raise ValueError("missing or malformed binding ContractSpec")
        graph[identity] = {query.dependency for query in meaning.value.observation_queries if query.dependency in domain}
    return graph


def topological_order(bindings: tuple[RecordIdentity, ...], composition: Composition, preferred_order: tuple[RecordIdentity, ...] = ()) -> tuple[RecordIdentity, ...]:
    if len(bindings) != len(set(bindings)):
        raise ValueError("duplicate dependency node")
    remaining = _proper_graph(bindings, composition)
    preference = {node: index for index, node in enumerate(preferred_order)}
    order: list[RecordIdentity] = []
    while remaining:
        ready = [node for node, dependencies in remaining.items() if not dependencies]
        if not ready:
            raise ValueError("dependency cycle")
        ready.sort(key=lambda node: (preference.get(node, len(preference)), node))
        node = ready[0]
        order.append(node)
        del remaining[node]
        for dependencies in remaining.values():
            dependencies.discard(node)
    return tuple(order)


def validate_dependency_graph(bindings: tuple[RecordIdentity, ...], composition: Composition) -> Judgment:
    for identity in bindings:
        binding = _resolve(composition, identity, SemanticBinding)
        if binding is None:
            return Judgment("MALFORMED", ("missing graph binding", identity))
        status = validate_binding(binding.value, composition)
        if status.tag != "CLOSED":
            return Judgment("MALFORMED", ("binding support/closure mismatch", identity, status))
    try:
        topological_order(bindings, composition)
    except ValueError as error:
        return Judgment("MALFORMED", (str(error),))
    return Judgment("WELL_FORMED")


def _environment(request: InvocationRequest, composition: Composition) -> tuple[SemanticEnvironment, DependencyEnvironment] | None:
    semantic = _resolve(composition, request.semantic_environment, SemanticEnvironment)
    dependency = _resolve(composition, request.dependency_environment, DependencyEnvironment)
    if semantic is None or dependency is None:
        return None
    if semantic.value.abi_version != request.requested_version and semantic.value.abi_version.components != (0,):
        return None
    expected_syntax = frozenset(semantic.value.declarations + semantic.value.pair_declarations)
    expected_subjects = frozenset(semantic.value.bindings + semantic.value.profile_bindings + semantic.value.pair_bindings)
    expected_associations = frozenset(
        (declaration, binding)
        for declaration in semantic.value.declarations
        for binding in semantic.value.bindings
        if (bound := _resolve(composition, binding, SemanticBinding)) is not None
        and bound.value.declaration == declaration
    )
    if dependency.value.syntax_root_keys != expected_syntax:
        return None
    if dependency.value.subject_root_keys != expected_subjects:
        return None
    if dependency.value.binding_association_edges != expected_associations:
        return None
    if dependency.value.expanded_root_keys != expected_syntax | expected_subjects:
        return None
    proper = frozenset().union(*(
        record.value.proper_semantic_dependencies
        for identity in expected_subjects
        if (record := _resolve(composition, identity, SemanticBinding)) is not None
    ))
    closure = _reachable_closure(proper, composition)
    if dependency.value.proper_dependencies != proper or dependency.value.transitive_dependency_closure != closure:
        return None
    if any(_resolve(composition, item) is None for item in closure):
        return None
    return semantic.value, dependency.value


def _trust(request: InvocationRequest, descriptor: CapabilityDescriptor, composition: Composition) -> Judgment:
    environment_record = _resolve(composition, request.trust_environment, TrustEnvironment)
    if environment_record is None:
        return Judgment("MALFORMED_REQUEST", (request.trust_environment,))
    environment = environment_record.value
    if environment.discovery_failure is not None:
        return Judgment("DISCOVERY_FAILED", (environment.discovery_failure,))
    policy = _resolve(composition, environment.policy, TrustPolicyRecord)
    if policy is None or environment.policy_owner != policy.value.policy_owner:
        return Judgment("TRUST_ROOT_ABSENT")
    states = dict(environment.root_judgments)
    for required in descriptor.required_trust_roots:
        root_record = _resolve(composition, required, TrustRootRecord)
        if root_record is None or required not in environment.roots or required not in states:
            return Judgment("TRUST_ROOT_ABSENT", (required,))
        root = root_record.value
        if (root.owner != policy.value.policy_owner
                or RecordIdentity(RecordKind.CAPABILITY, descriptor.capability_key) not in root.trusted_validators
                or descriptor.service not in root.permitted_targets
                or root.adoption != "V0_EXTERNAL_TRUST_PREMISE"):
            return Judgment("TRUST_ROOT_INCOMPATIBLE", (required,))
        judgment = states[required]
        state = judgment.state
        if state is TrustState.ADMITTED and judgment.admitted_root != root:
            return Judgment("TRUST_ROOT_INCOMPATIBLE", (required,))
        if state is TrustState.UNDECIDED:
            return Judgment("TRUST_ROOT_UNDECIDED", (required,))
        if state is TrustState.ABSENT:
            return Judgment("TRUST_ROOT_ABSENT", (required,))
        if state is TrustState.FAILED:
            return Judgment("DISCOVERY_FAILED", (required, *judgment.reasons))
        if state is not TrustState.ADMITTED:
            return Judgment("TRUST_ROOT_INCOMPATIBLE", (required,))
    return Judgment("TRUST_ROOT_ADMITTED")


def evaluate_invocation(request_identity: RecordIdentity, composition: Composition) -> ContractReplay:
    request_record = _resolve(composition, request_identity, InvocationRequest)
    if request_record is None:
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, "MALFORMED_REQUEST", None)
    request = request_record.value
    environment_pair = _environment(request, composition)
    if environment_pair is None:
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, "MALFORMED_REQUEST", None)
    environment, _ = environment_pair
    if request.target not in environment.declarations or _resolve(composition, request.target, DeclarationShape) is None:
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, "DECLARATION_ABSENT", None)
    binding_records = tuple(_resolve(composition, identity, SemanticBinding) for identity in environment.bindings)
    binding_record = next((item for item in binding_records if item is not None and item.value.declaration == request.target), None)
    if binding_record is None:
        return ContractReplay(Formation.WELL_FORMED, Closure.OPEN_BINDINGS, Evaluability.UNKNOWN, "BINDING_ABSENT", None)
    binding_status = validate_binding(binding_record.value, composition)
    if binding_status.tag != "CLOSED":
        formation = Formation.MALFORMED if binding_status.tag == "MALFORMED" else Formation.WELL_FORMED
        closure = Closure.NOT_APPLICABLE if formation is Formation.MALFORMED else Closure.OPEN_BINDINGS
        return ContractReplay(formation, closure, Evaluability.UNKNOWN, binding_status.tag, None)
    models = tuple(record for record in composition.records if isinstance(record.value, ModelContract) and record.value.target_binding == binding_record.identity and record.value.semantic_contract == binding_record.value.meaning_contract)
    if len(models) != 1:
        return ContractReplay(Formation.WELL_FORMED, Closure.OPEN_BINDINGS, Evaluability.UNKNOWN, "MODEL_CONTRACT_ABSENT", None)
    model = models[0].value
    if not exact_version_agreement(request.requested_version, model.exact_version):
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, "VERSION_MISMATCH", None)
    summary_keys = frozenset(summary.capability_key for summary in model.capability_summaries)
    descriptors = tuple(record for record in composition.records if isinstance(record.value, CapabilityDescriptor) and record.identity in summary_keys)
    if len(descriptors) != 1:
        return ContractReplay(Formation.WELL_FORMED, Closure.CLOSED, Evaluability.MISSING, "CAPABILITY_ABSENT", None)
    descriptor = descriptors[0].value
    validated = validate_model_descriptor(model, descriptor, composition)
    if validated.tag != "WELL_FORMED":
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, validated.details[0], None)
    trust = _trust(request, descriptor, composition)
    if trust.tag == "MALFORMED_REQUEST":
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, "MALFORMED_REQUEST", None)
    if trust.tag == "DISCOVERY_FAILED":
        return ContractReplay(Formation.WELL_FORMED, Closure.CLOSED, Evaluability.UNKNOWN, "DISCOVERY_FAILED", None)
    if trust.tag == "TRUST_ROOT_UNDECIDED":
        return ContractReplay(Formation.WELL_FORMED, Closure.CLOSED, Evaluability.UNKNOWN, "TRUST_ROOT_UNDECIDED", None)
    if trust.tag in {"TRUST_ROOT_ABSENT", "TRUST_ROOT_INCOMPATIBLE"}:
        return ContractReplay(Formation.WELL_FORMED, Closure.CLOSED, Evaluability.MISSING, trust.tag, None)
    meaning = _resolve(composition, binding_record.value.meaning_contract, ContractSpec)
    if meaning is None:
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, "MEANING_CONTRACT_ABSENT", None)
    if len(request.arguments) != len(meaning.value.primary_input_domain):
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, "ARGUMENT_ARITY", None)
    from . import coding_plugin
    relations = {
        "task_accepts": coding_plugin.task_accepts,
        "verification_passed": coding_plugin.verification_passed,
        "observations_equal": coding_plugin.observations_equal,
        "dependency_metadata_changed": coding_plugin.dependency_metadata_changed,
        "event_matches": coding_plugin.event_matches,
        "event_occurred": coding_plugin.event_occurred,
        "refresh_scope": coding_plugin.refresh_scope,
    }
    relation = relations.get(meaning.value.relation_name)
    if relation is None:
        raise FiniteProfileError(f"unsupported resolved ContractSpec relation: {meaning.value.relation_name}")
    result = relation(*request.arguments)
    result_records = tuple(
        record.value for record in composition.records
        if isinstance(record.value, ResultRecord) and record.value.request == request_identity
    )
    if len(result_records) != 1:
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, "RESULT_PROTOCOL", None)
    authoritative = result_records[0]
    if authoritative.result_kind != type(result).__name__ or authoritative.result != result:
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, "SEMANTIC_RESULT_MISMATCH", None)
    return ContractReplay(Formation.WELL_FORMED, Closure.CLOSED, Evaluability.AVAILABLE, f"INVOCABLE_FOR({request_identity.key.local})", result)


def _producer_set(subject: RecordIdentity, composition: Composition) -> frozenset[str]:
    return frozenset(record.value.producer for record in composition.records if isinstance(record.value, ProducerRecord) and record.value.subject == subject)


def validate_pair(request_identity: RecordIdentity, composition: Composition) -> PairValidationResult | Judgment:
    request_record = _resolve(composition, request_identity, PairRequestData)
    if request_record is None:
        return Judgment("MALFORMED_REQUEST")
    request = request_record.value
    binding_record = _resolve(composition, request.pair_binding, PairBinding)
    trust_record = _resolve(composition, request.trust_environment, TrustEnvironment)
    environment_record = _resolve(composition, request.semantic_environment, SemanticEnvironment)
    dependencies_record = _resolve(composition, request.complete_dependencies, DependencyEnvironment)
    capability_record = _resolve(composition, request.capability_key, CapabilityDescriptor)
    if any(item is None for item in (binding_record, trust_record, environment_record, dependencies_record, capability_record)):
        return Judgment("MALFORMED", ("PAIR_REQUEST_CARRIER",))
    if request.abi_version.components != (0,) or request.capability_target.kind is not RecordKind.PAIR_DECLARATION:
        return Judgment("MALFORMED", ("PAIR_REQUEST_ABI_OR_TARGET",))
    binding = binding_record.value
    declaration_identity = RecordIdentity(RecordKind.PAIR_DECLARATION, binding.pair_key)
    declaration_record = _resolve(composition, declaration_identity, PairDeclaration)
    scope_record = _resolve(composition, binding.scope_binding_key, SemanticBinding)
    bundle_record = _resolve(composition, binding.occurrence_bundle, OccurrenceSemanticContractBundle)
    occurrence_model = _resolve(composition, binding.occurrence_model_contract_key, ModelContract)
    certificate_record = _resolve(composition, binding.certificate, CertificateEnvelope)
    if any(item is None for item in (declaration_record, scope_record, bundle_record, occurrence_model, certificate_record)):
        return Judgment("OPEN_BINDINGS")
    if (request.capability_target != declaration_identity
            or binding.scope_binding_key not in environment_record.value.bindings
            or request.pair_binding not in environment_record.value.pair_bindings
            or declaration_identity not in environment_record.value.pair_declarations):
        return Judgment("MALFORMED", ("PAIR_ENVIRONMENT_MEMBERSHIP",))
    if binding.validation_references != frozenset({binding.certificate, binding.validator}):
        return Judgment("MALFORMED", ("VALIDATION_REFERENCE_MISMATCH",))
    if dependencies_record.value.validation_references != binding.validation_references:
        return Judgment("MALFORMED", ("PAIR_DEPENDENCY_VALIDATION_REFERENCES",))
    if binding.validation_references & (binding.proper_semantic_dependencies | binding.dependency_closure):
        return Judgment("MALFORMED", ("VALIDATION_REFERENCE_IN_PROPER_DAG",))
    expected_pair_proper = frozenset({declaration_identity, binding.scope_binding_key,
                                      binding.occurrence_bundle,
                                      binding.occurrence_model_contract_key})
    if binding.proper_semantic_dependencies != expected_pair_proper:
        return Judgment("MALFORMED", ("PAIR_PROPER_DEPENDENCIES",))
    if binding.dependency_closure != _reachable_closure(expected_pair_proper, composition):
        return Judgment("MALFORMED", ("PAIR_DEPENDENCY_CLOSURE",))
    if validate_binding(scope_record.value, composition).tag != "CLOSED":
        return Judgment("MALFORMED", ("PAIR_SCOPE_BINDING",))
    bundle = bundle_record.value
    bundle_fields = (
        (bundle.meaning_contract, ContractRole.PREDICATE_MEANING),
        (bundle.evidence_schema, ContractRole.EVIDENCE_SCHEMA),
        (bundle.access_boundary, ContractRole.ACCESS_BOUNDARY),
        (bundle.unknown_contract, ContractRole.UNKNOWN_BEHAVIOR),
        (bundle.evaluation_error_contract, ContractRole.EVALUATION_ERROR_BEHAVIOR),
    )
    resolved_bundle = tuple((_resolve(composition, key, ContractSpec), role) for key, role in bundle_fields)
    occurrence_declarations = tuple(
        record for record in composition.records
        if isinstance(record.value, DeclarationShape)
        and record.value.symbol_key == declaration_record.value.occurrence_symbol
    )
    expected_bundle_proper = (
        frozenset(key for key, _ in bundle_fields)
        | resolved_bundle[0][0].value.support
        | frozenset({occurrence_declarations[0].identity})
        if resolved_bundle[0][0] is not None and len(occurrence_declarations) == 1
        else frozenset()
    )
    if (any(record is None or record.value.owner_layer is not Layer.SIGMA or record.value.role is not role for record, role in resolved_bundle)
            or bundle.permitted_facet_inputs != (frozenset({"trace"}),)
            or bundle.determinism_rule != "SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT"
            or bundle.proper_semantic_dependencies != expected_bundle_proper
            or bundle.dependency_closure != _reachable_closure(expected_bundle_proper, composition)):
        return Judgment("MALFORMED", ("PAIR_OCCURRENCE_BUNDLE",))
    model = occurrence_model.value
    expected_pair_summary = ModelCapabilitySummary(
        binding.validator, capability_record.value.service_role,
        capability_record.value.supported_judgments,
        capability_record.value.capability_class,
        capability_record.value.sound_fragment,
        capability_record.value.complete_fragment,
        capability_record.value.dependency_scope,
    )
    if (model.target_binding != binding.occurrence_bundle
            or model.semantic_contract != bundle.meaning_contract
            or model.evidence_contract != bundle.evidence_schema
            or model.unknown_contract != bundle.unknown_contract
            or model.error_contract != bundle.evaluation_error_contract
            or model.capability_summaries != frozenset({expected_pair_summary})):
        return Judgment("MALFORMED", ("PAIR_OCCURRENCE_MODEL",))
    capability = capability_record.value
    service = _resolve(composition, capability.service, ServiceIdentity)
    required_specs = (
        (capability.sound_fragment, ContractRole.SOUND_FRAGMENT),
        (capability.complete_fragment, ContractRole.COMPLETE_FRAGMENT),
        (capability.required_evidence, ContractRole.REQUIRED_EVIDENCE),
        (capability.failure_contract, ContractRole.SERVICE_FAILURE_BEHAVIOR),
    )
    if (service is None or service.value.abi_version != request.abi_version
            or service.value.plugin_key != capability.plugin_key
            or capability.service_role != "PAIR_VALIDATION"
            or capability.capability_class != "COMPLETE_FOR_DECLARED_FRAGMENT"
            or capability.supported_judgments != frozenset({"PAIR_VALIDATION"})
            or capability.supported_targets != frozenset({declaration_identity})
            or any(key is None or (spec := _resolve(composition, key, ContractSpec)) is None or spec.value.role is not role for key, role in required_specs)):
        return Judgment("MALFORMED", ("PAIR_CAPABILITY",))
    envelope = certificate_record.value
    proof_record = _resolve(composition, envelope.payload, PairFullEvalProof)
    evidence_records = tuple(_resolve(composition, item, EvidenceRecord) for item in envelope.evidence_refs)
    if (envelope.request_binding != request_identity
            or envelope.subjects != (declaration_identity, binding.occurrence_bundle)
            or envelope.environment != request.semantic_environment
            or envelope.capability_key != request.capability_key
            or envelope.fragment != capability.sound_fragment
            or envelope.dependencies != request.complete_dependencies
            or envelope.claimed_conclusion != "PAIR_COHERENCE_ADMITTED"
            or envelope.validator_key != binding.validator
            or envelope.certificate_kind != "EVENT_PAIR_COHERENCE_PROOF"
            or envelope.abstraction_class != "SYMBOLIC"
            or proof_record is None or len(evidence_records) != 1 or evidence_records[0] is None
            or evidence_records[0].value.schema_contract != capability.sound_fragment):
        return Judgment("MALFORMED", ("PAIR_CERTIFICATE_ENVELOPE",))
    proof = proof_record.value
    if (proof.pair_key != binding.pair_key or proof.bundle != binding.occurrence_bundle
            or proof.reference_contract != bundle.meaning_contract
            or proof.trace_domain != "ALL_ADMITTED_TRACES"
            or proof.compared_fields != "COMPLETE_EVAL_RECORD"):
        return Judgment("MALFORMED", ("PAIR_FULL_EVAL_PROOF",))
    trust = trust_record.value
    policy_record = _resolve(composition, trust.policy, TrustPolicyRecord)
    if policy_record is None or any(_resolve(composition, root, TrustRootRecord) is None for root in trust.roots):
        return Judgment("MALFORMED", ("PAIR_TRUST_CHAIN",))
    root_states = dict(trust.root_judgments)
    for root_identity in trust.roots:
        root_record = _resolve(composition, root_identity, TrustRootRecord)
        assert root_record is not None
        judgment = root_states.get(root_identity)
        if judgment is None or judgment.state is not TrustState.ADMITTED:
            return Judgment("INCOMPATIBLE", ("PAIR_TRUST_NOT_ADMITTED", root_identity))
        if (judgment.admitted_root != root_record.value
                or root_record.value.owner != policy_record.value.policy_owner
                or binding.validator not in root_record.value.trusted_validators
                or envelope.certificate_kind not in root_record.value.permitted_certificate_kinds
                or declaration_identity not in root_record.value.permitted_targets
                or capability.service not in root_record.value.permitted_targets):
            return Judgment("INCOMPATIBLE", ("PAIR_TRUST_SCOPE", root_identity))
    subjects = (declaration_identity, binding.certificate, binding.validator)
    producer_sets = tuple(_producer_set(subject, composition) for subject in subjects)
    trust_producers = _producer_set(request_record.value.trust_environment, composition) | _producer_set(trust.policy, composition)
    for root in trust.roots:
        trust_producers |= _producer_set(root, composition)
    producer_sets = producer_sets + (trust_producers,)
    if any(not producers for producers in producer_sets):
        return Judgment("MALFORMED", ("INCOMPLETE_PRODUCER_SET",))
    if _producer_set(declaration_identity, composition) != frozenset({declaration_record.value.pair_key.owner}):
        return Judgment("MALFORMED", ("PAIR_SUBJECT_PRODUCER",))
    for index, producers in enumerate(producer_sets):
        if any(producers & other for other in producer_sets[index + 1:]):
            return Judgment("MALFORMED", ("PAIR_SELF_TRUST",))
    return PairValidationResult(declaration_record.value.pair_key, envelope.certificate_key, envelope.claimed_conclusion)


def evaluate_observation_graph(request: GraphEvaluationRequest, composition: Composition) -> ObservationEvaluation:
    from .coding_plugin import changes_between, observe
    reasoning = _resolve(composition, request.reasoning_request, ReasoningRequest)
    trust = _resolve(composition, request.trust_environment, TrustEnvironment)
    semantic = _resolve(composition, request.semantic_environment, SemanticEnvironment)
    dependencies = _resolve(composition, request.dependency_environment, DependencyEnvironment)
    authoritative_observations = _resolve(composition, request.observation_environment, ObservationEnvironment)
    authoritative_result = _resolve(composition, request.result_record, ResultRecord)
    lifecycle = _resolve(composition, request.lifecycle_record, LifecycleRecord)
    status = _resolve(composition, request.status_record, OutcomeRecord)
    if any(item is None for item in (reasoning, trust, semantic, dependencies,
                                     authoritative_observations,
                                     authoritative_result, lifecycle, status)):
        raise ValueError("confluence carrier absent or wrong-kind")
    rr = reasoning.value
    if (rr.abi_version.components != (0,) or rr.judgment != "CONSISTENCY"
            or rr.subjects != ("C_c",)
            or rr.semantic_environment != request.semantic_environment
            or rr.trust_environment != request.trust_environment
            or rr.complete_dependencies != request.dependency_environment):
        raise ValueError("malformed confluence reasoning request")
    capability = _resolve(composition, rr.capability_key, CapabilityDescriptor)
    fragment = _resolve(composition, rr.required_fragment, ContractSpec)
    if (capability is None or fragment is None
            or capability.value.service_role != "REASONING"
            or capability.value.capability_class != "PARTIAL_SYMBOLIC_REASONING"
            or capability.value.supported_judgments != frozenset({"CONSISTENCY"})
            or capability.value.supported_targets != frozenset({rr.capability_target})
            or capability.value.sound_fragment != rr.required_fragment
            or fragment.value.role is not ContractRole.SOUND_FRAGMENT
            or fragment.value.support != frozenset(request.nodes)):
        raise ValueError("malformed confluence capability/fragment")
    if (semantic.value.bindings != tuple(
            record.identity for record in composition.records
            if isinstance(record.value, SemanticBinding)
            and record.identity.key.namespace == "confluence.binding")
            and frozenset(semantic.value.bindings) != frozenset(
                record.identity for record in composition.records
                if isinstance(record.value, SemanticBinding)
                and record.identity.key.namespace == "confluence.binding")):
        raise ValueError("malformed confluence semantic environment")
    if (dependencies.value.subject_root_keys != frozenset(semantic.value.bindings)
            or dependencies.value.validation_references):
        raise ValueError("malformed confluence dependency environment")
    policy = _resolve(composition, trust.value.policy, TrustPolicyRecord)
    if policy is None or len(trust.value.roots) != 1:
        raise ValueError("malformed confluence trust environment")
    root = _resolve(composition, trust.value.roots[0], TrustRootRecord)
    root_judgment = None if root is None else dict(trust.value.root_judgments).get(root.identity)
    if (root is None or root_judgment is None
            or root_judgment.state is not TrustState.ADMITTED
            or root_judgment.admitted_root != root.value
            or rr.capability_key not in root.value.trusted_validators
            or rr.capability_target not in root.value.permitted_targets):
        raise ValueError("confluence trust not admitted")
    nodes: dict[RecordIdentity, ObservationNode] = {}
    bindings: dict[RecordIdentity, SemanticBinding] = {}
    for identity in request.nodes:
        node = _resolve(composition, identity, ObservationNode)
        if node is None:
            raise ValueError("observation graph has an absent or wrong-kind node")
        nodes[identity] = node.value
        binding = next((record.value for record in composition.records if isinstance(record.value, SemanticBinding) and record.value.meaning_contract == node.value.contract_spec), None)
        if binding is None:
            raise ValueError("observation node has no semantic binding")
        bindings[identity] = binding
    graph: dict[RecordIdentity, set[RecordIdentity]] = {}
    for identity, node in nodes.items():
        spec_record = _resolve(composition, node.contract_spec, ContractSpec)
        if spec_record is None or validate_contract_spec(spec_record.value).tag != "WELL_FORMED":
            raise ValueError("observation node has malformed ContractSpec")
        graph[identity] = {query.dependency for query in spec_record.value.observation_queries if query.dependency in nodes}
    # Topological order is computed from the ContractSpec query maps above.
    remaining = {key: set(value) for key, value in graph.items()}
    preference = {node: index for index, node in enumerate(request.preferred_order)}
    ordered: list[RecordIdentity] = []
    while remaining:
        ready = [node for node, dependencies in remaining.items() if not dependencies]
        if not ready:
            raise ValueError("dependency cycle")
        ready.sort(key=lambda node: (preference.get(node, len(preference)), node))
        node = ready[0]
        ordered.append(node)
        del remaining[node]
        for dependencies in remaining.values():
            dependencies.discard(node)
    order = tuple(ordered)
    observations: dict[RecordIdentity, Any] = {}
    for identity in order:
        node = nodes[identity]
        value = observe(*node.arguments) if node.operation is NodeOperation.OBSERVE else changes_between(*node.arguments)
        observations[identity] = value
    complete = tuple(sorted(observations.items()))
    if authoritative_observations.value.values != complete:
        raise ValueError("confluence observation environment mismatch")
    if (authoritative_result.value.request != request.reasoning_request
            or authoritative_result.value.result_kind != "ReasoningResult"
            or authoritative_result.value.result != "COMPLETED_INCONCLUSIVE"):
        raise ValueError("confluence result mismatch")
    if (lifecycle.value.request != request.reasoning_request
            or lifecycle.value.judgment != "COMPLETED(Y_c)"):
        raise ValueError("confluence lifecycle mismatch")
    expected_status_refs = frozenset({request.observation_environment,
                                      request.result_record,
                                      request.lifecycle_record})
    if (status.value.outcome_kind != "CONFLUENCE_STATUS"
            or status.value.references != expected_status_refs
            or status.value.value != ("WELL_FORMED", "CLOSED",
                                      "EVALUABILITY_AVAILABLE",
                                      "CONSISTENCY_UNKNOWN")):
        raise ValueError("confluence status mismatch")
    return ObservationEvaluation(complete, Judgment("COMPLETED_INCONCLUSIVE"), "COMPLETED", ("WELL_FORMED", "CLOSED", "EVALUABILITY_AVAILABLE", "COMPLETED", "CONSISTENCY_UNKNOWN"))


def project_interface_failure(failure: InterfaceFailure) -> Judgment:
    if not failure.reasons:
        return Judgment("MALFORMED_RESULT", ("EMPTY_FAILURE_REASONS",))
    tags = {
        FailureDomain.FUNCTION_EVALUATION: "TERM_ERROR",
        FailureDomain.PREDICATE_EVALUATION: "EVAL_ERROR",
        FailureDomain.PROFILE_CONCRETE: "PROFILE_EVALUATION_ERROR",
        FailureDomain.REASONING: "REASONING_ERROR",
    }
    return Judgment(tags[failure.domain], (failure.kind, failure.reasons))


# Exact closed K3-S §9.4 resolution coordinates.  These are semantic
# identities, not packet tags, answer values, or a relation-to-status table.
_FINITE_RESOLUTION_COORDINATES = frozenset({
    ("FORMATION_RECORD", "ABI_RECORD", "ABI0", "coding-minimal", None),
    ("FORMATION_RECORD", "PACKAGE_RECORD", "coding-minimal", "ABI0", None),
    ("FORMATION_RECORD", "DECLARATION_RECORD", "DP(task_accepts)", "coding-minimal", None),
    ("FORMATION_RECORD", "EVENT_DECLARATION_RECORD", "DE(dependency_refresh)", "coding-minimal", None),
    ("FORMATION_RECORD", "PAIR_DECLARATION_RECORD", "PAIR(refresh)", "coding-minimal", None),
    ("FORMATION_RECORD", "OUTCOME_RECORD", "O_w", "ABI0", None),
    ("BINDING_MEMBER", "BINDING_RECORD", "BINDING(DP(task_accepts))", "coding-minimal", None),
    ("BINDING_MEMBER", "PROFILE_BINDING_RECORD", "PROFILE_BINDING(PK(implementation_evidence))", "coding-minimal", None),
    ("BINDING_MEMBER", "PAIR_BINDING_RECORD", "PB_alt", "coding-minimal", None),
    ("AUTHORITY_MEMBER", "AUTHORITY_FACT_RECORD", "AF(choice,1)", "E_choice", None),
    ("CHOICE_MEMBER", "CHOICE_BINDING_RECORD", "cb0", "E_choice", None),
    ("LEXICAL_MEMBER", "LEXICAL_BINDING_RECORD", "lk0", "E_lex", None),
    ("EXTRANEOUS_LEXICAL", "REQUEST_RECORD", "Q_t[ADMITTED]", "E_t_extra", None),
    ("SERVICE_DISCOVERY", "SERVICE_RECORD", "SK(predicates)", "Q_t[ADMITTED]", None),
    ("SERVICE_DISCOVERY", "CAPABILITY_RECORD", "CAP(predicates)", "Q_t[ADMITTED]", None),
    ("TRUST_POLICY", "TRUST_POLICY_RECORD", "TP", "T_admitted", None),
    ("TRUST_ROOT", "TRUST_ROOT_RECORD", "TR", "T_admitted", None),
    ("CERTIFICATE_ADMISSION", "CERTIFICATE_RECORD", "PCERT", "R_p", None),
    ("MIGRATION", "MIGRATION_RECORD", "MK0", "CCK0", None),
    ("COMPATIBILITY", "COMPATIBILITY_RECORD", "CCK0", "XK1", None),
    ("OPTIONAL_EXTENSION", "SEMANTIC_EXTENSION_RECORD", "XK0", "AK0", None),
    ("REQUIRED_EXTENSION", "SEMANTIC_EXTENSION_RECORD", "XK1", "AK1", None),
    ("MODEL_BINDING", "MODEL_CONTRACT_RECORD", "MODEL_task_accepts", "coding-minimal", None),
    ("OPTIONAL_ALIAS", "ALIAS_RECORD", "AK0", "XK0", None),
    ("REQUIRED_ALIAS", "ALIAS_RECORD", "AK1", "XK1", None),
    ("SIGMA_CONTRACT", "CONTRACT_SPEC_RECORD", "CS(PREDICATE_MEANING,task_accepts)", "BINDING(DP(task_accepts))", None),
    ("SERVICE_CONTRACT", "CONTRACT_SPEC_RECORD", "QSOUND", "CAP(predicates)", None),
    ("REQUEST_RECORD", "REQUEST_RECORD", "Q_t[ADMITTED]", "RES_t[ADMITTED]", None),
    ("RESULT_PROTOCOL", "RESULT_RECORD", "RES_t[ADMITTED]", "Q_t[ADMITTED]", None),
    ("REQUEST_ENVIRONMENT", "SEMANTIC_ENVIRONMENT_RECORD", "E_t", "Q_t[ADMITTED]", None),
    ("REQUEST_ENVIRONMENT", "TRUST_ENVIRONMENT_RECORD", "T_admitted", "Q_t[ADMITTED]", None),
    ("REQUEST_ENVIRONMENT", "DEPENDENCY_ENVIRONMENT_RECORD", "D_t", "Q_t[ADMITTED]", None),
    ("OBSERVATION_RESULT", "OBSERVATION_ENVIRONMENT_RECORD", "M_c", "Y_c", None),
    ("LIFECYCLE_TRANSITION", "LIFECYCLE_RECORD", "L_c_final", None, "L_life_after"),
    ("FORMATION_RECORD", "EVENT_VALUE_RECORD", "ev0", "ABI0", None),
    ("FORMATION_RECORD", "TRACE_EVENT_RECORD", "te0", "ABI0", None),
    ("FORMATION_RECORD", "SOURCE_RECORD", "SRC(choice,1)", "ABI0", None),
    ("FORMATION_RECORD", "AUTHORITY_REF_RECORD", "AUTH(choice,1)", "ABI0", None),
    ("EVIDENCE_TRUTH", "EVIDENCE_RECORD", "e0", "t_t_evidence_subject", None),
    ("REASON_CARRIER", "REASON_RECORD", "u0", "VALUE(UNKNOWN)", None),
    ("CONFLICT_REPLACEMENT", "CONFLICT_RECORD", "conflict0", None, "conflict1"),
})


def _resolve_failed_coordinate(
    target: RecordIdentity,
    coordinate: ResolutionCoordinate,
    composition: Composition,
) -> Judgment:
    """Project the failed K2 coordinate after checking its real consumer.

    The coordinate is a typed resolution obligation.  It contains no status,
    truth, lifecycle, trust state, or fixture tag.  Unsupported combinations
    fail before a semantic judgment is returned.
    """

    signature = (
        coordinate.relation.value,
        target.kind.value,
        target.key.local,
        None if coordinate.consumer is None else coordinate.consumer.key.local,
        None if coordinate.replacement is None else coordinate.replacement.key.local,
    )
    if signature not in _FINITE_RESOLUTION_COORDINATES:
        raise FiniteProfileError("unsupported missing coordinate outside K3-S §9.4")
    consumer = None if coordinate.consumer is None else composition.at(coordinate.consumer)
    replacement = None if coordinate.replacement is None else composition.at(coordinate.replacement)
    consumer_value = None if consumer is None else consumer.value
    replacement_value = None if replacement is None else replacement.value
    relation = coordinate.relation

    if coordinate.consumer is not None and consumer is None:
        raise FiniteProfileError("unsupported missing coordinate: absent consumer")
    if coordinate.replacement is not None and replacement is None:
        raise FiniteProfileError("unsupported missing coordinate: absent replacement")

    if relation is ResolutionRelation.FORMATION_RECORD:
        formation_kinds = {
            RecordKind.ABI, RecordKind.PACKAGE, RecordKind.DECLARATION,
            RecordKind.EVENT, RecordKind.PAIR_DECLARATION, RecordKind.OUTCOME,
            RecordKind.EVENT_VALUE, RecordKind.TRACE_EVENT, RecordKind.SOURCE,
            RecordKind.AUTHORITY_REF,
        }
        if target.kind not in formation_kinds or consumer is None:
            raise FiniteProfileError("unsupported formation-record coordinate")
        if target.kind is RecordKind.ABI:
            if not isinstance(consumer_value, PluginPackage) or consumer_value.abi_version != target.key.version:
                raise FiniteProfileError("ABI coordinate is not induced by its package")
        elif target.kind is RecordKind.PACKAGE:
            if not isinstance(consumer_value, AbiRecord):
                raise FiniteProfileError("package coordinate is not induced by its ABI")
        elif target.kind in {RecordKind.DECLARATION, RecordKind.EVENT, RecordKind.PAIR_DECLARATION}:
            if not isinstance(consumer_value, PluginPackage) or consumer_value.plugin_key.owner != target.key.owner:
                raise FiniteProfileError("declaration coordinate is not induced by its package")
        return Judgment("MALFORMED")

    if relation is ResolutionRelation.BINDING_MEMBER:
        if target.kind not in {RecordKind.BINDING, RecordKind.PROFILE_BINDING, RecordKind.PAIR_BINDING} or not isinstance(consumer_value, (PluginPackage, SemanticEnvironment)):
            raise FiniteProfileError("unsupported binding-member coordinate")
        return Judgment("OPEN_BINDINGS")
    if relation in {ResolutionRelation.AUTHORITY_MEMBER, ResolutionRelation.CHOICE_MEMBER, ResolutionRelation.LEXICAL_MEMBER}:
        permitted = {
            ResolutionRelation.AUTHORITY_MEMBER: {RecordKind.AUTHORITY_FACT},
            ResolutionRelation.CHOICE_MEMBER: {RecordKind.CHOICE_BINDING},
            ResolutionRelation.LEXICAL_MEMBER: {RecordKind.LEXICAL_BINDING},
        }[relation]
        if target.kind not in permitted or not isinstance(consumer_value, SemanticEnvironment):
            raise FiniteProfileError("unsupported semantic-environment membership coordinate")
        return Judgment("OPEN_BINDINGS", (target,))
    if relation is ResolutionRelation.EXTRANEOUS_LEXICAL:
        if target.kind is not RecordKind.REQUEST or not isinstance(consumer_value, SemanticEnvironment) or not consumer_value.lexical_bindings:
            raise FiniteProfileError("unsupported extraneous-lexical coordinate")
        return Judgment("MALFORMED_REQUEST", ("EXTRANEOUS_LEXICAL_BINDING", consumer_value.lexical_bindings[-1]))
    if relation is ResolutionRelation.SERVICE_DISCOVERY:
        if target.kind not in {RecordKind.SERVICE, RecordKind.CAPABILITY} or not isinstance(consumer_value, InvocationRequest):
            raise FiniteProfileError("unsupported service-discovery coordinate")
        return Judgment("EVALUABILITY_MISSING")
    if relation is ResolutionRelation.TRUST_POLICY:
        if target.kind is not RecordKind.TRUST_POLICY or not isinstance(consumer_value, TrustEnvironment):
            raise FiniteProfileError("unsupported trust-policy coordinate")
        return Judgment("TRUST_ROOT_ABSENT")
    if relation is ResolutionRelation.TRUST_ROOT:
        if target.kind is not RecordKind.TRUST_ROOT or not isinstance(consumer_value, TrustEnvironment):
            raise FiniteProfileError("unsupported trust-root coordinate")
        return Judgment("TRUST_ROOT_ABSENT", (target,))
    if relation is ResolutionRelation.CERTIFICATE_ADMISSION:
        if target.kind is not RecordKind.CERTIFICATE or not isinstance(consumer_value, PairRequestData):
            raise FiniteProfileError("unsupported certificate-admission coordinate")
        pair_binding = _resolve(composition, consumer_value.pair_binding, PairBinding)
        if pair_binding is None or pair_binding.value.certificate != target:
            raise FiniteProfileError("certificate coordinate is not induced by its pair binding")
        return Judgment("NO_CERTIFICATE_ADMISSION", ("CONSISTENCY_UNKNOWN",))
    if relation is ResolutionRelation.MIGRATION:
        if target.kind is not RecordKind.MIGRATION or not isinstance(consumer_value, EvolutionRecord):
            raise FiniteProfileError("unsupported migration coordinate")
        return Judgment("NO_MIGRATION", (target.key.local,))
    if relation is ResolutionRelation.COMPATIBILITY:
        if target.kind is not RecordKind.COMPATIBILITY_CLAIM or not isinstance(consumer_value, EvolutionRecord):
            raise FiniteProfileError("unsupported compatibility coordinate")
        return Judgment("NO_COMPATIBILITY", (target.key.local,))
    if relation in {ResolutionRelation.OPTIONAL_EXTENSION, ResolutionRelation.REQUIRED_EXTENSION}:
        required = relation is ResolutionRelation.REQUIRED_EXTENSION
        if target.kind is not RecordKind.SEMANTIC_EXTENSION or not isinstance(consumer_value, EvolutionRecord) or consumer_value.required is not required:
            raise FiniteProfileError("unsupported extension coordinate")
        return Judgment("INCOMPATIBLE" if required else "NO_EFFECT", (target.key.local,))
    if relation is ResolutionRelation.MODEL_BINDING:
        if target.kind is not RecordKind.MODEL_CONTRACT or not isinstance(consumer_value, PluginPackage):
            raise FiniteProfileError("unsupported model-binding coordinate")
        return Judgment("OPEN_BINDINGS", ("MODEL_CONTRACT",))
    if relation in {ResolutionRelation.OPTIONAL_ALIAS, ResolutionRelation.REQUIRED_ALIAS}:
        required = relation is ResolutionRelation.REQUIRED_ALIAS
        if target.kind is not RecordKind.ALIAS or not isinstance(consumer_value, EvolutionRecord) or consumer_value.required is not required:
            raise FiniteProfileError("unsupported alias coordinate")
        if required:
            return Judgment("MALFORMED", ("MISSING_ALIAS", target.key.local))
        return Judgment("NO_ALIAS", (target.key.local,))
    if relation is ResolutionRelation.SIGMA_CONTRACT:
        if target.kind is not RecordKind.CONTRACT_SPEC or not isinstance(consumer_value, SemanticBinding):
            raise FiniteProfileError("unsupported Sigma-contract coordinate")
        return Judgment("BINDING_INCOMPATIBLE", ("OPEN_BINDINGS",))
    if relation is ResolutionRelation.SERVICE_CONTRACT:
        if target.kind is not RecordKind.CONTRACT_SPEC or not isinstance(consumer_value, CapabilityDescriptor):
            raise FiniteProfileError("unsupported Service-contract coordinate")
        return Judgment("CAPABILITY_INCOMPATIBLE", ("EVALUABILITY_MISSING",))
    if relation is ResolutionRelation.REQUEST_RECORD:
        if target.kind is not RecordKind.REQUEST or not isinstance(consumer_value, ResultRecord):
            raise FiniteProfileError("unsupported request-record coordinate")
        return Judgment("MALFORMED_REQUEST")
    if relation is ResolutionRelation.RESULT_PROTOCOL:
        if target.kind is not RecordKind.RESULT or not isinstance(consumer_value, InvocationRequest):
            raise FiniteProfileError("unsupported result-protocol coordinate")
        return Judgment("INVOCATION_FAILED", ("PROTOCOL", "NO_RESULT", "NO_TRUTH"))
    if relation is ResolutionRelation.REQUEST_ENVIRONMENT:
        if target.kind not in {RecordKind.SEMANTIC_ENVIRONMENT, RecordKind.TRUST_ENVIRONMENT, RecordKind.DEPENDENCY_ENVIRONMENT} or not isinstance(consumer_value, InvocationRequest):
            raise FiniteProfileError("unsupported request-environment coordinate")
        return Judgment("MALFORMED_REQUEST", (consumer.identity,))
    if relation is ResolutionRelation.OBSERVATION_RESULT:
        if target.kind is not RecordKind.OBSERVATION_ENVIRONMENT or not isinstance(consumer_value, ResultRecord):
            raise FiniteProfileError("unsupported observation-result coordinate")
        return Judgment("MALFORMED_RESULT", ("SEMANTIC_MISMATCH",))
    if relation is ResolutionRelation.LIFECYCLE_TRANSITION:
        if target.kind is not RecordKind.LIFECYCLE or not isinstance(replacement_value, LifecycleRecord):
            raise FiniteProfileError("unsupported lifecycle-transition coordinate")
        return Judgment("LIFECYCLE_REPLACED", (replacement.identity, "INVOCABLE_FOR"))
    if relation is ResolutionRelation.EVIDENCE_TRUTH:
        if target.kind is not RecordKind.EVIDENCE or not isinstance(consumer_value, OutcomeRecord) or target not in consumer_value.references:
            raise FiniteProfileError("unsupported evidence-truth coordinate")
        return Judgment("TRUTH_UNKNOWN")
    if relation is ResolutionRelation.REASON_CARRIER:
        if target.kind is not RecordKind.REASON or not isinstance(consumer_value, OutcomeRecord) or target not in consumer_value.references:
            raise FiniteProfileError("unsupported reason-carrier coordinate")
        return Judgment("MALFORMED_RESULT", ("MALFORMED_CARRIER",))
    if relation is ResolutionRelation.CONFLICT_REPLACEMENT:
        if target.kind is not RecordKind.CONFLICT or replacement is None or replacement.identity.kind is not RecordKind.CONFLICT:
            raise FiniteProfileError("unsupported conflict-replacement coordinate")
        return Judgment("CONFLICT_REPLACED", (replacement.identity, "MALFORMED"))
    raise FiniteProfileError(f"unsupported missing coordinate: {relation.value}")


def replay(universe: Universe) -> Any:
    composition = compose_records(universe.records)
    package_status = validate_packages(composition)
    if package_status.tag != "WELL_FORMED":
        return CompositionReplay(composition, Formation.MALFORMED, Closure.NOT_APPLICABLE)
    request = universe.request
    if isinstance(request, InvocationReplayRequest):
        outcome = evaluate_invocation(request.request, composition)
        return CoreReplay(composition, outcome.formation, outcome.closure, outcome.evaluability, outcome.lifecycle, outcome.result)
    if isinstance(request, PairReplayRequest):
        outcome = validate_pair(request.request, composition)
        if isinstance(outcome, Judgment):
            return outcome
        return PairReplay(composition, Formation.WELL_FORMED, Closure.CLOSED, outcome)
    if isinstance(request, LookupRequest):
        if any(composition.at(root) is None for root in request.context_roots):
            return LookupReplay(composition, Judgment("MALFORMED_CONTEXT", tuple(root for root in request.context_roots if composition.at(root) is None)))
        record = composition.at(request.target)
        result = Judgment("PRESENT", (record,)) if record is not None else _resolve_failed_coordinate(request.target, request.coordinate, composition)
        return LookupReplay(composition, result)
    if isinstance(request, GraphEvaluationRequest):
        return evaluate_observation_graph(request, composition)
    if isinstance(request, FormationRequest):
        status = validate_dependency_graph(request.bindings, composition)
        return (Formation.WELL_FORMED, Closure.CLOSED) if status.tag == "WELL_FORMED" else (Formation.MALFORMED, Closure.NOT_APPLICABLE, status)
    if isinstance(request, CompositionRequest):
        flattened = tuple(record for presentation in request.presentations for record in presentation)
        replayed = compose_records(flattened)
        return CompositionReplay(replayed, Formation.MALFORMED if replayed.conflicts else Formation.WELL_FORMED, Closure.NOT_APPLICABLE if replayed.conflicts else Closure.CLOSED)
    raise FiniteProfileError(f"unsupported replay request: {type(request).__name__}")
