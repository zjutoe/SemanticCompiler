# K3-S handoff — minimal coding-plugin semantics

> Status: review candidate. This document grants no mutation authority until independently accepted and main separately binds an exact clean source commit.

## 1. Binding and purpose

- Original governing plan: `docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md`
- Accepted original-plan blob: `01f959bc55f644a376f8ffa6059e9e77936be77c`
- Governing amendment: `docs/plans/K3_Semantics_and_Executable_Spike_Amendment.md`
- Accepted amendment blob: `7f1c3627245ec0c0fc86df64f77e374d104649a0`
- Amendment acceptance commit: `17f57e83d8a57646f34f8b26b30b65fae3276c5b`
- Amendment acceptance-record blob: `93069c111a38d3be13219088a7b5b92da83d6318`
- Accepted K0 deliverable blob: `e86e184300a6620fb6fe25062635d9bc7cb410a1`
- Accepted K1 deliverable blob: `d928010319c2c3bd08a94e1856cfca24dc2ae39e`
- Accepted K2 deliverable blob: `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`
- K2 acceptance-record blob: `c4adccc538e83e0a32de96f645c76cfe6ca8b3b2`
- Opaque held-out receipt only: `K1-HO-GATE-20260828-A`
- Stage: `K3-S`
- Classification: blocking coding-plugin semantic design
- Predecessor: accepted K2 and accepted K3-S/K3-X plan amendment
- Successor authority: none
- External output roots: none

K3-S chooses the smallest coding-domain vocabulary that can express the
accepted K0 seed challenges through the accepted K1 calculus and K2 logical
ABI. Its exit question is:

> Can the accepted coding challenges be represented through typed, versioned
> plugin semantics without a coding-specific kernel branch, hidden expected
> answer, or execution semantics?

The sole future K3-S deliverable is:

```text
KernelPlugin/K3_S_Minimal_Coding_Plugin_Semantics_v0.md
```

Only after this handoff is accepted and main issues a separate exact dispatch
may one writer mutate that path. The writer must not edit this handoff, plans,
reviews, K0--K2 artifacts, repository navigation, Phase 0/1 material, held-out
material, or any other path, and must not commit.

## 2. Frozen K1/K2 boundary

K3-S instantiates accepted extension points; it does not reinterpret them. The
following are frozen:

- K1 owns formula composition, requirement and authorization roles, variables,
  choices, provenance, authority, three-valued truth, evaluation/reasoning
  errors, closure, consistency, relations, and profile results.
- K2 owns exact plugin/symbol/version identity, `Delta` declarations, `Sigma`
  meanings, Service capabilities, model contracts, lifecycle, mechanical
  dependencies, separate validation references, trust, certificates, requests,
  results, failures, discovery, migration, duplicates, and conflicts.
- `PRE`, `TRACE`, `FINAL`, and `EVIDENCE` are K1 outcome facets. Coding symbols
  may consume only explicitly typed projections permitted by their access
  contracts.
- A declaration is not a meaning, and a meaning is not an available evaluator.
  Missing declaration, binding, capability, trust, and evidence remain
  different statuses.
- Evaluability grants no authority. Trace events are controlled only through
  immutable typed declarations and the separate K1 authorization relation.
- Exact identity includes owner namespace, plugin, local identity, kind, and
  exact version. Display labels, aliases, input order, and discovery order do
  not bind or migrate meaning.
- Frozen K1 syntax dependencies and derived K2 semantic closure cannot be
  supplied or overridden by the coding plugin. Mandatory certificate,
  validator, and trust references remain separate from the semantic proper DAG.
- `UNKNOWN`, `FALSE`, `EVALUATION_ERROR`, `REASONING_ERROR`, malformedness,
  incompatibility, missingness, and `UNREPRESENTABLE` are not interchangeable.
- Concrete evaluators, symbolic reasoners, profiles, and broad predicates are
  capability-relative and may claim only their exact declared fragment.
- K3-S may define no byte representation, implementation, parser, binder,
  planner, state-transition executor, repository operation, or K3-X path.

If the coding semantics require changing any frozen rule, the stage stops and
returns the conflict to main.

## 3. Isolation and anti-oracle boundary

K3-S may use the accepted plans, K0 seed catalog, accepted K1/K2 artifacts,
their acceptance records, and only the opaque held-out receipt. It must not
locate, inspect, request, infer, or reproduce held-out contents, annotations,
paths, hashes, history, logs, or indirect stores.

The deliverable must not contain or rely on:

- a production branch keyed by K0/K3 case ID, source document, fixture order,
  expected status, expected Contract, gold patch, or expected outcome;
- `FIX_BUG`, `ADD_FEATURE`, `REFACTOR`, task labels, benchmark labels, or one
  expected patch as semantic primitives;
- implicit access to repository files, environment variables, commands,
  network state, evaluator internals, hidden tests, or undeclared evidence;
- a predicate whose meaning is “return the expected answer” or whose evidence
  contract merely names an opaque success token;
- latest-version, name-only, first-found, registration-order, or service-order
  fallback;
- a plugin-owned truth value, connective, authority rule, source adoption,
  choice controller, failure conversion, or joint-composition shortcut;
- implementation code, executable pseudocode that fixes representation,
  K3-X/K4 handoff, mutation path, execution command, or downstream authority.

Challenge identifiers may appear only in coverage, separating-pair, and
conformance-case tables. They are test labels, never semantic inputs.

## 4. Required deliverable structure

The deliverable must contain exactly these ten top-level sections in order:

1. `Scope, non-claims, and conformance`
2. `Coding semantic universe and outcome projections`
3. `Exact plugin vocabulary, identities, and versions`
4. `Declarations, meanings, dependencies, and model contracts`
5. `Trace events, requirements, authorization, and choices`
6. `Evidence, capabilities, trust, results, and failures`
7. `K0 seed challenge bindings and status analysis`
8. `Relative minimality and separating cases`
9. `K3-X semantic input boundary`
10. `K3-S acceptance checklist`

The document may use typed logical records, equations, tables, and declarative
pseudocode. Every proposed type, value, function, predicate, event, profile,
capability, evidence schema, and model contract must be defined locally and
mapped to exact K2 record roles.

## 5. Coding semantic universe and vocabulary decision

The deliverable must make one explicit minimal-vocabulary decision. It must
cover, possibly under different justified names:

- an abstract repository snapshot for `PRE` and `FINAL`;
- typed path and path-set values with exact normalization/equality semantics;
- typed artifact or file-content observations without ambient filesystem
  access;
- a finite change-set relation derived from the two snapshots, not an executor
  action plan;
- a typed observation domain and observation result usable for preservation;
- abstract command/test, path-change, network-contact, release, and other
  challenge-required trace events, with immutable controlled-event ownership;
- verification evidence whose references and schemas are distinct from truth;
- a typed task or acceptance-specification value suitable for a reusable broad
  predicate;
- only the additional numeric, format, dependency, policy, provenance, or
  authority values demonstrably required by the seed challenges.

The design may unify roles only when it proves no accepted distinction is lost.
It must reject untyped strings and universal maps as escape hatches. Path or
artifact identity must not depend on host filesystem behavior. A change set is
an extensional relation between supplied snapshots; it cannot prescribe how an
agent edits a repository.

For every retained vocabulary item, define:

- exact `DeclarationKey`/`SymbolKey`/`EventKey`/`ProfileKey` or other K2 key;
- owner/plugin namespace, local identity, kind, and exact version;
- `Delta`, `Sigma`, or Service ownership;
- complete signature, admitted values, and allowed outcome facets;
- exact K1 syntax dependencies, K2 semantic roots, and any distinct validation
  references;
- evidence, access, unknown, evaluation-error, and reasoning-error contracts;
- model-facing `ModelContract` bound to the same semantic identity;
- omission, duplicate, version-skew, and conflict behavior;
- supporting seed cases and a separating counterexample.

## 6. Required semantic behaviors

The selected vocabulary and bindings must demonstrate all of the following:

1. A final-state acceptance condition and a pre/final preservation relation use
   supplied typed observations, not fixed expected outputs.
2. A forbidden event and an authorized event remain different normative roles;
   conditional permission does not become obligation.
3. A factual result pending declared test evidence is `TRUTH_UNKNOWN`, not an
   owned choice, success, or failure.
4. A broad predicate such as task/rubric acceptance has an exact typed
   `TaskSpec`-like input, outcome scope, reusable denotation, dependencies,
   evidence schema, capability fragment, and honest unknown/error behavior. A
   bound meaning with no evaluator remains closed but unevaluable.
5. Plugin numeric or domain reasoning may prove only an exact named
   contradiction under an admitted capability/certificate; lack of a joint or
   complete reasoner remains the matching logical unknown.
6. Exact old versus incompatible new versions do not substitute. Model-facing
   and machine-facing contracts bind one exact meaning.
7. Provenance does not grant authority. Identical content from an authenticated
   principal and an untrusted quoted source retains different adoption status.
8. Multiple acceptable outcomes, unresolved controller-owned choices, and
   unknown facts remain separate.
9. Cross-plugin constraints compose in K1, while plugin-local conclusions do
   not establish joint consistency without one exact joint capability.
10. An abstract satisfying outcome or proof does not imply a concrete patch,
    buildable implementation, or execution plan.

Every evaluator or reasoner sees only its declared typed inputs. The broad
predicate and all narrower predicates must be extensionally reusable across
more than one challenge; a case-specific wrapper around an expected mapping is
non-conformant.

## 7. K0 coverage and worked semantic cases

Section 7 must contain exactly one coverage row for every seed challenge
`K0-C01` through `K0-C19`. Each row records:

```text
challenge | exact Contract pattern | plugin symbols and versions |
declared facets/dependencies/evidence | lifecycle/status family |
capability/trust premise | information preserved | forbidden shortcut
```

A row may conclude `UNREPRESENTABLE`, `UNRESOLVED`, or a namespaced unknown or
error when required; it must explain why and must not add an ad hoc atom to
force success. Equivalent ordinary phrasings must map to the same semantic
pattern rather than phrase-indexed symbols.

The section must also include exactly eight complete worked traces, covering:

- final-state acceptance with evidence;
- pre/final preservation;
- forbidden versus conditionally authorized events;
- factual unknown before evidence and its decisive completion;
- plugin-proved contradiction versus capability-limited unknown;
- exact version mismatch with no fallback;
- broad predicate with and without a compatible evaluator; and
- provenance/authority plus abstract satisfiability without a concrete patch.

Each trace begins from exact declarations/bindings, follows applicable K2
lifecycle coordinates, and ends with only the K1/K2 public statuses justified
by its premises.

## 8. Minimality ledger and adversarial cases

Section 8 must contain an exhaustive responsibility/minimality ledger. Every
coding-specific record or exact field receives exactly one disposition:

```text
RETAINED_DELTA | RETAINED_SIGMA | RETAINED_SERVICE | DERIVED | EXCLUDED
```

Each row records owner, semantic role, signature/facets, dependencies,
evidence/access/failure boundary, identity/version rule, omission result,
consumer, seed cases, and separating pair. A retained item without a
separating case is removed or made derived. Readable derived syntax does not
become an independent primitive.

The section must define exactly 18 adversarial cases `K3S-A01` through
`K3S-A18`, in order, covering:

1. same display atoms but different owner/plugin namespaces and kinds;
2. exact version mismatch and no fallback;
3. declaration versus binding versus capability absence;
4. final-state versus pre/final semantics;
5. path/content/change-set scope and undeclared access;
6. forbidden versus authorized events;
7. conditional requirement versus conditional permission;
8. factual unknown versus owned choice;
9. broad predicate with evaluator versus the same meaning without one;
10. false versus unknown versus evaluation/reasoning error;
11. plugin-visible contradiction versus unresolved conflict;
12. plugin-local versus joint cross-plugin reasoning;
13. identical content with different provenance/authority;
14. equal duplicates versus unequal same-identity conflicts;
15. semantic proper dependency versus validation reference and genuine cycle;
16. model/machine semantic identity mismatch;
17. task-taxonomy/phrase-indexed vocabulary exclusion; and
18. abstract satisfying outcome without a concrete implementation.

Each case states abstract inputs, exact records, expected status family,
information lost by conflation, and forbidden shortcut. Case IDs cannot enter a
meaning, evaluator, request, result, or evidence record.

## 9. K3-X semantic input boundary

Section 9 freezes only semantic inputs for later K3-X handoff design. It must:

- enumerate the smallest exact subset of K3-S declarations, bindings, model
  contracts, capabilities, trust records, events, evidence schemas, and
  statuses needed to cover all 13 executable checks in the accepted amendment;
- map each amendment check to K3-S symbols, K3S adversarial cases, and exact
  K1/K2 clauses;
- identify every K2/K3-S branch intentionally outside the finite executable
  slice;
- specify only finite logical fixture values, never host paths, real commands,
  network endpoints, repositories, expected patches, or hidden answers;
- preserve both provenance gates: a future mutation handoff binds an accepted
  base, while a later execution binding can name only a frozen reviewed
  implementation commit;
- state that any implementation ambiguity returns to K2 or K3-S.

It must not create a K3-X file path, implementation language, module layout,
test command, output directory, handoff, dispatch, or mutation authority.

## 10. Acceptance criteria and stop conditions

K3-S is acceptable only if:

1. the deliverable has exactly the ten required top-level sections in order;
2. it makes one minimal-vocabulary decision and maps every item to exact K2
   declaration, meaning, service, identity, dependency, evidence, and model
   roles;
3. all 19 K0 seed challenges have exactly one honest coverage row;
4. the ledger is exhaustive and every retained item has a separating case;
5. exactly 18 ordered adversarial cases and exactly eight complete traces are
   present and derive from general rules;
6. all K1 truth, authority, choice, provenance, closure, consistency, relation,
   profile, and failure families remain unchanged;
7. declaration, binding, capability, trust, and evidence availability stay
   independent;
8. repository snapshots, paths, content observations, changes, trace events,
   and evidence are typed and have no ambient or undeclared access;
9. the broad task-acceptance predicate is reusable, explicitly bounded, and
   non-oracular, and its absence of evaluator remains meaningful;
10. plugin-visible contradiction uses admitted sound reasoning while unresolved
    or cross-plugin claims remain unknown without the exact capability;
11. identity, version, duplicate, conflict, model/machine, dependency, and
    validation-reference rules preserve K2 with no fallback;
12. the K3-X semantic packet covers all 13 amendment checks without granting
    implementation authority;
13. conclusions remain limited to semantic representability over the accepted
    seed scope; and
14. no held-out content, implementation, repository mutation, command/model
    execution, benchmark, downstream handoff, or external artifact appears.

Stop and return to main if:

- any coding requirement needs a new K1 primitive, status, connective,
  authority, choice, provenance, or failure rule;
- the K2 ABI lacks an exact record, lifecycle transition, identity, dependency,
  trust, certificate, or error path required by an accepted case;
- a retained coding primitive has no distinction from a composition or derived
  projection;
- repository state, evidence, or expected outcome must be accessed outside an
  explicit typed facet or declared capability;
- a broad predicate is meaningful only through a hidden expected mapping;
- an operation vocabulary prescribes planning or state-transition execution
  rather than constraining an abstract completed outcome;
- a required result depends on display name, input order, discovery order, or
  silent version substitution;
- held-out information or a concrete K3-X/K4 handoff, path, command, or
  authority would be required.

## 11. Dispatch and verification packet

This candidate handoff grants no mutation authority. After independent handoff
acceptance, main may issue one exact dispatch that binds:

- a clean source commit descending from the accepted K2 and amendment history;
- the accepted handoff blob;
- the sole deliverable path in section 1;
- no external output root and no held-out access;
- one writer, no commit, and a return-on-stop-condition rule.

The future writer must verify at minimum:

```text
git diff --check
git diff --name-only
git status --short
git hash-object KernelPlugin/K3_S_Minimal_Coding_Plugin_Semantics_v0.md
wc -l -c KernelPlugin/K3_S_Minimal_Coding_Plugin_Semantics_v0.md
```

It must also report reproducible counts for the ten headings, 19 seed rows, the
minimality ledger by disposition, 18 adversarial cases, eight traces, code
fences, and final newline. Main freezes any candidate before review. No
acceptance, K3-X handoff, or downstream authority follows automatically from
execution.
