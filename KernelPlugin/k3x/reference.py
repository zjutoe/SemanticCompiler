"""Finite, pure reference kernel for the accepted K2/K3-S executable slice."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class FiniteProfileError(NotImplementedError):
    """An operation is outside the explicitly enumerated K3-X slice."""


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


@dataclass(frozen=True)
class InterfaceFailure:
    domain: FailureDomain
    kind: str
    reasons: frozenset[str]


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


class MissingKind(Enum):
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


@dataclass(frozen=True, order=True)
class RecordIdentity:
    key: ExactKey


@dataclass(frozen=True)
class LogicalRecord:
    identity: RecordIdentity
    record_kind: str
    fields: tuple[tuple[str, Any], ...]

    def field_map(self) -> dict[str, Any]:
        return dict(self.fields)


@dataclass(frozen=True)
class TypeDeclaration:
    type_key: ExactKey
    admitted_constructor_tags: frozenset[str]
    nested_type_dependencies: frozenset[ExactKey]


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
    proper_type_dependencies: frozenset[ExactKey]


@dataclass(frozen=True)
class SemanticBinding:
    declaration_key: ExactKey
    meaning_contract_key: ExactKey
    proper_dependencies: frozenset[str]
    dependency_closure: frozenset[str]


@dataclass(frozen=True)
class ConflictRef:
    identity: RecordIdentity
    unequal_records: frozenset[LogicalRecord]


@dataclass(frozen=True)
class Composition:
    records: frozenset[LogicalRecord]
    conflicts: tuple[ConflictRef, ...]


@dataclass(frozen=True)
class PluginPackage:
    abi_version: Version
    plugin_key: ExactKey
    members: frozenset[RecordIdentity]


@dataclass(frozen=True)
class ObservationQuery:
    dependency: str
    expected_kind: ObservationKind
    input_projection: str


@dataclass(frozen=True)
class ContractSpec:
    key: ExactKey
    owner_layer: Layer
    role: ContractRole
    primary_input_domain: str
    codomain: frozenset[str]
    observation_queries: tuple[ObservationQuery, ...]
    support: frozenset[str]
    relation_name: str


@dataclass(frozen=True)
class CapabilityDescriptor:
    capability_key: ExactKey
    abi_version: Version
    plugin_key: ExactKey
    supported_judgments: frozenset[str]
    supported_targets: frozenset[str]
    sound_fragment_key: ExactKey
    complete_fragment_key: ExactKey | None
    proper_dependencies: frozenset[str]
    dependency_closure: frozenset[str]
    validation_references: frozenset[str]
    required_trust_roots: frozenset[str]


@dataclass(frozen=True)
class ModelContract:
    key: ExactKey
    target_key: ExactKey
    exact_version: Version
    semantic_contract_key: ExactKey
    capability_summaries: frozenset[ExactKey]


@dataclass(frozen=True)
class DependencyGraph:
    nodes: tuple[str, ...]
    proper_dependencies: tuple[tuple[str, tuple[str, ...]], ...]
    validation_references: frozenset[str] = frozenset()

    def dependencies(self) -> dict[str, tuple[str, ...]]:
        return dict(self.proper_dependencies)


@dataclass(frozen=True)
class ObservationNode:
    key: str
    operation: NodeOperation
    arguments: tuple[Any, ...]
    expected_kind: ObservationKind


@dataclass(frozen=True)
class Judgment:
    tag: str
    details: tuple[Any, ...] = ()


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
class TrustProjection:
    discovery: str
    evaluability: Evaluability
    lifecycle: str
    result: Any | None


@dataclass(frozen=True)
class PairValidationResult:
    pair_key: str
    certificate_key: str
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
class PairContract:
    pair_key: str
    certificate_key: str
    proper_graph: DependencyGraph
    validation_references: frozenset[str]
    required_validation_references: frozenset[str]
    subject_producers: frozenset[str]
    certificate_producers: frozenset[str]
    validation_producers: frozenset[str]
    trust_producers: frozenset[str]
    pair_owner: str


@dataclass(frozen=True)
class ObservationEvaluation:
    observations: tuple[tuple[str, Any], ...]
    reasoning_result: Judgment
    lifecycle: str
    status: tuple[str, ...]


@dataclass(frozen=True)
class CompositionReplay:
    composition: Composition
    formation: Formation
    closure: Closure


@dataclass(frozen=True)
class ExecutableContract:
    declared: bool
    bound: bool
    capability_present: bool
    requested_version: Version
    binding_version: Version
    model_contract: ModelContract
    descriptor: CapabilityDescriptor
    task: Any
    final_snapshot: Any
    evidence: tuple[Any, ...]


@dataclass(frozen=True)
class CoreRequest:
    contract: ExecutableContract


@dataclass(frozen=True)
class PairRequest:
    pair: PairContract


@dataclass(frozen=True)
class TrustRequest:
    state: TrustState
    target: str
    failure: str | None = None


@dataclass(frozen=True)
class LookupRequest:
    target: RecordIdentity
    kind: MissingKind


@dataclass(frozen=True)
class GraphEvaluationRequest:
    graph: DependencyGraph
    observation_nodes: tuple[ObservationNode, ...]
    preferred_order: tuple[str, ...]


@dataclass(frozen=True)
class FormationRequest:
    graph: DependencyGraph


@dataclass(frozen=True)
class CompositionRequest:
    presentations: tuple[tuple[LogicalRecord, ...], ...]


@dataclass(frozen=True)
class Universe:
    records: tuple[LogicalRecord, ...]
    packages: tuple[PluginPackage, ...]
    request: Any


def exact_version_agreement(requested: Version, supplied: Version) -> bool:
    """Versions agree only by exact component equality; there is no fallback."""
    return requested == supplied


def admit_typed_value(declaration: TypeDeclaration, value: TypedValue) -> Judgment:
    if value.type_key != declaration.type_key:
        return Judgment("NOT_ADMITTED", ("TYPE_KEY_MISMATCH",))
    if value.constructor_tag not in declaration.admitted_constructor_tags:
        return Judgment("NOT_ADMITTED", ("CONSTRUCTOR_TAG", value.constructor_tag))
    return Judgment("ADMITTED")


def validate_declaration_shape(declaration: DeclarationShape) -> Judgment:
    if declaration.declaration_kind not in {"FUNCTION", "PREDICATE"}:
        return Judgment("MALFORMED", ("DECLARATION_KIND",))
    if declaration.declaration_key.owner != declaration.symbol_key.owner:
        return Judgment("MALFORMED", ("DECLARATION_SYMBOL_OWNER",))
    if not exact_version_agreement(
        declaration.declaration_key.version, declaration.symbol_key.version
    ):
        return Judgment("MALFORMED", ("DECLARATION_SYMBOL_VERSION",))
    if len(declaration.facet_positions) != len(declaration.argument_types):
        return Judgment("MALFORMED", ("FACET_ARITY",))
    plugin_types = frozenset(
        key for key in declaration.argument_types if key.namespace != "carrier.type"
    )
    if declaration.proper_type_dependencies != plugin_types:
        return Judgment("MALFORMED", ("TYPE_DEPENDENCY_MISMATCH",))
    return Judgment("WELL_FORMED")


def validate_binding(binding: SemanticBinding) -> Judgment:
    meaning_root = f"CONTRACT_SPEC({binding.meaning_contract_key.local})"
    if meaning_root not in binding.proper_dependencies:
        return Judgment("OPEN_BINDINGS", (meaning_root,))
    if not binding.proper_dependencies <= binding.dependency_closure:
        return Judgment("MALFORMED", ("DEPENDENCY_CLOSURE",))
    return Judgment("CLOSED")


def project_interface_failure(failure: InterfaceFailure) -> Judgment:
    """Apply the exact K2 failure-family projection without collapsing domains."""
    if not failure.reasons:
        return Judgment("MALFORMED_RESULT", ("EMPTY_FAILURE_REASONS",))
    if failure.domain is FailureDomain.FUNCTION_EVALUATION:
        return Judgment("TERM_ERROR", (failure.kind, failure.reasons))
    if failure.domain is FailureDomain.PREDICATE_EVALUATION:
        return Judgment("EVAL_ERROR", (failure.kind, failure.reasons))
    if failure.domain is FailureDomain.PROFILE_CONCRETE:
        return Judgment("PROFILE_EVALUATION_ERROR", (failure.kind, failure.reasons))
    if failure.domain is FailureDomain.REASONING:
        return Judgment("REASONING_ERROR", (failure.kind, failure.reasons))
    raise FiniteProfileError(f"unsupported failure domain: {failure.domain}")


def compose_records(records: tuple[LogicalRecord, ...]) -> Composition:
    grouped: dict[RecordIdentity, set[LogicalRecord]] = {}
    for record in records:
        if not isinstance(record, LogicalRecord):
            raise TypeError("composition accepts complete LogicalRecord values")
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


def validate_packages(
    packages: tuple[PluginPackage, ...], composition: Composition
) -> Judgment:
    if composition.conflicts:
        return Judgment("MALFORMED", ("CONFLICT", composition.conflicts))
    identities = {record.identity for record in composition.records}
    for package in packages:
        if not package.members <= identities:
            return Judgment("MALFORMED", ("MISSING_PACKAGE_MEMBER", package.plugin_key))
        for identity in package.members:
            if identity.key.owner != package.plugin_key.owner:
                return Judgment("MALFORMED", ("PACKAGE_OWNER", identity))
    return Judgment("WELL_FORMED")


def validate_contract_spec(spec: ContractSpec) -> Judgment:
    query_keys = tuple(query.dependency for query in spec.observation_queries)
    if len(query_keys) != len(set(query_keys)):
        return Judgment("MALFORMED", ("DUPLICATE_OBSERVATION_QUERY",))
    if frozenset(query_keys) != spec.support:
        return Judgment("MALFORMED", ("SUPPORT_QUERY_MISMATCH",))
    delta_roles = {ContractRole.TYPE_ADMISSION}
    service_roles = {
        ContractRole.SOUND_FRAGMENT,
        ContractRole.COMPLETE_FRAGMENT,
        ContractRole.REQUIRED_EVIDENCE,
        ContractRole.SERVICE_FAILURE_BEHAVIOR,
    }
    if spec.owner_layer is Layer.DELTA and spec.role not in delta_roles:
        return Judgment("MALFORMED", ("DELTA_ROLE",))
    if spec.owner_layer is Layer.SERVICE and spec.role not in service_roles:
        return Judgment("MALFORMED", ("SERVICE_ROLE",))
    if spec.owner_layer is Layer.SIGMA and spec.role in delta_roles | service_roles:
        return Judgment("MALFORMED", ("SIGMA_ROLE",))
    if spec.owner_layer is Layer.SERVICE:
        legal = {
            ObservationKind.TERM_RESULT,
            ObservationKind.EVAL_RESULT,
            ObservationKind.EVAL_RESULT_SEQUENCE,
            ObservationKind.PROFILE_RESULT,
        }
        if any(query.expected_kind not in legal for query in spec.observation_queries):
            return Judgment("MALFORMED", ("SERVICE_OBSERVATION_KIND",))
    if any(not query.input_projection for query in spec.observation_queries):
        return Judgment("MALFORMED", ("NON_TOTAL_INPUT_PROJECTION",))
    if not spec.primary_input_domain or not spec.codomain or not spec.relation_name:
        return Judgment("MALFORMED", ("INCOMPLETE_CONTRACT_SPEC",))
    return Judgment("WELL_FORMED")


def validate_model_descriptor(
    model: ModelContract, descriptor: CapabilityDescriptor
) -> Judgment:
    if not exact_version_agreement(model.exact_version, model.target_key.version):
        return Judgment("MALFORMED", ("MODEL_TARGET_VERSION",))
    descriptor_summary = frozenset({descriptor.capability_key})
    if model.capability_summaries != descriptor_summary:
        return Judgment("MALFORMED", ("MODEL_DESCRIPTOR_MISMATCH",))
    if model.target_key.owner != model.key.owner:
        return Judgment("MALFORMED", ("MODEL_OWNER_MISMATCH",))
    return Judgment("WELL_FORMED")


def topological_order(
    graph: DependencyGraph, preferred_order: tuple[str, ...] = ()
) -> tuple[str, ...]:
    if len(graph.nodes) != len(set(graph.nodes)):
        raise ValueError("duplicate dependency node")
    dependencies = graph.dependencies()
    if set(dependencies) != set(graph.nodes):
        raise ValueError("every node needs one explicit proper-dependency entry")
    if any(dep not in dependencies for values in dependencies.values() for dep in values):
        raise ValueError("proper dependency names an absent node")
    remaining = {node: set(values) for node, values in dependencies.items()}
    order: list[str] = []
    preference = {node: position for position, node in enumerate(preferred_order)}
    while remaining:
        ready = [node for node, values in remaining.items() if not values]
        if not ready:
            raise ValueError("dependency cycle")
        ready.sort(key=lambda node: (preference.get(node, len(preference)), node))
        node = ready[0]
        order.append(node)
        del remaining[node]
        for values in remaining.values():
            values.discard(node)
    return tuple(order)


def validate_dependency_graph(graph: DependencyGraph) -> Judgment:
    try:
        topological_order(graph)
    except ValueError as error:
        return Judgment("MALFORMED", (str(error),))
    return Judgment("WELL_FORMED")


def evaluate_observation_graph(
    graph: DependencyGraph,
    nodes: tuple[ObservationNode, ...],
    preferred_order: tuple[str, ...],
) -> ObservationEvaluation:
    from .coding_plugin import changes_between, observe

    node_map = {node.key: node for node in nodes}
    if set(node_map) != set(graph.nodes) or len(node_map) != len(nodes):
        raise ValueError("observation nodes must equal the proper graph domain")
    order = topological_order(graph, preferred_order)
    observations: dict[str, Any] = {}
    for key in order:
        node = node_map[key]
        if node.operation is NodeOperation.OBSERVE:
            value = observe(*node.arguments)
        elif node.operation is NodeOperation.CHANGES_BETWEEN:
            value = changes_between(*node.arguments)
        else:
            raise FiniteProfileError(f"unsupported observation node: {node.operation}")
        if node.expected_kind is not ObservationKind.TERM_RESULT:
            raise FiniteProfileError("the finite confluence graph expects TERM_RESULT")
        observations[key] = value
    complete = tuple(sorted(observations.items(), key=lambda item: item[0]))
    return ObservationEvaluation(
        complete,
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


def project_trust(request: TrustRequest) -> TrustProjection:
    if request.state is TrustState.ADMITTED:
        return TrustProjection(
            "CAPABILITY_DISCOVERED",
            Evaluability.AVAILABLE,
            f"INVOCABLE_FOR({request.target})",
            Judgment("INVOCABLE_FOR", (request.target,)),
        )
    if request.state is TrustState.ABSENT:
        return TrustProjection(
            "CAPABILITY_INCOMPATIBLE",
            Evaluability.MISSING,
            "TRUST_ROOT_ABSENT",
            None,
        )
    if request.state is TrustState.UNDECIDED:
        return TrustProjection(
            "CAPABILITY_DISCOVERED",
            Evaluability.UNKNOWN,
            "TRUST_ROOT_UNDECIDED",
            None,
        )
    if request.state is TrustState.INCOMPATIBLE:
        return TrustProjection(
            "CAPABILITY_INCOMPATIBLE",
            Evaluability.MISSING,
            "TRUST_ROOT_INCOMPATIBLE",
            None,
        )
    if request.state is TrustState.FAILED:
        if request.failure is None:
            raise ValueError("failed discovery requires its protocol/transport failure")
        return TrustProjection(
            "DISCOVERY_FAILED",
            Evaluability.UNKNOWN,
            "DISCOVERY_FAILED",
            None,
        )
    raise FiniteProfileError(f"unsupported trust state: {request.state}")


def missing_status(kind: MissingKind) -> Judgment:
    if kind in {
        MissingKind.ABI,
        MissingKind.PLUGIN,
        MissingKind.DECLARATION,
        MissingKind.SYMBOL,
        MissingKind.EVENT,
        MissingKind.PAIR_DECLARATION,
        MissingKind.OUTCOME,
        MissingKind.EVENT_VALUE,
        MissingKind.TRACE_EVENT,
        MissingKind.SOURCE,
        MissingKind.AUTHORITY_REF,
    }:
        return Judgment("MALFORMED")
    if kind in {
        MissingKind.BINDING,
        MissingKind.PROFILE_BINDING,
        MissingKind.PAIR_BINDING,
    }:
        return Judgment("OPEN_BINDINGS")
    if kind is MissingKind.AUTHORITY_FACT:
        return Judgment("OPEN_BINDINGS", ("AUTHORITY_FACT(AF(choice,1))",))
    if kind is MissingKind.CHOICE_BINDING:
        return Judgment("OPEN_BINDINGS", ("CHOICE_BINDING(cb0)",))
    if kind is MissingKind.LEXICAL_BINDING:
        return Judgment("OPEN_BINDINGS", ("LEXICAL_BINDING(lk0)",))
    if kind is MissingKind.EXTRANEOUS_LEXICAL_BINDING:
        return Judgment("MALFORMED_REQUEST", ("EXTRANEOUS_LEXICAL_BINDING(lk_extra)",))
    if kind in {MissingKind.SERVICE, MissingKind.CAPABILITY}:
        return Judgment("EVALUABILITY_MISSING")
    if kind is MissingKind.TRUST_POLICY:
        return Judgment("TRUST_ROOT_ABSENT")
    if kind is MissingKind.TRUST_ROOT:
        return Judgment("TRUST_ROOT_ABSENT", ("TR",))
    if kind is MissingKind.CERTIFICATE:
        return Judgment("NO_CERTIFICATE_ADMISSION", ("CONSISTENCY_UNKNOWN",))
    if kind is MissingKind.MIGRATION:
        return Judgment("NO_MIGRATION", ("MK0",))
    if kind is MissingKind.COMPATIBILITY_CLAIM:
        return Judgment("NO_COMPATIBILITY", ("CCK0",))
    if kind is MissingKind.EXTENSION_OPTIONAL:
        return Judgment("NO_EFFECT", ("XK0",))
    if kind is MissingKind.EXTENSION_REQUIRED:
        return Judgment("INCOMPATIBLE", ("XK1",))
    if kind is MissingKind.MODEL_CONTRACT:
        return Judgment("OPEN_BINDINGS", ("MODEL_CONTRACT",))
    if kind is MissingKind.ALIAS_OPTIONAL:
        return Judgment("NO_ALIAS", ("AK0",))
    if kind is MissingKind.ALIAS_REQUIRED:
        return Judgment("MALFORMED", ("MISSING_ALIAS(AK1)",))
    if kind is MissingKind.SIGMA_CONTRACT_SPEC:
        return Judgment("BINDING_INCOMPATIBLE", ("OPEN_BINDINGS",))
    if kind is MissingKind.SERVICE_CONTRACT_SPEC:
        return Judgment("CAPABILITY_INCOMPATIBLE", ("EVALUABILITY_MISSING",))
    if kind is MissingKind.REQUEST:
        return Judgment("MALFORMED_REQUEST")
    if kind is MissingKind.RESULT:
        return Judgment("INVOCATION_FAILED", ("PROTOCOL", "fr_noresult", "NO_TRUTH"))
    if kind in {
        MissingKind.SEMANTIC_ENVIRONMENT,
        MissingKind.TRUST_ENVIRONMENT,
        MissingKind.DEPENDENCY_ENVIRONMENT,
    }:
        return Judgment("MALFORMED_REQUEST", ("IDENTITY_OF(Q_t[T_admitted])",))
    if kind is MissingKind.OBSERVATION_ENVIRONMENT:
        return Judgment("MALFORMED_RESULT", ("SEMANTIC_MISMATCH",))
    if kind is MissingKind.LIFECYCLE:
        return Judgment(
            "LIFECYCLE_REPLACED",
            ("R_c_alt", "L_life_after", "INVOCABLE_FOR(R_c_alt)"),
        )
    if kind is MissingKind.EVIDENCE:
        return Judgment("TRUTH_UNKNOWN")
    if kind is MissingKind.REASON:
        return Judgment("MALFORMED_RESULT", ("MALFORMED_CARRIER",))
    if kind is MissingKind.CONFLICT:
        return Judgment("CONFLICT_REPLACED", ("conflict1", "MALFORMED"))
    raise FiniteProfileError(f"unsupported missing record kind: {kind}")


def record_at(universe: Universe, target: RecordIdentity) -> LogicalRecord | None:
    matches = tuple(record for record in universe.records if record.identity == target)
    if len(matches) > 1 and len(set(matches)) > 1:
        raise ValueError("conflicting authoritative records at lookup identity")
    return matches[0] if matches else None


def evaluate_contract(contract: ExecutableContract) -> ContractReplay:
    from .coding_plugin import task_accepts

    if not contract.declared:
        return ContractReplay(
            Formation.MALFORMED,
            Closure.NOT_APPLICABLE,
            Evaluability.UNKNOWN,
            "DECLARATION_ABSENT",
            None,
        )
    if not contract.bound:
        return ContractReplay(
            Formation.WELL_FORMED,
            Closure.OPEN_BINDINGS,
            Evaluability.UNKNOWN,
            "BINDING_ABSENT",
            None,
        )
    if not exact_version_agreement(
        contract.requested_version, contract.binding_version
    ):
        return ContractReplay(
            Formation.MALFORMED,
            Closure.NOT_APPLICABLE,
            Evaluability.UNKNOWN,
            "VERSION_MISMATCH",
            None,
        )
    model_status = validate_model_descriptor(
        contract.model_contract, contract.descriptor
    )
    if model_status.tag != "WELL_FORMED":
        return ContractReplay(
            Formation.MALFORMED,
            Closure.NOT_APPLICABLE,
            Evaluability.UNKNOWN,
            model_status.tag,
            None,
        )
    if not contract.capability_present:
        return ContractReplay(
            Formation.WELL_FORMED,
            Closure.CLOSED,
            Evaluability.MISSING,
            "CAPABILITY_ABSENT",
            None,
        )
    result = task_accepts(contract.task, contract.final_snapshot, contract.evidence)
    return ContractReplay(
        Formation.WELL_FORMED,
        Closure.CLOSED,
        Evaluability.AVAILABLE,
        "COMPLETED",
        result,
    )


def validate_pair(pair: PairContract) -> PairValidationResult | Judgment:
    graph_status = validate_dependency_graph(pair.proper_graph)
    if graph_status.tag != "WELL_FORMED":
        return graph_status
    if pair.validation_references != pair.required_validation_references:
        return Judgment("MALFORMED", ("VALIDATION_REFERENCE_MISMATCH",))
    if pair.validation_references & set(pair.proper_graph.nodes):
        return Judgment("MALFORMED", ("VALIDATION_REFERENCE_IN_PROPER_DAG",))
    if pair.subject_producers != frozenset({pair.pair_owner}):
        return Judgment("MALFORMED", ("PAIR_SUBJECT_PRODUCER",))
    producer_sets = (
        pair.subject_producers,
        pair.certificate_producers,
        pair.validation_producers,
        pair.trust_producers,
    )
    if any(not producers for producers in producer_sets):
        return Judgment("MALFORMED", ("INCOMPLETE_PRODUCER_SET",))
    for position, producers in enumerate(producer_sets):
        for other in producer_sets[position + 1 :]:
            if producers & other:
                return Judgment("MALFORMED", ("PAIR_SELF_TRUST",))
    return PairValidationResult(pair.pair_key, pair.certificate_key, "PAIR_COHERENCE_ADMITTED")


def replay(universe: Universe) -> Any:
    """Replay one self-contained finite universe from its typed K2 request."""
    composition = compose_records(universe.records)
    package_status = validate_packages(universe.packages, composition)
    if package_status.tag != "WELL_FORMED":
        return CompositionReplay(composition, Formation.MALFORMED, Closure.NOT_APPLICABLE)
    request = universe.request
    if isinstance(request, CoreRequest):
        outcome = evaluate_contract(request.contract)
        return CoreReplay(
            composition,
            outcome.formation,
            outcome.closure,
            outcome.evaluability,
            outcome.lifecycle,
            outcome.result,
        )
    if isinstance(request, PairRequest):
        outcome = validate_pair(request.pair)
        if isinstance(outcome, Judgment):
            return outcome
        return PairReplay(
            composition,
            Formation.WELL_FORMED,
            Closure.CLOSED,
            outcome,
        )
    if isinstance(request, TrustRequest):
        projection = project_trust(request)
        if request.state is TrustState.ADMITTED:
            return projection.result
        if request.state is TrustState.ABSENT:
            return Judgment("EVALUABILITY_MISSING")
        if request.state is TrustState.UNDECIDED:
            return Judgment("EVALUABILITY_UNKNOWN")
        if request.state is TrustState.INCOMPATIBLE:
            return Judgment("EVALUABILITY_MISSING")
        return Judgment("DISCOVERY_FAILED", (request.failure,))
    if isinstance(request, LookupRequest):
        record = record_at(universe, request.target)
        outcome = (
            Judgment("PRESENT", (record,))
            if record is not None
            else missing_status(request.kind)
        )
        return LookupReplay(composition, outcome)
    if isinstance(request, GraphEvaluationRequest):
        return evaluate_observation_graph(
            request.graph, request.observation_nodes, request.preferred_order
        )
    if isinstance(request, FormationRequest):
        status = validate_dependency_graph(request.graph)
        if status.tag == "WELL_FORMED":
            return (Formation.WELL_FORMED, Closure.CLOSED)
        return (Formation.MALFORMED, Closure.NOT_APPLICABLE, status)
    if isinstance(request, CompositionRequest):
        flattened = tuple(
            record for presentation in request.presentations for record in presentation
        )
        replayed = compose_records(flattened)
        formation = Formation.MALFORMED if replayed.conflicts else Formation.WELL_FORMED
        closure = Closure.NOT_APPLICABLE if replayed.conflicts else Closure.CLOSED
        return CompositionReplay(replayed, formation, closure)
    raise FiniteProfileError(f"unsupported replay request: {type(request).__name__}")
