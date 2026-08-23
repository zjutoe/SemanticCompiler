"""Finite reference runtime for elaborated Phase 0 E1 semantics."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations, product

from Phase0.implementation.dialect import (
    AssignmentItem,
    MANAGED_EFFECTS,
    TRAJECTORIES_BY_ID,
    Trajectory,
    evaluate_predicate,
)
from Phase0.implementation.elaboration import ElaboratedCandidate, ElaboratedSemanticState
from Phase0.implementation.schema import (
    Modality,
    OpenOwner,
    TYPE_VALUE_ORDER,
    TypedValue,
    ValueTerm,
    OpenTerm,
)


Assignment = tuple[AssignmentItem, ...]
ResolutionTrace = AssignmentItem


class RuntimeFailure(ValueError):
    """Loud runtime-stage failure with a stable public reason."""

    def __init__(self, reason: str) -> None:
        self.stage = "runtime"
        self.reason = reason
        super().__init__(f"{self.stage}/{self.reason}")


@dataclass(frozen=True)
class AskDecision:
    kind: str = field(default="ASK", init=False)
    semantic_slot_links: tuple[str, ...]


@dataclass(frozen=True)
class ExecuteDecision:
    kind: str = field(default="EXECUTE", init=False)
    action_id: str
    executor_resolutions: tuple[ResolutionTrace, ...]


@dataclass(frozen=True)
class ClauseConflictWitness:
    kind: str = field(default="ClauseConflictWitness", init=False)
    clause_links: tuple[str, ...]


@dataclass(frozen=True)
class EmptyDomainWitness:
    kind: str = field(default="EmptyDomainWitness", init=False)
    semantic_slot_link: str
    excluding_constraint_links: tuple[str, ...]


@dataclass(frozen=True)
class CrossConstraintWitness:
    kind: str = field(default="CrossConstraintWitness", init=False)
    cross_constraint_links: tuple[str, ...]


@dataclass(frozen=True)
class ExcludedAction:
    action_id: str
    unauthorized_managed_effects: tuple[str, ...]


@dataclass(frozen=True)
class NoAuthorizedActionWitness:
    kind: str = field(default="NoAuthorizedActionWitness", init=False)
    excluded_actions: tuple[ExcludedAction, ...]


@dataclass(frozen=True)
class RejectDecision:
    kind: str = field(default="REJECT", init=False)
    reason: str
    witness: ClauseConflictWitness | EmptyDomainWitness | CrossConstraintWitness | NoAuthorizedActionWitness
    executor_resolutions: tuple[ResolutionTrace, ...]


Decision = AskDecision | ExecuteDecision | RejectDecision


@dataclass(frozen=True)
class RuntimeEvaluation:
    legal_joint_completions: tuple[Assignment, ...]
    decision: Decision
    _supporting_trajectories: tuple[Trajectory, ...] = ()


@dataclass(frozen=True)
class _Pair:
    completion: Assignment
    trajectory: Trajectory


@dataclass(frozen=True)
class _SafeChoice:
    action_id: str
    executor_assignment: tuple[TypedValue, ...]
    trajectories: tuple[Trajectory, ...]


def _runtime_fail(reason: str) -> None:
    raise RuntimeFailure(reason)


def _assignment_map(assignment: Assignment) -> dict[str, TypedValue]:
    return {item.semantic_slot_link: item.value for item in assignment}


def _domain_by_link(elaborated: ElaboratedSemanticState) -> dict[str, tuple[TypedValue, ...]]:
    return {domain.semantic_slot_link: domain.values for domain in elaborated.slot_domains}


def _schema_domain_by_link(elaborated: ElaboratedSemanticState) -> dict[str, tuple[TypedValue, ...]]:
    return {domain.semantic_slot_link: domain.values for domain in elaborated._schema_domains}


def _effective_values(
    slot_link: str,
    resolved_value: TypedValue | None,
    domain_values: tuple[TypedValue, ...],
) -> tuple[TypedValue, ...]:
    if resolved_value is None:
        return domain_values
    if resolved_value in domain_values:
        return (resolved_value,)
    return ()


def _satisfies_cross_constraints(
    assignment: Assignment,
    cross_constraints: tuple[object, ...],
) -> bool:
    values = _assignment_map(assignment)
    for constraint in cross_constraints:
        left, right = constraint.semantic_slot_links
        pair = (values[left], values[right])
        if pair not in constraint.allowed_tuples:
            return False
    return True


def enumerate_joint_completions(
    elaborated: ElaboratedSemanticState,
) -> tuple[Assignment, ...]:
    if not elaborated.open_slots:
        return ((),)
    domains = _domain_by_link(elaborated)
    value_lists: list[tuple[TypedValue, ...]] = []
    for slot in elaborated.open_slots:
        if slot.semantic_slot_link not in domains:
            _runtime_fail("ELABORATED_SLOT_DOMAIN_MISMATCH")
        value_lists.append(
            _effective_values(
                slot.semantic_slot_link,
                slot.resolved_value,
                domains[slot.semantic_slot_link],
            )
        )
    completions: list[Assignment] = []
    for values in product(*value_lists):
        assignment = tuple(
            AssignmentItem(slot.semantic_slot_link, value)
            for slot, value in zip(elaborated.open_slots, values, strict=True)
        )
        if _satisfies_cross_constraints(assignment, elaborated.cross_constraints):
            completions.append(assignment)
    return tuple(completions)


def _first_empty_domain_witness(
    elaborated: ElaboratedSemanticState,
) -> EmptyDomainWitness | None:
    domains = _domain_by_link(elaborated)
    schema_domains = _schema_domain_by_link(elaborated)
    for slot in elaborated.open_slots:
        values = _effective_values(
            slot.semantic_slot_link,
            slot.resolved_value,
            domains[slot.semantic_slot_link],
        )
        if values:
            continue
        required_values = (
            (slot.resolved_value,)
            if slot.resolved_value is not None
            else schema_domains[slot.semantic_slot_link]
        )
        selected_links: list[str] = []
        for required_value in required_values:
            matching_links = tuple(
                exclusion.constraint_link
                for exclusion in elaborated._static_exclusions
                if exclusion.semantic_slot_link == slot.semantic_slot_link
                and exclusion.value == required_value
            )
            if not matching_links:
                _runtime_fail("EMPTY_DOMAIN_WITNESS_NOT_FOUND")
            selected_links.append(min(matching_links))
        return EmptyDomainWitness(
            semantic_slot_link=slot.semantic_slot_link,
            excluding_constraint_links=tuple(sorted(selected_links)),
        )
    return None


def _base_completions_without_cross(
    elaborated: ElaboratedSemanticState,
) -> tuple[Assignment, ...]:
    if not elaborated.open_slots:
        return ((),)
    domains = _domain_by_link(elaborated)
    value_lists = tuple(
        _effective_values(
            slot.semantic_slot_link,
            slot.resolved_value,
            domains[slot.semantic_slot_link],
        )
        for slot in elaborated.open_slots
    )
    return tuple(
        tuple(
            AssignmentItem(slot.semantic_slot_link, value)
            for slot, value in zip(elaborated.open_slots, values, strict=True)
        )
        for values in product(*value_lists)
    )


def _cross_empty_witness(
    elaborated: ElaboratedSemanticState,
) -> CrossConstraintWitness:
    constraints = tuple(
        sorted(elaborated.cross_constraints, key=lambda item: item.constraint_link)
    )
    base_completions = _base_completions_without_cross(elaborated)
    for size in range(1, len(constraints) + 1):
        for subset in combinations(constraints, size):
            if not any(
                _satisfies_cross_constraints(completion, subset)
                for completion in base_completions
            ):
                return CrossConstraintWitness(
                    cross_constraint_links=tuple(
                        constraint.constraint_link for constraint in subset
                    )
                )
    _runtime_fail("CROSS_CONSTRAINT_WITNESS_NOT_FOUND")


def _candidate_trajectories(
    candidate_trajectory_ids: tuple[str, ...],
) -> tuple[Trajectory, ...]:
    if len(set(candidate_trajectory_ids)) != len(candidate_trajectory_ids):
        _runtime_fail("DUPLICATE_TRAJECTORY_ID")
    trajectories: list[Trajectory] = []
    for trajectory_id in candidate_trajectory_ids:
        trajectory = TRAJECTORIES_BY_ID.get(trajectory_id)
        if trajectory is None:
            _runtime_fail("UNKNOWN_TRAJECTORY_ID")
        trajectories.append(trajectory)
    return tuple(trajectories)


def _validate_trajectory_structure(
    elaborated: ElaboratedSemanticState,
    trajectories: tuple[Trajectory, ...],
) -> None:
    expected_links = tuple(slot.semantic_slot_link for slot in elaborated.open_slots)
    slot_by_link = {slot.semantic_slot_link: slot for slot in elaborated.open_slots}
    schema_domains = _schema_domain_by_link(elaborated)
    for trajectory in trajectories:
        actual_links = tuple(item.semantic_slot_link for item in trajectory.assignment)
        if actual_links != expected_links:
            _runtime_fail("STRUCTURALLY_INCOMPATIBLE_TRAJECTORY")
        for item in trajectory.assignment:
            slot = slot_by_link[item.semantic_slot_link]
            if item.value.type != slot.type:
                _runtime_fail("STRUCTURALLY_INCOMPATIBLE_TRAJECTORY")
            if item.value not in schema_domains[item.semantic_slot_link]:
                _runtime_fail("STRUCTURALLY_INCOMPATIBLE_TRAJECTORY")


def _matching_pairs(
    legal_joint_completions: tuple[Assignment, ...],
    trajectories: tuple[Trajectory, ...],
) -> tuple[_Pair, ...]:
    pairs: list[_Pair] = []
    for completion in legal_joint_completions:
        for trajectory in trajectories:
            if trajectory.assignment == completion:
                pairs.append(_Pair(completion=completion, trajectory=trajectory))
    return tuple(pairs)


def _substituted_args(candidate: ElaboratedCandidate, assignment: Assignment) -> tuple[TypedValue, ...]:
    values = _assignment_map(assignment)
    args: list[TypedValue] = []
    for term in candidate.original.args:
        if isinstance(term, ValueTerm):
            args.append(term.value)
        elif isinstance(term, OpenTerm):
            try:
                args.append(values[term.semantic_slot_link])
            except KeyError:
                _runtime_fail("MISSING_ASSIGNMENT_VALUE")
        else:
            _runtime_fail("INVALID_TERM")
    return tuple(args)


def _predicate_value(candidate: ElaboratedCandidate, pair: _Pair) -> bool:
    return evaluate_predicate(
        candidate.original.predicate,
        _substituted_args(candidate, pair.completion),
        pair.trajectory.initial_observables,
        pair.trajectory.final_observables,
        pair.trajectory.ordered_effects,
    )


def _hard_candidates(elaborated: ElaboratedSemanticState) -> tuple[ElaboratedCandidate, ...]:
    hard_modalities = (
        Modality.GOAL.value,
        Modality.REQUIRE.value,
        Modality.PRESERVE.value,
        Modality.FORBID.value,
    )
    return tuple(
        candidate
        for candidate in elaborated.candidates
        if candidate.active and candidate.original.modality in hard_modalities
    )


def _candidate_satisfied(candidate: ElaboratedCandidate, pair: _Pair) -> bool:
    modality = candidate.original.modality
    value = _predicate_value(candidate, pair)
    if modality in (
        Modality.GOAL.value,
        Modality.REQUIRE.value,
        Modality.PRESERVE.value,
    ):
        return value
    if modality == Modality.FORBID.value:
        return not value
    _runtime_fail("INVALID_HARD_MODALITY")


def _hard_valid_pairs(
    elaborated: ElaboratedSemanticState,
    pairs: tuple[_Pair, ...],
) -> tuple[_Pair, ...]:
    hard = _hard_candidates(elaborated)
    return tuple(
        pair
        for pair in pairs
        if all(_candidate_satisfied(candidate, pair) for candidate in hard)
    )


def _active_allows(elaborated: ElaboratedSemanticState) -> tuple[ElaboratedCandidate, ...]:
    return tuple(
        candidate
        for candidate in elaborated.candidates
        if candidate.active and candidate.original.modality == Modality.ALLOW.value
    )


def _effect_authorized(
    effect: str,
    pair: _Pair,
    allows: tuple[ElaboratedCandidate, ...],
) -> bool:
    expected_predicate = f"effect.{effect}"
    return any(
        candidate.original.predicate == expected_predicate
        and _predicate_value(candidate, pair)
        for candidate in allows
    )


def _authorization(
    elaborated: ElaboratedSemanticState,
    hard_valid_pairs: tuple[_Pair, ...],
) -> tuple[tuple[_Pair, ...], dict[str, tuple[str, ...]]]:
    allows = _active_allows(elaborated)
    authorized: list[_Pair] = []
    excluded_by_action: dict[str, set[str]] = {}
    managed_effects = set(MANAGED_EFFECTS)
    for pair in hard_valid_pairs:
        unmatched = tuple(
            sorted(
                effect
                for effect in pair.trajectory.ordered_effects
                if effect in managed_effects and not _effect_authorized(effect, pair, allows)
            )
        )
        if unmatched:
            excluded_by_action.setdefault(pair.trajectory.action_id, set()).update(
                unmatched
            )
        else:
            authorized.append(pair)
    return tuple(authorized), {
        action_id: tuple(sorted(effects))
        for action_id, effects in excluded_by_action.items()
    }


def _value_order_key(value: TypedValue) -> int:
    try:
        return TYPE_VALUE_ORDER[value.type].index(value.value)
    except (KeyError, ValueError):
        _runtime_fail("UNKNOWN_ENUM_VALUE")


def _projection(assignment: Assignment, links: tuple[str, ...]) -> tuple[TypedValue, ...]:
    values = _assignment_map(assignment)
    return tuple(values[link] for link in links)


def _distinct_ordered(items: tuple[tuple[TypedValue, ...], ...]) -> tuple[tuple[TypedValue, ...], ...]:
    seen: set[tuple[TypedValue, ...]] = set()
    result: list[tuple[TypedValue, ...]] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return tuple(result)


def _unresolved_user_links(elaborated: ElaboratedSemanticState) -> tuple[str, ...]:
    return tuple(
        slot.semantic_slot_link
        for slot in elaborated.open_slots
        if slot.owner == OpenOwner.USER.value and slot.resolved_value is None
    )


def _executor_links(elaborated: ElaboratedSemanticState) -> tuple[str, ...]:
    return tuple(
        slot.semantic_slot_link
        for slot in elaborated.open_slots
        if slot.owner == OpenOwner.EXECUTOR.value
    )


def _safe_choices(
    elaborated: ElaboratedSemanticState,
    legal_joint_completions: tuple[Assignment, ...],
    authorized_pairs: tuple[_Pair, ...],
) -> tuple[_SafeChoice, ...]:
    if not legal_joint_completions:
        return ()
    user_links = _unresolved_user_links(elaborated)
    executor_links = _executor_links(elaborated)
    user_projection = _distinct_ordered(
        tuple(_projection(completion, user_links) for completion in legal_joint_completions)
    )
    executor_projection = _distinct_ordered(
        tuple(_projection(completion, executor_links) for completion in legal_joint_completions)
    )
    choices: list[_SafeChoice] = []
    for executor_assignment in executor_projection:
        fiber_user_projection = _distinct_ordered(
            tuple(
                _projection(completion, user_links)
                for completion in legal_joint_completions
                if _projection(completion, executor_links) == executor_assignment
            )
        )
        if not user_projection or fiber_user_projection != user_projection:
            continue
        action_ids = tuple(
            sorted(
                {
                    pair.trajectory.action_id
                    for pair in authorized_pairs
                    if _projection(pair.completion, executor_links) == executor_assignment
                }
            )
        )
        for action_id in action_ids:
            covered = True
            supporting: list[Trajectory] = []
            for user_assignment in user_projection:
                user_support = tuple(
                    pair
                    for pair in authorized_pairs
                    if pair.trajectory.action_id == action_id
                    and _projection(pair.completion, executor_links) == executor_assignment
                    and _projection(pair.completion, user_links) == user_assignment
                )
                if not user_support:
                    covered = False
                    break
                supporting.extend(pair.trajectory for pair in user_support)
            if covered:
                choices.append(
                    _SafeChoice(
                        action_id=action_id,
                        executor_assignment=executor_assignment,
                        trajectories=tuple(supporting),
                    )
                )
    return tuple(
        sorted(
            choices,
            key=lambda choice: (
                choice.action_id,
                tuple(_value_order_key(value) for value in choice.executor_assignment),
            ),
        )
    )


def _executor_resolutions(
    elaborated: ElaboratedSemanticState,
    executor_assignment: tuple[TypedValue, ...],
) -> tuple[ResolutionTrace, ...]:
    return tuple(
        AssignmentItem(link, value)
        for link, value in zip(_executor_links(elaborated), executor_assignment, strict=True)
    )


def _clause_conflict_witness(
    elaborated: ElaboratedSemanticState,
    pairs: tuple[_Pair, ...],
) -> ClauseConflictWitness:
    hard = _hard_candidates(elaborated)
    if not hard:
        _runtime_fail("EMPTY_CLAUSE_CONFLICT_WITNESS")
    for size in range(1, len(hard) + 1):
        candidate_witnesses: list[tuple[str, ...]] = []
        for subset in combinations(hard, size):
            if not any(
                all(_candidate_satisfied(candidate, pair) for candidate in subset)
                for pair in pairs
            ):
                candidate_witnesses.append(
                    tuple(candidate.clause_link for candidate in subset)
                )
        if candidate_witnesses:
            return ClauseConflictWitness(clause_links=min(candidate_witnesses))
    _runtime_fail("CLAUSE_CONFLICT_WITNESS_NOT_FOUND")


def _no_authorized_action_witness(
    excluded_by_action: dict[str, tuple[str, ...]],
) -> NoAuthorizedActionWitness:
    return NoAuthorizedActionWitness(
        excluded_actions=tuple(
            ExcludedAction(
                action_id=action_id,
                unauthorized_managed_effects=excluded_by_action[action_id],
            )
            for action_id in sorted(excluded_by_action)
        )
    )


def _restricted_legal(
    legal_joint_completions: tuple[Assignment, ...],
    query_links: tuple[str, ...],
    answer: tuple[TypedValue, ...],
) -> tuple[Assignment, ...]:
    return tuple(
        completion
        for completion in legal_joint_completions
        if _projection(completion, query_links) == answer
    )


def _closes_without_another_ask(
    elaborated: ElaboratedSemanticState,
    restricted_legal: tuple[Assignment, ...],
    trajectories: tuple[Trajectory, ...],
) -> bool:
    pairs = _matching_pairs(restricted_legal, trajectories)
    hard_valid = _hard_valid_pairs(elaborated, pairs)
    if not hard_valid:
        return True
    authorized, _excluded = _authorization(elaborated, hard_valid)
    if not authorized:
        return True
    return bool(_safe_choices(elaborated, restricted_legal, authorized))


def _ask_decision(
    elaborated: ElaboratedSemanticState,
    legal_joint_completions: tuple[Assignment, ...],
    trajectories: tuple[Trajectory, ...],
) -> AskDecision:
    user_links = _unresolved_user_links(elaborated)
    for size in range(1, len(user_links) + 1):
        for subset in combinations(user_links, size):
            answers = _distinct_ordered(
                tuple(
                    _projection(completion, subset)
                    for completion in legal_joint_completions
                )
            )
            if answers and all(
                _closes_without_another_ask(
                    elaborated,
                    _restricted_legal(legal_joint_completions, subset, answer),
                    trajectories,
                )
                for answer in answers
            ):
                return AskDecision(semantic_slot_links=tuple(subset))
    _runtime_fail("NO_SUFFICIENT_USER_QUERY")


def decide(
    elaborated: ElaboratedSemanticState,
    candidate_trajectory_ids: tuple[str, ...],
) -> RuntimeEvaluation:
    legal_joint_completions = enumerate_joint_completions(elaborated)
    empty_domain_witness = _first_empty_domain_witness(elaborated)
    if empty_domain_witness is not None:
        return RuntimeEvaluation(
            legal_joint_completions=legal_joint_completions,
            decision=RejectDecision(
                reason="HARD_UNSAT",
                witness=empty_domain_witness,
                executor_resolutions=(),
            ),
        )
    if not legal_joint_completions:
        return RuntimeEvaluation(
            legal_joint_completions=legal_joint_completions,
            decision=RejectDecision(
                reason="HARD_UNSAT",
                witness=_cross_empty_witness(elaborated),
                executor_resolutions=(),
            ),
        )
    trajectories = _candidate_trajectories(candidate_trajectory_ids)
    _validate_trajectory_structure(elaborated, trajectories)
    pairs = _matching_pairs(legal_joint_completions, trajectories)
    hard_valid = _hard_valid_pairs(elaborated, pairs)
    if not hard_valid:
        return RuntimeEvaluation(
            legal_joint_completions=legal_joint_completions,
            decision=RejectDecision(
                reason="HARD_UNSAT",
                witness=_clause_conflict_witness(elaborated, pairs),
                executor_resolutions=(),
            ),
        )
    authorized, excluded_by_action = _authorization(elaborated, hard_valid)
    if not authorized:
        return RuntimeEvaluation(
            legal_joint_completions=legal_joint_completions,
            decision=RejectDecision(
                reason="NO_AUTHORIZED_ACTION",
                witness=_no_authorized_action_witness(excluded_by_action),
                executor_resolutions=(),
            ),
        )
    safe_choices = _safe_choices(elaborated, legal_joint_completions, authorized)
    if safe_choices:
        selected = safe_choices[0]
        return RuntimeEvaluation(
            legal_joint_completions=legal_joint_completions,
            decision=ExecuteDecision(
                action_id=selected.action_id,
                executor_resolutions=_executor_resolutions(
                    elaborated,
                    selected.executor_assignment,
                ),
            ),
            _supporting_trajectories=selected.trajectories,
        )
    return RuntimeEvaluation(
        legal_joint_completions=legal_joint_completions,
        decision=_ask_decision(elaborated, legal_joint_completions, trajectories),
    )
