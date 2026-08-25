# E4 handoff — bounded trace and end-to-end closure

- Proposed status after contract acceptance: `READY_TO_BIND`
- Classification: blocking and final required Phase 0 stage
- Governing plan: [`IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md`](../IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md)
- Authored against clean source commit: `6bc5c216b4d1436c37c4145ededd8176bfb788f8`
- Accepted predecessor implementation: `fb4be7c36ae3b8175c39364aa446c82f9f2a5d87`
- Accepted predecessor reviewed range: `c3f2c94268c05dae1e57ecc989cdd57836d06fb2..fb4be7c36ae3b8175c39364aa446c82f9f2a5d87`
- Accepted predecessor review: [`E3_fb4be7c_review.md`](../reviews/E3_fb4be7c_review.md)

## Objective and non-goals

Close the deterministic Phase 0 path with one bounded trace schema shared by A, B, C, Gold-C debug, and gold-canonical debug. Produce three small committed evidence packages from a clean reviewed implementation commit, keeping normal, Gold-C debug, and gold-canonical debug artifacts in distinct roots, and prove that every F8 invalid route stops at its exact failure stage without a decision or execution result.

E4 is orchestration and observability over accepted E0-E3 behavior. It must not change or reinterpret any fixture, schema, dialect, adapter, bridge, elaborator, runtime, decision, result, or failure reason.

E4 does not add:

- a generic tracing/telemetry framework, database, event bus, plugin system, artifact service, or arbitrary scenario/config language;
- retries, fallbacks, default insertion, arm switching, failure recovery, or exception masking;
- new fixtures, actions, effects, metrics, statistics, comparisons, thresholds, or scientific claims;
- learned compilation, optional LM integration, E5 code, or any downstream handoff;
- timestamps, random IDs, environment dumps, model outputs, or source-package checksums.

## Two-gate stage workflow

E4 has two sequential gates under this one handoff:

1. **Implementation gate.** A single writer edits only the two implementation paths below, runs the test commands, and returns without committing. Main freezes the diff, then a strict independent reviewer accepts or rejects the exact implementation range.
2. **Recorded closure gate.** Only after implementation review acceptance, main starts from that exact clean implementation commit and binds the derived evidence base root. The runner writes three fixed four-file packages below it. Main freezes those files in a separate evidence commit, then a fresh independent reviewer checks the implementation, committed evidence, reproducibility, F8 fail-stop behavior, and Phase 0 exit checklist.

E4 is not complete after implementation review alone. Any rejected implementation or evidence requires a separate repair commit, a fresh clean run in a new root derived from the repaired implementation SHA, and a new independent review. Reviewed history is never rewritten and superseded evidence is never used in conclusions.

## Implementation binding and mutation lease

Main may dispatch the implementation only after this exact handoff package is independently accepted. The binding packet must include stage `E4`, the exact clean source commit containing the accepted contract review, this path and Git blob SHA, the accepted E3 commit/range above, these two paths, the verification commands, and implementation output roots `none`.

Allowed implementation paths:

```text
Phase0/run_phase0.py
Phase0/tests/test_e4_trace_and_closure.py
```

Every other path is forbidden during implementation. In particular, do not add `tracing.py`, edit E0-E3 code/tests/fixtures, create evidence early, or modify package initializers. If these two files are insufficient, stop and return to main.

## Runner boundary and shared trace schema

`run_phase0.py` is a narrow fixed-matrix harness. It defines one `E4_HANDOFF_BLOB` constant copied from the accepted binding packet; both CLI commands reject any different `--handoff-blob`. This is a Git identity for the reviewed contract, not a parallel source-package checksum. The harness may use fixture `expected` fields only to validate the completed actual path and must keep all such reads inside the harness. Existing normal adapters, bridge, elaborator, runtime, and backend remain expected-blind and unchanged.

Define frozen records equivalent to:

```text
StageTrace:
  stage: surface | adapter_or_bridge | elaboration | runtime | execution
  input_ref: artifact ref
  output_ref: artifact ref | null
  failure_reason: stable reason | null

ScenarioTrace:
  scenario_id: fixed ID
  input_ref: artifact ref
  arm: A | B | C | GOLD_C_DEBUG | GOLD_CANONICAL_DEBUG
  stages: tuple[StageTrace, ...]
  final_outcome: DECISION | SYSTEM_FAILURE
  final_decision: EXECUTE | ASK | REJECT | NOT_PRODUCED
  result_ref: artifact ref | null
  ask_links: tuple[slot link, ...]
  executor_resolutions: tuple[existing AssignmentItem, ...]
  reject_reason: HARD_UNSAT | NO_AUTHORIZED_ACTION | null
  reject_witness_ref: artifact ref | null
```

The harness also exposes a minimal in-memory bundle builder, deterministic evidence writer, committed-evidence verifier, and CLI. Exact private helper names may vary. Do not create a general recorder API or accept arbitrary scenario lists.

Every artifact ref has one entry in its package's `artifacts.json`; refs never cross package roots, and no dangling or duplicate refs are allowed. Artifacts contain bounded JSON projections of actual fixture input/surface, canonical state, elaboration, legal completions/decision, result, failure, or reject witness. Never serialize private runtime support trajectories or arbitrary process/environment state. Raw source text may exist in its referenced input/surface artifact but never inline in `ScenarioTrace`.

For a successful path, append stages in actual pipeline order. `ASK` and `REJECT` end after `runtime`; only `EXECUTE` may append `execution` and have a non-null `result_ref`. On a system failure, the final stage has `output_ref=null` and the exact failure reason, then tracing stops. A system failure always has `NOT_PRODUCED`, no result, no ASK links, no resolutions, no reject metadata, and no later-stage artifact.

Existing exception types and their public `stage/reason` values determine failure location. The harness must not infer a different stage from fixture identity, catch an exception and continue, retry another arm, or turn a failure into an empty state/ordinary decision.

## Exact ten-scenario matrix

Generate exactly these traces. Within each package's `traces.jsonl`, preserve the relative row order shown below:

| # | Package | Scenario ID | Arm | Exact stage tuple | Expected terminal state |
|---|---|---|---|---|---|
| 1 | `normal` | `A__F1__unresolved` | A | `adapter_or_bridge, elaboration, runtime` | `ASK`, exact F1 links |
| 2 | `normal` | `B__F3__unresolved` | B | `adapter_or_bridge, elaboration, runtime` | `EXECUTE`, exact F3 resolution, null result |
| 3 | `normal` | `C__F9__normal` | C | `surface, adapter_or_bridge, elaboration, runtime, execution` | exact F9 `EXECUTE` and result |
| 4 | `gold_c_debug` | `GOLD_C_DEBUG__F9__gold_c_original` | GOLD_C_DEBUG | `adapter_or_bridge, elaboration, runtime, execution` | exact F9 Gold-C `EXECUTE` and result |
| 5 | `gold_canonical_debug` | `GOLD_CANONICAL_DEBUG__F6__clause_conflict` | GOLD_CANONICAL_DEBUG | `elaboration, runtime` | exact `REJECT(HARD_UNSAT)` and witness |
| 6 | `gold_canonical_debug` | `GOLD_CANONICAL_DEBUG__F8__dangling_support` | GOLD_CANONICAL_DEBUG | `elaboration` (failure) | `elaboration/DANGLING_SUPPORT_REF` |
| 7 | `gold_canonical_debug` | `GOLD_CANONICAL_DEBUG__F8__wrong_enum_type` | GOLD_CANONICAL_DEBUG | `elaboration` (failure) | `elaboration/TYPE_MISMATCH` |
| 8 | `normal` | `A__F8__missing_adapter_link` | A | `adapter_or_bridge` (failure) | `adapter_or_bridge/MISSING_ADAPTER_LINK` |
| 9 | `gold_canonical_debug` | `GOLD_CANONICAL_DEBUG__F8__malformed_domain` | GOLD_CANONICAL_DEBUG | `elaboration` (failure) | `elaboration/MALFORMED_DOMAIN_DECLARATION` |
| 10 | `gold_canonical_debug` | `GOLD_CANONICAL_DEBUG__F8__declared_empty_domain` | GOLD_CANONICAL_DEBUG | `elaboration` (failure) | `elaboration/DECLARED_EMPTY_DOMAIN` |

The named package is a fixed enum, not a configurable partitioning facility. `normal` contains rows 1, 2, 3, and 8; `gold_c_debug` contains row 4; `gold_canonical_debug` contains rows 5, 6, 7, 9, and 10. A stage marked `(failure)` has `output_ref=null` and the listed stable reason. F3 ends at `runtime`: its accepted decision is `EXECUTE`, but the backend returns no `Result` because its legal supporting trajectories do not share final observables.

The missing-link probe is labeled A only to remain inside the plan's closed arm enum; its trace must show that dispatch fails before inspecting or accepting the generic fixture surface. It must not call `alpha_A`, construct a replacement Contract surface, or switch to B.

The A and B surfaces are small explicit in-harness fixture-direct records, not generic canonical-to-surface compilers. Their adapter outputs must equal the corresponding accepted F1/F3 canonical fixture inputs before the backend is called. Do not import test-private helpers or duplicate a general reverse adapter.

The matrix is intentionally representative rather than a second copy of all 21 fixture cases. The full E0-E4 unittest command remains the exhaustive blocking-fixture gate.

## Required decisions, artifacts, and invariants

The ten traces have exact aggregate counts:

```text
scenario_count = 10
decision_count = 5
system_failure_count = 5
ASK = 1
EXECUTE = 3
REJECT = 1
executed_result_count = 2
```

Package-local counts are fixed as follows: `normal` has 4 scenarios, 3 decisions, 1 system failure, 1 ASK, 2 EXECUTE, 0 REJECT, and 1 result; `gold_c_debug` has 1 scenario, 1 EXECUTE decision, and 1 result; `gold_canonical_debug` has 5 scenarios, 1 REJECT decision, 4 system failures, and no result. Verification also checks their aggregate against the totals above.

All actual terminal decisions, results, witnesses, and failures must match the frozen fixture expected values before the bundle can be marked passing. Expected values validate outputs only; they cannot construct a normal C canonical value, choose a decision, synthesize a result, route a failure, or populate actual artifacts.

Each trace has at most five stage records. Scenario IDs, stage order, artifact refs, artifact ordering, trace ordering, and JSON serialization are deterministic. No timestamp, UUID, filesystem inode, hostname, absolute workspace path, or dictionary/set iteration order may affect bytes.

Each package summary is an engineering closure record only. It reports that package's fixed local counts, `status=PASS`, ordered scenario IDs, and source commit. `verify` computes and checks the aggregate totals above in memory; it does not add a fourth aggregate package. A summary must not rank arms, compute a score, claim causality, or recommend publication/deployment.

## CLI and three fixed four-file evidence packages

The CLI supports only:

```text
record --source-commit <40 lowercase hex> --handoff-blob <40 lowercase hex> --output-root <path>
verify --source-commit <40 lowercase hex> --handoff-blob <40 lowercase hex> --output-root <path>
```

Both commands require `output-root` to be the normalized repo-relative base path `Phase0/evidence/E4_<source-commit>`; absolute paths and alternate roots are invalid. `record` must fail before writing unless the Git HEAD equals `source-commit`, the worktree/index is clean including untracked paths, the handoff blob argument equals `E4_HANDOFF_BLOB`, and the base root does not exist. It then creates exactly these package roots:

```text
Phase0/evidence/E4_<source-commit>/normal/
Phase0/evidence/E4_<source-commit>/gold_c_debug/
Phase0/evidence/E4_<source-commit>/gold_canonical_debug/
```

Each package root contains exactly `manifest.json`, `artifacts.json`, `traces.jsonl`, and `summary.json`; the base root contains no files or other directories. `verify` requires the same embedded handoff identity, rejects any missing or extra root/file and schema drift, rebuilds the fixed matrix using current versioned code/fixtures, serializes each package canonically, and requires exact byte equality for all twelve files. It does not require current HEAD to equal the recorded source commit because the evidence commit is necessarily a descendant that changes only evidence files.

Each `manifest.json` records exactly the schema version, package name, implementation source commit, accepted handoff path/blob, runner path, applicable fixture paths, exact relative package root, and ordered scenario IDs for that package. Collectively they name the five fixture paths used by the matrix. No parallel source checksum is recorded.

After implementation review acceptance, main binds:

```text
E4_IMPL_SHA=<full accepted implementation SHA>
E4_HANDOFF_BLOB=<accepted E4 handoff blob SHA>
E4_OUTPUT_ROOT=Phase0/evidence/E4_<E4_IMPL_SHA>
```

The exact recorded command is then:

```sh
python -B Phase0/run_phase0.py record --source-commit <E4_IMPL_SHA> --handoff-blob <E4_HANDOFF_BLOB> --output-root Phase0/evidence/E4_<E4_IMPL_SHA>
```

The run must start from the clean implementation commit. Main verifies the fixed three-directory/twelve-file allowlist, runs `verify`, freezes only that derived evidence base root in a new commit, and gives the final reviewer both the implementation and evidence commits. Because accepted evidence becomes Git-versioned, do not maintain parallel checksums for its files.

## Implementation tests and verification

`test_e4_trace_and_closure.py` must establish:

1. exact package membership, per-package trace order, arm labels, frozen stage tuples, package-local and aggregate counts, fixture decision/result/failure parity, F3's runtime-terminal null-result EXECUTE, and F8 stop points;
2. all artifact refs resolve exactly once, no unreferenced large artifact is emitted, trace JSON contains no raw source text, and every trace has at most five stages;
3. ASK/EXECUTE/REJECT/SYSTEM_FAILURE field consistency and result/witness refs;
4. A/B fixture-direct canonical equality, C normal non-gold flow, Gold-C same-bridge flow, and gold-canonical bypass semantics;
5. writer determinism, exact three-root/twelve-file allowlist, non-overwrite behavior, manifest fields, fixed normalized base root and embedded handoff-blob checks, verifier rejection of missing/extra/tampered files, and no timestamps/random IDs/absolute paths;
6. `record` rejects source/HEAD mismatch plus dirty staged, dirty tracked-but-unstaged, and untracked states before creating the base output root;
7. production normal components remain expected-blind and no E0-E3 file changes are required.

Run exactly:

```sh
python -B -m unittest Phase0.tests.test_e0_dialect_and_fixtures Phase0.tests.test_e1_elaboration_and_runtime Phase0.tests.test_e2_typed_paths Phase0.tests.test_e3_content_bridge Phase0.tests.test_e4_trace_and_closure
ruff check --no-cache Phase0/run_phase0.py Phase0/tests/test_e4_trace_and_closure.py
git diff --check
```

The implementation executor returns binding identity, exact paths, summary, all command results/test count, expected-data isolation confirmation, no-commit confirmation, three concise observations about trace readability/duplication/maintenance cost, and residual risks.

## Review and final acceptance

The implementation reviewer checks exact binding/two-path scope, all invariants above, test integrity, expected-data direction, deterministic output, failure-stop behavior, KISS, and absence of E5/general infrastructure. `ACCEPT` authorizes only the recorded closure gate, not E4 final acceptance.

The final evidence reviewer receives the exact implementation commit/range, evidence commit/range, handoff blob, recorded command, committed three-package root, completed tests, and no external artifacts. It reruns `verify` and the full suite; checks trace/artifact/manifest/summary consistency and every Phase 0 exit item; confirms superseded evidence is excluded; and returns:

```text
VERDICT: ACCEPT | REJECT
REVIEWED_COMMIT_OR_RANGE: <exact implementation and evidence ranges>
HANDOFF_BLOB_SHA: <exact SHA>
VERIFICATION: <commands and results>
FINDINGS: <none or numbered findings>
REQUIRED_REPAIR: <none or exact requirements>
```

Only main may accept E4 and Phase 0 engineering closure. E5 remains optional, requires explicit user authorization, and is never generated or run merely because E4 passes.
