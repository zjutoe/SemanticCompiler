# K3-S minimal coding-plugin semantics v0

This document instantiates the accepted K1 calculus through the exact K2
logical ABI.  It is a semantic specification, not a representation or an
implementation.

## 1. Scope, non-claims, and conformance

K3-S makes one decision: retain only a typed observation vocabulary for an
abstract repository outcome, a typed vocabulary for challenge-required trace
events, one reusable task-acceptance predicate, and the smallest supporting
evidence and reasoning surface.  Everything else is either derived through K1
composition or excluded.  The decision is relative to the accepted seed
challenges; it is not a universal coding ontology.

The exact inherited protocol is
`K2_ABI_V0 = (contract-ir.plugin.logical-abi,(0))`.  K1 alone owns
`Outcome=(PRE,TRACE,FINAL,EVIDENCE)`, formula composition, requirements,
authorizations, choices, provenance, authority, truth and error aggregation,
closure, consistency, relations, and profile results.  K2 alone owns the
identity, declaration, binding, service, model-contract, lifecycle,
dependency, validation-reference, trust, certificate, request, result,
failure, discovery, migration, duplicate, version, conflict, and extension
machinery used below.  This document adds no status, connective, normative
role, choice controller, source-adoption rule, or failure conversion.

Conformance means all of the following.

- Every exact key expands by the constructors in section 3; shorthand is never
  a display-name lookup.
- Every value is admitted by its exact `TypeDeclaration`; every literal used
  by a Contract has the exact literal declaration/binding family in section 3.
- Every atom or function uses its exact declaration, `SemanticBinding`,
  `ContractSpec` roles, derived support, and `ModelContract`.  Services are
  separate.
- `PRE`, `TRACE`, `FINAL`, and `EVIDENCE` enter a meaning only through typed
  anchor-derived positional arguments allowed by the declaration and access
  contract.  No ambient repository, filesystem, command, environment,
  network, evaluator state, hidden test, or expected answer is visible.
- K2 exact-version, no-fallback, duplicate/conflict, trust, result-equality,
  unknown, evaluation-error, reasoning-error, and model/machine identity rules
  apply without qualification.

This document claims only semantic representability over the accepted seed
scope.  It does not claim a concrete patch, buildable implementation,
execution plan, byte format, parser, binder, registry, evaluator, reasoner,
repository operation, operating-system command, network operation, model
behavior, benchmark result, K3-X feasibility, held-out adequacy, or intent
completeness.  It creates no downstream path, handoff, dispatch, mutation
authority, or external artifact.

The only held-out information used is the opaque receipt
`K1-HO-GATE-20260828-A`.  No held-out content, annotation, location, history,
hash, log, or indirect store is part of this specification.

## 2. Coding semantic universe and outcome projections

### 2.1 Abstract values

All collections are finite mathematical sets, maps, or sequences.  Map and set
equality is extensional; sequence equality is positional.  The following are
logical values, not encodings.

- `Path = Path(segment_1,...,segment_n)` is a nonempty root-relative sequence
  of exact case-sensitive `PathSegment` atoms.  Admission rejects an empty
  segment and the reserved atoms `.` and `..`.  `/`, `\`, host roots, case
  folding, symlink resolution, Unicode rewriting, and current-directory rules
  have no semantic role.  A value is already canonical; normalization is the
  admission relation, and two paths are equal exactly when their admitted
  segment sequences are equal.
- `PathSet` is a finite set of admitted `Path` values.  It has no traversal
  order and no glob, host, or prefix convention beyond the explicit
  segment-prefix relation used by its admitting criterion.
- `ArtifactContent = (artifact_role,content_kind,content_value)` is a typed
  observation value.  `content_value` is an exact finite logical value admitted
  by `content_kind`; it is neither bytes nor an instruction to read a file.
- `RepositorySnapshot` is a finite map `Path -> ArtifactContent`.  Absence from
  the map is artifact absence.  Snapshot identity is complete map equality;
  it is independent of a host repository.
- `ChangeSet` is a finite map from every and only differing path to one of
  `CREATED(new)`, `DELETED(old)`, or `MODIFIED(old,new)`, with unequal old/new
  content in the last case.  It is an extensional relation between two supplied
  snapshots, not a sequence, patch, edit request, or transition plan.
- `ObservationSpec` is a closed tagged value naming a finite path/domain
  selector, an observable projection, and its declared comparison domain.
  Selectors can mention exact paths, artifact roles, formats, or an explicitly
  universal abstract request/workload domain; they cannot contain a callback,
  service, environment, expected-answer handle, or host lookup.
- `ObservationResult` is a closed tagged finite value containing the exact
  selected presence/content/behavior observations.  It contains no truth tag.
- `ArtifactSelector` is a typed path/role selector used only over a supplied
  snapshot.  `ByteSize` is a nonnegative integer in the abstract `KiB` unit.
  `Format` is an exact format atom.  `ObservationRelation` is one of
  `EQUAL`, `ACCEPT_REJECT_EQUAL`, `NO_GREATER`, `STRICTLY_LOWER`, or an exact
  `FIELD_CORRESPONDENCE(m)` where `m` is a finite typed bijection between
  observation-field identities.  The last relation holds exactly when renaming
  selected fields by `m` makes the two finite observation structures equal;
  it is not a callback, service handle, or opaque relation name.
- `VerificationSpec=(protocol_identity,subject_scope,evidence_schema_key)` is
  a typed factual verification request.  `VerificationRecord` binds one exact
  spec and snapshot identity to `PASS`, `FAIL`, or `INCONCLUSIVE`, typed
  observations, and one or more stable `EvidenceRef`s.  A record is evidence;
  the applicable predicate, not the record reference, returns K1 truth.
- `Criterion` is exactly one of
  `OBSERVATION_EQUALS(spec,result)`,
  `ONE_FORMAT_OF(selector,nonempty finset(Format))`,
  `ARTIFACTS_NONEMPTY(selector)`,
  `ARTIFACT_SIZE_LT(selector,ByteSize)`,
  `ARTIFACT_SIZE_AT_LEAST(selector,ByteSize)`,
  `UNIVERSAL_OBSERVATION(spec,ObservationRelation)`,
  `DEPENDENCY_REPRODUCIBLE(spec)`, or
  `ADAPTER_CORRESPONDS(spec,ObservationRelation)`.
  These tags are semantic criteria, not task categories.
- `TaskSpec=(nonempty finset(Criterion),finset(VerificationSpec))`.  It contains
  all criteria and evidence requirements visible to `task_accepts`; it cannot
  name a source challenge, expected Contract, expected status, evaluator,
  service, hidden target, or opaque success token.
- `EventPattern` is a closed selector over an exact `EventKey` and, where
  needed, typed payload fields.  It has constructors for any event at a key,
  path membership, and exact command, test, contact, release, or refresh
  subjects.  It has no executable command or network endpoint.

The six event payload values are distinct closed types:

```text
CommandEventPayload          = (abstract_command_id, declared_purpose)
TestEventPayload             = (VerificationSpec, PASS|FAIL|INCONCLUSIVE,
                                finset(EvidenceRef))
PathChangeEventPayload       = (Path, CREATED|DELETED|MODIFIED)
NetworkContactEventPayload   = (contact_class, declared_purpose)
ReleaseEventPayload          = (abstract_release_id, subject_snapshot_identity)
DependencyRefreshEventPayload= (ArtifactSelector, subject_snapshot_identity)
```

`abstract_command_id`, `contact_class`, and `abstract_release_id` are logical
atoms.  They cannot be rendered or invoked as real commands, endpoints, or
release operations by this semantics.

### 2.2 Projection and derivation rules

`snapshot_of : State -> RepositorySnapshot` is the sole coding projection of a
K1 state.  It returns the supplied state value when that value is admitted by
the exact repository-snapshot type contract; otherwise it returns
`TERM_ERROR(NOT_A_REPOSITORY_SNAPSHOT)`.  It reads nothing else.

For admitted snapshots `P` and `F`, the unique change relation is

```text
changes_between(P,F)[p] = CREATED(F[p])       iff p notin dom(P), p in dom(F)
changes_between(P,F)[p] = DELETED(P[p])       iff p in dom(P), p notin dom(F)
changes_between(P,F)[p] = MODIFIED(P[p],F[p]) iff p in both and P[p] != F[p]
```

No other path is in the result.  `observe(spec,snapshot)` is the total exact
projection selected by the typed spec.  A malformed selector is impossible in
an admitted value; a supplied snapshot outside its declared observation domain
returns a term error, not an implicit lookup.

The standard preservation pattern is

```text
Require(Atom(SP(observations_equal),
  Apply(SF(observe),L(T(ObservationSpec),spec),
    Apply(SF(snapshot_of),Anchor(pre))),
  Apply(SF(observe),L(T(ObservationSpec),spec),
    Apply(SF(snapshot_of),Anchor(final)))))
```

The final-state task pattern is

```text
Require(Atom(SP(task_accepts),L(T(TaskSpec),task_spec),
  Apply(SF(snapshot_of),Anchor(final)),Anchor(evidence)))
```

These are ordinary K1 terms and atoms.  `snapshot_of`, `observe`, and
`changes_between` return `TermResult`; term failure follows K1 A2.
`observations_equal`, `task_accepts`, and all other predicates return the exact
K1 `Eval`.  Nothing here creates an outcome, mutates a state, or schedules an
event.

### 2.3 Minimal-vocabulary decision

Repository contents and observations remain separate because equal selected
observations need not imply equal snapshots.  Paths and path sets remain
separate because element identity and finite scope are distinct.  Change sets
are derived values because a second asserted change record could disagree with
the snapshots.  Verification records and `EvidenceRef`s remain separate from
truth because the same evidence can support a false, true, or inconclusive
predicate result under different exact meanings.  `TaskSpec` is retained
because a reusable broad predicate needs a typed, inspectable acceptance
boundary; task-taxonomy atoms are excluded.  Separate event keys are retained
only where immutable K2 event class or payload type differs.  All readable
goal, preservation, prohibition, permission, implication, and alternative
forms remain K1-derived.

## 3. Exact plugin vocabulary, identities, and versions

### 3.1 Exact key constructors

The following definitions are exact logical constructors:

```text
ABI0 = (contract-ir.plugin.logical-abi,(0))
PI   = (capknow.semantic,coding-minimal)
CK   = (PI,(1))

T(n)  = (CK,coding.type,n,TYPE)
L(T,v)= (CK,coding.literal,LITERAL_LOCAL_ID(T,IDENTITY_OF(v)),LITERAL)
DF(n) = (CK,coding.declaration,n,FUNCTION)
DP(n) = (CK,coding.declaration,n,PREDICATE)
SF(n) = (CK,coding.symbol,n,FUNCTION)
SP(n) = (CK,coding.symbol,n,PREDICATE)
DE(n) = (CK,coding.declaration,n,EVENT)
EK(n) = (CK,coding.event,n)
PK(n) = (CK,n)
PAIR(n)= (CK,coding.pair,n)
CS(role,n) = (CK,coding.contract,n,(1),role)
MC(target,n) = (target,coding.model,en-US,(1))
```

`LITERAL_LOCAL_ID` and `IDENTITY_OF` are logical constructors over the exact
type key and complete admitted value.  They are not bytes, hashes, display
names, or lookup functions.  Independently constructed equal values therefore
produce equal literal keys.  A different value produces a different key.

Every retained coding key has exact `PluginKey CK`.  `(PI,(0))`, `(PI,(2))`,
or any other version is a different plugin key.  No ordering or compatibility
is implied.  The namespace/local atoms in the tables below are the exact
arguments to these constructors.

### 3.2 Delta type and literal declarations

<!-- TYPES-BEGIN -->
| Exact type key | Admitted values | Nested type-dependency portion |
|---|---|---|
| `T(Path)` | canonical `Path` values from section 2 | `{}` |
| `T(PathSet)` | finite sets of `T(Path)` | `{DECLARATION(T(Path))}` |
| `T(ArtifactContent)` | exact `(role,kind,value)` records | `{}` |
| `T(RepositorySnapshot)` | finite maps `T(Path)->T(ArtifactContent)` | `{DECLARATION(T(Path)),DECLARATION(T(ArtifactContent))}` |
| `T(ChangeSet)` | exact extensional change maps | `{DECLARATION(T(Path)),DECLARATION(T(ArtifactContent))}` |
| `T(ObservationSpec)` | closed typed observation selectors | `{DECLARATION(T(PathSet))}` |
| `T(ObservationResult)` | closed typed finite observation values | `{DECLARATION(T(Path)),DECLARATION(T(ArtifactContent))}` |
| `T(ArtifactSelector)` | exact path/role selectors | `{DECLARATION(T(PathSet))}` |
| `T(ByteSize)` | nonnegative abstract KiB integers | `{}` |
| `T(Format)` | exact format atoms | `{}` |
| `T(ObservationRelation)` | the closed relation tags in section 2 | `{}` |
| `T(VerificationSpec)` | exact verification specifications | `{}` |
| `T(VerificationRecord)` | exact typed verification records | `{DECLARATION(T(VerificationSpec)),DECLARATION(T(ObservationResult))}` |
| `T(Criterion)` | exactly the eight closed criterion variants | `{DECLARATION(T(ObservationSpec)),DECLARATION(T(ObservationResult)),DECLARATION(T(ArtifactSelector)),DECLARATION(T(ByteSize)),DECLARATION(T(Format)),DECLARATION(T(ObservationRelation))}` |
| `T(TaskSpec)` | finite typed task specifications | `{DECLARATION(T(Criterion)),DECLARATION(T(VerificationSpec))}` |
| `T(EventPattern)` | closed event selectors | `{DECLARATION(T(PathSet)),DECLARATION(T(VerificationSpec)),DECLARATION(T(ArtifactSelector))}` |
| `T(CommandEventPayload)` | exact abstract command records | `{}` |
| `T(TestEventPayload)` | exact test-observation records | `{DECLARATION(T(VerificationSpec))}` |
| `T(PathChangeEventPayload)` | exact path/change-kind records | `{DECLARATION(T(Path))}` |
| `T(NetworkContactEventPayload)` | exact contact-class records | `{}` |
| `T(ReleaseEventPayload)` | exact abstract release records | `{}` |
| `T(DependencyRefreshEventPayload)` | exact refresh records | `{DECLARATION(T(ArtifactSelector))}` |
<!-- TYPES-END -->

For each type row `T(n)`, the exact
`proper_declaration_dependencies` field is the displayed nested portion union
`{CONTRACT_SPEC(CS(TYPE_ADMISSION,type.n))}` and every support root of that
type-admission ContractSpec.  Thus even a scalar row with displayed `{}` has
its exact admitting-contract root; no producer can omit it.

For every admitted value `v:T`, the exact literal declaration family is

```text
LiteralDeclaration(T,v) = (
  key=L(T,v), literal_identity=v, result_type=T,
  proper_declaration_dependencies={DECLARATION(T)})
```

and its exact literal `SemanticBinding` has `binding_key=declaration_key=L(T,v)`,
kind `LITERAL`, meaning `TERM_VALUE(v)`,
`CS(EVIDENCE_SCHEMA,none)`, `CS(ACCESS_BOUNDARY,literal)`, unknown
`CS(UNKNOWN_BEHAVIOR,not_applicable)`, error
`CS(EVALUATION_ERROR_BEHAVIOR,literal)`, and the model contract
`MC(BINDING_IDENTITY(L(T,v)),literal)` with exact signature `()->T`, empty
facet sequence, and `NO_SYMBOL_LITERAL`.  Its permitted-facet sequence is
empty, its determinism rule is
`SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT`, and its exact proper semantic
dependencies are its literal declaration plus the five displayed ContractSpec
roots; their supports and the type declaration occur only in the mechanically
derived closure.  Literal meanings have no v0 service.  An absent literal
declaration is malformed; a declared literal with no exact binding or model
contract is open.

### 3.3 Function and predicate declarations

K1 carrier sorts `State`, `Trace`, `EvidenceStore`, and `EventValue` occur in
signatures exactly as in accepted K2 cases and pair rules; they are not coding
type declarations.

| Exact declaration / symbol | Kind and signature | Exact facet positions |
|---|---|---|
| `DF(snapshot_of)` / `SF(snapshot_of)` | function `(State)->T(RepositorySnapshot)` | `({pre,final})` |
| `DF(changes_between)` / `SF(changes_between)` | function `(T(RepositorySnapshot),T(RepositorySnapshot))->T(ChangeSet)` | `({pre},{final})` |
| `DF(observe)` / `SF(observe)` | function `(T(ObservationSpec),T(RepositorySnapshot))->T(ObservationResult)` | `({}, {pre,final})` |
| `DP(observations_equal)` / `SP(observations_equal)` | predicate `(T(ObservationResult),T(ObservationResult))->Bool` | `({pre},{final})` |
| `DP(task_accepts)` / `SP(task_accepts)` | predicate `(T(TaskSpec),T(RepositorySnapshot),EvidenceStore)->Bool` | `({}, {final}, {evidence})` |
| `DP(dependency_metadata_changed)` / `SP(dependency_metadata_changed)` | predicate `(T(ChangeSet))->Bool` | `({pre,final})` |
| `DP(verification_passed)` / `SP(verification_passed)` | predicate `(T(VerificationSpec),EvidenceStore)->Bool` | `({}, {evidence})` |
| `DP(event_matches)` / `SP(event_matches)` | predicate `(T(EventPattern),EventValue)->Bool` | `({}, {})` |
| `DP(event_occurred)` / `SP(event_occurred)` | predicate `(T(EventPattern),Trace)->Bool` | `({}, {trace})` |
| `DP(refresh_scope)` / `SP(refresh_scope)` | predicate `(EventValue)->Bool` | `({})` |
| `DP(refresh_occurred)` / `SP(refresh_occurred)` | predicate `(Trace)->Bool` | `({trace})` |

For each row the declaration key kind, symbol key kind, plugin, namespace, and
local atom must agree exactly.  Proper declaration dependencies are exactly
the displayed plugin type keys lifted to `DECLARATION`; K1 carrier sorts add no
plugin dependency.  No declaration owns meaning, evidence, service, or trust.

### 3.4 Event, pair, and profile keys

| Event declaration / key | Payload type | Immutable class | Semantic purpose |
|---|---|---|---|
| `DE(command)` / `EK(command)` | `T(CommandEventPayload)` | `CONTROLLED` | abstract command occurrence |
| `DE(test)` / `EK(test)` | `T(TestEventPayload)` | `OBSERVATIONAL` | factual test observation |
| `DE(path_change)` / `EK(path_change)` | `T(PathChangeEventPayload)` | `CONTROLLED` | abstract path-change occurrence |
| `DE(network_contact)` / `EK(network_contact)` | `T(NetworkContactEventPayload)` | `CONTROLLED` | abstract network contact |
| `DE(release)` / `EK(release)` | `T(ReleaseEventPayload)` | `CONTROLLED` | abstract release occurrence |
| `DE(dependency_refresh)` / `EK(dependency_refresh)` | `T(DependencyRefreshEventPayload)` | `CONTROLLED` | dependency materialization refresh |

Each event's proper declaration dependency is exactly its payload-type
declaration.  An event payload never supplies or overrides `event_class`.

The sole companion declaration is

```text
PAIR(refresh) = (CK,coding.pair,refresh)
scope_symbol      = SP(refresh_scope)
occurrence_symbol = SP(refresh_occurred)
controlled_keys   = {EK(dependency_refresh)}
admission          = DEFINITIONAL_T3_A1
```

Its signatures/facets are the exact K2-derived pair shapes.  Its exact proper
declaration dependencies are the declaration and symbol roots of both members
and `EVENT(EK(dependency_refresh))`; member type dependencies occur only in
their derived closure.  The pair-owned occurrence binding is the K2
`OccurrenceBindingProjection`; no ordinary
`SemanticBinding(DP(refresh_occurred))` exists.

The sole profile is

```text
PK(implementation_evidence) = (CK,implementation_evidence)
dimensions = {
  (PK(implementation_evidence),abstract_acceptance_evidence),
  (PK(implementation_evidence),concrete_implementation_evidence)
}
```

Its coverage meaning judges only evidence-dimension coverage.  It changes no
hard acceptance or consistency result.

## 4. Declarations, meanings, dependencies, and model contracts

### 4.1 Exact ContractSpec catalog

Every contract below is a K2 `ContractSpec` with exact key `CS(role,name)`,
owner `CK`, displayed owner layer and role, exact primary/codomain types, exact
observation-query map, and the displayed extensional relation.  The query map
domain equals extensional `support`; no relation receives a binding,
`SemanticEnvironment`, trust record, request, or another contract.

| ContractSpec family | Layer / role | Primary input -> codomain and exact relation | Derived support |
|---|---|---|---|
| `CS(TYPE_ADMISSION,type.n)` for every section 3 type | Delta / `TYPE_ADMISSION` | `Value -> admitted|not_admitted` by the closed value definition in section 2 | exactly the nested `DECLARATION[TYPE] -> TYPE_ADMISSION_FACT` keys in the type table; empty for scalar rows |
| `CS(LITERAL_MEANING,literal.T.v)` | Sigma / `LITERAL_MEANING` | exact literal identity -> `TERM_VALUE(v)` | `{}` |
| `CS(FUNCTION_MEANING,snapshot_of)` | Sigma / `FUNCTION_MEANING` | `State -> TERM_VALUE(snapshot)` iff admitted, else `TERM_ERROR(NOT_A_REPOSITORY_SNAPSHOT)` | `{DECLARATION(T(RepositorySnapshot))->TYPE_ADMISSION_FACT}` |
| `CS(FUNCTION_MEANING,changes_between)` | Sigma / `FUNCTION_MEANING` | snapshot pair -> the unique section 2 `TERM_VALUE(ChangeSet)` | `{}` |
| `CS(FUNCTION_MEANING,observe)` | Sigma / `FUNCTION_MEANING` | `(ObservationSpec,RepositorySnapshot) -> TERM_VALUE(ObservationResult)` or declared domain `TERM_ERROR` | `{}` |
| `CS(PREDICATE_MEANING,observations_equal)` | Sigma / `PREDICATE_MEANING` | two results -> `VALUE(TRUE|FALSE,{},{})` by exact equality | `{}` |
| `CS(PREDICATE_MEANING,verification_passed)` | Sigma / `PREDICATE_MEANING` | spec/store -> `TRUE` for one schema-valid decisive pass, `FALSE` for a decisive fail, `UNKNOWN` for absent/inconclusive compatible evidence, `ERROR` for schema/conflict/access failure | `{}` |
| `CS(PREDICATE_MEANING,task_accepts)` | Sigma / `PREDICATE_MEANING` | task/snapshot/store -> K1 A1 conjunction of all typed criterion results and required verification results; empty hidden context | `{BINDING(DF(observe))->TERM_RESULT, BINDING(DP(verification_passed))->EVAL_RESULT}` |
| `CS(PREDICATE_MEANING,dependency_metadata_changed)` | Sigma / `PREDICATE_MEANING` | change set -> true iff at least one extensional entry has dependency-metadata artifact role | `{}` |
| `CS(PREDICATE_MEANING,event_matches)` | Sigma / `PREDICATE_MEANING` | pattern/event value -> exact structural match; keys outside the pattern are false | `{}` |
| `CS(PREDICATE_MEANING,event_occurred)` | Sigma / `PREDICATE_MEANING` | pattern/trace -> K1 `ANY_RESULT` over `event_matches(pattern,event_value)` in trace order-insensitive set aggregation | `{BINDING(DP(event_matches))->EVAL_RESULT_SEQUENCE}` |
| `CS(PREDICATE_MEANING,refresh_scope)` | Sigma / `PREDICATE_MEANING` | event value -> true exactly for admitted `EK(dependency_refresh)` payloads whose selector is the exact `dependency-lock` artifact role, false for every other admitted event | `{}` |
| `CS(PROFILE_COVERAGE,implementation_evidence)` | Sigma / `PROFILE_COVERAGE` | typed coverage subject -> exact complete/incomplete/unknown profile result | `{BINDING(DP(task_accepts))->EVAL_RESULT}` |
| `CS(EVIDENCE_SCHEMA,none)` | Sigma / `EVIDENCE_SCHEMA` | explicit inputs -> only empty evidence-reference set admitted | `{}` |
| `CS(EVIDENCE_SCHEMA,verification)` | Sigma / `EVIDENCE_SCHEMA` | EvidenceStore projection -> exactly schema-valid `VerificationRecord`/`EvidenceRef` pairs | `{DECLARATION(T(VerificationRecord))->TYPE_ADMISSION_FACT}` |
| `CS(ACCESS_BOUNDARY,A)` | Sigma / `ACCESS_BOUNDARY` | for each exact `A` named below, admits only its listed positional fields/facets and lower observations | exactly the same lower binding support as its meaning, otherwise `{}` |
| `CS(UNKNOWN_BEHAVIOR,not_applicable)` | Sigma / `UNKNOWN_BEHAVIOR` | literal/function input -> `NOT_APPLICABLE` | `{}` |
| `CS(UNKNOWN_BEHAVIOR,never)` | Sigma / `UNKNOWN_BEHAVIOR` | admitted predicate input -> no unknown result is in the relation | `{}` |
| `CS(UNKNOWN_BEHAVIOR,evidence_pending)` | Sigma / `UNKNOWN_BEHAVIOR` | predicate input -> stable missing/inconclusive verification reasons only | `{}` |
| `CS(UNKNOWN_BEHAVIOR,task)` | Sigma / `UNKNOWN_BEHAVIOR` | task input -> stable missing/inconclusive verification or declared universal-domain incompleteness only | `{}` |
| `CS(EVALUATION_ERROR_BEHAVIOR,literal)` | Sigma / `EVALUATION_ERROR_BEHAVIOR` | admitted literal input -> no evaluation error is in the relation | `{}` |
| `CS(EVALUATION_ERROR_BEHAVIOR,term)` | Sigma / `EVALUATION_ERROR_BEHAVIOR` | term input -> nonempty stable type/domain/access errors | `{}` |
| `CS(EVALUATION_ERROR_BEHAVIOR,predicate)` | Sigma / `EVALUATION_ERROR_BEHAVIOR` | predicate input -> nonempty stable schema/conflict/access errors | `{}` |
| `CS(EVALUATION_ERROR_BEHAVIOR,profile)` | Sigma / `EVALUATION_ERROR_BEHAVIOR` | profile input -> nonempty stable schema/conflict/access errors | `{}` |
| `CS(REASONING_ERROR_BEHAVIOR,profile)` | Sigma / `REASONING_ERROR_BEHAVIOR` | profile request -> nonempty stable reasoning failure | `{}` |
| `CS(SOUND_FRAGMENT,functions)` | Service / `SOUND_FRAGMENT` | exactly the three function binding targets and their admitted typed invocations | complete target closures |
| `CS(SOUND_FRAGMENT,predicates)` | Service / `SOUND_FRAGMENT` | exactly the seven ordinary predicate targets and the pair-owned occurrence target and their admitted typed invocations | complete target closures |
| `CS(SOUND_FRAGMENT,profile)` | Service / `SOUND_FRAGMENT` | exactly the implementation-evidence profile target and admitted coverage subjects | complete profile closure |
| `CS(SOUND_FRAGMENT,bundle_bounds)` | Service / `SOUND_FRAGMENT` | exact closed conjunctions of the nonempty/size criterion atoms over one selector/snapshot | `{BINDING(DP(task_accepts))}` |
| `CS(COMPLETE_FRAGMENT,bundle_bounds)` | Service / `COMPLETE_FRAGMENT` | the same named finite contradiction fragment | `{BINDING(DP(task_accepts))}` |
| `CS(REQUIRED_EVIDENCE,service)` | Service / `REQUIRED_EVIDENCE` | exact request evidence required by the target meaning or proof | target binding/profile support only |
| `CS(SERVICE_FAILURE_BEHAVIOR,service)` | Service / `SERVICE_FAILURE_BEHAVIOR` | exact K2 role-specific evaluation/reasoning failure tags | `{}` |

The access names are exact: `literal`, `state_only`, `snapshot_pair`, `spec_snapshot`,
`result_pair`, `task_final_evidence`, `change_set_only`,
`evidence_only`, `pattern_event`, `pattern_trace`, `event_only`, and
no others.  Each admits
only the signature positions its name enumerates and the exact facet positions
in section 3.  In particular, `task_final_evidence` admits the `TaskSpec`, one
supplied final snapshot, one supplied `EvidenceStore`, and the two lower
observations in its support; it admits no Contract, challenge, expected result,
service state, provenance, choice, or other outcome facet.

`task_accepts` is reusable: its criterion algebra applies to every admitted
`TaskSpec`, not to a finite challenge mapping.  For each criterion it computes
the extensional fact from the supplied snapshot/observation result.  Required
verification facts use `verification_passed`.  K1 A1 unions all evidence,
unknown reasons, and errors; error dominates, otherwise false dominates,
otherwise unknown precedes true.  A `VerificationRecord` with the wrong schema
or snapshot identity is not success.  A missing record is factual unknown.

The eight criterion results are exact.  `OBSERVATION_EQUALS` compares
`observe(spec,snapshot)` with its supplied typed result.  `ONE_FORMAT_OF`
requires a nonempty selected population whose artifacts all share one member
of the supplied format set.  `ARTIFACTS_NONEMPTY` tests selected-map
nonemptiness.  The two size criteria quantify over every selected artifact in
the abstract KiB unit.  `UNIVERSAL_OBSERVATION` compares every declared
subject/reference observation pair by its relation;
`DEPENDENCY_REPRODUCIBLE` compares the two complete dependency-resolution
lanes selected by its spec; and `ADAPTER_CORRESPONDS` compares every declared
client/adapter pair by its relation.  A complete observation with a
counterexample is false, a complete one without a counterexample is true, and
a declared universal/correspondence domain whose result is incomplete is
unknown with a stable reason.  Type, schema, conflict, or undeclared-access
failure is `Eval.ERROR`.  None of these rules consults a challenge label,
expected mapping, service state, or ambient repository.

### 4.2 Semantic bindings and dependency closure

| Binding(s) | Meaning / evidence / access / unknown / error ContractSpecs | Exact semantic roots beyond the declaration and these specs | Validation references |
|---|---|---|---|
| `DF(snapshot_of)` | `snapshot_of`; `none`; `state_only`; `not_applicable`; `term` | type-admission observation for `T(RepositorySnapshot)` | `{}` |
| `DF(changes_between)` | `changes_between`; `none`; `snapshot_pair`; `not_applicable`; `term` | `{}` | `{}` |
| `DF(observe)` | `observe`; `none`; `spec_snapshot`; `not_applicable`; `term` | `{}` | `{}` |
| `DP(observations_equal)` | same-named meaning; `none`; `result_pair`; `never`; `predicate` | `{}` | `{}` |
| `DP(task_accepts)` | same-named meaning; `verification`; `task_final_evidence`; `task`; `predicate` | exact lower `observe` and `verification_passed` bindings | `{}` |
| `DP(dependency_metadata_changed)` | same-named meaning; `none`; `change_set_only`; `never`; `predicate` | `{}` | `{}` |
| `DP(verification_passed)` | same-named meaning; `verification`; `evidence_only`; `evidence_pending`; `predicate` | `{}` | `{}` |
| `DP(event_matches)` | same-named meaning; `none`; `pattern_event`; `never`; `predicate` | `{}` | `{}` |
| `DP(event_occurred)` | same-named meaning; `none`; `pattern_trace`; `never`; `predicate` | exact lower `event_matches` binding | `{}` |
| `DP(refresh_scope)` | same-named meaning; `none`; `event_only`; `never`; `predicate` | `{}` | `{}` |
| `PAIR(refresh)` occurrence projection | exact K2 `T3_A1_MEANING_LIFT`, `T3_A1_EVIDENCE_LIFT`, `T3_A1_ACCESS_LIFT`, `T3_A1_UNKNOWN_LIFT`, and `T3_A1_ERROR_LIFT` records | exact `T3_A1_DEPENDENCY_LIFT(pd,pb,sb)` for the retained pair declaration/binding and scope binding | `{}` for the retained definitional path |

Every binding key is derived from its declaration key; all binding kinds,
facets, contracts, and `SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT` are exact.
For every row, K2 section 3.3 recomputes `proper_semantic_dependencies` and the
least acyclic `dependency_closure` from the declaration, listed ContractSpecs,
their extensional supports, and listed lower bindings.  The producer cannot
supply a smaller or larger set.  `task_accepts` has two independent lower
nodes, so any valid topological order yields the same complete observation
map.  A self-edge or genuine cycle is malformed.  Mandatory validation
references, when a K2 independent-proof conformance fixture selects that
generic path, remain in `DependencyEnvironment.validation_references` and are
never added to this proper DAG.

The retained `EventPairBinding` itself has the exact K2 proper roots
`PAIR_DECLARATION(PAIR(refresh))`, `BINDING(DP(refresh_scope))`,
`BINDING(DP(refresh_occurred))`, and
`MODEL_CONTRACT(MC(BINDING_IDENTITY(DP(refresh_occurred)),refresh_occurred))`.
Those pair-record roots are distinct from the occurrence projection's exact
`T3_A1_DEPENDENCY_LIFT`.  In particular, none is a validation reference and
the definitional path invents no certificate or validator dependency.

The profile binding uses the exact profile/dimensions in section 3,
`CS(PROFILE_COVERAGE,implementation_evidence)`,
`CS(EVIDENCE_SCHEMA,verification)`, derived support on `task_accepts`,
`evidence_pending`, `profile` evaluation error, and `profile` reasoning error.
Its missing binding is open;
checker absence gives no profile result.

### 4.3 Exact model/machine identity

Every ordinary literal/function/predicate binding and the pair-owned
occurrence projection has exactly one required English model record:

```text
model key = MC(BINDING_IDENTITY(binding_key), local_binding_name)
target_binding_key = binding_key
exact_symbol_key = the exact SF/SP key, or NO_SYMBOL_LITERAL
exact_signature = the section 3 signature
exact_facet_positions = the section 3 facet sequence
evidence_contract = the identical binding evidence ContractSpec
unknown_contract = the identical binding unknown ContractSpec
error_contract = the identical binding error ContractSpec
semantic_contract_reference = the identical meaning ContractSpecKey
capability_summaries = exact projection of every descriptor targeting binding
```

Consequently the three function model records each summarize only
`CAP(functions)`; the seven ordinary predicate model records each summarize
only `CAP(predicates)`; the pair occurrence model record summarizes only
`CAP(predicates)`; and literal model records have the empty summary set.  These
are exact sets, not lower bounds.

For `refresh_occurred`, the model key is producer-supplied exactly as
`MC(BINDING_IDENTITY(DP(refresh_occurred)),refresh_occurred)` in the retained
`EventPairBinding`; its fields equal the complete K2 occurrence projection.
No model record creates a meaning or service.  Absence is
`OPEN_BINDINGS(model contract)`; any field mismatch is malformed; unequal
same-key records conflict.  Explanatory prose is diagnostic only.  A model
contract at `(2)` or for a display-similar symbol does not bind `(1)`.

### 4.4 Omission, duplicates, versions, and conflicts

These total K2 outcomes apply to every item above.

| Missing or conflicting role | Exact result |
|---|---|
| required type/literal/function/predicate/event/pair declaration | `MALFORMED` / `DECLARATION_INVALID`, later lifecycle coordinates blocked |
| valid declaration but ordinary/pair/profile/model binding absent | `OPEN_BINDINGS` with exact missing key; no service can repair it |
| exact semantic binding present but compatible capability absent/outside fragment/root-incompatible | closed if otherwise complete plus `EVALUABILITY_MISSING`; no truth/profile result |
| capability or root discovery undecided | `EVALUABILITY_UNKNOWN`; no invocation |
| discovery protocol/transport or invocation failure | the exact K2 discovery or role-projected failure; no fabricated logical result |
| exact equal duplicate logical records | coalesce independent of input order |
| unequal records at one exact identity | kind-appropriate malformed/conflict; no winner |
| different owner, plugin, kind, or exact version | distinct identity; never a duplicate or substitute |

Aliases, latest-version selection, input order, registration order, discovery
order, service order, and display labels never change these results.

## 5. Trace events, requirements, authorization, and choices

### 5.1 Event meanings

`event_matches(pattern,event_value)` checks the exact event key first and then
only the payload fields admitted by that pattern constructor.  A key mismatch
is `VALUE(FALSE,{},{})`; an ill-typed event is rejected by Delta before the
meaning runs.  `event_occurred(pattern,trace)` is the exact K1 T3/A1
`ANY_RESULT` of those per-event matches: empty trace is false; evidence,
unknowns, and errors are all unioned; error dominates; otherwise any true is
decisive while unknown metadata is retained.

The retained `PAIR(refresh)` is narrower because K1 controlled-event
conditional requirements require an exact unary scope/trace companion.  Its
scope is true exactly for admitted `EK(dependency_refresh)` payloads selecting
the `dependency-lock` artifact role and false for every other admitted event.
Its occurrence meaning is the K2 definitional T3/A1 lift.  The pair adds no
planner or event constructor.

### 5.2 Normative patterns

The following are ordinary K1 compositions; none is a plugin-owned role.

```text
Forbidden(pattern) =
  Require(Not(Atom(SP(event_occurred),
    L(T(EventPattern),pattern),Anchor(trace))))

Authorized(p,pattern,guard) =
  Authorize(p,x:EventValue,
    Atom(SP(event_matches),L(T(EventPattern),pattern),Var(x)), guard)

RefreshRequiredWhen(condition) =
  Require(Implies(condition,
    Atom(SP(refresh_occurred),Anchor(trace))))

RefreshAuthorizedWhen(p,condition) =
  Authorize(p,x:EventValue,
    Atom(SP(refresh_scope),Var(x)), condition)
```

A conditional refresh obligation contains both the requirement and the grant;
a conditional permission contains only the grant.  When the condition is true
and no event occurs, permission succeeds but obligation fails.  When the
condition is false and the event occurs, closed-world authorization fails.
Evaluability of the guard, scope, or occurrence meaning grants no authority.

Network prohibition uses `Forbidden(NETWORK_ANY)`.  Path-change permission
uses an exact `PATH_IN(PathSet)` pattern.  Release permission can be guarded by
`verification_passed(spec,EVIDENCE)`.  Test events are observational and do
not enter K1 authorization compliance, but their payload does not substitute
for verification evidence unless the declared evidence schema explicitly
links the same stable references.

### 5.3 Requirements, alternatives, and choices

Final acceptance and preservation use the section 2 patterns.  Controlled
path scope uses the exact `PATH_IN(PathSet)` event pattern; no second
change-scope predicate is retained.

Alternative formats are K1 `Any` over two or more `task_accepts` atoms or one
typed `ONE_FORMAT_OF` criterion; both have extensional factual semantics and
select no choice.  A controller-owned format or backend choice instead uses a
K1 `ChoiceDecl` over admitted values.  Only a validated
`BIND_CHOICE(choice_id)` authority fact creates `chi_C`; before that the
Contract is well formed and open.  Missing verification evidence is
`TRUTH_UNKNOWN`, never `OPEN_BINDINGS` and never an owned choice.

Provenance stays in K1 `SourceRef`/`Origins`.  Identical formula content from
two exact sources stays separately attributed.  Only an exact K2-admitted
`AuthorityFactKey=(AuthorityRef,SourceRef,Principal,NormativeRole)` permits
adoption.  Neither a coding event, predicate result, verification record,
model contract, trust root, nor source wording creates normative force.

## 6. Evidence, capabilities, trust, results, and failures

### 6.1 Evidence and result contract

Every coding verification reference has the exact K2 shape

```text
EvidenceRef(
  issuer_scope,
  coding.verification,
  stable_record_identity,
  CS(EVIDENCE_SCHEMA,verification))
```

The referenced `VerificationRecord` must match the exact spec and snapshot
identity and be admitted by that schema.  The reference contains no truth,
success, authority, consistency, profile, or expected-answer field.
`verification_passed` returns false only from decisive admitted failing
evidence, true only from decisive admitted passing evidence, unknown with a
nonempty stable reason for missing/inconclusive evidence, and error for
schema, conflict, or access failure.  `task_accepts` preserves these sets under
K1 A1.

All function results equal their exact `FUNCTION_MEANING` relation as complete
`TermResult` records.  All predicate results equal their exact
`PREDICATE_MEANING` relation as complete `Eval` records.  A shape-valid unequal
truth, value, evidence set, unknown set, or error set is K2
`MALFORMED_RESULT(SEMANTIC_MISMATCH)`; the returned semantics is discarded and
the role projection produces the matching evaluation error.  `FALSE`,
`UNKNOWN`, `Eval.ERROR`, `TERM_ERROR`, malformedness, and reasoning failure
remain disjoint.

### 6.2 Exact services and capabilities

```text
TP = (capknow.embedding,coding-fixture-policy,(1))
TR = (TP,coding,semantic-service-root,(1))

SK(functions) = (CK,coding.service,functions,(1),FUNCTION_EVALUATION)
CAP(functions)= (SK(functions),core_functions)
SK(predicates)= (CK,coding.service,predicates,(1),PREDICATE_EVALUATION)
CAP(predicates)= (SK(predicates),core_predicates)
SK(profile)    = (CK,coding.service,profile,(1),PROFILE_CONCRETE)
CAP(profile)   = (SK(profile),implementation_evidence)
SK(bounds)     = (CK,coding.service,bounds,(1),REASONING)
CAP(bounds)    = (SK(bounds),bundle_bounds)

FUNCTION_TARGETS = {
  BINDING_TARGET(DF(snapshot_of)),
  BINDING_TARGET(DF(changes_between)),
  BINDING_TARGET(DF(observe))
}
PREDICATE_TARGETS = {
  BINDING_TARGET(DP(observations_equal)),
  BINDING_TARGET(DP(task_accepts)),
  BINDING_TARGET(DP(dependency_metadata_changed)),
  BINDING_TARGET(DP(verification_passed)),
  BINDING_TARGET(DP(event_matches)),
  BINDING_TARGET(DP(event_occurred)),
  BINDING_TARGET(DP(refresh_scope)),
  BINDING_TARGET(DP(refresh_occurred))
}
```

For the finite bounds target, let `S_b:T(ArtifactSelector)` and the three
criterion-specific task values
`ts_nonempty`, `ts_lt_100`, and `ts_ge_200:T(TaskSpec)` be exact admitted
logical values over one artifact population and unit.  Let `C_b` be the exact
closed K1 Contract whose sole hard formula is
`All({TA(ts_nonempty),TA(ts_lt_100),TA(ts_ge_200)})`, with a matching admitted
authority adoption, empty grants/choices/profiles beyond mechanically required
records, and all mechanically derived facets.  Here `TA` is the exact expansion
in section 7.1.  Let `E_b` be the complete
exact `SemanticEnvironment` mechanically required by `C_b`, and define

```text
J_b = ENVIRONMENT_JUDGMENT_TARGET(
        CONSISTENCY, (C_b), semanticIdentity(E_b))
```

`J_b` is a finite exact logical target.  Neither its subject nor environment
contains a challenge identifier.

| Capability | Class and supported targets/judgments | Exact fragment and dependency scope | Required root/failure contract |
|---|---|---|---|
| `CAP(functions)` | `CONCRETE_EVALUATION_ONLY`; `{FUNCTION_EVALUATION}`; supported targets exactly `FUNCTION_TARGETS` | `CS(SOUND_FRAGMENT,functions)`, no complete fragment; dependency scope is the exact union of all three target closures | nonempty `{TR}`; `CS(REQUIRED_EVIDENCE,service)` and `CS(SERVICE_FAILURE_BEHAVIOR,service)` |
| `CAP(predicates)` | `CONCRETE_EVALUATION_ONLY`; `{PREDICATE_EVALUATION}`; supported targets exactly `PREDICATE_TARGETS` | `CS(SOUND_FRAGMENT,predicates)`, no complete fragment; dependency scope is the exact union of all eight target closures | same exact requirements |
| `CAP(profile)` | `CONCRETE_EVALUATION_ONLY`; `{PROFILE_COVERAGE}`; supported targets exactly `{PROFILE_TARGET(PK(implementation_evidence))}` | `CS(SOUND_FRAGMENT,profile)`, no complete fragment; dependency scope is the exact profile closure | same exact requirements |
| `CAP(bounds)` | `COMPLETE_FOR_DECLARED_FRAGMENT`; `{CONSISTENCY}`; supported targets exactly `{J_b}` | sound `CS(SOUND_FRAGMENT,bundle_bounds)` and complete `CS(COMPLETE_FRAGMENT,bundle_bounds)`; dependency scope exactly equals the complete mechanical dependency set of `J_b` | same exact requirements, reasoning-role failure mapping |

Every descriptor also has exact ABI/plugin/service identity, nonempty target
set, derived proper dependencies/closure, and a `ModelCapabilitySummary` in
each targeted model contract.  A service is availability, not denotation.  A
meaning may be bound and closed while these descriptors are absent or unusable.

The bounds capability proves only the exact theorem at `J_b`

```text
ARTIFACTS_NONEMPTY(S) AND
forall artifact in S: size < upper AND size >= lower AND lower >= upper
  -> CONSISTENCY_UNSAT
```

for one admitted selector, unit, snapshot domain, and complete closed
conjunction.  It proves no arbitrary arithmetic, task correctness, existence,
or cross-plugin joint conclusion.  Outside that fragment, or without its exact
admitted certificate, the consistency result is `CONSISTENCY_UNKNOWN` absent a
different K1 witness/proof.  Service failure is `REASONING_ERROR` and yields no
consistency result for that invocation.

### 6.3 Trust and lifecycle

`TP` and `TR` are embedding-policy identities, not coding-plugin records.  A
request-specific `TrustEnvironment` is exact and finite.  `TR` is usable only
under `TRUST_ROOT_ADMITTED` with owner
`EMBEDDING_POLICY_PRODUCER(TP)`, `V0_EXTERNAL_TRUST_PREMISE`, and permitted
targets that enumerate each exact capability, judgment, `ServiceUseSubject`,
and `SemanticEnvironmentIdentity`.  No wildcard is permitted.  Its producer
must satisfy K2 service-use independence from the capability and full semantic
subject producer set.

The five trust branches stay exact:

- admitted and correctly scoped root: compatible discovery may reach
  `CAPABILITY_DISCOVERED`, `INVOCABLE_FOR`, and one conformant completion;
- absent or incompatible/wrong-scope root: capability incompatible and
  `EVALUABILITY_MISSING`;
- `TRUST_ROOT_UNDECIDED`: `EVALUABILITY_UNKNOWN`, no invocation;
- `TRUST_ROOT_FAILED`: exact discovery protocol/transport failure and no
  evaluability or semantic result.

The declaration, binding, discovery, and invocation coordinates are always
reported independently by K2 section 2.4.  Trust never adopts a clause or
binds a choice.

### 6.4 Cross-plugin and abstract-evidence limits

A foreign plugin atom composes with a coding atom only through K1 `All` under
its own exact `PluginKey`, declaration, binding, model contract, service, and
trust records.  `CAP(bounds)` covers only `CK`; it cannot establish a joint
license/dependency conclusion.  Without one exact joint
`ENVIRONMENT_JUDGMENT_TARGET` capability whose dependency scope and root cover
the entire composed subject, evaluability may be missing while consistency is
`CONSISTENCY_UNKNOWN`.

An admitted abstract satisfying witness may establish `CONSISTENCY_SAT` for a
closed Contract.  It is an abstract `Outcome` under the exact meanings and
derived `chi_C`; it is not a patch, build, command, repository transition, or
construction method.  The separate implementation-evidence profile may still
be `PROFILE_INCOMPLETE`.

## 7. K0 seed challenge bindings and status analysis

### 7.1 Exact coverage table

Challenge identifiers in this table are conformance labels only.  They are not
values in any declaration, binding, task, request, result, evidence record, or
service.

The Contract-pattern column uses only the following exact expansions.  Each
lower-case argument denotes one complete admitted literal value of the shown
type supplied with the Contract, not a lookup or hidden fixture.

```text
RS(a)       = Apply(SF(snapshot_of),Anchor(a))
CH          = Apply(SF(changes_between),RS(pre),RS(final))
OBS(s,a)    = Apply(SF(observe),L(T(ObservationSpec),s),RS(a))
OBS_EQ(s)   = Atom(SP(observations_equal),OBS(s,pre),OBS(s,final))
TA(t)       = Atom(SP(task_accepts),L(T(TaskSpec),t),RS(final),Anchor(evidence))
VP(v)       = Atom(SP(verification_passed),L(T(VerificationSpec),v),
                   Anchor(evidence))
MD          = Atom(SP(dependency_metadata_changed),CH)
OCC(pat)    = Atom(SP(event_occurred),L(T(EventPattern),pat),Anchor(trace))
MATCH(pat,x)= Atom(SP(event_matches),L(T(EventPattern),pat),Var(x))
REFRESH_SCOPE(x) = Atom(SP(refresh_scope),Var(x))
REFRESH_OCC      = Atom(SP(refresh_occurred),Anchor(trace))

NET_ANY     = ANY_EVENT(EK(network_contact))
RELEASE_ANY = ANY_EVENT(EK(release))
MIGRATION   = PATH_IN(migration_paths)
SCHEMA_CHANGED = Not(OBS_EQ(schema_observation))
```

For the version-skew row, the external exact keys are
`LPI=(organization.policy,license)`, `LP0=(LPI,(0))`, `LP1=(LPI,(1))`,
`LDP0=(LP0,policy.declaration,license_check,PREDICATE)`, and
`LSP0=(LP0,policy.symbol,license_check,PREDICATE)`.  The row assumes the exact
`LDP0/LSP0` declaration, with signature
`(T(RepositorySnapshot),EvidenceStore)->Bool` and facets `({final},{evidence})`,
is present but its exact Sigma binding is absent,
while a fully usable display-similar declaration/binding at `LP1` is present.

<!-- K0-COVERAGE-BEGIN -->
| challenge | exact Contract pattern | plugin symbols and versions | declared facets/dependencies/evidence | lifecycle/status family | capability/trust premise | information preserved | forbidden shortcut |
|---|---|---|---|---|---|---|---|
| K0-C01 | `Require(TA(ts_win))` | `SF(snapshot_of)` and `SP(task_accepts)` at exact `CK`; exact typed literals | final/evidence; syntax roots plus `observe` and `verification_passed`; verification schema | declared, bound, discovered, invocable, exact `TRUTH_TRUE` or honest unknown/error | `CAP(functions)` and `CAP(predicates)` with request-scoped admitted `TR` | final behavioral acceptance and supporting evidence, independent of production | task label, fixture ID, fixed patch, or exact-output oracle |
| K0-C02 | `Require(OBS_EQ(public_request_observation))` | `SF(snapshot_of)`, `SF(observe)`, and `SP(observations_equal)` at exact `CK` | pre/final; exact observation/type dependencies; empty evidence | well formed/closed; decisive true or false after successful term evaluation, otherwise exact A2 evaluation error | exact function/predicate capabilities and admitted service-use targets | relation to the supplied baseline rather than a fixed final list | final-only expected outputs or ambient baseline read |
| K0-C03 | `Require(Not(OCC(NET_ANY)))` | `SP(event_occurred)`, lower `SP(event_matches)`, and `EK(network_contact)` at exact `CK` | trace only; exact event/pattern declarations; no implicit final inference | closed/evaluable; false on a matching admitted event, true on none, error only by exact contract | predicate capability/root; event Delta admission is independent | trace history despite equal final snapshots | infer no contact from final state or caller event-class flag |
| K0-C04 | only `Authorize(p,x,REFRESH_SCOPE(x),MD)` | `SP(refresh_scope)`, `SP(dependency_metadata_changed)`, `SF(changes_between)`, and `EK(dependency_refresh)` at exact `CK` | event variable plus pre/final guard; change-set dependencies; no occurrence requirement | grant scope/condition is decisive or errors; empty trace remains authorization-compliant | exact predicate capability/root; separately admitted authority adoption | conditional permission without duty | turn may into must or evaluability into authority |
| K0-C05 | `Contract(Hard={Require(Implies(MD,REFRESH_OCC))}, Grants={Authorize(p,x,REFRESH_SCOPE(x),MD)}, PairRequirements={PAIR(refresh)})` | exact `PAIR(refresh)` and its two members at `CK`, plus `SP(dependency_metadata_changed)` | pre/final guard and trace occurrence; pair/member/event/type roots; definitional T3/A1, no evidence shortcut | closed only with pair binding/model; four K1 truth cases preserved | predicate capability/root; pair meaning is Sigma, not service availability | conditional obligation and necessary authority | permission-only rewrite, unlinked occurrence atom, or formula-as-term |
| K0-C06 | `Authorize(p,x,MATCH(MIGRATION,x),SCHEMA_CHANGED)` | `SP(event_matches)`, `SF(snapshot_of)`, `SF(observe)`, `SP(observations_equal)`, and `EK(path_change)` at exact `CK` | event variable and pre/final guard; exact paths, observations, and event payload | authorization result only; no occurrence obligation | exact evaluator/root and admitted authority fact | semantic condition, path scope, and optionality | edit whenever condition holds, untyped path, or host path access |
| K0-C07 | `Require(Any({TA(ts_toml),TA(ts_yaml)}))` | `SP(task_accepts)` and `T(Format)` at exact `CK` | final/evidence; exact task and verification dependencies | T3 alternatives; true if one succeeds, unknown/error preserved | exact predicate/root; no choice service | multiple acceptable outcomes without advance selection | fixture order, default format, or requiring both |
| K0-C08 | K1 `Choice(storage,T(Format),{local,hosted},user,none)` using admitted typed values | exact `T(Format)@CK` and literal declarations; no predicate result | choice/type/literal/authority dependencies; no evidence truth | `WELL_FORMED+OPEN_BINDINGS`; source binding remains `UNRESOLVED`; no Eval | no evaluator premise; only exact `BIND_CHOICE` authority can close | controller-owned discretion | default, executor ownership, or factual unknown |
| K0-C09 | `Contract(Hard={Require(VP(full_suite))}, Grants={Authorize(p,x,MATCH(RELEASE_ANY,x),VP(full_suite))})` | `SP(verification_passed)` and `EK(release)` at exact `CK`; typed verification/pattern literals | evidence and trace; exact schema/ref/event dependencies | before evidence `TRUTH_UNKNOWN`; pass/fail gives decisive completion; schema fault gives error | predicate capability with admitted root; release authority remains separate | factual uncertainty versus discretionary choice | missing evidence as pass, chosen test result, or opaque success token |
| K0-C10 | `Require(All({TA(ts_logging),Not(TA(ts_logging))}))` | the same exact `SP(task_accepts)` occurrence and dependencies in both positions | exact atom facets/evidence retained; K1 structure proves contradiction after closure | `WELL_FORMED+CLOSED+CONSISTENCY_UNSAT` by K-CONTRA | no plugin reasoner required; binding/model closure still required | formation versus consistency | malformed classification, atom substitution, or plugin case branch |
| K0-C11 | `Require(All({TA(ts_nonempty),TA(ts_lt_100),TA(ts_ge_200)}))` over the exact `S_b` population | `SP(task_accepts)`, `T(ByteSize)`, `T(ArtifactSelector)`, and `CAP(bounds)` at exact `CK` | final/evidence plus exact complete bounds fragment and dependencies | admitted proof gives `CONSISTENCY_UNSAT`; absent/inapplicable proof gives `CONSISTENCY_UNKNOWN`; failure gives `REASONING_ERROR` | exact `{J_b}` target, admitted `TR`, sound complete-fragment certificate | plugin-visible numeric contradiction with unit/nonempty premise | numeric kernel rule or lack-of-proof as satisfiable |
| K0-C12 | `Require(All({TA(ts_universal_latency),TA(ts_universal_memory)}))` | same reusable `SP(task_accepts)` at exact `CK` with typed universal observation specs | final/evidence; declared universal domains; sampled evidence insufficient | closed and locally evaluable; no witness/proof gives `CONSISTENCY_UNKNOWN` | concrete evaluator may be available; no complete joint capability claimed | capability-limited unresolved judgment | sampled success as universal witness or binary default |
| K0-C13 | `Require(Atom(LSP0,RS(final),Anchor(evidence)))` | exact `LDP0/LSP0` declaration exists; exact old binding absent; distinct `LP1` records exist; `CK` does not replace either | syntax derives the old exact declaration/binding key; all new-version evidence/services are irrelevant | exact `DECLARED+BINDING_ABSENT+DISCOVERY_BLOCKED_BY_BINDING+INVOCATION_BLOCKED_BY_BINDING`; public `WELL_FORMED+OPEN_BINDINGS`, no truth; old-version service absence would be `EVALUABILITY_MISSING` only after binding | no compatibility claim or migration is admitted | mandated semantic version | latest/name-only substitution or coding broad predicate standing in for policy |
| K0-C14 | K1 `All({coding reproducibility atom, foreign licensing atom})` | exact `SP(task_accepts)@CK` plus a distinct foreign plugin key/version | union of both syntax/semantic roots, services, evidence, and trust scopes | representable; local evaluability may coexist with `CONSISTENCY_UNKNOWN` jointly | no exact joint environment target/certificate is declared | cross-plugin composition and shared dependency uncertainty | local-SAT conjunction, redefined `All`, or task-specific kernel branch |
| K0-C15 | `Require(TA(ts_rubric))` with finite typed rubric and declared verification records | `SP(task_accepts)` at exact `CK` with exact meaning/model/capability identity | final/evidence; lower observe/verification bindings; explicit access, unknown, error, schema contracts | closed; compatible rooted evaluator returns only exact bound `Eval` | `CAP(predicates)` exact binding target and admitted request root | useful reusable broad abstraction | gold Contract, challenge ID, expected decision, hidden evaluator context |
| K0-C16 | the identical `Require(TA(ts_rubric))`, but capability absent or `TR` unusable | identical exact `SP(task_accepts)` meaning at `CK` | same facets/dependencies/evidence contract as the preceding row | `CLOSED+EVALUABILITY_MISSING`; no truth request completion | intentionally no compatible root-qualified evaluator | denotation versus service availability | meaningless/true/false/satisfied from evaluator absence |
| K0-C17 | two attributed copies of the same coding formula; only the authenticated source has matching `Adopt`/authority fact | coding symbols unchanged; exact K2 `SourceRef`, `AuthorityRef`, `AuthorityFactKey` differ by source/adoption | proposition deps equal; origins and authority bindings distinct; authentication evidence is not truth evidence | both provenance records remain; only admitted adoption enters `Hard`/`Grants` | exact external authority validator/trust path, not coding evaluator | identical content with different source authority | normative wording or provenance as authority |
| K0-C18 | both phrasings bind to `Require(OBS_EQ(public_command_observation))` | exact same `observe`, `snapshot_of`, `observations_equal` keys/version | identical formula deps/facets/result function; distinct origins retained | internal `==Eval` proof supports formula/acceptance equivalence; full Contract equivalence may fail on origins | exact closed environments; evaluator error gives no relation | semantic equivalence without provenance erasure | phrase-indexed symbol or source-string equality |
| K0-C19 | `Contract(Hard={Require(OBS_EQ(adapter_client_observation)),Require(TA(ts_adapter))}, ProfileRequirements={PK(implementation_evidence)})` | exact coding meanings/profile at `CK` | pre/final/evidence, profile binding/dimensions, accepted abstract witness | witness may give `CONSISTENCY_SAT`; missing concrete dimension gives `PROFILE_INCOMPLETE` independently | admitted witness certificate and separate compatible profile checker | satisfiable abstract outcome versus concrete implementation evidence | no-known-patch as UNSAT or witness as patch/construction oracle |
<!-- K0-COVERAGE-END -->

Coverage count: **19** rows, one per accepted seed label.

### 7.2 Exactly eight complete worked traces

#### Worked trace 1 — final-state acceptance with evidence

1. Delta contains exact `T(TaskSpec)`, `T(RepositorySnapshot)`,
   `T(VerificationSpec)`, `T(VerificationRecord)`, `DF(snapshot_of)`,
   `DF(observe)`, and `DP(verification_passed/task_accepts)` declarations plus
   all recursively required type/literal declarations.  Declaration coordinates
   are `DECLARED`.
2. Sigma contains each exact binding, its complete ContractSpecs and model
   record.  K2 recomputes the two independent lower supports of
   `task_accepts`; all binding coordinates are `SEMANTICALLY_BOUND`, and the
   Contract is `CLOSED` after exact authority adoption.
3. Discovery under the exact semantic/trust environments finds
   `CAP(functions)` and `CAP(predicates)` with admitted `TR`; both requests
   reach `INVOCABLE_FOR` and therefore `EVALUABILITY_AVAILABLE`.
4. `FINAL` projects to supplied snapshot `F`.  Evidence store `E` contains a
   schema-valid passing platform record bound to `F`.  `observe` returns its
   exact result; `verification_passed` returns
   `VALUE(TRUE,{e_platform},{})`; `task_accepts` returns the exact A1-composed
   `VALUE(TRUE,{e_platform},{})`.
5. There are no controlled trace events.  `AuthEval=TRUE`, so final
   `AcceptEval=VALUE(TRUE,{e_platform},{})` and the public result is
   `TRUTH_TRUE({e_platform})`.  This establishes only acceptance of this
   supplied abstract outcome.

#### Worked trace 2 — pre/final preservation

1. Delta/Sigma/model records for `snapshot_of`, `observe`, and
   `observations_equal` are exact and closed; their capabilities and `TR` are
   admitted for one semantic environment.
2. The Contract uses one exact `ObservationSpec` literal and the preservation
   pattern from section 2.  Mechanical K1 dependencies include both functions,
   the predicate, plugin/type/literal declarations, and no caller list.
3. `PRE=P1` and `FINAL=F1` yield equal `ObservationResult` values while the
   snapshots may differ elsewhere; the predicate completes `TRUE` and the
   requirement accepts.
4. Holding `F1` and the observation spec fixed but changing `PRE=P2` so its
   selected result differs makes the predicate complete `FALSE`.  A fixed
   final-state check would not see this variation.  Term failure instead would
   project through A2 to `EVALUATION_ERROR`, not false.

#### Worked trace 3 — forbidden versus conditionally authorized events

1. Exact Delta event declarations classify network, path-change, release, and
   refresh events; the outcome cannot override their classes.  Exact pattern,
   match, occurrence, change, pair bindings, and model records close.
2. A network prohibition is a hard negated occurrence atom.  One admitted
   matching controlled event makes it false even if `FINAL` is unchanged.
3. A path-change permission is only an adopted `Authorize` grant.  With no
   occurrence, authorization compliance is vacuously true; no event is
   required.  An occurring matching event is compliant only for its actor and
   true guard.
4. For refresh, condition true plus empty trace makes permission true but the
   paired conditional requirement false.  Condition true plus one matching
   actor event makes both true.  Condition false plus event leaves the event
   unauthorized in both.  All guard/scope/occurrence metadata and errors are
   unioned under K1 A1; evaluator availability never supplies the grant.

#### Worked trace 4 — factual unknown and decisive completion

1. Exact verification and release declarations/bindings/models are closed.
   Predicate discovery is root-admitted and available; release authority is a
   separate exact adopted grant guarded by `verification_passed`.
2. With no compatible verification record, the predicate's exact meaning
   returns `VALUE(UNKNOWN,{}, {missing_full_suite})`.  This yields
   `TRUTH_UNKNOWN`; no `ChoiceDecl`, controller, or binding is created.
3. Add one schema-valid passing record and stable reference for the same spec
   and snapshot.  The same meaning now returns
   `VALUE(TRUE,{e_suite},{})`; a matching release event can be authorized.
4. A decisive failing record instead returns false.  A conflicting or
   malformed record returns `Eval.ERROR` and therefore `EVALUATION_ERROR` with
   no truth.  Missing evidence, failure evidence, and evaluator failure remain
   distinct.

#### Worked trace 5 — plugin contradiction versus capability-limited unknown

1. Three exact `task_accepts` atoms share one snapshot and selector: nonempty,
   every size below 100 KiB, and every size at least 200 KiB.  Delta/Sigma,
   literals, model contracts, complete dependencies, and Contract closure all
   validate.
2. `CAP(bounds)` is discovered at the exact joint environment target, its
   admitted root covers the whole subject, and the request lies in its complete
   fragment.  An admitted sound contradiction certificate including the
   nonempty premise gives `CONSISTENCY_UNSAT`.
3. Replace the subject with two universal workload criteria outside the bounds
   fragment.  Local concrete evaluations do not provide a universal shared
   witness and no other joint capability exists.  The exact result is
   `CONSISTENCY_UNKNOWN`, possibly alongside `EVALUABILITY_MISSING` for joint
   reasoning.
4. If the admitted reasoner invocation fails, the result is
   `REASONING_ERROR` and no consistency conclusion for that invocation.  Lack
   of proof never becomes SAT.

#### Worked trace 6 — exact version mismatch with no fallback

1. A Contract syntax occurrence names an exact policy predicate owned by
   plugin version `(0)`.  K1 dependency extraction retains that exact plugin,
   declaration, symbol, and literal identity.
2. Variant A lacks the exact `(0)` declaration: the lifecycle is
   `DECLARATION_INVALID`, then binding/discovery/invocation blocked, and the
   Contract is malformed.
3. Variant B has the exact declaration but lacks its meaning: it is
   `DECLARED+BINDING_ABSENT`, then discovery/invocation blocked, and the
   Contract is well formed but open.
4. A display-similar fully usable version `(1)` is a distinct key in both
   variants.  It cannot change either lifecycle.  No alias, compatibility
   claim, or admitted migration is present; therefore there is no fallback and
   no truth result.

#### Worked trace 7 — broad predicate with and without an evaluator

1. One finite `TaskSpec` and the exact `task_accepts` declaration, meaning,
   access/evidence/unknown/error contracts, lower dependencies, and model
   record form a closed semantic environment.  No challenge label or expected
   result occurs in any record.
2. Under an exact admitted service-use root, `CAP(predicates)` targets that
   binding and the request reaches `INVOCABLE_FOR`.  The service receives only
   task, supplied final snapshot, evidence store, and the two declared lower
   observation results.  Exact complete result equality is required.
3. In the controlled environment with the same semantic binding but an absent
   or incompatible root, binding remains `SEMANTICALLY_BOUND` and the Contract
   remains `CLOSED`; discovery yields capability incompatible/absent,
   `EVALUABILITY_MISSING`, and no truth result.
4. An attempted hidden repository, expected-answer, authority, choice, or
   service-state observation violates the K2 role matrix/access contract and
   is malformed or an evaluation error.  Broadness never grants privileged
   access.

#### Worked trace 8 — provenance, authority, and abstract satisfiability

1. Two exact `SourceRef` records carry identical preservation/task formula
   content.  Both remain in `Origins`; only one has an independently admitted
   `AuthorityFactBinding` matching its source, principal, and `REQUIRE` role.
   Only that adoption enters `Hard`.  Coding predicate evaluation is not used
   to admit either authority fact.
2. The adopted closed Contract also requires the exact
   `PK(implementation_evidence)` profile.  An admitted abstract `Outcome`
   witness uses the Contract-derived `chi_C`, makes preservation and task atoms
   true with accepted evidence, and establishes `CONSISTENCY_SAT`.
3. The profile checker finds the abstract-acceptance dimension but a known
   omission of concrete-implementation evidence, yielding
   `PROFILE_INCOMPLETE`.  Both statuses coexist.
4. The unadopted quoted source remains provenance only.  Neither the satisfying
   witness nor the profile result identifies a patch, build, action sequence,
   repository transition, or implementation.

Trace count: **8** complete worked traces.

## 8. Relative minimality and separating cases

### 8.1 Exhaustive responsibility/minimality ledger

This ledger covers every coding-specific record family and every exact field
introduced above.  Grouped dot-qualified fields receive the displayed
disposition independently and occur in no other row.  K2 carrier fields not
introduced by the coding plugin retain their K2 disposition.

<!-- K3S-LEDGER-BEGIN -->
| Record or exact fields | Disposition | Owner | Semantic role / signature and facets | Dependencies | Evidence/access/failure boundary | Identity/version and omission | Consumer | seed cases | separating pair |
|---|---|---|---|---|---|---|---|---|---|
| all `TypeDeclaration.{key,admitted_value_domain,proper_declaration_dependencies}` rows in section 3 | `RETAINED_DELTA` | `CK` Delta | typed value admission for every closed value sort | exact nested type-admission DAG | no truth/service; rejected value is malformed in use | exact `T(n)@(1)`; absence malformed | literal, signature, event, value admission | C01,C02,C07,C11 | K3S-A05: typed path/content/snapshot versus an untyped map |
| every `LiteralDeclaration.{key,literal_identity,result_type,proper_declaration_dependencies}` instance | `RETAINED_DELTA` | `CK` Delta | exact typed Contract constant | exact result type | no evidence or service | structural `L(T,v)@(1)`; absence malformed | K1 `Lit`, literal binding | C07,C08,C15 | K3S-A03: declaration presence versus binding/service absence |
| three `FunctionDeclaration` complete field sets | `RETAINED_DELTA` | `CK` Delta | exact ordered signatures and pre/final facet positions | argument/result types | no meaning/service in Delta | exact `DF/SF@(1)`; absence malformed | terms/predicates | C01,C02,C19 | K3S-A04: final-only versus pre/final support |
| eight `PredicateDeclaration` complete field sets, including the pair-owned occurrence declaration | `RETAINED_DELTA` | `CK` Delta | exact Boolean signatures/facets | argument types | no meaning/service in Delta | exact `DP/SP@(1)`; absence malformed | atoms/grants/reasoning | C01-C07,C09,C11,C15 | K3S-A01 and A09: kind/owner identity and reusable evaluator boundary |
| six `EventDeclaration.{key,event_key,payload_type,event_class,proper_declaration_dependencies}` records | `RETAINED_DELTA` | `CK` Delta | typed immutable observational/controlled event classes | payload types | no caller class or authority | exact `DE/EK@(1)`; absence/ill type malformed | Outcome admission/AuthEval | C03-C06,C09 | K3S-A06: forbidden event versus authorized event |
| `EventScopePairDeclaration` complete fields for `PAIR(refresh)` | `RETAINED_DELTA` | `CK` Delta | exact unary scope/trace pair and controlled set | members/events/types | no meaning/proof in Delta | exact pair `(1)`; absence malformed | conditional requirement | C04,C05 | K3S-A07: permission versus obligation |
| each literal `SemanticBinding` complete field set | `RETAINED_SIGMA` | `CK` Sigma | exact `TERM_VALUE(v)` meaning | declaration plus ContractSpecs | empty evidence/access; N/A unknown | binding key derived; absence open | literal evaluation/model | C07,C08,C15 | K3S-A03: declaration is not binding |
| three function `SemanticBinding` complete field sets | `RETAINED_SIGMA` | `CK` Sigma | deterministic `TermResult` meanings | declaration/spec/support closure | typed positions only; term errors | exact binding `(1)`; absence open | term evaluator | C01,C02,C19 | K3S-A05: supplied snapshot projection versus ambient repository |
| seven ordinary predicate `SemanticBinding` complete field sets | `RETAINED_SIGMA` | `CK` Sigma | reusable exact `Eval` meanings | declarations/specs/lower bindings | explicit schemas/access/unknown/error | exact binding `(1)`; absence open | atom evaluator | C01-C07,C09,C11,C15,C16 | K3S-A09 and A10: same meaning with/without evaluator; false/unknown/errors |
| `EventPairBinding` and pair-owned `OccurrenceBindingProjection` fields | `RETAINED_SIGMA` | `CK` Sigma | definitional T3/A1 full-`Eval` refresh occurrence | pair/scope/model/lift specs | exact union/error behavior; no separate occurrence binding | exact pair `(1)`; absence open; duplicate ordinary binding conflicts | conditional trace formula | C04,C05 | K3S-A15: semantic proper support versus validation machinery |
| `ProfileBinding` complete fields and two `ProfileDimensionKey`s | `RETAINED_SIGMA` | `CK` Sigma | implementation-evidence coverage only | task predicate and evidence schema | profile unknown/evaluation/reasoning errors exact | exact `PK@(1)`; absence open | profile checker | C19 | K3S-A18: abstract SAT versus concrete evidence |
| Delta type-admission `ContractSpec` complete fields | `RETAINED_DELTA` | `CK` Delta | exact admitted domains | extensional nested supports | no trust/service/semantic side channel | exact `CS(TYPE_ADMISSION,...)@(1)`; absence declaration-malformed | value admission | C01,C07,C11 | K3S-A05: typed admission versus universal map |
| Sigma meaning `ContractSpec` complete fields | `RETAINED_SIGMA` | `CK` Sigma | exact function/predicate/occurrence/profile relations | exact lower observations | only explicit primary inputs | exact role/key `(1)`; absence binding-incompatible/open | binding/result validator | C01-C19 | K3S-A09 and A17: reusable meaning versus phrase/expected mapping |
| evidence-schema and access-boundary `ContractSpec` complete fields | `RETAINED_SIGMA` | `CK` Sigma | schema admission and positional access | typed record/lower-result support | evidence distinct from truth; undeclared access errors | exact role/key `(1)`; absence incompatible | evaluator/model contract | C01,C09,C15 | K3S-A05 and A10: explicit evidence/access versus hidden input |
| unknown/evaluation/reasoning-error `ContractSpec` complete fields | `RETAINED_SIGMA` | `CK` Sigma | honest unknown and disjoint failure relations | no hidden support | nonempty typed reasons; no cross-family conversion | exact role/key `(1)`; absence incompatible | result/status boundary | C09,C12,C15 | K3S-A10: false/unknown/evaluation/reasoning error |
| ordinary binding `ModelContract` and `ModelCapabilitySummary` complete fields | `RETAINED_SIGMA` | `CK` Sigma/model projection | exact machine/model identity | binding contracts and descriptors | prose diagnostic only | exact `MC(target,...,(1))`; absence model-open, mismatch malformed | compiler/model-facing lookup | C13,C15,C16 | K3S-A16: model/machine mismatch |
| pair occurrence `ModelContract` complete fields | `RETAINED_SIGMA` | `CK` Sigma/model projection | exact occurrence projection identity | pair-owned binding and descriptor summaries | same evidence/unknown/error specs | producer-named `(1)` key; no inferred document identity | pair/model lookup | C05 | K3S-A16: same prose with different semantic identity |
| verification `EvidenceRef` identity fields and `VerificationRecord` schema relation | `RETAINED_SIGMA` | K1 carrier / `CK` Sigma schema | stable support identity, not truth | exact spec/snapshot/schema | pass/fail/inconclusive interpreted only by meaning | issuer/schema/version exact; missing evidence yields unknown | verification/task predicates | C01,C09,C15 | K3S-A08 and A10: factual evidence versus choice/truth/failure |
| Service-layer sound/complete-fragment, required-evidence, and failure `ContractSpec` complete fields | `RETAINED_SERVICE` | `CK` Service | exact capability fragments and role-specific request/failure boundaries | target observations and complete closures only | certificate/evidence premises never become denotation or truth | exact `CS` role/key `(1)`; absence makes descriptor incompatible | capability discovery/invocation | C01,C09,C11,C19 | K3S-A10 and A11: logical result versus service failure; in-fragment proof versus unresolved claim |
| `CapabilityDescriptor` fields for `CAP(functions)` | `RETAINED_SERVICE` | `CK` Service | concrete exact function targets | complete target closures | required evidence/root/failure contracts | exact service/capability `(1)`; absence evaluability-missing | function requests | C01,C02 | K3S-A03: meaning bound while capability absent |
| `CapabilityDescriptor` fields for `CAP(predicates)` | `RETAINED_SERVICE` | `CK` Service | concrete exact predicate targets | complete target/lower closures | exact root and evaluation failure | exact service/capability `(1)`; no fallback | predicate requests | C01-C07,C09,C15,C16 | K3S-A09: same meaning with/without compatible evaluator |
| `CapabilityDescriptor` fields for `CAP(profile)` | `RETAINED_SERVICE` | `CK` Service | concrete exact profile target | coverage subject/dependencies | profile result/failure families | exact service/capability `(1)`; absence no profile result | profile request | C19 | K3S-A18: SAT versus profile coverage |
| `CapabilityDescriptor` fields for `CAP(bounds)` | `RETAINED_SERVICE` | `CK` Service | complete exact named bounds fragment | whole closed conjunction | admitted proof or reasoning error; no wider claim | exact environment target `(1)`; absence logical unknown | consistency request | C11,C12,C14 | K3S-A11 and A12: visible contradiction versus unresolved/local-only |
| `TrustEnvironment`, `TrustRootRecord/Judgment`, exact `TP/TR` service-use fields | `RETAINED_SERVICE` | embedding policy | request-specific external service trust | full subject producer set | admitted/absent/undecided/incompatible/failed separate | exact policy/root `(1)`; omission root-absent | discovery/invocation | C01,C11,C15,C16 | K3S-A03 and A13: trust/provenance/authority remain separate |
| `ChangeSet` value for a supplied snapshot pair | `DERIVED` | `CK` function meaning | exact extensional difference relation | both snapshots | no event/plan/evidence | identity is complete derived map | scope/metadata predicates | C02,C04-C06 | K3S-A05: change relation versus path/content/ambient access |
| `ObservationResult` values from `observe` | `DERIVED` | `CK` function meaning | typed projection | spec and supplied snapshot | no truth; term error on domain failure | complete structural result equality | preservation/task predicate | C01,C02,C18 | K3S-A04: fixed final result versus pre/final relation |
| K1 readable goal/preserve/forbid/allow/conditional/alternative patterns | `DERIVED` | K1 | exact macro/composition semantics | underlying exact syntax deps | K1 T1-T4/A1-A2 | no independent key/version | Contracts | C01-C07,C09 | K3S-A06-A08: normative and uncertainty separations |
| K2 binding keys, supports, closures, observation maps, model summaries, lifecycle coordinates, service identity, and validation-reference sets | `DERIVED` | K2 | mechanical exact projections | complete structural graph | owner-specific missing/error statuses | cannot be supplied or omitted | every validator | C01-C19 | K3S-A03,A14,A15: lifecycle/duplicate/dependency distinctions |
| alternate independent-pair proof certificate/validator roots used only by the section 9 conformance fixture | `DERIVED` | K2 validation | exact non-proper `ValidationReference` projection | alternate pair record and operation roots | certificate/trust failures prove nothing | exact fixture keys; never a new coding primitive | dependency-boundary check | C05 | K3S-A15: mandatory validation reference versus proper edge |
| change set as patch/action sequence; event payload as executable command/endpoint | `EXCLUDED` | none | no declarative denotation | none | presence violates access boundary | never an identity | none | C03-C06,C19 | K3S-A18: satisfying semantics without implementation |
| universal string/map/opaque handle for path, task, evidence, result, or expected answer | `EXCLUDED` | none | destroys typed distinction | none | presence malformed/oracular | never an identity | none | C01,C02,C09,C15 | K3S-A05,A17: typed reusable values versus escape hatch |
| task taxonomy, phrase-indexed symbols, challenge IDs, expected mappings, gold Contracts/patches | `EXCLUDED` | none | no semantic role | none | presence rejects | never an identity | none | C01,C15,C18 | K3S-A17: equivalent phrasing shares symbols |
| implicit version/name/order fallback, plugin-owned truth/authority/choice/connective/failure rule | `EXCLUDED` | none | owned by K1/K2 or invalid | none | fail loud in owning family | never an identity | none | C04,C08,C10,C13,C17 | K3S-A01,A02,A13: exact identity and ownership |
| implementation, parser, binder, planner, executor, repository/filesystem/network operation, model/prompt/benchmark | `EXCLUDED` | none | outside K3-S | none | no semantic result | never an identity | none | C01-C19 | K3S-A18: abstract outcome is not construction |
<!-- K3S-LEDGER-END -->

Ledger count: **34** rows: 7 `RETAINED_DELTA`, 11 `RETAINED_SIGMA`,
6 `RETAINED_SERVICE`, 5 `DERIVED`, and 5 `EXCLUDED`.

### 8.2 Exactly eighteen adversarial cases

Case identifiers below are conformance labels only; no meaning, evaluator,
request, result, certificate, or evidence record receives them.

<!-- K3S-CASES-BEGIN -->
| case | abstract inputs | exact records | expected status family | information lost by conflation | forbidden shortcut |
|---|---|---|---|---|---|
| K3S-A01 | display-equal local atom under `CK`, foreign owner/plugin, and function versus predicate kinds | independently constructed `PluginKey`, `DeclarationKey`, `SymbolKey` records | different owners/kinds coexist; forcing unequal kinds under one exact key is malformed conflict | owner, plugin, namespace, and declaration kind | display/name equality, shadowing, or one kind cast to another |
| K3S-A02 | exact coding key at `(1)` and display-similar `(2)` with no admitted migration | old/new declarations, bindings, model records, targets | requested `(1)` remains missing/open/evaluability-missing as applicable; `(2)` never substitutes | exact meaning and model/machine version | latest, compatible-looking, first-found, or alias-as-migration |
| K3S-A03 | predicate declaration present; variants omit binding, capability, or admitted root | declaration, semantic/model records, descriptor, TrustEnvironment, lifecycle | `DECLARED+BINDING_ABSENT`; or bound+capability absent/incompatible; or fully invocable | formation, denotation, availability, and trust | let a service create meaning, let meaning create service, or root listing imply admission |
| K3S-A04 | equal final observations under one baseline, unequal under another | state projection, observe, equality bindings and two Outcomes | final-state atom unchanged; pre/final preservation changes truth | relation to baseline versus fixed final property | replace PRE with a manifest/fixed result |
| K3S-A05 | canonical path/content snapshots, extensional change set, and attempted undeclared host read | type declarations, three function bindings, access ContractSpecs | typed values/derived relation conform; undeclared access is malformed or evaluation error | path identity, content, scope, supplied state, and ambient state | untyped string/map, host normalization, filesystem read, or change plan |
| K3S-A06 | same trace has a forbidden network event and a separately granted path event | event declarations, occurrence/match bindings, hard clause and grant | prohibition false; path event authorization independently true/false/unknown/error | hard trace condition versus event authority | absent grant as prohibition or evaluability as authorization |
| K3S-A07 | condition true with refresh event absent | exact pair, grant-only Contract, and grant-plus-requirement Contract | permission accepts omission; conditional obligation rejects omission | permission versus requirement | convert may to must or omit the paired hard occurrence clause |
| K3S-A08 | open controller-owned format choice and closed missing-suite fact | `ChoiceDecl`/authority records versus verification predicate/evidence schema | `OPEN_BINDINGS/UNRESOLVED` versus `TRUTH_UNKNOWN` | discretion/controller versus factual uncertainty | default choice, let evidence bind choice, or let principal choose fact |
| K3S-A09 | identical exact broad meaning/model; one environment has a compatible rooted evaluator, one does not | task binding, model record, capability/TrustEnvironment/lifecycle | both semantically bound/closed; available versus `EVALUABILITY_MISSING` | denotation versus evaluator availability | call unevaluable meaning meaningless/satisfied or add expected mapping |
| K3S-A10 | exact results `FALSE`, `UNKNOWN`, `Eval.ERROR`, reasoner failure, and shape-valid unequal result | Eval/ReasoningResult/InterfaceFailure records | distinct truth, evaluation-error, reasoning-error, and malformed-result families | logical falsity, ignorance, evaluator fault, reasoner fault, protocol mismatch | false/unknown/error conversion or shape-only result acceptance |
| K3S-A11 | nonempty bundle with incompatible exact byte bounds; variant outside bounds fragment | task atoms, bounds capability target, certificate/request | admitted in-fragment proof gives UNSAT; otherwise consistency unknown; failure gives reasoning error | proved domain contradiction versus unresolved conflict | numeric kernel branch or absence of proof as SAT/UNSAT |
| K3S-A12 | coding reproducibility and foreign licensing constraints with only local services | two exact plugin environments and local targets versus one absent joint target | local results may coexist; joint consistency remains unknown and joint evaluability missing | local soundness versus joint shared witness/proof | conjoin local SAT/certificates or let one plugin redefine K1 `All` |
| K3S-A13 | identical formula content from authenticated and untrusted quoted `SourceRef`s | origins, authority candidate/admission/binding, trust records | both provenance values retained; only admitted exact adoption is normative | content, provenance, authentication, and authority | normative wording, content equality, evidence, or trust root as adoption |
| K3S-A14 | independently constructed equal package records and unequal records at one key, in reversed input orders | declarations/bindings/model/descriptors and `ConflictRef` | equal duplicates coalesce; unequal same-key records conflict identically for all orders | logical equality versus conflicting semantics | last/first writer wins, registration order, or diagnostic equality |
| K3S-A15 | pair semantic DAG plus non-proper certificate/validator references; variant adds genuine semantic back-edge | pair/bundle/DependencyEnvironment/ValidationReference records | validation refs remain mandatory and non-traversed; genuine proper cycle is malformed | semantic meaning support versus validation admission binding | delete required reference, turn it into proper edge, or ignore true cycle |
| K3S-A16 | model record at exact key points to old signature/meaning or foreign capability summary | binding, ModelContract, descriptor/summary records | exact record conforms; mismatch malformed; absent record model-open | compiler-visible contract versus machine meaning | trust prose/alias, partial projection, or document-version inference |
| K3S-A17 | two equivalent preservation phrasings and an attempted task-label/fixture-specific atom | identical general formula bindings with distinct origins; excluded atom attempt | general bindings support equivalence; phrase/case-indexed vocabulary is nonconformant | surface language versus extensional meaning | task taxonomy, phrase atom, challenge branch, expected output |
| K3S-A18 | admitted abstract satisfying Outcome with no concrete implementation evidence | witness certificate, task/preservation meanings, implementation-evidence profile | `CONSISTENCY_SAT` may coexist with `PROFILE_INCOMPLETE`; no patch result | semantic existence versus construction/buildability | witness as patch/plan, missing patch as UNSAT, or execution claim |
<!-- K3S-CASES-END -->

Case count: **18**, in the required order.

## 9. K3-X semantic input boundary

### 9.1 Smallest finite semantic packet

This section freezes semantic inputs only.  It does not select a language,
module, representation, path, command, output directory, test framework, or
implementation technique.

The smallest K3-S subset needed by the thirteen accepted executable checks is:

- Delta types `T(Path)`, `T(PathSet)`, `T(ArtifactContent)`,
  `T(RepositorySnapshot)`, `T(ChangeSet)`, `T(ObservationSpec)`,
  `T(ObservationResult)`, `T(ArtifactSelector)`, `T(ByteSize)`,
  `T(Format)`, `T(ObservationRelation)`,
  `T(VerificationSpec)`, `T(VerificationRecord)`, `T(Criterion)`,
  `T(TaskSpec)`, `T(EventPattern)`, `T(NetworkContactEventPayload)`,
  `T(ReleaseEventPayload)`, and `T(DependencyRefreshEventPayload)`, plus only
  the exact finite literal declarations used by fixtures;
- all three function declarations/bindings and all eight predicate declarations
  needed to close the exact `CAP(functions)` and `CAP(predicates)` target sets;
  this includes the seven ordinary predicate bindings and the pair-owned
  `DP(refresh_occurred)` projection, their ContractSpecs, dependency closures,
  and complete model contracts;
- `DE(network_contact)`, `DE(release)`, `DE(dependency_refresh)`, their exact
  EventKeys/classes/payloads, and `PAIR(refresh)` with its retained definitional
  binding;
- `CAP(functions)`, `CAP(predicates)`, and `CAP(bounds)`; exact request-scoped
  `TP`, `TR`, `TrustEnvironment` judgments; `CS(EVIDENCE_SCHEMA,verification)`;
  stable verification EvidenceRefs and all exact K2 request/result/failure
  carriers reachable from these records;
- K1/K2 statuses `WELL_FORMED`, `MALFORMED`, `CLOSED`, `OPEN_BINDINGS`, the
  three evaluability outcomes, `TRUTH_TRUE/FALSE/UNKNOWN`,
  `EVALUATION_ERROR`, `CONSISTENCY_SAT/UNSAT/UNKNOWN`, `REASONING_ERROR`, and
  the four complete lifecycle coordinates.

One conformance-only alternate fixture replaces, in a separate environment,
the retained definitional `EventPairBinding` by a complete K2
`INDEPENDENT_COHERENCE_PROOF` for the same exact pair semantics.  It uses

```text
PVK  = ((capknow.audit,pair-validator),(1))
PVSK = (PVK,coding.validation,refresh,(1),PAIR_VALIDATION)
PVC  = (PVSK,refresh_full_eval)
PVCERT = (PLUGIN_CERTIFICATE_ISSUER(PVK),coding.certificate,refresh_coherence)
```

and an exact admitted `TR` scoped independently to validator service use and
pair-certificate admission.  The alternate pair record derives mandatory
`VALIDATION_CERTIFICATE(PVCERT)` and `VALIDATION_CAPABILITY(PVC)` entries while
its semantic proper DAG excludes them.  The validator/certificate/trust
records are generic K2 conformance carriers, not new coding types, atoms,
truths, or production meanings.  The two pair-binding variants are never
composed, so their same-key inequality is not hidden.

All fixture values are finite logical values: abstract segments/content,
snapshots, task/verification specs, EvidenceRefs, event payloads, exact keys,
root judgments, and result records.  They contain no host path, real command,
network endpoint, repository, expected patch, hidden answer, or challenge ID.

### 9.2 Mapping of all thirteen checks

| amendment check | K3-S symbols/records | adversarial cases | exact K1/K2 clauses and required outcome |
|---:|---|---|---|
| 1 | `snapshot_of`, `observe`, `verification_passed`, `task_accepts`, final snapshot/evidence fixtures | K3S-A04,A09,A10 | K1 §§2.3,3.1-3.2,4; K2 §§2.4,4.1-4.2,5.1-5.2: well formed, closed, evaluable, exact `TRUTH_TRUE` |
| 2 | exact `CK/T/DF/DP/SF/SP` constructors with independently built equal records and one forced kind collision | K3S-A01,A14 | K2 §§3.1,8.3: equal identities coalesce; owner/plugin/kind variants remain distinct; one-key unequal kind rejects |
| 3 | identical logical meaning at exact `(1)` and an exact `(2)` target | K3S-A02,A16 | K1 §§2.3,3.5; K2 §§3.4,4.3,8.2: agreement succeeds, mismatch rejects, no fallback |
| 4 | `DP(task_accepts)` declaration; environments omitting its binding or `CAP(predicates)` | K3S-A03,A09 | K1 §2.3; K2 §§2.4,8.1: declaration present/binding absent/capability absent are distinct coordinates |
| 5 | retained pair DAG plus the separate alternate proof fixture and a variant with a true proper back-edge | K3S-A15 | K2 §§3.3,7.2: validation refs exact/non-proper; genuine semantic self-edge/cycle malformed |
| 6 | five exact `TrustEnvironment.root_judgments` for `TR` on one predicate request | K3S-A03,A13 | K2 §§2.3-2.4,5.4,8.1: admitted -> usable; absent -> exact missing/evaluability missing; undecided -> evaluability unknown; incompatible -> evaluability missing; failed -> exact discovery failure and no fabricated K1 result |
| 7 | task result fixtures, malformed unequal Eval, and bounds-reasoner result/failure | K3S-A10,A11 | K1 §§4,5.3; K2 §§5.2-5.4,6.3: false, logical unknown, evaluation error, reasoning error, malformed result stay distinct |
| 8 | network prohibition and exact release/refresh grants/pair | K3S-A06,A07 | K1 §§3.2-3.4; K2 §7.1: hard trace truth and authority are independent; evaluability grants no authority |
| 9 | `task_accepts` support on independent `observe` and `verification_passed` lower nodes; finite sets/packages in two permutations | K3S-A09,A14,A15 | K2 §§1.1,3.3,7.5,8.3: at least two topological orders yield identical complete maps/statuses; package/record permutations do likewise |
| 10 | equal duplicate declarations/bindings/models and one unequal same-key variant in reversed order | K3S-A14 | K2 §§1.1,8.3: equality coalesces and conflict is order-independent |
| 11 | omit in turn `DECLARATION`, `BINDING`, `MODEL_CONTRACT`, `CAPABILITY`, `TRUST_ROOT`, `CERTIFICATE`, and selected carrier/result | K3S-A03,A15,A16 | K2 §3.3 `missingStatus` and §2.4 lifecycle: each exact record kind yields only its specified missing family |
| 12 | the entire finite packet and every derived identity/result map | K3S-A14 | K1 §4.8; K2 §§1.1,3.3,5.2: exact finite equality, deterministic meanings, set semantics, and source binding permit replay only after the later clean-commit gate |
| 13 | task predicate variant requesting ambient repository/evidence/expected-answer state | K3S-A05,A09,A17 | K1 §§1.2,2.2,3.1; K2 §§3.3,4.2,5.1: invalid observation/access is rejected before a truth can be used |

### 9.3 Intentionally excluded executable branches

The finite slice intentionally omits every retained K3-S type, function,
predicate, event, profile, or capability not enumerated in section 9.1,
including concrete profile checking, path-scope/dependency-change evaluation,
command/test/path-change event payload branches, migration, compatibility,
semantic extensions, aliases, authority admission, general cross-plugin joint
reasoning, public relation services, independent non-pair certificate kinds,
and every K2 branch not required by the thirteen checks.  It also omits byte
serialization, discovery transport, real repository state, real commands,
network activity, concurrency, retry behavior, planning, mutation, and models.
Omission from this finite slice is not a semantic rejection of K2 or K3-S.

Two provenance gates remain mandatory and distinct.  A future mutation
handoff may bind only an accepted clean semantic base and explicitly allowed
mutation paths; it cannot name a not-yet-created implementation commit.  A
later execution binding may name only a frozen, reviewed, clean implementation
commit and its exact committed finite fixtures.  Diagnostic developer runs
before that second gate cannot support acceptance evidence.

If two conforming implementations of this packet could produce different
K1/K2/K3-S judgments because the semantics do not determine the result, later
work stops and returns the ambiguity to K2 or K3-S.  This section grants no
implementation or execution authority.

## 10. K3-S acceptance checklist

- [x] Exactly ten required top-level sections appear in the required order.
- [x] One minimal coding-vocabulary decision is explicit; every retained value,
  declaration, meaning, service, profile, event, evidence schema, and model
  contract has an exact K2 identity, layer, signature, version, dependency,
  access, evidence, unknown, error, omission, duplicate, and conflict rule.
- [x] Paths, snapshots, contents, observations, changes, trace events, and
  verification records are typed logical values with no ambient access;
  `ChangeSet` is an extensional snapshot relation and never an action plan.
- [x] `task_accepts` has a finite typed `TaskSpec`, reusable denotation,
  explicit outcome/evidence scope, exact lower dependencies, capability
  fragment, and honest unknown/error behavior; meaning without a compatible
  evaluator remains closed but unevaluable.
- [x] K1 requirements, authorization, choices, provenance, authority, truth,
  errors, consistency, relations, profiles, and aggregation are unchanged.
- [x] Declaration, binding, model contract, capability, trust, and evidence
  availability remain independent, and exact K2 lifecycle coordinates are
  total.
- [x] Plugin contradiction is admitted only in the exact bounds fragment;
  unsupported, incomplete, or cross-plugin joint claims remain logically
  unknown absent the matching capability, while service failure is reasoning
  error.
- [x] Exact identity/version, no-fallback, model/machine equality,
  dependency/validation separation, duplicate, conflict, and migration rules
  preserve K2.
- [x] The section 7 coverage table has exactly one row for each of the 19 seed
  challenges; no ad hoc atom forces success.
- [x] The section 8 ledger is exhaustive under its grouping convention; every
  retained row cites a separating adversarial case, and derived/excluded items
  acquire no independent primitive semantics.
- [x] Exactly 18 ordered adversarial cases and exactly eight complete worked
  traces derive from general rules; their identifiers are never semantic
  inputs.
- [x] The section 9 semantic packet covers all thirteen accepted executable
  checks with finite logical values, names the excluded branches, preserves
  both provenance gates, and freezes no implementation detail or authority.
- [x] Abstract satisfiability and profile coverage imply no patch, build,
  planner, executor, repository operation, or concrete implementation.
- [x] Conclusions remain limited to accepted-seed semantic representability.
  No held-out content, implementation, command/model execution, benchmark,
  external artifact, downstream handoff/path, or downstream authority appears.

No K3-S stop condition was encountered.  The exact K1 and K2 records suffice;
no frozen kernel or ABI rule is reinterpreted or repaired here.
