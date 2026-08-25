# E5 handoff contract review

- Stage: `E5`
- Package: optional local `qwen3:14b` LM-interface smoke handoff; no implementation, inference, or evidence was reviewed or authorized
- Verdict: `ACCEPT`
- Reviewed commit/range: `b40a50caf5fbef50eed0b1881c1306c406bb723d..5c5894a5c611f799bd86c86db215f7773ece3e9c`
- Accepted package HEAD: `5c5894a5c611f799bd86c86db215f7773ece3e9c`
- Initial handoff commit: `d8658094925ba6d6fa9d63be82cb98f381fd076e`
- Contract repair commit: `5c5894a5c611f799bd86c86db215f7773ece3e9c`
- Handoff path: `Phase0/handoffs/E5_local_qwen3_14b_smoke.md`
- Accepted handoff blob SHA: `ca8daecea42dcaf28c9d1de5cfc6a4988013be10`
- Accepted predecessor evidence: `20411e9daca5606ad864fef4fe3be43ec5eb9689`
- Predecessor review: `Phase0/reviews/E4_20411e9_review.md`

## Intended package

The accepted range changes exactly:

```text
Phase0/README.md
Phase0/handoffs/E5_local_qwen3_14b_smoke.md
Phase0/handoffs/README.md
```

It freezes one optional, non-blocking local smoke using the already installed Ollama `qwen3:14b`: one A request followed by one B request over the same F2 unresolved semantics. It authorizes no download, external network, paid API, retry, model switch, prompt search, metric, or scientific claim.

The handoff separates contract, implementation, and recorded-smoke gates. Its implementation lease is exactly `Phase0/run_e5_smoke.py` and `Phase0/tests/test_e5_local_smoke.py`; implementation tests make zero real model calls. A later accepted implementation may authorize exactly two localhost inference requests and one four-file evidence root.

## Verification

- `git rev-parse 5c5894a5c611f799bd86c86db215f7773ece3e9c:Phase0/handoffs/E5_local_qwen3_14b_smoke.md` -> `ca8daecea42dcaf28c9d1de5cfc6a4988013be10`.
- Parent topology and merge base are exact: `d865809` descends directly from `b40a50c`, and `5c5894a` descends directly from `d865809`.
- The full range changes only the three intended package paths above; the repair range changes only the handoff.
- The reviewer parsed the frozen schema and confirmed seven `$defs` plus four mutually exclusive Decision branches.
- The reviewer derived the unique minimum-sufficient F2 decision from model-visible facts: neither executor choice safely preserves both USER projections, the only unresolved USER link is `slot:clause:000:arg0`, and either answer then closes to `EXECUTE`.
- Expected output is post-response validation only and is absent from system/user packets and the schema.
- The exact two-call/no-retry local protocol, source/model/handoff preflight, raw response preservation, truthful `PASS|FAIL`, atomic evidence writer, and offline verifier are completely frozen and fit the two-file lease.
- `python -B -m unittest Phase0.tests.test_e0_dialect_and_fixtures Phase0.tests.test_e1_elaboration_and_runtime Phase0.tests.test_e2_typed_paths Phase0.tests.test_e3_content_bridge Phase0.tests.test_e4_trace_and_closure` -> 57 tests passed.
- `git diff --check` passed; the reviewed worktree and index were clean.
- No reviewer network, Ollama, or model call occurred. External artifacts were not generated.

## Findings and repair

The first independent reviewer rejected the initial handoff for two blocking contract defects:

1. the model-visible policy did not define safe execution, minimum-sufficient USER-only ASK selection, or expose the trajectory facts needed to derive the expected decision;
2. the Decision JSON Schema and its byte serialization were described only in prose.

Repair `5c5894a5c611f799bd86c86db215f7773ece3e9c` added complete non-expected F2 trajectory/runtime facts, general ordered decision rules, the literal closed schema, and exact system/user compact JSON serialization. A fresh independent strict read-only reviewer accepted the full repaired range with no findings or required repair.

## Acceptance and dispatch status

Main accepts exactly the handoff package ending at `5c5894a5c611f799bd86c86db215f7773ece3e9c`. The E5 handoff is contract-accepted and `READY_TO_BIND`.

This record does not authorize inference. E5 implementation requires a main-thread binding packet naming the exact clean source commit containing this record, accepted handoff path/blob, accepted E4 predecessor, both leased paths, exact verification commands, and implementation output roots `none`. Only a separately frozen and independently accepted implementation may authorize the one recorded two-request smoke.

Residual risk is bounded to the actual preflight and smoke outcome: the local model binding may have changed, the service may fail, or the two responses may produce a truthful non-blocking `FAIL`.
