# Contract IR Minimal Kernel and Coding Plugin Research Plan

> Status: planning candidate authorized for drafting on 2026-08-27. This document grants no implementation, experiment, deletion, or stage-dispatch authority until it is independently reviewed and accepted.

## 1. Route decision

The project pauses the controlled-code Phase 1 milestone after accepted C0 commit `4e3135b` on branch `milestone/phase1-controlled-code-planning`. No C1 handoff exists. The branch remains intact as historical evidence and is not merged into `main`.

Phase 0 and the paused Phase 1 may provide reusable counterexamples, terminology, tests, or implementation fragments, but neither defines the new kernel. Reuse is optional and must be justified against the accepted new semantics. Deletion is unnecessary during design and is not authorized by this plan.

The project now asks a prior question:

> Can a minimal, domain-independent Contract IR kernel define how declarative constraints are formed, composed, validated, and reasoned about, while versioned plugins define the domain-specific types, functions, predicates, evaluators, evidence, and optional symbolic reasoning needed for coding tasks?

This milestone designs that semantic boundary before resuming execution, repository grounding, learned compilation, or model evaluation.

## 2. Intended semantic boundary

Contract IR describes constraints over an abstract execution trace. It does not prescribe how an executor searches for or produces that trace.

The kernel owns:

- formula construction and composition;
- normative roles such as hard requirement and authorization;
- typed variables, binding, and unresolved choices;
- provenance and authority attachment;
- plugin symbol identity and version binding;
- truth and failure protocols;
- structural validation, normalization, and proof/witness interfaces;
- the meanings of well-formedness, closure, evaluability, consistency, and profile-relative completeness.

Plugins own:

- domain types and values;
- atomic functions and predicates;
- predicate scope over abstract pre-state, final-state, trace, and evidence references;
- concrete evaluators and evidence schemas;
- optional encodings, satisfiability checks, entailment checks, equivalence checks, proofs, models, and counterexamples;
- domain completeness profiles;
- model-facing symbol documentation.

A plugin may add atoms but may not redefine kernel connectives, truth values, authority, provenance, binding, or failure semantics.

## 3. Denotational target

The design must define an abstract completed execution without defining a planner or executor:

```text
Outcome = (PRE, TRACE, FINAL, EVIDENCE)
```

A Contract denotes constraints over `Outcome`, plus authorization conditions over controlled trace events and ownership for unresolved choices. If soft preferences remain in scope after the challenge analysis, they denote an ordering over otherwise acceptable outcomes rather than a hard truth condition.

The design must keep the following separate:

- representability: whether an in-scope intent has an equivalent Contract;
- well-formedness: whether the Contract obeys kernel and plugin schemas;
- closure: whether every required symbol, reference, and variable is bound;
- evaluability: whether required plugin semantics are available for the requested judgment;
- consistency: whether satisfiability is proved, contradiction is proved, or neither is known;
- profile-relative completeness: whether a declared plugin profile's required semantic dimensions are covered;
- intent completeness: whether the Contract captures everything the user meant, which cannot be certified from the Contract alone.

## 4. Initial kernel hypothesis

The first design candidate, not yet a frozen schema, is:

```text
Term :=
    Literal
  | Variable
  | PRE | FINAL | TRACE | EVIDENCE
  | PluginFunction(Term*)

Atom := PluginPredicate(Term*)

Formula :=
    Atom
  | NOT Formula
  | ALL_OF(Formula*)
  | ANY_OF(Formula*)
  | EXISTS Variable:Type WHERE Formula

Clause :=
    REQUIRE Formula
  | AUTHORIZE Principal, Formula

Contract :=
    Clauses
  + OwnedChoices
  + Provenance
  + PluginBindings
```

This candidate must be minimized through separating counterexamples. `GOAL`, `PRESERVE`, `FORBID`, and `ALLOW` are initially treated as possible derived forms rather than assumed primitives:

```text
GOAL p      := REQUIRE p(FINAL)
PRESERVE f  := REQUIRE equal(f(PRE), f(FINAL))
FORBID e    := REQUIRE NOT occurs(e, TRACE)
ALLOW e     := AUTHORIZE principal, occurs(e, TRACE)
```

The design must reject a derivation when it loses semantics. A readable construct may remain standard syntax without becoming an irreducible kernel primitive.

An atomic requirement such as the following is valid in principle:

```text
REQUIRE coding.task_is_correct@v1(task_spec, FINAL, EVIDENCE)
```

It is meaningful only when the bound plugin supplies a typed signature, versioned denotation or evaluation contract, declared dependencies, evidence contract, and honest unknown/error behavior. An abstract predicate is not rejected merely because the kernel cannot inspect its domain semantics.

## 5. Truth, failure, and reasoning discipline

Logical evaluation must distinguish:

```text
TRUE | FALSE | UNKNOWN
```

Plugin or infrastructure failure is not a truth value:

```text
EvaluationResult = VALUE(TRUE | FALSE | UNKNOWN, evidence) | ERROR(reason)
```

The kernel must define exact composition rules for its connectives. No plugin may treat `UNKNOWN` as `TRUE` or `FALSE`, and no error may be rewritten as a logical conclusion.

Reasoning is sound and capability-relative, not universally complete. A plugin may declare one of at least these capability classes:

```text
CONCRETE_EVALUATION_ONLY
PARTIAL_SYMBOLIC_REASONING
COMPLETE_FOR_DECLARED_FRAGMENT
```

The kernel may report contradiction only with a valid kernel derivation or plugin proof/witness accepted under the bound capability contract. Failure to prove conflict means `UNKNOWN`, not consistency. The same rule applies to entailment and equivalence.

## 6. Coding plugin design target

The first coding plugin tests the extension boundary; it does not attempt to enumerate coding task kinds. It must not introduce `FIX_BUG`, `ADD_FEATURE`, or `REFACTOR` as kernel concepts.

Candidate reusable types include:

```text
TaskSpec
RepositoryState
Path
PathSet
Artifact
ChangeSet
TestSuite
VerificationEvidence
```

Candidate reusable functions and predicates include state projections, change-set queries, task acceptance, test evidence, path-scope checks, public-interface comparison, and dependency-state comparison. The exact vocabulary must be derived from semantic challenges rather than frozen by this roadmap.

The plugin must demonstrate that:

- a broad predicate such as `task_is_correct` can be bound without hidden expected-answer access;
- state projections compose with kernel formulas;
- coding-specific conflict or entailment knowledge can be supplied without changing the kernel;
- plugin reasoning limitations remain explicit;
- new coding atoms do not acquire authority merely by being evaluable;
- model-facing documentation and machine-facing semantics bind the same exact symbol and version.

## 7. Semantic challenge method

Design proceeds from independent natural-language tasks and semantic counterexamples, not from schemas chosen to make existing fixtures pass.

The seed set must cover at least:

- a positive final-state acceptance condition;
- preservation of an observable relation between pre-state and final-state;
- forbidden and authorized trace conditions;
- conditional requirements and permissions;
- multiple acceptable outcomes;
- an unresolved user-owned choice;
- a fact that is unknown until evidence is available but is not a discretionary choice;
- a kernel-visible contradiction;
- a coding-plugin-visible contradiction;
- a conflict that neither kernel nor plugin can decide;
- a missing or incompatible plugin symbol/version;
- composition of constraints from more than one plugin;
- a broad task predicate with an explicit evaluator and evidence boundary.

For each proposed kernel construct, the plan must provide a separating pair of intents that become indistinguishable if the construct is removed. Constructs without a separating counterexample are removed or demoted to derived syntax.

At least one held-out challenge set must be selected independently of the final candidate vocabulary. Unrepresentable cases are recorded as `UNREPRESENTABLE`; unavailable reasoning is recorded as `UNKNOWN`. Neither may be repaired with an opaque expected lookup or a task-specific kernel branch.

## 8. Coarse progressive stages

Only the next stage may receive a concrete handoff after this plan is independently accepted. The stages below are a dependency roadmap, not mutation authority.

| Stage | Objective | Exit question |
|---|---|---|
| K0 | Freeze research scope, semantic status vocabulary, seed challenges, held-out selection procedure, and anti-oracle rules | Are the design inputs independent enough to falsify the proposed boundary? |
| K1 | Define the kernel calculus and denotational semantics on the accepted K0 challenges | Does every retained construct have exact semantics and a separating counterexample? |
| K2 | Define the versioned plugin ABI, truth/evidence protocol, and capability-relative reasoning interface | Can plugins add atoms and reasoning without changing kernel meaning? |
| K3 | Define the minimal coding plugin against the accepted kernel and ABI | Can the coding challenges be represented without coding-specific kernel branches? |
| K4 | Perform held-out semantic closure and manual natural-language-to-Contract binding assessment | What remains unrepresentable, unresolved, ambiguous, or only capability-relative? |

No stage may implement planning, state-transition execution, patch generation, repository mutation, model training, model inference, prompt search, or benchmarks. A later executable reference checker requires a separately accepted successor plan after K4.

## 9. Acceptance and stop/revise criteria

The design milestone may be accepted only if:

- the kernel has an explicit denotation independent of serialization;
- every irreducible kernel construct has a separating counterexample;
- derived syntax is identified as derived rather than given independent semantics;
- plugin symbols are typed, namespaced, versioned, and bound to matching model-facing and machine-facing contracts;
- structural completeness, plugin-profile completeness, and intent completeness are not conflated;
- all judgments distinguish proved truth, proved falsehood, unknown, and evaluation error;
- broad predicates are permitted only through explicit plugin contracts and evidence boundaries;
- the coding plugin adds no new kernel semantics;
- held-out challenges preserve all failures rather than triggering ad hoc kernel expansion;
- conclusions remain limited to the accepted challenge scope.

Stop and revise if:

- plugins must redefine core connectives, truth, authority, or provenance;
- cross-plugin composition requires task-specific kernel branches;
- a retained primitive has no semantic distinction from a composition of other constructs;
- completeness or consistency can be reported only by treating `UNKNOWN` as success;
- the coding plugin can appear complete only through hidden expected mappings;
- manual source-to-symbol binding repeatedly requires guessing rather than explicit unresolved representation;
- the held-out tasks expose a missing semantic category that cannot be expressed by plugin atoms and existing kernel composition.

## 10. Allowed conclusion

Passing this milestone may establish only that a specific minimal kernel and plugin protocol are semantically coherent and adequate for the accepted coding challenge scope. It cannot establish universal semantic completeness, learned natural-language compilation quality, execution reliability, coding-agent performance, plugin discovery quality, or a benefit over self-contained IR.

Those claims require later, separately planned experiments after the semantic boundary is accepted.

## 11. Provenance and process

- This milestone uses branch `milestone/contract-kernel-plugin-design` from clean `main` commit `787378d3763e584c9e9cc66aa699154641975a6b`.
- Historical Phase 0 and paused Phase 1 artifacts are not modified during semantic design.
- Each accepted stage, review repair, and report is committed without rewriting reviewed history.
- Concrete stage handoffs are generated just in time and independently reviewed before dispatch.
- The main thread owns semantic decisions, stage acceptance, review resolution, and the commit gate.
- No implementation evidence or scientific claim may rely on uncommitted or superseded artifacts.
