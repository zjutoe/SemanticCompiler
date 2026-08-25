# E5 handoff — local `qwen3:14b` LM-interface smoke

- Proposed status after contract acceptance: `READY_TO_BIND`
- Classification: optional and non-blocking; Phase 0 is already accepted
- Governing plan: [`IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md`](../IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md), section 11
- Authored against clean `main` commit: `b40a50caf5fbef50eed0b1881c1306c406bb723d`
- Accepted E4 implementation: `028cea8b4b68ed855eca77eed2def899b9ebf417`
- Accepted E4 evidence: `20411e9daca5606ad864fef4fe3be43ec5eb9689`
- Accepted E4 review: [`E4_20411e9_review.md`](../reviews/E4_20411e9_review.md)
- User authorization: local `qwen3:14b`, localhost Ollama only, exactly two inference requests, no download, no external network, and no paid API

## Frozen local model binding

```text
Ollama endpoint: http://127.0.0.1:11434
Ollama version: 0.32.6
model tag: qwen3:14b
ollama list ID: bdbd181c33f2
architecture: qwen3
parameters: 14.8B
quantization: Q4_K_M
context length: 40960
model blob path: /data1/ollama/models/blobs/sha256-a8cc1361f3145dc01f6d77c6c82c9116b9ffe3c97b34716fe20418455876c40e
model blob bytes: 9276184896
model blob SHA-256: a8cc1361f3145dc01f6d77c6c82c9116b9ffe3c97b34716fe20418455876c40e
ollama show qwen3:14b --modelfile SHA-256: f9490322d6987537a71e039fc188246336809f00bd5e3c472b83c4ff9f132414
```

The full blob checksum was computed from the actual local file, not inferred from its name. The Modelfile checksum binds the tag's `FROM` target, chat template, default parameters, and license text. Any mismatch blocks the run; do not pull, recreate, rename, retag, or switch a model.

## Objective and interpretation

Run one A request and one B request over the same frozen F2 unresolved semantics. Check only whether this exact local model/harness pair can consume modality, support-derived USER authority, USER versus EXECUTOR OPEN ownership, and the existing closed `Decision` shape well enough to return the exact minimum-sufficient `ASK`.

`PASS` means only that this narrow interface smoke worked twice, once per encoding. `FAIL` is a valid recorded result and means only that the current model/harness pair did not satisfy the smoke. Neither outcome changes the accepted E0-E4 engineering closure, establishes representation superiority, supports deployment, or authorizes additional model tests.

E5 does not add learned compilation, bridge training, prompt search, model comparison, repeated sampling, metrics, thresholds, tools, retrieval, internet access, fallback, retry, or automatic repair.

## Three-gate workflow

1. **Contract gate.** Main freezes this handoff and obtains an independent strict read-only acceptance before dispatch.
2. **Implementation gate.** One writer edits only the two leased paths below. Tests use a fake local transport and must make zero real Ollama requests. Main freezes and independently reviews the exact implementation range.
3. **Recorded smoke gate.** Only after implementation acceptance, main runs from that exact clean implementation commit. The runner performs exactly two localhost inference requests, writes one four-file evidence root, and is never rerun automatically. Main commits only that root, then a fresh independent reviewer performs offline verification and accepts the evidence package whether its recorded smoke status is `PASS` or `FAIL`, provided the package is truthful and complete.

An HTTP/transport error, model-binding mismatch, malformed service envelope, or incomplete second response is an infrastructure failure: stop without creating the evidence root and return to main. A completed model response whose `message.content` is invalid or semantically wrong is not infrastructure failure; preserve both completed raw responses and record `status=FAIL`. Do not retry or change any setting.

## Implementation lease

Allowed paths:

```text
Phase0/run_e5_smoke.py
Phase0/tests/test_e5_local_smoke.py
```

Every other path is forbidden during implementation. In particular, do not edit E0-E4 source, fixtures, tests, evidence, plan, handoff, or package initializers. Use only the Python standard library and accepted Phase 0 modules. If two files are insufficient, stop and return to main.

## Exact semantic pair

Use only `Phase0/fixtures/F2_OPEN_UE_OWNER_BOUNDARY.json`, case `unresolved`. Construct two explicit fixture-direct surfaces inside the runner:

- A is the accepted clause-centric `ContractSurfaceState` for F2: one `REQUIRE world.error_handling_is(OPEN ErrorPolicy USER, OPEN LogMode EXECUTOR)` clause, with both support fields equal to `[u1]`.
- B is the accepted semantic-isomorphic `SemanticIsomorphicSurfaceState` for the same clause: `force=REQUIRE`, `relation=world.error_handling_is`, two typed OPEN terms, evidence and authority evidence `[u1]`, and the matching USER/EXECUTOR open bindings.

The runner must prove before constructing requests that `alpha_A(A) == alpha_B(B) ==` the F2 fixture canonical input. It must not import test-private conversion helpers. The LM receives the A or B JSON projection, never the canonical state.

Both user messages contain the same source envelope, visible world context, slot declarations, static constraints, cross constraints, and candidate trajectory IDs from F2. Only `encoding` and `semantic_serialization` differ. No fixture `expected`, canonical state, expected decision, or scenario-specific answer hint appears in either system or user message.

The shared system message consists of this exact general-policy prefix followed by `\nDecision JSON schema:\n` and the canonical compact JSON serialization of the frozen schema below. It contains no fixture-specific answer hint:

```text
Interpret only the supplied semantic packet. A normative proposition is active only when its claimed authority support resolves to a USER source. Never choose a value for an unresolved USER-owned OPEN slot. An EXECUTOR-owned OPEN slot may be resolved only after every USER-owned slot required by the same constraints is resolved. Return exactly one Decision matching the supplied closed JSON schema, with no prose.
```

The exact expected output for post-response validation is the accepted F2 result:

```json
{"kind":"ASK","semantic_slot_links":["slot:clause:000:arg0"]}
```

Expected data is a validator only. It must not enter either prompt, request schema restriction, transport, or model-visible artifact.

## Closed Decision schema

The `format` value is one frozen JSON Schema `oneOf` matching the existing Phase 0 records:

- `ASK`: exactly `kind=ASK` and a non-empty unique ordered `semantic_slot_links` string array;
- `EXECUTE`: exactly `kind=EXECUTE`, `action_id`, and ordered `executor_resolutions`, where each resolution has a slot link and typed `{type,value}`;
- hard-unsat `REJECT`: exactly `kind=REJECT`, `reason=HARD_UNSAT`, ordered `executor_resolutions`, and a clause-conflict, empty-domain, or cross-constraint witness;
- no-authorized-action `REJECT`: exactly `kind=REJECT`, `reason=NO_AUTHORIZED_ACTION`, ordered `executor_resolutions`, and a no-authorized-action witness.

The shared definitions are exact:

```text
TypedValue = {type: non-empty string, value: non-empty string}
Resolution = {semantic_slot_link: non-empty string, value: TypedValue}
ClauseConflictWitness = {kind: ClauseConflictWitness, clause_links: unique string array}
EmptyDomainWitness = {kind: EmptyDomainWitness, semantic_slot_link: non-empty string, excluding_constraint_links: unique string array}
CrossConstraintWitness = {kind: CrossConstraintWitness, cross_constraint_links: unique string array}
ExcludedAction = {action_id: non-empty string, unauthorized_managed_effects: unique string array}
NoAuthorizedActionWitness = {kind: NoAuthorizedActionWitness, excluded_actions: [ExcludedAction, ...]}
```

Every object has `additionalProperties=false`; all fields for its variant are required, every declared string is non-empty, and arrays preserve order. Do not constrain the schema to F2, `ASK`, or the expected slot link. Serialize the same schema into the system message and pass the same object as Ollama `format`.

## Exact request protocol

Send exactly two sequential `POST /api/chat` calls in order `A`, then `B`, through a Python standard-library HTTP client with proxies disabled. The exact URL is `http://127.0.0.1:11434/api/chat`; redirects and non-local destinations are forbidden. Each request has only `Content-Type: application/json` and this body shape:

```text
model = qwen3:14b
messages = [shared system message, encoding-specific user message]
format = frozen closed Decision JSON Schema
stream = false
think = false
keep_alive = 0
options = {temperature: 0, seed: 0, num_predict: 256}
```

Use a 600-second timeout and a 1 MiB response-body limit. Do not send tools, images, history, authentication, proxy data, fixture expected values, or other options. Do not use `/api/generate`, the OpenAI-compatible endpoint, cloud routing, or environment-selected base URLs.

Before the first request, `record` must verify: exact clean Git HEAD/source commit, accepted handoff blob, normalized absent output root, Ollama version, exact current Modelfile checksum and `FROM` blob, actual blob size/checksum, and that no proxy or alternate host can affect transport. Complete every preflight before creating the output root.

A valid service envelope has exactly one assistant message, `done=true`, no tool calls or images, empty/absent thinking, non-empty string content, and model identity `qwen3:14b`. Preserve the complete returned JSON object. Timestamps, durations, and token counts are observational fields, not comparison metrics.

## Evidence package and CLI

The CLI supports only:

```text
record --source-commit <40 lowercase hex> --handoff-blob <40 lowercase hex> --output-root <path>
verify --source-commit <40 lowercase hex> --handoff-blob <40 lowercase hex> --output-root <path>
```

The normalized root is exactly:

```text
Phase0/evidence/E5_<source-commit>_qwen3_14b
```

After both completed service responses, `record` atomically creates exactly:

```text
manifest.json
requests.json
responses.json
summary.json
```

`manifest.json` binds schema version, implementation commit, handoff path/blob, runner, F2 fixture path/case, localhost endpoint, Ollama version, tag/list ID, blob path/bytes/SHA-256, Modelfile SHA-256, full request options, output root, and ordered request IDs `[A__F2__unresolved, B__F2__unresolved]`.

`requests.json` is the canonical byte serialization of the two exact model-visible requests. `responses.json` preserves the two complete service JSON responses plus separately parsed content or a stable parse/schema error. `summary.json` contains only source/model/request identity, per-request `EXACT_MATCH|INVALID_OUTPUT|DECISION_MISMATCH`, A/B parsed-decision parity, aggregate `PASS|FAIL`, and a reminder that the outcome is non-blocking and non-scientific. It contains no score or recommendation.

`record` returns success after a complete truthful package is written, even when `summary.status=FAIL`; preflight or infrastructure failure returns nonzero and writes no root. `verify` is offline: it makes zero HTTP/model calls, rebuilds the fixed requests, checks the exact four-file allowlist and manifest/request bytes, validates both preserved response envelopes and contents, and recomputes the summary. It does not require current HEAD to equal the recorded implementation commit because the evidence commit is its descendant.

No separate response-file checksums are maintained after the package is committed; Git binds those files. The external model blob remains bound by its path, size, and checksum in the manifest.

## Implementation verification

`test_e5_local_smoke.py` must establish:

1. A/B typed surfaces both equal the frozen F2 canonical value, while their JSON projections differ and contain no expected output;
2. messages differ only in encoding/serialization and contain modality, support, source role, both OPEN owners, constraints, and the full closed Decision schema;
3. exact request order/body/options, localhost-only proxy-disabled transport, two-call ceiling, timeout, response bound, and no retry/fallback/model switch;
4. model/Modelfile/blob/source/handoff/output-root preflight rejects every mismatch before any HTTP inference or output-root creation;
5. complete exact, invalid JSON, schema-invalid, decision-mismatch, and A/B-parity cases produce the frozen summary without hiding raw responses;
6. HTTP/transport or invalid service-envelope failures stop without evidence, and `record` never converts them into LM `FAIL`;
7. exact four-file atomic non-overwrite writer and offline verifier reject missing, extra, or tampered evidence while making zero HTTP calls;
8. E0-E4 paths are unchanged and fixture expected values are read only after both actual responses are complete.

Run exactly:

```sh
python -B -m unittest Phase0.tests.test_e0_dialect_and_fixtures Phase0.tests.test_e1_elaboration_and_runtime Phase0.tests.test_e2_typed_paths Phase0.tests.test_e3_content_bridge Phase0.tests.test_e4_trace_and_closure Phase0.tests.test_e5_local_smoke
ruff check --no-cache Phase0/run_e5_smoke.py Phase0/tests/test_e5_local_smoke.py
git diff --check
```

The implementation executor returns exact binding and paths, test counts/results, confirmation of zero real model calls/evidence/staging/commit, expected-data isolation, and any concrete complexity or interface risk.

## Review and acceptance

The implementation reviewer checks the exact two-file scope, fixed messages/schema, expected-data direction, two-call/no-retry bound, local-only transport, model/source/handoff provenance, complete response preservation, truthful PASS/FAIL semantics, offline verification, and KISS. `ACCEPT` authorizes only the one recorded smoke run.

The final evidence reviewer receives the exact implementation/evidence ranges, handoff blob, model binding, recorded command, and committed four-file root. It must not call the model. It reruns offline `verify`, inspects both requests/responses and the summary, confirms the Phase 0 conclusion is unchanged, and returns an evidence-integrity verdict separately from the recorded LM smoke status.

Only main accepts E5. No successor handoff, extra model, prompt repair, rerun, or Phase 1 experiment is authorized by either outcome.
