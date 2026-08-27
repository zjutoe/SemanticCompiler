# K0 Semantic Design Inputs v0

## 1. Research scope and exclusions

K0 freezes falsification-oriented inputs for a domain-independent Contract IR design. It does not claim universal coding completeness. Its representational universe is natural-language coding intent that can be discussed as constraints over a completed abstract outcome:

```text
Outcome = (PRE, TRACE, FINAL, EVIDENCE)
```

In scope are conditions on `PRE`, `TRACE`, `FINAL`, or `EVIDENCE`; authorization conditions over controlled trace events; alternatives and explicitly controller-owned unresolved choices; and relations among constraints. Coding-task labels such as bug fix, feature, or refactor may occur in source language, but they are not presumed semantic categories.

Soft preference is excluded from the initial semantic scope. K1 must nevertheless preserve the boundary between a hard acceptance condition and language that merely ranks otherwise acceptable outcomes: it may report the latter as outside the initial scope, but must not silently strengthen it into a requirement. Reconsidering preference requires a revised, independently accepted K0 boundary.

Arbitrary domain predicates are permitted in principle, including a broad predicate informally described as `task_is_correct`. A name alone does not make a predicate meaningful, evaluable, consistent, or sufficient. Meaning requires an explicit bound semantic contract; evaluation requires its declared capabilities and evidence; and sufficiency remains relative to an explicit profile, never to unknowable intent completeness.

K0 excludes:

- planning, action selection, state-transition execution, repository mutation, and patch generation;
- concrete operation vocabularies and hierarchical execution or action graphs;
- final kernel syntax, schema, serialization, or normalization rules;
- the plugin ABI and selection of coding-plugin symbols;
- learned or prompted natural-language compilation, model prompts, training, or inference;
- plugin retrieval, discovery, installation, or synthesis;
- performance, scalability, benchmark, deployment, publication, or comparative-benefit claims;
- automatic proof of intent completeness or universal decidability;
- an executable checker, evaluator implementation, planner, or executor.

The conclusions available from K0 are limited to whether these frozen inputs are sufficiently independent and discriminating to constrain K1-K3 design. They are not evidence that any eventual design is adequate beyond the accepted challenge scope.

## 2. Semantic status vocabulary

Each status belongs to one namespaced judgment family. Identical words such as “unknown” in ordinary language do not permit conversion between families.

### 2.1 Representation judgment

```text
REPRESENTABLE
UNREPRESENTABLE(reason)
UNRESOLVED(reason)
```

`REPRESENTABLE` says an in-scope intent has an equivalent semantic binding. `UNREPRESENTABLE` records that the accepted semantic boundary cannot express it. `UNRESOLVED` records that the available intent admits multiple semantic bindings or lacks information required to choose one. `UNRESOLVED` is neither plugin inability nor logical `TRUTH_UNKNOWN`.

### 2.2 Structural judgment

```text
WELL_FORMED
MALFORMED(reason)

CLOSED
OPEN_BINDINGS(binding_refs)
```

Well-formedness concerns compliance with the applicable structural contracts. Closure concerns whether required variables, references, symbols, versions, and choices are bound. A well-formed partial Contract may intentionally have `OPEN_BINDINGS`.

### 2.3 Evaluation-capability judgment

```text
EVALUABILITY_AVAILABLE(capability_refs)
EVALUABILITY_MISSING(missing_capability_refs)
EVALUABILITY_UNKNOWN(reason)
```

This family reports whether the requested concrete evaluation or proof service is available. It implies nothing about formula truth, satisfiability, completeness, entailment, or equivalence.

### 2.4 Formula truth and evaluation failure

```text
TRUTH_TRUE(evidence_refs)
TRUTH_FALSE(evidence_refs)
TRUTH_UNKNOWN(reason, evidence_refs)
EVALUATION_ERROR(reason)
```

The first three statuses preserve the logical domain `TRUE | FALSE | UNKNOWN`. `TRUTH_UNKNOWN` is never rewritten as true or false. `EVALUATION_ERROR` is outside that domain: an evaluator or evaluator-infrastructure failure produces no logical truth conclusion and no conclusion in another judgment family.

### 2.5 Consistency judgment

```text
CONSISTENCY_SAT(witness_ref)
CONSISTENCY_UNSAT(proof_or_core_ref)
CONSISTENCY_UNKNOWN(reason)
```

`CONSISTENCY_SAT` requires a valid satisfying witness under the bound semantics. `CONSISTENCY_UNSAT` requires a valid proof or unsatisfiable core accepted under the bound reasoning capability. Completion without either result is `CONSISTENCY_UNKNOWN`, not satisfiable. A service failure is `REASONING_ERROR` and produces no consistency judgment.

### 2.6 Profile-relative completeness judgment

```text
PROFILE_COMPLETE(profile_ref, evidence_refs)
PROFILE_INCOMPLETE(profile_ref, missing_dimensions)
PROFILE_UNKNOWN(profile_ref, reason)
```

This family is meaningful only relative to an explicit versioned profile and its required semantic dimensions. No member can be promoted to a certificate of intent completeness.

### 2.7 Entailment, equivalence, and reasoning-service failure

```text
RELATION_PROVED(ENTAILMENT | EQUIVALENCE, proof_ref)
RELATION_DISPROVED(ENTAILMENT | EQUIVALENCE, counterexample_ref)
RELATION_UNKNOWN(ENTAILMENT | EQUIVALENCE, reason)
REASONING_ERROR(reason)
```

`RELATION_UNKNOWN` means that the bound reasoning service completed without proving or disproving the requested relation. `REASONING_ERROR` is outside the relation family and produces no entailment, equivalence, or consistency conclusion. Formula evaluation failure remains `EVALUATION_ERROR` and likewise produces no truth, consistency, profile, entailment, or equivalence conclusion.

### 2.8 Cross-status independence

| Example | Statuses that may coexist | Independence demonstrated |
|---|---|---|
| A typed partial Contract leaves the user’s backend selection open. | `WELL_FORMED`; `OPEN_BINDINGS(user-owned choice)` | Structural validity does not imply closure. |
| A Contract binds all references, but the bound plugin exposes no requested evaluator. | `CLOSED`; `EVALUABILITY_MISSING(required evaluation capability)` | Closure does not supply semantics or services. |
| A concrete evaluator is available, but no satisfying witness or refutation is obtained. | `EVALUABILITY_AVAILABLE(concrete evaluator)`; `CONSISTENCY_UNKNOWN(no accepted witness or proof)` | Capability availability does not settle satisfiability. |
| A witness satisfies all clauses but omits a profile-required evidence dimension. | `CONSISTENCY_SAT(accepted witness)`; `PROFILE_INCOMPLETE(bound profile, missing evidence dimension)` | Satisfiability is not profile completeness. |
| All dimensions of a versioned profile are covered. | `PROFILE_COMPLETE(bound profile, coverage evidence)` | Profile completion cannot certify that unstated user intent was captured. |
| A formula evaluator crashes before returning a value. | `EVALUATION_ERROR(evaluator failure)` | Failure yields no `TRUTH_TRUE`, `TRUTH_FALSE`, or `TRUTH_UNKNOWN`. |
| A symbolic service times out or violates its protocol. | `REASONING_ERROR(reasoning-service failure)` | Failure yields no consistency, entailment, or equivalence judgment. |

No general implication holds between representation, structure, closure, capability availability, truth, consistency, profile completeness, and semantic relations except where a later accepted semantic contract explicitly states and justifies one.

## 3. Seed semantic challenges

The following 19 cases are natural-language design inputs, not expected-IR fixtures. Their abstract conditions name semantic distinctions without prescribing syntax, plugin atoms, actions, patches, or implementation results.

### K0-C01 — positive final-state acceptance

- **Challenge ID:** K0-C01
- **Natural-language instruction:** Keep the command-line tool usable on Windows after the change, including paths that contain spaces.
- **Minimal context:** Acceptance is judged on the completed repository state using a declared platform test protocol and its evidence.
- **Semantic distinction under test:** A positive final-state acceptance condition, separate from how the change is produced.
- **Abstract acceptance or authorization condition:** The declared final-state behavior holds under the stated platform observations.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(declared platform test and evidence contract)`.
- **Forbidden shortcut:** Treating the task label, a fixture ID, or one expected patch as the acceptance condition.
- **Why the case can falsify a design choice:** A design that can describe only trace operations or exact outputs cannot state outcome-level behavioral acceptance.

### K0-C02 — preservation across states

- **Challenge ID:** K0-C02
- **Natural-language instruction:** Update the cache internals without changing which public requests are accepted or rejected.
- **Minimal context:** Public request behavior is observable both before and after the change under the same declared observation protocol.
- **Semantic distinction under test:** Preservation of an observable relation between pre-state and final-state, rather than a final-state property in isolation.
- **Abstract acceptance or authorization condition:** Corresponding pre-state and final-state observations agree for the declared public-request domain.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(comparative observation capability)`.
- **Forbidden shortcut:** Substituting a fixed list of expected final outputs that ignores the pre-state.
- **Why the case can falsify a design choice:** A final-state-only design loses what behavior is being preserved when the baseline varies.

### K0-C03 — forbidden trace condition

- **Challenge ID:** K0-C03
- **Natural-language instruction:** Do not contact the network while preparing or validating this change.
- **Minimal context:** Network contacts are observable controlled events in the completed trace; final files alone do not reveal every contact.
- **Semantic distinction under test:** A forbidden trace condition, independent of final-state equivalence.
- **Abstract acceptance or authorization condition:** No controlled network-contact event occurs in the relevant trace.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(trace observation capability)`.
- **Forbidden shortcut:** Inferring trace compliance solely from the final repository state.
- **Why the case can falsify a design choice:** Two executions can have the same final state while only one violates the prohibition.

### K0-C04 — authorization is not obligation

- **Challenge ID:** K0-C04
- **Natural-language instruction:** You may regenerate the lockfile if dependency metadata actually changes.
- **Minimal context:** Regeneration is a controlled trace event; unchanged metadata leaves it unauthorized, while changed metadata permits but does not require it.
- **Semantic distinction under test:** Conditional permission versus a positive obligation.
- **Abstract acceptance or authorization condition:** The identified principal is authorized to regenerate only under the stated condition; absence of regeneration is not by itself a failure.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(metadata and trace observation capabilities)`.
- **Forbidden shortcut:** Converting “may” into “must” or treating evaluability as authority.
- **Why the case can falsify a design choice:** A design with only positive truth requirements either compels an optional event or cannot constrain its authorization.

### K0-C05 — conditional requirement

- **Challenge ID:** K0-C05
- **Natural-language instruction:** If dependency metadata changes, regenerate the lockfile.
- **Minimal context:** This differs from K0-C04 only in requiring, rather than permitting, regeneration when the same condition holds.
- **Semantic distinction under test:** A requirement activated by a condition, rather than an unconditional requirement or permission.
- **Abstract acceptance or authorization condition:** Whenever dependency metadata changes, the relevant completed trace includes lockfile regeneration.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(metadata and trace observation capabilities)`.
- **Forbidden shortcut:** Treating required regeneration as merely authorized, or requiring it when metadata is unchanged.
- **Why the case can falsify a design choice:** A design without conditional composition changes the accepted outcome set.

### K0-C06 — conditional permission

- **Challenge ID:** K0-C06
- **Natural-language instruction:** A migration file may be edited only when the public database schema changes.
- **Minimal context:** File edits are controlled trace events and schema change is an observable relation across states.
- **Semantic distinction under test:** Permission conditioned on a semantic fact, distinct from requiring the edit when the fact holds.
- **Abstract acceptance or authorization condition:** The identified principal has authority for the edit only in outcomes with the stated schema change.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(schema-comparison and trace capabilities)`.
- **Forbidden shortcut:** Recasting the condition as an instruction to edit whenever the schema changes.
- **Why the case can falsify a design choice:** Collapsing conditional authorization into implication over truth obligations invents an action requirement.

### K0-C07 — multiple acceptable outcomes

- **Challenge ID:** K0-C07
- **Natural-language instruction:** The new export may be configured in either TOML or YAML; support for one of them is enough.
- **Minimal context:** Both formats have declared acceptance observations and neither is preferred.
- **Semantic distinction under test:** Multiple acceptable outcome alternatives without selecting one in advance.
- **Abstract acceptance or authorization condition:** At least one of the two declared acceptance alternatives holds.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(format acceptance capabilities)`.
- **Forbidden shortcut:** Choosing a format via fixture order or requiring both alternatives.
- **Why the case can falsify a design choice:** A purely conjunctive or single-target design rejects an explicitly allowed outcome.

### K0-C08 — unresolved user-owned choice

- **Challenge ID:** K0-C08
- **Natural-language instruction:** Leave the choice between local and hosted storage to me; do not decide it yet.
- **Minimal context:** Either choice can be semantically bound, but the user has deliberately retained control and supplied no selection.
- **Semantic distinction under test:** An unresolved discretionary choice with an identified controller.
- **Abstract acceptance or authorization condition:** The choice remains explicitly open and user-owned until the user binds one alternative.
- **Expected K0 meta-statuses:** `UNRESOLVED(user-owned choice not selected)`; `WELL_FORMED`; `OPEN_BINDINGS(user-owned storage choice)`.
- **Forbidden shortcut:** Guessing a default, treating the choice as an unknown environmental fact, or allowing the executor to own it.
- **Why the case can falsify a design choice:** A design without ownership can silently transfer decision authority.

### K0-C09 — unknown fact pending evidence

- **Challenge ID:** K0-C09
- **Natural-language instruction:** Release the package only if the full compatibility suite passes.
- **Minimal context:** The suite has not run yet; its result is factual, not a discretionary choice.
- **Semantic distinction under test:** Indeterminate formula truth pending evidence versus an unresolved owned choice.
- **Abstract acceptance or authorization condition:** Release acceptance depends on the factual suite result; before evidence arrives its truth is unknown.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(declared suite evaluator)`; `TRUTH_UNKNOWN(required evidence not yet available, no evidence reference)`.
- **Forbidden shortcut:** Letting any principal choose the test result or treating missing evidence as success.
- **Why the case can falsify a design choice:** Conflating uncertainty with discretion corrupts both truth and authority.

### K0-C10 — kernel-visible contradiction

- **Challenge ID:** K0-C10
- **Natural-language instruction:** Require the final configuration to retain diagnostic logging, and also require it not to retain diagnostic logging.
- **Minimal context:** Both clauses refer to the same bound proposition, outcome, and meaning; each atomic reference is individually well-formed.
- **Semantic distinction under test:** An unsatisfiable combination visible from core logical structure without domain-specific contradiction knowledge.
- **Abstract acceptance or authorization condition:** The same proposition is simultaneously required and denied for the same outcome.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `WELL_FORMED`; `CLOSED`; `CONSISTENCY_UNSAT(kernel derivation over the same proposition)`.
- **Forbidden shortcut:** Declaring the document malformed, dropping one clause, or asking a plugin to special-case the challenge.
- **Why the case can falsify a design choice:** A design that conflates formation with consistency, or lacks core contradiction reasoning, misclassifies two valid atoms.

### K0-C11 — plugin-visible contradiction

- **Challenge ID:** K0-C11
- **Natural-language instruction:** Produce at least one bundle, keep every generated bundle below 100 KiB, and require every generated bundle to be at least 200 KiB.
- **Minimal context:** At least one generated bundle is required. The size constraints are individually well-formed and apply to that same nonempty population using the same declared unit; the bound domain reasoner understands numeric bounds.
- **Semantic distinction under test:** Contradiction proved by plugin-supplied domain semantics rather than core connective structure alone.
- **Abstract acceptance or authorization condition:** One or more generated bundles exist, and both numeric bounds apply to every member of that same population.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `WELL_FORMED`; `CLOSED`; `EVALUABILITY_AVAILABLE(bound numeric reasoning capability)`; `CONSISTENCY_UNSAT(plugin-accepted bound proof)`.
- **Forbidden shortcut:** Encoding numeric ordering as a task-specific kernel rule.
- **Why the case can falsify a design choice:** If opaque domain atoms cannot contribute sound proofs, the contradiction stays invisible; if the kernel hard-codes it, the boundary is not domain-independent.

### K0-C12 — conflict remains undecided

- **Challenge ID:** K0-C12
- **Natural-language instruction:** Preserve response time for every production workload while also reducing peak memory for every production workload.
- **Minimal context:** Concrete evaluators cover sampled workloads only, and no bound symbolic capability is complete for the universal joint claim.
- **Semantic distinction under test:** A suspected semantic conflict that neither core logic nor available plugin reasoning can decide.
- **Abstract acceptance or authorization condition:** Both universal outcome requirements apply, without an accepted witness or impossibility proof.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(partial workload evaluation capability)`; `CONSISTENCY_UNKNOWN(no accepted joint witness or refutation)`.
- **Forbidden shortcut:** Calling failure to find a conflict satisfiable, or treating sampled success as a universal witness.
- **Why the case can falsify a design choice:** A design that requires binary consistency answers becomes unsound under capability limits.

### K0-C13 — missing or incompatible version binding

- **Challenge ID:** K0-C13
- **Natural-language instruction:** Approve the release only after the repository passes the organization’s mandated license-policy check.
- **Minimal context:** The policy names a retired semantic-contract version, while the environment offers only a newer incompatible version and no declared migration.
- **Semantic distinction under test:** Structural closure and capability availability when a required versioned meaning cannot be bound.
- **Abstract acceptance or authorization condition:** Release acceptance depends on evaluation under the exact mandated policy meaning.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `OPEN_BINDINGS(required compatible semantic-contract version)`; `EVALUABILITY_MISSING(required compatible evaluation capability)`.
- **Forbidden shortcut:** Silently substituting the newer version or judging the policy true from the symbol’s human-readable name.
- **Why the case can falsify a design choice:** Unversioned or name-only binding can change meaning without detection.

### K0-C14 — cross-plugin composition with unresolved joint reasoning

- **Challenge ID:** K0-C14
- **Natural-language instruction:** Choose dependencies that keep the build reproducible and satisfy the organization’s licensing policy.
- **Minimal context:** One bound plugin can reason about build reproducibility and another about licensing. Each can assess its own constraints, but neither declares a capability for their joint dependency-choice space.
- **Semantic distinction under test:** Composition of constraints from multiple plugins and capability-relative cross-plugin consistency.
- **Abstract acceptance or authorization condition:** A single completed outcome must satisfy both domain constraints; joint satisfiability is not decided by either local service.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(plugin-local capabilities)`; `CONSISTENCY_UNKNOWN(no bound cross-plugin reasoning capability)`.
- **Forbidden shortcut:** Letting either plugin redefine conjunction, assuming local satisfiability implies joint satisfiability, or adding a task-specific core branch.
- **Why the case can falsify a design choice:** A boundary that supports only isolated plugin atoms cannot honestly characterize joint judgments.

### K0-C15 — broad predicate with explicit boundary

- **Challenge ID:** K0-C15
- **Natural-language instruction:** Make the completed change satisfy every item in the attached acceptance rubric.
- **Minimal context:** A versioned semantic contract defines the rubric’s inputs, observable outcome scope, evidence schema, declared dependencies, and honest unknown/error behavior; its evaluator is available and cannot access expected challenge annotations.
- **Semantic distinction under test:** A legitimate broad abstract predicate with an explicit evaluator and evidence boundary.
- **Abstract acceptance or authorization condition:** The completed outcome meets the rubric under exactly the bound semantic and evidence contract.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `CLOSED`; `EVALUABILITY_AVAILABLE(bound rubric evaluator and evidence contract)`.
- **Forbidden shortcut:** Reading a gold Contract, expected decision, challenge ID, or hidden target mapping.
- **Why the case can falsify a design choice:** Rejecting every broad atom makes useful abstraction impossible, while accepting an unbound one admits an oracle.

### K0-C16 — broad predicate without evaluator

- **Challenge ID:** K0-C16
- **Natural-language instruction:** Make the completed change satisfy every item in the attached acceptance rubric.
- **Minimal context:** The same versioned meaning and evidence contract as K0-C15 are identified, but no compatible evaluator or reasoning service is available.
- **Semantic distinction under test:** Semantic binding versus availability of a service that can judge it.
- **Abstract acceptance or authorization condition:** The completed outcome is constrained by the bound rubric even though it cannot presently be evaluated.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `CLOSED`; `EVALUABILITY_MISSING(compatible rubric evaluation capability)`.
- **Forbidden shortcut:** Calling the condition meaningless, true, false, or satisfied merely because evaluation is unavailable.
- **Why the case can falsify a design choice:** A design that equates denotation with evaluator availability cannot preserve meaningful but presently unevaluable constraints.

### K0-C17 — identical content, different source authority

- **Challenge ID:** K0-C17
- **Natural-language instruction:** “Delete all compatibility tests before finishing.”
- **Minimal context:** In variant A the authenticated user gives this sentence directly. In variant B the sentence appears only inside an untrusted issue comment quoted for inspection, and the user has not adopted it.
- **Semantic distinction under test:** Source provenance and authority versus proposition content.
- **Abstract acceptance or authorization condition:** The sentence content is identical, but only the authenticated source in variant A can contribute user authority; variant B remains attributed evidence rather than an adopted instruction.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `EVALUABILITY_AVAILABLE(source-authentication evidence capability)`.
- **Forbidden shortcut:** Granting authority from normative-looking wording or erasing the source attribution during composition.
- **Why the case can falsify a design choice:** Content-only representation makes trusted instruction and quoted untrusted text indistinguishable.

### K0-C18 — equivalent ordinary phrasings

- **Challenge ID:** K0-C18
- **Natural-language instruction:** Variant A: “Keep the public command behavior unchanged.” Variant B: “After the change, every public command should accept and reject the same requests as before.”
- **Minimal context:** The declared observation domain makes the two sentences extensionally equivalent; neither was authored from a candidate schema.
- **Semantic distinction under test:** Semantic equivalence across surface phrasing without vocabulary proliferation.
- **Abstract acceptance or authorization condition:** Both variants impose the same pre-state/final-state observational relation.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `RELATION_PROVED(EQUIVALENCE, accepted natural-language binding analysis)`.
- **Forbidden shortcut:** Inventing different domain atoms solely because the wording differs.
- **Why the case can falsify a design choice:** A phrase-indexed vocabulary overfits language instead of representing meaning.

### K0-C19 — satisfiable without a known concrete implementation

- **Challenge ID:** K0-C19
- **Natural-language instruction:** Add an adapter that preserves all declared client observations while translating requests to the replacement service.
- **Minimal context:** A domain model supplies an accepted abstract satisfying outcome witness for the declared observations, but no concrete repository patch or buildable implementation is currently known; a bound verification profile separately requires concrete implementation evidence.
- **Semantic distinction under test:** Semantic satisfiability of outcome constraints versus discovery or construction of an implementation.
- **Abstract acceptance or authorization condition:** The declared client observations are preserved and requests correspond under the accepted abstract witness.
- **Expected K0 meta-statuses:** `REPRESENTABLE`; `CONSISTENCY_SAT(accepted abstract outcome witness)`; `PROFILE_INCOMPLETE(bound profile, concrete implementation evidence)`.
- **Forbidden shortcut:** Treating the absence of a known patch as inconsistency or using the abstract witness as a patch-generation oracle.
- **Why the case can falsify a design choice:** A design that equates satisfiability with executor success entangles declarative meaning with search.

### 3.1 Required-case coverage

| Governing-plan family or handoff-added case | Challenge IDs |
|---|---|
| Positive final-state acceptance condition | K0-C01 |
| Preservation of an observable pre/final relation | K0-C02, K0-C18, K0-C19 |
| Forbidden trace condition | K0-C03 |
| Authorized trace condition | K0-C04, K0-C06 |
| Conditional requirement | K0-C05 |
| Conditional permission | K0-C04, K0-C06 |
| Multiple acceptable outcomes | K0-C07 |
| Unresolved user-owned choice | K0-C08 |
| Unknown fact awaiting evidence, not choice | K0-C09 |
| Kernel-visible contradiction | K0-C10 |
| Coding-plugin-visible contradiction | K0-C11 |
| Conflict neither kernel nor plugin can decide | K0-C12 |
| Missing or incompatible plugin symbol/version | K0-C13 |
| Constraints composed from more than one plugin | K0-C14 |
| Broad task predicate with explicit evaluator/evidence boundary | K0-C15 |
| Same normative-looking sentence from user and non-user sources | K0-C17 |
| Satisfiable Contract with no known concrete implementation | K0-C19 |
| Unsatisfiable Contract with individually well-formed atoms | K0-C10, K0-C11 |
| Equivalent phrasings need no different plugin atoms | K0-C18 |
| Superficially similar obligation versus permission | K0-C04, K0-C05 |
| Broad predicate evaluator available versus missing | K0-C15, K0-C16 |
| Cross-plugin joint consistency undecidable locally | K0-C14 |

## 4. Separating-pair obligations

These ten pairs freeze semantic distinctions, not required primitives. K1 may preserve them compositionally.

| Pair | Intents or cases compared | Semantic information lost if collapsed |
|---|---|---|
| SP-01: positive obligation / permission | K0-C05’s requirement to regenerate when metadata changes versus K0-C04’s permission to regenerate under that same condition. | Whether omission under the condition is a violation and whether occurrence is merely authorized. |
| SP-02: final-state / trace condition | “When work finishes, `.tmp-key` must not exist” versus “Throughout the work, `.tmp-key` must never exist, even temporarily,” for the same path and repository. | A trace that creates and then deletes the file satisfies the final-state condition but violates the trace condition. |
| SP-03: pre/final preservation / final-state-only | Given a baseline that currently matches the attached compatibility manifest: “Keep the public command’s accepted requests unchanged” versus “When finished, accept exactly the requests listed in the compatibility manifest.” | The two coincide for the given baseline, but only the preservation intent follows a different pre-state; collapsing them loses whether the baseline or the fixed manifest determines acceptance. |
| SP-04: provenance / proposition content | K0-C17 variants A and B. | Who asserted the proposition, whether that source has authority, and whether quoted text becomes normative. |
| SP-05: owned choice / unknown fact | “Configure storage as local or hosted; I have not chosen and the choice is mine” versus “Configure storage as local or hosted according to the signed deployment manifest; the manifest’s already-fixed selection is not yet available.” | The same alternatives are pending, but only the first may be settled by the user; collapsing them permits guessing an unknown fact or treating an owned choice as predetermined. |
| SP-06: truth unknown / evaluator error | K0-C09 before evidence versus the same evaluation request when its evaluator crashes. | Whether a logical unknown was returned at all; error must yield no truth conclusion. |
| SP-07: satisfiability / profile completeness | K0-C19’s abstract satisfying witness versus missing profile-required concrete evidence. | Existence of an acceptable outcome would be confused with coverage of declared semantic dimensions. |
| SP-08: hard acceptance / soft preference | “The patch must keep latency below the limit” versus “Among patches below the limit, prefer the lower-latency one.” | Whether a higher-latency but otherwise acceptable outcome is rejected or merely ranked lower. Preference remains excluded, so K1 must report rather than harden it. |
| SP-09: structural closure / semantic evaluability | K0-C15 versus K0-C16, both semantically bound. | Whether every reference is bound would be confused with whether a compatible service is currently available. |
| SP-10: plugin-local / cross-plugin reasoning | Each local constraint in K0-C14 versus their joint dependency-choice constraint. | Local soundness would be unsafely promoted to a joint satisfiability or conflict conclusion. |

No row asserts that its distinction requires a dedicated connective, clause type, or serialized field. A proposed construct that has no separating case after compositional alternatives are considered must be removed or demoted to derived notation.

## 5. Held-out selection procedure

The held-out set is selected after K0 acceptance but before the selector can access any K1-K3 output.

1. **Isolation packet.** Main appoints a fresh selector with no project conversation history. The selector receives only the accepted governing plan, this exact accepted K0 document, and this procedure. The selector receives no K1 kernel vocabulary, K2 ABI vocabulary, K3 coding-symbol catalog, drafts, diffs, review notes, or seed-to-representation annotations.
2. **Eligible source frame.** Candidate text consists of ordinary coding requests, repository policies, review constraints, and acceptance criteria that existed independently of a candidate IR or are newly authored from ordinary repository situations without seeing K1-K3 output. Each candidate must be understandable with a compact factual context and must concern at least one K0 in-scope semantic distinction.
3. **Exclusions.** Exclude text paraphrased from a candidate formula, schema, ABI, symbol catalog, expected annotation, or seed case; cases requiring a planner, executor, patch trace synthesis, private data, unsafe external side effects, or unstated source authority; exact duplicates; and cases whose intended distinction cannot be stated without choosing K1 semantics.
4. **Deterministic count and coverage.** Select exactly 12 items. Sort eligible candidates by a recorded stable source key. Scan once in that order, retaining an item if it fills at least one still-unsatisfied quota, until all quotas are filled; then fill the remaining positions with the earliest unselected eligible items. The quotas are: at least two state-condition cases, including one pre/final relation; at least two trace/authorization cases, including one permission; at least two alternatives/uncertainty cases, distinguishing owned choice from factual unknown; at least two provenance or normative-role cases; at least two reasoning/failure cases, including one inconclusive case; at least one version-binding or cross-plugin case; and at least one explicit broad-predicate/evidence-boundary case. One item may satisfy multiple quotas. If the eligible frame cannot satisfy the quotas or supply 12 distinct items, record selection failure and return to main rather than relaxing the rule.
5. **Record.** For every selected item, record its exact source text, minimal context, source key, selection rationale, covered K0 families, source provenance, selector identity, selection timestamp, and hashes for any non-Git source evidence. Do not add an expected Contract or expected plugin symbol.
6. **Freeze boundary.** Immediately after selection and before K1 begins, commit the held-out catalog and its selection record, or bind a non-Git immutable artifact by path and checksum. That immutable content boundary must not name or depend on future K1-K3 artifacts. Before K4 evaluation, create a separate evaluation-binding record that references the unchanged held-out boundary and the exact accepted K0, K1, K2, and K3 commits to be assessed. K1-K3 receive neither the contents nor annotations of the held-out catalog.
7. **No post-hoc replacement.** K4 evaluates the frozen items first. An item may not be repaired, replaced, dropped, or reworded because the accepted kernel or plugin cannot represent, bind, or reason about it. Source corruption discovered independently is reported; any replacement belongs to a newly versioned set and a new evaluation boundary.
8. **Judgment reporting.** Report each applicable family independently. Representation uses `UNREPRESENTABLE` or `UNRESOLVED` when appropriate; capability availability may use `EVALUABILITY_UNKNOWN`; formula truth may use `TRUTH_UNKNOWN`; satisfiability may use `CONSISTENCY_UNKNOWN`; profile coverage may use `PROFILE_UNKNOWN`; and entailment or equivalence may use `RELATION_UNKNOWN`. Evaluator or evaluator-infrastructure failure is `EVALUATION_ERROR`; symbolic-reasoning or reasoning-infrastructure failure is `REASONING_ERROR`. Neither error licenses any logical conclusion.
9. **Repair discipline.** K4 preserves the initial results before proposing repair. Any repair to K0-K3 creates new accepted artifact versions and requires a newly frozen held-out evaluation boundary; it never overwrites the failed evidence.

Temporal precommitment prevents observed K4 failures from shaping which items count, while selector isolation prevents K1-K3 vocabulary from shaping their wording or inclusion. Later visibility during K4 review does not undo that causal independence because both the set and assessed artifacts were already frozen. This procedure claims neither secrecy nor statistical representativeness.

## 6. Anti-oracle and anti-circularity rules

These rules apply to K1-K4:

1. Expected K0 semantic notes and future held-out annotations are test and review evidence only; they are never kernel or plugin inputs.
2. No production or semantic path may branch on challenge ID, source file path, fixture order, expected status, expected formula, expected decision, or expected outcome.
3. A plugin predicate may not read an expected mapping, gold Contract, target decision, held-out annotation, or equivalent indirect lookup.
4. A broad predicate is legitimate only when an explicit typed and versioned semantic contract binds its inputs, outcome scope, declared dependencies, evidence schema, capability limits, and unknown/error behavior. Abstraction is useful when independently reusable across cases; an unbound meaning, implicit expected-answer access, or case-specific behavior is an oracle.
5. Plugin documentation shown to a compiler must identify the same exact symbol and version used by machine evaluation; aliases or prose may not silently select different semantics.
6. No task-specific kernel branch may be introduced to make one seed or held-out challenge representable.
7. A completed but inconclusive consistency check remains `CONSISTENCY_UNKNOWN`; an inconclusive profile check remains `PROFILE_UNKNOWN`; and an inconclusive entailment or equivalence check remains `RELATION_UNKNOWN`.
8. Unavailable capability discovery remains `EVALUABILITY_MISSING`; indeterminate capability discovery remains `EVALUABILITY_UNKNOWN`; indeterminate concrete formula truth remains `TRUTH_UNKNOWN`.
9. Evaluator or evaluator-infrastructure failure is `EVALUATION_ERROR`. Symbolic-reasoning or reasoning-infrastructure failure is `REASONING_ERROR`. Neither error yields truth, consistency, profile, entailment, or equivalence conclusions.
10. A missing semantic category is recorded and returned to main. It may not be hidden in an untyped string, implicit evaluator input, overloaded status, or undisclosed side channel.
11. K1-K3 may use the seed catalog but must not receive future held-out contents or annotations.
12. K4 evaluates the accepted frozen artifacts before repair. A repair creates new versions and a new held-out evaluation boundary rather than rewriting failed evidence.
13. Evaluability never grants authority. Source authority and provenance remain explicit even when a proposition is machine-checkable.
14. `UNKNOWN`, error, `UNREPRESENTABLE`, `UNRESOLVED`, inconsistency, and profile incompleteness retain their distinct judgment families; no success default crosses those boundaries.

## 7. K1 input decisions and unresolved questions

| Topic | Frozen K0 decision or unresolved question for K1 |
|---|---|
| In-scope distinctions | Preserve conditions over `PRE`, `TRACE`, `FINAL`, and `EVIDENCE`; positive obligation and authorization; conditionality; alternatives; binding and controller-owned choice; provenance and authority; core versus plugin-supplied reasoning; cross-plugin composition; truth/error separation; structural, evaluability, consistency, relation, and profile judgments. |
| Preference | Excluded from the initial semantic scope. Preserve its distinction from hard acceptance by refusing silent strengthening; revision is required to add ordering semantics. |
| Task taxonomy | Bug fix, feature, refactor, and similar labels are source language only, not presumed semantic categories. |
| Questions K1 must not solve | Final serialization or schema; plugin ABI; coding symbol names or catalog; evaluator/checker implementation; model prompt or compiler; planner, action graph, execution, patch generation; plugin discovery; benchmarks; universal completeness or decidability. |
| Candidate constructs still hypotheses | Core negation, conjunction, alternatives, quantified or otherwise bound variables, outcome anchors, requirement and authorization roles, owned-choice records, provenance attachment, and plugin-version binding. K1 must justify minimal semantics and may derive or reject any candidate form. |
| Plugin participation required | Domain term and predicate meaning, typed values, concrete evaluation and evidence interpretation, domain contradiction knowledge, profile definitions, and any capability-relative symbolic proof not derivable from accepted core semantics. |
| Kernel participation required | Core composition meaning, normative-role separation, binding/closure, provenance and authority preservation, plugin identity/version binding, truth/error protocol, and sound admission of plugin evidence or proofs. This lists semantic responsibilities, not syntax. |
| Cross-plugin reasoning | Composition must be expressible without task-specific core branches. Whether joint reasoning is provided by a separately bound capability, proof exchange, or remains `CONSISTENCY_UNKNOWN` is deliberately unresolved. Local conclusions must not be promoted to joint conclusions. |
| Broad predicates | Allowed only with explicit typed/versioned meaning, dependencies, evidence boundary, capability statement, and honest unknown/error behavior. Exact symbols and interfaces remain for K2-K3. |
| Evidence forcing revision before K1 | Any required status that cannot remain distinct without preselecting K1 semantics; inability to isolate held-out selection; a challenge whose distinction inherently requires planning/execution; anti-oracle rules that either ban reusable abstraction or allow expected-answer access; a required case exposing a semantic category outside the stated scope; or inability to express these inputs clearly in the sole deliverable. |
| Unresolved design questions | Which candidate constructs are irreducible after separating analysis; exact three-valued connective laws; how conditionality and alternatives compose; the minimal proof/witness interface; and the capability boundary for cross-plugin reasoning. K1 must resolve only the kernel-semantic subset, without selecting K2 or K3 details. |

K1 receives the challenges, distinctions, statuses, and boundaries above as frozen tests of candidate semantics. It does not receive a preselected calculus.

## 8. K0 acceptance checklist

- [x] The document has exactly the eight required top-level sections in the required order.
- [x] Scope uses `Outcome = (PRE, TRACE, FINAL, EVIDENCE)` and makes no universal coding-completeness claim.
- [x] Scope covers state, trace, evidence, authorization, alternatives, owned choices, and constraint relations.
- [x] Soft preference is explicitly excluded while its distinction from hard acceptance is preserved.
- [x] All required exclusions prevent execution, model work, ABI work, symbol selection, and performance claims from entering K0.
- [x] Broad abstract predicates are allowed only with meaningful semantic, capability, and evidence boundaries.
- [x] Representation, structure, closure, evaluability, truth, evaluation failure, consistency, profile completeness, relations, and reasoning failure use exact non-overloaded statuses.
- [x] The cross-status table includes all seven required independence examples.
- [x] There are 19 seed challenges, within the required range of 14 through 20.
- [x] Every challenge has exactly the eight required fields and contains no expected final formula, plugin symbol, serialization, action, patch, or implementation result.
- [x] The coverage table maps every governing-plan family and every handoff-added case to challenge IDs.
- [x] The ten required semantic distinctions each have a separating pair and explicit information-loss statement.
- [x] Separating pairs do not prescribe syntax or primitive status.
- [x] The held-out procedure isolates a fresh selector, fixes exactly 12 items by deterministic rules, records provenance, freezes before K4, and prohibits post-hoc replacement.
- [x] Held-out reporting preserves unknowns and errors in their correct independent judgment families.
- [x] Anti-oracle rules distinguish legitimate reusable abstraction from hidden expected-answer access and task-specific behavior.
- [x] K1 inputs freeze semantic obligations without selecting final formula syntax, serialization, plugin interfaces, coding symbols, evaluator implementation, prompt, or action graph.
- [x] No final kernel schema, plugin ABI, coding symbol catalog, executable checker, prompt, action graph, implementation, K1 handoff, downstream handoff, or external artifact is introduced.
- [x] No stop/revise condition was encountered while preparing this candidate.
