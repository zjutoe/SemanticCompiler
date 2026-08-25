"""E3 evidence for the strict normal C extraction and bridge path."""

from __future__ import annotations

import ast
import inspect
import json
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from typing import Any

from Phase0.implementation import content_bridge
from Phase0.implementation.backend import run_backend
from Phase0.implementation.content_bridge import (
    CPathFailure,
    ExtractiveContentState,
    ReferencedSupportView,
    beta_C,
    build_referenced_support_view,
    normal_c_extract,
    segment_source,
)
from Phase0.implementation.dialect import PREDICATES
from Phase0.implementation.fixture_loader import (
    _parse_canonical_state,
    load_fixture_inputs,
)
from Phase0.implementation.runtime import ExecuteDecision
from Phase0.implementation.schema import (
    ContextValue,
    ExtractiveContentPayload,
    OpenTerm,
    SourceEnvelope,
    SourceSpan,
    TypedValue,
    ValueTerm,
    VisibleWorldContext,
)


ROOT = Path(__file__).resolve().parents[1]
F9_PATH = ROOT / "fixtures" / "F9_C_NORMAL_END_TO_END_EXACT.json"
EMPTY_CONTEXT = VisibleWorldContext(entities=(), observable_values=())


def _read_f9() -> dict[str, Any]:
    with F9_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _cases_by_id():
    return {case.case_id: case for case in load_fixture_inputs(F9_PATH)}


def _expected_by_id() -> dict[str, dict[str, Any]]:
    return {case["case_id"]: case["expected"] for case in _read_f9()["cases"]}


def _typed_value(value) -> dict[str, str]:
    return {"type": value.type, "value": value.value}


def _assignment(value) -> list[dict[str, Any]]:
    return [
        {
            "semantic_slot_link": item.semantic_slot_link,
            "value": _typed_value(item.value),
        }
        for item in value
    ]


def _project_elaboration(value) -> dict[str, Any]:
    if value.knowledge_assertions:
        raise AssertionError(value.knowledge_assertions)
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
        "knowledge_assertions": [],
        "open_slots": [
            {
                "semantic_slot_link": slot.semantic_slot_link,
                "type": slot.type,
                "owner": slot.owner,
                "resolved_value": (
                    None
                    if slot.resolved_value is None
                    else _typed_value(slot.resolved_value)
                ),
            }
            for slot in value.open_slots
        ],
        "slot_domains": [
            {
                "semantic_slot_link": domain.semantic_slot_link,
                "values": [_typed_value(item) for item in domain.values],
            }
            for domain in value.slot_domains
        ],
        "constraint_links": list(value.constraint_links),
    }


def _project_decision(value: ExecuteDecision) -> dict[str, Any]:
    return {
        "kind": value.kind,
        "action_id": value.action_id,
        "executor_resolutions": _assignment(value.executor_resolutions),
    }


def _project_result(value) -> dict[str, Any]:
    return {
        "kind": value.kind,
        "action_id": value.action_id,
        "final_observables": {
            observable.name: _typed_value(observable.value)
            for observable in value.final_observables
        },
        "ordered_effects": list(value.ordered_effects),
    }


def _run_case(case, canonical_state):
    return run_backend(
        canonical_state,
        case.source_envelope,
        case.visible_world_context,
        case.slot_declarations,
        case.static_constraints,
        case.cross_constraints,
        case.candidate_trajectory_ids,
    )


class E3ContentBridgeTest(unittest.TestCase):
    maxDiff = None

    def assert_c_failure(self, stage, reason, function, *args) -> None:
        with self.assertRaises(CPathFailure) as raised:
            function(*args)
        self.assertEqual(raised.exception.stage, stage)
        self.assertEqual(raised.exception.reason, reason)
        self.assertEqual(str(raised.exception), f"{stage}/{reason}")

    def test_f9_normal_path_has_exact_bridge_and_backend_output(self) -> None:
        case = _cases_by_id()["normal"]
        expected = _expected_by_id()["normal"]
        state = normal_c_extract(case.source_envelope)
        self.assertEqual(state.content_refs, ("u1", "u2", "a1"))
        self.assertEqual(
            list(state.content_refs),
            expected["dependency_assertions"]["normal_content_refs"],
        )
        view = build_referenced_support_view(case.source_envelope, state)
        expected_view = tuple(
            SourceSpan(**span)
            for span in expected["dependency_assertions"]["referenced_support_view"]
        )
        self.assertEqual(view.spans, expected_view)

        canonical = beta_C(state, view, PREDICATES, case.visible_world_context)
        expected_canonical = _parse_canonical_state(
            expected["canonical_state"],
            "normal.expected.canonical_state",
        )
        self.assertEqual(canonical, expected_canonical)
        outcome = _run_case(case, canonical)
        self.assertEqual(_project_elaboration(outcome.elaborated), expected["elaboration"])
        self.assertEqual(
            [_assignment(item) for item in outcome.legal_joint_completions],
            expected["legal_joint_completions"],
        )
        self.assertIsInstance(outcome.decision, ExecuteDecision)
        self.assertEqual(_project_decision(outcome.decision), expected["decision"])
        self.assertEqual(_project_result(outcome.result), expected["result"])

    def test_f9_gold_refs_exclude_distractor_and_share_the_same_bridge(self) -> None:
        cases = _cases_by_id()
        expected = _expected_by_id()
        bridged = {}
        views = {}
        for case_id in ("gold_c_original", "gold_c_distractor_variant"):
            case = cases[case_id]
            self.assertIsInstance(case.entry_payload, ExtractiveContentPayload)
            state = ExtractiveContentState(case.entry_payload.content_refs)
            self.assertEqual(state.content_refs, ("u1", "u2"))
            view = build_referenced_support_view(case.source_envelope, state)
            views[case_id] = view
            self.assertEqual(tuple(span.ref for span in view.spans), ("u1", "u2"))
            self.assertNotIn("a1", tuple(span.ref for span in view.spans))
            bridged[case_id] = beta_C(
                state,
                view,
                PREDICATES,
                case.visible_world_context,
            )
            self.assertEqual(
                bridged[case_id],
                _parse_canonical_state(
                    expected[case_id]["canonical_state"],
                    f"{case_id}.expected.canonical_state",
                ),
            )
        self.assertEqual(views["gold_c_original"], views["gold_c_distractor_variant"])
        self.assertEqual(
            bridged["gold_c_original"],
            bridged["gold_c_distractor_variant"],
        )

    def test_f9_gold_original_reaches_the_unchanged_backend_exactly(self) -> None:
        case = _cases_by_id()["gold_c_original"]
        expected = _expected_by_id()["gold_c_original"]
        state = ExtractiveContentState(case.entry_payload.content_refs)
        canonical = beta_C(
            state,
            build_referenced_support_view(case.source_envelope, state),
            PREDICATES,
            case.visible_world_context,
        )
        outcome = _run_case(case, canonical)
        self.assertEqual(_project_elaboration(outcome.elaborated), expected["elaboration"])
        self.assertEqual(
            [_assignment(item) for item in outcome.legal_joint_completions],
            expected["legal_joint_completions"],
        )
        self.assertEqual(_project_decision(outcome.decision), expected["decision"])
        self.assertEqual(_project_result(outcome.result), expected["result"])

    def test_elaboration_projection_rejects_nonempty_knowledge_assertions(self) -> None:
        case = _cases_by_id()["normal"]
        state = normal_c_extract(case.source_envelope)
        canonical = beta_C(
            state,
            build_referenced_support_view(case.source_envelope, state),
            PREDICATES,
            case.visible_world_context,
        )
        outcome = _run_case(case, canonical)
        with self.assertRaises(AssertionError):
            _project_elaboration(
                replace(outcome.elaborated, knowledge_assertions=(object(),))
            )

    def test_open_user_and_executor_have_exact_typed_links_and_support(self) -> None:
        envelope = SourceEnvelope(
            spans=(
                SourceSpan("u1", "USER", "Require final format OPEN(USER)."),
                SourceSpan("a1", "ASSISTANT", "Require final format OPEN(EXECUTOR)."),
            )
        )
        state = normal_c_extract(envelope)
        canonical = beta_C(
            state,
            build_referenced_support_view(envelope, state),
            PREDICATES,
            EMPTY_CONTEXT,
        )
        self.assertEqual(
            tuple(candidate.args for candidate in canonical.normative_candidates),
            (
                (OpenTerm("OPEN", "OutputFormat", "slot:clause:000:arg0"),),
                (OpenTerm("OPEN", "OutputFormat", "slot:clause:001:arg0"),),
            ),
        )
        self.assertEqual(
            tuple(
                (
                    mention.type,
                    mention.owner,
                    mention.proposition_link,
                    mention.argument_position,
                    mention.proposition_support,
                )
                for mention in canonical.open_slot_mentions
            ),
            (
                ("OutputFormat", "USER", "clause:000", 0, ("u1",)),
                ("OutputFormat", "EXECUTOR", "clause:001", 0, ("a1",)),
            ),
        )

    def test_extraction_and_bridge_do_not_filter_source_roles(self) -> None:
        envelope = SourceEnvelope(
            spans=(
                SourceSpan("u1", "USER", "Require final format JSON."),
                SourceSpan("a1", "ASSISTANT", "Use YAML."),
                SourceSpan("t1", "TOOL", "Allow managed effect WRITE_OUTPUT."),
            )
        )
        state = normal_c_extract(envelope)
        self.assertEqual(state.content_refs, ("u1", "a1", "t1"))
        view = build_referenced_support_view(envelope, state)
        self.assertEqual(tuple(span.role for span in view.spans), ("USER", "ASSISTANT", "TOOL"))
        canonical = beta_C(state, view, PREDICATES, EMPTY_CONTEXT)
        self.assertEqual(
            tuple(
                (
                    candidate.proposition_support,
                    candidate.claimed_authority_support,
                )
                for candidate in canonical.normative_candidates
            ),
            (
                (("u1",), ("u1",)),
                (("a1",), ("a1",)),
                (("t1",), ("t1",)),
            ),
        )

    def test_lexical_selection_precedes_loud_semantic_rejection(self) -> None:
        envelope = SourceEnvelope(
            spans=(
                SourceSpan("u1", "USER", "Require final format TOML."),
                SourceSpan("u2", "USER", "Allow managed effect UNKNOWN_EFFECT."),
                SourceSpan("u3", "USER", "Require final format OPEN(ADMIN)."),
                SourceSpan("u4", "USER", "This shape is not understood."),
            )
        )
        extracted = normal_c_extract(envelope)
        self.assertEqual(extracted.content_refs, ("u1", "u2", "u3"))
        for ref in extracted.content_refs:
            with self.subTest(ref=ref):
                state = ExtractiveContentState((ref,))
                view = build_referenced_support_view(envelope, state)
                self.assert_c_failure(
                    "adapter_or_bridge",
                    "UNSUPPORTED_CONTENT",
                    beta_C,
                    state,
                    view,
                    PREDICATES,
                    EMPTY_CONTEXT,
                )

        unrecognized = SourceEnvelope(
            spans=(
                SourceSpan("u1", "USER", "Please return JSON."),
                SourceSpan("a1", "ASSISTANT", "Use plain text."),
            )
        )
        self.assert_c_failure(
            "surface",
            "NO_REPRESENTABLE_CONTENT",
            normal_c_extract,
            unrecognized,
        )

    def test_segmenter_strictly_validates_and_freshly_copies_atomic_spans(self) -> None:
        spans = (
            SourceSpan("u1", "USER", "Require final format JSON."),
            SourceSpan("a1", "ASSISTANT", "Use YAML."),
        )
        copied = segment_source(SourceEnvelope(spans))
        self.assertEqual(copied, spans)
        self.assertIsNot(copied, spans)
        for original, fresh in zip(spans, copied, strict=True):
            self.assertIsNot(original, fresh)

        malformed = (
            object(),
            SourceEnvelope(list(spans)),
            SourceEnvelope((object(),)),
            SourceEnvelope((SourceSpan("", "USER", "Use JSON."),)),
            SourceEnvelope((SourceSpan(1, "USER", "Use JSON."),)),
            SourceEnvelope((SourceSpan("u1", "SYSTEM", "Use JSON."),)),
            SourceEnvelope((SourceSpan("u1", 1, "Use JSON."),)),
            SourceEnvelope((SourceSpan("u1", "USER", ""),)),
            SourceEnvelope((SourceSpan("u1", "USER", " Use JSON."),)),
            SourceEnvelope((SourceSpan("u1", "USER", "Use JSON. "),)),
            SourceEnvelope((SourceSpan("u1", "USER", "Use JSON"),)),
            SourceEnvelope((SourceSpan("u1", "USER", "Use JSON.."),)),
            SourceEnvelope((SourceSpan("u1", "USER", "Use\nJSON."),)),
            SourceEnvelope((spans[0], replace(spans[1], ref="u1"))),
        )
        for index, value in enumerate(malformed):
            with self.subTest(index=index):
                self.assert_c_failure(
                    "surface",
                    "INVALID_SOURCE_ENVELOPE",
                    segment_source,
                    value,
                )

    def test_unicode_line_boundary_invalidates_entire_mixed_envelope(self) -> None:
        envelope = SourceEnvelope(
            (
                SourceSpan("u1", "USER", "Use JSON."),
                SourceSpan("u2", "USER", "Use\u2028YAML."),
            )
        )

        for function in (segment_source, normal_c_extract):
            with self.subTest(function=function.__name__):
                self.assert_c_failure(
                    "surface",
                    "INVALID_SOURCE_ENVELOPE",
                    function,
                    envelope,
                )

    def test_support_builder_validates_refs_and_preserves_exact_provenance(self) -> None:
        envelope = SourceEnvelope(
            (
                SourceSpan("u1", "USER", "Require final format JSON."),
                SourceSpan("a1", "ASSISTANT", "Use YAML."),
                SourceSpan("t1", "TOOL", "Allow managed effect WRITE_OUTPUT."),
            )
        )
        state = ExtractiveContentState(("u1", "t1"))
        view = build_referenced_support_view(envelope, state)
        self.assertEqual(view.spans, (envelope.spans[0], envelope.spans[2]))
        self.assertEqual(tuple(span.ref for span in view.spans), ("u1", "t1"))
        self.assertNotIn("a1", tuple(span.ref for span in view.spans))
        self.assertIsNot(view.spans[0], envelope.spans[0])
        self.assertIsNot(view.spans[1], envelope.spans[2])

        invalid_states = (
            ("INVALID_EXTRACTIVE_CONTENT", object()),
            ("INVALID_EXTRACTIVE_CONTENT", ExtractiveContentState([])),
            ("INVALID_EXTRACTIVE_CONTENT", ExtractiveContentState(())),
            ("INVALID_EXTRACTIVE_CONTENT", ExtractiveContentState((1,))),
            ("INVALID_EXTRACTIVE_CONTENT", ExtractiveContentState(("",))),
            ("INVALID_CONTENT_REFS", ExtractiveContentState(("u1", "u1"))),
            ("INVALID_CONTENT_REFS", ExtractiveContentState(("missing",))),
            ("INVALID_CONTENT_REFS", ExtractiveContentState(("t1", "u1"))),
        )
        for reason, invalid in invalid_states:
            with self.subTest(reason=reason, invalid=invalid):
                self.assert_c_failure(
                    "surface",
                    reason,
                    build_referenced_support_view,
                    envelope,
                    invalid,
                )

    def test_bridge_rejects_malformed_state_view_and_mismatches(self) -> None:
        span1 = SourceSpan("u1", "USER", "Use JSON.")
        span2 = SourceSpan("u2", "USER", "Use YAML.")
        valid_state = ExtractiveContentState(("u1",))
        valid_view = ReferencedSupportView((span1,))
        invalid_states = (
            object(),
            ExtractiveContentState([]),
            ExtractiveContentState(()),
            ExtractiveContentState((1,)),
            ExtractiveContentState(("",)),
            ExtractiveContentState(("u1", "u1")),
        )
        for invalid in invalid_states:
            with self.subTest(invalid_state=invalid):
                self.assert_c_failure(
                    "adapter_or_bridge",
                    "INVALID_EXTRACTIVE_CONTENT",
                    beta_C,
                    invalid,
                    valid_view,
                    PREDICATES,
                    EMPTY_CONTEXT,
                )

        invalid_views = (
            object(),
            ReferencedSupportView([]),
            ReferencedSupportView(()),
            ReferencedSupportView((object(),)),
            ReferencedSupportView((replace(span1, role="SYSTEM"),)),
            ReferencedSupportView((replace(span1, text="Use JSON"),)),
            ReferencedSupportView((span1, span1)),
        )
        for invalid in invalid_views:
            with self.subTest(invalid_view=invalid):
                self.assert_c_failure(
                    "adapter_or_bridge",
                    "INVALID_REFERENCED_SUPPORT_VIEW",
                    beta_C,
                    valid_state,
                    invalid,
                    PREDICATES,
                    EMPTY_CONTEXT,
                )

        mismatches = (
            (
                ExtractiveContentState(("u1",)),
                ReferencedSupportView((span1, span2)),
            ),
            (
                ExtractiveContentState(("u1", "u2")),
                ReferencedSupportView((span2, span1)),
            ),
        )
        for state, view in mismatches:
            with self.subTest(state=state, view=view):
                self.assert_c_failure(
                    "adapter_or_bridge",
                    "CONTENT_VIEW_MISMATCH",
                    beta_C,
                    state,
                    view,
                    PREDICATES,
                    EMPTY_CONTEXT,
                )

    def test_bridge_rejects_malformed_manifest_and_visible_context(self) -> None:
        state = ExtractiveContentState(("u1",))
        view = ReferencedSupportView((SourceSpan("u1", "USER", "Use JSON."),))
        manifests = (
            list(PREDICATES),
            tuple(reversed(PREDICATES)),
            (object(),) + PREDICATES[1:],
            (replace(PREDICATES[0], signature=["OutputFormat"]),) + PREDICATES[1:],
            (replace(PREDICATES[0], scope="UNKNOWN"),) + PREDICATES[1:],
        )
        for manifest in manifests:
            with self.subTest(manifest=manifest):
                self.assert_c_failure(
                    "adapter_or_bridge",
                    "INVALID_DIALECT_MANIFEST",
                    beta_C,
                    state,
                    view,
                    manifest,
                    EMPTY_CONTEXT,
                )

        valid_observation = ContextValue(
            predicate="world.format_supported",
            scope="STATIC",
            args=(TypedValue("OutputFormat", "JSON"),),
            value=True,
        )
        self.assertEqual(
            beta_C(
                state,
                view,
                PREDICATES,
                VisibleWorldContext((), (valid_observation,)),
            ).normative_candidates[0].args,
            (ValueTerm("VALUE", TypedValue("OutputFormat", "JSON")),),
        )
        invalid_contexts = (
            object(),
            VisibleWorldContext([], ()),
            VisibleWorldContext((object(),), ()),
            VisibleWorldContext((), []),
            VisibleWorldContext((), (object(),)),
            VisibleWorldContext((), (replace(valid_observation, predicate="unknown"),)),
            VisibleWorldContext((), (replace(valid_observation, scope="FINAL"),)),
            VisibleWorldContext((), (replace(valid_observation, args=[]),)),
            VisibleWorldContext((), (replace(valid_observation, args=()),)),
            VisibleWorldContext(
                (),
                (replace(valid_observation, args=(TypedValue("Strictness", "STRICT"),)),),
            ),
            VisibleWorldContext(
                (),
                (replace(valid_observation, args=(TypedValue("OutputFormat", "TOML"),)),),
            ),
            VisibleWorldContext((), (replace(valid_observation, value=1),)),
        )
        for context in invalid_contexts:
            with self.subTest(context=context):
                self.assert_c_failure(
                    "adapter_or_bridge",
                    "INVALID_VISIBLE_WORLD_CONTEXT",
                    beta_C,
                    state,
                    view,
                    PREDICATES,
                    context,
                )

    def test_frozen_public_records_and_expected_blind_production_dependencies(self) -> None:
        for record in (
            ExtractiveContentState(("u1",)),
            ReferencedSupportView((SourceSpan("u1", "USER", "Use JSON."),)),
        ):
            with self.assertRaises(FrozenInstanceError):
                setattr(record, next(iter(record.__dict__)), ())

        source = inspect.getsource(content_bridge)
        tree = ast.parse(source)
        imports = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }
        self.assertEqual(
            imports,
            {
                "__future__",
                "dataclasses",
                "Phase0.implementation.dialect",
                "Phase0.implementation.schema",
            },
        )
        self.assertEqual(
            tuple(
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            ),
            (),
        )
        identifiers = {
            node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
        } | {
            node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
        }
        forbidden = {
            "open",
            "fixture_id",
            "case_id",
            "scenario_id",
            "expected",
            "gold",
            "candidate_trajectory_ids",
            "action_id",
            "ordered_effects",
            "final_observables",
            "trajectories",
            "actions",
            "results",
            "run_backend",
        }
        self.assertTrue(identifiers.isdisjoint(forbidden))
        self.assertNotIn("Phase0.tests", source)
        self.assertNotIn("fixture_loader", source)
        self.assertNotIn("implementation.backend", source)
        self.assertNotIn("import json", source)
        sentence_key_dicts = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Dict)
            and any(
                isinstance(key, ast.Constant)
                and isinstance(key.value, str)
                and key.value.endswith(".")
                for key in node.keys
            )
        ]
        self.assertEqual(sentence_key_dicts, [])


if __name__ == "__main__":
    unittest.main()
