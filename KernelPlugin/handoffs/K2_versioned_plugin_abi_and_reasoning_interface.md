# K2 handoff — versioned plugin ABI and reasoning interface

> Status: review candidate. This document grants no mutation authority until independently accepted and main separately binds an exact clean source commit.

## 1. Binding and purpose

- Governing plan: `docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md`
- Accepted governing-plan blob: `01f959bc55f644a376f8ffa6059e9e77936be77c`
- Accepted K1 deliverable: `KernelPlugin/K1_Kernel_Calculus_and_Denotational_Semantics_v0.md`
- Accepted K1 deliverable blob: `d928010319c2c3bd08a94e1856cfca24dc2ae39e`
- K1 result commit: `f3418a6f74cae9563510066644be7118a37b97ef`
- K1 acceptance commit: `3c0a98b780b2613d96314bb76ba2589584a4fcc9`
- K1 acceptance record: `docs/reviews/kernel_plugin/K1_Kernel_Calculus_f3418a6_review.md`
- K1 acceptance-record blob: `461c04796170f62cd507561429eee17d29d56d77`
- Accepted K0 deliverable blob: `e86e184300a6620fb6fe25062635d9bc7cb410a1`
- Stage: `K2`
- Classification: blocking plugin-interface design
- Predecessor: accepted K1; no K2 interface artifact or K3 handoff
- External output roots: none

K2 defines the smallest exact, versioned interface by which plugins supply the
declarations, semantic bindings, evaluators, evidence contracts, profiles, and
optional reasoning capabilities parameterized by K1. Its exit question is:

> Can a plugin add typed atoms and sound domain reasoning through this interface
> without changing any kernel meaning?

K2 specifies an interface contract, not an implementation. It must not change
the K1 calculus, define coding symbols, implement a registry or evaluator,
construct an execution trace, or assess held-out adequacy.

The sole K2 deliverable is:

```text
KernelPlugin/K2_Versioned_Plugin_ABI_and_Reasoning_Interface_v0.md
```

After a separate explicit dispatch, the executor may mutate exactly that path.
It must not edit this handoff, accepted plans or reviews, K0/K1 artifacts,
repository navigation, held-out material, Phase 0/1 material, or any other
path. It does not commit.

## 2. Frozen K1 boundary and non-negotiable invariants

K2 operationalizes the accepted K1 semantics; it does not reinterpret them.
The following are frozen:

- `Delta` declarations are distinct from `Sigma` semantic meanings and from
  evaluator/reasoner availability.
- `Dependencies(C)` is mechanically extracted from Contract syntax plus
  explicit profile and event-scope-pair requirements. No ABI field may let a
  caller omit, replace, or override it.
- exact plugin, declaration, symbol, event, profile, and companion-pair
  identities are namespaced and versioned; display names and discovery order
  never bind semantics.
- functions return `TermResult`; predicates return the exact K1 `Eval` algebra.
  `UNKNOWN`, evaluation error, and reasoning error remain different families.
- plugins receive only declared, typed arguments. Outcome facets are available
  only through explicit anchor-derived values; no hidden Contract, challenge,
  expected result, or undeclared outcome access is permitted.
- evidence references, unknown reasons, and error reasons have stable semantic
  identity and set behavior independent of serialization or traversal order.
- controlled-event classification comes only from exact immutable `Delta`
  declarations. An `EventScopePair` must preserve the full K1 empty-trace,
  multi-event, truth, evidence, unknown, and error denotation.
- `SourceRef` preserves provenance but grants no authority. Only a separately
  validated `AuthorityRef` can support adoption or choice binding.
- `chi_C` is mechanically derived from validated Contract choice records; no
  request, witness, proof, model, or plugin can override it.
- concrete evaluation, symbolic reasoning, and profile checking retain their
  exact closure, capability, trust, result, and failure premises.
- plugin-local conclusions never become joint cross-plugin conclusions unless
  one admitted capability covers the complete exact dependency set.

If an exact interface cannot satisfy an invariant without changing K1, K2 must
stop and return the conflict to main rather than weakening the invariant.

## 3. Isolation and prohibited scope

K2 may use the accepted plan, K0 seed challenges, accepted K1 result, accepted
reviews, and opaque receipt `K1-HO-GATE-20260828-A`. It must not locate, inspect,
request, infer, or reproduce held-out contents or annotations through Git
history, filesystem search, logs, other agents, or indirect stores.

K2 must not introduce:

- coding-domain types, predicates, functions, task labels, or expected K3
  vocabulary;
- a plugin implementation, registry, loader, evaluator, reasoner, certificate
  checker, compiler, prompt, model-facing prompt template, or source-to-IR
  binder;
- planning, action selection, state-transition execution, patch generation,
  repository mutation, model training/inference, prompt search, or benchmark;
- task IDs, challenge IDs, expected mappings, gold Contracts, or privileged
  evaluator inputs in any production interface;
- a K3 handoff, K3 mutation path, or downstream execution authority.

Examples and conformance cases use fresh abstract keys and values only. They may
reference K0 challenge IDs solely in a coverage table, never as an ABI input or
branch condition.

## 4. Required deliverable structure

The deliverable must contain exactly these ten top-level sections in order:

1. `Scope, conformance, and representation decision`
2. `ABI object model and lifecycle`
3. `Exact identity, declarations, dependencies, and versioning`
4. `Semantic bindings and model-facing contracts`
5. `Invocation, values, truth, evidence, and failure protocol`
6. `Capabilities, reasoning requests, and certificate admission`
7. `Events, profiles, provenance, authority, and cross-plugin composition`
8. `Discovery, compatibility, migration, and conflict handling`
9. `K1 obligation coverage and adversarial conformance cases`
10. `K3 input boundary and K2 acceptance checklist`

The document may use typed record notation, state machines, validation rules,
tables, and compact pseudocode. Every interface object, transition, result, and
error must be defined locally. Concrete field names are permitted; coding
symbols and executable code are not.

## 5. Scope, conformance, and representation decision

The deliverable must define what “K2 ABI conformance” means for a plugin
package, semantic binding, service, request, result, and certificate. It must
separate at least:

- declaration conformance;
- semantic-binding conformance;
- service/capability conformance;
- invocation/result conformance;
- certificate and trust conformance;
- whole-package conformance.

K2 must make one explicit representation decision:

1. define a canonical v0 serialization/transport representation; or
2. define a transport-neutral logical ABI whose typed records, equality,
   validation, and state transitions are complete enough for K3, while
   explicitly excluding byte-level encoding from v0.

Either choice must leave no semantic equality, identity, omission, default,
ordering, duplicate, or unknown-field behavior ambiguous. A transport-neutral
choice must not call itself interoperable at the byte or process boundary. A
canonical representation must distinguish malformed transport from K1
evaluation/reasoning failure and must not make field order semantically
relevant where K1 uses sets.

The deliverable must include an interface-responsibility ledger. Every record
and semantically relevant field receives exactly one disposition:

```text
REQUIRED_SEMANTIC | DERIVED | OPTIONAL_DIAGNOSTIC | EXCLUDED
```

For each row, record the K1 obligation, producer, consumer, validator, identity
and version rule, omission behavior, failure family, and conformance case. An
`OPTIONAL_DIAGNOSTIC` field must not affect any K1 judgment. Unjustified fields
are excluded rather than retained for hypothetical convenience.

## 6. ABI object model and lifecycle

The deliverable must define the minimal logical record roles needed to carry
K1 semantics. It may combine roles when no distinction is lost, but must cover:

- the ABI protocol/version identity;
- plugin identity and exact plugin version;
- type, literal/value-admission, function, predicate, event, event-scope-pair,
  and other `Delta` declarations;
- semantic contracts or binding descriptors for declared literal, function,
  predicate, event-pair-coherence, and profile meanings;
- model-facing symbol documentation bound to the same semantic identity;
- evaluator, profile-checker, and reasoning capability descriptors;
- function and predicate invocation requests;
- term, formula, profile, discovery, and reasoning results;
- evidence, unknown-reason, evaluation-error, and reasoning-error identities;
- witness, proof, model, counterexample, equivalence, and entailment
  certificate envelopes, including the separate internal `==Eval` derivation
  role;
- provenance values and authority attestations where they cross the interface.

The object model and responsibility ledger must allocate every semantic field
to exactly one of these non-overlapping layers:

| Layer | Owns | Does not own |
|---|---|---|
| `Delta` declaration | identity, type/value admission, signatures, facet positions, immutable event declarations, and event-pair membership/signatures/controlled keys | denotation, evidence contract, unknown/error behavior, profile meaning, service availability |
| `Sigma` semantic binding | literal/function/predicate meanings, evidence and access contract, unknown/error behavior, admitted event-pair coherence, profile definitions, and authority facts | evaluator/reasoner discovery or availability |
| Service/capability | invocable evaluator/profile-checker/reasoner, supported judgment and fragment, dependency scope, trust basis, and service failure contract | declaration or semantic meaning |

Combining transport records is allowed only if validation still projects these
three layers uniquely. A missing `Delta` field is malformed; an absent required
`Sigma` binding is open; an absent compatible service is an evaluability result,
not a declaration or closure failure.

The deliverable must give an exact lifecycle or state-transition relation that
keeps these states independent:

```text
DECLARED
SEMANTICALLY_BOUND
CAPABILITY_DISCOVERED
INVOCABLE_FOR(requested judgment)
```

The actual names may differ. The transitions must explain which K0/K1 public
status follows when a declaration is malformed, a meaning is absent, discovery
is missing or indeterminate, a capability is incompatible, invocation fails,
or a completed result is inconclusive. Registration order, retries, and service
location cannot change semantic identity or judgment.

This lifecycle is an interface validation model, not a planner, loader
implementation, or execution architecture.

## 7. Exact identity, declarations, dependencies, and versioning

K2 must define exact equality and validation for every K1 key family:

```text
PluginKey
DeclarationKey
SymbolKey
EventKey
ProfileKey
EventScopePair identity
ABI protocol version
```

The interface must specify namespace ownership, kind separation, exact-version
matching, duplicate handling, collision handling, and whether identity is a
record, reference, digest, or another exact representation. Human-readable
names, aliases, documentation titles, service endpoints, and discovery order
must not silently alter equality.

Declaration schemas and validation must cover:

- plugin-owned types and value admission;
- literals and their exact types;
- function argument/result types and symbol kind;
- predicate argument types, Boolean result kind, and outcome-facet positions;
- immutable event key, payload type, and `CONTROLLED | OBSERVATIONAL` class;
- exact event-scope/trace-occurrence companion membership, signatures,
  controlled keys, and facet declaration.

`TermResult` behavior, predicate `Eval` behavior, evidence/access dependencies,
unknown/error contracts, exact profile dimensions, and profile coverage meaning
belong to `Sigma` semantic bindings, not to these `Delta` schemas. Evaluator,
profile-checker, and reasoner availability belongs only to the service layer.

The ABI must preserve K1 mechanical dependency extraction. A descriptor may
declare transitive declaration dependencies, but it cannot supply a smaller
replacement for dependencies extracted from a Contract. Missing declarations
are malformed; valid declarations with absent exact meanings are open; bound
meanings with absent compatible services remain closed but not evaluable.

Version compatibility and migration must be explicit. K2 must define:

- what exact compatibility claims can and cannot establish;
- how a migration names its source, target, semantic relation, validator, and
  trust basis;
- when migration requires a new Contract binding or representation judgment;
- why “latest”, display-name equality, first-found service, implicit aliasing,
  and undeclared backward compatibility never substitute one key for another.

K2 need not require cryptographic hashes, but any chosen digest or signature
must be treated as an identity/integrity mechanism rather than proof of semantic
validity.

## 8. Semantic bindings and model-facing contracts

For every declared literal, function, or predicate, the interface must define
how an exact semantic meaning is bound independently of service availability.
It must do the same for exact profile definitions and for admitted
`EventScopePair` coherence. A semantic binding must expose enough information
to validate:

- exact declaration and version;
- denotation or evaluation contract;
- permitted outcome-facet inputs;
- exact direct and transitive dependencies;
- evidence schema and access boundary;
- stable unknown and error behavior;
- deterministic meaning for the same semantic inputs;
- compatibility with the declaration and ABI version.

Profile bindings additionally own their versioned dimensions and coverage
meaning. Event-pair bindings must use the non-circular admission path required
by §11. None of these semantic fields may be required merely to make the
corresponding `Delta` declaration well formed.

Broad atoms are permitted only under the same explicit boundary. Their
interface must make undeclared access non-conformant, including access to a
challenge ID, expected mapping, gold Contract, hidden target, repository state
not passed through a declared value, or evidence outside the declared schema.
“The evaluator knows whether the task is correct” is not a semantic contract.

Model-facing documentation and machine-facing meaning must bind the same exact
key and semantic-contract identity. The deliverable must define:

- the minimum model-facing signature, facet, evidence, unknown/error, and
  capability information;
- the machine-facing binding it references;
- mismatch behavior;
- whether aliases or translations are permitted and how they preserve the
  exact target key;
- why documentation wording never creates authority or a second denotation.

K2 does not write a compiler prompt or natural-language binding policy.

## 9. Invocation, values, truth, evidence, and failure protocol

The interface must define separate typed request/result protocols for:

- literal/value admission where invoked;
- plugin function application returning `TERM_VALUE` or `TERM_ERROR`;
- plugin predicate evaluation returning the exact K1 `Eval` algebra;
- profile checking;
- capability discovery;
- symbolic/reasoning requests.

Function and predicate requests must bind the exact ABI version, symbol,
semantic contract, dependency environment, argument positions and types, and
requested capability. A predicate receives only its positional typed values.
It does not receive an implicit full `Outcome`, Contract, choice map, authority
context, challenge identity, or expected answer. An anchor-derived state,
trace, or evidence value is visible only when the declared signature includes
that argument.

The result protocol must preserve exactly:

```text
TERM_VALUE(value)
TERM_ERROR(nonempty set of EvaluationErrorReason)
VALUE(TRUE | FALSE | UNKNOWN, evidence_refs, unknown_reasons)
ERROR(nonempty evaluation_errors, evidence_refs, unknown_reasons)
REASONING_ERROR(nonempty reasoning_errors)
```

It must define typed value validation; stable identity and equality for
evidence and reasons; set deduplication; duplicate and ordering behavior;
empty/nonempty invariants, including nonempty unknown reasons for
`VALUE(UNKNOWN,...)` and nonempty error sets for both error variants;
malformed-result behavior; and how transport or protocol failure maps outside
logical truth. It must not reimplement the K1 T1--T4 or A1--A2 connective
aggregation inside plugins.

Evidence references must identify admissible support without embedding a
success conclusion. Unknown reasons must say what remains unresolved without
granting discretion. Error reasons must not be accepted as truth, consistency,
profile, or relation results. Retry metadata, logs, timing, endpoints, and
request IDs are optional diagnostics only unless the deliverable proves a K1
semantic role.

## 10. Capabilities, reasoning requests, and certificate admission

The capability interface must represent at least:

```text
CONCRETE_EVALUATION_ONLY
PARTIAL_SYMBOLIC_REASONING
COMPLETE_FOR_DECLARED_FRAGMENT
```

For each capability, define its exact plugin/ABI versions, supported judgment
families, sound fragment, complete fragment if any, dependency scope, required
evidence, trust basis, service availability, and failure behavior. A service
claim outside its declared fragment is non-conformant. A partial capability, or
a request outside a declared complete fragment, may complete without a decisive
proof and yield the applicable relation/consistency unknown. A
`COMPLETE_FOR_DECLARED_FRAGMENT` service handling an in-fragment request must
return the admitted decisive judgment; a completed in-fragment “no result” is a
protocol violation and yields `REASONING_ERROR`, never logical `UNKNOWN`. A
service failure likewise returns reasoning error.

Reasoning requests must name exactly one public K1 judgment/relation taxonomy
member or the separate internal `EVAL_FUNCTION_EQUALITY_DERIVATION` role that
operationalizes K1 `f ==Eval g`. Every request binds the complete mechanically
extracted environment. Contract-level requests require closed Contracts;
formula and `==Eval` requests require a closed formula environment. No request
may supply an alternate `chi_C`.

The certificate interface must distinguish and validate:

- satisfying witnesses;
- contradiction proofs;
- models and abstract witnesses;
- decisive logical counterexamples;
- strong entailment and truth-behavior equivalence proofs;
- internal `==Eval` derivations proving equality of complete `Eval` functions,
  including truth, evidence, unknown-reason and evaluation-error sets and exact
  free dependencies under one exact `Delta`, `Sigma`, `chi_C`, and lexical
  scope;
- exact full-Contract equivalence or inequality evidence;
- profile coverage evidence.

Every certificate must bind the exact semantic environment, capability,
fragment, dependencies, requested conclusion, validator, and trust basis. It
must state whether it is concrete, symbolic, or abstract. Admission must follow
K1 §5.2--§5.4 exactly: `UNKNOWN` is not a decisive logical counterexample;
evaluation or reasoning error proves nothing; an abstract satisfying witness
is not a patch; and a certificate for one relation cannot be relabeled as
another.

An admitted `==Eval` derivation is an internal proof object only. It may support
a derived-form preservation argument, a stronger public formula/acceptance
equivalence proof, or one facet of full-Contract equivalence, but it never
directly renders `RELATION_PROVED` and cannot be relabeled as public logical or
full-Contract equivalence evidence without the receiving rule's other premises.

For joint reasoning, the declared capability dependency set must cover the
entire cross-plugin formula and shared dependencies. Separate local results do
not compose into joint satisfiability, entailment, or equivalence.

## 11. Events, profiles, provenance, authority, and composition

The ABI must define the exact interface representation and validation of:

- immutable event declarations and event payload values;
- admitted trace-event records containing the exact `EventValue` and optional
  actor, with a controlled event lacking an actor receiving no matching grant;
- `EventScopePair` membership, signatures, controlled keys, and coherence
  validation record or certificate;
- exact profile keys, versioned dimensions, coverage evidence, checker class,
  and complete/incomplete/unknown/error results;
- self-contained `SourceRef` provenance values;
- `AuthorityRef` attestations for `REQUIRE`, `AUTHORIZE`, and
  `BIND_CHOICE(choice_id)`;
- multi-plugin dependency and trust scope.

The event-pair interface must make the K1 full-result equality an actual
semantic-binding conformance condition for every admitted trace, including
empty and multi-event traces and truth, evidence, unknown, and error
aggregation. A producer's bare coherence claim is never sufficient. K2 must
choose and define at least one non-circular admission path:

- the occurrence meaning is definitionally constructed from the scope meaning
  by the frozen T3/A1 aggregation; or
- an exact coherence proof is admitted by a separately trusted validator whose
  declared sound fragment and trust basis do not depend on the pair's own
  unvalidated claim.

Successful admission binds the exact pair meanings. Missing validation leaves
the required coherence semantic binding open; an unavailable validation
capability may additionally be reported as missing evaluability. Validator or
protocol failure yields `REASONING_ERROR` and no admission, so the Contract
cannot close. An admitted counterexample or failed exact check makes the
semantic binding incompatible/malformed. The deliverable must define these
states without turning a bare claim, missing validator, or failed validator
into closure. A caller cannot classify an event, weaken the controlled-key set,
or link unrelated scope and occurrence predicates after binding.

Profile checking must keep known omission, completed inconclusive coverage,
concrete evaluation failure, and symbolic reasoning failure distinct. A
profile cannot certify intent completeness or change Contract acceptance.

Provenance transport cannot grant authority. An evaluator result, plugin
signature, service registration, or documentation sentence cannot create an
adoption or choice-binding attestation. Trust mechanisms validate the exact K1
authority tuple; they do not redefine its meaning.

Composition must be conflict-detecting and order-independent. Duplicate exact
declarations may coalesce only under the chosen equality rule. Incompatible
declarations, meanings, profiles, pair definitions, ABI versions, or trust
claims fail loudly; “first registered wins” and silent shadowing are forbidden.

## 12. Discovery, compatibility, migration, and conflict handling

K2 must define discovery results and state transitions that distinguish:

- exact compatible binding found;
- exact binding absent;
- discovery unable to decide;
- incompatible declaration or semantic binding;
- compatible meaning present but requested service absent;
- service present but outside the required capability fragment;
- completed inconclusive reasoning from a partial or out-of-complete-fragment
  request;
- a complete in-fragment service returning no decisive result, which is a
  reasoning protocol error rather than unknown;
- evaluation, reasoning, and transport/protocol failure.

Discovery and registration are interface concerns only. The deliverable must
not choose a process manager, network protocol implementation, dynamic loader,
package repository, retry scheduler, or deployment topology.

Compatibility declarations and migrations must never mutate the original
Contract identity silently. The deliverable must give exact rejection behavior
for conflicting duplicates, version skew, kind confusion, stale model-facing
documentation, dependency cycles if disallowed, and unknown extensions. If
extensions are permitted, their namespace and semantic effect must be explicit;
an unrecognized semantically relevant extension cannot be ignored.

## 13. Required adversarial conformance cases

The deliverable must include one table with exactly these twenty abstract
cases, using fresh keys and no coding vocabulary:

| ID | Required distinction |
|---|---|
| K2-A01 | malformed missing declaration versus well-formed declaration with missing meaning |
| K2-A02 | bound meaning with compatible evaluator versus the same meaning with no evaluator |
| K2-A03 | exact v1 requirement versus only incompatible v2 discovery, with no silent fallback |
| K2-A04 | same display name but different namespace, kind, or plugin identity |
| K2-A05 | machine-facing semantic binding versus stale or mismatched model-facing documentation |
| K2-A06 | mechanically extracted dependency versus a caller attempt to omit or replace it |
| K2-A07 | well-typed values and choices versus an ill-typed alternative, argument, event payload, or result |
| K2-A08 | declared facet argument access versus hidden full-Outcome or undeclared evidence access |
| K2-A09 | legitimate broad predicate contract versus expected-answer/oracle access |
| K2-A10 | `TERM_ERROR`, factual `UNKNOWN`, and predicate `ERROR` as three distinct results |
| K2-A11 | unordered evidence/reason sets versus reordered or duplicated transport forms |
| K2-A12 | immutable controlled event declaration and actor matching versus a caller-supplied control flag or missing/wrong actor |
| K2-A13 | definitionally or independently validated event-scope coherence on empty/multi-event traces versus a bare claim, missing/failed validator, or disproved pair |
| K2-A14 | self-contained provenance versus authority adoption or choice-binding attestation |
| K2-A15 | profile complete, incomplete, unknown, evaluation error, and reasoning error |
| K2-A16 | concrete-only, partial-symbolic, and complete-fragment capabilities on in/out-of-fragment requests, including forbidden in-fragment inconclusive completion |
| K2-A17 | valid witness/proof/counterexample/internal `==Eval` derivation bound to the exact environment versus stale or relabeled evidence |
| K2-A18 | Contract-derived `chi_C` versus a witness/request override attempt |
| K2-A19 | plugin-local results versus one joint capability covering the complete cross-plugin dependency set |
| K2-A20 | explicit compatible migration versus alias, latest-version, first-found, or discovery-order substitution |

Every row must provide:

```text
exact abstract inputs
interface objects and lifecycle states
expected validation and K0/K1 status family
semantic information that would be lost by conflation
forbidden shortcut
K1 obligation exercised
```

The deliverable must work through at least A01, A05, A09, A10, A13, A15, A16,
A17, A19, and A20 as complete interface traces from declaration through final
status. A case-specific field, branch, expected lookup, or privileged input is
not evidence of conformance.

## 14. K1 coverage and K3 input boundary

The deliverable must map every row of K1 §8’s frozen-obligation table to exact
ABI records, validation rules, lifecycle transitions, conformance cases, and
remaining representation-only choices. No frozen semantic obligation may be
left for K3.

K2 must end with a compact K3 input packet containing only:

- the accepted ABI/protocol version and representation decision;
- plugin-owned extension points;
- exact declaration, binding, invocation, evidence, capability, certificate,
  internal `==Eval`, profile, event, provenance, and migration obligations;
- the twenty accepted K2 conformance cases;
- K3’s allowed task: choose a minimal coding-domain vocabulary and demonstrate
  it against the accepted kernel and ABI;
- exclusions and stop conditions inherited from K0--K2.

The packet must not choose any coding type or symbol, pre-freeze a K3 mutation
path, create a K3 handoff, or authorize K3 work.

## 15. Required verification and return packet

The executor must run and return:

```text
git diff --check
```

It must also report:

1. exact changed path, which must be only
   `KernelPlugin/K2_Versioned_Plugin_ABI_and_Reasoning_Interface_v0.md`;
2. the exact ten top-level sections in order;
3. the representation decision and its precise non-claim;
4. interface-responsibility ledger counts by disposition;
5. all logical record roles, their unique declaration/binding/service layer,
   lifecycle states, and the internal `==Eval` role;
6. K1 §8 obligation coverage count and mapping;
7. adversarial conformance count, which must be twenty, and the ten required
   complete interface-trace IDs;
8. exact version, migration, conflict, unknown-extension, and duplicate rules;
9. held-out non-access confirmation;
10. external artifacts and checksums, which must be `none`;
11. confirmation that no implementation, coding symbol catalog, K3 handoff, or
    downstream authority was created.

## 16. Acceptance and stop criteria

K2 may be accepted only if:

- the interface is exact enough that two conforming implementations cannot
  disagree about semantic identity, validation state, request meaning, result
  family, certificate conclusion, or conflict behavior;
- every K1 §8 obligation has one complete, non-circular interface path;
- declaration, meaning, discovery, capability, invocation, and result states
  remain independent;
- every semantically relevant record/field has one ledger disposition and no
  diagnostic field affects a K1 judgment;
- model-facing and machine-facing contracts bind the same exact meaning;
- broad atoms have explicit typed, facet, dependency, evidence, access,
  unknown, error, and capability boundaries without oracle inputs;
- truth, metadata, evaluation error, reasoning error, and profile results
  preserve K1 exactly;
- proof and certificate admission is sound, exact-environment-bound, and
  capability-relative; complete in-fragment requests cannot finish
  inconclusively, and internal `==Eval` is not a public relation status;
- event classification, event-scope coherence, choice ownership, provenance,
  authority, profile relativity, and cross-plugin trust cannot be overridden;
- version skew, duplicates, conflicts, migration, discovery uncertainty, and
  unavailable services fail or remain unknown in the correct family without a
  silent fallback;
- all twenty conformance cases and ten complete traces follow from general ABI
  rules;
- K3 receives a complete interface boundary without receiving coding symbols,
  a handoff, or execution authority;
- conclusions remain limited to interface coherence within accepted K0/K1
  scope.

Stop and return to main if:

- any interface rule requires changing a K1 connective, denotation, status,
  closure premise, authority rule, or error rule;
- semantic identity depends on display text, service location, discovery order,
  or an unvalidated optional field;
- a plugin needs undeclared access to express an accepted K0/K1 case;
- a proof/certificate cannot bind the complete exact environment without
  choosing coding-specific semantics;
- event-scope coherence or joint reasoning requires a task-specific kernel or
  ABI branch;
- a representation choice makes `UNKNOWN`, absence, malformed input, and
  failure indistinguishable;
- satisfying K2 requires held-out content, a coding vocabulary, implementation,
  execution, model behavior, or benchmarking.

Return exactly the eleven items in §15. The executor must not commit. Main
freezes a candidate diff and dispatches a fresh independent read-only review
against this exact handoff, plan, K0/K1 artifacts, candidate range, and blobs.
