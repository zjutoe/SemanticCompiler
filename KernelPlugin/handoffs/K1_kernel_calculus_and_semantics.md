# K1 handoff — minimal kernel calculus and denotational semantics

> Status: review candidate. This document grants no mutation authority until independently accepted, the held-out prerequisite is satisfied, and main explicitly binds an exact clean source commit.

## 1. Binding and purpose

- Governing plan: `docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md`
- Accepted governing-plan blob: `01f959bc55f644a376f8ffa6059e9e77936be77c`
- Governing-plan acceptance commit: `3533a4b279e78ebe72d3cefeeab4bb1e15bc776c`
- Accepted K0 deliverable: `KernelPlugin/K0_Semantic_Design_Inputs_v0.md`
- Accepted K0 deliverable blob: `e86e184300a6620fb6fe25062635d9bc7cb410a1`
- K0 acceptance commit: `d6554e33c7c7d3ba2b4b29ffced446b032b00c63`
- K0 acceptance record: `docs/reviews/kernel_plugin/K0_Design_Inputs_6ad555e_review.md`
- Stage: `K1`
- Classification: blocking kernel-semantic design
- Predecessor: accepted K0; no K1 implementation or held-out evaluation
- External output roots: none

K1 defines the smallest justified domain-independent kernel calculus and its denotational semantics against the accepted K0 inputs. It must decide which candidate kernel constructs are irreducible, derived, delegated to plugin semantics, or excluded. It does not define a serialization, plugin ABI, coding vocabulary, executable checker, compiler, planner, or evaluator.

The sole K1 deliverable is:

```text
KernelPlugin/K1_Kernel_Calculus_and_Denotational_Semantics_v0.md
```

After explicit dispatch, the executor may mutate exactly that path. It must not edit this handoff, accepted plans or reviews, K0, repository navigation, held-out material, Phase 0/1 material, or any other path. It does not commit.

## 2. Pre-dispatch held-out gate

Creating or accepting this handoff does not start K1. Before K1 is bound to an executor, main must confirm that the accepted K0 held-out procedure has been executed:

- a fresh selector received only the accepted plan, accepted K0 deliverable, and K0 selection procedure;
- exactly twelve items satisfying the frozen deterministic coverage rule were selected;
- the catalog and selection record were made immutable before K1 execution;
- the immutable content boundary and selector provenance are recorded for later K4 use;
- the K1 binding packet contains only an opaque prerequisite receipt, not held-out text, annotations, expected representations, artifact paths, or a resolvable content reference;
- the K1 executor is instructed not to locate or inspect held-out content through Git history, filesystem search, logs, other agents, or indirect lookup.

This is operational selector isolation, not a claim of permanent secrecy or statistical representativeness. If main cannot establish the gate without disclosing held-out content or annotations to K1, K1 must not be dispatched.

## 3. Required deliverable structure

The deliverable must contain exactly these top-level sections in order:

1. `Semantic domains and parameter boundary`
2. `Abstract syntax and static judgments`
3. `Denotational semantics and normative roles`
4. `Truth, error, and composition laws`
5. `Kernel judgments, reasoning, and normalization`
6. `Minimality and derived-form ledger`
7. `K0 challenge coverage and separating derivations`
8. `K2 semantic obligations and unresolved interface questions`
9. `K1 acceptance checklist`

The document may use mathematical notation, inference rules, truth tables, and compact pseudocode. All notation must be defined locally and remain independent of a concrete serialization or programming language.

## 4. Semantic domains and parameter boundary

The deliverable must define the semantic objects required to interpret a completed abstract outcome:

```text
Outcome = (PRE, TRACE, FINAL, EVIDENCE)
```

It must state exact abstract domains for terms, values, variables, principals, controlled events, source/provenance references, owned choices, plugin identities and versions, evidence references, and semantic environments. These domains may be abstract sets or sorts; they must not select coding-specific members.

The meaning of a Contract must expose, at minimum, independently inspectable facets for:

- hard acceptance constraints over outcomes;
- authorization conditions for principals and controlled trace events;
- open bindings and controller-owned choices;
- provenance and authority attachments;
- exact plugin identity/version dependencies.

The deliverable must define how these facets compose and whether each is defined for open as well as closed Contracts. An open Contract must not acquire a truth, consistency, or success result merely because its syntax is well-formed.

Plugin semantics must enter only as an explicitly declared abstract parameter supplying typed atom/function meanings and, where relevant, evidence or reasoning assumptions. K1 may state the semantic obligations on this parameter, but must not choose K2 wire formats, registration methods, capability-discovery APIs, proof encodings, or coding-plugin symbols.

## 5. Abstract syntax and static judgments

The deliverable must provide a serialization-independent abstract grammar or equivalent inductive definition for every retained kernel category. It must define exact formation, typing, binding, scope, and closure rules.

The design must explicitly decide the status of every candidate family inherited from the governing plan and K0:

- literals, variables, and typed binding;
- `PRE`, `TRACE`, `FINAL`, and `EVIDENCE` outcome anchors;
- plugin functions and plugin predicates as semantic parameters;
- negation, conjunction, alternatives, conditionality, and any retained quantification;
- hard requirement and authorization roles;
- owned unresolved choices and their controller;
- provenance, authority, and plugin identity/version attachment;
- Contract-level composition.

For each family, K1 must retain an irreducible construct, derive it compositionally, delegate it to the plugin parameter, or exclude it with a precise reason. It must not preserve a construct merely for readability.

The static judgments must map without overloading to the accepted K0 representation, well-formedness, closure, and evaluability families. In particular:

- `WELL_FORMED` is independent of `CLOSED`;
- missing or incompatible semantic bindings remain open or malformed as explicitly defined, never silently rebound;
- evaluability is a capability judgment, not authority or truth;
- a user-owned unresolved choice remains open and retains its controller.

No coding-task label or operation kind may become a kernel syntactic category.

## 6. Denotational semantics and normative roles

Every retained construct must receive a compositional denotation. The semantics must be independent of search, action selection, execution, or patch construction.

The deliverable must define exactly:

- how terms and plugin atoms are interpreted against an `Outcome` and bound semantic environment;
- how a Contract determines hard acceptance without claiming intent completeness;
- how requirement differs from authorization;
- how conditional requirements and conditional permissions compose;
- whether and how an unauthorized controlled event affects the Contract meaning;
- why permission does not require the permitted event and evaluability does not grant permission;
- how final-state, trace, and pre/final relational conditions remain distinct;
- how alternative acceptable outcomes differ from unresolved controller-owned choices;
- how provenance and source authority affect normative adoption without changing proposition content;
- how open bindings behave without being guessed or converted into factual unknowns;
- how exact plugin identity and version participate in meaning without defining the K2 ABI.

Soft preference is outside K1. Language that ranks otherwise acceptable outcomes must be reported outside the accepted scope; it must not be silently converted into a hard constraint.

The document must give explicit denotations for every retained primitive and prove or refute the proposed derived readings of `GOAL`, `PRESERVE`, `FORBID`, and `ALLOW`. A derived form may be accepted only if it preserves all relevant outcome, authorization, provenance, binding, truth, evidence-reference, unknown-reason, and error behavior—not merely two-valued acceptance.

## 7. Truth, error, and composition laws

K1 must choose and define exact three-valued laws for every retained logical connective and binder. It must include complete truth tables or equivalent total rules covering `TRUTH_TRUE`, `TRUTH_FALSE`, and `TRUTH_UNKNOWN`.

`EVALUATION_ERROR` and `REASONING_ERROR` remain outside the logical truth domain. The deliverable must specify, without evaluation-order dependence:

- how multiple child values, unknowns, and errors compose;
- whether a logically decisive child may make another child semantically irrelevant, and the exact rule if so;
- how `evidence_refs` and unknown reasons from relevant children are retained, deduplicated or combined, and reported, including when another child is logically decisive;
- how one or more errors are retained, combined, or reported;
- why no error becomes true, false, unknown, satisfiable, inconsistent, complete, entailed, or equivalent;
- how quantification, if retained, treats empty domains, unknown instances, and evaluation failures;
- how conditionality and alternatives behave under unknown conditions;
- which laws such as commutativity, associativity, idempotence, and De Morgan equivalence hold, fail, or require side conditions.

The deliverable must define the semantic collection model for evidence references and reasons, including equality and aggregation behavior, without relying on serialization order. It must state exactly which child metadata is semantically relevant in each connective or binder case; it may omit metadata only under an explicit rule justified by the denotation, never by short-circuit implementation order.

The rules must be compositional and deterministic for the same semantic inputs. Truth, error, evidence-reference, and unknown-reason results must be invariant under evaluator traversal order. They must not branch on challenge IDs, fixture order, evaluator order, or expected outcomes.

## 8. Kernel judgments, reasoning, and normalization

The deliverable must define the meaning and admissible evidence for all accepted K0 judgment families:

- representation;
- well-formedness and closure;
- evaluation capability;
- formula truth and evaluation failure;
- consistency;
- profile-relative completeness;
- entailment and equivalence;
- reasoning-service failure.

It must state which judgments are kernel-only, which are parameterized by plugin semantics or declared capability, and which cannot be concluded from a Contract alone. Profile completeness must remain relative to an explicit versioned profile; intent completeness remains uncertifiable.

Core derivation rules must be sound with respect to the denotation. At minimum, the deliverable must define:

- what constitutes a satisfying witness and a kernel-visible contradiction;
- when a plugin-supplied witness, proof, model, counterexample, or equivalence claim may be admitted abstractly, leaving its K2 representation unresolved;
- why local plugin results do not imply cross-plugin consistency or entailment;
- when the result must be `CONSISTENCY_UNKNOWN` or `RELATION_UNKNOWN`;
- how service failure produces `REASONING_ERROR` and no logical conclusion;
- semantic equivalence for Contracts, including authorization, provenance, binding, and plugin-version facets.

If the calculus defines normalization, every rule must have a denotation-preservation argument across all semantic facets and truth, evidence-reference, unknown-reason, and error behavior. If no nontrivial normalization is justified in K1, the deliverable must say so explicitly rather than promising an unspecified normal form.

K1 may establish soundness only for the explicitly stated core rules and assumptions. It must not claim universal decidability, completeness of plugin reasoning, or adequacy beyond the accepted K0 challenges.

## 9. Minimality and derived-form ledger

The deliverable must include a complete ledger for every inherited candidate construct and every new construct introduced by K1. Each row must record:

```text
Construct or semantic role
Disposition: RETAINED_PRIMITIVE | DERIVED | PLUGIN_PARAMETER | EXCLUDED
Exact denotation or derivation reference
Controlled separating pair or derivation proof
Why a simpler composition does or does not preserve meaning
K0 challenge IDs exercised
```

Every `RETAINED_PRIMITIVE` must have a controlled separating counterexample. Pair members must hold unrelated context fixed so they do not remain distinguishable for another reason after the proposed construct is removed. Every `DERIVED` form must have a denotational equivalence argument, including truth/error and non-acceptance facets where applicable.

Constructs without a valid separating pair or derivation obligation must be excluded or delegated. K1 must not claim an absolutely minimal calculus over all possible formalisms; it may claim only minimality relative to the accepted semantic distinctions, candidate space, and stated equivalences.

No kernel-semantic construct may remain undecided at K1 exit. Questions about concrete plugin interfaces, encodings, and coding vocabulary remain for K2-K3.

## 10. K0 challenge coverage and separating derivations

The deliverable must map all nineteen accepted seed challenges and all ten accepted separating pairs to the proposed calculus. It must not access or mention held-out contents.

Each challenge row must contain:

```text
Challenge ID
Kernel structure used
Abstract plugin-semantic assumptions
Applicable K0 judgments
Semantic distinction preserved
Unknown or failure path
Forbidden shortcut avoided
```

Plugin assumptions must use typed abstract placeholders defined for semantic analysis. They must not freeze K3 coding symbols, evaluator names, expected-answer lookups, or serialized IR.

The deliverable must include worked semantic derivations or countermodels for at least:

- K0-C04 versus K0-C05: conditional permission versus conditional obligation;
- K0-C08 versus K0-C09: controller-owned choice versus unknown fact;
- K0-C10: kernel-visible contradiction over individually well-formed atoms;
- K0-C11: plugin-visible contradiction over a nonempty population;
- K0-C12: capability-relative unknown consistency;
- K0-C13: exact version binding and missing evaluability;
- K0-C14: plugin-local versus cross-plugin reasoning;
- K0-C15 versus K0-C16: bound broad meaning versus evaluator availability;
- K0-C17: identical content with different source authority;
- K0-C18: equivalence of different surface phrasings after semantic binding;
- K0-C19: satisfiability without known implementation and profile incompleteness.

For every accepted separating pair, K1 must show either that the pair receives different denotations under the retained calculus or that the distinction is preserved by an explicit composition. A task-specific branch, challenge identifier, expected mapping, or broad unbound predicate is not evidence of coverage.

## 11. K2 semantic obligations and unresolved interface questions

K1 must end with a compact table separating frozen semantics from K2 interface choices. It must identify the exact semantic obligations K2 must operationalize for:

- typed, namespaced, versioned plugin symbols;
- matching model-facing and machine-facing semantic identity;
- atom/function denotations over the declared outcome facets;
- concrete evaluation and evidence contracts;
- capability declarations and capability-relative proof admission;
- witness, proof, model, counterexample, entailment, and equivalence evidence;
- evaluator and reasoning-service errors;
- profile-relative completeness;
- cross-plugin composition and trust boundaries.

The table may leave transport, serialization, registration, discovery, certificate encoding, and concrete symbol catalogs unresolved. It must not leave a kernel connective, normative role, truth/error rule, binding rule, provenance rule, or denotation dependent on a future K2 choice.

## 12. Required verification

The executor must run and return:

```text
git diff --check
```

It must also report:

- exact changed paths, which must be only `KernelPlugin/K1_Kernel_Calculus_and_Denotational_Semantics_v0.md`;
- the exact nine top-level sections in order;
- retained-primitive, derived, plugin-parameter, and excluded counts from the ledger;
- challenge coverage count, which must be nineteen;
- separating-pair coverage count, which must be ten;
- a list of every truth/error table, evidence/unknown-reason aggregation rule, and worked derivation or countermodel;
- confirmation that no held-out content or annotation was accessed or reproduced;
- confirmation that no serialization, plugin ABI, coding symbol catalog, executable checker, compiler, prompt, action graph, implementation, K2 handoff, or external artifact was introduced;
- external artifacts and checksums, which must be `none`.

## 13. Acceptance and stop criteria

K1 may be accepted only if:

- the abstract syntax and denotation are exact, compositional, and serialization-independent;
- every retained kernel construct has a controlled separating counterexample;
- every derived form has an equivalence argument across all affected semantic facets;
- every construct has a single final ledger disposition;
- normative roles, choice ownership, provenance, authority, binding, and plugin version remain explicit;
- truth/unknown/error composition and associated evidence-reference/unknown-reason aggregation are total, deterministic, and evaluation-order independent;
- kernel reasoning is sound with respect to the stated denotation and never treats failed proof as success;
- plugin and cross-plugin conclusions are capability-relative;
- all nineteen challenges and ten separating pairs are covered without coding-specific kernel branches or hidden expected mappings;
- K2 receives explicit semantic obligations without inheriting unresolved kernel meaning;
- conclusions remain limited to the accepted K0 scope.

Stop and return to main if:

- any required distinction cannot be represented without coding-specific kernel semantics;
- a retained primitive lacks a controlled separating pair;
- authorization cannot be defined without becoming obligation or execution policy;
- truth and error composition cannot be made exact without choosing a K2 implementation detail;
- a plugin must redefine a kernel connective, authority, provenance, binding, or failure meaning;
- cross-plugin reasoning requires a task-specific core rule;
- a K0 challenge exposes a semantic category outside the accepted scope;
- satisfying the handoff would require access to held-out content or annotations;
- preference ordering, planning, execution, model behavior, or benchmarking enters the design.

## 14. Return packet

Return exactly:

1. changed path;
2. concise section summary;
3. construct-disposition counts and ledger summary;
4. nineteen-challenge and ten-pair coverage tables;
5. truth/error tables and worked-derivation index;
6. verification commands and exact results;
7. unresolved K2 interface questions and stop conditions encountered;
8. held-out non-access confirmation;
9. external artifacts and checksums;
10. explicit confirmation that no implementation, K2 handoff, or downstream authority was created.

The executor must not commit. Main freezes any accepted candidate diff and then dispatches a fresh independent read-only review against this exact handoff, plan, K0 artifact, candidate range, and blobs.
