# K0 handoff — scope, semantic statuses, challenges, and anti-oracle boundary

> Status: review candidate. This document grants no mutation authority until independently accepted and explicitly bound by main.

## 1. Binding and purpose

- Governing plan: `docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md`
- Accepted governing-plan blob: `01f959bc55f644a376f8ffa6059e9e77936be77c`
- Governing-plan acceptance commit: `3533a4b279e78ebe72d3cefeeab4bb1e15bc776c`
- Governing-plan review: `docs/reviews/kernel_plugin/Contract_IR_Kernel_Plugin_Plan_3f7fc69_review.md`
- Stage: `K0`
- Classification: blocking semantic-design input freeze
- Predecessor: accepted governing plan; no prior implementation stage
- Output roots: none

K0 freezes the design inputs needed by K1. It does not select the final kernel syntax, define the plugin ABI, define the coding plugin vocabulary, implement a checker, or evaluate a language model.

The sole K0 deliverable is:

```text
KernelPlugin/K0_Semantic_Design_Inputs_v0.md
```

The executor may mutate exactly that path. It must not edit this handoff, the accepted plan or review, repository navigation, Phase 0/1 material, or any other path. It does not commit.

## 2. Required deliverable structure

The deliverable must contain exactly these top-level sections in order:

1. `Research scope and exclusions`
2. `Semantic status vocabulary`
3. `Seed semantic challenges`
4. `Separating-pair obligations`
5. `Held-out selection procedure`
6. `Anti-oracle and anti-circularity rules`
7. `K1 input decisions and unresolved questions`
8. `K0 acceptance checklist`

The document may use tables and compact pseudocode. It must not define a JSON/YAML serialization, Python data model, evaluator implementation, model prompt, or plan/execution graph.

## 3. Research scope and exclusions

The scope section must define K0's representational universe without claiming universal coding completeness. It must treat a completed abstract outcome as:

```text
Outcome = (PRE, TRACE, FINAL, EVIDENCE)
```

The scope includes natural-language coding intents whose meaning can be discussed as one or more of:

- conditions on pre-state, final-state, trace, or evidence;
- authorization conditions over controlled trace events;
- alternatives or unresolved choices with an identified controller;
- relations among multiple constraints;
- optional preference among otherwise acceptable outcomes, with an explicit K0 decision on whether preference belongs in the initial design scope.

The scope must remain independent of task labels such as bug fix, feature, or refactor. Those labels may appear in source instructions but cannot become presumed kernel categories.

The exclusions must include:

- planning, action selection, state-transition execution, repository mutation, and patch generation;
- concrete operation vocabularies and hierarchical execution graphs;
- final kernel syntax or serialization;
- plugin ABI and coding-plugin symbol selection;
- learned or prompted natural-language compilation;
- plugin retrieval, discovery, installation, or synthesis;
- performance, scalability, benchmark, deployment, or publication claims;
- automatic proof of intent completeness or universal decidability.

The scope must state that arbitrary domain predicates are permitted in principle, including a broad `task_is_correct` predicate, but are not automatically meaningful, evaluable, consistent, or sufficient merely because they are named.

## 4. Semantic status vocabulary

The deliverable must freeze exact, namespaced, non-overloaded K0 terms for distinct judgments. At minimum it must define:

### 4.1 Representation judgment

```text
REPRESENTABLE
UNREPRESENTABLE(reason)
UNRESOLVED(reason)
```

`UNRESOLVED` means the available intent permits multiple semantic bindings or lacks required information. It must not be used as a synonym for plugin inability or logical `UNKNOWN`.

### 4.2 Structural judgment

```text
WELL_FORMED
MALFORMED(reason)

CLOSED
OPEN_BINDINGS(binding_refs)
```

Well-formedness and closure are separate. A well-formed partial Contract may contain explicit open bindings.

### 4.3 Evaluation-capability judgment

```text
EVALUABILITY_AVAILABLE(capability_refs)
EVALUABILITY_MISSING(missing_capability_refs)
EVALUABILITY_UNKNOWN(reason)
```

This judgment concerns whether the requested evaluation or proof service is available. It says nothing by itself about truth or satisfiability.

### 4.4 Formula truth and evaluation failure

```text
TRUTH_TRUE(evidence_refs)
TRUTH_FALSE(evidence_refs)
TRUTH_UNKNOWN(reason, evidence_refs)
EVALUATION_ERROR(reason)
```

`EVALUATION_ERROR` is outside the logical truth domain. `TRUTH_UNKNOWN` must not be rewritten as `TRUTH_TRUE` or `TRUTH_FALSE`. These names preserve the governing plan's logical values `TRUE | FALSE | UNKNOWN` while preventing collision with unknown results in other judgment families.

### 4.5 Consistency judgment

```text
CONSISTENCY_SAT(witness_ref)
CONSISTENCY_UNSAT(proof_or_core_ref)
CONSISTENCY_UNKNOWN(reason)
```

`CONSISTENCY_SAT` requires a valid satisfying witness under the bound semantics; `CONSISTENCY_UNSAT` requires a valid proof or unsatisfiable core under the bound reasoning capability. If the bound reasoning service completes without deriving either, the result is `CONSISTENCY_UNKNOWN`, not `CONSISTENCY_SAT`. A reasoning-service or infrastructure failure is `REASONING_ERROR` under section 4.7 and produces no consistency judgment.

### 4.6 Profile-relative completeness judgment

```text
PROFILE_COMPLETE(profile_ref, evidence_refs)
PROFILE_INCOMPLETE(profile_ref, missing_dimensions)
PROFILE_UNKNOWN(profile_ref, reason)
```

Profile completeness is relative to an explicit versioned profile. It cannot be promoted to intent completeness.

### 4.7 Entailment, equivalence, and reasoning-service failure

```text
RELATION_PROVED(ENTAILMENT | EQUIVALENCE, proof_ref)
RELATION_DISPROVED(ENTAILMENT | EQUIVALENCE, counterexample_ref)
RELATION_UNKNOWN(ENTAILMENT | EQUIVALENCE, reason)
REASONING_ERROR(reason)
```

`RELATION_UNKNOWN` means the bound reasoning service completed without proving or disproving the requested relation. `REASONING_ERROR` is outside the semantic relation judgment and produces no entailment or equivalence conclusion. Formula-evaluator or evaluator-infrastructure failure remains `EVALUATION_ERROR` under section 4.4 and likewise produces no truth, consistency, profile, entailment, or equivalence conclusion.

The deliverable must include a cross-status table showing which judgments are independent. It must include at least these examples:

- well-formed but open;
- closed but not evaluable;
- evaluable but consistency unknown;
- satisfiable but profile-incomplete;
- profile-complete but not certifiably intent-complete;
- evaluator error without a logical conclusion;
- reasoning-service error without a consistency, entailment, or equivalence conclusion.

## 5. Seed semantic challenges

The seed catalog is a design input for K1-K3, not an expected-IR dataset. It must contain at least fourteen challenges and no more than twenty. Each challenge must have exactly these fields:

```text
Challenge ID
Natural-language instruction
Minimal context
Semantic distinction under test
Abstract acceptance or authorization condition
Expected K0 meta-statuses
Forbidden shortcut
Why the case can falsify a design choice
```

The catalog must cover every challenge family named in section 7 of the governing plan. It must additionally include:

- the same normative-looking sentence attributed separately to user and non-user sources;
- a satisfiable Contract that has no currently known concrete implementation;
- an unsatisfiable Contract whose atomic predicates are individually well-formed;
- two semantically equivalent phrasings that should not require different plugin atoms;
- two superficially similar instructions that differ only in obligation versus permission;
- a broad `task_is_correct` predicate whose evaluator is available, and a paired case whose evaluator is missing;
- at least one cross-plugin constraint whose joint consistency is not decidable from either plugin alone.

Expected K0 meta-statuses must use only the frozen status vocabulary. They must not contain an expected final kernel formula, plugin symbol name, serialized IR, action, patch, decision, or result.

Natural-language instructions must not be written by paraphrasing a proposed final IR. They should resemble ordinary coding requests, repository policies, review requirements, or acceptance statements. Minimal context may define abstract facts needed to make a distinction precise, but it cannot include the expected representation.

## 6. Separating-pair obligations

K0 does not decide the final primitive set. It freezes pairs that later proposals must distinguish.

The deliverable must include at least one separating pair for each of these candidate distinctions:

- positive obligation versus permission;
- final-state condition versus trace condition;
- pre/final preservation relation versus final-state-only condition;
- source provenance versus proposition content;
- unresolved user choice versus unknown environmental fact;
- logical `UNKNOWN` versus evaluator `ERROR`;
- satisfiability versus profile completeness;
- hard acceptance versus soft preference, whether preference is retained or explicitly excluded;
- structural closure versus semantic evaluability;
- plugin-local reasoning versus cross-plugin reasoning.

Each pair must state exactly what semantic information would be lost if the distinction were removed. It must not assert that a particular syntax or primitive is required when the distinction could be preserved compositionally.

## 7. Held-out selection procedure

The deliverable must freeze a procedure, not the final held-out tasks. The procedure must ensure that held-out challenges are selected without access to the final K1 kernel vocabulary, K2 plugin ABI vocabulary, or K3 coding-plugin symbol catalog.

The procedure must specify:

- selector independence: a fresh selector receives this accepted K0 deliverable, the accepted governing plan, and the selection protocol only; it receives no K1-K3 outputs or conversation history;
- an eligible source frame consisting of ordinary coding requests, repository policies, review constraints, and acceptance criteria not authored as paraphrases of a candidate IR;
- inclusion and exclusion rules;
- minimum semantic-family coverage;
- a fixed task count or deterministic count rule;
- exact recording of source text, minimal context, selection rationale, and provenance;
- a commit or artifact boundary fixed before K4 evaluation begins;
- prohibition on replacing, repairing, or dropping a held-out item because the accepted kernel or plugin cannot represent it;
- required judgment-family reporting when appropriate: `UNREPRESENTABLE` or `UNRESOLVED` for representation; `EVALUABILITY_UNKNOWN` for capability availability; `TRUTH_UNKNOWN` for formula truth; `CONSISTENCY_UNKNOWN` for satisfiability; `PROFILE_UNKNOWN` for profile coverage; and `RELATION_UNKNOWN` for entailment or equivalence;
- required `EVALUATION_ERROR` or `REASONING_ERROR` reporting for evaluator, reasoning-service, or infrastructure failure, with no logical conclusion inferred from the failure.

The procedure must explicitly explain why temporal precommitment and selector isolation provide design independence even if the held-out tasks are later visible during K4 review. It must not claim statistical representativeness or secrecy.

## 8. Anti-oracle and anti-circularity rules

The deliverable must freeze rules that apply to K1-K4. At minimum:

- expected K0 semantic notes and future held-out annotations are test/review evidence, never kernel or plugin inputs;
- no production or semantic path may branch on challenge ID, source file path, fixture order, expected status, expected formula, or expected outcome;
- a plugin predicate may not read an expected mapping, gold Contract, or target decision;
- a broad predicate is allowed only through an explicit typed/versioned semantic and evidence contract;
- plugin documentation shown to a compiler must identify the same exact symbol/version used by machine evaluation;
- no task-specific kernel branch may be introduced to make one challenge representable;
- a completed but inconclusive consistency check must remain `CONSISTENCY_UNKNOWN`; an inconclusive profile check must remain `PROFILE_UNKNOWN`; and an inconclusive entailment or equivalence check must remain `RELATION_UNKNOWN`;
- unavailable or indeterminate capability discovery must remain `EVALUABILITY_MISSING` or `EVALUABILITY_UNKNOWN`, and indeterminate concrete formula truth must remain `TRUTH_UNKNOWN`;
- evaluator or evaluator-infrastructure failure must be `EVALUATION_ERROR`, and symbolic reasoning or reasoning-infrastructure failure must be `REASONING_ERROR`; neither error yields a truth, consistency, profile, entailment, or equivalence conclusion;
- a missing semantic category must be recorded and returned to main rather than hidden inside an untyped string or an evaluator with implicit inputs;
- K1-K3 may use seed challenges but must not receive the future held-out challenge contents;
- K4 must evaluate the accepted artifacts before any repair; any repair creates a new version and a new held-out evaluation boundary rather than rewriting the failed evidence.

The rules must distinguish a legitimate abstract predicate from a hidden oracle: abstraction is allowed, but implicit expected-answer access, case-specific behavior, or an unbound meaning is not.

## 9. K1 input decisions and unresolved questions

K0 must end with a compact decision table containing:

- exact in-scope semantic distinctions K1 must preserve;
- exact excluded questions K1 must not solve;
- candidate constructs that remain hypotheses rather than frozen primitives;
- whether soft preference is included in the initial semantic scope;
- which judgments require plugin participation;
- which cross-plugin reasoning questions remain deliberately unresolved;
- what evidence would force plan or K0 revision before K1.

This section must not select final formula syntax, serialization, plugin interfaces, or coding symbols.

## 10. Required verification

The executor must run and return:

```text
git diff --check
```

It must also report:

- exact changed paths, which must be only `KernelPlugin/K0_Semantic_Design_Inputs_v0.md`;
- counts for seed challenges and separating pairs;
- a coverage table mapping every governing-plan challenge family and every handoff-required additional case to challenge IDs;
- a checklist showing all required top-level sections in exact order;
- confirmation that no final kernel schema, plugin ABI, coding symbol catalog, executable checker, prompt, or action graph was introduced;
- external artifacts and checksums, which must be `none`.

## 11. Acceptance criteria

K0 may be accepted only if:

- every required section and status distinction is exact and internally consistent;
- scope and exclusions prevent execution or model work from entering K0;
- challenge statements are independent natural-language design inputs rather than reverse verbalizations of an IR;
- semantic targets are abstract enough not to preselect kernel syntax or plugin symbols;
- every required distinction has a separating pair and a stated information loss;
- held-out selection prevents K1-K3 vocabulary feedback and prohibits post-hoc task replacement;
- anti-oracle rules permit legitimate abstract predicates while blocking hidden expected mappings;
- unknown, error, unrepresentable, unresolved, inconsistency, and incompleteness are not conflated;
- K1 receives sufficient frozen design inputs without being told its final design;
- no claim exceeds the K0 challenge scope.

Stop and return to main if the executor finds that:

- a required status cannot be defined without choosing K1 kernel semantics;
- the held-out procedure cannot isolate selection from K1-K3 vocabulary;
- a challenge requires planning or execution semantics to state its intended distinction;
- the anti-oracle rules would prohibit all useful abstract predicates or permit implicit expected-answer access;
- the single allowed deliverable cannot express the required K0 design inputs clearly.

## 12. Return packet

Return exactly:

1. changed path;
2. concise section summary;
3. seed challenge count and separating-pair count;
4. coverage table;
5. verification commands and exact results;
6. unresolved questions and stop conditions encountered;
7. external artifacts and checksums;
8. explicit confirmation that no implementation, K1 handoff, or downstream authority was created.

The executor must not commit. Main freezes any accepted candidate diff and then dispatches a fresh independent read-only review against this exact handoff and blob.
