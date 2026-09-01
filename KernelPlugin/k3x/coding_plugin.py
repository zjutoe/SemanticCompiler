"""Closed, pure coding semantics for the accepted finite K3-S slice."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Iterable


class FiniteCodingProfileError(NotImplementedError):
    """The supplied constructor or relation is outside the finite profile."""


class UndeclaredAccessError(ValueError):
    """A meaning requested a facet absent from its exact access contract."""


class Truth(Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"


class ArtifactRole(Enum):
    SOURCE = "SOURCE"
    DEPENDENCY_METADATA = "DEPENDENCY_METADATA"
    DEPENDENCY_LOCK = "DEPENDENCY_LOCK"
    MIGRATION = "MIGRATION"
    BUNDLE = "BUNDLE"
    CONFIGURATION = "CONFIGURATION"
    PUBLIC_SCHEMA = "PUBLIC_SCHEMA"


@dataclass(frozen=True, order=True)
class OtherArtifactRole:
    """The closed K3-S OTHER_ROLE(atom) constructor."""

    atom: str

    def __post_init__(self) -> None:
        if type(self.atom) is not str or not self.atom:
            raise ValueError("OTHER_ROLE atom is nonempty")


class Format(Enum):
    TOML = "TOML"
    YAML = "YAML"
    JSON = "JSON"
    TEXT = "TEXT"
    BINARY = "BINARY"


@dataclass(frozen=True, order=True)
class OtherFormat:
    """The closed K3-S OTHER_FORMAT(atom) constructor."""

    atom: str

    def __post_init__(self) -> None:
        if type(self.atom) is not str or not self.atom:
            raise ValueError("OTHER_FORMAT atom is nonempty")


class ArtifactTag(Enum):
    TEXT = "TEXT_ARTIFACT"
    STRUCTURED = "STRUCTURED_ARTIFACT"
    OPAQUE = "OPAQUE_ARTIFACT"
    BEHAVIOR = "BEHAVIOR_ARTIFACT"


class ArtifactBodyKind(Enum):
    TEXT = "TEXT_BODY_KIND"
    STRUCTURED = "STRUCTURED_BODY_KIND"
    OPAQUE = "OPAQUE_BODY_KIND"
    BEHAVIOR = "BEHAVIOR_BODY_KIND"


class SelectorTag(Enum):
    PATHS = "SELECT_PATHS"
    ROLE = "SELECT_ROLE"
    PATHS_WITH_ROLE = "SELECT_PATHS_WITH_ROLE"


class ProjectionTag(Enum):
    PRESENCE = "PRESENCE"
    CONTENT = "CONTENT"
    FORMAT_ONLY = "FORMAT_ONLY"
    SIZE_ONLY = "SIZE_ONLY"
    STRUCTURED_FIELD = "STRUCTURED_FIELD"


class SubjectTag(Enum):
    REQUEST = "REQUEST_SUBJECT"
    WORKLOAD = "WORKLOAD_SUBJECT"
    RESOLUTION_LANE = "RESOLUTION_LANE"
    CLIENT_PAIR = "CLIENT_PAIR"


class BehaviorTag(Enum):
    ACCEPTED = "BEHAVIOR_ACCEPTED"
    REJECTED = "BEHAVIOR_REJECTED"
    METRIC = "BEHAVIOR_METRIC"
    RESOLUTION = "BEHAVIOR_RESOLUTION"
    CORRESPONDENCE = "BEHAVIOR_CORRESPONDENCE"


class ObservationSpecTag(Enum):
    ARTIFACT_VIEW = "ARTIFACT_VIEW"
    REQUEST_BEHAVIOR_VIEW = "REQUEST_BEHAVIOR_VIEW"
    WORKLOAD_METRIC_VIEW = "WORKLOAD_METRIC_VIEW"
    DEPENDENCY_RESOLUTION_VIEW = "DEPENDENCY_RESOLUTION_VIEW"
    CLIENT_ADAPTER_VIEW = "CLIENT_ADAPTER_VIEW"


class ObservationValueTag(Enum):
    ABSENT = "ABSENT"
    ROLE_MISMATCH = "ROLE_MISMATCH"
    PROJECTION_MISMATCH = "PROJECTION_MISMATCH"
    PRESENT = "PRESENT"
    PRESENT_CONTENT = "PRESENT_CONTENT"
    PRESENT_FORMAT = "PRESENT_FORMAT"
    PRESENT_SIZE = "PRESENT_SIZE"
    PRESENT_FIELD = "PRESENT_FIELD"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    METRIC_VALUE = "METRIC_VALUE"
    RESOLUTION_VALUE = "RESOLUTION_VALUE"
    CORRESPONDENCE_VALUE = "CORRESPONDENCE_VALUE"
    BEHAVIOR_CONFLICT = "BEHAVIOR_CONFLICT"


class ObservationResultTag(Enum):
    ARTIFACT = "ARTIFACT_RESULT"
    SUBJECT = "SUBJECT_RESULT"
    LANE = "LANE_RESULT"
    CORRESPONDENCE = "CORRESPONDENCE_RESULT"


class CoverageTag(Enum):
    COMPLETE = "COMPLETE"
    INCOMPLETE_SUBJECTS = "INCOMPLETE_SUBJECTS"


class ObservationRelationTag(Enum):
    EQUAL = "EQUAL"
    ACCEPT_REJECT_EQUAL = "ACCEPT_REJECT_EQUAL"
    NO_GREATER = "NO_GREATER"
    STRICTLY_LOWER = "STRICTLY_LOWER"
    FIELD_CORRESPONDENCE = "FIELD_CORRESPONDENCE"


class VerificationStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


class ChangeKind(Enum):
    CREATED = "CREATED_KIND"
    DELETED = "DELETED_KIND"
    MODIFIED = "MODIFIED_KIND"


class EvidencePayloadTag(Enum):
    VERIFICATION = "VERIFICATION_EVIDENCE"
    IMPLEMENTATION_PROFILE = "IMPLEMENTATION_PROFILE_EVIDENCE"


class ImplementationEvidenceTag(Enum):
    ABSTRACT_ACCEPTANCE = "ABSTRACT_ACCEPTANCE_EVIDENCE"
    CONCRETE_IMPLEMENTATION = "CONCRETE_IMPLEMENTATION_EVIDENCE"
    DIMENSION_PENDING = "DIMENSION_EVIDENCE_PENDING"


class AbstractCoverageTag(Enum):
    NONE = "NO_ABSTRACT_RESULT"
    REASONING = "ABSTRACT_REASONING_RESULT"


class ReasoningTag(Enum):
    ADMITTED_JUDGMENT = "ADMITTED_JUDGMENT"
    COMPLETED_INCONCLUSIVE = "COMPLETED_INCONCLUSIVE"
    REASONING_ERROR = "REASONING_ERROR"


class ProfileTag(Enum):
    COMPLETE = "PROFILE_COMPLETE"
    INCOMPLETE = "PROFILE_INCOMPLETE"
    UNKNOWN = "PROFILE_UNKNOWN"
    EVALUATION_ERROR = "EVALUATION_ERROR"
    REASONING_ERROR = "REASONING_ERROR"


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


class PairTraceDomain(Enum):
    ALL_ADMITTED_TRACES = "ALL_ADMITTED_TRACES"


class PairComparedFields(Enum):
    COMPLETE_EVAL_RECORD = "COMPLETE_EVAL_RECORD"


VERIFICATION_SCHEMA = "CS(EVIDENCE_SCHEMA,verification)"
IMPLEMENTATION_PROFILE_SCHEMA = "CS(EVIDENCE_SCHEMA,implementation_profile)"


@dataclass(frozen=True, order=True)
class PathSegment:
    atom: str

    def __post_init__(self) -> None:
        if type(self.atom) is not str or not self.atom or self.atom in {".", ".."}:
            raise ValueError("inadmitted PathSegment")


@dataclass(frozen=True, order=True)
class Path:
    segments: tuple[PathSegment, ...]

    def __post_init__(self) -> None:
        if type(self.segments) is not tuple or not self.segments or any(type(item) is not PathSegment for item in self.segments):
            raise ValueError("Path is nonempty")


@dataclass(frozen=True, order=True)
class ByteSize:
    kib: int

    def __post_init__(self) -> None:
        if type(self.kib) is not int or self.kib < 0:
            raise ValueError("ByteSize is nonnegative")


@dataclass(frozen=True, order=True)
class ContentIdentity:
    atom: str

    def __post_init__(self) -> None:
        if type(self.atom) is not str or not self.atom:
            raise ValueError("ContentIdentity atom is nonempty")


@dataclass(frozen=True, order=True)
class CommandId:
    atom: str

    def __post_init__(self) -> None:
        if type(self.atom) is not str or not self.atom:
            raise ValueError("CommandId atom is nonempty")


@dataclass(frozen=True, order=True)
class ContactClass:
    atom: str

    def __post_init__(self) -> None:
        if type(self.atom) is not str or not self.atom:
            raise ValueError("ContactClass atom is nonempty")


@dataclass(frozen=True, order=True)
class ReleaseId:
    atom: str

    def __post_init__(self) -> None:
        if type(self.atom) is not str or not self.atom:
            raise ValueError("ReleaseId atom is nonempty")


@dataclass(frozen=True, order=True)
class FieldId:
    atom: str

    def __post_init__(self) -> None:
        if type(self.atom) is not str or not self.atom:
            raise ValueError("FieldId atom is nonempty")


class FieldValueTag(Enum):
    BOOL = "BOOL_VALUE"
    INT = "INT_VALUE"
    ATOM = "ATOM_VALUE"


@dataclass(frozen=True, order=True)
class FieldValue:
    """Closed BOOL_VALUE/INT_VALUE/ATOM_VALUE field algebra."""

    tag: FieldValueTag
    value: bool | int | str

    def __post_init__(self) -> None:
        valid = (
            (self.tag is FieldValueTag.BOOL and type(self.value) is bool)
            or (self.tag is FieldValueTag.INT and type(self.value) is int)
            or (self.tag is FieldValueTag.ATOM and isinstance(self.value, str) and bool(self.value))
        )
        if not valid:
            raise ValueError("FieldValue tag/value mismatch")


@dataclass(frozen=True, order=True)
class SubjectId:
    tag: SubjectTag
    atom: str

    def __post_init__(self) -> None:
        if not isinstance(self.tag, SubjectTag) or type(self.atom) is not str or not self.atom:
            raise ValueError("SubjectId tag and atom are admitted sorts")


@dataclass(frozen=True)
class BehaviorValue:
    tag: BehaviorTag
    metric: FieldId | None = None
    integer: int | None = None
    content: ContentIdentity | None = None
    left: tuple[tuple[FieldId, Any], ...] = ()
    right: tuple[tuple[FieldId, Any], ...] = ()

    def __post_init__(self) -> None:
        if (type(self.tag) is not BehaviorTag
                or (self.metric is not None and type(self.metric) is not FieldId)
                or (self.integer is not None and type(self.integer) is not int)
                or (self.content is not None and type(self.content) is not ContentIdentity)
                or type(self.left) is not tuple or type(self.right) is not tuple):
            raise ValueError("BehaviorValue nested sort")
        if len({key for key, _ in self.left}) != len(self.left):
            raise ValueError("duplicate left correspondence field")
        if len({key for key, _ in self.right}) != len(self.right):
            raise ValueError("duplicate right correspondence field")
        if any(not isinstance(key, FieldId) or not isinstance(value, FieldValue) for key, value in self.left + self.right):
            raise ValueError("BehaviorValue correspondence map is FieldId -> FieldValue")
        if self.tag in {BehaviorTag.ACCEPTED, BehaviorTag.REJECTED}:
            valid = self.metric is None and self.integer is None and self.content is None and not self.left and not self.right
        elif self.tag is BehaviorTag.METRIC:
            valid = self.metric is not None and self.integer is not None and self.content is None and not self.left and not self.right
        elif self.tag is BehaviorTag.RESOLUTION:
            valid = self.metric is None and self.integer is None and self.content is not None and not self.left and not self.right
        else:
            # Both finite correspondence maps may independently be empty.
            valid = self.metric is None and self.integer is None and self.content is None
        if not valid:
            raise ValueError("BehaviorValue fields do not match its tag")
        object.__setattr__(self, "left", tuple(sorted(self.left, key=lambda item: item[0])))
        object.__setattr__(self, "right", tuple(sorted(self.right, key=lambda item: item[0])))


@dataclass(frozen=True)
class ArtifactContent:
    tag: ArtifactTag
    role: ArtifactRole | OtherArtifactRole
    format: Format | OtherFormat
    size: ByteSize
    content: ContentIdentity | None = None
    fields: tuple[tuple[FieldId, Any], ...] = ()
    observations: tuple[tuple[SubjectId, BehaviorValue], ...] = ()

    def __post_init__(self) -> None:
        if (not isinstance(self.tag, ArtifactTag)
                or not isinstance(self.role, (ArtifactRole, OtherArtifactRole))
                or not isinstance(self.format, (Format, OtherFormat))
                or not isinstance(self.size, ByteSize)):
            raise ValueError("ArtifactContent nested sort")
        if len({key for key, _ in self.fields}) != len(self.fields):
            raise ValueError("duplicate structured field")
        if len({key for key, _ in self.observations}) != len(self.observations):
            raise ValueError("duplicate behavior subject")
        if any(not isinstance(key, FieldId) or not isinstance(value, FieldValue) for key, value in self.fields):
            raise ValueError("structured artifact fields are FieldId -> FieldValue")
        if any(not isinstance(key, SubjectId) or not isinstance(value, BehaviorValue) for key, value in self.observations):
            raise ValueError("behavior artifact observations are SubjectId -> BehaviorValue")
        if self.tag in {ArtifactTag.TEXT, ArtifactTag.OPAQUE}:
            valid = self.content is not None and not self.fields and not self.observations
        elif self.tag is ArtifactTag.STRUCTURED:
            valid = self.content is None and not self.observations
        else:
            valid = self.content is None and not self.fields
        if not valid:
            raise ValueError("ArtifactContent fields do not match its tag")
        object.__setattr__(self, "fields", tuple(sorted(self.fields, key=lambda item: item[0])))
        object.__setattr__(self, "observations", tuple(sorted(self.observations, key=lambda item: repr(item[0]))))

    @property
    def body_kind(self) -> ArtifactBodyKind:
        return {
            ArtifactTag.TEXT: ArtifactBodyKind.TEXT,
            ArtifactTag.STRUCTURED: ArtifactBodyKind.STRUCTURED,
            ArtifactTag.OPAQUE: ArtifactBodyKind.OPAQUE,
            ArtifactTag.BEHAVIOR: ArtifactBodyKind.BEHAVIOR,
        }[self.tag]


@dataclass(frozen=True)
class RepositorySnapshot:
    entries: tuple[tuple[Path, ArtifactContent], ...]

    def __post_init__(self) -> None:
        if any(not isinstance(path, Path) or not isinstance(value, ArtifactContent) for path, value in self.entries):
            raise ValueError("RepositorySnapshot is Path -> ArtifactContent")
        if len({path for path, _ in self.entries}) != len(self.entries):
            raise ValueError("duplicate snapshot path")
        object.__setattr__(self, "entries", tuple(sorted(self.entries, key=lambda item: item[0])))

    def as_map(self) -> dict[Path, ArtifactContent]:
        return dict(self.entries)


@dataclass(frozen=True)
class SnapshotIdentity:
    snapshot: RepositorySnapshot

    def __post_init__(self) -> None:
        if type(self.snapshot) is not RepositorySnapshot:
            raise ValueError("SnapshotIdentity contains an exact RepositorySnapshot")


@dataclass(frozen=True)
class ArtifactSelector:
    tag: SelectorTag
    paths: frozenset[Path] = frozenset()
    role: ArtifactRole | OtherArtifactRole | None = None

    def __post_init__(self) -> None:
        if (not isinstance(self.tag, SelectorTag)
                or any(not isinstance(path, Path) for path in self.paths)
                or (self.role is not None and not isinstance(self.role, (ArtifactRole, OtherArtifactRole)))):
            raise ValueError("ArtifactSelector nested sort")
        valid = (
            self.tag is SelectorTag.PATHS and self.role is None
        ) or (
            self.tag is SelectorTag.ROLE and not self.paths and self.role is not None
        ) or (
            self.tag is SelectorTag.PATHS_WITH_ROLE
            and self.role is not None
        )
        if not valid:
            raise ValueError("ArtifactSelector fields do not match its tag")


@dataclass(frozen=True)
class ArtifactProjection:
    tag: ProjectionTag
    field: FieldId | None = None

    def __post_init__(self) -> None:
        if (type(self.tag) is not ProjectionTag
                or (self.field is not None and type(self.field) is not FieldId)):
            raise ValueError("ArtifactProjection nested sort")
        if (self.tag is ProjectionTag.STRUCTURED_FIELD) != (self.field is not None):
            raise ValueError("ArtifactProjection fields do not match its tag")


@dataclass(frozen=True)
class ObservationSpec:
    tag: ObservationSpecTag
    selector: ArtifactSelector | None = None
    projection: ArtifactProjection | None = None
    domain: frozenset[SubjectId] = frozenset()
    metric: FieldId | None = None

    def __post_init__(self) -> None:
        if (type(self.tag) is not ObservationSpecTag
                or type(self.domain) is not frozenset
                or any(type(subject) is not SubjectId for subject in self.domain)
                or (self.selector is not None and type(self.selector) is not ArtifactSelector)
                or (self.projection is not None and type(self.projection) is not ArtifactProjection)
                or (self.metric is not None and type(self.metric) is not FieldId)):
            raise ValueError("ObservationSpec nested sort")
        if self.tag is ObservationSpecTag.ARTIFACT_VIEW:
            valid = self.selector is not None and self.projection is not None and not self.domain and self.metric is None
        elif self.tag is ObservationSpecTag.WORKLOAD_METRIC_VIEW:
            valid = bool(self.domain) and self.metric is not None and self.selector is None and self.projection is None
        elif self.tag is ObservationSpecTag.DEPENDENCY_RESOLUTION_VIEW:
            valid = bool(self.domain) and self.selector is not None and self.projection is None and self.metric is None
        else:
            valid = bool(self.domain) and self.selector is None and self.projection is None and self.metric is None
        expected_subject = {
            ObservationSpecTag.REQUEST_BEHAVIOR_VIEW: SubjectTag.REQUEST,
            ObservationSpecTag.WORKLOAD_METRIC_VIEW: SubjectTag.WORKLOAD,
            ObservationSpecTag.DEPENDENCY_RESOLUTION_VIEW: SubjectTag.RESOLUTION_LANE,
            ObservationSpecTag.CLIENT_ADAPTER_VIEW: SubjectTag.CLIENT_PAIR,
        }.get(self.tag)
        if expected_subject is not None and any(subject.tag is not expected_subject for subject in self.domain):
            valid = False
        if not valid:
            raise ValueError("ObservationSpec fields do not match its tag")


@dataclass(frozen=True)
class Coverage:
    tag: CoverageTag
    missing_subjects: frozenset[SubjectId] = frozenset()

    def __post_init__(self) -> None:
        if (type(self.tag) is not CoverageTag or type(self.missing_subjects) is not frozenset
                or any(type(subject) is not SubjectId for subject in self.missing_subjects)):
            raise ValueError("Coverage nested sort")
        if (self.tag is CoverageTag.COMPLETE) == bool(self.missing_subjects):
            raise ValueError("Coverage fields do not match its tag")


@dataclass(frozen=True)
class ObservationValue:
    tag: ObservationValueTag
    payload: tuple[Any, ...] = ()

    def __post_init__(self) -> None:
        if type(self.tag) is not ObservationValueTag or type(self.payload) is not tuple:
            raise ValueError("ObservationValue nested sort")
        def correspondence_map(value: Any) -> bool:
            return (type(value) is tuple
                    and len({key for key, _ in value}) == len(value)
                    and all(type(key) is FieldId and type(item) is FieldValue
                            for key, item in value))
        arity = {
            ObservationValueTag.ABSENT: 0,
            ObservationValueTag.ROLE_MISMATCH: 2,
            ObservationValueTag.PROJECTION_MISMATCH: 2,
            ObservationValueTag.PRESENT: 0,
            ObservationValueTag.PRESENT_CONTENT: 1,
            ObservationValueTag.PRESENT_FORMAT: 1,
            ObservationValueTag.PRESENT_SIZE: 1,
            ObservationValueTag.PRESENT_FIELD: 1,
            ObservationValueTag.ACCEPTED: 0,
            ObservationValueTag.REJECTED: 0,
            ObservationValueTag.METRIC_VALUE: 1,
            ObservationValueTag.RESOLUTION_VALUE: 1,
            ObservationValueTag.CORRESPONDENCE_VALUE: 2,
            ObservationValueTag.BEHAVIOR_CONFLICT: 1,
        }[self.tag]
        if len(self.payload) != arity:
            raise ValueError("ObservationValue payload arity")
        checks = {
            ObservationValueTag.ROLE_MISMATCH: lambda values: all(isinstance(value, (ArtifactRole, OtherArtifactRole)) for value in values),
            ObservationValueTag.PROJECTION_MISMATCH: lambda values: isinstance(values[0], ArtifactBodyKind) and isinstance(values[1], ArtifactProjection),
            ObservationValueTag.PRESENT_CONTENT: lambda values: isinstance(values[0], ArtifactContent),
            ObservationValueTag.PRESENT_FORMAT: lambda values: isinstance(values[0], (Format, OtherFormat)),
            ObservationValueTag.PRESENT_FIELD: lambda values: isinstance(values[0], FieldValue),
            ObservationValueTag.PRESENT_SIZE: lambda values: isinstance(values[0], ByteSize),
            ObservationValueTag.METRIC_VALUE: lambda values: type(values[0]) is int,
            ObservationValueTag.RESOLUTION_VALUE: lambda values: isinstance(values[0], ContentIdentity),
            ObservationValueTag.CORRESPONDENCE_VALUE: lambda values: all(correspondence_map(value) for value in values),
            ObservationValueTag.BEHAVIOR_CONFLICT: lambda values: type(values[0]) is frozenset and bool(values[0]) and all(type(value) is BehaviorValue for value in values[0]),
        }
        if self.tag in checks and not checks[self.tag](self.payload):
            raise ValueError("ObservationValue payload type")


@dataclass(frozen=True)
class ObservationResult:
    tag: ObservationResultTag
    spec_identity: ObservationSpec
    coverage: Coverage
    values: tuple[tuple[Any, ObservationValue], ...]

    def __post_init__(self) -> None:
        if (type(self.tag) is not ObservationResultTag
                or type(self.spec_identity) is not ObservationSpec
                or type(self.coverage) is not Coverage
                or type(self.values) is not tuple
                or any(type(item) is not tuple or len(item) != 2
                       or type(item[1]) is not ObservationValue for item in self.values)):
            raise ValueError("ObservationResult nested sort")
        if len({key for key, _ in self.values}) != len(self.values):
            raise ValueError("duplicate observation-result key")
        expected = {
            ObservationSpecTag.ARTIFACT_VIEW: ObservationResultTag.ARTIFACT,
            ObservationSpecTag.REQUEST_BEHAVIOR_VIEW: ObservationResultTag.SUBJECT,
            ObservationSpecTag.WORKLOAD_METRIC_VIEW: ObservationResultTag.SUBJECT,
            ObservationSpecTag.DEPENDENCY_RESOLUTION_VIEW: ObservationResultTag.LANE,
            ObservationSpecTag.CLIENT_ADAPTER_VIEW: ObservationResultTag.CORRESPONDENCE,
        }[self.spec_identity.tag]
        if self.tag is not expected:
            raise ValueError("result tag does not match observation spec")
        key_type = Path if self.tag is ObservationResultTag.ARTIFACT else SubjectId
        if any(type(key) is not key_type for key, _ in self.values):
            raise ValueError("observation result key sort")
        allowed = {
            ObservationSpecTag.ARTIFACT_VIEW: {
                ObservationValueTag.ABSENT,
                ObservationValueTag.ROLE_MISMATCH,
                ObservationValueTag.PROJECTION_MISMATCH,
                ObservationValueTag.PRESENT,
                ObservationValueTag.PRESENT_CONTENT,
                ObservationValueTag.PRESENT_FORMAT,
                ObservationValueTag.PRESENT_SIZE,
                ObservationValueTag.PRESENT_FIELD,
            },
            ObservationSpecTag.REQUEST_BEHAVIOR_VIEW: {
                ObservationValueTag.ACCEPTED,
                ObservationValueTag.REJECTED,
                ObservationValueTag.BEHAVIOR_CONFLICT,
            },
            ObservationSpecTag.WORKLOAD_METRIC_VIEW: {
                ObservationValueTag.METRIC_VALUE,
                ObservationValueTag.BEHAVIOR_CONFLICT,
            },
            ObservationSpecTag.DEPENDENCY_RESOLUTION_VIEW: {
                ObservationValueTag.RESOLUTION_VALUE,
                ObservationValueTag.BEHAVIOR_CONFLICT,
            },
            ObservationSpecTag.CLIENT_ADAPTER_VIEW: {
                ObservationValueTag.CORRESPONDENCE_VALUE,
                ObservationValueTag.BEHAVIOR_CONFLICT,
            },
        }[self.spec_identity.tag]
        if any(value.tag not in allowed for _, value in self.values):
            raise ValueError("observation value is illegal for its spec")
        if self.spec_identity.tag is not ObservationSpecTag.ARTIFACT_VIEW:
            keys = frozenset(key for key, _ in self.values)
            if not keys <= self.spec_identity.domain:
                raise ValueError("observation result exceeds its exact domain")
            missing = self.spec_identity.domain - keys
            if self.coverage.missing_subjects != missing:
                raise ValueError("coverage is not the exact missing domain")
        object.__setattr__(self, "values", tuple(sorted(self.values, key=lambda item: repr(item[0]))))


@dataclass(frozen=True)
class ObservationRelation:
    tag: ObservationRelationTag
    field_bijection: tuple[tuple[FieldId, FieldId], ...] = ()

    def __post_init__(self) -> None:
        if (type(self.tag) is not ObservationRelationTag
                or type(self.field_bijection) is not tuple
                or any(type(pair) is not tuple or len(pair) != 2
                       or type(pair[0]) is not FieldId or type(pair[1]) is not FieldId
                       for pair in self.field_bijection)):
            raise ValueError("ObservationRelation nested sort")
        if self.tag is ObservationRelationTag.FIELD_CORRESPONDENCE:
            left = {key for key, _ in self.field_bijection}
            right = {value for _, value in self.field_bijection}
            if not self.field_bijection or len(left) != len(self.field_bijection) or len(right) != len(self.field_bijection):
                raise ValueError("FIELD_CORRESPONDENCE requires a finite bijection")
        elif self.field_bijection:
            raise ValueError("only FIELD_CORRESPONDENCE carries a bijection")
        object.__setattr__(self, "field_bijection", tuple(sorted(self.field_bijection, key=lambda item: item[0])))


@dataclass(frozen=True)
class ChangeEntry:
    kind: ChangeKind
    old: ArtifactContent | None = None
    new: ArtifactContent | None = None

    def __post_init__(self) -> None:
        valid = (
            self.kind is ChangeKind.CREATED and self.old is None and self.new is not None
        ) or (
            self.kind is ChangeKind.DELETED and self.old is not None and self.new is None
        ) or (
            self.kind is ChangeKind.MODIFIED
            and self.old is not None
            and self.new is not None
            and self.old != self.new
        )
        if not valid:
            raise ValueError("ChangeEntry fields do not match its tag")


@dataclass(frozen=True)
class ChangeSet:
    entries: tuple[tuple[Path, ChangeEntry], ...]

    def __post_init__(self) -> None:
        if len({path for path, _ in self.entries}) != len(self.entries):
            raise ValueError("duplicate ChangeSet path")
        object.__setattr__(self, "entries", tuple(sorted(self.entries, key=lambda item: item[0])))


@dataclass(frozen=True)
class TermResult:
    value: Any = None
    error: str | None = None

    def __post_init__(self) -> None:
        if (self.error is None) == (self.value is None):
            raise ValueError("TermResult is exactly TERM_VALUE or TERM_ERROR")

    @property
    def is_value(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class Eval:
    truth: Truth | None
    evidence_refs: frozenset["EvidenceRef"] = frozenset()
    reasons: frozenset[str] = frozenset()
    errors: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if (self.truth is None) == bool(self.errors):
            return
        raise ValueError("Eval is exactly VALUE or ERROR")


@dataclass(frozen=True, order=True)
class EvidenceRef:
    issuer_scope: str
    namespace: str
    stable_identity: str
    schema_binding: str

    def __post_init__(self) -> None:
        if not self.issuer_scope or not self.namespace or not self.stable_identity or not self.schema_binding:
            raise ValueError("EvidenceRef fields are nonempty")


@dataclass(frozen=True)
class VerificationSpec:
    protocol_identity: str
    subject: ObservationSpec
    evidence_schema_key: str

    def __post_init__(self) -> None:
        if not self.protocol_identity or not self.evidence_schema_key:
            raise ValueError("VerificationSpec fields are nonempty")


@dataclass(frozen=True)
class VerificationRecord:
    spec: VerificationSpec
    snapshot_identity: SnapshotIdentity
    status: VerificationStatus
    observation: ObservationResult
    evidence_refs: frozenset[EvidenceRef]

    def __post_init__(self) -> None:
        if type(self.snapshot_identity) is not SnapshotIdentity or not self.evidence_refs:
            raise ValueError("VerificationRecord evidence_refs is nonempty")
        if self.observation.spec_identity != self.spec.subject:
            raise ValueError("verification observation/spec mismatch")


@dataclass(frozen=True)
class ReasoningResult:
    tag: ReasoningTag
    certificate_key: str | None = None
    judgment: str | None = None
    reasons: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if self.tag is ReasoningTag.ADMITTED_JUDGMENT:
            valid = self.certificate_key is not None and self.judgment is not None and not self.reasons
        else:
            valid = self.certificate_key is None and self.judgment is None and bool(self.reasons)
        if not valid:
            raise ValueError("ReasoningResult fields do not match its tag")


@dataclass(frozen=True)
class ImplementationEvidence:
    tag: ImplementationEvidenceTag
    contract_identity: str
    snapshot_identity: SnapshotIdentity
    certificate_key: str | None = None
    implementation_identity: str | None = None
    dimension: str | None = None
    reason: str | None = None

    def __post_init__(self) -> None:
        if type(self.snapshot_identity) is not SnapshotIdentity:
            raise ValueError("ImplementationEvidence snapshot identity sort")
        if self.tag is ImplementationEvidenceTag.ABSTRACT_ACCEPTANCE:
            valid = self.certificate_key is not None and self.implementation_identity is None and self.dimension is None and self.reason is None
        elif self.tag is ImplementationEvidenceTag.CONCRETE_IMPLEMENTATION:
            valid = self.certificate_key is None and self.implementation_identity is not None and self.dimension is None and self.reason is None
        else:
            valid = self.certificate_key is None and self.implementation_identity is None and self.dimension is not None and self.reason is not None
        if not valid:
            raise ValueError("ImplementationEvidence fields do not match its tag")


@dataclass(frozen=True)
class CodingEvidencePayload:
    tag: EvidencePayloadTag
    value: VerificationRecord | ImplementationEvidence

    def __post_init__(self) -> None:
        expected = VerificationRecord if self.tag is EvidencePayloadTag.VERIFICATION else ImplementationEvidence
        if not isinstance(self.value, expected):
            raise ValueError("evidence payload/tag mismatch")


@dataclass(frozen=True)
class CodingEvidenceEntry:
    reference: EvidenceRef
    payload: CodingEvidencePayload


@dataclass(frozen=True)
class AbstractCoverageResult:
    tag: AbstractCoverageTag
    result: ReasoningResult | None = None

    def __post_init__(self) -> None:
        if (self.tag is AbstractCoverageTag.REASONING) != (self.result is not None):
            raise ValueError("AbstractCoverageResult fields do not match its tag")


@dataclass(frozen=True)
class ObservationEquals:
    spec: ObservationSpec
    expected: ObservationResult


@dataclass(frozen=True)
class OneFormatOf:
    selector: ArtifactSelector
    formats: frozenset[Format | OtherFormat]

    def __post_init__(self) -> None:
        if (type(self.formats) is not frozenset or not self.formats
                or any(type(item) not in {Format, OtherFormat} for item in self.formats)):
            raise ValueError("ONE_FORMAT_OF format set is nonempty")


@dataclass(frozen=True)
class ArtifactsNonempty:
    selector: ArtifactSelector


@dataclass(frozen=True)
class ArtifactSizeLt:
    selector: ArtifactSelector
    upper: ByteSize


@dataclass(frozen=True)
class ArtifactSizeAtLeast:
    selector: ArtifactSelector
    lower: ByteSize


@dataclass(frozen=True)
class UniversalObservation:
    spec: ObservationSpec
    baseline: ObservationResult
    relation: ObservationRelation

    def __post_init__(self) -> None:
        if self.spec.tag not in {
            ObservationSpecTag.REQUEST_BEHAVIOR_VIEW,
            ObservationSpecTag.WORKLOAD_METRIC_VIEW,
        }:
            raise ValueError("UNIVERSAL_OBSERVATION requires request/workload view")


@dataclass(frozen=True)
class DependencyReproducible:
    spec: ObservationSpec

    def __post_init__(self) -> None:
        if self.spec.tag is not ObservationSpecTag.DEPENDENCY_RESOLUTION_VIEW:
            raise ValueError("DEPENDENCY_REPRODUCIBLE requires lane view")


@dataclass(frozen=True)
class AdapterCorresponds:
    spec: ObservationSpec
    relation: ObservationRelation

    def __post_init__(self) -> None:
        if self.spec.tag is not ObservationSpecTag.CLIENT_ADAPTER_VIEW or self.relation.tag is not ObservationRelationTag.FIELD_CORRESPONDENCE:
            raise ValueError("ADAPTER_CORRESPONDS requires client view/bijection")


Criterion = ObservationEquals | OneFormatOf | ArtifactsNonempty | ArtifactSizeLt | ArtifactSizeAtLeast | UniversalObservation | DependencyReproducible | AdapterCorresponds


@dataclass(frozen=True)
class TaskSpec:
    criteria: frozenset[Criterion] = frozenset()
    required_verifications: frozenset[VerificationSpec] = frozenset()

    def __post_init__(self) -> None:
        if (type(self.criteria) is not frozenset
                or any(type(item) not in _CRITERION_TYPES for item in self.criteria)
                or type(self.required_verifications) is not frozenset
                or any(type(item) is not VerificationSpec for item in self.required_verifications)):
            raise ValueError("TaskSpec contains only admitted criteria and verification specs")


@dataclass(frozen=True)
class ImplementationCoverageSubject:
    contract_identity: str
    task: TaskSpec
    snapshot: RepositorySnapshot
    evidence_store: frozenset[CodingEvidenceEntry]
    task_result: Eval
    abstract_result: AbstractCoverageResult


@dataclass(frozen=True)
class ProfileResult:
    tag: ProfileTag
    profile_key: str
    evidence_refs: frozenset[EvidenceRef] = frozenset()
    missing_dimensions: frozenset[str] = frozenset()
    reasons: frozenset[str] = frozenset()
    errors: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.profile_key:
            raise ValueError("profile key is nonempty")
        populated = (bool(self.evidence_refs), bool(self.missing_dimensions), bool(self.reasons), bool(self.errors))
        valid = {
            ProfileTag.COMPLETE: populated[0] and not any(populated[1:]),
            ProfileTag.INCOMPLETE: populated[1] and not populated[0] and not populated[2] and not populated[3],
            ProfileTag.UNKNOWN: populated[2] and not populated[0] and not populated[1] and not populated[3],
            ProfileTag.EVALUATION_ERROR: populated[3] and not populated[0] and not populated[1] and not populated[2],
            ProfileTag.REASONING_ERROR: populated[3] and not populated[0] and not populated[1] and not populated[2],
        }[self.tag]
        if not valid:
            raise ValueError("ProfileResult fields do not match its tag")


@dataclass(frozen=True)
class CommandEventPayload:
    command_id: CommandId
    purpose: str

    def __post_init__(self) -> None:
        if type(self.command_id) is not CommandId or type(self.purpose) is not str or not self.purpose:
            raise ValueError("command-event atoms are nonempty")


@dataclass(frozen=True)
class TestEventPayload:
    spec: VerificationSpec
    snapshot: SnapshotIdentity
    status: VerificationStatus
    evidence_refs: frozenset[EvidenceRef]

    def __post_init__(self) -> None:
        if type(self.snapshot) is not SnapshotIdentity or not self.evidence_refs:
            raise ValueError("test-event evidence_refs is nonempty")


@dataclass(frozen=True)
class PathChangeEventPayload:
    path: Path
    change: ChangeEntry


@dataclass(frozen=True)
class NetworkContactEventPayload:
    contact_class: ContactClass
    purpose: str

    def __post_init__(self) -> None:
        if type(self.contact_class) is not ContactClass or type(self.purpose) is not str or not self.purpose:
            raise ValueError("network-event atoms are nonempty")


@dataclass(frozen=True)
class ReleaseEventPayload:
    release_id: ReleaseId
    snapshot: SnapshotIdentity

    def __post_init__(self) -> None:
        if type(self.release_id) is not ReleaseId or type(self.snapshot) is not SnapshotIdentity:
            raise ValueError("release event fields are admitted sorts")


@dataclass(frozen=True)
class DependencyRefreshEventPayload:
    selector: ArtifactSelector
    snapshot: SnapshotIdentity

    def __post_init__(self) -> None:
        if type(self.selector) is not ArtifactSelector or type(self.snapshot) is not SnapshotIdentity:
            raise ValueError("dependency refresh fields are admitted sorts")


EventPayload = CommandEventPayload | TestEventPayload | PathChangeEventPayload | NetworkContactEventPayload | ReleaseEventPayload | DependencyRefreshEventPayload


@dataclass(frozen=True)
class EventValue:
    key: EventKind
    payload: EventPayload

    def __post_init__(self) -> None:
        expected = {
            EventKind.COMMAND: CommandEventPayload,
            EventKind.TEST: TestEventPayload,
            EventKind.PATH_CHANGE: PathChangeEventPayload,
            EventKind.NETWORK_CONTACT: NetworkContactEventPayload,
            EventKind.RELEASE: ReleaseEventPayload,
            EventKind.DEPENDENCY_REFRESH: DependencyRefreshEventPayload,
        }[self.key]
        if not isinstance(self.payload, expected):
            raise ValueError("event key/payload mismatch")


@dataclass(frozen=True)
class EventPattern:
    tag: PatternKind
    event_key: EventKind | None = None
    command_id: CommandId | None = None
    verification_spec: VerificationSpec | None = None
    statuses: frozenset[VerificationStatus] = frozenset()
    paths: frozenset[Path] = frozenset()
    change_kinds: frozenset[ChangeKind] = frozenset()
    contact_class: ContactClass | None = None
    release_id: ReleaseId | None = None
    selector: ArtifactSelector | None = None
    snapshot: SnapshotIdentity | None = None

    def __post_init__(self) -> None:
        populated = {
            "event_key": self.event_key is not None,
            "command_id": self.command_id is not None,
            "verification_spec": self.verification_spec is not None,
            "statuses": bool(self.statuses),
            "paths": bool(self.paths),
            "change_kinds": bool(self.change_kinds),
            "contact_class": self.contact_class is not None,
            "release_id": self.release_id is not None,
            "selector": self.selector is not None,
            "snapshot": self.snapshot is not None,
        }
        required = {
            PatternKind.ANY_EVENT: {"event_key"},
            PatternKind.COMMAND_IS: {"command_id"},
            PatternKind.TEST_IS: {"verification_spec", "statuses"},
            PatternKind.PATH_CHANGE_IN: {"paths", "change_kinds"},
            PatternKind.NETWORK_CLASS: {"contact_class"},
            PatternKind.RELEASE_IS: {"release_id", "snapshot"},
            PatternKind.REFRESHES: {"selector", "snapshot"},
        }[self.tag]
        if {name for name, present in populated.items() if present} != required:
            raise ValueError("EventPattern fields do not match its tag")
        typed = {
            "event_key": EventKind,
            "command_id": CommandId,
            "verification_spec": VerificationSpec,
            "statuses": frozenset,
            "paths": frozenset,
            "change_kinds": frozenset,
            "contact_class": ContactClass,
            "release_id": ReleaseId,
            "selector": ArtifactSelector,
            "snapshot": SnapshotIdentity,
        }
        if any(populated[name] and type(getattr(self, name)) is not expected
               for name, expected in typed.items()):
            raise ValueError("EventPattern nested sort")
        if (any(type(value) is not VerificationStatus for value in self.statuses)
                or any(type(value) is not Path for value in self.paths)
                or any(type(value) is not ChangeKind for value in self.change_kinds)):
            raise ValueError("EventPattern set member sort")


@dataclass(frozen=True)
class TraceEvent:
    event_value: EventValue
    actor: str

    def __post_init__(self) -> None:
        if not self.actor:
            raise ValueError("trace actor is nonempty")


_CRITERION_TYPES = (
    ObservationEquals, OneFormatOf, ArtifactsNonempty, ArtifactSizeLt,
    ArtifactSizeAtLeast, UniversalObservation, DependencyReproducible,
    AdapterCorresponds,
)

_ADMISSION_TYPES: dict[str, type[Any] | tuple[type[Any], ...]] = {
    "PathSegment": PathSegment, "Path": Path, "PathSet": frozenset,
    "ArtifactRole": (ArtifactRole, OtherArtifactRole),
    "Format": (Format, OtherFormat), "ByteSize": ByteSize,
    "ContentIdentity": ContentIdentity, "FieldId": FieldId,
    "FieldValue": FieldValue, "SubjectId": SubjectId,
    "BehaviorValue": BehaviorValue, "ArtifactBodyKind": ArtifactBodyKind,
    "ArtifactContent": ArtifactContent, "RepositorySnapshot": RepositorySnapshot,
    "SnapshotIdentity": SnapshotIdentity, "ArtifactSelector": ArtifactSelector,
    "ArtifactProjection": ArtifactProjection, "Coverage": Coverage,
    "ObservationSpec": ObservationSpec, "ObservationValue": ObservationValue,
    "ObservationResult": ObservationResult, "ObservationRelation": ObservationRelation,
    "VerificationSpec": VerificationSpec, "VerificationStatus": VerificationStatus,
    "Criterion": _CRITERION_TYPES, "TaskSpec": TaskSpec,
    "ChangeKind": ChangeKind, "CommandId": CommandId, "ContactClass": ContactClass,
    "ReleaseId": ReleaseId, "EventPattern": EventPattern,
    "DependencyRefreshEventPayload": DependencyRefreshEventPayload,
    "PairTraceDomain": PairTraceDomain,
    "PairComparedFields": PairComparedFields,
}


def admission_type(type_name: str) -> type[Any] | tuple[type[Any], ...]:
    """Resolve one frozen K3-S type-table row for its embedded relation."""
    admitted = _ADMISSION_TYPES.get(type_name)
    if admitted is None:
        raise FiniteCodingProfileError(f"unsupported type-admission row: {type_name}")
    return admitted


def admitted_closed_value(expected_type: type[Any] | tuple[type[Any], ...], value: Any) -> bool:
    """Evaluate exact constructor and nested-field membership, including int/bool separation."""
    expected_types = expected_type if isinstance(expected_type, tuple) else (expected_type,)
    if expected_types == (frozenset,):
        return type(value) is frozenset and all(
            type(item) is Path and _admitted_payload(item) for item in value)
    return type(value) in expected_types and _admitted_payload(value)


def _admitted_payload(value: Any) -> bool:
    """Exact membership predicate for every retained closed constructor."""
    kind = type(value)
    if kind in {ArtifactRole, Format, ArtifactBodyKind, VerificationStatus, ChangeKind}:
        return kind(value.value) is value
    if kind in {PairTraceDomain, PairComparedFields}:
        return kind(value.value) is value
    if kind is PathSegment:
        return type(value.atom) is str and bool(value.atom) and value.atom not in {".", ".."}
    if kind is Path:
        return type(value.segments) is tuple and bool(value.segments) and all(
            type(item) is PathSegment and _admitted_payload(item) for item in value.segments)
    if kind is frozenset:
        return all(_admitted_payload(item) for item in value)
    if kind in {OtherArtifactRole, OtherFormat, ContentIdentity, FieldId,
                CommandId, ContactClass, ReleaseId}:
        return type(value.atom) is str and bool(value.atom)
    if kind is ByteSize:
        return type(value.kib) is int and value.kib >= 0
    if kind is FieldValue:
        return ((value.tag is FieldValueTag.BOOL and type(value.value) is bool)
                or (value.tag is FieldValueTag.INT and type(value.value) is int)
                or (value.tag is FieldValueTag.ATOM and type(value.value) is str and bool(value.value)))
    if kind is SubjectId:
        return type(value.tag) is SubjectTag and type(value.atom) is str and bool(value.atom)
    if kind is BehaviorValue:
        try:
            return (BehaviorValue(value.tag, value.metric, value.integer, value.content,
                                  value.left, value.right) == value
                    and (value.metric is None or _admitted_payload(value.metric))
                    and (value.content is None or _admitted_payload(value.content))
                    and (value.left is None or _admitted_payload(value.left))
                    and (value.right is None or _admitted_payload(value.right)))
        except (TypeError, ValueError):
            return False
    if kind is ArtifactContent:
        try:
            return (ArtifactContent(value.tag, value.role, value.format, value.size,
                                    value.content, value.fields, value.observations) == value
                    and _admitted_payload(value.role) and _admitted_payload(value.format)
                    and _admitted_payload(value.size)
                    and (value.content is None or _admitted_payload(value.content))
                    and all(_admitted_payload(key) and _admitted_payload(item) for key, item in value.fields)
                    and all(_admitted_payload(key) and _admitted_payload(item) for key, item in value.observations))
        except (TypeError, ValueError):
            return False
    if kind is RepositorySnapshot:
        try:
            return (RepositorySnapshot(value.entries) == value
                    and all(_admitted_payload(path) and _admitted_payload(item)
                            for path, item in value.entries))
        except (TypeError, ValueError):
            return False
    if kind is SnapshotIdentity:
        return type(value.snapshot) is RepositorySnapshot and _admitted_payload(value.snapshot)
    if kind is ArtifactSelector:
        try:
            return (ArtifactSelector(value.tag, value.paths, value.role) == value
                    and type(value.paths) is frozenset
                    and all(type(path) is Path and _admitted_payload(path) for path in value.paths)
                    and (value.role is None or _admitted_payload(value.role)))
        except (TypeError, ValueError):
            return False
    if kind is ArtifactProjection:
        try:
            return (ArtifactProjection(value.tag, value.field) == value
                    and (value.field is None or _admitted_payload(value.field)))
        except (TypeError, ValueError):
            return False
    if kind is ObservationSpec:
        try:
            return (ObservationSpec(value.tag, value.selector, value.projection,
                                    value.domain, value.metric) == value
                    and (value.selector is None or _admitted_payload(value.selector))
                    and (value.projection is None or _admitted_payload(value.projection))
                    and all(_admitted_payload(subject) for subject in value.domain)
                    and (value.metric is None or _admitted_payload(value.metric)))
        except (TypeError, ValueError):
            return False
    if kind is Coverage:
        try:
            return (Coverage(value.tag, value.missing_subjects) == value
                    and all(_admitted_payload(subject) for subject in value.missing_subjects))
        except (TypeError, ValueError):
            return False
    if kind is ObservationValue:
        try:
            return (ObservationValue(value.tag, value.payload) == value
                    and all(_admitted_payload(item) for item in value.payload))
        except (TypeError, ValueError):
            return False
    if kind is ObservationResult:
        try:
            return (ObservationResult(value.tag, value.spec_identity, value.coverage,
                                      value.values) == value
                    and _admitted_payload(value.spec_identity)
                    and _admitted_payload(value.coverage)
                    and all(_admitted_payload(key) and _admitted_payload(item)
                            for key, item in value.values))
        except (TypeError, ValueError):
            return False
    if kind is ObservationRelation:
        try:
            return (ObservationRelation(value.tag, value.field_bijection) == value
                    and all(_admitted_payload(left) and _admitted_payload(right)
                            for left, right in value.field_bijection))
        except (TypeError, ValueError):
            return False
    if kind is VerificationSpec:
        return (type(value.protocol_identity) is str and bool(value.protocol_identity)
                and _admitted_payload(value.subject)
                and type(value.evidence_schema_key) is str and bool(value.evidence_schema_key))
    if kind is ObservationEquals:
        return _admitted_payload(value.spec) and _admitted_payload(value.expected)
    if kind is OneFormatOf:
        return (_admitted_payload(value.selector) and type(value.formats) is frozenset
                and bool(value.formats)
                and all(type(item) in {Format, OtherFormat} and _admitted_payload(item)
                        for item in value.formats))
    if kind is ArtifactsNonempty:
        return _admitted_payload(value.selector)
    if kind is ArtifactSizeLt:
        return _admitted_payload(value.selector) and _admitted_payload(value.upper)
    if kind is ArtifactSizeAtLeast:
        return _admitted_payload(value.selector) and _admitted_payload(value.lower)
    if kind is UniversalObservation:
        return (_admitted_payload(value.spec) and _admitted_payload(value.baseline)
                and _admitted_payload(value.relation))
    if kind is DependencyReproducible:
        return _admitted_payload(value.spec)
    if kind is AdapterCorresponds:
        return _admitted_payload(value.spec) and _admitted_payload(value.relation)
    if kind is TaskSpec:
        return (type(value.criteria) is frozenset
                and all(type(item) in _CRITERION_TYPES and _admitted_payload(item)
                        for item in value.criteria)
                and type(value.required_verifications) is frozenset
                and all(type(item) is VerificationSpec and _admitted_payload(item)
                        for item in value.required_verifications))
    if kind is EventPattern:
        try:
            return (EventPattern(
                value.tag, value.event_key, value.command_id,
                value.verification_spec, value.statuses, value.paths,
                value.change_kinds, value.contact_class, value.release_id,
                value.selector, value.snapshot,
            ) == value
                    and all(_admitted_payload(item) for item in (
                        value.event_key, value.command_id, value.verification_spec,
                        value.statuses, value.paths, value.change_kinds,
                        value.contact_class, value.release_id, value.selector,
                        value.snapshot,
                    )))
        except (TypeError, ValueError):
            return False
    if kind is DependencyRefreshEventPayload:
        return (_admitted_payload(value.selector)
                and _admitted_payload(value.snapshot))
    if kind.__module__ == "KernelPlugin.k3x.reference" and kind.__name__ == "PairCoherenceSubject":
        from .reference import RecordIdentity
        return (type(value.pair) is RecordIdentity
                and type(value.scope_binding) is RecordIdentity
                and type(value.occurrence_binding) is RecordIdentity
                and value.trace_domain is PairTraceDomain.ALL_ADMITTED_TRACES
                and value.compared_fields is PairComparedFields.COMPLETE_EVAL_RECORD)
    if value is None or kind in {bool, int}:
        return True
    if kind is str:
        return bool(value)
    if isinstance(value, Enum):
        return type(value)(value.value) is value
    if kind is tuple:
        return all(_admitted_payload(item) for item in value)
    return False


def snapshot_identity(snapshot: RepositorySnapshot) -> SnapshotIdentity:
    return SnapshotIdentity(snapshot)


def snapshot_of(state: Any) -> TermResult:
    if isinstance(state, RepositorySnapshot):
        return TermResult(value=state)
    return TermResult(error="NOT_A_REPOSITORY_SNAPSHOT")


def changes_between(before: RepositorySnapshot, after: RepositorySnapshot) -> TermResult:
    if not isinstance(before, RepositorySnapshot) or not isinstance(after, RepositorySnapshot):
        return TermResult(error="NOT_A_REPOSITORY_SNAPSHOT")
    old = before.as_map()
    new = after.as_map()
    entries: list[tuple[Path, ChangeEntry]] = []
    for path in sorted(set(old) | set(new)):
        if path not in old:
            entries.append((path, ChangeEntry(ChangeKind.CREATED, new=new[path])))
        elif path not in new:
            entries.append((path, ChangeEntry(ChangeKind.DELETED, old=old[path])))
        elif old[path] != new[path]:
            entries.append((path, ChangeEntry(ChangeKind.MODIFIED, old[path], new[path])))
    return TermResult(value=ChangeSet(tuple(entries)))


def _selector_domain(selector: ArtifactSelector, snapshot: RepositorySnapshot) -> frozenset[Path]:
    if selector.tag in {SelectorTag.PATHS, SelectorTag.PATHS_WITH_ROLE}:
        return selector.paths
    assert selector.role is not None
    return frozenset(path for path, artifact in snapshot.entries if artifact.role == selector.role)


def _selected_present(selector: ArtifactSelector, snapshot: RepositorySnapshot) -> tuple[ArtifactContent, ...]:
    values = []
    snapshot_map = snapshot.as_map()
    for path in _selector_domain(selector, snapshot):
        artifact = snapshot_map.get(path)
        if artifact is None:
            continue
        if selector.tag is SelectorTag.PATHS_WITH_ROLE and artifact.role != selector.role:
            continue
        values.append(artifact)
    return tuple(values)


def _project(projection: ArtifactProjection, artifact: ArtifactContent) -> ObservationValue:
    if projection.tag is ProjectionTag.PRESENCE:
        return ObservationValue(ObservationValueTag.PRESENT)
    if projection.tag is ProjectionTag.CONTENT:
        return ObservationValue(ObservationValueTag.PRESENT_CONTENT, (artifact,))
    if projection.tag is ProjectionTag.FORMAT_ONLY:
        return ObservationValue(ObservationValueTag.PRESENT_FORMAT, (artifact.format,))
    if projection.tag is ProjectionTag.SIZE_ONLY:
        return ObservationValue(ObservationValueTag.PRESENT_SIZE, (artifact.size,))
    assert projection.field is not None
    if artifact.tag is not ArtifactTag.STRUCTURED:
        return ObservationValue(
            ObservationValueTag.PROJECTION_MISMATCH,
            (artifact.body_kind, projection),
        )
    fields = dict(artifact.fields)
    if projection.field not in fields:
        return ObservationValue(ObservationValueTag.ABSENT)
    return ObservationValue(ObservationValueTag.PRESENT_FIELD, (fields[projection.field],))


def _artifact_observation(spec: ObservationSpec, snapshot: RepositorySnapshot) -> ObservationResult:
    assert spec.selector is not None and spec.projection is not None
    snapshot_map = snapshot.as_map()
    values: list[tuple[Path, ObservationValue]] = []
    for path in sorted(_selector_domain(spec.selector, snapshot)):
        artifact = snapshot_map.get(path)
        if artifact is None:
            value = ObservationValue(ObservationValueTag.ABSENT)
        elif spec.selector.tag is SelectorTag.PATHS_WITH_ROLE and artifact.role != spec.selector.role:
            value = ObservationValue(
                ObservationValueTag.ROLE_MISMATCH,
                (artifact.role, spec.selector.role),
            )
        else:
            value = _project(spec.projection, artifact)
        values.append((path, value))
    return ObservationResult(
        ObservationResultTag.ARTIFACT,
        spec,
        Coverage(CoverageTag.COMPLETE),
        tuple(values),
    )


def _behavior_candidates(spec: ObservationSpec, subject: SubjectId, snapshot: RepositorySnapshot) -> frozenset[BehaviorValue]:
    selected_paths = _selector_domain(spec.selector, snapshot) if spec.selector is not None else frozenset(path for path, _ in snapshot.entries)
    raw = {
        value
        for path, artifact in snapshot.entries
        if path in selected_paths
        if spec.selector is None or spec.selector.tag is not SelectorTag.PATHS_WITH_ROLE or artifact.role == spec.selector.role
        if artifact.tag is ArtifactTag.BEHAVIOR
        for key, value in artifact.observations
        if key == subject
    }
    if spec.tag is ObservationSpecTag.REQUEST_BEHAVIOR_VIEW:
        return frozenset(value for value in raw if value.tag in {BehaviorTag.ACCEPTED, BehaviorTag.REJECTED})
    if spec.tag is ObservationSpecTag.WORKLOAD_METRIC_VIEW:
        return frozenset(value for value in raw if value.tag is BehaviorTag.METRIC and value.metric == spec.metric)
    if spec.tag is ObservationSpecTag.DEPENDENCY_RESOLUTION_VIEW:
        return frozenset(value for value in raw if value.tag is BehaviorTag.RESOLUTION)
    if spec.tag is ObservationSpecTag.CLIENT_ADAPTER_VIEW:
        return frozenset(value for value in raw if value.tag is BehaviorTag.CORRESPONDENCE)
    raise FiniteCodingProfileError("artifact view has no behavior candidates")


def _aggregate(values: frozenset[BehaviorValue]) -> ObservationValue | None:
    if not values:
        return None
    if len(values) > 1:
        return ObservationValue(ObservationValueTag.BEHAVIOR_CONFLICT, (values,))
    value = next(iter(values))
    if value.tag is BehaviorTag.ACCEPTED:
        return ObservationValue(ObservationValueTag.ACCEPTED)
    if value.tag is BehaviorTag.REJECTED:
        return ObservationValue(ObservationValueTag.REJECTED)
    if value.tag is BehaviorTag.METRIC:
        return ObservationValue(ObservationValueTag.METRIC_VALUE, (value.integer,))
    if value.tag is BehaviorTag.RESOLUTION:
        return ObservationValue(ObservationValueTag.RESOLUTION_VALUE, (value.content,))
    return ObservationValue(ObservationValueTag.CORRESPONDENCE_VALUE, (value.left, value.right))


def _behavior_observation(spec: ObservationSpec, snapshot: RepositorySnapshot) -> ObservationResult:
    values = []
    missing = set()
    for subject in sorted(spec.domain, key=lambda item: (item.tag.value, item.atom)):
        aggregate = _aggregate(_behavior_candidates(spec, subject, snapshot))
        if aggregate is None:
            missing.add(subject)
        else:
            values.append((subject, aggregate))
    coverage = Coverage(CoverageTag.INCOMPLETE_SUBJECTS, frozenset(missing)) if missing else Coverage(CoverageTag.COMPLETE)
    result_tag = {
        ObservationSpecTag.REQUEST_BEHAVIOR_VIEW: ObservationResultTag.SUBJECT,
        ObservationSpecTag.WORKLOAD_METRIC_VIEW: ObservationResultTag.SUBJECT,
        ObservationSpecTag.DEPENDENCY_RESOLUTION_VIEW: ObservationResultTag.LANE,
        ObservationSpecTag.CLIENT_ADAPTER_VIEW: ObservationResultTag.CORRESPONDENCE,
    }[spec.tag]
    return ObservationResult(result_tag, spec, coverage, tuple(values))


def observe(spec: ObservationSpec, snapshot: RepositorySnapshot) -> TermResult:
    if not isinstance(spec, ObservationSpec) or not isinstance(snapshot, RepositorySnapshot):
        return TermResult(error="INVALID_OBSERVATION_INPUT")
    if spec.tag is ObservationSpecTag.ARTIFACT_VIEW:
        return TermResult(value=_artifact_observation(spec, snapshot))
    return TermResult(value=_behavior_observation(spec, snapshot))


def observations_equal(left: ObservationResult, right: ObservationResult) -> Eval:
    if not isinstance(left, ObservationResult) or not isinstance(right, ObservationResult):
        return Eval(None, errors=frozenset({"INVALID_OBSERVATION_RESULT"}))
    return Eval(Truth.TRUE if left == right else Truth.FALSE)


def _coding_projection(entries: Iterable[CodingEvidenceEntry]) -> tuple[dict[EvidenceRef, CodingEvidencePayload] | None, frozenset[str]]:
    grouped: dict[EvidenceRef, set[CodingEvidencePayload]] = {}
    for entry in entries:
        if not isinstance(entry, CodingEvidenceEntry):
            return None, frozenset({"EVIDENCE_SCHEMA_ERROR"})
        schema = entry.reference.schema_binding
        if schema not in {VERIFICATION_SCHEMA, IMPLEMENTATION_PROFILE_SCHEMA}:
            continue
        expected = EvidencePayloadTag.VERIFICATION if schema == VERIFICATION_SCHEMA else EvidencePayloadTag.IMPLEMENTATION_PROFILE
        if entry.payload.tag is not expected:
            return None, frozenset({"EVIDENCE_SCHEMA_ERROR"})
        if entry.payload.tag is EvidencePayloadTag.VERIFICATION:
            record = entry.payload.value
            assert isinstance(record, VerificationRecord)
            if entry.reference not in record.evidence_refs:
                return None, frozenset({"EVIDENCE_REFERENCE_ERROR"})
        grouped.setdefault(entry.reference, set()).add(entry.payload)
    conflicts = frozenset(
        f"EVIDENCE_REFERENCE_CONFLICT:{reference.stable_identity}"
        for reference, values in grouped.items()
        if len(values) > 1
    )
    if conflicts:
        return None, conflicts
    return {reference: next(iter(values)) for reference, values in grouped.items()}, frozenset()


def verification_passed(spec: VerificationSpec, snapshot: RepositorySnapshot, evidence: frozenset[CodingEvidenceEntry]) -> Eval:
    evidence_map, errors = _coding_projection(evidence)
    if errors:
        return Eval(None, errors=errors)
    assert evidence_map is not None
    matching: list[tuple[EvidenceRef, VerificationRecord]] = []
    for reference, payload in evidence_map.items():
        if payload.tag is not EvidencePayloadTag.VERIFICATION:
            continue
        record = payload.value
        assert isinstance(record, VerificationRecord)
        # K3-S §2.2 uses exactly: spec identity, final snapshot identity,
        # observation-subject/spec identity, and evidence-map membership.  It
        # deliberately does not re-observe or compare a returned value.
        if (
            record.spec == spec
            and record.snapshot_identity == SnapshotIdentity(snapshot)
            and record.observation.spec_identity == spec.subject
            and reference.schema_binding == spec.evidence_schema_key
        ):
            matching.append((reference, record))
    statuses = {record.status for _, record in matching}
    refs = frozenset(reference for reference, _ in matching)
    reasons = frozenset(
        f"INCONCLUSIVE:{reference.stable_identity}"
        for reference, record in matching
        if record.status is VerificationStatus.INCONCLUSIVE
    )
    if VerificationStatus.PASS in statuses and VerificationStatus.FAIL in statuses:
        return Eval(None, errors=frozenset({"OPPOSITE_DECISIVE_RECORD_CONFLICT"}))
    if VerificationStatus.FAIL in statuses:
        return Eval(Truth.FALSE, refs, reasons)
    if VerificationStatus.PASS in statuses:
        return Eval(Truth.TRUE, refs, reasons)
    if not reasons:
        reasons = frozenset({f"MISSING_VERIFICATION:{spec.protocol_identity}"})
    return Eval(Truth.UNKNOWN, refs, reasons)


def _relation_result(relation: ObservationRelation, current: ObservationResult, baseline: ObservationResult) -> Eval:
    if current.coverage.tag is CoverageTag.INCOMPLETE_SUBJECTS or baseline.coverage.tag is CoverageTag.INCOMPLETE_SUBJECTS:
        missing = current.coverage.missing_subjects | baseline.coverage.missing_subjects
        return Eval(Truth.UNKNOWN, reasons=frozenset({"INCOMPLETE_SUBJECTS:" + ",".join(sorted(item.atom for item in missing))}))
    conflict_tags = {ObservationValueTag.BEHAVIOR_CONFLICT, ObservationValueTag.PROJECTION_MISMATCH}
    if any(value.tag in conflict_tags for _, value in (*current.values, *baseline.values)):
        return Eval(None, errors=frozenset({"OBSERVATION_SCHEMA_OR_CONFLICT"}))
    if relation.tag is ObservationRelationTag.EQUAL:
        answer = current == baseline
    elif relation.tag is ObservationRelationTag.ACCEPT_REJECT_EQUAL:
        answer = current.values == baseline.values and all(value.tag in {ObservationValueTag.ACCEPTED, ObservationValueTag.REJECTED} for _, value in current.values)
    elif relation.tag in {ObservationRelationTag.NO_GREATER, ObservationRelationTag.STRICTLY_LOWER}:
        left = tuple(value.payload[0] for _, value in current.values if value.tag is ObservationValueTag.METRIC_VALUE)
        right = tuple(value.payload[0] for _, value in baseline.values if value.tag is ObservationValueTag.METRIC_VALUE)
        if len(left) != len(current.values) or len(right) != len(baseline.values) or len(left) != len(right):
            answer = False
        elif relation.tag is ObservationRelationTag.NO_GREATER:
            answer = all(a <= b for a, b in zip(left, right))
        else:
            answer = all(a < b for a, b in zip(left, right))
    else:
        mapping = dict(relation.field_bijection)
        answer = True
        for _, value in current.values:
            if value.tag is not ObservationValueTag.CORRESPONDENCE_VALUE:
                answer = False
                break
            left_map, right_map = map(dict, value.payload)
            answer = answer and set(mapping) == set(left_map) and set(mapping.values()) == set(right_map) and all(left_map[key] == right_map[mapping[key]] for key in mapping)
    return Eval(Truth.TRUE if answer else Truth.FALSE)


def _criterion_result(criterion: Criterion, snapshot: RepositorySnapshot) -> Eval:
    if isinstance(criterion, ObservationEquals):
        current = observe(criterion.spec, snapshot)
        return observations_equal(current.value, criterion.expected) if current.is_value else Eval(None, errors=frozenset({current.error or "TERM_ERROR"}))
    if isinstance(criterion, (OneFormatOf, ArtifactsNonempty, ArtifactSizeLt, ArtifactSizeAtLeast)):
        population = _selected_present(criterion.selector, snapshot)
        if not population:
            return Eval(Truth.FALSE)
        if isinstance(criterion, OneFormatOf):
            answer = all(artifact.format in criterion.formats for artifact in population)
        elif isinstance(criterion, ArtifactsNonempty):
            answer = True
        elif isinstance(criterion, ArtifactSizeLt):
            answer = all(artifact.size.kib < criterion.upper.kib for artifact in population)
        else:
            answer = all(artifact.size.kib >= criterion.lower.kib for artifact in population)
        return Eval(Truth.TRUE if answer else Truth.FALSE)
    if isinstance(criterion, UniversalObservation):
        current = observe(criterion.spec, snapshot)
        return _relation_result(criterion.relation, current.value, criterion.baseline) if current.is_value else Eval(None, errors=frozenset({current.error or "TERM_ERROR"}))
    if isinstance(criterion, DependencyReproducible):
        current = observe(criterion.spec, snapshot)
        if not current.is_value:
            return Eval(None, errors=frozenset({current.error or "TERM_ERROR"}))
        result = current.value
        if result.coverage.tag is CoverageTag.INCOMPLETE_SUBJECTS:
            return Eval(Truth.UNKNOWN, reasons=frozenset({"INCOMPLETE_DEPENDENCY_DOMAIN"}))
        if any(value.tag is ObservationValueTag.BEHAVIOR_CONFLICT for _, value in result.values):
            return Eval(None, errors=frozenset({"OBSERVATION_SCHEMA_OR_CONFLICT"}))
        values = tuple(value.payload[0] for _, value in result.values if value.tag is ObservationValueTag.RESOLUTION_VALUE)
        answer = len(values) == len(result.values) and len(values) >= 2 and len(set(values)) == 1
        return Eval(Truth.TRUE if answer else Truth.FALSE)
    if isinstance(criterion, AdapterCorresponds):
        current = observe(criterion.spec, snapshot)
        if not current.is_value:
            return Eval(None, errors=frozenset({current.error or "TERM_ERROR"}))
        return _relation_result(criterion.relation, current.value, current.value)
    raise FiniteCodingProfileError(f"unsupported criterion: {type(criterion).__name__}")


def _conjoin(results: Iterable[Eval]) -> Eval:
    values = tuple(results)
    errors = frozenset().union(*(value.errors for value in values))
    evidence = frozenset().union(*(value.evidence_refs for value in values))
    reasons = frozenset().union(*(value.reasons for value in values))
    if errors:
        return Eval(None, evidence, reasons, errors)
    truths = {value.truth for value in values}
    if Truth.FALSE in truths:
        return Eval(Truth.FALSE, evidence, reasons)
    if Truth.UNKNOWN in truths:
        return Eval(Truth.UNKNOWN, evidence, reasons)
    return Eval(Truth.TRUE, evidence, reasons)


def task_accepts(task: TaskSpec, final: RepositorySnapshot, evidence: frozenset[CodingEvidenceEntry]) -> Eval:
    if not isinstance(task, TaskSpec) or not isinstance(final, RepositorySnapshot):
        return Eval(None, errors=frozenset({"INVALID_TASK_INPUT"}))
    return _conjoin(
        (*(_criterion_result(criterion, final) for criterion in task.criteria), *(verification_passed(spec, final, evidence) for spec in task.required_verifications))
    )


def dependency_metadata_changed(changes: ChangeSet) -> Eval:
    if not isinstance(changes, ChangeSet):
        return Eval(None, errors=frozenset({"INVALID_CHANGE_SET"}))
    for _, entry in changes.entries:
        if (entry.old is not None and entry.old.role is ArtifactRole.DEPENDENCY_METADATA) or (entry.new is not None and entry.new.role is ArtifactRole.DEPENDENCY_METADATA):
            return Eval(Truth.TRUE)
    return Eval(Truth.FALSE)


def event_matches(pattern: EventPattern, event: EventValue) -> Eval:
    if not isinstance(pattern, EventPattern) or not isinstance(event, EventValue):
        return Eval(None, errors=frozenset({"MALFORMED_EVENT_INPUT"}))
    payload = event.payload
    if pattern.tag is PatternKind.ANY_EVENT:
        answer = event.key is pattern.event_key
    elif pattern.tag is PatternKind.COMMAND_IS:
        answer = isinstance(payload, CommandEventPayload) and payload.command_id == pattern.command_id
    elif pattern.tag is PatternKind.TEST_IS:
        answer = isinstance(payload, TestEventPayload) and payload.spec == pattern.verification_spec and payload.status in pattern.statuses
    elif pattern.tag is PatternKind.PATH_CHANGE_IN:
        answer = isinstance(payload, PathChangeEventPayload) and payload.path in pattern.paths and payload.change.kind in pattern.change_kinds
    elif pattern.tag is PatternKind.NETWORK_CLASS:
        answer = isinstance(payload, NetworkContactEventPayload) and payload.contact_class == pattern.contact_class
    elif pattern.tag is PatternKind.RELEASE_IS:
        answer = isinstance(payload, ReleaseEventPayload) and payload.release_id == pattern.release_id and payload.snapshot == pattern.snapshot
    elif pattern.tag is PatternKind.REFRESHES:
        answer = isinstance(payload, DependencyRefreshEventPayload) and payload.selector == pattern.selector and payload.snapshot == pattern.snapshot
    else:
        raise FiniteCodingProfileError(f"unsupported event pattern: {pattern.tag}")
    return Eval(Truth.TRUE if answer else Truth.FALSE)


def event_occurred(pattern: EventPattern, trace: frozenset[TraceEvent]) -> Eval:
    results = tuple(event_matches(pattern, item.event_value) for item in trace)
    errors = frozenset().union(*(result.errors for result in results))
    if errors:
        return Eval(None, errors=errors)
    return Eval(Truth.TRUE if any(result.truth is Truth.TRUE for result in results) else Truth.FALSE)


def refresh_scope(event: EventValue) -> Eval:
    answer = isinstance(event, EventValue) and isinstance(event.payload, DependencyRefreshEventPayload) and event.payload.selector.tag in {SelectorTag.ROLE, SelectorTag.PATHS_WITH_ROLE} and event.payload.selector.role is ArtifactRole.DEPENDENCY_LOCK
    return Eval(Truth.TRUE if answer else Truth.FALSE)


def implementation_evidence_profile(subject: ImplementationCoverageSubject) -> ProfileResult:
    profile_key = "implementation_evidence"
    evidence_map, errors = _coding_projection(subject.evidence_store)
    if errors:
        return ProfileResult(ProfileTag.EVALUATION_ERROR, profile_key, errors=errors)
    expected_task = task_accepts(subject.task, subject.snapshot, subject.evidence_store)
    if subject.task_result != expected_task:
        return ProfileResult(ProfileTag.EVALUATION_ERROR, profile_key, errors=frozenset({"TASK_RESULT_MISMATCH"}))
    if expected_task.errors:
        return ProfileResult(ProfileTag.EVALUATION_ERROR, profile_key, errors=expected_task.errors)
    abstract = subject.abstract_result
    assert evidence_map is not None
    d_abs = "abstract_acceptance_evidence"
    d_conc = "concrete_implementation_evidence"
    covered = set()
    pending = set()
    witnesses = set()
    pending_reasons = set()
    for reference, payload in evidence_map.items():
        if payload.tag is not EvidencePayloadTag.IMPLEMENTATION_PROFILE:
            continue
        item = payload.value
        assert isinstance(item, ImplementationEvidence)
        if item.contract_identity != subject.contract_identity or item.snapshot_identity != SnapshotIdentity(subject.snapshot):
            continue
        if item.tag is ImplementationEvidenceTag.ABSTRACT_ACCEPTANCE:
            abstract = subject.abstract_result
            if abstract.tag is AbstractCoverageTag.REASONING and abstract.result is not None and abstract.result.tag is ReasoningTag.ADMITTED_JUDGMENT and abstract.result.judgment == "CONSISTENCY_SAT" and abstract.result.certificate_key == item.certificate_key:
                covered.add(d_abs)
                witnesses.add(reference)
        elif item.tag is ImplementationEvidenceTag.CONCRETE_IMPLEMENTATION:
            covered.add(d_conc)
            witnesses.add(reference)
        else:
            assert item.dimension is not None and item.reason is not None
            pending.add(item.dimension)
            pending_reasons.add(item.reason)
    dimensions = {d_abs, d_conc}
    missing = dimensions - covered
    if not missing:
        return ProfileResult(ProfileTag.COMPLETE, profile_key, frozenset(witnesses))
    reasons = set(pending_reasons if missing & pending else ())
    reasons.update(expected_task.reasons if expected_task.truth is Truth.UNKNOWN else ())
    if abstract.tag is AbstractCoverageTag.REASONING and abstract.result is not None and abstract.result.tag is ReasoningTag.COMPLETED_INCONCLUSIVE:
        reasons.update(abstract.result.reasons)
    if reasons:
        return ProfileResult(ProfileTag.UNKNOWN, profile_key, reasons=frozenset(reasons))
    return ProfileResult(ProfileTag.INCOMPLETE, profile_key, missing_dimensions=frozenset(missing))


def enforce_declared_access(requested_facets: frozenset[str], allowed_facets: frozenset[str]) -> None:
    undeclared = requested_facets - allowed_facets
    if undeclared:
        raise UndeclaredAccessError("UNDECLARED_ACCESS:" + ",".join(sorted(undeclared)))


def invoke_with_declared_access(requested_facets: frozenset[str], allowed_facets: frozenset[str], meaning: Callable[..., Any], arguments: tuple[Any, ...]) -> Any:
    enforce_declared_access(requested_facets, allowed_facets)
    if not callable(meaning):
        raise TypeError("meaning must be callable")
    return meaning(*arguments)
