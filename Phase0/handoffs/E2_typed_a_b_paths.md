# E2 handoff — fixture-direct typed A/B paths

- Proposed status after contract acceptance: `READY_TO_BIND`
- Classification: blocking
- Governing plan: [`IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md`](../IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md)
- Authored against clean source commit: `31f139f97a9961d9fa66aa20f8783c4c241a1ba8`
- Accepted predecessor implementation: `086f9da0519977e55af7d63b98032ab1e207e22f`
- Accepted predecessor reviewed range: `d8ffeb0301d53f3fd55b649bf1ebff3b7cf30bd5..086f9da0519977e55af7d63b98032ab1e207e22f`
- Accepted predecessor review: [`E1_086f9da_review.md`](../reviews/E1_086f9da_review.md)

## Objective and non-goals

Implement the two minimum fixture-direct typed paths required by the Phase 0 plan:

```text
ContractSurfaceState             -> alpha_A -+
                                               +-> CanonicalSemanticState -> existing run_backend
SemanticIsomorphicSurfaceState   -> alpha_B -+
```

Both surfaces carry the same clause, fixed knowledge, OPEN ownership, proposition support, and claimed-authority support information. They differ only in a small field organization: A is clause-centric with explicit canonical links and nested OPEN metadata; B is position-indexed with flat OPEN bindings. `alpha_A` and `alpha_B` are deterministic, expected-blind adapters with the exact existing `CanonicalSemanticState` codomain.

E2 exercises the accepted E1 backend through both adapters. It does not change or reinterpret E0 fixtures, canonical records, dialect semantics, elaboration, runtime, decisions, or results.

E2 does not implement or edit:

- the C source extractor, segmenter, `ExtractiveContentState`, `ReferencedSupportView`, `VisibleWorldContext`, or `beta_C`;
- a natural-language compiler for A or B;
- a second backend, arm-specific elaboration/runtime behavior, or adapter-specific semantic rules;
- E3/E4 tracing, runners, recorded outputs, reports, or experiment infrastructure;
- optional LM integration, retries, defaults, fallbacks, a generic serialization framework, or a general schema/validation library.

Production code must not read fixtures or fixture `expected` fields, import tests, accept fixture/case/scenario IDs, inspect candidate trajectories/actions/effects, or branch on an expected decision/result. Gold canonical values may be read only by the E2 test harness to construct typed test inputs and must enter the same ordinary adapters and existing backend.

## Start conditions and binding packet

Main may dispatch E2 only after this handoff contract package has been committed and independently accepted. The dispatch must contain all of:

1. stage ID `E2`;
2. exact clean source commit containing the accepted E2 handoff and its accepted review record;
3. this exact handoff path and its Git blob SHA at that source commit;
4. predecessor accepted implementation `086f9da0519977e55af7d63b98032ab1e207e22f` and reviewed range `d8ffeb0301d53f3fd55b649bf1ebff3b7cf30bd5..086f9da0519977e55af7d63b98032ab1e207e22f`;
5. the exact allowed mutation paths below;
6. the exact verification commands below;
7. output roots `none`, because E2 creates no formal experiment or recorded-run output.

The authored-against commit binds the actual accepted E1 interfaces and review findings used to write this handoff; it is not by itself execution authority. A branch name, draft, superseded handoff, or different blob grants no mutation authority. If an accepted E0/E1 source, fixture, plan invariant, or this handoff changes after review, main must reconcile and re-review the contract before dispatch.

Any contract conflict or required change outside the allowed paths blocks E2 and returns to main. The executor must not patch a predecessor, broaden the mutation lease, or work around the conflict.

## Allowed mutation paths

```text
Phase0/implementation/typed_paths.py
Phase0/tests/test_e2_typed_paths.py
```

Every other path is forbidden. In particular, E2 may not edit `schema.py`, `dialect.py`, `fixture_loader.py`, `elaboration.py`, `runtime.py`, `backend.py`, any F1-F9 JSON file, E0/E1 tests, plans, handoffs, reviews, package `__init__.py` files, or create any other source, test, configuration, cache, note, report, or output file. If the two allowed files are insufficient, stop and return the exact missing contract or path requirement to main.

## Accepted dependencies and public boundary

E2 must import and reuse, without copying or redefining:

- canonical records and enum order from `Phase0.implementation.schema`;
- `run_backend` and `BackendOutcome` from `Phase0.implementation.backend`;
- the accepted expected-blind fixture loader only from tests;
- the nine accepted JSON fixtures as immutable test inputs and test-only gold/expected data.

The production module may import only Python standard-library modules and other modules under `Phase0.implementation`. It may not open JSON files. It must expose:

```text
AdapterFailure(stage="adapter_or_bridge", reason=<stable code>)

alpha_A(surface: ContractSurfaceState) -> CanonicalSemanticState
alpha_B(surface: SemanticIsomorphicSurfaceState) -> CanonicalSemanticState
adapt_typed_surface(
    adapter_link: "alpha_A" | "alpha_B" | null,
    surface,
) -> CanonicalSemanticState
```

`AdapterFailure` is the only public adapter failure channel and carries exact string `stage` and `reason` attributes. The dispatcher applies this precedence before inspecting arm contents:

1. `adapter_link is None` -> `adapter_or_bridge/MISSING_ADAPTER_LINK`;
2. a non-string link -> `adapter_or_bridge/INVALID_ADAPTER_LINK`;
3. an unknown string -> `adapter_or_bridge/UNKNOWN_ADAPTER_LINK`;
4. a known link with the wrong exact surface class -> `adapter_or_bridge/ADAPTER_SURFACE_TYPE_MISMATCH`;
5. otherwise invoke the corresponding adapter.

The dispatcher exists only to close the accepted F8 adapter-entry boundary. `run_backend` remains arm-blind and unchanged; no arm name or adapter link may be added to its signature or result.

## Minimum immutable surface schemas

All listed records are frozen dataclasses in `typed_paths.py`. Private helpers and exact class names for nested records may vary only when the public information and validation behavior below remain unambiguous. Do not introduce mappings, inheritance hierarchies, generic AST nodes, registries, or serialization layers.

### A: clause-centric Contract surface

```text
ContractValueArgument:
  value: existing TypedValue

ContractOpenArgument:
  semantic_slot_link: string
  type: frozen enum type ID
  owner: USER | EXECUTOR
  proposition_support: tuple[string, ...]

ContractClause:
  clause_link: clause:<three-digit-index>
  modality
  predicate
  arguments: tuple[ContractValueArgument | ContractOpenArgument, ...]
  proposition_support: tuple[string, ...]
  claimed_authority_support: tuple[string, ...]

ContractKnowledgeAssertion:
  knowledge_link: knowledge:<three-digit-index>
  predicate
  arguments: tuple[ContractValueArgument, ...]
  basis
  commitment
  proposition_support: tuple[string, ...]

ContractSurfaceState:
  clauses: tuple[ContractClause, ...]
  knowledge_assertions: tuple[ContractKnowledgeAssertion, ...]
```

A nests each OPEN's owner and support beside its term and carries explicit canonical clause/slot links. Links must form complete contiguous sequences from zero. `alpha_A` sorts by those links, validates every OPEN link as `slot:<clause_link>:arg<argument-index>`, and emits one matching `OpenTerm` plus one `OpenSlotMention`.

### B: position-indexed semantic-isomorphic surface

```text
IsomorphicTerm:
  kind: VALUE | OPEN
  value_type: frozen enum type ID
  value: frozen enum value ID | null

IsomorphicProposition:
  proposition_index: nonnegative integer
  force: modality
  relation: predicate
  terms: tuple[IsomorphicTerm, ...]
  evidence: tuple[string, ...]
  authority_evidence: tuple[string, ...]

IsomorphicFact:
  fact_index: nonnegative integer
  relation: predicate
  terms: tuple[IsomorphicTerm, ...] containing VALUE terms only
  basis
  commitment
  evidence: tuple[string, ...]

IsomorphicOpenBinding:
  proposition_index: nonnegative integer
  argument_index: nonnegative integer
  owner: USER | EXECUTOR
  evidence: tuple[string, ...]

SemanticIsomorphicSurfaceState:
  propositions: tuple[IsomorphicProposition, ...]
  facts: tuple[IsomorphicFact, ...]
  open_bindings: tuple[IsomorphicOpenBinding, ...]
```

B carries no clause or slot strings. Proposition/fact indices must each be unique and form a complete contiguous sequence from zero. One and only one binding must exist for every OPEN term, no binding may target a VALUE term, and binding order is canonical `(proposition_index, argument_index)` order. `alpha_B` derives `clause:<index>` and `slot:clause:<index>:arg<argument_index>` mechanically.

A and B add no authority label, active flag, action/effect data, world result, fixture identity, or expected value. Claimed authority remains support evidence and continues to be derived only by the accepted E1 elaborator.

## Deterministic adapter contract

Both adapters must validate their complete public input boundary before constructing a canonical value:

- require the exact surface/nested dataclass families and exact tuple containers; do not accept lists, mappings, subclasses, iterators, or coercible values;
- require exact strings, and exact non-boolean integers for B indices;
- require recognized VALUE/OPEN tags and frozen enum type/member IDs;
- require valid modality, OPEN owner, knowledge basis, and knowledge commitment enum members;
- require support tuples to contain unique strings while preserving their order;
- require A link topology and B index/binding topology exactly as defined above;
- construct fresh immutable canonical records and tuples; never return or mutate a surface object.

Any malformed A record/container/link topology raises `adapter_or_bridge/INVALID_CONTRACT_SURFACE`. Any malformed B record/container/index/binding topology raises `adapter_or_bridge/INVALID_ISOMORPHIC_SURFACE`. No raw `TypeError`, `KeyError`, assertion, partial canonical value, fallback, repair, or default is allowed.

Validation that requires the dialect, source envelope, or world remains in the accepted E1 elaborator. In particular, predicate existence/signature, term-to-predicate type compatibility, support-ref existence, claimed-support legality, modality/scope compatibility, and authority derivation must not be duplicated in E2. Thus the accepted F8 `wrong_enum_type` canonical semantics must survive either adapter and still fail at `elaboration/TYPE_MISMATCH`, not at the adapter boundary.

For well-formed inputs, adapters map fields exactly:

- VALUE -> `ValueTerm(kind="VALUE", TypedValue(type, value))`;
- OPEN -> `OpenTerm(kind="OPEN", type, derived-or-validated semantic_slot_link)` plus exactly one matching `OpenSlotMention`;
- A clause fields or B proposition fields -> `NormativeCandidate` fields without deriving authority;
- A knowledge fields or B fact fields -> `KnowledgeAssertion` fields;
- candidates, knowledge, and OPEN mentions -> their canonical link/index order.

No dictionary/set iteration, object identity, input permutation outside the explicit link/index normalization, fixture filename, or test order may become a semantic tie-break.

## Gold round-trip and backend parity

`test_e2_typed_paths.py` may define test-local expected/gold readers and canonical-to-A/B constructors. These helpers must remain under tests and must not become production dependencies.

The tests must establish all of:

1. For every `entry_stage=CANONICAL` F1-F8 case except F8 `missing_adapter_link`, construct both typed surfaces from the accepted input canonical state and assert exact dataclass equality:

   ```text
   alpha_A(gold_A) == alpha_B(gold_B) == accepted canonical input
   ```

2. For each F9 case, test-only read its frozen `expected.canonical_state`, construct both gold typed surfaces, and assert the same exact round-trip. This is typed-path debug coverage, not C-path evidence.
3. For every non-failure case above, pass each adapter output with the identical accepted source/context/declaration/constraint/trajectory inputs to the unchanged `run_backend`; assert exact A/B `BackendOutcome`, decision, and result parity.
4. For F8 `dangling_support`, `wrong_enum_type`, `malformed_domain`, and `declared_empty_domain`, assert both typed paths reach the same exact accepted E1 failure stage/reason. The adapters may not absorb or reroute those failures.
5. Include at least one hand-authored, non-trivial A/B pair for F1 and one for an F2/F3 USER/EXECUTOR case so joint OPEN ownership is not covered only by generic conversion helpers.
6. Include one small in-memory fixed-value `KnowledgeAssertion` round-trip for both schemas because the accepted JSON fixtures carry no nonempty knowledge list.
7. Assert production import/source dependencies are expected-blind: no JSON reads, test imports, fixture/expected identifiers, scenario IDs, candidate trajectory/action/effect access, or backend copy in `typed_paths.py`.

The test-local canonical-to-surface constructors are test data preparation, not normal A/B compilers and not evidence of learned compilation. They must not be exported or moved into production.

## Malformed-input and F8 closure

Tests must directly construct malformed dataclasses rather than relying only on the strict JSON loader. At minimum they cover:

- non-tuple top-level and nested containers for both arms;
- malformed `TypedValue`/term tag/member records;
- duplicate, missing, non-contiguous, or wrongly shaped A links and B indices;
- a mismatched A OPEN slot link;
- missing, duplicate, extra, or VALUE-targeting B OPEN bindings;
- non-string support entries and a boolean used as a B index;
- dispatcher null, non-string, unknown, and link/surface mismatch routes.

The accepted F8 `missing_adapter_link` payload must be passed to `adapt_typed_surface` and produce exactly:

```text
adapter_or_bridge/MISSING_ADAPTER_LINK
```

It must fail before surface inspection, canonical construction, elaboration, or runtime. No invalid adapter input may silently yield an empty `CanonicalSemanticState` or reach an ordinary decision.

## Engineering observation return

Do not build metrics or a report file. The executor returns three concise observations based on the implementation diff:

1. which A or B encoding was clearer to validate and why;
2. where adapter logic was duplicated;
3. the concrete maintenance cost visible at E2 scale.

These are provisional engineering notes only. They do not establish general encoding superiority and do not alter acceptance.

## Verification

Run exactly:

```sh
python -B -m unittest Phase0.tests.test_e0_dialect_and_fixtures Phase0.tests.test_e1_elaboration_and_runtime Phase0.tests.test_e2_typed_paths
git diff --check
```

All tests must pass with exit status 0, and `git diff --check` must produce no output. No experiment output or external artifact checksum exists for E2.

## Executor return format

Return:

1. bound source commit, handoff path, and handoff blob SHA;
2. predecessor accepted commit/range;
3. exact changed paths;
4. concise A/B schema and adapter summary;
5. both verification commands, exit status, and unittest count;
6. confirmation that production dependencies are expected-blind, no forbidden path changed, and no commit was created;
7. the three engineering observations requested above;
8. residual risks or `none`.

## Independent implementation reviewer checklist and verdict

The reviewer checks:

- exact binding identity and two-path mutation compliance;
- preservation of every accepted E0/E1 interface, fixture, source file, and test;
- complete strict validation of direct-dataclass boundaries and stable adapter failures without raw exceptions;
- exact F8 `MISSING_ADAPTER_LINK` precedence and no silent empty canonical state;
- exact A/B information equivalence, canonical round-trip, OPEN link/binding bijection, ordering, and knowledge preservation;
- absence of extra arm-specific semantics or information;
- expected-blind production dependencies and unchanged shared `run_backend` usage;
- exact A/B backend outcome/failure parity across the required fixtures;
- absence of C, tracing, runners, general schema systems, fallback/default/retry, and extra output scope;
- successful E0/E1/E2 verification.

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

The writer does not commit. Main freezes the implementation diff in a sequential E2 commit, then dispatches an independent strict read-only review of that exact commit/range. A rejection requires a separate repair commit and a fresh independent review. Reviewed history is never rewritten.

Only main may accept the exact reviewed implementation, create `Phase0/reviews/E2_<short-reviewed-sha>_review.md`, and then generate the E3 handoff from actual accepted E2 interfaces and findings. E3 cannot be generated or bound before E2 acceptance.
