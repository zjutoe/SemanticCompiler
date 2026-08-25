"""Finite immutable input records for Phase 0 E0 fixtures."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence


class StrictSchemaError(ValueError):
    """Raised when a fixture input violates the frozen E0 record syntax."""


class _StrEnum(str, Enum):
    @classmethod
    def values(cls) -> tuple[str, ...]:
        return tuple(member.value for member in cls)


class SourceRole(_StrEnum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    TOOL = "TOOL"


class NormativeAuthority(_StrEnum):
    USER = "USER"
    NONE = "NONE"


class OpenOwner(_StrEnum):
    USER = "USER"
    EXECUTOR = "EXECUTOR"


class Modality(_StrEnum):
    GOAL = "GOAL"
    REQUIRE = "REQUIRE"
    PRESERVE = "PRESERVE"
    FORBID = "FORBID"
    ALLOW = "ALLOW"


class PredicateScope(_StrEnum):
    INITIAL = "INITIAL"
    FINAL = "FINAL"
    TRACE = "TRACE"
    EVENT = "EVENT"


class ContextAvailability(_StrEnum):
    STATIC = "STATIC"
    INITIAL = "INITIAL"


class OutputFormat(_StrEnum):
    UNSET = "UNSET"
    JSON = "JSON"
    YAML = "YAML"


class Strictness(_StrEnum):
    STRICT = "STRICT"
    LENIENT = "LENIENT"


class ErrorPolicy(_StrEnum):
    RETURN_NONE = "RETURN_NONE"
    RAISE = "RAISE"


class LogMode(_StrEnum):
    QUIET = "QUIET"
    VERBOSE = "VERBOSE"


class ServiceMode(_StrEnum):
    SAFE = "SAFE"
    FAST = "FAST"


class Backend(_StrEnum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"


class EntryStage(_StrEnum):
    CANONICAL = "CANONICAL"
    SOURCE = "SOURCE"
    EXTRACTIVE_CONTENT = "EXTRACTIVE_CONTENT"
    ADAPTER = "ADAPTER"


class AssertionBasis(_StrEnum):
    EXPLICIT_STATEMENT = "EXPLICIT_STATEMENT"
    OBSERVATION = "OBSERVATION"
    DERIVATION = "DERIVATION"
    ASSUMPTION = "ASSUMPTION"


class AssertionCommitment(_StrEnum):
    ASSERTED = "ASSERTED"
    TENTATIVE = "TENTATIVE"
    DENIED = "DENIED"


ENUM_TYPES: Mapping[str, type[_StrEnum]] = {
    "SourceRole": SourceRole,
    "NormativeAuthority": NormativeAuthority,
    "OpenOwner": OpenOwner,
    "Modality": Modality,
    "PredicateScope": PredicateScope,
    "ContextAvailability": ContextAvailability,
    "OutputFormat": OutputFormat,
    "Strictness": Strictness,
    "ErrorPolicy": ErrorPolicy,
    "LogMode": LogMode,
    "ServiceMode": ServiceMode,
    "Backend": Backend,
}


TYPE_VALUE_ORDER: Mapping[str, tuple[str, ...]] = {
    "OutputFormat": OutputFormat.values(),
    "Strictness": Strictness.values(),
    "ErrorPolicy": ErrorPolicy.values(),
    "LogMode": LogMode.values(),
    "ServiceMode": ServiceMode.values(),
    "Backend": Backend.values(),
}


@dataclass(frozen=True)
class TypedValue:
    type: str
    value: str


@dataclass(frozen=True)
class ValueTerm:
    kind: str
    value: TypedValue


@dataclass(frozen=True)
class OpenTerm:
    kind: str
    type: str
    semantic_slot_link: str


Term = ValueTerm | OpenTerm


@dataclass(frozen=True)
class SourceSpan:
    ref: str
    role: str
    text: str


@dataclass(frozen=True)
class SourceEnvelope:
    spans: tuple[SourceSpan, ...]


@dataclass(frozen=True)
class NormativeCandidate:
    modality: str
    predicate: str
    args: tuple[Term, ...]
    proposition_support: tuple[str, ...]
    claimed_authority_support: tuple[str, ...]


@dataclass(frozen=True)
class KnowledgeAssertion:
    predicate: str
    args: tuple[Term, ...]
    basis: str
    commitment: str
    proposition_support: tuple[str, ...]


@dataclass(frozen=True)
class OpenSlotMention:
    type: str
    owner: str
    proposition_link: str
    argument_position: int
    proposition_support: tuple[str, ...]


@dataclass(frozen=True)
class CanonicalSemanticState:
    normative_candidates: tuple[NormativeCandidate, ...]
    knowledge_assertions: tuple[KnowledgeAssertion, ...]
    open_slot_mentions: tuple[OpenSlotMention, ...]


@dataclass(frozen=True)
class SlotDeclaration:
    semantic_slot_link: str
    type: str
    owner: str
    schema_domain: tuple[TypedValue, ...] | Any
    resolved_value: TypedValue | None


@dataclass(frozen=True)
class ContextValue:
    predicate: str
    scope: str
    args: tuple[TypedValue, ...]
    value: bool


@dataclass(frozen=True)
class VisibleWorldContext:
    entities: tuple[Any, ...]
    observable_values: tuple[ContextValue, ...]


@dataclass(frozen=True)
class StaticConstraint:
    constraint_link: str
    semantic_slot_link: str
    candidate_value: TypedValue
    context_predicate: str
    required_context_value: bool


@dataclass(frozen=True)
class CrossConstraint:
    constraint_link: str
    semantic_slot_links: tuple[str, str]
    allowed_tuples: tuple[tuple[TypedValue, TypedValue], ...]


@dataclass(frozen=True)
class CanonicalPayload:
    kind: str
    canonical_state: CanonicalSemanticState


@dataclass(frozen=True)
class SourcePayload:
    kind: str


@dataclass(frozen=True)
class ExtractiveContentPayload:
    kind: str
    content_refs: tuple[str, ...]


@dataclass(frozen=True)
class AdapterSurface:
    normative_candidates: tuple[NormativeCandidate, ...]


@dataclass(frozen=True)
class AdapterPayload:
    kind: str
    adapter_link: str | None
    surface: AdapterSurface


EntryPayload = CanonicalPayload | SourcePayload | ExtractiveContentPayload | AdapterPayload


@dataclass(frozen=True)
class FixtureInput:
    fixture_id: str
    case_id: str
    entry_stage: str
    source_envelope: SourceEnvelope | None
    entry_payload: EntryPayload
    visible_world_context: VisibleWorldContext
    slot_declarations: tuple[SlotDeclaration, ...]
    static_constraints: tuple[StaticConstraint, ...]
    cross_constraints: tuple[CrossConstraint, ...]
    candidate_trajectory_ids: tuple[str, ...]


def require_mapping(value: Any, where: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise StrictSchemaError(f"{where} must be an object")
    return value


def require_exact_keys(value: Mapping[str, Any], keys: Sequence[str], where: str) -> None:
    actual = tuple(value.keys())
    expected = tuple(keys)
    if actual != expected:
        raise StrictSchemaError(f"{where} keys {actual!r} != {expected!r}")


def require_string(value: Any, where: str) -> str:
    if not isinstance(value, str):
        raise StrictSchemaError(f"{where} must be a string")
    return value


def require_bool(value: Any, where: str) -> bool:
    if not isinstance(value, bool):
        raise StrictSchemaError(f"{where} must be a boolean")
    return value


def require_list(value: Any, where: str) -> list[Any]:
    if not isinstance(value, list):
        raise StrictSchemaError(f"{where} must be an array")
    return value


def require_enum(value: Any, enum_type: type[_StrEnum], where: str) -> str:
    raw = require_string(value, where)
    if raw not in enum_type.values():
        raise StrictSchemaError(f"{where} has unknown value {raw!r}")
    return raw


def parse_typed_value(value: Any, where: str) -> TypedValue:
    obj = require_mapping(value, where)
    require_exact_keys(obj, ("type", "value"), where)
    type_id = require_string(obj["type"], f"{where}.type")
    enum_type = ENUM_TYPES.get(type_id)
    if enum_type is None:
        raise StrictSchemaError(f"{where}.type has unknown enum type {type_id!r}")
    value_id = require_enum(obj["value"], enum_type, f"{where}.value")
    return TypedValue(type=type_id, value=value_id)


def parse_term(value: Any, where: str) -> Term:
    obj = require_mapping(value, where)
    kind = require_string(obj.get("kind"), f"{where}.kind")
    if kind == "VALUE":
        require_exact_keys(obj, ("kind", "value"), where)
        return ValueTerm(kind=kind, value=parse_typed_value(obj["value"], f"{where}.value"))
    if kind == "OPEN":
        require_exact_keys(obj, ("kind", "type", "semantic_slot_link"), where)
        type_id = require_string(obj["type"], f"{where}.type")
        if type_id not in TYPE_VALUE_ORDER:
            raise StrictSchemaError(f"{where}.type has unknown open enum type {type_id!r}")
        return OpenTerm(
            kind=kind,
            type=type_id,
            semantic_slot_link=require_string(obj["semantic_slot_link"], f"{where}.semantic_slot_link"),
        )
    raise StrictSchemaError(f"{where}.kind has unknown term kind {kind!r}")


def parse_ref_list(value: Any, where: str) -> tuple[str, ...]:
    refs = tuple(require_string(item, f"{where}[]") for item in require_list(value, where))
    if len(set(refs)) != len(refs):
        raise StrictSchemaError(f"{where} has duplicate refs")
    return refs
