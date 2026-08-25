"""Versioned finite dialect manifest and runtime-only trajectories for E0."""

from __future__ import annotations

from dataclasses import dataclass

from Phase0.implementation.schema import (
    Backend,
    ErrorPolicy,
    LogMode,
    OutputFormat,
    PredicateScope,
    ServiceMode,
    Strictness,
    TypedValue,
)


DIALECT_VERSION = "contract-ir.phase0.v0"
FIXTURE_SCHEMA_VERSION = "phase0.e0.v1"
MANAGED_EFFECTS = ("WRITE_OUTPUT",)


@dataclass(frozen=True)
class PredicateDefinition:
    predicate: str
    signature: tuple[str, ...]
    scope: str
    interpretation: str


PREDICATES = (
    PredicateDefinition(
        "world.final_format_is",
        ("OutputFormat",),
        PredicateScope.FINAL.value,
        "final observable format equals the argument",
    ),
    PredicateDefinition(
        "world.output_policy_is",
        ("OutputFormat", "Strictness"),
        PredicateScope.FINAL.value,
        "final observables format and strictness equal both arguments",
    ),
    PredicateDefinition(
        "world.error_handling_is",
        ("ErrorPolicy", "LogMode"),
        PredicateScope.FINAL.value,
        "final observables error_policy and log_mode equal both arguments",
    ),
    PredicateDefinition(
        "world.service_route_is",
        ("ServiceMode", "Backend"),
        PredicateScope.FINAL.value,
        "final observables service_mode and backend equal both arguments",
    ),
    PredicateDefinition(
        "world.format_supported",
        ("OutputFormat",),
        PredicateScope.INITIAL.value,
        "initial observable mapping format_supported[argument] is true",
    ),
    PredicateDefinition(
        "effect.WRITE_OUTPUT",
        (),
        PredicateScope.EVENT.value,
        "one emitted event matches the exact effect ID WRITE_OUTPUT",
    ),
)

PREDICATE_BY_ID = {item.predicate: item for item in PREDICATES}

OBSERVABLE_TYPES = {
    "format": "OutputFormat",
    "strictness": "Strictness",
    "error_policy": "ErrorPolicy",
    "log_mode": "LogMode",
    "service_mode": "ServiceMode",
    "backend": "Backend",
}


@dataclass(frozen=True)
class AssignmentItem:
    semantic_slot_link: str
    value: TypedValue


@dataclass(frozen=True)
class Observable:
    name: str
    value: TypedValue


@dataclass(frozen=True)
class Trajectory:
    trajectory_id: str
    action_id: str
    assignment: tuple[AssignmentItem, ...]
    initial_observables: tuple[Observable, ...]
    final_observables: tuple[Observable, ...]
    ordered_effects: tuple[str, ...]


def tv(type_id: str, value_id: str) -> TypedValue:
    return TypedValue(type=type_id, value=value_id)


S0 = "slot:clause:000:arg0"
S1 = "slot:clause:000:arg1"


TRAJECTORIES = (
    Trajectory(
        "tau:f1:json_strict",
        "f1_render_json_strict",
        (AssignmentItem(S0, tv("OutputFormat", OutputFormat.JSON.value)), AssignmentItem(S1, tv("Strictness", Strictness.STRICT.value))),
        (Observable("format", tv("OutputFormat", OutputFormat.UNSET.value)),),
        (Observable("format", tv("OutputFormat", OutputFormat.JSON.value)), Observable("strictness", tv("Strictness", Strictness.STRICT.value))),
        (),
    ),
    Trajectory(
        "tau:f1:yaml_lenient",
        "f1_render_yaml_lenient",
        (AssignmentItem(S0, tv("OutputFormat", OutputFormat.YAML.value)), AssignmentItem(S1, tv("Strictness", Strictness.LENIENT.value))),
        (Observable("format", tv("OutputFormat", OutputFormat.UNSET.value)),),
        (Observable("format", tv("OutputFormat", OutputFormat.YAML.value)), Observable("strictness", tv("Strictness", Strictness.LENIENT.value))),
        (),
    ),
    Trajectory(
        "tau:f2:return_none_quiet",
        "f2_return_none_quiet",
        (AssignmentItem(S0, tv("ErrorPolicy", ErrorPolicy.RETURN_NONE.value)), AssignmentItem(S1, tv("LogMode", LogMode.QUIET.value))),
        (),
        (Observable("error_policy", tv("ErrorPolicy", ErrorPolicy.RETURN_NONE.value)), Observable("log_mode", tv("LogMode", LogMode.QUIET.value))),
        (),
    ),
    Trajectory(
        "tau:f2:raise_verbose",
        "f2_raise_verbose",
        (AssignmentItem(S0, tv("ErrorPolicy", ErrorPolicy.RAISE.value)), AssignmentItem(S1, tv("LogMode", LogMode.VERBOSE.value))),
        (),
        (Observable("error_policy", tv("ErrorPolicy", ErrorPolicy.RAISE.value)), Observable("log_mode", tv("LogMode", LogMode.VERBOSE.value))),
        (),
    ),
    Trajectory(
        "tau:f3:safe_local",
        "f3_use_local",
        (AssignmentItem(S0, tv("ServiceMode", ServiceMode.SAFE.value)), AssignmentItem(S1, tv("Backend", Backend.LOCAL.value))),
        (),
        (Observable("service_mode", tv("ServiceMode", ServiceMode.SAFE.value)), Observable("backend", tv("Backend", Backend.LOCAL.value))),
        (),
    ),
    Trajectory(
        "tau:f3:fast_local",
        "f3_use_local",
        (AssignmentItem(S0, tv("ServiceMode", ServiceMode.FAST.value)), AssignmentItem(S1, tv("Backend", Backend.LOCAL.value))),
        (),
        (Observable("service_mode", tv("ServiceMode", ServiceMode.FAST.value)), Observable("backend", tv("Backend", Backend.LOCAL.value))),
        (),
    ),
    Trajectory(
        "tau:f3:fast_remote",
        "f3_use_remote",
        (AssignmentItem(S0, tv("ServiceMode", ServiceMode.FAST.value)), AssignmentItem(S1, tv("Backend", Backend.REMOTE.value))),
        (),
        (Observable("service_mode", tv("ServiceMode", ServiceMode.FAST.value)), Observable("backend", tv("Backend", Backend.REMOTE.value))),
        (),
    ),
    Trajectory(
        "tau:f4:yaml_lenient",
        "f4_a_yaml_lenient",
        (AssignmentItem(S0, tv("OutputFormat", OutputFormat.YAML.value)), AssignmentItem(S1, tv("Strictness", Strictness.LENIENT.value))),
        (Observable("format", tv("OutputFormat", OutputFormat.UNSET.value)),),
        (Observable("format", tv("OutputFormat", OutputFormat.YAML.value)), Observable("strictness", tv("Strictness", Strictness.LENIENT.value))),
        (),
    ),
    Trajectory(
        "tau:f4:json_strict",
        "f4_b_json_strict",
        (AssignmentItem(S0, tv("OutputFormat", OutputFormat.JSON.value)), AssignmentItem(S1, tv("Strictness", Strictness.STRICT.value))),
        (Observable("format", tv("OutputFormat", OutputFormat.UNSET.value)),),
        (Observable("format", tv("OutputFormat", OutputFormat.JSON.value)), Observable("strictness", tv("Strictness", Strictness.STRICT.value))),
        (),
    ),
    Trajectory("tau:f5:fixed_yaml", "f5_a_yaml", (), (Observable("format", tv("OutputFormat", "UNSET")),), (Observable("format", tv("OutputFormat", "YAML")),), ()),
    Trajectory("tau:f5:fixed_json", "f5_b_json", (), (Observable("format", tv("OutputFormat", "UNSET")),), (Observable("format", tv("OutputFormat", "JSON")),), ()),
    Trajectory("tau:f5:open_yaml", "f5_a_yaml", (AssignmentItem(S0, tv("OutputFormat", "YAML")),), (Observable("format", tv("OutputFormat", "UNSET")),), (Observable("format", tv("OutputFormat", "YAML")),), ()),
    Trajectory("tau:f5:open_json", "f5_b_json", (AssignmentItem(S0, tv("OutputFormat", "JSON")),), (Observable("format", tv("OutputFormat", "UNSET")),), (Observable("format", tv("OutputFormat", "JSON")),), ()),
    Trajectory("tau:f6:json", "f6_render_json", (), (Observable("format", tv("OutputFormat", "UNSET")),), (Observable("format", tv("OutputFormat", "JSON")),), ()),
    Trajectory("tau:f6:yaml", "f6_render_yaml", (), (Observable("format", tv("OutputFormat", "UNSET")),), (Observable("format", tv("OutputFormat", "YAML")),), ()),
    Trajectory("tau:f7:write_json", "f7_write_json", (), (Observable("format", tv("OutputFormat", "UNSET")),), (Observable("format", tv("OutputFormat", "JSON")),), ("WRITE_OUTPUT",)),
    Trajectory("tau:f9:write_json", "write_json", (), (Observable("format", tv("OutputFormat", "UNSET")),), (Observable("format", tv("OutputFormat", "JSON")),), ("WRITE_OUTPUT",)),
)

TRAJECTORIES_BY_ID = {item.trajectory_id: item for item in TRAJECTORIES}


def _observable_map(observables: tuple[Observable, ...]) -> dict[str, TypedValue]:
    return {item.name: item.value for item in observables}


def evaluate_predicate(
    predicate: str,
    args: tuple[TypedValue, ...],
    initial_observables: tuple[Observable, ...],
    final_observables: tuple[Observable, ...],
    ordered_effects: tuple[str, ...],
) -> bool:
    """Evaluate one finite manifest predicate against one trajectory-like record."""
    initial = _observable_map(initial_observables)
    final = _observable_map(final_observables)
    if predicate == "world.final_format_is":
        return final.get("format") == args[0]
    if predicate == "world.output_policy_is":
        return final.get("format") == args[0] and final.get("strictness") == args[1]
    if predicate == "world.error_handling_is":
        return final.get("error_policy") == args[0] and final.get("log_mode") == args[1]
    if predicate == "world.service_route_is":
        return final.get("service_mode") == args[0] and final.get("backend") == args[1]
    if predicate == "world.format_supported":
        return initial.get(f"format_supported[{args[0].value}]") == TypedValue("bool", "true")
    if predicate == "effect.WRITE_OUTPUT":
        return "WRITE_OUTPUT" in ordered_effects
    raise KeyError(predicate)
