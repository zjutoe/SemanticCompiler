"""Strict controlled-language extraction and bridge for the Phase 0 C path."""

from __future__ import annotations

from dataclasses import dataclass

from Phase0.implementation.dialect import PREDICATES, PredicateDefinition
from Phase0.implementation.schema import (
    CanonicalSemanticState,
    ContextAvailability,
    ContextValue,
    Modality,
    NormativeCandidate,
    OpenOwner,
    OpenSlotMention,
    OpenTerm,
    PredicateScope,
    SourceEnvelope,
    SourceRole,
    SourceSpan,
    TYPE_VALUE_ORDER,
    TypedValue,
    ValueTerm,
    VisibleWorldContext,
)


class CPathFailure(ValueError):
    """Loud C-path failure with a stable public stage and reason."""

    def __init__(self, stage: str, reason: str) -> None:
        self.stage = stage
        self.reason = reason
        super().__init__(f"{stage}/{reason}")


@dataclass(frozen=True)
class ExtractiveContentState:
    content_refs: tuple[str, ...]


@dataclass(frozen=True)
class ReferencedSupportView:
    spans: tuple[SourceSpan, ...]


@dataclass(frozen=True)
class _InterpretedAtom:
    modality: str
    definition: PredicateDefinition
    argument_kind: str
    argument_value: str


def _fail(stage: str, reason: str) -> None:
    raise CPathFailure(stage, reason)


def _valid_atomic_span(span: object) -> bool:
    if type(span) is not SourceSpan:
        return False
    if type(span.ref) is not str or not span.ref:
        return False
    if type(span.role) is not str or span.role not in SourceRole.values():
        return False
    if type(span.text) is not str or not span.text or span.text != span.text.strip():
        return False
    if "\n" in span.text or "\r" in span.text:
        return False
    return span.text.endswith(".") and span.text.count(".") == 1


def _fresh_span(span: SourceSpan) -> SourceSpan:
    return SourceSpan(ref=span.ref, role=span.role, text=span.text)


def segment_source(source_envelope: SourceEnvelope) -> tuple[SourceSpan, ...]:
    """Validate and freshly copy the envelope's existing atomic spans."""

    reason = "INVALID_SOURCE_ENVELOPE"
    if type(source_envelope) is not SourceEnvelope:
        _fail("surface", reason)
    if type(source_envelope.spans) is not tuple:
        _fail("surface", reason)
    refs: set[str] = set()
    for span in source_envelope.spans:
        if not _valid_atomic_span(span) or span.ref in refs:
            _fail("surface", reason)
        refs.add(span.ref)
    return tuple(_fresh_span(span) for span in source_envelope.spans)


def _is_identifier(value: str) -> bool:
    if not value or not ("A" <= value[0] <= "Z"):
        return False
    return all(
        "A" <= character <= "Z"
        or "0" <= character <= "9"
        or character == "_"
        for character in value[1:]
    )


def _recognize_atom(text: str) -> tuple[str, str] | None:
    tokens = text[:-1].split(" ")
    if len(tokens) == 4 and tokens[:3] == ["Require", "final", "format"]:
        argument = tokens[3]
        if _is_identifier(argument):
            return "FORMAT_VALUE", argument
        if argument.startswith("OPEN(") and argument.endswith(")"):
            owner = argument[5:-1]
            if _is_identifier(owner):
                return "FORMAT_OPEN", owner
        return None
    if len(tokens) == 2 and tokens[0] == "Use" and _is_identifier(tokens[1]):
        return "FORMAT_VALUE", tokens[1]
    if (
        len(tokens) == 4
        and tokens[:3] == ["Allow", "managed", "effect"]
        and _is_identifier(tokens[3])
    ):
        return "EFFECT", tokens[3]
    return None


def normal_c_extract(source_envelope: SourceEnvelope) -> ExtractiveContentState:
    """Select every lexically representable atom in exact source order."""

    spans = segment_source(source_envelope)
    refs = tuple(span.ref for span in spans if _recognize_atom(span.text) is not None)
    if not refs:
        _fail("surface", "NO_REPRESENTABLE_CONTENT")
    return ExtractiveContentState(content_refs=refs)


def _validate_surface_state(state: object) -> tuple[str, ...]:
    if type(state) is not ExtractiveContentState:
        _fail("surface", "INVALID_EXTRACTIVE_CONTENT")
    refs = state.content_refs
    if type(refs) is not tuple or not refs:
        _fail("surface", "INVALID_EXTRACTIVE_CONTENT")
    if any(type(ref) is not str or not ref for ref in refs):
        _fail("surface", "INVALID_EXTRACTIVE_CONTENT")
    return refs


def build_referenced_support_view(
    source_envelope: SourceEnvelope,
    content_state: ExtractiveContentState,
) -> ReferencedSupportView:
    """Dereference exactly the selected source spans and freshly copy them."""

    spans = segment_source(source_envelope)
    refs = _validate_surface_state(content_state)
    if len(set(refs)) != len(refs):
        _fail("surface", "INVALID_CONTENT_REFS")
    positions = {span.ref: index for index, span in enumerate(spans)}
    if any(ref not in positions for ref in refs):
        _fail("surface", "INVALID_CONTENT_REFS")
    indices = tuple(positions[ref] for ref in refs)
    if indices != tuple(sorted(indices)):
        _fail("surface", "INVALID_CONTENT_REFS")
    by_ref = {span.ref: span for span in spans}
    return ReferencedSupportView(
        spans=tuple(_fresh_span(by_ref[ref]) for ref in refs),
    )


def _validate_bridge_state(state: object) -> tuple[str, ...]:
    if type(state) is not ExtractiveContentState:
        _fail("adapter_or_bridge", "INVALID_EXTRACTIVE_CONTENT")
    refs = state.content_refs
    if type(refs) is not tuple or not refs:
        _fail("adapter_or_bridge", "INVALID_EXTRACTIVE_CONTENT")
    if any(type(ref) is not str or not ref for ref in refs):
        _fail("adapter_or_bridge", "INVALID_EXTRACTIVE_CONTENT")
    if len(set(refs)) != len(refs):
        _fail("adapter_or_bridge", "INVALID_EXTRACTIVE_CONTENT")
    return refs


def _validate_support_view(view: object) -> tuple[SourceSpan, ...]:
    reason = "INVALID_REFERENCED_SUPPORT_VIEW"
    if type(view) is not ReferencedSupportView or type(view.spans) is not tuple:
        _fail("adapter_or_bridge", reason)
    if not view.spans:
        _fail("adapter_or_bridge", reason)
    refs: set[str] = set()
    for span in view.spans:
        if not _valid_atomic_span(span) or span.ref in refs:
            _fail("adapter_or_bridge", reason)
        refs.add(span.ref)
    return view.spans


def _validate_manifest(
    manifest: object,
) -> tuple[PredicateDefinition, ...]:
    reason = "INVALID_DIALECT_MANIFEST"
    if type(manifest) is not tuple:
        _fail("adapter_or_bridge", reason)
    for definition in manifest:
        if type(definition) is not PredicateDefinition:
            _fail("adapter_or_bridge", reason)
        if type(definition.predicate) is not str or not definition.predicate:
            _fail("adapter_or_bridge", reason)
        if type(definition.signature) is not tuple or any(
            type(type_id) is not str for type_id in definition.signature
        ):
            _fail("adapter_or_bridge", reason)
        if (
            type(definition.scope) is not str
            or definition.scope not in PredicateScope.values()
            or type(definition.interpretation) is not str
        ):
            _fail("adapter_or_bridge", reason)
    if manifest != PREDICATES:
        _fail("adapter_or_bridge", reason)
    return manifest


def _validate_context(
    context: object,
    definitions: dict[str, PredicateDefinition],
) -> VisibleWorldContext:
    reason = "INVALID_VISIBLE_WORLD_CONTEXT"
    if type(context) is not VisibleWorldContext:
        _fail("adapter_or_bridge", reason)
    if type(context.entities) is not tuple or context.entities:
        _fail("adapter_or_bridge", reason)
    if type(context.observable_values) is not tuple:
        _fail("adapter_or_bridge", reason)
    for observation in context.observable_values:
        if type(observation) is not ContextValue:
            _fail("adapter_or_bridge", reason)
        if type(observation.predicate) is not str:
            _fail("adapter_or_bridge", reason)
        definition = definitions.get(observation.predicate)
        if definition is None:
            _fail("adapter_or_bridge", reason)
        if (
            type(observation.scope) is not str
            or observation.scope not in ContextAvailability.values()
            or type(observation.args) is not tuple
            or len(observation.args) != len(definition.signature)
            or type(observation.value) is not bool
        ):
            _fail("adapter_or_bridge", reason)
        for argument, expected_type in zip(
            observation.args,
            definition.signature,
            strict=True,
        ):
            if type(argument) is not TypedValue:
                _fail("adapter_or_bridge", reason)
            if (
                type(argument.type) is not str
                or type(argument.value) is not str
                or argument.type != expected_type
            ):
                _fail("adapter_or_bridge", reason)
            members = TYPE_VALUE_ORDER.get(expected_type)
            if members is None or argument.value not in members:
                _fail("adapter_or_bridge", reason)
    return context


def _interpret_atom(
    span: SourceSpan,
    definitions: dict[str, PredicateDefinition],
) -> _InterpretedAtom:
    recognized = _recognize_atom(span.text)
    if recognized is None:
        _fail("adapter_or_bridge", "UNSUPPORTED_CONTENT")
    kind, value = recognized
    if kind in ("FORMAT_VALUE", "FORMAT_OPEN"):
        modality = Modality.REQUIRE.value
        definition = definitions.get("world.final_format_is")
        if (
            modality not in Modality.values()
            or definition is None
            or definition.scope != PredicateScope.FINAL.value
            or len(definition.signature) != 1
        ):
            _fail("adapter_or_bridge", "UNSUPPORTED_CONTENT")
        argument_type = definition.signature[0]
        members = TYPE_VALUE_ORDER.get(argument_type)
        if members is None:
            _fail("adapter_or_bridge", "UNSUPPORTED_CONTENT")
        if kind == "FORMAT_VALUE" and value not in members:
            _fail("adapter_or_bridge", "UNSUPPORTED_CONTENT")
        if kind == "FORMAT_OPEN" and value not in OpenOwner.values():
            _fail("adapter_or_bridge", "UNSUPPORTED_CONTENT")
        return _InterpretedAtom(modality, definition, kind, value)

    modality = Modality.ALLOW.value
    definition = definitions.get(f"effect.{value}")
    if (
        modality not in Modality.values()
        or definition is None
        or definition.signature != ()
        or definition.scope != PredicateScope.EVENT.value
    ):
        _fail("adapter_or_bridge", "UNSUPPORTED_CONTENT")
    return _InterpretedAtom(modality, definition, kind, value)


def beta_C(
    content_state: ExtractiveContentState,
    support_view: ReferencedSupportView,
    manifest: tuple[PredicateDefinition, ...],
    visible_world_context: VisibleWorldContext,
) -> CanonicalSemanticState:
    """Interpret the frozen controlled language into canonical semantics."""

    refs = _validate_bridge_state(content_state)
    spans = _validate_support_view(support_view)
    if refs != tuple(span.ref for span in spans):
        _fail("adapter_or_bridge", "CONTENT_VIEW_MISMATCH")
    checked_manifest = _validate_manifest(manifest)
    definitions = {
        definition.predicate: definition for definition in checked_manifest
    }
    _validate_context(visible_world_context, definitions)
    interpreted = tuple(_interpret_atom(span, definitions) for span in spans)

    candidates: list[NormativeCandidate] = []
    mentions: list[OpenSlotMention] = []
    for clause_index, (span, atom) in enumerate(zip(spans, interpreted, strict=True)):
        clause_link = f"clause:{clause_index:03d}"
        support = (span.ref,)
        if atom.argument_kind == "FORMAT_VALUE":
            terms = (
                ValueTerm(
                    kind="VALUE",
                    value=TypedValue(
                        type=atom.definition.signature[0],
                        value=atom.argument_value,
                    ),
                ),
            )
        elif atom.argument_kind == "FORMAT_OPEN":
            semantic_slot_link = f"slot:{clause_link}:arg0"
            terms = (
                OpenTerm(
                    kind="OPEN",
                    type=atom.definition.signature[0],
                    semantic_slot_link=semantic_slot_link,
                ),
            )
            mentions.append(
                OpenSlotMention(
                    type=atom.definition.signature[0],
                    owner=atom.argument_value,
                    proposition_link=clause_link,
                    argument_position=0,
                    proposition_support=support,
                )
            )
        else:
            terms = ()
        candidates.append(
            NormativeCandidate(
                modality=atom.modality,
                predicate=atom.definition.predicate,
                args=terms,
                proposition_support=support,
                claimed_authority_support=support,
            )
        )
    return CanonicalSemanticState(
        normative_candidates=tuple(candidates),
        knowledge_assertions=(),
        open_slot_mentions=tuple(mentions),
    )
