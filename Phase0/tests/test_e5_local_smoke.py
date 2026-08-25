"""E5 checks using only fake local transport and temporary evidence roots."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest import mock

from Phase0 import run_e5_smoke
from Phase0.implementation.fixture_loader import load_fixture_input
from Phase0.implementation.schema import CanonicalPayload
from Phase0.implementation.typed_paths import alpha_A, alpha_B
from Phase0.run_e5_smoke import E5Error


SOURCE_COMMIT = "a" * 40
OUTPUT_ROOT = f"Phase0/evidence/E5_{SOURCE_COMMIT}_qwen3_14b"
EXACT_DECISION = {
    "kind": "ASK",
    "semantic_slot_links": ["slot:clause:000:arg0"],
}


def _service_response(content: str) -> dict:
    return {
        "model": run_e5_smoke.MODEL,
        "created_at": "2026-08-25T00:00:00Z",
        "message": {
            "role": "assistant",
            "content": content,
            "thinking": "",
        },
        "done": True,
        "done_reason": "stop",
        "total_duration": 1,
        "eval_count": 1,
    }


def _exact_response() -> dict:
    return _service_response(
        json.dumps(EXACT_DECISION, sort_keys=True, separators=(",", ":"))
    )


def _records(responses: tuple[dict, dict]):
    return [
        run_e5_smoke._analyze_response(request_id, response, EXACT_DECISION)
        for request_id, response in zip(
            run_e5_smoke.REQUEST_IDS,
            responses,
            strict=True,
        )
    ]


class E5LocalSmokeTest(unittest.TestCase):
    maxDiff = None

    def test_a_b_surfaces_and_packets_are_exact_isolates(self) -> None:
        fixture = load_fixture_input(
            run_e5_smoke.REPO_ROOT / run_e5_smoke.FIXTURE_PATH,
            run_e5_smoke.FIXTURE_CASE,
        )
        self.assertIsInstance(fixture.entry_payload, CanonicalPayload)
        self.assertEqual(
            alpha_A(run_e5_smoke._a_surface()),
            fixture.entry_payload.canonical_state,
        )
        self.assertEqual(
            alpha_B(run_e5_smoke._b_surface()),
            fixture.entry_payload.canonical_state,
        )

        a_packet, b_packet = run_e5_smoke.build_packets()
        self.assertNotEqual(
            a_packet["semantic_serialization"],
            b_packet["semantic_serialization"],
        )
        for packet in (a_packet, b_packet):
            self.assertEqual(
                set(packet),
                {
                    "encoding",
                    "source_envelope",
                    "semantic_serialization",
                    "visible_world_context",
                    "slot_declarations",
                    "static_constraints",
                    "cross_constraints",
                    "dialect_interpretations",
                    "managed_effect_universe",
                    "candidate_trajectories",
                },
            )
            self.assertEqual(packet["source_envelope"]["spans"][0]["role"], "USER")
            self.assertEqual(
                [item["owner"] for item in packet["slot_declarations"]],
                ["USER", "EXECUTOR"],
            )
            self.assertEqual(len(packet["candidate_trajectories"]), 2)
            for trajectory in packet["candidate_trajectories"]:
                self.assertEqual(
                    set(trajectory),
                    {
                        "trajectory_id",
                        "action_id",
                        "assignment",
                        "initial_observables",
                        "final_observables",
                        "ordered_effects",
                    },
                )
                self.assertEqual(len(trajectory["assignment"]), 2)
                self.assertEqual(len(trajectory["final_observables"]), 2)
        a_shared = {
            key: value
            for key, value in a_packet.items()
            if key not in {"encoding", "semantic_serialization"}
        }
        b_shared = {
            key: value
            for key, value in b_packet.items()
            if key not in {"encoding", "semantic_serialization"}
        }
        self.assertEqual(a_shared, b_shared)

    def test_messages_schema_and_request_bodies_are_frozen(self) -> None:
        first, second = run_e5_smoke.build_requests()
        self.assertEqual([item["model"] for item in (first, second)], ["qwen3:14b"] * 2)
        for request in (first, second):
            self.assertEqual(
                set(request),
                {
                    "model",
                    "messages",
                    "format",
                    "stream",
                    "think",
                    "keep_alive",
                    "options",
                },
            )
            self.assertEqual(request["format"], run_e5_smoke.DECISION_SCHEMA)
            self.assertEqual(request["messages"][0]["content"], run_e5_smoke.SYSTEM_MESSAGE)
            self.assertEqual(request["options"], {"temperature": 0, "seed": 0, "num_predict": 256})
            self.assertIs(request["stream"], False)
            self.assertIs(request["think"], False)
            self.assertEqual(request["keep_alive"], 0)
            user_content = request["messages"][1]["content"]
            self.assertEqual(
                user_content,
                json.dumps(
                    json.loads(user_content),
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ),
            )
            self.assertNotIn('"expected"', user_content)
        self.assertEqual(
            run_e5_smoke.SYSTEM_MESSAGE,
            run_e5_smoke.SYSTEM_POLICY
            + "\nDecision JSON schema:\n"
            + run_e5_smoke._compact_json(run_e5_smoke.DECISION_SCHEMA),
        )
        self.assertEqual(len(run_e5_smoke.DECISION_SCHEMA["$defs"]), 7)
        self.assertEqual(len(run_e5_smoke.DECISION_SCHEMA["oneOf"]), 4)
        first_packet = json.loads(first["messages"][1]["content"])
        second_packet = json.loads(second["messages"][1]["content"])
        self.assertEqual(first_packet["encoding"], "A")
        self.assertEqual(second_packet["encoding"], "B")

    def test_proxy_disabled_local_transport_timeout_limit_and_body(self) -> None:
        opener = run_e5_smoke._build_opener()
        proxy_handlers = [
            item for item in opener.handlers if isinstance(item, urllib.request.ProxyHandler)
        ]
        # An empty ProxyHandler installs no protocol methods and therefore is not
        # retained by OpenerDirector; its presence suppresses the default
        # environment-derived proxy handler.
        self.assertEqual(proxy_handlers, [])
        self.assertTrue(
            any(isinstance(item, run_e5_smoke._NoRedirect) for item in opener.handlers)
        )

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *unused):
                return False

            def read(self, amount):
                self.amount = amount
                return json.dumps(_exact_response()).encode()

        class FakeOpener:
            def __init__(self):
                self.response = Response()

            def open(self, request, timeout):
                self.request = request
                self.timeout = timeout
                return self.response

        fake = FakeOpener()
        body = run_e5_smoke.build_requests()[0]
        with mock.patch.object(run_e5_smoke, "_build_opener", return_value=fake):
            self.assertEqual(run_e5_smoke._http_transport(body), _exact_response())
        self.assertEqual(fake.request.full_url, "http://127.0.0.1:11434/api/chat")
        self.assertEqual(fake.request.method, "POST")
        self.assertEqual(fake.request.headers, {"Content-type": "application/json"})
        self.assertEqual(fake.request.data, run_e5_smoke._compact_json(body).encode())
        self.assertEqual(fake.timeout, 600)
        self.assertEqual(fake.response.amount, 1024 * 1024 + 1)

    def test_response_limit_and_redirect_handler_fail_loud(self) -> None:
        class LargeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *unused):
                return False

            def read(self, amount):
                return b"x" * amount

        fake = mock.Mock()
        fake.open.return_value = LargeResponse()
        with mock.patch.object(run_e5_smoke, "_build_opener", return_value=fake):
            with self.assertRaisesRegex(E5Error, "1 MiB"):
                run_e5_smoke._http_transport(run_e5_smoke.build_requests()[0])
        self.assertIsNone(
            run_e5_smoke._NoRedirect().redirect_request(
                None,
                None,
                302,
                "redirect",
                {},
                "http://example.com",
            )
        )

    def test_completed_outputs_produce_truthful_statuses_and_keep_raw(self) -> None:
        invalid_json = _service_response("not json")
        invalid_schema = _service_response('{"kind":"ASK","semantic_slot_links":[]}')
        mismatch = _service_response(
            '{"action_id":"other","executor_resolutions":[],"kind":"EXECUTE"}'
        )
        exact = _exact_response()
        cases = (
            (invalid_json, "INVALID_OUTPUT", "INVALID_JSON"),
            (invalid_schema, "INVALID_OUTPUT", "INVALID_DECISION_SCHEMA"),
            (mismatch, "DECISION_MISMATCH", None),
            (exact, "EXACT_MATCH", None),
        )
        for response, outcome, error in cases:
            with self.subTest(outcome=outcome, error=error):
                record = run_e5_smoke._analyze_response("A", response, EXACT_DECISION)
                self.assertIs(record["service_response"], response)
                self.assertEqual(record["outcome"], outcome)
                self.assertEqual(record["validation_error"], error)

        summaries = (
            (_records((exact, exact)), "MATCH", "PASS"),
            (_records((exact, mismatch)), "MISMATCH", "FAIL"),
            (_records((invalid_json, invalid_schema)), "NOT_COMPARABLE", "FAIL"),
        )
        for records, parity, status in summaries:
            summary = run_e5_smoke._build_summary(SOURCE_COMMIT, records)
            self.assertEqual(summary["parsed_decision_parity"], parity)
            self.assertEqual(summary["status"], status)
            self.assertNotIn("score", summary)
            self.assertNotIn("recommendation", summary)

    def test_service_envelope_failures_are_infrastructure_errors(self) -> None:
        mutations = (
            {"model": "other"},
            {"done": False},
            {"message": {"role": "tool", "content": "{}"}},
            {"message": {"role": "assistant", "content": ""}},
            {
                "message": {
                    "role": "assistant",
                    "content": "{}",
                    "tool_calls": [{"function": {}}],
                }
            },
            {"message": {"role": "assistant", "content": "{}", "thinking": "x"}},
        )
        for mutation in mutations:
            response = _exact_response()
            response.update(mutation)
            with self.subTest(mutation=mutation):
                with self.assertRaises(E5Error):
                    run_e5_smoke._validate_service_envelope(response)

    def test_record_makes_exactly_two_calls_then_reads_expected_and_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "evidence"
            events = []

            def transport(request):
                events.append(json.loads(request["messages"][1]["content"])["encoding"])
                self.assertNotIn("expected", events)
                return _exact_response()

            def expected():
                events.append("expected")
                return EXACT_DECISION

            with (
                mock.patch.object(run_e5_smoke, "_preflight_record", return_value=root),
                mock.patch.object(run_e5_smoke, "_read_expected_decision", side_effect=expected),
            ):
                summary = run_e5_smoke.record_evidence(
                    SOURCE_COMMIT,
                    run_e5_smoke.HANDOFF_BLOB,
                    OUTPUT_ROOT,
                    transport=transport,
                )
            self.assertEqual(events, ["A", "B", "expected"])
            self.assertEqual(summary["status"], "PASS")
            self.assertEqual({item.name for item in root.iterdir()}, set(run_e5_smoke.PACKAGE_FILES))
            responses = json.loads((root / "responses.json").read_text())
            self.assertEqual(len(responses["responses"]), 2)
            self.assertEqual(
                [item["service_response"] for item in responses["responses"]],
                [_exact_response(), _exact_response()],
            )

    def test_invalid_completed_content_is_fail_with_no_retry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "evidence"
            calls = []

            def transport(request):
                calls.append(request)
                return _service_response("invalid")

            with (
                mock.patch.object(run_e5_smoke, "_preflight_record", return_value=root),
                mock.patch.object(run_e5_smoke, "_read_expected_decision", return_value=EXACT_DECISION),
            ):
                summary = run_e5_smoke.record_evidence(
                    SOURCE_COMMIT,
                    run_e5_smoke.HANDOFF_BLOB,
                    OUTPUT_ROOT,
                    transport=transport,
                )
            self.assertEqual(len(calls), 2)
            self.assertEqual(summary["status"], "FAIL")

    def test_transport_or_envelope_failure_creates_no_evidence(self) -> None:
        failures = (
            OSError("transport"),
            _service_response(""),
        )
        for failure in failures:
            with self.subTest(failure=type(failure).__name__):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "evidence"

                    def transport(unused):
                        if isinstance(failure, Exception):
                            raise failure
                        return failure

                    with (
                        mock.patch.object(run_e5_smoke, "_preflight_record", return_value=root),
                        mock.patch.object(run_e5_smoke, "_read_expected_decision") as expected,
                    ):
                        with self.assertRaises((E5Error, OSError)):
                            run_e5_smoke.record_evidence(
                                SOURCE_COMMIT,
                                run_e5_smoke.HANDOFF_BLOB,
                                OUTPUT_ROOT,
                                transport=transport,
                            )
                    expected.assert_not_called()
                    self.assertFalse(root.exists())

    def test_atomic_writer_is_exact_and_non_overwriting(self) -> None:
        files = {name: name.encode() for name in run_e5_smoke.PACKAGE_FILES}
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "evidence"
            run_e5_smoke.write_evidence_package(root, files)
            self.assertEqual(
                {item.name: item.read_bytes() for item in root.iterdir()},
                files,
            )
            self.assertEqual({item.name for item in parent.iterdir()}, {"evidence"})
            with self.assertRaisesRegex(E5Error, "already exists"):
                run_e5_smoke.write_evidence_package(root, files)
            with self.assertRaises(E5Error):
                run_e5_smoke.write_evidence_package(
                    parent / "other",
                    {"manifest.json": b"x"},
                )

    def test_offline_verifier_accepts_exact_and_rejects_tampering(self) -> None:
        requests = run_e5_smoke.build_requests()
        records = _records((_exact_response(), _exact_response()))
        files = run_e5_smoke._serialize_package(
            SOURCE_COMMIT,
            OUTPUT_ROOT,
            requests,
            records,
        )
        for mutation in ("none", "missing", "extra", "tampered"):
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "evidence"
                    run_e5_smoke.write_evidence_package(root, files)
                    if mutation == "missing":
                        (root / "summary.json").unlink()
                    elif mutation == "extra":
                        (root / "extra.json").write_text("{}")
                    elif mutation == "tampered":
                        (root / "responses.json").write_bytes(
                            (root / "responses.json").read_bytes() + b" "
                        )
                    with mock.patch.object(
                        run_e5_smoke,
                        "_http_transport",
                        side_effect=AssertionError("offline verifier made HTTP call"),
                    ):
                        if mutation == "none":
                            summary = run_e5_smoke.verify_evidence_files(
                                SOURCE_COMMIT,
                                OUTPUT_ROOT,
                                root,
                            )
                            self.assertEqual(summary["status"], "PASS")
                        else:
                            with self.assertRaises(E5Error):
                                run_e5_smoke.verify_evidence_files(
                                    SOURCE_COMMIT,
                                    OUTPUT_ROOT,
                                    root,
                                )

    def test_source_handoff_root_and_git_preflight_mismatches_stop_early(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "evidence"
            git_cases = (
                ("b" * 40, "", run_e5_smoke.HANDOFF_BLOB, "Git HEAD"),
                (SOURCE_COMMIT, " M Phase0/run_e5_smoke.py", run_e5_smoke.HANDOFF_BLOB, "not clean"),
                (SOURCE_COMMIT, "", "b" * 40, "checked-out handoff"),
            )
            for head, status, blob, message in git_cases:
                with self.subTest(message=message):
                    values = iter((head, status, blob))
                    with (
                        mock.patch.object(run_e5_smoke, "_output_path", return_value=root),
                        mock.patch.object(run_e5_smoke, "_git_output", side_effect=lambda *args: next(values)),
                        mock.patch.object(run_e5_smoke, "_preflight_model") as model_check,
                    ):
                        with self.assertRaisesRegex(E5Error, message):
                            run_e5_smoke._preflight_record(
                                SOURCE_COMMIT,
                                run_e5_smoke.HANDOFF_BLOB,
                                OUTPUT_ROOT,
                            )
                    model_check.assert_not_called()
                    self.assertFalse(root.exists())

        for bad_commit in ("A" * 40, "a" * 39, "g" * 40):
            with self.assertRaises(E5Error):
                run_e5_smoke._require_commit(bad_commit)
        with self.assertRaises(E5Error):
            run_e5_smoke._require_handoff("b" * 40)
        for bad_root in (
            f"./{OUTPUT_ROOT}",
            str(run_e5_smoke.REPO_ROOT / OUTPUT_ROOT),
            "Phase0/evidence/alternate",
        ):
            with self.assertRaises(E5Error):
                run_e5_smoke._output_path(SOURCE_COMMIT, bad_root)

    def test_existing_output_root_rejects_before_model_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "evidence"
            root.mkdir()
            values = iter((SOURCE_COMMIT, "", run_e5_smoke.HANDOFF_BLOB))
            with (
                mock.patch.object(run_e5_smoke, "_output_path", return_value=root),
                mock.patch.object(run_e5_smoke, "_git_output", side_effect=lambda *args: next(values)),
                mock.patch.object(run_e5_smoke, "_preflight_model") as model_check,
            ):
                with self.assertRaisesRegex(E5Error, "already exists"):
                    run_e5_smoke._preflight_record(
                        SOURCE_COMMIT,
                        run_e5_smoke.HANDOFF_BLOB,
                        OUTPUT_ROOT,
                    )
            model_check.assert_not_called()

    def test_model_preflight_success_and_each_frozen_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            blob_path = Path(directory) / "blob"
            blob_path.write_bytes(b"frozen blob")
            good_modelfile = f"FROM {blob_path}\n".encode()

            def outputs(*arguments):
                if arguments == ("--version",):
                    return b"ollama version is 0.32.6\n"
                if arguments == ("list",):
                    return b"NAME ID SIZE\nqwen3:14b bdbd181c33f2 9.3 GB\n"
                if arguments == ("show", "qwen3:14b", "--modelfile"):
                    return good_modelfile
                raise AssertionError(arguments)

            patches = (
                mock.patch.object(run_e5_smoke, "MODEL_BLOB_PATH", blob_path),
                mock.patch.object(run_e5_smoke, "MODEL_BLOB_BYTES", len(b"frozen blob")),
                mock.patch.object(
                    run_e5_smoke,
                    "MODEL_BLOB_SHA256",
                    hashlib.sha256(b"frozen blob").hexdigest(),
                ),
                mock.patch.object(
                    run_e5_smoke,
                    "MODELFILE_SHA256",
                    hashlib.sha256(good_modelfile).hexdigest(),
                ),
                mock.patch.object(run_e5_smoke, "_ollama_output", side_effect=outputs),
            )
            with patches[0], patches[1], patches[2], patches[3], patches[4]:
                run_e5_smoke._preflight_model()

                mismatch_cases = (
                    ("OLLAMA_VERSION", "0.0.0", "version"),
                    ("MODEL_LIST_ID", "wrong", "tag/list ID"),
                    ("MODELFILE_SHA256", "0" * 64, "Modelfile checksum"),
                    ("MODEL_BLOB_BYTES", 1, "blob size"),
                    ("MODEL_BLOB_SHA256", "0" * 64, "blob checksum"),
                )
                for attribute, value, message in mismatch_cases:
                    with self.subTest(attribute=attribute):
                        with mock.patch.object(run_e5_smoke, attribute, value):
                            with self.assertRaisesRegex(E5Error, message):
                                run_e5_smoke._preflight_model()

                wrong_from = b"FROM /wrong/blob\n"
                with (
                    mock.patch.object(
                        run_e5_smoke,
                        "MODELFILE_SHA256",
                        hashlib.sha256(wrong_from).hexdigest(),
                    ),
                    mock.patch.object(
                        run_e5_smoke,
                        "_ollama_output",
                        side_effect=lambda *args: wrong_from
                        if args == ("show", "qwen3:14b", "--modelfile")
                        else outputs(*args),
                    ),
                ):
                    with self.assertRaisesRegex(E5Error, "FROM target"):
                        run_e5_smoke._preflight_model()

    def test_ollama_preflight_environment_cannot_select_proxy_or_host(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "HTTP_PROXY": "http://external.invalid",
                "https_proxy": "http://external.invalid",
                "OLLAMA_HOST": "http://external.invalid",
            },
            clear=True,
        ):
            environment = run_e5_smoke._local_ollama_environment()
        self.assertEqual(environment, {"OLLAMA_HOST": run_e5_smoke.ENDPOINT})


if __name__ == "__main__":
    unittest.main()
