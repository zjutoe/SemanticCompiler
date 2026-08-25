"""Fixed E4 Phase 0 trace matrix and deterministic evidence closure."""

# ruff: noqa: E402

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Phase0.implementation.backend import BackendOutcome, ExecutedResult, run_backend
from Phase0.implementation.content_bridge import (
    CPathFailure,
    ExtractiveContentState,
    beta_C,
    build_referenced_support_view,
    normal_c_extract,
)
from Phase0.implementation.dialect import AssignmentItem, PREDICATES
from Phase0.implementation.elaboration import (
    ElaboratedSemanticState,
    ElaborationFailure,
)
from Phase0.implementation.fixture_loader import load_fixture_input
from Phase0.implementation.runtime import (
    AskDecision,
    ExecuteDecision,
    RejectDecision,
    RuntimeFailure,
)
from Phase0.implementation.schema import (
    AdapterPayload,
    CanonicalPayload,
    ExtractiveContentPayload,
    FixtureInput,
)
from Phase0.implementation.typed_paths import (
    AdapterFailure,
    ContractClause,
    ContractOpenArgument,
    ContractSurfaceState,
    IsomorphicOpenBinding,
    IsomorphicProposition,
    IsomorphicTerm,
    SemanticIsomorphicSurfaceState,
    adapt_typed_surface,
)


E4_HANDOFF_BLOB = "80c4358b28d3b41d0b6a46065ba0b3db32f3841a"
SCHEMA_VERSION = "phase0.e4.v1"
HANDOFF_PATH = "Phase0/handoffs/E4_trace_and_end_to_end_closure.md"
RUNNER_PATH = "Phase0/run_phase0.py"

REPO_ROOT = Path(__file__).resolve().parents[1]

F1_PATH = "Phase0/fixtures/F1_OPEN_UU_COUPLED_MIN_ASK.json"
F3_PATH = "Phase0/fixtures/F3_EXECUTOR_COVERAGE_NONVACUOUS.json"
F6_PATH = "Phase0/fixtures/F6_HARD_UNSAT_WITNESS.json"
F8_PATH = "Phase0/fixtures/F8_NO_SILENT_INVALID_EXECUTION.json"
F9_PATH = "Phase0/fixtures/F9_C_NORMAL_END_TO_END_EXACT.json"

PACKAGE_FILES = (
    "manifest.json",
    "artifacts.json",
    "traces.jsonl",
    "summary.json",
)


class E4Error(ValueError):
    """Raised when the fixed E4 record or verification contract is violated."""


class Package(str, Enum):
    NORMAL = "normal"
    GOLD_C_DEBUG = "gold_c_debug"
    GOLD_CANONICAL_DEBUG = "gold_canonical_debug"


class Arm(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    GOLD_C_DEBUG = "GOLD_C_DEBUG"
    GOLD_CANONICAL_DEBUG = "GOLD_CANONICAL_DEBUG"


class Stage(str, Enum):
    SURFACE = "surface"
    ADAPTER_OR_BRIDGE = "adapter_or_bridge"
    ELABORATION = "elaboration"
    RUNTIME = "runtime"
    EXECUTION = "execution"


class FinalOutcome(str, Enum):
    DECISION = "DECISION"
    SYSTEM_FAILURE = "SYSTEM_FAILURE"


class FinalDecision(str, Enum):
    EXECUTE = "EXECUTE"
    ASK = "ASK"
    REJECT = "REJECT"
    NOT_PRODUCED = "NOT_PRODUCED"


@dataclass(frozen=True)
class StageTrace:
    stage: Stage
    input_ref: str
    output_ref: str | None
    failure_reason: str | None


@dataclass(frozen=True)
class ScenarioTrace:
    scenario_id: str
    input_ref: str
    arm: Arm
    stages: tuple[StageTrace, ...]
    final_outcome: FinalOutcome
    final_decision: FinalDecision
    result_ref: str | None
    ask_links: tuple[str, ...]
    executor_resolutions: tuple[AssignmentItem, ...]
    reject_reason: str | None
    reject_witness_ref: str | None


@dataclass(frozen=True)
class EvidencePackage:
    package: Package
    manifest: Mapping[str, Any]
    artifacts: tuple[Mapping[str, Any], ...]
    traces: tuple[ScenarioTrace, ...]
    summary: Mapping[str, Any]


@dataclass(frozen=True)
class _ScenarioSpec:
    package: Package
    scenario_id: str
    arm: Arm
    fixture_path: str
    case_id: str
    stages: tuple[Stage, ...]


_SCENARIOS = (
    _ScenarioSpec(
        Package.NORMAL,
        "A__F1__unresolved",
        Arm.A,
        F1_PATH,
        "unresolved",
        (Stage.ADAPTER_OR_BRIDGE, Stage.ELABORATION, Stage.RUNTIME),
    ),
    _ScenarioSpec(
        Package.NORMAL,
        "B__F3__unresolved",
        Arm.B,
        F3_PATH,
        "unresolved",
        (Stage.ADAPTER_OR_BRIDGE, Stage.ELABORATION, Stage.RUNTIME),
    ),
    _ScenarioSpec(
        Package.NORMAL,
        "C__F9__normal",
        Arm.C,
        F9_PATH,
        "normal",
        (
            Stage.SURFACE,
            Stage.ADAPTER_OR_BRIDGE,
            Stage.ELABORATION,
            Stage.RUNTIME,
            Stage.EXECUTION,
        ),
    ),
    _ScenarioSpec(
        Package.GOLD_C_DEBUG,
        "GOLD_C_DEBUG__F9__gold_c_original",
        Arm.GOLD_C_DEBUG,
        F9_PATH,
        "gold_c_original",
        (
            Stage.ADAPTER_OR_BRIDGE,
            Stage.ELABORATION,
            Stage.RUNTIME,
            Stage.EXECUTION,
        ),
    ),
    _ScenarioSpec(
        Package.GOLD_CANONICAL_DEBUG,
        "GOLD_CANONICAL_DEBUG__F6__clause_conflict",
        Arm.GOLD_CANONICAL_DEBUG,
        F6_PATH,
        "clause_conflict",
        (Stage.ELABORATION, Stage.RUNTIME),
    ),
    _ScenarioSpec(
        Package.GOLD_CANONICAL_DEBUG,
        "GOLD_CANONICAL_DEBUG__F8__dangling_support",
        Arm.GOLD_CANONICAL_DEBUG,
        F8_PATH,
        "dangling_support",
        (Stage.ELABORATION,),
    ),
    _ScenarioSpec(
        Package.GOLD_CANONICAL_DEBUG,
        "GOLD_CANONICAL_DEBUG__F8__wrong_enum_type",
        Arm.GOLD_CANONICAL_DEBUG,
        F8_PATH,
        "wrong_enum_type",
        (Stage.ELABORATION,),
    ),
    _ScenarioSpec(
        Package.NORMAL,
        "A__F8__missing_adapter_link",
        Arm.A,
        F8_PATH,
        "missing_adapter_link",
        (Stage.ADAPTER_OR_BRIDGE,),
    ),
    _ScenarioSpec(
        Package.GOLD_CANONICAL_DEBUG,
        "GOLD_CANONICAL_DEBUG__F8__malformed_domain",
        Arm.GOLD_CANONICAL_DEBUG,
        F8_PATH,
        "malformed_domain",
        (Stage.ELABORATION,),
    ),
    _ScenarioSpec(
        Package.GOLD_CANONICAL_DEBUG,
        "GOLD_CANONICAL_DEBUG__F8__declared_empty_domain",
        Arm.GOLD_CANONICAL_DEBUG,
        F8_PATH,
        "declared_empty_domain",
        (Stage.ELABORATION,),
    ),
)

_PACKAGE_ORDER = (
    Package.NORMAL,
    Package.GOLD_C_DEBUG,
    Package.GOLD_CANONICAL_DEBUG,
)

_FIXTURES_BY_PACKAGE = {
    Package.NORMAL: (F1_PATH, F3_PATH, F9_PATH, F8_PATH),
    Package.GOLD_C_DEBUG: (F9_PATH,),
    Package.GOLD_CANONICAL_DEBUG: (F6_PATH, F8_PATH),
}

_EXPECTED_LOCAL_COUNTS = {
    Package.NORMAL: {
        "scenario_count": 4,
        "decision_count": 3,
        "system_failure_count": 1,
        "ASK": 1,
        "EXECUTE": 2,
        "REJECT": 0,
        "executed_result_count": 1,
    },
    Package.GOLD_C_DEBUG: {
        "scenario_count": 1,
        "decision_count": 1,
        "system_failure_count": 0,
        "ASK": 0,
        "EXECUTE": 1,
        "REJECT": 0,
        "executed_result_count": 1,
    },
    Package.GOLD_CANONICAL_DEBUG: {
        "scenario_count": 5,
        "decision_count": 1,
        "system_failure_count": 4,
        "ASK": 0,
        "EXECUTE": 0,
        "REJECT": 1,
        "executed_result_count": 0,
    },
}

_EXPECTED_TOTAL_COUNTS = {
    "scenario_count": 10,
    "decision_count": 5,
    "system_failure_count": 5,
    "ASK": 1,
    "EXECUTE": 3,
    "REJECT": 1,
    "executed_result_count": 2,
}

_COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _project_elaboration(value: ElaboratedSemanticState) -> dict[str, Any]:
    return {
        "candidates": [
            {
                "clause_link": candidate.clause_link,
                "authority": candidate.authority,
                "active": candidate.active,
            }
            for candidate in value.candidates
        ],
        "active_clause_links": list(value.active_clause_links),
        "knowledge_assertions": _jsonable(value.knowledge_assertions),
        "open_slots": _jsonable(value.open_slots),
        "slot_domains": _jsonable(value.slot_domains),
        "constraint_links": list(value.constraint_links),
    }


def _project_elaboration_input(
    case: FixtureInput,
    canonical_state: Any,
) -> dict[str, Any]:
    return {
        "canonical_state": _jsonable(canonical_state),
        "source_envelope": _jsonable(case.source_envelope),
        "visible_world_context": _jsonable(case.visible_world_context),
        "slot_declarations": _jsonable(case.slot_declarations),
        "static_constraints": _jsonable(case.static_constraints),
        "cross_constraints": _jsonable(case.cross_constraints),
    }


def _project_decision(value: Any) -> dict[str, Any]:
    return _jsonable(value)


def _project_result(value: ExecutedResult | None) -> dict[str, Any] | None:
    if value is None:
        return None
    return {
        "kind": value.kind,
        "action_id": value.action_id,
        "final_observables": {
            observable.name: _jsonable(observable.value)
            for observable in value.final_observables
        },
        "ordered_effects": list(value.ordered_effects),
    }


def _project_runtime(
    value: BackendOutcome,
    witness_ref: str | None,
) -> dict[str, Any]:
    decision = _project_decision(value.decision)
    if isinstance(value.decision, RejectDecision):
        decision.pop("witness")
        decision["witness_ref"] = witness_ref
    return {
        "legal_joint_completions": _jsonable(value.legal_joint_completions),
        "decision": decision,
    }


def _artifact_ref(spec: _ScenarioSpec, suffix: str) -> str:
    return f"artifact:{spec.package.value}:{spec.scenario_id}:{suffix}"


def _add_artifact(
    artifacts: list[Mapping[str, Any]],
    ref: str,
    kind: str,
    value: Any,
) -> str:
    if any(item["ref"] == ref for item in artifacts):
        raise E4Error(f"duplicate artifact ref: {ref}")
    artifacts.append({"ref": ref, "kind": kind, "value": _jsonable(value)})
    return ref


def _a_f1_surface() -> ContractSurfaceState:
    support = ("u1",)
    return ContractSurfaceState(
        clauses=(
            ContractClause(
                clause_link="clause:000",
                modality="REQUIRE",
                predicate="world.output_policy_is",
                arguments=(
                    ContractOpenArgument(
                        "slot:clause:000:arg0",
                        "OutputFormat",
                        "USER",
                        support,
                    ),
                    ContractOpenArgument(
                        "slot:clause:000:arg1",
                        "Strictness",
                        "USER",
                        support,
                    ),
                ),
                proposition_support=support,
                claimed_authority_support=support,
            ),
        ),
        knowledge_assertions=(),
    )


def _b_f3_surface() -> SemanticIsomorphicSurfaceState:
    support = ("u1",)
    return SemanticIsomorphicSurfaceState(
        propositions=(
            IsomorphicProposition(
                proposition_index=0,
                force="REQUIRE",
                relation="world.service_route_is",
                terms=(
                    IsomorphicTerm("OPEN", "ServiceMode", None),
                    IsomorphicTerm("OPEN", "Backend", None),
                ),
                evidence=support,
                authority_evidence=support,
            ),
        ),
        facts=(),
        open_bindings=(
            IsomorphicOpenBinding(0, 0, "USER", support),
            IsomorphicOpenBinding(0, 1, "EXECUTOR", support),
        ),
    )


def _fixture_case(spec: _ScenarioSpec) -> FixtureInput:
    return load_fixture_input(REPO_ROOT / spec.fixture_path, spec.case_id)


def _read_expected(spec: _ScenarioSpec) -> Mapping[str, Any]:
    with (REPO_ROOT / spec.fixture_path).open("r", encoding="utf-8") as handle:
        document = json.load(handle)
    matches = [
        item["expected"]
        for item in document["cases"]
        if item["case_id"] == spec.case_id
    ]
    if len(matches) != 1:
        raise E4Error(f"missing expected fixture case: {spec.scenario_id}")
    return matches[0]


def _run_backend(case: FixtureInput, canonical_state: Any) -> BackendOutcome:
    return run_backend(
        canonical_state,
        case.source_envelope,
        case.visible_world_context,
        case.slot_declarations,
        case.static_constraints,
        case.cross_constraints,
        case.candidate_trajectory_ids,
    )


def _validate_success(
    spec: _ScenarioSpec,
    case: FixtureInput,
    canonical_state: Any,
    outcome: BackendOutcome,
) -> None:
    expected = _read_expected(spec)
    if expected["failure"] is not None:
        raise E4Error(f"{spec.scenario_id}: expected failure but produced decision")
    if spec.arm in (Arm.A, Arm.B):
        if not isinstance(case.entry_payload, CanonicalPayload):
            raise E4Error(f"{spec.scenario_id}: canonical fixture input required")
        if canonical_state != case.entry_payload.canonical_state:
            raise E4Error(f"{spec.scenario_id}: typed adapter canonical mismatch")
    elif spec.arm in (Arm.C, Arm.GOLD_C_DEBUG):
        if _jsonable(canonical_state) != expected["canonical_state"]:
            raise E4Error(f"{spec.scenario_id}: C canonical mismatch")
    elif not isinstance(case.entry_payload, CanonicalPayload):
        raise E4Error(f"{spec.scenario_id}: gold-canonical input required")

    checks = (
        (_project_elaboration(outcome.elaborated), expected["elaboration"]),
        (
            _jsonable(outcome.legal_joint_completions),
            expected["legal_joint_completions"],
        ),
        (_project_decision(outcome.decision), expected["decision"]),
        (_project_result(outcome.result), expected["result"]),
    )
    if any(actual != wanted for actual, wanted in checks):
        raise E4Error(f"{spec.scenario_id}: actual outcome does not match fixture")


def _validate_failure(spec: _ScenarioSpec, failure: Any) -> None:
    expected = _read_expected(spec)
    actual = {"stage": failure.stage, "reason": failure.reason}
    if actual != expected["failure"]:
        raise E4Error(f"{spec.scenario_id}: actual failure does not match fixture")
    if any(
        expected[field] is not None
        for field in (
            "elaboration",
            "legal_joint_completions",
            "decision",
            "result",
        )
    ):
        raise E4Error(f"{spec.scenario_id}: invalid failure expectation")


def _decision_trace_fields(
    decision: Any,
    runtime_ref: str,
) -> tuple[
    FinalDecision,
    tuple[str, ...],
    tuple[AssignmentItem, ...],
    str | None,
    str | None,
]:
    if isinstance(decision, AskDecision):
        return FinalDecision.ASK, decision.semantic_slot_links, (), None, None
    if isinstance(decision, ExecuteDecision):
        return (
            FinalDecision.EXECUTE,
            (),
            decision.executor_resolutions,
            None,
            None,
        )
    if isinstance(decision, RejectDecision):
        return (
            FinalDecision.REJECT,
            (),
            decision.executor_resolutions,
            decision.reason,
            runtime_ref,
        )
    raise E4Error(f"unknown decision record: {type(decision).__name__}")


def _build_success_trace(
    spec: _ScenarioSpec,
    case: FixtureInput,
    canonical_state: Any,
    input_ref: str,
    stages: list[StageTrace],
    artifacts: list[Mapping[str, Any]],
) -> ScenarioTrace:
    canonical_ref = stages[-1].output_ref if stages else input_ref
    if canonical_ref is None:
        raise E4Error(f"{spec.scenario_id}: missing canonical ref")

    try:
        outcome = _run_backend(case, canonical_state)
    except (ElaborationFailure, RuntimeFailure) as failure:
        _validate_failure(spec, failure)
        stages.append(
            StageTrace(Stage(failure.stage), canonical_ref, None, failure.reason)
        )
        return ScenarioTrace(
            scenario_id=spec.scenario_id,
            input_ref=input_ref,
            arm=spec.arm,
            stages=tuple(stages),
            final_outcome=FinalOutcome.SYSTEM_FAILURE,
            final_decision=FinalDecision.NOT_PRODUCED,
            result_ref=None,
            ask_links=(),
            executor_resolutions=(),
            reject_reason=None,
            reject_witness_ref=None,
        )

    _validate_success(spec, case, canonical_state, outcome)
    elaboration_ref = _add_artifact(
        artifacts,
        _artifact_ref(spec, "runtime_input"),
        "runtime_input",
        {
            "elaboration": _project_elaboration(outcome.elaborated),
            "candidate_trajectory_ids": list(case.candidate_trajectory_ids),
        },
    )
    stages.append(
        StageTrace(Stage.ELABORATION, canonical_ref, elaboration_ref, None)
    )
    witness_ref = (
        _artifact_ref(spec, "reject_witness")
        if isinstance(outcome.decision, RejectDecision)
        else None
    )
    runtime_ref = _add_artifact(
        artifacts,
        _artifact_ref(spec, "runtime"),
        "runtime",
        _project_runtime(outcome, witness_ref),
    )
    stages.append(StageTrace(Stage.RUNTIME, elaboration_ref, runtime_ref, None))
    if witness_ref is not None:
        _add_artifact(
            artifacts,
            witness_ref,
            "reject_witness",
            outcome.decision.witness,
        )

    result_ref = None
    if outcome.result is not None:
        result_ref = _add_artifact(
            artifacts,
            _artifact_ref(spec, "result"),
            "result",
            _project_result(outcome.result),
        )
        stages.append(StageTrace(Stage.EXECUTION, runtime_ref, result_ref, None))

    final, ask_links, resolutions, reject_reason, decision_witness_ref = (
        _decision_trace_fields(outcome.decision, witness_ref or runtime_ref)
    )
    return ScenarioTrace(
        scenario_id=spec.scenario_id,
        input_ref=input_ref,
        arm=spec.arm,
        stages=tuple(stages),
        final_outcome=FinalOutcome.DECISION,
        final_decision=final,
        result_ref=result_ref,
        ask_links=ask_links,
        executor_resolutions=resolutions,
        reject_reason=reject_reason,
        reject_witness_ref=decision_witness_ref,
    )


def _build_typed_trace(
    spec: _ScenarioSpec,
    case: FixtureInput,
    artifacts: list[Mapping[str, Any]],
) -> ScenarioTrace:
    surface = _a_f1_surface() if spec.arm is Arm.A else _b_f3_surface()
    adapter_link = "alpha_A" if spec.arm is Arm.A else "alpha_B"
    surface_ref = _add_artifact(
        artifacts,
        _artifact_ref(spec, "surface"),
        "typed_surface",
        surface,
    )
    canonical_state = adapt_typed_surface(adapter_link, surface)
    canonical_ref = _add_artifact(
        artifacts,
        _artifact_ref(spec, "elaboration_input"),
        "elaboration_input",
        _project_elaboration_input(case, canonical_state),
    )
    stages = [
        StageTrace(Stage.ADAPTER_OR_BRIDGE, surface_ref, canonical_ref, None)
    ]
    return _build_success_trace(
        spec,
        case,
        canonical_state,
        surface_ref,
        stages,
        artifacts,
    )


def _build_c_trace(
    spec: _ScenarioSpec,
    case: FixtureInput,
    artifacts: list[Mapping[str, Any]],
) -> ScenarioTrace:
    if case.source_envelope is None:
        raise E4Error(f"{spec.scenario_id}: source envelope required")
    stages: list[StageTrace] = []
    if spec.arm is Arm.C:
        input_ref = _add_artifact(
            artifacts,
            _artifact_ref(spec, "source"),
            "source_envelope",
            case.source_envelope,
        )
        content = normal_c_extract(case.source_envelope)
        content_ref = _add_artifact(
            artifacts,
            _artifact_ref(spec, "extractive_content"),
            "extractive_content",
            content,
        )
        stages.append(StageTrace(Stage.SURFACE, input_ref, content_ref, None))
    else:
        if not isinstance(case.entry_payload, ExtractiveContentPayload):
            raise E4Error(f"{spec.scenario_id}: extractive fixture input required")
        content = ExtractiveContentState(case.entry_payload.content_refs)
        input_ref = _add_artifact(
            artifacts,
            _artifact_ref(spec, "gold_c_input"),
            "gold_c_input",
            {
                "source_envelope": case.source_envelope,
                "extractive_content": content,
            },
        )
        content_ref = input_ref

    view = build_referenced_support_view(case.source_envelope, content)
    canonical_state = beta_C(
        content,
        view,
        PREDICATES,
        case.visible_world_context,
    )
    canonical_ref = _add_artifact(
        artifacts,
        _artifact_ref(spec, "elaboration_input"),
        "elaboration_input",
        _project_elaboration_input(case, canonical_state),
    )
    stages.append(
        StageTrace(Stage.ADAPTER_OR_BRIDGE, content_ref, canonical_ref, None)
    )
    return _build_success_trace(
        spec,
        case,
        canonical_state,
        input_ref,
        stages,
        artifacts,
    )


def _build_gold_canonical_trace(
    spec: _ScenarioSpec,
    case: FixtureInput,
    artifacts: list[Mapping[str, Any]],
) -> ScenarioTrace:
    if not isinstance(case.entry_payload, CanonicalPayload):
        raise E4Error(f"{spec.scenario_id}: canonical fixture input required")
    canonical_state = case.entry_payload.canonical_state
    canonical_ref = _add_artifact(
        artifacts,
        _artifact_ref(spec, "elaboration_input"),
        "elaboration_input",
        _project_elaboration_input(case, canonical_state),
    )
    return _build_success_trace(
        spec,
        case,
        canonical_state,
        canonical_ref,
        [],
        artifacts,
    )


def _build_missing_link_trace(
    spec: _ScenarioSpec,
    case: FixtureInput,
    artifacts: list[Mapping[str, Any]],
) -> ScenarioTrace:
    if not isinstance(case.entry_payload, AdapterPayload):
        raise E4Error(f"{spec.scenario_id}: adapter fixture input required")
    input_ref = _add_artifact(
        artifacts,
        _artifact_ref(spec, "adapter_dispatch"),
        "adapter_dispatch",
        {
            "adapter_link": case.entry_payload.adapter_link,
            "surface_inspected": False,
        },
    )
    try:
        adapt_typed_surface(
            case.entry_payload.adapter_link,
            case.entry_payload.surface,
        )
    except AdapterFailure as failure:
        _validate_failure(spec, failure)
        return ScenarioTrace(
            scenario_id=spec.scenario_id,
            input_ref=input_ref,
            arm=spec.arm,
            stages=(
                StageTrace(
                    Stage.ADAPTER_OR_BRIDGE,
                    input_ref,
                    None,
                    failure.reason,
                ),
            ),
            final_outcome=FinalOutcome.SYSTEM_FAILURE,
            final_decision=FinalDecision.NOT_PRODUCED,
            result_ref=None,
            ask_links=(),
            executor_resolutions=(),
            reject_reason=None,
            reject_witness_ref=None,
        )
    raise E4Error(f"{spec.scenario_id}: missing adapter link did not fail")


def _build_scenario(
    spec: _ScenarioSpec,
) -> tuple[ScenarioTrace, tuple[Mapping[str, Any], ...]]:
    case = _fixture_case(spec)
    artifacts: list[Mapping[str, Any]] = []
    try:
        if spec.scenario_id == "A__F8__missing_adapter_link":
            trace = _build_missing_link_trace(spec, case, artifacts)
        elif spec.arm in (Arm.A, Arm.B):
            trace = _build_typed_trace(spec, case, artifacts)
        elif spec.arm in (Arm.C, Arm.GOLD_C_DEBUG):
            trace = _build_c_trace(spec, case, artifacts)
        else:
            trace = _build_gold_canonical_trace(spec, case, artifacts)
    except CPathFailure as failure:
        _validate_failure(spec, failure)
        raise E4Error(
            f"{spec.scenario_id}: unexpected fixed-matrix C failure"
        ) from failure

    actual_stages = tuple(stage.stage for stage in trace.stages)
    if actual_stages != spec.stages:
        raise E4Error(
            f"{spec.scenario_id}: stage tuple {actual_stages} != {spec.stages}"
        )
    if len(trace.stages) > 5:
        raise E4Error(f"{spec.scenario_id}: trace exceeds five stages")
    _validate_trace_refs(trace, tuple(artifacts))
    return trace, tuple(artifacts)


def _validate_trace_refs(
    trace: ScenarioTrace,
    artifacts: tuple[Mapping[str, Any], ...],
) -> None:
    refs = tuple(item["ref"] for item in artifacts)
    if len(refs) != len(set(refs)):
        raise E4Error(f"{trace.scenario_id}: duplicate artifact refs")
    used = {trace.input_ref}
    for stage in trace.stages:
        used.add(stage.input_ref)
        if stage.output_ref is not None:
            used.add(stage.output_ref)
    if trace.result_ref is not None:
        used.add(trace.result_ref)
    if trace.reject_witness_ref is not None:
        used.add(trace.reject_witness_ref)
    if used != set(refs):
        raise E4Error(f"{trace.scenario_id}: dangling or unused artifact ref")


def _counts(traces: Sequence[ScenarioTrace]) -> dict[str, int]:
    return {
        "scenario_count": len(traces),
        "decision_count": sum(
            trace.final_outcome is FinalOutcome.DECISION for trace in traces
        ),
        "system_failure_count": sum(
            trace.final_outcome is FinalOutcome.SYSTEM_FAILURE for trace in traces
        ),
        "ASK": sum(trace.final_decision is FinalDecision.ASK for trace in traces),
        "EXECUTE": sum(
            trace.final_decision is FinalDecision.EXECUTE for trace in traces
        ),
        "REJECT": sum(
            trace.final_decision is FinalDecision.REJECT for trace in traces
        ),
        "executed_result_count": sum(
            trace.result_ref is not None for trace in traces
        ),
    }


def _validate_trace_fields(trace: ScenarioTrace) -> None:
    if trace.final_outcome is FinalOutcome.SYSTEM_FAILURE:
        if (
            trace.final_decision is not FinalDecision.NOT_PRODUCED
            or trace.result_ref is not None
            or trace.ask_links
            or trace.executor_resolutions
            or trace.reject_reason is not None
            or trace.reject_witness_ref is not None
            or trace.stages[-1].output_ref is not None
            or trace.stages[-1].failure_reason is None
        ):
            raise E4Error(f"{trace.scenario_id}: inconsistent system failure")
        return

    if any(stage.failure_reason is not None for stage in trace.stages):
        raise E4Error(f"{trace.scenario_id}: decision has a failure stage")
    if trace.final_decision is FinalDecision.ASK:
        valid = bool(trace.ask_links) and not (
            trace.executor_resolutions
            or trace.result_ref
            or trace.reject_reason
            or trace.reject_witness_ref
        )
    elif trace.final_decision is FinalDecision.EXECUTE:
        valid = not (
            trace.ask_links or trace.reject_reason or trace.reject_witness_ref
        )
    elif trace.final_decision is FinalDecision.REJECT:
        valid = (
            trace.reject_reason in ("HARD_UNSAT", "NO_AUTHORIZED_ACTION")
            and trace.reject_witness_ref is not None
            and not trace.ask_links
            and trace.result_ref is None
        )
    else:
        valid = False
    if not valid:
        raise E4Error(f"{trace.scenario_id}: inconsistent decision fields")
    if trace.result_ref is not None and trace.stages[-1].stage is not Stage.EXECUTION:
        raise E4Error(f"{trace.scenario_id}: result without execution stage")


def _manifest(
    package: Package,
    source_commit: str,
    scenario_ids: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "package": package.value,
        "implementation_source_commit": source_commit,
        "accepted_handoff_path": HANDOFF_PATH,
        "accepted_handoff_blob": E4_HANDOFF_BLOB,
        "runner_path": RUNNER_PATH,
        "fixture_paths": list(_FIXTURES_BY_PACKAGE[package]),
        "package_root": (
            f"Phase0/evidence/E4_{source_commit}/{package.value}"
        ),
        "scenario_ids": list(scenario_ids),
    }


def build_evidence_bundles(source_commit: str) -> tuple[EvidencePackage, ...]:
    """Build the exact three-package E4 evidence set without writing files."""

    _require_commit(source_commit)
    traces_by_package: dict[Package, list[ScenarioTrace]] = {
        package: [] for package in _PACKAGE_ORDER
    }
    artifacts_by_package: dict[Package, list[Mapping[str, Any]]] = {
        package: [] for package in _PACKAGE_ORDER
    }
    for spec in _SCENARIOS:
        trace, artifacts = _build_scenario(spec)
        _validate_trace_fields(trace)
        traces_by_package[spec.package].append(trace)
        artifacts_by_package[spec.package].extend(artifacts)

    bundles = []
    for package in _PACKAGE_ORDER:
        traces = tuple(traces_by_package[package])
        local_counts = _counts(traces)
        if local_counts != _EXPECTED_LOCAL_COUNTS[package]:
            raise E4Error(f"{package.value}: fixed local counts changed")
        scenario_ids = tuple(trace.scenario_id for trace in traces)
        bundles.append(
            EvidencePackage(
                package=package,
                manifest=_manifest(package, source_commit, scenario_ids),
                artifacts=tuple(artifacts_by_package[package]),
                traces=traces,
                summary={
                    "schema_version": SCHEMA_VERSION,
                    "package": package.value,
                    "implementation_source_commit": source_commit,
                    "status": "PASS",
                    "scenario_ids": list(scenario_ids),
                    "counts": local_counts,
                },
            )
        )

    aggregate = _counts(
        tuple(trace for bundle in bundles for trace in bundle.traces)
    )
    if aggregate != _EXPECTED_TOTAL_COUNTS:
        raise E4Error("fixed aggregate counts changed")
    return tuple(bundles)


def _canonical_json_bytes(value: Any) -> bytes:
    text = json.dumps(
        _jsonable(value),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return f"{text}\n".encode()


def serialize_evidence_package(
    bundle: EvidencePackage,
) -> Mapping[str, bytes]:
    traces = b"".join(_canonical_json_bytes(trace) for trace in bundle.traces)
    artifacts_document = {
        "schema_version": SCHEMA_VERSION,
        "package": bundle.package.value,
        "artifacts": list(bundle.artifacts),
    }
    return {
        "manifest.json": _canonical_json_bytes(bundle.manifest),
        "artifacts.json": _canonical_json_bytes(artifacts_document),
        "traces.jsonl": traces,
        "summary.json": _canonical_json_bytes(bundle.summary),
    }


def _validate_bundle_set(bundles: Sequence[EvidencePackage]) -> None:
    if tuple(bundle.package for bundle in bundles) != _PACKAGE_ORDER:
        raise E4Error("evidence packages must use the fixed package order")


def write_evidence_packages(
    bundles: Sequence[EvidencePackage],
    base_root: Path,
) -> None:
    """Write one new fixed three-package set without overwriting."""

    _validate_bundle_set(bundles)
    if base_root.exists():
        raise E4Error(f"evidence root already exists: {base_root}")
    base_root.mkdir(parents=True)
    for bundle in bundles:
        package_root = base_root / bundle.package.value
        package_root.mkdir()
        serialized = serialize_evidence_package(bundle)
        for file_name in PACKAGE_FILES:
            (package_root / file_name).write_bytes(serialized[file_name])


def verify_evidence_packages(
    bundles: Sequence[EvidencePackage],
    base_root: Path,
) -> Mapping[str, int]:
    """Require an on-disk package set to equal a fresh fixed-matrix build."""

    _validate_bundle_set(bundles)
    if not base_root.is_dir():
        raise E4Error(f"missing evidence root: {base_root}")
    root_entries = {item.name: item for item in base_root.iterdir()}
    if tuple(sorted(root_entries)) != tuple(sorted(item.value for item in Package)):
        raise E4Error("evidence root has missing or extra entries")
    if any(not item.is_dir() for item in root_entries.values()):
        raise E4Error("evidence root entries must be package directories")

    for bundle in bundles:
        package_root = base_root / bundle.package.value
        entries = {item.name: item for item in package_root.iterdir()}
        if tuple(sorted(entries)) != tuple(sorted(PACKAGE_FILES)):
            raise E4Error(f"{bundle.package.value}: missing or extra package file")
        if any(not item.is_file() for item in entries.values()):
            raise E4Error(f"{bundle.package.value}: package entries must be files")
        expected = serialize_evidence_package(bundle)
        for file_name in PACKAGE_FILES:
            if entries[file_name].read_bytes() != expected[file_name]:
                raise E4Error(f"{bundle.package.value}/{file_name}: byte mismatch")

    aggregate = _counts(
        tuple(trace for bundle in bundles for trace in bundle.traces)
    )
    if aggregate != _EXPECTED_TOTAL_COUNTS:
        raise E4Error("verified aggregate counts changed")
    return aggregate


def _require_commit(source_commit: str) -> None:
    if not _COMMIT_RE.fullmatch(source_commit):
        raise E4Error("source commit must be 40 lowercase hexadecimal characters")


def _require_handoff(handoff_blob: str) -> None:
    if handoff_blob != E4_HANDOFF_BLOB:
        raise E4Error("handoff blob does not match the embedded E4 contract")


def _output_path(source_commit: str, output_root: str) -> Path:
    expected = f"Phase0/evidence/E4_{source_commit}"
    if output_root != expected:
        raise E4Error(f"output root must be the normalized path {expected}")
    return REPO_ROOT / output_root


def _git_output(*arguments: str) -> str:
    completed = subprocess.run(
        ("git", *arguments),
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout.strip()


def _repo_head() -> str:
    return _git_output("rev-parse", "HEAD")


def _repo_status() -> str:
    return _git_output("status", "--porcelain", "--untracked-files=all")


def _preflight_record(
    source_commit: str,
    handoff_blob: str,
    output_root: str,
) -> Path:
    _require_commit(source_commit)
    _require_handoff(handoff_blob)
    base_root = _output_path(source_commit, output_root)
    if _repo_head() != source_commit:
        raise E4Error("source commit does not equal Git HEAD")
    if _repo_status():
        raise E4Error("worktree or index is not clean")
    if base_root.exists():
        raise E4Error(f"evidence root already exists: {output_root}")
    return base_root


def record_evidence(
    source_commit: str,
    handoff_blob: str,
    output_root: str,
) -> Mapping[str, int]:
    """Run the clean-HEAD gate and write the fixed evidence packages."""

    base_root = _preflight_record(source_commit, handoff_blob, output_root)
    bundles = build_evidence_bundles(source_commit)
    write_evidence_packages(bundles, base_root)
    return _counts(tuple(trace for bundle in bundles for trace in bundle.traces))


def verify_recorded_evidence(
    source_commit: str,
    handoff_blob: str,
    output_root: str,
) -> Mapping[str, int]:
    """Rebuild and byte-verify the fixed evidence packages."""

    _require_commit(source_commit)
    _require_handoff(handoff_blob)
    base_root = _output_path(source_commit, output_root)
    bundles = build_evidence_bundles(source_commit)
    return verify_evidence_packages(bundles, base_root)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("record", "verify"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--source-commit", required=True)
        subparser.add_argument("--handoff-blob", required=True)
        subparser.add_argument("--output-root", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "record":
            counts = record_evidence(
                arguments.source_commit,
                arguments.handoff_blob,
                arguments.output_root,
            )
        else:
            counts = verify_recorded_evidence(
                arguments.source_commit,
                arguments.handoff_blob,
                arguments.output_root,
            )
    except (E4Error, subprocess.CalledProcessError) as error:
        parser.error(str(error))
    print(json.dumps(counts, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
