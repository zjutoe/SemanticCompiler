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
                BEHAVIOR_METRIC(metric : FieldId, value : integer) |
                BEHAVIOR_RESOLUTION(ContentIdentity) |
                BEHAVIOR_CORRESPONDENCE(
                  finite map(FieldId -> FieldValue),
                  finite map(FieldId -> FieldValue))
ArtifactBody =
    TEXT_BODY(ContentIdentity)
  | STRUCTURED_BODY(finite map(FieldId -> FieldValue))
  | OPAQUE_BODY(ContentIdentity)
  | BEHAVIOR_BODY(finite map(SubjectId -> BehaviorValue))
ArtifactBodyKind = TEXT_BODY_KIND | STRUCTURED_BODY_KIND |
                   OPAQUE_BODY_KIND | BEHAVIOR_BODY_KIND

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
    ABSENT | ROLE_MISMATCH(actual : ArtifactRole, required : ArtifactRole) |
    PROJECTION_MISMATCH(actual : ArtifactBodyKind,
                        required : ArtifactProjection) |
    PRESENT | PRESENT_CONTENT(ArtifactContent) | PRESENT_FORMAT(Format) |
    PRESENT_SIZE(ByteSize) | PRESENT_FIELD(FieldValue) |
    ACCEPTED | REJECTED | METRIC_VALUE(integer) |
    RESOLUTION_VALUE(ContentIdentity) |
    CORRESPONDENCE_VALUE(finite map(FieldId -> FieldValue),
                         finite map(FieldId -> FieldValue)) |
    BEHAVIOR_CONFLICT(nonempty finset(BehaviorValue))

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
matching tag.  Artifact selection is the following total equation, where
`role(F[p])` is the total `artifact_role` projection:

```text
selector_domain(SELECT_PATHS(P),F) = P
selector_domain(SELECT_ROLE(r),F) = {p in dom(F) | role(F[p])=r}
selector_domain(SELECT_PATHS_WITH_ROLE(P,r),F) = P

selected_value(SELECT_PATHS(_),projection,p,F) =
  ABSENT                                      if p notin dom(F)
  project(projection,F[p])                   otherwise
selected_value(SELECT_ROLE(r),projection,p,F) =
  project(projection,F[p])                   (domain already proves role=r)
selected_value(SELECT_PATHS_WITH_ROLE(_,r),projection,p,F) =
  ABSENT                                      if p notin dom(F)
  ROLE_MISMATCH(role(F[p]),r)                 if role(F[p]) != r
  project(projection,F[p])                   otherwise
```

`project(PRESENCE,a)=PRESENT`, `project(CONTENT,a)=PRESENT_CONTENT(a)`,
`project(FORMAT_ONLY,a)=PRESENT_FORMAT(artifact_format(a))`, and
`project(SIZE_ONLY,a)=PRESENT_SIZE(artifact_size(a))`.
`project(STRUCTURED_FIELD(f),STRUCTURED_ARTIFACT(...,M))` is
`PRESENT_FIELD(M[f])` when `f` is present and `ABSENT` otherwise; on any other
artifact constructor it is
`PROJECTION_MISMATCH(body_kind(artifact_body(a)),STRUCTURED_FIELD(f))`, where
`body_kind` is the total tag projection.  This is rejected as an evaluation
error by any criterion that needs a field value.

An `ObservationResult` is admitted only when its result tag matches the spec
tag, `spec_identity` is exact, all keys have the required sort, and its value
constructors match the projection.  `PRESENCE` permits
`ABSENT|ROLE_MISMATCH|PRESENT`; `CONTENT` permits
`ABSENT|ROLE_MISMATCH|PRESENT_CONTENT`; `FORMAT_ONLY` permits
`ABSENT|ROLE_MISMATCH|PRESENT_FORMAT`; `SIZE_ONLY` permits
`ABSENT|ROLE_MISMATCH|PRESENT_SIZE`; and `STRUCTURED_FIELD` permits
`ABSENT|ROLE_MISMATCH|PROJECTION_MISMATCH|PRESENT_FIELD`.  Its map domain is exactly
`selector_domain(selector,F)`, so absent requested paths and present
wrong-role paths are both explicit and distinct.

For every non-artifact view and subject `s`, let `raw(F,s)` be the finite set
of exact `BehaviorValue`s found at key `s` in every
`BEHAVIOR_ARTIFACT(...,observations)` in `F`.  Define the view-specific
candidate set and total aggregate:

```text
candidates(REQUEST_BEHAVIOR_VIEW(_),s,F) =
  raw(F,s) intersect {BEHAVIOR_ACCEPTED,BEHAVIOR_REJECTED}
candidates(WORKLOAD_METRIC_VIEW(_,m),s,F) =
  {BEHAVIOR_METRIC(m,n) in raw(F,s)}
candidates(DEPENDENCY_RESOLUTION_VIEW(_,_),s,F) =
  {BEHAVIOR_RESOLUTION(c) in raw(F,s)}
candidates(CLIENT_ADAPTER_VIEW(_),s,F) =
  {BEHAVIOR_CORRESPONDENCE(L,R) in raw(F,s)}

aggregate(V) = MISSING                          if V={}
aggregate({BEHAVIOR_ACCEPTED}) = ACCEPTED
aggregate({BEHAVIOR_REJECTED}) = REJECTED
aggregate({BEHAVIOR_METRIC(m,n)}) = METRIC_VALUE(n)
aggregate({BEHAVIOR_RESOLUTION(c)}) = RESOLUTION_VALUE(c)
aggregate({BEHAVIOR_CORRESPONDENCE(L,R)}) = CORRESPONDENCE_VALUE(L,R)
aggregate(V) = BEHAVIOR_CONFLICT(V)             otherwise
```

Because `raw` and `candidates` are sets, equal duplicate artifact claims
coalesce and two or more unequal matching claims deterministically produce the
same `BEHAVIOR_CONFLICT`, independent of artifact or package order.  A metric
view selects only the exact requested `FieldId`; a differently keyed metric is
nonmatching rather than silently used.  Request results permit only
`ACCEPTED|REJECTED|BEHAVIOR_CONFLICT`; workload results only
`METRIC_VALUE|BEHAVIOR_CONFLICT`; lane results only
`RESOLUTION_VALUE|BEHAVIOR_CONFLICT`; and client results only
`CORRESPONDENCE_VALUE|BEHAVIOR_CONFLICT`.

For each of these four views, the result map contains exactly the declared
subjects whose aggregate is not `MISSING`.  It is `COMPLETE` iff none is
missing.  Otherwise `INCOMPLETE_SUBJECTS(M)` has the exact nonempty set
`M={s in declared_domain | aggregate(candidates(view,s,F))=MISSING}` and the
map domain is the declared domain minus `M`.  A conflict is a present map
value, not missing coverage; any task criterion needing it returns the stable
schema/conflict `Eval.ERROR`.  These equations exhaust every admitted view,
subject, value constructor, absence, role mismatch, duplicate, and conflict.

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

ImplementationEvidence =
    ABSTRACT_ACCEPTANCE_EVIDENCE(
      contract_identity : ContractIdentity,
      snapshot_identity : SnapshotIdentity,
      certificate_key : CertificateKey)
  | CONCRETE_IMPLEMENTATION_EVIDENCE(
      contract_identity : ContractIdentity,
      snapshot_identity : SnapshotIdentity,
      implementation_identity : implementation_evidence_atom)
  | DIMENSION_EVIDENCE_PENDING(
      contract_identity : ContractIdentity,
      snapshot_identity : SnapshotIdentity,
      dimension : ProfileDimensionKey,
      reason : UnknownReason)
CodingEvidencePayload =
    VERIFICATION_EVIDENCE(VerificationRecord)
  | IMPLEMENTATION_PROFILE_EVIDENCE(ImplementationEvidence)
CodingEvidenceEntry = EVIDENCE_ENTRY(
  reference : EvidenceRef, payload : CodingEvidencePayload)
AbstractCoverageResult = NO_ABSTRACT_RESULT |
                         ABSTRACT_REASONING_RESULT(ReasoningResult)
ImplementationCoverageSubject = IMPLEMENTATION_COVERAGE_SUBJECT(
  contract_identity : ContractIdentity,
  task : TaskSpec,
  snapshot : RepositorySnapshot,
  evidence_store : EvidenceStore,
  task_result : Eval,
  abstract_result : AbstractCoverageResult)

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

PairTraceDomain = ALL_ADMITTED_TRACES
PairComparedFields = COMPLETE_EVAL_RECORD
AuthorityClauseTag = BOUNDS_CLAUSE | CONFLUENCE_OBSERVATION_CLAUSE |
  CONFLUENCE_CHANGE_CLAUSE | ADAPTER_PRESERVATION_CLAUSE |
  ADAPTER_ACCEPTANCE_CLAUSE
AuthorityAttestationSubjectIdentity =
    CLAUSE_ATTESTATION_SUBJECT(contract_identity : ContractIdentity,
                               clause_tag : AuthorityClauseTag)
  | CHOICE_ATTESTATION_SUBJECT(contract_identity : ContractIdentity,
                               choice_id : ChoiceId)
AuthorityAttestationValue = AUTHORITY_ATTESTATION_VALUE(
  authority_ref : AuthorityRef,
  source_ref : SourceRef,
  principal : Principal,
  normative_role : NormativeRole,
  subject_identity : AuthorityAttestationSubjectIdentity)

ServiceAdmissionSubject =
    FUNCTION_CALL_SUBJECT(binding : BindingKey,
                          arguments : finite sequence(Value))
  | PREDICATE_CALL_SUBJECT(binding : BindingKey,
                           arguments : finite sequence(Value))
  | PROFILE_CALL_SUBJECT(profile : ProfileKey,
                         subject : ImplementationCoverageSubject)
  | BOUNDS_SUBJECT(selector : ArtifactSelector,
                   nonempty_task : TaskSpec,
                   upper_task : TaskSpec,
                   lower_task : TaskSpec)
  | CONFLUENCE_SUBJECT(spec : ObservationSpec,
                       pre : RepositorySnapshot,
                       final : RepositorySnapshot)
  | ADAPTER_WITNESS_SUBJECT(contract_identity : ContractIdentity,
                            observation : ObservationSpec,
                            task : TaskSpec,
                            pre : RepositorySnapshot,
                            final : RepositorySnapshot)
  | PAIR_COHERENCE_SUBJECT(pair : EventScopePairKey,
                           scope_binding : BindingKey,
                           occurrence_binding : BindingKey,
                           trace_domain : PairTraceDomain,
                           compared_fields : PairComparedFields)
  | AUTHORITY_ATTESTATION_SUBJECT(
      authority_fact_key : AuthorityFactKey,
      attestation : AuthorityAttestationValue,
      offered_evidence_refs : finset(EvidenceRef))

EvolutionAdmissionSubject =
    MIGRATION_RELATION_SUBJECT(
      migration_key : MigrationKey,
      source_identity : SemanticEnvironmentIdentity,
      target_identity : SemanticEnvironmentIdentity,
      relation : FULL_CONTRACT_EQUIVALENCE | ACCEPTANCE_EQUIVALENCE |
                 FORMULA_EQUIVALENCE | EXPLICIT_SEMANTIC_CHANGE)
  | COMPATIBILITY_CLAIM_SUBJECT(
      claim_key : CompatibilityClaimKey,
      source_abi : AbiVersion, target_abi : AbiVersion,
      source_keys : finset(DependencyKey),
      target_keys : finset(DependencyKey))
  | SEMANTIC_EXTENSION_SUBJECT_VALUE(
      extension_key : SemanticExtensionKey,
      target_record_identity : RecordIdentity,
      owner_layer : Delta | Sigma | Service)
```

These seven admitted value sorts are closed first-order algebras.  A
`PairTraceDomain` value is admitted iff it is the literal tag
`ALL_ADMITTED_TRACES`; a `PairComparedFields` value is admitted iff it is the
literal tag `COMPLETE_EVAL_RECORD`.  An `AuthorityClauseTag` value is admitted
iff it is one of its five displayed nullary tags.  An
`AuthorityAttestationSubjectIdentity` is admitted iff it is one of its two
displayed tags and every field has its displayed frozen K1/K2 sort.  An
`AuthorityAttestationValue` is admitted iff it has the displayed record tag
and all five fields are admitted at their displayed sorts.  A
`ServiceAdmissionSubject` or `EvolutionAdmissionSubject` is admitted iff it
has one displayed tag and every field is admitted at its displayed sort.
Equality for all seven sorts is tag equality followed by exact componentwise
field equality; there is no raw field-name, prose sort, open map, subtyping, or
coercion rule.  They contain no `ContractSpec`,
`OccurrenceSemanticContractBundle`, `SemanticEnvironment`, `AliasBinding`,
trust record, request, result, or relation value.  The environment identity in
a migration subject is the finite K2 identity already derived from the
separately carried environments; it is not the environment record and is
never dereferenced by a `ContractSpec`.

A `VerificationRecord` is admitted only when its observation has exact
`spec.subject` identity, its evidence references bind the displayed evidence
schema, and its fields have the displayed types.  It remains evidence, not a
truth value.  The coding projection of a supplied K1 `EvidenceStore E` is an
exact finite set `coding_entries(E)` of `CodingEvidenceEntry` values.  Entry
equality is complete field equality.  Equal entries coalesce.  Grouping by
`reference`, define the total result algebra and equation

```text
CodingEvidenceProjection =
    EVIDENCE_MAP(finite map(EvidenceRef -> CodingEvidencePayload))
  | EVIDENCE_CONFLICT(nonempty finset(EvidenceReferenceConflict))
EvidenceReferenceConflict = EVIDENCE_REFERENCE_CONFLICT(
  reference : EvidenceRef,
  payloads : nonempty finset(CodingEvidencePayload))
groups(E,e)={i.payload | i in coding_entries(E), i.reference=e}
conflicts(E)={EVIDENCE_REFERENCE_CONFLICT(e,groups(E,e)) |
              e in references(coding_entries(E)), |groups(E,e)|>1}
coding_projection(E)=EVIDENCE_CONFLICT(conflicts(E)) if conflicts(E)!={}
coding_projection(E)=EVIDENCE_MAP(
  {e->the unique member of groups(E,e) |
   e in references(coding_entries(E))})                 otherwise
evidence_map(E)=M iff coding_projection(E)=EVIDENCE_MAP(M)
```

Thus two unequal payloads for one exact `EvidenceRef` produce one exact
conflict member; any number of equal duplicates coalesces.  Consumers treat
the `EVIDENCE_CONFLICT` branch as the exact schema/conflict `Eval.ERROR` and
never select a map from it.  There is no first/last-record rule.

Exact schema membership is total.  A `VERIFICATION_EVIDENCE(r)` entry is
admitted only when its reference has
`schema_binding=CS(EVIDENCE_SCHEMA,verification)`, its reference is a member
of `r.evidence_refs`, and `r` is admitted.  An
`IMPLEMENTATION_PROFILE_EVIDENCE(i)` entry is admitted only when its reference
has `schema_binding=CS(EVIDENCE_SCHEMA,implementation_profile)` and every field
of `i` is admitted.  A schema/payload mismatch, a referenced record omitting
the indexing reference, an inadmitted payload, or an unequal same-reference
payload is the exact evidence-schema/conflict evaluation error.  Foreign
schema references are outside `coding_entries(E)` and cannot satisfy a coding
predicate.  Thus membership, reference, schema, uniqueness, duplicate, and
conflict behavior are finite and exact; an `EvidenceRef` still contains no
truth, authority, consistency, or profile conclusion.

Criterion admission additionally requires the obvious matching
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

For current supplied snapshot `F`, `verification_passed(v,F,E)` first requires
the unique `evidence_map(E)`.  It selects exactly the map entries
`(e,VERIFICATION_EVIDENCE(r))` satisfying all four equations
`r.spec=v`, `r.snapshot_identity=SNAPSHOT_IDENTITY(F)`,
`r.observation.spec_identity=v.subject`, and `e in r.evidence_refs`.
Wrong-spec, wrong-snapshot, implementation-profile, and foreign-schema entries
are nonmatching evidence, never success.  A malformed schema/reference or any
`EVIDENCE_REFERENCE_CONFLICT` returns the exact `Eval.ERROR`.  Let `M` be the
finite matching set.  If both a `PASS` and a `FAIL` occur in `M`, return the
stable opposite-decisive-record conflict `Eval.ERROR`.  Otherwise a `FAIL`
returns `VALUE(FALSE,refs(M),inconclusiveReasons(M))`; a `PASS` returns
`VALUE(TRUE,refs(M),inconclusiveReasons(M))`; and no decisive record returns
`VALUE(UNKNOWN,refs(M),missingOrInconclusiveReasons(v,F,M))`.  The last reason
set is nonempty.  These cases are disjoint and exhaustive for every admitted
finite store.

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

`dependency_metadata_changed(X)` is total and returns true exactly when at
least one `(p,e)` in `X` satisfies the following role equation:

```text
metadata_role(CREATED(new))      = artifact_role(new)=DEPENDENCY_METADATA
metadata_role(DELETED(old))      = artifact_role(old)=DEPENDENCY_METADATA
metadata_role(MODIFIED(old,new)) =
  artifact_role(old)=DEPENDENCY_METADATA OR
  artifact_role(new)=DEPENDENCY_METADATA
dependency_metadata_changed(X) = ANY(metadata_role(e) | (_,e) in X)
```

The empty change set is false.  A modification from metadata to another role
and a modification from another role to metadata are both true; neither side
is silently preferred.

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
| `T(ArtifactBodyKind)` | exact four artifact-body tag projections | `{}` |
| `T(ArtifactContent)` | exact four tagged artifact constructors | `{DECLARATION(T(ArtifactRole)),DECLARATION(T(Format)),DECLARATION(T(ByteSize)),DECLARATION(T(ContentIdentity)),DECLARATION(T(FieldId)),DECLARATION(T(FieldValue)),DECLARATION(T(SubjectId)),DECLARATION(T(BehaviorValue))}` |
| `T(ObservationValue)` | exact closed observation-value constructors | `{DECLARATION(T(ArtifactRole)),DECLARATION(T(ArtifactBodyKind)),DECLARATION(T(ArtifactProjection)),DECLARATION(T(ArtifactContent)),DECLARATION(T(BehaviorValue)),DECLARATION(T(Format)),DECLARATION(T(ByteSize)),DECLARATION(T(FieldId)),DECLARATION(T(FieldValue)),DECLARATION(T(ContentIdentity))}` |
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
| `T(ImplementationEvidence)` | exact abstract/concrete/pending profile-evidence constructors | `{DECLARATION(T(SnapshotIdentity))}` |
| `T(CodingEvidencePayload)` | exact verification/profile payload variants | `{DECLARATION(T(VerificationRecord)),DECLARATION(T(ImplementationEvidence))}` |
| `T(CodingEvidenceEntry)` | exact reference/payload entries | `{DECLARATION(T(CodingEvidencePayload))}` |
| `T(AbstractCoverageResult)` | no result or one exact K2 reasoning-result carrier | `{}` |
| `T(ImplementationCoverageSubject)` | exact profile subject fields | `{DECLARATION(T(TaskSpec)),DECLARATION(T(RepositorySnapshot)),DECLARATION(T(AbstractCoverageResult))}` |
| `T(PairTraceDomain)` | exactly the literal tag `ALL_ADMITTED_TRACES` | `{}` |
| `T(PairComparedFields)` | exactly the literal tag `COMPLETE_EVAL_RECORD` | `{}` |
| `T(AuthorityClauseTag)` | exactly the five displayed authority-clause tags | `{}` |
| `T(AuthorityAttestationSubjectIdentity)` | exact clause/choice subject-identity constructors and fields | `{DECLARATION(T(AuthorityClauseTag))}` |
| `T(AuthorityAttestationValue)` | exact five-field attestation record | `{DECLARATION(T(AuthorityAttestationSubjectIdentity))}` |
| `T(ServiceAdmissionSubject)` | exact eight field-explicit service-subject constructors; no contract, bundle, environment, alias, trust, request, or result record | `{DECLARATION(T(TaskSpec)),DECLARATION(T(RepositorySnapshot)),DECLARATION(T(ObservationSpec)),DECLARATION(T(ArtifactSelector)),DECLARATION(T(ImplementationCoverageSubject)),DECLARATION(T(PairTraceDomain)),DECLARATION(T(PairComparedFields)),DECLARATION(T(AuthorityAttestationValue))}` |
| `T(EvolutionAdmissionSubject)` | exact migration/compatibility/extension subject-value constructors containing only finite K2 identities, keys, relation tag, and owner tag | `{}` |
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
`CS(EVALUATION_ERROR_BEHAVIOR,literal)`, and model-contract key
`MC(BINDING_IDENTITY(L(T,v)),literal)`.  Its complete `MODEL_LITERAL(T,v)`
record has exact signature `()->T`, empty
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
| `CS(PREDICATE_MEANING,dependency_metadata_changed)` | Sigma / `PREDICATE_MEANING` | change set -> the exact total `CREATED(new)`, `DELETED(old)`, and `MODIFIED(old,new)` role equation in §2.2 | `{}` |
| `CS(PREDICATE_MEANING,event_matches)` | Sigma / `PREDICATE_MEANING` | pattern/event value -> exact structural match; keys outside the pattern are false | `{}` |
| `CS(PREDICATE_MEANING,event_occurred)` | Sigma / `PREDICATE_MEANING` | pattern/trace -> K1 `ANY_RESULT` over `event_matches(pattern,event_value)` in trace order-insensitive set aggregation | `{BINDING(DP(event_matches))->EVAL_RESULT_SEQUENCE}` |
| `CS(PREDICATE_MEANING,refresh_scope)` | Sigma / `PREDICATE_MEANING` | event value -> true exactly for admitted `EK(dependency_refresh)` payloads whose selector is the exact `DEPENDENCY_LOCK` artifact role, false for every other admitted event | `{}` |
| `CS(PROFILE_COVERAGE,implementation_evidence)` | Sigma / `PROFILE_COVERAGE` | exact `ImplementationCoverageSubject -> ProfileResult` by the total dimension equation below, with the supplied `task_result` required to equal direct `task_accepts` | `{BINDING(DP(task_accepts))->EVAL_RESULT}` |
| `CS(EVIDENCE_SCHEMA,none)` | Sigma / `EVIDENCE_SCHEMA` | explicit inputs -> only empty evidence-reference set admitted | `{}` |
| `CS(EVIDENCE_SCHEMA,verification)` | Sigma / `EVIDENCE_SCHEMA` | `EvidenceStore ->` exactly the unique map entries whose references and `VERIFICATION_EVIDENCE` payloads satisfy §2.1 | `{DECLARATION(T(CodingEvidenceEntry))->TYPE_ADMISSION_FACT}` |
| `CS(EVIDENCE_SCHEMA,implementation_profile)` | Sigma / `EVIDENCE_SCHEMA` | `EvidenceStore ->` exactly the unique map entries whose references and `IMPLEMENTATION_PROFILE_EVIDENCE` payloads satisfy §2.1 | `{DECLARATION(T(CodingEvidenceEntry))->TYPE_ADMISSION_FACT}` |
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
| `FSOUND` | Service / `SOUND_FRAGMENT` | `T(ServiceAdmissionSubject)->{IN_FRAGMENT,OUTSIDE_FRAGMENT}`; in exactly for the three admitted `FUNCTION_CALL_SUBJECT` families | literal `{}` |
| `QSOUND` | Service / `SOUND_FRAGMENT` | `T(ServiceAdmissionSubject)->{IN_FRAGMENT,OUTSIDE_FRAGMENT}`; in exactly for the eight admitted `PREDICATE_CALL_SUBJECT` families | literal `{}` |
| `PROFSOUND` | Service / `SOUND_FRAGMENT` | `T(ServiceAdmissionSubject)->{IN_FRAGMENT,OUTSIDE_FRAGMENT}`; in exactly for `PROFILE_CALL_SUBJECT(PK(implementation_evidence),s)` with admitted `s` | literal `{}` |
| `BSOUND`, `BCOMPLETE` | Service / `SOUND_FRAGMENT`, `COMPLETE_FRAGMENT` | `T(ServiceAdmissionSubject)->{IN_FRAGMENT,OUTSIDE_FRAGMENT}`; in exactly for `BOUNDS_SUBJECT(S_b,ts_nonempty,ts_lt_100,ts_ge_200)` | literal `{}` |
| `WSOUND` | Service / `SOUND_FRAGMENT` | `T(ServiceAdmissionSubject)->{IN_FRAGMENT,OUTSIDE_FRAGMENT}`; in exactly for `ADAPTER_WITNESS_SUBJECT(IDENTITY_OF(C_w),s_w,t_w,P_w,F_w)` | literal `{}` |
| `CSOUND` | Service / `SOUND_FRAGMENT` | `T(ServiceAdmissionSubject)->{IN_FRAGMENT,OUTSIDE_FRAGMENT}`; relation consumes only its two legal lower `TERM_OBS` values | literal `{N_o->(TERM_RESULT,project_observe),N_d->(TERM_RESULT,project_changes)}` |
| `FREQ`, `QREQ`, `PROFREQ`, `BREQ`, `CREQ`, `WREQ` | Service / `REQUIRED_EVIDENCE` | fixed `(T(ServiceAdmissionSubject),finset(EvidenceRef))->{ADMISSIBLE,INADMISSIBLE}` relation for the named capability family | literal `{}` for every record |
| `FFAIL`, `QFAIL`, `PROFFAIL`, `BFAIL`, `CFAIL`, `WFAIL` | Service / `SERVICE_FAILURE_BEHAVIOR` | fixed `InterfaceFailure` primary input to respectively the exact `TermResult.TERM_ERROR`, `Eval.ERROR`, `ProfileResult.EVALUATION_ERROR`, or `ReasoningResult.REASONING_ERROR` codomain, using only K2 §5.4 role projection | literal `{}` for every record |

The records in the Service rows are field-explicit as follows.  Each
`SERVICE_SPEC` expands to one complete K2 record, and the final two arguments
are respectively its literal `observation_queries` map and its relation; no
record receives a closure, environment, binding, model, contract, authority,
choice, or trust value as primary input.

```text
SERVICE_SPEC(key,role,domain,codomain,queries,relation) = ContractSpec(
  contract_key=key,owner_layer=Service,contract_role=role,
  primary_input_domain=domain,codomain=codomain,
  observation_queries=queries,logical_relation=relation)

FSOUND=SERVICE_SPEC(CS(SOUND_FRAGMENT,functions),SOUND_FRAGMENT,
  T(ServiceAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  FUNCTION_CALL_SUBJECT(k,args)->IN_FRAGMENT exactly when
    k in {DF(snapshot_of),DF(changes_between),DF(observe)} and args are
    admitted positionally by k; every other admitted subject->OUTSIDE_FRAGMENT)
QSOUND=SERVICE_SPEC(CS(SOUND_FRAGMENT,predicates),SOUND_FRAGMENT,
  T(ServiceAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  PREDICATE_CALL_SUBJECT(k,args)->IN_FRAGMENT exactly when
    k in {DP(observations_equal),DP(task_accepts),
          DP(dependency_metadata_changed),DP(verification_passed),
          DP(event_matches),DP(event_occurred),DP(refresh_scope),
          DP(refresh_occurred)} and args are admitted positionally by k;
    every other admitted subject->OUTSIDE_FRAGMENT)
PROFSOUND=SERVICE_SPEC(CS(SOUND_FRAGMENT,profile),SOUND_FRAGMENT,
  T(ServiceAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  PROFILE_CALL_SUBJECT(PK(implementation_evidence),s)->IN_FRAGMENT for every
    admitted ImplementationCoverageSubject s;
  every other admitted subject->OUTSIDE_FRAGMENT)
BSOUND=SERVICE_SPEC(CS(SOUND_FRAGMENT,bundle_bounds),SOUND_FRAGMENT,
  T(ServiceAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  BOUNDS_SUBJECT(S_b,ts_nonempty,ts_lt_100,ts_ge_200)->IN_FRAGMENT;
  every unequal admitted subject->OUTSIDE_FRAGMENT)
BCOMPLETE=SERVICE_SPEC(CS(COMPLETE_FRAGMENT,bundle_bounds),COMPLETE_FRAGMENT,
  T(ServiceAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  the identical BSOUND relation)
WSOUND=SERVICE_SPEC(CS(SOUND_FRAGMENT,adapter_witness),SOUND_FRAGMENT,
  T(ServiceAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  ADAPTER_WITNESS_SUBJECT(IDENTITY_OF(C_w),s_w,t_w,P_w,F_w)->IN_FRAGMENT;
  every unequal admitted subject->OUTSIDE_FRAGMENT)

project_observe(x)=
  (s,F) when x=CONFLUENCE_SUBJECT(s,P,F);
  (s_c,F_c) for every other admitted ServiceAdmissionSubject x
project_changes(x)=
  (P,F) when x=CONFLUENCE_SUBJECT(s,P,F);
  (P_c,F_c) for every other admitted ServiceAdmissionSubject x
Q_c_obs=(expected_kind=TERM_RESULT,input_projection=project_observe)
Q_c_changes=(expected_kind=TERM_RESULT,input_projection=project_changes)
CSOUND=SERVICE_SPEC(CS(SOUND_FRAGMENT,confluence_fixture),SOUND_FRAGMENT,
  T(ServiceAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},
  {N_o->Q_c_obs,N_d->Q_c_changes},
  (CONFLUENCE_SUBJECT(s_c,P_c,F_c),O)->IN_FRAGMENT exactly when
    O={N_o->TERM_OBS(TERM_VALUE(O_c)),
       N_d->TERM_OBS(TERM_VALUE(X_c))};
  every other admitted `(subject,O)`->OUTSIDE_FRAGMENT)

FREQ=SERVICE_SPEC(CS(REQUIRED_EVIDENCE,functions),REQUIRED_EVIDENCE,
  (T(ServiceAdmissionSubject),finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (FUNCTION_CALL_SUBJECT(k,args),{})->ADMISSIBLE exactly when
    k in {DF(snapshot_of),DF(changes_between),DF(observe)} and args are
    admitted positionally by k; every other admitted input->INADMISSIBLE)
QREQ=SERVICE_SPEC(CS(REQUIRED_EVIDENCE,predicates),REQUIRED_EVIDENCE,
  (T(ServiceAdmissionSubject),finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (PREDICATE_CALL_SUBJECT(k,args),refs)->ADMISSIBLE exactly when
    k is one of the eight keys enumerated in the `QSOUND` relation, args are
    admitted positionally by k, and refs equal the evidence references fixed
    by the key's evidence-schema rule; every other input->INADMISSIBLE)
PROFREQ=SERVICE_SPEC(CS(REQUIRED_EVIDENCE,profile),REQUIRED_EVIDENCE,
  (T(ServiceAdmissionSubject),finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (PROFILE_CALL_SUBJECT(PK(implementation_evidence),s),refs)->ADMISSIBLE
    exactly when refs are the coding profile references in s.evidence_store;
  every other input->INADMISSIBLE)
BREQ=SERVICE_SPEC(CS(REQUIRED_EVIDENCE,bounds),REQUIRED_EVIDENCE,
  (T(ServiceAdmissionSubject),finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (BOUNDS_SUBJECT(S_b,ts_nonempty,ts_lt_100,ts_ge_200),{BPROOF_REF})
    ->ADMISSIBLE; every other input->INADMISSIBLE)
CREQ=SERVICE_SPEC(CS(REQUIRED_EVIDENCE,confluence),REQUIRED_EVIDENCE,
  (T(ServiceAdmissionSubject),finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (CONFLUENCE_SUBJECT(s_c,P_c,F_c),{})->ADMISSIBLE;
  every other input->INADMISSIBLE)
WREQ=SERVICE_SPEC(CS(REQUIRED_EVIDENCE,witness),REQUIRED_EVIDENCE,
  (T(ServiceAdmissionSubject),finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (ADAPTER_WITNESS_SUBJECT(IDENTITY_OF(C_w),s_w,t_w,P_w,F_w),
   {WPROOF_REF})->ADMISSIBLE; every other input->INADMISSIBLE)

FFAIL=SERVICE_SPEC(CS(SERVICE_FAILURE_BEHAVIOR,functions),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,TermResult.TERM_ERROR,{},
  F->the exact K2 FUNCTION_EVALUATION failure projection of F)
QFAIL=SERVICE_SPEC(CS(SERVICE_FAILURE_BEHAVIOR,predicates),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,Eval.ERROR,{},
  F->the exact K2 PREDICATE_EVALUATION failure projection of F)
PROFFAIL=SERVICE_SPEC(CS(SERVICE_FAILURE_BEHAVIOR,profile),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,ProfileResult.EVALUATION_ERROR,{},
  F->the exact K2 PROFILE_CONCRETE failure projection of F)
BFAIL=SERVICE_SPEC(CS(SERVICE_FAILURE_BEHAVIOR,bounds),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,ReasoningResult.REASONING_ERROR,{},
  F->the exact K2 REASONING failure projection of F)
CFAIL=SERVICE_SPEC(CS(SERVICE_FAILURE_BEHAVIOR,confluence),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,ReasoningResult.REASONING_ERROR,{},
  F->the exact K2 REASONING failure projection of F)
WFAIL=SERVICE_SPEC(CS(SERVICE_FAILURE_BEHAVIOR,witness),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,ReasoningResult.REASONING_ERROR,{},
  F->the exact K2 REASONING failure projection of F)
```

`N_o` and `N_d` are the two exact binding keys defined in §9.5.  Both query
kinds are legal for a Service `SOUND_FRAGMENT`, and both projections are total
on the fixed `CONFLUENCE_SUBJECT` primary domain.  The `CSOUND` relation reads
only the two displayed `TERM_OBS` values.  All other Service specifications
have literal empty query maps and therefore consume only their field-explicit
primary input.  This is the complete query map for every retained core Service
specification; no `MODEL_CONTRACT`, `CONTRACT_SPEC`, or other forbidden key is
queried.

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

Profile coverage is also a total extensional relation, not a prose checker.
Write

```text
P_impl = PK(implementation_evidence)
d_abs  = (P_impl,abstract_acceptance_evidence)
d_conc = (P_impl,concrete_implementation_evidence)
D_impl = {d_abs,d_conc}
```

For admitted subject
`s=IMPLEMENTATION_COVERAGE_SUBJECT(cid,t,F,E,r,a)`, first construct the exact
`evidence_map(E)` and exact direct `r_expected=task_accepts(t,F,E)`.  A map
schema/reference/conflict error or `r != r_expected` returns
`ProfileResult.EVALUATION_ERROR` with the corresponding stable nonempty error
set.  If `r_expected=Eval.ERROR(R,_,_)`, return
`ProfileResult.EVALUATION_ERROR(R)`.  Otherwise define:

```text
abstract_acceptance_evidence(e,s) iff
  evidence_map(E)[e] = IMPLEMENTATION_PROFILE_EVIDENCE(
    ABSTRACT_ACCEPTANCE_EVIDENCE(cid,SNAPSHOT_IDENTITY(F),c))
  and e.schema_binding = CS(EVIDENCE_SCHEMA,implementation_profile)
  and a = ABSTRACT_REASONING_RESULT(
            ADMITTED_JUDGMENT(CONSISTENCY_SAT,c))

concrete_implementation_evidence(e,s) iff
  evidence_map(E)[e] = IMPLEMENTATION_PROFILE_EVIDENCE(
    CONCRETE_IMPLEMENTATION_EVIDENCE(
      cid,SNAPSHOT_IDENTITY(F),implementation_identity))
  and e.schema_binding = CS(EVIDENCE_SCHEMA,implementation_profile)

covered(s) =
  ({d_abs}  if some e satisfies abstract_acceptance_evidence(e,s) else {})
  union
  ({d_conc} if some e satisfies concrete_implementation_evidence(e,s) else {})

pending(s) = {d in D_impl |
  some e has evidence_map(E)[e] = IMPLEMENTATION_PROFILE_EVIDENCE(
    DIMENSION_EVIDENCE_PENDING(cid,SNAPSHOT_IDENTITY(F),d,u))}
missing(s) = D_impl minus covered(s)
```

The evidence-reference set of `PROFILE_COMPLETE` is exactly all references
witnessing the two predicates above.  If `missing(s)={}`, return that exact
`PROFILE_COMPLETE`.  If `missing(s) intersect pending(s)` is nonempty, or
`r_expected` is `VALUE(UNKNOWN,_,U)`, or `a` is
`ABSTRACT_REASONING_RESULT(COMPLETED_INCONCLUSIVE(U))`, return
`PROFILE_UNKNOWN(P_impl,U_profile)`, where `U_profile` is the nonempty exact
union of the displayed task, reasoning, and pending reasons.  Otherwise return
`PROFILE_INCOMPLETE(P_impl,missing(s))`; the set is necessarily nonempty and
is the complete omitted-dimension set, never one selected omission.

An `a=NO_ABSTRACT_RESULT`, a different admitted abstract result/certificate,
or an abstract evidence payload with a different contract or snapshot is
nonmatching and leaves `d_abs`
in `missing`; a concrete payload with a different contract or snapshot is
likewise nonmatching.  If such a mismatched payload uses the exact same
reference as a matching payload, the store conflict rule returns evaluation
error.  Any other admitted reasoning-result tag is decisive but covers no
abstract dimension.  The symbolic profile service may itself return
`REASONING_ERROR`; concrete invocation/protocol failure returns
`EVALUATION_ERROR`; neither is produced by this coverage relation and neither
is converted to profile unknown.  These equations cover every admitted
subject field, both dimensions, complete, exact incomplete, unknown, and both
failure families.

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
separate `CSOUND` record has exactly two independent
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
`CS(EVIDENCE_SCHEMA,implementation_profile)`, derived support on `task_accepts`,
`evidence_pending`, `profile` evaluation error, and `profile` reasoning error.
Its missing binding is open;
checker absence gives no profile result.

The package names used below denote these two complete records:

```text
PB_refresh=EventPairBinding(
  pair_key=PAIR(refresh),scope_binding_key=DP(refresh_scope),
  occurrence_binding_key=DP(refresh_occurred),
  occurrence_model_contract_key=
    MC(BINDING_IDENTITY(DP(refresh_occurred)),refresh_occurred),
  admission=DEFINITIONAL_T3_A1,
  proper_semantic_dependencies={
    PAIR_DECLARATION(PAIR(refresh)),BINDING(DP(refresh_scope)),
    BINDING(DP(refresh_occurred)),
    MODEL_CONTRACT(
      MC(BINDING_IDENTITY(DP(refresh_occurred)),refresh_occurred))},
  dependency_closure=the least acyclic proper closure of that literal set)
PROFILE_impl=ProfileBinding(
  profile_key=PK(implementation_evidence),
  dimensions={
    (PK(implementation_evidence),abstract_acceptance_evidence),
    (PK(implementation_evidence),concrete_implementation_evidence)},
  coverage_meaning=CS(PROFILE_COVERAGE,implementation_evidence),
  evidence_schema=CS(EVIDENCE_SCHEMA,implementation_profile),
  proper_semantic_dependencies={
    CONTRACT_SPEC(CS(PROFILE_COVERAGE,implementation_evidence)),
    CONTRACT_SPEC(CS(EVIDENCE_SCHEMA,implementation_profile)),
    CONTRACT_SPEC(CS(UNKNOWN_BEHAVIOR,evidence_pending)),
    CONTRACT_SPEC(CS(EVALUATION_ERROR_BEHAVIOR,profile)),
    CONTRACT_SPEC(CS(REASONING_ERROR_BEHAVIOR,profile))},
  dependency_closure=the least acyclic proper closure of that literal set,
  unknown_contract=CS(UNKNOWN_BEHAVIOR,evidence_pending),
  evaluation_error_contract=CS(EVALUATION_ERROR_BEHAVIOR,profile),
  reasoning_error_contract=CS(REASONING_ERROR_BEHAVIOR,profile))
```

### 4.3 Exact model/machine identity

`MC(target,name)` is only a `ModelContractKey`.  A record position always uses
the following complete record, never that bare key:

```text
MODEL(binding_key,name,symbol,signature,facets,evidence,unknown,error,
      meaning_key,summaries) = ModelContract(
  model_contract_key=MC(BINDING_IDENTITY(binding_key),name),
  target_binding_key=binding_key,
  exact_symbol_key=symbol,
  exact_signature=signature,
  exact_facet_positions=facets,
  evidence_contract=evidence,
  unknown_contract=unknown,
  error_contract=error,
  capability_summaries=summaries,
  semantic_contract_reference=meaning_key,
  explanatory_text=ABSENT)

MODEL_LITERAL(T,v) = MODEL(
  L(T,v),literal,NO_SYMBOL_LITERAL,()->T,(),
  CS(EVIDENCE_SCHEMA,none),CS(UNKNOWN_BEHAVIOR,not_applicable),
  CS(EVALUATION_ERROR_BEHAVIOR,literal),
  CS(LITERAL_MEANING,literal.T.v).contract_key,{})

MODEL_snapshot_of = MODEL(
  DF(snapshot_of),snapshot_of,SF(snapshot_of),
  (State)->T(RepositorySnapshot),({pre,final}),
  CS(EVIDENCE_SCHEMA,none),CS(UNKNOWN_BEHAVIOR,not_applicable),
  CS(EVALUATION_ERROR_BEHAVIOR,term),
  CS(FUNCTION_MEANING,snapshot_of).contract_key,
  {modelCapabilitySummary(CAP(functions))})
MODEL_changes_between = MODEL(
  DF(changes_between),changes_between,SF(changes_between),
  (T(RepositorySnapshot),T(RepositorySnapshot))->T(ChangeSet),
  ({pre},{final}),CS(EVIDENCE_SCHEMA,none),
  CS(UNKNOWN_BEHAVIOR,not_applicable),
  CS(EVALUATION_ERROR_BEHAVIOR,term),
  CS(FUNCTION_MEANING,changes_between).contract_key,
  {modelCapabilitySummary(CAP(functions))})
MODEL_observe = MODEL(
  DF(observe),observe,SF(observe),
  (T(ObservationSpec),T(RepositorySnapshot))->T(ObservationResult),
  ({},{pre,final}),CS(EVIDENCE_SCHEMA,none),
  CS(UNKNOWN_BEHAVIOR,not_applicable),
  CS(EVALUATION_ERROR_BEHAVIOR,term),
  CS(FUNCTION_MEANING,observe).contract_key,
  {modelCapabilitySummary(CAP(functions))})
```

The eight predicate records are the following field-complete calls (the final
singleton in each ordinary row is literal, not a lower bound):

```text
MODEL_observations_equal = MODEL(
  DP(observations_equal),observations_equal,SP(observations_equal),
  (T(ObservationResult),T(ObservationResult))->Bool,({pre},{final}),
  CS(EVIDENCE_SCHEMA,none),CS(UNKNOWN_BEHAVIOR,never),
  CS(EVALUATION_ERROR_BEHAVIOR,predicate),
  CS(PREDICATE_MEANING,observations_equal).contract_key,
  {modelCapabilitySummary(CAP(predicates))})
MODEL_task_accepts = MODEL(
  DP(task_accepts),task_accepts,SP(task_accepts),
  (T(TaskSpec),T(RepositorySnapshot),EvidenceStore)->Bool,
  ({},{final},{evidence}),CS(EVIDENCE_SCHEMA,verification),
  CS(UNKNOWN_BEHAVIOR,task),CS(EVALUATION_ERROR_BEHAVIOR,predicate),
  CS(PREDICATE_MEANING,task_accepts).contract_key,
  {modelCapabilitySummary(CAP(predicates))})
MODEL_dependency_metadata_changed = MODEL(
  DP(dependency_metadata_changed),dependency_metadata_changed,
  SP(dependency_metadata_changed),(T(ChangeSet))->Bool,({pre,final}),
  CS(EVIDENCE_SCHEMA,none),CS(UNKNOWN_BEHAVIOR,never),
  CS(EVALUATION_ERROR_BEHAVIOR,predicate),
  CS(PREDICATE_MEANING,dependency_metadata_changed).contract_key,
  {modelCapabilitySummary(CAP(predicates))})
MODEL_verification_passed = MODEL(
  DP(verification_passed),verification_passed,SP(verification_passed),
  (T(VerificationSpec),T(RepositorySnapshot),EvidenceStore)->Bool,
  ({},{final},{evidence}),CS(EVIDENCE_SCHEMA,verification),
  CS(UNKNOWN_BEHAVIOR,evidence_pending),
  CS(EVALUATION_ERROR_BEHAVIOR,predicate),
  CS(PREDICATE_MEANING,verification_passed).contract_key,
  {modelCapabilitySummary(CAP(predicates))})
MODEL_event_matches = MODEL(
  DP(event_matches),event_matches,SP(event_matches),
  (T(EventPattern),EventValue)->Bool,({},{}),CS(EVIDENCE_SCHEMA,none),
  CS(UNKNOWN_BEHAVIOR,never),CS(EVALUATION_ERROR_BEHAVIOR,predicate),
  CS(PREDICATE_MEANING,event_matches).contract_key,
  {modelCapabilitySummary(CAP(predicates))})
MODEL_event_occurred = MODEL(
  DP(event_occurred),event_occurred,SP(event_occurred),
  (T(EventPattern),Trace)->Bool,({},{trace}),CS(EVIDENCE_SCHEMA,none),
  CS(UNKNOWN_BEHAVIOR,never),CS(EVALUATION_ERROR_BEHAVIOR,predicate),
  CS(PREDICATE_MEANING,event_occurred).contract_key,
  {modelCapabilitySummary(CAP(predicates))})
MODEL_refresh_scope = MODEL(
  DP(refresh_scope),refresh_scope,SP(refresh_scope),(EventValue)->Bool,({}),
  CS(EVIDENCE_SCHEMA,none),CS(UNKNOWN_BEHAVIOR,never),
  CS(EVALUATION_ERROR_BEHAVIOR,predicate),
  CS(PREDICATE_MEANING,refresh_scope).contract_key,
  {modelCapabilitySummary(CAP(predicates))})
MODEL_refresh_occurred = MODEL(
  DP(refresh_occurred),refresh_occurred,SP(refresh_occurred),(Trace)->Bool,
  ({trace}),T3_A1_EVIDENCE_LIFT(pd,sb),
  T3_A1_UNKNOWN_LIFT(pd,sb),T3_A1_ERROR_LIFT(pd,sb),
  T3_A1_MEANING_LIFT(pd,sb).contract_key,
  {modelCapabilitySummary(CAP(predicates))})
```

These eleven named ordinary/pair records and each explicitly enumerated
`MODEL_LITERAL(T,v)` are complete `ModelContract` records; none is a
`ModelContractKey` masquerading as one.

For `refresh_occurred`, the key field of `MODEL_refresh_occurred` is
producer-supplied exactly as
`MC(BINDING_IDENTITY(DP(refresh_occurred)),refresh_occurred)` in the retained
`EventPairBinding`; every other field equals the complete K2 occurrence
projection.
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

Network prohibition uses `Forbidden(NET_ANY)`.  Path-change permission
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
ATP = (capknow.embedding,coding-authority-policy,(1))
TR = (TP,coding,semantic-service-root,(1))
TRB = (TP,coding,bounds-admission-root,(1))
TRW = (TP,coding,witness-admission-root,(1))
TRA = (ATP,coding,authority-admission-root,(1))

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

APK = ((capknow.authority,coding-fixture-source),(1))
ATK = ((capknow.attestation,coding-fixture-authority),(1))
AVK = ((capknow.audit,coding-authority-validator),(1))
AVSK = (AVK,coding.validation,authority,(1),AUTHORITY_VALIDATION)
CAP(authority) = (AVSK,validate_coding_authority)

BCERT = (PLUGIN_CERTIFICATE_ISSUER(CK),
         coding.certificate,bundle_bounds_unsat)
WCERT = (PLUGIN_CERTIFICATE_ISSUER(AWK),
         coding.certificate,adapter_satisfying_witness)
ACERT(z,i) = (PLUGIN_CERTIFICATE_ISSUER(ATK),
              coding.authority.certificate,AUTHORITY_CERT_LOCAL(z,i))

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

Every atom is sort-local logical data; `p_b` is not a host path.  Fix principal
`fixture_principal` and exact clause

```text
f_b = All({TA(ts_nonempty),TA(ts_lt_100),TA(ts_ge_200)})
cl_b = Attribute(coding.bounds.clause,SRC(b,1),Require(f_b))
ad_b = Adopt(coding.bounds.clause,AUTH(b,1),fixture_principal)
C_b = Contract(
  AttributedClauses={cl_b},Adoptions={ad_b},Choices={},
  ProfileRequirements={},PairRequirements={})
```

Here `TA` is the exact expansion in section 7.1 and `SRC/AUTH` are the finite
authority records below.  To eliminate every environment alias, define the
following one total finite constructor for the three closed fixtures.  For a
finite Contract `C`, finite function/predicate key sets `F/Q`, finite literal
value set `L`, finite profile set `P`, and finite admitted authority map `A`:

```text
types(C,F,Q,L,P) = the least finite set of T(n) containing every coding type
  in C, every value in L, every signature in F union Q, and every profile
  subject in P, closed under the exact nested-type rows of §3.2

ENV(C,F,Q,L,P,A) = SemanticEnvironment(
  abi_version=ABI0,
  declarations=
    {the exact §3.2 TypeDeclaration(t) | t in types(C,F,Q,L,P)} union
    {LiteralDeclaration(type(v),v) | v in L} union
    {the exact §3.3 declaration for k | k in F union Q},
  pair_declarations=
    {the exact §3.4 declaration for p | K1_PAIR(p) in required(C)},
  bindings=
    {the exact §3.2 literal SemanticBinding(type(v),v) | v in L} union
    {the exact §4.2 ordinary SemanticBinding for k | k in F union Q},
  pair_bindings=
    {the exact retained definitional EventPairBinding(p) |
       K1_PAIR(p) in required(C)},
  profile_bindings={the exact §3.4/§4.2 ProfileBinding(p) | p in P},
  authority_facts=A,
  semantic_extensions={}, lexical_bindings={}, choice_bindings={},
  mechanically_extracted_dependencies=required(CONTRACT_SUBJECT(C)),
  chi_C={})

MODEL_RECORDS(F,Q,L) =
  ({MODEL_snapshot_of} if DF(snapshot_of) in F else {}) union
  ({MODEL_changes_between} if DF(changes_between) in F else {}) union
  ({MODEL_observe} if DF(observe) in F else {}) union
  ({MODEL_observations_equal} if DP(observations_equal) in Q else {}) union
  ({MODEL_task_accepts} if DP(task_accepts) in Q else {}) union
  ({MODEL_dependency_metadata_changed}
     if DP(dependency_metadata_changed) in Q else {}) union
  ({MODEL_verification_passed} if DP(verification_passed) in Q else {}) union
  ({MODEL_event_matches} if DP(event_matches) in Q else {}) union
  ({MODEL_event_occurred} if DP(event_occurred) in Q else {}) union
  ({MODEL_refresh_scope} if DP(refresh_scope) in Q else {}) union
  ({MODEL_refresh_occurred} if DP(refresh_occurred) in Q else {}) union
  {MODEL_LITERAL(type(v),v) | v in the displayed finite set L}

contractFields(r) = the finite set containing exactly each value of every
  `ContractSpec`-typed field displayed by K2 for record r; it is `{}` when r
  has no such field

RECORDS(C,F,Q,L,P,A) =
  {ABI0,ENV(C,F,Q,L,P,A)} union
  ENV(C,F,Q,L,P,A).declarations union
  ENV(C,F,Q,L,P,A).pair_declarations union
  ENV(C,F,Q,L,P,A).bindings union
  ENV(C,F,Q,L,P,A).pair_bindings union
  ENV(C,F,Q,L,P,A).profile_bindings union range(A) union
  MODEL_RECORDS(F,Q,L) union
  UNION(contractFields(r) | r in
    ENV(C,F,Q,L,P,A).declarations union
    ENV(C,F,Q,L,P,A).bindings union
    ENV(C,F,Q,L,P,A).pair_bindings union
    ENV(C,F,Q,L,P,A).profile_bindings union MODEL_RECORDS(F,Q,L))
```

`contractFields` is a field projection, not reachability or a prose closure;
for example it returns the admitting domain for a `TypeDeclaration`, the five
meaning/evidence/access/unknown/error contracts for a `SemanticBinding`, every
contract in an occurrence bundle for an `EventPairBinding`, and the seven
coverage/evidence/unknown/error fields for a `ProfileBinding`.  All
comprehensions range over the displayed finite sets and select the unique
records already defined field-by-field in §§3-4; this is an extensional record
equation, not “the required environment” shorthand.  Model contracts and
services remain separate package records exactly as K2 requires.  For bounds,

```text
F_b={DF(snapshot_of)}
Q_b={DP(task_accepts)}
L_b={ts_nonempty:T(TaskSpec),ts_lt_100:T(TaskSpec),
     ts_ge_200:T(TaskSpec)}
P_b={}
E_b^0=ENV(C_b,F_b,Q_b,L_b,P_b,{})
```

The authority construction below yields exact binding `AFB(b,1)` and final
`E_b=ENV(C_b,F_b,Q_b,L_b,P_b,{AF(b,1)->AFB(b,1)})`.  Let `D_b` be exactly
`DependencyEnvironment(CONTRACT_SUBJECT(C_b),Omega_b)` under the K2 §3.3
field equations in the finite universe
`Omega_b=RECORDS(C_b,F_b,Q_b,L_b,P_b,{AF(b,1)->AFB(b,1)}) union
AUTH_LOOKUPS({(b,1)})`; no
dependency field is supplied.  Define

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

Define the exact two-clause Contract and its admission stages:

```text
cl_c1 = Attribute(coding.confluence.observation,SRC(c,1),Require(f_c_o))
cl_c2 = Attribute(coding.confluence.change,SRC(c,2),Require(f_c_d))
ad_c1 = Adopt(coding.confluence.observation,AUTH(c,1),fixture_principal)
ad_c2 = Adopt(coding.confluence.change,AUTH(c,2),fixture_principal)
C_c = Contract(
  AttributedClauses={cl_c1,cl_c2},Adoptions={ad_c1,ad_c2},Choices={},
  ProfileRequirements={},PairRequirements={})
F_c_keys={DF(observe),DF(changes_between)}
Q_c={DP(observations_equal),DP(dependency_metadata_changed)}
L_c={s_c:T(ObservationSpec),P_c:T(RepositorySnapshot),
     F_c:T(RepositorySnapshot),O_c:T(ObservationResult)}
P_c_keys={}
E_c^0=ENV(C_c,F_c_keys,Q_c,L_c,P_c_keys,{})
E_c^1=ENV(C_c,F_c_keys,Q_c,L_c,P_c_keys,
          {AF(c,1)->AFB(c,1)})
E_c=ENV(C_c,F_c_keys,Q_c,L_c,P_c_keys,
        {AF(c,1)->AFB(c,1),AF(c,2)->AFB(c,2)})
D_c=DependencyEnvironment(CONTRACT_SUBJECT(C_c),Omega_c)
Omega_c=RECORDS(C_c,F_c_keys,Q_c,L_c,P_c_keys,
  {AF(c,1)->AFB(c,1),AF(c,2)->AFB(c,2)}) union
  AUTH_LOOKUPS({(c,1),(c,2)})
```

`Omega_c` is the displayed literal finite record universe.  Its dependency
environment fields are therefore the exact K2 recomputation, not a caller
list.  Define

```text
J_c = ENVIRONMENT_JUDGMENT_TARGET(
        CONSISTENCY,(C_c),semanticIdentity(E_c))
```

`CSOUND` is the only record in this document
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

Define the exact attributed/adopted Contract and environments:

```text
f_w1 = OBS_EQ(s_w)
f_w2 = TA(t_w)
cl_w1 = Attribute(coding.adapter.preservation,SRC(w,1),Require(f_w1))
cl_w2 = Attribute(coding.adapter.acceptance,SRC(w,2),Require(f_w2))
ad_w1 = Adopt(coding.adapter.preservation,AUTH(w,1),fixture_principal)
ad_w2 = Adopt(coding.adapter.acceptance,AUTH(w,2),fixture_principal)
C_w = Contract(
  AttributedClauses={cl_w1,cl_w2},Adoptions={ad_w1,ad_w2},Choices={},
  ProfileRequirements={PK(implementation_evidence)},PairRequirements={})
F_w_keys={DF(snapshot_of),DF(observe)}
Q_w={DP(observations_equal),DP(task_accepts)}
L_w={s_w:T(ObservationSpec),t_w:T(TaskSpec)}
P_w_keys={PK(implementation_evidence)}
E_w^0=ENV(C_w,F_w_keys,Q_w,L_w,P_w_keys,{})
E_w^1=ENV(C_w,F_w_keys,Q_w,L_w,P_w_keys,
          {AF(w,1)->AFB(w,1)})
E_w=ENV(C_w,F_w_keys,Q_w,L_w,P_w_keys,
        {AF(w,1)->AFB(w,1),AF(w,2)->AFB(w,2)})
D_w=DependencyEnvironment(CONTRACT_SUBJECT(C_w),Omega_w)
Omega_w=RECORDS(C_w,F_w_keys,Q_w,L_w,P_w_keys,
  {AF(w,1)->AFB(w,1),AF(w,2)->AFB(w,2)}) union
  AUTH_LOOKUPS({(w,1),(w,2)})
J_w=ENVIRONMENT_JUDGMENT_TARGET(CONSISTENCY,(C_w),semanticIdentity(E_w))
```

`Omega_w` is the displayed finite universe.  Fix one admitted abstract outcome
`O_w=(P_w,TRACE_w,F_w,EVIDENCE_w)` with no controlled events, exact
Contract-derived `chi_C={}`, direct task/preservation results equal to
`VALUE(TRUE,E_witness,{})`, and evidence refs admitted by their displayed
schemas.  `O_w` is finite semantic data, not a patch or construction method.

Freeze the complete choice fixture before authority admission:

```text
choice_binding0=(LOCAL_STORAGE,user,SRC(choice,1),AUTH(choice,1))
C_choice=Contract(
  AttributedClauses={},Adoptions={},
  Choices={Choice(storage,T(StorageBackend),
                  {LOCAL_STORAGE,HOSTED_STORAGE},user,choice_binding0)},
  ProfileRequirements={},PairRequirements={})
cb0=ChoiceBindingKey(IDENTITY_OF(C_choice),storage)
cbe0=ChoiceBindingEntry(
  choice_binding_key=cb0,declared_type=T(StorageBackend),
  admitted_value=LOCAL_STORAGE,controller=user,
  source_ref=SRC(choice,1),authority_fact_key=AF(choice,1))
L_choice={LOCAL_STORAGE:T(StorageBackend),
          HOSTED_STORAGE:T(StorageBackend)}
E_choice^0=ENV(C_choice,{},{},L_choice,{}, {})
E_choice=SemanticEnvironment(
  abi_version=ABI0,
  declarations=E_choice^0.declarations,
  pair_declarations={},bindings=E_choice^0.bindings,
  pair_bindings={},profile_bindings={},
  authority_facts={AF(choice,1)->AFB(choice,1)},
  semantic_extensions={},lexical_bindings={},
  choice_bindings={cb0->cbe0},
  mechanically_extracted_dependencies=required(CONTRACT_SUBJECT(C_choice)),
  chi_C={storage->LOCAL_STORAGE})
```

The choice record is structurally complete before admission but remains open
in `E_choice^0`: neither `cbe0` nor its `chi_C` entry exists until the exact
`BIND_CHOICE(storage)` fact is received.  The five normative adoptions above
and this choice binding are closed by the following finite K2 authority
packet.  There is no `ABI-issued authority` shorthand.  Define:

```text
I_REQ={(b,1),(c,1),(c,2),(w,1),(w,2)}
I_CHOICE={(choice,1)}
I_A={(b,1),(c,1),(c,2),(w,1),(w,2),(choice,1)}
clause(b,1)=cl_b
clause(c,1)=cl_c1   clause(c,2)=cl_c2
clause(w,1)=cl_w1   clause(w,2)=cl_w2
clause_id(b,1)=coding.bounds.clause
clause_id(c,1)=coding.confluence.observation
clause_id(c,2)=coding.confluence.change
clause_id(w,1)=coding.adapter.preservation
clause_id(w,2)=coding.adapter.acceptance
clause_id(choice,1)=coding.choice.storage
attestation_clause_tag(b,1)=BOUNDS_CLAUSE
attestation_clause_tag(c,1)=CONFLUENCE_OBSERVATION_CLAUSE
attestation_clause_tag(c,2)=CONFLUENCE_CHANGE_CLAUSE
attestation_clause_tag(w,1)=ADAPTER_PRESERVATION_CLAUSE
attestation_clause_tag(w,2)=ADAPTER_ACCEPTANCE_CLAUSE
subject_contract(b,1)=C_b
subject_contract(c,1)=C_c     subject_contract(c,2)=C_c
subject_contract(w,1)=C_w     subject_contract(w,2)=C_w
attestation_subject_identity(z,i)=CLAUSE_ATTESTATION_SUBJECT(
  IDENTITY_OF(subject_contract(z,i)),attestation_clause_tag(z,i))
  for (z,i) in I_REQ
attestation_subject_identity(choice,1)=CHOICE_ATTESTATION_SUBJECT(
  IDENTITY_OF(C_choice),storage)
role(z,i)=REQUIRE for (z,i) in I_REQ
role(choice,1)=BIND_CHOICE(storage)
principal(z,i)=fixture_principal for (z,i) in I_REQ
principal(choice,1)=user
base(b,1)=E_b^0
base(c,1)=E_c^0     base(c,2)=E_c^0
base(w,1)=E_w^0     base(w,2)=E_w^0
base(choice,1)=E_choice^0

SRC(z,i)=SourceRef(
  issuer=PLUGIN_ISSUER(APK),source_kind=AUTHENTICATED_FIXTURE_INSTRUCTION,
  stable_source_identity=CODING_SOURCE(z,i),
  provenance_facts={AUTHENTICATED_BY(APK),
                    CLAUSE_LOCAL_IDENTITY(clause_id(z,i))})
AUTH(z,i)=AuthorityRef(
  owner=PLUGIN_ISSUER(APK),authority_namespace=coding.fixture,
  stable_attestation_identity=CODING_AUTHORITY(z,i))
AF(z,i)=AuthorityFactKey(
  AUTH(z,i),SRC(z,i),principal(z,i),role(z,i))
AE_REF(z,i)=EvidenceRef(
  PLUGIN_ISSUER(ATK),coding.authority.attestation,
  AUTHORITY_EVIDENCE_LOCAL(z,i),AREQUIRED.contract_key)
ATTEST(z,i)=AUTHORITY_ATTESTATION_VALUE(
  authority_ref=AUTH(z,i),source_ref=SRC(z,i),
  principal=principal(z,i),normative_role=role(z,i),
  subject_identity=attestation_subject_identity(z,i))
AC(z,i)=AuthorityFactCandidate(
  authority_fact_key=AF(z,i),admission_subject_data=ATTEST(z,i),
  offered_evidence_refs={AE_REF(z,i)})
authority_subject(z,i)=AUTHORITY_ATTESTATION_SUBJECT(
  AF(z,i),ATTEST(z,i),{AE_REF(z,i)})
L_authority={authority_subject(b,1),authority_subject(c,1),
  authority_subject(c,2),authority_subject(w,1),authority_subject(w,2),
  authority_subject(choice,1)} : T(ServiceAdmissionSubject)
Delta_authority_fields={
  the exact TypeDeclaration(T(AuthorityClauseTag)),
  the exact TypeDeclaration(T(AuthorityAttestationSubjectIdentity)),
  the exact TypeDeclaration(T(AuthorityAttestationValue)),
  LiteralDeclaration(T(AuthorityClauseTag),BOUNDS_CLAUSE),
  LiteralDeclaration(T(AuthorityClauseTag),CONFLUENCE_OBSERVATION_CLAUSE),
  LiteralDeclaration(T(AuthorityClauseTag),CONFLUENCE_CHANGE_CLAUSE),
  LiteralDeclaration(T(AuthorityClauseTag),ADAPTER_PRESERVATION_CLAUSE),
  LiteralDeclaration(T(AuthorityClauseTag),ADAPTER_ACCEPTANCE_CLAUSE),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(b,1)),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(c,1)),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(c,2)),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(w,1)),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(w,2)),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(choice,1)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(b,1)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(c,1)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(c,2)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(w,1)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(w,2)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(choice,1))}
Delta_authority=Delta_authority_fields union {
  the exact TypeDeclaration(T(ServiceAdmissionSubject)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(b,1)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(c,1)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(c,2)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(w,1)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(w,2)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(choice,1))}
BIND_authority_fields={
  the exact literal SemanticBinding(T(AuthorityClauseTag),BOUNDS_CLAUSE),
  the exact literal SemanticBinding(
    T(AuthorityClauseTag),CONFLUENCE_OBSERVATION_CLAUSE),
  the exact literal SemanticBinding(
    T(AuthorityClauseTag),CONFLUENCE_CHANGE_CLAUSE),
  the exact literal SemanticBinding(
    T(AuthorityClauseTag),ADAPTER_PRESERVATION_CLAUSE),
  the exact literal SemanticBinding(
    T(AuthorityClauseTag),ADAPTER_ACCEPTANCE_CLAUSE),
  the exact literal SemanticBinding(
    T(AuthorityAttestationSubjectIdentity),attestation_subject_identity(b,1)),
  the exact literal SemanticBinding(
    T(AuthorityAttestationSubjectIdentity),attestation_subject_identity(c,1)),
  the exact literal SemanticBinding(
    T(AuthorityAttestationSubjectIdentity),attestation_subject_identity(c,2)),
  the exact literal SemanticBinding(
    T(AuthorityAttestationSubjectIdentity),attestation_subject_identity(w,1)),
  the exact literal SemanticBinding(
    T(AuthorityAttestationSubjectIdentity),attestation_subject_identity(w,2)),
  the exact literal SemanticBinding(
    T(AuthorityAttestationSubjectIdentity),attestation_subject_identity(choice,1)),
  the exact literal SemanticBinding(T(AuthorityAttestationValue),ATTEST(b,1)),
  the exact literal SemanticBinding(T(AuthorityAttestationValue),ATTEST(c,1)),
  the exact literal SemanticBinding(T(AuthorityAttestationValue),ATTEST(c,2)),
  the exact literal SemanticBinding(T(AuthorityAttestationValue),ATTEST(w,1)),
  the exact literal SemanticBinding(T(AuthorityAttestationValue),ATTEST(w,2)),
  the exact literal SemanticBinding(T(AuthorityAttestationValue),ATTEST(choice,1)),
  MODEL_LITERAL(T(AuthorityClauseTag),BOUNDS_CLAUSE),
  MODEL_LITERAL(T(AuthorityClauseTag),CONFLUENCE_OBSERVATION_CLAUSE),
  MODEL_LITERAL(T(AuthorityClauseTag),CONFLUENCE_CHANGE_CLAUSE),
  MODEL_LITERAL(T(AuthorityClauseTag),ADAPTER_PRESERVATION_CLAUSE),
  MODEL_LITERAL(T(AuthorityClauseTag),ADAPTER_ACCEPTANCE_CLAUSE),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(b,1)),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(c,1)),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(c,2)),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(w,1)),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(w,2)),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(choice,1)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(b,1)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(c,1)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(c,2)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(w,1)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(w,2)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(choice,1))}
BIND_authority=BIND_authority_fields union {
  the exact literal SemanticBinding(T(ServiceAdmissionSubject),authority_subject(b,1)),
  the exact literal SemanticBinding(T(ServiceAdmissionSubject),authority_subject(c,1)),
  the exact literal SemanticBinding(T(ServiceAdmissionSubject),authority_subject(c,2)),
  the exact literal SemanticBinding(T(ServiceAdmissionSubject),authority_subject(w,1)),
  the exact literal SemanticBinding(T(ServiceAdmissionSubject),authority_subject(w,2)),
  the exact literal SemanticBinding(T(ServiceAdmissionSubject),authority_subject(choice,1)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(b,1)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(c,1)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(c,2)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(w,1)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(w,2)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(choice,1))}
Sigma_authority=BIND_authority union
  UNION(contractFields(r) | r in Delta_authority union BIND_authority)
```

The four service contracts are exact `ContractSpec[Service]` records:

```text
ASOUND=SERVICE_SPEC(
  (AVK,coding.authority.contract,sound,(1),SOUND_FRAGMENT),SOUND_FRAGMENT,
  AuthorityFactCandidate,{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  x->IN_FRAGMENT exactly when x in
    {AC(b,1),AC(c,1),AC(c,2),AC(w,1),AC(w,2),AC(choice,1)};
  every other admitted candidate->OUTSIDE_FRAGMENT)
ACOMPLETE=SERVICE_SPEC(
  (AVK,coding.authority.contract,complete,(1),COMPLETE_FRAGMENT),
  COMPLETE_FRAGMENT,AuthorityFactCandidate,{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  x->IN_FRAGMENT exactly when x in
    {AC(b,1),AC(c,1),AC(c,2),AC(w,1),AC(w,2),AC(choice,1)};
  every other admitted candidate->OUTSIDE_FRAGMENT)
AREQUIRED=SERVICE_SPEC(
  (AVK,coding.authority.contract,evidence,(1),REQUIRED_EVIDENCE),
  REQUIRED_EVIDENCE,
  (AuthorityFactCandidate,T(ServiceAdmissionSubject),finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  x->ADMISSIBLE exactly when x in {
    (AC(b,1),authority_subject(b,1),{AE_REF(b,1)}),
    (AC(c,1),authority_subject(c,1),{AE_REF(c,1)}),
    (AC(c,2),authority_subject(c,2),{AE_REF(c,2)}),
    (AC(w,1),authority_subject(w,1),{AE_REF(w,1)}),
    (AC(w,2),authority_subject(w,2),{AE_REF(w,2)}),
    (AC(choice,1),authority_subject(choice,1),{AE_REF(choice,1)})};
  every other admitted tuple->INADMISSIBLE)
AFAILURE=SERVICE_SPEC(
  (AVK,coding.authority.contract,failure,(1),SERVICE_FAILURE_BEHAVIOR),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,
  AuthorityAdmissionResult.REASONING_ERROR,{},
  F->the exact K2 AUTHORITY_VALIDATION failure projection of F)
```

All four are complete `ContractSpec[Service]` records with owner `AVK`, Service
layer, their displayed role, and the literal observation-query map `{}`.
`ASOUND` and `ACOMPLETE` have primary domain `AuthorityFactCandidate`, codomain
`{IN_FRAGMENT,OUTSIDE_FRAGMENT}`, and return `IN_FRAGMENT` exactly for the six
field-complete candidates in `I_A`; every unequal admitted candidate returns
`OUTSIDE_FRAGMENT`.  The independent K2 request-formation checks separately
require the exact target-excluded environment, dependency environment, and
target displayed below.  `AREQUIRED` has fixed primary domain
`(AuthorityFactCandidate,T(ServiceAdmissionSubject),finset(EvidenceRef))`,
codomain `{ADMISSIBLE,INADMISSIBLE}`, literal query map `{}`, and returns
`ADMISSIBLE` exactly on
`(AC(z,i),authority_subject(z,i),{AE_REF(z,i)})` for `(z,i) in I_A`; every
other admitted tuple returns `INADMISSIBLE`.  `AFAILURE` has fixed primary
domain `InterfaceFailure`,
codomain `AuthorityAdmissionResult.REASONING_ERROR`, and returns only the total
K2 authority-validation role projection.  Their logical relations have no
other branch and consume no lower observation value.  These are legal K2
Service primary domains: `AuthorityFactCandidate` is the field-complete finite
K2 candidate carrier, and the `AREQUIRED` tuple consists only of that carrier,
the closed `T(ServiceAdmissionSubject)` value, and a finite evidence-reference
set.  Candidate equality distinguishes its `AuthorityFactKey` from the later
`AuthorityFactBinding`; no Service relation accepts a binding in place of the
key or candidate.

For every `(z,i) in I_A`, define without omission:

```text
baseRecords(b,1)=RECORDS(C_b,F_b,Q_b,L_b,P_b,{})
baseRecords(c,1)=baseRecords(c,2)=
  RECORDS(C_c,F_c_keys,Q_c,L_c,P_c_keys,{})
baseRecords(w,1)=baseRecords(w,2)=
  RECORDS(C_w,F_w_keys,Q_w,L_w,P_w_keys,{})
baseRecords(choice,1)=
  RECORDS(C_choice,{},{},L_choice,{}, {}) union {C_choice}
Omega_A(z,i)=baseRecords(z,i) union
  Delta_authority union Sigma_authority union
  {SRC(z,i),AUTH(z,i),AE_REF(z,i),
   ASOUND,ACOMPLETE,AREQUIRED,AFAILURE}
DA(z,i)=DependencyEnvironment(
  AUTHORITY_ADMISSION_SUBJECT(AC(z,i),base(z,i)),Omega_A(z,i))
JA(z,i)=ENVIRONMENT_JUDGMENT_TARGET(
  AUTHORITY_FACT_ADMISSION,(AC(z,i)),semanticIdentity(base(z,i)))
UA(z,i)=SERVICE_USE_TRUST_TARGET(
  CAP(authority),AUTHORITY_FACT_ADMISSION,
  ENVIRONMENT_USE(AUTHORITY_FACT_ADMISSION,(AC(z,i))),
  semanticIdentity(base(z,i)))
AA(z,i)=AUTHORITY_TRUST_TARGET(AF(z,i))
```

Each `Omega_A(z,i)` is the displayed finite fact-free record set.  Capability,
root, request, envelope, validation request, admission, result, and binding
records are deliberately outside the subject dependency universe and are
supplied separately below; including any of them in proper subject closure
would be a cycle/error.  No `Omega_A(z,i)` contains an authority-fact binding.
K2 §3.3 therefore fixes every field of each `DA`:
its syntax roots are the exact `required(AUTHORITY_ADMISSION_SUBJECT(...))`,
its subject roots contain the displayed base environment, its association and
proper closures are the least reachable sets, its validation-reference set is
empty, and `AUTHORITY_FACT(AF(z,i))` is absent from all of them.

The complete `CapabilityDescriptor(CAP(authority))` has ABI `ABI0`, plugin
`AVK`, role `AUTHORITY_VALIDATION`, class
`COMPLETE_FOR_DECLARED_FRAGMENT`, judgments `{AUTHORITY_FACT_ADMISSION}`, exact
targets `{JA(b,1),JA(c,1),JA(c,2),JA(w,1),JA(w,2),JA(choice,1)}`, fragments
`ASOUND/ACOMPLETE`, dependency scope
`DA(b,1).transitive_dependency_closure union
DA(c,1).transitive_dependency_closure union
DA(c,2).transitive_dependency_closure union
DA(w,1).transitive_dependency_closure union
DA(w,2).transitive_dependency_closure union
DA(choice,1).transitive_dependency_closure`, required evidence
`AREQUIRED`, roots `{TRA}`, and failure contract `AFAILURE`; its proper
dependencies and closure are the exact K2 derivation.

```text
ROOT_A=TrustRootRecord(
  trust_root_key=TRA,owner=EMBEDDING_POLICY_PRODUCER(ATP),
  trusted_validators={CAP(authority)},
  permitted_certificate_kinds={AUTHORITY_FACT_ATTESTATION},
  permitted_targets={UA(b,1),UA(c,1),UA(c,2),UA(w,1),UA(w,2),UA(choice,1),
                     AA(b,1),AA(c,1),AA(c,2),AA(w,1),AA(w,2),AA(choice,1)},
  adoption=V0_EXTERNAL_TRUST_PREMISE)
T_A=TrustEnvironment(
  trust_policy_key=ATP,policy_owner=EMBEDDING_POLICY_PRODUCER(ATP),
  root_judgments={TRA->TRUST_ROOT_ADMITTED(ROOT_A)})
RA(z,i)=AuthorityAdmissionRequest(
  abi_version=ABI0,candidate=AC(z,i),
  environment_without_fact=base(z,i),trust_environment=T_A,
  complete_dependencies=DA(z,i),capability_target=JA(z,i),
  capability_key=CAP(authority))
AENV(z,i)=CertificateEnvelope(
  certificate_key=ACERT(z,i),
  certificate_kind=AUTHORITY_FACT_ATTESTATION,
  request_binding=RA(z,i),subjects=(AC(z,i)),environment=base(z,i),
  capability_key=CAP(authority),fragment=ASOUND,dependencies=DA(z,i),
  claimed_conclusion=AUTHORITY_FACT_ADMITTED(AF(z,i),ACERT(z,i)),
  validator_key=CAP(authority),trust_root_key=TRA,
  abstraction_class=SYMBOLIC,payload=ATTEST(z,i),
  evidence_refs={AE_REF(z,i)})
```

K2 derives `certificateValidationRequest(AENV(z,i))` with validator role
`AUTHORITY_VALIDATION`, target `JA(z,i)`, receiving rule
`RECEIVE_AUTHORITY_FACT`, service-use target `UA(z,i)`, and certificate target
`AA(z,i)`.  Its sole successful chain is

```text
AADMIT(z,i)=CertificateAdmission.ADMITTED(
  ACERT(z,i),AUTHORITY_FACT_ADMITTED(AF(z,i),ACERT(z,i)))
ARES(z,i)=AuthorityAdmissionResult.AUTHORITY_FACT_ADMITTED(
  AF(z,i),ACERT(z,i))
AADMIT(z,i) -> ARES(z,i)
             -> AFB(z,i)=AuthorityFactBinding(AF(z,i),{ACERT(z,i)})
AUTH_LOOKUPS(S)={ASOUND,ACOMPLETE,AREQUIRED,AFAILURE,
  CapabilityDescriptor(CAP(authority)),ServiceIdentityRecord(AVSK),ROOT_A,T_A}
  union {SRC(z,i),AUTH(z,i),AE_REF(z,i),RA(z,i),AENV(z,i),
         AADMIT(z,i),ARES(z,i),AFB(z,i) | (z,i) in S}
```

The six candidates are admitted independently against their fact-free base
environments; the singleton receiving maps are then composed by exact
authority-map union to form the displayed final `E_b/E_c/E_w`.  This avoids
self-support and a chain through a previous validator.  For every candidate,
the validation-filtered subject producer set is exactly
`{PLUGIN_PRODUCER(CK),PLUGIN_PRODUCER(APK),PLUGIN_PRODUCER(ATK),
ABI_PRODUCER(ABI0)}`; `PLUGIN_PRODUCER(AVK)` and
`EMBEDDING_POLICY_PRODUCER(ATP)` are outside it and distinct from the
certificate producer.  After composition, each final `C_b/C_c/C_w`
reasoning-subject producer set is exactly
`{PLUGIN_PRODUCER(CK),PLUGIN_PRODUCER(APK),PLUGIN_PRODUCER(ATK),
PLUGIN_PRODUCER(AVK),EMBEDDING_POLICY_PRODUCER(ATP),ABI_PRODUCER(ABI0)}`:
the received authority binding reaches its admitted certificate envelope,
independent validator, and authority root.  Validation filtering applies only
while that authority certificate is being admitted; it does not erase an
already admitted authority chain from a later reasoning subject.  The separate
bounds/confluence/witness validators and `TP` roots below are therefore also
producer-independent.  Every adopted tuple now has an exact source,
authority, candidate, request, capability, certificate, envelope, root scope,
validation, result, reception, and final binding.

| Capability | Class and supported targets/judgments | Exact fragment and dependency scope | Required root/failure contract |
|---|---|---|---|
| `CAP(functions)` | `CONCRETE_EVALUATION_ONLY`; `{FUNCTION_EVALUATION}`; supported targets exactly `FUNCTION_TARGETS` | `FSOUND`, no complete fragment; dependency scope is the exact union of all three target closures | nonempty `{TR}`; `FREQ/FFAIL` |
| `CAP(predicates)` | `CONCRETE_EVALUATION_ONLY`; `{PREDICATE_EVALUATION}`; supported targets exactly `PREDICATE_TARGETS` | `QSOUND`, no complete fragment; dependency scope is the exact union of all eight target closures | nonempty `{TR}`; `QREQ/QFAIL` |
| `CAP(profile)` | `CONCRETE_EVALUATION_ONLY`; `{PROFILE_COVERAGE}`; supported targets exactly `{PROFILE_TARGET(PK(implementation_evidence))}` | `PROFSOUND`, no complete fragment; dependency scope is the exact profile closure | nonempty `{TR}`; `PROFREQ/PROFFAIL` |
| `CAP(bounds)` | `COMPLETE_FOR_DECLARED_FRAGMENT`; `{CONSISTENCY}`; supported targets exactly `{J_b}` | `BSOUND/BCOMPLETE`; dependency scope exactly equals `D_b.transitive_dependency_closure` | nonempty `{TRB}`; `BREQ/BFAIL` |
| `CAP(confluence)` | `PARTIAL_SYMBOLIC_REASONING`; `{CONSISTENCY}`; supported targets exactly `{J_c}` | `CSOUND`, no complete fragment; dependency scope exactly equals `D_c.transitive_dependency_closure` and contains both independent lower roots | nonempty `{TR}`; `CREQ/CFAIL` |
| `CAP(witness)` | `PARTIAL_SYMBOLIC_REASONING`; `{CONSISTENCY}`; supported targets exactly `{J_w}` | `WSOUND`, no complete fragment; dependency scope exactly equals `D_w.transitive_dependency_closure` | nonempty `{TRW}`; `WREQ/WFAIL` |
| `CAP(validate_bounds)` | `COMPLETE_FOR_DECLARED_FRAGMENT`; `{CONSISTENCY}`; supported targets exactly `{J_b}` | exact `BSOUND/BCOMPLETE`; dependency scope exactly equals `D_b.transitive_dependency_closure` | nonempty `{TRB}`; `BREQ/BFAIL`; producer `PLUGIN_PRODUCER(RVK)` |
| `CAP(validate_witness)` | `PARTIAL_SYMBOLIC_REASONING`; `{CONSISTENCY}`; supported targets exactly `{J_w}` | exact `WSOUND`, no complete fragment; dependency scope exactly equals `D_w.transitive_dependency_closure` | nonempty `{TRW}`; `WREQ/WFAIL`; producer `PLUGIN_PRODUCER(RVK)` |
| `CAP(authority)` | `COMPLETE_FOR_DECLARED_FRAGMENT`; `{AUTHORITY_FACT_ADMISSION}`; supported targets exactly `{JA(b,1),JA(c,1),JA(c,2),JA(w,1),JA(w,2),JA(choice,1)}` | exact `ASOUND/ACOMPLETE`; dependency scope is the exact union of the six named `DA` closures | nonempty `{TRA}`; exact `AREQUIRED/AFAILURE`; producer `PLUGIN_PRODUCER(AVK)` |

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
BSOUND,D_b,J_b,CAP(bounds))`.  Let

```text
BundleBoundsProof = BOUNDS_CORE(
  selector=S_b, population_nonempty=TRUE,
  upper=KIB(100), lower=KIB(200),
  relation=(200>=100),
  subject_identity=IDENTITY_OF(C_b))
BPROOF_REF = EvidenceRef(
  PLUGIN_ISSUER(CK),coding.bounds-proof,bounds_core,
  BREQ.contract_key)
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
`{PLUGIN_PRODUCER(CK),PLUGIN_PRODUCER(APK),PLUGIN_PRODUCER(ATK),
PLUGIN_PRODUCER(AVK),EMBEDDING_POLICY_PRODUCER(ATP),ABI_PRODUCER(ABI0)}`,
the recomputed final `C_b/E_b` set.  The certificate producer is
`PLUGIN_PRODUCER(CK)`, the validator producer is
`PLUGIN_PRODUCER(RVK)`, and the root producer is
`EMBEDDING_POLICY_PRODUCER(TP)`; all K2-required inequalities therefore hold.
`CertificateAdmission.ADMITTED(BCERT,CONSISTENCY_UNSAT)` is received only as
`ReasoningResult.ADMITTED_JUDGMENT(CONSISTENCY_UNSAT,BCERT)`.  Missing,
rejected, malformed, wrong-scope, or failed records yield their exact K2
no-admission/evaluability/error branch and no UNSAT conclusion.

The C19 witness uses a separate producer, certificate, request, and payload.
Let `R_w` be the exact `ReasoningRequest(ABI0,CONSISTENCY,(C_w),E_w,T_w,
WSOUND,D_w,J_w,CAP(witness))` and

```text
AdapterWitness = ABSTRACT_OUTCOME_WITNESS(
  contract_identity=IDENTITY_OF(C_w), outcome=O_w,
  chi_C={}, accept_eval=VALUE(TRUE,E_witness,{}),
  admitted_evidence=E_witness)
WPROOF_REF = EvidenceRef(
  PLUGIN_ISSUER(AWK),coding.witness,adapter_abstract,
  WREQ.contract_key)
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
`{PLUGIN_PRODUCER(CK),PLUGIN_PRODUCER(APK),PLUGIN_PRODUCER(ATK),
PLUGIN_PRODUCER(AVK),EMBEDDING_POLICY_PRODUCER(ATP),ABI_PRODUCER(ABI0)}`;
certificate producer
`PLUGIN_PRODUCER(AWK)`, validator producer `PLUGIN_PRODUCER(RVK)`, and root
producer `EMBEDDING_POLICY_PRODUCER(TP)` are pairwise distinct from the
subject as K2 requires.  Only
`CertificateAdmission.ADMITTED(WCERT,CONSISTENCY_SAT)` yields
`ReasoningResult.ADMITTED_JUDGMENT(CONSISTENCY_SAT,WCERT)`.  The separate
profile request is the following complete record, not an asserted outcome:

```text
e_abs_w=EvidenceRef(
  PLUGIN_ISSUER(AWK),coding.implementation-profile,adapter_abstract_accepted,
  CS(EVIDENCE_SCHEMA,implementation_profile))
i_abs_w=EVIDENCE_ENTRY(
  e_abs_w,IMPLEMENTATION_PROFILE_EVIDENCE(
    ABSTRACT_ACCEPTANCE_EVIDENCE(
      IDENTITY_OF(C_w),SNAPSHOT_IDENTITY(F_w),WCERT)))
u_pending_abs_w=UnknownReason(
  PLUGIN_ISSUER(AWK),coding.implementation-profile.pending,
  (IDENTITY_OF(C_w),d_abs))
i_pending_abs_w=EVIDENCE_ENTRY(
  e_abs_w,IMPLEMENTATION_PROFILE_EVIDENCE(
    DIMENSION_EVIDENCE_PENDING(
      IDENTITY_OF(C_w),SNAPSHOT_IDENTITY(F_w),d_abs,u_pending_abs_w)))
coding_entries(H_w)={i_abs_w}
r_task_w=VALUE(TRUE,{}, {})
r_abs_w=ABSTRACT_REASONING_RESULT(
  ReasoningResult.ADMITTED_JUDGMENT(CONSISTENCY_SAT,WCERT))
s_profile_w=IMPLEMENTATION_COVERAGE_SUBJECT(
  IDENTITY_OF(C_w),t_w,F_w,H_w,r_task_w,r_abs_w)
U_profile_w=SERVICE_USE_TRUST_TARGET(
  CAP(profile),PROFILE_COVERAGE,
  PROFILE_USE(PK(implementation_evidence)),semanticIdentity(E_w))
ROOT_PROFILE_W=TrustRootRecord(
  trust_root_key=TR,owner=EMBEDDING_POLICY_PRODUCER(TP),
  trusted_validators={CAP(profile)},
  permitted_certificate_kinds={PROFILE_COVERAGE_EVIDENCE},
  permitted_targets={U_profile_w},adoption=V0_EXTERNAL_TRUST_PREMISE)
T_profile_w=TrustEnvironment(
  trust_policy_key=TP,policy_owner=EMBEDDING_POLICY_PRODUCER(TP),
  root_judgments={TR->TRUST_ROOT_ADMITTED(ROOT_PROFILE_W)})
Q_profile_w=ProfileRequest(
  abi_version=ABI0,profile_key=PK(implementation_evidence),
  semantic_environment=E_w,trust_environment=T_profile_w,
  coverage_subject=s_profile_w,
  capability_target=PROFILE_TARGET(PK(implementation_evidence)),
  capability_key=CAP(profile))
P_w_result=PROFILE_INCOMPLETE(
  PK(implementation_evidence),
  {(PK(implementation_evidence),concrete_implementation_evidence)})
```

`abstract_acceptance_evidence(e_abs_w,s_profile_w)` holds, no entry satisfies
`concrete_implementation_evidence`, there is no pending marker, and the exact
missing set is the singleton displayed in `P_w_result`.  Therefore
`expectedProfile(Q_profile_w,E_w)=P_w_result`, which replaces invocability with
`COMPLETED(P_w_result)`.  Adding a matching concrete evidence entry gives
`PROFILE_COMPLETE`; adding only a pending concrete entry gives
`PROFILE_UNKNOWN`; a conflicting entry or unequal supplied task result gives
`EVALUATION_ERROR`; a symbolic service failure gives `REASONING_ERROR` and no
profile judgment.

### 6.3 Trust and lifecycle

`TP/ATP` and `TR/TRB/TRW/TRA` are embedding-policy identities, not plugin
records.  The first three roots have owner `EMBEDDING_POLICY_PRODUCER(TP)`;
`TRA` has owner `EMBEDDING_POLICY_PRODUCER(ATP)`; every root has adoption
`V0_EXTERNAL_TRUST_PREMISE`.
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

`TRA` is exactly `ROOT_A` and has only the twelve targets and six certificate
subjects enumerated by `UA/AA`; it permits only `CAP(authority)` and
`AUTHORITY_FACT_ATTESTATION`.  It never appears in a coding evaluator,
bounds, confluence, witness, or profile request.  Conversely `TR/TRB/TRW`
cannot admit an authority fact.

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
   `{PLUGIN_PRODUCER(CK),PLUGIN_PRODUCER(APK),PLUGIN_PRODUCER(ATK),
   PLUGIN_PRODUCER(AVK),EMBEDDING_POLICY_PRODUCER(ATP),
   ABI_PRODUCER(ABI0)}` and the root producer is outside
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
| `PathSegment.SEGMENT.segment_atom`; `Path.PATH.segments`; `PathSet` membership | `RETAINED_DELTA` | `CK` Delta value algebra | canonical root-relative path identity and finite scope | segment then path admission | no host access or truth | exact structural equality; inadmitted values malformed in use | snapshots/selectors | C02,C06 | `SEP_PATH` |
| all `ArtifactRole` tags and `OTHER_ROLE.role_atom` | `RETAINED_DELTA` | `CK` Delta value algebra | exact semantic artifact role | none | not authority or format | tag/payload equality | selectors/criteria | C04,C11 | `SEP_ROLE` |
| all `Format` tags and `OTHER_FORMAT.format_atom` | `RETAINED_DELTA` | `CK` Delta value algebra | artifact representation format | none | not backend choice | tag/payload equality | artifact/format criterion | C07 | `SEP_FORMAT` |
| `StorageBackend.{LOCAL_STORAGE,HOSTED_STORAGE}` | `RETAINED_DELTA` | `CK` Delta value algebra | controller-owned storage alternatives only | none | never artifact format | exact two-tag equality | K1 choice | C08 | `SEP_BACKEND_CHOICE` |
| `ByteSize.KIB.integer`; `ContentIdentity.CONTENT_ID.atom`; `FieldId.FIELD.atom`; all `FieldValue` and metric-keyed `BehaviorValue` tags/payloads | `RETAINED_DELTA` | `CK` Delta value algebra | exact scalar and behavior fields | sort-local only | no untyped atom coercion | tag and payload equality | artifacts/observations | C01,C11,C19 | `SEP_SCALAR` |
| all `ArtifactBodyKind` tags; four `ArtifactBody` tags and every payload; four `ArtifactContent` tags and every role/format/size field plus each content, fields-map, and observations-map payload field; total role/format/size/body projections | `RETAINED_DELTA` | `CK` Delta value algebra | exhaustive artifact content with total size/format | scalar roles/format/size/body | no filesystem or backend | complete tagged-field equality | snapshots/criteria | C01,C07,C11 | `SEP_CONTENT` |
| `RepositorySnapshot` map fields; `ChangeEntry.{CREATED.new,DELETED.old,MODIFIED.old,new}`; `ChangeSet` map fields | `RETAINED_DELTA` | `CK` Delta value algebra | complete state and difference-value domains | path/content | no plan/event | extensional maps; modified requires inequality | functions/criteria | C02,C04-C06 | `SEP_CHANGE` |
| three `ArtifactSelector` tags and all path/role fields | `RETAINED_DELTA` | `CK` Delta value algebra | finite supplied-snapshot selection | path set/role | no callback | tagged-field equality | observe/task/events | C01,C06,C11 | `SEP_SELECTOR` |
| all `ArtifactProjection`, `SubjectId`, `Coverage`, and exhaustive request/workload/lane/client `ObservationValue` tags/payloads including absence, role/projection mismatch, and behavior conflict | `RETAINED_DELTA` | `CK` Delta value algebra | typed observation coordinates/results | artifact/scalar types | no truth in an observation | tagged-field equality | observation records | C02,C12,C19 | `SEP_OBSERVATION_VALUE` |
| five `ObservationSpec` tags and every selector/domain/metric/lanes/pairs field | `RETAINED_DELTA` | `CK` Delta value algebra | exhaustive requested projections | selector/subject/field | supplied snapshot only | tag plus complete fields | observe/task | C01,C02,C12,C19 | `SEP_OBSERVATION_SPEC` |
| four `ObservationResult` tags and every `{spec_identity,coverage,values}` field | `RETAINED_DELTA` | `CK` Delta value algebra | exhaustive finite typed observations | exact spec/domain/value | contains no truth | tag/full map equality; admission enforces coverage | equality/task | C01,C02,C18 | `SEP_OBSERVATION_RESULT` |
| all `ObservationRelation` tags and bijection field | `RETAINED_DELTA` | `CK` Delta value algebra | exact comparison choice | result fields only | no callback/service | tag plus exact bijection | task criteria | C02,C12,C19 | `SEP_OBSERVATION_RELATION` |
| `VerificationStatus` tags; `VerificationSpec.{protocol_identity,subject,evidence_schema_key}`; `VerificationRecord.{spec,snapshot_identity,status,observation,evidence_refs}` | `RETAINED_DELTA` | `CK` Delta value algebra | exact snapshot-bound factual record | spec/snapshot/result/schema | evidence distinct from truth | full field equality; wrong snapshot never matches | verification/task | C01,C09,C15 | `SEP_VERIFICATION_RECORD` |
| `ImplementationEvidence`, `CodingEvidencePayload`, `CodingEvidenceEntry`, `AbstractCoverageResult`, and `ImplementationCoverageSubject`: every constructor and displayed field | `RETAINED_DELTA` | `CK` Delta value algebra | exact verification/profile evidence and admitted coverage input | snapshot/task/result fields | reference and payload remain separate | tag/full-field equality | verification/profile | C01,C09,C15,C19 | `SEP_EVIDENCE_PAYLOAD` |
| eight `Criterion` tags and every displayed field | `RETAINED_DELTA` | `CK` Delta value algebra | finite acceptance criteria, not task taxonomy | exact selector/spec/result/scalars | no service/expected answer | tag/full-field equality | direct task meaning | C01,C07,C11,C12,C19 | `SEP_CRITERION` |
| `TaskSpec.TASK.{criteria,required_verifications}` | `RETAINED_DELTA` | `CK` Delta value algebra | arbitrary finite broad predicate input | criterion/verification types | no evaluator/case field | complete set equality | task meaning | C01,C15,C16 | `SEP_TASK_CARDINALITY` |
| `ChangeKind` tags; seven `EventPattern` tags and every key/id/spec/status/path/kind/class/snapshot/selector field | `RETAINED_DELTA` | `CK` Delta value algebra | exhaustive structural event matching | event/payload value types | no command/endpoint | tag/full-field equality | event predicates/grants | C03-C06,C09 | `SEP_EVENT_PATTERN` |
| all six payload types, all eight payload tags, and every command/purpose/spec/snapshot/status/evidence/path/content/contact/release/selector field | `RETAINED_DELTA` | `CK` Delta value algebra | exhaustive typed trace payloads | listed value types | immutable event class external | tag/full-field equality | Outcome admission | C03-C06,C09 | `SEP_EVENT_PAYLOAD` |
| every `TypeDeclaration.{key,admitted_value_domain,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | admission of all section 3 value rows | exact finite type DAG | rejected value malformed | exact `T(n)@(1)`; absence malformed | all typed records | C01-C19 | `SEP_TYPE_DECLARATION` |
| every literal `Declaration.{key,literal_identity,result_type,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | exact typed constants | result type | no meaning/service | structural `L(T,v)@(1)` | K1 literals | C07,C08,C15 | `SEP_LITERAL_DECLARATION` |
| three function `Declaration.{key,symbol_key,argument_types,result_type,facet_positions,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | exact ordered signatures/facets | displayed types | no meaning/service | exact DF/SF `(1)` | terms | C01,C02,C19 | `SEP_FUNCTION_DECLARATION` |
| eight predicate `Declaration.{key,symbol_key,argument_types,result_kind,facet_positions,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | exact Boolean signatures, including snapshot-bound verification | displayed types | no meaning/service | exact DP/SP `(1)` | atoms/grants | C01-C16 | `SEP_PREDICATE_DECLARATION` |
| six `EventDeclaration.{key,event_key,payload_type,event_class,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | immutable class/payload | payload types | caller cannot set class | exact DE/EK `(1)` | outcome/AuthEval | C03-C06,C09 | `SEP_EVENT_DECLARATION` |
| `EventScopePairDeclaration.{pair_key,scope_symbol,occurrence_symbol,controlled_keys,proper_declaration_dependencies}` | `RETAINED_DELTA` | `CK` Delta | exact refresh companion | members/event | no meaning/proof | exact pair `(1)` | conditional requirement | C04,C05 | `SEP_PAIR_DECLARATION` |
| every literal `SemanticBinding` field | `RETAINED_SIGMA` | `CK` Sigma | exact `TERM_VALUE(v)` | declaration/spec roots | empty evidence/access; N/A unknown | derived key; absent open | literal evaluation/model | C07,C08 | `SEP_LITERAL_BINDING` |
| all three function `SemanticBinding` fields | `RETAINED_SIGMA` | `CK` Sigma | exact deterministic `TermResult` | declaration/spec/support | typed input only | exact `(1)`; absent open | term evaluator | C01,C02 | `SEP_FUNCTION_BINDING` |
| all seven ordinary predicate `SemanticBinding` fields | `RETAINED_SIGMA` | `CK` Sigma | exact deterministic `Eval`; direct total task/verification meanings | declaration/spec/support | explicit schema/access/unknown/error | exact `(1)`; absent open | atom evaluator | C01-C16 | `SEP_PREDICATE_BINDING` |
| `EventPairBinding` and complete pair-owned `OccurrenceBindingProjection` fields | `RETAINED_SIGMA` | `CK` Sigma | definitional T3/A1 occurrence | pair/scope/model/lifts | full Eval aggregation | no second ordinary binding | conditional event | C04,C05 | `SEP_PAIR_BINDING` |
| `ProfileBinding` fields and both `ProfileDimensionKey`s | `RETAINED_SIGMA` | `CK` Sigma | implementation evidence coverage | direct task result/evidence | five profile/failure outcomes | exact profile `(1)`; absent open | profile checker | C19 | `SEP_PROFILE_BINDING` |
| all Sigma meaning/profile `ContractSpec` fields, including direct task and snapshot-bound verification relations | `RETAINED_SIGMA` | `CK` Sigma | exact extensional denotations | exact support | explicit primary input only | exact key/role `(1)` | result validator | C01-C19 | `SEP_MEANING_CONTRACT` |
| all Sigma evidence-schema/access-boundary `ContractSpec` fields | `RETAINED_SIGMA` | `CK` Sigma | exact evidence admission/positional access | typed schema/support | undeclared access error | exact key/role `(1)` | evaluator/model | C01,C09,C15 | `SEP_EVIDENCE_ACCESS` |
| all Sigma unknown/evaluation/reasoning-error `ContractSpec` fields | `RETAINED_SIGMA` | `CK` Sigma | honest disjoint outcomes | no hidden support | nonempty stable reasons | exact key/role `(1)` | status boundary | C09,C12,C15 | `SEP_STATUS_FAMILY` |
| every ordinary/pair `ModelContract` and `ModelCapabilitySummary` field | `RETAINED_SIGMA` | exact target projection | complete model/machine identity | binding contracts/descriptors | prose diagnostic only | named exact key; absent open/wrong malformed | model-facing lookup | C05,C13,C15 | `SEP_MODEL` |
| coding `EvidenceRef.{issuer_scope,evidence_namespace,local_identity,schema_binding}` values: every verification reference plus `e_abs_w` and `e0` | `RETAINED_SIGMA` | K1 carrier under exact coding schema | stable support identity only | exact schema key | no embedded truth/authority | full identity equality; unique reference-to-payload map | verification/profile meaning | C01,C09,C15,C19 | `SEP_EVIDENCE_REFERENCE` |
| every field of `FSOUND/QSOUND/PROFSOUND/BSOUND/BCOMPLETE/WSOUND/CSOUND`, `FREQ/QREQ/PROFREQ/BREQ/CREQ/WREQ`, `FFAIL/QFAIL/PROFFAIL/BFAIL/CFAIL/WFAIL`, `LEX_SOUND/LEX_REQ/LEX_FAIL`, `PSOUND/PCOMPLETE/PEVIDENCE/PFAILURE`, and the finite authority/evolution service specs, including their closed typed admission-subject domains | `RETAINED_SERVICE` | owning service layer | exact field-total fragments/evidence/failure boundaries | only literal legal query maps; `CSOUND` has the two-node DAG | no denotation/truth shortcut | exact role/key/type; omission incompatible | capabilities | C01,C11,C19 | `SEP_FRAGMENT` |
| every field of `CAP(functions)`, `CAP(predicates)`, and `CAP(profile)` descriptors | `RETAINED_SERVICE` | `CK` Service | concrete binding/profile targets | complete closures | exact service-use roots | exact service/capability `(1)` | invocation | C01-C16,C19 | `SEP_EVALUATOR_CAPABILITY` |
| every field of provider descriptors `CAP(bounds)`, `CAP(confluence)`, `CAP(witness)`, and `LEX_CAP` | `RETAINED_SERVICE` | `CK`/`AWK` Service | exact finite environment/formula targets | `D_b/D_c/D_w/D_lex` | admitted proof or permitted inconclusive/error | exact target/version; no fallback | reasoning requests | C11,C19 | `SEP_PROVIDER_CAPABILITY` |
| every field of `CAP(validate_bounds)` and `CAP(validate_witness)` descriptors | `RETAINED_SERVICE` | independent `RVK` Service | exact certificate validation capabilities | complete subject dependency sets | separately trusted validation | exact validator/version; missing evaluability status | derived validator request | C11,C19 | `SEP_VALIDATOR_CAPABILITY` |
| exact `ReasoningRequest` fields of `R_b`, `R_w`, and `R_c`; exact `J_b/J_w/J_c` targets | `RETAINED_SERVICE` | request former | exact subject/environment/trust/fragment/dependencies/target/capability | `D_b/D_w/D_c` | no alternate `chi_C` | complete request identity | reasoner/certificate | C11,C19 | `SEP_REASONING_REQUEST` |
| `BCERT`/`WCERT` keys; every `CertificateEnvelope` field of `BENV`/`WENV`; every `BundleBoundsProof`/`AdapterWitness` payload field; `BPROOF_REF/WPROOF_REF` | `RETAINED_SERVICE` | `CK`/`AWK` certificate producer | exact contradiction/witness claims | full requests/environments/dependencies | exact validator/root/abstraction/evidence | certificate/key equality; no fallback | certificate gate | C11,C19 | `SEP_REASONING_CERTIFICATE` |
| `TrustPolicyKey TP`; root keys `TR/TRB/TRW`; every admitted `TrustRootRecord` permission/owner/adoption field and all five `TrustRootJudgment` variants/reason fields | `RETAINED_SERVICE` | embedding policy | independent exact service/certificate trust | full producer sets | five branches distinct | exact policy/root versions | discovery/admission | C01,C11,C19 | `SEP_TRUST` |
| alternate pair-proof keys `PVC/PCERT`; every field of `PSOUND/PCOMPLETE/PEVIDENCE/PFAILURE`, `CapabilityDescriptor(PVC)`, `ROOT_p/T_p`, complete occurrence bundle, and `PAIR_PROOF_REF` | `RETAINED_SERVICE` | independent pair-validator/certificate producers | exact independent pair admission fixture | pair subject plus validation references | rejection/failure proves nothing | exact fixture keys | pair validator | C05 | `SEP_PAIR_PROOF` |
| every `SourceRef.{issuer,source_kind,stable_source_identity,provenance_facts}` value `SRC(z,i)` and `src0`; every `AuthorityRef.{owner,authority_namespace,stable_attestation_identity}` value `AUTH(z,i)` and `auth0` | `RETAINED_SIGMA` | inherited K1 carrier; attributed-source/authority producers | provenance and authority identities remain disjoint | no semantic support | neither record admits authority | complete structural identity | origins/adoption | C13,C19 | `SEP_SOURCE_AUTHORITY` |
| every field of `AC(z,i).{authority_fact_key,admission_subject_data,offered_evidence_refs}`, the two exact `AuthorityAttestationSubjectIdentity` tags, every field of typed `ATTEST(z,i)`, and `AE_REF(z,i)` for the six members of `I_A` | `RETAINED_SERVICE` | inherited K1 carrier at the `APK/ATK` authority-admission boundary | exact finite authority candidate and closed attestation algebra | fact-free base and attestation schema | evidence is not admission; fact key is not a binding | exact tag/field/tuple/ref identity | authority validator | C13,C19 | `SEP_AUTHORITY_CANDIDATE` |
| every field of the six `AFB(z,i)=AuthorityFactBinding(AF(z,i),{ACERT(z,i)})` and their final authority-map entries | `RETAINED_SIGMA` | admitted Sigma receiving rule | exact normative adoption/choice binding | successful independent admission | certificate set is mandatory | exact fact-key map identity; absent stays open | Contract closure | C13,C19 | `SEP_AUTHORITY_BINDING` |
| every field of `ASOUND/ACOMPLETE/AREQUIRED/AFAILURE`, `ServiceIdentityRecord(AVSK)`, and `CapabilityDescriptor(CAP(authority))` | `RETAINED_SERVICE` | independent `AVK` Service | exact six-target authority validation fragment | union of six fact-free dependency closures | only typed attestations and exact error mapping | exact ATP/AVK versions | authority requests | C13,C19 | `SEP_AUTHORITY_CAPABILITY` |
| `ATP/TRA`; every field of `ROOT_A/T_A`; every field of the six `RA(z,i)` and `AENV(z,i)`; all six `ACERT(z,i)` keys | `RETAINED_SERVICE` | external embedding policy / attestation validator | exact service-use and authority target scopes | exact `DA/JA/UA/AA` records | proper producer independence | request/envelope/root exact identity | authority certificate gate | C13,C19 | `SEP_AUTHORITY_REQUEST` |
| every field of the five `Q_t[T_x]`, `R_lex`, and `Q_profile_w`; exact request-specific Semantic/Trust/DependencyEnvironment carriers (ProfileRequest has no dependency-environment field) | `RETAINED_SERVICE` | inherited K2 invocation carrier; request former | predicate, formula, and profile invocations | exact `E_t/D_t`, `E_lex/D_lex`, and profile-closed `E_w` | trust and evidence remain explicit fields | complete request identity | discovery/invocation | C01,C09,C15,C19 | `SEP_FINITE_REQUEST` |
| every field of `R_p`, its `PairFullEvalProof`, fixed `ALL_ADMITTED_TRACES`/`COMPLETE_EVAL_RECORD` tags, `PENV`, and its exact `PairValidationResult` | `RETAINED_SERVICE` | inherited K2 pair-admission carrier; pair request/proof former | exact independent full-Eval equality admission | `E_p/D_p` plus exactly two non-proper validation refs | sole `PAIR_PROOF_REF` in pair-service row | tag/request/result/certificate exact | pair admission | C05 | `SEP_PAIR_REQUEST` |
| `m0.{migration_key,source_environment,target_environment,semantic_relation,relation_contract}`; `x0/x1.{extension_key,target_record_identity,owner_layer,semantic_effect,payload}`; every field of `a0/a1`; every field of `MR0/XE0/XP0` | `RETAINED_SIGMA` | exact `EOK` Sigma/evolution owners | explicit migration relation, extension effect/payload, and aliases | exact target/source keys/environments | no implicit migration or alias substitution | exact record keys and versions | K3-X missing matrix | C10,C17 | `SEP_EVOLUTION_RECORD` |
| `m0.{certificate_key,validator_key,trust_root_key}`; every field of `c0/CC0`; `x0/x1.{certificate_key,validator_key,trust_root_key}`; every field of the three `PKG_evo_*` package membership records | `RETAINED_SERVICE` | K2 evolution-validation/package surface with exact declared owners | compatibility and mandatory independent validation references | exact source/target/certificate/capability/root keys | absent admission gives no migration/compatibility/effect | exact record/package identities | K3-X missing matrix | C10,C17 | `SEP_EVOLUTION_SERVICE_RECORD` |
| every field of the literal `EVCAP_m/EVCAP_c/EVCAP_x0/EVCAP_x1` descriptors and their sixteen named specs, `ROOT_E/T_evo`, `R_m/R_c0/R_x0/R_x1`, four named `EENV`/`EADMIT` records, and `ER_m/ER_c/ER_x0/ER_x1` | `RETAINED_SERVICE` | independent `EVK/EPK/TP` | four finite evolution admissions | exact four `D_ev/TARGET` records and non-proper triples | one typed proof/ref per row | exact request/envelope/admission identity | evolution validation | C10,C17 | `SEP_EVOLUTION_ADMISSION` |
| `SNAPSHOT_IDENTITY(F)`, `changes_between(P,F)`, `observe(spec,F)`, and direct per-criterion/per-verification task projections | `DERIVED` | exact coding relations | total extensional outputs | supplied typed values | no ambient access | complete logical equality | meanings/payloads | C01-C19 | A04/A05/A09: derived output versus primitive assertion |
| `coding_entries`, `evidence_map`, exact schema/ref membership, equal-duplicate coalescence, unequal-payload conflict, and metric-keyed behavior aggregation | `DERIVED` | K3-S total projection | unique extensional observation/evidence maps | finite supplied artifact/evidence records | absent/mismatch/conflict constructors exhaustive | no prose selection alias | observe/verification/profile | C01,C09,C11,C15,C19 | `SEP_TOTAL_PROJECTION` |
| K1 goal/preserve/forbid/allow/conditional/alternative patterns | `DERIVED` | K1 | exact macro/composition | syntax dependencies | K1 T1-T4/A1-A2 | no coding key | Contracts | C01-C09 | A06-A08: normative roles |
| K2 binding keys, supports, closures, observation maps, summaries, lifecycle, service identity, and validation-reference projections | `DERIVED` | K2 | mechanical views | exhaustive graph | owner-specific missing/error | cannot be supplied | validators | C01-C19 | A03/A14/A15: lifecycle/graph/conflict |
| derived `CertificateValidationRequest` fields and `CertificateAdmission`/receiving projections for BENV/WENV/pair fixture | `DERIVED` | K2 certificate gate | exact independent validation invocation/result | original request/envelope/root | failures yield no claim | derived identity only | reasoning/pair result | C05,C11,C19 | `SEP_CERTIFICATE_RECEPTION` |
| six derived authority validation requests, six exact admissions/results/receptions, and recomputed subject-producer sets | `DERIVED` | K2 authority gate | one fact-free validation per adoption/choice then exact map union | `RA/AENV/ROOT_A` | no self-support or prior-fact chain | derived request/result identities only | authority map | C13,C19 | `SEP_AUTHORITY_RECEPTION` |
| per-`FixtureId` authoritative record map, equal-duplicate coalescence, conflict sets, package/record permutation result, and row-local `missingStatus` projection | `DERIVED` | K2 composition | order-independent exact output within one tagged universe | record identities and reconstruction sets | no cross-entry union or last-writer fallback | finite tagged map equality | composition/K3-X | C01-C19 | A14: equality/conflict/order |
| exact two-node observation maps for the two separately tagged valid confluence orders | `DERIVED` | K2 §3.3 | identical complete maps/results/statuses | `observe` and `changes_between` nodes | interface failure aborts | per-tag map equality | K3-X check 9 | C01,C02 | `SEP_CONFLUENCE` |
| change set as patch/action sequence; event payload as executable command/endpoint | `EXCLUDED` | none | no declarative denotation | none | presence violates access boundary | never an identity | none | C03-C06,C19 | K3S-A18: satisfying semantics without implementation |
| universal string/map/opaque handle for path, task, evidence, result, or expected answer | `EXCLUDED` | none | destroys typed distinction | none | presence malformed/oracular | never an identity | none | C01,C02,C09,C15 | K3S-A05,A17: typed reusable values versus escape hatch |
| task taxonomy, phrase-indexed symbols, challenge IDs, expected mappings, gold Contracts/patches | `EXCLUDED` | none | no semantic role | none | presence rejects | never an identity | none | C01,C15,C18 | K3S-A17: equivalent phrasing shares symbols |
| implicit version/name/order fallback, plugin-owned truth/authority/choice/connective/failure rule | `EXCLUDED` | none | owned by K1/K2 or invalid | none | fail loud in owning family | never an identity | none | C04,C08,C10,C13,C17 | K3S-A01,A02,A13: exact identity and ownership |
| implementation, parser, binder, planner, executor, repository/filesystem/network operation, model/prompt/benchmark | `EXCLUDED` | none | outside K3-S | none | no semantic result | never an identity | none | C01-C19 | K3S-A18: abstract outcome is not construction |
<!-- K3S-LEDGER-END -->

Ledger count: **65** rows: 24 `RETAINED_DELTA`, 13 `RETAINED_SIGMA`,
15 `RETAINED_SERVICE`, 8 `DERIVED`, and 5 `EXCLUDED`, under the exact body-row
convention above.  The split is
recomputable from the second cell alone.

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

Every retained or supplied ledger row instead names one finite exact paired
fixture.  This avoids sub-case labels.  Define

```text
SeparationRecord = SEPARATES(
  exact_id,left_records,right_records,left_status,right_status)
```

and let `r[f:=v]` mean the complete record `r` with exactly field `f` replaced
by exact value `v`; all undisplayed fields are definitionally equal.  The
following is the entire finite `SeparationRecord` set:

| exact record | left records / status | right records / status |
|---|---|---|
| `SEP_PATH` | `{PATH((SEGMENT(dependency),SEGMENT(lock)))}` / `WELL_FORMED` | `{PATH((SEGMENT(lock),SEGMENT(dependency)))}` / `WELL_FORMED` |
| `SEP_ROLE` | `{DEPENDENCY_LOCK}` / `WELL_FORMED` | `{PUBLIC_SCHEMA}` / `WELL_FORMED` |
| `SEP_FORMAT` | `{TEXT}` / `WELL_FORMED` | `{JSON}` / `WELL_FORMED` |
| `SEP_BACKEND_CHOICE` | `{LOCAL_STORAGE}` / `WELL_FORMED` | `{HOSTED_STORAGE}` / `WELL_FORMED` |
| `SEP_SCALAR` | `{KIB(1),FIELD(request_field),BEHAVIOR_METRIC(FIELD(latency),1)}` / `WELL_FORMED` | `{KIB(2),FIELD(client_field),BEHAVIOR_METRIC(FIELD(latency),2)}` / `WELL_FORMED` |
| `SEP_CONTENT` | `{a_b}` / `WELL_FORMED` | `{a_b[format:=JSON]}` / `WELL_FORMED` |
| `SEP_CHANGE` | `{CREATED(a_b)}` / `WELL_FORMED` | `{DELETED(a_b)}` / `WELL_FORMED` |
| `SEP_SELECTOR` | `{SELECT_PATHS({p_b})}` / `WELL_FORMED` | `{SELECT_ROLE(DEPENDENCY_LOCK)}` / `WELL_FORMED` |
| `SEP_OBSERVATION_VALUE` | `{PRESENT_CONTENT(a_b)}` / `WELL_FORMED` | `{ABSENT}` / `WELL_FORMED` |
| `SEP_OBSERVATION_SPEC` | `{s_c}` / `WELL_FORMED` | `{WORKLOAD_METRIC_VIEW({WORKLOAD_SUBJECT(main)},FIELD(latency))}` / `WELL_FORMED` |
| `SEP_OBSERVATION_RESULT` | `{O_c}` / `WELL_FORMED` | `{O_c[values:={p_b->ABSENT}]}` / `WELL_FORMED` |
| `SEP_OBSERVATION_RELATION` | `{EQUAL}` / `WELL_FORMED` | `{FIELD_CORRESPONDENCE(m_w)}` / `WELL_FORMED` |
| `SEP_VERIFICATION_RECORD` | `{vr0}` / `WELL_FORMED` | `{vr0[status:=FAIL]}` / `WELL_FORMED` |
| `SEP_EVIDENCE_PAYLOAD` | `{i_abs_w}` / `WELL_FORMED` | `{i_pending_abs_w}` / `WELL_FORMED` |
| `SEP_CRITERION` | `{ARTIFACTS_NONEMPTY(S_b)}` / `WELL_FORMED` | `{ARTIFACT_SIZE_LT(S_b,KIB(100))}` / `WELL_FORMED` |
| `SEP_TASK_CARDINALITY` | `{TASK({},{})}` / `WELL_FORMED` | `{TASK({ARTIFACT_SIZE_LT(S_b,KIB(100))},{})}` / `WELL_FORMED` |
| `SEP_EVENT_PATTERN` | `{ANY_EVENT(EK(command))}` / `WELL_FORMED` | `{ANY_EVENT(EK(network_contact))}` / `WELL_FORMED` |
| `SEP_EVENT_PAYLOAD` | `{COMMAND_EVENT(command0,build)}` / `WELL_FORMED` | `{NETWORK_CONTACT(public_registry,build)}` / `WELL_FORMED` |
| `SEP_TYPE_DECLARATION` | `{E_c}` / `WELL_FORMED` | `{E_c[declarations:=E_c.declarations minus {TypeDeclaration(T(Path))}]}` / `MALFORMED` |
| `SEP_LITERAL_DECLARATION` | `{E_b}` / `WELL_FORMED` | `{E_b[declarations:=E_b.declarations minus {LiteralDeclaration(T(TaskSpec),ts_nonempty)}]}` / `MALFORMED` |
| `SEP_FUNCTION_DECLARATION` | `{Declaration(DF(observe))}` / `WELL_FORMED` | `{Declaration(DF(observe))[facet_positions:=({}, {})]}` / `MALFORMED` |
| `SEP_PREDICATE_DECLARATION` | `{Declaration(DP(task_accepts))}` / `WELL_FORMED` | `{d_bad}` / `MALFORMED` |
| `SEP_EVENT_DECLARATION` | `{Declaration(DE(network_contact))}` / `WELL_FORMED` | `{Declaration(DE(network_contact))[event_class:=OBSERVATIONAL]}` / `MALFORMED` |
| `SEP_PAIR_DECLARATION` | `{E_p}` / `WELL_FORMED` | `{E_p[pair_declarations:={}]}` / `MALFORMED` |
| `SEP_LITERAL_BINDING` | `{E_b}` / `CLOSED` | `{E_b[bindings:=E_b.bindings minus {SemanticBinding(L(T(TaskSpec),ts_nonempty))}]}` / `OPEN_BINDINGS` |
| `SEP_FUNCTION_BINDING` | `{E_c}` / `CLOSED` | `{E_c[bindings:=E_c.bindings minus {SemanticBinding(DF(observe))}]}` / `OPEN_BINDINGS` |
| `SEP_PREDICATE_BINDING` | `{E_t}` / `CLOSED` | `{E_t[bindings:={}]}` / `OPEN_BINDINGS` |
| `SEP_PAIR_BINDING` | `{E_p}` / `CLOSED` | `{E_p[pair_bindings:={}]}` / `OPEN_BINDINGS` |
| `SEP_PROFILE_BINDING` | `{E_w}` / `CLOSED` | `{E_w[profile_bindings:={}]}` / `OPEN_BINDINGS` |
| `SEP_MEANING_CONTRACT` | `{CS(PREDICATE_MEANING,task_accepts)}` / `CLOSED` | `{CS(PREDICATE_MEANING,task_accepts)[logical_relation:={}]}` / `MALFORMED` |
| `SEP_EVIDENCE_ACCESS` | `{CS(EVIDENCE_SCHEMA,verification)}` / `WELL_FORMED` | `{CS(EVIDENCE_SCHEMA,implementation_profile)}` / `WELL_FORMED` |
| `SEP_STATUS_FAMILY` | `{VALUE(FALSE,{},{})}` / `TRUTH_FALSE` | `{VALUE(UNKNOWN,{},{u0})}` / `TRUTH_UNKNOWN` |
| `SEP_MODEL` | `Omega_t` / `CLOSED` | `Omega_t minus {MODEL_task_accepts}` / `OPEN_BINDINGS(model contract)` |
| `SEP_EVIDENCE_REFERENCE` | `{e_abs_w}` / `WELL_FORMED` | `{e_abs_w[schema_binding:=CS(EVIDENCE_SCHEMA,verification)]}` / `WELL_FORMED` |
| `SEP_FRAGMENT` | `{BSOUND}` / `WELL_FORMED` | `{WSOUND}` / `WELL_FORMED` |
| `SEP_EVALUATOR_CAPABILITY` | `{Q_t[T_admitted],CAP(predicates)}` / `INVOCABLE_FOR(Q_t[T_admitted])` | `{Q_t[T_admitted]}` with `CAP(predicates)` absent / `EVALUABILITY_MISSING` |
| `SEP_PROVIDER_CAPABILITY` | `{R_b,CAP(bounds)}` / `INVOCABLE_FOR(R_b)` | `{R_b,CAP(witness)}` with `CAP(bounds)` absent / `EVALUABILITY_MISSING` |
| `SEP_VALIDATOR_CAPABILITY` | `{certificateValidationRequest(BENV),CAP(validate_bounds)}` / `INVOCABLE_FOR(certificateValidationRequest(BENV))` | `{certificateValidationRequest(BENV)}` with `CAP(validate_bounds)` absent / `EVALUABILITY_MISSING` |
| `SEP_REASONING_REQUEST` | `{R_b}` / `INVOCABLE_FOR(R_b)` | `{R_b[complete_dependencies:=D_w]}` / `MALFORMED_REQUEST` |
| `SEP_REASONING_CERTIFICATE` | `{BENV}` / `CertificateAdmission.ADMITTED(BCERT,CONSISTENCY_UNSAT)` | `{BENV[payload:=AdapterWitness]}` / `CertificateAdmission.MALFORMED_ENVELOPE` |
| `SEP_TRUST` | `{Q_t[T_undecided]}` / `EVALUABILITY_UNKNOWN` | `{Q_t[T_incompatible]}` / `EVALUABILITY_MISSING` |
| `SEP_PAIR_PROOF` | `{PENV}` / `CertificateAdmission.ADMITTED(PCERT,PAIR_COHERENCE_ADMITTED(PAIR(refresh),PCERT))` | `{PENV[payload:=BundleBoundsProof]}` / `CertificateAdmission.MALFORMED_ENVELOPE` |
| `SEP_SOURCE_AUTHORITY` | `{SRC(b,1)}` / `WELL_FORMED` | `{AUTH(b,1)}` / `WELL_FORMED` |
| `SEP_AUTHORITY_CANDIDATE` | `{AC(b,1)}` / `WELL_FORMED` | `{AC(b,1)[admission_subject_data:=ATTEST(c,1)]}` / `WELL_FORMED` |
| `SEP_AUTHORITY_BINDING` | `{E_b}` / `CLOSED` | `{E_b^0}` / `OPEN_BINDINGS({AUTHORITY_FACT(AF(b,1))})` |
| `SEP_AUTHORITY_CAPABILITY` | `{RA(b,1),CAP(authority)}` / `INVOCABLE_FOR(RA(b,1))` | `{RA(b,1)}` with `CAP(authority)` absent / `EVALUABILITY_MISSING` |
| `SEP_AUTHORITY_REQUEST` | `{RA(b,1)}` / `INVOCABLE_FOR(RA(b,1))` | `{RA(b,1)[environment_without_fact:=E_b]}` / `MALFORMED_REQUEST` |
| `SEP_FINITE_REQUEST` | `{Q_t[T_admitted]}` / `INVOCABLE_FOR(Q_t[T_admitted])` | `{Q_t[T_failed]}` / `DISCOVERY_FAILED` |
| `SEP_PAIR_REQUEST` | `{R_p}` / `INVOCABLE_FOR(R_p)` | `{pair_subject[trace_domain:=TRACE_SUBSET({})],R_p}` / `MALFORMED` |
| `SEP_EVOLUTION_RECORD` | `{PKG_evo_EOK}` / `WELL_FORMED` | `{PKG_evo_EOK_no_a1}` / `MALFORMED(missing alias AK1)` |
| `SEP_EVOLUTION_SERVICE_RECORD` | `{PKG_evo_EOK}` / `WELL_FORMED` | `{PKG_evo_EOK_no_m}` / `NO_MIGRATION(MK0)` |
| `SEP_EVOLUTION_ADMISSION` | `{EENV_m}` / `CertificateAdmission.ADMITTED(EC_m,MIGRATION_RELATION_ADMITTED(MK0,EC_m))` | `{EENV_m_bad_root}` / `CertificateAdmission.MALFORMED_ENVELOPE` |

There are exactly 52 `SeparationRecord` rows, one for each retained
ledger row.  The pair table does not add adversarial cases; each record cites
the applicable one of the 18 `K3S-A01..A18` case rows through its ledger row.

## 9. K3-X semantic input boundary

### 9.1 Smallest finite semantic packet

This section freezes semantic inputs only.  It does not select a language,
module, representation, path, command, output directory, test framework, or
implementation technique.

The packet is the following closed finite family.  These are the only typed
Service/evolution admission values that the finite fixtures invoke:

```text
bounds_subject_b=BOUNDS_SUBJECT(S_b,ts_nonempty,ts_lt_100,ts_ge_200)
confluence_subject_c=CONFLUENCE_SUBJECT(s_c,P_c,F_c)
witness_subject_w=ADAPTER_WITNESS_SUBJECT(
  IDENTITY_OF(C_w),s_w,t_w,P_w,F_w)
predicate_subject_t=PREDICATE_CALL_SUBJECT(
  DP(task_accepts),(t_t,F_t,EVIDENCE_t))
profile_subject_w=PROFILE_CALL_SUBJECT(
  PK(implementation_evidence),s_profile_w)

L_X={
  ts_nonempty:T(TaskSpec),ts_lt_100:T(TaskSpec),ts_ge_200:T(TaskSpec),
  s_c:T(ObservationSpec),P_c:T(RepositorySnapshot),
  F_c:T(RepositorySnapshot),O_c:T(ObservationResult),
  s_w:T(ObservationSpec),t_w:T(TaskSpec),t_t:T(TaskSpec),
  LOCAL_STORAGE:T(StorageBackend),HOSTED_STORAGE:T(StorageBackend),
  ALL_ADMITTED_TRACES:T(PairTraceDomain),
  COMPLETE_EVAL_RECORD:T(PairComparedFields),
  BOUNDS_CLAUSE:T(AuthorityClauseTag),
  CONFLUENCE_OBSERVATION_CLAUSE:T(AuthorityClauseTag),
  CONFLUENCE_CHANGE_CLAUSE:T(AuthorityClauseTag),
  ADAPTER_PRESERVATION_CLAUSE:T(AuthorityClauseTag),
  ADAPTER_ACCEPTANCE_CLAUSE:T(AuthorityClauseTag),
  attestation_subject_identity(b,1):T(AuthorityAttestationSubjectIdentity),
  attestation_subject_identity(c,1):T(AuthorityAttestationSubjectIdentity),
  attestation_subject_identity(c,2):T(AuthorityAttestationSubjectIdentity),
  attestation_subject_identity(w,1):T(AuthorityAttestationSubjectIdentity),
  attestation_subject_identity(w,2):T(AuthorityAttestationSubjectIdentity),
  attestation_subject_identity(choice,1):T(AuthorityAttestationSubjectIdentity),
  ATTEST(b,1):T(AuthorityAttestationValue),
  ATTEST(c,1):T(AuthorityAttestationValue),
  ATTEST(c,2):T(AuthorityAttestationValue),
  ATTEST(w,1):T(AuthorityAttestationValue),
  ATTEST(w,2):T(AuthorityAttestationValue),
  ATTEST(choice,1):T(AuthorityAttestationValue),
  bounds_subject_b:T(ServiceAdmissionSubject),
  confluence_subject_c:T(ServiceAdmissionSubject),
  witness_subject_w:T(ServiceAdmissionSubject),
  predicate_subject_t:T(ServiceAdmissionSubject),
  profile_subject_w:T(ServiceAdmissionSubject),
  pair_subject:T(ServiceAdmissionSubject),
  authority_subject(b,1):T(ServiceAdmissionSubject),
  authority_subject(c,1):T(ServiceAdmissionSubject),
  authority_subject(c,2):T(ServiceAdmissionSubject),
  authority_subject(w,1):T(ServiceAdmissionSubject),
  authority_subject(w,2):T(ServiceAdmissionSubject),
  authority_subject(choice,1):T(ServiceAdmissionSubject),
  mr_subject:T(EvolutionAdmissionSubject),
  cc_subject:T(EvolutionAdmissionSubject),
  x0_subject:T(EvolutionAdmissionSubject),
  x1_subject:T(EvolutionAdmissionSubject)}

TYPE_X={
  T(PathSegment),T(Path),T(PathSet),T(ArtifactRole),T(Format),
  T(StorageBackend),T(ByteSize),T(ContentIdentity),T(FieldId),T(FieldValue),
  T(SubjectId),T(BehaviorValue),T(ArtifactBody),T(ArtifactBodyKind),
  T(ArtifactContent),T(ObservationValue),T(RepositorySnapshot),
  T(SnapshotIdentity),T(ChangeEntry),T(ChangeSet),T(ArtifactSelector),
  T(ArtifactProjection),T(Coverage),T(ObservationSpec),T(ObservationResult),
  T(ObservationRelation),T(VerificationStatus),T(VerificationSpec),
  T(VerificationRecord),T(ImplementationEvidence),T(CodingEvidencePayload),
  T(CodingEvidenceEntry),T(AbstractCoverageResult),
  T(ImplementationCoverageSubject),T(PairTraceDomain),T(PairComparedFields),
  T(AuthorityClauseTag),
  T(AuthorityAttestationSubjectIdentity),T(AuthorityAttestationValue),
  T(ServiceAdmissionSubject),
  T(EvolutionAdmissionSubject),T(Criterion),T(TaskSpec),T(ChangeKind),
  T(CommandId),T(ContactClass),T(ReleaseId),T(Purpose),T(EventPattern),
  T(CommandEventPayload),T(TestEventPayload),T(PathChangeEventPayload),
  T(NetworkContactEventPayload),T(ReleaseEventPayload),
  T(DependencyRefreshEventPayload)}

DELTA_TYPE_X={
  TypeDeclaration(T(PathSegment)),TypeDeclaration(T(Path)),
  TypeDeclaration(T(PathSet)),TypeDeclaration(T(ArtifactRole)),
  TypeDeclaration(T(Format)),TypeDeclaration(T(StorageBackend)),
  TypeDeclaration(T(ByteSize)),TypeDeclaration(T(ContentIdentity)),
  TypeDeclaration(T(FieldId)),TypeDeclaration(T(FieldValue)),
  TypeDeclaration(T(SubjectId)),TypeDeclaration(T(BehaviorValue)),
  TypeDeclaration(T(ArtifactBody)),TypeDeclaration(T(ArtifactBodyKind)),
  TypeDeclaration(T(ArtifactContent)),TypeDeclaration(T(ObservationValue)),
  TypeDeclaration(T(RepositorySnapshot)),TypeDeclaration(T(SnapshotIdentity)),
  TypeDeclaration(T(ChangeEntry)),TypeDeclaration(T(ChangeSet)),
  TypeDeclaration(T(ArtifactSelector)),TypeDeclaration(T(ArtifactProjection)),
  TypeDeclaration(T(Coverage)),TypeDeclaration(T(ObservationSpec)),
  TypeDeclaration(T(ObservationResult)),TypeDeclaration(T(ObservationRelation)),
  TypeDeclaration(T(VerificationStatus)),TypeDeclaration(T(VerificationSpec)),
  TypeDeclaration(T(VerificationRecord)),TypeDeclaration(T(ImplementationEvidence)),
  TypeDeclaration(T(CodingEvidencePayload)),TypeDeclaration(T(CodingEvidenceEntry)),
  TypeDeclaration(T(AbstractCoverageResult)),
  TypeDeclaration(T(ImplementationCoverageSubject)),
  TypeDeclaration(T(PairTraceDomain)),TypeDeclaration(T(PairComparedFields)),
  TypeDeclaration(T(AuthorityClauseTag)),
  TypeDeclaration(T(AuthorityAttestationSubjectIdentity)),
  TypeDeclaration(T(AuthorityAttestationValue)),
  TypeDeclaration(T(ServiceAdmissionSubject)),
  TypeDeclaration(T(EvolutionAdmissionSubject)),TypeDeclaration(T(Criterion)),
  TypeDeclaration(T(TaskSpec)),TypeDeclaration(T(ChangeKind)),
  TypeDeclaration(T(CommandId)),TypeDeclaration(T(ContactClass)),
  TypeDeclaration(T(ReleaseId)),TypeDeclaration(T(Purpose)),
  TypeDeclaration(T(EventPattern)),TypeDeclaration(T(CommandEventPayload)),
  TypeDeclaration(T(TestEventPayload)),TypeDeclaration(T(PathChangeEventPayload)),
  TypeDeclaration(T(NetworkContactEventPayload)),
  TypeDeclaration(T(ReleaseEventPayload)),
  TypeDeclaration(T(DependencyRefreshEventPayload))}

DELTA_LITERAL_X={
  LiteralDeclaration(T(TaskSpec),ts_nonempty),
  LiteralDeclaration(T(TaskSpec),ts_lt_100),
  LiteralDeclaration(T(TaskSpec),ts_ge_200),
  LiteralDeclaration(T(ObservationSpec),s_c),
  LiteralDeclaration(T(RepositorySnapshot),P_c),
  LiteralDeclaration(T(RepositorySnapshot),F_c),
  LiteralDeclaration(T(ObservationResult),O_c),
  LiteralDeclaration(T(ObservationSpec),s_w),
  LiteralDeclaration(T(TaskSpec),t_w),LiteralDeclaration(T(TaskSpec),t_t),
  LiteralDeclaration(T(StorageBackend),LOCAL_STORAGE),
  LiteralDeclaration(T(StorageBackend),HOSTED_STORAGE),
  LiteralDeclaration(T(PairTraceDomain),ALL_ADMITTED_TRACES),
  LiteralDeclaration(T(PairComparedFields),COMPLETE_EVAL_RECORD),
  LiteralDeclaration(T(AuthorityClauseTag),BOUNDS_CLAUSE),
  LiteralDeclaration(T(AuthorityClauseTag),CONFLUENCE_OBSERVATION_CLAUSE),
  LiteralDeclaration(T(AuthorityClauseTag),CONFLUENCE_CHANGE_CLAUSE),
  LiteralDeclaration(T(AuthorityClauseTag),ADAPTER_PRESERVATION_CLAUSE),
  LiteralDeclaration(T(AuthorityClauseTag),ADAPTER_ACCEPTANCE_CLAUSE),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(b,1)),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(c,1)),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(c,2)),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(w,1)),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(w,2)),
  LiteralDeclaration(T(AuthorityAttestationSubjectIdentity),
                     attestation_subject_identity(choice,1)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(b,1)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(c,1)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(c,2)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(w,1)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(w,2)),
  LiteralDeclaration(T(AuthorityAttestationValue),ATTEST(choice,1)),
  LiteralDeclaration(T(ServiceAdmissionSubject),bounds_subject_b),
  LiteralDeclaration(T(ServiceAdmissionSubject),confluence_subject_c),
  LiteralDeclaration(T(ServiceAdmissionSubject),witness_subject_w),
  LiteralDeclaration(T(ServiceAdmissionSubject),predicate_subject_t),
  LiteralDeclaration(T(ServiceAdmissionSubject),profile_subject_w),
  LiteralDeclaration(T(ServiceAdmissionSubject),pair_subject),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(b,1)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(c,1)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(c,2)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(w,1)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(w,2)),
  LiteralDeclaration(T(ServiceAdmissionSubject),authority_subject(choice,1)),
  LiteralDeclaration(T(EvolutionAdmissionSubject),mr_subject),
  LiteralDeclaration(T(EvolutionAdmissionSubject),cc_subject),
  LiteralDeclaration(T(EvolutionAdmissionSubject),x0_subject),
  LiteralDeclaration(T(EvolutionAdmissionSubject),x1_subject)}

DELTA_SYMBOL_X={
  FunctionDeclaration(DF(snapshot_of)),
  FunctionDeclaration(DF(changes_between)),FunctionDeclaration(DF(observe)),
  PredicateDeclaration(DP(observations_equal)),
  PredicateDeclaration(DP(task_accepts)),
  PredicateDeclaration(DP(dependency_metadata_changed)),
  PredicateDeclaration(DP(verification_passed)),
  PredicateDeclaration(DP(event_matches)),
  PredicateDeclaration(DP(event_occurred)),
  PredicateDeclaration(DP(refresh_scope)),
  PredicateDeclaration(DP(refresh_occurred)),
  EventDeclaration(DE(command)),EventDeclaration(DE(test)),
  EventDeclaration(DE(path_change)),EventDeclaration(DE(network_contact)),
  EventDeclaration(DE(release)),EventDeclaration(DE(dependency_refresh))}
DELTA_PAIR_X={EventScopePairDeclaration(PAIR(refresh))}
DELTA_CONTRACT_SPECS_X={
  TypeDeclaration(T(PathSegment)).admitted_value_domain,
  TypeDeclaration(T(Path)).admitted_value_domain,
  TypeDeclaration(T(PathSet)).admitted_value_domain,
  TypeDeclaration(T(ArtifactRole)).admitted_value_domain,
  TypeDeclaration(T(Format)).admitted_value_domain,
  TypeDeclaration(T(StorageBackend)).admitted_value_domain,
  TypeDeclaration(T(ByteSize)).admitted_value_domain,
  TypeDeclaration(T(ContentIdentity)).admitted_value_domain,
  TypeDeclaration(T(FieldId)).admitted_value_domain,
  TypeDeclaration(T(FieldValue)).admitted_value_domain,
  TypeDeclaration(T(SubjectId)).admitted_value_domain,
  TypeDeclaration(T(BehaviorValue)).admitted_value_domain,
  TypeDeclaration(T(ArtifactBody)).admitted_value_domain,
  TypeDeclaration(T(ArtifactBodyKind)).admitted_value_domain,
  TypeDeclaration(T(ArtifactContent)).admitted_value_domain,
  TypeDeclaration(T(ObservationValue)).admitted_value_domain,
  TypeDeclaration(T(RepositorySnapshot)).admitted_value_domain,
  TypeDeclaration(T(SnapshotIdentity)).admitted_value_domain,
  TypeDeclaration(T(ChangeEntry)).admitted_value_domain,
  TypeDeclaration(T(ChangeSet)).admitted_value_domain,
  TypeDeclaration(T(ArtifactSelector)).admitted_value_domain,
  TypeDeclaration(T(ArtifactProjection)).admitted_value_domain,
  TypeDeclaration(T(Coverage)).admitted_value_domain,
  TypeDeclaration(T(ObservationSpec)).admitted_value_domain,
  TypeDeclaration(T(ObservationResult)).admitted_value_domain,
  TypeDeclaration(T(ObservationRelation)).admitted_value_domain,
  TypeDeclaration(T(VerificationStatus)).admitted_value_domain,
  TypeDeclaration(T(VerificationSpec)).admitted_value_domain,
  TypeDeclaration(T(VerificationRecord)).admitted_value_domain,
  TypeDeclaration(T(ImplementationEvidence)).admitted_value_domain,
  TypeDeclaration(T(CodingEvidencePayload)).admitted_value_domain,
  TypeDeclaration(T(CodingEvidenceEntry)).admitted_value_domain,
  TypeDeclaration(T(AbstractCoverageResult)).admitted_value_domain,
  TypeDeclaration(T(ImplementationCoverageSubject)).admitted_value_domain,
  TypeDeclaration(T(PairTraceDomain)).admitted_value_domain,
  TypeDeclaration(T(PairComparedFields)).admitted_value_domain,
  TypeDeclaration(T(AuthorityClauseTag)).admitted_value_domain,
  TypeDeclaration(T(AuthorityAttestationSubjectIdentity)).admitted_value_domain,
  TypeDeclaration(T(AuthorityAttestationValue)).admitted_value_domain,
  TypeDeclaration(T(ServiceAdmissionSubject)).admitted_value_domain,
  TypeDeclaration(T(EvolutionAdmissionSubject)).admitted_value_domain,
  TypeDeclaration(T(Criterion)).admitted_value_domain,
  TypeDeclaration(T(TaskSpec)).admitted_value_domain,
  TypeDeclaration(T(ChangeKind)).admitted_value_domain,
  TypeDeclaration(T(CommandId)).admitted_value_domain,
  TypeDeclaration(T(ContactClass)).admitted_value_domain,
  TypeDeclaration(T(ReleaseId)).admitted_value_domain,
  TypeDeclaration(T(Purpose)).admitted_value_domain,
  TypeDeclaration(T(EventPattern)).admitted_value_domain,
  TypeDeclaration(T(CommandEventPayload)).admitted_value_domain,
  TypeDeclaration(T(TestEventPayload)).admitted_value_domain,
  TypeDeclaration(T(PathChangeEventPayload)).admitted_value_domain,
  TypeDeclaration(T(NetworkContactEventPayload)).admitted_value_domain,
  TypeDeclaration(T(ReleaseEventPayload)).admitted_value_domain,
  TypeDeclaration(T(DependencyRefreshEventPayload)).admitted_value_domain}
DELTA_X=DELTA_TYPE_X union DELTA_LITERAL_X union DELTA_SYMBOL_X union
  DELTA_PAIR_X union DELTA_CONTRACT_SPECS_X
```

The complete Sigma member sets are literal; `PB_refresh` and `PROFILE_impl`
denote the single field-complete records fixed in §§3.4/4.2, not record
families:

```text
BIND_LITERAL_X={
  SemanticBinding(L(T(TaskSpec),ts_nonempty)),
  SemanticBinding(L(T(TaskSpec),ts_lt_100)),
  SemanticBinding(L(T(TaskSpec),ts_ge_200)),
  SemanticBinding(L(T(ObservationSpec),s_c)),
  SemanticBinding(L(T(RepositorySnapshot),P_c)),
  SemanticBinding(L(T(RepositorySnapshot),F_c)),
  SemanticBinding(L(T(ObservationResult),O_c)),
  SemanticBinding(L(T(ObservationSpec),s_w)),
  SemanticBinding(L(T(TaskSpec),t_w)),SemanticBinding(L(T(TaskSpec),t_t)),
  SemanticBinding(L(T(StorageBackend),LOCAL_STORAGE)),
  SemanticBinding(L(T(StorageBackend),HOSTED_STORAGE)),
  SemanticBinding(L(T(PairTraceDomain),ALL_ADMITTED_TRACES)),
  SemanticBinding(L(T(PairComparedFields),COMPLETE_EVAL_RECORD)),
  SemanticBinding(L(T(AuthorityClauseTag),BOUNDS_CLAUSE)),
  SemanticBinding(L(T(AuthorityClauseTag),CONFLUENCE_OBSERVATION_CLAUSE)),
  SemanticBinding(L(T(AuthorityClauseTag),CONFLUENCE_CHANGE_CLAUSE)),
  SemanticBinding(L(T(AuthorityClauseTag),ADAPTER_PRESERVATION_CLAUSE)),
  SemanticBinding(L(T(AuthorityClauseTag),ADAPTER_ACCEPTANCE_CLAUSE)),
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(b,1))),
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(c,1))),
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(c,2))),
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(w,1))),
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(w,2))),
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(choice,1))),
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(b,1))),
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(c,1))),
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(c,2))),
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(w,1))),
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(w,2))),
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(choice,1))),
  SemanticBinding(L(T(ServiceAdmissionSubject),bounds_subject_b)),
  SemanticBinding(L(T(ServiceAdmissionSubject),confluence_subject_c)),
  SemanticBinding(L(T(ServiceAdmissionSubject),witness_subject_w)),
  SemanticBinding(L(T(ServiceAdmissionSubject),predicate_subject_t)),
  SemanticBinding(L(T(ServiceAdmissionSubject),profile_subject_w)),
  SemanticBinding(L(T(ServiceAdmissionSubject),pair_subject)),
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(b,1))),
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(c,1))),
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(c,2))),
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(w,1))),
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(w,2))),
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(choice,1))),
  SemanticBinding(L(T(EvolutionAdmissionSubject),mr_subject)),
  SemanticBinding(L(T(EvolutionAdmissionSubject),cc_subject)),
  SemanticBinding(L(T(EvolutionAdmissionSubject),x0_subject)),
  SemanticBinding(L(T(EvolutionAdmissionSubject),x1_subject))}
BIND_ORDINARY_X={
  SemanticBinding(DF(snapshot_of)),SemanticBinding(DF(changes_between)),
  SemanticBinding(DF(observe)),SemanticBinding(DP(observations_equal)),
  SemanticBinding(DP(task_accepts)),
  SemanticBinding(DP(dependency_metadata_changed)),
  SemanticBinding(DP(verification_passed)),SemanticBinding(DP(event_matches)),
  SemanticBinding(DP(event_occurred)),SemanticBinding(DP(refresh_scope))}
BIND_X=BIND_LITERAL_X union BIND_ORDINARY_X union {PB_refresh,PROFILE_impl}

MODEL_X={
  MODEL_LITERAL(T(TaskSpec),ts_nonempty),
  MODEL_LITERAL(T(TaskSpec),ts_lt_100),MODEL_LITERAL(T(TaskSpec),ts_ge_200),
  MODEL_LITERAL(T(ObservationSpec),s_c),
  MODEL_LITERAL(T(RepositorySnapshot),P_c),
  MODEL_LITERAL(T(RepositorySnapshot),F_c),
  MODEL_LITERAL(T(ObservationResult),O_c),
  MODEL_LITERAL(T(ObservationSpec),s_w),MODEL_LITERAL(T(TaskSpec),t_w),
  MODEL_LITERAL(T(TaskSpec),t_t),
  MODEL_LITERAL(T(StorageBackend),LOCAL_STORAGE),
  MODEL_LITERAL(T(StorageBackend),HOSTED_STORAGE),
  MODEL_LITERAL(T(PairTraceDomain),ALL_ADMITTED_TRACES),
  MODEL_LITERAL(T(PairComparedFields),COMPLETE_EVAL_RECORD),
  MODEL_LITERAL(T(AuthorityClauseTag),BOUNDS_CLAUSE),
  MODEL_LITERAL(T(AuthorityClauseTag),CONFLUENCE_OBSERVATION_CLAUSE),
  MODEL_LITERAL(T(AuthorityClauseTag),CONFLUENCE_CHANGE_CLAUSE),
  MODEL_LITERAL(T(AuthorityClauseTag),ADAPTER_PRESERVATION_CLAUSE),
  MODEL_LITERAL(T(AuthorityClauseTag),ADAPTER_ACCEPTANCE_CLAUSE),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(b,1)),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(c,1)),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(c,2)),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(w,1)),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(w,2)),
  MODEL_LITERAL(T(AuthorityAttestationSubjectIdentity),
                attestation_subject_identity(choice,1)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(b,1)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(c,1)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(c,2)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(w,1)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(w,2)),
  MODEL_LITERAL(T(AuthorityAttestationValue),ATTEST(choice,1)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),bounds_subject_b),
  MODEL_LITERAL(T(ServiceAdmissionSubject),confluence_subject_c),
  MODEL_LITERAL(T(ServiceAdmissionSubject),witness_subject_w),
  MODEL_LITERAL(T(ServiceAdmissionSubject),predicate_subject_t),
  MODEL_LITERAL(T(ServiceAdmissionSubject),profile_subject_w),
  MODEL_LITERAL(T(ServiceAdmissionSubject),pair_subject),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(b,1)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(c,1)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(c,2)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(w,1)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(w,2)),
  MODEL_LITERAL(T(ServiceAdmissionSubject),authority_subject(choice,1)),
  MODEL_LITERAL(T(EvolutionAdmissionSubject),mr_subject),
  MODEL_LITERAL(T(EvolutionAdmissionSubject),cc_subject),
  MODEL_LITERAL(T(EvolutionAdmissionSubject),x0_subject),
  MODEL_LITERAL(T(EvolutionAdmissionSubject),x1_subject),
  MODEL_snapshot_of,MODEL_changes_between,MODEL_observe,
  MODEL_observations_equal,MODEL_task_accepts,
  MODEL_dependency_metadata_changed,MODEL_verification_passed,
  MODEL_event_matches,MODEL_event_occurred,MODEL_refresh_scope,
  MODEL_refresh_occurred}
SIGMA_CONTRACT_SPECS_X={
  SemanticBinding(L(T(TaskSpec),ts_nonempty)).meaning_contract,
  SemanticBinding(L(T(TaskSpec),ts_lt_100)).meaning_contract,
  SemanticBinding(L(T(TaskSpec),ts_ge_200)).meaning_contract,
  SemanticBinding(L(T(ObservationSpec),s_c)).meaning_contract,
  SemanticBinding(L(T(RepositorySnapshot),P_c)).meaning_contract,
  SemanticBinding(L(T(RepositorySnapshot),F_c)).meaning_contract,
  SemanticBinding(L(T(ObservationResult),O_c)).meaning_contract,
  SemanticBinding(L(T(ObservationSpec),s_w)).meaning_contract,
  SemanticBinding(L(T(TaskSpec),t_w)).meaning_contract,
  SemanticBinding(L(T(TaskSpec),t_t)).meaning_contract,
  SemanticBinding(L(T(StorageBackend),LOCAL_STORAGE)).meaning_contract,
  SemanticBinding(L(T(StorageBackend),HOSTED_STORAGE)).meaning_contract,
  SemanticBinding(L(T(PairTraceDomain),ALL_ADMITTED_TRACES)).meaning_contract,
  SemanticBinding(L(T(PairComparedFields),COMPLETE_EVAL_RECORD)).meaning_contract,
  SemanticBinding(L(T(AuthorityClauseTag),BOUNDS_CLAUSE)).meaning_contract,
  SemanticBinding(L(T(AuthorityClauseTag),
                    CONFLUENCE_OBSERVATION_CLAUSE)).meaning_contract,
  SemanticBinding(L(T(AuthorityClauseTag),
                    CONFLUENCE_CHANGE_CLAUSE)).meaning_contract,
  SemanticBinding(L(T(AuthorityClauseTag),
                    ADAPTER_PRESERVATION_CLAUSE)).meaning_contract,
  SemanticBinding(L(T(AuthorityClauseTag),
                    ADAPTER_ACCEPTANCE_CLAUSE)).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(b,1))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(c,1))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(c,2))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(w,1))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(w,2))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationSubjectIdentity),
                    attestation_subject_identity(choice,1))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(b,1))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(c,1))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(c,2))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(w,1))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(w,2))).meaning_contract,
  SemanticBinding(L(T(AuthorityAttestationValue),ATTEST(choice,1))).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),bounds_subject_b)).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),confluence_subject_c)).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),witness_subject_w)).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),predicate_subject_t)).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),profile_subject_w)).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),pair_subject)).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(b,1))).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(c,1))).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(c,2))).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(w,1))).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(w,2))).meaning_contract,
  SemanticBinding(L(T(ServiceAdmissionSubject),authority_subject(choice,1))).meaning_contract,
  SemanticBinding(L(T(EvolutionAdmissionSubject),mr_subject)).meaning_contract,
  SemanticBinding(L(T(EvolutionAdmissionSubject),cc_subject)).meaning_contract,
  SemanticBinding(L(T(EvolutionAdmissionSubject),x0_subject)).meaning_contract,
  SemanticBinding(L(T(EvolutionAdmissionSubject),x1_subject)).meaning_contract,
  CS(FUNCTION_MEANING,snapshot_of),CS(FUNCTION_MEANING,changes_between),
  CS(FUNCTION_MEANING,observe),
  CS(PREDICATE_MEANING,observations_equal),
  CS(PREDICATE_MEANING,task_accepts),
  CS(PREDICATE_MEANING,dependency_metadata_changed),
  CS(PREDICATE_MEANING,verification_passed),
  CS(PREDICATE_MEANING,event_matches),CS(PREDICATE_MEANING,event_occurred),
  CS(PREDICATE_MEANING,refresh_scope),
  CS(PROFILE_COVERAGE,implementation_evidence),
  CS(EVIDENCE_SCHEMA,none),CS(EVIDENCE_SCHEMA,verification),
  CS(EVIDENCE_SCHEMA,implementation_profile),
  CS(ACCESS_BOUNDARY,literal),CS(ACCESS_BOUNDARY,state_only),
  CS(ACCESS_BOUNDARY,snapshot_pair),CS(ACCESS_BOUNDARY,spec_snapshot),
  CS(ACCESS_BOUNDARY,result_pair),
  CS(ACCESS_BOUNDARY,task_final_evidence),
  CS(ACCESS_BOUNDARY,change_set_only),
  CS(ACCESS_BOUNDARY,verification_snapshot_evidence),
  CS(ACCESS_BOUNDARY,pattern_event),CS(ACCESS_BOUNDARY,pattern_trace),
  CS(ACCESS_BOUNDARY,event_only),
  CS(UNKNOWN_BEHAVIOR,not_applicable),CS(UNKNOWN_BEHAVIOR,never),
  CS(UNKNOWN_BEHAVIOR,evidence_pending),CS(UNKNOWN_BEHAVIOR,task),
  CS(EVALUATION_ERROR_BEHAVIOR,literal),
  CS(EVALUATION_ERROR_BEHAVIOR,term),
  CS(EVALUATION_ERROR_BEHAVIOR,predicate),
  CS(EVALUATION_ERROR_BEHAVIOR,profile),
  CS(REASONING_ERROR_BEHAVIOR,profile),
  T3_A1_MEANING_LIFT(pd,sb),T3_A1_EVIDENCE_LIFT(pd,sb),
  T3_A1_ACCESS_LIFT(pd,sb),T3_A1_UNKNOWN_LIFT(pd,sb),
  T3_A1_ERROR_LIFT(pd,sb)}
SIGMA_X=BIND_X union MODEL_X union SIGMA_CONTRACT_SPECS_X
```

Every member of `DELTA_CONTRACT_SPECS_X` and
`SIGMA_CONTRACT_SPECS_X` is the complete field value projected from the named
record or the complete catalog record of §4.1; no member is its
`ContractSpecKey`.  The sets are literal and finite, so a missing
`CONTRACT_SPEC` row below deletes an actual universe record.

Every service set and identity is enumerated, never selected by a family:

```text
SERVICE_SPECS_X={
  FSOUND,QSOUND,PROFSOUND,BSOUND,BCOMPLETE,WSOUND,CSOUND,
  FREQ,QREQ,PROFREQ,BREQ,CREQ,WREQ,
  FFAIL,QFAIL,PROFFAIL,BFAIL,CFAIL,WFAIL,
  ASOUND,ACOMPLETE,AREQUIRED,AFAILURE,
  PSOUND,PCOMPLETE,PEVIDENCE,PFAILURE,
  LEX_SOUND,LEX_REQ,LEX_FAIL,
  ES_m,ECOMP_m,EE_m,EF_m,ES_c,ECOMP_c,EE_c,EF_c,
  ES_x0,ECOMP_x0,EE_x0,EF_x0,ES_x1,ECOMP_x1,EE_x1,EF_x1}
SERVICE_DESCRIPTORS_X={
  CapabilityDescriptor(CAP(functions)),
  CapabilityDescriptor(CAP(predicates)),CapabilityDescriptor(CAP(profile)),
  CapabilityDescriptor(CAP(bounds)),CapabilityDescriptor(CAP(confluence)),
  CapabilityDescriptor(CAP(witness)),
  CapabilityDescriptor(CAP(validate_bounds)),
  CapabilityDescriptor(CAP(validate_witness)),
  CapabilityDescriptor(CAP(authority)),CapabilityDescriptor(PVC),
  LEX_CAP,
  EVCAP_m,EVCAP_c,EVCAP_x0,EVCAP_x1}
SERVICE_IDENTITIES_X={
  ServiceIdentityRecord(SK(functions)),ServiceIdentityRecord(SK(predicates)),
  ServiceIdentityRecord(SK(profile)),ServiceIdentityRecord(SK(bounds)),
  ServiceIdentityRecord(SK(confluence)),ServiceIdentityRecord(AWSK),
  ServiceIdentityRecord(RVSK(bounds)),ServiceIdentityRecord(RVSK(witness)),
  ServiceIdentityRecord(AVSK),ServiceIdentityRecord(PVSK),
  ServiceIdentityRecord(LEXSK),
  ServiceIdentityRecord(EVSK_m),ServiceIdentityRecord(EVSK_c),
  ServiceIdentityRecord(EVSK_x0),ServiceIdentityRecord(EVSK_x1)}
SERVICE_X=SERVICE_SPECS_X union SERVICE_DESCRIPTORS_X union SERVICE_IDENTITIES_X
```

The owner packages have literal member sets.  A field not shown with a member
is the displayed literal empty set; no package family or wildcard exists:

```text
PKG_CK=PluginPackage(
  ABI0,CK,
  declarations=DELTA_TYPE_X union DELTA_LITERAL_X union DELTA_SYMBOL_X,
  pair_declarations=DELTA_PAIR_X,
  bindings=BIND_LITERAL_X union BIND_ORDINARY_X,pair_bindings={PB_refresh},
  profile_bindings={PROFILE_impl},model_contracts=MODEL_X,aliases={},
  services={CapabilityDescriptor(CAP(functions)),
    CapabilityDescriptor(CAP(predicates)),CapabilityDescriptor(CAP(profile)),
    CapabilityDescriptor(CAP(bounds)),CapabilityDescriptor(CAP(confluence)),
    LEX_CAP},
  certificates={BENV},authority_facts={},compatibility_claims={},migrations={},
  semantic_extensions={},diagnostics=NONE)
PKG_AWK=PluginPackage(
  ABI0,AWK,declarations={},pair_declarations={},bindings={},pair_bindings={},
  profile_bindings={},model_contracts={},aliases={},
  services={CapabilityDescriptor(CAP(witness))},certificates={WENV},
  authority_facts={},compatibility_claims={},migrations={},
  semantic_extensions={},diagnostics=NONE)
PKG_RVK=PluginPackage(
  ABI0,RVK,declarations={},pair_declarations={},bindings={},pair_bindings={},
  profile_bindings={},model_contracts={},aliases={},
  services={CapabilityDescriptor(CAP(validate_bounds)),
            CapabilityDescriptor(CAP(validate_witness))},certificates={},
  authority_facts={},compatibility_claims={},migrations={},
  semantic_extensions={},diagnostics=NONE)
PKG_APK=PluginPackage(
  ABI0,APK,declarations={},pair_declarations={},bindings={},pair_bindings={},
  profile_bindings={},model_contracts={},aliases={},services={},certificates={},
  authority_facts={AFB(b,1),AFB(c,1),AFB(c,2),AFB(w,1),AFB(w,2),
                   AFB(choice,1)},compatibility_claims={},migrations={},
  semantic_extensions={},diagnostics=NONE)
PKG_ATK=PluginPackage(
  ABI0,ATK,declarations={},pair_declarations={},bindings={},pair_bindings={},
  profile_bindings={},model_contracts={},aliases={},services={},
  certificates={AENV(b,1),AENV(c,1),AENV(c,2),AENV(w,1),AENV(w,2),
                AENV(choice,1)},authority_facts={},compatibility_claims={},
  migrations={},semantic_extensions={},diagnostics=NONE)
PKG_AVK=PluginPackage(
  ABI0,AVK,declarations={},pair_declarations={},bindings={},pair_bindings={},
  profile_bindings={},model_contracts={},aliases={},
  services={CapabilityDescriptor(CAP(authority))},certificates={},
  authority_facts={},compatibility_claims={},migrations={},
  semantic_extensions={},diagnostics=NONE)
PKG_PPK=PluginPackage(
  ABI0,PPK,declarations={},pair_declarations={},bindings={},pair_bindings={},
  profile_bindings={},model_contracts={},aliases={},services={},
  certificates={PENV},authority_facts={},compatibility_claims={},migrations={},
  semantic_extensions={},diagnostics=NONE)
PKG_PVK=PluginPackage(
  ABI0,PVK,declarations={},pair_declarations={},bindings={},pair_bindings={},
  profile_bindings={},model_contracts={},aliases={},services={PVC},
  certificates={},authority_facts={},compatibility_claims={},migrations={},
  semantic_extensions={},diagnostics=NONE)
PACKAGE_CATALOG_X={PKG_CK,PKG_AWK,PKG_RVK,PKG_APK,PKG_ATK,PKG_AVK,
  PKG_CK_no_task_model,PKG_APK_no_choice_fact,PKG_PPK,PKG_PVK,PKG_pair_CK,
  PKG_evo_EOK,PKG_evo_EOK_no_m,PKG_evo_EOK_no_c,
  PKG_evo_EOK_no_x0,PKG_evo_EOK_no_x1,
  PKG_evo_EOK_alias_optional,PKG_evo_EOK_alias_optional_no_a0,
  PKG_evo_EOK_no_a1,PKG_evo_EPK,PKG_evo_EVK,
  PKG_pi1,PKG_pi2}
```

The corresponding exact package/record sequences are literal:

```text
SEQ_CK=[ABI0,PKG_CK,PB_refresh,PROFILE_impl,
  CapabilityDescriptor(CAP(functions)),
  CapabilityDescriptor(CAP(predicates)),CapabilityDescriptor(CAP(profile)),
  CapabilityDescriptor(CAP(bounds)),CapabilityDescriptor(CAP(confluence)),
  LEX_CAP,BENV]
SEQ_AWK=[ABI0,PKG_AWK,CapabilityDescriptor(CAP(witness)),WENV]
SEQ_RVK=[ABI0,PKG_RVK,CapabilityDescriptor(CAP(validate_bounds)),
  CapabilityDescriptor(CAP(validate_witness))]
SEQ_APK=[ABI0,PKG_APK,AFB(b,1),AFB(c,1),AFB(c,2),AFB(w,1),AFB(w,2),
  AFB(choice,1)]
SEQ_ATK=[ABI0,PKG_ATK,AENV(b,1),AENV(c,1),AENV(c,2),AENV(w,1),AENV(w,2),
  AENV(choice,1)]
SEQ_AVK=[ABI0,PKG_AVK,CapabilityDescriptor(CAP(authority))]
SEQ_PPK=[ABI0,PKG_PPK,PENV]
SEQ_PVK=[ABI0,PKG_PVK,PVC]
SEQ_PAIR_CK=[ABI0,PKG_pair_CK,PB_alt,B_alt,E_p,D_p]
SEQ_EOK=[ABI0,PKG_evo_EOK,a0,a1,c0,m0,x0,x1]
SEQ_EPK=[ABI0,PKG_evo_EPK,EENV_m,EENV_c,EENV_x0,EENV_x1]
SEQ_EVK=[ABI0,PKG_evo_EVK,EVCAP_m,EVCAP_c,EVCAP_x0,EVCAP_x1]
SEQ_CK_NO_MODEL=[ABI0,PKG_CK_no_task_model]
SEQ_APK_NO_CHOICE_FACT=[ABI0,PKG_APK_no_choice_fact]
SEQ_EOK_NO_M=[ABI0,PKG_evo_EOK_no_m]
SEQ_EOK_NO_C=[ABI0,PKG_evo_EOK_no_c]
SEQ_EOK_NO_X0=[ABI0,PKG_evo_EOK_no_x0]
SEQ_EOK_NO_X1=[ABI0,PKG_evo_EOK_no_x1]
SEQ_EOK_ALIAS_OPTIONAL=[ABI0,PKG_evo_EOK_alias_optional]
SEQ_EOK_ALIAS_OPTIONAL_NO_A0=[ABI0,PKG_evo_EOK_alias_optional_no_a0]
SEQ_EOK_NO_A1=[ABI0,PKG_evo_EOK_no_a1]
PACKAGE_RECORD_PRESENTATION_CATALOG_X={SEQ_CK,SEQ_AWK,SEQ_RVK,SEQ_APK,SEQ_ATK,
  SEQ_AVK,SEQ_PPK,SEQ_PVK,SEQ_PAIR_CK,SEQ_EOK,SEQ_EPK,SEQ_EVK,
  SEQ_CK_NO_MODEL,SEQ_APK_NO_CHOICE_FACT,
  SEQ_EOK_NO_M,SEQ_EOK_NO_C,SEQ_EOK_NO_X0,SEQ_EOK_NO_X1,
  SEQ_EOK_ALIAS_OPTIONAL,SEQ_EOK_ALIAS_OPTIONAL_NO_A0,SEQ_EOK_NO_A1,
  Pi_pkg_1,Pi_pkg_2,Pi_rec_1(PKG_pi1),Pi_rec_2(PKG_pi1),
  Pi_rec_1(PKG_pi2),Pi_rec_2(PKG_pi2)}
```

The supplied fixture records are also a literal set.  The six authority rows
and four evolution rows are expanded so no family comprehension remains:

```text
AUTHORITY_FIXTURE_X={
  SRC(b,1),AUTH(b,1),AF(b,1),AC(b,1),ATTEST(b,1),authority_subject(b,1),
  AE_REF(b,1),DA(b,1),JA(b,1),UA(b,1),AA(b,1),RA(b,1),AENV(b,1),
  AADMIT(b,1),ARES(b,1),AFB(b,1),
  SRC(c,1),AUTH(c,1),AF(c,1),AC(c,1),ATTEST(c,1),authority_subject(c,1),
  AE_REF(c,1),DA(c,1),JA(c,1),UA(c,1),AA(c,1),RA(c,1),AENV(c,1),
  AADMIT(c,1),ARES(c,1),AFB(c,1),
  SRC(c,2),AUTH(c,2),AF(c,2),AC(c,2),ATTEST(c,2),authority_subject(c,2),
  AE_REF(c,2),DA(c,2),JA(c,2),UA(c,2),AA(c,2),RA(c,2),AENV(c,2),
  AADMIT(c,2),ARES(c,2),AFB(c,2),
  SRC(w,1),AUTH(w,1),AF(w,1),AC(w,1),ATTEST(w,1),authority_subject(w,1),
  AE_REF(w,1),DA(w,1),JA(w,1),UA(w,1),AA(w,1),RA(w,1),AENV(w,1),
  AADMIT(w,1),ARES(w,1),AFB(w,1),
  SRC(w,2),AUTH(w,2),AF(w,2),AC(w,2),ATTEST(w,2),authority_subject(w,2),
  AE_REF(w,2),DA(w,2),JA(w,2),UA(w,2),AA(w,2),RA(w,2),AENV(w,2),
  AADMIT(w,2),ARES(w,2),AFB(w,2),
  SRC(choice,1),AUTH(choice,1),AF(choice,1),AC(choice,1),ATTEST(choice,1),
  authority_subject(choice,1),AE_REF(choice,1),DA(choice,1),JA(choice,1),
  UA(choice,1),AA(choice,1),RA(choice,1),AENV(choice,1),AADMIT(choice,1),
  ARES(choice,1),AFB(choice,1)}
EVOLUTION_FIXTURE_X={
  ES_m,ECOMP_m,EE_m,EF_m,EVCAP_m,ServiceIdentityRecord(EVSK_m),
  D_ev_m,ER_m,EADMIT_m,MIGRATION_RELATION_ADMITTED(MK0,EC_m),
  ES_c,ECOMP_c,EE_c,EF_c,EVCAP_c,ServiceIdentityRecord(EVSK_c),
  D_ev_c,ER_c,EADMIT_c,COMPATIBILITY_CLAIM_ADMITTED(CCK0,EC_c),
  ES_x0,ECOMP_x0,EE_x0,EF_x0,EVCAP_x0,ServiceIdentityRecord(EVSK_x0),
  D_ev_x0,ER_x0,EADMIT_x0,SEMANTIC_EXTENSION_ADMITTED(XK0,EC_x0),
  ES_x1,ECOMP_x1,EE_x1,EF_x1,EVCAP_x1,ServiceIdentityRecord(EVSK_x1),
  D_ev_x1,ER_x1,EADMIT_x1,SEMANTIC_EXTENSION_ADMITTED(XK1,EC_x1)}
TRUST_REQUEST_FIXTURE_X={Q_t[T_admitted],Q_t[T_absent],Q_t[T_undecided],
  Q_t[T_incompatible],Q_t[T_failed]}
FIXTURE_X={
  C_b,C_c,C_w,C_choice,cb0,cbe0,E_choice^0,E_choice,
  E_choice_missing,
  E_b,E_c,E_w,D_b,D_c,D_w,J_b,J_c,J_w,
  R_b,R_c,R_w,BENV,WENV,O_w,BundleBoundsProof,AdapterWitness,
  BPROOF_REF,WPROOF_REF,ROOT_B,ROOT_W,T_b,T_w,
  CertificateAdmission.ADMITTED(BCERT,CONSISTENCY_UNSAT),
  ReasoningResult.ADMITTED_JUDGMENT(CONSISTENCY_UNSAT,BCERT),
  CertificateAdmission.ADMITTED(WCERT,CONSISTENCY_SAT),
  ReasoningResult.ADMITTED_JUDGMENT(CONSISTENCY_SAT,WCERT),
  pd,sb,od,B_alt,PB_alt,E_p,D_p,U_p,A_p,
  R_p,PENV,PairFullEvalProof,PAIR_PROOF_REF,ROOT_p,T_p,
  t_t,F_t,EVIDENCE_t,S_t,E_t,D_t,r_t,RES_t,R_lex,E_lex,D_lex,
  LEX_SOUND,LEX_REQ,LEX_FAIL,LEXSK,CAP_lex,TARGET_lex,LEX_CAP,
  ServiceIdentityRecord(LEXSK),
  x_task,f_lex,g_lex,scope_lex,S_lex,lk0,lb0,
  scope_extra,E_t_extra,D_t_extra,Q_t_extra,lk_extra,lb_extra,
  e0,v0,vr0,i0,H0,ev0,te0,src0,auth0,u0,F_noresult,
  ROOT_TR_t,T_admitted,T_absent,T_undecided,T_incompatible,T_failed,
  e_abs_w,i_abs_w,u_pending_abs_w,i_pending_abs_w,H_w,r_task_w,r_abs_w,
  s_profile_w,U_profile_w,Q_profile_w,ROOT_PROFILE_W,T_profile_w,P_w_result,
  m0,c0,x0,x1,a0,a1,MR0,CC0,XE0,XP0,ROOT_E,T_evo,
  mr_subject,cc_subject,x0_subject,x1_subject,
  D_ev_m,D_ev_c,D_ev_x0,D_ev_x1,
  R_m,R_c0,R_x0,R_x1,EENV_m,EENV_c,EENV_x0,EENV_x1,
  N_o,N_d,V_o,V_d,M_c,O_1,O_2,U_c,ROOT_TR_c,T_c,u_c,Y_c,
  L_c_ready,L_c_final,K_c,
  RESULT_RECORD(result_identity=(IDENTITY_OF(R_c),ReasoningResult,
                IDENTITY_OF(Y_c)),result_value=Y_c),
  ROOT_TR_c_alt,T_c_alt,R_c_alt,L_life_after,K_life_after,
  d,d_bad,d_bad_signature,conflict0,conflict1,
  EENV_m_bad_root,
  CertificateAdmission.ADMITTED(
    PCERT,PAIR_COHERENCE_ADMITTED(PAIR(refresh),PCERT)),
  PAIR_COHERENCE_ADMITTED(PAIR(refresh),PCERT),
  D_pi11,D_pi12,D_pi21,D_pi22,A_pi11,A_pi12,A_pi21,A_pi22,
  ROOT_A,T_A} union AUTHORITY_FIXTURE_X union EVOLUTION_FIXTURE_X union
  TRUST_REQUEST_FIXTURE_X
```

`PACKAGE_CATALOG_X`, `PACKAGE_RECORD_PRESENTATION_CATALOG_X`, and `FIXTURE_X`
are finite catalogs of literal constructors, not universes and not operands of
composition.  In particular, catalog membership never co-installs `PKG_CK`
with `PKG_pair_CK`, never co-installs an evolution package with one of its
same-key omission variants, and never combines the two pair bindings or the
two conflict presentations.

The packet itself is a tagged finite map.  Its key sort is the following
closed algebra (all parameter sorts shown here are the finite enumerations
defined in §§9.3--9.5):

```text
TrustFixtureTag = ADMITTED | ABSENT | UNDECIDED | INCOMPATIBLE | FAILED
OrderTag = FORWARD | REVERSE
PackageOrderTag = PI1_PI2 | PI2_PI1
RecordOrderTag = DECLARATION_THEN_SPEC | SPEC_THEN_DECLARATION
FixtureId =
    CORE_DEFINITIONAL
  | PAIR_INDEPENDENT
  | TRUST_BRANCH(TrustFixtureTag)
  | MISSING_BASE(MissingRowId)
  | MISSING_VARIANT(MissingRowId)
  | CONFLUENCE_ORDER(OrderTag)
  | PERMUTATION(PackageOrderTag,RecordOrderTag)
  | DUPLICATE_EQUAL(OrderTag)
  | DUPLICATE_CONFLICT(OrderTag)

FixtureUniverse = exact finite K2 logical record universe
FixturePacket = finite map(FixtureId -> FixtureUniverse)

FIXTURE_PACKET_X={
  CORE_DEFINITIONAL -> U_CORE_DEFINITIONAL,
  PAIR_INDEPENDENT -> U_PAIR_INDEPENDENT,
  TRUST_BRANCH(x) -> U_TRUST_x for each displayed TrustFixtureTag x,
  MISSING_BASE(k) -> B_k for each of the 42 displayed MissingRowId values k,
  MISSING_VARIANT(k) -> V_k for each such k,
  CONFLUENCE_ORDER(o) -> U_CONFLUENCE_o for each displayed OrderTag o,
  PERMUTATION(p,r) -> U_PI_p_r for each of the four displayed `(p,r)` pairs,
  DUPLICATE_EQUAL(o) -> U_DUPLICATE_EQUAL_o for each displayed OrderTag o,
  DUPLICATE_CONFLICT(o) -> U_DUPLICATE_CONFLICT_o for each displayed OrderTag o}
```

Each right-hand side is one self-contained universe, not a union of packet
entries.  The notation above expands to a finite literal map because every
parameter sort is displayed and finite.  Every map value conforms to the K2
universe input algebra; `WELL_FORMED`, `MALFORMED`, open, and missing are its
derived judgments and do not make the input an untyped packet value.
`U_CORE_DEFINITIONAL` contains only
`PKG_CK/PB_refresh`; `U_PAIR_INDEPENDENT` contains only
`PKG_pair_CK/PB_alt`; every omission baseline/variant owns its own exact
package and referring carriers; and each permutation or duplicate/conflict
presentation has its own entry.  No hidden global universe exists.

Every package, complete model record, service descriptor/specification,
certificate, authority fact, evolution record, choice record, carrier,
request, and result referenced by a packet entry is its complete record; no
package or model key stands in for a record and no implicit package-member
closure is used.

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
PSOUND=SERVICE_SPEC(
  (PVK,coding.validation.contract,refresh_sound,(1),SOUND_FRAGMENT),
  SOUND_FRAGMENT,T(ServiceAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  pair_subject->IN_FRAGMENT;
  every unequal admitted subject->OUTSIDE_FRAGMENT)
PCOMPLETE=SERVICE_SPEC(
  (PVK,coding.validation.contract,refresh_complete,(1),COMPLETE_FRAGMENT),
  COMPLETE_FRAGMENT,T(ServiceAdmissionSubject),
  {IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  pair_subject->IN_FRAGMENT;
  every unequal admitted subject->OUTSIDE_FRAGMENT)
PEVIDENCE=SERVICE_SPEC(
  (PVK,coding.validation.contract,refresh_evidence,(1),REQUIRED_EVIDENCE),
  REQUIRED_EVIDENCE,
  (T(ServiceAdmissionSubject),PairFullEvalProof,finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (pair_subject,PairFullEvalProof,{PAIR_PROOF_REF})->ADMISSIBLE;
  every other admitted tuple->INADMISSIBLE)
PFAILURE=SERVICE_SPEC(
  (PVK,coding.validation.contract,refresh_failure,(1),
   SERVICE_FAILURE_BEHAVIOR),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,
  PairValidationResult.REASONING_ERROR,{},
  F->the exact K2 PAIR_VALIDATION failure projection of F)
```

Each has owner `PVK`, owner layer `Service`, and role equal to its key's final
field.  Freeze the exact finite typed primary value

```text
pair_subject=PAIR_COHERENCE_SUBJECT(
  PAIR(refresh),DP(refresh_scope),DP(refresh_occurred),
  ALL_ADMITTED_TRACES,COMPLETE_EVAL_RECORD)
```

`PSOUND` and `PCOMPLETE` have primary input domain
`T(ServiceAdmissionSubject)`, codomain `{IN_FRAGMENT,OUTSIDE_FRAGMENT}`, and
literal observation-query map `{}`.  Their total relation returns
`IN_FRAGMENT` exactly on `pair_subject` and `OUTSIDE_FRAGMENT` on every other
admitted `ServiceAdmissionSubject`.  The finite subject value fixes the pair,
both binding keys, trace domain, and every complete `Eval` field compared by
the certificate payload; it contains no `OccurrenceSemanticContractBundle`,
`ContractSpec`, semantic environment, binding record, or relation value.
`PEVIDENCE` has primary input domain
`(T(ServiceAdmissionSubject),PairFullEvalProof,finset(EvidenceRef))`, codomain
`{ADMISSIBLE,INADMISSIBLE}`, literal query map `{}`, and returns `ADMISSIBLE`
exactly for `(pair_subject,PairFullEvalProof,{PAIR_PROOF_REF})`.
`PFAILURE` has primary input domain `InterfaceFailure`, exact codomain
`PairValidationResult.REASONING_ERROR`, literal query map `{}`, and the total
K2 `PAIR_VALIDATION` failure projection.  Every other admitted input follows
the displayed negative branch of its relation.  All four supports are `{}`.

The complete `CapabilityDescriptor(PVC)` has ABI `ABI0`, plugin `PVK`, service
role `PAIR_VALIDATION`, class `COMPLETE_FOR_DECLARED_FRAGMENT`, judgments
`{EVENT_PAIR_COHERENCE_ADMISSION}`, targets `{PAIR_TARGET(PAIR(refresh))}`,
sound/complete fragments `PSOUND/PCOMPLETE`, dependency scope exactly the
transitive proper closure of the pair subject, required evidence `PEVIDENCE`,
required roots `{TRP}`, and failure contract `PFAILURE`; its proper
dependencies and closure are exactly the K2 derivation from those fields.

The pair environment and its finite record domain are literally

```text
types_p=the least §3.2 nested-type closure of
  {T(DependencyRefreshEventPayload),T(ServiceAdmissionSubject)}
Delta_p={TypeDeclaration(k)|k in types_p} union
  {LiteralDeclaration(T(PairTraceDomain),ALL_ADMITTED_TRACES),
   LiteralDeclaration(T(PairComparedFields),COMPLETE_EVAL_RECORD),
   LiteralDeclaration(T(ServiceAdmissionSubject),pair_subject),
   the exact PredicateDeclaration(DP(refresh_scope)),
   the exact PredicateDeclaration(DP(refresh_occurred)),
   the exact EventDeclaration(DE(dependency_refresh))}
Sigma_p={sb,
  the exact literal SemanticBinding(T(PairTraceDomain),ALL_ADMITTED_TRACES),
  the exact literal SemanticBinding(T(PairComparedFields),COMPLETE_EVAL_RECORD),
  the exact literal SemanticBinding(T(ServiceAdmissionSubject),pair_subject),
  MODEL_LITERAL(T(PairTraceDomain),ALL_ADMITTED_TRACES),
  MODEL_LITERAL(T(PairComparedFields),COMPLETE_EVAL_RECORD),
  MODEL_LITERAL(T(ServiceAdmissionSubject),pair_subject),
  MODEL_refresh_scope,
  MODEL_refresh_occurred} union
  contractFields(sb) union contractFields(B_alt) union contractFields(PB_alt)
E_p=SemanticEnvironment(
  abi_version=ABI0,declarations=Delta_p,pair_declarations={pd},
  bindings={sb},pair_bindings={PB_alt},profile_bindings={},
  authority_facts={},semantic_extensions={},lexical_bindings={},
  choice_bindings={},mechanically_extracted_dependencies=
    required(PAIR_ADMISSION_SUBJECT(PAIR(refresh))),chi_C={})
Omega_p={ABI0,E_p,pd,PB_alt,B_alt} union Delta_p union Sigma_p
D_p=DependencyEnvironment(PAIR_ADMISSION_SUBJECT(PAIR(refresh)),Omega_p)
```

There is no ordinary `SemanticBinding(DP(refresh_occurred))`.  `D_p`'s
validation-reference set is exactly
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
  trace_domain=ALL_ADMITTED_TRACES,
  compared_fields=COMPLETE_EVAL_RECORD)
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

Fix the following literal values and records:

```text
t_t=TASK({OBSERVATION_EQUALS(s_c,O_c)},{})
F_t=F_c
coding_entries(EVIDENCE_t)={}
r_t=VALUE(TRUE,{}, {})
S_t=PREDICATE_SUBJECT(
  SP(task_accepts),DP(task_accepts),(t_t,F_t,EVIDENCE_t))
types_t=the least exact §3.2 nested-type closure of
  {T(TaskSpec),T(RepositorySnapshot)} and the admitted values t_t,F_t
Delta_t={TypeDeclaration(k)|k in types_t} union
        {the exact PredicateDeclaration(DP(task_accepts))}
Sigma_t={the exact §4.2 SemanticBinding(DP(task_accepts)),
         MODEL_task_accepts,
         CS(PREDICATE_MEANING,task_accepts),
         CS(EVIDENCE_SCHEMA,verification),
         CS(ACCESS_BOUNDARY,task_final_evidence),
         CS(UNKNOWN_BEHAVIOR,task),
         CS(EVALUATION_ERROR_BEHAVIOR,predicate)}
E_t=SemanticEnvironment(
  abi_version=ABI0,
  declarations=Delta_t,
  pair_declarations={},
  bindings={the exact §4.2 SemanticBinding(DP(task_accepts))},
  pair_bindings={},profile_bindings={},authority_facts={},
  semantic_extensions={},lexical_bindings={},choice_bindings={},
  mechanically_extracted_dependencies=required(S_t),chi_C={})
Omega_t={ABI0,E_t} union Delta_t union Sigma_t
D_t=DependencyEnvironment(S_t,Omega_t)
```

`Omega_t` has exactly `2+|Delta_t|+7` records; no capability, trust, request,
result, lifecycle, or carrier projection is a semantic dependency record for
`S_t`.  Those independently required request fields are supplied below.  The
`D_t` equation fixes all seven displayed K2 fields: syntax roots
`required(S_t)`, subject root `BINDING(DP(task_accepts))`, its derived
association edges, expanded roots, proper dependencies, least transitive
closure, and empty validation-reference set.  Direct task evaluation on the
single observation-equality criterion is exactly `r_t`; no evidence entry or
ambient value is consulted.  For a supplied trust environment `T`, define the
otherwise identical request

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

Each row below names its own complete finite baseline and one exact
target-removing reconstruction.  Every containing package, environment,
request, result, and derived carrier is rebuilt explicitly; no referencing
field is silently removed.  Where K2's total function is context-sensitive,
the contexts are separate named baselines and variants.

The otherwise auxiliary keys/values used only to exercise the total missing
function are fixed as follows:

```text
EOK=((capknow.fixture,evolution-owner),(1))
MK0 = (EOK,coding.migration,missing_fixture,(1))
CCK0 = (EOK,coding.compatibility,missing_fixture,(1))
XK0 = (EOK,coding.extension,optional_missing_fixture,(1))
XK1 = (EOK,coding.extension,required_missing_fixture,(1))
AK0 = (EOK,coding.alias,optional_missing_fixture)
AK1 = (EOK,coding.alias,required_missing_fixture)
MR0 = ContractSpec(
  contract_key=(EOK,coding.migration.relation,missing_fixture,(1),
                MIGRATION_RELATION),owner_layer=Sigma,
  contract_role=MIGRATION_RELATION,
  primary_input_domain=T(EvolutionAdmissionSubject),
  codomain={FULL_CONTRACT_EQUIVALENCE},observation_queries={},
  logical_relation={mr_subject->FULL_CONTRACT_EQUIVALENCE;
                    every unequal admitted subject->FULL_CONTRACT_EQUIVALENCE})
CC0 = ContractSpec(
  contract_key=(EOK,coding.compatibility.validation,missing_fixture,(1),
                COMPATIBILITY_VALIDATION),owner_layer=Service,
  contract_role=COMPATIBILITY_VALIDATION,
  primary_input_domain=T(EvolutionAdmissionSubject),
  codomain={COMPATIBLE,INCOMPATIBLE},observation_queries={},
  logical_relation={cc_subject->COMPATIBLE;
                    every unequal admitted subject->INCOMPATIBLE})
XE0 = ContractSpec(
  contract_key=(EOK,coding.extension.effect,missing_fixture,(1),
                SEMANTIC_EXTENSION_EFFECT),owner_layer=Sigma,
  contract_role=SEMANTIC_EXTENSION_EFFECT,
  primary_input_domain=T(EvolutionAdmissionSubject),
  codomain={PRESERVE_EXACT_TARGET},observation_queries={},
  logical_relation={x0_subject->PRESERVE_EXACT_TARGET,
                    x1_subject->PRESERVE_EXACT_TARGET;
                    every other admitted subject->PRESERVE_EXACT_TARGET})
XP0 = ContractSpec(
  contract_key=(EOK,coding.extension.payload,missing_fixture,(1),
                SEMANTIC_EXTENSION_PAYLOAD),owner_layer=Sigma,
  contract_role=SEMANTIC_EXTENSION_PAYLOAD,
  primary_input_domain=T(EvolutionAdmissionSubject),
  codomain={NO_ADDITIONAL_MEANING},observation_queries={},
  logical_relation={x0_subject->NO_ADDITIONAL_MEANING,
                    x1_subject->NO_ADDITIONAL_MEANING;
                    every other admitted subject->NO_ADDITIONAL_MEANING})

a0 = AliasBinding(
  alias_key=AK0,exact_target_key=DP(task_accepts),
  target_kind=PREDICATE,target_exact_version=(1))
a1 = AliasBinding(
  alias_key=AK1,exact_target_key=DP(task_accepts),
  target_kind=PREDICATE,target_exact_version=(1))
m0 = MigrationDeclaration(
  migration_key=MK0,source_environment=E_t,target_environment=E_t,
  semantic_relation=FULL_CONTRACT_EQUIVALENCE,relation_contract=MR0,
  certificate_key=EC_m,validator_key=EVC_m,trust_root_key=TRE)
c0 = CompatibilityClaim(
  claim_key=CCK0,source_abi=ABI0,target_abi=ABI0,
  source_keys={MIGRATION(MK0)},target_keys={BINDING(DP(task_accepts))},
  compatibility_contract=CC0,certificate_key=EC_c,
  validator_key=EVC_c,trust_root_key=TRE)
x0 = SemanticExtension(
  extension_key=XK0,target_record_identity=ALIAS_RECORD(AK0),
  owner_layer=Sigma,semantic_effect=XE0,payload=XP0,
  certificate_key=EC_x0,validator_key=EVC_x0,trust_root_key=TRE)
x1 = SemanticExtension(
  extension_key=XK1,target_record_identity=ALIAS_RECORD(AK1),
  owner_layer=Sigma,semantic_effect=XE0,payload=XP0,
  certificate_key=EC_x1,validator_key=EVC_x1,trust_root_key=TRE)
mr_subject=MIGRATION_RELATION_SUBJECT(
  MK0,semanticIdentity(E_t),semanticIdentity(E_t),
  FULL_CONTRACT_EQUIVALENCE)
cc_subject=COMPATIBILITY_CLAIM_SUBJECT(
  CCK0,ABI0,ABI0,{MIGRATION(MK0)},{BINDING(DP(task_accepts))})
x0_subject=SEMANTIC_EXTENSION_SUBJECT_VALUE(
  XK0,ALIAS_RECORD(AK0),Sigma)
x1_subject=SEMANTIC_EXTENSION_SUBJECT_VALUE(
  XK1,ALIAS_RECORD(AK1),Sigma)
L_ev={mr_subject:T(EvolutionAdmissionSubject),
      cc_subject:T(EvolutionAdmissionSubject),
      x0_subject:T(EvolutionAdmissionSubject),
      x1_subject:T(EvolutionAdmissionSubject)}
Delta_ev={the exact TypeDeclaration(T(EvolutionAdmissionSubject)),
  LiteralDeclaration(T(EvolutionAdmissionSubject),mr_subject),
  LiteralDeclaration(T(EvolutionAdmissionSubject),cc_subject),
  LiteralDeclaration(T(EvolutionAdmissionSubject),x0_subject),
  LiteralDeclaration(T(EvolutionAdmissionSubject),x1_subject)}
BIND_ev={
  the exact literal SemanticBinding(T(EvolutionAdmissionSubject),mr_subject),
  the exact literal SemanticBinding(T(EvolutionAdmissionSubject),cc_subject),
  the exact literal SemanticBinding(T(EvolutionAdmissionSubject),x0_subject),
  the exact literal SemanticBinding(T(EvolutionAdmissionSubject),x1_subject),
  MODEL_LITERAL(T(EvolutionAdmissionSubject),mr_subject),
  MODEL_LITERAL(T(EvolutionAdmissionSubject),cc_subject),
  MODEL_LITERAL(T(EvolutionAdmissionSubject),x0_subject),
  MODEL_LITERAL(T(EvolutionAdmissionSubject),x1_subject)}
Sigma_ev=BIND_ev union
  UNION(contractFields(r) | r in Delta_ev union BIND_ev)
src0=SRC(choice,1)
auth0=AUTH(choice,1)
x_task = Variable(task_argument,T(TaskSpec))
f_lex = Atom(
  SP(task_accepts),Var(x_task),
  Apply(SF(snapshot_of),Anchor(final)),Anchor(evidence))
g_lex = All({})
scope_lex = LexicalScopeIdentity(FORMULA_ENTAILMENT,(f_lex,g_lex))
S_lex = FORMULA_SUBJECT({f_lex,g_lex},scope_lex)
lk0 = LexicalBindingKey(scope_lex,x_task,T(TaskSpec))
lb0 = LexicalBinding(lexical_binding_key=lk0,admitted_value=t_t)
Delta_lex=Delta_t union {the exact FunctionDeclaration(DF(snapshot_of))}
Sigma_lex=Sigma_t union {
  the exact §4.1 SemanticBinding(DF(snapshot_of)),
  MODEL_snapshot_of,
  CS(FUNCTION_MEANING,snapshot_of),CS(EVIDENCE_SCHEMA,none),
  CS(ACCESS_BOUNDARY,state_only),
  CS(UNKNOWN_BEHAVIOR,not_applicable),
  CS(EVALUATION_ERROR_BEHAVIOR,term)}
E_lex=SemanticEnvironment(
  abi_version=ABI0,declarations=Delta_lex,pair_declarations={},
  bindings={b|b in Sigma_lex and b is a SemanticBinding},
  pair_bindings={},profile_bindings={},authority_facts={},
  semantic_extensions={},lexical_bindings={lk0->lb0},choice_bindings={},
  mechanically_extracted_dependencies=required(S_lex),chi_C={})
Omega_lex={ABI0,E_lex,lb0} union Delta_lex union Sigma_lex
D_lex = DependencyEnvironment(S_lex,Omega_lex)
LEX_SOUND = ContractSpec(
  contract_key=(CK,coding.fixture,lexical_entailment,(1),SOUND_FRAGMENT),
  owner_layer=Service,contract_role=SOUND_FRAGMENT,
  primary_input_domain=(Formula,Formula),codomain={IN_FRAGMENT,OUTSIDE_FRAGMENT},
  observation_queries={},
  logical_relation={(f_lex,g_lex)->IN_FRAGMENT;
                    every unequal admitted pair->OUTSIDE_FRAGMENT})
LEX_REQ=SERVICE_SPEC(
  (CK,coding.fixture,lexical_entailment_evidence,(1),REQUIRED_EVIDENCE),
  REQUIRED_EVIDENCE,((Formula,Formula),finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  ((f_lex,g_lex),{})->ADMISSIBLE;
  every other admitted tuple->INADMISSIBLE)
LEX_FAIL=SERVICE_SPEC(
  (CK,coding.fixture,lexical_entailment_failure,(1),
   SERVICE_FAILURE_BEHAVIOR),SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,
  ReasoningResult.REASONING_ERROR,{},
  F->the exact K2 REASONING failure projection of F)
LEXSK=(CK,coding.fixture,lexical_entailment,(1),REASONING)
CAP_lex=(LEXSK,formula_entailment)
TARGET_lex=ENVIRONMENT_JUDGMENT_TARGET(
  FORMULA_ENTAILMENT,(f_lex,g_lex),semanticIdentity(E_lex))
LEX_CAP=CapabilityDescriptor(
  capability_key=CAP_lex,abi_version=ABI0,plugin_key=CK,
  service_role=REASONING,capability_class=PARTIAL_SYMBOLIC_REASONING,
  supported_judgments={FORMULA_ENTAILMENT},supported_targets={TARGET_lex},
  sound_fragment=LEX_SOUND,complete_fragment=ABSENT,
  dependency_scope=D_lex.transitive_dependency_closure,
  proper_semantic_dependencies=D_lex.proper_dependencies,
  dependency_closure=D_lex.transitive_dependency_closure,
  required_evidence=LEX_REQ,required_trust_roots={TR},
  failure_contract=LEX_FAIL)
R_lex = ReasoningRequest(
  abi_version=ABI0,judgment=FORMULA_ENTAILMENT,
  subjects=(f_lex,g_lex),semantic_environment=E_lex,
  trust_environment=T_absent,required_fragment=LEX_SOUND,
  complete_dependencies=D_lex,
  capability_target=TARGET_lex,
  capability_key=CAP_lex)

scope_extra=LexicalScopeIdentity(PREDICATE_EVALUATION,(S_t))
lk_extra=LexicalBindingKey(scope_extra,x_task,T(TaskSpec))
lb_extra=LexicalBinding(lexical_binding_key=lk_extra,admitted_value=t_t)
E_t_extra=SemanticEnvironment(
  abi_version=ABI0,declarations=Delta_t,pair_declarations={},
  bindings={the exact §4.2 SemanticBinding(DP(task_accepts))},
  pair_bindings={},profile_bindings={},authority_facts={},
  semantic_extensions={},lexical_bindings={lk_extra->lb_extra},
  choice_bindings={},mechanically_extracted_dependencies=required(S_t),
  chi_C={})
Omega_t_extra={ABI0,E_t_extra,lb_extra} union Delta_t union Sigma_t
D_t_extra=DependencyEnvironment(S_t,Omega_t_extra)
Q_t_extra=PredicateRequest(
  abi_version=ABI0,symbol_key=SP(task_accepts),
  binding_key=DP(task_accepts),semantic_environment=E_t_extra,
  trust_environment=T_admitted,dependency_environment=D_t_extra,
  arguments=(t_t,F_t,EVIDENCE_t),
  capability_target=BINDING_TARGET(DP(task_accepts)),
  capability_key=CAP(predicates))
EPK=((capknow.audit,evolution-proof),(1))
EVK=((capknow.audit,evolution-validator),(1))
TRE=(TP,coding,evolution-admission-root,(1))
EC_m=(PLUGIN_CERTIFICATE_ISSUER(EPK),coding.evolution,migration_m0)
EC_c=(PLUGIN_CERTIFICATE_ISSUER(EPK),coding.evolution,compatibility_c0)
EC_x0=(PLUGIN_CERTIFICATE_ISSUER(EPK),coding.evolution,extension_x0)
EC_x1=(PLUGIN_CERTIFICATE_ISSUER(EPK),coding.evolution,extension_x1)
EVSK_m=(EVK,coding.validation,migration_m0,(1),MIGRATION_VALIDATION)
EVSK_c=(EVK,coding.validation,compatibility_c0,(1),COMPATIBILITY_VALIDATION)
EVSK_x0=(EVK,coding.validation,extension_x0,(1),
         SEMANTIC_EXTENSION_VALIDATION)
EVSK_x1=(EVK,coding.validation,extension_x1,(1),
         SEMANTIC_EXTENSION_VALIDATION)
EVC_m=(EVSK_m,migration_relation)
EVC_c=(EVSK_c,compatibility_claim)
EVC_x0=(EVSK_x0,semantic_extension)
EVC_x1=(EVSK_x1,semantic_extension)
e0 = EvidenceRef(
  PLUGIN_ISSUER(CK),coding.verification,missing_matrix_record,
  CS(EVIDENCE_SCHEMA,verification))
v0 = VERIFY(coding.missing-matrix,s_c,CS(EVIDENCE_SCHEMA,verification))
vr0 = VERIFICATION_RECORD(
  v0,SNAPSHOT_IDENTITY(F_c),PASS,O_c,{e0})
i0=EVIDENCE_ENTRY(e0,VERIFICATION_EVIDENCE(vr0))
coding_entries(H0)={i0}
ev0 = EventValue(
  EK(dependency_refresh),DEPENDENCY_REFRESH(S_b,SNAPSHOT_IDENTITY(F_c)))
te0 = TraceEvent(ev0,user)
u0 = UnknownReason(
  PLUGIN_ISSUER(CK),coding.missing-matrix,(DP(task_accepts)))
fr_noresult=failureReason(
  CONCRETE_INVOCATION,PROTOCOL_FAILURE,Q_t[T_admitted],NO_RESULT_SENTINEL)
F_noresult=InterfaceFailure(
  domain=CONCRETE_INVOCATION,kind=PROTOCOL_FAILURE,reasons={fr_noresult})
RES_t=RESULT_RECORD(
  result_identity=(IDENTITY_OF(Q_t[T_admitted]),Eval,IDENTITY_OF(r_t)),
  result_value=r_t)
```

All validation objects for the four evolution records are finite and exact.
Let `Z={m,c,x0,x1}` and use only this total table:

| `z` | subject/key | request / judgment | validator / certificate / kind | certificate target / received result |
|---|---|---|---|---|
| `m` | `m0/MK0` | `MigrationAdmissionRequest` / `MIGRATION_RELATION_ADMISSION` | `EVC_m/EC_m/MIGRATION_RELATION_PROOF` | `MIGRATION_TRUST_TARGET(MK0)` / `MIGRATION_RELATION_ADMITTED(MK0,EC_m)` |
| `c` | `c0/CCK0` | `CompatibilityAdmissionRequest` / `COMPATIBILITY_CLAIM_ADMISSION` | `EVC_c/EC_c/COMPATIBILITY_CLAIM_PROOF` | `COMPATIBILITY_TRUST_TARGET(CCK0)` / `COMPATIBILITY_CLAIM_ADMITTED(CCK0,EC_c)` |
| `x0` | `x0/XK0` | `SemanticExtensionAdmissionRequest` / `SEMANTIC_EXTENSION_ADMISSION` | `EVC_x0/EC_x0/SEMANTIC_EXTENSION_VALIDATION` | `SEMANTIC_EXTENSION_TRUST_TARGET(XK0)` / `SEMANTIC_EXTENSION_ADMITTED(XK0,EC_x0)` |
| `x1` | `x1/XK1` | `SemanticExtensionAdmissionRequest` / `SEMANTIC_EXTENSION_ADMISSION` | `EVC_x1/EC_x1/SEMANTIC_EXTENSION_VALIDATION` | `SEMANTIC_EXTENSION_TRUST_TARGET(XK1)` / `SEMANTIC_EXTENSION_ADMITTED(XK1,EC_x1)` |

The literal records `ES_m/ECOMP_m/EE_m/EF_m`,
`ES_c/ECOMP_c/EE_c/EF_c`, `ES_x0/ECOMP_x0/EE_x0/EF_x0`, and
`ES_x1/ECOMP_x1/EE_x1/EF_x1` below are the exhaustive four rows.  Every sound
and complete record has fixed primary domain `T(EvolutionAdmissionSubject)`;
every evidence record has fixed primary domain
`(T(EvolutionAdmissionSubject),EVOLUTION_PROOF,finset(EvidenceRef))`; every
failure record has fixed primary domain `InterfaceFailure`.  Every query map
and derived support is literal `{}`.  No relation receives a migration,
claim, extension, alias, environment, `ContractSpec`, or relation record.  The
sixteen field-complete records are:

```text
ES_m=SERVICE_SPEC(
  (EVK,coding.evolution.contract,m,(1),SOUND_FRAGMENT),SOUND_FRAGMENT,
  T(EvolutionAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  mr_subject->IN_FRAGMENT; every unequal admitted value->OUTSIDE_FRAGMENT)
ECOMP_m=SERVICE_SPEC(
  (EVK,coding.evolution.contract,m,(1),COMPLETE_FRAGMENT),COMPLETE_FRAGMENT,
  T(EvolutionAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  mr_subject->IN_FRAGMENT; every unequal admitted value->OUTSIDE_FRAGMENT)
EE_m=SERVICE_SPEC(
  (EVK,coding.evolution.contract,m,(1),REQUIRED_EVIDENCE),REQUIRED_EVIDENCE,
  (T(EvolutionAdmissionSubject),EVOLUTION_PROOF,finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (mr_subject,EVOLUTION_PROOF(m,recordIdentity(m0),MIGRATION_TRUST_TARGET(MK0)),
   {ER_m})->ADMISSIBLE; every other admitted tuple->INADMISSIBLE)
EF_m=SERVICE_SPEC(
  (EVK,coding.evolution.contract,m,(1),SERVICE_FAILURE_BEHAVIOR),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,
  MigrationAdmissionResult.REASONING_ERROR,{},
  F->the exact K2 MIGRATION_VALIDATION failure projection of F)
ES_c=SERVICE_SPEC(
  (EVK,coding.evolution.contract,c,(1),SOUND_FRAGMENT),SOUND_FRAGMENT,
  T(EvolutionAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  cc_subject->IN_FRAGMENT; every unequal admitted value->OUTSIDE_FRAGMENT)
ECOMP_c=SERVICE_SPEC(
  (EVK,coding.evolution.contract,c,(1),COMPLETE_FRAGMENT),COMPLETE_FRAGMENT,
  T(EvolutionAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  cc_subject->IN_FRAGMENT; every unequal admitted value->OUTSIDE_FRAGMENT)
EE_c=SERVICE_SPEC(
  (EVK,coding.evolution.contract,c,(1),REQUIRED_EVIDENCE),REQUIRED_EVIDENCE,
  (T(EvolutionAdmissionSubject),EVOLUTION_PROOF,finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (cc_subject,EVOLUTION_PROOF(c,recordIdentity(c0),
   COMPATIBILITY_TRUST_TARGET(CCK0)),{ER_c})->ADMISSIBLE;
  every other admitted tuple->INADMISSIBLE)
EF_c=SERVICE_SPEC(
  (EVK,coding.evolution.contract,c,(1),SERVICE_FAILURE_BEHAVIOR),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,
  CompatibilityAdmissionResult.REASONING_ERROR,{},
  F->the exact K2 COMPATIBILITY_VALIDATION failure projection of F)
ES_x0=SERVICE_SPEC(
  (EVK,coding.evolution.contract,x0,(1),SOUND_FRAGMENT),SOUND_FRAGMENT,
  T(EvolutionAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  x0_subject->IN_FRAGMENT; every unequal admitted value->OUTSIDE_FRAGMENT)
ECOMP_x0=SERVICE_SPEC(
  (EVK,coding.evolution.contract,x0,(1),COMPLETE_FRAGMENT),COMPLETE_FRAGMENT,
  T(EvolutionAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  x0_subject->IN_FRAGMENT; every unequal admitted value->OUTSIDE_FRAGMENT)
EE_x0=SERVICE_SPEC(
  (EVK,coding.evolution.contract,x0,(1),REQUIRED_EVIDENCE),REQUIRED_EVIDENCE,
  (T(EvolutionAdmissionSubject),EVOLUTION_PROOF,finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (x0_subject,EVOLUTION_PROOF(x0,recordIdentity(x0),
   SEMANTIC_EXTENSION_TRUST_TARGET(XK0)),{ER_x0})->ADMISSIBLE;
  every other admitted tuple->INADMISSIBLE)
EF_x0=SERVICE_SPEC(
  (EVK,coding.evolution.contract,x0,(1),SERVICE_FAILURE_BEHAVIOR),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,
  SemanticExtensionAdmissionResult.REASONING_ERROR,{},
  F->the exact K2 SEMANTIC_EXTENSION_VALIDATION failure projection of F)
ES_x1=SERVICE_SPEC(
  (EVK,coding.evolution.contract,x1,(1),SOUND_FRAGMENT),SOUND_FRAGMENT,
  T(EvolutionAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  x1_subject->IN_FRAGMENT; every unequal admitted value->OUTSIDE_FRAGMENT)
ECOMP_x1=SERVICE_SPEC(
  (EVK,coding.evolution.contract,x1,(1),COMPLETE_FRAGMENT),COMPLETE_FRAGMENT,
  T(EvolutionAdmissionSubject),{IN_FRAGMENT,OUTSIDE_FRAGMENT},{},
  x1_subject->IN_FRAGMENT; every unequal admitted value->OUTSIDE_FRAGMENT)
EE_x1=SERVICE_SPEC(
  (EVK,coding.evolution.contract,x1,(1),REQUIRED_EVIDENCE),REQUIRED_EVIDENCE,
  (T(EvolutionAdmissionSubject),EVOLUTION_PROOF,finset(EvidenceRef)),
  {ADMISSIBLE,INADMISSIBLE},{},
  (x1_subject,EVOLUTION_PROOF(x1,recordIdentity(x1),
   SEMANTIC_EXTENSION_TRUST_TARGET(XK1)),{ER_x1})->ADMISSIBLE;
  every other admitted tuple->INADMISSIBLE)
EF_x1=SERVICE_SPEC(
  (EVK,coding.evolution.contract,x1,(1),SERVICE_FAILURE_BEHAVIOR),
  SERVICE_FAILURE_BEHAVIOR,InterfaceFailure,
  SemanticExtensionAdmissionResult.REASONING_ERROR,{},
  F->the exact K2 SEMANTIC_EXTENSION_VALIDATION failure projection of F)
ER_m=EvidenceRef(PLUGIN_ISSUER(EPK),coding.evolution,m,EE_m.contract_key)
ER_c=EvidenceRef(PLUGIN_ISSUER(EPK),coding.evolution,c,EE_c.contract_key)
ER_x0=EvidenceRef(PLUGIN_ISSUER(EPK),coding.evolution,x0,EE_x0.contract_key)
ER_x1=EvidenceRef(PLUGIN_ISSUER(EPK),coding.evolution,x1,EE_x1.contract_key)
```

The generic `z` equations above are only a finite audit table; package member
sets use the sixteen literal names.  The four descriptors are exactly

```text
TARGET_m=ENVIRONMENT_JUDGMENT_TARGET(
  MIGRATION_RELATION_ADMISSION,(m0),semanticIdentity(E_t))
TARGET_c=ENVIRONMENT_JUDGMENT_TARGET(
  COMPATIBILITY_CLAIM_ADMISSION,(c0),semanticIdentity(E_t))
TARGET_x0=ENVIRONMENT_JUDGMENT_TARGET(
  SEMANTIC_EXTENSION_ADMISSION,(x0),semanticIdentity(E_t))
TARGET_x1=ENVIRONMENT_JUDGMENT_TARGET(
  SEMANTIC_EXTENSION_ADMISSION,(x1),semanticIdentity(E_t))
Omega_ev_m=Omega_t union Delta_ev union Sigma_ev union {m0,MR0}
Omega_ev_c=Omega_t union Delta_ev union Sigma_ev union {c0,CC0,m0}
Omega_ev_x0=Omega_t union Delta_ev union Sigma_ev union {x0,a0,XE0,XP0}
Omega_ev_x1=Omega_t union Delta_ev union Sigma_ev union {x1,a1,XE0,XP0}
D_ev_m=DependencyEnvironment(MIGRATION_SUBJECT(m0),Omega_ev_m)
D_ev_c=DependencyEnvironment(COMPATIBILITY_SUBJECT(c0),Omega_ev_c)
D_ev_x0=DependencyEnvironment(SEMANTIC_EXTENSION_SUBJECT(x0),Omega_ev_x0)
D_ev_x1=DependencyEnvironment(SEMANTIC_EXTENSION_SUBJECT(x1),Omega_ev_x1)
EVCAP_m=CapabilityDescriptor(
  capability_key=EVC_m,abi_version=ABI0,plugin_key=EVK,
  service_role=MIGRATION_VALIDATION,
  capability_class=COMPLETE_FOR_DECLARED_FRAGMENT,
  supported_judgments={MIGRATION_RELATION_ADMISSION},
  supported_targets={TARGET_m},sound_fragment=ES_m,
  complete_fragment=ECOMP_m,
  dependency_scope=D_ev_m.transitive_dependency_closure,
  proper_semantic_dependencies=D_ev_m.proper_dependencies,
  dependency_closure=D_ev_m.transitive_dependency_closure,
  required_evidence=EE_m,required_trust_roots={TRE},failure_contract=EF_m)
EVCAP_c=CapabilityDescriptor(
  capability_key=EVC_c,abi_version=ABI0,plugin_key=EVK,
  service_role=COMPATIBILITY_VALIDATION,
  capability_class=COMPLETE_FOR_DECLARED_FRAGMENT,
  supported_judgments={COMPATIBILITY_CLAIM_ADMISSION},
  supported_targets={TARGET_c},sound_fragment=ES_c,
  complete_fragment=ECOMP_c,
  dependency_scope=D_ev_c.transitive_dependency_closure,
  proper_semantic_dependencies=D_ev_c.proper_dependencies,
  dependency_closure=D_ev_c.transitive_dependency_closure,
  required_evidence=EE_c,required_trust_roots={TRE},failure_contract=EF_c)
EVCAP_x0=CapabilityDescriptor(
  capability_key=EVC_x0,abi_version=ABI0,plugin_key=EVK,
  service_role=SEMANTIC_EXTENSION_VALIDATION,
  capability_class=COMPLETE_FOR_DECLARED_FRAGMENT,
  supported_judgments={SEMANTIC_EXTENSION_ADMISSION},
  supported_targets={TARGET_x0},sound_fragment=ES_x0,
  complete_fragment=ECOMP_x0,
  dependency_scope=D_ev_x0.transitive_dependency_closure,
  proper_semantic_dependencies=D_ev_x0.proper_dependencies,
  dependency_closure=D_ev_x0.transitive_dependency_closure,
  required_evidence=EE_x0,required_trust_roots={TRE},failure_contract=EF_x0)
EVCAP_x1=CapabilityDescriptor(
  capability_key=EVC_x1,abi_version=ABI0,plugin_key=EVK,
  service_role=SEMANTIC_EXTENSION_VALIDATION,
  capability_class=COMPLETE_FOR_DECLARED_FRAGMENT,
  supported_judgments={SEMANTIC_EXTENSION_ADMISSION},
  supported_targets={TARGET_x1},sound_fragment=ES_x1,
  complete_fragment=ECOMP_x1,
  dependency_scope=D_ev_x1.transitive_dependency_closure,
  proper_semantic_dependencies=D_ev_x1.proper_dependencies,
  dependency_closure=D_ev_x1.transitive_dependency_closure,
  required_evidence=EE_x1,required_trust_roots={TRE},failure_contract=EF_x1)
```

The K2 projections put respectively the literal triples
`{VALIDATION_CERTIFICATE(EC_m),VALIDATION_CAPABILITY(EVC_m),
VALIDATION_TRUST_ROOT(TRE)}`, `{VALIDATION_CERTIFICATE(EC_c),
VALIDATION_CAPABILITY(EVC_c),VALIDATION_TRUST_ROOT(TRE)}`,
`{VALIDATION_CERTIFICATE(EC_x0),VALIDATION_CAPABILITY(EVC_x0),
VALIDATION_TRUST_ROOT(TRE)}`, and `{VALIDATION_CERTIFICATE(EC_x1),
VALIDATION_CAPABILITY(EVC_x1),VALIDATION_TRUST_ROOT(TRE)}` into
`D_ev_m/D_ev_c/D_ev_x0/D_ev_x1.validation_references`, never into proper
closure.  Define the finite trust and request records:

```text
U_m=SERVICE_USE_TRUST_TARGET(
  EVC_m,MIGRATION_RELATION_ADMISSION,
  ENVIRONMENT_USE(MIGRATION_RELATION_ADMISSION,(m0)),semanticIdentity(E_t))
U_c=SERVICE_USE_TRUST_TARGET(
  EVC_c,COMPATIBILITY_CLAIM_ADMISSION,
  ENVIRONMENT_USE(COMPATIBILITY_CLAIM_ADMISSION,(c0)),semanticIdentity(E_t))
U_x0=SERVICE_USE_TRUST_TARGET(
  EVC_x0,SEMANTIC_EXTENSION_ADMISSION,
  ENVIRONMENT_USE(SEMANTIC_EXTENSION_ADMISSION,(x0)),semanticIdentity(E_t))
U_x1=SERVICE_USE_TRUST_TARGET(
  EVC_x1,SEMANTIC_EXTENSION_ADMISSION,
  ENVIRONMENT_USE(SEMANTIC_EXTENSION_ADMISSION,(x1)),semanticIdentity(E_t))
ROOT_E=TrustRootRecord(
  trust_root_key=TRE,owner=EMBEDDING_POLICY_PRODUCER(TP),
  trusted_validators={EVC_m,EVC_c,EVC_x0,EVC_x1},
  permitted_certificate_kinds={MIGRATION_RELATION_PROOF,
    COMPATIBILITY_CLAIM_PROOF,SEMANTIC_EXTENSION_VALIDATION},
  permitted_targets={U_m,U_c,U_x0,U_x1,
    MIGRATION_TRUST_TARGET(MK0),COMPATIBILITY_TRUST_TARGET(CCK0),
    SEMANTIC_EXTENSION_TRUST_TARGET(XK0),
    SEMANTIC_EXTENSION_TRUST_TARGET(XK1)},
  adoption=V0_EXTERNAL_TRUST_PREMISE)
T_evo=TrustEnvironment(
  trust_policy_key=TP,policy_owner=EMBEDDING_POLICY_PRODUCER(TP),
  root_judgments={TRE->TRUST_ROOT_ADMITTED(ROOT_E)})
R_m=MigrationAdmissionRequest(ABI0,m0,E_t,T_evo,D_ev_m,TARGET_m,EVC_m)
R_c0=CompatibilityAdmissionRequest(ABI0,c0,E_t,T_evo,D_ev_c,TARGET_c,EVC_c)
R_x0=SemanticExtensionAdmissionRequest(
  ABI0,x0,E_t,T_evo,D_ev_x0,TARGET_x0,EVC_x0)
R_x1=SemanticExtensionAdmissionRequest(
  ABI0,x1,E_t,T_evo,D_ev_x1,TARGET_x1,EVC_x1)
```

The four complete envelopes and admissions are literal records:

```text
EENV_m=CertificateEnvelope(
  certificate_key=EC_m,certificate_kind=MIGRATION_RELATION_PROOF,
  request_binding=R_m,subjects=(m0),environment=E_t,capability_key=EVC_m,
  fragment=ES_m,dependencies=D_ev_m,
  claimed_conclusion=MIGRATION_RELATION_ADMITTED(MK0,EC_m),
  validator_key=EVC_m,trust_root_key=TRE,abstraction_class=SYMBOLIC,
  payload=EVOLUTION_PROOF(m,recordIdentity(m0),MIGRATION_TRUST_TARGET(MK0)),
  evidence_refs={ER_m})
EENV_c=CertificateEnvelope(
  certificate_key=EC_c,certificate_kind=COMPATIBILITY_CLAIM_PROOF,
  request_binding=R_c0,subjects=(c0),environment=E_t,capability_key=EVC_c,
  fragment=ES_c,dependencies=D_ev_c,
  claimed_conclusion=COMPATIBILITY_CLAIM_ADMITTED(CCK0,EC_c),
  validator_key=EVC_c,trust_root_key=TRE,abstraction_class=SYMBOLIC,
  payload=EVOLUTION_PROOF(c,recordIdentity(c0),
                          COMPATIBILITY_TRUST_TARGET(CCK0)),
  evidence_refs={ER_c})
EENV_x0=CertificateEnvelope(
  certificate_key=EC_x0,certificate_kind=SEMANTIC_EXTENSION_VALIDATION,
  request_binding=R_x0,subjects=(x0),environment=E_t,capability_key=EVC_x0,
  fragment=ES_x0,dependencies=D_ev_x0,
  claimed_conclusion=SEMANTIC_EXTENSION_ADMITTED(XK0,EC_x0),
  validator_key=EVC_x0,trust_root_key=TRE,abstraction_class=SYMBOLIC,
  payload=EVOLUTION_PROOF(x0,recordIdentity(x0),
                          SEMANTIC_EXTENSION_TRUST_TARGET(XK0)),
  evidence_refs={ER_x0})
EENV_x1=CertificateEnvelope(
  certificate_key=EC_x1,certificate_kind=SEMANTIC_EXTENSION_VALIDATION,
  request_binding=R_x1,subjects=(x1),environment=E_t,capability_key=EVC_x1,
  fragment=ES_x1,dependencies=D_ev_x1,
  claimed_conclusion=SEMANTIC_EXTENSION_ADMITTED(XK1,EC_x1),
  validator_key=EVC_x1,
  trust_root_key=TRE,abstraction_class=SYMBOLIC,
  payload=EVOLUTION_PROOF(x1,recordIdentity(x1),
                          SEMANTIC_EXTENSION_TRUST_TARGET(XK1)),
  evidence_refs={ER_x1})
EENV_m_bad_root=EENV_m[trust_root_key:=TR]
EADMIT_m=CertificateAdmission.ADMITTED(
  EC_m,MIGRATION_RELATION_ADMITTED(MK0,EC_m))
EADMIT_c=CertificateAdmission.ADMITTED(
  EC_c,COMPATIBILITY_CLAIM_ADMITTED(CCK0,EC_c))
EADMIT_x0=CertificateAdmission.ADMITTED(
  EC_x0,SEMANTIC_EXTENSION_ADMITTED(XK0,EC_x0))
EADMIT_x1=CertificateAdmission.ADMITTED(
  EC_x1,SEMANTIC_EXTENSION_ADMITTED(XK1,EC_x1))
```

The preceding records exhaust the four-row table; no constructor family or
prose alias supplies a package member.  The exact subject producer set is
`{PLUGIN_PRODUCER(EOK),PLUGIN_PRODUCER(CK),ABI_PRODUCER(ABI0)}` because the
source/target environment contributes its exact ABI record.  Certificate,
validator, and root producers are
`PLUGIN_PRODUCER(EPK)`, `PLUGIN_PRODUCER(EVK)`, and
`EMBEDDING_POLICY_PRODUCER(TP)`, respectively, and are pairwise distinct.
The complete package records used by this fixture are

```text
PKG_evo_EOK=PluginPackage(
  ABI0,EOK,declarations={},pair_declarations={},bindings={},pair_bindings={},
  profile_bindings={},model_contracts={},aliases={a0,a1},services={},
  certificates={},authority_facts={},compatibility_claims={c0},
  migrations={m0},semantic_extensions={x0,x1},diagnostics=NONE)
PKG_evo_EPK=PluginPackage(
  ABI0,EPK,declarations={},pair_declarations={},bindings={},pair_bindings={},
  profile_bindings={},model_contracts={},aliases={},services={},
  certificates={EENV_m,EENV_c,EENV_x0,EENV_x1},authority_facts={},
  compatibility_claims={},migrations={},semantic_extensions={},
  diagnostics=NONE)
PKG_evo_EVK=PluginPackage(
  ABI0,EVK,declarations={},pair_declarations={},bindings={},pair_bindings={},
  profile_bindings={},model_contracts={},aliases={},
  services={EVCAP_m,EVCAP_c,EVCAP_x0,EVCAP_x1},certificates={},
  authority_facts={},compatibility_claims={},migrations={},
  semantic_extensions={},diagnostics=NONE)
PKG_CK_no_task_model=
  PKG_CK[model_contracts:=MODEL_X minus {MODEL_task_accepts}]
PKG_APK_no_choice_fact=PKG_APK[authority_facts:=
  {AFB(b,1),AFB(c,1),AFB(c,2),AFB(w,1),AFB(w,2)}]
PKG_evo_EOK_no_m=PKG_evo_EOK[migrations:={}]
PKG_evo_EOK_no_c=PKG_evo_EOK[compatibility_claims:={}]
PKG_evo_EOK_no_x0=PKG_evo_EOK[semantic_extensions:={x1}]
PKG_evo_EOK_no_x1=PKG_evo_EOK[semantic_extensions:={x0}]
PKG_evo_EOK_alias_optional=
  PKG_evo_EOK[semantic_extensions:={x1}]
PKG_evo_EOK_alias_optional_no_a0=
  PKG_evo_EOK[aliases:={a1},semantic_extensions:={x1}]
PKG_evo_EOK_no_a1=PKG_evo_EOK[aliases:={a0}]
```

These packages are finite fixture constructors only; no omission package is
ever composed with its same-key baseline package.

The independent pair owner package, used only by the `PAIR_INDEPENDENT`
packet entry and pair rows below, is the following complete record:

```text
PKG_pair_CK=PluginPackage(
  ABI0,CK,declarations=DELTA_TYPE_X union {
    LiteralDeclaration(T(PairTraceDomain),ALL_ADMITTED_TRACES),
    LiteralDeclaration(T(PairComparedFields),COMPLETE_EVAL_RECORD),
    LiteralDeclaration(T(ServiceAdmissionSubject),pair_subject),
    PredicateDeclaration(DP(refresh_scope)),
    PredicateDeclaration(DP(refresh_occurred)),
    EventDeclaration(DE(dependency_refresh))},pair_declarations={pd},
  bindings={sb,
    the exact literal SemanticBinding(T(PairTraceDomain),ALL_ADMITTED_TRACES),
    the exact literal SemanticBinding(T(PairComparedFields),COMPLETE_EVAL_RECORD),
    the exact literal SemanticBinding(T(ServiceAdmissionSubject),pair_subject)},
  pair_bindings={PB_alt},profile_bindings={},
  model_contracts={MODEL_refresh_scope,MODEL_refresh_occurred,
    MODEL_LITERAL(T(PairTraceDomain),ALL_ADMITTED_TRACES),
    MODEL_LITERAL(T(PairComparedFields),COMPLETE_EVAL_RECORD),
    MODEL_LITERAL(T(ServiceAdmissionSubject),pair_subject)},aliases={},
  services={},certificates={},authority_facts={},compatibility_claims={},
  migrations={},semantic_extensions={},diagnostics=NONE)
```

The missing fixture uses canonical K2 record maps, not bags of nested values.
For an exact universe `U`, `A(U)` is the K2 §3.3 map from `RecordIdentity` to
the unique authoritative complete record after independently supplied equal
records coalesce.  Define

```text
authoritativeCount(i,U)=1 when A(U)[i] is defined, otherwise 0
authoritativePairs(R)=A(the exact reconstruction fragment whose complete
  containers are precisely R), including each container's displayed members
RECONSTRUCT(U,Rminus,Rplus)=
  the exact universe obtained by removing every complete container in Rminus,
  inserting every complete container in Rplus, and changing no other record
```

`RECONSTRUCT` is defined only when `Rminus` names every package, environment,
request, result, or derived carrier that contains the target record rather
than merely its key.  Its exact postcondition is
`A(U) symmetric_difference A(RECONSTRUCT(U,Rminus,Rplus)) =
authoritativePairs(Rminus) symmetric_difference authoritativePairs(Rplus)`.
Thus a stale nested copy makes a fixture
undefined instead of silently turning a deletion into a no-op.

The complete replacements used below are literal.  Bracket notation changes
the displayed field and repeats every other complete field exactly.  Each
`D_*'`, request, result, lifecycle, and `chi_C` value is recomputed from the
replacement inputs; none is copied from its baseline.

```text
PKG_CK_no_decl=PKG_CK[declarations:=PKG_CK.declarations minus
  {PredicateDeclaration(DP(task_accepts))}]
PKG_CK_no_event=PKG_CK[declarations:=PKG_CK.declarations minus
  {EventDeclaration(DE(dependency_refresh))}]
PKG_CK_no_binding=PKG_CK[bindings:=PKG_CK.bindings minus
  {SemanticBinding(DP(task_accepts))}]
PKG_CK_no_profile=PKG_CK[profile_bindings:={}]
PKG_pair_CK_no_pair_decl=PKG_pair_CK[pair_declarations:={}]
PKG_pair_CK_no_pair_binding=PKG_pair_CK[pair_bindings:={}]
PKG_CK_no_predicate_service=PKG_CK[services:=
  PKG_CK.services minus {CapabilityDescriptor(CAP(predicates))}]

E_choice_no_fact=E_choice[
  authority_facts:={},choice_bindings:={},chi_C:={}]
E_choice_no_binding=E_choice[choice_bindings:={},chi_C:={}]
E_lex_no_lb=E_lex[lexical_bindings:={}]
Omega_lex_no_lb={ABI0,E_lex_no_lb} union Delta_lex union Sigma_lex
D_lex_no_lb=DependencyEnvironment(S_lex,Omega_lex_no_lb)
R_lex_no_lb=R_lex[semantic_environment:=E_lex_no_lb,
  complete_dependencies:=D_lex_no_lb]

CAP_pred_wrong_sound=CapabilityDescriptor(CAP(predicates))[
  sound_fragment:=FSOUND]
PKG_CK_wrong_service_spec=PKG_CK[services:=
  (PKG_CK.services minus {CapabilityDescriptor(CAP(predicates))}) union
  {CAP_pred_wrong_sound}]
B_task_wrong_meaning=SemanticBinding(DP(task_accepts))[
  meaning_contract:=CS(PREDICATE_MEANING,observations_equal)]
PKG_CK_wrong_sigma_spec=PKG_CK[bindings:=
  (PKG_CK.bindings minus {SemanticBinding(DP(task_accepts))}) union
  {B_task_wrong_meaning}]

E_t_empty=E_t[declarations:={},bindings:={},pair_bindings:={},
  profile_bindings:={},authority_facts:={},semantic_extensions:={},
  lexical_bindings:={},choice_bindings:={},
  mechanically_extracted_dependencies:={},chi_C:={}]
Omega_t_empty={ABI0,E_t_empty}
D_t_empty=DependencyEnvironment(S_t,Omega_t_empty)
Q_t_empty=Q_t[T_admitted][semantic_environment:=E_t_empty,
  dependency_environment:=D_t_empty]
RES_t_empty=RESULT_RECORD(
  result_identity=(IDENTITY_OF(Q_t_empty),Eval,IDENTITY_OF(r_t)),
  result_value=r_t)

Q_t_no_trust=Q_t[T_admitted][trust_environment:=T_absent]
RES_t_no_trust=RESULT_RECORD(
  result_identity=(IDENTITY_OF(Q_t_no_trust),Eval,IDENTITY_OF(r_t)),
  result_value=r_t)

D_t_incomplete=DependencyEnvironment(
  S_t,Omega_t minus {SemanticBinding(DP(task_accepts))})
Q_t_incomplete=Q_t[T_admitted][dependency_environment:=D_t_incomplete]
RES_t_incomplete=RESULT_RECORD(
  result_identity=(IDENTITY_OF(Q_t_incomplete),Eval,IDENTITY_OF(r_t)),
  result_value=r_t)

M_c_missing=DependencyObservationEnvironment({N_o->V_o})
fr_c_missing=failureReason(
  REASONING_INVOCATION,MALFORMED_RESULT(SEMANTIC_MISMATCH),R_c,
  RESULT_OFFENDER((IDENTITY_OF(R_c),ReasoningResult,IDENTITY_OF(Y_c))))
F_c_missing=InterfaceFailure(
  domain=REASONING_INVOCATION,
  kind=MALFORMED_RESULT(SEMANTIC_MISMATCH),reasons={fr_c_missing})
L_c_missing=LifecycleState(DECLARATION_NOT_REQUIRED,
  BINDING_NOT_REQUIRED,CAPABILITY_DISCOVERED,
  INVOCATION_FAILED(PROTOCOL,{fr_c_missing}))
K_c_missing=(WELL_FORMED,CLOSED,EVALUABILITY_AVAILABLE,
  LIFECYCLE_RECORD((J_c,IDENTITY_OF(R_c)))->L_c_missing,
  OBSERVATION_ENVIRONMENT_RECORD(IDENTITY_OF(M_c_missing))->M_c_missing,
  interface_failure=F_c_missing,
  CONSISTENCY_UNKNOWN)

ROOT_TR_c_alt=ROOT_TR_c[permitted_targets:={U_c,U_t}]
T_c_alt=TrustEnvironment(
  trust_policy_key=TP,policy_owner=EMBEDDING_POLICY_PRODUCER(TP),
  root_judgments={TR->TRUST_ROOT_ADMITTED(ROOT_TR_c_alt)})
R_c_alt=R_c[trust_environment:=T_c_alt]
L_life_after=LifecycleState(DECLARATION_NOT_REQUIRED,
  BINDING_NOT_REQUIRED,CAPABILITY_DISCOVERED,
  INVOCABLE_FOR(R_c_alt))
K_life_after=(WELL_FORMED,CLOSED,EVALUABILITY_AVAILABLE,
  LIFECYCLE_RECORD((J_c,IDENTITY_OF(R_c_alt)))->L_life_after,
  CONSISTENCY_UNKNOWN)

d_bad_signature=d_bad[argument_types:=
  (T(TaskSpec),T(RepositorySnapshot),T(EvidenceStore),T(StorageBackend))]
conflict0=CONFLICT_OF(d,d_bad)
conflict1=CONFLICT_OF(d,d_bad_signature)

T_root_missing=TrustEnvironment(
  trust_policy_key=TP,policy_owner=EMBEDDING_POLICY_PRODUCER(TP),
  root_judgments={})
```

The `d_bad_signature` substitution changes a real declaration field; there is
no declaration `exact_version` field.  `E_choice_no_fact` and
`E_choice_no_binding` recompute `chi_C={}`.  `AF(choice,1)` remains an
`AuthorityFactKey` inside `cbe0`; it is never used where an
`AuthorityFactBinding` is required.

`MissingRowId` is exactly this 42-tag enumeration:

```text
MissingRowId = ABI | PLUGIN | DECLARATION | SYMBOL | EVENT |
  PAIR_DECLARATION | OUTCOME | BINDING | PROFILE_BINDING | PAIR_BINDING |
  AUTHORITY_FACT | CHOICE_BINDING | LEXICAL_BINDING |
  EXTRANEOUS_LEXICAL_BINDING | SERVICE | CAPABILITY | TRUST_POLICY |
  TRUST_ROOT | CERTIFICATE | MIGRATION | COMPATIBILITY_CLAIM |
  EXTENSION_OPTIONAL | EXTENSION_REQUIRED | MODEL_CONTRACT |
  ALIAS_OPTIONAL | ALIAS_REQUIRED | SIGMA_CONTRACT_SPEC |
  SERVICE_CONTRACT_SPEC | REQUEST | RESULT | SEMANTIC_ENVIRONMENT |
  TRUST_ENVIRONMENT | DEPENDENCY_ENVIRONMENT | OBSERVATION_ENVIRONMENT |
  LIFECYCLE | EVENT_VALUE | TRACE_EVENT | SOURCE | AUTHORITY_REF |
  EVIDENCE | REASON | CONFLICT
```

For each row `k`, `ROW(k;...)` constructs a fresh, separately tagged K2
universe containing exactly the displayed complete records and the exact
proper and validation roots of those records.  The literal package member
sets are the ones displayed in their complete `PluginPackage` values; this is
not an implicit package-member closure.  `ROW` deep-copies values, so no
package, environment, request, result, or carrier is shared by two rows.
`B_k` is the named baseline `ROW(k;baseline records)` and
`V_k=RECONSTRUCT(B_k,Rminus_k,Rplus_k)`.  The table is also the literal
definition of the finite maps `i[k]`, `Rminus[k]`, `Rplus[k]`, and
`MISSING_EXPECTED[k]`; its fourth cell is the complete value of
`MISSING_EXPECTED[k]`, not a comment or selector.

<!-- K3S-MISSING-BEGIN -->
| `MissingRowId k`; target `RecordIdentity i_k` | exact self-contained `B_k` records | exact `Rminus_k -> Rplus_k` reconstruction | exact variant result |
|---|---|---|---|
| `ABI`; `ABI_RECORD(ABI0)` | `ROW(ABI; ABI0,PKG_CK)` | `{ABI0}->{}` | `MALFORMED` |
| `PLUGIN`; `PACKAGE_RECORD(ABI0,CK)` | `ROW(PLUGIN; ABI0,PKG_CK)` | `{PKG_CK}->{}` | `MALFORMED` |
| `DECLARATION`; `DECLARATION_RECORD(DP(task_accepts))` | `ROW(DECLARATION; ABI0,PKG_CK)` | `{PKG_CK}->{PKG_CK_no_decl}` | `MALFORMED` |
| `SYMBOL`; `DECLARATION_RECORD(DP(task_accepts))`, queried as `SYMBOL(SP(task_accepts))` | `ROW(SYMBOL; ABI0,PKG_CK)` | `{PKG_CK}->{PKG_CK_no_decl}` | `MALFORMED` |
| `EVENT`; `DECLARATION_RECORD(DE(dependency_refresh))`, queried as `EVENT(EK(dependency_refresh))` | `ROW(EVENT; ABI0,PKG_CK)` | `{PKG_CK}->{PKG_CK_no_event}` | `MALFORMED` |
| `PAIR_DECLARATION`; `PAIR_DECLARATION_RECORD(PAIR(refresh))` | `ROW(PAIR_DECLARATION; ABI0,PKG_pair_CK)` | `{PKG_pair_CK}->{PKG_pair_CK_no_pair_decl}` | `MALFORMED` |
| `OUTCOME`; `OUTCOME_RECORD(IDENTITY_OF(O_w))` | `ROW(OUTCOME; ABI0,C_w,O_w)` | `{O_w}->{}` | `MALFORMED` |
| `BINDING`; `BINDING_RECORD(DP(task_accepts))` | `ROW(BINDING; ABI0,PKG_CK)` | `{PKG_CK}->{PKG_CK_no_binding}` | `OPEN_BINDINGS` |
| `PROFILE_BINDING`; `PROFILE_BINDING_RECORD(PK(implementation_evidence))` | `ROW(PROFILE_BINDING; ABI0,PKG_CK)` | `{PKG_CK}->{PKG_CK_no_profile}` | `OPEN_BINDINGS` |
| `PAIR_BINDING`; `PAIR_BINDING_RECORD(PAIR(refresh))` | `ROW(PAIR_BINDING; ABI0,PKG_pair_CK)` | `{PKG_pair_CK}->{PKG_pair_CK_no_pair_binding}` | `OPEN_BINDINGS` |
| `AUTHORITY_FACT`; `AUTHORITY_FACT_RECORD(AF(choice,1))` | `ROW(AUTHORITY_FACT; ABI0,PKG_APK,C_choice,E_choice,cbe0)` | `{PKG_APK,E_choice}->{PKG_APK_no_choice_fact,E_choice_no_fact}` | `OPEN_BINDINGS({AUTHORITY_FACT(AF(choice,1))})` |
| `CHOICE_BINDING`; `CHOICE_BINDING_RECORD(cb0)` | `ROW(CHOICE_BINDING; ABI0,PKG_APK,C_choice,E_choice)` | `{E_choice}->{E_choice_no_binding}` | `OPEN_BINDINGS({CHOICE_BINDING(cb0)})` |
| `LEXICAL_BINDING`; `LEXICAL_BINDING_RECORD(lk0)` | `ROW(LEXICAL_BINDING; ABI0,PKG_CK,S_lex,E_lex,D_lex,R_lex)` | `{E_lex,D_lex,R_lex}->{E_lex_no_lb,D_lex_no_lb,R_lex_no_lb}` | `OPEN_BINDINGS({LEXICAL_BINDING(lk0)})` |
| `EXTRANEOUS_LEXICAL_BINDING`; `REQUEST_RECORD(IDENTITY_OF(Q_t[T_admitted]))` | `ROW(EXTRANEOUS_LEXICAL_BINDING; ABI0,PKG_CK,E_t,D_t,T_admitted,Q_t[T_admitted])` | `{E_t,D_t,Q_t[T_admitted]}->{E_t_extra,D_t_extra,Q_t_extra}` | `MALFORMED_REQUEST(EXTRANEOUS_LEXICAL_BINDING(lk_extra))` |
| `SERVICE`; `SERVICE_RECORD(SK(predicates))` | `ROW(SERVICE; ABI0,PKG_CK,E_t,D_t,T_admitted,Q_t[T_admitted])` | `{PKG_CK}->{PKG_CK_no_predicate_service}` | `EVALUABILITY_MISSING` |
| `CAPABILITY`; `CAPABILITY_RECORD(CAP(predicates))` | `ROW(CAPABILITY; ABI0,PKG_CK,E_t,D_t,T_admitted,Q_t[T_admitted])` | `{PKG_CK}->{PKG_CK[services:=PKG_CK.services minus {CapabilityDescriptor(CAP(predicates))}]}` | `EVALUABILITY_MISSING` |
| `TRUST_POLICY`; `TRUST_POLICY_RECORD(TP)` | `ROW(TRUST_POLICY; ABI0,T_admitted)` | `{T_admitted}->{}` | `TRUST_ROOT_ABSENT` |
| `TRUST_ROOT`; `TRUST_ROOT_RECORD(TR)` | `ROW(TRUST_ROOT; ABI0,ROOT_TR_t,T_admitted)` | `{ROOT_TR_t,T_admitted}->{T_root_missing}` | `TRUST_ROOT_ABSENT(TR)` |
| `CERTIFICATE`; `CERTIFICATE_RECORD(BCERT)` | `ROW(CERTIFICATE; ABI0,PKG_CK,BENV,R_b,T_b)` | `{PKG_CK,BENV}->{PKG_CK[certificates:={}]}` | `(NO_CERTIFICATE_ADMISSION,CONSISTENCY_UNKNOWN)` |
| `MIGRATION`; `MIGRATION_RECORD(MK0)` | `ROW(MIGRATION; ABI0,PKG_evo_EOK,c0)` | `{PKG_evo_EOK}->{PKG_evo_EOK_no_m}` | `NO_MIGRATION(MK0)` |
| `COMPATIBILITY_CLAIM`; `COMPATIBILITY_RECORD(CCK0)` | `ROW(COMPATIBILITY_CLAIM; ABI0,PKG_evo_EOK,R_c0)` | `{PKG_evo_EOK,R_c0}->{PKG_evo_EOK_no_c}` | `NO_COMPATIBILITY(CCK0)` |
| `EXTENSION_OPTIONAL`; `SEMANTIC_EXTENSION_RECORD(XK0)` | `ROW(EXTENSION_OPTIONAL; ABI0,PKG_evo_EOK)` | `{PKG_evo_EOK}->{PKG_evo_EOK_no_x0}` | `NO_EFFECT(XK0)` |
| `EXTENSION_REQUIRED`; `SEMANTIC_EXTENSION_RECORD(XK1)` | `ROW(EXTENSION_REQUIRED; ABI0,PKG_evo_EOK,R_x1)` | `{PKG_evo_EOK,R_x1}->{PKG_evo_EOK_no_x1}` | `INCOMPATIBLE(XK1)` |
| `MODEL_CONTRACT`; `MODEL_CONTRACT_RECORD(MODEL_task_accepts.model_contract_key)` | `ROW(MODEL_CONTRACT; ABI0,PKG_CK)` | `{PKG_CK}->{PKG_CK_no_task_model}` | `OPEN_BINDINGS(model contract)` |
| `ALIAS_OPTIONAL`; `ALIAS_RECORD(AK0)` | `ROW(ALIAS_OPTIONAL; ABI0,PKG_evo_EOK_alias_optional)` | `{PKG_evo_EOK_alias_optional}->{PKG_evo_EOK_alias_optional_no_a0}` | `NO_ALIAS(AK0)` |
| `ALIAS_REQUIRED`; `ALIAS_RECORD(AK1)` | `ROW(ALIAS_REQUIRED; ABI0,PKG_evo_EOK,R_x1)` | `{PKG_evo_EOK}->{PKG_evo_EOK_no_a1}` | `MALFORMED(missing alias AK1)` |
| `SIGMA_CONTRACT_SPEC`; `CONTRACT_SPEC_RECORD(CS(PREDICATE_MEANING,task_accepts))` | `ROW(SIGMA_CONTRACT_SPEC; ABI0,PKG_CK)` | `{PKG_CK}->{PKG_CK_wrong_sigma_spec}` | `(BINDING_INCOMPATIBLE,OPEN_BINDINGS)` |
| `SERVICE_CONTRACT_SPEC`; `CONTRACT_SPEC_RECORD(QSOUND.contract_key)` | `ROW(SERVICE_CONTRACT_SPEC; ABI0,PKG_CK)` | `{PKG_CK}->{PKG_CK_wrong_service_spec}` | `(CAPABILITY_INCOMPATIBLE,EVALUABILITY_MISSING)` |
| `REQUEST`; `REQUEST_RECORD(IDENTITY_OF(Q_t[T_admitted]))` | `ROW(REQUEST; ABI0,PKG_CK,E_t,D_t,T_admitted,Q_t[T_admitted],RES_t)` | `{Q_t[T_admitted],RES_t}->{}` | `MALFORMED_REQUEST` |
| `RESULT`; `RESULT_RECORD((IDENTITY_OF(Q_t[T_admitted]),Eval,IDENTITY_OF(r_t)))` | `ROW(RESULT; ABI0,PKG_CK,E_t,D_t,T_admitted,Q_t[T_admitted],RES_t)` | `{RES_t}->{F_noresult}` | `INVOCATION_FAILED(PROTOCOL,{fr_noresult})`; no truth |
| `SEMANTIC_ENVIRONMENT`; `SEMANTIC_ENVIRONMENT_RECORD(semanticIdentity(E_t))` | `ROW(SEMANTIC_ENVIRONMENT; ABI0,PKG_CK,E_t,D_t,T_admitted,Q_t[T_admitted],RES_t)` | `{E_t,D_t,Q_t[T_admitted],RES_t}->{E_t_empty,D_t_empty,Q_t_empty,RES_t_empty}` | `MALFORMED_REQUEST(IDENTITY_OF(Q_t[T_admitted]))` |
| `TRUST_ENVIRONMENT`; `TRUST_ENVIRONMENT_RECORD(trustEnvironmentIdentity(T_admitted))` | `ROW(TRUST_ENVIRONMENT; ABI0,PKG_CK,E_t,D_t,T_admitted,Q_t[T_admitted],RES_t)` | `{T_admitted,Q_t[T_admitted],RES_t}->{T_absent,Q_t_no_trust,RES_t_no_trust}` | `MALFORMED_REQUEST(IDENTITY_OF(Q_t[T_admitted]))` |
| `DEPENDENCY_ENVIRONMENT`; `DEPENDENCY_ENVIRONMENT_RECORD(IDENTITY_OF(D_t))` | `ROW(DEPENDENCY_ENVIRONMENT; ABI0,PKG_CK,E_t,D_t,T_admitted,Q_t[T_admitted],RES_t)` | `{D_t,Q_t[T_admitted],RES_t}->{D_t_incomplete,Q_t_incomplete,RES_t_incomplete}` | `MALFORMED_REQUEST(IDENTITY_OF(Q_t[T_admitted]))` |
| `OBSERVATION_ENVIRONMENT`; `OBSERVATION_ENVIRONMENT_RECORD(IDENTITY_OF(M_c))` | `ROW(OBSERVATION_ENVIRONMENT; ABI0,PKG_CK,R_c,M_c,Y_c,L_c_final,K_c)` | `{M_c,Y_c,L_c_final,K_c}->{M_c_missing,F_c_missing,L_c_missing,K_c_missing}` | `MALFORMED_RESULT(SEMANTIC_MISMATCH)` |
| `LIFECYCLE`; `LIFECYCLE_RECORD((J_c,IDENTITY_OF(R_c)))` | `ROW(LIFECYCLE; ABI0,PKG_CK,R_c,M_c,Y_c,L_c_final,K_c)` | `{R_c,L_c_final,K_c}->{R_c_alt,L_life_after,K_life_after}` | `(LIFECYCLE_RECORD((J_c,IDENTITY_OF(R_c_alt)))->L_life_after,INVOCABLE_FOR(R_c_alt))` |
| `EVENT_VALUE`; `EVENT_VALUE_RECORD(IDENTITY_OF(ev0))` | `ROW(EVENT_VALUE; ABI0,EventDeclaration(DE(dependency_refresh)),ev0,te0)` | `{ev0,te0}->{}` | `MALFORMED` |
| `TRACE_EVENT`; `TRACE_EVENT_RECORD(IDENTITY_OF(te0))` | `ROW(TRACE_EVENT; ABI0,ev0,te0)` | `{te0}->{}` | `MALFORMED` |
| `SOURCE`; `SOURCE_RECORD(IDENTITY_OF(src0))` | `ROW(SOURCE; ABI0,src0)` | `{src0}->{}` | `MALFORMED` |
| `AUTHORITY_REF`; `AUTHORITY_REF_RECORD(IDENTITY_OF(auth0))` | `ROW(AUTHORITY_REF; ABI0,auth0)` | `{auth0}->{}` | `MALFORMED` |
| `EVIDENCE`; `EVIDENCE_RECORD(e0)` | `ROW(EVIDENCE; ABI0,e0,v0,vr0,i0,H0)` | `{e0,vr0,i0,H0}->{}` | `TRUTH_UNKNOWN` |
| `REASON`; `REASON_RECORD(UnknownReason,IDENTITY_OF(u0))` | `ROW(REASON; ABI0,u0,VALUE(UNKNOWN,{},{u0}))` | `{u0,VALUE(UNKNOWN,{},{u0})}->{}` | `MALFORMED_RESULT(MALFORMED_CARRIER)` |
| `CONFLICT`; `CONFLICT_RECORD(conflict0)` | `ROW(CONFLICT; ABI0,d,d_bad,conflict0)` | `{d_bad,conflict0}->{d_bad_signature,conflict1}` | `(CONFLICT_RECORD(conflict1),MALFORMED)` |
<!-- K3S-MISSING-END -->

For every one of these 42 rows, the following equations are fixture
assertions, not review-time prose:

```text
q[SYMBOL]=SYMBOL(SP(task_accepts))
q[EVENT]=EVENT(EK(dependency_refresh))
q[k]=dependencyRoot(i[k]) for every other displayed MissingRowId k
conformantUniverseInput(B_k)=TRUE
conformantUniverseInput(V_k)=TRUE
authoritativeCount(i[k],B_k)=1
recordAt(q[k],B_k)=PRESENT(A(B_k)[i[k]])
authoritativeCount(i[k],V_k)=0
recordAt(q[k],V_k)=ABSENT_REQUIRED_RECORD(q[k])
A(B_k) symmetric_difference A(V_k)=
  authoritativePairs(Rminus[k]) symmetric_difference
  authoritativePairs(Rplus[k])
missingStatus(q[k],V_k)=MISSING_EXPECTED[k]
```

For a universe `U`, define
`serviceDescriptors(s,U)={c in range(A(U)) | c=CapabilityDescriptor(_) and
c.capability_key.service_key=s}` and
`authoritativeServiceTargetCount(s,U)=|serviceDescriptors(s,U)|`.  For the
`SERVICE` row, with `B_SERVICE=B_{SERVICE}` and `V_SERVICE=V_{SERVICE}`,
`serviceDescriptors(SK(predicates),B_SERVICE)={CapabilityDescriptor(CAP(predicates))}`
and `serviceDescriptors(SK(predicates),V_SERVICE)={}`.  Therefore the exact
derived `ServiceIdentityRecord(SK(predicates))` target count is `1 -> 0`, and
`recordAt(q[SERVICE],V_SERVICE)=ABSENT_REQUIRED_RECORD(q[SERVICE])`; removing
only its derived carrier would not be a reconstruction.  For `TRUST_ROOT`,
`T_root_missing.root_judgments` has no `TR` entry and the row contains no
request, descriptor, certificate, or other record requiring `TR`; it is a
genuine absent-record row, not a replacement by `TRUST_ROOT_ABSENT(TR)`.  For
`EVIDENCE`, `vr0` is removed together with `e0`, `i0`, and `H0`, so the
reconstructed row has zero occurrences of `e0` in every record or nested
container.  These three row-local assertions are part of the preceding
exhaustive equations.

For `EXTRANEOUS_LEXICAL_BINDING`, `LIFECYCLE`, and `CONFLICT`, `V_k`
additionally has exactly one occurrence of the displayed substituted request,
lifecycle, or conflict identity.  For all other rows it has no substituted
target identity.  Baseline and variant records from one row are never members
of another row's universe.

The non-missing packet entries are independently constructed as follows:

```text
U_CORE_DEFINITIONAL=ROW(CORE_DEFINITIONAL;
  ABI0,PKG_CK,PKG_AWK,PKG_RVK,PKG_APK,PKG_ATK,PKG_AVK,
  C_b,C_c,C_w,C_choice,E_b,E_c,E_w,E_choice)
U_PAIR_INDEPENDENT=ROW(PAIR_INDEPENDENT;
  ABI0,PKG_pair_CK,PKG_PPK,PKG_PVK,E_p,D_p,R_p,PENV,
  PairFullEvalProof,PAIR_PROOF_REF,
  CertificateAdmission.ADMITTED(
    PCERT,PAIR_COHERENCE_ADMITTED(PAIR(refresh),PCERT)))
U_TRUST_ADMITTED=ROW(TRUST_ADMITTED;
  ABI0,PKG_CK,E_t,D_t,T_admitted,Q_t[T_admitted],RES_t)
U_TRUST_ABSENT=ROW(TRUST_ABSENT;
  ABI0,PKG_CK,E_t,D_t,T_absent,Q_t[T_absent])
U_TRUST_UNDECIDED=ROW(TRUST_UNDECIDED;
  ABI0,PKG_CK,E_t,D_t,T_undecided,Q_t[T_undecided])
U_TRUST_INCOMPATIBLE=ROW(TRUST_INCOMPATIBLE;
  ABI0,PKG_CK,E_t,D_t,T_incompatible,Q_t[T_incompatible])
U_TRUST_FAILED=ROW(TRUST_FAILED;
  ABI0,PKG_CK,E_t,D_t,T_failed,Q_t[T_failed])
```

There is no generic carrier/result selector: every retained K2 missing-status
constructor has this exact named row, target identity, reconstruction set, and
result.  The packet map uses each `B_k` and `V_k` as distinct values and never
unions them.
### 9.5 Two-node confluence and permutation fixtures

Fix the already named `s_c,P_c,F_c,C_c,E_c,D_c,J_c` and define the two exact
node results

```text
N_o = BINDING(DF(observe))
N_d = BINDING(DF(changes_between))
V_o = TERM_OBS(TERM_VALUE(O_c))
V_d = TERM_OBS(TERM_VALUE(X_c))
M_c = DependencyObservationEnvironment({N_o -> V_o, N_d -> V_d})
```

The `CSOUND` query at `N_o` is exactly
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
  CSOUND,D_c,J_c,CAP(confluence))
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

For this exact `R_c`, the final reasoning-subject producer set is identically
`{PLUGIN_PRODUCER(CK),PLUGIN_PRODUCER(APK),PLUGIN_PRODUCER(ATK),
PLUGIN_PRODUCER(AVK),EMBEDDING_POLICY_PRODUCER(ATP),ABI_PRODUCER(ABI0)}`;
the `CAP(confluence)` producer is `PLUGIN_PRODUCER(CK)` and the independent
root producer `EMBEDDING_POLICY_PRODUCER(TP)` is outside that subject set.

The nonempty certificate-kind set grants no admission target.  The ordered
invocation transition under either topological order is

```text
L_c_ready = LifecycleState(
  DECLARATION_NOT_REQUIRED,BINDING_NOT_REQUIRED,
  CAPABILITY_DISCOVERED,INVOCABLE_FOR(R_c))
L_c_final = LifecycleState(
  DECLARATION_NOT_REQUIRED,BINDING_NOT_REQUIRED,
  CAPABILITY_DISCOVERED,COMPLETED(Y_c))
K_c = (WELL_FORMED,CLOSED,EVALUABILITY_AVAILABLE,
       LIFECYCLE_RECORD((J_c,IDENTITY_OF(R_c)))->L_c_final,
       OBSERVATION_ENVIRONMENT_RECORD(IDENTITY_OF(M_c))->M_c,
       RESULT_RECORD((IDENTITY_OF(R_c),ReasoningResult,
                      IDENTITY_OF(Y_c)))->Y_c,
       CONSISTENCY_UNKNOWN)
```

`L_c_ready -> L_c_final` is one ordered state transition.  `L_c_final` has
exactly one `InvocationState`, `COMPLETED(Y_c)`; it does not retain
`INVOCABLE_FOR(R_c)`.  Thus both orders have the identical complete map,
result, final lifecycle, and `K_c`.  Adding `N_o -> N_d` still permits only
`O_1`; adding
both `N_o -> N_d` and `N_d -> N_o`, or a self-edge, is `MALFORMED`.  This DAG
is independent of direct, empty-support `task_accepts`.

```text
U_CONFLUENCE_FORWARD=ROW(CONFLUENCE_FORWARD;
  ABI0,PKG_CK,N_o,N_d,V_o,V_d,O_1,M_c,R_c,Y_c,L_c_final,K_c)
U_CONFLUENCE_REVERSE=ROW(CONFLUENCE_REVERSE;
  ABI0,PKG_CK,N_o,N_d,V_o,V_d,O_2,M_c,R_c,Y_c,L_c_final,K_c)
```

These are distinct packet universes with the same exact derived output
`(M_c,Y_c,K_c)`; the two orders are not co-composed.

The package-order fixture is a separate finite literal construction.  Fix

```text
P_pi1=((capknow.fixture,permutation-one),(1))
P_pi2=((capknow.fixture,permutation-two),(1))
T_pi11=(P_pi1,coding.fixture,fixture_unit_one,TYPE)
T_pi12=(P_pi1,coding.fixture,fixture_unit_two,TYPE)
T_pi21=(P_pi2,coding.fixture,fixture_unit_three,TYPE)
T_pi22=(P_pi2,coding.fixture,fixture_unit_four,TYPE)
```

For `ij in {11,12,21,22}`, `A_piij` is the complete
`ContractSpec[Delta]` whose key is
`(owner(T_piij),coding.fixture.type-admission,local(T_piij),(1),TYPE_ADMISSION)`,
owner layer and role are `Delta/TYPE_ADMISSION`, primary domain is the exact
sort `Value`, codomain is the abstract membership sort
`{admitted,not_admitted}`, observation-query map and support are `{}`, and
logical relation returns `admitted` exactly on `UNIT_piij` and `not_admitted`
on every unequal supplied `v`.  `ValueAdmissionResult` is constructed only by
the K2 value-admission request/result wrapper around this relation; it is not
the codomain of a `ContractSpec`.  Define the four
complete declarations

```text
D_piij = TypeDeclaration(
  key=T_piij,admitted_value_domain=A_piij,
  proper_declaration_dependencies={CONTRACT_SPEC(A_piij.contract_key)})
```

and the two literal packages (every omitted-looking field is displayed):

```text
PKG_pi1 = PluginPackage(
  abi_version=ABI0,plugin_key=P_pi1,
  declarations={D_pi11,D_pi12},pair_declarations={},bindings={},
  pair_bindings={},profile_bindings={},model_contracts={},aliases={},
  services={},certificates={},authority_facts={},compatibility_claims={},
  migrations={},semantic_extensions={},diagnostics=NONE)
PKG_pi2 = PluginPackage(
  abi_version=ABI0,plugin_key=P_pi2,
  declarations={D_pi21,D_pi22},pair_declarations={},bindings={},
  pair_bindings={},profile_bindings={},model_contracts={},aliases={},
  services={},certificates={},authority_facts={},compatibility_claims={},
  migrations={},semantic_extensions={},diagnostics=NONE)
G_pi={PKG_pi1,PKG_pi2}
R_pi1={ABI_RECORD(ABI0),PACKAGE_RECORD(ABI0,P_pi1),
       DECLARATION_RECORD(T_pi11),DECLARATION_RECORD(T_pi12),
       CONTRACT_SPEC_RECORD(A_pi11.contract_key),
       CONTRACT_SPEC_RECORD(A_pi12.contract_key)}
R_pi2={ABI_RECORD(ABI0),PACKAGE_RECORD(ABI0,P_pi2),
       DECLARATION_RECORD(T_pi21),DECLARATION_RECORD(T_pi22),
       CONTRACT_SPEC_RECORD(A_pi21.contract_key),
       CONTRACT_SPEC_RECORD(A_pi22.contract_key)}
```

The only two package presentations and their two literal per-package record
presentations are

```text
Pi_pkg_1=[ABI0,PKG_pi1,PKG_pi2]
Pi_pkg_2=[ABI0,PKG_pi2,PKG_pi1]
Pi_rec_1(PKG_pi1)=[ABI0,PKG_pi1,D_pi11,A_pi11,D_pi12,A_pi12]
Pi_rec_2(PKG_pi1)=[ABI0,A_pi12,D_pi12,A_pi11,D_pi11,PKG_pi1]
Pi_rec_1(PKG_pi2)=[ABI0,PKG_pi2,D_pi21,A_pi21,D_pi22,A_pi22]
Pi_rec_2(PKG_pi2)=[ABI0,A_pi22,D_pi22,A_pi21,D_pi21,PKG_pi2]
```

There is no implicit constructor ordering or unlisted record.  Define the
only composition operator for this fixture by

```text
COMPOSE_PI(pkg_order,record_order)=K2_COMPOSE(
  the selected complete Pi_pkg sequence,
  the selected complete Pi_rec sequence for PKG_pi1,
  the same selected complete Pi_rec sequence for PKG_pi2)
selected Pi_pkg sequence=Pi_pkg_1 iff pkg_order=PI1_PI2,
                         otherwise Pi_pkg_2
selected Pi_rec sequence=Pi_rec_1 iff
  record_order=DECLARATION_THEN_SPEC, otherwise Pi_rec_2
PI_EXPECTED=(
  abi_record=ABI_RECORD(ABI0),
  packages=G_pi,
  record_identities=(R_pi1 union R_pi2),
  declarations={T_pi11->D_pi11,T_pi12->D_pi12,
                T_pi21->D_pi21,T_pi22->D_pi22},
  contract_specs={A_pi11.contract_key->A_pi11,
                  A_pi12.contract_key->A_pi12,
                  A_pi21.contract_key->A_pi21,
                  A_pi22.contract_key->A_pi22},
  formation=WELL_FORMED,closure=CLOSED)
U_PI_PI1_PI2_DECLARATION_THEN_SPEC=
  COMPOSE_PI(PI1_PI2,DECLARATION_THEN_SPEC)
U_PI_PI1_PI2_SPEC_THEN_DECLARATION=
  COMPOSE_PI(PI1_PI2,SPEC_THEN_DECLARATION)
U_PI_PI2_PI1_DECLARATION_THEN_SPEC=
  COMPOSE_PI(PI2_PI1,DECLARATION_THEN_SPEC)
U_PI_PI2_PI1_SPEC_THEN_DECLARATION=
  COMPOSE_PI(PI2_PI1,SPEC_THEN_DECLARATION)
```

Each of these four separately tagged universes contains one explicit `ABI0`,
the two literal package records, the four literal declarations, and the four
literal admission ContractSpecs.  All four outcomes are exactly
`PI_EXPECTED`; in particular each includes exactly `ABI_RECORD(ABI0)` and the
same complete package/member record set.  Separately, `O_1/O_2` yield exactly
`(M_c,Y_c,K_c)`.

Finally, let `d` be the complete `PredicateDeclaration(DP(task_accepts))`
member of `PKG_CK`, and let `d'` be an independently constructed complete
field-for-field equal copy.  Let `d_bad` have that same key but the unequal
two-argument signature omitting `EvidenceStore`; all of its remaining fields
are those of `d`.  Each duplicate presentation is embedded in the complete,
dependency-closed owner/package-valid universe used by
`U_CORE_DEFINITIONAL`: it includes `ABI0`, `PKG_CK`, its retained owner,
certificate, validator, authority, model, declaration, binding, and service
packages, plus `C_b,C_c,C_w,C_choice,E_b,E_c,E_w,E_choice`.  Thus the only
difference between the equal and conflict presentations is equality versus
inequality of the one exact declaration identity, rather than a missing
owner, package member, type declaration, admission contract, or dependency.

```text
DUPLICATE_CLOSED_TAIL=[PKG_AWK,PKG_RVK,PKG_APK,PKG_ATK,PKG_AVK,
  C_b,C_c,C_w,C_choice,E_b,E_c,E_w,E_choice]
DUPLICATE_BASE=K2_COMPOSE([ABI0,PKG_CK] ++ DUPLICATE_CLOSED_TAIL)
U_DUPLICATE_EQUAL_FORWARD=K2_COMPOSE(
  [ABI0,PKG_CK,d'] ++ DUPLICATE_CLOSED_TAIL)
U_DUPLICATE_EQUAL_REVERSE=K2_COMPOSE(
  [ABI0,d',PKG_CK] ++ DUPLICATE_CLOSED_TAIL)
U_DUPLICATE_CONFLICT_FORWARD=K2_COMPOSE(
  [ABI0,PKG_CK,d_bad] ++ DUPLICATE_CLOSED_TAIL)
U_DUPLICATE_CONFLICT_REVERSE=K2_COMPOSE(
  [ABI0,d_bad,PKG_CK] ++ DUPLICATE_CLOSED_TAIL)
EXPECTED_DUPLICATE_EQUAL=(
  authoritative_map=A(DUPLICATE_BASE),
  formation=WELL_FORMED,closure=CLOSED)
EXPECTED_DUPLICATE_CONFLICT=(
  authoritative_map=(A(DUPLICATE_BASE) minus
    {DECLARATION_RECORD(DP(task_accepts))->d}) union
    {CONFLICT_RECORD(conflict0)->conflict0},
  formation=MALFORMED,closure=NOT_APPLICABLE)
A(U_DUPLICATE_EQUAL_FORWARD)=A(U_DUPLICATE_EQUAL_REVERSE)=
  EXPECTED_DUPLICATE_EQUAL.authoritative_map
A(U_DUPLICATE_CONFLICT_FORWARD)=A(U_DUPLICATE_CONFLICT_REVERSE)=
  EXPECTED_DUPLICATE_CONFLICT.authoritative_map
```

The first two packet entries both yield exactly `EXPECTED_DUPLICATE_EQUAL`;
the last two both yield exactly `EXPECTED_DUPLICATE_CONFLICT`.  No entry is
unioned with another presentation.

### 9.6 Mapping of all thirteen checks

Check 12 replays packet entries independently.  Its exact expected-output map
has the same finite domain as `FIXTURE_PACKET_X`:

```text
FIXTURE_EXPECTED_X={
  CORE_DEFINITIONAL ->
    (A(U_CORE_DEFINITIONAL),WELL_FORMED,CLOSED),
  PAIR_INDEPENDENT ->
    (A(U_PAIR_INDEPENDENT),WELL_FORMED,CLOSED,
     PAIR_COHERENCE_ADMITTED(PAIR(refresh),PCERT) : PairValidationResult),
  TRUST_BRANCH(ADMITTED) -> INVOCABLE_FOR(Q_t[T_admitted]),
  TRUST_BRANCH(ABSENT) -> EVALUABILITY_MISSING,
  TRUST_BRANCH(UNDECIDED) -> EVALUABILITY_UNKNOWN,
  TRUST_BRANCH(INCOMPATIBLE) -> EVALUABILITY_MISSING,
  TRUST_BRANCH(FAILED) -> DISCOVERY_FAILED,
  MISSING_BASE(k) ->
    (A(B_k),PRESENT(A(B_k)[i[k]])) for each displayed MissingRowId k,
  MISSING_VARIANT(k) ->
    (A(V_k),MISSING_EXPECTED[k]) for each displayed MissingRowId k,
  CONFLUENCE_ORDER(FORWARD) -> (M_c,Y_c,K_c),
  CONFLUENCE_ORDER(REVERSE) -> (M_c,Y_c,K_c),
  PERMUTATION(p,r) -> PI_EXPECTED for each of the four displayed pairs,
  DUPLICATE_EQUAL(FORWARD) -> EXPECTED_DUPLICATE_EQUAL,
  DUPLICATE_EQUAL(REVERSE) -> EXPECTED_DUPLICATE_EQUAL,
  DUPLICATE_CONFLICT(FORWARD) -> EXPECTED_DUPLICATE_CONFLICT,
  DUPLICATE_CONFLICT(REVERSE) -> EXPECTED_DUPLICATE_CONFLICT}

CHECK_12_REPLAY=id ->
  (K2_REPLAY(FIXTURE_PACKET_X[id]) = FIXTURE_EXPECTED_X[id])
  for each id in the exact finite domain of FIXTURE_PACKET_X
```

There is no replay of a union, catalog, alternative package, or another
entry's records.  The input tag, exact universe, and exact derived output are
one replay coordinate.

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
| 12 | each `FixtureId -> FixtureUniverse` entry in `FIXTURE_PACKET_X` paired with the same-tag exact `FIXTURE_EXPECTED_X` output; never a cross-entry union | K3S-A14 | K1 §4.8; K2 §§1.1,3.3,5.2: exact finite equality, deterministic meanings, set semantics, and source binding require the displayed per-tag replay equality, only after the later clean-commit gate |
| 13 | task predicate variant requesting ambient repository/evidence/expected-answer state | K3S-A05,A09,A17 | K1 §§1.2,2.2,3.1; K2 §§3.3,4.2,5.1: invalid observation/access is rejected before a truth can be used |

### 9.7 Intentionally excluded executable branches

The finite slice intentionally omits every literal value, request, target, and
capability not enumerated by one tagged universe in `FIXTURE_PACKET_X` and its
literal `L_X/FIXTURE_X/SERVICE_X` catalogs.  Catalog membership alone supplies
no universe record.  In particular the slice
omits general cross-plugin joint reasoning, public relation services,
evolution records beyond the four `Z` fixtures, authority facts beyond the
six `I_A` fixtures, certificate kinds/targets beyond the enumerated
pair/authority/evolution/bounds/witness records, and every K2 branch not
required by the thirteen checks.  It also omits byte
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
- [x] The section 9 tagged semantic packet covers all thirteen accepted
  executable checks with one exact universe and derived output per
  `FixtureId`, names the excluded branches, preserves both provenance gates,
  and freezes no implementation detail or authority.
- [x] Abstract satisfiability and profile coverage imply no patch, build,
  planner, executor, repository operation, or concrete implementation.
- [x] Conclusions remain limited to accepted-seed semantic representability.
  No held-out content, implementation, command/model execution, benchmark,
  external artifact, downstream handoff/path, or downstream authority appears.

No K3-S stop condition was encountered.  The exact K1 and K2 records suffice;
no frozen kernel or ABI rule is reinterpreted or repaired here.
