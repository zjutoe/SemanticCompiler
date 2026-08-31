"""Pure finite coding meanings admitted by the accepted K3-S packet.

The values in this module are logical data.  No operation observes or changes
the host repository.  Unsupported projections and relations fail before a
semantic result is produced.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable


class FiniteCodingProfileError(NotImplementedError):
    """The requested value or relation is outside the finite K3-X profile."""


class UndeclaredAccessError(ValueError):
    """A meaning requested a facet absent from its exact access contract."""


class Truth(Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"


class VerificationStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


class ChangeKind(Enum):
    CREATED = "CREATED"
    DELETED = "DELETED"
    MODIFIED = "MODIFIED"


class CriterionKind(Enum):
    OBSERVATION_EQUALS = "OBSERVATION_EQUALS"
    ONE_FORMAT_OF = "ONE_FORMAT_OF"
    ARTIFACTS_NONEMPTY = "ARTIFACTS_NONEMPTY"
    ARTIFACT_SIZE_LT = "ARTIFACT_SIZE_LT"
    ARTIFACT_SIZE_AT_LEAST = "ARTIFACT_SIZE_AT_LEAST"
    UNIVERSAL_OBSERVATION = "UNIVERSAL_OBSERVATION"
    DEPENDENCY_REPRODUCIBLE = "DEPENDENCY_REPRODUCIBLE"
    ADAPTER_CORRESPONDS = "ADAPTER_CORRESPONDS"


class EventKind(Enum):
    COMMAND = "command"
    TEST = "test"
    PATH_CHANGE = "path_change"
    NETWORK_CONTACT = "network_contact"
    RELEASE = "release"
    DEPENDENCY_REFRESH = "dependency_refresh"


class PatternKind(Enum):
    ANY_EVENT = "ANY_EVENT"
    COMMAND_IS = "COMMAND_IS"
    TEST_IS = "TEST_IS"
    PATH_CHANGE_IN = "PATH_CHANGE_IN"
    NETWORK_CLASS = "NETWORK_CLASS"
    RELEASE_IS = "RELEASE_IS"
    REFRESHES = "REFRESHES"


@dataclass(frozen=True)
class ArtifactContent:
    role: str
    format: str
    size_kib: int
    content_identity: str
    body: tuple[tuple[str, Any], ...] = ()

    def __post_init__(self) -> None:
        if self.size_kib < 0:
            raise ValueError("artifact size must be non-negative")


@dataclass(frozen=True)
class RepositorySnapshot:
    entries: tuple[tuple[str, ArtifactContent], ...]

    def __post_init__(self) -> None:
        paths = tuple(path for path, _ in self.entries)
        if len(paths) != len(set(paths)):
            raise ValueError("snapshot contains a duplicate path")

    def as_map(self) -> dict[str, ArtifactContent]:
        return dict(self.entries)


@dataclass(frozen=True)
class ArtifactSelector:
    paths: frozenset[str] = frozenset()
    role: str | None = None


@dataclass(frozen=True)
class ObservationSpec:
    identity: str
    selector: ArtifactSelector
    projection: str


@dataclass(frozen=True)
class ObservationResult:
    spec_identity: str
    rows: tuple[tuple[str, Any], ...]
    complete: bool = True


@dataclass(frozen=True)
class ChangeEntry:
    path: str
    kind: ChangeKind
    old: ArtifactContent | None
    new: ArtifactContent | None


@dataclass(frozen=True)
class ChangeSet:
    entries: tuple[ChangeEntry, ...]


@dataclass(frozen=True)
class TermResult:
    value: Any = None
    error: str | None = None

    @property
    def is_value(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class Eval:
    truth: Truth | None
    evidence_refs: frozenset[str] = frozenset()
    reasons: frozenset[str] = frozenset()
    error: str | None = None

    def __post_init__(self) -> None:
        if (self.truth is None) == (self.error is None):
            raise ValueError("Eval is exactly one of VALUE or ERROR")


@dataclass(frozen=True)
class VerificationSpec:
    identity: str
    subject: ObservationSpec


@dataclass(frozen=True)
class VerificationRecord:
    spec: VerificationSpec
    snapshot_identity: str
    status: VerificationStatus
    observation: ObservationResult
    evidence_refs: frozenset[str]


@dataclass(frozen=True)
class EvidenceEntry:
    reference: str
    schema: str
    payload: Any


@dataclass(frozen=True)
class Criterion:
    kind: CriterionKind
    arguments: tuple[Any, ...]


@dataclass(frozen=True)
class TaskSpec:
    criteria: tuple[Criterion, ...] = ()
    required_verifications: tuple[VerificationSpec, ...] = ()


@dataclass(frozen=True)
class EventValue:
    kind: EventKind
    payload: tuple[tuple[str, Any], ...]

    def fields(self) -> dict[str, Any]:
        return dict(self.payload)


@dataclass(frozen=True)
class EventPattern:
    kind: PatternKind
    arguments: tuple[Any, ...]


@dataclass(frozen=True)
class ProfileResult:
    status: str
    dimensions: tuple[tuple[str, str], ...] = ()
    error: str | None = None


def snapshot_identity(snapshot: RepositorySnapshot) -> tuple[Any, ...]:
    """Return the exact structural identity of an admitted snapshot."""
    return tuple(sorted(snapshot.entries, key=lambda item: item[0]))


def snapshot_of(state: Any) -> TermResult:
    if isinstance(state, RepositorySnapshot):
        return TermResult(value=state)
    return TermResult(error="NOT_A_REPOSITORY_SNAPSHOT")


def changes_between(
    before: RepositorySnapshot, after: RepositorySnapshot
) -> TermResult:
    if not isinstance(before, RepositorySnapshot) or not isinstance(
        after, RepositorySnapshot
    ):
        return TermResult(error="NOT_A_REPOSITORY_SNAPSHOT")
    old = before.as_map()
    new = after.as_map()
    changes: list[ChangeEntry] = []
    for path in sorted(set(old) | set(new)):
        if path not in old:
            changes.append(ChangeEntry(path, ChangeKind.CREATED, None, new[path]))
        elif path not in new:
            changes.append(ChangeEntry(path, ChangeKind.DELETED, old[path], None))
        elif old[path] != new[path]:
            changes.append(
                ChangeEntry(path, ChangeKind.MODIFIED, old[path], new[path])
            )
    return TermResult(value=ChangeSet(tuple(changes)))


def _selected(
    selector: ArtifactSelector, snapshot: RepositorySnapshot
) -> tuple[tuple[str, ArtifactContent], ...]:
    selected = []
    for path, artifact in snapshot.entries:
        if selector.paths and path not in selector.paths:
            continue
        if selector.role is not None and artifact.role != selector.role:
            continue
        selected.append((path, artifact))
    return tuple(sorted(selected, key=lambda item: item[0]))


def observe(spec: ObservationSpec, snapshot: RepositorySnapshot) -> TermResult:
    if not isinstance(spec, ObservationSpec) or not isinstance(
        snapshot, RepositorySnapshot
    ):
        return TermResult(error="INVALID_OBSERVATION_INPUT")
    selected = _selected(spec.selector, snapshot)
    if spec.projection == "IDENTITY":
        rows = tuple((path, item.content_identity) for path, item in selected)
    elif spec.projection == "FORMAT":
        rows = tuple((path, item.format) for path, item in selected)
    elif spec.projection == "SIZE":
        rows = tuple((path, item.size_kib) for path, item in selected)
    elif spec.projection == "CONTENT":
        rows = tuple(selected)
    else:
        raise FiniteCodingProfileError(
            f"unsupported observation projection: {spec.projection}"
        )
    return TermResult(value=ObservationResult(spec.identity, rows))


def observations_equal(left: ObservationResult, right: ObservationResult) -> Eval:
    if not isinstance(left, ObservationResult) or not isinstance(
        right, ObservationResult
    ):
        return Eval(None, error="INVALID_OBSERVATION_RESULT")
    truth = Truth.TRUE if left == right else Truth.FALSE
    return Eval(truth)


def _evidence_map(
    entries: Iterable[EvidenceEntry],
) -> tuple[dict[str, EvidenceEntry] | None, str | None]:
    grouped: dict[str, set[EvidenceEntry]] = {}
    for entry in entries:
        if not isinstance(entry, EvidenceEntry):
            return None, "EVIDENCE_SCHEMA_ERROR"
        grouped.setdefault(entry.reference, set()).add(entry)
    if any(len(values) != 1 for values in grouped.values()):
        return None, "EVIDENCE_REFERENCE_CONFLICT"
    return {reference: next(iter(values)) for reference, values in grouped.items()}, None


def verification_passed(
    spec: VerificationSpec,
    snapshot: RepositorySnapshot,
    evidence: tuple[EvidenceEntry, ...],
) -> Eval:
    evidence_map, error = _evidence_map(evidence)
    if error is not None:
        return Eval(None, error=error)
    assert evidence_map is not None
    matching: list[tuple[str, VerificationRecord]] = []
    current_identity = repr(snapshot_identity(snapshot))
    for reference, entry in evidence_map.items():
        if entry.schema != "verification":
            continue
        if not isinstance(entry.payload, VerificationRecord):
            return Eval(None, error="EVIDENCE_SCHEMA_ERROR")
        record = entry.payload
        if reference not in record.evidence_refs:
            return Eval(None, error="EVIDENCE_REFERENCE_ERROR")
        if (
            record.spec == spec
            and record.snapshot_identity == current_identity
            and record.observation.spec_identity == spec.subject.identity
        ):
            matching.append((reference, record))
    statuses = {record.status for _, record in matching}
    refs = frozenset(reference for reference, _ in matching)
    if VerificationStatus.PASS in statuses and VerificationStatus.FAIL in statuses:
        return Eval(None, error="OPPOSITE_DECISIVE_RECORD_CONFLICT")
    reasons = frozenset(
        f"INCONCLUSIVE:{reference}"
        for reference, record in matching
        if record.status is VerificationStatus.INCONCLUSIVE
    )
    if VerificationStatus.FAIL in statuses:
        return Eval(Truth.FALSE, refs, reasons)
    if VerificationStatus.PASS in statuses:
        return Eval(Truth.TRUE, refs, reasons)
    if not reasons:
        reasons = frozenset({f"MISSING_VERIFICATION:{spec.identity}"})
    return Eval(Truth.UNKNOWN, refs, reasons)


def _criterion_result(
    criterion: Criterion,
    snapshot: RepositorySnapshot,
) -> Eval:
    args = criterion.arguments
    if criterion.kind is CriterionKind.OBSERVATION_EQUALS:
        spec, expected = args
        current = observe(spec, snapshot)
        return observations_equal(current.value, expected) if current.is_value else Eval(
            None, error=current.error
        )
    if criterion.kind in {
        CriterionKind.ONE_FORMAT_OF,
        CriterionKind.ARTIFACTS_NONEMPTY,
        CriterionKind.ARTIFACT_SIZE_LT,
        CriterionKind.ARTIFACT_SIZE_AT_LEAST,
    }:
        selector = args[0]
        population = _selected(selector, snapshot)
        if not population:
            return Eval(Truth.FALSE)
        if criterion.kind is CriterionKind.ARTIFACTS_NONEMPTY:
            return Eval(Truth.TRUE)
        if criterion.kind is CriterionKind.ONE_FORMAT_OF:
            formats = args[1]
            answer = all(item.format in formats for _, item in population)
        elif criterion.kind is CriterionKind.ARTIFACT_SIZE_LT:
            answer = all(item.size_kib < args[1] for _, item in population)
        else:
            answer = all(item.size_kib >= args[1] for _, item in population)
        return Eval(Truth.TRUE if answer else Truth.FALSE)
    if criterion.kind is CriterionKind.UNIVERSAL_OBSERVATION:
        spec, baseline, relation = args
        current = observe(spec, snapshot)
        if not current.is_value:
            return Eval(None, error=current.error)
        if relation == "EQUAL":
            return observations_equal(current.value, baseline)
        raise FiniteCodingProfileError(f"unsupported observation relation: {relation}")
    if criterion.kind in {
        CriterionKind.DEPENDENCY_REPRODUCIBLE,
        CriterionKind.ADAPTER_CORRESPONDS,
    }:
        spec = args[0]
        current = observe(spec, snapshot)
        if not current.is_value:
            return Eval(None, error=current.error)
        result = current.value
        if not result.complete:
            return Eval(Truth.UNKNOWN, reasons=frozenset({"INCOMPLETE_DOMAIN"}))
        values = tuple(value for _, value in result.rows)
        if criterion.kind is CriterionKind.DEPENDENCY_REPRODUCIBLE:
            answer = len(values) >= 2 and len(set(values)) == 1
        else:
            if len(args) != 2 or args[1] != "FIELD_CORRESPONDENCE":
                raise FiniteCodingProfileError("unsupported adapter relation")
            answer = len(values) == 2 and values[0] == values[1]
        return Eval(Truth.TRUE if answer else Truth.FALSE)
    raise FiniteCodingProfileError(f"unsupported criterion: {criterion.kind}")


def _conjoin(results: Iterable[Eval]) -> Eval:
    values = tuple(results)
    errors = tuple(value.error for value in values if value.error is not None)
    if errors:
        return Eval(None, error=";".join(sorted(set(errors))))
    evidence = frozenset().union(*(value.evidence_refs for value in values))
    reasons = frozenset().union(*(value.reasons for value in values))
    truths = {value.truth for value in values}
    if Truth.FALSE in truths:
        return Eval(Truth.FALSE, evidence, reasons)
    if Truth.UNKNOWN in truths:
        return Eval(Truth.UNKNOWN, evidence, reasons)
    return Eval(Truth.TRUE, evidence, reasons)


def task_accepts(
    task: TaskSpec,
    final: RepositorySnapshot,
    evidence: tuple[EvidenceEntry, ...],
) -> Eval:
    if not isinstance(task, TaskSpec) or not isinstance(final, RepositorySnapshot):
        return Eval(None, error="INVALID_TASK_INPUT")
    criterion_results = (
        _criterion_result(criterion, final) for criterion in task.criteria
    )
    verification_results = (
        verification_passed(spec, final, evidence)
        for spec in task.required_verifications
    )
    return _conjoin((*criterion_results, *verification_results))


def dependency_metadata_changed(changes: ChangeSet) -> Eval:
    for entry in changes.entries:
        old_metadata = entry.old is not None and entry.old.role == "DEPENDENCY_METADATA"
        new_metadata = entry.new is not None and entry.new.role == "DEPENDENCY_METADATA"
        if old_metadata or new_metadata:
            return Eval(Truth.TRUE)
    return Eval(Truth.FALSE)


def event_matches(pattern: EventPattern, event: EventValue) -> Eval:
    fields = event.fields()
    args = pattern.arguments
    if pattern.kind is PatternKind.ANY_EVENT:
        answer = event.kind is args[0]
    elif pattern.kind is PatternKind.COMMAND_IS:
        answer = event.kind is EventKind.COMMAND and fields.get("command_id") == args[0]
    elif pattern.kind is PatternKind.TEST_IS:
        answer = (
            event.kind is EventKind.TEST
            and fields.get("spec") == args[0]
            and fields.get("status") in args[1]
        )
    elif pattern.kind is PatternKind.PATH_CHANGE_IN:
        answer = (
            event.kind is EventKind.PATH_CHANGE
            and fields.get("path") in args[0]
            and fields.get("change_kind") in args[1]
        )
    elif pattern.kind is PatternKind.NETWORK_CLASS:
        answer = event.kind is EventKind.NETWORK_CONTACT and fields.get(
            "contact_class"
        ) == args[0]
    elif pattern.kind is PatternKind.RELEASE_IS:
        answer = (
            event.kind is EventKind.RELEASE
            and fields.get("release_id") == args[0]
            and fields.get("snapshot_identity") == args[1]
        )
    elif pattern.kind is PatternKind.REFRESHES:
        answer = (
            event.kind is EventKind.DEPENDENCY_REFRESH
            and fields.get("selector") == args[0]
            and fields.get("snapshot_identity") == args[1]
        )
    else:
        raise FiniteCodingProfileError(f"unsupported event pattern: {pattern.kind}")
    return Eval(Truth.TRUE if answer else Truth.FALSE)


def event_occurred(pattern: EventPattern, trace: frozenset[EventValue]) -> Eval:
    results = tuple(event_matches(pattern, event) for event in trace)
    if any(result.error is not None for result in results):
        return Eval(None, error="EVENT_MATCH_ERROR")
    return Eval(
        Truth.TRUE if any(result.truth is Truth.TRUE for result in results) else Truth.FALSE
    )


def refresh_scope(event: EventValue) -> Eval:
    fields = event.fields()
    answer = (
        event.kind is EventKind.DEPENDENCY_REFRESH
        and isinstance(fields.get("selector"), ArtifactSelector)
        and fields["selector"].role == "DEPENDENCY_LOCK"
    )
    return Eval(Truth.TRUE if answer else Truth.FALSE)


def implementation_evidence_profile(
    task_result: Eval,
    direct_result: Eval,
    entries: tuple[EvidenceEntry, ...],
) -> ProfileResult:
    if task_result != direct_result:
        return ProfileResult("EVALUATION_ERROR", error="TASK_RESULT_MISMATCH")
    evidence_map, error = _evidence_map(entries)
    if error is not None:
        return ProfileResult("EVALUATION_ERROR", error=error)
    assert evidence_map is not None
    abstract = any(entry.schema == "abstract_acceptance" for entry in evidence_map.values())
    concrete = any(entry.schema == "concrete_implementation" for entry in evidence_map.values())
    dimensions = (
        ("abstract_acceptance_evidence", "COVERED" if abstract else "MISSING"),
        ("concrete_implementation_evidence", "COVERED" if concrete else "MISSING"),
    )
    status = "PROFILE_COMPLETE" if abstract and concrete else "PROFILE_INCOMPLETE"
    return ProfileResult(status, dimensions)


def enforce_declared_access(
    requested_facets: frozenset[str], allowed_facets: frozenset[str]
) -> None:
    undeclared = requested_facets - allowed_facets
    if undeclared:
        raise UndeclaredAccessError(
            "UNDECLARED_ACCESS:" + ",".join(sorted(undeclared))
        )


def invoke_with_declared_access(
    requested_facets: frozenset[str],
    allowed_facets: frozenset[str],
    meaning: Any,
    arguments: tuple[Any, ...],
) -> Any:
    """Check the exact access boundary before invoking a supplied pure meaning."""
    enforce_declared_access(requested_facets, allowed_facets)
    if not callable(meaning):
        raise TypeError("meaning must be callable")
    return meaning(*arguments)
