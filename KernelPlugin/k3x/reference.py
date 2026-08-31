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
    TERM_RESULT = "TERM_RESULT"
    EVAL_RESULT = "EVAL_RESULT"
    EVAL_RESULT_SEQUENCE = "EVAL_RESULT_SEQUENCE"
    PROFILE_RESULT = "PROFILE_RESULT"


class NodeOperation(Enum):
    OBSERVE = "observe"
    CHANGES_BETWEEN = "changes_between"


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
    admitted_constructor_tags: frozenset[str]
    nested_type_dependencies: frozenset[RecordIdentity]

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
    declaration: RecordIdentity
    meaning_contract: RecordIdentity
    proper_dependencies: frozenset[RecordIdentity]
    dependency_closure: frozenset[RecordIdentity]


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
    capability_summaries: frozenset[RecordIdentity]
    explanatory_text: None = None

    def __post_init__(self) -> None:
        if self.explanatory_text is not None:
            raise ValueError("finite model explanatory_text is exactly ABSENT")


@dataclass(frozen=True)
class ServiceIdentity:
    service_key: ExactKey
    service_kind: str


@dataclass(frozen=True)
class CapabilityDescriptor:
    capability_key: ExactKey
    service: RecordIdentity
    abi_version: Version
    plugin_key: ExactKey
    supported_judgments: frozenset[str]
    supported_targets: frozenset[RecordIdentity]
    sound_fragment: RecordIdentity
    complete_fragment: RecordIdentity | None
    proper_dependencies: frozenset[RecordIdentity]
    dependency_closure: frozenset[RecordIdentity]
    validation_references: frozenset[RecordIdentity]
    required_trust_roots: frozenset[RecordIdentity]


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
    policy: RecordIdentity
    admitted_owners: frozenset[str]
    permitted_targets: frozenset[RecordIdentity]


@dataclass(frozen=True)
class TrustEnvironment:
    policy: RecordIdentity
    roots: tuple[RecordIdentity, ...]
    root_judgments: tuple[tuple[RecordIdentity, TrustState], ...]
    discovery_failure: str | None = None

    def __post_init__(self) -> None:
        if len({root for root, _ in self.root_judgments}) != len(self.root_judgments):
            raise ValueError("duplicate trust-root judgment")


@dataclass(frozen=True)
class SemanticEnvironment:
    declarations: tuple[RecordIdentity, ...]
    bindings: tuple[RecordIdentity, ...]
    profile_bindings: tuple[RecordIdentity, ...] = ()
    pair_bindings: tuple[RecordIdentity, ...] = ()
    authority_facts: tuple[RecordIdentity, ...] = ()
    semantic_extensions: tuple[RecordIdentity, ...] = ()
    lexical_bindings: tuple[RecordIdentity, ...] = ()
    choice_bindings: tuple[RecordIdentity, ...] = ()
    mechanically_extracted_dependencies: frozenset[RecordIdentity] = frozenset()

    def all_references(self) -> frozenset[RecordIdentity]:
        return frozenset(
            self.declarations
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
    semantic_environment: RecordIdentity
    abi: RecordIdentity
    members: frozenset[RecordIdentity]


@dataclass(frozen=True)
class InvocationRequest:
    target: RecordIdentity
    semantic_environment: RecordIdentity
    dependency_environment: RecordIdentity
    trust_environment: RecordIdentity
    requested_version: Version
    arguments: tuple[Any, ...]


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
    left: RecordIdentity
    right: RecordIdentity


@dataclass(frozen=True)
class PairBinding:
    declaration: RecordIdentity
    certificate: RecordIdentity
    proper_subjects: frozenset[RecordIdentity]
    validation_references: frozenset[RecordIdentity]
    required_validation_references: frozenset[RecordIdentity]


@dataclass(frozen=True)
class PairRequestData:
    pair_binding: RecordIdentity
    trust_environment: RecordIdentity


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
    bindings: tuple["LogicalRecord", ...] = ()
    model_contracts: tuple["LogicalRecord", ...] = ()
    contract_specs: tuple["LogicalRecord", ...] = ()
    services: tuple["LogicalRecord", ...] = ()
    certificates: tuple["LogicalRecord", ...] = ()
    other_records: tuple["LogicalRecord", ...] = ()

    def members(self) -> tuple["LogicalRecord", ...]:
        return self.declarations + self.bindings + self.model_contracts + self.contract_specs + self.services + self.certificates + self.other_records


RecordValue = AbiRecord | TypeDeclaration | TypedValue | DeclarationShape | ContractSpec | SemanticBinding | ModelContract | ServiceIdentity | CapabilityDescriptor | CertificateRecord | ProducerRecord | TrustPolicyRecord | TrustRootRecord | TrustEnvironment | SemanticEnvironment | DependencyEnvironment | InvocationRequest | ResultRecord | LifecycleRecord | ObservationEnvironment | PairDeclaration | PairBinding | PairRequestData | ChoiceBinding | LexicalBinding | EvolutionRecord | NamedCarrier | ObservationNode | PluginPackage


@dataclass(frozen=True)
class LogicalRecord:
    identity: RecordIdentity
    value: RecordValue


@dataclass(frozen=True)
class ConflictRef:
    identity: RecordIdentity
    unequal_records: frozenset[LogicalRecord]


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
class LookupRequest:
    target: RecordIdentity
    referring_record: RecordIdentity | None = None
    context_roots: tuple[RecordIdentity, ...] = ()

    def __post_init__(self) -> None:
        if not self.context_roots:
            raise ValueError("lookup requires its literal row-local context roots")


@dataclass(frozen=True)
class GraphEvaluationRequest:
    nodes: tuple[RecordIdentity, ...]
    preferred_order: tuple[RecordIdentity, ...]


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
    ResultRecord: {RecordKind.RESULT},
    LifecycleRecord: {RecordKind.LIFECYCLE},
    ObservationEnvironment: {RecordKind.OBSERVATION_ENVIRONMENT},
    PairDeclaration: {RecordKind.PAIR_DECLARATION},
    PairBinding: {RecordKind.PAIR_BINDING},
    PairRequestData: {RecordKind.REQUEST},
    ChoiceBinding: {RecordKind.CHOICE_BINDING},
    LexicalBinding: {RecordKind.LEXICAL_BINDING},
    EvolutionRecord: {RecordKind.MIGRATION, RecordKind.COMPATIBILITY_CLAIM, RecordKind.SEMANTIC_EXTENSION, RecordKind.ALIAS},
    ObservationNode: {RecordKind.OBSERVATION_NODE},
    PluginPackage: {RecordKind.PACKAGE},
}


def _record_shape(record: LogicalRecord) -> bool:
    allowed = _VALUE_KIND.get(type(record.value))
    if allowed is not None:
        return record.identity.kind in allowed
    named_kinds = {
        RecordKind.OUTCOME, RecordKind.AUTHORITY_FACT, RecordKind.EVENT_VALUE,
        RecordKind.TRACE_EVENT, RecordKind.SOURCE, RecordKind.AUTHORITY_REF,
        RecordKind.EVIDENCE, RecordKind.REASON, RecordKind.CONFLICT,
        RecordKind.PRESENTATION,
    }
    return isinstance(record.value, TypedValue) or (isinstance(record.value, NamedCarrier) and record.identity.kind in named_kinds)


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
            conflicts.append(ConflictRef(identity, frozenset(alternatives)))
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
            (package.declarations, {RecordKind.TYPE_DECLARATION, RecordKind.DECLARATION, RecordKind.SYMBOL, RecordKind.EVENT, RecordKind.PAIR_DECLARATION}),
            (package.bindings, {RecordKind.BINDING, RecordKind.PROFILE_BINDING, RecordKind.PAIR_BINDING, RecordKind.CHOICE_BINDING, RecordKind.LEXICAL_BINDING}),
            (package.model_contracts, {RecordKind.MODEL_CONTRACT}),
            (package.contract_specs, {RecordKind.CONTRACT_SPEC}),
            (package.services, {RecordKind.SERVICE, RecordKind.CAPABILITY}),
            (package.certificates, {RecordKind.CERTIFICATE}),
        )
        for members, kinds in categories:
            if any(member.identity.kind not in kinds for member in members):
                return Judgment("MALFORMED", ("PACKAGE_MEMBER_CATEGORY", record.identity))
        if any(isinstance(member.value, CapabilityDescriptor) and (member.value.abi_version != package.abi_version or member.value.plugin_key != package.plugin_key) for member in package.services):
            return Judgment("MALFORMED", ("DESCRIPTOR_PACKAGE_ABI_OR_PLUGIN", record.identity))
    return Judgment("WELL_FORMED")


def validate_binding(binding: SemanticBinding, composition: Composition) -> Judgment:
    declaration = _resolve(composition, binding.declaration, DeclarationShape)
    meaning = _resolve(composition, binding.meaning_contract, ContractSpec)
    if declaration is None or meaning is None:
        return Judgment("OPEN_BINDINGS", (binding.declaration if declaration is None else binding.meaning_contract,))
    if binding.meaning_contract not in binding.proper_dependencies:
        return Judgment("OPEN_BINDINGS", (binding.meaning_contract,))
    if not binding.proper_dependencies <= binding.dependency_closure:
        return Judgment("MALFORMED", ("DEPENDENCY_CLOSURE",))
    if any(_resolve(composition, item) is None for item in binding.dependency_closure):
        return Judgment("OPEN_BINDINGS", tuple(item for item in binding.dependency_closure if _resolve(composition, item) is None))
    return Judgment("CLOSED")


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
    if service.value.service_kind not in descriptor.supported_judgments or not descriptor.supported_judgments:
        return Judgment("MALFORMED", ("DESCRIPTOR_JUDGMENT",))
    if sound is not None and (sound.value.owner_layer is not Layer.SERVICE or sound.value.role is not ContractRole.SOUND_FRAGMENT):
        return Judgment("MALFORMED", ("DESCRIPTOR_SOUND_ROLE",))
    if complete is not None and (complete.value.owner_layer is not Layer.SERVICE or complete.value.role is not ContractRole.COMPLETE_FRAGMENT):
        return Judgment("MALFORMED", ("DESCRIPTOR_COMPLETE_ROLE",))
    if model.capability_summaries != frozenset({descriptor_identity}):
        return Judgment("MALFORMED", ("MODEL_DESCRIPTOR_MISMATCH",))
    if not descriptor.proper_dependencies <= descriptor.dependency_closure:
        return Judgment("MALFORMED", ("DESCRIPTOR_DEPENDENCY_CLOSURE",))
    if descriptor.validation_references & descriptor.proper_dependencies:
        return Judgment("MALFORMED", ("DESCRIPTOR_VALIDATION_IN_PROPER_SUPPORT",))
    if any(item.kind is not RecordKind.TRUST_ROOT for item in descriptor.required_trust_roots):
        return Judgment("MALFORMED", ("DESCRIPTOR_TRUST_ROOT_KIND",))
    if any(_resolve(composition, item) is None for item in descriptor.dependency_closure | descriptor.validation_references):
        return Judgment("MALFORMED", ("DESCRIPTOR_DANGLING_REFERENCE",))
    if target_binding.value.declaration not in descriptor.supported_targets:
        return Judgment("MALFORMED", ("DESCRIPTOR_TARGET",))
    return Judgment("WELL_FORMED")


def _proper_graph(bindings: tuple[RecordIdentity, ...], composition: Composition) -> dict[RecordIdentity, set[RecordIdentity]]:
    domain = set(bindings)
    graph: dict[RecordIdentity, set[RecordIdentity]] = {}
    for identity in bindings:
        record = _resolve(composition, identity, SemanticBinding)
        if record is None:
            raise ValueError("missing graph binding")
        graph[identity] = {item for item in record.value.proper_dependencies if item in domain}
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
    if dependency.value.semantic_environment != request.semantic_environment:
        return None
    if _resolve(composition, dependency.value.abi, AbiRecord) is None:
        return None
    if semantic.value.all_references() != semantic.value.mechanically_extracted_dependencies:
        return None
    if not semantic.value.all_references() <= dependency.value.members:
        return None
    if any(_resolve(composition, item) is None for item in dependency.value.members):
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
    if policy is None:
        return Judgment("TRUST_ROOT_ABSENT")
    states = dict(environment.root_judgments)
    for required in descriptor.required_trust_roots:
        root_record = _resolve(composition, required, TrustRootRecord)
        if root_record is None or required not in environment.roots or required not in states:
            return Judgment("TRUST_ROOT_ABSENT", (required,))
        root = root_record.value
        if root.policy != environment.policy or descriptor.plugin_key.owner not in root.admitted_owners or descriptor.service not in root.permitted_targets:
            return Judgment("TRUST_ROOT_INCOMPATIBLE", (required,))
        state = states[required]
        if state is TrustState.UNDECIDED:
            return Judgment("TRUST_ROOT_UNDECIDED", (required,))
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
    descriptors = tuple(record for record in composition.records if isinstance(record.value, CapabilityDescriptor) and record.identity in model.capability_summaries)
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
    if len(request.arguments) != 3:
        return ContractReplay(Formation.MALFORMED, Closure.NOT_APPLICABLE, Evaluability.UNKNOWN, "ARGUMENT_ARITY", None)
    from .coding_plugin import task_accepts
    result = task_accepts(request.arguments[0], request.arguments[1], request.arguments[2])
    return ContractReplay(Formation.WELL_FORMED, Closure.CLOSED, Evaluability.AVAILABLE, f"INVOCABLE_FOR({request_identity.key.local})", result)


def _producer_set(subject: RecordIdentity, composition: Composition) -> frozenset[str]:
    return frozenset(record.value.producer for record in composition.records if isinstance(record.value, ProducerRecord) and record.value.subject == subject)


def validate_pair(request_identity: RecordIdentity, composition: Composition) -> PairValidationResult | Judgment:
    request_record = _resolve(composition, request_identity, PairRequestData)
    if request_record is None:
        return Judgment("MALFORMED_REQUEST")
    binding_record = _resolve(composition, request_record.value.pair_binding, PairBinding)
    trust_record = _resolve(composition, request_record.value.trust_environment, TrustEnvironment)
    if binding_record is None or trust_record is None:
        return Judgment("OPEN_BINDINGS")
    binding = binding_record.value
    declaration_record = _resolve(composition, binding.declaration, PairDeclaration)
    certificate_record = _resolve(composition, binding.certificate, CertificateRecord)
    if declaration_record is None or certificate_record is None:
        return Judgment("OPEN_BINDINGS")
    if certificate_record.value.subject != binding.declaration or certificate_record.value.judgment != "PAIR_COHERENCE_ADMITTED":
        return Judgment("MALFORMED", ("PAIR_CERTIFICATE_SUBJECT_OR_JUDGMENT",))
    if binding.validation_references != binding.required_validation_references or len(binding.validation_references) != 2:
        return Judgment("MALFORMED", ("VALIDATION_REFERENCE_MISMATCH",))
    if binding.validation_references & binding.proper_subjects:
        return Judgment("MALFORMED", ("VALIDATION_REFERENCE_IN_PROPER_DAG",))
    if any(_resolve(composition, reference, CertificateRecord) is None for reference in binding.validation_references):
        return Judgment("MALFORMED", ("MISSING_VALIDATION_REFERENCE",))
    graph_status = validate_dependency_graph(tuple(binding.proper_subjects), composition)
    if graph_status.tag != "WELL_FORMED":
        return graph_status
    trust = trust_record.value
    if _resolve(composition, trust.policy, TrustPolicyRecord) is None or any(_resolve(composition, root, TrustRootRecord) is None for root in trust.roots):
        return Judgment("MALFORMED", ("PAIR_TRUST_CHAIN",))
    subjects = (binding.declaration, binding.certificate, *tuple(sorted(binding.validation_references)))
    producer_sets = tuple(_producer_set(subject, composition) for subject in subjects)
    trust_producers = _producer_set(request_record.value.trust_environment, composition) | _producer_set(trust.policy, composition)
    for root in trust.roots:
        trust_producers |= _producer_set(root, composition)
    producer_sets = producer_sets + (trust_producers,)
    if any(not producers for producers in producer_sets):
        return Judgment("MALFORMED", ("INCOMPLETE_PRODUCER_SET",))
    if _producer_set(binding.declaration, composition) != frozenset({declaration_record.value.pair_key.owner}):
        return Judgment("MALFORMED", ("PAIR_SUBJECT_PRODUCER",))
    for index, producers in enumerate(producer_sets):
        if any(producers & other for other in producer_sets[index + 1:]):
            return Judgment("MALFORMED", ("PAIR_SELF_TRUST",))
    return PairValidationResult(declaration_record.value.pair_key, certificate_record.value.certificate_key, certificate_record.value.judgment)


def evaluate_observation_graph(request: GraphEvaluationRequest, composition: Composition) -> ObservationEvaluation:
    from .coding_plugin import changes_between, observe
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


def _missing_result(target: RecordIdentity, referring: LogicalRecord | None, composition: Composition) -> Judgment:
    kind = target.kind
    if kind in {RecordKind.ABI, RecordKind.PACKAGE, RecordKind.DECLARATION, RecordKind.SYMBOL, RecordKind.EVENT, RecordKind.PAIR_DECLARATION, RecordKind.OUTCOME, RecordKind.EVENT_VALUE, RecordKind.TRACE_EVENT, RecordKind.SOURCE, RecordKind.AUTHORITY_REF}:
        return Judgment("MALFORMED")
    if kind in {RecordKind.BINDING, RecordKind.PROFILE_BINDING, RecordKind.PAIR_BINDING}:
        return Judgment("OPEN_BINDINGS")
    if kind in {RecordKind.AUTHORITY_FACT, RecordKind.CHOICE_BINDING, RecordKind.LEXICAL_BINDING}:
        return Judgment("OPEN_BINDINGS", (target,))
    if kind is RecordKind.SERVICE or kind is RecordKind.CAPABILITY:
        return Judgment("EVALUABILITY_MISSING")
    if kind is RecordKind.TRUST_POLICY:
        return Judgment("TRUST_ROOT_ABSENT")
    if kind is RecordKind.TRUST_ROOT:
        return Judgment("TRUST_ROOT_ABSENT", (target,))
    if kind is RecordKind.CERTIFICATE:
        return Judgment("NO_CERTIFICATE_ADMISSION", ("CONSISTENCY_UNKNOWN",))
    if kind is RecordKind.MIGRATION:
        return Judgment("NO_MIGRATION", (target.key.local,))
    if kind is RecordKind.COMPATIBILITY_CLAIM:
        return Judgment("NO_COMPATIBILITY", (target.key.local,))
    if kind is RecordKind.SEMANTIC_EXTENSION:
        required = isinstance(referring.value, EvolutionRecord) and referring.value.required if referring is not None else False
        return Judgment("INCOMPATIBLE" if required else "NO_EFFECT", (target.key.local,))
    if kind is RecordKind.MODEL_CONTRACT:
        return Judgment("OPEN_BINDINGS", ("MODEL_CONTRACT",))
    if kind is RecordKind.ALIAS:
        required = isinstance(referring.value, EvolutionRecord) and referring.value.required if referring is not None else False
        return Judgment("MALFORMED", ("MISSING_ALIAS", target.key.local)) if required else Judgment("NO_ALIAS", (target.key.local,))
    if kind is RecordKind.CONTRACT_SPEC:
        if referring is not None and isinstance(referring.value, CapabilityDescriptor):
            return Judgment("CAPABILITY_INCOMPATIBLE", ("EVALUABILITY_MISSING",))
        return Judgment("BINDING_INCOMPATIBLE", ("OPEN_BINDINGS",))
    if kind is RecordKind.REQUEST:
        if referring is not None and isinstance(referring.value, SemanticEnvironment) and referring.value.lexical_bindings:
            return Judgment("MALFORMED_REQUEST", ("EXTRANEOUS_LEXICAL_BINDING", referring.value.lexical_bindings[-1]))
        return Judgment("MALFORMED_REQUEST")
    if kind is RecordKind.RESULT:
        return Judgment("INVOCATION_FAILED", ("PROTOCOL", "NO_RESULT", "NO_TRUTH"))
    if kind in {RecordKind.SEMANTIC_ENVIRONMENT, RecordKind.TRUST_ENVIRONMENT, RecordKind.DEPENDENCY_ENVIRONMENT}:
        return Judgment("MALFORMED_REQUEST", (referring.identity if referring is not None else target,))
    if kind is RecordKind.OBSERVATION_ENVIRONMENT:
        return Judgment("MALFORMED_RESULT", ("SEMANTIC_MISMATCH",))
    if kind is RecordKind.LIFECYCLE:
        return Judgment("LIFECYCLE_REPLACED", (referring.identity if referring is not None else target, "INVOCABLE_FOR"))
    if kind is RecordKind.EVIDENCE:
        return Judgment("TRUTH_UNKNOWN")
    if kind is RecordKind.REASON:
        return Judgment("MALFORMED_RESULT", ("MALFORMED_CARRIER",))
    if kind is RecordKind.CONFLICT:
        replacement = next((record for record in composition.records if record.identity.kind is RecordKind.CONFLICT), None)
        return Judgment("CONFLICT_REPLACED", ((replacement.identity if replacement else None), "MALFORMED"))
    raise FiniteProfileError(f"no missing-status branch for {kind.value}")


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
        referring = composition.at(request.referring_record) if request.referring_record is not None else None
        if request.referring_record is not None and referring is None:
            return LookupReplay(composition, Judgment("MALFORMED_CONTEXT", (request.referring_record,)))
        result = Judgment("PRESENT", (record,)) if record is not None else _missing_result(request.target, referring, composition)
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
