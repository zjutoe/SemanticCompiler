"""Strict fixture-direct typed adapters for the Phase 0 A/B paths."""

from __future__ import annotations

from dataclasses import dataclass

from Phase0.implementation.schema import (
    AssertionBasis,
    AssertionCommitment,
    CanonicalSemanticState,
    KnowledgeAssertion,
    Modality,
    NormativeCandidate,
    OpenOwner,
    OpenSlotMention,
    OpenTerm,
    TYPE_VALUE_ORDER,
    TypedValue,
    ValueTerm,
)


class AdapterFailure(ValueError):
    """Loud adapter-boundary failure with a stable public reason."""

    def __init__(self, reason: str) -> None:
        self.stage = "adapter_or_bridge"
        self.reason = reason
        super().__init__(f"{self.stage}/{self.reason}")


@dataclass(frozen=True)
class ContractValueArgument:
    value: TypedValue


@dataclass(frozen=True)
class ContractOpenArgument:
    semantic_slot_link: str
    type: str
    owner: str
    proposition_support: tuple[str, ...]


@dataclass(frozen=True)
class ContractClause:
    clause_link: str
    modality: str
    predicate: str
    arguments: tuple[ContractValueArgument | ContractOpenArgument, ...]
    proposition_support: tuple[str, ...]
    claimed_authority_support: tuple[str, ...]


@dataclass(frozen=True)
class ContractKnowledgeAssertion:
    knowledge_link: str
    predicate: str
    arguments: tuple[ContractValueArgument, ...]
    basis: str
    commitment: str
    proposition_support: tuple[str, ...]


@dataclass(frozen=True)
class ContractSurfaceState:
    clauses: tuple[ContractClause, ...]
    knowledge_assertions: tuple[ContractKnowledgeAssertion, ...]


@dataclass(frozen=True)
class IsomorphicTerm:
    kind: str
    value_type: str
    value: str | None


@dataclass(frozen=True)
class IsomorphicProposition:
    proposition_index: int
    force: str
    relation: str
    terms: tuple[IsomorphicTerm, ...]
    evidence: tuple[str, ...]
    authority_evidence: tuple[str, ...]


@dataclass(frozen=True)
class IsomorphicFact:
    fact_index: int
    relation: str
    terms: tuple[IsomorphicTerm, ...]
    basis: str
    commitment: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class IsomorphicOpenBinding:
    proposition_index: int
    argument_index: int
    owner: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class SemanticIsomorphicSurfaceState:
    propositions: tuple[IsomorphicProposition, ...]
    facts: tuple[IsomorphicFact, ...]
    open_bindings: tuple[IsomorphicOpenBinding, ...]


def _fail(reason: str) -> None:
    raise AdapterFailure(reason)


def _require_string(value: object, reason: str) -> str:
    if type(value) is not str:
        _fail(reason)
    return value


def _require_index(value: object, reason: str) -> int:
    if type(value) is not int or value < 0:
        _fail(reason)
    return value


def _validate_support(value: object, reason: str) -> tuple[str, ...]:
    if type(value) is not tuple:
        _fail(reason)
    for ref in value:
        _require_string(ref, reason)
    if len(set(value)) != len(value):
        _fail(reason)
    return value


def _validate_enum_type(value: object, reason: str) -> str:
    type_id = _require_string(value, reason)
    if type_id not in TYPE_VALUE_ORDER:
        _fail(reason)
    return type_id


def _validate_typed_value(value: object, reason: str) -> TypedValue:
    if type(value) is not TypedValue:
        _fail(reason)
    type_id = _validate_enum_type(value.type, reason)
    member_id = _require_string(value.value, reason)
    if member_id not in TYPE_VALUE_ORDER[type_id]:
        _fail(reason)
    return value


def _validate_member(value: object, members: tuple[str, ...], reason: str) -> str:
    member = _require_string(value, reason)
    if member not in members:
        _fail(reason)
    return member


def _fresh_value_term(value: TypedValue) -> ValueTerm:
    return ValueTerm(
        kind="VALUE",
        value=TypedValue(type=value.type, value=value.value),
    )


def _fresh_strings(value: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(item for item in value)


def _validate_contract_surface(
    surface: ContractSurfaceState,
) -> tuple[tuple[ContractClause, ...], tuple[ContractKnowledgeAssertion, ...]]:
    reason = "INVALID_CONTRACT_SURFACE"
    if type(surface.clauses) is not tuple or type(surface.knowledge_assertions) is not tuple:
        _fail(reason)

    for clause in surface.clauses:
        if type(clause) is not ContractClause:
            _fail(reason)
        _require_string(clause.clause_link, reason)
        _validate_member(clause.modality, Modality.values(), reason)
        _require_string(clause.predicate, reason)
        if type(clause.arguments) is not tuple:
            _fail(reason)
        _validate_support(clause.proposition_support, reason)
        _validate_support(clause.claimed_authority_support, reason)
        for argument in clause.arguments:
            if type(argument) is ContractValueArgument:
                _validate_typed_value(argument.value, reason)
            elif type(argument) is ContractOpenArgument:
                _require_string(argument.semantic_slot_link, reason)
                _validate_enum_type(argument.type, reason)
                _validate_member(argument.owner, OpenOwner.values(), reason)
                _validate_support(argument.proposition_support, reason)
            else:
                _fail(reason)

    clauses = tuple(sorted(surface.clauses, key=lambda clause: clause.clause_link))
    if tuple(clause.clause_link for clause in clauses) != tuple(
        f"clause:{index:03d}" for index in range(len(clauses))
    ):
        _fail(reason)
    for clause in clauses:
        for argument_index, argument in enumerate(clause.arguments):
            if type(argument) is ContractOpenArgument and argument.semantic_slot_link != (
                f"slot:{clause.clause_link}:arg{argument_index}"
            ):
                _fail(reason)

    for assertion in surface.knowledge_assertions:
        if type(assertion) is not ContractKnowledgeAssertion:
            _fail(reason)
        _require_string(assertion.knowledge_link, reason)
        _require_string(assertion.predicate, reason)
        if type(assertion.arguments) is not tuple:
            _fail(reason)
        for argument in assertion.arguments:
            if type(argument) is not ContractValueArgument:
                _fail(reason)
            _validate_typed_value(argument.value, reason)
        _validate_member(assertion.basis, AssertionBasis.values(), reason)
        _validate_member(
            assertion.commitment,
            AssertionCommitment.values(),
            reason,
        )
        _validate_support(assertion.proposition_support, reason)

    assertions = tuple(
        sorted(
            surface.knowledge_assertions,
            key=lambda assertion: assertion.knowledge_link,
        )
    )
    if tuple(assertion.knowledge_link for assertion in assertions) != tuple(
        f"knowledge:{index:03d}" for index in range(len(assertions))
    ):
        _fail(reason)
    return clauses, assertions


def alpha_A(surface: ContractSurfaceState) -> CanonicalSemanticState:
    """Validate and adapt a clause-centric Contract surface."""

    if type(surface) is not ContractSurfaceState:
        _fail("INVALID_CONTRACT_SURFACE")
    clauses, assertions = _validate_contract_surface(surface)

    candidates: list[NormativeCandidate] = []
    mentions: list[OpenSlotMention] = []
    for clause in clauses:
        terms = []
        for argument_index, argument in enumerate(clause.arguments):
            if type(argument) is ContractValueArgument:
                terms.append(_fresh_value_term(argument.value))
            else:
                terms.append(
                    OpenTerm(
                        kind="OPEN",
                        type=argument.type,
                        semantic_slot_link=argument.semantic_slot_link,
                    )
                )
                mentions.append(
                    OpenSlotMention(
                        type=argument.type,
                        owner=argument.owner,
                        proposition_link=clause.clause_link,
                        argument_position=argument_index,
                        proposition_support=_fresh_strings(
                            argument.proposition_support
                        ),
                    )
                )
        candidates.append(
            NormativeCandidate(
                modality=clause.modality,
                predicate=clause.predicate,
                args=tuple(terms),
                proposition_support=_fresh_strings(clause.proposition_support),
                claimed_authority_support=_fresh_strings(
                    clause.claimed_authority_support
                ),
            )
        )

    knowledge = tuple(
        KnowledgeAssertion(
            predicate=assertion.predicate,
            args=tuple(
                _fresh_value_term(argument.value)
                for argument in assertion.arguments
            ),
            basis=assertion.basis,
            commitment=assertion.commitment,
            proposition_support=_fresh_strings(assertion.proposition_support),
        )
        for assertion in assertions
    )
    return CanonicalSemanticState(
        normative_candidates=tuple(candidates),
        knowledge_assertions=knowledge,
        open_slot_mentions=tuple(mentions),
    )


def _validate_isomorphic_term(term: object, reason: str) -> IsomorphicTerm:
    if type(term) is not IsomorphicTerm:
        _fail(reason)
    _validate_enum_type(term.value_type, reason)
    kind = _require_string(term.kind, reason)
    if kind == "VALUE":
        member = _require_string(term.value, reason)
        if member not in TYPE_VALUE_ORDER[term.value_type]:
            _fail(reason)
    elif kind == "OPEN":
        if term.value is not None:
            _fail(reason)
    else:
        _fail(reason)
    return term


def _validate_isomorphic_surface(
    surface: SemanticIsomorphicSurfaceState,
) -> tuple[
    tuple[IsomorphicProposition, ...],
    tuple[IsomorphicFact, ...],
    tuple[IsomorphicOpenBinding, ...],
]:
    reason = "INVALID_ISOMORPHIC_SURFACE"
    if (
        type(surface.propositions) is not tuple
        or type(surface.facts) is not tuple
        or type(surface.open_bindings) is not tuple
    ):
        _fail(reason)

    for proposition in surface.propositions:
        if type(proposition) is not IsomorphicProposition:
            _fail(reason)
        _require_index(proposition.proposition_index, reason)
        _validate_member(proposition.force, Modality.values(), reason)
        _require_string(proposition.relation, reason)
        if type(proposition.terms) is not tuple:
            _fail(reason)
        for term in proposition.terms:
            _validate_isomorphic_term(term, reason)
        _validate_support(proposition.evidence, reason)
        _validate_support(proposition.authority_evidence, reason)

    propositions = tuple(
        sorted(
            surface.propositions,
            key=lambda proposition: proposition.proposition_index,
        )
    )
    if tuple(item.proposition_index for item in propositions) != tuple(
        range(len(propositions))
    ):
        _fail(reason)

    for fact in surface.facts:
        if type(fact) is not IsomorphicFact:
            _fail(reason)
        _require_index(fact.fact_index, reason)
        _require_string(fact.relation, reason)
        if type(fact.terms) is not tuple:
            _fail(reason)
        for term in fact.terms:
            if _validate_isomorphic_term(term, reason).kind != "VALUE":
                _fail(reason)
        _validate_member(fact.basis, AssertionBasis.values(), reason)
        _validate_member(fact.commitment, AssertionCommitment.values(), reason)
        _validate_support(fact.evidence, reason)

    facts = tuple(sorted(surface.facts, key=lambda fact: fact.fact_index))
    if tuple(item.fact_index for item in facts) != tuple(range(len(facts))):
        _fail(reason)

    for binding in surface.open_bindings:
        if type(binding) is not IsomorphicOpenBinding:
            _fail(reason)
        _require_index(binding.proposition_index, reason)
        _require_index(binding.argument_index, reason)
        _validate_member(binding.owner, OpenOwner.values(), reason)
        _validate_support(binding.evidence, reason)

    binding_keys = tuple(
        (binding.proposition_index, binding.argument_index)
        for binding in surface.open_bindings
    )
    if binding_keys != tuple(sorted(binding_keys)):
        _fail(reason)
    required_keys = tuple(
        (proposition.proposition_index, argument_index)
        for proposition in propositions
        for argument_index, term in enumerate(proposition.terms)
        if term.kind == "OPEN"
    )
    if binding_keys != required_keys:
        _fail(reason)
    return propositions, facts, surface.open_bindings


def alpha_B(surface: SemanticIsomorphicSurfaceState) -> CanonicalSemanticState:
    """Validate and adapt a position-indexed semantic-isomorphic surface."""

    if type(surface) is not SemanticIsomorphicSurfaceState:
        _fail("INVALID_ISOMORPHIC_SURFACE")
    propositions, facts, bindings = _validate_isomorphic_surface(surface)

    candidates: list[NormativeCandidate] = []
    mentions: list[OpenSlotMention] = []
    binding_index = 0
    for proposition in propositions:
        clause_link = f"clause:{proposition.proposition_index:03d}"
        terms = []
        for argument_index, term in enumerate(proposition.terms):
            if term.kind == "VALUE":
                terms.append(
                    _fresh_value_term(
                        TypedValue(type=term.value_type, value=term.value)
                    )
                )
            else:
                semantic_slot_link = f"slot:{clause_link}:arg{argument_index}"
                terms.append(
                    OpenTerm(
                        kind="OPEN",
                        type=term.value_type,
                        semantic_slot_link=semantic_slot_link,
                    )
                )
                binding = bindings[binding_index]
                binding_index += 1
                mentions.append(
                    OpenSlotMention(
                        type=term.value_type,
                        owner=binding.owner,
                        proposition_link=clause_link,
                        argument_position=argument_index,
                        proposition_support=_fresh_strings(binding.evidence),
                    )
                )
        candidates.append(
            NormativeCandidate(
                modality=proposition.force,
                predicate=proposition.relation,
                args=tuple(terms),
                proposition_support=_fresh_strings(proposition.evidence),
                claimed_authority_support=_fresh_strings(
                    proposition.authority_evidence
                ),
            )
        )

    knowledge = tuple(
        KnowledgeAssertion(
            predicate=fact.relation,
            args=tuple(
                _fresh_value_term(
                    TypedValue(type=term.value_type, value=term.value)
                )
                for term in fact.terms
            ),
            basis=fact.basis,
            commitment=fact.commitment,
            proposition_support=_fresh_strings(fact.evidence),
        )
        for fact in facts
    )
    return CanonicalSemanticState(
        normative_candidates=tuple(candidates),
        knowledge_assertions=knowledge,
        open_slot_mentions=tuple(mentions),
    )


def adapt_typed_surface(
    adapter_link: str | None,
    surface: object,
) -> CanonicalSemanticState:
    """Dispatch a typed surface while enforcing the accepted F8 precedence."""

    if adapter_link is None:
        _fail("MISSING_ADAPTER_LINK")
    if type(adapter_link) is not str:
        _fail("INVALID_ADAPTER_LINK")
    if adapter_link not in ("alpha_A", "alpha_B"):
        _fail("UNKNOWN_ADAPTER_LINK")
    if adapter_link == "alpha_A":
        if type(surface) is not ContractSurfaceState:
            _fail("ADAPTER_SURFACE_TYPE_MISMATCH")
        return alpha_A(surface)
    if type(surface) is not SemanticIsomorphicSurfaceState:
        _fail("ADAPTER_SURFACE_TYPE_MISMATCH")
    return alpha_B(surface)
