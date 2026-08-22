# E0 handoff — dialect and fixtures

- Status: `READY_TO_BIND`
- Classification: blocking
- Governing plan: [`IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md`](../IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md), including the boundary clarification frozen by `9115cef916c1d62b74ff23321e6cb57ad754967c`
- Predecessor: none

This handoff supersedes the pre-plan-revision template blob `f1f2d02ff717fd08fd7f0fcbb50e7bb403367269`. That blob must never be bound or dispatched.

## Objective and non-goals

Materialize one explicit finite schema, the versioned `DialectManifest`, predicate scopes and interpretations, the managed-effect universe, the runtime-only candidate trajectories, and the exact F1-F9 fixture inputs and test-only expected values frozen below.

E0 creates only the semantic substrate and fixture evidence needed by later stages. It does not implement an elaborator, production runtime, A/B adapters, extractor, `beta_C`, tracing, runner, learned or prompted compiler, LM integration, or behavior outside the frozen Phase 0 micro-world. It does not add F10, optional modality-coverage fixtures, a general constraint DSL, dynamic domains, a planner, or reusable solver infrastructure.

Cross-slot relations are exactly the finite, fixture-local tables below. They must remain joint relations and may not be rewritten as independent per-slot choices.

## Start conditions and binding packet

Main must dispatch a binding packet containing all of the following:

1. stage ID `E0`;
2. exact source commit on the clean `milestone/phase0-engineering-exploration` branch;
3. this exact handoff path and its post-review Git blob SHA;
4. predecessor `none`;
5. the exact allowed mutation paths below;
6. the exact verification command below;
7. output roots `none` because E0 creates no experiment or run output.

Missing or inconsistent binding data means no mutation authority. A branch name by itself is not a binding. Any conflict with the governing plan blocks work and returns to main; the executor must not repair or reinterpret the plan or handoff.

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

Every other path is forbidden. In particular, the executor may not edit plans, handoffs, reviews, predecessors, or add files; implement production elaboration/runtime/adapter/bridge behavior; add hidden fallback/default/retry logic; generate experiment output; or expose test-only expected values through normal schema, dialect, or loader interfaces.

## Frozen representation and isolation contract

### Versions and strict JSON envelope

- Fixture schema version: `phase0.e0.v1`.
- Dialect version: `contract-ir.phase0.v0`.
- Exactly nine JSON files exist, one for each exact F1-F9 ID in the allowed-path list.
- Every file has exactly the top-level keys `fixture_id`, `schema_version`, `dialect_version`, and `cases`.
- Every case has exactly `case_id`, `entry_stage`, `input`, and `expected`.
- `entry_stage` is exactly one of `CANONICAL`, `SOURCE`, `EXTRACTIVE_CONTENT`, or `ADAPTER`.
- Every `input` has exactly `source_envelope`, `entry_payload`, `visible_world_context`, `slot_declarations`, `static_constraints`, `cross_constraints`, and `candidate_trajectory_ids`; unused fields are `null` or `[]`, never omitted.
- Every test-only `expected` has exactly `canonical_state`, `elaboration`, `legal_joint_completions`, `decision`, `result`, `failure`, and `dependency_assertions`; unused fields are `null` or `[]`, never omitted.
- Undeclared keys, duplicate IDs, duplicate refs, unknown enum values, and wrong JSON shapes fail loudly. No coercion or defaults are allowed.

`schema.py` defines the finite normal input types. `fixture_loader.py` exposes only `load_fixture_inputs(path) -> tuple[FixtureInput, ...]`; returned values contain `fixture_id`, `case_id`, `entry_stage`, and validated `input`, but never `expected`. The loader may require the `expected` key to exist, but it must not parse it into a production type, return it, or provide any expected lookup API.

The test module raw-reads `expected` through a private test helper, validates its exact shape, and compares it with normal input and the test-local oracle. No module under `Phase0/implementation/` may import `Phase0.tests`, open an expected subtree, branch behavior on a fixture ID, or use a fixture/scenario ID to retrieve expected decisions, witnesses, canonical states, or results. A fixture ID may be retained only as provenance on loaded input.

### Finite enums and dialect

The following declaration order is normative:

| Type | Values in declaration order |
|---|---|
| `SourceRole` | `USER`, `ASSISTANT`, `TOOL` |
| `NormativeAuthority` | `USER`, `NONE` |
| `OpenOwner` | `USER`, `EXECUTOR` |
| `Modality` | `GOAL`, `REQUIRE`, `PRESERVE`, `FORBID`, `ALLOW` |
| `PredicateScope` | `INITIAL`, `FINAL`, `TRACE`, `EVENT` |
| `ContextAvailability` | `STATIC`, `INITIAL` |
| `OutputFormat` | `UNSET`, `JSON`, `YAML` |
| `Strictness` | `STRICT`, `LENIENT` |
| `ErrorPolicy` | `RETURN_NONE`, `RAISE` |
| `LogMode` | `QUIET`, `VERBOSE` |
| `ServiceMode` | `SAFE`, `FAST` |
| `Backend` | `LOCAL`, `REMOTE` |

`PredicateScope` and `ContextAvailability` are distinct types and must never be interchanged. OPEN schema domains may be strict nonempty subsets of a declared enum; `UNSET` is world state for F1/F4/F5/F6/F7/F9 and is never an admissible OPEN value.

The exact `DialectManifest` is:

| Predicate | Typed signature | Scope | Computable interpretation |
|---|---|---|---|
| `world.final_format_is` | `(OutputFormat) -> bool` | `FINAL` | final observable `format` equals the argument |
| `world.output_policy_is` | `(OutputFormat, Strictness) -> bool` | `FINAL` | final observables `format` and `strictness` equal both arguments |
| `world.error_handling_is` | `(ErrorPolicy, LogMode) -> bool` | `FINAL` | final observables `error_policy` and `log_mode` equal both arguments |
| `world.service_route_is` | `(ServiceMode, Backend) -> bool` | `FINAL` | final observables `service_mode` and `backend` equal both arguments |
| `world.format_supported` | `(OutputFormat) -> bool` | `INITIAL` | initial observable mapping `format_supported[argument]` is `true` |
| `effect.WRITE_OUTPUT` | `() -> bool` | `EVENT` | one emitted event matches the exact effect ID `WRITE_OUTPUT` |

The managed-effect universe is exactly `[WRITE_OUTPUT]`. All other fixture trajectories emit no effects. `GOAL`, `REQUIRE`, `PRESERVE`, `FORBID`, and `ALLOW` retain the governing-plan semantics; E0 adds no fixture solely to broaden modality coverage.

### Canonical ordering, links, and tie-break inputs

- Source spans retain declared source order.
- Normative candidates order by earliest `proposition_support` source position; ties order by `(modality, predicate, typed args)` using ascending ASCII IDs.
- Knowledge assertions use the same support-first rule. Every E0 fixture has `knowledge_assertions=[]`.
- OPEN slots order by canonical candidate order, then `argument_position`.
- Clause links are `clause:<fixture_id>:<case_id>:<three-digit-candidate-index>`.
- Slot links are `slot:<fixture_id>:<case_id>:<three-digit-candidate-index>:arg<argument_position>`.
- Constraint links, action IDs, and effect IDs order by ascending ASCII ID unless an ordered trajectory effect list is being preserved.
- Enum-domain and joint-assignment enumeration uses the declaration order above after slots are put in canonical slot-link order.
- A witness first minimizes cardinality and then uses the lexicographically smallest tuple of canonical links.
- Minimum-sufficient ASK first minimizes queried USER-slot count and then uses canonical slot-link order.
- After validity, authorization, and executor coverage, action tie-break is ascending `action_id`; remaining executor-assignment ties use canonical slot order and enum declaration order.

The short names `C0`, `C1`, `S0`, and `S1` below are explanatory aliases for the full generated links. JSON expected values must store the full links, not the aliases.

## Frozen fixture manifest

Unless a case says otherwise, both support fields of each normative candidate equal the listed source ref, all listed sources are present, `visible_world_context` is empty, trajectory `initial_observables={}`, ordered effects are `[]`, and no result is frozen before E4. A canonical input candidate never stores derived `authority` or `active`; wording such as USER-supported below means its support is expected to derive those values only during later elaboration. Each trajectory record contains exact `trajectory_id`, `action_id`, slot assignment, initial observables, final observables, and ordered effects.

### F1 `OPEN_UU_COUPLED_MIN_ASK`

One case `unresolved` with USER span `u1 = "Require a supported output policy."` and one USER-supported `REQUIRE world.output_policy_is(S0, S1)` candidate. `S0` is `OutputFormat`/USER with schema domain `[JSON,YAML]`; `S1` is `Strictness`/USER with `[STRICT,LENIENT]`.

The sole cross constraint is `constraint:f1:output_policy_pairs` with allowed pairs `[(JSON,STRICT),(YAML,LENIENT)]`. Exact trajectories are:

- `tau:f1:json_strict`, action `f1_render_json_strict`, assignment `(JSON,STRICT)`, initial `{format:UNSET}`, final `{format:JSON,strictness:STRICT}`;
- `tau:f1:yaml_lenient`, action `f1_render_yaml_lenient`, assignment `(YAML,LENIENT)`, initial `{format:UNSET}`, final `{format:YAML,strictness:LENIENT}`.

Expected legal joint completions are those two pairs in that order. Expected decision is `ASK([S0])`; querying both slots, querying `S1`, an empty ASK, or any common EXECUTE is wrong.

### F2 `OPEN_UE_OWNER_BOUNDARY`

USER span `u1 = "Require a supported error-handling policy."` supports one `REQUIRE world.error_handling_is(S0, S1)` candidate. `S0` is `ErrorPolicy`/USER with `[RETURN_NONE,RAISE]`; `S1` is `LogMode`/EXECUTOR with `[QUIET,VERBOSE]`. Cross constraint `constraint:f2:error_log_pairs` allows exactly `[(RETURN_NONE,QUIET),(RAISE,VERBOSE)]`.

Trajectories are `tau:f2:return_none_quiet` / action `f2_return_none_quiet` with final `{error_policy:RETURN_NONE,log_mode:QUIET}`, and `tau:f2:raise_verbose` / action `f2_raise_verbose` with final `{error_policy:RAISE,log_mode:VERBOSE}`.

Cases:

- `unresolved`: expected completions are both pairs and decision is `ASK([S0])`; neither executor value has USER coverage.
- `resolved_return_none`: inject USER answer `RETURN_NONE`; expected decision is `EXECUTE(f2_return_none_quiet)` with exactly one preceding executor resolution `(S1,QUIET)`.

### F3 `EXECUTOR_COVERAGE_NONVACUOUS`

Case `unresolved` has USER span `u1 = "Require a supported service route."` and one USER-supported `REQUIRE world.service_route_is(S0, S1)` candidate. `S0` is `ServiceMode`/USER `[SAFE,FAST]`; `S1` is `Backend`/EXECUTOR `[LOCAL,REMOTE]`. Constraint `constraint:f3:service_backend_pairs` allows `[(SAFE,LOCAL),(FAST,LOCAL),(FAST,REMOTE)]`.

Trajectories are:

- `tau:f3:safe_local`, action `f3_use_local`, assignment `(SAFE,LOCAL)`, final `{service_mode:SAFE,backend:LOCAL}`;
- `tau:f3:fast_local`, action `f3_use_local`, assignment `(FAST,LOCAL)`, final `{service_mode:FAST,backend:LOCAL}`;
- `tau:f3:fast_remote`, action `f3_use_remote`, assignment `(FAST,REMOTE)`, final `{service_mode:FAST,backend:REMOTE}`.

Expected decision is `EXECUTE(f3_use_local)` with exactly `(S1,LOCAL)` recorded before the action. `REMOTE`, an empty/narrow fiber, ASK, or vacuous success is wrong.

### F4 `EXECUTOR_JOINT_TRACE`

Case `unresolved` has USER spans `u1 = "Require an executor-selected output policy."` and `u2 = "Require final format JSON."`. Candidate `C0` is USER-supported `REQUIRE world.output_policy_is(S0, S1)` with two EXECUTOR slots: `S0` is `OutputFormat [JSON,YAML]`, `S1` is `Strictness [STRICT,LENIENT]`. Candidate `C1` is USER-supported `REQUIRE world.final_format_is(JSON)`.

Constraint `constraint:f4:output_policy_pairs` allows `[(JSON,STRICT),(YAML,LENIENT)]`. `tau:f4:yaml_lenient` / action `f4_a_yaml_lenient` produces `{format:YAML,strictness:LENIENT}`; `tau:f4:json_strict` / action `f4_b_json_strict` produces `{format:JSON,strictness:STRICT}`. Only the latter is hard-valid because of `C1`.

Expected decision is `EXECUTE(f4_b_json_strict)` with executor resolutions `[(S0,JSON),(S1,STRICT)]` in that order before the action. Greedy per-slot resolution or omitting either resolution is wrong.

### F5 `AUTHORITY_ROLE_COUNTERFACTUAL`

All cases use trajectories `tau:f5:yaml` / action `f5_a_yaml` with initial `{format:UNSET}` and final `{format:YAML}`, and `tau:f5:json` / action `f5_b_json` with initial `{format:UNSET}` and final `{format:JSON}`.

Cases:

- `user_fixed`: USER `u1 = "Require final format JSON."`; `REQUIRE world.final_format_is(JSON)` derives `authority=USER`, is active, and yields `EXECUTE(f5_b_json)`.
- `assistant_fixed`: ASSISTANT `a1` with the same text; the candidate derives `authority=NONE`, is inactive, and the frozen action tie-break yields `EXECUTE(f5_a_yaml)`.
- `tool_fixed`: TOOL `t1` with the same text; the candidate derives `authority=NONE`, is inactive, and yields `EXECUTE(f5_a_yaml)`.
- `user_executor_open`: USER `u1 = "Require an executor-selected final format."`; candidate `REQUIRE world.final_format_is(S0)` derives `authority=USER`; `S0` is EXECUTOR-owned `OutputFormat [JSON,YAML]`. Both values are legal, and action tie-break yields `EXECUTE(f5_a_yaml)` with preceding resolution `(S0,YAML)`. The resolution does not create or change authority.

### F6 `HARD_UNSAT_WITNESS`

Cases:

- `clause_conflict`: USER `u1 = "Require final format JSON."` and `u2 = "Require final format YAML."` support candidates `C0` and `C1`, both expected to become active. `tau:f6:json` / `f6_render_json` ends in JSON; `tau:f6:yaml` / `f6_render_yaml` ends in YAML. Legal completion is `[{}]`; no action satisfies both clauses. Expected decision is `REJECT(HARD_UNSAT, ClauseConflictWitness([C0,C1]), executor_resolutions=[])`.
- `static_empty`: one USER-supported `REQUIRE world.final_format_is(S0)` with USER-owned `OutputFormat [JSON,YAML]`. `VisibleWorldContext.observable_values` contains exactly `world.format_supported(JSON)=false` and `world.format_supported(YAML)=false`, both with `ContextAvailability.STATIC`. Valid constraints `constraint:f6:format_not_json` and `constraint:f6:format_not_yaml` exclude JSON and YAML respectively. Expected legal completions are `[]` and decision is `REJECT(HARD_UNSAT, EmptyDomainWitness(S0,[constraint:f6:format_not_json,constraint:f6:format_not_yaml]), executor_resolutions=[])`.
- `cross_empty`: one USER-supported `REQUIRE world.output_policy_is(S0,S1)` with USER-owned `OutputFormat [JSON,YAML]` and `Strictness [STRICT,LENIENT]`; individual domains remain nonempty. Valid constraint `constraint:f6:no_output_policy_pair` has `allowed_pairs=[]`. Expected legal completions are `[]` and decision is `REJECT(HARD_UNSAT, CrossConstraintWitness([constraint:f6:no_output_policy_pair]), executor_resolutions=[])`.

The three cases are mutually exclusive routes. They must not be converted into one another, ASK, action tie-break, default recovery, or `NO_AUTHORIZED_ACTION`.

### F7 `NO_AUTHORIZED_ACTION_WITNESS`

Case `missing_allow` has USER `u1 = "Require final format JSON."` supporting one `REQUIRE world.final_format_is(JSON)` candidate expected to become active, and no `ALLOW` candidate. `tau:f7:write_json` / action `f7_write_json` moves `{format:UNSET}` to `{format:JSON}` and emits `[WRITE_OUTPUT]`.

The sole legal completion is `[{}]`; the trajectory is hard-valid but unauthorized. Expected decision is `REJECT(NO_AUTHORIZED_ACTION, NoAuthorizedActionWitness([{action_id:f7_write_json,unauthorized_managed_effects:[WRITE_OUTPUT]}]), executor_resolutions=[])`.

### F8 `NO_SILENT_INVALID_EXECUTION`

Cases and stable expected failures:

| Case | Frozen defect | Expected future stage/code | E0 check |
|---|---|---|---|
| `dangling_support` | canonical candidate references absent `missing_ref` | `elaboration/DANGLING_SUPPORT_REF` | valid JSON loads; test records the exact failure oracle |
| `wrong_enum_type` | `world.final_format_is` receives typed `Strictness.STRICT` | `elaboration/TYPE_MISMATCH` | valid JSON loads; test records the exact failure oracle |
| `missing_adapter_link` | `ADAPTER` payload has required `adapter_link=null` | `adapter_or_bridge/MISSING_ADAPTER_LINK` | valid JSON loads; no adapter is implemented |
| `malformed_domain` | `schema_domain="JSON,YAML"` instead of an array | `elaboration/MALFORMED_DOMAIN_DECLARATION` | loader raises the exact structured stage/code without producing normal input |
| `declared_empty_domain` | structurally valid `schema_domain=[]` | `elaboration/DECLARED_EMPTY_DOMAIN` | loader raises the exact structured stage/code without producing normal input |

All five expected decisions and results are `null`; expected `failure` is non-null. The domain errors use a typed `FixtureInputError` carrying the frozen future pipeline stage and stable reason code; the error is derived from the invalid input, never read from `expected`. This loader/preflight validation is not a production elaborator. The other three cases load as invalid semantic/adapter inputs for later-stage checks. No case may become an empty Contract, default value, retry, ASK, EXECUTE, or runtime REJECT.

### F9 `C_NORMAL_END_TO_END_EXACT`

The source envelope always has exact source order: USER `u1 = "Require final format JSON."`; USER `u2 = "Allow managed effect WRITE_OUTPUT."`; and third span `a1`. The sole trajectory is exact `tau:f9:write_json` / action `write_json`, initial `{format:UNSET}`, final `{format:JSON}`, ordered effects `[WRITE_OUTPUT]`. The managed-effect universe remains `[WRITE_OUTPUT]`.

Cases:

- `normal`: `a1 = "Use YAML."` from ASSISTANT; `entry_stage=SOURCE`; expected normal extractor refs are `[u1,u2,a1]`. Exact canonical candidates in order are USER `REQUIRE world.final_format_is(JSON)` with both supports `[u1]`, USER `ALLOW effect.WRITE_OUTPUT()` with both supports `[u2]`, and ASSISTANT `REQUIRE world.final_format_is(YAML)` with both supports `[a1]`; `knowledge_assertions=[]`, `open_slot_mentions=[]`.
- `gold_c_original`: same envelope, `entry_stage=EXTRACTIVE_CONTENT`, exact refs `[u1,u2]`, and `ReferencedSupportView` excludes `a1`. Exact canonical state contains only the first two USER candidates.
- `gold_c_distractor_variant`: same as `gold_c_original` except unreferenced `a1 = "Use plain text."`. Its `ReferencedSupportView` and exact canonical state must equal those of `gold_c_original` byte-for-byte after canonical serialization.

For all three cases, expected elaborated authorities are `[USER,USER]` for the two USER candidates; for `normal`, the third authority is `NONE` and that candidate remains present but inactive. The exact elaborated candidate records retain canonical order and links `C0`, `C1`, and, for `normal`, `C2`; their `(authority,active)` values are respectively `(USER,true)`, `(USER,true)`, and `(NONE,false)`. The active Contract contains exactly `C0` and `C1`; elaborated knowledge, OPEN slots, slot domains, and constraints are all `[]`. Exact decision is `EXECUTE(write_json, executor_resolutions=[])`. Exact result is `Result(kind=EXECUTED, action_id=write_json, final_observables={format:JSON}, ordered_effects=[WRITE_OUTPUT])`.

E0 stores and validates these inputs and test-only expected values but does not implement the normal extractor or `beta_C`. Production extractor/bridge dependency paths in E3 may not import the fixture expected helper, scenario IDs, gold canonical states, expected decisions, or expected results.

## Required implementation and E0-only verification semantics

The executor must:

- define explicit finite enums and immutable value models in `schema.py` without third-party dependencies;
- implement the exact versioned manifest, predicate interpretations, managed-effect universe, trajectories, and deterministic ordering in `dialect.py`;
- implement strict normal-input loading and test-only expected isolation exactly as above;
- encode exactly the named files and cases above, with no additional fixtures or cases;
- test exact IDs, shapes, enum/domain bounds, signatures/scopes/interpretations, canonical ordering/links, trajectory values/effects, expected-value isolation, and all exact fixture assertions.

The test module may contain a private, finite, test-only enumeration oracle that expands the frozen slot domains and fixture-local relation tables and compares the result with stored `legal_joint_completions`, expected decisions, and witnesses. This is permitted only to catch internally inconsistent fixture data. It must not be imported by production code, exposed as an E1 runtime API, implement dynamic constraints, or become a scenario-ID lookup that simply returns expected outputs.

E0 does not execute a production pipeline. For F8, it verifies strict loader/preflight behavior and the frozen future-stage failure oracle; for F9, it verifies exact stored source/ref/canonical/elaborated/decision/result values and dependency assertions without implementing extraction, bridge, elaboration, runtime, or execution.

Returned artifacts are only the allowed source, fixture, and test files plus the complete verification result. E0 creates no experiment output.

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

The reviewer checks the binding identity; allowed-path compliance; strict envelope/loading; test-only expected isolation; exact enum and dialect tables; ordering/link/tie-break rules; every named case and exact F1-F9 value; finite fixture-local constraints; trajectory/effect determinism; F6 route separation and witnesses; F8 non-execution behavior; F9 exact normal and Gold-C values; and the absence of production elaborator/runtime/adapter/extractor/bridge code or expected lookup dependencies.

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

The writer does not commit. Main freezes the diff in a sequential E0 commit, then dispatches an independent read-only review of that exact commit. Rejection requires a separate repair commit and fresh review. Only main may mark the exact reviewed commit/range accepted; only then may main create `Phase0/reviews/E0_<short-reviewed-sha>_review.md` and generate the E1 handoff from accepted interfaces, fixtures, artifacts, and findings. E1 cannot be bound before that new handoff is committed, independently reviewed as a contract package where required, and explicitly dispatched.
