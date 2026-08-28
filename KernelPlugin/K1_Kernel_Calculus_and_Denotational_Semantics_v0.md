# Contract IR kernel calculus and denotational semantics v0

This document specifies a serialization-independent calculus. Its adequacy and
relative-minimality claims are limited to the accepted K0 distinctions and the
candidate construct space considered here.

## 1. Semantic domains and parameter boundary

### 1.1 Domains and notation

All named collections below are abstract sets. `finset(X)` is the set of finite
sets over `X`; sets have no traversal order. `A + B` is a disjoint sum. `X?`
adds absence. Equality of identifiers is exact, not display-name equality.

```text
Outcome O = (PRE, TRACE, FINAL, EVIDENCE)
PRE, FINAL : State
TRACE      : finite sequence of Event
EVIDENCE   : EvidenceStore

Event = (event_value : EventValue, actor : Principal?, controlled : Bool)
Facet = pre | trace | final | evidence
Value, Type, Variable, Principal, ChoiceId, SourceRef, AuthorityRef,
EvidenceRef, UnknownReason, EvaluationErrorReason, ReasoningErrorReason

PluginKey = (plugin_identity, exact_version)
SymbolKey = (PluginKey, namespace, local_name, kind, declared_signature)
ProfileKey = (plugin_identity, exact_version, profile_name)
```

`PRE`, `TRACE`, `FINAL`, and `EVIDENCE` are projections, not commands or
mutable stores. A controlled event is merely an event whose occurrence is
subject to the authorization facet; the calculus neither selects nor performs
events.

A semantic environment is

```text
Sigma = (types, literal_meanings, symbol_meanings, exact_bindings,
         evaluator_capabilities, reasoning_capabilities, profiles,
         authority_facts)
rho   : Variable partial-map Value
kappa : ChoiceId partial-map Value
```

`authority_facts` is a set of attestations
`(AuthorityRef, SourceRef, Principal, NormativeRole)`, where `NormativeRole` is
`REQUIRE`, `AUTHORIZE`, or `BIND_CHOICE(choice_id)`. Its meaning is fixed by
the kernel: the referenced source authorizes that principal to exercise the
named normative role. K2
must say how an attestation is represented and trusted, but may not change this
meaning. Authority is not supplied by predicate evaluation.

Semantic result metadata consists of finite sets. An evidence reference is
equal only when its issuer-scoped stable identity is equal. Reasons are equal
only when their tagged semantic identity and parameters are equal. Set union
therefore deduplicates exact repeats and never depends on serialization or
evaluation order.

### 1.2 Plugin semantic parameter

For each exactly bound `SymbolKey`, `Sigma` may provide:

```text
function meaning : Value* -> Value or TERM_ERROR(reason)
predicate meaning: Value* -> Eval
```

Every outcome component observable by a predicate must be supplied explicitly
through an anchor-derived argument, and its declared facet dependencies must
match those arguments. Every type, literal, function, and predicate meaning
is typed and belongs to one exact `PluginKey`. A predicate result obeys the
kernel `Eval` algebra in section 4; plugins cannot redefine connectives,
truth, errors, evidence aggregation, authority, provenance, or binding.
Capabilities and profiles are also semantic parameters, but their results are
admitted only by section 5. A meaning can be bound while no evaluator exists.

### 1.3 Contract denotation and independently inspectable facets

For a well-formed Contract `C`, `D_Sigma(C)` is the record

```text
Hard(C)       : finite set of authority-adopted requirement formulas
Grants(C)     : finite set of authority-adopted authorization grants
Choices(C)    : finite map ChoiceId -> (Type, finite nonempty alternatives,
                                        controller, ChoiceBinding?)
Origins(C)    : finite set of (clause_id, SourceRef, Clause,
                               optional (AuthorityRef, adopter))
Dependencies(C): finite set of exact PluginKey and SymbolKey requirements
Open(C)       : finite set of unresolved variables, choices, references,
                symbols, versions, and required semantic contracts
```

All facets exist for open Contracts. `Hard` and `Grants` preserve formulas but
are not evaluated while `Open(C)` is nonempty. Composition is compatible set
union (section 3.8), so no facet is overwritten. A well-formed open Contract
has neither a truth result nor a consistency, relation, profile-success, or
acceptance result. It remains `OPEN_BINDINGS` rather than acquiring factual
`UNKNOWN`.

## 2. Abstract syntax and static judgments

### 2.1 Inductive syntax

The following is abstract syntax, not a file format.

```text
Term t ::= Lit[PluginKey](literal : T)
         | Var(x : T)
         | Anchor(pre | trace | final | evidence)
         | Apply(SymbolKey_function, t1, ..., tn)

Formula f ::= Atom(SymbolKey_predicate, t1, ..., tn)
            | Not(f)
            | All(S)                    where S is a finite set of Formula

Clause c ::= Require(f)
           | Authorize(principal, x : EventValue, scope(x), guard(x))

AttributedClause ::= Attribute(clause_id, source, Clause)
Adoption      ::= Adopt(clause_id, authority_ref, adopter)
ChoiceBinding ::= (value, binder, source, authority_ref)
ChoiceDecl    ::= Choice(choice_id, T, finite_nonempty_alternatives,
                         controller, ChoiceBinding?)
Contract      ::= finite sets of AttributedClause, Adoption, ChoiceDecl, and
                  exact symbol/profile requirements
```

`Any(S) := Not(All({Not(f) | f in S}))` and
`Implies(a,b) := Any({Not(a),b})`. These are definitions, not additional
constructors. `TrueF := All({})`; `FalseF := Not(TrueF)`. A choice reference is
`Var(choice_id:T)` whose only possible Contract binding is the corresponding
choice binding. There is no general kernel quantifier: domain quantification
belongs inside a typed plugin predicate because K0 provides no case requiring
kernel enumeration, and infinite or evidence-dependent domains would otherwise
leave its evaluation contract unresolved.

### 2.2 Formation and typing

Judgments have the form `Delta; Gamma |- t : T` and
`Delta; Gamma |- f : Bool`, where `Delta` contains declared exact symbol
signatures and `Gamma` contains lexically bound event variables plus declared
choice variables.

```text
(LIT)    literal is admitted by PluginKey's declared type T
         --------------------------------------------------
         Delta;Gamma |- Lit[PluginKey](literal:T) : T

(VAR)    Gamma(x)=T
         -----------------------
         Delta;Gamma |- Var(x:T) : T

(ANCHOR) pre:State, trace:Trace, final:State, evidence:EvidenceStore

(APP)    Delta(q)=(T1,...,Tn)->T    each Delta;Gamma |- ti:Ti
         ---------------------------------------------------
         Delta;Gamma |- Apply(q,t1,...,tn) : T

(ATOM)   Delta(q)=(T1,...,Tn)->Bool each Delta;Gamma |- ti:Ti
         ----------------------------------------------------
         Delta;Gamma |- Atom(q,t1,...,tn) : Bool

(NOT)    Delta;Gamma |- f:Bool
         ------------------------
         Delta;Gamma |- Not(f):Bool

(ALL)    for every f in S, Delta;Gamma |- f:Bool
         -----------------------------------------
         Delta;Gamma |- All(S):Bool
```

`Require(f)` is formed under the Contract choice environment. In
`Authorize(p,x:T_event,scope,guard)`, `p` must be a principal, `T_event` must be
the trace's declared `EventValue` type, and both formulas type-check under
`Gamma,x:T_event`. A choice binding must be a member of its declared
alternatives, have its declared type, name the declared controller as binder,
and carry a `BIND_CHOICE(choice_id)` authority claim for its source. Its
resolved fact must match; absence leaves the binding open and mismatch is
malformed. Choice IDs and clause IDs are unique; repeated declarations must be
exactly identical or the Contract is malformed.

Every `Adopt` must reference exactly one existing `Attribute`. It is locally
well formed only if its authority claim names `(authority_ref, source, adopter,
role(Clause))` from that attribute. When the reference resolves, the authority
fact must match that tuple exactly; a mismatch is malformed and an absent fact
remains open. Only a resolved match contributes the attributed clause to
`Hard` or `Grants` at closed-Contract evaluation. A quotation may therefore
remain in `Origins` as attributed content without normative adoption.
Provenance is never inferred from wording.

### 2.3 Structure, closure, and evaluability

`WELL_FORMED` means all inductive rules, uniqueness rules, declared signatures,
choice constraints, and authority-attestation checks pass. A bound semantic
contract whose signature or declared identity differs is `MALFORMED`; an absent
exact contract is instead a well-formed unresolved reference.

`CLOSED` means every free variable is bound, every choice is bound by its
controller, every source/authority reference resolves, and every exact
`SymbolKey` and `PluginKey` dependency has a matching semantic contract in
`Sigma`. Otherwise the result is `OPEN_BINDINGS(the exact finite missing set)`.
No compatible-looking version is substituted. Lexical event variables are
bound by `Authorize` and do not make a Contract open.

For a requested judgment `j`, `EVALUABILITY_AVAILABLE(capability_refs)` means
the exact bound semantics declare all services required by `j`.
`EVALUABILITY_MISSING(missing_capability_refs)` means at least one exact service
is absent; discovery that cannot determine this is `EVALUABILITY_UNKNOWN`.
These results do not adopt clauses, bind choices, or imply truth.

Representation remains a source-to-semantics judgment:
`REPRESENTABLE` requires an equivalent Contract denotation;
`UNRESOLVED(reason)` preserves multiple or controller-pending bindings; and
`UNREPRESENTABLE(reason)` records an in-scope distinction absent from the
calculus. It is not inferred merely from well-formedness.

## 3. Denotational semantics and normative roles

### 3.1 Terms and atoms

For closed bindings, `[[t]]_{Sigma,rho,kappa,O}` is defined recursively.
Literals use their exact plugin-version meaning; variables use `rho` or
`kappa`; anchors project the correspondingly named component of `O`; and
function application applies the exact bound meaning to recursively obtained
arguments. A term error makes its enclosing atom return `ERROR` with that
reason. An absent binding is not evaluated: it was already `OPEN_BINDINGS`.

An atom evaluates its terms, then invokes only its exact bound predicate
meaning with the resulting values; anchor-derived arguments are its only
access to outcome facets. This gives
`[[f]]` by the rules in section 4. A plugin atom may be broad, but only its
declared typed meaning, dependencies, facet boundary, evidence contract,
unknown behavior, error behavior, and capability limits give it meaning. Its
name conveys none.

### 3.2 Requirements and hard acceptance

For a closed Contract and outcome `O`, let

```text
ReqEval(C,O)  = eval(All(Hard(C)), O)
AuthEval(C,O) = authorization-compliance evaluation from section 3.3
AcceptEval(C,O) = ALL_RESULT({ReqEval(C,O), AuthEval(C,O)})
```

`O` is accepted exactly when `AcceptEval` is `VALUE(TRUE,...)`. `FALSE` rejects
it, `UNKNOWN` leaves acceptance undetermined, and `ERROR` yields no truth or
acceptance conclusion. This is hard acceptance relative to the expressed
Contract, never a certificate of intent completeness.

### 3.3 Grants and authorization

For an adopted grant `g = Authorize(p,x,scope,guard)` and controlled trace event
`e` with `e.actor=p`, define

```text
GrantEval(g,e,O) = eval(All({scope, guard}), rho[x := e.event_value], O)
```

For every controlled event `e`, collect all grants naming `e.actor`. Its
authorization result is `ANY_RESULT` over their `GrantEval` results; the empty
set is `FALSE`. `AuthEval` is `ALL_RESULT` over all controlled-event results;
the empty controlled trace is `TRUE`. Thus an occurrence with no true grant is
unauthorized and makes compliance `FALSE` (unless an evaluation error prevents
a truth result); an unknown grant leaves it unknown if no grant is true. A
grant never requires an event: when no controlled event occurs, compliance is
vacuously true.

`scope` identifies which event a grant concerns; `guard` states the condition
under which it is granted. Both are formulas so their unknown, evidence, and
error behavior is fixed by section 4. Evaluability supplies facts but cannot
create a grant. This is a declarative condition over a completed trace, not an
execution policy.

### 3.4 Conditionality, alternatives, states, and choices

A conditional requirement is `Require(Implies(condition, consequence))`. A
conditional permission is `Authorize(p,x,scope,condition)`. The former can fail
when the condition is true and the consequence false; the latter cannot fail
merely because no matching event occurs.

Alternative acceptable outcomes use `Any({a,b,...})` inside a requirement.
They are factual disjunctions evaluated for an outcome. An owned choice instead
declares a controller and remains in `Open(C)` until that controller supplies a
listed binding. Alternatives do not choose a value, and a missing factual input
is `TRUTH_UNKNOWN`, not an authority to choose.

State and trace distinctions are explicit because atoms receive projections:
a final-state atom sees `FINAL`; a preservation atom receives both `PRE` and
`FINAL`; an occurrence atom receives `TRACE`; an evidence-dependent atom
receives `EVIDENCE`. Equal final states do not imply equal traces, and a fixed
final target is not a relation to a varying baseline.

### 3.5 Provenance, authority, and exact versions

Adoption affects normative force, not proposition truth. Two sources may carry
identical formula content, but only a matching authority attestation admits an
`AdoptedClause`. `Origins(C)` remains independently inspectable even when two
adopted formulas are propositionally equivalent. Exact symbol/version
dependencies participate in term and atom meanings and in semantic equivalence;
same display name or a newer version is insufficient.

### 3.6 Derived readable forms and facet-preservation proofs

For an origin tuple `o`, the following macros copy `o` unchanged onto the
single expanded clause and introduce no choices or bindings:

```text
GOAL(P)                := Require(P(FINAL))
PRESERVE(R)            := Require(R(PRE, FINAL))
FORBID(Occurs)          := Require(Not(Occurs(TRACE)))
ALLOW(p, x, Scope)      := Authorize(p, x, Scope(x), TrueF)
```

Here `P`, `R`, and `Occurs` are typed exact plugin predicates, not new kernel
symbols. `FORBID` means non-occurrence, which is stronger than merely omitting
a grant. `ALLOW` grants authority and does not assert occurrence.

The proof for each macro is definitional expansion. For every `Sigma`, binding,
and `O`, the expanded term/formula is the macro's stated meaning; hence truth,
error, evidence sets, and unknown-reason sets are identical, not merely
two-valued acceptance. Copying `o` preserves provenance and authority; copying
the exact symbol references preserves plugin versions; identical free variables
preserve closure and choice ownership. `GOAL` changes no authorization facet.
`PRESERVE` changes none. `FORBID` adds one hard requirement and no grant.
`ALLOW` adds one grant and no hard occurrence condition. Thus acceptance,
authorization, provenance, binding, version, truth, evidence, unknown-reason,
and error facets are preserved wherever applicable.

### 3.7 Soft preference

A ranking among already accepted outcomes is `UNREPRESENTABLE(outside accepted
K0 scope)` in this calculus. It is never rewritten as `Require`. Adding an
ordering would require a revised, independently accepted semantic boundary.

### 3.8 Contract composition

`C1 compose C2` is derived as union of all six denotational facets. It is
well-formed only when shared IDs have identical declarations; otherwise it is
`MALFORMED(conflicting declaration)`. Union does not erase origins or locally
proved results. Hard constraints and authorization compliance are jointly
evaluated by `All`; plugin-local satisfiability does not imply satisfiability of
the union.

## 4. Truth, error, and composition laws

### 4.1 Total result algebra

```text
Truth = TRUE | FALSE | UNKNOWN
Eval  = VALUE(Truth, evidence : finset(EvidenceRef),
                     unknowns : finset(UnknownReason))
      | ERROR(errors : nonempty finset(EvaluationErrorReason),
              evidence : finset(EvidenceRef),
              unknowns : finset(UnknownReason))
```

`VALUE(UNKNOWN,...)` requires a nonempty unknown set; `TRUE` and `FALSE` may
carry unknown reasons collected from non-decisive children. Every `ERROR` has a
nonempty error set. Evidence sets may be empty for any result.

For a `VALUE`, `unknowns` contains reasons returned by semantically relevant
children, even when another child determines `TRUE` or `FALSE`. The public K0
truth status is `TRUTH_TRUE(evidence)`, `TRUTH_FALSE(evidence)`, or
`TRUTH_UNKNOWN(unknowns,evidence)`; decisive-result unknowns remain companion
diagnostic metadata rather than being discarded. `ERROR` renders
`EVALUATION_ERROR(errors)` and carries its evidence/unknown metadata without
creating a truth status.

All operands are semantically relevant. First union all child evidence and
unknown sets. If any child is `ERROR`, return `ERROR` with the union of every
child error set and the same metadata unions. Thus errors dominate rather than
being masked by a decisive truth value. Otherwise apply the truth tables below.
This rule is mathematical aggregation, not an instruction to evaluate in an
order.

### 4.2 Truth/error table T1 — negation

`Not` preserves all metadata and any error unchanged.

| child | result truth |
|---|---|
| `TRUE` | `FALSE` |
| `FALSE` | `TRUE` |
| `UNKNOWN` | `UNKNOWN` |
| `ERROR(R,E,U)` | `ERROR(R,E,U)` |

### 4.3 Truth/error table T2 — finite conjunction `All`

After the error-dominance rule:

| child truth multiset | result truth |
|---|---|
| contains `FALSE` | `FALSE` |
| no `FALSE`, contains `UNKNOWN` | `UNKNOWN` |
| all `TRUE`, including the empty set | `TRUE` |

Evidence and unknown reasons are unions from all children in every row,
including children made truth-irrelevant by a `FALSE`.

### 4.4 Truth/error table T3 — derived alternatives `Any`

Expansion through `Not` and `All` yields:

| child truth multiset | result truth |
|---|---|
| contains `TRUE` | `TRUE` |
| no `TRUE`, contains `UNKNOWN` | `UNKNOWN` |
| all `FALSE`, including the empty set | `FALSE` |

The same error dominance and all-child metadata unions apply, including an
unknown child beside a decisive `TRUE`.

### 4.5 Truth/error table T4 — derived implication

Rows are the condition, columns the consequence.

| `Implies` | `TRUE` | `FALSE` | `UNKNOWN` |
|---|---:|---:|---:|
| `TRUE` | `TRUE` | `FALSE` | `UNKNOWN` |
| `FALSE` | `TRUE` | `TRUE` | `TRUE` |
| `UNKNOWN` | `TRUE` | `UNKNOWN` | `UNKNOWN` |

An error in either operand yields the unioned `ERROR`, even in a truth-decisive
cell. Evidence and unknown reasons from both operands are unioned in every cell.

### 4.6 Aggregation rule A1 — formulas and grants

For every `Not`, `All`, derived `Any`, implication, grant conjunction,
per-event grant alternative, requirement conjunction, authorization-compliance
conjunction, and final acceptance conjunction: (1) operands form a finite set;
(2) evidence, unknown reasons, and errors use set union; (3) any error dominates;
(4) otherwise T1--T4 determine truth. Empty `All` is true and empty `Any` false.
There is no omitted short-circuit metadata.

### 4.7 Aggregation rule A2 — term and atom boundaries

Argument term errors are unioned before predicate invocation; any term error
prevents invocation and returns `ERROR`. If invocation occurs, its returned
sets are preserved exactly. A plugin may cite multiple evidence items or
unknown causes but cannot prioritize one by return order. Repeated equal
references/reasons collapse by semantic set equality.

### 4.8 Laws

At full `Eval` granularity, `All` and `Any` are commutative, associative,
idempotent, and have identities `TrueF` and `FalseF`; set syntax and set-union
metadata make these laws exact. `Not(Not(f)) = f`, and De Morgan laws hold for
truth, errors, evidence, and unknown reasons. Implication has only the laws of
its expansion. Replacing `f` by a merely truth-equivalent formula is unsafe if
its evidence, unknown, error, provenance, binding, or version facets differ.
No error is a truth value or licenses consistency, completeness, entailment, or
equivalence.

No quantifier truth table is needed because quantification is not a kernel
construct. A plugin predicate that quantifies must declare its domain, empty
case, evidence, unknown, and error behavior and still return this `Eval` type.

## 5. Kernel judgments, reasoning, and normalization

### 5.1 Judgment meanings and admissible evidence

| Family | Meaning and admissible evidence | Owner |
|---|---|---|
| Representation | Equivalent binding from source intent, or explicit unresolved/unrepresentable reason; never syntax alone. | Binding analysis using kernel denotation |
| Well-formedness | Derivation by section 2 rules; failure names the violated rule. | Kernel, parameterized by declared signatures/authority facts |
| Closure | Exact finite set of missing bindings, or none. | Kernel |
| Evaluability | Availability of exact requested evaluator/reasoner capability; absence and indeterminate discovery stay distinct. | Declared plugin/cross-plugin capability |
| Formula truth/failure | Section 4 `Eval` over a closed Contract and concrete `Outcome`; error produces no truth. | Kernel composition over plugin atoms |
| Consistency | `SAT` needs an accepted witness; `UNSAT` needs a sound kernel derivation or admitted proof; otherwise `UNKNOWN`. | Kernel plus admitted capabilities |
| Profile completeness | Coverage of every dimension in one exact `ProfileKey`, with evidence; missing/unknown stay explicit. | Versioned profile parameter |
| Entailment/equivalence | Sound proof or counterexample under all facets and exact dependencies; otherwise `RELATION_UNKNOWN`. | Kernel plus admitted capabilities |
| Reasoning failure | Protocol/service failure gives `REASONING_ERROR` and no relation or consistency result. | Kernel failure boundary |

Intent completeness cannot be certified from a Contract. Profile completeness,
truth, and satisfiability imply none of one another except through an explicitly
proved rule.

### 5.2 Satisfaction and core reasoning

A satisfying witness is `(O,kappa,evidence)` for a closed semantic environment
such that the choice bindings are controller-valid, exact plugin meanings are
used, supplied evidence validates, and `AcceptEval(C,O)` is `VALUE(TRUE,...)`.
It may be abstract; it need not be a patch or an executor output.

Core rules are:

```text
All({f, Not(f)}) is UNSAT                         (K-CONTRA)
VALUE(TRUE,...) for accepted witness w => SAT(w) (K-WITNESS)
C1 facet-equivalent C2 => EQUIVALENCE            (K-EQUIV)
accepted countermodel O with C1 true, C2 nontrue
    => disprove entailment C1 |= C2               (K-COUNTER)
```

`K-CONTRA` is sound because T1/T2 have no truth assignment making both operands
true; evaluator failure cannot refute that denotational fact. `K-WITNESS` is
sound by the definition of acceptance. `K-EQUIV` requires equality of hard
`Eval` functions for every outcome and binding, grant/authorization functions,
choice/open-binding facets, origins/authority facets, and exact version
dependencies. Proposition-only equivalence is insufficient.

Formula entailment `f |= g` means that, under one exact closed `Sigma`, every
valuation/outcome making `f` logically `TRUE` makes `g` logically `TRUE`.
Acceptance entailment `C1 |=accept C2` means every completion and outcome
accepted by `C1` under their common exact environment is accepted by `C2`; it
does not transfer provenance or authority. Full Contract equivalence is the
stronger `K-EQUIV` facet equality above. A relation request must name which of
these relations it asks; results are never silently converted among them.

### 5.3 Capability-relative proof admission

A plugin witness, proof, model, counterexample, entailment, or equivalence
claim is admitted only if it identifies exact semantics and dependencies, lies
inside the capability's declared sound fragment, has a valid trust attestation,
and its conclusion is the judgment requested. `COMPLETE_FOR_DECLARED_FRAGMENT`
permits `UNKNOWN` only outside that fragment; `PARTIAL_SYMBOLIC_REASONING` and
`CONCRETE_EVALUATION_ONLY` never turn lack of result into a conclusion.

A plugin-local proof ranges only over its declared symbols. Separate local
`SAT` results do not establish a shared witness and cannot establish joint
cross-plugin `SAT`, entailment, or equivalence. A joint result requires an
explicitly bound sound capability whose declared dependency set covers the
whole joint formula. Without an accepted witness/proof/counterexample the
result is `CONSISTENCY_UNKNOWN` or `RELATION_UNKNOWN`. Service or protocol
failure is `REASONING_ERROR` and yields no member of either family.

Abstractly, a reasoning request returns exactly one of an admitted judgment or
`REASONING_ERROR(nonempty finset(ReasoningErrorReason))`. If a declared joint
request depends on multiple services, all participating service failures are
set-unioned and any failure dominates: no consistency or relation judgment is
returned. This aggregation is order-independent and does not turn completed
inconclusive results into errors or errors into `UNKNOWN`.

### 5.4 Profile completeness

For exact profile `P`, `PROFILE_COMPLETE(P,E)` requires evidence `E` covering
every versioned dimension declared by `P`. A known omitted dimension produces
`PROFILE_INCOMPLETE`; inability to decide coverage produces `PROFILE_UNKNOWN`.
Neither changes acceptance or satisfiability and none certifies unstated intent.

### 5.5 Normalization policy

The only kernel normalizations are alpha-renaming of the bound authorization
event variable, the definitional expansion of `Any`, `Implies`, `GOAL`,
`PRESERVE`, `FORBID`, and `ALLOW`, and mathematical canonicalization of finite
sets. Alpha-renaming preserves environments by capture-free bijection.
Definitional expansions preserve every facet by sections 3.6 and 4; finite-set
canonicalization preserves set membership and union metadata. No distribution,
atom rewriting, provenance erasure, version substitution, or proposition-only
deduplication is authorized. There is no promised additional normal form.

These rules are sound only under the stated semantics and admitted capability
assumptions. They establish neither universal decidability nor completeness.

## 6. Minimality and derived-form ledger

The controlled examples below keep `Sigma`, bindings, origins, and all unrelated
clauses fixed. `CP-a/b` means the two named cases differ only in the stated
feature. This supports relative minimality for the accepted cases, not absolute
minimality over all possible calculi.

| Construct or role | Disposition | Denotation/derivation | Controlled pair or proof; why simpler composition fails | K0 |
|---|---|---|---|---|
| Completed `Outcome` tuple | RETAINED_PRIMITIVE | §1.1 projections | CP-O: same formula/bindings, two outcomes differing only in observed final value must differ; without an outcome argument constraints denote no completed result | C01,C19 |
| Plugin-typed literals | PLUGIN_PARAMETER | §1.2, §3.1 | Exact type/value meaning is domain-specific; the kernel only preserves its key | C11 |
| Typed variables and binding | RETAINED_PRIMITIVE | §2.1--2.3 | CP-V: same grant and trace, binding `x` to the current event versus an unrelated event distinguishes scope; constants cannot relate each iterated event without vocabulary growth | C04,C06,C08 |
| `PRE` anchor | RETAINED_PRIMITIVE | `O.PRE` | SP-03 with only baseline varied; a final constant cannot preserve a varying relation | C02,C18,C19 |
| `TRACE` anchor | RETAINED_PRIMITIVE | `O.TRACE` | SP-02 uses identical final states and differing transient traces | C03,C04,C06 |
| `FINAL` anchor | RETAINED_PRIMITIVE | `O.FINAL` | SP-02 converse: equal trace prefix can end in differing final states; trace occurrence is not final property | C01,C07 |
| `EVIDENCE` anchor | RETAINED_PRIMITIVE | `O.EVIDENCE` | CP-E: identical states/trace, suite evidence present versus absent yields true versus unknown | C09,C15 |
| Plugin functions | PLUGIN_PARAMETER | exact typed function meaning §1.2 | State projections and domain computations are not core logic | C02,C11 |
| Plugin predicates/atoms | PLUGIN_PARAMETER | exact typed predicate `Eval` §1.2 | Atomic domain meaning cannot be composed from domain-independent connectives | all semantic cases |
| Negation `Not` | RETAINED_PRIMITIVE | T1 | CP-N: with a fixed positive occurrence atom, require occurrence versus require non-occurrence; positive atoms/`All` alone cannot complement its accepted set | C03,C10 |
| Finite conjunction `All` | RETAINED_PRIMITIVE | T2 | CP-C: outcomes satisfy only `a`, only `b`, or both; requiring both cannot be represented by either atom or negation alone | C10,C14 |
| Alternatives `Any` | DERIVED | `Not(All(Not children))` | T1--T3 prove identical truth/error/evidence/unknown results and bindings | C07 |
| Conditionality `Implies` | DERIVED | `Any({Not(a),b})` | T4 is the full result-level derivation; no new normative role is needed | C05,C09 |
| General quantification | EXCLUDED | delegated inside atom | No K0 pair forces kernel enumeration; adding it would require unresolved domain/evaluation semantics | C11,C12 |
| Hard `Require` role | RETAINED_PRIMITIVE | §3.2 | SP-01: with condition true and event absent, requirement fails while permission succeeds | C01,C05 |
| `Authorize` role with principal/event scope/guard | RETAINED_PRIMITIVE | §3.3 | SP-01: same condition/event proposition; occurrence is optional but, if controlled, must have a true grant | C04,C06 |
| Owned choice plus controller | RETAINED_PRIMITIVE | §1.3, §3.4 | SP-05 holds alternatives fixed: controller may bind one case; nobody may choose the unavailable fixed fact | C08 |
| Provenance attachment | RETAINED_PRIMITIVE | `Origins(C)` §3.5 | SP-04 holds text fixed and changes only source; erasing origin makes the variants identical | C17 |
| Authority attestation/adoption | RETAINED_PRIMITIVE | §1.1, §2.2 | SP-04 holds content/source record fixed but varies valid adoption authority; only one contributes a clause | C17 |
| Exact plugin identity/version dependency | RETAINED_PRIMITIVE | `Dependencies(C)` §3.5 | CP-P: same display name, incompatible v1/v2 meanings; substituting v2 changes truth and closure | C13,C15,C16 |
| Contract composition | DERIVED | compatible facet-wise set union §3.8 | Union preserves all facets; a new connective would add no distinction | C14 |
| `GOAL` | DERIVED | §3.6 | Definitional full-facet proof §3.6 | C01 |
| `PRESERVE` | DERIVED | §3.6 | Definitional full-facet proof §3.6 | C02,C18,C19 |
| `FORBID` | DERIVED | §3.6 | Definitional full-facet proof; not confused with absent authority | C03 |
| `ALLOW` | DERIVED | §3.6 | Definitional full-facet proof; empty trace proves no obligation | C04 |
| Three truth values | RETAINED_PRIMITIVE | §4.1--4.5 | CP-U: same closed condition before versus after decisive evidence; collapsing unknown with true or false changes release acceptance | C09 |
| Evaluation error boundary | RETAINED_PRIMITIVE | §4.1 | SP-06 fixes request and varies missing evidence versus evaluator crash; one returns truth unknown, the other no truth | C09 |
| Evidence-reference set | RETAINED_PRIMITIVE | §1.1, A1/A2 | CP-R: same truth with independent signed versus unsigned observations; erasure loses admissible support | C01,C15 |
| Unknown-reason set | RETAINED_PRIMITIVE | §1.1, A1/A2 | CP-UR: same unknown truth with missing suite result versus inaccessible manifest; reason determines what remains unresolved | C09,C12 |
| Reasoning-error boundary | RETAINED_PRIMITIVE | §5.3 | CP-RE: same query with completed inconclusive service versus crashed service; only the first yields relation/consistency unknown | C12,C14 |
| Capability declarations/proof assumptions | PLUGIN_PARAMETER | §5.3 | Domain proof soundness/fragment is not core-denotable; kernel only gates admission | C11,C12,C14 |
| Versioned completeness profile | PLUGIN_PARAMETER | §5.4 | Required dimensions are domain-specific; kernel fixes only relative status laws | C19 |
| Authorization compliance | DERIVED | nested `Any` grants and `All` events §3.3 | T2/T3 give full truth/error/evidence/unknown behavior | C03,C04,C06 |
| Soft preference ordering | EXCLUDED | outside accepted scope §3.7 | SP-08 requires ranking, which hard truth cannot preserve | SP-08 |
| Coding task/operation taxonomy | EXCLUDED | no denotation | No K0 distinction requires it; would be a domain-specific core branch | all |

Ledger counts: **19 `RETAINED_PRIMITIVE`; 8 `DERIVED`; 5
`PLUGIN_PARAMETER`; 3 `EXCLUDED`** (35 rows).

## 7. K0 challenge coverage and separating derivations

In this section, `A_*`, `F_*`, and `R_*` are schematic typed plugin atoms,
functions, and relations with fresh exact keys. They describe assumptions only;
they do not select K3 names or interfaces.

### 7.1 Nineteen-challenge coverage table

| ID | Kernel structure | Abstract plugin assumptions | Applicable K0 judgments | Distinction | Unknown/failure path | Shortcut avoided |
|---|---|---|---|---|---|---|
| K0-C01 | `Require(A_win(FINAL,EVIDENCE))` | typed platform observation/evidence meaning | `REPRESENTABLE`; evaluator available | positive final acceptance | missing observation -> truth unknown; evaluator fault -> error | no patch/ID lookup |
| K0-C02 | `Require(R_public(PRE,FINAL))` | comparative observation relation | representable; evaluator available | pre/final preservation | incomplete domain evidence -> unknown | no fixed final list |
| K0-C03 | `Require(Not(A_contact(TRACE)))` | trace occurrence meaning | representable; evaluator available | trace prohibition | absent trace evidence -> unknown | no final-state inference |
| K0-C04 | `Authorize(p,x,A_regen(x),A_metadata_changed(PRE,FINAL))` | event scope and metadata relation | representable; evaluator available | conditional permission | unknown guard leaves occurring event authorization unknown | no obligation/evaluability authority |
| K0-C05 | `Require(Implies(A_metadata_changed(PRE,FINAL),A_regen(TRACE)))` | same meanings as C04 | representable; evaluator available | conditional obligation | unknown condition follows T4 | no unconditional/permission rewrite |
| K0-C06 | conditional `Authorize` as C04 | edit scope and schema relation | representable; evaluator available | permission without duty | error in guard -> evaluation error if event occurs | no invented edit |
| K0-C07 | `Require(Any({A_toml(FINAL),A_yaml(FINAL)}))` | two typed acceptance atoms | representable; evaluator available | acceptable alternatives | both unknown -> unknown | no fixture choice/both requirement |
| K0-C08 | unbound `Choice(storage,T,{local,hosted},user,none)` | meanings for alternatives only | `UNRESOLVED`; `WELL_FORMED`; `OPEN_BINDINGS` | controller-owned discretion | remains open, never truth unknown | no default/executor ownership |
| K0-C09 | `Require(Implies(A_release(FINAL,TRACE),A_suite(EVIDENCE)))` | suite fact/evidence meaning | representable; evaluator available; truth unknown pre-evidence | factual uncertainty | missing evidence -> unknown when release occurs; crash -> error | nobody chooses fact |
| K0-C10 | `Require(All({a,Not(a)}))` | same exact bound atom `a` | representable; well formed; closed; consistency unsat | kernel contradiction | evaluator error yields no concrete truth but K-CONTRA remains sound | not malformed/plugin special case |
| K0-C11 | conjunction of nonempty/bounds atoms | sound numeric-domain proof capability | representable; well formed; closed; evaluator available; unsat | plugin contradiction | proof failure -> consistency unknown; service fault -> reasoning error | no numeric kernel rule |
| K0-C12 | `Require(All({A_preserve,A_reduce}))` | sampled evaluation only; no complete joint reasoner | representable; local evaluator available; consistency unknown | capability-relative uncertainty | no witness/proof -> unknown | no sampled universal SAT |
| K0-C13 | requirement references exact retired key | mandated meaning declared; exact service absent | representable; open bindings; evaluability missing | version closure vs capability | no substitution; discovery uncertainty stays evaluability unknown | no name-based rebind |
| K0-C14 | composed requirements with two exact plugin keys | local reasoners only | representable; local evaluability; joint consistency unknown | cross-plugin composition | absent joint capability -> unknown; failure -> reasoning error | no local-to-joint promotion |
| K0-C15 | `Require(A_rubric(inputs,FINAL,EVIDENCE))` | explicit typed/versioned meaning, dependencies, evidence boundary, evaluator | representable; closed; evaluator available | legitimate broad atom | declared unknown/error only | no gold/ID access |
| K0-C16 | same exact atom/meaning as C15 | semantic binding present, evaluator absent | representable; closed; evaluability missing | denotation vs service | no truth judgment requested | not meaningless/satisfied |
| K0-C17 | same formula under two source records | source-authentication authority fact | representable; source evidence available | content vs normative adoption | unresolved authority ref -> open | no authority from wording |
| K0-C18 | both phrasings bind to `Require(R_public(PRE,FINAL))` | one declared observation relation | representable; relation proved equivalence | surface-independent meaning | ambiguous binding would be unresolved | no phrase atoms |
| K0-C19 | preservation/translation requirements | accepted abstract witness; concrete-evidence profile | representable; consistency sat; profile incomplete | satisfiability vs implementation evidence | missing profile dimension remains incomplete | no patch oracle/inconsistency |

Coverage count: **19** (`C01`--`C19`).

### 7.2 Ten separating-pair derivations

| Pair | Denotational derivation or countermodel |
|---|---|
| SP-01 obligation/permission | Set condition `c=TRUE`, no regeneration event. `Implies(c,occurs)=FALSE`, so C05 rejects. C04 has no controlled occurrence, so authorization compliance is empty `All=TRUE`; it accepts if other requirements do. With an occurrence and `c=TRUE`, both can accept. Omission is the separator. |
| SP-02 final/trace | Outcomes share `FINAL` without `.tmp-key`; one trace creates then deletes it, the other never creates it. Final atom is true for both. `Not(occurs(TRACE))` is false only for the first. |
| SP-03 preservation/fixed final | At baseline `PRE1` matching manifest `M`, both intents accept `FINAL=M`. Change only baseline to `PRE2 != M` and final to `PRE2`: preservation is true while fixed-manifest final is false. |
| SP-04 provenance/content | Hold formula text fixed. Variant A has a matching authenticated-user authority attestation and enters `Hard/Grants`; variant B retains the issue-comment source only as evidence and contributes no adopted clause. `Origins` and normative facets differ. |
| SP-05 choice/unknown fact | Both expose `{local,hosted}`. The declared user may close the owned choice with either alternative. The manifest case has no choice declaration; before its fixed value is evidenced, its atom is truth unknown and no principal may bind it. |
| SP-06 unknown/error | Missing suite evidence returns `VALUE(UNKNOWN,E,{missing-suite})`. A crash returns `ERROR({crash},E,U)`. T1--T4 preserve the former truth and the latter absence of truth. |
| SP-07 satisfiability/profile | C19 witness makes `AcceptEval=TRUE`, deriving `CONSISTENCY_SAT`. The exact profile lacks concrete implementation evidence, independently deriving `PROFILE_INCOMPLETE`; neither judgment rewrites the other. |
| SP-08 hard/preference | Hard limit rejects an over-limit outcome. Of two under-limit outcomes both satisfy hard acceptance; the requested ranking distinguishes them, but no kernel denotation does. Preference is therefore explicitly outside scope rather than hardened. |
| SP-09 closure/evaluability | C15 and C16 have identical exact semantic bindings, so both are `CLOSED`. Only C15 has the compatible evaluator capability. Their denotations are meaningful in both cases while evaluability differs. |
| SP-10 local/joint reasoning | Let local reasoners each return a satisfying local model with incompatible shared dependency values. Neither model witnesses the conjunction. Without a declared joint capability, composition is representable but joint consistency is unknown. |

Coverage count: **10** (`SP-01`--`SP-10`).

### 7.3 Required worked derivations and countermodels

**W1 — C04/C05 conditional roles.** The SP-01 calculation covers all truth
states through T4. For C04 an occurring event evaluates `scope AND condition`;
no occurrence adds no formula. For C05 the hard implication is evaluated even
without occurrence. Evidence/unknown sets union from condition and occurrence
in both; any operand error dominates. Origins, bindings, and exact versions are
held equal, leaving only the normative role to separate them.

**W2 — C08/C09 discretion versus fact.** C08 has
`Open={choice_id}` and no `Eval`; a controller-valid binding closes it. C09 is
closed and its evidence atom returns `VALUE(UNKNOWN,{},{missing-suite})`.
Changing C09 requires evidence, not a choice binding. Thus representation,
binding, truth, provenance, and authority facets cannot be exchanged.

**W3 — C10 kernel contradiction.** For any logical value `v`, T1 gives
`not(v)`. T2 applied to `{v,not(v)}` is never true: it is false for `TRUE` and
`FALSE`, unknown for `UNKNOWN`. Hence no satisfying truth assignment exists,
and K-CONTRA proves `CONSISTENCY_UNSAT` although both atoms type-check.

**W4 — C11 plugin contradiction.** Assume a sound admitted plugin proof states:
`nonempty(B) AND forall b in B,size(b)<100KiB AND size(b)>=200KiB` has no model
under one exact unit/version meaning. The proof covers the entire conjunction
and its nonempty premise, so section 5.3 admits `CONSISTENCY_UNSAT`. Without
that proof the kernel sees opaque atoms and returns unknown; it does not encode
numeric ordering.

**W5 — C12 undecided conflict.** Sampled successes are neither a universal
witness nor a refutation. No core contradiction applies and the declared
capability is partial. Therefore the only sound consistency result is
`CONSISTENCY_UNKNOWN(no accepted joint witness or refutation)`; a service crash
would instead be `REASONING_ERROR`.

**W6 — C13 exact version.** The syntax declares key `q@v1`; only incompatible
`q@v2` is offered. Exact lookup leaves `q@v1` in `Open`, and its requested
evaluator in the missing-capability set. No formula truth is evaluated. Display
name equality supplies neither closure nor migration.

**W7 — C14 cross-plugin countermodel.** Plugin A's local model assigns shared
dependency `d=1`; plugin B's assigns `d=2`. Both local formulas are satisfiable,
but no shared witness follows. With no capability covering `{A,B}` jointly,
the composed `All` remains `CONSISTENCY_UNKNOWN`; core conjunction remains
unchanged.

**W8 — C15/C16 broad meaning.** Both bind the identical typed/versioned atom,
facet dependencies, evidence schema, and unknown/error contract, so both are
closed and denotationally equal. Only the capability sets differ. C15 may yield
an `Eval`; C16 yields `EVALUABILITY_MISSING` and no truth. Broadness neither
creates an oracle nor makes the absent evaluator semantic absence.

**W9 — C17 authority countermodel.** Use identical proposition `p`. In A,
`authority_facts` validates the user's adoption, so `p` enters `Hard`. In B,
the untrusted quote has a source record but no matching authority attestation,
so `p` does not enter `Hard`. Assign `p=FALSE`: A rejects, B (absent other
requirements) accepts. Content truth is unchanged; provenance/adoption differs.

**W10 — C18 surface equivalence.** Binding analysis maps both phrasings to the
same exact relation atom over `(PRE,FINAL)` with the same origin/adoption rule.
Their five denotational facets are equal, so K-EQUIV proves equivalence. No
surface strings enter the calculus.

**W11 — C19 abstract satisfaction.** An admitted abstract `Outcome` witness
makes the preservation and translation atoms true with accepted evidence, so
K-WITNESS gives `CONSISTENCY_SAT`. The separately bound profile lacks its
concrete-implementation-evidence dimension and is `PROFILE_INCOMPLETE`. The
witness is not an implementation or construction method.

### 7.4 Derived-form proof matrix

| Form | Acceptance/truth/error/evidence/unknown | Authorization | Provenance/authority | Binding/version |
|---|---|---|---|---|
| `GOAL` | identical to its expanded final-state requirement by definition | adds none | origin copied | same free refs/exact key |
| `PRESERVE` | identical to expanded pre/final relation requirement | adds none | origin copied | same free refs/exact key |
| `FORBID` | T1 on the same occurrence result; all metadata/error preserved | adds no grant; prohibits occurrence | origin copied | same free refs/exact key |
| `ALLOW` | adds no hard truth condition | exact unconditional grant; empty trace remains compliant | origin copied | same event binder/exact keys |
| `Any` | T1/T2 derive T3 with identical unions and error dominance | unchanged wherever embedded | unchanged | unchanged |
| `Implies` | T1/T3 derive T4 with identical unions and error dominance | conditional grant uses guard directly, not this macro | unchanged | unchanged |
| Contract composition | `All` of unioned hard sets | unioned grants, then same per-event rules | origins/attestations unioned | choices/dependencies unioned or malformed on conflict |
| Authorization compliance | nested T3 per event and T2 across events | definition itself | grant origins retained | grant bindings/keys retained |

## 8. K2 semantic obligations and unresolved interface questions

The left column is frozen kernel meaning. The right column is an interface
question K2 may answer without changing that meaning.

| Frozen semantic obligation | Unresolved K2 interface choice |
|---|---|
| Every type/function/predicate has typed, namespaced, exact-version identity; mismatches never silently bind. | Transport, registration, identity encoding, compatibility and explicit migration declarations. |
| Model-facing documentation and machine evaluation identify the same exact semantic key and contract. | How identity is displayed, resolved, signed, and compared mechanically. |
| Function/atom meanings declare argument/result types and permitted `Outcome` facets. | Declaration schema and invocation mechanism. |
| Concrete evaluators return the exact `Eval` algebra with stable evidence/reason identities and declared dependencies. | Evidence schema encoding, storage/reference transport, invocation protocol. |
| Capability declarations state sound fragment, exact dependencies, trust basis, and whether they are concrete-only, partial-symbolic, or complete for a declared fragment. | Capability discovery/negotiation and declaration format. |
| Witnesses, proofs, models, counterexamples, entailment, and equivalence claims are admitted only under §5.3 and bind exact semantics. | Certificate encodings, validators, proof-system identifiers, trust roots. |
| Evaluator failures return evaluation errors; reasoning-service failures return reasoning errors; neither returns a logical conclusion. | Error taxonomies, retry metadata, transport mapping. |
| Completeness is relative to an exact profile and dimension set; intent completeness is unavailable. | Profile declaration and coverage-evidence formats. |
| A joint claim needs a capability whose dependency scope covers the whole cross-plugin formula; local results do not compose into joint results. | Proof exchange, orchestrating joint services, and cross-plugin trust plumbing. |
| Authority attestations have the fixed adoption meaning in §1.1 and provenance survives composition. | Authentication/attestation encoding and verification transport. |

K2 may also choose serialization, discovery, registration, and certificate
formats. It may not alter any connective, normative role, closure rule,
provenance/adoption rule, exact-version rule, metadata aggregation rule, or
error boundary above. Concrete coding symbols remain a K3 question.

## 9. K1 acceptance checklist

- [x] The document has exactly the nine required top-level sections in order.
- [x] All notation and abstract domains are local and serialization-independent.
- [x] Contract denotation exposes hard, authorization, choice/open, provenance/
  authority, and exact-version facets, including for open Contracts.
- [x] Formation, typing, scope, binding, closure, and evaluability are exact and
  remain independent judgment families.
- [x] Every inherited candidate and every introduced semantic role has one
  ledger disposition; retained constructs have controlled counterexamples and
  derived constructs have full-facet proofs.
- [x] T1--T4 and A1--A2 are total, deterministic, error-preserving, and
  evaluation-order independent; decisive truth never drops child metadata.
- [x] Requirement, conditional permission, and conditional obligation have
  distinct denotations; permission never creates an occurrence obligation.
- [x] Choice, factual unknown, provenance, authority, and exact version binding
  remain explicit and are never inferred from content or evaluator availability.
- [x] Core and admitted reasoning rules are sound and capability-relative;
  local plugin conclusions are not promoted to joint conclusions.
- [x] Normalization is limited to proved full-facet-preserving operations.
- [x] All 19 K0 challenges and all 10 separating pairs are covered, with W1--W11
  supplying the required derivations/countermodels.
- [x] Soft preference is reported outside scope; no coding-specific branch,
  task taxonomy, expected mapping, or universal-completeness claim is present.
- [x] K2 obligations are precise while transport, ABI representation, discovery,
  proof encoding, and concrete symbols remain interface questions only.
- [x] No serialization, plugin ABI, coding symbol catalog, executable checker,
  compiler, prompt, planner/action graph, execution semantics, implementation,
  K2 handoff, benchmark, downstream authority, or external artifact is created.
- [x] Only opaque receipt `K1-HO-GATE-20260828-A` was received; no held-out
  content, annotation, path, reference, history, filesystem location, log,
  other-agent source, or indirect store was accessed, located, inferred, or
  reproduced.
- [x] No K1 stop/revise condition was encountered.

Truth/error index: T1 (§4.2), T2 (§4.3), T3 (§4.4), T4 (§4.5).
Aggregation index: A1 (§4.6), A2 (§4.7).
Worked derivation/countermodel index: W1--W11 (§7.3), SP-01--SP-10 (§7.2),
derived-form proof matrix (§7.4), and controlled primitive cases CP-O, CP-V,
SP-03, SP-02, CP-E, CP-N, CP-C, SP-01, SP-05, SP-04, CP-P, CP-U, SP-06,
CP-R, CP-UR, and CP-RE (§6).
