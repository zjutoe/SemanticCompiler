# E3 handoff — normal C extraction and real bridge path

- Proposed status after contract acceptance: `READY_TO_BIND`
- Classification: blocking
- Governing plan: [`IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md`](../IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md)
- Authored against clean source commit: `608bdb0c1e9f3fdc15595eb0516828b45cca6edb`
- Accepted predecessor implementation: `bb85d237f55d685bc718ccdc2d07bf913285b724`
- Accepted predecessor reviewed range: `4f7d1da3e6eb1dfaf12532ed327779d2c7b7834d..bb85d237f55d685bc718ccdc2d07bf913285b724`
- Accepted predecessor review: [`E2_bb85d23_review.md`](../reviews/E2_bb85d23_review.md)

## Objective and non-goals

Implement the one Phase 0 path that begins with normal source input:

```text
SourceEnvelope
-> segment_source
-> normal_c_extract
-> ExtractiveContentState
-> build_referenced_support_view
-> exactly one beta_C
-> CanonicalSemanticState
-> existing run_backend
```

E3 must close F9 twice through the same `beta_C`: first from the frozen Gold-C refs for debugging, then from normal non-gold extraction. It must also prove that an unreferenced distractor cannot enter the support view or affect bridge output.

E3 does not implement or edit:

- A/B surfaces or adapters, E0 fixtures, schemas, dialect, elaboration, runtime, or backend;
- learned or prompted compilation, relevance models, training data, retries, fallbacks, or a second bridge;
- a general NLP parser, generic AST, serialization framework, entity system, dynamic dialect, or arbitrary constraint language;
- E4 traces, runners, manifests, recorded outputs, reports, artifact stores, or experiment infrastructure;
- optional LM integration.

The bridge is evidence only for the frozen controlled language and F9. It does not establish natural-language compilation quality or general bridge superiority.

## Start conditions and mutation lease

Main may dispatch E3 only after this exact handoff package is committed and independently contract-accepted. The binding packet must name stage `E3`, the exact clean source commit, this path and Git blob SHA, the accepted E2 commit/range above, the two allowed paths below, all verification commands, and output roots `none`.

If an accepted predecessor interface, F9 fixture, governing-plan invariant, or this handoff changes after review, main must reconcile and re-review the contract before dispatch. Any required edit outside the lease blocks E3; the executor must not patch a predecessor or broaden scope.

Allowed mutation paths:

```text
Phase0/implementation/content_bridge.py
Phase0/tests/test_e3_content_bridge.py
```

Every other path is forbidden, including package `__init__.py` files. E3 creates no cache, configuration, output, note, trace, or report file.

## Reused accepted interfaces

Production must reuse without copying or redefining:

- `SourceEnvelope`, `SourceSpan`, `VisibleWorldContext`, `ContextValue`, canonical records, enums, and `TYPE_VALUE_ORDER` from `Phase0.implementation.schema`;
- `PredicateDefinition` and the frozen `PREDICATES` manifest from `Phase0.implementation.dialect`;
- the existing fixture loader and `run_backend` only from tests.

The accepted E1 boundary supports only an empty `VisibleWorldContext.entities` tuple. E3 freezes that already accepted subset and does not introduce the unused entity-table system described as a possible narrow shape in the plan. Valid `observable_values` remain structurally accepted, but the frozen E3 grammar performs no context-dependent entity linking.

## Public production boundary

`content_bridge.py` must expose frozen dataclasses and functions equivalent to:

```text
CPathFailure(stage=<surface | adapter_or_bridge>, reason=<stable code>)

ExtractiveContentState:
  content_refs: tuple[string, ...]

ReferencedSupportView:
  spans: tuple[existing SourceSpan, ...]

segment_source(SourceEnvelope) -> tuple[SourceSpan, ...]
normal_c_extract(SourceEnvelope) -> ExtractiveContentState
build_referenced_support_view(
    SourceEnvelope,
    ExtractiveContentState,
) -> ReferencedSupportView
beta_C(
    ExtractiveContentState,
    ReferencedSupportView,
    tuple[PredicateDefinition, ...],
    VisibleWorldContext,
) -> CanonicalSemanticState
```

`CPathFailure` is the only C surface/bridge failure channel and carries exact `stage` and `reason` string attributes. No malformed public input may leak a raw exception, yield a partial canonical value, or silently become an empty Contract.

## Atomic source and normal extraction

E0 already freezes source order and stable atomic span refs in `SourceEnvelope`; E3 must not invent new refs or split one accepted ref into subrefs. `segment_source` is therefore a strict atomic-span validator and fresh copier:

- require the exact `SourceEnvelope`, exact tuple container, and exact `SourceSpan` records;
- require unique nonempty string refs, recognized source roles, and nonempty trimmed one-line text;
- require one terminal period and no additional period, so one input span remains one controlled-language atom;
- preserve source order and return fresh immutable `SourceSpan` records.

Malformed input raises `surface/INVALID_SOURCE_ENVELOPE`.

`normal_c_extract` must call the same segmenter and select every syntactically supported atom, regardless of USER/ASSISTANT/TOOL role, in exact source order. Selection is based only on the frozen grammar shapes below. A recognized shape with an unknown typed value/effect is selected and then fails in `beta_C`; it must not be silently filtered as a distractor. Unknown sentence shapes are unrepresentable distractors and are omitted. If no span is representable, fail with `surface/NO_REPRESENTABLE_CONTENT`.

For F9 normal input, the exact refs are `("u1", "u2", "a1")`.

## Frozen controlled-language grammar

Implement a small structural interpreter, not a table from complete fixture sentences to canonical objects. After removing the one terminal period, accept exactly these ASCII token shapes:

```text
Require final format <OutputFormat-member>
Require final format OPEN(<USER|EXECUTOR>)
Use <OutputFormat-member>
Allow managed effect <zero-argument EVENT name>
```

Interpret them as follows:

- `Require final format X` -> `REQUIRE world.final_format_is(X)`;
- `Use X` -> imperative `REQUIRE world.final_format_is(X)`;
- `Allow managed effect E` -> `ALLOW effect.E()`;
- `OPEN(owner)` in the first form -> an `OpenTerm` of the manifest argument type and one matching `OpenSlotMention`.

The interpreter must separately perform modality recognition, phrase-to-predicate linking, manifest signature/scope checks, enum type/member checks, OPEN owner extraction, canonical clause/slot-link construction, and support mapping. Do not use a full-sentence lookup, fixture/case ID, source role branch, expected canonical value, decision, action, trajectory, result, or emitted-effect data.

For every interpreted candidate, both support fields are exactly the one source ref. This records claimed support only; `beta_C` must not derive authority. Candidate and OPEN order follows `ReferencedSupportView` order. Clause links are `clause:<three-digit-index>` and OPEN links are `slot:<clause-link>:arg<argument-index>`. E3 produces no knowledge assertions for this grammar.

`beta_C` must check that the passed manifest is the exact frozen `PREDICATES` value, then use its predicate definitions rather than bypassing signature/scope validation. An enum member must be checked against `TYPE_VALUE_ORDER` for the manifest signature type. An allowed effect must correspond to a zero-argument `EVENT` predicate in that manifest.

## Extractive state, support view, and context boundaries

`ExtractiveContentState.content_refs` must be a nonempty exact tuple of unique nonempty strings. `build_referenced_support_view` validates that every ref exists in the segmented envelope and that the tuple is already in source order; missing, duplicate, or reordered refs raise `surface/INVALID_CONTENT_REFS`. Invalid state structure raises `surface/INVALID_EXTRACTIVE_CONTENT`.

The builder returns a fresh `ReferencedSupportView` containing only fresh copies of the selected spans. It must never attach an unreferenced span, source envelope, scenario identity, or gold metadata.

Before constructing canonical output, `beta_C` validates its complete four-argument boundary:

- exact nonempty extractive state and exact immutable support-view records;
- exact equality between `content_refs` and view span refs, including order;
- unique refs, valid roles, and valid atomic span strings in the view;
- exact frozen manifest tuple and records;
- exact `VisibleWorldContext`, tuple containers, empty entities, and structurally valid `ContextValue` records, signatures, enum values, scopes, and exact booleans.

Stable bridge failures are:

```text
adapter_or_bridge/INVALID_EXTRACTIVE_CONTENT
adapter_or_bridge/INVALID_REFERENCED_SUPPORT_VIEW
adapter_or_bridge/CONTENT_VIEW_MISMATCH
adapter_or_bridge/INVALID_DIALECT_MANIFEST
adapter_or_bridge/INVALID_VISIBLE_WORLD_CONTEXT
adapter_or_bridge/UNSUPPORTED_CONTENT
```

`UNSUPPORTED_CONTENT` covers a selected atom whose grammar, predicate, effect, owner, type, or member cannot be interpreted under the frozen manifest. Validation completes before canonical construction; no earlier candidates may escape on failure.

## Required evidence

`test_e3_content_bridge.py` may read F9 expected fields and convert fixture `ExtractiveContentPayload` into the production state. Gold data remains test-local and must enter the same ordinary view builder, `beta_C`, and backend.

Tests must establish all of:

1. F9 normal source produces exact refs `("u1", "u2", "a1")`, the exact frozen support view, exact canonical state, exact elaborated projection, `EXECUTE(write_json, executor_resolutions=())`, and exact executed result.
2. F9 `gold_c_original` and `gold_c_distractor_variant` each use their frozen refs `("u1", "u2")`; both support views are exactly equal and exclude `a1`; the same `beta_C` returns equal canonical values matching the frozen Gold-C canonical state.
3. The Gold-C original output reaches the unchanged backend with its exact frozen elaboration, decision, and result. No alternate oracle bridge or canonical substitution is used.
4. One small direct in-memory source covers both `OPEN(USER)` and `OPEN(EXECUTOR)` and asserts exact typed terms, owners, canonical links, and support refs. It does not create a new fixture or backend scenario.
5. A mixed in-memory envelope proves normal extraction includes all recognized grammar shapes in source order, includes a syntactically recognized invalid typed atom for loud bridge failure, and omits only unknown sentence shapes.
6. Direct-dataclass malformed cases cover source containers/records/roles/refs/atomic text; empty/duplicate/missing/reordered refs; extra, reordered, wrong-role, or changed-text view spans; malformed manifest and visible context; unsupported values/effects/owners; and exact failure stages/reasons without raw exceptions.
7. Production dependency inspection proves no JSON/file reads, fixture/test/backend imports, expected/gold identifiers, scenario IDs, candidate trajectories/actions/results, `TRAJECTORIES`, or full-sentence canonical lookup.

Tests must keep fixture expected readers and backend projections local. Production cannot import the fixture loader, backend, or test modules.

## Engineering observation return

Do not create a metrics/report file. The executor returns three bounded observations:

1. where normal extraction and bridge interpretation failures became distinguishable;
2. what extra representation/validation cost C adds relative to the accepted direct typed path;
3. the most brittle concrete part of the frozen controlled-language bridge.

These are provisional engineering notes, not comparative scientific claims.

## Verification and return

Run exactly:

```sh
python -B -m unittest Phase0.tests.test_e0_dialect_and_fixtures Phase0.tests.test_e1_elaboration_and_runtime Phase0.tests.test_e2_typed_paths Phase0.tests.test_e3_content_bridge
ruff check --no-cache Phase0/implementation/content_bridge.py Phase0/tests/test_e3_content_bridge.py
git diff --check
```

Return the binding identity, accepted E2 predecessor/range, exact changed paths, concise implementation summary, command results and unittest count, expected-blind/scope confirmation, the three observations, and residual risks. Do not commit.

## Independent reviewer and acceptance gate

In addition to the common repository review protocol, the read-only reviewer must check:

- exact binding identity and two-path mutation compliance;
- strict complete public boundaries and stable failures without raw exceptions or silent empty canonical output;
- normal extractor completeness/order without gold relevance or role filtering;
- structural controlled-language interpretation rather than full-sentence or expected lookup;
- exact manifest-driven predicate/signature/type/effect and OPEN-link semantics;
- support-view exclusion of unreferenced data and F9 distractor invariance through the same bridge;
- exact F9 normal and Gold-C canonical/backend evidence;
- unchanged E0-E2 code, fixtures, and shared backend;
- absence of E4 tracing/runners/artifacts and other scope expansion;
- successful full E0-E3 verification.

Verdict format:

```text
VERDICT: ACCEPT | REJECT
REVIEWED_COMMIT_OR_RANGE: <exact SHA or range>
HANDOFF_BLOB_SHA: <exact SHA>
VERIFICATION: <commands and results>
FINDINGS: <none or numbered findings>
REQUIRED_REPAIR: <none or exact requirements>
```

Main freezes the implementation before independent review. A rejection requires a separate repair commit and a fresh independent reviewer; history is never rewritten. Only main may accept E3 and then generate the E4 handoff from actual accepted interfaces and findings.
