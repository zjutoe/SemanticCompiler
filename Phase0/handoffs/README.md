# Phase 0 handoff index

Concrete handoffs are generated one stage at a time. Only the next executable stage may have a checked-in dispatch template. Their common implementation layout is intentionally self-contained and Python-standard-library-first:

```text
Phase0/implementation/
Phase0/fixtures/
Phase0/tests/
Phase0/run_phase0.py
```

## Status model

| Status | Meaning |
|---|---|
| `READY_TO_BIND` | Checked-in template is complete but grants no mutation authority by itself |
| `BOUND` | Main has issued a binding packet for the exact source commit and template blob SHA; the single writer may mutate only the bound paths |
| `IN_REVIEW` | Main froze the writer's diff in a commit and an independent reviewer is evaluating that exact commit/range read-only |
| `ACCEPTED` | Main accepted the exact reviewed commit/range after a passing independent review |
| `REJECTED` | Review or main rejected the frozen change; any repair must be a separate commit and receive a fresh review |

When a current stage template exists, it is `READY_TO_BIND` only after its independent contract-acceptance gate. Actual dispatch changes operational state through a main-thread message; the template itself is not edited. The binding message must contain the stage ID, exact source commit, handoff path, handoff blob SHA, predecessor accepted commit/range, exact allowed mutation paths, exact verification commands, and exact output roots. If any binding field is absent, there is no mutation authority. Historical accepted handoffs remain committed for provenance but are not current templates and grant no new authority. If no current template is listed below, no stage may be dispatched.

## Progressive generation rule

- Do not create concrete E1-E5 handoff files while E0 is unaccepted. The same rule applies recursively at every later stage.
- Generate the successor handoff only after the predecessor's exact commit/range and all repairs are independently accepted.
- Base the successor on actual accepted interfaces, fixtures, artifacts, and review findings—not assumptions made before execution.
- If a stage exposes an unexpected contract or scope issue, stop and repair/review the governing plan first. A stale or prewritten future handoff must not be used.
- Optional E5 receives a handoff only after accepted E4 and explicit user authorization for its model, network, budget, cost, and side effects.

## Common execution and review rules

- The [engineering plan](../IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md) outranks a bound handoff, and a bound handoff outranks implementation. Any conflict blocks and returns to main; an executor never patches the plan or handoff.
- Only one writer mutation lease exists. The executor does not commit; main freezes the returned diff.
- A stage may touch only its exact allowed paths. It may not edit predecessors, broaden scope, add unlisted files, use hidden fallback/default/retry behavior, or introduce Gold/expected mappings into normal dependencies.
- Verification uses Python standard-library `unittest` unless main first accepts a separate contract repair that explicitly introduces another dependency.
- An independent reviewer receives the exact handoff/blob SHA, reviewed commit/range, verification results, and relevant artifacts. The reviewer remains read-only and returns the handoff's verdict format.
- Rejection requires a separate repair commit and fresh review. Acceptance applies only to the exact reviewed commit/range.

## Current executable handoff

[E5 — local `qwen3:14b` LM-interface smoke](E5_local_qwen3_14b_smoke.md) is contract-accepted at `5c5894a` with handoff blob `ca8daecea42dcaf28c9d1de5cfc6a4988013be10`; see [`E5_5c5894a_review.md`](../reviews/E5_5c5894a_review.md). It is `READY_TO_BIND` and still requires a main-thread binding packet; this template alone grants no mutation or inference authority.

## Accepted predecessor handoffs

- [E0 — dialect and fixtures](E0_dialect_and_fixtures.md), implementation accepted at `70de224`; see [`E0_70de224_review.md`](../reviews/E0_70de224_review.md).
- [E1 — shared semantics, elaborator, and runtime](E1_shared_semantics_elaborator_runtime.md), implementation accepted at `086f9da`; see [`E1_086f9da_review.md`](../reviews/E1_086f9da_review.md).
- [E2 — fixture-direct typed A/B paths](E2_typed_a_b_paths.md), implementation accepted at `bb85d23`; see [`E2_bb85d23_review.md`](../reviews/E2_bb85d23_review.md).
- [E3 — normal C extraction and real bridge path](E3_c_real_bridge_path.md), implementation accepted at `fb4be7c`; see [`E3_fb4be7c_review.md`](../reviews/E3_fb4be7c_review.md).
- [E4 — bounded trace and end-to-end closure](E4_trace_and_end_to_end_closure.md), implementation and evidence accepted at `20411e9`; see [`E4_20411e9_review.md`](../reviews/E4_20411e9_review.md).

## Non-binding dependency roadmap

These entries name expected successors but are not handoffs and grant no mutation authority:

| Stage | Coarse objective | When its handoff may be generated |
|---|---|---|
| E3 | Normal C extractor and real bridge path | Accepted at `fb4be7c` |
| E4 | Bounded tracing and end-to-end closure | Accepted at `20411e9`; Phase 0 blocking sequence complete |
| E5 | Optional frozen-LM interface smoke | Contract accepted at `5c5894a`; implementation is next and model inference remains unauthorized |
