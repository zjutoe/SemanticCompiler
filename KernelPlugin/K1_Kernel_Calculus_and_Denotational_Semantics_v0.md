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

Value, Type, Variable, Principal, ChoiceId, SourceRef, AuthorityRef,
EvidenceRef, UnknownReason, EvaluationErrorReason, ReasoningErrorReason

PluginKey = (plugin_identity, exact_version)
EventKey = (PluginKey, event_namespace, local_name)
EventValue = (event_key : EventKey, payload : Value)
Event = (event_value : EventValue, actor : Principal?)
EventClass = CONTROLLED | OBSERVATIONAL
Facet = pre | trace | final | evidence
SymbolKey = (PluginKey, namespace, local_name, kind)
ProfileKey = (plugin_identity, exact_version, profile_name)
```

`Outcome` is the derived Cartesian product of the four separately retained
facet domains. `PRE`, `TRACE`, `FINAL`, and `EVIDENCE` are its projections, not
commands or mutable stores. Product equality is componentwise, so the product
adds no observation beyond those projections. An event is controlled exactly
when its immutable `Delta` declaration says `CONTROLLED`; its occurrence is
then subject to the authorization facet. The calculus neither selects nor
performs events.

A declaration context exists independently of semantic or service availability:

```text
Delta = (type_declarations,
         literal_declarations_and_admission,
         symbol_signatures,
         symbol_facet_declarations,
         event_declarations,
         event_scope_pair_declarations)

Sigma = (Delta, literal_meanings, function_meanings, predicate_meanings,
         exact_semantic_bindings, evaluator_capabilities,
         reasoning_capabilities, profiles, authority_facts)
rho   : Variable partial-map Value
```

`Delta` declares types, literal admissibility and types, exact function or
predicate signatures, the outcome facets each symbol may consume, an
immutable exact map `EventKey -> (payload_type, EventClass)`, and the exact
companion declarations defined in section 1.2. `Delta |- v:T` denotes the
abstract value-admission/type relation supplied by its type declarations; it
does not require a semantic evaluator. `Delta` says nothing about whether a
semantic meaning, evaluator, or reasoner is installed. Neither an outcome nor
a plugin result supplies event classification. `Sigma` binds meanings and
services to those exact declarations. There is no caller-supplied choice map;
section 2.3 derives the only choice environment from the Contract's validated
choice records.

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

For each exactly declared and semantically bound key, `Sigma` may provide:

```text
TermResult       = TERM_VALUE(Value)
                 | TERM_ERROR(nonempty finset(EvaluationErrorReason))
literal meaning : declared literal -> TERM_VALUE(Value)
function meaning: Value* -> TermResult
predicate meaning: Value* -> Eval
```

Every outcome component observable by a predicate must be supplied explicitly
through an anchor-derived argument, and its declared facet dependencies must
match those arguments. Every type, literal, function, and predicate meaning
is typed and belongs to one exact `PluginKey`. Literal and function meanings
return only values or term-evaluation failures; `UNKNOWN` is not a term result.
A predicate result obeys the kernel `Eval` algebra in section 4; plugins cannot
redefine connectives, truth, errors, evidence aggregation, authority,
provenance, or binding.
Capabilities and profiles are also semantic parameters, but their results are
admitted only by section 5. A meaning can be bound while no evaluator exists.

For a controlled-event conditional requirement, `Delta` may declare an exact
semantic companion pair

```text
EventScopePair(q_scope, q_occurred, controlled_keys)
Delta(q_scope)    = (EventValue) -> Bool
Delta(q_occurred) = (Trace) -> Bool, with trace facet declared
```

Every member of the nonempty `controlled_keys` set must have a `CONTROLLED`
event declaration, and `q_scope` must return `VALUE(FALSE,{},{})` for any
`EventValue` whose key is outside that set. Within it, the predicate may inspect
the declared payload and return any valid `Eval`.

`Sigma` must satisfy this frozen coherence obligation for every admitted
trace `T`:

```text
eval(Atom(q_occurred, Anchor(trace)), rho, O with O.TRACE=T)
  = ANY_RESULT({
      eval(Atom(q_scope, Var(x:EventValue)), rho[x:=e.event_value], O)
      | e occurs in T
    })
```

The right side uses T3/A1 exactly: an empty trace returns
`VALUE(FALSE,{},{})`; evidence, unknown reasons, and errors from every event
scope result are set-unioned; any error dominates; otherwise `TRUE` is
decisive while collected unknown metadata is retained. `q_scope` and
`q_occurred` are distinct exact plugin predicates. This is a declaration-level
semantic coherence requirement, not a kernel quantifier or a formula passed as
a term. Any Contract using the pair includes both exact `SymbolKey`s and the
pair declaration in `Dependencies`. A missing declaration is malformed; a
missing compatible meaning is open; a meaning that violates the declared
equality is incompatible.

### 1.3 Contract denotation and independently inspectable facets

For a well-formed Contract `C`, `D_Sigma(C)` is the record

```text
Hard(C)       : finite set of authority-adopted requirement formulas
Grants(C)     : finite set of authority-adopted authorization grants
Choices(C)    : finite map ChoiceId -> (Type, finite nonempty alternatives,
                                        controller, ChoiceBinding?)
Origins(C)    : finite set of (clause_id, SourceRef, Clause,
                               optional (AuthorityRef, adopter))
Dependencies(C): finite set of exact PluginKey, SymbolKey, ProfileKey, and
                 EventScopePair declaration requirements
Open(C)       : finite set of unresolved variables, choices, AuthorityRefs,
                symbols, versions, profiles, and required semantic contracts
```

All facets exist for open Contracts. `Hard` and `Grants` preserve formulas but
are not evaluated while `Open(C)` is nonempty. Composition is compatible set
union (section 3.8), so no facet is overwritten. A well-formed open Contract
has neither a truth result nor a consistency, relation, profile-success, or
acceptance result. It remains `OPEN_BINDINGS` rather than acquiring factual
`UNKNOWN`.

A `SourceRef` is a self-contained provenance value established by the
source-to-Contract binding analysis before it appears in an `Attribute` or
`ChoiceBinding`. It is preserved verbatim in `Origins` and does not require a
second lookup for Contract closure. This provenance fact grants no normative
authority; only a separately resolved `AuthorityRef` and matching
`authority_fact` can do that. If source-to-Contract analysis cannot identify a
source, representation is `UNRESOLVED(reason)` before a `SourceRef`-bearing
Contract is formed; it is not encoded as an open source lookup.

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
                  exact symbol/profile/EventScopePair requirements
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
signatures, literal admissions, and facet declarations, while `Gamma` contains
lexically bound event variables plus declared choice variables. These judgments
do not consult semantic meanings or evaluator/reasoner capabilities.

```text
(LIT)    Delta admits the exact PluginKey literal at declared type T
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

Facet support is structural: literals and variables have empty direct support,
`support(Anchor(a))={a}`, and application support is the union of its argument
supports. Each `(APP)` or `(ATOM)` premise additionally requires every
argument's support to be allowed by that exact declaration's corresponding
facet position. The formula's actual facet dependency is the recursive union;
no meaning receives an undeclared or implicit outcome component.

Outcome admission is also declaration-relative:

```text
(EVENT) Delta.event_declarations(k)=(T,class)   Delta |- payload:T
        ----------------------------------------------------------
        Delta |- Event(EventValue(k,payload),actor?) : Event

(OUTCOME) every event in TRACE is admitted by (EVENT)
          ------------------------------------------------
          Delta |- (PRE,TRACE,FINAL,EVIDENCE) : Outcome
```

An undeclared event key or ill-typed payload is not an admitted `Outcome`.
Supplying such a purported outcome to concrete evaluation returns
`EVALUATION_ERROR(invalid outcome event declaration or payload)` and no truth
or other judgment. The event's `EventClass` comes only from `Delta`.

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

`WELL_FORMED` means all inductive rules, uniqueness rules, declaration-level
literal admissions, signatures/facet declarations, choice constraints, and
authority-attestation checks pass. A referenced literal or symbol key absent
from `Delta`, or an incompatible declaration for that exact key, is
`MALFORMED(missing or incompatible declaration)` because no typing derivation
exists. By contrast, a valid exact declaration with no matching semantic
meaning in `Sigma` is well formed but open. A purported semantic binding whose
identity, signature, literal type, or facet contract disagrees with `Delta` is
also `MALFORMED(incompatible semantic binding)`.

`CLOSED` means every free variable is bound, every choice is bound by its
controller, every `AuthorityRef` resolves and validates, every exact
`SymbolKey` and `PluginKey` dependency has a matching semantic contract in
`Sigma`, every required `EventScopePair` has compatible meanings satisfying its
coherence obligation, and every required `ProfileKey` has its exact bound profile. Otherwise
the result is `OPEN_BINDINGS(the exact finite missing set)`. `SourceRef` values
in `Origins` are already-bound provenance and add no closure lookup. No
compatible-looking symbol, plugin version, or profile is substituted. Lexical
event variables are bound by `Authorize` and do not make a Contract open.

For a well-formed Contract, define its choice environment mechanically:

```text
chi_C(choice_id) = binding.value
```

exactly when the unique `ChoiceDecl` has a `ChoiceBinding` whose value is in
the declared alternatives, whose binder equals the declared controller, and
whose exact source/authority fact validates `BIND_CHOICE(choice_id)`. No other
entry exists. Thus `C` is closed only if every referenced choice has an entry
in `chi_C`; no caller, evaluator, witness, or executor may override it.

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

For a closed Contract, `[[t]]^term_{Sigma,rho,chi_C,O}` returns `TermResult`
recursively. Literals use their exact declared and bound meaning. A lexical
event variable uses `rho`; a choice variable uses only `chi_C`; their namespaces
are disjoint. Anchors return `TERM_VALUE` of the named projection.

For `Apply(q,t1,...,tn)`, evaluate every argument denotationally. If one or more
arguments return `TERM_ERROR`, return one `TERM_ERROR` containing the set union
of all argument error reasons and do not invoke `q`. Otherwise invoke the exact
bound function on the positional values and preserve its `TermResult`. This
recursive rule is deterministic and traversal-order independent: argument
positions determine values while error sets use semantic set union. An absent
meaning is not evaluated because it already produced `OPEN_BINDINGS`.

An atom evaluates every term argument by that same rule. Any term errors are
unioned and projected to `ERROR(errors, evidence={}, unknowns={})`; the
predicate is not invoked. Otherwise the atom invokes only its exact bound
predicate meaning with the positional values; anchor-derived arguments are its
only access to outcome facets. Term failure is therefore an
`EVALUATION_ERROR`, never factual `UNKNOWN`, and cannot be hidden by argument
order. This gives
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

For an adopted grant `g = Authorize(p,x,scope,guard)` and an admitted trace
event `e` whose exact `Delta` declaration has class `CONTROLLED` and whose
`e.actor=p`, define

```text
GrantEval(g,e,O) = eval(All({scope, guard}), rho[x := e.event_value], O)
```

`AuthEval` selects exactly the trace events whose `EventKey` is classified
`CONTROLLED` by `Delta`; an outcome cannot override that selection. For each,
collect all grants naming its actor. A controlled event with no actor has no
matching grants. Its authorization result is `ANY_RESULT` over the collected
`GrantEval` results; the empty set is `FALSE`. `AuthEval` is `ALL_RESULT` over
all controlled-event results; a trace with no controlled events is `TRUE`.
Thus an occurrence with no true grant is unauthorized and makes compliance
`FALSE` (unless an evaluation error prevents a truth result); an unknown grant
leaves it unknown if no grant is true. A grant never requires an event: when no
controlled event occurs, compliance is vacuously true.

`scope` identifies which event a grant concerns; `guard` states the condition
under which it is granted. Both are formulas so their unknown, evidence, and
error behavior is fixed by section 4. Evaluability supplies facts but cannot
create a grant. This is a declarative condition over a completed trace, not an
execution policy.

### 3.4 Conditionality, alternatives, states, and choices

A conditional requirement for a controlled event uses one exact declared
`EventScopePair(q_scope,q_occurred,controlled_keys)` and the well-typed composition

```text
Scope(x)              = Atom(q_scope, Var(x:EventValue))
OccurredScope(TRACE)  = Atom(q_occurred, Anchor(trace))

Require(Implies(condition, OccurredScope(TRACE)))
Authorize(p, x, Scope(x), condition)
```

The first clause imposes the obligation; the second supplies exactly the
authority required by closed-world authorization if the event occurs. A
conditional permission contains only the second clause. Consequently condition
true plus occurrence can satisfy both forms, condition true plus omission
separates them, and condition false plus omission satisfies both. Condition
false plus occurrence is unauthorized in both. For a consequence that is not
a controlled event, the conditional requirement needs only the `Require`.
The companion equality in §1.2 guarantees that the hard occurrence predicate
and authorization scope denote the same event set with identical aggregate
truth, evidence, unknown-reason, and error behavior.

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
identical formula content, but only a matching authority attestation adopts an
attributed clause into `Hard` or `Grants`. `Origins(C)` remains independently
inspectable even when two adopted formulas are propositionally equivalent.
Exact symbol/version
dependencies participate in term and atom meanings. Exact required
`ProfileKey`s participate in profile judgments. Plugin, symbol, and profile
dependencies all participate in full semantic equivalence; same display name
or a newer version is insufficient.

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

The proof for each macro is definitional expansion. For every `Delta`, `Sigma`,
mechanically derived `chi_C`, lexical environment, and `O`, the expanded
term/formula is internally `==Eval` to the macro's stated meaning; hence truth,
error, evidence sets, and unknown-reason sets are identical, not merely
two-valued acceptance. Copying `o` preserves provenance and authority; copying
the exact symbol/profile references preserves dependencies; identical free variables
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

At every function node, all nested argument `TermResult`s are collected; any
`TERM_ERROR` reasons are set-unioned, prevent that function invocation, and
remain a `TERM_ERROR`. At the atom boundary, all argument term-error sets are
unioned and projected once to `ERROR(errors,{}, {})`, preventing predicate
invocation. If invocation occurs, its returned `Eval` sets are preserved
exactly. A plugin may cite multiple evidence items or unknown causes but cannot
prioritize one by return order. Repeated equal references/reasons collapse by
semantic set equality. Neither a term error nor its projection can become
`UNKNOWN`.

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
| Profile completeness/failure | Coverage of every dimension in one required exact `ProfileKey`; completed incomplete/inconclusive results stay distinct, while evaluator or reasoning failure yields no profile judgment. | Versioned profile parameter plus kernel failure boundary |
| Entailment/equivalence | A named relation from §5.2 with a sound proof or relation-specific definite counterexample; otherwise `RELATION_UNKNOWN`. | Kernel plus admitted capabilities |
| Reasoning failure | Protocol/service failure gives `REASONING_ERROR` and no relation, consistency, or profile result. | Kernel failure boundary |

Intent completeness cannot be certified from a Contract. Profile completeness,
truth, and satisfiability imply none of one another except through an explicitly
proved rule.

### 5.2 Satisfaction and core reasoning

A satisfying witness is `(C,O,evidence)` where `C` is closed, its sole choice
environment is the mechanically derived `chi_C`, exact plugin meanings are
used, supplied evidence validates, and `AcceptEval(C,O)` is
`VALUE(TRUE,...)`. Neither the witness nor its validator supplies or overrides
choice values. The witness may be abstract; it need not be a patch or executor
output. If concrete witness validation returns an evaluator error, the result is
`EVALUATION_ERROR` and neither `CONSISTENCY_SAT` nor `CONSISTENCY_UNSAT` is
produced.

Core rules are:

```text
All({f, Not(f)}) is UNSAT                              (K-CONTRA)
VALUE(TRUE,...) for accepted witness w => SAT(w)      (K-WITNESS)
six-facet equality(C1,C2) => FULL_CONTRACT_EQUIVALENCE (K-EQUIV)

eval(f,O)=VALUE(TRUE,...) and eval(g,O)=VALUE(FALSE,...)
    => disprove FORMULA_ENTAILMENT(f,g)                (K-FORM-COUNTER)

eval(f,O)=VALUE(vf,...) and eval(g,O)=VALUE(vg,...),
vf,vg in {TRUE,FALSE}, vf != vg
    => disprove FORMULA_EQUIVALENCE(f,g)               (K-FORM-EQ-COUNTER)

AcceptEval(C1,O)=VALUE(TRUE,...) and
AcceptEval(C2,O)=VALUE(FALSE,...)
    => disprove ACCEPTANCE_ENTAILMENT(C1,C2)           (K-ACC-COUNTER)

AcceptEval(C1,O)=VALUE(v1,...) and AcceptEval(C2,O)=VALUE(v2,...),
v1,v2 in {TRUE,FALSE}, v1 != v2
    => disprove ACCEPTANCE_EQUIVALENCE(C1,C2)          (K-ACC-EQ-COUNTER)

a definite unequal structural facet, or unequal non-error VALUE outputs in
the Hard or Grants exact result functions
    => disprove FULL_CONTRACT_EQUIVALENCE(C1,C2)       (K-FACET-COUNTER)
```

`K-CONTRA` is sound because T1/T2 have no truth assignment making both operands
true. It is a denotational core derivation, never a conclusion inferred from an
observed evaluator error. An evaluator failure alone proves neither `UNSAT` nor
any relation. `K-WITNESS` is sound by the definition of acceptance.

First define the internal, non-status relation `f ==Eval g`: under the same
exact `Delta`, `Sigma`, `chi_C`, and lexical scope, the complete `Eval` results
are equal for every admitted outcome, including truth, evidence,
unknown-reason, and evaluation-error sets and exact free dependencies. It is
used to prove derived-form preservation and full Contract equivalence; it is
not itself `RELATION_PROVED`. A symbolic derivation may establish `==Eval`
across every result branch. In a concrete comparison, an encountered `ERROR`
returns `EVALUATION_ERROR`, not equality or inequality. Otherwise two unequal
`VALUE` results are a definite internal inequality, including differing
`UNKNOWN` reasons or metadata; that compares result records and does not treat
`UNKNOWN` as `FALSE`.

The public logical relations use definite truth/refutation semantics over
partial `Eval` results. They are not total Boolean comparisons of result
records: a proof establishes the absence of the named decisive countermodel,
a decisive countermodel disproves the relation, and a needed `UNKNOWN` proves
neither. This makes the proof condition and falsification condition exact
duals without treating factual uncertainty as false. Exact result-record
equality remains the separate internal `==Eval` relation above.

The public logical-relation protocol is:

| Relation request | Proof condition | Definite countermodel | Otherwise |
|---|---|---|---|
| `FORMULA_ENTAILMENT(f,g)` | A sound proof establishes that no admitted valuation/outcome has `f=TRUE` and `g=FALSE`. | One admitted outcome with `f=TRUE`, `g=FALSE`. | A needed `UNKNOWN` gives `RELATION_UNKNOWN(ENTAILMENT,reason)`. |
| `FORMULA_EQUIVALENCE(f,g)` | A sound proof establishes that no admitted valuation/outcome gives the formulas opposite determinate `TRUE`/`FALSE` values; `f ==Eval g` is stronger sufficient evidence. | One admitted outcome with opposite determinate `TRUE`/`FALSE` values. | A needed `UNKNOWN` gives `RELATION_UNKNOWN(EQUIVALENCE,reason)`. |
| `ACCEPTANCE_ENTAILMENT(C1,C2)` | A sound proof establishes that no admitted outcome has C1 acceptance `TRUE` and C2 acceptance `FALSE`. | One admitted outcome with C1 acceptance `TRUE`, C2 acceptance `FALSE`. | A needed `UNKNOWN` gives `RELATION_UNKNOWN(ENTAILMENT,reason)`. |
| `ACCEPTANCE_EQUIVALENCE(C1,C2)` | A sound proof establishes that no admitted outcome gives the Contracts opposite determinate `TRUE`/`FALSE` acceptance; exact equality of both `AcceptEval` functions is stronger sufficient evidence. | One admitted outcome with opposite determinate `TRUE`/`FALSE` acceptance. | A needed `UNKNOWN` gives `RELATION_UNKNOWN(EQUIVALENCE,reason)`. |

`FULL_CONTRACT_EQUIVALENCE(C1,C2)` is the separate exact denotational relation
used by `K-EQUIV`: equality of all six facets—`Hard` under `==Eval`,
`Grants`/authorization exact result functions, `Choices` including validated
bindings, `Origins`/authority attachments, exact `Dependencies` including
`ProfileKey`s and `EventScopePair`s, and `Open` bindings. A definite structural
inequality disproves it. So does an unequal pair of non-error `VALUE` outputs
from corresponding Hard or Grants functions, including unequal
`UNKNOWN`/metadata records, without treating unknown as false. An encountered
concrete `ERROR` instead yields `EVALUATION_ERROR` and no full-equivalence
result.

For every logical relation, `UNKNOWN` is never itself a countermodel. If
concrete evaluation returns `ERROR`, the request returns `EVALUATION_ERROR` and
no relation judgment. A symbolic/reasoning service failure returns
`REASONING_ERROR` and no relation judgment. A relation result is never silently
converted to another taxonomy member.

The public K0 status remains namespaced exactly: the two entailment relations
render `RELATION_PROVED(ENTAILMENT,proof_ref)`,
`RELATION_DISPROVED(ENTAILMENT,counterexample_ref)`, or
`RELATION_UNKNOWN(ENTAILMENT,reason)`; the three equivalence relations render
the corresponding statuses with `EQUIVALENCE`. The request and referenced
evidence record the taxonomy member. No new status family is introduced.

### 5.3 Capability-relative proof admission

A plugin witness, proof, model, counterexample, entailment, or equivalence
claim is admitted only if it identifies exact semantics and dependencies, lies
inside the capability's declared sound fragment, has a valid trust attestation,
names one exact §5.2 relation when applicable, and its conclusion is the
judgment requested. A logical countermodel must meet its decisive TRUE/FALSE
rule; `UNKNOWN` is inadmissible there. For full exact Contract equivalence, an
unequal non-error `VALUE`, including an unequal `UNKNOWN`/metadata record, is a
denotational counterexample without being a logical falsehood. An evaluator
error is inadmissible for every relation. `COMPLETE_FOR_DECLARED_FRAGMENT`
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

Only a required `ProfileKey P` present in `Dependencies(C)` and exactly bound
under closure may be checked; an absent binding remains `OPEN_BINDINGS` and
produces no profile judgment. An unavailable requested checker is
`EVALUABILITY_MISSING` and is not a failed check. For such `P` with an available
checker, `PROFILE_COMPLETE(P,E)` requires evidence `E` covering
every versioned dimension declared by `P`. A known omitted dimension produces
`PROFILE_INCOMPLETE`. A completed check that cannot decide coverage produces
`PROFILE_UNKNOWN(P,reason)`. Failure of a concrete profile evaluator or its
invocation/protocol produces `EVALUATION_ERROR(reason)` and no profile
judgment. Failure of a symbolic profile reasoner or its reasoning protocol
produces `REASONING_ERROR(reason)` and no profile judgment. No error is recast
as `PROFILE_UNKNOWN`, incomplete, or complete. None of these profile outcomes
changes acceptance or satisfiability or certifies unstated intent.
Contracts differing only in a required `ProfileKey` therefore differ in
`Dependencies`, are not fully Contract-equivalent, and may receive different
profile judgments even when their hard acceptance functions agree.

### 5.5 Normalization policy

The only kernel normalizations are alpha-renaming of the bound authorization
event variable, the definitional expansion of `TrueF`, `FalseF`, `Any`,
`Implies`, `GOAL`, `PRESERVE`, `FORBID`, and `ALLOW`, and mathematical canonicalization of finite
sets. Alpha-renaming preserves environments by capture-free bijection.
Definitional expansions preserve every facet by sections 3.6 and 4; finite-set
canonicalization preserves set membership and union metadata. No distribution,
atom rewriting, provenance erasure, version substitution, or proposition-only
deduplication is authorized. There is no promised additional normal form.

These rules are sound only under the stated semantics and admitted capability
assumptions. They establish neither universal decidability nor completeness.

## 6. Minimality and derived-form ledger

The controlled examples below keep `Delta`, `Sigma`, mechanically derived
`chi_C`, origins, and all unrelated clauses fixed except for the named
variation. `CP-a/b` means the two cases differ only in that feature. This
supports relative minimality for the accepted cases, not absolute minimality
over all possible calculi.

| Construct or role | Disposition | Denotation/derivation | Controlled pair or proof; why simpler composition fails | K0 |
|---|---|---|---|---|
| Completed `Outcome` tuple | DERIVED | Delta-admitted Cartesian product `PRE x TRACE x FINAL x EVIDENCE`, §1.1/§2.2 | Componentwise product and projection laws preserve every observation; trace admission/classification comes from Delta, not a fifth product field | C01,C19 |
| Declaration context `Delta` | RETAINED_PRIMITIVE | §1.1, §2.2--2.3 | CP-D: hold a symbol reference and unavailable service fixed; absent declaration is malformed, exact declaration without meaning is open, and exact meaning without evaluator is closed but not evaluable. Collapsing declaration with service state loses these judgments | C13,C15,C16 |
| Exact event declaration/classification | RETAINED_PRIMITIVE | §1.1, §2.2, §3.3 | CP-CTL: hold one admitted event key/payload/actor, Contract, and empty grant set fixed while changing only its immutable Delta class between `OBSERVATIONAL` and `CONTROLLED`; the first is outside AuthEval and the second is unauthorized. A witness-supplied flag cannot preserve this trusted distinction | C03,C04,C06 |
| Plugin-typed literals | PLUGIN_PARAMETER | §1.2, §3.1 | Exact type/value meaning is domain-specific; the kernel only preserves its key | C11 |
| Typed variables and binding | RETAINED_PRIMITIVE | §2.1--2.3 | CP-V: two otherwise identical admitted controlled trace events differ only in `EventValue` key/payload; the grant scope applied to the actually bound current-event `x` is true for one and false for the other. Without that binder the grant cannot distinguish them | C04,C06 |
| `PRE` anchor | RETAINED_PRIMITIVE | `O.PRE` | CP-PRE: hold formula, `FINAL`, admitted `TRACE`, and `EVIDENCE` fixed; vary only `PRE` so a pre/final relation changes truth. A final-only term cannot observe it | C02,C18,C19 |
| `TRACE` anchor | RETAINED_PRIMITIVE | `O.TRACE` | SP-02 uses identical final states and differing transient traces | C03,C04,C06 |
| `FINAL` anchor | RETAINED_PRIMITIVE | `O.FINAL` | CP-F: hold `PRE`, admitted `TRACE`, `EVIDENCE`, declarations, and formula fixed; change only `FINAL` so a final-state atom changes truth. No other anchor observes that difference | C01,C07 |
| `EVIDENCE` anchor | RETAINED_PRIMITIVE | `O.EVIDENCE` | CP-E: identical states/trace, suite evidence present versus absent yields true versus unknown | C09,C15 |
| Plugin functions | PLUGIN_PARAMETER | exact typed function meaning §1.2 | State projections and domain computations are not core logic | C02,C11 |
| Plugin predicates/atoms | PLUGIN_PARAMETER | exact typed predicate `Eval` §1.2 | Atomic domain meaning cannot be composed from domain-independent connectives | all semantic cases |
| Event-scope/trace-occurrence companion semantics | PLUGIN_PARAMETER | exact `EventScopePair` coherence §1.2 | The pair supplies domain event matching while T3/A1 fixes aggregation; independent unlinked atoms could disagree on empty traces, truth, evidence, unknowns, or errors | C04,C05,C06 |
| Negation `Not` | RETAINED_PRIMITIVE | T1 | CP-N: with a fixed positive occurrence atom, require occurrence versus require non-occurrence; positive atoms/`All` alone cannot complement its accepted set | C03,C10 |
| Finite conjunction `All` | RETAINED_PRIMITIVE | T2 | CP-C: outcomes satisfy only `a`, only `b`, or both; requiring both cannot be represented by either atom or negation alone | C10,C14 |
| Alternatives `Any` | DERIVED | `Not(All(Not children))` | T1--T3 prove identical truth/error/evidence/unknown results and bindings | C07 |
| Conditionality `Implies` | DERIVED | `Any({Not(a),b})` | T4 is the full result-level derivation; no new normative role is needed | C05,C09 |
| `TrueF` | DERIVED | `All({})` | T2 gives exactly `VALUE(TRUE,{},{})`; there are no children, errors, evidence, unknown reasons, free bindings, dependencies, grants, or origins to lose | C05,C07 |
| `FalseF` | DERIVED | `Not(TrueF)` | T1 applied to the complete `TrueF` result gives exactly `VALUE(FALSE,{},{})`; all nontruth facets remain empty | C07 |
| General quantification | EXCLUDED | delegated inside atom | No K0 pair forces kernel enumeration; adding it would require unresolved domain/evaluation semantics | C11,C12 |
| Hard `Require` role | RETAINED_PRIMITIVE | §3.2 | SP-01: with condition true and event absent, requirement fails while permission succeeds | C01,C05 |
| `Authorize` role with principal/event scope/guard | RETAINED_PRIMITIVE | §3.3 | CP-A: with one identical admitted controlled event, actor, requirements, and environment, a matching true grant is present in one Contract and absent in the other; AuthEval/acceptance is true versus false. No `Require` changes | C04,C06 |
| Owned choice plus controller | RETAINED_PRIMITIVE | §1.3, §3.4 | SP-05 distinguishes owned choice from factual unknown. CP-CTRL holds choice ID/type/alternatives/unbound state fixed and changes only controller `p` versus `q`; only the named controller can furnish a valid binding | C08 |
| Provenance attachment | RETAINED_PRIMITIVE | `Origins(C)` §1.3, §3.5 | CP-PR: identical unadopted attributed formulas with no normative adoption differ only in self-contained `SourceRef`; all normative/evaluation facets agree while `Origins` differ | C17 |
| Authority attestation/adoption | RETAINED_PRIMITIVE | §1.1, §2.2 | SP-04 holds content/source record fixed but varies valid adoption authority; only one contributes a clause | C17 |
| Exact plugin/symbol/profile/pair dependency | RETAINED_PRIMITIVE | `Dependencies(C)` §1.3, §3.5 | CP-P: same display name with incompatible v1/v2 meaning changes closure/truth. CP-PROFILE: Contracts differ only in required `ProfileKey`; Dependencies/full equivalence and possible profile judgment differ. Pair use likewise binds both keys and coherence declaration | C04,C05,C13,C15,C16,C19 |
| Contract composition | DERIVED | compatible facet-wise set union §3.8 | Union preserves all facets; a new connective would add no distinction | C14 |
| `GOAL` | DERIVED | §3.6 | Definitional full-facet proof §3.6 | C01 |
| `PRESERVE` | DERIVED | §3.6 | Definitional full-facet proof §3.6 | C02,C18,C19 |
| `FORBID` | DERIVED | §3.6 | Definitional full-facet proof; not confused with absent authority | C03 |
| `ALLOW` | DERIVED | §3.6 | Definitional full-facet proof; empty trace proves no obligation | C04 |
| Three truth values | RETAINED_PRIMITIVE | §4.1--4.5 | CP-U: same closed condition before versus after decisive evidence; collapsing unknown with true or false changes release acceptance | C09 |
| `TermResult` value/error algebra | RETAINED_PRIMITIVE | §1.2, §3.1, A2 | CP-TE: hold the outer atom fixed; a nested function failure projects to evaluation error/no truth, while a valid term followed by an evidence-pending predicate returns truth unknown. Boolean truth cannot type or compose the term failure | C09,C15 |
| Evaluation error boundary | RETAINED_PRIMITIVE | §4.1 | SP-06 fixes request and varies missing evidence versus evaluator crash; one returns truth unknown, the other no truth | C09 |
| Evidence-reference set | RETAINED_PRIMITIVE | §1.1, A1/A2 | CP-R: same truth with independent signed versus unsigned observations; erasure loses admissible support | C01,C15 |
| Unknown-reason set | RETAINED_PRIMITIVE | §1.1, A1/A2 | CP-UR: same unknown truth with missing suite result versus inaccessible manifest; reason determines what remains unresolved | C09,C12 |
| Reasoning-error boundary | RETAINED_PRIMITIVE | §5.3 | CP-RE: same query with completed inconclusive service versus crashed service; only the first yields relation/consistency unknown | C12,C14 |
| Capability declarations/proof assumptions | PLUGIN_PARAMETER | §5.3 | Domain proof soundness/fragment is not core-denotable; kernel only gates admission | C11,C12,C14 |
| Versioned completeness profile | PLUGIN_PARAMETER | §5.4 | Required dimensions are domain-specific; kernel fixes only relative status laws | C19 |
| Authorization compliance | DERIVED | nested `Any` grants and `All` events §3.3 | T2/T3 give full truth/error/evidence/unknown behavior | C03,C04,C06 |
| Soft preference ordering | EXCLUDED | outside accepted scope §3.7 | SP-08 requires ranking, which hard truth cannot preserve | SP-08 |
| Coding task/operation taxonomy | EXCLUDED | no denotation | No K0 distinction requires it; would be a domain-specific core branch | all |

Ledger counts: **21 `RETAINED_PRIMITIVE`; 11 `DERIVED`; 6
`PLUGIN_PARAMETER`; 3 `EXCLUDED`** (41 rows).

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
| K0-C04 | `Authorize(p,x,Scope_regen(x),A_metadata_changed(PRE,FINAL))` | `Scope_regen:(EventValue)->Bool`; regeneration key is immutably controlled in `Delta` | representable; evaluator available | conditional permission | unknown guard leaves an occurring matching controlled event authorization unknown | no obligation, trace-typed scope, or witness-controlled flag |
| K0-C05 | C04's grant plus `Require(Implies(A_metadata_changed(PRE,FINAL),OccurredScope_regen(TRACE)))` | exact `EventScopePair(Scope_regen,OccurredScope_regen,keys)` satisfying §1.2 coherence | representable; evaluator available | controlled conditional obligation plus necessary authority | hard implication follows T4; occurrence aggregate and grant preserve exact metadata/error rules | no untyped formula-as-term, unlinked occurrence atom, or permission-only rewrite |
| K0-C06 | `Authorize(p,x,Scope_edit(x),A_schema_changed(PRE,FINAL))` | `Scope_edit:(EventValue)->Bool`; edit key/payload and controlled class declared exactly in `Delta` | representable; evaluator available | permission without duty | scope/guard error -> evaluation error only for a candidate controlled event | no invented edit or caller-selected control class |
| K0-C07 | `Require(Any({A_toml(FINAL),A_yaml(FINAL)}))` | two typed acceptance atoms | representable; evaluator available | acceptable alternatives | both unknown -> unknown | no fixture choice/both requirement |
| K0-C08 | unbound `Choice(storage,T,{local,hosted},user,none)` | meanings for alternatives only | `UNRESOLVED`; `WELL_FORMED`; `OPEN_BINDINGS` | controller-owned discretion | remains open, never truth unknown | no default/executor ownership |
| K0-C09 | `Require(Implies(A_release(FINAL,TRACE),A_suite(EVIDENCE)))` | suite fact/evidence meaning | representable; evaluator available; truth unknown pre-evidence | factual uncertainty | missing evidence -> unknown when release occurs; crash -> error | nobody chooses fact |
| K0-C10 | `Require(All({a,Not(a)}))` | same exact bound atom `a` | representable; well formed; closed; consistency unsat | kernel contradiction | evaluator error yields no concrete truth but K-CONTRA remains sound | not malformed/plugin special case |
| K0-C11 | conjunction of nonempty/bounds atoms | sound numeric-domain proof capability | representable; well formed; closed; evaluator available; unsat | plugin contradiction | proof failure -> consistency unknown; service fault -> reasoning error | no numeric kernel rule |
| K0-C12 | `Require(All({A_preserve,A_reduce}))` | sampled evaluation only; no complete joint reasoner | representable; local evaluator available; consistency unknown | capability-relative uncertainty | no witness/proof -> unknown | no sampled universal SAT |
| K0-C13 | requirement has an exact declaration for the retired key | declaration is valid; exact semantic meaning/service absent while incompatible newer key is separate | representable; well formed; open bindings; evaluability missing | declaration, semantic closure, and capability remain separate | no substitution; discovery uncertainty stays evaluability unknown | no name-based rebind |
| K0-C14 | composed requirements with two exact plugin keys | local reasoners only | representable; local evaluability; joint consistency unknown | cross-plugin composition | absent joint capability -> unknown; failure -> reasoning error | no local-to-joint promotion |
| K0-C15 | `Require(A_rubric(inputs,FINAL,EVIDENCE))` | explicit typed/versioned meaning, dependencies, evidence boundary, evaluator | representable; closed; evaluator available | legitimate broad atom | declared unknown/error only | no gold/ID access |
| K0-C16 | same exact atom/meaning as C15 | semantic binding present, evaluator absent | representable; closed; evaluability missing | denotation vs service | no truth judgment requested | not meaningless/satisfied |
| K0-C17 | same attributed formula under two self-contained `SourceRef` values | source-authentication authority fact | representable; source provenance bound; authority evidence available | source provenance vs normative adoption | unadopted quote is closed provenance; an attempted adoption with unresolved `AuthorityRef` is open | no authority from wording or source existence |
| K0-C18 | both phrasings bind to the same `R_public(PRE,FINAL)` formula but retain separate source origins | one exact declared observation relation | representable; internal `==Eval`, hence `RELATION_PROVED(EQUIVALENCE, formula proof)` and acceptance equivalence | surface-independent proposition with preserved provenance | ambiguous binding -> unresolved; evaluation error -> no relation | no phrase atoms, accepted-set shortcut, or full-facet provenance erasure |
| K0-C19 | preservation/translation requirements plus exact required `ProfileKey` | accepted abstract witness; exact concrete-evidence profile | representable; closed profile binding; consistency sat; profile incomplete | satisfiability vs implementation evidence | known missing dimension -> incomplete; completed inconclusive -> profile unknown; concrete/symbolic service failure -> evaluation/reasoning error and no profile judgment | no patch oracle/inconsistency or profile-error default |

Coverage count: **19** (`C01`--`C19`).

### 7.2 Ten separating-pair derivations

| Pair | Denotational derivation or countermodel |
|---|---|
| SP-01 obligation/permission | Fix one exact coherent pair `(Scope,OccurredScope)`. C04 is grant `G=Authorize(p,x,Scope(x),c)`; C05 is the same `G` plus `Require(Implies(c,OccurredScope(TRACE)))`. With `c=TRUE` and empty trace, both have vacuous authorization compliance but only C05's hard implication is false. With `c=TRUE` and a matching controlled event by actor `p`, coherence makes `OccurredScope` and the grant scope true, so both can accept. With `c=FALSE` and omission, both accept. Obligation alone separates them. |
| SP-02 final/trace | Outcomes share `FINAL` without `.tmp-key`; one trace creates then deletes it, the other never creates it. Final atom is true for both. `Not(occurs(TRACE))` is false only for the first. |
| SP-03 preservation/fixed final | At baseline `PRE1` matching manifest `M`, both intents accept `FINAL=M`. Change only baseline to `PRE2 != M` and final to `PRE2`: preservation is true while fixed-manifest final is false. |
| SP-04 provenance/content | Hold formula content and its self-contained `SourceRef` fixed. Variant A adds a matching authenticated-user adoption and enters `Hard/Grants`; variant B has no adoption and remains attributed content in `Origins`. Authority/adoption alone changes the normative facets. |
| SP-05 choice/unknown fact | Both expose `{local,hosted}`. The declared user may add an authority-validated `ChoiceBinding` for either alternative, from which `chi_C` is derived. The manifest case has no choice declaration; before its fixed value is evidenced, its atom is truth unknown and no principal or witness may bind it. |
| SP-06 unknown/error | Missing suite evidence returns `VALUE(UNKNOWN,E,{missing-suite})`. A crash returns `ERROR({crash},E,U)`. T1--T4 preserve the former truth and the latter absence of truth. |
| SP-07 satisfiability/profile | C19 witness makes `AcceptEval=TRUE`, deriving `CONSISTENCY_SAT`. The exact profile lacks concrete implementation evidence, independently deriving `PROFILE_INCOMPLETE`; neither judgment rewrites the other. |
| SP-08 hard/preference | Hard limit rejects an over-limit outcome. Of two under-limit outcomes both satisfy hard acceptance; the requested ranking distinguishes them, but no kernel denotation does. Preference is therefore explicitly outside scope rather than hardened. |
| SP-09 closure/evaluability | C15 and C16 have identical exact semantic bindings, so both are `CLOSED`. Only C15 has the compatible evaluator capability. Their denotations are meaningful in both cases while evaluability differs. |
| SP-10 local/joint reasoning | Let local reasoners each return a satisfying local model with incompatible shared dependency values. Neither model witnesses the conjunction. Without a declared joint capability, composition is representable but joint consistency is unknown. |

Coverage count: **10** (`SP-01`--`SP-10`).

### 7.3 Required worked derivations and countermodels

**W1 — C04/C05 conditional roles.** Let shared grant
`G=Authorize(p,x,Scope_regen(x),c)`, where `Scope_regen:(EventValue)->Bool`
and `OccurredScope_regen:(Trace)->Bool` are the distinct exact predicates of
one coherent `EventScopePair`. C04 contains only `G`; C05 contains `G` and
`Require(Implies(c,OccurredScope_regen(TRACE)))`. “Present” below means one
admitted matching controlled event whose actor is `p`. The four cases are:

| `c` | occurrence | C04 | C05 |
|---|---|---|---|
| `TRUE` | absent | authorization empty-`All=TRUE` | authorization `TRUE`, implication `FALSE`: rejects |
| `TRUE` | present | scope/guard grant `TRUE`: accepts | same grant `TRUE`, implication `TRUE`: accepts |
| `FALSE` | absent | authorization empty-`All=TRUE` | authorization `TRUE`, implication `TRUE`: accepts |
| `FALSE` | present | grant `FALSE`: rejects | grant `FALSE` despite true implication: rejects |

With empty trace, `OccurredScope_regen(TRACE)` is exactly
`VALUE(FALSE,{},{})` by companion coherence; neither Contract evaluates grant
scope or guard because AuthEval has no candidate controlled event. C05 still
evaluates both operands of its hard implication under A1, so condition metadata
is retained. With a matching admitted controlled event, AuthEval binds `x` to
that event's exact key/payload and evaluates scope plus guard. C05 separately
evaluates the condition and `OccurredScope_regen`; the latter has exactly the
T3/A1 aggregate of `Scope_regen` over trace events. Final `AcceptEval` set-unions
all evidence, unknown-reason, and error sets, deduplicating exact repeated
identities returned by the grant scope, occurrence companion, or repeated
condition. Any collected evaluation error dominates. Origins differ only by
C05's added requirement adoption; event declarations, choice bindings,
semantic keys/pair, condition, and shared grant origin are held fixed.

**W2 — C08/C09 discretion versus fact.** C08 has
`Open={choice_id}` and no `Eval`; a controller-valid binding closes it. C09 is
closed and its evidence atom returns `VALUE(UNKNOWN,{},{missing-suite})`.
For C08, closing means adding the unique controller/source/authority-validated
`ChoiceBinding`; `chi_C(choice_id)` is then mechanically that record's value.
No caller or witness supplies a second map. Changing C09 requires evidence,
not a choice binding. Thus representation, binding, truth, provenance, and
authority facets cannot be exchanged.

**W3 — C10 kernel contradiction.** For any logical value `v`, T1 gives
`not(v)`. T2 applied to `{v,not(v)}` is never true: it is false for `TRUE` and
`FALSE`, unknown for `UNKNOWN`. Hence no satisfying truth assignment exists,
and the denotational K-CONTRA derivation proves `CONSISTENCY_UNSAT` although
both atoms type-check. An observed evaluator `ERROR` would instead produce
`EVALUATION_ERROR` and proves nothing; K-CONTRA does not infer from that error.

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

**W6 — C13 exact version.** `Delta` contains the mandated exact declaration
`q@v1`, so the formula is well formed. `Sigma` has no `q@v1` semantic meaning
or evaluator; an available `q@v2` declaration/meaning is a separate,
incompatible key. Exact lookup therefore leaves `q@v1` in `Open` and its
requested evaluator in the missing-capability set. No formula truth is
evaluated. Display-name equality supplies neither closure nor migration.

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
`authority_facts` validates adoption of an attributed source, so `p` enters
`Hard`; with the same content and same `SourceRef` but no adoption, `p` remains
only in `Origins`. Assign `p=FALSE`: the adopted Contract rejects and the
unadopted Contract accepts absent other requirements. This SP-04 refinement
isolates authority/adoption. Separately, CP-PR compares the authenticated-user
and issue-comment `SourceRef` values while neither is adopted: normative and
evaluation facets agree while `Origins` differ. Combining these two independent
steps represents C17 without making source existence authority or a closure
requirement.

**W10 — C18 surface equivalence.** Binding analysis maps both phrasings to the
same exact relation atom over `(PRE,FINAL)`. A structural derivation proves the
stronger internal `f_A ==Eval f_B`, including every truth, evidence,
unknown-reason, and error branch. That exact denotational proof implies public
logical `RELATION_PROVED(EQUIVALENCE,formula-proof)` without using an observed
`UNKNOWN` as success. With identical remaining acceptance-affecting facets, it
also proves acceptance equivalence. Their distinct `SourceRef` values remain in
`Origins`, so full six-facet Contract equivalence is definitely disproved and
K-EQUIV is inapplicable. A concrete evaluator error would yield only
`EVALUATION_ERROR`; no surface string enters the vocabulary and no provenance
is erased.

**W11 — C19 abstract satisfaction.** An admitted closed-Contract/`Outcome`
witness uses that Contract's mechanically derived `chi_C` and makes the
preservation and translation atoms true with accepted evidence, so K-WITNESS
gives `CONSISTENCY_SAT`. The separately bound profile lacks its
concrete-implementation-evidence dimension and is `PROFILE_INCOMPLETE`. The
witness is not an implementation or construction method. If the profile check
instead completed inconclusively it would be `PROFILE_UNKNOWN`; concrete or
symbolic service failure would yield the corresponding evaluation or reasoning
error and no profile judgment.

### 7.4 Derived-form proof matrix

| Form | Acceptance/truth/error/evidence/unknown | Authorization | Provenance/authority | Binding/version |
|---|---|---|---|---|
| `Outcome` product | Componentwise tuple formation exposes exactly four retained anchor values after Delta trace admission and introduces no `Eval` behavior | no event, grant, or control flag added | none added | immutable event declarations remain external exact context |
| `TrueF` | empty T2 yields exactly `VALUE(TRUE,{},{})` | when used as `ALLOW` guard it adds no condition beyond that grant | formula itself adds none; adopting clause origin remains external | no free binding or dependency |
| `FalseF` | T1 of complete `TrueF` yields exactly `VALUE(FALSE,{},{})` | adds none by itself | formula itself adds none; adopting clause origin remains external | no free binding or dependency |
| `GOAL` | structural expansion proves internal `==Eval` to its final-state requirement | adds none | origin copied | same free refs/exact key |
| `PRESERVE` | structural expansion proves internal `==Eval` to the pre/final relation requirement | adds none | origin copied | same free refs/exact key |
| `FORBID` | T1 proves internal `==Eval` on the same occurrence result; all metadata/error preserved | adds no grant; prohibits occurrence | origin copied | same free refs/exact key |
| `ALLOW` | adds no hard truth condition | exact unconditional grant; empty trace remains compliant | origin copied | same event binder/exact keys |
| `Any` | T1/T2 prove internal `==Eval` with identical unions and error dominance | unchanged wherever embedded | unchanged | unchanged |
| `Implies` | T1/T3 prove internal `==Eval` with identical unions and error dominance | conditional grant uses guard directly, not this macro | unchanged | unchanged |
| Contract composition | `All` of unioned hard sets | unioned grants, then Delta-classified per-event rules | origins/attestations unioned | choices and exact plugin/symbol/profile dependencies unioned or malformed on conflict |
| Authorization compliance | T3 over grants per Delta-classified controlled event and T2 across those events | definition itself; missing actor has empty grant set | grant origins retained | grant bindings/keys and immutable event declarations retained |

## 8. K2 semantic obligations and unresolved interface questions

The left column is frozen kernel meaning. The right column is an interface
question K2 may answer without changing that meaning.

| Frozen semantic obligation | Unresolved K2 interface choice |
|---|---|
| `Delta` declarations for types, literals, signatures, facets, and immutable EventKey/payload/classification remain distinct from meanings and services; outcomes cannot supply control class. | Transport, declaration/registration schema, identity encoding, compatibility and explicit migration declarations. |
| Model-facing documentation and machine evaluation identify the same exact semantic key and contract. | How identity is displayed, resolved, signed, and compared mechanically. |
| Function/atom meanings match `Delta`; functions return the local `TermResult`, atoms return `Eval`, and permitted outcome facets arrive only through declared anchor arguments. | Invocation mechanism and representation of declarations/results. |
| Every declared `EventScopePair` links a typed `(EventValue)->Bool` scope to a distinct `(Trace)->Bool` occurrence predicate with exact empty-trace and T3/A1 full-result coherence; controlled keys come from `Delta`. | How companion declarations and their semantic validation are encoded. |
| Concrete evaluators return the exact `Eval` algebra with stable evidence/reason identities and declared dependencies. | Evidence schema encoding, storage/reference transport, invocation protocol. |
| Capability declarations state sound fragment, exact dependencies, trust basis, and whether they are concrete-only, partial-symbolic, or complete for a declared fragment. | Capability discovery/negotiation and declaration format. |
| Witnesses, proofs, models, and relation claims name the §5.2 logical or exact relation, satisfy §5.3, bind exact semantics, and never override `chi_C`; logical countermodels require decisive TRUE/FALSE while internal `==Eval` supports derivation proofs. | Certificate encodings, validators, proof-system identifiers, trust roots. |
| Evaluator failures return evaluation errors; reasoning-service failures return reasoning errors; neither returns a logical or profile conclusion. | Error taxonomies, retry metadata, transport mapping. |
| Every required exact `ProfileKey` is in `Dependencies`, closure, composition, and full Contract equivalence. Completed inconclusive profile checks return profile unknown; concrete/symbolic failures return evaluation/reasoning error and no profile judgment. | Profile declaration, coverage-evidence, and checker invocation formats. |
| A joint claim needs a capability whose dependency scope covers the whole cross-plugin formula; local results do not compose into joint results. | Proof exchange, orchestrating joint services, and cross-plugin trust plumbing. |
| `SourceRef` is self-contained provenance and never grants authority or adds a closure lookup; only `AuthorityRef` validation can adopt. | Source-value and authentication/attestation encoding. |

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
  remain independent judgment families; `Delta`, semantic meanings, and service
  capabilities are not conflated.
- [x] Every trace event is admitted and classified only by immutable exact
  `Delta` declarations; no witness/plugin/caller supplies a controlled flag.
- [x] Conditional controlled-event requirements use a typed exact
  `EventScopePair` with full-result scope/occurrence coherence and no kernel
  quantifier or formula-as-term.
- [x] Every inherited candidate and every introduced semantic role has one
  ledger disposition; retained constructs have controlled counterexamples and
  derived constructs have full-facet proofs.
- [x] T1--T4 and A1--A2 are total, deterministic, error-preserving, and
  evaluation-order independent; decisive truth never drops child metadata.
- [x] Requirement, conditional permission, and conditional obligation have
  distinct denotations; permission never creates an occurrence obligation.
- [x] Choice, factual unknown, provenance, authority, and exact version binding
  remain explicit and are never inferred from content or evaluator availability;
  only validated Contract records mechanically determine `chi_C`.
- [x] Core and admitted reasoning rules are sound and capability-relative;
  local plugin conclusions are not promoted to joint conclusions, `UNKNOWN` is
  not a logical countermodel, exact non-error result inequality remains
  distinguishable, and evaluation/reasoning errors yield no relation.
- [x] Logical relation protocols are separate from internal `==Eval` and full
  six-facet equivalence; C18 preserves distinct origins.
- [x] Exact `ProfileKey` requirements participate in dependencies, closure,
  composition, and full equivalence; profile unknown and both failure classes
  remain distinct.
- [x] `SourceRef` is self-contained provenance and never a closure or authority
  shortcut; only `AuthorityRef` resolution can create normative adoption.
- [x] Normalization is limited to proved full-facet-preserving operations.
- [x] The 41-row ledger has 21 retained primitives, 11 derived forms, 6 plugin
  parameters, and 3 exclusions, including dispositions for the derived Outcome
  product, `TrueF`, `FalseF`, exact event declarations, and occurrence companion
  semantics.
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
Relation-table index: public logical-relation protocol and internal `==Eval`/
full-equivalence rules (§5.2); W1 four-case obligation/permission table (§7.3).
Worked derivation/countermodel index: W1--W11 (§7.3), SP-01--SP-10 (§7.2),
derived-form proof matrix (§7.4), and controlled primitive cases CP-D, CP-CTL,
CP-V, CP-PRE, SP-02, CP-F, CP-E, CP-N, CP-C, SP-01, CP-A, SP-05, CP-CTRL,
CP-PR, SP-04, CP-P, CP-PROFILE, CP-U, CP-TE, SP-06, CP-R, CP-UR, and CP-RE
(§6).
