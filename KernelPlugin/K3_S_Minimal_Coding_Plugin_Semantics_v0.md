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

### 2.1 Exhaustive finite value algebra

All collections are finite.  Set and map equality is extensional; sequence
equality is positional; record equality is field equality; and values with
different constructor tags are unequal.  Every atom below is an exact logical
atom in its displayed sort, never an untyped string or an encoding.  Every
displayed `*_atom` field is admitted exactly when it is nonempty, and equality
is exact within that one sort; no atom is coerced across sorts.

```text
PathSegment = SEGMENT(segment_atom)
Path        = PATH(nonempty sequence(PathSegment))
PathSet     = finite set(Path)

ArtifactRole = SOURCE | DEPENDENCY_METADATA | DEPENDENCY_LOCK | MIGRATION |
               BUNDLE | CONFIGURATION | PUBLIC_SCHEMA |
               OTHER_ROLE(role_atom)
Format       = TOML | YAML | JSON | TEXT | BINARY |
               OTHER_FORMAT(format_atom)
StorageBackend = LOCAL_STORAGE | HOSTED_STORAGE
ByteSize      = KIB(nonnegative integer)
ContentIdentity = CONTENT_ID(content_atom)
FieldId       = FIELD(field_atom)
FieldValue    = BOOL_VALUE(Bool) | INT_VALUE(integer) |
                ATOM_VALUE(field_value_atom)
BehaviorValue = BEHAVIOR_ACCEPTED | BEHAVIOR_REJECTED |
                BEHAVIOR_METRIC(integer) |
                BEHAVIOR_RESOLUTION(ContentIdentity) |
                BEHAVIOR_CORRESPONDENCE(
                  finite map(FieldId -> FieldValue),
                  finite map(FieldId -> FieldValue))
ArtifactBody =
    TEXT_BODY(ContentIdentity)
  | STRUCTURED_BODY(finite map(FieldId -> FieldValue))
  | OPAQUE_BODY(ContentIdentity)
  | BEHAVIOR_BODY(finite map(SubjectId -> BehaviorValue))

ArtifactContent =
    TEXT_ARTIFACT(role : ArtifactRole, format : Format,
                  size : ByteSize, content : ContentIdentity)
  | STRUCTURED_ARTIFACT(role : ArtifactRole, format : Format,
                        size : ByteSize,
                        fields : finite map(FieldId -> FieldValue))
  | OPAQUE_ARTIFACT(role : ArtifactRole, format : Format,
                    size : ByteSize, content : ContentIdentity)
  | BEHAVIOR_ARTIFACT(role : ArtifactRole, format : Format,
                      size : ByteSize,
                      observations : finite map(SubjectId -> BehaviorValue))
```

`SEGMENT(a)` is admitted iff `a` is nonempty and is neither `.` nor `..`.
`PATH(s)` is admitted iff `s` is nonempty and every member is admitted.  No
slash, backslash, host root, current directory, case fold, symlink, Unicode
rewrite, or other host convention participates.  Thus canonicalization is
exactly admission and path equality is sequence equality.  `OTHER_ROLE` and
`OTHER_FORMAT` remain typed constructors; their atoms cannot be compared to an
atom of any other sort.

Each `ArtifactContent` constructor is admitted exactly when all displayed
fields are admitted.  The four tags are exhaustive.  The total projections
`artifact_role`, `artifact_format`, and `artifact_size` return their same-named
field in every branch.  The total tagged `artifact_body` projection returns
`TEXT_BODY(ContentIdentity)`, `STRUCTURED_BODY(map)`,
`OPAQUE_BODY(ContentIdentity)`, or `BEHAVIOR_BODY(map)` respectively.
Consequently size and format are determined for every
artifact.  `Format` describes artifact representation only.  The distinct
two-constructor `StorageBackend` sort is retained solely for the controller-
owned choice in C08; local/hosted storage is never a `Format`.

```text
RepositorySnapshot = finite map(Path -> ArtifactContent)
SnapshotIdentity   = SNAPSHOT_IDENTITY(exact RepositorySnapshot)
ChangeEntry = CREATED(new : ArtifactContent) |
              DELETED(old : ArtifactContent) |
              MODIFIED(old : ArtifactContent, new : ArtifactContent)
ChangeSet   = finite map(Path -> ChangeEntry)
```

`SNAPSHOT_IDENTITY(F)=SNAPSHOT_IDENTITY(G)` iff `F=G` by complete map
equality; it is not a digest or handle.  `MODIFIED(old,new)` is admitted only
when `old != new`.  A `ChangeSet` is an extensional relation between supplied
snapshots, never an action sequence.

The selector and observation algebras are closed:

```text
ArtifactSelector =
    SELECT_PATHS(paths : PathSet)
  | SELECT_ROLE(role : ArtifactRole)
  | SELECT_PATHS_WITH_ROLE(paths : PathSet, role : ArtifactRole)

ArtifactProjection = PRESENCE | CONTENT | FORMAT_ONLY | SIZE_ONLY |
                     STRUCTURED_FIELD(FieldId)
SubjectId = REQUEST_SUBJECT(subject_atom) | WORKLOAD_SUBJECT(subject_atom) |
            RESOLUTION_LANE(subject_atom) | CLIENT_PAIR(subject_atom)
Coverage = COMPLETE | INCOMPLETE_SUBJECTS(nonempty finset(SubjectId))
ObservationValue =
    ABSENT | PRESENT | PRESENT_CONTENT(ArtifactContent) | PRESENT_FORMAT(Format) |
    PRESENT_SIZE(ByteSize) | PRESENT_FIELD(FieldValue) |
    ACCEPTED | REJECTED | METRIC_VALUE(integer) |
    RESOLUTION_VALUE(ContentIdentity) |
    CORRESPONDENCE_VALUE(finite map(FieldId -> FieldValue),
                         finite map(FieldId -> FieldValue))

ObservationSpec =
    ARTIFACT_VIEW(selector : ArtifactSelector,
                  projection : ArtifactProjection)
  | REQUEST_BEHAVIOR_VIEW(domain : nonempty finset(SubjectId))
  | WORKLOAD_METRIC_VIEW(domain : nonempty finset(SubjectId),
                         metric : FieldId)
  | DEPENDENCY_RESOLUTION_VIEW(selector : ArtifactSelector,
                               lanes : nonempty finset(SubjectId))
  | CLIENT_ADAPTER_VIEW(pairs : nonempty finset(SubjectId))

ObservationResult =
    ARTIFACT_RESULT(spec_identity : exact ObservationSpec,
                    coverage : Coverage,
                    values : finite map(Path -> ObservationValue))
  | SUBJECT_RESULT(spec_identity : exact ObservationSpec,
                   coverage : Coverage,
                   values : finite map(SubjectId -> ObservationValue))
  | LANE_RESULT(spec_identity : exact ObservationSpec,
                coverage : Coverage,
                values : finite map(SubjectId -> ObservationValue))
  | CORRESPONDENCE_RESULT(spec_identity : exact ObservationSpec,
                          coverage : Coverage,
                          values : finite map(SubjectId -> ObservationValue))

ObservationRelation = EQUAL | ACCEPT_REJECT_EQUAL | NO_GREATER |
                      STRICTLY_LOWER |
                      FIELD_CORRESPONDENCE(
                        finite bijection(FieldId -> FieldId))
```

Every `SubjectId` in a request/workload/lane/client domain must carry the
matching tag.  An `ObservationResult` is admitted only when its result tag
matches the spec tag, `spec_identity` is exact, all keys have the required
sort, and its value constructors match the projection: `PRESENCE` permits
only `ABSENT|PRESENT`, `CONTENT` only `ABSENT|PRESENT_CONTENT`, `FORMAT_ONLY`
only `ABSENT|PRESENT_FORMAT`, `SIZE_ONLY` only `ABSENT|PRESENT_SIZE`, and
`STRUCTURED_FIELD` only `ABSENT|PRESENT_FIELD`.  An artifact result is
always `COMPLETE` and has the exact selected path set as its map domain; path
selectors include selected absent paths as `ABSENT`, and role-only selectors
range over the finite supplied map.  A subject/lane/correspondence result is
`COMPLETE` iff its map domain is the exact declared subject domain.
`INCOMPLETE_SUBJECTS(M)` requires `M` to be exactly the nonempty missing
subject subset and the map domain to be the declared domain minus `M`.  The
four non-artifact views read only matching `BEHAVIOR_ARTIFACT` tables from that
same snapshot.  A missing declared subject yields `INCOMPLETE_SUBJECTS`, never
a hidden lookup.

`EQUAL` is complete result equality.  `ACCEPT_REJECT_EQUAL` compares equal
subject domains and exact `ACCEPTED`/`REJECTED` values.  `NO_GREATER` and
`STRICTLY_LOWER` compare positionally equal complete integer metric maps.
`FIELD_CORRESPONDENCE(m)` holds on a pair of complete structured artifact
results exactly when renaming the left field domain by `m` gives the right
field/value map.  On one complete `CORRESPONDENCE_RESULT`, it holds exactly
when every `CORRESPONDENCE_VALUE(L,R)` has
`domain(m)=domain(L)`, `range(m)=domain(R)`, and `L[i]=R[m(i)]` for every
`i`; this is the unary relation used by `ADAPTER_CORRESPONDS`.  Every relation
is otherwise false for complete inputs and unknown for an incomplete needed
input.  No relation contains a callback or service handle.

Verification and task values are likewise exhaustive:

```text
VerificationStatus = PASS | FAIL | INCONCLUSIVE
VerificationSpec = VERIFY(
  protocol_identity : verification_protocol_atom,
  subject : ObservationSpec,
  evidence_schema_key : ContractSpecKey)
VerificationRecord = VERIFICATION_RECORD(
  spec : VerificationSpec,
  snapshot_identity : SnapshotIdentity,
  status : VerificationStatus,
  observation : ObservationResult,
  evidence_refs : nonempty finset(EvidenceRef))

Criterion =
    OBSERVATION_EQUALS(spec : ObservationSpec,
                       expected : ObservationResult)
  | ONE_FORMAT_OF(selector : ArtifactSelector,
                  formats : nonempty finset(Format))
  | ARTIFACTS_NONEMPTY(selector : ArtifactSelector)
  | ARTIFACT_SIZE_LT(selector : ArtifactSelector, upper : ByteSize)
  | ARTIFACT_SIZE_AT_LEAST(selector : ArtifactSelector, lower : ByteSize)
  | UNIVERSAL_OBSERVATION(spec : ObservationSpec,
                          baseline : ObservationResult,
                          relation : ObservationRelation)
  | DEPENDENCY_REPRODUCIBLE(spec : ObservationSpec)
  | ADAPTER_CORRESPONDS(spec : ObservationSpec,
                        relation : ObservationRelation)
TaskSpec = TASK(
  criteria : finset(Criterion),
  required_verifications : finset(VerificationSpec))
```

A `VerificationRecord` is admitted only when its observation has exact
`spec.subject` identity, its evidence references bind the displayed evidence
schema, and its fields have the displayed types.  It remains evidence, not a
truth value.  Criterion admission additionally requires the obvious matching
spec/result tag: `UNIVERSAL_OBSERVATION` has a request/workload view,
`DEPENDENCY_REPRODUCIBLE` has a dependency-resolution view, and
`ADAPTER_CORRESPONDS` has a client-adapter view and requires a
`FIELD_CORRESPONDENCE` relation.  `TASK` admits every finite combination of
admitted criteria and verification specs, including the empty/empty value;
there is no case ID,
task taxonomy, evaluator, service, expected Contract, hidden target, or opaque
success field.

The event-pattern and six payload algebras are complete:

```text
ChangeKind = CREATED_KIND | DELETED_KIND | MODIFIED_KIND
EventPattern =
    ANY_EVENT(key : EventKey)
  | COMMAND_IS(command_id : abstract_command_atom)
  | TEST_IS(spec : VerificationSpec,
            statuses : nonempty finset(VerificationStatus))
  | PATH_CHANGE_IN(paths : PathSet,
                   kinds : nonempty finset(ChangeKind))
  | NETWORK_CLASS(contact_class : contact_class_atom)
  | RELEASE_IS(release_id : abstract_release_atom,
               snapshot : SnapshotIdentity)
  | REFRESHES(selector : ArtifactSelector,
              snapshot : SnapshotIdentity)

CommandEventPayload = COMMAND_EVENT(
  command_id : abstract_command_atom, purpose : purpose_atom)
TestEventPayload = TEST_EVENT(
  spec : VerificationSpec, snapshot : SnapshotIdentity,
  status : VerificationStatus,
  evidence_refs : nonempty finset(EvidenceRef))
PathChangeEventPayload =
    PATH_CREATED(path : Path, new : ArtifactContent)
  | PATH_DELETED(path : Path, old : ArtifactContent)
  | PATH_MODIFIED(path : Path, old : ArtifactContent,
                  new : ArtifactContent)
NetworkContactEventPayload = NETWORK_CONTACT(
  contact_class : contact_class_atom, purpose : purpose_atom)
ReleaseEventPayload = RELEASE_EVENT(
  release_id : abstract_release_atom, snapshot : SnapshotIdentity)
DependencyRefreshEventPayload = DEPENDENCY_REFRESH(
  selector : ArtifactSelector, snapshot : SnapshotIdentity)
```

Each payload is admitted exactly when its displayed tag and every displayed
field are admitted; payload equality is tag plus complete field equality.
`PATH_MODIFIED` requires unequal contents.  Each pattern tag implies exactly
the section 3 event key of the same family; `ANY_EVENT` alone carries an
arbitrary exact key.  A pattern is admitted exactly when every displayed field
is admitted and each displayed `nonempty finset` is nonempty; equality is tag
plus complete field equality.  `event_matches` compares all displayed selected fields,
including snapshot identity where present.  All atoms have exact sort-local
equality and cannot be rendered as a command, endpoint, repository action, or
release operation.

### 2.2 Total projections and direct meanings

`snapshot_of : State -> RepositorySnapshot` returns `TERM_VALUE(F)` exactly
when the supplied state is admitted as `F`, otherwise
`TERM_ERROR(NOT_A_REPOSITORY_SNAPSHOT)`.  It reads nothing else.  For admitted
snapshots `P,F`, the unique relation is

```text
changes_between(P,F)[p] = CREATED(F[p])       iff p notin dom(P), p in dom(F)
changes_between(P,F)[p] = DELETED(P[p])       iff p in dom(P), p notin dom(F)
changes_between(P,F)[p] = MODIFIED(P[p],F[p]) iff p in both and P[p] != F[p]
```

No other path occurs.  `observe(spec,F)` applies the exact selector/result
rules above and returns the unique `TERM_VALUE(ObservationResult)`; an
inadmitted value produces the declared term error.  These functions are
extensional and never prescribe a state transition.

For current supplied snapshot `F`, `verification_passed(v,F,E)` selects only
schema-valid `VerificationRecord`s in supplied `EvidenceStore E` whose spec is
exactly `v` and whose snapshot identity is exactly `SNAPSHOT_IDENTITY(F)`.
Wrong-snapshot records are nonmatching evidence, never success.  A malformed
schema/reference or two matching decisive records with opposite status returns
`Eval.ERROR`.  Otherwise any matching `FAIL` returns `FALSE`, any matching
`PASS` returns `TRUE`, and no decisive match returns `UNKNOWN`; all matching
evidence and inconclusive reasons are retained under K1 set semantics.

`task_accepts(t,F,E)` is a direct extensional relation on its three supplied
values.  It does not call or observe another binding.  It computes each of the
eight criterion results from the exhaustive rules above and computes each
required verification by the same mathematical relation just defined with
the same `F,E`.  It then returns their K1 A1 conjunction.  This gives a unique
result for every admitted finite `TaskSpec`, including zero or arbitrarily many
criteria and verification specs and repeated constructor kinds; the empty/
empty task is K1 `TrueF` and returns `VALUE(TRUE,{},{})`.  This does not
pretend that one K2 lower observation stands for a variable number of calls.  The direct
definition is not an evaluator algorithm and adds no ambient access.

The standard preservation and final-state patterns remain ordinary K1 terms:

```text
Require(Atom(SP(observations_equal),
  Apply(SF(observe),L(T(ObservationSpec),spec),
    Apply(SF(snapshot_of),Anchor(pre))),
  Apply(SF(observe),L(T(ObservationSpec),spec),
    Apply(SF(snapshot_of),Anchor(final)))))

Require(Atom(SP(task_accepts),L(T(TaskSpec),task_spec),
  Apply(SF(snapshot_of),Anchor(final)),Anchor(evidence)))
```

Every function returns `TermResult`; every predicate returns K1 `Eval`; term
failure follows K1 A2.  Nothing creates an outcome, mutates state, or schedules
an event.

### 2.3 Minimal-vocabulary decision

Repository contents and observations remain separate because equal selected
observations need not imply equal snapshots.  Paths and path sets separate
element identity from finite scope.  Change sets and snapshot identities are
derived because separately asserted values could disagree with their supplied
snapshots.  Size, format, and storage choice remain distinct: every artifact
has total size/format projections, while C08's controller-owned backend has no
representation meaning.  Verification records and `EvidenceRef`s remain
separate from truth.  `TaskSpec` is retained for one reusable, fully typed
broad predicate, but its meaning is direct and lower-observation-free.  Event
keys remain separate only where payload type or immutable class differs.  All
goal, preservation, prohibition, permission, implication, alternative, truth,
choice, provenance, and authority forms remain K1-derived.

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
| `T(PathSegment)` | exact admitted `SEGMENT` values | `{}` |
| `T(Path)` | exact admitted `PATH` values | `{DECLARATION(T(PathSegment))}` |
| `T(PathSet)` | finite sets of `T(Path)` | `{DECLARATION(T(Path))}` |
| `T(ArtifactRole)` | exact eight `ArtifactRole` constructors, including `OTHER_ROLE` | `{}` |
| `T(Format)` | exact six representation-format constructors | `{}` |
| `T(StorageBackend)` | exactly `LOCAL_STORAGE` or `HOSTED_STORAGE` | `{}` |
| `T(ByteSize)` | exact `KIB(nonnegative integer)` values | `{}` |
| `T(ContentIdentity)` | exact `CONTENT_ID` values | `{}` |
| `T(FieldId)` | exact `FIELD` values | `{}` |
| `T(FieldValue)` | exact Boolean/integer/atom field values | `{}` |
| `T(SubjectId)` | exact request/workload/lane/client subject tags | `{}` |
| `T(BehaviorValue)` | exact five behavior-value constructors | `{DECLARATION(T(ContentIdentity)),DECLARATION(T(FieldId)),DECLARATION(T(FieldValue))}` |
| `T(ArtifactBody)` | exact four tagged body-projection constructors | `{DECLARATION(T(ContentIdentity)),DECLARATION(T(FieldId)),DECLARATION(T(FieldValue)),DECLARATION(T(SubjectId)),DECLARATION(T(BehaviorValue))}` |
| `T(ArtifactContent)` | exact four tagged artifact constructors | `{DECLARATION(T(ArtifactRole)),DECLARATION(T(Format)),DECLARATION(T(ByteSize)),DECLARATION(T(ContentIdentity)),DECLARATION(T(FieldId)),DECLARATION(T(FieldValue)),DECLARATION(T(SubjectId)),DECLARATION(T(BehaviorValue))}` |
| `T(ObservationValue)` | exact closed observation-value constructors | `{DECLARATION(T(ArtifactContent)),DECLARATION(T(Format)),DECLARATION(T(ByteSize)),DECLARATION(T(FieldId)),DECLARATION(T(FieldValue)),DECLARATION(T(ContentIdentity))}` |
| `T(RepositorySnapshot)` | finite maps `T(Path)->T(ArtifactContent)` | `{DECLARATION(T(Path)),DECLARATION(T(ArtifactContent))}` |
| `T(SnapshotIdentity)` | exact `SNAPSHOT_IDENTITY` values | `{DECLARATION(T(RepositorySnapshot))}` |
| `T(ChangeEntry)` | exact created/deleted/modified constructors | `{DECLARATION(T(ArtifactContent))}` |
| `T(ChangeSet)` | exact extensional change maps | `{DECLARATION(T(Path)),DECLARATION(T(ChangeEntry))}` |
| `T(ArtifactSelector)` | exact three selector constructors | `{DECLARATION(T(PathSet)),DECLARATION(T(ArtifactRole))}` |
| `T(ArtifactProjection)` | exact presence/content/format/size/field tags | `{DECLARATION(T(FieldId))}` |
| `T(Coverage)` | exact `COMPLETE`/`INCOMPLETE_SUBJECTS` constructors | `{DECLARATION(T(SubjectId))}` |
| `T(ObservationSpec)` | exact five observation-spec constructors | `{DECLARATION(T(ArtifactSelector)),DECLARATION(T(ArtifactProjection)),DECLARATION(T(SubjectId)),DECLARATION(T(FieldId))}` |
| `T(ObservationResult)` | exact four result constructors | `{DECLARATION(T(Path)),DECLARATION(T(SubjectId)),DECLARATION(T(Coverage)),DECLARATION(T(ObservationSpec)),DECLARATION(T(ObservationValue))}` |
| `T(ObservationRelation)` | exact five relation constructors | `{DECLARATION(T(FieldId))}` |
| `T(VerificationStatus)` | exactly `PASS`, `FAIL`, or `INCONCLUSIVE` | `{}` |
| `T(VerificationSpec)` | exact `VERIFY` records | `{DECLARATION(T(ObservationSpec))}` |
| `T(VerificationRecord)` | exact `VERIFICATION_RECORD` values | `{DECLARATION(T(VerificationSpec)),DECLARATION(T(SnapshotIdentity)),DECLARATION(T(VerificationStatus)),DECLARATION(T(ObservationResult))}` |
| `T(Criterion)` | exactly the eight criterion constructors and fields | `{DECLARATION(T(ObservationSpec)),DECLARATION(T(ObservationResult)),DECLARATION(T(ArtifactSelector)),DECLARATION(T(ByteSize)),DECLARATION(T(Format)),DECLARATION(T(ObservationRelation))}` |
| `T(TaskSpec)` | finite typed task specifications | `{DECLARATION(T(Criterion)),DECLARATION(T(VerificationSpec))}` |
| `T(ChangeKind)` | exactly created/deleted/modified kind tags | `{}` |
| `T(CommandId)` | exact abstract command atoms | `{}` |
| `T(ContactClass)` | exact contact-class atoms | `{}` |
| `T(ReleaseId)` | exact abstract release atoms | `{}` |
| `T(Purpose)` | exact declared-purpose atoms | `{}` |
| `T(EventPattern)` | exact seven event-pattern constructors | `{DECLARATION(T(PathSet)),DECLARATION(T(VerificationSpec)),DECLARATION(T(VerificationStatus)),DECLARATION(T(ChangeKind)),DECLARATION(T(CommandId)),DECLARATION(T(ContactClass)),DECLARATION(T(ReleaseId)),DECLARATION(T(SnapshotIdentity)),DECLARATION(T(ArtifactSelector))}` |
| `T(CommandEventPayload)` | exact `COMMAND_EVENT` records | `{DECLARATION(T(CommandId)),DECLARATION(T(Purpose))}` |
| `T(TestEventPayload)` | exact `TEST_EVENT` records | `{DECLARATION(T(VerificationSpec)),DECLARATION(T(SnapshotIdentity)),DECLARATION(T(VerificationStatus))}` |
| `T(PathChangeEventPayload)` | exact three path-change constructors | `{DECLARATION(T(Path)),DECLARATION(T(ArtifactContent))}` |
| `T(NetworkContactEventPayload)` | exact `NETWORK_CONTACT` records | `{DECLARATION(T(ContactClass)),DECLARATION(T(Purpose))}` |
| `T(ReleaseEventPayload)` | exact `RELEASE_EVENT` records | `{DECLARATION(T(ReleaseId)),DECLARATION(T(SnapshotIdentity))}` |
| `T(DependencyRefreshEventPayload)` | exact `DEPENDENCY_REFRESH` records | `{DECLARATION(T(ArtifactSelector)),DECLARATION(T(SnapshotIdentity))}` |
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
| `DP(verification_passed)` / `SP(verification_passed)` | predicate `(T(VerificationSpec),T(RepositorySnapshot),EvidenceStore)->Bool` | `({}, {final}, {evidence})` |
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
| `CS(PREDICATE_MEANING,verification_passed)` | Sigma / `PREDICATE_MEANING` | `(VerificationSpec,RepositorySnapshot,EvidenceStore) -> Eval` by exact spec/schema/current-snapshot matching and the total decisive/conflict rule in §2.2 | `{}` |
| `CS(PREDICATE_MEANING,task_accepts)` | Sigma / `PREDICATE_MEANING` | `(TaskSpec,RepositorySnapshot,EvidenceStore) -> Eval` by the direct total extensional criterion/verification relation in §2.2 and K1 A1 | `{}` |
| `CS(PREDICATE_MEANING,dependency_metadata_changed)` | Sigma / `PREDICATE_MEANING` | change set -> true iff at least one extensional entry has dependency-metadata artifact role | `{}` |
| `CS(PREDICATE_MEANING,event_matches)` | Sigma / `PREDICATE_MEANING` | pattern/event value -> exact structural match; keys outside the pattern are false | `{}` |
| `CS(PREDICATE_MEANING,event_occurred)` | Sigma / `PREDICATE_MEANING` | pattern/trace -> K1 `ANY_RESULT` over `event_matches(pattern,event_value)` in trace order-insensitive set aggregation | `{BINDING(DP(event_matches))->EVAL_RESULT_SEQUENCE}` |
| `CS(PREDICATE_MEANING,refresh_scope)` | Sigma / `PREDICATE_MEANING` | event value -> true exactly for admitted `EK(dependency_refresh)` payloads whose selector is the exact `DEPENDENCY_LOCK` artifact role, false for every other admitted event | `{}` |
| `CS(PROFILE_COVERAGE,implementation_evidence)` | Sigma / `PROFILE_COVERAGE` | exact `(TaskSpec,RepositorySnapshot,EvidenceStore,Eval)` coverage subject -> exact complete/incomplete/unknown profile result, with the supplied Eval required to equal direct `task_accepts` | `{BINDING(DP(task_accepts))->EVAL_RESULT}` |
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
| `CS(SOUND_FRAGMENT,bundle_bounds)` | Service / `SOUND_FRAGMENT` | exact closed conjunctions of the nonempty/size criterion atoms over one selector/snapshot | `{}` |
| `CS(COMPLETE_FRAGMENT,bundle_bounds)` | Service / `COMPLETE_FRAGMENT` | the same named finite contradiction fragment | `{}` |
| `CS(SOUND_FRAGMENT,adapter_witness)` | Service / `SOUND_FRAGMENT` | exactly the closed adapter-preservation Contract `C_w` and admitted abstract witness shape in §6.2 | `{}` |
| `CS(SOUND_FRAGMENT,confluence_fixture)` | Service / `SOUND_FRAGMENT` | exact closed fixture Contract containing admitted literals `(spec,P,F)` -> `IN_FRAGMENT` iff the independently observed `observe(spec,F)` and `changes_between(P,F)` results are both their exact `TERM_VALUE` constructors, otherwise `OUTSIDE_FRAGMENT` | `{BINDING(DF(observe))->TERM_RESULT, BINDING(DF(changes_between))->TERM_RESULT}` |
| `CS(REQUIRED_EVIDENCE,service)` | Service / `REQUIRED_EVIDENCE` | exact request evidence required by the target meaning or proof | target binding/profile support only |
| `CS(SERVICE_FAILURE_BEHAVIOR,service)` | Service / `SERVICE_FAILURE_BEHAVIOR` | exact K2 role-specific evaluation/reasoning failure tags | `{}` |

The access names are exact: `literal`, `state_only`, `snapshot_pair`, `spec_snapshot`,
`result_pair`, `task_final_evidence`, `change_set_only`,
`verification_snapshot_evidence`, `pattern_event`, `pattern_trace`, `event_only`, and
no others.  Each admits
only the signature positions its name enumerates and the exact facet positions
in section 3.  In particular, `task_final_evidence` admits the `TaskSpec`, one
supplied final snapshot, and one supplied `EvidenceStore`, with no lower
observation.  `verification_snapshot_evidence` admits exactly one spec, one
supplied snapshot, and one supplied store.  Neither admits a Contract,
challenge, expected result, service state, provenance, choice, or other outcome
facet.

`task_accepts` is reusable and total for every admitted finite `TaskSpec`, not
a finite challenge mapping.  Its ContractSpec has an empty query map and empty
support.  For each criterion it computes the extensional fact directly from
the supplied snapshot; for each required verification it applies the same
mathematical snapshot-bound verification relation directly.  This is one
extensional relation, not a variable batch of K2 lower calls.  K1 A1 unions all
evidence, unknown reasons, and errors; error dominates, otherwise false
dominates, otherwise unknown precedes true.  A wrong-schema or wrong-snapshot
record is never success, and no matching decisive record is factual unknown.

The eight criterion results are exact.  `OBSERVATION_EQUALS` compares the
direct section 2 observation with the exact admitted expected result.
`ONE_FORMAT_OF` requires a nonempty selected population and every total
`artifact_format` projection to lie in the nonempty supplied set.
`ARTIFACTS_NONEMPTY` tests selected present-map nonemptiness.  The two size
criteria quantify over every selected present artifact using the total
`artifact_size` projection and the abstract KiB integer.  Empty selection is
false for all three population/size constructors.  `UNIVERSAL_OBSERVATION`
compares the current result with its supplied baseline under the displayed
relation.  `DEPENDENCY_REPRODUCIBLE` requires a complete lane result with at
least two lanes and identical `RESOLUTION_VALUE`s.  `ADAPTER_CORRESPONDS`
requires a complete client-pair result satisfying its exact relation.  A
complete counterexample is false, a complete success is true, and an
incomplete needed domain is unknown with a stable reason.  Type, schema,
conflict, or undeclared-access failure is `Eval.ERROR`.  None consults a
challenge label, expected mapping, service state, or ambient repository.

### 4.2 Semantic bindings and dependency closure

| Binding(s) | Meaning / evidence / access / unknown / error ContractSpecs | Exact semantic roots beyond the declaration and these specs | Validation references |
|---|---|---|---|
| `DF(snapshot_of)` | `snapshot_of`; `none`; `state_only`; `not_applicable`; `term` | type-admission observation for `T(RepositorySnapshot)` | `{}` |
| `DF(changes_between)` | `changes_between`; `none`; `snapshot_pair`; `not_applicable`; `term` | `{}` | `{}` |
| `DF(observe)` | `observe`; `none`; `spec_snapshot`; `not_applicable`; `term` | `{}` | `{}` |
| `DP(observations_equal)` | same-named meaning; `none`; `result_pair`; `never`; `predicate` | `{}` | `{}` |
| `DP(task_accepts)` | same-named direct meaning; `verification`; `task_final_evidence`; `task`; `predicate` | `{}` | `{}` |
| `DP(dependency_metadata_changed)` | same-named meaning; `none`; `change_set_only`; `never`; `predicate` | `{}` | `{}` |
| `DP(verification_passed)` | same-named current-snapshot meaning; `verification`; `verification_snapshot_evidence`; `evidence_pending`; `predicate` | `{}` | `{}` |
| `DP(event_matches)` | same-named meaning; `none`; `pattern_event`; `never`; `predicate` | `{}` | `{}` |
| `DP(event_occurred)` | same-named meaning; `none`; `pattern_trace`; `never`; `predicate` | exact lower `event_matches` binding | `{}` |
| `DP(refresh_scope)` | same-named meaning; `none`; `event_only`; `never`; `predicate` | `{}` | `{}` |
| `PAIR(refresh)` occurrence projection | exact K2 `T3_A1_MEANING_LIFT`, `T3_A1_EVIDENCE_LIFT`, `T3_A1_ACCESS_LIFT`, `T3_A1_UNKNOWN_LIFT`, and `T3_A1_ERROR_LIFT` records | exact `T3_A1_DEPENDENCY_LIFT(pd,pb,sb)` for the retained pair declaration/binding and scope binding | `{}` for the retained definitional path |

Every binding key is derived from its declaration key; all binding kinds,
facets, contracts, and `SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT` are exact.
For every row, K2 section 3.3 recomputes `proper_semantic_dependencies` and the
least acyclic `dependency_closure` from the declaration, listed ContractSpecs,
their extensional supports, and listed lower bindings.  The producer cannot
supply a smaller or larger set.  `task_accepts` has no lower node.  The
separate `CS(SOUND_FRAGMENT,confluence_fixture)` has exactly two independent
lower nodes, `BINDING(DF(observe))` and
`BINDING(DF(changes_between))`, with input projections from its exact fixture
Contract respectively extracting `(spec,F)` and `(P,F)`.  Neither node is a
predecessor of the other, the relation depends on both, and the two orders
`[observe,changes_between]` and `[changes_between,observe]` therefore
produce the same exact two-entry observation map by K2 §3.3.  A self-edge or
genuine cycle is malformed.  Mandatory validation references remain in
`DependencyEnvironment.validation_references` and never enter this proper
DAG.

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
the `DEPENDENCY_LOCK` artifact role and false for every other admitted event.
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
`verification_passed(spec,FINAL,EVIDENCE)`.  Test events are observational and do
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
TRB = (TP,coding,bounds-admission-root,(1))
TRW = (TP,coding,witness-admission-root,(1))

SK(functions) = (CK,coding.service,functions,(1),FUNCTION_EVALUATION)
CAP(functions)= (SK(functions),core_functions)
SK(predicates)= (CK,coding.service,predicates,(1),PREDICATE_EVALUATION)
CAP(predicates)= (SK(predicates),core_predicates)
SK(profile)    = (CK,coding.service,profile,(1),PROFILE_CONCRETE)
CAP(profile)   = (SK(profile),implementation_evidence)
SK(bounds)     = (CK,coding.service,bounds,(1),REASONING)
CAP(bounds)    = (SK(bounds),bundle_bounds)
SK(confluence) = (CK,coding.service,confluence,(1),REASONING)
CAP(confluence)= (SK(confluence),two_node_confluence)

AWK = ((capknow.semantic,adapter-witness),(1))
AWSK = (AWK,coding.service,adapter-witness,(1),REASONING)
CAP(witness) = (AWSK,abstract_adapter_witness)

RVK = ((capknow.audit,coding-certificate-validator),(1))
RVSK(bounds) = (RVK,coding.validation,bounds,(1),REASONING)
CAP(validate_bounds) = (RVSK(bounds),validate_bundle_bounds)
RVSK(witness) = (RVK,coding.validation,witness,(1),REASONING)
CAP(validate_witness) = (RVSK(witness),validate_adapter_witness)

BCERT = (PLUGIN_CERTIFICATE_ISSUER(CK),
         coding.certificate,bundle_bounds_unsat)
WCERT = (PLUGIN_CERTIFICATE_ISSUER(AWK),
         coding.certificate,adapter_satisfying_witness)

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

For the finite bounds target, freeze these admitted values:

```text
p_b = PATH((SEGMENT(dependency),SEGMENT(lock)))
a_b = TEXT_ARTIFACT(DEPENDENCY_LOCK,TEXT,KIB(150),CONTENT_ID(lock_v1))
S_b = SELECT_PATHS({p_b})
ts_nonempty = TASK({ARTIFACTS_NONEMPTY(S_b)}, {})
ts_lt_100   = TASK({ARTIFACT_SIZE_LT(S_b,KIB(100))}, {})
ts_ge_200   = TASK({ARTIFACT_SIZE_AT_LEAST(S_b,KIB(200))}, {})
```

Every atom is sort-local logical data; `p_b` is not a host path.  Let `C_b` be the exact
closed K1 Contract whose sole hard formula is
`All({TA(ts_nonempty),TA(ts_lt_100),TA(ts_ge_200)})`, with a matching admitted
authority adoption, empty grants/choices/profiles beyond mechanically required
records, and all mechanically derived facets.  Here `TA` is the exact expansion
in section 7.1.  Let `E_b` be the complete
exact `SemanticEnvironment` mechanically required by `C_b`, let `D_b` be the
complete `DependencyEnvironment` mechanically derived from `(C_b,E_b)` by K2
§3.3, and define

```text
J_b = ENVIRONMENT_JUDGMENT_TARGET(
        CONSISTENCY, (C_b), semanticIdentity(E_b))
```

`J_b` is a finite exact logical target.  Neither its subject nor environment
contains a challenge identifier.

For the independent topological fixture, freeze

```text
P_c = {}
F_c = {p_b -> a_b}
s_c = ARTIFACT_VIEW(SELECT_PATHS({p_b}),CONTENT)
O_c = ARTIFACT_RESULT(s_c,COMPLETE,{p_b -> PRESENT_CONTENT(a_b)})
X_c = {p_b -> CREATED(a_b)}
f_c_o = Atom(SP(observations_equal),
             Apply(SF(observe),L(T(ObservationSpec),s_c),
                   L(T(RepositorySnapshot),F_c)),
             L(T(ObservationResult),O_c))
f_c_d = Atom(SP(dependency_metadata_changed),
             Apply(SF(changes_between),L(T(RepositorySnapshot),P_c),
                   L(T(RepositorySnapshot),F_c)))
```

Let `C_c` be the exact closed Contract with hard formulas
`{Require(f_c_o),Require(f_c_d)}`, ABI-issued source/authority adoption, and no
other clauses, grants, choices, pairs, or profiles.  Let `E_c` and `D_c` be its exact
derived semantic and dependency environments and define

```text
J_c = ENVIRONMENT_JUDGMENT_TARGET(
        CONSISTENCY,(C_c),semanticIdentity(E_c))
```

`CS(SOUND_FRAGMENT,confluence_fixture)` is the only record in this document
whose proper observation DAG has the two independent lower result nodes.  It
exists for K3-X confluence testing, not as a dependency of `task_accepts`.

For the abstract C19 route, freeze

```text
f_left  = FIELD(request_field)
f_right = FIELD(client_field)
m_w = {f_left -> f_right}
sid_w = CLIENT_PAIR(adapter_pair)
left_w  = {f_left -> ATOM_VALUE(accepted_shape)}
right_w = {f_right -> ATOM_VALUE(accepted_shape)}
p_w = PATH((SEGMENT(adapter),SEGMENT(schema)))
a_w = BEHAVIOR_ARTIFACT(
  PUBLIC_SCHEMA,JSON,KIB(1),
  {sid_w -> BEHAVIOR_CORRESPONDENCE(left_w,right_w)})
P_w = {p_w -> a_w}
F_w = {p_w -> a_w}
s_w = CLIENT_ADAPTER_VIEW({sid_w})
o_w = CORRESPONDENCE_RESULT(
  s_w,COMPLETE,{sid_w -> CORRESPONDENCE_VALUE(left_w,right_w)})
t_w = TASK({ADAPTER_CORRESPONDS(s_w,FIELD_CORRESPONDENCE(m_w))},{})
TRACE_w = {}
EVIDENCE_w = {}
E_witness = {}
```

Let `C_w` be exactly
`Contract(Hard={Require(OBS_EQ(s_w)),Require(TA(t_w))},
ProfileRequirements={PK(implementation_evidence)})`, with exact ABI-issued
source/authority adoption, no choices, grants, or pair requirements.  Let `E_w`, `D_w`, and
`J_w=ENVIRONMENT_JUDGMENT_TARGET(CONSISTENCY,(C_w),semanticIdentity(E_w))`
be the exact derived records.  Fix one admitted abstract outcome
`O_w=(P_w,TRACE_w,F_w,EVIDENCE_w)` with no controlled events, exact
Contract-derived `chi_C={}`, direct task/preservation results equal to
`VALUE(TRUE,E_witness,{})`, and evidence refs admitted by their displayed
schemas.  `O_w` is finite semantic data, not a patch or construction method.

| Capability | Class and supported targets/judgments | Exact fragment and dependency scope | Required root/failure contract |
|---|---|---|---|
| `CAP(functions)` | `CONCRETE_EVALUATION_ONLY`; `{FUNCTION_EVALUATION}`; supported targets exactly `FUNCTION_TARGETS` | `CS(SOUND_FRAGMENT,functions)`, no complete fragment; dependency scope is the exact union of all three target closures | nonempty `{TR}`; `CS(REQUIRED_EVIDENCE,service)` and `CS(SERVICE_FAILURE_BEHAVIOR,service)` |
| `CAP(predicates)` | `CONCRETE_EVALUATION_ONLY`; `{PREDICATE_EVALUATION}`; supported targets exactly `PREDICATE_TARGETS` | `CS(SOUND_FRAGMENT,predicates)`, no complete fragment; dependency scope is the exact union of all eight target closures | same exact requirements |
| `CAP(profile)` | `CONCRETE_EVALUATION_ONLY`; `{PROFILE_COVERAGE}`; supported targets exactly `{PROFILE_TARGET(PK(implementation_evidence))}` | `CS(SOUND_FRAGMENT,profile)`, no complete fragment; dependency scope is the exact profile closure | same exact requirements |
| `CAP(bounds)` | `COMPLETE_FOR_DECLARED_FRAGMENT`; `{CONSISTENCY}`; supported targets exactly `{J_b}` | sound `CS(SOUND_FRAGMENT,bundle_bounds)` and complete `CS(COMPLETE_FRAGMENT,bundle_bounds)`; dependency scope exactly equals `D_b.transitive_dependency_closure` | nonempty `{TRB}` and the same exact evidence/failure contracts |
| `CAP(confluence)` | `PARTIAL_SYMBOLIC_REASONING`; `{CONSISTENCY}`; supported targets exactly `{J_c}` | sound `CS(SOUND_FRAGMENT,confluence_fixture)`, no complete fragment; dependency scope exactly equals `D_c.transitive_dependency_closure` and contains both independent lower roots | nonempty `{TR}` and the same exact evidence/failure contracts |
| `CAP(witness)` | `PARTIAL_SYMBOLIC_REASONING`; `{CONSISTENCY}`; supported targets exactly `{J_w}` | sound `CS(SOUND_FRAGMENT,adapter_witness)`, no complete fragment; dependency scope exactly equals `D_w.transitive_dependency_closure` | nonempty `{TRW}` and the same exact evidence/failure contracts |
| `CAP(validate_bounds)` | `COMPLETE_FOR_DECLARED_FRAGMENT`; `{CONSISTENCY}`; supported targets exactly `{J_b}` | the same exact bounds sound/complete fragments; dependency scope exactly equals `D_b.transitive_dependency_closure` | nonempty `{TRB}` and the same exact evidence/failure contracts; producer `PLUGIN_PRODUCER(RVK)` |
| `CAP(validate_witness)` | `PARTIAL_SYMBOLIC_REASONING`; `{CONSISTENCY}`; supported targets exactly `{J_w}` | sound `CS(SOUND_FRAGMENT,adapter_witness)`, no complete fragment; dependency scope exactly equals `D_w.transitive_dependency_closure` | nonempty `{TRW}` and the same exact evidence/failure contracts; producer `PLUGIN_PRODUCER(RVK)` |

Every descriptor also has exact ABI/plugin/service identity, nonempty target
set, derived proper dependencies/closure, and, only when it targets a binding,
the exact `ModelCapabilitySummary` in that binding's model contract.  The five
environment-target capabilities add no model summary.  A service is
availability, not denotation.  A meaning may be bound and closed while these
descriptors are absent or unusable.

The two certificate fixtures use these complete trust records; there is no
implicit root lookup or wildcard scope:

```text
U_b_provider = SERVICE_USE_TRUST_TARGET(
  CAP(bounds),CONSISTENCY,ENVIRONMENT_USE(CONSISTENCY,(C_b)),
  semanticIdentity(E_b))
U_b_validator = SERVICE_USE_TRUST_TARGET(
  CAP(validate_bounds),CONSISTENCY,ENVIRONMENT_USE(CONSISTENCY,(C_b)),
  semanticIdentity(E_b))
A_b = JUDGMENT_TRUST_TARGET(CONSISTENCY,(C_b))
ROOT_B = TrustRootRecord(
  trust_root_key=TRB, owner=EMBEDDING_POLICY_PRODUCER(TP),
  trusted_validators={CAP(bounds),CAP(validate_bounds)},
  permitted_certificate_kinds={CONTRADICTION_PROOF},
  permitted_targets={U_b_provider,U_b_validator,A_b},
  adoption=V0_EXTERNAL_TRUST_PREMISE)
T_b = TrustEnvironment(
  trust_policy_key=TP, policy_owner=EMBEDDING_POLICY_PRODUCER(TP),
  root_judgments={TRB -> TRUST_ROOT_ADMITTED(ROOT_B)})

U_w_provider = SERVICE_USE_TRUST_TARGET(
  CAP(witness),CONSISTENCY,ENVIRONMENT_USE(CONSISTENCY,(C_w)),
  semanticIdentity(E_w))
U_w_validator = SERVICE_USE_TRUST_TARGET(
  CAP(validate_witness),CONSISTENCY,ENVIRONMENT_USE(CONSISTENCY,(C_w)),
  semanticIdentity(E_w))
A_w = JUDGMENT_TRUST_TARGET(CONSISTENCY,(C_w))
ROOT_W = TrustRootRecord(
  trust_root_key=TRW, owner=EMBEDDING_POLICY_PRODUCER(TP),
  trusted_validators={CAP(witness),CAP(validate_witness)},
  permitted_certificate_kinds={SATISFYING_WITNESS},
  permitted_targets={U_w_provider,U_w_validator,A_w},
  adoption=V0_EXTERNAL_TRUST_PREMISE)
T_w = TrustEnvironment(
  trust_policy_key=TP, policy_owner=EMBEDDING_POLICY_PRODUCER(TP),
  root_judgments={TRW -> TRUST_ROOT_ADMITTED(ROOT_W)})
```

The bounds capability proves only the exact theorem at `J_b`

```text
ARTIFACTS_NONEMPTY(S) AND
forall artifact in S: size < upper AND size >= lower AND lower >= upper
  -> CONSISTENCY_UNSAT
```

for one admitted selector, exact `KIB` byte-size constructor, snapshot domain, and complete closed
conjunction.  It proves no arbitrary arithmetic, task correctness, existence,
or cross-plugin joint conclusion.  Outside that fragment, or without its exact
admitted certificate, the consistency result is `CONSISTENCY_UNKNOWN` absent a
different K1 witness/proof.  Service failure is `REASONING_ERROR` and yields no
consistency result for that invocation.

The C11 admission path is a complete K2 construction, not a prose assumption.
Let `R_b` be the exact `ReasoningRequest(ABI0,CONSISTENCY,(C_b),E_b,T_b,
CS(SOUND_FRAGMENT,bundle_bounds),D_b,J_b,CAP(bounds))`.  Let

```text
BundleBoundsProof = BOUNDS_CORE(
  selector=S_b, population_nonempty=TRUE,
  upper=KIB(100), lower=KIB(200),
  relation=(200>=100),
  subject_identity=IDENTITY_OF(C_b))
BPROOF_REF = EvidenceRef(
  PLUGIN_ISSUER(CK),coding.bounds-proof,bounds_core,
  CS(REQUIRED_EVIDENCE,service))
```

and let `BENV` be the exact `CertificateEnvelope` with key `BCERT`, kind
`CONTRADICTION_PROOF`, request binding `R_b`, subjects `(C_b)`, environment
`E_b`, producer capability `CAP(bounds)`, bounds sound fragment, dependencies
`D_b`, claimed conclusion `CONSISTENCY_UNSAT`, validator
`CAP(validate_bounds)`, root `TRB`, abstraction `SYMBOLIC`, payload
`BundleBoundsProof`, and evidence refs exactly `{BPROOF_REF}`.  K2 derives the
complete `CertificateValidationRequest` with validator role `REASONING`, target
`J_b`, receiving rule `RECEIVE_REASONING_JUDGMENT`, both exact service-use and
certificate-admission targets, and the same environments/dependencies.

The exact validation-filtered subject producer set is
`{PLUGIN_PRODUCER(CK),ABI_PRODUCER(ABI0)}`: `CK` owns the coding meanings and
ABI0 owns the fixed source/authority carriers.  The certificate producer is
`PLUGIN_PRODUCER(CK)`, the validator producer is
`PLUGIN_PRODUCER(RVK)`, and the root producer is
`EMBEDDING_POLICY_PRODUCER(TP)`; all K2-required inequalities therefore hold.
`CertificateAdmission.ADMITTED(BCERT,CONSISTENCY_UNSAT)` is received only as
`ReasoningResult.ADMITTED_JUDGMENT(CONSISTENCY_UNSAT,BCERT)`.  Missing,
rejected, malformed, wrong-scope, or failed records yield their exact K2
no-admission/evaluability/error branch and no UNSAT conclusion.

The C19 witness uses a separate producer, certificate, request, and payload.
Let `R_w` be the exact `ReasoningRequest(ABI0,CONSISTENCY,(C_w),E_w,T_w,
CS(SOUND_FRAGMENT,adapter_witness),D_w,J_w,CAP(witness))` and

```text
AdapterWitness = ABSTRACT_OUTCOME_WITNESS(
  contract_identity=IDENTITY_OF(C_w), outcome=O_w,
  chi_C={}, accept_eval=VALUE(TRUE,E_witness,{}),
  admitted_evidence=E_witness)
WPROOF_REF = EvidenceRef(
  PLUGIN_ISSUER(AWK),coding.witness,adapter_abstract,
  CS(REQUIRED_EVIDENCE,service))
```

Let `WENV` be the exact envelope with key `WCERT`, kind
`SATISFYING_WITNESS`, request `R_w`, subjects `(C_w,O_w)`, environment `E_w`,
capability `CAP(witness)`, witness sound fragment, dependencies `D_w`, claimed
conclusion `CONSISTENCY_SAT`, validator `CAP(validate_witness)`, root `TRW`,
abstraction `ABSTRACT`, payload `AdapterWitness`, and evidence refs exactly
`{WPROOF_REF}`.
Its derived validation request has target `J_w`, validator role `REASONING`,
receiving rule `RECEIVE_REASONING_JUDGMENT`, and both exact trust targets.  Its
validation-filtered subject producer set is again
`{PLUGIN_PRODUCER(CK),ABI_PRODUCER(ABI0)}`; certificate producer
`PLUGIN_PRODUCER(AWK)`, validator producer `PLUGIN_PRODUCER(RVK)`, and root
producer `EMBEDDING_POLICY_PRODUCER(TP)` are pairwise distinct from the
subject as K2 requires.  Only
`CertificateAdmission.ADMITTED(WCERT,CONSISTENCY_SAT)` yields
`ReasoningResult.ADMITTED_JUDGMENT(CONSISTENCY_SAT,WCERT)`.  The separate
profile request may still return `PROFILE_INCOMPLETE`.

### 6.3 Trust and lifecycle

`TP`, `TR`, `TRB`, and `TRW` are embedding-policy identities, not plugin
records.  Their exact admitted `TrustRootRecord`s all have owner
`EMBEDDING_POLICY_PRODUCER(TP)` and adoption `V0_EXTERNAL_TRUST_PREMISE`.
The permitted target family for `TR` consists only of ordinary service-use
targets of `CAP(functions)`, `CAP(predicates)`, `CAP(profile)`, and
`CAP(confluence)` for their displayed judgments, `ServiceUseSubject`s, and
exact environment identities.  Each request-scoped `TrustEnvironment` freezes
the exact finite required subset and validator set, as §9 does for `ROOT_TR_t`
and `ROOT_TR_c`; it contains no wildcard or unused target.  `TRB` lists exactly the service-use targets of `CAP(bounds)` and
`CAP(validate_bounds)` at `J_b` plus
`JUDGMENT_TRUST_TARGET(CONSISTENCY,(C_b))` for certificate kind
`CONTRADICTION_PROOF`.  `TRW` lists exactly the service-use targets of
`CAP(witness)` and `CAP(validate_witness)` at `J_w` plus
`JUDGMENT_TRUST_TARGET(CONSISTENCY,(C_w))` for
`SATISFYING_WITNESS`.  Each trusted-validator set and permitted-kind/target set
is exactly that enumeration and nonempty.  No wildcard is permitted.  Every
root producer is independent of its complete semantic subject, provider,
validator, and certificate producer set.

The five trust branches stay exact:

- admitted and correctly scoped root: compatible discovery may reach
  `CAPABILITY_DISCOVERED`, `INVOCABLE_FOR`, and one conformant completion;
- absent root: `TRUST_ROOT_ABSENT(exact key)`, capability incompatible, and
  `EVALUABILITY_MISSING`;
- `TRUST_ROOT_UNDECIDED`: `EVALUABILITY_UNKNOWN`, no invocation;
- `TRUST_ROOT_INCOMPATIBLE`: a nonempty exact mismatch-reason set, capability
  incompatible, and `EVALUABILITY_MISSING`;
- `TRUST_ROOT_FAILED`: exact homogeneous protocol- or transport-failure reason
  set, discovery failure, and no evaluability or semantic result.

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
                   RS(final),Anchor(evidence))
MD          = Atom(SP(dependency_metadata_changed),CH)
OCC(pat)    = Atom(SP(event_occurred),L(T(EventPattern),pat),Anchor(trace))
MATCH(pat,x)= Atom(SP(event_matches),L(T(EventPattern),pat),Var(x))
REFRESH_SCOPE(x) = Atom(SP(refresh_scope),Var(x))
REFRESH_OCC      = Atom(SP(refresh_occurred),Anchor(trace))

PATH_IN(P)  = PATH_CHANGE_IN(
                P,{CREATED_KIND,DELETED_KIND,MODIFIED_KIND})
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
| K0-C01 | `Require(TA(ts_win))` | `SF(snapshot_of)` and `SP(task_accepts)` at exact `CK`; exact typed literals | final/evidence; syntax roots plus the direct task meaning and verification schema; no false lower-call support | declared, bound, discovered, invocable, exact `TRUTH_TRUE` or honest unknown/error | `CAP(functions)` and `CAP(predicates)` with request-scoped admitted `TR` | final behavioral acceptance and supporting evidence, independent of production | task label, fixture ID, fixed patch, or exact-output oracle |
| K0-C02 | `Require(OBS_EQ(public_request_observation))` | `SF(snapshot_of)`, `SF(observe)`, and `SP(observations_equal)` at exact `CK` | pre/final; exact observation/type dependencies; empty evidence | well formed/closed; decisive true or false after successful term evaluation, otherwise exact A2 evaluation error | exact function/predicate capabilities and admitted service-use targets | relation to the supplied baseline rather than a fixed final list | final-only expected outputs or ambient baseline read |
| K0-C03 | `Require(Not(OCC(NET_ANY)))` | `SP(event_occurred)`, lower `SP(event_matches)`, and `EK(network_contact)` at exact `CK` | trace only; exact event/pattern declarations; no implicit final inference | closed/evaluable; false on a matching admitted event, true on none, error only by exact contract | predicate capability/root; event Delta admission is independent | trace history despite equal final snapshots | infer no contact from final state or caller event-class flag |
| K0-C04 | only `Authorize(p,x,REFRESH_SCOPE(x),MD)` | `SP(refresh_scope)`, `SP(dependency_metadata_changed)`, `SF(changes_between)`, and `EK(dependency_refresh)` at exact `CK` | event variable plus pre/final guard; change-set dependencies; no occurrence requirement | grant scope/condition is decisive or errors; empty trace remains authorization-compliant | exact predicate capability/root; separately admitted authority adoption | conditional permission without duty | turn may into must or evaluability into authority |
| K0-C05 | `Contract(Hard={Require(Implies(MD,REFRESH_OCC))}, Grants={Authorize(p,x,REFRESH_SCOPE(x),MD)}, PairRequirements={PAIR(refresh)})` | exact `PAIR(refresh)` and its two members at `CK`, plus `SP(dependency_metadata_changed)` | pre/final guard and trace occurrence; pair/member/event/type roots; definitional T3/A1, no evidence shortcut | closed only with pair binding/model; four K1 truth cases preserved | predicate capability/root; pair meaning is Sigma, not service availability | conditional obligation and necessary authority | permission-only rewrite, unlinked occurrence atom, or formula-as-term |
| K0-C06 | `Authorize(p,x,MATCH(MIGRATION,x),SCHEMA_CHANGED)` | `SP(event_matches)`, `SF(snapshot_of)`, `SF(observe)`, `SP(observations_equal)`, and `EK(path_change)` at exact `CK` | event variable and pre/final guard; exact paths, observations, and event payload | authorization result only; no occurrence obligation | exact evaluator/root and admitted authority fact | semantic condition, path scope, and optionality | edit whenever condition holds, untyped path, or host path access |
| K0-C07 | `Require(Any({TA(ts_toml),TA(ts_yaml)}))` | `SP(task_accepts)` and `T(Format)` at exact `CK` | final/evidence; exact task and verification dependencies | T3 alternatives; true if one succeeds, unknown/error preserved | exact predicate/root; no choice service | multiple acceptable outcomes without advance selection | fixture order, default format, or requiring both |
| K0-C08 | K1 `Choice(storage,T(StorageBackend),{LOCAL_STORAGE,HOSTED_STORAGE},user,none)` using admitted typed values | exact `T(StorageBackend)@CK` and literal declarations; no predicate result | choice/type/literal/authority dependencies; no evidence truth | `WELL_FORMED+OPEN_BINDINGS`; source binding remains `UNRESOLVED`; no Eval | no evaluator premise; only exact `BIND_CHOICE` authority can close | controller-owned discretion, separate from artifact format | default, executor ownership, factual unknown, or format/backend conflation |
| K0-C09 | `Contract(Hard={Require(VP(full_suite))}, Grants={Authorize(p,x,MATCH(RELEASE_ANY,x),VP(full_suite))})` | `SP(verification_passed)` and `EK(release)` at exact `CK`; typed verification/pattern literals | evidence and trace; exact schema/ref/event dependencies | before evidence `TRUTH_UNKNOWN`; pass/fail gives decisive completion; schema fault gives error | predicate capability with admitted root; release authority remains separate | factual uncertainty versus discretionary choice | missing evidence as pass, chosen test result, or opaque success token |
| K0-C10 | `Require(All({TA(ts_logging),Not(TA(ts_logging))}))` | the same exact `SP(task_accepts)` occurrence and dependencies in both positions | exact atom facets/evidence retained; K1 structure proves contradiction after closure | `WELL_FORMED+CLOSED+CONSISTENCY_UNSAT` by K-CONTRA | no plugin reasoner required; binding/model closure still required | formation versus consistency | malformed classification, atom substitution, or plugin case branch |
| K0-C11 | `Require(All({TA(ts_nonempty),TA(ts_lt_100),TA(ts_ge_200)}))` over exact `S_b` | direct `SP(task_accepts)`, `T(ByteSize)`, `T(ArtifactSelector)`, provider `CAP(bounds)`, independent `CAP(validate_bounds)`, and `BCERT` | final/evidence plus exact `R_b/E_b/D_b/J_b`, bounds fragments, envelope, derived validator request, and admitted result | only `CertificateAdmission.ADMITTED(BCERT,CONSISTENCY_UNSAT)` gives `CONSISTENCY_UNSAT`; absent/rejected gives unknown; failure gives error | exact `TRB` scopes provider use, validator use, and contradiction-certificate admission; validator/root producers are independent | constructible plugin-visible numeric contradiction with nonempty population and exact KiB values | numeric kernel rule, self-validation, validation proper back-edge, or lack-of-proof as satisfiable |
| K0-C12 | `Require(All({TA(ts_universal_latency),TA(ts_universal_memory)}))` | same reusable `SP(task_accepts)` at exact `CK` with typed universal observation specs | final/evidence; declared universal domains; sampled evidence insufficient | closed and locally evaluable; no witness/proof gives `CONSISTENCY_UNKNOWN` | concrete evaluator may be available; no complete joint capability claimed | capability-limited unresolved judgment | sampled success as universal witness or binary default |
| K0-C13 | `Require(Atom(LSP0,RS(final),Anchor(evidence)))` | exact `LDP0/LSP0` declaration exists; exact old binding absent; distinct `LP1` records exist; `CK` does not replace either | syntax derives the old exact declaration/binding key; all new-version evidence/services are irrelevant | exact `DECLARED+BINDING_ABSENT+DISCOVERY_BLOCKED_BY_BINDING+INVOCATION_BLOCKED_BY_BINDING`; public `WELL_FORMED+OPEN_BINDINGS`, no truth; old-version service absence would be `EVALUABILITY_MISSING` only after binding | no compatibility claim or migration is admitted | mandated semantic version | latest/name-only substitution or coding broad predicate standing in for policy |
| K0-C14 | K1 `All({coding reproducibility atom, foreign licensing atom})` | exact `SP(task_accepts)@CK` plus a distinct foreign plugin key/version | union of both syntax/semantic roots, services, evidence, and trust scopes | representable; local evaluability may coexist with `CONSISTENCY_UNKNOWN` jointly | no exact joint environment target/certificate is declared | cross-plugin composition and shared dependency uncertainty | local-SAT conjunction, redefined `All`, or task-specific kernel branch |
| K0-C15 | `Require(TA(ts_rubric))` with finite typed rubric and declared verification records | `SP(task_accepts)` at exact `CK` with exact direct meaning/model/capability identity | final/evidence; empty lower support; explicit access, unknown, error, schema contracts | closed; compatible rooted evaluator returns only exact bound `Eval` | `CAP(predicates)` exact binding target and admitted request root | useful reusable broad abstraction for arbitrary finite criteria | gold Contract, challenge ID, expected decision, hidden evaluator context |
| K0-C16 | the identical `Require(TA(ts_rubric))`, but capability absent or `TR` unusable | identical exact `SP(task_accepts)` meaning at `CK` | same facets/dependencies/evidence contract as the preceding row | `CLOSED+EVALUABILITY_MISSING`; no truth request completion | intentionally no compatible root-qualified evaluator | denotation versus service availability | meaningless/true/false/satisfied from evaluator absence |
| K0-C17 | two attributed copies of the same coding formula; only the authenticated source has matching `Adopt`/authority fact | coding symbols unchanged; exact K2 `SourceRef`, `AuthorityRef`, `AuthorityFactKey` differ by source/adoption | proposition deps equal; origins and authority bindings distinct; authentication evidence is not truth evidence | both provenance records remain; only admitted adoption enters `Hard`/`Grants` | exact external authority validator/trust path, not coding evaluator | identical content with different source authority | normative wording or provenance as authority |
| K0-C18 | both phrasings bind to `Require(OBS_EQ(public_command_observation))` | exact same `observe`, `snapshot_of`, `observations_equal` keys/version | identical formula deps/facets/result function; distinct origins retained | internal `==Eval` proof supports formula/acceptance equivalence; full Contract equivalence may fail on origins | exact closed environments; evaluator error gives no relation | semantic equivalence without provenance erasure | phrase-indexed symbol or source-string equality |
| K0-C19 | exact `C_w=Contract(Hard={Require(OBS_EQ(s_w)),Require(TA(t_w))}, ProfileRequirements={PK(implementation_evidence)})` | coding meanings/profile at `CK`, provider `CAP(witness)@AWK`, independent `CAP(validate_witness)@RVK`, and `WCERT` | exact `E_w/D_w/J_w`, abstract `O_w`, envelope/derived validator request, admitted evidence, and profile binding | only admitted `WCERT` gives `CONSISTENCY_SAT`; missing concrete dimension independently gives `PROFILE_INCOMPLETE` | exact `TRW` scopes provider, validator, and witness-certificate targets with complete producer independence | constructible abstract satisfaction versus concrete implementation evidence | no-known-patch as UNSAT, self-trusted witness, or witness as patch/construction oracle |
<!-- K0-COVERAGE-END -->

Coverage count: **19** rows, one per accepted seed label.

### 7.2 Exactly eight complete worked traces

#### Worked trace 1 — final-state acceptance with evidence

1. Delta contains exact `T(TaskSpec)`, `T(RepositorySnapshot)`,
   `T(VerificationSpec)`, `T(VerificationRecord)`, `DF(snapshot_of)`, and
   `DP(task_accepts)` declarations plus all recursively required type/literal
   declarations.  Declaration coordinates are `DECLARED`.
2. Sigma contains each exact binding, its complete ContractSpecs and model
   record.  K2 recomputes empty support for the direct `task_accepts` meaning;
   the relation nevertheless evaluates every finite criterion and required
   verification extensionally from its supplied `(task,F,E)`.  All binding
   coordinates are `SEMANTICALLY_BOUND`, and the Contract is `CLOSED` after
   exact authority adoption.
3. Discovery under the exact semantic/trust environments finds
   `CAP(functions)` and `CAP(predicates)` with admitted `TR`; both requests
   reach `INVOCABLE_FOR` and therefore `EVALUABILITY_AVAILABLE`.
4. `FINAL` projects to supplied snapshot `F`.  Evidence store `E` contains a
   schema-valid passing platform record bound to `SNAPSHOT_IDENTITY(F)`.
   Direct criterion evaluation returns its exact observation result; the
   mathematical verification subrelation returns
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
   selected observation differs makes the predicate complete `FALSE`.  A fixed
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
   and exact `SNAPSHOT_IDENTITY(F)`.  The same meaning on `(spec,F,E)` now returns
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
2. Exact request `R_b` discovers provider `CAP(bounds)` under `TRB`.  Envelope
   `BENV` binds `BCERT`, the complete subject/environment/dependencies,
   `BundleBoundsProof`, and independent validator `CAP(validate_bounds)`.
   The derived validator request uses the exact validator service-use and
   certificate-admission scopes.  Its producer is outside
   `{PLUGIN_PRODUCER(CK),ABI_PRODUCER(ABI0)}` and the root producer is outside
   subject/provider/validator/certificate producers.  Only
   `CertificateAdmission.ADMITTED(BCERT,CONSISTENCY_UNSAT)` yields UNSAT.
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

1. One finite `TaskSpec` and the exact `task_accepts` declaration, direct
   meaning, access/evidence/unknown/error contracts, empty support, and model
   record form a closed semantic environment.  No challenge label or expected
   result occurs in any record.
2. Under an exact admitted service-use root, `CAP(predicates)` targets that
   binding and the request reaches `INVOCABLE_FOR`.  The service receives only
   task, supplied final snapshot, and evidence store.  Exact equality to the
   total direct result for all finite criterion/verification multiplicities is
   required.
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
2. The adopted exact `C_w` also requires
   `PK(implementation_evidence)`.  `WENV` binds finite abstract `O_w`, exact
   `E_w/D_w/J_w`, provider `CAP(witness)`, independent
   `CAP(validate_witness)`, `TRW`, and `WCERT`.  Only the derived validator
   request and `CertificateAdmission.ADMITTED(WCERT,CONSISTENCY_SAT)` admit the
   witness; its payload uses Contract-derived `chi_C={}` and exact
   `AcceptEval=TRUE`.
3. The profile checker finds the abstract-acceptance dimension but a known
   omission of concrete-implementation evidence, yielding
   `PROFILE_INCOMPLETE`.  Both statuses coexist.
4. The unadopted quoted source remains provenance only.  Neither the satisfying
   witness nor the profile result identifies a patch, build, action sequence,
   repository transition, or implementation.

Trace count: **8** complete worked traces.

## 8. Relative minimality and separating cases

### 8.1 Exhaustive responsibility/minimality ledger

This ledger uses one reproducible grouping convention.  Count each Markdown
body row strictly between `K3S-LEDGER-BEGIN` and `K3S-LEDGER-END`, excluding
the header and separator.  A row may group fields or constructors only when it
lists the exhaustive member set, gives every member the same owner and
disposition, and no listed member occurs in another row.  Constructor fields,
declaration fields, binding fields, and derived result projections are distinct
members and therefore get distinct rows where their responsibilities differ.
K2 carrier fields not specialized here retain their accepted K2 disposition.

<!-- K3S-LEDGER-BEGIN -->
| Record or exact fields | Disposition | Owner | Semantic role / signature and facets | Dependencies | Evidence/access/failure boundary | Identity/version and omission | Consumer | seed cases | separating pair |
|---|---|---|---|---|---|---|---|---|---|
| `PathSegment.SEGMENT.segment_atom`; `Path.PATH.segments`; `PathSet` membership | `RETAINED_DELTA` | `CK` Delta value algebra | canonical root-relative path identity and finite scope | segment then path admission | no host access or truth | exact structural equality; inadmitted values malformed in use | snapshots/selectors | C02,C06 | A05.a: segment/path/set distinctions |
| all `ArtifactRole` tags and `OTHER_ROLE.role_atom` | `RETAINED_DELTA` | `CK` Delta value algebra | exact semantic artifact role | none | not authority or format | tag/payload equality | selectors/criteria | C04,C11 | A05.b: role versus path/format |
| all `Format` tags and `OTHER_FORMAT.format_atom` | `RETAINED_DELTA` | `CK` Delta value algebra | artifact representation format | none | not backend choice | tag/payload equality | artifact/format criterion | C07 | A05.c: format versus backend |
| `StorageBackend.{LOCAL_STORAGE,HOSTED_STORAGE}` | `RETAINED_DELTA` | `CK` Delta value algebra | controller-owned storage alternatives only | none | never artifact format | exact two-tag equality | K1 choice | C08 | A08.a: backend choice versus factual format |
| `ByteSize.KIB.integer`; `ContentIdentity.CONTENT_ID.atom`; `FieldId.FIELD.atom`; all `FieldValue` and `BehaviorValue` tags/payloads | `RETAINED_DELTA` | `CK` Delta value algebra | exact scalar and behavior fields | sort-local only | no untyped atom coercion | tag and payload equality | artifacts/observations | C01,C11,C19 | A05.d: size/field/behavior sort separation |
| four `ArtifactBody` tags and every payload; four `ArtifactContent` tags and every role/format/size field plus each content, fields-map, and observations-map payload field; total role/format/size/body projections | `RETAINED_DELTA` | `CK` Delta value algebra | exhaustive artifact content with total size/format | scalar roles/format/size/body | no filesystem or backend | complete tagged-field equality | snapshots/criteria | C01,C07,C11 | A05.e: each body/content constructor and projection |
| `RepositorySnapshot` map fields; `ChangeEntry.{CREATED.new,DELETED.old,MODIFIED.old,new}`; `ChangeSet` map fields | `RETAINED_DELTA` | `CK` Delta value algebra | complete state and difference-value domains | path/content | no plan/event | extensional maps; modified requires inequality | functions/criteria | C02,C04-C06 | A05.f: snapshot/change entry variants |
| three `ArtifactSelector` tags and all path/role fields | `RETAINED_DELTA` | `CK` Delta value algebra | finite supplied-snapshot selection | path set/role | no callback | tagged-field equality | observe/task/events | C01,C06,C11 | A05.g: paths versus role versus conjunction |
| all `ArtifactProjection`, `SubjectId`, `Coverage`, and `ObservationValue` tags/payloads | `RETAINED_DELTA` | `CK` Delta value algebra | typed observation coordinates/results | artifact/scalar types | no truth in an observation | tagged-field equality | observation records | C02,C12,C19 | A05.h: presence/content/behavior/coverage |
| five `ObservationSpec` tags and every selector/domain/metric/lanes/pairs field | `RETAINED_DELTA` | `CK` Delta value algebra | exhaustive requested projections | selector/subject/field | supplied snapshot only | tag plus complete fields | observe/task | C01,C02,C12,C19 | A04.a/A05.i: observation kinds and facets |
| four `ObservationResult` tags and every `{spec_identity,coverage,values}` field | `RETAINED_DELTA` | `CK` Delta value algebra | exhaustive finite typed observations | exact spec/domain/value | contains no truth | tag/full map equality; admission enforces coverage | equality/task | C01,C02,C18 | A04.b/A10.a: result tag/coverage distinctions |
| all `ObservationRelation` tags and bijection field | `RETAINED_DELTA` | `CK` Delta value algebra | exact comparison choice | result fields only | no callback/service | tag plus exact bijection | task criteria | C02,C12,C19 | A05.j: equality/order/correspondence |
| `VerificationStatus` tags; `VerificationSpec.{protocol_identity,subject,evidence_schema_key}`; `VerificationRecord.{spec,snapshot_identity,status,observation,evidence_refs}` | `RETAINED_DELTA` | `CK` Delta value algebra | exact snapshot-bound factual record | spec/snapshot/result/schema | evidence distinct from truth | full field equality; wrong snapshot never matches | verification/task | C01,C09,C15 | A10.b: pass/fail/inconclusive/snapshot |
| eight `Criterion` tags and every displayed field | `RETAINED_DELTA` | `CK` Delta value algebra | finite acceptance criteria, not task taxonomy | exact selector/spec/result/scalars | no service/expected answer | tag/full-field equality | direct task meaning | C01,C07,C11,C12,C19 | A09.a: every criterion constructor |
| `TaskSpec.TASK.{criteria,required_verifications}` | `RETAINED_DELTA` | `CK` Delta value algebra | arbitrary finite broad predicate input | criterion/verification types | no evaluator/case field | complete set equality | task meaning | C01,C15,C16 | A09.b: zero/one/many verification requirements |
| `ChangeKind` tags; seven `EventPattern` tags and every key/id/spec/status/path/kind/class/snapshot/selector field | `RETAINED_DELTA` | `CK` Delta value algebra | exhaustive structural event matching | event/payload value types | no command/endpoint | tag/full-field equality | event predicates/grants | C03-C06,C09 | A06.a: each event-pattern distinction |
| all six payload types, all eight payload tags, and every command/purpose/spec/snapshot/status/evidence/path/content/contact/release/selector field | `RETAINED_DELTA` | `CK` Delta value algebra | exhaustive typed trace payloads | listed value types | immutable event class external | tag/full-field equality | Outcome admission | C03-C06,C09 | A06.b: payload and actor/class separation |
| every `TypeDeclaration.{key,admitted_value_domain,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | admission of all section 3 value rows | exact finite type DAG | rejected value malformed | exact `T(n)@(1)`; absence malformed | all typed records | C01-C19 | A05.k: admission versus meaning |
| every literal `Declaration.{key,literal_identity,result_type,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | exact typed constants | result type | no meaning/service | structural `L(T,v)@(1)` | K1 literals | C07,C08,C15 | A03.a: declaration versus binding |
| three function `Declaration.{key,symbol_key,argument_types,result_type,facet_positions,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | exact ordered signatures/facets | displayed types | no meaning/service | exact DF/SF `(1)` | terms | C01,C02,C19 | A04.c: pre/final positions |
| eight predicate `Declaration.{key,symbol_key,argument_types,result_kind,facet_positions,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | exact Boolean signatures, including snapshot-bound verification | displayed types | no meaning/service | exact DP/SP `(1)` | atoms/grants | C01-C16 | A01/A09.c: kind and signature |
| six `EventDeclaration.{key,event_key,payload_type,event_class,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | immutable class/payload | payload types | caller cannot set class | exact DE/EK `(1)` | outcome/AuthEval | C03-C06,C09 | A06.c: controlled versus observational |
| `EventScopePairDeclaration.{pair_key,scope_symbol,occurrence_symbol,controlled_keys,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | exact refresh companion | members/event | no meaning/proof | exact pair `(1)` | conditional requirement | C04,C05 | A07/A15.a: pair declaration/binding separation |
| every literal `SemanticBinding` field | `RETAINED_SIGMA` | `CK` Sigma | exact `TERM_VALUE(v)` | declaration/spec roots | empty evidence/access; N/A unknown | derived key; absent open | literal evaluation/model | C07,C08 | A03.b: declaration is not meaning |
| all three function `SemanticBinding` fields | `RETAINED_SIGMA` | `CK` Sigma | exact deterministic `TermResult` | declaration/spec/support | typed input only | exact `(1)`; absent open | term evaluator | C01,C02 | A05.l: supplied snapshot only |
| all seven ordinary predicate `SemanticBinding` fields | `RETAINED_SIGMA` | `CK` Sigma | exact deterministic `Eval`; direct total task/verification meanings | declaration/spec/support | explicit schema/access/unknown/error | exact `(1)`; absent open | atom evaluator | C01-C16 | A09.d/A10.c: reuse and result families |
| `EventPairBinding` and complete pair-owned `OccurrenceBindingProjection` fields | `RETAINED_SIGMA` | `CK` Sigma | definitional T3/A1 occurrence | pair/scope/model/lifts | full Eval aggregation | no second ordinary binding | conditional event | C04,C05 | A15.b: semantic DAG versus validation |
| `ProfileBinding` fields and both `ProfileDimensionKey`s | `RETAINED_SIGMA` | `CK` Sigma | implementation evidence coverage | direct task result/evidence | five profile/failure outcomes | exact profile `(1)`; absent open | profile checker | C19 | A18.a: SAT versus profile |
| all Sigma meaning/profile `ContractSpec` fields, including direct task and snapshot-bound verification relations | `RETAINED_SIGMA` | `CK` Sigma | exact extensional denotations | exact support | explicit primary input only | exact key/role `(1)` | result validator | C01-C19 | A09.e: general relation versus oracle |
| all Sigma evidence-schema/access-boundary `ContractSpec` fields | `RETAINED_SIGMA` | `CK` Sigma | exact evidence admission/positional access | typed schema/support | undeclared access error | exact key/role `(1)` | evaluator/model | C01,C09,C15 | A05.m/A10.d: evidence/access |
| all Sigma unknown/evaluation/reasoning-error `ContractSpec` fields | `RETAINED_SIGMA` | `CK` Sigma | honest disjoint outcomes | no hidden support | nonempty stable reasons | exact key/role `(1)` | status boundary | C09,C12,C15 | A10.e: false/unknown/errors |
| every ordinary/pair `ModelContract` and `ModelCapabilitySummary` field | `RETAINED_SIGMA` | exact target projection | complete model/machine identity | binding contracts/descriptors | prose diagnostic only | named exact key; absent open/wrong malformed | model-facing lookup | C05,C13,C15 | A16: every projection field |
| verification `EvidenceRef.{issuer_scope,evidence_namespace,local_identity,schema_binding}` | `RETAINED_SIGMA` | K1 carrier under coding schema | stable support identity only | schema key | no embedded truth/authority | full identity equality | verification meaning | C01,C09,C15 | A10.f: record versus reference/truth |
| every field of `CS(SOUND_FRAGMENT,{functions,predicates,profile,bundle_bounds,adapter_witness,confluence_fixture})`, `CS(COMPLETE_FRAGMENT,bundle_bounds)`, `CS(REQUIRED_EVIDENCE,service)`, `CS(SERVICE_FAILURE_BEHAVIOR,service)`, `PSOUND`, `PCOMPLETE`, `PEVIDENCE`, and `PFAILURE` | `RETAINED_SERVICE` | owning service layer | exact target fragments and failure boundaries | exact target closures/two-node DAG | no denotation/truth shortcut | exact role/key; omission incompatible | capabilities | C01,C11,C19 | A11.a/A15.c: fragment/support distinctions |
| every field of `CAP(functions)`, `CAP(predicates)`, and `CAP(profile)` descriptors | `RETAINED_SERVICE` | `CK` Service | concrete binding/profile targets | complete closures | exact service-use roots | exact service/capability `(1)` | invocation | C01-C16,C19 | A03.c/A09.f: service availability |
| every field of provider descriptors `CAP(bounds)`, `CAP(confluence)`, and `CAP(witness)` | `RETAINED_SERVICE` | `CK`/`AWK` Service | exact finite environment targets | `D_b/D_c/D_w` | admitted proof or permitted inconclusive/error | exact target/version; no fallback | reasoning requests | C11,C19 | A11.b/A18.b: provider versus validator |
| every field of `CAP(validate_bounds)` and `CAP(validate_witness)` descriptors | `RETAINED_SERVICE` | independent `RVK` Service | exact certificate validation capabilities | complete subject dependency sets | separately trusted validation | exact validator/version; missing evaluability status | derived validator request | C11,C19 | A11.c/A18.c: producer independence |
| exact `ReasoningRequest` fields of `R_b` and `R_w`; exact confluence descriptor target `J_c` | `RETAINED_SERVICE` | request former | exact subject/environment/fragment/capability | `D_b/D_w/D_c` | no alternate `chi_C` | complete request identity | reasoner/certificate | C11,C19 | A11.d/A18.d: request-bound claim |
| `BCERT`/`WCERT` keys; every `CertificateEnvelope` field of `BENV`/`WENV`; every `BundleBoundsProof`/`AdapterWitness` payload field | `RETAINED_SERVICE` | `CK`/`AWK` certificate producer | exact contradiction/witness claims | full requests/environments/dependencies | exact validator/root/abstraction/evidence | certificate/key equality; no fallback | certificate gate | C11,C19 | A11.e/A18.e: kind-specific certificate |
| `TrustPolicyKey TP`; root keys `TR/TRB/TRW`; every admitted `TrustRootRecord` permission/owner/adoption field and all five `TrustRootJudgment` variants/reason fields | `RETAINED_SERVICE` | embedding policy | independent exact service/certificate trust | full producer sets | five branches distinct | exact policy/root versions | discovery/admission | C01,C11,C19 | A03.d/A13/A18.f: trust is not authority/self-trust |
| alternate pair-proof `PVC`, `PCERT`, complete occurrence bundle/envelope/root permissions supplied by §9 | `RETAINED_SERVICE` | independent pair-validator/certificate producers | exact independent pair admission fixture | pair subject plus validation references | rejection/failure proves nothing | exact fixture keys | pair validator | C05 | A15.d: supplied validation records are not derived away |
| `SNAPSHOT_IDENTITY(F)`, `changes_between(P,F)`, `observe(spec,F)`, and direct per-criterion/per-verification task projections | `DERIVED` | exact coding relations | total extensional outputs | supplied typed values | no ambient access | complete logical equality | meanings/payloads | C01-C19 | A04/A05/A09: derived output versus primitive assertion |
| K1 goal/preserve/forbid/allow/conditional/alternative patterns | `DERIVED` | K1 | exact macro/composition | syntax dependencies | K1 T1-T4/A1-A2 | no coding key | Contracts | C01-C09 | A06-A08: normative roles |
| K2 binding keys, supports, closures, observation maps, summaries, lifecycle, service identity, and validation-reference projections | `DERIVED` | K2 | mechanical views | exhaustive graph | owner-specific missing/error | cannot be supplied | validators | C01-C19 | A03/A14/A15: lifecycle/graph/conflict |
| derived `CertificateValidationRequest` fields and `CertificateAdmission`/receiving projections for BENV/WENV/pair fixture | `DERIVED` | K2 certificate gate | exact independent validation invocation/result | original request/envelope/root | failures yield no claim | derived identity only | reasoning/pair result | C05,C11,C19 | A11.f/A15.e/A18.g: producer request versus validator request |
| equal-duplicate coalescence, conflict sets, package/record permutation result, and `missingStatus` projection | `DERIVED` | K2 composition | order-independent exact outcome | record identities | no last-writer fallback | finite set/map equality | composition/K3-X | C01-C19 | A14: equality/conflict/order |
| exact two-node observation maps for the two valid confluence topological orders | `DERIVED` | K2 §3.3 | identical complete maps/results/statuses | `observe` and `changes_between` nodes | interface failure aborts | map equality | K3-X check 9 | C01,C02 | A15.f: independent order confluence |
| change set as patch/action sequence; event payload as executable command/endpoint | `EXCLUDED` | none | no declarative denotation | none | presence violates access boundary | never an identity | none | C03-C06,C19 | K3S-A18: satisfying semantics without implementation |
| universal string/map/opaque handle for path, task, evidence, result, or expected answer | `EXCLUDED` | none | destroys typed distinction | none | presence malformed/oracular | never an identity | none | C01,C02,C09,C15 | K3S-A05,A17: typed reusable values versus escape hatch |
| task taxonomy, phrase-indexed symbols, challenge IDs, expected mappings, gold Contracts/patches | `EXCLUDED` | none | no semantic role | none | presence rejects | never an identity | none | C01,C15,C18 | K3S-A17: equivalent phrasing shares symbols |
| implicit version/name/order fallback, plugin-owned truth/authority/choice/connective/failure rule | `EXCLUDED` | none | owned by K1/K2 or invalid | none | fail loud in owning family | never an identity | none | C04,C08,C10,C13,C17 | K3S-A01,A02,A13: exact identity and ownership |
| implementation, parser, binder, planner, executor, repository/filesystem/network operation, model/prompt/benchmark | `EXCLUDED` | none | outside K3-S | none | no semantic result | never an identity | none | C01-C19 | K3S-A18: abstract outcome is not construction |
<!-- K3S-LEDGER-END -->

Ledger count: **52** rows: 23 `RETAINED_DELTA`, 10 `RETAINED_SIGMA`,
8 `RETAINED_SERVICE`, 6 `DERIVED`, and 5 `EXCLUDED`, under the exact body-row
convention above.  The split is recomputable from the second cell alone.

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
| K3S-A08 | open controller-owned storage-backend choice and closed missing-suite fact | `ChoiceDecl`/authority records versus verification predicate/evidence schema | `OPEN_BINDINGS/UNRESOLVED` versus `TRUTH_UNKNOWN` | discretion/controller versus factual uncertainty | default choice, let evidence bind choice, or let principal choose fact |
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

The following lettered items are mandatory variants of those eighteen rows,
not additional cases.  Each variant reuses its parent `K3S-Axx` label.

- `A05.a-k` separately exercise: admitted versus inadmitted path segments and
  positional paths/path sets; every `ArtifactRole`; every `Format` plus the
  distinct two-tag `StorageBackend`; `ByteSize`, content, field, and behavior
  scalar sorts; all four `ArtifactContent` tags and every total projection;
  all three change entries; all three selectors; all projection, subject,
  coverage, and observation-value tags; all five observation-spec and four
  observation-result tags including exact incomplete domains; all five
  observation relations; every type-admission field; and all six payload
  types, including all three path-change tags.  Each paired variant differs in
  exactly the named tag or field and therefore cannot be accepted by an
  untyped map, a partial `size`/`format` projection, or a storage/format cast.
- `A09.a-e` use `TASK` values with zero criteria/verifications, one criterion
  and zero verifications, one verification, two distinct verifications, two
  criteria of the same tag, and one instance of each of the eight criterion
  tags.  All are constructible and
  determined by the direct three-input relation; the exact task observation
  map is empty in every variant.
- `A10.a-f` fix one verification spec and current snapshot, then use no
  record, an exact `INCONCLUSIVE`, exact `PASS`, exact `FAIL`, equal duplicate
  `PASS`, opposite decisive records, a wrong-snapshot `PASS`, and a
  wrong-schema record.  The results are respectively unknown, unknown, true,
  false, true, error, unknown, and error; evidence-reference equality and all
  complete `Eval` fields remain visible.
- `A11.a-f` separately remove or corrupt `R_b`, `BENV`, `BCERT`,
  `CAP(validate_bounds)`, `TRB`, its service-use target, its certificate target,
  the bounds payload, and the returned `CertificateAdmission`.  Only the exact
  fully formed and independently validated branch yields
  `ADMITTED(BCERT,CONSISTENCY_UNSAT)`; every other branch retains K2's exact
  no-admission, trust, evaluability, malformed, or failure family.
- `A13.a-d` separately vary `SourceRef`, authenticated provenance,
  `AuthorityRef`, exact admitted authority fact, service trust, and certificate
  trust.  No pair of those coordinates is interchangeable and none lets the
  subject producer, certificate producer, validator, or embedding-policy
  producer satisfy an independence inequality by self-assertion.
- `A14.a-d` permute the exact package sequence, each package's exact record
  sequence, equal duplicates, and unequal same-key records.  The first three
  preserve the complete result map; the last yields the same conflict set in
  either order.
- `A15.a-f` run both the retained definitional pair and the complete independent
  pair fixture in §9, omit each non-proper certificate/validator/root lookup in
  turn, reverse both valid topological orders, and add either a pair proper
  self-edge or a two-node proper back-edge.  Validation references never enter
  the semantic DAG; each genuine proper cycle is malformed.
- `A18.a-g` separately omit `R_w`, `WENV`, `WCERT`,
  `CAP(validate_witness)`, `TRW`, one exact trust target, the abstract outcome,
  and concrete implementation-profile evidence.  Only the complete independent
  certificate route establishes `CONSISTENCY_SAT`; even there the last
  omission leaves `PROFILE_INCOMPLETE`.

## 9. K3-X semantic input boundary

### 9.1 Smallest finite semantic packet

This section freezes semantic inputs only.  It does not select a language,
module, representation, path, command, output directory, test framework, or
implementation technique.

The packet contains the complete transitive type/declaration closure of every
section 2 value used below, including `T(StorageBackend)`, all four artifact
and observation-result tags, all six payload types, snapshot identity,
verification/task types, and their exact finite literal families.  It contains
all three function bindings; all seven ordinary predicate bindings; the
pair-owned occurrence projection; their ContractSpecs, exact supports,
closures, access/evidence/failure records, and complete model contracts.  It
contains all six event declarations, `PAIR(refresh)`, the profile record,
`CAP(functions)`, `CAP(predicates)`, `CAP(profile)`, `CAP(bounds)`,
`CAP(confluence)`, `CAP(witness)`, both reasoning-certificate validators, and
the pair validator frozen below.  Finally it contains the exact requests,
results, certificates, roots, environments, lifecycle coordinates, and
missing/conflict variants in §§9.2-9.5.  No declaration or support root needed
by one of those records is implicit.

Every fixture value is finite logical data: abstract segments/content,
snapshots, task/verification specs, EvidenceRefs, event payloads, exact keys,
root judgments, and complete result records.  None contains a host path, real
command, network endpoint, repository, expected patch, hidden answer, or
challenge ID.

### 9.2 Complete independent pair-proof fixture

The alternate fixture lives in a semantic environment distinct from the
retained definitional pair environment.  Fix these exact keys:

```text
PPK   = ((capknow.audit,pair-proof),(1))
PCERT = (PLUGIN_CERTIFICATE_ISSUER(PPK),coding.certificate,refresh_coherence)
PVK   = ((capknow.audit,pair-validator),(1))
PVSK  = (PVK,coding.validation,refresh,(1),PAIR_VALIDATION)
PVC   = (PVSK,refresh_full_eval)
TRP   = (TP,coding,pair-admission-root,(1))
```

Let `pd`, `sb`, and `od` be the exact section 3 `PAIR(refresh)` declaration,
`DP(refresh_scope)` binding, and `DP(refresh_occurred)` declaration.  Freeze
the following complete bundle; the names on the right are the exact K2 lift
records for these three fixed inputs; every field is fixed by the displayed
constructors:

```text
B_alt = OccurrenceSemanticContractBundle(
  meaning_contract=T3_A1_MEANING_LIFT(pd,sb),
  permitted_facet_inputs=({trace}),
  evidence_schema=T3_A1_EVIDENCE_LIFT(pd,sb),
  access_boundary=T3_A1_ACCESS_LIFT(pd,sb),
  unknown_contract=T3_A1_UNKNOWN_LIFT(pd,sb),
  evaluation_error_contract=T3_A1_ERROR_LIFT(pd,sb),
  determinism_rule=SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT,
  proper_semantic_dependencies=T3_A1_DEPENDENCY_LIFT(pd,sb),
  dependency_closure=least acyclic proper closure of that exact set)

PB_alt = EventPairBinding(
  pair_key=PAIR(refresh),
  scope_binding_key=DP(refresh_scope),
  occurrence_binding_key=DP(refresh_occurred),
  occurrence_model_contract_key=
    MC(BINDING_IDENTITY(DP(refresh_occurred)),refresh_occurred),
  admission=INDEPENDENT_COHERENCE_PROOF(B_alt,PCERT,PVC),
  proper_semantic_dependencies=the exact K2 pair roots for these fields,
  dependency_closure=their least acyclic proper closure)
```

`PSOUND`, `PCOMPLETE`, `PEVIDENCE`, and `PFAILURE` are four exact
`ContractSpec[Service]` records owned by `PVK`, with keys

```text
PSOUND.key    = (PVK,coding.validation.contract,refresh_sound,
                 (1),SOUND_FRAGMENT)
PCOMPLETE.key = (PVK,coding.validation.contract,refresh_complete,
                 (1),COMPLETE_FRAGMENT)
PEVIDENCE.key = (PVK,coding.validation.contract,refresh_evidence,
                 (1),REQUIRED_EVIDENCE)
PFAILURE.key  = (PVK,coding.validation.contract,refresh_failure,
                 (1),SERVICE_FAILURE_BEHAVIOR)
```

Each has owner `PVK`, owner layer `Service`, and role equal to its key's final
field.  `PSOUND` and `PCOMPLETE` have primary input `PairAdmissionRequest`,
codomain `IN_FRAGMENT|OUTSIDE_FRAGMENT`, the complete pair closure as their
query-map domain, and the exact relation that returns `IN_FRAGMENT` iff
`B_alt`'s complete `Eval` is equal to the K2 T3/A1 aggregate for every admitted
finite trace.
`PEVIDENCE` admits exactly the typed payload below and its displayed evidence
references; `PFAILURE` admits exactly the K2 pair-validation evaluation and
reasoning failure tags.  Their logical relations have no other branch, and
their supports are respectively the exact pair closure, the exact payload
references, and `{}`.

The complete `CapabilityDescriptor(PVC)` has ABI `ABI0`, plugin `PVK`, service
role `PAIR_VALIDATION`, class `COMPLETE_FOR_DECLARED_FRAGMENT`, judgments
`{EVENT_PAIR_COHERENCE_ADMISSION}`, targets `{PAIR_TARGET(PAIR(refresh))}`,
sound/complete fragments `PSOUND/PCOMPLETE`, dependency scope exactly the
transitive proper closure of the pair subject, required evidence `PEVIDENCE`,
required roots `{TRP}`, and failure contract `PFAILURE`; its proper
dependencies and closure are exactly the K2 derivation from those fields.

Let `E_p` be the complete semantic environment containing `PB_alt` and all
records reachable from the pair/member/model roots, with no ordinary
`SemanticBinding(DP(refresh_occurred))`.  Let `D_p` be its exact pair-request
dependency environment.  Its validation-reference set is exactly
`{VALIDATION_CERTIFICATE(PCERT),VALIDATION_CAPABILITY(PVC)}`; neither reference
is in `D_p.proper_dependencies` or its transitive proper closure.  Define

```text
U_p = SERVICE_USE_TRUST_TARGET(
        PVC,EVENT_PAIR_COHERENCE_ADMISSION,
        PAIR_USE(PAIR(refresh)),semanticIdentity(E_p))
A_p = PAIR_TRUST_TARGET(PAIR(refresh))
ROOT_p = TrustRootRecord(
  trust_root_key=TRP, owner=EMBEDDING_POLICY_PRODUCER(TP),
  trusted_validators={PVC},
  permitted_certificate_kinds={EVENT_PAIR_COHERENCE_PROOF},
  permitted_targets={U_p,A_p}, adoption=V0_EXTERNAL_TRUST_PREMISE)
T_p = TrustEnvironment(
  trust_policy_key=TP, policy_owner=EMBEDDING_POLICY_PRODUCER(TP),
  root_judgments={TRP -> TRUST_ROOT_ADMITTED(ROOT_p)})
R_p = PairAdmissionRequest(
  abi_version=ABI0, pair_key=PAIR(refresh), semantic_environment=E_p,
  trust_environment=T_p, complete_dependencies=D_p,
  capability_target=PAIR_TARGET(PAIR(refresh)), capability_key=PVC)
PairFullEvalProof = FULL_EVAL_EQUALITY(
  pair_key=PAIR(refresh), bundle_identity=IDENTITY_OF(B_alt),
  reference_contract=T3_A1_MEANING_LIFT(pd,sb),
  trace_domain=TYPED_DOMAIN(Trace),
  compared_fields={truth,evidence_refs,unknown_reasons,evaluation_errors})
PENV = CertificateEnvelope(
  certificate_key=PCERT, certificate_kind=EVENT_PAIR_COHERENCE_PROOF,
  request_binding=R_p, subjects=(PAIR(refresh),B_alt), environment=E_p,
  capability_key=PVC, fragment=PSOUND, dependencies=D_p,
  claimed_conclusion=PAIR_COHERENCE_ADMITTED(PAIR(refresh),PCERT),
  validator_key=PVC, trust_root_key=TRP, abstraction_class=SYMBOLIC,
  payload=PairFullEvalProof, evidence_refs={PAIR_PROOF_REF})
```

`PAIR_PROOF_REF` is exactly
`EvidenceRef(PLUGIN_ISSUER(PPK),coding.pair-proof,refresh_full_eval,
PSOUND.contract_key)` and is the sole reference admitted by `PEVIDENCE`.
K2 derives every field of `certificateValidationRequest(PENV)`; its validator
target is `PAIR_TARGET(PAIR(refresh))`, role is `PAIR_VALIDATION`, receiving
rule is `RECEIVE_PAIR_COHERENCE`, service-use target is `U_p`, and certificate
target is `A_p`.  The validation-filtered subject producer set is exactly
`{PLUGIN_PRODUCER(CK)}`.  The certificate, validator, and root producers are
respectively `PLUGIN_PRODUCER(PPK)`, `PLUGIN_PRODUCER(PVK)`, and
`EMBEDDING_POLICY_PRODUCER(TP)`, so every required independence inequality is
proper and no service/root/certificate is self-trusted.  Exact validation
yields only
`CertificateAdmission.ADMITTED(PCERT,
PAIR_COHERENCE_ADMITTED(PAIR(refresh),PCERT))`, received as that exact
`PairValidationResult`; only then is `PB_alt` semantically bound.

The alternate record and the retained definitional record are tested in
separate environments.  Their same-key inequality is therefore visible and
never coalesced.

### 9.3 Five exact trust-state fixtures

Fix admitted `t_t:T(TaskSpec)`, `F_t:T(RepositorySnapshot)`, and
`EVIDENCE_t:EvidenceStore`; let `E_t` and `D_t` be the complete exact semantic
and dependency environments of the direct `task_accepts` invocation.  For a
supplied trust environment `T`, define the otherwise identical request

```text
Q_t[T] = PredicateRequest(
  abi_version=ABI0, symbol_key=SP(task_accepts),
  binding_key=DP(task_accepts), semantic_environment=E_t,
  trust_environment=T, dependency_environment=D_t,
  arguments=(t_t,F_t,EVIDENCE_t),
  capability_target=BINDING_TARGET(DP(task_accepts)),
  capability_key=CAP(predicates))
U_t = SERVICE_USE_TRUST_TARGET(
  CAP(predicates),PREDICATE_EVALUATION,
  BINDING_USE(DP(task_accepts)),semanticIdentity(E_t))
```

The service-subject producer set is exactly `{PLUGIN_PRODUCER(CK)}` in all
five variants.  The root producer is exactly
`{EMBEDDING_POLICY_PRODUCER(TP)}` and the capability producer is exactly
`{PLUGIN_PRODUCER(CK)}`; these sets are disjoint.  Freeze

```text
ROOT_TR_t = TrustRootRecord(
  trust_root_key=TR, owner=EMBEDDING_POLICY_PRODUCER(TP),
  trusted_validators={CAP(predicates)},
  permitted_certificate_kinds={CONTRADICTION_PROOF},
  permitted_targets={U_t}, adoption=V0_EXTERNAL_TRUST_PREMISE)
```

The certificate-kind field is nonempty as K2 requires but grants no
certificate use because this record has no admission target.  The complete
five maps and outcomes are:

| fixture | exact `TrustEnvironment.root_judgments` entry at `TR` | exact scope/reason | lifecycle/evaluability result |
|---|---|---|---|
| `T_admitted` | `TRUST_ROOT_ADMITTED(ROOT_TR_t)` | `ROOT_TR_t` permits exactly target `U_t` | compatible discovery, then `CAPABILITY_DISCOVERED` and `INVOCABLE_FOR(Q_t[T_admitted])` |
| `T_absent` | `TRUST_ROOT_ABSENT(TR)` | key-only absence at policy `TP`; no target is usable | capability incompatible and `EVALUABILITY_MISSING` |
| `T_undecided` | `TRUST_ROOT_UNDECIDED(TR,{TrustRootStatusReason(ABI_REASON_ISSUER,ROOT_DISCOVERY_UNRESOLVED,TP,TR,CAP(predicates))})` | exact request capability and root coordinate; no request/result/environment in the reason | `EVALUABILITY_UNKNOWN`, no invocation |
| `T_incompatible` | `TRUST_ROOT_INCOMPATIBLE(TR,{TrustRootStatusReason(ABI_REASON_ISSUER,ROOT_TARGET_NOT_PERMITTED,TP,TR,CAP(predicates))})` | exact missing permission is `U_t` | capability incompatible and `EVALUABILITY_MISSING` |
| `T_failed` | `TRUST_ROOT_FAILED(TR,{TrustRootStatusReason(ABI_REASON_ISSUER,ROOT_DISCOVERY_PROTOCOL_FAILURE,TP,TR,CAP(predicates))})` | homogeneous protocol-failure family at the exact root/capability | exact `DISCOVERY_FAILED`, no evaluability result and no invocation |

Each `T_x` has fields `trust_policy_key=TP`,
`policy_owner=EMBEDDING_POLICY_PRODUCER(TP)`, and exactly the one displayed map
entry.  Thus the five request identities `Q_t[T_x]` differ only in the complete
trust-environment field.  None produces a logical `Eval` except a conformant
completion after the admitted branch becomes invocable.

### 9.4 Exhaustive missing-record fixture

For each row, start from the complete finite packet and remove exactly the
named required record/root; do not remove its referencing field.  Where K2's
total function is context-sensitive, the two contexts are separate frozen
subvariants in the final column.

The otherwise auxiliary keys/values used only to exercise the total missing
function are fixed as follows:

```text
m0 = (CK,coding.migration,missing_fixture,(1))
c0 = (CK,coding.compatibility,missing_fixture,(1))
x0 = (CK,coding.extension,optional_missing_fixture,(1))
x1 = (CK,coding.extension,required_missing_fixture,(1))
a0 = (CK,coding.alias,optional_missing_fixture)
a1 = (CK,coding.alias,required_missing_fixture)
C_choice = Contract(
  Hard={},Grants={},Choices={
    Choice(storage,T(StorageBackend),
           {LOCAL_STORAGE,HOSTED_STORAGE},user,none)},
  ProfileRequirements={},PairRequirements={})
cb0 = ChoiceBindingKey(IDENTITY_OF(C_choice),storage)
src0 = SourceRef(
  ABI_REASON_ISSUER,coding.fixture,storage_choice_source,{})
auth0 = AuthorityRef(
  ABI_REASON_ISSUER,coding.fixture,storage_choice_authority)
af0 = (auth0,src0,user,BIND_CHOICE(storage))
lk0 = LexicalBindingKey(
  LexicalScopeIdentity(PREDICATE_REQUEST,subjectOf(Q_t[T_admitted])),
  task_argument,T(TaskSpec))
e0 = EvidenceRef(
  PLUGIN_ISSUER(CK),coding.verification,missing_matrix_record,
  CS(EVIDENCE_SCHEMA,verification))
v0 = VERIFY(coding.missing-matrix,s_c,CS(EVIDENCE_SCHEMA,verification))
vr0 = VERIFICATION_RECORD(
  v0,SNAPSHOT_IDENTITY(F_c),PASS,O_c,{e0})
ev0 = EventValue(
  EK(dependency_refresh),DEPENDENCY_REFRESH(S_b,SNAPSHOT_IDENTITY(F_c)))
te0 = TraceEvent(ev0,user)
u0 = UnknownReason(
  PLUGIN_ISSUER(CK),coding.missing-matrix,(DP(task_accepts)))
```

| missing kind | exact fixture reference | exact `missingStatus` / resulting family |
|---|---|---|
| `ABI` | `ABI_RECORD(ABI0)` | `MALFORMED` |
| `PLUGIN` | `PACKAGE_RECORD(ABI0,CK)` | `MALFORMED` |
| `DECLARATION` | `DECLARATION_RECORD(DP(task_accepts))` | `MALFORMED` |
| `SYMBOL` | `SP(task_accepts)` from that declaration | `MALFORMED` |
| `EVENT` | `EVENT_VALUE_RECORD`'s required `EK(dependency_refresh)` declaration | `MALFORMED` |
| `PAIR_DECLARATION` | `PAIR_DECLARATION_RECORD(PAIR(refresh))` | `MALFORMED` |
| required Delta `CARRIER` | exact `vr0` required by `CS(EVIDENCE_SCHEMA,verification)` | `MALFORMED` |
| `BINDING` | `BINDING_RECORD(DP(task_accepts))` | `OPEN_BINDINGS` |
| `PROFILE_BINDING` | `PROFILE_BINDING_RECORD(PK(implementation_evidence))` | `OPEN_BINDINGS` |
| `PAIR_BINDING` | `PAIR_BINDING_RECORD(PAIR(refresh))` | `OPEN_BINDINGS` |
| `AUTHORITY_FACT` | `af0` | `OPEN_BINDINGS` |
| required `CHOICE_BINDING` | `cb0` | `OPEN_BINDINGS` |
| `LEXICAL_BINDING` | required `lk0`; the same key in a subject with no matching free variable | respectively `MALFORMED_REQUEST`; `OPEN_BINDINGS` only when the exact K1 closure premise names that unbound coordinate |
| `SERVICE` | `SERVICE_RECORD(SK(predicates))` | `EVALUABILITY_MISSING` |
| `CAPABILITY` | `CAPABILITY_RECORD(CAP(predicates))` | `EVALUABILITY_MISSING` |
| `TRUST_POLICY` | exact derived `TRUST_POLICY_RECORD(TP)` coordinate | `TRUST_ROOT_ABSENT` and no service use |
| `TRUST_ROOT` | `TRUST_ROOT_RECORD(TR)` required by `Q_t` | `TRUST_ROOT_ABSENT(TR)` and no service use |
| `CERTIFICATE` | `CERTIFICATE_RECORD(BCERT)` required by `R_b` | `NO_CERTIFICATE_ADMISSION`; no `CONSISTENCY_UNSAT` |
| `MIGRATION` | one exact referenced `MigrationKey m0` | `NO_MIGRATION(m0)` |
| `COMPATIBILITY_CLAIM` | one exact referenced `CompatibilityClaimKey c0` | `NO_COMPATIBILITY(c0)` |
| `SEMANTIC_EXTENSION` | exact optional extension `x0`; exact required offered extension `x1` | respectively `NO_EFFECT(x0)`; `INCOMPATIBLE(x1)` |
| `MODEL_CONTRACT` | model record for `DP(task_accepts)` | `OPEN_BINDINGS(model contract)` |
| `ALIAS` | unreferenced exact alias `a0`; required exact alias `a1` | respectively `NO_ALIAS(a0)`; `MALFORMED(missing alias a1)` |
| `CONTRACT_SPEC` | `CS(PREDICATE_MEANING,task_accepts)` | Sigma owner incompatibility and the binding stays open; a missing Service spec makes its descriptor incompatible |
| `REQUEST` | `REQUEST_RECORD(IDENTITY_OF(Q_t[T_admitted]))` at invocation | `MALFORMED_REQUEST` |
| `RESULT` | the completed result record for that exact request | exact `NO_RESULT_SENTINEL` protocol failure, with no returned truth |
| non-Delta environment `CARRIER` | each of `SEMANTIC_ENVIRONMENT_RECORD(E_t)`, `TRUST_ENVIRONMENT_RECORD(T_admitted)`, `DEPENDENCY_ENVIRONMENT_RECORD(D_t)`, and the required observation-environment record | `MALFORMED_REQUEST` when absent from request formation; an unequal completed projection is protocol failure |
| non-Delta lifecycle/value `CARRIER` | lifecycle coordinate of `Q_t[T_admitted]`; `O_w`; `ev0`; `te0`; `src0`; `auth0`; `e0`; `u0`; and the exact conflict of `d/d_bad` in §9.5 | respectively derived-coordinate nonconformance; malformed request; malformed event/trace/source/authority carriers; factual unknown for the absent referenced verification record; malformed result for an omitted required nonempty reason; and no independently omittable derived conflict record |

There is no generic carrier/result selector in this matrix: every retained K2
missing-status constructor has an exact named row or exhaustive named
subvariant, and none fabricates a semantic result.

### 9.5 Two-node confluence and permutation fixtures

Fix the already named `s_c,P_c,F_c,C_c,E_c,D_c,J_c` and define the two exact
node results

```text
N_o = BINDING(DF(observe))
N_d = BINDING(DF(changes_between))
V_o = TERM_VALUE(O_c)
V_d = TERM_VALUE(X_c)
M_c = {N_o -> V_o, N_d -> V_d}
```

The `CS(SOUND_FRAGMENT,confluence_fixture)` query at `N_o` is exactly
`TERM_RESULT` with input projection `(s_c,F_c)`; its query at `N_d` is exactly
`TERM_RESULT` with input projection `(P_c,F_c)`.  Both nodes have empty support
in this fixture, there is no edge between them, and the fragment relation
returns exactly `IN_FRAGMENT` on `M_c`.  Consequently both complete orders

```text
O_1 = [N_o,N_d]
O_2 = [N_d,N_o]
```

produce the identical complete `DependencyObservationEnvironment M_c` and the
identical relation result.  With the admitted §6.3 root for
`CAP(confluence)`, define the exact request

```text
R_c = ReasoningRequest(
  ABI0,CONSISTENCY,(C_c),E_c,T_c,
  CS(SOUND_FRAGMENT,confluence_fixture),D_c,J_c,CAP(confluence))
u_c = UnknownReason(
  PLUGIN_ISSUER(CK),coding.confluence.fixture_inconclusive,
  (IDENTITY_OF(C_c),IDENTITY_OF(M_c)))
Y_c = ReasoningResult.COMPLETED_INCONCLUSIVE({u_c})
```

where

```text
U_c = SERVICE_USE_TRUST_TARGET(
  CAP(confluence),CONSISTENCY,ENVIRONMENT_USE(CONSISTENCY,(C_c)),
  semanticIdentity(E_c))
ROOT_TR_c = TrustRootRecord(
  trust_root_key=TR, owner=EMBEDDING_POLICY_PRODUCER(TP),
  trusted_validators={CAP(confluence)},
  permitted_certificate_kinds={CONTRADICTION_PROOF},
  permitted_targets={U_c}, adoption=V0_EXTERNAL_TRUST_PREMISE)
T_c = TrustEnvironment(
  trust_policy_key=TP, policy_owner=EMBEDDING_POLICY_PRODUCER(TP),
  root_judgments={TR -> TRUST_ROOT_ADMITTED(ROOT_TR_c)})
```

The nonempty certificate-kind set grants no admission target.  Under both
orders, the exact status vector is
`(WELL_FORMED,CLOSED,CAPABILITY_DISCOVERED,INVOCABLE_FOR(R_c),COMPLETED(Y_c),
CONSISTENCY_UNKNOWN)`.  Adding `N_o -> N_d` still permits only `O_1`; adding
both `N_o -> N_d` and `N_d -> N_o`, or a self-edge, is `MALFORMED`.  This DAG
is independent of direct, empty-support `task_accepts`.

Let `PKG_CK`, `PKG_AWK`, `PKG_RVK`, `PKG_PPK`, and `PKG_PVK` denote the exact
complete finite K2 packages whose fields are the records frozen in §§3-6 and
§9.2 for their respective plugin keys.  Define the finite package set
`G={PKG_CK,PKG_AWK,PKG_RVK,PKG_PPK,PKG_PVK}` and two presentations

```text
Pi_pkg_1 = [PKG_CK,PKG_AWK,PKG_RVK,PKG_PPK,PKG_PVK]
Pi_pkg_2 = [PKG_PVK,PKG_PPK,PKG_RVK,PKG_AWK,PKG_CK]
```

For each package, its record set is exhaustively ordered first by the K2
`RecordIdentity` constructor order and then by complete identity-field tuple;
call that sequence `Pi_rec_1(P)` and its reversal `Pi_rec_2(P)`.  This is a
reproducible order over every record, not a name/display sort or an omitted
subset.  Composition of either package presentation and either record
presentation yields the same set `G`, environments, observation map `M_c`,
status vector, and result `Y_c`.

Finally, let `d` and `d'` be independently constructed complete equal copies
of the exact `DP(task_accepts)` declaration, and let `d_bad` have the same key
but the unequal two-argument signature omitting `EvidenceStore`.  Presentations
`[d,d']` and `[d',d]` coalesce to `d`; presentations `[d,d_bad]` and
`[d_bad,d]` yield the identical one-key conflict set and `MALFORMED`.  No last-
writer or package-order rule exists.

### 9.6 Mapping of all thirteen checks

| amendment check | K3-S symbols/records | adversarial cases | exact K1/K2 clauses and required outcome |
|---:|---|---|---|
| 1 | `snapshot_of`, `observe`, `verification_passed`, `task_accepts`, final snapshot/evidence fixtures | K3S-A04,A09,A10 | K1 §§2.3,3.1-3.2,4; K2 §§2.4,4.1-4.2,5.1-5.2: well formed, closed, evaluable, exact `TRUTH_TRUE` |
| 2 | exact `CK/T/DF/DP/SF/SP` constructors with independently built equal records and one forced kind collision | K3S-A01,A14 | K2 §§3.1,8.3: equal identities coalesce; owner/plugin/kind variants remain distinct; one-key unequal kind rejects |
| 3 | identical logical meaning at exact `(1)` and an exact `(2)` target | K3S-A02,A16 | K1 §§2.3,3.5; K2 §§3.4,4.3,8.2: agreement succeeds, mismatch rejects, no fallback |
| 4 | `DP(task_accepts)` declaration; environments omitting its binding or `CAP(predicates)` | K3S-A03,A09 | K1 §2.3; K2 §§2.4,8.1: declaration present/binding absent/capability absent are distinct coordinates |
| 5 | retained pair DAG plus complete `B_alt/PB_alt/R_p/PENV/PVC/TRP` independent fixture and a true proper back-edge | K3S-A15 | K2 §§3.3,7.2: exact validation refs stay mandatory/non-proper; admitted proof closes; genuine semantic self-edge/cycle malformed |
| 6 | the five complete `Q_t[T_x]` requests, exact root reasons/scopes, and producer sets in §9.3 | K3S-A03,A13 | K2 §§2.3-2.4,5.4,8.1: admitted -> usable; absent -> exact missing/evaluability missing; undecided -> evaluability unknown; incompatible -> evaluability missing; failed -> exact discovery failure and no fabricated K1 result |
| 7 | task result fixtures, malformed unequal Eval, and bounds-reasoner result/failure | K3S-A10,A11 | K1 §§4,5.3; K2 §§5.2-5.4,6.3: false, logical unknown, evaluation error, reasoning error, malformed result stay distinct |
| 8 | network prohibition and exact release/refresh grants/pair | K3S-A06,A07 | K1 §§3.2-3.4; K2 §7.1: hard trace truth and authority are independent; evaluability grants no authority |
| 9 | independent `N_o/N_d` confluence DAG with `O_1/O_2`, exact `M_c/Y_c`, and both package/record presentations | K3S-A09,A14,A15 | K2 §§1.1,3.3,7.5,8.3: both topological orders yield the identical complete map/status; package/record permutations do likewise; direct `task_accepts` remains empty-support |
| 10 | equal duplicate declarations/bindings/models and one unequal same-key variant in reversed order | K3S-A14 | K2 §§1.1,8.3: equality coalesces and conflict is order-independent |
| 11 | every exact row and context subvariant of the exhaustive §9.4 missing-record matrix | K3S-A03,A15,A16 | K2 §3.3 `missingStatus` and §2.4 lifecycle: every missing kind yields only its displayed malformed/open/evaluability/trust/no-admission/protocol family |
| 12 | the entire finite packet and every derived identity/result map | K3S-A14 | K1 §4.8; K2 §§1.1,3.3,5.2: exact finite equality, deterministic meanings, set semantics, and source binding permit replay only after the later clean-commit gate |
| 13 | task predicate variant requesting ambient repository/evidence/expected-answer state | K3S-A05,A09,A17 | K1 §§1.2,2.2,3.1; K2 §§3.3,4.2,5.1: invalid observation/access is rejected before a truth can be used |

### 9.7 Intentionally excluded executable branches

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
