"""The closed 102-entry K3-S packet and its separate assertion map."""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .coding_plugin import (
    ArtifactContent,
    ArtifactSelector,
    ChangeEntry,
    ChangeKind,
    ChangeSet,
    Criterion,
    CriterionKind,
    Eval,
    EvidenceEntry,
    ObservationResult,
    ObservationSpec,
    RepositorySnapshot,
    TaskSpec,
    TermResult,
    Truth,
    VerificationRecord,
    VerificationSpec,
    VerificationStatus,
    snapshot_identity,
)
from .reference import (
    CapabilityDescriptor,
    Closure,
    Composition,
    CompositionReplay,
    CompositionRequest,
    ConflictRef,
    CoreReplay,
    CoreRequest,
    DeclarationShape,
    DependencyGraph,
    Evaluability,
    ExactKey,
    ExecutableContract,
    Formation,
    FormationRequest,
    GraphEvaluationRequest,
    Judgment,
    LogicalRecord,
    LookupReplay,
    LookupRequest,
    MissingKind,
    ModelContract,
    NodeOperation,
    ObservationEvaluation,
    ObservationKind,
    ObservationNode,
    PairContract,
    PairReplay,
    PairRequest,
    PairValidationResult,
    PluginPackage,
    RecordIdentity,
    SemanticBinding,
    TrustRequest,
    TrustState,
    TypeDeclaration,
    TypedValue,
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
            raise ValueError("invalid FixtureId arity")


ABI0 = Version((0,))
V1 = Version((1,))


def _key(local: str, owner: str = "capknow.semantic", namespace: str = "coding") -> ExactKey:
    return ExactKey(owner, namespace, local, V1)


def _identity(local: str, owner: str = "capknow.semantic", namespace: str = "coding") -> RecordIdentity:
    return RecordIdentity(_key(local, owner, namespace))


def _record(
    local: str,
    record_kind: str,
    fields: tuple[tuple[str, Any], ...],
    owner: str = "capknow.semantic",
    namespace: str = "coding",
) -> LogicalRecord:
    return LogicalRecord(_identity(local, owner, namespace), record_kind, fields)


def _package(owner: str, local: str, records: tuple[LogicalRecord, ...]) -> PluginPackage:
    return PluginPackage(
        ABI0,
        _key(local, owner, "package"),
        frozenset(record.identity for record in records),
    )


def _package_record(package: PluginPackage) -> LogicalRecord:
    return _record(
        f"package.{package.plugin_key.local}",
        "PLUGIN_PACKAGE",
        (
            ("abi_version", package.abi_version),
            ("plugin_key", package.plugin_key),
            ("literal_members", package.members),
        ),
        owner=package.plugin_key.owner,
        namespace="package",
    )


def _core_universe() -> tuple[Universe, CoreReplay]:
    artifact = ArtifactContent("SOURCE", "PYTHON", 7, "content-final")
    final = RepositorySnapshot((("src/module.py", artifact),))
    selector = ArtifactSelector(frozenset({"src/module.py"}), "SOURCE")
    spec = ObservationSpec("s_final", selector, "IDENTITY")
    observed = ObservationResult("s_final", (("src/module.py", "content-final"),))
    verification = VerificationSpec("v_final", spec)
    reference = "verification/final"
    verification_record = VerificationRecord(
        verification,
        repr(snapshot_identity(final)),
        VerificationStatus.PASS,
        observed,
        frozenset({reference}),
    )
    evidence = (EvidenceEntry(reference, "verification", verification_record),)
    task = TaskSpec(
        (Criterion(CriterionKind.OBSERVATION_EQUALS, (spec, observed)),),
        (verification,),
    )
    target = _key("task_accepts")
    symbol_key = _key("task_accepts", namespace="coding.symbol")
    task_type = _key("TaskSpec", namespace="coding.type")
    snapshot_type = _key("RepositorySnapshot", namespace="coding.type")
    task_type_declaration = TypeDeclaration(
        task_type,
        frozenset({"TASK"}),
        frozenset(),
    )
    snapshot_type_declaration = TypeDeclaration(
        snapshot_type,
        frozenset({"REPOSITORY_SNAPSHOT"}),
        frozenset(),
    )
    declaration = DeclarationShape(
        target,
        symbol_key,
        "PREDICATE",
        (task_type, snapshot_type, _key("EvidenceStore", namespace="carrier.type")),
        "BOOL",
        (frozenset(), frozenset({"final"}), frozenset({"evidence"})),
        frozenset({task_type, snapshot_type}),
    )
    model_key = _key("model.task_accepts", namespace="coding.model")
    meaning_key = _key("predicate.task_accepts", namespace="coding.contract")
    capability_key = _key("predicates", namespace="coding.capability")
    sound_key = _key("predicates.sound", namespace="coding.contract")
    model = ModelContract(
        model_key,
        target,
        V1,
        meaning_key,
        frozenset({capability_key}),
    )
    descriptor = CapabilityDescriptor(
        capability_key,
        ABI0,
        _key("coding-minimal", namespace="plugin"),
        frozenset({"PREDICATE_EVALUATION"}),
        frozenset({"BINDING_TARGET(task_accepts)"}),
        sound_key,
        None,
        frozenset({"BINDING(task_accepts)"}),
        frozenset({"BINDING(task_accepts)"}),
        frozenset(),
        frozenset({"TR"}),
    )
    contract = ExecutableContract(
        True, True, True, V1, V1, model, descriptor, task, final, evidence
    )
    binding = SemanticBinding(
        target,
        meaning_key,
        frozenset({f"CONTRACT_SPEC({meaning_key.local})"}),
        frozenset({f"CONTRACT_SPEC({meaning_key.local})"}),
    )
    ck_members = (
        _record("abi0", "ABI", (("version", ABI0),)),
        _record("TaskSpec.type", "TYPE_DECLARATION", (("declaration", task_type_declaration),)),
        _record("RepositorySnapshot.type", "TYPE_DECLARATION", (("declaration", snapshot_type_declaration),)),
        _record("task.literal", "LITERAL", (("value", TypedValue(task_type, "TASK", task)),)),
        _record("task_accepts.declaration", "DECLARATION", (("declaration", declaration),)),
        _record("task_accepts.binding", "BINDING", (("binding", binding),)),
        _record("task_accepts.model", "MODEL_CONTRACT", (("model", model),)),
        _record("predicates.capability", "CAPABILITY", (("descriptor", descriptor),)),
    )
    owner_members = {
        "capknow.audit.adapter-witness": (
            _record("witness.capability", "CAPABILITY", (("service", "CAP(witness)"),), owner="capknow.audit.adapter-witness"),
            _record("witness.certificate", "CERTIFICATE", (("certificate", "WENV"),), owner="capknow.audit.adapter-witness"),
        ),
        "capknow.audit.reasoner-validator": (
            _record("bounds.validator", "CAPABILITY", (("service", "CAP(validate_bounds)"),), owner="capknow.audit.reasoner-validator"),
            _record("witness.validator", "CAPABILITY", (("service", "CAP(validate_witness)"),), owner="capknow.audit.reasoner-validator"),
        ),
        "capknow.audit.authority-producer": tuple(
            _record(f"authority.fact.{name}", "AUTHORITY_FACT", (("fact", f"AF({name})"),), owner="capknow.audit.authority-producer")
            for name in ("b.1", "c.1", "c.2", "w.1", "w.2", "choice.1")
        ),
        "capknow.audit.authority-trust": tuple(
            _record(f"authority.certificate.{name}", "CERTIFICATE", (("certificate", f"AENV({name})"),), owner="capknow.audit.authority-trust")
            for name in ("b.1", "c.1", "c.2", "w.1", "w.2", "choice.1")
        ),
        "capknow.audit.authority-validator": (
            _record("authority.capability", "CAPABILITY", (("service", "CAP(authority)"),), owner="capknow.audit.authority-validator"),
        ),
    }
    packages = [_package("capknow.semantic", "PKG_CK", ck_members)]
    groups = [ck_members]
    for owner, members in owner_members.items():
        packages.append(_package(owner, "PKG_" + owner.rsplit(".", 1)[-1].upper(), members))
        groups.append(members)
    records = (
        *tuple(_package_record(package) for package in packages),
        *(record for group in groups for record in group),
    )
    universe = Universe(records, tuple(packages), CoreRequest(contract))
    expected = CoreReplay(
        Composition(frozenset(records), ()),
        Formation.WELL_FORMED,
        Closure.CLOSED,
        Evaluability.AVAILABLE,
        "COMPLETED",
        Eval(Truth.TRUE, frozenset({reference})),
    )
    return universe, expected


def _pair_universe() -> tuple[Universe, PairReplay]:
    graph = DependencyGraph(
        ("refresh_scope", "refresh_occurred"),
        (("refresh_scope", ()), ("refresh_occurred", ("refresh_scope",))),
        frozenset({"VALIDATION_CERTIFICATE(PCERT)", "VALIDATION_CAPABILITY(PVC)"}),
    )
    pair = PairContract(
        "PAIR(refresh)",
        "PCERT",
        graph,
        graph.validation_references,
        frozenset({"VALIDATION_CERTIFICATE(PCERT)", "VALIDATION_CAPABILITY(PVC)"}),
        frozenset({"PLUGIN_PRODUCER(CK)"}),
        frozenset({"PLUGIN_PRODUCER(PPK)"}),
        frozenset({"PLUGIN_PRODUCER(PVK)"}),
        frozenset({"EMBEDDING_POLICY_PRODUCER(TP)"}),
        "PLUGIN_PRODUCER(CK)",
    )
    ck_members = (
        _record("pair.refresh", "PAIR_DECLARATION", (("pair", "PAIR(refresh)"),)),
        _record("pair.refresh.binding", "PAIR_BINDING", (("admission", "INDEPENDENT_COHERENCE_PROOF"),)),
        _record("pair.refresh.bundle", "OCCURRENCE_BUNDLE", (("meaning", "T3_A1_MEANING_LIFT"),)),
    )
    proof_members = (
        _record("pair.refresh.certificate", "CERTIFICATE", (("certificate", "PCERT"),), owner="capknow.audit.pair-proof"),
    )
    validator_members = (
        _record("pair.refresh.validator", "CAPABILITY", (("capability", "PVC"),), owner="capknow.audit.pair-validator"),
        _record("pair.refresh.sound", "CONTRACT_SPEC", (("role", "SOUND_FRAGMENT"),), owner="capknow.audit.pair-validator"),
        _record("pair.refresh.complete", "CONTRACT_SPEC", (("role", "COMPLETE_FRAGMENT"),), owner="capknow.audit.pair-validator"),
        _record("pair.refresh.evidence", "CONTRACT_SPEC", (("role", "REQUIRED_EVIDENCE"),), owner="capknow.audit.pair-validator"),
        _record("pair.refresh.failure", "CONTRACT_SPEC", (("role", "SERVICE_FAILURE_BEHAVIOR"),), owner="capknow.audit.pair-validator"),
    )
    packages = (
        _package("capknow.semantic", "PKG_pair_CK", ck_members),
        _package("capknow.audit.pair-proof", "PKG_PPK", proof_members),
        _package("capknow.audit.pair-validator", "PKG_PVK", validator_members),
    )
    records = (
        *tuple(_package_record(package) for package in packages),
        *ck_members,
        *proof_members,
        *validator_members,
    )
    return (
        Universe(records, packages, PairRequest(pair)),
        PairReplay(
            Composition(frozenset(records), ()),
            Formation.WELL_FORMED,
            Closure.CLOSED,
            PairValidationResult("PAIR(refresh)", "PCERT", "PAIR_COHERENCE_ADMITTED"),
        ),
    )


def _trust_universe(state: TrustState) -> tuple[Universe, Judgment]:
    target = "Q_t[T_admitted]"
    failure = "PROTOCOL_OR_TRANSPORT" if state is TrustState.FAILED else None
    record = _record(
        f"trust.{state.value.lower()}",
        "TRUST_ENVIRONMENT",
        (("state", state.value), ("target", target)),
    )
    expected = {
        TrustState.ADMITTED: Judgment("INVOCABLE_FOR", (target,)),
        TrustState.ABSENT: Judgment("EVALUABILITY_MISSING"),
        TrustState.UNDECIDED: Judgment("EVALUABILITY_UNKNOWN"),
        TrustState.INCOMPATIBLE: Judgment("EVALUABILITY_MISSING"),
        TrustState.FAILED: Judgment("DISCOVERY_FAILED", (failure,)),
    }[state]
    package = _package("capknow.semantic", "PKG_CK", (record,))
    return (
        Universe((_package_record(package), record), (package,), TrustRequest(state, target, failure)),
        expected,
    )


def _missing_row(kind: MissingKind) -> tuple[Universe, Universe, LookupReplay, LookupReplay]:
    target = _record(
        f"missing.{kind.value.lower()}.target",
        kind.value,
        (("complete", True), ("row", kind.value)),
        owner="capknow.fixture",
        namespace="missing",
    )
    carrier = _record(
        f"missing.{kind.value.lower()}.carrier",
        "CARRIER",
        (("target", target.identity), ("state", "baseline")),
        owner="capknow.fixture",
        namespace="missing",
    )
    replacement = _record(
        f"missing.{kind.value.lower()}.carrier",
        "CARRIER",
        (("target", None), ("state", "reconstructed")),
        owner="capknow.fixture",
        namespace="missing",
    )
    replacement_extras: tuple[LogicalRecord, ...] = ()
    if kind is MissingKind.EXTRANEOUS_LEXICAL_BINDING:
        replacement_extras = (
            _record(
                "missing.extraneous_lexical_binding.lk_extra",
                "LEXICAL_BINDING",
                (("scope", "scope_extra"),),
                owner="capknow.fixture",
                namespace="missing",
            ),
        )
    elif kind is MissingKind.LIFECYCLE:
        replacement_extras = (
            _record(
                "missing.lifecycle.alternate",
                "LIFECYCLE",
                (("request", "R_c_alt"), ("state", "L_life_after")),
                owner="capknow.fixture",
                namespace="missing",
            ),
        )
    elif kind is MissingKind.CONFLICT:
        replacement_extras = (
            _record(
                "missing.conflict.alternate",
                "CONFLICT",
                (("conflict", "conflict1"),),
                owner="capknow.fixture",
                namespace="missing",
            ),
        )
    baseline_members = (target, carrier)
    variant_members = (replacement, *replacement_extras)
    package_local = f"PKG_missing_{kind.value.lower()}"
    baseline_package = _package("capknow.fixture", package_local, baseline_members)
    variant_package = _package("capknow.fixture", package_local, variant_members)
    baseline_records = (_package_record(baseline_package), *baseline_members)
    variant_records = (_package_record(variant_package), *variant_members)
    baseline = Universe(
        baseline_records,
        (baseline_package,),
        LookupRequest(target.identity, kind),
    )
    variant = Universe(
        variant_records,
        (variant_package,),
        LookupRequest(target.identity, kind),
    )
    return (
        baseline,
        variant,
        LookupReplay(Composition(frozenset(baseline_records), ()), Judgment("PRESENT", (target,))),
        LookupReplay(Composition(frozenset(variant_records), ()), _missing_judgment(kind)),
    )


def _missing_judgment(kind: MissingKind) -> Judgment:
    malformed = {
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
    }
    if kind in malformed:
        return Judgment("MALFORMED")
    values = {
        MissingKind.BINDING: Judgment("OPEN_BINDINGS"),
        MissingKind.PROFILE_BINDING: Judgment("OPEN_BINDINGS"),
        MissingKind.PAIR_BINDING: Judgment("OPEN_BINDINGS"),
        MissingKind.AUTHORITY_FACT: Judgment("OPEN_BINDINGS", ("AUTHORITY_FACT(AF(choice,1))",)),
        MissingKind.CHOICE_BINDING: Judgment("OPEN_BINDINGS", ("CHOICE_BINDING(cb0)",)),
        MissingKind.LEXICAL_BINDING: Judgment("OPEN_BINDINGS", ("LEXICAL_BINDING(lk0)",)),
        MissingKind.EXTRANEOUS_LEXICAL_BINDING: Judgment("MALFORMED_REQUEST", ("EXTRANEOUS_LEXICAL_BINDING(lk_extra)",)),
        MissingKind.SERVICE: Judgment("EVALUABILITY_MISSING"),
        MissingKind.CAPABILITY: Judgment("EVALUABILITY_MISSING"),
        MissingKind.TRUST_POLICY: Judgment("TRUST_ROOT_ABSENT"),
        MissingKind.TRUST_ROOT: Judgment("TRUST_ROOT_ABSENT", ("TR",)),
        MissingKind.CERTIFICATE: Judgment("NO_CERTIFICATE_ADMISSION", ("CONSISTENCY_UNKNOWN",)),
        MissingKind.MIGRATION: Judgment("NO_MIGRATION", ("MK0",)),
        MissingKind.COMPATIBILITY_CLAIM: Judgment("NO_COMPATIBILITY", ("CCK0",)),
        MissingKind.EXTENSION_OPTIONAL: Judgment("NO_EFFECT", ("XK0",)),
        MissingKind.EXTENSION_REQUIRED: Judgment("INCOMPATIBLE", ("XK1",)),
        MissingKind.MODEL_CONTRACT: Judgment("OPEN_BINDINGS", ("MODEL_CONTRACT",)),
        MissingKind.ALIAS_OPTIONAL: Judgment("NO_ALIAS", ("AK0",)),
        MissingKind.ALIAS_REQUIRED: Judgment("MALFORMED", ("MISSING_ALIAS(AK1)",)),
        MissingKind.SIGMA_CONTRACT_SPEC: Judgment("BINDING_INCOMPATIBLE", ("OPEN_BINDINGS",)),
        MissingKind.SERVICE_CONTRACT_SPEC: Judgment("CAPABILITY_INCOMPATIBLE", ("EVALUABILITY_MISSING",)),
        MissingKind.REQUEST: Judgment("MALFORMED_REQUEST"),
        MissingKind.RESULT: Judgment("INVOCATION_FAILED", ("PROTOCOL", "fr_noresult", "NO_TRUTH")),
        MissingKind.SEMANTIC_ENVIRONMENT: Judgment("MALFORMED_REQUEST", ("IDENTITY_OF(Q_t[T_admitted])",)),
        MissingKind.TRUST_ENVIRONMENT: Judgment("MALFORMED_REQUEST", ("IDENTITY_OF(Q_t[T_admitted])",)),
        MissingKind.DEPENDENCY_ENVIRONMENT: Judgment("MALFORMED_REQUEST", ("IDENTITY_OF(Q_t[T_admitted])",)),
        MissingKind.OBSERVATION_ENVIRONMENT: Judgment("MALFORMED_RESULT", ("SEMANTIC_MISMATCH",)),
        MissingKind.LIFECYCLE: Judgment("LIFECYCLE_REPLACED", ("R_c_alt", "L_life_after", "INVOCABLE_FOR(R_c_alt)")),
        MissingKind.EVIDENCE: Judgment("TRUTH_UNKNOWN"),
        MissingKind.REASON: Judgment("MALFORMED_RESULT", ("MALFORMED_CARRIER",)),
        MissingKind.CONFLICT: Judgment("CONFLICT_REPLACED", ("conflict1", "MALFORMED")),
    }
    return values[kind]


def _confluence_universe(order: OrderTag) -> tuple[Universe, ObservationEvaluation]:
    source = ArtifactContent("SOURCE", "PYTHON", 1, "old")
    changed = ArtifactContent("SOURCE", "PYTHON", 2, "new")
    before = RepositorySnapshot((("src/a.py", source),))
    final = RepositorySnapshot((("src/a.py", changed),))
    spec = ObservationSpec("s_c", ArtifactSelector(role="SOURCE"), "IDENTITY")
    graph = DependencyGraph(("N_o", "N_d"), (("N_o", ()), ("N_d", ())))
    nodes = (
        ObservationNode("N_o", NodeOperation.OBSERVE, (spec, final), ObservationKind.TERM_RESULT),
        ObservationNode("N_d", NodeOperation.CHANGES_BETWEEN, (before, final), ObservationKind.TERM_RESULT),
    )
    preferred = ("N_o", "N_d") if order is OrderTag.FORWARD else ("N_d", "N_o")
    observations = (
        (
            "N_d",
            TermResult(value=ChangeSet((ChangeEntry("src/a.py", ChangeKind.MODIFIED, source, changed),))),
        ),
        ("N_o", TermResult(value=ObservationResult("s_c", (("src/a.py", "new"),)))),
    )
    expected = ObservationEvaluation(
        observations,
        Judgment("COMPLETED_INCONCLUSIVE"),
        "COMPLETED",
        ("WELL_FORMED", "CLOSED", "EVALUABILITY_AVAILABLE", "COMPLETED", "CONSISTENCY_UNKNOWN"),
    )
    record = _record("confluence.request", "REQUEST", (("order", order.value),))
    package = _package("capknow.semantic", "PKG_CK", (record,))
    return (
        Universe(
            (_package_record(package), record),
            (package,),
            GraphEvaluationRequest(graph, nodes, preferred),
        ),
        expected,
    )


def _cycle_universe() -> tuple[Universe, tuple[Any, ...]]:
    graph = DependencyGraph(
        ("event_matches", "event_occurred"),
        (("event_matches", ("event_occurred",)), ("event_occurred", ("event_matches",))),
    )
    records = (
        _record("cycle.event_matches", "BINDING", (("depends", "event_occurred"),)),
        _record("cycle.event_occurred", "BINDING", (("depends", "event_matches"),)),
    )
    expected = (
        Formation.MALFORMED,
        Closure.NOT_APPLICABLE,
        Judgment("MALFORMED", ("dependency cycle",)),
    )
    package = _package("capknow.semantic", "PKG_CK", records)
    all_records = (_package_record(package), *records)
    return Universe(all_records, (package,), FormationRequest(graph)), expected


def _permutation_universe(
    package_order: PackageOrderTag, record_order: RecordOrderTag
) -> tuple[Universe, CompositionReplay]:
    pi1_declaration = _record("pi1.declaration", "DECLARATION", (("symbol", "pi1"),))
    pi1_specification = _record("pi1.specification", "CONTRACT_SPEC", (("role", "PREDICATE_MEANING"),))
    pi2_declaration = _record("pi2.declaration", "DECLARATION", (("symbol", "pi2"),))
    pi2_specification = _record("pi2.specification", "CONTRACT_SPEC", (("role", "PREDICATE_MEANING"),))
    pi1 = (pi1_declaration, pi1_specification)
    pi2 = (pi2_declaration, pi2_specification)
    if record_order is RecordOrderTag.SPEC_THEN_DECLARATION:
        pi1 = tuple(reversed(pi1))
        pi2 = tuple(reversed(pi2))
    package_pi1 = _package("capknow.semantic", "PKG_pi1", (pi1_declaration, pi1_specification))
    package_pi2 = _package("capknow.semantic", "PKG_pi2", (pi2_declaration, pi2_specification))
    presentation_pi1 = (_package_record(package_pi1), *pi1)
    presentation_pi2 = (_package_record(package_pi2), *pi2)
    if package_order is PackageOrderTag.PI1_PI2:
        presentations = (presentation_pi1, presentation_pi2)
        packages = (package_pi1, package_pi2)
    else:
        presentations = (presentation_pi2, presentation_pi1)
        packages = (package_pi2, package_pi1)
    records = tuple(record for group in presentations for record in group)
    composition = Composition(
        frozenset(
            {
                _package_record(package_pi1),
                _package_record(package_pi2),
                pi1_declaration,
                pi1_specification,
                pi2_declaration,
                pi2_specification,
            }
        ),
        (),
    )
    expected = CompositionReplay(composition, Formation.WELL_FORMED, Closure.CLOSED)
    return Universe(records, packages, CompositionRequest(presentations)), expected


def _duplicate_universe(
    conflict: bool, order: OrderTag
) -> tuple[Universe, CompositionReplay]:
    declaration = _record(
        "duplicate.task_accepts",
        "DECLARATION",
        (("facets", ((), ("final",), ("evidence",))),),
    )
    other = declaration if not conflict else LogicalRecord(
        declaration.identity,
        declaration.record_kind,
        (("facets", ((), (), ("evidence",))),),
    )
    records = (declaration, other) if order is OrderTag.FORWARD else (other, declaration)
    if conflict:
        composition = Composition(
            frozenset(),
            (ConflictRef(declaration.identity, frozenset({declaration, other})),),
        )
        expected = CompositionReplay(composition, Formation.MALFORMED, Closure.NOT_APPLICABLE)
    else:
        composition = Composition(frozenset({declaration}), ())
        expected = CompositionReplay(composition, Formation.WELL_FORMED, Closure.CLOSED)
    return Universe(records, (), CompositionRequest((records,))), expected


def _build_packet() -> tuple[dict[FixtureId, Universe], dict[FixtureId, Any]]:
    packet: dict[FixtureId, Universe] = {}
    assertions: dict[FixtureId, Any] = {}

    core_id = FixtureId(FixtureFamily.CORE_DEFINITIONAL)
    packet[core_id], assertions[core_id] = _core_universe()
    pair_id = FixtureId(FixtureFamily.PAIR_INDEPENDENT)
    packet[pair_id], assertions[pair_id] = _pair_universe()

    for state in TrustState:
        key = FixtureId(FixtureFamily.TRUST_BRANCH, (state,))
        packet[key], assertions[key] = _trust_universe(state)

    missing_rows = {kind: _missing_row(kind) for kind in MissingKind}
    for kind in MissingKind:
        key = FixtureId(FixtureFamily.MISSING_BASE, (kind,))
        packet[key], _, assertions[key], _ = missing_rows[kind]
    for kind in MissingKind:
        key = FixtureId(FixtureFamily.MISSING_VARIANT, (kind,))
        _, packet[key], _, assertions[key] = missing_rows[kind]

    for order in OrderTag:
        key = FixtureId(FixtureFamily.CONFLUENCE_ORDER, (order,))
        packet[key], assertions[key] = _confluence_universe(order)

    cycle_id = FixtureId(FixtureFamily.PROPER_CYCLE_REJECTION)
    packet[cycle_id], assertions[cycle_id] = _cycle_universe()

    for package_order in PackageOrderTag:
        for record_order in RecordOrderTag:
            key = FixtureId(FixtureFamily.PERMUTATION, (package_order, record_order))
            packet[key], assertions[key] = _permutation_universe(package_order, record_order)

    for order in OrderTag:
        key = FixtureId(FixtureFamily.DUPLICATE_EQUAL, (order,))
        packet[key], assertions[key] = _duplicate_universe(False, order)
    for order in OrderTag:
        key = FixtureId(FixtureFamily.DUPLICATE_CONFLICT, (order,))
        packet[key], assertions[key] = _duplicate_universe(True, order)
    return packet, assertions


FIXTURE_PACKET_X, FIXTURE_EXPECTED_X = _build_packet()
