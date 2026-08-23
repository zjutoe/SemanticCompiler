"""Deterministic canonical semantic elaboration for Phase 0 E1."""

from __future__ import annotations

from dataclasses import dataclass

from Phase0.implementation.dialect import PREDICATE_BY_ID
from Phase0.implementation.schema import (
    AssertionBasis,
    AssertionCommitment,
    CanonicalSemanticState,
    ContextAvailability,
    ContextValue,
    CrossConstraint,
    KnowledgeAssertion,
    Modality,
    NormativeAuthority,
    NormativeCandidate,
    OpenOwner,
    OpenSlotMention,
    OpenTerm,
    PredicateScope,
    SlotDeclaration,
    SourceEnvelope,
    SourceRole,
    SourceSpan,
    StaticConstraint,
    TYPE_VALUE_ORDER,
    TypedValue,
    ValueTerm,
    VisibleWorldContext,
)


class ElaborationFailure(ValueError):
    """Loud elaboration-stage failure with a stable public reason."""

    def __init__(self, reason: str) -> None:
        self.stage = "elaboration"
        self.reason = reason
        super().__init__(f"{self.stage}/{self.reason}")


@dataclass(frozen=True)
class ElaboratedCandidate:
    original: NormativeCandidate
    clause_link: str
    authority: str
    active: bool


@dataclass(frozen=True)
class ElaboratedOpenSlot:
    semantic_slot_link: str
    type: str
    owner: str
    resolved_value: TypedValue | None


@dataclass(frozen=True)
class SlotDomain:
    semantic_slot_link: str
    values: tuple[TypedValue, ...]


@dataclass(frozen=True)
class _StaticExclusion:
    semantic_slot_link: str
    value: TypedValue
    constraint_link: str


@dataclass(frozen=True)
class ElaboratedSemanticState:
    candidates: tuple[ElaboratedCandidate, ...]
    active_clause_links: tuple[str, ...]
    knowledge_assertions: tuple[KnowledgeAssertion, ...]
    open_slots: tuple[ElaboratedOpenSlot, ...]
    slot_domains: tuple[SlotDomain, ...]
    static_constraints: tuple[StaticConstraint, ...]
    cross_constraints: tuple[CrossConstraint, ...]
    constraint_links: tuple[str, ...]
    _schema_domains: tuple[SlotDomain, ...]
    _static_exclusions: tuple[_StaticExclusion, ...]


def _fail(reason: str) -> None:
    raise ElaborationFailure(reason)


def _require_tuple(value: object, reason: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        _fail(reason)
    return value


def _require_string(value: object, reason: str) -> str:
    if type(value) is not str:
        _fail(reason)
    return value


def _require_bool(value: object, reason: str) -> bool:
    if type(value) is not bool:
        _fail(reason)
    return value


def _validate_ref_tuple(value: object, reason: str) -> tuple[str, ...]:
    refs = _require_tuple(value, reason)
    for ref in refs:
        _require_string(ref, "INVALID_SUPPORT_REF")
    if len(set(refs)) != len(refs):
        _fail("DUPLICATE_SUPPORT_REF")
    return refs


def _validate_typed_value_record(value: object, reason: str) -> TypedValue:
    if not isinstance(value, TypedValue):
        _fail(reason)
    _require_string(value.type, "INVALID_TYPED_VALUE_SHAPE")
    _require_string(value.value, "INVALID_TYPED_VALUE_SHAPE")
    return value


def _validate_value_term(term: ValueTerm) -> None:
    _require_string(term.kind, "INVALID_VALUE_TERM_KIND")
    _validate_typed_value_record(term.value, "INVALID_TERM_VALUE_SHAPE")


def _validate_open_term(term: OpenTerm) -> None:
    _require_string(term.kind, "INVALID_OPEN_TERM_KIND")
    _require_string(term.type, "INVALID_OPEN_TERM_SHAPE")
    _require_string(term.semantic_slot_link, "INVALID_OPEN_TERM_SHAPE")


def _validate_terms(value: object) -> tuple[object, ...]:
    terms = _require_tuple(value, "INVALID_TERM_CONTAINER")
    for term in terms:
        if isinstance(term, ValueTerm):
            _validate_value_term(term)
        elif isinstance(term, OpenTerm):
            _validate_open_term(term)
        else:
            _fail("INVALID_TERM")
    return terms


def _validate_source_envelope(source_envelope: SourceEnvelope | None) -> None:
    if source_envelope is None:
        return
    if not isinstance(source_envelope, SourceEnvelope):
        _fail("INVALID_SOURCE_ENVELOPE_RECORD")
    spans = _require_tuple(source_envelope.spans, "INVALID_SOURCE_SPANS")
    for span in spans:
        if not isinstance(span, SourceSpan):
            _fail("INVALID_SOURCE_SPAN_RECORD")
        _require_string(span.ref, "INVALID_SOURCE_REF")
        _require_string(span.role, "INVALID_SOURCE_ROLE")
        _require_string(span.text, "INVALID_SOURCE_TEXT")


def _validate_candidate(candidate: object) -> None:
    if not isinstance(candidate, NormativeCandidate):
        _fail("INVALID_CANDIDATE_RECORD")
    _require_string(candidate.modality, "UNKNOWN_MODALITY")
    _require_string(candidate.predicate, "UNKNOWN_PREDICATE")
    _validate_terms(candidate.args)
    _validate_ref_tuple(candidate.proposition_support, "INVALID_SUPPORT_REFS")
    _validate_ref_tuple(candidate.claimed_authority_support, "INVALID_SUPPORT_REFS")


def _validate_knowledge_assertion(assertion: object) -> None:
    if not isinstance(assertion, KnowledgeAssertion):
        _fail("INVALID_KNOWLEDGE_RECORD")
    _require_string(assertion.predicate, "UNKNOWN_PREDICATE")
    _validate_terms(assertion.args)
    _require_string(assertion.basis, "INVALID_KNOWLEDGE_BASIS")
    _require_string(assertion.commitment, "INVALID_KNOWLEDGE_COMMITMENT")
    _validate_ref_tuple(assertion.proposition_support, "INVALID_SUPPORT_REFS")


def _validate_open_slot_mention(mention: object) -> None:
    if not isinstance(mention, OpenSlotMention):
        _fail("INVALID_OPEN_SLOT_MENTION_RECORD")
    _require_string(mention.type, "UNKNOWN_SLOT_TYPE")
    _require_string(mention.owner, "INVALID_OPEN_OWNER")
    _require_string(mention.proposition_link, "INVALID_OPEN_SLOT_MENTION_SHAPE")
    if type(mention.argument_position) is not int or mention.argument_position < 0:
        _fail("INVALID_OPEN_SLOT_MENTION_SHAPE")
    _validate_ref_tuple(mention.proposition_support, "INVALID_SUPPORT_REFS")


def _validate_canonical_state(canonical_state: CanonicalSemanticState) -> None:
    if not isinstance(canonical_state, CanonicalSemanticState):
        _fail("INVALID_CANONICAL_STATE_RECORD")
    candidates = _require_tuple(
        canonical_state.normative_candidates,
        "INVALID_CANDIDATE_CONTAINER",
    )
    assertions = _require_tuple(
        canonical_state.knowledge_assertions,
        "INVALID_KNOWLEDGE_CONTAINER",
    )
    mentions = _require_tuple(
        canonical_state.open_slot_mentions,
        "INVALID_OPEN_SLOT_MENTION_CONTAINER",
    )
    for candidate in candidates:
        _validate_candidate(candidate)
    for assertion in assertions:
        _validate_knowledge_assertion(assertion)
    for mention in mentions:
        _validate_open_slot_mention(mention)


def _validate_context_value(value: object) -> None:
    if not isinstance(value, ContextValue):
        _fail("INVALID_CONTEXT_VALUE_RECORD")
    _require_string(value.predicate, "UNKNOWN_PREDICATE")
    _require_string(value.scope, "INVALID_CONTEXT_SCOPE")
    if value.scope not in ContextAvailability.values():
        _fail("INVALID_CONTEXT_SCOPE")
    args = _require_tuple(value.args, "INVALID_CONTEXT_ARGS")
    definition = PREDICATE_BY_ID.get(value.predicate)
    if definition is None:
        _fail("UNKNOWN_PREDICATE")
    if len(args) != len(definition.signature):
        _fail("CONTEXT_SIGNATURE_MISMATCH")
    for arg, expected_type in zip(args, definition.signature, strict=True):
        typed_arg = _validate_typed_value_record(arg, "INVALID_CONTEXT_ARGUMENT")
        _check_typed_value(typed_arg, expected_type)
    _require_bool(value.value, "INVALID_CONTEXT_BOOL")


def _validate_visible_world_context(
    visible_world_context: VisibleWorldContext,
) -> None:
    if not isinstance(visible_world_context, VisibleWorldContext):
        _fail("INVALID_VISIBLE_CONTEXT_RECORD")
    entities = _require_tuple(visible_world_context.entities, "INVALID_CONTEXT_ENTITIES")
    if entities:
        _fail("UNSUPPORTED_CONTEXT_ENTITIES")
    observable_values = _require_tuple(
        visible_world_context.observable_values,
        "INVALID_CONTEXT_OBSERVABLES",
    )
    for value in observable_values:
        _validate_context_value(value)


def _validate_slot_declaration(declaration: object) -> None:
    if not isinstance(declaration, SlotDeclaration):
        _fail("INVALID_SLOT_DECLARATION_RECORD")
    _require_string(declaration.semantic_slot_link, "INVALID_SLOT_DECLARATION_SHAPE")
    _require_string(declaration.type, "UNKNOWN_SLOT_TYPE")
    _require_string(declaration.owner, "INVALID_OPEN_OWNER")
    if declaration.resolved_value is not None:
        _validate_typed_value_record(
            declaration.resolved_value,
            "INVALID_SLOT_DECLARATION_SHAPE",
        )


def _validate_static_constraint(constraint: object) -> None:
    if not isinstance(constraint, StaticConstraint):
        _fail("INVALID_STATIC_CONSTRAINT_RECORD")
    _require_string(constraint.constraint_link, "INVALID_STATIC_CONSTRAINT_SHAPE")
    _require_string(constraint.semantic_slot_link, "INVALID_STATIC_CONSTRAINT_SHAPE")
    _validate_typed_value_record(
        constraint.candidate_value,
        "INVALID_STATIC_CONSTRAINT_SHAPE",
    )
    _require_string(constraint.context_predicate, "UNKNOWN_PREDICATE")
    _require_bool(
        constraint.required_context_value,
        "INVALID_STATIC_CONSTRAINT_BOOL",
    )


def _validate_cross_constraint(constraint: object) -> None:
    if not isinstance(constraint, CrossConstraint):
        _fail("INVALID_CROSS_CONSTRAINT_RECORD")
    _require_string(constraint.constraint_link, "INVALID_CROSS_CONSTRAINT_SHAPE")
    links = _require_tuple(
        constraint.semantic_slot_links,
        "CROSS_CONSTRAINT_LINK_SHAPE",
    )
    if len(links) != 2:
        _fail("CROSS_CONSTRAINT_LINK_SHAPE")
    for link in links:
        _require_string(link, "CROSS_CONSTRAINT_LINK_SHAPE")
    allowed_tuples = _require_tuple(
        constraint.allowed_tuples,
        "CROSS_CONSTRAINT_ALLOWED_TUPLES_SHAPE",
    )
    for pair in allowed_tuples:
        if type(pair) is not tuple or len(pair) != 2:
            _fail("CROSS_CONSTRAINT_TUPLE_SHAPE")
        for value in pair:
            _validate_typed_value_record(value, "CROSS_CONSTRAINT_VALUE_SHAPE")


def _validate_elaboration_inputs(
    canonical_state: CanonicalSemanticState,
    source_envelope: SourceEnvelope | None,
    visible_world_context: VisibleWorldContext,
    slot_declarations: tuple[SlotDeclaration, ...],
    static_constraints: tuple[StaticConstraint, ...],
    cross_constraints: tuple[CrossConstraint, ...],
) -> None:
    _validate_canonical_state(canonical_state)
    _validate_source_envelope(source_envelope)
    _validate_visible_world_context(visible_world_context)
    slots = _require_tuple(slot_declarations, "INVALID_SLOT_DECLARATION_CONTAINER")
    statics = _require_tuple(static_constraints, "INVALID_STATIC_CONSTRAINT_CONTAINER")
    crosses = _require_tuple(cross_constraints, "INVALID_CROSS_CONSTRAINT_CONTAINER")
    for declaration in slots:
        _validate_slot_declaration(declaration)
    for constraint in statics:
        _validate_static_constraint(constraint)
    for constraint in crosses:
        _validate_cross_constraint(constraint)


def _source_ref_table(source_envelope: SourceEnvelope | None) -> dict[str, str]:
    if source_envelope is None:
        _fail("MISSING_SOURCE_ENVELOPE")
    refs: dict[str, str] = {}
    for span in source_envelope.spans:
        if span.role not in SourceRole.values():
            _fail("INVALID_SOURCE_ROLE")
        if span.ref in refs:
            _fail("DUPLICATE_SOURCE_REF")
        refs[span.ref] = span.role
    return refs


def _source_order(source_envelope: SourceEnvelope) -> dict[str, int]:
    return {span.ref: index for index, span in enumerate(source_envelope.spans)}


def _require_supports(refs: tuple[str, ...], source_roles: dict[str, str]) -> None:
    for ref in refs:
        if ref not in source_roles:
            _fail("DANGLING_SUPPORT_REF")


def _support_sort_key(
    refs: tuple[str, ...],
    source_positions: dict[str, int],
) -> int:
    if not refs:
        _fail("MISSING_PROPOSITION_SUPPORT")
    return min(source_positions[ref] for ref in refs)


def _term_sort_key(term: object) -> str:
    if isinstance(term, ValueTerm):
        _check_value_term_kind(term)
        _check_enum_member(term.value)
        return f"VALUE:{term.value.type}:{term.value.value}"
    if isinstance(term, OpenTerm):
        _check_open_term_kind(term)
        return f"OPEN:{term.type}:{term.semantic_slot_link}"
    _fail("INVALID_TERM")


def _candidate_sort_key(
    candidate: NormativeCandidate,
    source_positions: dict[str, int],
) -> tuple[int, str, str, tuple[str, ...]]:
    if candidate.modality not in Modality.values():
        _fail("UNKNOWN_MODALITY")
    return (
        _support_sort_key(candidate.proposition_support, source_positions),
        candidate.modality,
        candidate.predicate,
        tuple(_term_sort_key(term) for term in candidate.args),
    )


def _knowledge_sort_key(
    assertion: KnowledgeAssertion,
    source_positions: dict[str, int],
) -> tuple[int, str, tuple[str, ...], str, str]:
    return (
        _support_sort_key(assertion.proposition_support, source_positions),
        assertion.predicate,
        tuple(_term_sort_key(term) for term in assertion.args),
        assertion.basis,
        assertion.commitment,
    )


def _ensure_unambiguous_order(keys: tuple[object, ...]) -> None:
    if len(set(keys)) != len(keys):
        _fail("AMBIGUOUS_CANONICAL_ORDER")


def _ordered_candidates(
    canonical_state: CanonicalSemanticState,
    source_roles: dict[str, str],
    source_positions: dict[str, int],
) -> tuple[NormativeCandidate, ...]:
    for candidate in canonical_state.normative_candidates:
        _require_supports(candidate.proposition_support, source_roles)
        _require_supports(candidate.claimed_authority_support, source_roles)
    keyed = tuple(
        (_candidate_sort_key(candidate, source_positions), candidate)
        for candidate in canonical_state.normative_candidates
    )
    _ensure_unambiguous_order(tuple(key for key, _candidate in keyed))
    return tuple(candidate for _key, candidate in sorted(keyed, key=lambda item: item[0]))


def _ordered_knowledge_assertions(
    canonical_state: CanonicalSemanticState,
    source_roles: dict[str, str],
    source_positions: dict[str, int],
) -> tuple[KnowledgeAssertion, ...]:
    for assertion in canonical_state.knowledge_assertions:
        if assertion.basis not in AssertionBasis.values():
            _fail("INVALID_KNOWLEDGE_BASIS")
        if assertion.commitment not in AssertionCommitment.values():
            _fail("INVALID_KNOWLEDGE_COMMITMENT")
        _require_supports(assertion.proposition_support, source_roles)
    keyed = tuple(
        (_knowledge_sort_key(assertion, source_positions), assertion)
        for assertion in canonical_state.knowledge_assertions
    )
    _ensure_unambiguous_order(tuple(key for key, _assertion in keyed))
    return tuple(assertion for _key, assertion in sorted(keyed, key=lambda item: item[0]))


def _check_value_term_kind(term: ValueTerm) -> None:
    if term.kind != "VALUE":
        _fail("INVALID_VALUE_TERM_KIND")


def _check_open_term_kind(term: OpenTerm) -> None:
    if term.kind != "OPEN":
        _fail("INVALID_OPEN_TERM_KIND")


def _check_enum_member(value: TypedValue) -> None:
    order = TYPE_VALUE_ORDER.get(value.type)
    if order is None:
        _fail("UNKNOWN_ENUM_TYPE")
    if value.value not in order:
        _fail("UNKNOWN_ENUM_VALUE")


def _check_typed_value(value: TypedValue, expected_type: str) -> None:
    if value.type != expected_type:
        _fail("TYPE_MISMATCH")
    _check_enum_member(value)


def _check_predicate_terms(
    predicate: str,
    terms: tuple[object, ...],
) -> tuple[str, ...]:
    definition = PREDICATE_BY_ID.get(predicate)
    if definition is None:
        _fail("UNKNOWN_PREDICATE")
    signature = definition.signature
    if len(terms) != len(signature):
        _fail("ARGUMENT_COUNT_MISMATCH")
    for term, expected_type in zip(terms, signature, strict=True):
        if isinstance(term, ValueTerm):
            _check_value_term_kind(term)
            _check_typed_value(term.value, expected_type)
        elif isinstance(term, OpenTerm):
            _check_open_term_kind(term)
            if term.type != expected_type:
                _fail("TYPE_MISMATCH")
        else:
            _fail("INVALID_TERM")
    return signature


def _check_modality_scope(candidate: NormativeCandidate) -> None:
    definition = PREDICATE_BY_ID[candidate.predicate]
    modality = candidate.modality
    scope = definition.scope
    if modality not in Modality.values():
        _fail("UNKNOWN_MODALITY")
    if modality == Modality.GOAL.value and scope != PredicateScope.FINAL.value:
        _fail("MODALITY_SCOPE_MISMATCH")
    if modality == Modality.PRESERVE.value and scope != PredicateScope.TRACE.value:
        _fail("MODALITY_SCOPE_MISMATCH")
    if modality in (Modality.FORBID.value, Modality.ALLOW.value) and scope != PredicateScope.EVENT.value:
        _fail("MODALITY_SCOPE_MISMATCH")


def _authority(candidate: NormativeCandidate, source_roles: dict[str, str]) -> str:
    claimed = candidate.claimed_authority_support
    proposition_refs = set(candidate.proposition_support)
    for ref in claimed:
        if ref not in proposition_refs:
            _fail("CLAIMED_AUTHORITY_NOT_DIRECT")
    if claimed and all(source_roles[ref] == SourceRole.USER.value for ref in claimed):
        return NormativeAuthority.USER.value
    return NormativeAuthority.NONE.value


def _open_slot_mentions(
    canonical_state: CanonicalSemanticState,
) -> dict[tuple[str, int], OpenSlotMention]:
    mentions: dict[tuple[str, int], OpenSlotMention] = {}
    for mention in canonical_state.open_slot_mentions:
        if mention.owner not in OpenOwner.values():
            _fail("INVALID_OPEN_OWNER")
        if mention.type not in TYPE_VALUE_ORDER:
            _fail("UNKNOWN_SLOT_TYPE")
        key = (mention.proposition_link, mention.argument_position)
        if key in mentions:
            _fail("DUPLICATE_OPEN_SLOT_MENTION")
        mentions[key] = mention
    return mentions


def _slot_declarations(
    slot_declarations: tuple[SlotDeclaration, ...],
) -> dict[str, SlotDeclaration]:
    declarations: dict[str, SlotDeclaration] = {}
    for declaration in slot_declarations:
        if declaration.owner not in OpenOwner.values():
            _fail("INVALID_OPEN_OWNER")
        if declaration.type not in TYPE_VALUE_ORDER:
            _fail("UNKNOWN_SLOT_TYPE")
        if declaration.semantic_slot_link in declarations:
            _fail("DUPLICATE_SLOT_DECLARATION")
        declarations[declaration.semantic_slot_link] = declaration
    return declarations


def _check_open_terms(
    candidates: tuple[NormativeCandidate, ...],
    mentions: dict[tuple[str, int], OpenSlotMention],
    declarations: dict[str, SlotDeclaration],
) -> tuple[ElaboratedOpenSlot, ...]:
    referenced_slots: dict[str, ElaboratedOpenSlot] = {}
    expected_mentions: set[tuple[str, int]] = set()
    for candidate_index, candidate in enumerate(candidates):
        clause_link = f"clause:{candidate_index:03d}"
        for argument_position, term in enumerate(candidate.args):
            if not isinstance(term, OpenTerm):
                continue
            expected_link = f"slot:{clause_link}:arg{argument_position}"
            if term.semantic_slot_link != expected_link:
                _fail("SLOT_LINK_MISMATCH")
            mention_key = (clause_link, argument_position)
            expected_mentions.add(mention_key)
            mention = mentions.get(mention_key)
            if mention is None:
                _fail("MISSING_OPEN_SLOT_MENTION")
            if (
                mention.type != term.type
                or mention.owner not in OpenOwner.values()
                or mention.proposition_link != clause_link
                or mention.argument_position != argument_position
                or mention.proposition_support != candidate.proposition_support
            ):
                _fail("OPEN_SLOT_MENTION_MISMATCH")
            declaration = declarations.get(expected_link)
            if declaration is None:
                _fail("MISSING_SLOT_DECLARATION")
            if declaration.type != term.type or declaration.owner != mention.owner:
                _fail("SLOT_DECLARATION_MISMATCH")
            if expected_link in referenced_slots:
                _fail("DUPLICATE_OPEN_SLOT")
            referenced_slots[expected_link] = ElaboratedOpenSlot(
                semantic_slot_link=expected_link,
                type=declaration.type,
                owner=declaration.owner,
                resolved_value=declaration.resolved_value,
            )
    if set(mentions) != expected_mentions:
        _fail("EXTRA_OPEN_SLOT_MENTION")
    if set(declarations) != set(referenced_slots):
        _fail("EXTRA_SLOT_DECLARATION")
    unresolved_count = sum(
        1 for slot in referenced_slots.values() if slot.resolved_value is None
    )
    if unresolved_count > 2:
        _fail("UNRESOLVED_SLOT_BOUND_EXCEEDED")
    return tuple(referenced_slots[link] for link in sorted(referenced_slots))


def _check_domain(declaration: SlotDeclaration) -> tuple[TypedValue, ...]:
    domain = declaration.schema_domain
    if not isinstance(domain, tuple):
        _fail("MALFORMED_DOMAIN_DECLARATION")
    if not domain:
        _fail("DECLARED_EMPTY_DOMAIN")
    order = TYPE_VALUE_ORDER.get(declaration.type)
    if order is None:
        _fail("UNKNOWN_SLOT_TYPE")
    seen: set[TypedValue] = set()
    previous_index = -1
    for value in domain:
        if not isinstance(value, TypedValue):
            _fail("MALFORMED_DOMAIN_DECLARATION")
        _check_typed_value(value, declaration.type)
        if value in seen:
            _fail("MALFORMED_DOMAIN_DECLARATION")
        seen.add(value)
        index = order.index(value.value)
        if index <= previous_index:
            _fail("MALFORMED_DOMAIN_DECLARATION")
        previous_index = index
    if declaration.resolved_value is not None:
        _check_typed_value(declaration.resolved_value, declaration.type)
        if declaration.resolved_value not in domain:
            _fail("RESOLVED_VALUE_OUTSIDE_DOMAIN")
    return domain


def _context_matches(
    visible_world_context: VisibleWorldContext,
    predicate: str,
    value: TypedValue,
) -> tuple[object, ...]:
    return tuple(
        item
        for item in visible_world_context.observable_values
        if item.predicate == predicate and item.args == (value,)
    )


def _apply_static_constraints(
    open_slots: tuple[ElaboratedOpenSlot, ...],
    declarations: dict[str, SlotDeclaration],
    visible_world_context: VisibleWorldContext,
    static_constraints: tuple[StaticConstraint, ...],
) -> tuple[tuple[SlotDomain, ...], tuple[_StaticExclusion, ...]]:
    constraints_by_slot: dict[str, list[StaticConstraint]] = {
        slot.semantic_slot_link: [] for slot in open_slots
    }
    for constraint in static_constraints:
        if constraint.semantic_slot_link not in constraints_by_slot:
            _fail("STATIC_CONSTRAINT_SLOT_MISMATCH")
        constraints_by_slot[constraint.semantic_slot_link].append(constraint)
    domains: list[SlotDomain] = []
    exclusions: list[_StaticExclusion] = []
    for slot in open_slots:
        declaration = declarations[slot.semantic_slot_link]
        schema_domain = _check_domain(declaration)
        admissible = list(schema_domain)
        for constraint in sorted(
            constraints_by_slot[slot.semantic_slot_link],
            key=lambda item: item.constraint_link,
        ):
            _check_typed_value(constraint.candidate_value, slot.type)
            if constraint.candidate_value not in schema_domain:
                _fail("STATIC_CONSTRAINT_VALUE_OUTSIDE_DOMAIN")
            definition = PREDICATE_BY_ID.get(constraint.context_predicate)
            if definition is None:
                _fail("UNKNOWN_PREDICATE")
            if definition.signature != (slot.type,):
                _fail("STATIC_CONSTRAINT_SIGNATURE_MISMATCH")
            if definition.scope != PredicateScope.INITIAL.value:
                _fail("STATIC_CONSTRAINT_PREDICATE_SCOPE_MISMATCH")
            matches = _context_matches(
                visible_world_context,
                constraint.context_predicate,
                constraint.candidate_value,
            )
            if not matches:
                _fail("MISSING_CONTEXT_OBSERVATION")
            if len(matches) != 1:
                _fail("AMBIGUOUS_CONTEXT_OBSERVATION")
            observation = matches[0]
            if observation.scope != ContextAvailability.STATIC.value:
                _fail("STATIC_CONSTRAINT_SCOPE_MISMATCH")
            if observation.value != constraint.required_context_value:
                admissible = [
                    value
                    for value in admissible
                    if value != constraint.candidate_value
                ]
                exclusions.append(
                    _StaticExclusion(
                        semantic_slot_link=slot.semantic_slot_link,
                        value=constraint.candidate_value,
                        constraint_link=constraint.constraint_link,
                    )
                )
        domains.append(
            SlotDomain(
                semantic_slot_link=slot.semantic_slot_link,
                values=tuple(admissible),
            )
        )
    return tuple(domains), tuple(exclusions)


def _schema_domains(
    open_slots: tuple[ElaboratedOpenSlot, ...],
    declarations: dict[str, SlotDeclaration],
) -> tuple[SlotDomain, ...]:
    return tuple(
        SlotDomain(
            semantic_slot_link=slot.semantic_slot_link,
            values=_check_domain(declarations[slot.semantic_slot_link]),
        )
        for slot in open_slots
    )


def _check_constraint_links(
    static_constraints: tuple[StaticConstraint, ...],
    cross_constraints: tuple[CrossConstraint, ...],
) -> tuple[str, ...]:
    links = tuple(item.constraint_link for item in static_constraints) + tuple(
        item.constraint_link for item in cross_constraints
    )
    if len(set(links)) != len(links):
        _fail("DUPLICATE_CONSTRAINT_LINK")
    return tuple(sorted(links))


def _check_cross_constraints(
    open_slots: tuple[ElaboratedOpenSlot, ...],
    declarations: dict[str, SlotDeclaration],
    cross_constraints: tuple[CrossConstraint, ...],
) -> tuple[CrossConstraint, ...]:
    slot_order = {slot.semantic_slot_link: index for index, slot in enumerate(open_slots)}
    schema_domains = {
        link: _check_domain(declaration)
        for link, declaration in declarations.items()
    }
    checked: list[CrossConstraint] = []
    for constraint in sorted(cross_constraints, key=lambda item: item.constraint_link):
        links = constraint.semantic_slot_links
        if len(links) != 2 or links[0] == links[1]:
            _fail("CROSS_CONSTRAINT_SLOT_LINKS")
        if links[0] not in slot_order or links[1] not in slot_order:
            _fail("CROSS_CONSTRAINT_SLOT_LINKS")
        if links != tuple(sorted(links, key=lambda item: slot_order[item])):
            _fail("CROSS_CONSTRAINT_LINK_ORDER")
        left = declarations[links[0]]
        right = declarations[links[1]]
        seen: set[tuple[TypedValue, TypedValue]] = set()
        for pair in constraint.allowed_tuples:
            if len(pair) != 2:
                _fail("CROSS_CONSTRAINT_TUPLE_ARITY")
            left_value, right_value = pair
            _check_typed_value(left_value, left.type)
            _check_typed_value(right_value, right.type)
            if left_value not in schema_domains[links[0]] or right_value not in schema_domains[links[1]]:
                _fail("CROSS_CONSTRAINT_VALUE_OUTSIDE_DOMAIN")
            if pair in seen:
                _fail("DUPLICATE_CROSS_CONSTRAINT_TUPLE")
            seen.add(pair)
        checked.append(constraint)
    return tuple(checked)


def elaborate(
    canonical_state: CanonicalSemanticState,
    source_envelope: SourceEnvelope | None,
    visible_world_context: VisibleWorldContext,
    slot_declarations: tuple[SlotDeclaration, ...],
    static_constraints: tuple[StaticConstraint, ...],
    cross_constraints: tuple[CrossConstraint, ...],
) -> ElaboratedSemanticState:
    _validate_elaboration_inputs(
        canonical_state,
        source_envelope,
        visible_world_context,
        slot_declarations,
        static_constraints,
        cross_constraints,
    )
    source_roles = _source_ref_table(source_envelope)
    source_positions = _source_order(source_envelope)
    candidates = _ordered_candidates(canonical_state, source_roles, source_positions)
    knowledge_assertions = _ordered_knowledge_assertions(
        canonical_state,
        source_roles,
        source_positions,
    )
    mentions = _open_slot_mentions(canonical_state)
    declarations = _slot_declarations(slot_declarations)
    elaborated_candidates: list[ElaboratedCandidate] = []
    for candidate_index, candidate in enumerate(candidates):
        _check_predicate_terms(candidate.predicate, candidate.args)
        _check_modality_scope(candidate)
        authority = _authority(candidate, source_roles)
        elaborated_candidates.append(
            ElaboratedCandidate(
                original=candidate,
                clause_link=f"clause:{candidate_index:03d}",
                authority=authority,
                active=authority == NormativeAuthority.USER.value,
            )
        )
    for assertion in knowledge_assertions:
        _check_predicate_terms(assertion.predicate, assertion.args)
    open_slots = _check_open_terms(candidates, mentions, declarations)
    constraint_links = _check_constraint_links(static_constraints, cross_constraints)
    checked_static_constraints = tuple(
        sorted(static_constraints, key=lambda item: item.constraint_link)
    )
    slot_domains, static_exclusions = _apply_static_constraints(
        open_slots,
        declarations,
        visible_world_context,
        checked_static_constraints,
    )
    checked_cross_constraints = _check_cross_constraints(
        open_slots,
        declarations,
        cross_constraints,
    )
    return ElaboratedSemanticState(
        candidates=tuple(elaborated_candidates),
        active_clause_links=tuple(
            candidate.clause_link
            for candidate in elaborated_candidates
            if candidate.active
        ),
        knowledge_assertions=knowledge_assertions,
        open_slots=open_slots,
        slot_domains=slot_domains,
        static_constraints=checked_static_constraints,
        cross_constraints=checked_cross_constraints,
        constraint_links=constraint_links,
        _schema_domains=_schema_domains(open_slots, declarations),
        _static_exclusions=static_exclusions,
    )
