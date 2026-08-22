# E1 handoff — shared semantics, elaborator, and runtime

- Status: `READY_TO_BIND`
- Classification: blocking
- Governing plan: [`IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md`](../IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md)
- Authored against clean source commit: `94772b2191b107badf46b84764a22723677d9c67`
- Accepted predecessor implementation: `70de224c6cdc40b8a0f5c2f35fe7d934987a9e31`
- Accepted predecessor review: [`E0_70de224_review.md`](../reviews/E0_70de224_review.md)

## Objective and non-goals

Implement the shared deterministic backend that consumes a `CanonicalSemanticState`, elaborates it against the frozen E0 dialect and visible context, enumerates finite joint completions, applies authority and managed-effect authorization, and returns one closed `EXECUTE | ASK | REJECT` decision. Exercise that backend through the Gold canonical debug path until every E1-owned blocking fixture route closes.

E1 reuses the exact E0 schemas, loader, dialect manifest, trajectories, fixtures, ordering, and expected values already accepted at `70de224c6cdc40b8a0f5c2f35fe7d934987a9e31`. It does not change or reinterpret them.

E1 does not implement or edit:

- A/B surface schemas or `alpha_A` / `alpha_B`;
- the C segmenter, normal extractor, `ReferencedSupportView`, or `beta_C`;
- `SourceEnvelope` or `ExtractiveContentState` entry handling;
- the F8 `missing_adapter_link` route, which first belongs to the E2 adapter boundary;
- the E4 `ScenarioTrace`, artifact store, runner, or recorded output roots;
- learned or prompted compilation, LM integration, retries, defaults, a general constraint DSL, dynamic domains, a planner, or behavior outside the frozen micro-world.

Production code must not read fixture `expected` fields, import tests, accept fixture/case/scenario IDs as semantic inputs, or branch on those IDs. Gold canonical values may be read only by the E1 test harness and passed as ordinary canonical values to the same production backend.

## Start conditions and binding packet

Main may dispatch E1 only after this handoff contract package has been committed and independently accepted. The dispatch must contain all of:

1. stage ID `E1`;
2. exact clean source commit containing the accepted E1 handoff and its accepted review record;
3. this exact handoff path and its Git blob SHA at that source commit;
4. predecessor accepted implementation `70de224c6cdc40b8a0f5c2f35fe7d934987a9e31` and reviewed range `2c41cd10f4b447f1a6ea30b77ae1c52baccf727b..70de224c6cdc40b8a0f5c2f35fe7d934987a9e31`;
5. the exact allowed mutation paths below;
6. the exact verification commands below;
7. output roots `none`, because E1 creates no experiment or recorded-run output.

The authored-against commit binds the accepted E0 interface used to write this handoff; it is not by itself execution authority. A branch name, a draft handoff, or a handoff blob that differs from the dispatched blob grants no mutation authority. If any accepted E0 source, fixture, plan invariant, or handoff contract has changed after this handoff was reviewed, main must reconcile and re-review the E1 handoff before dispatch.

Any contract conflict or required change outside the allowed paths blocks E1 and returns to main. The executor must not patch a predecessor, broaden the mutation lease, or work around the conflict.

## Allowed mutation paths

```text
Phase0/implementation/elaboration.py
Phase0/implementation/runtime.py
Phase0/implementation/backend.py
Phase0/tests/test_e1_elaboration_and_runtime.py
```

Every other path is forbidden. In particular, E1 may not edit `schema.py`, `dialect.py`, `fixture_loader.py`, any F1-F9 JSON file, E0 tests, plans, handoffs, reviews, package `__init__.py` files, or create any additional source, test, configuration, cache, report, or output file. If these four paths are insufficient, stop and return the exact missing contract or path requirement to main.

## Accepted E0 dependencies

E1 must use, without copying or redefining:

- immutable canonical/input records and enum order from `Phase0.implementation.schema`;
- `DIALECT_VERSION`, `PREDICATES`, `PREDICATE_BY_ID`, `MANAGED_EFFECTS`, `OBSERVABLE_TYPES`, `TRAJECTORIES_BY_ID`, `Trajectory`, `AssignmentItem`, `Observable`, and `evaluate_predicate` from `Phase0.implementation.dialect`;
- `load_fixture_inputs` / `load_fixture_input` only from tests to obtain expected-blind fixture input;
- the nine accepted JSON fixtures as immutable input and test-only expectation data.

The production modules may import only Python standard-library modules and other modules under `Phase0.implementation`. They may not open fixture JSON files. E1 tests may privately raw-read the existing `expected` subtrees and decode the F9 gold canonical value, but may not expose an expected lookup through production code.

The frozen enum, slot, clause, constraint, action, effect, and assignment ordering rules in E0 remain authoritative. Dictionary insertion order, set iteration, source filename order, or fixture order must not become a semantic tie-break.

## Production API and immutable result models

The implementation may choose private helper names, but the following public behavior and module ownership are fixed.

### `elaboration.py`

Expose:

```text
ElaborationFailure(stage="elaboration", reason=<stable code>)

elaborate(
    canonical_state,
    source_envelope,
    visible_world_context,
    slot_declarations,
    static_constraints,
    cross_constraints,
) -> ElaboratedSemanticState
```

`ElaborationFailure` is a loud exception with exact public `stage` and `reason` string attributes. `ElaboratedSemanticState` and its nested records are frozen dataclasses and retain enough original canonical data for runtime evaluation. They expose, directly or through unambiguous frozen nested records, all of:

```text
ElaboratedCandidate:
  original NormativeCandidate
  clause_link
  authority: USER | NONE
  active: bool

ElaboratedOpenSlot:
  semantic_slot_link
  type
  owner
  resolved_value

SlotDomain:
  semantic_slot_link
  values in frozen enum declaration order

ElaboratedSemanticState:
  candidates in canonical order
  active_clause_links
  checked knowledge_assertions
  open_slots in canonical slot-link order
  slot_domains in the same order
  accepted static_constraints
  accepted cross_constraints
  constraint_links in ascending ASCII order
```

Tests compare the corresponding E0 `expected.elaboration` projection field by field. Production code must not create a second canonical-state representation or add fixture-derived fields.

### `runtime.py`

Expose frozen dataclasses for the exact closed decision union and witnesses:

```text
ResolutionTrace = AssignmentItem

AskDecision(kind="ASK", semantic_slot_links)
ExecuteDecision(kind="EXECUTE", action_id, executor_resolutions)
RejectDecision(kind="REJECT", reason, witness, executor_resolutions)

ClauseConflictWitness(kind="ClauseConflictWitness", clause_links)
EmptyDomainWitness(kind="EmptyDomainWitness", semantic_slot_link, excluding_constraint_links)
CrossConstraintWitness(kind="CrossConstraintWitness", cross_constraint_links)
ExcludedAction(action_id, unauthorized_managed_effects)
NoAuthorizedActionWitness(kind="NoAuthorizedActionWitness", excluded_actions)

Decision = AskDecision | ExecuteDecision | RejectDecision

enumerate_joint_completions(elaborated) -> tuple[Assignment, ...]
decide(elaborated, candidate_trajectory_ids) -> RuntimeEvaluation
```

`RuntimeEvaluation` contains exactly the ordered `legal_joint_completions`, the closed `decision`, and only private or explicitly named derived support needed by `backend.py` to determine whether an exact execution result exists. It may not contain expected values, fixture IDs, retries, fallback decisions, or a second decision channel.

Unexpected runtime contract violations fail loudly through one explicit runtime exception type carrying `stage="runtime"` and a stable reason. They do not become `ASK`, an empty Contract, a default value, or a fabricated witness. At minimum, unknown trajectory IDs, a trajectory assignment outside `Omega`, an impossible empty clause-conflict witness, and failure to find a sufficient USER query use distinct stable reasons.

### `backend.py`

Expose one shared backend entry point that takes the six elaborator inputs plus `candidate_trajectory_ids`, calls `elaborate` and `decide`, and returns a frozen `BackendOutcome` containing:

```text
elaborated
legal_joint_completions
decision
result: ExecutedResult | null
```

The entry point must not accept `fixture_id`, `case_id`, `scenario_id`, `entry_stage`, an expected record, a gold flag, or an arm name. E2 and E3 will feed their canonical values into this same backend later.

`ExecutedResult` has `kind="EXECUTED"`, `action_id`, final observables in frozen trajectory order, and ordered effects. It is produced only when the selected `EXECUTE` is already sufficient to identify one exact post-state/effect sequence across every supporting trajectory. If unresolved USER alternatives supporting the same safe action yield different post-states, E1 must not choose a USER value or fabricate one exact result; `result` remains `null` until a later concrete execution input exists. `ASK` and `REJECT` do not mutate world state and have `result=null`.

For F9 Gold canonical input, the unique trajectory must produce the exact frozen JSON projection:

```json
{
  "kind": "EXECUTED",
  "action_id": "write_json",
  "final_observables": {
    "format": {"type": "OutputFormat", "value": "JSON"}
  },
  "ordered_effects": ["WRITE_OUTPUT"]
}
```

No production API serializes or reads a test-only expected record. A small test-local projection helper may compare dataclasses with the frozen JSON values.

## Deterministic elaboration contract

Elaboration operates only on canonical semantics, source support, visible context, declarations, and constraints. It must not receive or inspect candidate trajectory IDs, actions, effects, expected decisions, or results.

### Canonical order, symbols, and links

1. Build the source-ref table from `SourceEnvelope.spans`; duplicate refs are already rejected by E0 loading. A missing envelope for a canonical backend input is an elaboration failure.
2. Canonically order normative candidates by the accepted E0 support-first key and tie-break; order knowledge assertions by the same rule.
3. Derive `clause:<three-digit-index>` only from that candidate order.
4. For each `OpenTerm` at candidate index `i`, argument position `j`, derive `slot:clause:<i>:arg<j>`. The embedded term link, exactly one `OpenSlotMention`, and exactly one `SlotDeclaration` must agree on link, type, owner, proposition link, argument position, and proposition support. Missing, duplicate, or extra mentions/declarations fail; links are never silently rewritten.
5. At most two slots may remain unresolved after applying declared `resolved_value`s. Exceeding the bound fails elaboration.

Candidate and knowledge predicate IDs must exist in the frozen manifest. Argument count and each `ValueTerm` / `OpenTerm` type must exactly match the predicate signature. Support refs must exist. A claimed-authority ref must also directly occur in the candidate's proposition support. No type coercion, missing-ref deletion, candidate deletion, default term, or implicit link repair is allowed.

Modality/scope compatibility is exact:

- `GOAL` requires a `FINAL` predicate;
- `REQUIRE` evaluates the predicate according to its manifest scope;
- `PRESERVE` requires a `TRACE` predicate whose frozen interpretation compares the selected observable across initial and final state;
- `FORBID` and `ALLOW` require an `EVENT` predicate.

The accepted E0 manifest contains no `TRACE` predicate, so no E1 fixture can instantiate `PRESERVE`; E1 must not invent a predicate or interpretation to broaden coverage.

### Authority gate

For each well-formed candidate:

- derive `authority=USER` only when `claimed_authority_support` is nonempty and every claimed ref is a direct proposition-support ref whose original source role is `USER`;
- otherwise derive `authority=NONE`;
- set `active=true` exactly for `authority=USER` and retain inactive candidates for inspection;
- never derive authority from OPEN owner, an executor resolution, assistant/tool text, a fixture label, or bridge inference.

An assistant/tool claimed support is valid evidence for retaining an inactive candidate; it is not an elaboration failure. A dangling support or a claimed ref not directly supporting the proposition is a failure.

### Domains and constraints

For every declared slot:

- `schema_domain` must be an actual nonempty tuple of unique `TypedValue`s of the declared enum type, in that enum's declaration order;
- `resolved_value`, when present, must be a member of that declared domain and does not rewrite the domain;
- apply only valid visible static constraints, in ascending constraint-link order, to compute `context_admissible_values` while preserving enum order;
- a candidate value remains admissible exactly when the unique matching visible context observation equals the constraint's `required_context_value`; a missing, ambiguous, wrong-scope, wrong-signature, wrong-slot, or wrong-type observation/constraint fails elaboration;
- an initially valid nonempty domain reduced to empty remains an empty `SlotDomain` and reaches runtime unchanged.

Each cross constraint must name two distinct declared slots in canonical link order. Every allowed tuple has the corresponding two declared types, contains domain members, and is unique. An empty `allowed_tuples` table is valid and reaches runtime. Constraint links are globally unique and output in ascending ASCII order. E1 implements only these fixture-local finite relation tables.

### Stable elaboration failures

The four F8 canonical cases must derive, without expected lookup, exactly:

| Case | Exact failure |
|---|---|
| `dangling_support` | `elaboration/DANGLING_SUPPORT_REF` |
| `wrong_enum_type` | `elaboration/TYPE_MISMATCH` |
| `malformed_domain` | `elaboration/MALFORMED_DOMAIN_DECLARATION` |
| `declared_empty_domain` | `elaboration/DECLARED_EMPTY_DOMAIN` |

Other invalid schema, source, ordering, link, support-declaration, modality/scope, resolved-value, static-constraint, cross-constraint, or unresolved-slot-bound failures must use one explicit, stable, specific reason per category. Their exact names may be the direct uppercase category names, but one generic `INVALID_INPUT`, raw `KeyError`, assertion, fallback, or retry is not acceptable. `missing_adapter_link` must remain untouched for E2; E1 may neither derive nor claim that adapter-stage failure.

## Joint completion and decision contract

### `Omega`

Enumerate slots by canonical slot-link order and values by `TYPE_VALUE_ORDER`, restricted to each elaborated domain, declared resolved values, and every finite cross-constraint table. With zero slots, `Omega` is exactly one empty assignment. Enumeration is independent of candidate trajectories and must match every non-failure case's frozen `expected.legal_joint_completions` exactly.

If a context-admissible domain is empty, return only:

```text
REJECT(HARD_UNSAT,
       EmptyDomainWitness(canonical empty slot,
                          minimal canonical excluding static-constraint links),
       executor_resolutions=[])
```

Do not enumerate actions or ASK. If individual domains are nonempty but cross constraints make `Omega` empty, return only `REJECT(HARD_UNSAT, CrossConstraintWitness(...), [])`. The witness is the minimum-cardinality subset of cross-constraint links whose conjunction empties `Omega`, with lexicographic canonical-link tie-break. Neither route is an elaboration failure or `NO_AUTHORIZED_ACTION`.

### Hard validity and authorization

For each `Omega` completion, consider only listed frozen trajectories whose complete ordered assignment equals that completion. Substitute the completion into every active candidate.

- `GOAL` and `REQUIRE` are hard-valid exactly when their frozen predicate interpretation is true.
- `PRESERVE` is hard-valid exactly when its frozen trace interpretation reports preservation.
- `FORBID` is hard-valid exactly when its event interpretation is false.
- `ALLOW` is not a hard obligation.
- inactive candidates and knowledge assertions do not constrain trajectory validity.

A pair is hard-valid only if every active hard candidate is satisfied. If no pair is hard-valid, return `HARD_UNSAT` with the minimum-cardinality active hard-clause subset that rules out every otherwise matching completion/trajectory pair; tie-break by the lexicographically smallest canonical clause-link tuple. An empty `ClauseConflictWitness` is forbidden and indicates a runtime contract failure, not a decision.

For each hard-valid pair, every emitted effect in `MANAGED_EFFECTS` must match at least one active `ALLOW` event candidate. Unmanaged effects require no `ALLOW`. If hard-valid pairs exist but none is authorized, return `NO_AUTHORIZED_ACTION`. Its witness lists each distinct hard-valid action in ascending action-ID order and that action's unmatched managed effects in ascending effect-ID order. It must not be reported as logical conflict.

### USER projection, executor coverage, and action selection

Let `P_U` be the distinct ordered projections of `Omega` onto unresolved USER-owned slots. Resolved USER slots constrain `Omega` but are not queried. For one complete assignment `e` to all EXECUTOR-owned slots, let `F_U(e)` be the USER projections paired with `e` in `Omega`. `e` preserves USER coverage exactly when `P_U` and `F_U(e)` are equal and nonempty.

An `(action_id, e)` is safe exactly when `e` preserves coverage and, for every `u` in `P_U`, the combined completion has a hard-valid authorized listed trajectory with that same `action_id`. Empty or narrower fibers cannot execute. Multiple EXECUTOR slots are selected jointly.

If any safe pair exists, choose ascending `action_id`; ties choose the executor assignment by canonical slot order and enum declaration order. Return `EXECUTE` and record every EXECUTOR-owned slot/value in canonical slot order before the action. No USER value appears in `executor_resolutions`, and an executor resolution never changes authority.

This must yield the frozen F2 resolved, F3, F4, and F5 behaviors, including F3 `LOCAL` coverage and F4's two jointly recorded resolutions.

### Minimum sufficient one-shot ASK

When hard-valid authorized pairs exist but no action is safe across the current `P_U`, enumerate nonempty subsets of unresolved USER slot links. A query subset is sufficient exactly when, for every feasible answer in its projection, restricting `Omega` by that answer allows the remaining uncertainty to close without another ASK: the restricted state must yield either a coverage-safe `EXECUTE`, `HARD_UNSAT`, or `NO_AUTHORIZED_ACTION` by the same existence definitions.

Choose the sufficient subset with minimum cardinality; ties use the lexicographically smallest tuple of canonical slot links. Return one batch `ASK` containing exactly those links. `ASK([])`, querying an EXECUTOR slot, querying a resolved USER slot, recursively asking, or independently solving coupled slots is forbidden. Failure to find a sufficient subset fails loudly as a runtime contract violation.

This must yield exactly F1 `ASK([slot:clause:000:arg0])` and F2 unresolved `ASK([slot:clause:000:arg0])`.

## E1-owned fixture closure

The E1 test harness must raw-read test-only expected data without making it reachable from production code and assert:

1. Every valid `entry_stage=CANONICAL` case in F1-F7 matches exact expected elaboration, legal joint completions, decision, witnesses, action IDs, and executor resolutions.
2. F8 `dangling_support`, `wrong_enum_type`, `malformed_domain`, and `declared_empty_domain` raise their exact elaboration failures before runtime; no decision or result is produced.
3. F8 `missing_adapter_link` is explicitly excluded from E1 execution and remains owned by E2. E1 must not add adapter behavior merely to make all F8 rows pass early.
4. Each F9 test-only expected canonical state can enter the same ordinary backend as a Gold canonical value. All three produce exact expected elaboration, `[[]]`, `EXECUTE(write_json, executor_resolutions=[])`, and exact `ExecutedResult` without invoking a source extractor or bridge. This is backend integration coverage only, not C-path evidence.
5. F5 proves USER/ASSISTANT/TOOL authority separation and that EXECUTOR ownership does not grant normative authority.
6. F6 proves the three mutually exclusive `ClauseConflictWitness`, `EmptyDomainWitness`, and `CrossConstraintWitness` routes.
7. F7 proves hard-validity is distinct from managed-effect authorization.
8. F1-F4 prove joint enumeration, USER projection, non-vacuous executor coverage, minimum sufficient ASK, canonical tie-breaks, and complete resolution traces.
9. Production modules do not import tests, read JSON fixtures/expected values, contain fixture/case IDs, or expose fixture identity in backend call signatures.

Tests may construct small in-memory counterexamples only to verify a named invariant or fail-loud route. They must not add fixture files, expand the dialect, build a generic solver, or freeze E2-E4 behavior.

## Verification

Run exactly:

```sh
python -m unittest Phase0.tests.test_e0_dialect_and_fixtures Phase0.tests.test_e1_elaboration_and_runtime
git diff --check
```

The first command must report the existing 11 E0 tests plus the new E1 tests with exit status 0. The second must produce no output and exit 0. No experiment output or external artifact checksum exists for E1.

## Executor return format

Return:

1. bound source commit, handoff path, and handoff blob SHA;
2. predecessor accepted commit/range;
3. exact changed paths;
4. concise elaboration/runtime/backend summary;
5. both verification commands, exit status, and unittest count;
6. confirmation that production dependencies are expected-blind, no forbidden path changed, and no commit was created;
7. residual risks or `none`.

## Independent implementation reviewer checklist and verdict

The reviewer checks:

- exact binding identity and four-path mutation compliance;
- preservation of every accepted E0 interface, fixture, and test;
- absence of expected/fixture identity leakage in production dependencies;
- canonical ordering/link/type/support and authority derivation;
- modality/scope checks and valid static/cross constraint handling;
- strict separation of malformed/declared-empty elaboration failures from runtime empty-domain/cross-empty rejects;
- exact `Omega`, hard validity, authorization, witness minimality, executor coverage, ASK sufficiency, and all tie-breaks;
- exact decisions for every E1-owned F1-F9 route and exact F9 Gold canonical Result;
- absence of A/B, C, tracing, general solver, fallback/default/retry, and extra output scope;
- successful targeted and E0 regression verification.

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

The writer does not commit. Main freezes the implementation diff in a sequential E1 commit, then dispatches an independent strict read-only review of that exact commit/range. A rejection requires a separate repair commit and a fresh independent review. Reviewed history is never rewritten.

Only main may accept the exact reviewed implementation, create `Phase0/reviews/E1_<short-reviewed-sha>_review.md`, and then generate the E2 handoff from actual accepted E1 interfaces and findings. E2 cannot be generated or bound before E1 acceptance.
