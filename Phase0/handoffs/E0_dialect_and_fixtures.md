# E0 handoff — dialect and fixtures

- Status: `READY_TO_BIND`
- Classification: blocking
- Predecessor: none

## Objective and non-goals

Materialize the frozen finite types, `DialectManifest`, predicate scopes and interpretations, managed-effect universe, candidate trajectories, F1-F9 fixture inputs, and expected test-only values.

E0 does not implement an elaborator, runtime, adapters, extractor, bridge, tracing, runner, LM integration, or any behavior outside the frozen Phase 0 micro-world.

## Start conditions

Main must bind this exact handoff blob to an exact source commit on the clean milestone branch and repeat the exact allowed paths and verification command below. Missing binding data means no mutation. Any conflict with the [engineering plan](../IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md) blocks work and returns to main.

## Allowed mutation paths

```text
Phase0/__init__.py
Phase0/implementation/__init__.py
Phase0/implementation/schema.py
Phase0/implementation/dialect.py
Phase0/implementation/fixture_loader.py
Phase0/fixtures/F1_OPEN_UU_COUPLED_MIN_ASK.json
Phase0/fixtures/F2_OPEN_UE_OWNER_BOUNDARY.json
Phase0/fixtures/F3_EXECUTOR_COVERAGE_NONVACUOUS.json
Phase0/fixtures/F4_EXECUTOR_JOINT_TRACE.json
Phase0/fixtures/F5_AUTHORITY_ROLE_COUNTERFACTUAL.json
Phase0/fixtures/F6_HARD_UNSAT_WITNESS.json
Phase0/fixtures/F7_NO_AUTHORIZED_ACTION_WITNESS.json
Phase0/fixtures/F8_NO_SILENT_INVALID_EXECUTION.json
Phase0/fixtures/F9_C_NORMAL_END_TO_END_EXACT.json
Phase0/tests/__init__.py
Phase0/tests/test_e0_dialect_and_fixtures.py
```

Every other path is forbidden. In particular, the executor may not edit plans, handoffs, reviews, predecessors, or add unlisted files; implement elaboration/runtime; add hidden fallback/default/retry logic; or expose expected fixture values through normal schema, dialect, or loader interfaces.

## Frozen inputs and interfaces

- Engineering-plan sections 3-6 define the surface boundaries, finite semantics, OPEN rules, and exact F1-F9 catalog.
- Finite declared domains are nonempty; each scenario has at most two unresolved OPEN slots.
- Normative authority is `USER | NONE`; OPEN ownership is `USER | EXECUTOR`.
- Predicate scopes are exactly `INITIAL | FINAL | TRACE | EVENT` and interpretations are deterministic.
- Candidate trajectories, ordered effects, managed-effect membership, tie-break inputs, F9 source/refs/expected values, and malformed/empty/cross-empty route cases are fixture data frozen by E0.
- Expected decisions, witnesses, and F9 expected canonical/result values are test-only data and must not be callable from normal production interfaces.

## Required implementation, tests, and artifacts

- Define explicit, finite schema data models and deterministic canonical ordering.
- Implement a versioned `DialectManifest`, computable predicate interpretations, managed-effect universe, and runtime-only candidate trajectory catalog.
- Implement strict JSON/schema fixture loading that fails early on malformed declarations.
- Encode exactly F1-F9 with exact IDs, including F9 source spans, normal and Gold refs, trajectory, exact decision/result, and distractor-invariance inputs.
- Test nonempty finite domains, the two-slot bound, scopes/signatures/interpretations, deterministic trajectories/effects, unique malformed versus static-empty versus cross-empty routes, and test-only expected-value separation.

The returned artifacts are the allowed source/fixture/test files and the complete verification result. E0 creates no recorded experiment output.

## Verification

Run exactly:

```sh
python -m unittest Phase0.tests.test_e0_dialect_and_fixtures
```

## Executor return format

Return:

1. bound source commit, handoff path, and handoff blob SHA;
2. exact changed paths;
3. concise schema/dialect/fixture summary;
4. verification command, exit status, and test count;
5. confirmation that no other path changed and no commit was created;
6. residual risks or `none`.

## Independent reviewer checklist and verdict

The reviewer checks JSON/schema loading; exact F1-F9 IDs; finite nonempty declared domains; the at-most-two unresolved-slot bound; scope/signature/interpretation completeness; trajectory/effect determinism; all three invalid/empty routes; exact F9 source/ref/expected values; and the absence of test-only expected mappings from normal interfaces and dependency paths.

Verdict format:

```text
VERDICT: ACCEPT | REJECT
REVIEWED_COMMIT_OR_RANGE: <exact SHA or range>
HANDOFF_BLOB_SHA: <exact SHA>
VERIFICATION: <commands and results>
FINDINGS: <none or numbered findings>
REQUIRED_REPAIR: <none or exact requirements>
```

## Commit, repair, and acceptance gate

The writer does not commit. Main freezes the diff in a sequential E0 commit, then dispatches an independent read-only review of that exact commit. Rejection requires a separate repair commit and fresh review. Only main may mark the exact reviewed commit/range accepted; only then may main generate the E1 handoff from the accepted E0 interfaces and artifacts. E1 cannot be bound before that new handoff is committed and explicitly dispatched.
