"""Shared deterministic backend for Phase 0 E1 canonical semantics."""

from __future__ import annotations

from dataclasses import dataclass, field

from Phase0.implementation.dialect import Observable
from Phase0.implementation.elaboration import ElaboratedSemanticState, elaborate
from Phase0.implementation.runtime import (
    Assignment,
    Decision,
    ExecuteDecision,
    RuntimeFailure,
    decide,
)
from Phase0.implementation.schema import (
    CanonicalSemanticState,
    CrossConstraint,
    SlotDeclaration,
    SourceEnvelope,
    StaticConstraint,
    VisibleWorldContext,
)


@dataclass(frozen=True)
class ExecutedResult:
    kind: str = field(default="EXECUTED", init=False)
    action_id: str
    final_observables: tuple[Observable, ...]
    ordered_effects: tuple[str, ...]


@dataclass(frozen=True)
class BackendOutcome:
    elaborated: ElaboratedSemanticState
    legal_joint_completions: tuple[Assignment, ...]
    decision: Decision
    result: ExecutedResult | None


def _execution_result(runtime_evaluation) -> ExecutedResult | None:
    decision = runtime_evaluation.decision
    if not isinstance(decision, ExecuteDecision):
        return None
    trajectories = runtime_evaluation._supporting_trajectories
    if not trajectories:
        raise RuntimeFailure("MISSING_EXECUTION_SUPPORT")
    if any(trajectory.action_id != decision.action_id for trajectory in trajectories):
        raise RuntimeFailure("EXECUTION_SUPPORT_MISMATCH")
    first = trajectories[0]
    if any(
        trajectory.final_observables != first.final_observables
        or trajectory.ordered_effects != first.ordered_effects
        for trajectory in trajectories
    ):
        return None
    return ExecutedResult(
        action_id=decision.action_id,
        final_observables=first.final_observables,
        ordered_effects=first.ordered_effects,
    )


def run_backend(
    canonical_state: CanonicalSemanticState,
    source_envelope: SourceEnvelope | None,
    visible_world_context: VisibleWorldContext,
    slot_declarations: tuple[SlotDeclaration, ...],
    static_constraints: tuple[StaticConstraint, ...],
    cross_constraints: tuple[CrossConstraint, ...],
    candidate_trajectory_ids: tuple[str, ...],
) -> BackendOutcome:
    elaborated = elaborate(
        canonical_state,
        source_envelope,
        visible_world_context,
        slot_declarations,
        static_constraints,
        cross_constraints,
    )
    runtime_evaluation = decide(elaborated, candidate_trajectory_ids)
    return BackendOutcome(
        elaborated=elaborated,
        legal_joint_completions=runtime_evaluation.legal_joint_completions,
        decision=runtime_evaluation.decision,
        result=_execution_result(runtime_evaluation),
    )
