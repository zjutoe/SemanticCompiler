"""E4 checks for bounded traces and deterministic Phase 0 closure."""

from __future__ import annotations

import inspect
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

from Phase0 import run_phase0
from Phase0.implementation import backend, content_bridge, elaboration, runtime
from Phase0.implementation import typed_paths
from Phase0.implementation.content_bridge import (
    ExtractiveContentState,
    beta_C,
    build_referenced_support_view,
    normal_c_extract,
)
from Phase0.implementation.dialect import AssignmentItem, PREDICATES
from Phase0.implementation.fixture_loader import load_fixture_input
from Phase0.implementation.schema import (
    CanonicalPayload,
    ExtractiveContentPayload,
    TypedValue,
)
from Phase0.implementation.typed_paths import AdapterFailure, alpha_A, alpha_B
from Phase0.run_phase0 import (
    Arm,
    E4Error,
    EvidencePackage,
    FinalDecision,
    FinalOutcome,
    Package,
    Stage,
    build_evidence_bundles,
    serialize_evidence_package,
    verify_evidence_packages,
    write_evidence_packages,
)


SOURCE_COMMIT = "a" * 40
ROOT = Path(__file__).resolve().parents[2]

EXPECTED_IDS = {
    Package.NORMAL: (
        "A__F1__unresolved",
        "B__F3__unresolved",
        "C__F9__normal",
        "A__F8__missing_adapter_link",
    ),
    Package.GOLD_C_DEBUG: (
        "GOLD_C_DEBUG__F9__gold_c_original",
    ),
    Package.GOLD_CANONICAL_DEBUG: (
        "GOLD_CANONICAL_DEBUG__F6__clause_conflict",
        "GOLD_CANONICAL_DEBUG__F8__dangling_support",
        "GOLD_CANONICAL_DEBUG__F8__wrong_enum_type",
        "GOLD_CANONICAL_DEBUG__F8__malformed_domain",
        "GOLD_CANONICAL_DEBUG__F8__declared_empty_domain",
    ),
}

EXPECTED_STAGES = {
    "A__F1__unresolved": (
        Stage.ADAPTER_OR_BRIDGE,
        Stage.ELABORATION,
        Stage.RUNTIME,
    ),
    "B__F3__unresolved": (
        Stage.ADAPTER_OR_BRIDGE,
        Stage.ELABORATION,
        Stage.RUNTIME,
    ),
    "C__F9__normal": (
        Stage.SURFACE,
        Stage.ADAPTER_OR_BRIDGE,
        Stage.ELABORATION,
        Stage.RUNTIME,
        Stage.EXECUTION,
    ),
    "GOLD_C_DEBUG__F9__gold_c_original": (
        Stage.ADAPTER_OR_BRIDGE,
        Stage.ELABORATION,
        Stage.RUNTIME,
        Stage.EXECUTION,
    ),
    "GOLD_CANONICAL_DEBUG__F6__clause_conflict": (
        Stage.ELABORATION,
        Stage.RUNTIME,
    ),
    "GOLD_CANONICAL_DEBUG__F8__dangling_support": (Stage.ELABORATION,),
    "GOLD_CANONICAL_DEBUG__F8__wrong_enum_type": (Stage.ELABORATION,),
    "A__F8__missing_adapter_link": (Stage.ADAPTER_OR_BRIDGE,),
    "GOLD_CANONICAL_DEBUG__F8__malformed_domain": (Stage.ELABORATION,),
    "GOLD_CANONICAL_DEBUG__F8__declared_empty_domain": (Stage.ELABORATION,),
}

EXPECTED_LOCAL_COUNTS = {
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


def _by_id(bundles: tuple[EvidencePackage, ...]):
    return {
        trace.scenario_id: trace
        for bundle in bundles
        for trace in bundle.traces
    }


def _aggregate_counts(bundles: tuple[EvidencePackage, ...]) -> dict[str, int]:
    traces = tuple(trace for bundle in bundles for trace in bundle.traces)
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


def _write_new_set(root: Path) -> tuple[EvidencePackage, ...]:
    bundles = build_evidence_bundles(SOURCE_COMMIT)
    write_evidence_packages(bundles, root)
    return bundles


class E4TraceAndClosureTest(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.bundles = build_evidence_bundles(SOURCE_COMMIT)
        self.traces = _by_id(self.bundles)

    def test_exact_matrix_order_stages_arms_and_counts(self) -> None:
        self.assertEqual(
            tuple(bundle.package for bundle in self.bundles),
            (
                Package.NORMAL,
                Package.GOLD_C_DEBUG,
                Package.GOLD_CANONICAL_DEBUG,
            ),
        )
        for bundle in self.bundles:
            self.assertEqual(
                tuple(trace.scenario_id for trace in bundle.traces),
                EXPECTED_IDS[bundle.package],
            )
            self.assertEqual(
                bundle.summary["counts"],
                EXPECTED_LOCAL_COUNTS[bundle.package],
            )
            for trace in bundle.traces:
                self.assertEqual(
                    tuple(stage.stage for stage in trace.stages),
                    EXPECTED_STAGES[trace.scenario_id],
                )
                self.assertLessEqual(len(trace.stages), 5)

        self.assertEqual(self.traces["A__F1__unresolved"].arm, Arm.A)
        self.assertEqual(self.traces["B__F3__unresolved"].arm, Arm.B)
        self.assertEqual(self.traces["C__F9__normal"].arm, Arm.C)
        self.assertEqual(
            self.traces["GOLD_C_DEBUG__F9__gold_c_original"].arm,
            Arm.GOLD_C_DEBUG,
        )
        self.assertTrue(
            all(
                trace.arm is Arm.GOLD_CANONICAL_DEBUG
                for trace in self.bundles[2].traces
            )
        )
        self.assertEqual(
            _aggregate_counts(self.bundles),
            {
                "scenario_count": 10,
                "decision_count": 5,
                "system_failure_count": 5,
                "ASK": 1,
                "EXECUTE": 3,
                "REJECT": 1,
                "executed_result_count": 2,
            },
        )

    def test_terminal_decisions_results_witnesses_and_f8_stop_points(self) -> None:
        ask = self.traces["A__F1__unresolved"]
        self.assertEqual(ask.final_decision, FinalDecision.ASK)
        self.assertEqual(ask.ask_links, ("slot:clause:000:arg0",))
        self.assertIsNone(ask.result_ref)

        f3 = self.traces["B__F3__unresolved"]
        self.assertEqual(f3.final_decision, FinalDecision.EXECUTE)
        self.assertEqual(
            f3.executor_resolutions,
            (
                AssignmentItem(
                    "slot:clause:000:arg1",
                    TypedValue("Backend", "LOCAL"),
                ),
            ),
        )
        self.assertIsNone(f3.result_ref)
        self.assertEqual(f3.stages[-1].stage, Stage.RUNTIME)

        for scenario_id in (
            "C__F9__normal",
            "GOLD_C_DEBUG__F9__gold_c_original",
        ):
            trace = self.traces[scenario_id]
            self.assertEqual(trace.final_decision, FinalDecision.EXECUTE)
            self.assertIsNotNone(trace.result_ref)
            self.assertEqual(trace.stages[-1].stage, Stage.EXECUTION)

        reject = self.traces[
            "GOLD_CANONICAL_DEBUG__F6__clause_conflict"
        ]
        self.assertEqual(reject.final_decision, FinalDecision.REJECT)
        self.assertEqual(reject.reject_reason, "HARD_UNSAT")
        self.assertNotEqual(reject.reject_witness_ref, reject.stages[-1].output_ref)
        self.assertTrue(reject.reject_witness_ref.endswith(":reject_witness"))
        self.assertIsNone(reject.result_ref)

        expected_failures = {
            "GOLD_CANONICAL_DEBUG__F8__dangling_support": (
                Stage.ELABORATION,
                "DANGLING_SUPPORT_REF",
            ),
            "GOLD_CANONICAL_DEBUG__F8__wrong_enum_type": (
                Stage.ELABORATION,
                "TYPE_MISMATCH",
            ),
            "A__F8__missing_adapter_link": (
                Stage.ADAPTER_OR_BRIDGE,
                "MISSING_ADAPTER_LINK",
            ),
            "GOLD_CANONICAL_DEBUG__F8__malformed_domain": (
                Stage.ELABORATION,
                "MALFORMED_DOMAIN_DECLARATION",
            ),
            "GOLD_CANONICAL_DEBUG__F8__declared_empty_domain": (
                Stage.ELABORATION,
                "DECLARED_EMPTY_DOMAIN",
            ),
        }
        for scenario_id, terminal in expected_failures.items():
            with self.subTest(scenario_id=scenario_id):
                trace = self.traces[scenario_id]
                self.assertEqual(trace.final_outcome, FinalOutcome.SYSTEM_FAILURE)
                self.assertEqual(trace.final_decision, FinalDecision.NOT_PRODUCED)
                self.assertEqual(
                    (trace.stages[-1].stage, trace.stages[-1].failure_reason),
                    terminal,
                )
                self.assertIsNone(trace.stages[-1].output_ref)
                self.assertIsNone(trace.result_ref)
                self.assertFalse(trace.ask_links)
                self.assertFalse(trace.executor_resolutions)
                self.assertIsNone(trace.reject_reason)
                self.assertIsNone(trace.reject_witness_ref)

    def test_artifact_refs_are_local_complete_bounded_and_trace_has_no_source(self) -> None:
        fixture_texts = (
            "Require a supported output policy.",
            "Require a supported service route.",
            "Require final format JSON.",
            "Allow managed effect WRITE_OUTPUT.",
        )
        for bundle in self.bundles:
            refs = [artifact["ref"] for artifact in bundle.artifacts]
            self.assertEqual(len(refs), len(set(refs)))
            self.assertTrue(
                all(
                    ref.startswith(f"artifact:{bundle.package.value}:")
                    for ref in refs
                )
            )
            used = set()
            for trace in bundle.traces:
                used.add(trace.input_ref)
                for stage in trace.stages:
                    used.add(stage.input_ref)
                    if stage.output_ref is not None:
                        used.add(stage.output_ref)
                if trace.result_ref is not None:
                    used.add(trace.result_ref)
                if trace.reject_witness_ref is not None:
                    used.add(trace.reject_witness_ref)
            self.assertEqual(used, set(refs))
            self.assertTrue(
                all(
                    len(json.dumps(artifact, sort_keys=True)) < 20_000
                    for artifact in bundle.artifacts
                )
            )
            trace_bytes = serialize_evidence_package(bundle)["traces.jsonl"]
            for text in fixture_texts:
                self.assertNotIn(text.encode(), trace_bytes)

    def test_decision_field_consistency(self) -> None:
        for trace in self.traces.values():
            with self.subTest(scenario_id=trace.scenario_id):
                if trace.final_outcome is FinalOutcome.SYSTEM_FAILURE:
                    self.assertEqual(
                        trace.final_decision,
                        FinalDecision.NOT_PRODUCED,
                    )
                    continue
                self.assertTrue(
                    all(stage.failure_reason is None for stage in trace.stages)
                )
                if trace.final_decision is FinalDecision.ASK:
                    self.assertTrue(trace.ask_links)
                    self.assertFalse(trace.executor_resolutions)
                elif trace.final_decision is FinalDecision.EXECUTE:
                    self.assertFalse(trace.ask_links)
                    self.assertIsNone(trace.reject_reason)
                    self.assertIsNone(trace.reject_witness_ref)
                elif trace.final_decision is FinalDecision.REJECT:
                    self.assertIn(
                        trace.reject_reason,
                        ("HARD_UNSAT", "NO_AUTHORIZED_ACTION"),
                    )
                    self.assertIsNotNone(trace.reject_witness_ref)
                    self.assertIsNone(trace.result_ref)
                else:
                    self.fail(trace.final_decision)

    def test_a_b_c_and_debug_entry_boundaries(self) -> None:
        f1 = load_fixture_input(ROOT / run_phase0.F1_PATH, "unresolved")
        f3 = load_fixture_input(ROOT / run_phase0.F3_PATH, "unresolved")
        self.assertIsInstance(f1.entry_payload, CanonicalPayload)
        self.assertIsInstance(f3.entry_payload, CanonicalPayload)
        self.assertEqual(
            alpha_A(run_phase0._a_f1_surface()),
            f1.entry_payload.canonical_state,
        )
        self.assertEqual(
            alpha_B(run_phase0._b_f3_surface()),
            f3.entry_payload.canonical_state,
        )

        normal = load_fixture_input(ROOT / run_phase0.F9_PATH, "normal")
        gold = load_fixture_input(
            ROOT / run_phase0.F9_PATH,
            "gold_c_original",
        )
        self.assertIsInstance(gold.entry_payload, ExtractiveContentPayload)
        normal_content = normal_c_extract(normal.source_envelope)
        gold_content = ExtractiveContentState(gold.entry_payload.content_refs)
        self.assertEqual(normal_content.content_refs, ("u1", "u2", "a1"))
        self.assertEqual(gold_content.content_refs, ("u1", "u2"))
        normal_canonical = beta_C(
            normal_content,
            build_referenced_support_view(
                normal.source_envelope,
                normal_content,
            ),
            PREDICATES,
            normal.visible_world_context,
        )
        gold_canonical = beta_C(
            gold_content,
            build_referenced_support_view(gold.source_envelope, gold_content),
            PREDICATES,
            gold.visible_world_context,
        )
        self.assertNotEqual(normal_canonical, gold_canonical)
        self.assertEqual(
            self.traces["C__F9__normal"].stages[0].stage,
            Stage.SURFACE,
        )
        self.assertEqual(
            self.traces["GOLD_C_DEBUG__F9__gold_c_original"].stages[0].stage,
            Stage.ADAPTER_OR_BRIDGE,
        )
        self.assertEqual(
            self.traces[
                "GOLD_CANONICAL_DEBUG__F6__clause_conflict"
            ].stages[0].stage,
            Stage.ELABORATION,
        )

        with mock.patch.object(
            typed_paths,
            "alpha_A",
            side_effect=AssertionError("alpha_A must not be called"),
        ):
            with self.assertRaises(AdapterFailure) as raised:
                typed_paths.adapt_typed_surface(None, object())
        self.assertEqual(raised.exception.reason, "MISSING_ADAPTER_LINK")

    def test_writer_is_deterministic_exact_and_non_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            first = temporary / "first"
            second = temporary / "second"
            write_evidence_packages(self.bundles, first)
            write_evidence_packages(
                build_evidence_bundles(SOURCE_COMMIT),
                second,
            )
            expected_packages = {
                "normal",
                "gold_c_debug",
                "gold_canonical_debug",
            }
            self.assertEqual({item.name for item in first.iterdir()}, expected_packages)
            for package in expected_packages:
                first_files = {
                    item.name: item.read_bytes()
                    for item in (first / package).iterdir()
                }
                second_files = {
                    item.name: item.read_bytes()
                    for item in (second / package).iterdir()
                }
                self.assertEqual(
                    set(first_files),
                    {
                        "manifest.json",
                        "artifacts.json",
                        "traces.jsonl",
                        "summary.json",
                    },
                )
                self.assertEqual(first_files, second_files)
                joined = b"".join(first_files.values())
                self.assertNotIn(str(ROOT).encode(), joined)
                for forbidden in (b"timestamp", b"uuid", b"hostname", b"inode"):
                    self.assertNotIn(forbidden, joined.lower())
            with self.assertRaises(E4Error):
                write_evidence_packages(self.bundles, first)

    def test_manifest_and_summary_have_the_fixed_schema(self) -> None:
        manifest_keys = {
            "schema_version",
            "package",
            "implementation_source_commit",
            "accepted_handoff_path",
            "accepted_handoff_blob",
            "runner_path",
            "fixture_paths",
            "package_root",
            "scenario_ids",
        }
        all_fixture_paths = set()
        for bundle in self.bundles:
            manifest = bundle.manifest
            self.assertEqual(set(manifest), manifest_keys)
            self.assertEqual(manifest["schema_version"], run_phase0.SCHEMA_VERSION)
            self.assertEqual(manifest["package"], bundle.package.value)
            self.assertEqual(manifest["implementation_source_commit"], SOURCE_COMMIT)
            self.assertEqual(
                manifest["accepted_handoff_blob"],
                run_phase0.E4_HANDOFF_BLOB,
            )
            self.assertEqual(manifest["accepted_handoff_path"], run_phase0.HANDOFF_PATH)
            self.assertEqual(manifest["runner_path"], run_phase0.RUNNER_PATH)
            self.assertEqual(
                manifest["package_root"],
                f"Phase0/evidence/E4_{SOURCE_COMMIT}/{bundle.package.value}",
            )
            self.assertEqual(
                tuple(manifest["scenario_ids"]),
                EXPECTED_IDS[bundle.package],
            )
            all_fixture_paths.update(manifest["fixture_paths"])
            self.assertEqual(bundle.summary["status"], "PASS")
            self.assertEqual(
                tuple(bundle.summary["scenario_ids"]),
                EXPECTED_IDS[bundle.package],
            )
        self.assertEqual(
            all_fixture_paths,
            {
                run_phase0.F1_PATH,
                run_phase0.F3_PATH,
                run_phase0.F6_PATH,
                run_phase0.F8_PATH,
                run_phase0.F9_PATH,
            },
        )

    def test_verifier_rejects_missing_extra_and_tampered_files(self) -> None:
        mutations = ("missing", "extra", "tampered")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "evidence"
                    bundles = _write_new_set(root)
                    self.assertEqual(
                        verify_evidence_packages(bundles, root)["scenario_count"],
                        10,
                    )
                    if mutation == "missing":
                        (root / "normal" / "summary.json").unlink()
                    elif mutation == "extra":
                        (root / "normal" / "extra.json").write_text("{}")
                    else:
                        path = root / "normal" / "traces.jsonl"
                        path.write_bytes(path.read_bytes() + b"{}\n")
                    with self.assertRaises(E4Error):
                        verify_evidence_packages(bundles, root)

    def test_record_preflight_rejects_head_and_all_dirty_states_before_write(self) -> None:
        source_commit = "1" * 40
        output_root = f"Phase0/evidence/E4_{source_commit}"
        base_root = ROOT / output_root
        self.assertFalse(base_root.exists())
        cases = (
            ("2" * 40, "", "source commit does not equal Git HEAD"),
            (source_commit, "M  Phase0/run_phase0.py", "not clean"),
            (source_commit, " M Phase0/run_phase0.py", "not clean"),
            (source_commit, "?? Phase0/untracked", "not clean"),
        )
        for head, status, message in cases:
            with self.subTest(status=status or "head-mismatch"):
                with (
                    mock.patch.object(run_phase0, "_repo_head", return_value=head),
                    mock.patch.object(run_phase0, "_repo_status", return_value=status),
                ):
                    with self.assertRaisesRegex(E4Error, message):
                        run_phase0._preflight_record(
                            source_commit,
                            run_phase0.E4_HANDOFF_BLOB,
                            output_root,
                        )
                self.assertFalse(base_root.exists())

    def test_cli_identity_and_normalized_root_checks(self) -> None:
        expected_root = f"Phase0/evidence/E4_{SOURCE_COMMIT}"
        self.assertEqual(
            run_phase0._output_path(SOURCE_COMMIT, expected_root),
            ROOT / expected_root,
        )
        for bad_commit in ("A" * 40, "a" * 39, "g" * 40):
            with self.subTest(commit=bad_commit):
                with self.assertRaises(E4Error):
                    run_phase0._require_commit(bad_commit)
        for bad_root in (
            str(ROOT / expected_root),
            f"./{expected_root}",
            f"Phase0/evidence/../evidence/E4_{SOURCE_COMMIT}",
            "Phase0/evidence/alternate",
        ):
            with self.subTest(root=bad_root):
                with self.assertRaises(E4Error):
                    run_phase0._output_path(SOURCE_COMMIT, bad_root)
        with self.assertRaises(E4Error):
            run_phase0._require_handoff("b" * 40)
        parser = run_phase0._parser()
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parser.parse_args(["other"])

    def test_expected_values_only_validate_completed_actual_paths(self) -> None:
        original_expected = run_phase0._read_expected

        def wrong_expected(spec):
            value = dict(original_expected(spec))
            value["decision"] = {"kind": "REJECT"}
            return value

        with (
            mock.patch.object(
                run_phase0,
                "adapt_typed_surface",
                wraps=run_phase0.adapt_typed_surface,
            ) as adapter_spy,
            mock.patch.object(
                run_phase0,
                "run_backend",
                wraps=run_phase0.run_backend,
            ) as backend_spy,
            mock.patch.object(run_phase0, "_read_expected", side_effect=wrong_expected),
        ):
            with self.assertRaisesRegex(E4Error, "actual outcome"):
                build_evidence_bundles(SOURCE_COMMIT)
        adapter_spy.assert_called_once()
        backend_spy.assert_called_once()

        for module in (
            typed_paths,
            content_bridge,
            elaboration,
            runtime,
            backend,
        ):
            source = inspect.getsource(module)
            self.assertNotIn('["expected"]', source)
            self.assertNotIn("['expected']", source)


if __name__ == "__main__":
    unittest.main()
