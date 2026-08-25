# E5 final evidence review

- Stage: `E5`
- Package: single authorized local `qwen3:14b` A/B smoke evidence
- Overall verdict: `ACCEPT`
- Evidence-integrity verdict: `ACCEPT`
- Recorded smoke status: `FAIL`
- Implementation range: `454e17089f1ec09f41fcfb7eda733a42ee81922e..18fd3bca753d15d0501fa8a807c1fd6689c8f14e`
- Evidence range: `18fd3bca753d15d0501fa8a807c1fd6689c8f14e..98da089206e0e5a252dfd09064bfbda397402e09`
- Handoff path: `Phase0/handoffs/E5_local_qwen3_14b_smoke.md`
- Accepted handoff blob SHA: `ca8daecea42dcaf28c9d1de5cfc6a4988013be10`
- Evidence root: `Phase0/evidence/E5_18fd3bca753d15d0501fa8a807c1fd6689c8f14e_qwen3_14b`
- Implementation review: `Phase0/reviews/E5_18fd3bc_review.md`

## Recorded operation

The runner was invoked once from the exact clean implementation commit:

```sh
python -B Phase0/run_e5_smoke.py record \
  --source-commit 18fd3bca753d15d0501fa8a807c1fd6689c8f14e \
  --handoff-blob ca8daecea42dcaf28c9d1de5cfc6a4988013be10 \
  --output-root Phase0/evidence/E5_18fd3bca753d15d0501fa8a807c1fd6689c8f14e_qwen3_14b
```

No retry, prompt repair, model switch, or additional inference was performed.

## Artifact checksums

```text
manifest.json   4e252c20243e4c6c22d7b018c36a93c6277de91f85b3bc0d50ce6a1d31bb82f8
requests.json   9ecd1e581aa1d55fe1142374a1cb82275a0544add61f31c9c6c3b47c96bd91a7
responses.json  a45af1f88af07c6c9ab0e15cf4b33f03f2087c8cb40bc105afb8b64a6c733ab8
summary.json    329bce1fcbf5b5aebd22cfaf01e3e6d674a881ae518038955fe62e9421fc9e56
```

The manifest additionally binds the external 9,276,184,896-byte model blob SHA-256 `a8cc1361f3145dc01f6d77c6c82c9116b9ffe3c97b34716fe20418455876c40e` and Modelfile SHA-256 `f9490322d6987537a71e039fc188246336809f00bd5e3c472b83c4ff9f132414`.

## Result and interpretation

- A returned schema-valid `ASK` with both `slot:clause:000:arg0` and EXECUTOR-owned `slot:clause:000:arg1`, so its outcome is `DECISION_MISMATCH`.
- B returned the exact minimum-sufficient USER-only `ASK` for `slot:clause:000:arg0`, so its outcome is `EXACT_MATCH`.
- Parsed-decision parity is `MISMATCH`; aggregate status is therefore `FAIL`.

This is a truthful, useful interface failure sample. It does not show that B is generally better than A, does not change the accepted E0-E4 Phase 0 engineering closure, and supports no scientific or deployment conclusion.

## Independent verification

- The evidence range adds exactly the four regular files in the bound root.
- All four checksums above match the committed bytes.
- Offline `verify` exited 0 and independently recomputed A `DECISION_MISMATCH`, B `EXACT_MATCH`, parity `MISMATCH`, and status `FAIL`.
- Requests contain no expected answer or canonical target; decoded packets are deeply equal after removing only encoding and semantic serialization.
- Both complete raw `qwen3:14b` service envelopes are preserved and valid, with `done=true`, one assistant message, and no tools, images, or thinking.
- The manifest binds the exact implementation, handoff, fixture, localhost endpoint, model/blob identity, request settings, output root, and A-before-B order.
- The current model blob was fully rehashed during offline review and matched the manifest.
- The E0-E5 test suite passed 72 tests; ruff and diff checks passed.
- The final reviewer made no Ollama, HTTP, or model request.

## Acceptance

The independent reviewer returned evidence-integrity `ACCEPT` and recorded-smoke status `FAIL`, with no required repair. Main accepts the evidence exactly as committed at `98da089206e0e5a252dfd09064bfbda397402e09`.

E5 is complete. No rerun, prompt repair, successor handoff, alternative model, or Phase 1 experiment is authorized by this acceptance.
