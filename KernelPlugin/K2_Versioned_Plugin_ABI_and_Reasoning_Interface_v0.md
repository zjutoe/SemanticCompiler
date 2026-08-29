# Contract IR versioned plugin ABI and reasoning interface v0

This specification operationalizes the accepted K1 calculus without changing
its denotation. Its conformance claim is limited to logical interface
coherence within the accepted K0/K1 scope.

## 1. Scope, conformance, and representation decision

### 1.1 Scope and exact representation decision

K2 v0 defines a **transport-neutral logical ABI**. Its abstract records,
disjoint unions, equality relations, validation rules, omissions, duplicates,
extensions, and lifecycle transitions are complete below. Finite sets are
mathematical sets; finite sequences are ordered; records compare field by
field; tagged variants of a disjoint union are never equal across tags.
The exact protocol identity is
`K2_ABI_V0 = (contract-ir.plugin.logical-abi, (0))`, where both components
are logical atoms, not an encoding.

K2 v0 deliberately defines no canonical byte encoding, field order, process
boundary, endpoint, loader, storage format, or network transport. It therefore
does **not** claim byte-level or process-level interoperability. Any later
representation must prove that it preserves this logical equality and keeps
malformed transport outside K1 truth and reasoning results.

There are no implicit fields, defaults, wildcard versions, null-as-absence
rules, or open records. A field marked optional below has exactly two logical
states, absent and present with a conforming value. Absence never selects a
default. Unless a collection is explicitly a sequence, order is irrelevant and
exact duplicates coalesce by logical equality. Two records with the same
identity and unequal non-diagnostic content conflict. An unrecognized field is
malformed; extensions exist only through the disjoint explicit semantic and
diagnostic extension records in section 8.

### 1.2 Conformance predicates

The following predicates are independent.

| Predicate | Required condition |
|---|---|
| `DECLARATION_CONFORMANT(d)` | `d` has a valid exact owner/key/kind, all declaration dependencies exist, every signature and facet position is well typed, every value-admission premise holds, and no declaration field contains meaning or service state. |
| `BINDING_CONFORMANT(b,Delta)` | `b` has the unique key derived from its exact declaration, matches that declaration, has every logical contract's exact derived trust-free denotational support and complete semantic closure, a deterministic typed meaning, explicit facet/evidence/access/unknown/error contracts, and no service field. |
| `SERVICE_CONFORMANT(s,Delta,Sigma)` | `s` names exact ABI/plugin/service/capability identities, a nonempty exact tagged target set, only conformant bindings, exact supported judgments/fragments/dependencies/nonempty required trust roots/failure behavior with derived support, and no declaration or meaning. Each ordinary use must pass the exact independently rooted service-use scope below. |
| `REQUEST_CONFORMANT(r,E,T)` | `r` is well typed, binds exact semantic environment `E` and trust environment `T`, names one exact tagged capability target and compatible capability, contains the complete derived dependency/support environment, validates role, judgment, target, fragments, roots and scopes together, supplies no forbidden context or alternate choice map, and lies in the claimed fragment when decisiveness is required. |
| `RESULT_CONFORMANT(x,r,E)` | For a denotational request, `x` has the valid carrier shape and equals the unique complete result derived from the exact bound logical relation under `r`'s admitted positional inputs and `E`; for an admission/reasoning request it satisfies its exact conclusion-receiving rule. A complete in-fragment request is decisive. |
| `CERTIFICATE_CONFORMANT(c,r)` | `c` binds the exact request, environment, capability, fragment, dependencies, conclusion, validator, independently admitted trust root, and abstraction class, and satisfies the certificate-kind admission rule in section 6. |
| `PACKAGE_CONFORMANT(p,E)` | Relative to composed typed environment `E` and its independently supplied trust environment, every required declaration reference resolves exactly; every present binding, model contract, service, certificate, authority fact, migration, compatibility claim, and semantic extension is individually conformant; diagnostic extensions are ignored; absent semantic/service references retain their open/missing states; duplicates coalesce or conflict by section 8; and the three ownership layers project uniquely. A package cannot contribute a trust root. |

A declaration-only package may be package-conformant while leaving a required
meaning open. A package with meanings but no compatible service may likewise
be conformant while the requested judgment is not evaluable. Whole-package
conformance never implies closure, service availability, truth, authority,
satisfiability, a relation, or profile completeness.

### 1.3 Fixed K1 boundary

The ABI carries K1's `Delta`, `Sigma`, and service/capability information
as different objects. It does not redefine any connective, `TermResult`,
`Eval`, T1--T4, A1--A2, authority tuple, `chi_C`, dependency extraction,
profile status, closure premise, or public relation. A predicate receives only
declared positional typed values. No request, result, certificate, model
contract, compatibility claim, or plugin may supply a challenge identity,
expected result, gold Contract, hidden target, implicit full `Outcome`,
undeclared evidence, or replacement `chi_C`.

K2 is a specification, not a registry, evaluator, reasoner, certificate
checker, compiler, planner, executor, prompt, model, deployment design, or
benchmark. It makes no adequacy, completeness, performance, discovery-quality,
or execution claim.

## 2. ABI object model and lifecycle

### 2.1 Local notation and exact logical roles

`Version` is a nonempty finite sequence of nonnegative integers. Equality is
componentwise, and lexicographic or numerical ordering has no semantic effect.
`Namespace`, `LocalId`, `KindTag`, and all identity atoms are exact,
case-sensitive abstract atoms. No display normalization exists.

The frozen K1 sorts are local ABI sorts:

```text
Value, Principal, ChoiceId, Variable, State, Trace, EvidenceStore
Facet = pre | trace | final | evidence
Truth = TRUE | FALSE | UNKNOWN
NormativeRole = REQUIRE | AUTHORIZE | BIND_CHOICE(ChoiceId)
Outcome = (PRE : State, TRACE : Trace,
           FINAL : State, EVIDENCE : EvidenceStore)
```

`ContractSpec` is a non-recursive exact logical contract. Its finite identity,
explicit primary-input domain, finite lower-level observation queries,
codomain, and mathematical relation are part of equality; it never consumes a
`SemanticEnvironment`, binding record, another `ContractSpec`, or another
logical relation. Section 3.3 gives the stratified type and its extensional
equality. Value-admission, meaning, coverage, evidence, access, unknown,
failure, fragment, and validation contracts below are typed `ContractSpec`
values owned by the layer that names them.

```text
AbiVersion        = (abi_namespace, exact_version)
PluginIdentity    = (owner_namespace, local_identity)
PluginKey         = (plugin_identity, exact_version)
DeclarationKey    = (plugin_key, declaration_namespace, local_name,
                     kind : TYPE | LITERAL | FUNCTION | PREDICATE | EVENT)
SymbolKey         = (plugin_key, symbol_namespace, local_name,
                     kind : FUNCTION | PREDICATE)
EventKey          = (plugin_key, event_namespace, local_name)
ProfileKey        = (plugin_key, profile_name)
EventScopePairKey = (plugin_key, pair_namespace, local_name)
BindingKey        = DeclarationKey
ServiceKey        = (plugin_key, service_namespace, local_name,
                     exact_service_version, service_role)
CapabilityKey     = (service_key : ServiceKey, capability_name)
CertificateIssuer =
    PLUGIN_CERTIFICATE_ISSUER(PluginKey)
  | EMBEDDING_POLICY_CERTIFICATE_ISSUER(TrustPolicyKey)
CertificateKey    = (issuer : CertificateIssuer, certificate_namespace,
                     local_identity)
MigrationKey      = (owner_plugin : PluginKey, migration_namespace,
                     local_identity,
                     exact_migration_version)
SemanticExtensionKey = (owner_plugin, extension_namespace, local_name,
                        exact_extension_version)
ProfileDimensionKey = (profile_key, dimension_name)
SemanticTargetIdentity =
    BINDING_IDENTITY(BindingKey)
  | PROFILE_IDENTITY(ProfileKey)
  | PAIR_IDENTITY(EventScopePairKey)
ModelContractKey    = (target_semantic_identity : SemanticTargetIdentity,
                       document_namespace,
                       locale_identity, exact_document_version)
AliasKey = (owner_plugin : PluginKey, alias_namespace, alias_atom)
CompatibilityClaimKey = (owner_plugin : PluginKey, claim_namespace,
                         local_identity,
                         exact_claim_version)
TrustPolicyKey = (embedding_policy_namespace, local_policy_identity,
                  exact_policy_version)
TrustRootKey = (trust_policy_key, root_namespace, local_root_identity,
                exact_root_version)
ProducerIdentity =
    PLUGIN_PRODUCER(PluginKey)
  | EMBEDDING_POLICY_PRODUCER(TrustPolicyKey)
  | ABI_PRODUCER(AbiVersion)
IssuerScope =
    PLUGIN_ISSUER(PluginKey)
  | EMBEDDING_POLICY_ISSUER(TrustPolicyKey)
  | ABI_ISSUER(AbiVersion)
ABI_REASON_ISSUER = ABI_ISSUER(K2_ABI_V0)
SemanticEnvironmentIdentity = IDENTITY_OF(all exact SemanticEnvironment fields)
TrustEnvironmentIdentity = IDENTITY_OF(
  trust_policy_key, policy_owner, exact root_judgments map)
AuthorityFactKey = (authority_ref : AuthorityRef, source_ref : SourceRef,
                    principal : Principal, normative_role : NormativeRole)
AuthorityFactCandidate = (
  authority_fact_key : AuthorityFactKey,
  admission_subject_data : exact finite typed attestation subject value,
  offered_evidence_refs : finset(EvidenceRef)
)
ContractIdentity = IDENTITY_OF(exact complete Contract logical record)
LexicalScopeIdentity = (judgment_or_binder_kind, exact subject tuple)
LexicalBindingKey = (scope_identity : LexicalScopeIdentity, variable : Variable,
                     declared_type : DeclarationKey[TYPE])
ChoiceBindingKey = (contract_identity : ContractIdentity,
                    choice_id : ChoiceId)
ContractSpecKey = (owner_plugin : PluginKey, contract_namespace, local_identity,
                   exact_contract_version, contract_role)
RequestIdentity = IDENTITY_OF(exact complete request record)
ResultIdentity = (request_identity : RequestIdentity, result_kind,
                  exact complete result logical identity)
CarrierRecordKind =
    ABI_VERSION | PLUGIN_PACKAGE | SEMANTIC_ENVIRONMENT
  | DEPENDENCY_OBSERVATION_ENVIRONMENT | DEPENDENCY_ENVIRONMENT
  | TRUST_ENVIRONMENT | LIFECYCLE | OUTCOME | EVENT_VALUE | TRACE_EVENT
  | SOURCE_REF | AUTHORITY_REF | EVIDENCE_REF | REASON | CONFLICT
K1SyntaxKey =
    K1_PLUGIN(PluginKey) | K1_DECLARATION(DeclarationKey)
  | K1_SYMBOL(SymbolKey) | K1_EVENT(EventKey) | K1_PROFILE(ProfileKey)
  | K1_PAIR(EventScopePairKey)
TrustTarget =
    PAIR_TRUST_TARGET(EventScopePairKey)
  | AUTHORITY_TRUST_TARGET(AuthorityFactKey)
  | MIGRATION_TRUST_TARGET(MigrationKey)
  | COMPATIBILITY_TRUST_TARGET(CompatibilityClaimKey)
  | SEMANTIC_EXTENSION_TRUST_TARGET(SemanticExtensionKey)
  | JUDGMENT_TRUST_TARGET(JudgmentTag, exact subject tuple)
  | SERVICE_USE_TRUST_TARGET(
      CapabilityKey, JudgmentTag, ServiceUseSubject,
      SemanticEnvironmentIdentity)
DependencyKey =
    ABI(AbiVersion) | PLUGIN(PluginKey) | DECLARATION(DeclarationKey)
  | SYMBOL(SymbolKey) | EVENT(EventKey) | PROFILE(ProfileKey)
  | PAIR(EventScopePairKey) | BINDING(BindingKey)
  | PAIR_DECLARATION(EventScopePairKey)
  | PAIR_BINDING(EventScopePairKey)
  | PROFILE_BINDING(ProfileKey)
  | SERVICE(ServiceKey) | CAPABILITY(CapabilityKey)
  | CERTIFICATE(CertificateKey) | MIGRATION(MigrationKey)
  | COMPATIBILITY_CLAIM(CompatibilityClaimKey)
  | MODEL_CONTRACT(ModelContractKey) | ALIAS(AliasKey)
  | AUTHORITY_FACT(AuthorityFactKey)
  | LEXICAL_BINDING(LexicalBindingKey)
  | CHOICE_BINDING(ChoiceBindingKey)
  | TRUST_POLICY(TrustPolicyKey)
  | TRUST_ROOT(TrustRootKey)
  | SEMANTIC_EXTENSION(SemanticExtensionKey)
  | CONTRACT_SPEC(ContractSpecKey)
  | REQUEST(RequestIdentity) | RESULT(ResultIdentity)
  | CARRIER(CarrierRecordKind, exact finite logical identity)

ValidationReference =
    VALIDATION_CERTIFICATE(CertificateKey)
  | VALIDATION_CAPABILITY(CapabilityKey)
  | VALIDATION_TRUST_ROOT(TrustRootKey)

ContractRole =
    TYPE_ADMISSION
  | LITERAL_MEANING | FUNCTION_MEANING | PREDICATE_MEANING
  | OCCURRENCE_MEANING | PROFILE_COVERAGE
  | EVIDENCE_SCHEMA | ACCESS_BOUNDARY | UNKNOWN_BEHAVIOR
  | EVALUATION_ERROR_BEHAVIOR | REASONING_ERROR_BEHAVIOR
  | SOUND_FRAGMENT | COMPLETE_FRAGMENT | REQUIRED_EVIDENCE
  | SERVICE_FAILURE_BEHAVIOR | COMPATIBILITY_VALIDATION
  | MIGRATION_RELATION | SEMANTIC_EXTENSION_EFFECT
  | SEMANTIC_EXTENSION_PAYLOAD

DependencyObservationKind =
    IDENTITY_PRESENCE | DECLARATION_SHAPE | TYPE_ADMISSION_FACT
  | VALUE_RESULT | TERM_RESULT | EVAL_RESULT | EVAL_RESULT_SEQUENCE
  | PROFILE_RESULT
  | PAIR_RESULT | MIGRATION_STATUS
  | COMPATIBILITY_STATUS | SEMANTIC_EXTENSION_STATUS
  | CERTIFICATE_STATUS

ObservationInput = exactly one finite typed projection of K1 `Value`,
                   `TermResult`, `Eval`, profile/admission subject value, or
                   finite tuple/sequence thereof suitable for its
                   DependencyObservationKind; never a ContractSpec, relation,
                   binding, SemanticEnvironment, or trust record
DependencyObservationQuery = (
  expected_kind : DependencyObservationKind,
  input_projection : exact extensional function from the ContractSpec's
                     explicit primary input to ObservationInput
)
DependencyObservationValue =
    IDENTITY_PRESENT(exact key identity)
  | DECLARATION_OBS(exact signature/type/facet/event-class logical value)
  | TYPE_ADMISSION_OBS(VALUE_ADMITTED | VALUE_NOT_ADMITTED)
  | VALUE_OBS(Value) | TERM_OBS(TermResult) | EVAL_OBS(Eval)
  | EVAL_SEQUENCE_OBS(finite sequence(Eval))
  | PROFILE_OBS(ProfileResult) | PAIR_OBS(PairValidationResult)
  | MIGRATION_OBS(ADMITTED | NOT_ADMITTED)
  | COMPATIBILITY_OBS(ADMITTED | NOT_ADMITTED)
  | SEMANTIC_EXTENSION_OBS(ADMITTED | NOT_ADMITTED)
  | CERTIFICATE_OBS(ADMITTED | REJECTED_NONDECISIVE)
  | LOWER_EVALUATION_ERROR(nonempty finset(EvaluationErrorReason))
  | LOWER_REASONING_ERROR(nonempty finset(ReasoningErrorReason))

DependencyObservationEnvironment = finite exact map
  DependencyKey -> DependencyObservationValue

ContractSpec[owner_layer] = (
  contract_key : ContractSpecKey,
  owner_layer : Delta | Sigma | Service,
  contract_role : ContractRole,
  primary_input_domain : exact typed domain identity containing only K1 values,
                         results, or finite typed subject tuples and never a
                         ContractSpec, relation, binding, SemanticEnvironment,
                         DependencyObservationEnvironment, or trust record,
  codomain : exact typed K1 value/result/status codomain identity, never a
             ContractSpec, relation, binding, SemanticEnvironment,
             DependencyObservationEnvironment, or trust record,
  observation_queries : finite exact map
    DependencyKey -> DependencyObservationQuery,
  logical_relation : exact extensional mathematical relation from
    (primary_input, DependencyObservationEnvironment) to codomain
)

CapabilityTarget =
    BINDING_TARGET(BindingKey)
  | TYPE_ADMISSION_TARGET(DeclarationKey[TYPE], SemanticEnvironmentIdentity)
  | PROFILE_TARGET(ProfileKey)
  | PAIR_TARGET(EventScopePairKey)
  | ENVIRONMENT_JUDGMENT_TARGET(
      judgment : JudgmentTag,
      subjects : exact judgment-specific subject tuple,
      environment_identity : SemanticEnvironmentIdentity)

ServiceUseSubject =
    BINDING_USE(BindingKey)
  | TYPE_ADMISSION_USE(DeclarationKey[TYPE])
  | PROFILE_USE(ProfileKey)
  | PAIR_USE(EventScopePairKey)
  | ENVIRONMENT_USE(JudgmentTag, exact judgment-specific subject tuple)
```

The five `CapabilityTarget` tags and five `ServiceUseSubject` tags are
disjoint. Their payloads compare by exact logical equality, including exact
versions, subject order where the judgment is ordered, and the derived
`SemanticEnvironmentIdentity`. A binding target carries one exact
semantic-bearing binding identity; function/predicate services use the matching
binding target, while literals resolve directly from their binding and have no
v0 service role. A type-admission target is the sole target for invoked value
admission; profile and pair targets are likewise kind-specific. The
environment/judgment tag is the sole target for consistency, logical
relations, internal `==Eval`, authority, migration, compatibility, semantic
extension, and other whole-environment admission. A type-admission target
includes its complete exact environment identity, and the request separately
binds the full environment; no binding-only or context-free type
target can stand for one of these kinds. `semanticIdentity(E)` is the exact
logical identity above: equality is equality of every displayed
`SemanticEnvironment` field, including every non-recursive `ContractSpec` and
all derived dependency and choice fields. It is a finite exact logical
identity, not a digest, encoding, computability claim, or semantic-validity
proof. Trust is not a field of `SemanticEnvironment`; the full `E` and the
separate exact `TrustEnvironment` are request fields. Consequently neither a
`CapabilityTarget` nor a `TrustTarget` recursively contains the trust map that
contains it.

`trustEnvironmentIdentity(T)` is exactly
`TrustEnvironmentIdentity(T.trust_policy_key,T.policy_owner,
T.root_judgments)`. Equality is component equality of the exact-versioned
policy key and structurally fixed owner plus finite-map equality of the exact
`TrustRootKey` domain and complete `TrustRootJudgment` value at every key.
Every non-admitted value uses only the closed root-local
`TrustRootStatusReason` algebra below; no judgment payload contains a request,
result, failure, or environment carrier. It is therefore a finite,
non-recursive exact logical identity, not a byte identity, digest, encoding,
computability claim, or trust-validity proof.

`BindingKey` is derived, not independently selected: the sole semantic
binding for a semantic-bearing declaration has exactly that
`DeclarationKey`. A different meaning requires a different exact plugin
version and hence a different declaration and binding key. There is never more
than one meaning for one exact declaration in a composed environment.

The logical record roles are:

| Role | Exact record |
|---|---|
| protocol/package | `AbiVersion`, `PluginPackage` |
| identities | the key records above, `EvidenceRef`, reason identities including `TrustRootStatusReason`, `SourceRef`, `AuthorityRef`, `AuthorityFactKey`, `TrustRootKey`, derived `ContractIdentity`/`SemanticEnvironmentIdentity`/`TrustEnvironmentIdentity`/`LexicalScopeIdentity`, `LexicalBindingKey`, `ChoiceBindingKey`, `ProfileDimensionKey` |
| declarations | `TypeDeclaration`, `LiteralDeclaration`, `FunctionDeclaration`, `PredicateDeclaration`, `EventDeclaration`, `EventScopePairDeclaration` |
| meanings | `SemanticBinding`, `EventPairBinding`, `ProfileBinding`, `ModelContract`, `ModelCapabilitySummary`, `AliasBinding`, `AuthorityFactBinding` |
| services | derived `ServiceIdentityRecord`, `CapabilityDescriptor` |
| environment/targets | `SemanticEnvironment`, `DependencyObservationEnvironment`, `DependencyEnvironment`, `TrustEnvironment`, `Subject`, `RecordIdentity`, `ValidationReference`, `CapabilityTarget`, `TrustTarget`, `ServiceUseSubject`, `LexicalBinding`, `ChoiceBindingEntry` |
| requests | `ValueAdmissionRequest`, `FunctionRequest`, `PredicateRequest`, `ProfileRequest`, `PairAdmissionRequest`, `AuthorityAdmissionRequest`, `MigrationAdmissionRequest`, `CompatibilityAdmissionRequest`, `SemanticExtensionAdmissionRequest`, `DiscoveryRequest`, `ReasoningRequest`, derived `CertificateValidationRequest` |
| results | `ValueAdmissionResult`, `TermResult`, `Eval`, derived `FormulaResult`, `ProfileResult`, `PairValidationResult`, `AuthorityAdmissionResult`, `MigrationAdmissionResult`, `CompatibilityAdmissionResult`, `SemanticExtensionAdmissionResult`, `DiscoveryResult`, `ReasoningResult`, `InterfaceFailure` |
| evidence | `CertificateEnvelope`, `CertificateAdmission`, `TrustRootRecord`, `TrustRootJudgment` |
| logical contracts | `ContractSpec` |
| events/provenance | `EventValue`, `TraceEvent`, `SourceRef`, `AuthorityRef`, `AuthorityFactCandidate`, `AuthorityFactBinding` |
| evolution | `CompatibilityClaim`, `MigrationDeclaration`, `SemanticExtension`, `DiagnosticExtension`, `Diagnostics` |

### 2.2 Unique ownership layers

| Owner layer | Owns | Cannot own |
|---|---|---|
| `Delta` declaration | exact identity; type/value admission; literal, function, predicate, and event signatures; facet positions; immutable event class; pair membership/signatures/controlled keys; declaration dependencies | denotation, evidence schema, unknown/error behavior, profile meaning, service availability |
| `Sigma` semantic binding | exact literal/function/predicate meaning; semantic dependencies; evidence/access/unknown/error contracts; event-pair coherence; profile dimensions and coverage meaning; model contract; authority fact | evaluator/reasoner discovery, availability, or capability |
| Service/capability | invocable service identity; supported judgments; sound/complete fragments; full dependency scope; required evidence; exact required trust-root keys; failure contract | declaration, type admission, denotation, profile meaning, authority meaning or trust-root admission |

K1-owned carrier fields such as `Eval` tags do not become plugin-owned. Every
request/result field is validated against exactly one owner above or against a
fixed K1 carrier rule. Combining records in a later representation is
conformant only when projection recovers these owners uniquely.

### 2.3 Record shapes

```text
PluginPackage = (
  abi_version, plugin_key,
  declarations : finset(Declaration),
  pair_declarations : finset(EventScopePairDeclaration),
  bindings : finset(SemanticBinding),
  pair_bindings : finset(EventPairBinding),
  profile_bindings : finset(ProfileBinding),
  model_contracts : finset(ModelContract),
  aliases : finset(AliasBinding),
  services : finset(CapabilityDescriptor),
  certificates : finset(CertificateEnvelope),
  authority_facts : finset(AuthorityFactBinding),
  compatibility_claims : finset(CompatibilityClaim),
  migrations : finset(MigrationDeclaration),
  semantic_extensions : finset(SemanticExtension),
  diagnostics : Diagnostics?
)

Declaration =
    TypeDeclaration | LiteralDeclaration | FunctionDeclaration
  | PredicateDeclaration | EventDeclaration

TypeDeclaration = (
  key : DeclarationKey[TYPE],
  admitted_value_domain : ContractSpec[Delta],
  proper_declaration_dependencies : finset(DependencyKey)
)
LiteralDeclaration = (
  key : DeclarationKey[LITERAL], literal_identity,
  result_type : DeclarationKey[TYPE],
  proper_declaration_dependencies : finset(DependencyKey)
)
FunctionDeclaration = (
  key : DeclarationKey[FUNCTION], symbol_key : SymbolKey[FUNCTION],
  argument_types : sequence(DeclarationKey[TYPE]),
  result_type : DeclarationKey[TYPE],
  facet_positions : sequence(finset(Facet)),
  proper_declaration_dependencies : finset(DependencyKey)
)
PredicateDeclaration = (
  key : DeclarationKey[PREDICATE], symbol_key : SymbolKey[PREDICATE],
  argument_types : sequence(DeclarationKey[TYPE]),
  result_kind : BOOL,
  facet_positions : sequence(finset(Facet)),
  proper_declaration_dependencies : finset(DependencyKey)
)
EventDeclaration = (
  key : DeclarationKey[EVENT], event_key : EventKey,
  payload_type : DeclarationKey[TYPE],
  event_class : CONTROLLED | OBSERVATIONAL,
  proper_declaration_dependencies : finset(DependencyKey)
)
EventScopePairDeclaration = (
  pair_key : EventScopePairKey,
  scope_symbol : SymbolKey[PREDICATE],
  occurrence_symbol : SymbolKey[PREDICATE],
  controlled_keys : nonempty finset(EventKey),
  proper_declaration_dependencies : finset(DependencyKey)
)
```

The two pair member signatures and facet positions are derived and must be
exactly `(EventValue)->Bool` with no outcome-facet position for
`scope_symbol`, and `(Trace)->Bool` with exactly `{trace}` for the sole
position of `occurrence_symbol`. Both members are distinct, are owned by the
pair's exact `PluginKey`, and every controlled key has an exact
`CONTROLLED` event declaration.

```text
SemanticBinding = (
  binding_key : BindingKey,
  declaration_key : DeclarationKey[LITERAL|FUNCTION|PREDICATE],
  binding_kind : LITERAL | FUNCTION | PREDICATE,
  meaning_contract : ContractSpec[Sigma],
  permitted_facet_inputs : sequence(finset(Facet)),
  proper_semantic_dependencies : finset(DependencyKey),
  dependency_closure : finset(DependencyKey),
  evidence_schema : ContractSpec[Sigma],
  access_boundary : ContractSpec[Sigma],
  unknown_contract : ContractSpec[Sigma],
  evaluation_error_contract : ContractSpec[Sigma],
  determinism_rule : SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT
)

EventPairBinding = (
  pair_key : EventScopePairKey,
  scope_binding_key : BindingKey,
  occurrence_binding_key : BindingKey,
  occurrence_model_contract_key : ModelContractKey,
  admission :
    DEFINITIONAL_T3_A1
  | INDEPENDENT_COHERENCE_PROOF(
        occurrence_contract_bundle : OccurrenceSemanticContractBundle,
        certificate_key : CertificateKey,
        validator_key : CapabilityKey),
  proper_semantic_dependencies : finset(DependencyKey),
  dependency_closure : finset(DependencyKey)
)

OccurrenceSemanticContractBundle = (
  meaning_contract : ContractSpec[Sigma],
  permitted_facet_inputs : sequence(finset(Facet)),
  evidence_schema : ContractSpec[Sigma],
  access_boundary : ContractSpec[Sigma],
  unknown_contract : ContractSpec[Sigma],
  evaluation_error_contract : ContractSpec[Sigma],
  determinism_rule : SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT,
  proper_semantic_dependencies : finset(DependencyKey),
  dependency_closure : finset(DependencyKey)
)

ProfileBinding = (
  profile_key : ProfileKey,
  dimensions : finset(ProfileDimensionKey),
  coverage_meaning : ContractSpec[Sigma],
  evidence_schema : ContractSpec[Sigma],
  proper_semantic_dependencies : finset(DependencyKey),
  dependency_closure : finset(DependencyKey),
  unknown_contract : ContractSpec[Sigma],
  evaluation_error_contract : ContractSpec[Sigma],
  reasoning_error_contract : ContractSpec[Sigma]
)

ServiceRole = VALUE_ADMISSION | FUNCTION_EVALUATION |
              PREDICATE_EVALUATION | PROFILE_CONCRETE |
              PROFILE_SYMBOLIC | REASONING | PAIR_VALIDATION |
              AUTHORITY_VALIDATION | MIGRATION_VALIDATION |
              COMPATIBILITY_VALIDATION |
              SEMANTIC_EXTENSION_VALIDATION

ModelCapabilitySummary = (
  capability_key : CapabilityKey,
  service_role : ServiceRole,
  supported_judgments : nonempty finset(JudgmentTag),
  capability_class : CONCRETE_EVALUATION_ONLY |
                     PARTIAL_SYMBOLIC_REASONING |
                     COMPLETE_FOR_DECLARED_FRAGMENT,
  sound_fragment_key : ContractSpecKey,
  complete_fragment_key : ContractSpecKey?,
  dependency_scope : finset(DependencyKey)
)
ModelContract = (
  model_contract_key : ModelContractKey,
  target_binding_key : BindingKey,
  exact_symbol_key : SymbolKey | NO_SYMBOL_LITERAL,
  exact_signature : exact ordered function signature,
  exact_facet_positions : sequence(finset(Facet)),
  evidence_contract : ContractSpec[Sigma],
  unknown_contract : ContractSpec[Sigma],
  error_contract : ContractSpec[Sigma],
  capability_summaries : finset(ModelCapabilitySummary),
  semantic_contract_reference : ContractSpecKey,
  explanatory_text?
)
AliasBinding = (
  alias_key : AliasKey, exact_target_key,
  target_kind, target_exact_version
)
ServiceIdentityRecord = (
  service_key : ServiceKey,
  abi_version : AbiVersion,
  plugin_key : PluginKey
)
CapabilityDescriptor = (
  capability_key, abi_version, plugin_key,
  service_role : ServiceRole,
  capability_class : CONCRETE_EVALUATION_ONLY |
                     PARTIAL_SYMBOLIC_REASONING |
                     COMPLETE_FOR_DECLARED_FRAGMENT,
  supported_judgments : nonempty finset(JudgmentTag),
  supported_targets : nonempty finset(CapabilityTarget),
  sound_fragment : ContractSpec[Service],
  complete_fragment : ContractSpec[Service]?,
  dependency_scope : finset(DependencyKey),
  proper_semantic_dependencies : finset(DependencyKey),
  dependency_closure : finset(DependencyKey),
  required_evidence : ContractSpec[Service],
  required_trust_roots : nonempty finset(TrustRootKey),
  failure_contract : ContractSpec[Service]
)

JudgmentTag =
    VALUE_ADMISSION | FUNCTION_EVALUATION | PREDICATE_EVALUATION
  | PROFILE_COVERAGE | CONSISTENCY
  | FORMULA_ENTAILMENT | FORMULA_EQUIVALENCE
  | ACCEPTANCE_ENTAILMENT | ACCEPTANCE_EQUIVALENCE
  | FULL_CONTRACT_EQUIVALENCE
  | EVAL_FUNCTION_EQUALITY_DERIVATION
  | EVENT_PAIR_COHERENCE_ADMISSION
  | AUTHORITY_FACT_ADMISSION
  | MIGRATION_RELATION_ADMISSION
  | COMPATIBILITY_CLAIM_ADMISSION
  | SEMANTIC_EXTENSION_ADMISSION

SemanticEnvironment = (
  abi_version : AbiVersion,
  declarations : finset(Declaration),
  pair_declarations : finset(EventScopePairDeclaration),
  bindings : finset(SemanticBinding),
  pair_bindings : finset(EventPairBinding),
  profile_bindings : finset(ProfileBinding),
  authority_facts : finite map AuthorityFactKey -> AuthorityFactBinding,
  semantic_extensions : finset(SemanticExtension),
  lexical_bindings : finite map LexicalBindingKey -> LexicalBinding,
  choice_bindings : finite map ChoiceBindingKey -> ChoiceBindingEntry,
  mechanically_extracted_dependencies : finset(K1SyntaxKey),
  chi_C : finite map ChoiceId -> Value
)
DependencyEnvironment = (
  syntax_root_keys : finset(K1SyntaxKey),
  subject_root_keys : finset(DependencyKey),
  binding_association_edges : finset(DependencyKey * DependencyKey),
  expanded_root_keys : finset(DependencyKey),
  proper_dependencies : finset(DependencyKey),
  transitive_dependency_closure : finset(DependencyKey),
  validation_references : finset(ValidationReference)
)
LexicalBinding = (
  lexical_binding_key : LexicalBindingKey,
  admitted_value : Value
)
ChoiceBindingEntry = (
  choice_binding_key : ChoiceBindingKey,
  declared_type : DeclarationKey[TYPE],
  admitted_value : Value,
  controller : Principal,
  source_ref : SourceRef,
  authority_fact_key : AuthorityFactKey
)
TrustRootRecord = (
  trust_root_key : TrustRootKey,
  owner : EMBEDDING_POLICY_PRODUCER(trust_root_key.trust_policy_key),
  trusted_validators : nonempty finset(CapabilityKey),
  permitted_certificate_kinds : nonempty finset(CertificateKind),
  permitted_targets : nonempty finset(TrustTarget),
  adoption : V0_EXTERNAL_TRUST_PREMISE
)
TrustPolicyRecord = (
  trust_policy_key : TrustPolicyKey,
  owner : EMBEDDING_POLICY_PRODUCER(trust_policy_key)
)
TrustRootStatusReasonCode =
    ROOT_DISCOVERY_UNRESOLVED
  | ROOT_DISCOVERY_PROTOCOL_FAILURE
  | ROOT_DISCOVERY_TRANSPORT_FAILURE
  | ROOT_RECORD_CONFLICT
  | ROOT_POLICY_KEY_MISMATCH
  | ROOT_POLICY_OWNER_MISMATCH
  | ROOT_RECORD_OWNER_MISMATCH
  | ROOT_ADOPTION_MISMATCH
  | ROOT_VALIDATOR_NOT_PERMITTED
  | ROOT_CERTIFICATE_KIND_NOT_PERMITTED
  | ROOT_TARGET_NOT_PERMITTED
TrustRootStatusReason = (
  issuer_scope : exactly ABI_REASON_ISSUER,
  status_code : TrustRootStatusReasonCode,
  trust_policy_key : TrustPolicyKey,
  trust_root_key : TrustRootKey,
  implicated_capability : CapabilityKey | NO_CAPABILITY
)
TrustRootJudgment =
    TRUST_ROOT_ADMITTED(TrustRootRecord)
  | TRUST_ROOT_ABSENT(TrustRootKey)
  | TRUST_ROOT_UNDECIDED(
      TrustRootKey, nonempty finset(TrustRootStatusReason))
  | TRUST_ROOT_FAILED(
      TrustRootKey, nonempty finset(TrustRootStatusReason))
  | TRUST_ROOT_INCOMPATIBLE(
      TrustRootKey, nonempty finset(TrustRootStatusReason))
TrustEnvironment = (
  trust_policy_key : TrustPolicyKey,
  policy_owner : EMBEDDING_POLICY_PRODUCER(trust_policy_key),
  root_judgments : finite map TrustRootKey -> TrustRootJudgment
)
Diagnostics = (
  display_label : finset(diagnostic atom),
  narrative : finset(diagnostic atom),
  timing : finset(diagnostic atom),
  endpoint_hint : finset(diagnostic atom),
  retry_note : finset(diagnostic atom),
  correlation_atom : finset(diagnostic atom),
  extensions : finset(DiagnosticExtension)
)
DiagnosticExtension = (
  grouping_identity : diagnostic atom?,
  payload : diagnostic logical value
)
```

Every collection in `SemanticEnvironment` has the displayed exact type.
`finset` equality is member equality with duplicate coalescing and no order.
Finite-map equality is equality of key domain and value at every key; two
unequal values for one map key conflict. `Declaration` and pair-declaration
collections are Delta, binding/profile/pair/authority/extension collections
are Sigma, and there is no ambiguous generic `pairs` collection.
`lexical_bindings` carries only admitted explicit request-scope entries.
`choice_bindings` carries the validated Contract records from which `chi_C`
is derived; the map domains and every derived value must agree exactly.
`mechanically_extracted_dependencies` is exactly the unchanged K1
`required(subject)` syntax-root set. It never contains the K2 association/
expansion as a replacement facet; `DependencyEnvironment` retains that syntax
set separately, adds the derived binding reachability alongside it, and
carries mandatory validation references in a third non-proper projection.
`authority_facts` contains only admitted, key-grouped bindings with their
nonempty unioned attestation-reference sets.
`semantic_extensions` contains only extensions with an exact admitted result;
an offered but unvalidated extension remains outside the environment and makes
its target incompatible under section 8.
The §3.3 `validationReferences` projection of a `SemanticEnvironment` is the
exact union over its pair bindings and semantic extensions; the projection of
a `PluginPackage` additionally includes its compatibility claims and
migrations. Package/environment equality still includes every underlying
required certificate/validator/root key, while semantic proper closure does
not traverse those separately typed bindings. Every derived
`DependencyEnvironment.validation_references` must equal the corresponding
complete projection; it cannot omit, add, or rewrite one.

`ServiceIdentityRecord` is the unique derived projection of one or more
conformant `CapabilityDescriptor`s with the exact same `service_key`; its ABI
and plugin fields must equal the corresponding descriptor fields and the key's
plugin. It is absent when there is no such descriptor, and conflicting
projections are malformed. It is never supplied as a second package field.
`TrustPolicyRecord` is analogously the unique derived projection of the exact
`TrustEnvironment.trust_policy_key` and its structurally fixed owner; it is not
a plugin-supplied record.

Trust is an independently owned embedding-policy input. `TrustRootKey` and
`TrustPolicyKey` compare componentwise, including exact versions. For every
root referenced by a descriptor, certificate, or admission record,
`TrustEnvironment.root_judgments` contains exactly one judgment. Omission is
`TRUST_ROOT_ABSENT`; an unequal record for the same key is
`TRUST_ROOT_INCOMPATIBLE`; unresolved external discovery is
`TRUST_ROOT_UNDECIDED`, and protocol/transport failure is
`TRUST_ROOT_FAILED`. None except admission permits validation. A root is usable only
under `TRUST_ROOT_ADMITTED`. Certificate use requires a listed validator,
certificate kind, and exact admission target; ordinary service use requires
the exact `SERVICE_USE_TRUST_TARGET`. Either use additionally requires the root key's policy
component to equal `TrustEnvironment.trust_policy_key`, the derived record
owner and `policy_owner` both to equal
`EMBEDDING_POLICY_PRODUCER(trust_policy_key)`, and
`adoption=V0_EXTERNAL_TRUST_PREMISE`; mismatch is the
incompatible judgment. A listed validator is not thereby available or sound; all
ordinary descriptor, fragment, support, and invocation checks still apply.

Every non-admitted judgment has an exact root-local payload. For every reason
`h` under key `k`, conformance requires
`h.issuer_scope=ABI_REASON_ISSUER`, `h.trust_root_key=k`, and
`h.trust_policy_key=k.trust_policy_key`. `TRUST_ROOT_UNDECIDED` permits only
`ROOT_DISCOVERY_UNRESOLVED`; `TRUST_ROOT_FAILED` permits a nonempty set whose
codes are all `ROOT_DISCOVERY_PROTOCOL_FAILURE` or all
`ROOT_DISCOVERY_TRANSPORT_FAILURE` (never a mixture); and
`TRUST_ROOT_INCOMPATIBLE` permits only the eight conflict, key/owner/adoption,
validator, kind, and target mismatch codes. `implicated_capability` is
`NO_CAPABILITY` unless the exact mismatch or failed lookup concerns one named
capability. `TRUST_ROOT_ABSENT` remains key-only. A wrong tag, code family,
root/policy coordinate, issuer, or capability coordinate makes the map
nonconformant; there is no reason fallback or prose equality.
`ROOT_DISCOVERY_UNRESOLVED` is a root evaluability state, not a K1
`UnknownReason`: it can yield `EVALUABILITY_UNKNOWN` but never by itself a
logical `Truth.UNKNOWN`, consistency/relation unknown, or profile result.
Likewise a failed root lookup becomes only the exact discovery failure, and an
incompatible root becomes only capability incompatibility/evaluability
missing. The three families are not collapsed.

`TrustRootStatusReason` is a closed first-order record containing only its
fixed enum, exact policy/root keys, and optionally one capability key. It is
structurally incapable of containing a `RequestIdentity`, `ResultIdentity`,
expected/offending result identity, any semantic/trust/dependency environment
or identity, `InterfaceFailure`, `InterfaceFailureReason`, `UnknownReason`, or
any request/result/environment carrier. `TRUST_ROOT_ADMITTED` contains one
`TrustRootRecord`; its finite `TrustTarget` values are independently
non-recursive by the next paragraph and contain no trust environment. Thus no
`TrustRootJudgment` points back to the `TrustEnvironment` whose map contains
it. Exact finite-map equality therefore makes `TrustEnvironmentIdentity`
finite and non-recursive.

`TrustTarget` equality is tag and payload equality. Its six admission tags
use the exact subject key; `JUDGMENT_TRUST_TARGET` uses the complete exact
reasoning subject tuple but deliberately excludes `SemanticEnvironment` and
all trust fields. The admission request independently binds the complete exact
environment. This separation scopes roots to an exact semantic subject without
making a root recursively contain the trust environment that contains it.
`SERVICE_USE_TRUST_TARGET` analogously uses `ServiceUseSubject` plus the exact
derived semantic-environment identity, never a structurally embedded
`CapabilityTarget`, `SemanticEnvironment`, or `TrustEnvironment`. Therefore
`TrustTarget`, `CapabilityTarget`, and `SemanticEnvironment` are finite and
non-recursive types.

`V0_EXTERNAL_TRUST_PREMISE` is an explicit v0 conformance premise adopted by
the embedding policy owner outside plugin packages and discovered services.
No plugin package, certificate, provenance value, K1 authority fact, or
service can produce, modify, or validate a root. In particular, the service
authorized by a root is never invoked to admit that root. A trust root has no
`NormativeRole` and cannot `REQUIRE`, `AUTHORIZE`, or `BIND_CHOICE`.
Bootstrap terminates at the adopted external input, not a plugin assertion.

Section 3.3 defines total structural `producerOf` and `subjectProducerSet`
equations. For pair, authority, migration, compatibility, semantic-extension,
and every other admission subject, conformance requires the validator producer
to be outside that exact subject-producer set and requires the derived
embedding-policy producer of the root to differ from every subject, validator,
and plugin-certificate producer. A certificate issuer may otherwise also be a
subject producer, but that fact grants no trust and cannot relax these checks.
The inequalities and an already admitted exact root scoped to the validator,
kind, and target are mandatory. No owner or producer is a free assertion.

For literal bindings, `meaning_contract` returns one admitted value and
`unknown_contract` is exactly `NOT_APPLICABLE`. For functions it maps
positional admitted values to `TermResult` and has
`unknown_contract=NOT_APPLICABLE`. For predicates it maps positional
admitted values to the exact K1 `Eval`. Evidence and access contracts may be
the exact empty contract, but never omitted. A pair-derived occurrence meaning
is the total `OccurrenceBindingProjection` of §7.2, owned only by
`EventPairBinding`; it contains every ordinary binding field and the exact
model projection. A second ordinary predicate meaning for that occurrence key
conflicts.

`SemanticEnvironment.lexical_bindings` is the exact finite
variable/type/value environment admitted for the request. Its mechanical
dependencies and `chi_C` fields are recomputed from the closed subject; they
are never accepted as caller assertions. `DependencyEnvironment` is the
judgment-specific projection separating frozen syntax roots, derived binding
association edges/expanded roots, proper outgoing edges, and their transitive
closure, plus exact non-proper validation/admission bindings.

Every `CapabilityDescriptor.supported_targets` member must agree with its
`service_role`, one `supported_judgments` member, its fragments, and its exact
dependency scope. A `FUNCTION_EVALUATION` or `PREDICATE_EVALUATION` service
can name only the matching `BINDING_TARGET`; `VALUE_ADMISSION` only a
`TYPE_ADMISSION_TARGET` carrying the same semantic-environment identity;
profile roles only
`PROFILE_TARGET`; pair validation
only `PAIR_TARGET`; and environment-level reasoning/admission only the exact
`ENVIRONMENT_JUDGMENT_TARGET`. Cross-kind targets make the descriptor
incompatible.
`AUTHORITY_VALIDATION`, `MIGRATION_VALIDATION`,
`COMPATIBILITY_VALIDATION`, and `SEMANTIC_EXTENSION_VALIDATION` require,
respectively, the matching four admission `JudgmentTag` values and the full
subject/environment shapes in section 5.1; `REASONING` cannot substitute for
one of those validation roles.

Every ordinary invocation consumes roots; v0 has no root-free service role.
For any invocation or admission request `r`, derive without producer input:

```text
serviceUseSubject(r) = the tag-specific projection of r.capability_target
serviceUseTrustTarget(r) = SERVICE_USE_TRUST_TARGET(
  r.capability_key, judgmentOf(r), serviceUseSubject(r),
  semanticIdentity(semanticEnvironmentOf(r)))
```

`semanticEnvironmentOf(r)` is `r.semantic_environment` for every ordinary
request carrying that field, `r.environment_without_fact` for authority
admission, and `r.environment_without_extension` for semantic-extension
admission. For the derived certificate-validation request it is the request's
exact `semantic_environment` field.

The target projection removes only the already separately bound environment
identity; it preserves the exact binding, type, profile, pair, or
environment-judgment subjects. Each descriptor root is usable for `r` only if
the separately carried `r.trust_environment` has the descriptor root under
`TRUST_ROOT_ADMITTED`, and that record permits the
exact capability, judgment, service-use subject, and environment identity.
The root policy owner must differ from the capability producer and every
non-trust producer represented in the target and
`SemanticEnvironmentIdentity`; the separately carried trust environment is
excluded from that subject-producer set (and necessarily contains the policy
owner itself). The ordinary capability may
still be supplied by the semantic subject's plugin. These are service-use
independence rules; certificate admission retains the stronger validator/
subject independence rules above. An absent, incompatible, or out-of-scope
required root makes the capability incompatible for this request and yields
`EVALUABILITY_MISSING`; a root-undecided judgment yields
`EVALUABILITY_UNKNOWN`; root discovery failure yields `DISCOVERY_FAILED` and
no evaluability result. None yields a value, truth, profile, pair, admission,
consistency, or relation conclusion.

Equivalently, with `rootProducer(k)=producerOf(k)` and singleton capability
producer sets, define

```text
serviceSubjectProducerSet(r,U) = subjectProducerSet(subjectOf(r),U)
  for every non-certificate-validation request
serviceSubjectProducerSet(v,U) = validationSubjectProducerSet(
  v.original_subject,U,v.certificate_key,v.validator_key,
  the root authorizing v.certificate_admission_trust_target)
  for CertificateValidationRequest v
```

Ordinary service use then requires

```text
rootProducer(root) intersect
  (serviceSubjectProducerSet(r,U) union producerOf(capabilityForService(r))) = {}
```

where `capabilityForService(v)=v.validator_key` and otherwise equals
`r.capability_key`. Certificate/admission use additionally requires

```text
producerOf(v.validator_key) intersect
  validationSubjectProducerSet(v.original_subject,U,v.certificate_key,
                               v.validator_key,admission_root) = {}
rootProducer(admission_root) intersect
  (validationSubjectProducerSet(v.original_subject,U,v.certificate_key,
                                 v.validator_key,admission_root)
   union producerOf(v.validator_key)
   union producerOf(v.certificate_key)) = {}
```

These sets are recomputed structurally. A producer field, certificate claim,
or target list cannot alter them.

### 2.4 Independent lifecycle state

For each required key and requested judgment, the lifecycle is the product of
four total independent coordinates, not a registration sequence. Every
coordinate always has exactly one variant, including after an earlier invalid,
irrelevant, or failed coordinate:

```text
DeclarationState =
    DECLARATION_INVALID(nonempty finset(InterfaceFailureReason))
  | DECLARATION_NOT_REQUIRED
  | DECLARED
BindingState =
    BINDING_BLOCKED_BY_DECLARATION
  | BINDING_NOT_REQUIRED
  | BINDING_ABSENT
  | BINDING_INCOMPATIBLE(nonempty finset(InterfaceFailureReason))
  | SEMANTICALLY_BOUND
DiscoveryState =
    DISCOVERY_BLOCKED_BY_DECLARATION
  | DISCOVERY_BLOCKED_BY_BINDING
  | DISCOVERY_NOT_REQUIRED
  | DISCOVERY_FAILED(InterfaceFailure[DISCOVERY])
  | DISCOVERY_UNDECIDED(nonempty finset(UnknownReason))
  | CAPABILITY_ABSENT
  | CAPABILITY_INCOMPATIBLE(nonempty finset(InterfaceFailureReason))
  | CAPABILITY_OUTSIDE_FRAGMENT
  | CAPABILITY_DISCOVERED
InvocationFailureFamily =
    EVALUATION | REASONING | REASONING_PROTOCOL | ADMISSION |
    PROTOCOL | TRANSPORT
InvocationState =
    INVOCATION_BLOCKED_BY_DECLARATION
  | INVOCATION_BLOCKED_BY_BINDING
  | INVOCATION_BLOCKED_BY_DISCOVERY
  | INVOCATION_NOT_REQUIRED
  | NOT_INVOCABLE(nonempty finset(InterfaceFailureReason))
  | INVOCABLE_FOR(exact_request)
  | COMPLETED(conformant_result)
  | INVOCATION_FAILED(
      failure_family : InvocationFailureFamily,
      reasons : nonempty finset(
        EvaluationErrorReason | ReasoningErrorReason |
        InterfaceFailureReason))

LifecycleState = (
  declaration_state : DeclarationState,
  binding_state : BindingState,
  discovery_state : DiscoveryState,
  invocation_state : InvocationState
)
```

Validation derives all four coordinates by these exhaustive rules. The first
applicable row in each coordinate is fixed by the stated earlier-coordinate
value; this is validation precedence, not registration order:

```text
declarationRequirement(BINDING_TARGET(k))       = REQUIRED(Delta declaration k)
declarationRequirement(TYPE_ADMISSION_TARGET(k,_)) = REQUIRED(TypeDeclaration k)
declarationRequirement(PAIR_TARGET(p))          = REQUIRED(actual Delta pair declaration p)
declarationRequirement(PROFILE_TARGET(_))       = NOT_REQUIRED
declarationRequirement(ENVIRONMENT_JUDGMENT_TARGET(_,_,_)) = NOT_REQUIRED

bindingRequirement(BINDING_TARGET(k)) = REQUIRED(BINDING(k))
bindingRequirement(PROFILE_TARGET(p)) = REQUIRED(PROFILE(p))
bindingRequirement(PAIR_TARGET(p))    = REQUIRED(PAIR binding p)
bindingRequirement(TYPE_ADMISSION_TARGET(_,_)) = NOT_REQUIRED
bindingRequirement(ENVIRONMENT_JUDGMENT_TARGET(_,_,_)) = NOT_REQUIRED
```

These functions are total and kernel-derived. Ordinary literal/function/
predicate targets require their exact `Delta` declaration; pair targets use
their actual `EventScopePairDeclaration`, not a synthetic declaration key.
Profile, environment/service-only, and admission-only targets invent no
`Delta` record. In particular, an absent `ProfileBinding` yields
`DECLARATION_NOT_REQUIRED+BINDING_ABSENT`, hence remains open. Subject closure
inside an environment-level target is validated separately and cannot be
skipped because the target itself needs no declaration or binding coordinate.

| Condition | Lifecycle result | K0/K1 public family |
|---|---|---|
| required declaration missing, ill-typed, kind-confused, or conflicting | `DECLARATION_INVALID+BINDING_BLOCKED_BY_DECLARATION+DISCOVERY_BLOCKED_BY_DECLARATION+INVOCATION_BLOCKED_BY_DECLARATION` | `MALFORMED`; no coordinate is omitted |
| target kind has no declaration coordinate | `DECLARATION_NOT_REQUIRED`; derive the binding coordinate independently | no declaration or `Delta` record is fabricated |
| exact declaration valid and target kind has no Sigma binding, including type admission | `DECLARED+BINDING_NOT_REQUIRED`; discovery is independently required or not required by the requested judgment | `WELL_FORMED`; `BINDING_NOT_REQUIRED` is not closure |
| environment/service-only or admission-only target needs neither coordinate | `DECLARATION_NOT_REQUIRED+BINDING_NOT_REQUIRED`; discovery is independently derived after subject closure | no target declaration/binding is fabricated; subject closure still applies |
| exact declaration valid, required meaning absent | `DECLARED+BINDING_ABSENT+DISCOVERY_BLOCKED_BY_BINDING+INVOCATION_BLOCKED_BY_BINDING` | `WELL_FORMED+OPEN_BINDINGS` |
| declaration not required and required profile binding absent | `DECLARATION_NOT_REQUIRED+BINDING_ABSENT+DISCOVERY_BLOCKED_BY_BINDING+INVOCATION_BLOCKED_BY_BINDING` | `OPEN_BINDINGS`; no synthetic Delta declaration |
| binding conflicts with declaration, or typed `PAIR_INCOHERENCE_ADMITTED` is received | `DECLARED+BINDING_INCOMPATIBLE+DISCOVERY_BLOCKED_BY_BINDING+INVOCATION_BLOCKED_BY_BINDING` | `MALFORMED(incompatible semantic binding)` |
| declaration/binding valid and no service judgment was requested | `DISCOVERY_NOT_REQUIRED+INVOCATION_NOT_REQUIRED` | no evaluability or result family is fabricated |
| exact meaning valid, requested service absent | `SEMANTICALLY_BOUND+CAPABILITY_ABSENT+INVOCATION_BLOCKED_BY_DISCOVERY` | closed if nothing else is open; `EVALUABILITY_MISSING` |
| discovery cannot decide | `DISCOVERY_UNDECIDED+INVOCATION_BLOCKED_BY_DISCOVERY` | `EVALUABILITY_UNKNOWN`; no invocation |
| discovery protocol or transport fails | `DISCOVERY_FAILED(failure)+INVOCATION_BLOCKED_BY_DISCOVERY` | exact discovery failure and no evaluability status; failure is not uncertainty |
| service incompatible or outside requested fragment | corresponding discovery state plus `INVOCATION_BLOCKED_BY_DISCOVERY` | `EVALUABILITY_MISSING` for that exact request |
| compatible service found and all request premises pass | `INVOCABLE_FOR(r)` | `EVALUABILITY_AVAILABLE`; no truth/relation follows |
| compatible service found but request validation fails | `NOT_INVOCABLE(reasons)` | malformed request; no invocation result |
| successful denotational invocation returns the exact expected `VALUE_ADMITTED/NOT_ADMITTED`, literal/function `TermResult`, predicate/pair-occurrence `Eval`, or profile complete/incomplete result | `COMPLETED(conformant_result)` replaces `INVOCABLE_FOR(r)` | exact admission/value/truth/evaluation-error/profile family; function error projects to evaluation error only at a containing atom |
| successful admission/reasoning invocation returns an admitted decisive conclusion permitted by its exact receiving rule | `COMPLETED(conformant_result)` replaces `INVOCABLE_FOR(r)` | exactly the named pair/admission/consistency/relation/internal conclusion |
| compatible partial or out-of-complete-fragment service is invoked and conformantly completes inconclusively, including `*_NOT_ADMITTED`, pair rejection, reasoning inconclusive, or profile unknown | `COMPLETED(conformant_nondecisive_result)` replaces `INVOCABLE_FOR(r)` | applicable logical/profile unknown only where K1 defines it; an admission rejection grants no conclusion |
| conformant denotational or admission error tag is returned | `COMPLETED(conformant_error_result)` replaces `INVOCABLE_FOR(r)` | exact evaluation/reasoning error family and no truth/profile/relation/admission conclusion |
| complete in-fragment service completes inconclusively | construct the exact reasoning-role `PROTOCOL_FAILURE` with `NO_RESULT_SENTINEL`, then `INVOCATION_FAILED(REASONING_PROTOCOL,...)` | pointwise `REASONING_ERROR`, never logical/profile unknown |
| result carrier is malformed or shape-valid but semantically unequal to its exact expected result/receiving rule | exact `resultFailure` yields `MALFORMED_RESULT(MALFORMED_CARRIER)` or `MALFORMED_RESULT(SEMANTIC_MISMATCH)` and replaces `INVOCABLE_FOR(r)` | total pointwise role projection in §5.4; the returned value/truth/admission is discarded |
| one of the four evaluation roles fails before a conformant result | `INVOCATION_FAILED(EVALUATION|PROTOCOL|TRANSPORT,...)` with exact canonical interface reasons | §5.4 `evaluationReasons` and exact role carrier; no truth/profile/relation |
| one of the seven reasoning/admission roles fails before a conformant result | `INVOCATION_FAILED(REASONING|REASONING_PROTOCOL|ADMISSION|PROTOCOL|TRANSPORT,...)` with exact canonical interface reasons | §5.4 `reasoningReasons` and exact role carrier; no consistency/profile/relation/admission |

Completion classification is exhaustive over the result unions in §§5--6:

```text
DECISIVE_COMPLETION =
  VALUE_ADMITTED | VALUE_NOT_ADMITTED |
  exact TERM_VALUE | exact TERM_ERROR |
  exact Eval.VALUE | exact Eval.ERROR |
  PROFILE_COMPLETE | PROFILE_INCOMPLETE |
  PAIR_COHERENCE_ADMITTED | PAIR_INCOHERENCE_ADMITTED |
  AUTHORITY_FACT_ADMITTED | MIGRATION_RELATION_ADMITTED |
  COMPATIBILITY_CLAIM_ADMITTED | SEMANTIC_EXTENSION_ADMITTED |
  ADMITTED_JUDGMENT | CertificateAdmission.ADMITTED

NONDECISIVE_COMPLETION =
  PROFILE_UNKNOWN | PAIR_VALIDATION_REJECTED |
  AUTHORITY_FACT_NOT_ADMITTED | MIGRATION_RELATION_NOT_ADMITTED |
  COMPATIBILITY_CLAIM_NOT_ADMITTED |
  SEMANTIC_EXTENSION_NOT_ADMITTED | COMPLETED_INCONCLUSIVE |
  CertificateAdmission.REJECTED_NONDECISIVE

CONFORMANT_ERROR_COMPLETION =
  ADMISSION_ERROR | ProfileResult.EVALUATION_ERROR |
  ProfileResult.REASONING_ERROR | PairValidationResult.EVALUATION_ERROR |
  PairValidationResult.REASONING_ERROR |
  every admission-result EVALUATION_ERROR or REASONING_ERROR |
  ReasoningResult.EVALUATION_ERROR | ReasoningResult.REASONING_ERROR |
  CertificateAdmission.EVALUATION_ERROR |
  CertificateAdmission.REASONING_ERROR
```

Every member replaces `INVOCABLE_FOR(r)` with `COMPLETED(the exact tagged
result)` and then projects only the public family defined for that tag.
`CertificateAdmission.MALFORMED_ENVELOPE`, malformed/unequal invocation
results, complete-fragment nondecisiveness, and service/protocol/transport
failures instead replace it with `INVOCATION_FAILED` in the exact family above.
No result union has an unclassified tag, and no completed coordinate remains
`INVOCABLE_FOR`.

The projection is exact: admission tags retain only admitted/not-admitted;
`TERM_VALUE` continues term evaluation and `TERM_ERROR` remains a term error
until A2 projects it to atom `EVALUATION_ERROR`; `Eval.VALUE(TRUE|FALSE|UNKNOWN)`
maps respectively to `TRUTH_TRUE|TRUTH_FALSE|TRUTH_UNKNOWN` with the complete
metadata, and `Eval.ERROR` maps only to `EVALUATION_ERROR`; the five profile tags
map only to their same-named profile/evaluation/reasoning families; positive or
typed-negative pair tags map only to pair bound/incompatible, while rejection
admits neither; each authority/migration/compatibility/extension admitted tag
admits only its exact subject and each not-admitted tag admits none; and an
`ADMITTED_JUDGMENT` maps only to its exact consistency/relation/internal
conclusion. Every declared error tag maps only to its displayed error family.

For a valid closed consistency or public-relation subject, the logical result
coordinate is derived independently: admitted decisive core/certificate
evidence gives its named decisive result; an admitted decisive counterexample
gives its named disproof; otherwise it is `CONSISTENCY_UNKNOWN` or
`RELATION_UNKNOWN` even when discovery is absent, outside-fragment, or
undecided. Thus evaluability missing/unknown and logical unknown can be
simultaneous. An invocation or validator failure instead yields its error and
no conclusion for that failed invocation. Profiles are different: no profile
result exists without an invoked compatible checker, and `PROFILE_UNKNOWN`
requires its conformant inconclusive completion.

Retries, registration order, discovery order, service location, and diagnostics
cannot change a coordinate's semantic identity or any completed judgment.
There is no omitted-coordinate notation and none of these variants is an
implicit default.

### 2.5 Exhaustive interface-responsibility ledger

This ledger is exhaustive. In a row listing several dot-qualified fields, the
single disposition applies independently to every listed field. No logical ABI
record or field exists outside these rows. `Axx` in the Case column is the
unambiguous abbreviation for `K2-Axx`.

<!-- LEDGER-BEGIN -->
| Record or exact fields | Disposition | Owner | K1 obligation | Producer | Consumer | Validator | Identity/version rule | Omission behavior | Failure family | Case |
|---|---|---|---|---|---|---|---|---|---|---|
| `AbiVersion.{abi_namespace,exact_version}` | `REQUIRED_SEMANTIC` | K1 carrier | exact protocol identity | package/request author | every ABI validator | exact equality | both components bind v0 | malformed | protocol | A03 |
| `PluginKey.{plugin_identity,exact_version}`; `PluginIdentity.{owner_namespace,local_identity}` | `REQUIRED_SEMANTIC` | Delta | exact plugin identity | plugin declarer | all layers | component equality | version is exact, unordered | malformed | structure | A04 |
| `DeclarationKey.{plugin_key,declaration_namespace,local_name,kind}` | `REQUIRED_SEMANTIC` | Delta | declaration/kind separation | declarer | Delta/Sigma validators | component equality | kind is identity | malformed | structure | A01 |
| `SymbolKey.{plugin_key,symbol_namespace,local_name,kind}` | `REQUIRED_SEMANTIC` | Delta | exact function/predicate identity | declarer | binding/request | exact declared match | kind and plugin exact | malformed | structure | A04 |
| `EventKey.{plugin_key,event_namespace,local_name}` | `REQUIRED_SEMANTIC` | Delta | immutable event identity | declarer | event/pair/auth validators | exact declared match | plugin version exact | malformed | structure | A12 |
| `ProfileKey.{plugin_key,profile_name}`; `ProfileDimensionKey.{profile_key,dimension_name}` | `REQUIRED_SEMANTIC` | Sigma | exact relative profile/dimensions | profile author | closure/checker | exact set equality | plugin version exact | open | closure/profile | A15 |
| `EventScopePairKey.{plugin_key,pair_namespace,local_name}` | `REQUIRED_SEMANTIC` | Delta | exact companion identity | declarer | pair binding/closure | exact equality | plugin version exact | malformed/open by layer | structure/closure | A13 |
| `BindingKey` | `DERIVED` | Sigma | unique meaning per declaration | binding validator | all meaning consumers | equals declaration key | no independent version | impossible to omit separately | structure | A01 |
| `ServiceKey.{plugin_key,service_namespace,local_name,exact_service_version,service_role}`; `CapabilityKey.{service_key,capability_name}` | `REQUIRED_SEMANTIC` | Service | exact capability identity | service declarer | discovery/request | component/kind equality | exact only | evaluability missing | evaluability | A02 |
| `CertificateIssuer`; `CertificateKey.{issuer,certificate_namespace,local_identity}` | `REQUIRED_SEMANTIC` | Service/embedding policy | stable exactly owned certificate identity | typed certificate issuer | admission validator | exact issuer structural equality | issuer producer and bound environment exact | malformed certificate | reasoning | A17 |
| `MigrationKey.{owner_plugin,migration_namespace,local_identity,exact_migration_version}` | `REQUIRED_SEMANTIC` | Sigma | explicit plugin-owned evolution identity | migration owner plugin | migration validator | component equality and derived owner | exact source/target remain separate | no migration | compatibility | A20 |
| `SemanticExtensionKey.{owner_plugin,extension_namespace,local_name,exact_extension_version}` | `REQUIRED_SEMANTIC` | owning layer | namespaced semantic extension identity | extension owner | package validator | component equality | exact owner/version | no extension | compatibility | A20 |
| `TrustPolicyKey.{embedding_policy_namespace,local_policy_identity,exact_policy_version}`; `TrustRootKey.{trust_policy_key,root_namespace,local_root_identity,exact_root_version}`; `IssuerScope` | `REQUIRED_SEMANTIC` | embedding policy/K1 carrier | exact typed issuer and independent trust identities | embedding policy or exact issuer | discovery/invocation/certificate/admission gates | component/tag equality | versions exact | root absent; no compatible service or admission | trust/evaluability/reasoning | A02,A14,A17 |
| `ProducerIdentity`; `TrustPolicyRecord.{trust_policy_key,owner}`; `TrustRootRecord.owner`; `TrustEnvironment.policy_owner`; total `producerOf`; `producerReachabilityRoots`; filtered `producerReachable`; total ordinary/validation `subjectProducerSet`; `validationReferenceProducers`; `validationBindingProducerSet` | `DERIVED` | ownership validation | no producer/owner assertion and complete independence | required plus semantic roots, derived associations, all non-validation proper references, with validation-reference producers separate | all trust/service/admission gates | recompute the complete finite semantic producer set and the exact validation certificate/validator/service/root producers, then enforce separate inequalities | owner keys/versions exact | cannot be supplied; malformed/conflict on mismatch | structure/trust/reasoning | A13,A14,A17,A19,A20 |
| `AuthorityFactKey.{authority_ref,source_ref,principal,normative_role}` | `REQUIRED_SEMANTIC` | Sigma | exact four-tuple fact identity | authority subject former | closure/adoption/choice | tuple equality | referenced identities exact | open/no fact | closure/reasoning | A14 |
| `AuthorityFactCandidate.{authority_fact_key,admission_subject_data,offered_evidence_refs}` | `REQUIRED_SEMANTIC` | admission input | exact non-self-rooting candidate subject, not a Sigma fact | candidate former | authority validator | typed data agrees with four-tuple; target-excluded environment; evidence admitted separately | candidate/request exact | no map entry | closure/reasoning/trust | A14,A18 |
| `ContractIdentity`; `SemanticEnvironmentIdentity`; `TrustEnvironmentIdentity`; `RequestIdentity`; `ResultIdentity`; `ExpectedResultContractIdentity`; `OffendingResultIdentity`; `LexicalScopeIdentity.{judgment_or_binder_kind,subjects}`; `LexicalBindingKey.{scope_identity,variable,declared_type}`; `ChoiceBindingKey.{contract_identity,choice_id}` | `DERIVED` | K1 carrier | exact finite non-recursive semantic/trust-environment, subject, request, result, and scope identities | exact structural derivation | support/closure/trust/reasoning/failure | complete logical fields and extensional ContractSpec relations; exact TrustEnvironment map equality whose non-admitted payloads are closed root-local reasons; then component/tag equality | subject/type/root versions exact | cannot be supplied | structure/closure/trust/protocol | A02,A10,A17,A18 |
| `ContractSpec.{contract_key,owner_layer,contract_role,primary_input_domain,codomain,observation_queries,logical_relation}`; `ContractRole`; `DependencyObservationKind`; `DependencyObservationQuery.{expected_kind,input_projection}`; `SemanticTargetIdentity`; `ModelContractKey.{target_semantic_identity,document_namespace,locale_identity,exact_document_version}`; `CompatibilityClaimKey.{owner_plugin,claim_namespace,local_identity,exact_claim_version}` | `REQUIRED_SEMANTIC` | record-declared | owner/use-specific stratified exact logical contract and auxiliary identities | owning declarer | applicable validator | exact use-role assignment and total owner/role/key/kind matrix; relation takes only explicit input plus allowed lower observations | enclosing exact versions/role bind | malformed if required or matrix-invalid | structure | A05,A06,A08,A09,A18 |
| `ObservationInput`; `DependencyObservationValue`; `support(ContractSpec)`; `freeDependencies`; `DependencyObservationEnvironment`; topologically confluent `dependencyObservations` | `DERIVED` | contract validation | total exact finite lower-level support without environment/contract recursion or hidden service/authority/choice channels | section 3.3 extensional/DAG rule | every denotational consumer | query-domain equals extensional support; exact typed finite-map equality; pure deterministic predecessor-only producers give equal maps in every topological order | enclosing contract identity/version | cannot be producer-supplied; missing gives exact malformed/open/evaluability status | layer-specific structure/closure/evaluability | A06,A08,A09,A10,A18 |
| `DependencyKey.{tag,exact_key}`; `K1SyntaxKey.{tag,exact_key}` | `DERIVED` | K1 carrier | kind-separated semantic roots with frozen syntax facet retained | mechanical extraction/tag lift | closure/request/certificate | tag and key equality | key version exact | cannot be supplied | structure/closure | A06 |
| `RecordIdentity`; `recordIdentity`; `dependencyRoot`; `rootKeys`; `subjectReferences`; `ValidationReference`; `validationReferences`; `validationReferenceRoots`; `admissionBindingReferences`; `Subject`; `subjectOf`; `subjectOfCapabilityTarget`; `subjectRoots`; `requestFieldRoots`; `semanticRequestRoots`; `requestValidationReferences`; `requestRoots`; `certificateProperReferences`; `certificateValidationRoots`; `certificateRoots`; `required`; `requiredKey`; `environmentWithoutAuthorityFact`; association/`recordAt` functions | `DERIVED` | K1/interface validation | exhaustive identity/root/subject algebra with non-proper mandatory validation bindings, TrustEnvironment carrier root, identity/proper-reference separation, non-self-rooting authority and exact missing/cycle status | structural equations in §3.3/§5.1 | closure/request/certificate/trust | total tagged equations, singleton start roots, separately exact semantic and validation roots/lookups, constructor-audited proper references, and least acyclic semantic closure | all embedded versions exact | cannot be supplied; malformed/open/missing per exact kind | structure/closure/evaluability/trust | A01,A02,A06,A13,A14,A17,A20 |
| `CapabilityTarget.{tag,payload}` | `REQUIRED_SEMANTIC` | Service | exact binding/type/profile/pair/environment target with non-recursive environment identity | service/request former | discovery/invocation/admission | tag-specific payload/environment-identity equality | every payload version exact | target/service absent | evaluability/protocol | A03 |
| `TrustTarget.{tag,payload}`; `ServiceUseSubject.{tag,payload}` | `REQUIRED_SEMANTIC` | embedding policy | exact non-recursive certificate and ordinary-service use scope | embedding policy owner | discovery/invocation/certificate admission | tag/payload equality, exact capability/judgment/subject/environment identity, full request environment and producer-independence checks | subject versions exact | root unusable; capability incompatible/unknown/failure by root state | trust/evaluability/reasoning | A02,A17 |
| `PluginPackage.{abi_version,plugin_key,declarations,pair_declarations,bindings,pair_bindings,profile_bindings,model_contracts,aliases,services,certificates,authority_facts,compatibility_claims,migrations,semantic_extensions}` | `REQUIRED_SEMANTIC` | projected | whole-package separation | package author | discovery/composition | package conformance | set members exact | empty sets mean absent roles | structure/conflict | A01 |
| `PluginPackage.diagnostics`; `Diagnostics.{display_label,narrative,timing,endpoint_hint,retry_note,correlation_atom,extensions}`; `DiagnosticExtension.{grouping_identity,payload}` | `OPTIONAL_DIAGNOSTIC` | Diagnostic | affects no K1 judgment or semantic grouping | any interface participant | human observer only | diagnostic noninterference | not identity/version | any/all may be dropped | none | A11 |
| `Outcome.{PRE,TRACE,FINAL,EVIDENCE}` | `REQUIRED_SEMANTIC` | K1 carrier | four independent outcome projections | outcome former | term/atom/auth evaluation | Delta admission and component equality | environment-bound, no version fallback | malformed outcome | evaluation | A08 |
| `TypeDeclaration.{key,admitted_value_domain}` | `REQUIRED_SEMANTIC` | Delta | type/value admission | declarer | formation/value validator | membership validation | key exact | malformed | structure | A07 |
| `LiteralDeclaration.{key,literal_identity,result_type}` | `REQUIRED_SEMANTIC` | Delta | typed literal declaration | declarer | binding/term validator | exact type/admission | key exact | malformed | structure | A07 |
| `FunctionDeclaration.{key,symbol_key,argument_types,result_type,facet_positions}` | `REQUIRED_SEMANTIC` | Delta | typed function signature/facets | declarer | binding/invocation | positional type/facet checks | keys exact/same owner | malformed | structure | A07 |
| `PredicateDeclaration.{key,symbol_key,argument_types,result_kind,facet_positions}` | `REQUIRED_SEMANTIC` | Delta | typed atom/facet boundary | declarer | binding/invocation | positional type/facet checks | keys exact/same owner | malformed | structure | A08 |
| `EventDeclaration.{key,event_key,payload_type,event_class}` | `REQUIRED_SEMANTIC` | Delta | typed immutable event class | declarer | outcome/auth/pair | payload/class exact | key exact | malformed | structure/evaluation | A12 |
| `EventScopePairDeclaration.{pair_key,scope_symbol,occurrence_symbol,controlled_keys}` | `REQUIRED_SEMANTIC` | Delta | pair membership/controlled set | declarer | pair binding/closure | signatures, nonempty controlled set | exact pair/member keys | malformed | structure | A13 |
| `TypeDeclaration.proper_declaration_dependencies`; `LiteralDeclaration.proper_declaration_dependencies`; `FunctionDeclaration.proper_declaration_dependencies`; `PredicateDeclaration.proper_declaration_dependencies`; `EventDeclaration.proper_declaration_dependencies`; `EventScopePairDeclaration.proper_declaration_dependencies` | `DERIVED` | Delta | proper outgoing support excludes roots/self-edges | section 3.3 | closure/request | recompute exact proper edges and reject cycles | exact DependencyKey sets | cannot be producer-supplied | structure/closure | A06 |
| `EventScopePairDeclaration.{scope_signature,occurrence_signature,scope_facets,occurrence_facets}` | `DERIVED` | Delta | frozen companion shapes | declaration validator | pair consumer | derive from member declarations | no identity contribution | cannot be supplied | structure | A13 |
| `SemanticBinding.{binding_key,declaration_key,binding_kind,meaning_contract,permitted_facet_inputs,evidence_schema,access_boundary,unknown_contract,evaluation_error_contract,determinism_rule}` | `REQUIRED_SEMANTIC` | Sigma | exact meaning independent of service | meaning author | closure/evaluator/model contract | binding conformance | binding key derived, plugin exact | open | closure/structure | A05 |
| `SemanticBinding.{proper_semantic_dependencies,dependency_closure}` | `DERIVED` | Sigma | exact proper support and well-founded transitive semantics | section 3.3/environment validator | closure/request | roots/proper edges then least closure | set exact; no self-edge | cannot be caller-omitted | structure/closure | A06 |
| `EventPairBinding.{pair_key,scope_binding_key,occurrence_binding_key,occurrence_model_contract_key,admission.tag,admission.certificate_key,admission.validator_key}` | `REQUIRED_SEMANTIC` | Sigma | full-result pair coherence path, exact producer-supplied occurrence model key, and mandatory non-proper validation references | meaning/proof author | closure/conditional/model forms | sections 3.3/4.3/7 admission; certificate/validator exact lookup without semantic back-edge | exact pair/binding/model/certificate/validator keys | open | closure/reasoning | A13 |
| `OccurrenceSemanticContractBundle.{meaning_contract,permitted_facet_inputs,evidence_schema,access_boundary,unknown_contract,evaluation_error_contract,determinism_rule}` | `REQUIRED_SEMANTIC` | Sigma | complete independent occurrence semantics before coherence proof | pair meaning author | pair admission/occurrence invocation | exact occurrence declaration/facets/contracts plus admitted universal full-Eval proof | pair/occurrence versions exact | missing/unequal bundle leaves no projection and is incompatible | structure/closure/reasoning | A13 |
| `EventPairBinding.{proper_semantic_dependencies,dependency_closure}` | `DERIVED` | Sigma | pair/member/event/support proper dependencies | pair validator | closure/request | root excluded then least closure | set exact; no pair self-edge | cannot be omitted | structure/closure | A13 |
| `OccurrenceSemanticContractBundle.{proper_semantic_dependencies,dependency_closure}`; `OccurrenceBindingProjection`; `occurrenceMeaningIdentity`; `occurrenceBindingIdentity`; `T3_A1_MEANING_LIFT`; `T3_A1_EVIDENCE_LIFT`; `T3_A1_ACCESS_LIFT`; `T3_A1_UNKNOWN_LIFT`; `T3_A1_ERROR_LIFT`; `T3_A1_DEPENDENCY_LIFT` | `DERIVED` | Sigma validation | complete pair-owned ordinary-binding projection with exact empty/multi-event T3/A1 semantics | §7.2 constructors | `recordAt(BINDING occurrence)`, invocation, closure, model consumer | derive every ordinary binding field; separately validate the producer-named model record; independent bundle proves full-Eval coherence | pair/occurrence/scope versions exact | no projection/open or incompatible; never ordinary fallback | structure/closure/evaluation/reasoning | A13 |
| `ProfileBinding.{profile_key,dimensions,coverage_meaning,evidence_schema,unknown_contract,evaluation_error_contract,reasoning_error_contract}` | `REQUIRED_SEMANTIC` | Sigma | exact profile-relative meaning | profile author | closure/checker | profile conformance | exact ProfileKey | open | closure/profile | A15 |
| `ProfileBinding.{proper_semantic_dependencies,dependency_closure}` | `DERIVED` | Sigma | proper support and full profile dependencies | section 3.3/environment validator | closure/checker | root excluded then least closure | set exact; no profile self-edge | cannot be omitted | structure/closure | A06 |
| `ModelContract.{model_contract_key,target_binding_key,exact_symbol_key,exact_signature,exact_facet_positions,evidence_contract,unknown_contract,error_contract,capability_summaries,semantic_contract_reference}`; `ModelCapabilitySummary.{capability_key,service_role,supported_judgments,capability_class,sound_fragment_key,complete_fragment_key,dependency_scope}` | `REQUIRED_SEMANTIC` | Sigma/model projection | same complete model/machine meaning and capability declaration | documentation author | binding analysis | exact field projection and bidirectional descriptor-summary conformance | complete target/document/capability versions exact | missing named record open; wrong malformed; unequal duplicate conflict | structure | A05,A13 |
| `ModelContract.explanatory_text` | `OPTIONAL_DIAGNOSTIC` | Diagnostic | wording creates no denotation/authority | documentation author | human/model presentation | target noninterference | not identity | no semantic effect | none | A05 |
| `AliasKey.{owner_plugin,alias_namespace,alias_atom}`; `AliasBinding.{alias_key,exact_target_key,target_kind,target_exact_version}` | `REQUIRED_SEMANTIC` | Sigma | explicit owned target-preserving alias | alias owner plugin | discovery/binding analysis | exact owner/target validation | alias never substitutes version | no alias | structure | A04 |
| `CapabilityDescriptor.{capability_key,abi_version,plugin_key,service_role,capability_class,supported_judgments,supported_targets,sound_fragment,complete_fragment,dependency_scope,required_evidence,required_trust_roots,failure_contract}` | `REQUIRED_SEMANTIC` | Service | capability-relative targeted admission and nonempty ordinary-use trust | service declarer | discovery/request/certificate | role/judgment/target/environment/fragment/scope/root-use conformance | exact service/plugin/ABI/targets/roots | evaluability missing/unknown/failure by root state | evaluability/reasoning/trust | A16 |
| `ServiceIdentityRecord.{service_key,abi_version,plugin_key}` | `DERIVED` | Service | exact service-root presence separate from capability roots | conformant capability projections | dependency/discovery lookup | unique projection from one or more same-service descriptors | exact ServiceKey/ABI/PluginKey | absent service or malformed conflicting projection | evaluability/structure | A06,A16 |
| `CapabilityDescriptor.{proper_semantic_dependencies,dependency_closure}` | `DERIVED` | Service | exact proper support of fragments/evidence/roots/failure | section 3.3 | discovery/request/certificate | roots/proper edges then least closure | target/key versions exact | cannot be supplied | capability incompatible/evaluability | A06 |
| `SemanticEnvironment.{abi_version,declarations,pair_declarations,bindings,pair_bindings,profile_bindings,authority_facts,semantic_extensions,lexical_bindings}` | `REQUIRED_SEMANTIC` | projected | one fully typed exact non-recursive Delta/Sigma/scope environment | kernel request former | closure/request/certificate | exact typed set/map and extensional non-recursive ContractSpec equality | exact keys/versions | open/malformed; trust remains separate | structure/closure | A17 |
| `SemanticEnvironment.{choice_bindings,mechanically_extracted_dependencies,chi_C}` | `DERIVED` | K1 carrier | choice records/dependencies/map cannot be overridden | kernel derivation | requests/certificates | recomputation equality | Contract-bound | cannot be supplied | structure/closure | A06 |
| `DependencyEnvironment.{syntax_root_keys,subject_root_keys,binding_association_edges,expanded_root_keys,proper_dependencies,transitive_dependency_closure,validation_references}` | `DERIVED` | K1 carrier | frozen K1 syntax roots plus exhaustive subject/record roots, association reachability, acyclic semantic closure, and separate mandatory admission bindings | kernel extraction/association/validation projection | closure/service/admission | exact K1 roots, total `subjectRoots`/`recordAt`, derived associations, reachable proper edges and least closure, plus exact non-traversed validation-reference set; reject malformed mapping/self/cycle/missing/conflict | exact sets/edge pairs/references | cannot be supplied or reduced; reachable missing binding stays open and missing validation retains its exact status | structure/closure/reasoning | A06,A13,A20 |
| `LexicalBinding.{lexical_binding_key,admitted_value}`; `ChoiceBindingEntry.{choice_binding_key,declared_type,admitted_value,controller,source_ref,authority_fact_key}` | `REQUIRED_SEMANTIC` | K1 carrier | exact typed scope and Contract choice records | subject/Contract former | environment/support/chi derivation | type, controller, source and authority checks | subject/key versions exact | malformed/open | structure/closure | A18 |
| `TrustRootRecord.{trust_root_key,trusted_validators,permitted_certificate_kinds,permitted_targets,adoption}`; `TrustEnvironment.trust_policy_key` | `REQUIRED_SEMANTIC` | embedding policy | independent exact v0 certificate and ordinary-service trust premise/scope | embedding policy owner | discovery/invocation/certificate/admission gates | exact versions, external adoption, use-specific scope and independence | policy/root versions exact | root absent; no compatible service or admission | trust/evaluability/reasoning | A02,A17 |
| `TrustRootStatusReason.{issuer_scope,status_code,trust_policy_key,trust_root_key,implicated_capability}`; `TrustRootStatusReasonCode`; `TrustRootJudgment.{TRUST_ROOT_ADMITTED.record,TRUST_ROOT_ABSENT.key,TRUST_ROOT_UNDECIDED.{key,reasons},TRUST_ROOT_FAILED.{key,reasons},TRUST_ROOT_INCOMPATIBLE.{key,reasons}}`; `TrustEnvironment.root_judgments` | `DERIVED` | embedding policy validation | total distinct root admission/absence/uncertainty/failure state with finite non-recursive identity | trust environment validator | discovery/invocation/certificate gates | exact map; exact tag-specific reason-code family and root/policy/capability coordinates; root reasons contain no request/result/failure/environment carrier | exact TrustRootKey/policy/capability | cannot be omitted/defaulted | trust/evaluability/reasoning | A02,A17 |
| `ValueAdmissionRequest.{abi_version,type_key,value,semantic_environment,trust_environment,dependency_environment,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | projected Delta/Service/embedding policy | typed contextual targeted value admission | request former | admission service | exact expected admission plus type, environments, support, target, role, fragment, root and scope together | exact type/environments/capability | malformed or evaluability missing/unknown/failure | protocol/evaluation/evaluability/trust | A07 |
| `FunctionRequest.{abi_version,symbol_key,arguments}`; `PredicateRequest.{abi_version,symbol_key,arguments}` | `REQUIRED_SEMANTIC` | Delta | exact positional typed invocation | kernel request former | evaluator | signature/admission | exact symbol/version | malformed request | protocol | A07 |
| `FunctionRequest.{binding_key,semantic_environment,dependency_environment}`; `PredicateRequest.{binding_key,semantic_environment,dependency_environment}` | `REQUIRED_SEMANTIC` | Sigma | exact meaning/environment/dependencies and expected complete result | kernel request former | evaluator/result validator | binding/environment/derived-result equality | binding/environment exact | not invocable or malformed result | closure/evaluation/protocol | A06 |
| `FunctionRequest.{trust_environment,capability_target,capability_key}`; `PredicateRequest.{trust_environment,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | Service/embedding policy | requested exact environment-bound binding-target evaluator | kernel request former | evaluator/discovery | role/judgment/target/environment/fragment/scope/root match | exact capability/target/environment | evaluability missing/unknown/failure | evaluability/trust | A02 |
| `ProfileRequest.{abi_version,profile_key,semantic_environment,trust_environment,coverage_subject}` | `REQUIRED_SEMANTIC` | Sigma/embedding policy | exact profile/check subject, environments and expected coverage result | kernel request former | checker | closure/profile/environment/root/result equality | exact profile/environments | open/not invocable/malformed result | closure/profile/trust/protocol | A15 |
| `ProfileRequest.{capability_target,capability_key}` | `REQUIRED_SEMANTIC` | Service | exact profile-target checker class | kernel request former | checker | role/judgment/target/fragment/scope match | exact capability/profile target | evaluability missing | evaluability | A15 |
| `PairAdmissionRequest.{abi_version,pair_key,semantic_environment,trust_environment,complete_dependencies,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | projected Sigma/Service/embedding policy | exact pair-target admission | kernel request former | pair validator | pair closure plus role/judgment/target/environment/fragment/scope/root | exact pair/environments/capability | open/evaluability missing/unknown/failure | closure/reasoning/trust | A13 |
| `AuthorityAdmissionRequest.{abi_version,candidate,environment_without_fact,trust_environment,complete_dependencies,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | projected Sigma/Service/embedding policy | exact non-self-rooting authority-fact admission subject | request former | authority validator | candidate fact absent; exact target/scope/service-use and certificate roots/complete producer independence | exact candidate/excluded environment/capability | open/no fact and no insertion | closure/reasoning/trust | A14,A18 |
| `MigrationAdmissionRequest.{abi_version,migration,semantic_environment,trust_environment,complete_dependencies,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | projected Sigma/Service/embedding policy | exact migration relation admission | request former | migration validator | exact subject/env/target/scope/roots/independence | exact migration/environments/capability | no migration | compatibility/reasoning/trust | A20 |
| `CompatibilityAdmissionRequest.{abi_version,claim,semantic_environment,trust_environment,complete_dependencies,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | Service/embedding policy | exact compatibility-claim admission | request former | compatibility validator | exact subject/env/target/scope/roots/independence | exact claim/environments/capability | no compatibility | compatibility/reasoning/trust | A20 |
| `SemanticExtensionAdmissionRequest.{abi_version,extension,environment_without_extension,trust_environment,complete_dependencies,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | projected owner/Service/embedding policy | exact non-self-supporting extension admission | request former | extension validator | subject excluded from env; exact target/scope/roots/independence | exact extension/environments/capability | incompatible/no effect | compatibility/reasoning/trust | A20 |
| `DiscoveryRequest.{abi_version,target,judgment,semantic_environment,trust_environment,required_fragment,complete_dependency_scope}` | `REQUIRED_SEMANTIC` | Service/embedding policy | one exact environment/root-bound tagged capability query | kernel request former | discovery interface | role/judgment/target/environments/fragment/scope/roots together | exact target/environments/versions | malformed request | discovery/evaluability/trust | A03 |
| `ReasoningRequest.{abi_version,judgment,subjects,semantic_environment,trust_environment,required_fragment,complete_dependencies}` | `REQUIRED_SEMANTIC` | Sigma/embedding policy | one K1 judgment/exact semantic and trust environments | kernel request former | reasoner | closure/taxonomy/dependency/root check | exact subjects/environments | malformed/open/evaluability missing/unknown | structure/reasoning/trust | A18 |
| `ReasoningRequest.{capability_target,capability_key}` | `REQUIRED_SEMANTIC` | Service | exact environment/judgment-target request | kernel request former | reasoner | role/judgment/target/fragment/scope match | exact capability/target | evaluability missing | evaluability | A16 |
| `CertificateValidationRequest.{abi_version,validator_key,certificate_key,envelope_identity,original_request_identity,original_subject,original_subject_identity,claimed_conclusion,validator_capability_target,validator_judgment,validator_service_role,fragment,complete_dependencies,semantic_environment,trust_environment,receiving_rule,service_use_trust_root_keys,service_use_trust_target,certificate_admission_trust_root_key,certificate_admission_trust_target}`; `ReceivingRuleTag` | `DERIVED` | certificate gate | independent typed validator invocation distinct from producer request | exact envelope projection | validator/lifecycle/receiving boundary | field-by-field constructor, complete roots/producer reachability, ordinary validator trust plus independent certificate trust | validator/certificate/original request/environment exact | cannot be supplied; no admission | discovery/trust/reasoning/protocol | A13,A17,A20 |
| `LifecycleState.{declaration_state,binding_state,discovery_state,invocation_state}` | `DERIVED` | K1 carrier | independent lifecycle product | validation relation | status mapper | recompute all four coordinates | exact required key/request | cannot be supplied | coordinate-specific | A01 |
| `DeclarationState.DECLARATION_INVALID.reasons`; `DeclarationState.DECLARATION_NOT_REQUIRED`; `DeclarationState.DECLARED` | `DERIVED` | Delta validation | total target-kind declaration applicability and exact reason set | target/declaration validator | lifecycle | total applicability function then declaration rules/set equality | exact target/declaration versions | cannot be supplied | structure | A01 |
| `BindingState.BINDING_BLOCKED_BY_DECLARATION`; `BindingState.BINDING_NOT_REQUIRED`; `BindingState.BINDING_ABSENT`; `BindingState.BINDING_INCOMPATIBLE.reasons`; `BindingState.SEMANTICALLY_BOUND` | `DERIVED` | Sigma validation | total closure coordinate and exact reason set | binding validator | lifecycle | exact declaration/binding/support/coherence precedence | exact binding versions | cannot be supplied/omitted | closure/structure | A01 |
| `DiscoveryState.DISCOVERY_BLOCKED_BY_DECLARATION`; `DiscoveryState.DISCOVERY_BLOCKED_BY_BINDING`; `DiscoveryState.DISCOVERY_NOT_REQUIRED`; `DiscoveryState.DISCOVERY_FAILED.failure`; `DiscoveryState.DISCOVERY_UNDECIDED.reasons`; `DiscoveryState.CAPABILITY_ABSENT`; `DiscoveryState.CAPABILITY_INCOMPATIBLE.reasons`; `DiscoveryState.CAPABILITY_OUTSIDE_FRAGMENT`; `DiscoveryState.CAPABILITY_DISCOVERED` | `DERIVED` | Service validation | total discovery coordinate, exact failure/uncertainty separation | discovery result validation | lifecycle | exact earlier states plus target/role/judgment/fragment/scope | exact target/capability versions | cannot be supplied/omitted | evaluability/discovery/protocol | A02 |
| `InvocationState.INVOCATION_BLOCKED_BY_DECLARATION`; `InvocationState.INVOCATION_BLOCKED_BY_BINDING`; `InvocationState.INVOCATION_BLOCKED_BY_DISCOVERY`; `InvocationState.INVOCATION_NOT_REQUIRED`; `InvocationState.NOT_INVOCABLE.reasons`; `InvocationState.INVOCABLE_FOR.exact_request`; `InvocationState.COMPLETED.conformant_result`; `InvocationState.INVOCATION_FAILED.{failure_family,reasons}` | `DERIVED` | request/result validation | total invocation coordinate with exact request/result/failure payload and exhaustive completion | request/result validators | lifecycle/status mapper | exact earlier states/request/semantic-result equality, receiving rule, completion class and nonempty reasons | request-bound | cannot be supplied/omitted or remain invocable after completion | evaluation/reasoning/admission/protocol | A16 |
| `ValueAdmissionResult.VALUE_ADMITTED.{type_key,value}` | `REQUIRED_SEMANTIC` | Delta | exact admitted typed value | admission service | request validator | complete equality to expected request/environment admission | request-bound | malformed result | protocol/evaluation | A07 |
| `ValueAdmissionResult.VALUE_NOT_ADMITTED.{type_key,value}` | `REQUIRED_SEMANTIC` | Delta | exact rejected typed-domain membership | admission service | request validator | complete equality to expected request/environment nonmembership | request-bound | malformed result | protocol/evaluation | A07 |
| `ValueAdmissionResult.ADMISSION_ERROR.evaluation_errors` | `REQUIRED_SEMANTIC` | Delta | admission failure, not nonmembership | admission service | request validator | nonempty stable error set | request-bound | malformed result | evaluation/protocol | A07 |
| `TermResult.TERM_VALUE.value` | `REQUIRED_SEMANTIC` | K1 carrier | admitted exact term value | literal/function meaning/service | term evaluator | carrier/type plus complete equality to exact bound logical relation | request/environment-bound | malformed result | protocol/evaluation | A10 |
| `TermResult.TERM_ERROR.evaluation_errors` | `REQUIRED_SEMANTIC` | K1 carrier | exact term error with no value | function meaning/service | term evaluator | nonempty stable error set plus complete equality to exact bound logical relation | request/environment-bound | malformed result | evaluation/protocol | A10 |
| `Eval.VALUE.{truth,evidence_refs,unknown_reasons}` | `REQUIRED_SEMANTIC` | K1 carrier | exact truth plus complete metadata | predicate/pair-occurrence service | kernel connective evaluator | carrier invariants plus complete equality to exact bound/derived logical relation | request/environment-bound | malformed result | evaluation/protocol | A10 |
| `Eval.ERROR.{evaluation_errors,evidence_refs,unknown_reasons}` | `REQUIRED_SEMANTIC` | K1 carrier | exact evaluation failure and complete metadata | predicate/pair-occurrence service | kernel connective evaluator | nonempty invariants plus complete equality to exact bound/derived logical relation | request/environment-bound | malformed result | evaluation/protocol | A10 |
| `FormulaResult` | `DERIVED` | K1 carrier | kernel formula result is exact Eval | kernel T1--T4/A1--A2 | truth/acceptance boundary | definitional equality to Eval | environment-bound | cannot be independently supplied | evaluation | A10 |
| `ProfileResult.PROFILE_COMPLETE.{profile_key,evidence_refs}` | `REQUIRED_SEMANTIC` | K1 carrier | exact full coverage | checker | profile boundary | carrier plus complete equality to exact coverage meaning | request/environment-bound | malformed result | profile/protocol | A15 |
| `ProfileResult.PROFILE_INCOMPLETE.{profile_key,missing_dimensions}` | `REQUIRED_SEMANTIC` | K1 carrier | exact known omission | checker | profile boundary | carrier plus complete equality to exact coverage meaning | request/environment-bound | malformed result | profile/protocol | A15 |
| `ProfileResult.PROFILE_UNKNOWN.{profile_key,unknown_reasons}` | `REQUIRED_SEMANTIC` | K1 carrier | invoked exact inconclusiveness | checker | profile boundary | carrier plus complete equality to exact coverage meaning | request/environment-bound | malformed result | profile/protocol | A15 |
| `ProfileResult.EVALUATION_ERROR.evaluation_errors` | `REQUIRED_SEMANTIC` | K1 carrier | concrete profile failure | checker | profile boundary | nonempty stable error set | request-bound | malformed result | evaluation | A15 |
| `ProfileResult.REASONING_ERROR.reasoning_errors` | `REQUIRED_SEMANTIC` | K1 carrier | symbolic profile failure | checker | profile boundary | nonempty stable error set | request-bound | malformed result | reasoning | A15 |
| `PairValidationResult.PAIR_COHERENCE_ADMITTED.{pair_key,certificate_key}` | `REQUIRED_SEMANTIC` | Sigma admission | exact positive pair binding | pair validator | pair binding/lifecycle | exact request and admitted coherence kind | pair/request-bound | no admission | reasoning | A13 |
| `PairValidationResult.PAIR_INCOHERENCE_ADMITTED.{pair_key,certificate_key,admitted_trace,scope_aggregate_eval,occurrence_eval}` | `REQUIRED_SEMANTIC` | Sigma admission | typed exact pair-negative result | pair validator | binding lifecycle | admitted trace, exact T3/A1 aggregate, unequal complete Eval records | pair/request-bound | no incompatibility | evaluation/reasoning | A13 |
| `PairValidationResult.PAIR_VALIDATION_REJECTED.{pair_key,rejection_reasons}`; `PairValidationResult.EVALUATION_ERROR.evaluation_errors`; `PairValidationResult.REASONING_ERROR.reasoning_errors` | `REQUIRED_SEMANTIC` | K1 carrier | generic rejection/failure proves no pair result | pair validator | pair lifecycle | echoed pair and nonempty exact reason/error sets | pair/request-bound | pair remains open | evaluation/reasoning | A13 |
| `AuthorityAdmissionResult.{AUTHORITY_FACT_ADMITTED.{authority_fact_key,certificate_key},AUTHORITY_FACT_NOT_ADMITTED.{authority_fact_key,rejection_reasons},REASONING_ERROR.reasoning_errors}` | `REQUIRED_SEMANTIC` | Sigma admission | exact fact admission or no fact | authority validator | authority map/closure | exact request/certificate and nonempty rejection/error sets | fact/request-bound | no fact | closure/reasoning | A14 |
| `MigrationAdmissionResult.{MIGRATION_RELATION_ADMITTED.{migration_key,certificate_key},MIGRATION_RELATION_NOT_ADMITTED.{migration_key,rejection_reasons},EVALUATION_ERROR.evaluation_errors,REASONING_ERROR.reasoning_errors}` | `REQUIRED_SEMANTIC` | Sigma admission | exact migration relation result | migration validator | migration boundary | exact request/certificate and nonempty sets | migration-bound | no migration | compatibility/evaluation/reasoning | A20 |
| `CompatibilityAdmissionResult.{COMPATIBILITY_CLAIM_ADMITTED.{claim_key,certificate_key},COMPATIBILITY_CLAIM_NOT_ADMITTED.{claim_key,rejection_reasons},REASONING_ERROR.reasoning_errors}` | `REQUIRED_SEMANTIC` | Service admission | exact compatibility result | compatibility validator | compatibility boundary | exact request/certificate and nonempty sets | claim-bound | no compatibility | compatibility/reasoning | A20 |
| `SemanticExtensionAdmissionResult.{SEMANTIC_EXTENSION_ADMITTED.{extension_key,certificate_key},SEMANTIC_EXTENSION_NOT_ADMITTED.{extension_key,rejection_reasons},REASONING_ERROR.reasoning_errors}` | `REQUIRED_SEMANTIC` | owning layer admission | exact extension effect admission | extension validator | package/target | exact request/certificate and nonempty sets | extension-bound | incompatible/no effect | compatibility/reasoning | A20 |
| `DiscoveryResult.EXACT_TARGET_FOUND.{target,matching_capabilities}` | `REQUIRED_SEMANTIC` | Service | exact environment/root-compatible capability found | discovery interface | lifecycle | echoed target plus nonempty set jointly matching role/judgment/environment/fragment/scope/roots | request-bound exact target/environments | malformed result | discovery/protocol/trust | A02 |
| `DiscoveryResult.EXACT_TARGET_ABSENT.target` | `REQUIRED_SEMANTIC` | Service | exact target absent | discovery interface | lifecycle | echoed target and target-kind absence | request-bound exact target | malformed result | discovery | A01 |
| `DiscoveryResult.DISCOVERY_UNDECIDED.{target,reasons}` | `REQUIRED_SEMANTIC` | Service | exact discovery uncertainty | discovery interface | lifecycle | echoed target/nonempty stable reasons | request-bound exact target | malformed result | discovery | A03 |
| `DiscoveryResult.INCOMPATIBLE_DECLARATION.{target,conflicts}`; `DiscoveryResult.INCOMPATIBLE_BINDING.{target,conflicts}` | `REQUIRED_SEMANTIC` | Service | exact incompatibility family | discovery interface | lifecycle | echoed target/nonempty exact conflicts | request-bound exact target | malformed result | structure/compatibility | A04 |
| `DiscoveryResult.TARGET_PRESENT_SERVICE_ABSENT.{target,requested_judgment}` | `REQUIRED_SEMANTIC` | Service | meaning/target present but service absent | discovery interface | lifecycle | echoed target/exact judgment/no compatible service | request-bound exact target | malformed result | evaluability | A03 |
| `DiscoveryResult.SERVICE_OUTSIDE_FRAGMENT.{target,capability_key,requested_fragment}`; `DiscoveryResult.SERVICE_INCOMPATIBLE.{target,capability_key,reasons}` | `REQUIRED_SEMANTIC` | Service | exact service fragment/environment/root incompatibility | discovery interface | lifecycle | echoed target/exact capability and fragment or nonempty incompatibility reasons | request-bound exact target/environments | malformed result | evaluability/trust | A16 |
| `DiscoveryResult.DISCOVERY_FAILURE.{target,failure_kind,reasons}` | `REQUIRED_SEMANTIC` | Service | discovery protocol/transport failure | discovery interface | lifecycle | echoed target/exact failure tag/nonempty reasons | request-bound exact target | malformed result | discovery/protocol/transport | A03 |
| `ReasoningResult.ADMITTED_JUDGMENT.{judgment,certificate_key}` | `REQUIRED_SEMANTIC` | K1 carrier | exact admitted decisive judgment | reasoner/admission | kernel reasoning boundary | request taxonomy and admitted certificate | request-bound | malformed result | reasoning/protocol | A16 |
| `ReasoningResult.COMPLETED_INCONCLUSIVE.unknown_reasons` | `REQUIRED_SEMANTIC` | K1 carrier | invoked partial/outside-complete inconclusiveness | reasoner | kernel reasoning boundary | nonempty reasons plus compatible invoked capability | request-bound | malformed result | reasoning/protocol | A19 |
| `ReasoningResult.EVALUATION_ERROR.evaluation_errors` | `REQUIRED_SEMANTIC` | K1 carrier | concrete validation failure | reasoner/admission | kernel reasoning boundary | nonempty stable errors | request-bound | malformed result | evaluation | A17 |
| `ReasoningResult.REASONING_ERROR.reasoning_errors` | `REQUIRED_SEMANTIC` | K1 carrier | service/validator/protocol failure | reasoner/admission | kernel reasoning boundary | nonempty stable errors | request-bound | malformed result | reasoning | A16 |
| `EvidenceRef.{issuer_scope,evidence_namespace,local_identity,schema_binding}`; `UnknownReason`, `EvaluationErrorReason`, `ReasoningErrorReason`, and `CertificateRejectionReason` fields `{issuer_scope,taxonomy_key,semantic_parameters}`; `InterfaceFailureReason.{issuer_scope,reason_code,capability_identity,request_identity,expected_contract_identity,offending_result_identity}` | `REQUIRED_SEMANTIC` | K1 carrier | stable set-member identities and canonical ABI interface failures | meaning/service/validator or fixed ABI constructor | result/certificate validators/status mapper | component equality; interface reason requires total canonical constructor | issuer and referenced contract/request/result exact | malformed result/failure | evaluation/reasoning/protocol | A10,A11 |
| `ConflictRef.{conflict_kind,involved_identities}` | `REQUIRED_SEMANTIC` | K1 carrier | exact order-independent conflict identity | composition validator | discovery/lifecycle | tag plus exact set equality | involved versions exact | no conflict | structure/compatibility | A20 |
| `CertificateEnvelope.{certificate_key,certificate_kind,request_binding,subjects,environment,capability_key,fragment,dependencies,claimed_conclusion,validator_key,trust_root_key,abstraction_class,payload,evidence_refs}` | `REQUIRED_SEMANTIC` | Service | exact proof admission | certificate issuer | admission | kind-specific rule, exact root scope and producer independence | exact env/capability/root | no admission | trust/reasoning | A17 |
| `CertificateAdmission.ADMITTED.{certificate_key,admitted_conclusion}` | `REQUIRED_SEMANTIC` | K1 carrier | admitted proof/witness/counterexample remains kind-specific | trusted validator | kernel judgment gate | exact certificate/kind/conclusion receiving rule | certificate-bound | no admission | reasoning | A17 |
| `CertificateAdmission.MALFORMED_ENVELOPE.reasons` | `REQUIRED_SEMANTIC` | K1 carrier | malformed object proves nothing | envelope validator | package/lifecycle | nonempty interface-failure reasons | no semantic certificate identity required | no admission | protocol | A13 |
| `CertificateAdmission.REJECTED_NONDECISIVE.{certificate_key,rejection_reasons}` | `REQUIRED_SEMANTIC` | K1 carrier | rejected evidence proves neither claim nor negation | trusted validator | kernel judgment gate | nonempty stable rejection reasons | certificate-bound | no admission | reasoning/nonconformance | A13 |
| `CertificateAdmission.EVALUATION_ERROR.{certificate_key,evaluation_errors}` | `REQUIRED_SEMANTIC` | K1 carrier | concrete validator failure proves nothing | trusted validator | kernel judgment gate | nonempty stable errors | certificate-bound | no admission | evaluation | A17 |
| `CertificateAdmission.REASONING_ERROR.{certificate_key,reasoning_errors}` | `REQUIRED_SEMANTIC` | K1 carrier | validator/protocol failure proves nothing | trusted validator | kernel judgment gate | nonempty stable errors | certificate-bound | no admission | reasoning | A17 |
| `EventValue.{event_key,payload}`; `TraceEvent.{event_value,actor?}` | `REQUIRED_SEMANTIC` | Delta | typed event and optional actor | outcome former | outcome/auth/pair | event admission | exact EventKey | malformed outcome | evaluation | A12 |
| `SourceRef.{issuer,source_kind,stable_source_identity,provenance_facts}`; `AuthorityRef.{owner,authority_namespace,stable_attestation_identity}` | `REQUIRED_SEMANTIC` | Sigma | typed producer-owned provenance separate from authority | exact issuer/owner | Origins/closure/producer derivation | self-contained/exact owner and component equality | issuer/owner/attestation identity exact | source unresolved before Contract; authority open | representation/closure | A14 |
| `AuthorityFactBinding.authority_fact_key` | `REQUIRED_SEMANTIC` | Sigma | exact adoption/choice fact identity | authority subject former | closure/adoption | exact admitted tuple | AuthorityFactKey exact | open/no fact | closure/reasoning | A14 |
| `AuthorityFactBinding.admitted_attestation_refs` | `DERIVED` | Sigma admission | nonempty union of independently admitted evidence | authority validators/composition | closure/audit | group by fact key and union admitted certificate refs | certificate sets not identity | no fact if empty | closure/reasoning | A14 |
| `CompatibilityClaim.{claim_key,source_abi,target_abi,source_keys,target_keys,compatibility_contract,certificate_key,validator_key,trust_root_key}` | `REQUIRED_SEMANTIC` | Service | protocol compatibility plus mandatory independently bound validation | claimant | discovery/migration | semantic proper support excludes the exact separately projected certificate/validator/root triple; request/result/certificate/root admission checks all three | versions remain distinct; validation keys exact | no compatibility | compatibility/reasoning | A20 |
| `MigrationDeclaration.{migration_key,source_environment,target_environment,semantic_relation,relation_contract,certificate_key}` | `REQUIRED_SEMANTIC` | Sigma | explicit semantics-preserving/change relation plus separately bound proof | migration author | binding analysis | acyclic semantic source/target/support plus exact non-proper certificate lookup/admission | source/target/certificate exact | no migration | compatibility/reasoning | A20 |
| `MigrationDeclaration.{validator_key,trust_root_key}` | `REQUIRED_SEMANTIC` | Service | independently trusted migration validation | migration author | certificate gate | exact non-proper validator/root reference, target/root scope, lookup and producer independence | exact capability/root version | no migration | compatibility/reasoning | A20 |
| `SemanticExtension.{extension_key,target_record_identity,owner_layer,semantic_effect,payload}` | `REQUIRED_SEMANTIC` | declared owner | explicit semantic extension | extension owner | package validator | exact support, target and owner rule | exact namespace/version | no extension | compatibility | A20 |
| `SemanticExtension.{certificate_key,validator_key,trust_root_key}` | `REQUIRED_SEMANTIC` | Service | independently trusted semantic-extension validation | extension owner | package validator | exact non-proper certificate/validator/root projection, admission target/root scope, lookup and producer independence | exact certificate/capability/root versions | incompatible if absent/unadmitted | compatibility/reasoning | A20 |
| `InterfaceFailure.{domain,kind,reasons}`; `InterfaceFailureCode`; `InterfaceFailureReason.trust_root_status_reason` | `REQUIRED_SEMANTIC` | K1 carrier | exact domain/kind failure outside truth with optional closed root-local coordinate | interface boundary | lifecycle/status mapper | allowed tags and nonempty canonical reason set; only exact request-time root incompatibility/failure projections carry a root reason | request/expected-contract/offender/root-bound | no logical result | protocol/transport/trust/discovery | A10,A17 |
| `ABI_REASON_ISSUER`; `ABI_ROOT_DISCOVERY_UNRESOLVED`; `failureReason`; `rootUndecidedReason`; `rootUndecidedReasons`; `rootIncompatibilityReason`; `rootIncompatibilityReasons`; `rootFailureReason`; `rootFailure`; `resultFailure`; `expectedContract`; `toEvaluationReason`; `toReasoningReason`; `evaluationReasons`; `reasoningReasons`; total service-role failure projection | `DERIVED` | K1 interface boundary | deterministic nonempty evaluation/reasoning and root discovery-uncertainty/incompatibility/failure mapping with discarded unequal result | §5.4 fixed ABI constructors | lifecycle and result projection | recompute pointwise, retain exact root-local coordinate, deduplicate exact reasons, enforce all eleven role rows and three distinct root-status projections | request/capability/contract/offender/root exact | cannot be supplied; trust/discovery pre-invocation produces no K1 result | evaluation/reasoning/protocol/trust/discovery | A10,A15,A16,A17 |
| challenge IDs, expected mappings/results, gold Contracts, hidden targets, undeclared outcome/evidence access, caller `chi_C`, caller replacement dependencies, caller event-class flags | `EXCLUDED` | Excluded | anti-oracle and frozen K1 ownership | none | none | presence rejects | never identity | always absent | malformed | A06 |
| implicit aliases, wildcard/`latest` versions, discovery-order or first-found selection, silent shadowing, unrecognized fields | `EXCLUDED` | Excluded | exact identity/conflict behavior | none | none | presence/use rejects | no equality role | always absent | compatibility/protocol | A20 |
| byte encoding, field serialization order, service endpoint as a semantic field, loader, repository, retry scheduler, deployment topology | `EXCLUDED` | Excluded | no K1 semantic role | none | none | outside v0 | no identity role | always absent | transport outside ABI | A03 |
| request IDs, timestamps, logs, timing, retry counters, display names outside `Diagnostics` | `EXCLUDED` | Excluded | cannot affect judgment | none | none | presence in semantic record rejects | no identity role | always absent | protocol | A11 |
| independent occurrence meaning beside a pair-owned occurrence binding; bare pair-coherence claim | `EXCLUDED` | Excluded | non-circular exact coherence | none | none | conflict/reject | no valid identity | always absent | structure/reasoning | A13 |
<!-- LEDGER-END -->

Ledger counts: **96 `REQUIRED_SEMANTIC`; 26 `DERIVED`; 2
`OPTIONAL_DIAGNOSTIC`; 5 `EXCLUDED`** (129 rows). The reproducible convention
counts each Markdown body row strictly between `LEDGER-BEGIN` and
`LEDGER-END` once according to the exact disposition in its second cell; the
header and separator are excluded. Grouped dot-qualified fields in one row
share that disposition independently; no field occurs in another ledger row.

## 3. Exact identity, declarations, dependencies, and versioning

### 3.1 Equality, namespace ownership, and kind separation

Every key compares by the component equality in section 2. Namespaces are
owned by their exact `PluginKey`; a record may declare only keys under that
owner. `TYPE`, `LITERAL`, `FUNCTION`, `PREDICATE`, and `EVENT` are
disjoint identity kinds even when all text atoms match. A `SymbolKey` must
have the same plugin, namespace, local name, and function/predicate kind as its
`DeclarationKey`. An `EventKey` has exactly one matching event declaration.

Display names, prose, aliases, signatures, service locations, and discovery
order are not identity. An `AliasBinding` is only an explicit presentation
mapping to one exact target; it cannot change the target key, kind, or version.
Its identity is `(owning PluginKey,alias_namespace,alias_atom)`. Two aliases
with that identity and different targets or target kinds conflict.

### 3.2 Declaration validation

Declaration validation is total:

1. validate the package `AbiVersion` and owner `PluginKey`;
2. require exact key ownership and kind;
3. require every derived proper declaration dependency, then take its finite
   transitive closure over proper edges; every self-edge or declaration or
   semantic dependency cycle is
   `MALFORMED(dependency cycle)`; the definitional occurrence construction
   is an ownership rule, not a dependency back-edge;
4. validate literal types, ordered function/predicate argument types, function
   result types, Boolean predicate result kind, and position-aligned facet
   declarations;
5. validate event payload type and immutable class;
6. validate a pair's distinct members, exact derived signatures/facets,
   nonempty controlled-key set, and every controlled declaration.

`proper_declaration_dependencies` is a derived projection, not authority:
the validator recomputes dependencies from the record's types, signatures,
value-admission contract, event payload, and pair members and requires exact
equality before taking the transitive closure.
For a `TypeDeclaration`, the value-admission contract's total support may
contain only its owner and Delta declaration dependencies; any binding,
profile, pair, service, or semantic-extension support violates layer ownership.
After projecting the exact declaration members of that support, equality with
`proper_declaration_dependencies` is required. Thus type admission cannot hide
a Sigma meaning or service lookup.

Type value admission is an abstract exact membership relation, not an
evaluator. A value is well typed exactly when the relation says so. A rejected
choice alternative, binding, argument, event payload, certificate value, or
result value makes the containing use malformed; it never becomes an unknown
fact.

No evidence, unknown/error, denotation, profile, or availability field is
needed for `DECLARED`. Conversely, no meaning or service can repair a missing
or incompatible declaration.

### 3.3 Total semantic support and mechanical dependencies

`ContractSpec` is stratified below every record that contains it. Let
`Q=keys(c.observation_queries)`. Its relation is typed only as

```text
c.logical_relation :
  c.primary_input_domain * DependencyObservationEnvironment[Q]
    -> c.codomain
```

and receives neither the containing binding nor any `ContractSpec`,
`SemanticEnvironment`, `CapabilityTarget`, `TrustTarget`, request, or
relation value. `DependencyObservationQuery.input_projection` receives only
the explicit primary input. Query equality is extensional equality of this
projection and exact equality of the expected observation kind. Relation
equality is extensional equality for every admitted primary input and every
well-typed finite observation map on `Q`, including complete values, result
tags, evidence, unknown-reason, evaluation-error, and reasoning-error sets.
This equality is mathematical; K2 claims neither an algorithm nor a byte
representation for deciding it.

Every use site fixes one exact `ContractRole`; a producer cannot choose it.
The assignment is total:

| Owner and field | Required `ContractRole` |
|---|---|
| `Delta TypeDeclaration.admitted_value_domain` | `TYPE_ADMISSION` |
| `Sigma SemanticBinding.meaning_contract`, by binding kind | `LITERAL_MEANING`, `FUNCTION_MEANING`, or `PREDICATE_MEANING` |
| pair-owned occurrence `meaning_contract` | `OCCURRENCE_MEANING` |
| `Sigma ProfileBinding.coverage_meaning` | `PROFILE_COVERAGE` |
| every Sigma `evidence_schema` or model `evidence_contract` | `EVIDENCE_SCHEMA` |
| every Sigma `access_boundary` | `ACCESS_BOUNDARY` |
| every Sigma `unknown_contract` | `UNKNOWN_BEHAVIOR` |
| every Sigma `evaluation_error_contract` or model `error_contract` | `EVALUATION_ERROR_BEHAVIOR` |
| `ProfileBinding.reasoning_error_contract` | `REASONING_ERROR_BEHAVIOR` |
| `CapabilityDescriptor.sound_fragment`; every request/envelope fragment that must equal it | `SOUND_FRAGMENT` |
| `CapabilityDescriptor.complete_fragment` | `COMPLETE_FRAGMENT` |
| `CapabilityDescriptor.required_evidence` | `REQUIRED_EVIDENCE` |
| `CapabilityDescriptor.failure_contract` | `SERVICE_FAILURE_BEHAVIOR` |
| `CompatibilityClaim.compatibility_contract` | `COMPATIBILITY_VALIDATION` |
| `MigrationDeclaration.relation_contract` | `MIGRATION_RELATION` |
| `SemanticExtension.semantic_effect` | `SEMANTIC_EXTENSION_EFFECT` |
| `SemanticExtension.payload` | `SEMANTIC_EXTENSION_PAYLOAD` |

The field's `owner_layer`, `contract_role`, and
`contract_key.contract_role` must equal this row. All other layer/role pairs
are invalid. Model-facing contracts do not introduce new specifications:
their three contracts must be exactly the occurrence/ordinary binding's
`EVIDENCE_SCHEMA`, `UNKNOWN_BEHAVIOR`, and
`EVALUATION_ERROR_BEHAVIOR` specifications.

The allowed-observation matrix is total. Each cell is the complete set of
allowed `(DependencyKey tag -> DependencyObservationKind)` pairs; every pair
not displayed in its cell is `INVALID_OBSERVATION`, making the
`ContractSpec` and its containing binding/descriptor malformed.

| Owner layer | Exact roles | Complete allowed key/kind pairs |
|---|---|---|
| `Delta` | `TYPE_ADMISSION`, `SEMANTIC_EXTENSION_EFFECT`, `SEMANTIC_EXTENSION_PAYLOAD` | `ABI,PLUGIN -> IDENTITY_PRESENCE`; `DECLARATION,SYMBOL,EVENT,PAIR_DECLARATION -> DECLARATION_SHAPE`; `DECLARATION[TYPE] -> TYPE_ADMISSION_FACT` |
| `Sigma` | `LITERAL_MEANING`, `FUNCTION_MEANING`, `PREDICATE_MEANING`, `OCCURRENCE_MEANING`, `PROFILE_COVERAGE`, `EVIDENCE_SCHEMA`, `ACCESS_BOUNDARY`, `UNKNOWN_BEHAVIOR`, `EVALUATION_ERROR_BEHAVIOR`, `REASONING_ERROR_BEHAVIOR`, `MIGRATION_RELATION`, `SEMANTIC_EXTENSION_EFFECT`, `SEMANTIC_EXTENSION_PAYLOAD` | `ABI,PLUGIN,PROFILE,PAIR -> IDENTITY_PRESENCE`; `DECLARATION,SYMBOL,EVENT,PAIR_DECLARATION -> DECLARATION_SHAPE`; `DECLARATION[TYPE] -> TYPE_ADMISSION_FACT`; `BINDING -> VALUE_RESULT, TERM_RESULT, EVAL_RESULT, or EVAL_RESULT_SEQUENCE`; `PROFILE_BINDING -> PROFILE_RESULT`; `PAIR_BINDING -> PAIR_RESULT or EVAL_RESULT` |
| `Service` | `SOUND_FRAGMENT`, `COMPLETE_FRAGMENT`, `REQUIRED_EVIDENCE`, `SERVICE_FAILURE_BEHAVIOR`, `COMPATIBILITY_VALIDATION`, `SEMANTIC_EXTENSION_EFFECT`, `SEMANTIC_EXTENSION_PAYLOAD` | all Sigma-cell pairs; plus `SERVICE,CAPABILITY,CERTIFICATE -> IDENTITY_PRESENCE`; `MIGRATION -> MIGRATION_STATUS`; `COMPATIBILITY_CLAIM -> COMPATIBILITY_STATUS`; `SEMANTIC_EXTENSION -> SEMANTIC_EXTENSION_STATUS`; `CERTIFICATE -> CERTIFICATE_STATUS`; `RESULT -> VALUE_RESULT, TERM_RESULT, EVAL_RESULT, PROFILE_RESULT, PAIR_RESULT, MIGRATION_STATUS, COMPATIBILITY_STATUS, SEMANTIC_EXTENSION_STATUS, or CERTIFICATE_STATUS` |

In particular, no Sigma role can observe `SERVICE`, `CAPABILITY`, discovery,
trust policy/root state, certificate state, authority-fact presence, lexical
state, or choice state. `AUTHORITY_FACT`, `LEXICAL_BINDING`,
`CHOICE_BINDING`, `TRUST_POLICY`, and `TRUST_ROOT` are invalid observation
keys for every role. Runtime state, trace, evidence, and choice values enter a
denotational Sigma relation only through its declared typed primary/positional
input. A lower binding result is permitted only when its query projection is
an exact function of that primary input. K1 applies the already derived
`chi_C` before formula evaluation; neither `chi_C` nor a choice value is an
observation side channel. Structural choice, authority, trust, capability,
discovery, and validation checks occur outside denotational `ContractSpec`
relations. Every semantic record allowed by the Sigma cell is a displayed
field/member of `SemanticEnvironment`, and therefore participates in
`SemanticEnvironmentIdentity`.

For every relation, including a constant relation, define:

```text
freeDependencies(c) = {
  d in keys(c.observation_queries) |
  there exist an admitted primary input x and well-typed finite maps O1,O2
  with the same exact key domain keys(c.observation_queries), differing only
  at d, for which c.logical_relation(x,O1) != c.logical_relation(x,O2)
}

support(c) = freeDependencies(c)
CONTRACT_SPEC_CONFORMANT(c) iff
  c.contract_key.owner_plugin owns c, c.owner_layer is its enclosing layer,
  c.contract_key.contract_role = c.contract_role and the use-site assignment
    and complete allowed-observation matrix above both hold,
  keys(c.observation_queries) = support(c),
  every query kind is valid for its exact key, and support(c) is finite
```

Thus neither a stated dependency set nor an unused query can enlarge support,
and omission cannot narrow it. `support(c)` is a derived projection, not a
field or producer assertion. Extensional equality of two `ContractSpec`s is
field equality of `contract_key`, owner layer, primary-domain and codomain
identities, query map, and logical relation. Since none of those fields has a
`ContractSpec` or semantic-environment type, this equality is finite and
non-recursive even when a `SemanticEnvironment` contains finitely many
bindings that contain such specifications.

For a conformant record graph, derive observations rather than passing records
to a relation. First apply the owner/role matrix above. If it rejects `(d,q)`,
`observationAt(d,q,x,U)=INVALID_OBSERVATION(d,q.expected_kind)`. Otherwise the
following equations are total; a missing/ambiguous record returns the exact
`recordAt` invalid status rather than a value:

```text
ABI, PLUGIN, PROFILE, PAIR with IDENTITY_PRESENCE
  -> IDENTITY_PRESENT(the exact key)
SERVICE, CAPABILITY with IDENTITY_PRESENCE
  -> IDENTITY_PRESENT(the exact derived service or descriptor key)
DECLARATION, SYMBOL, EVENT, PAIR_DECLARATION with DECLARATION_SHAPE
  -> DECLARATION_OBS(the exact type/signature/facets/event class/pair members
                     and controlled keys, excluding every ContractSpec)
DECLARATION(type) with TYPE_ADMISSION_FACT
  -> TYPE_ADMISSION_OBS for q.input_projection(x)
BINDING with VALUE_RESULT
  -> VALUE_OBS(the exact lower admitted value)
BINDING with TERM_RESULT
  -> TERM_OBS(the exact lower TermResult)
BINDING with EVAL_RESULT
  -> EVAL_OBS(the exact lower Eval)
BINDING with EVAL_RESULT_SEQUENCE
  -> EVAL_SEQUENCE_OBS(the exact position-preserving finite Eval sequence)
PROFILE_BINDING with PROFILE_RESULT
  -> PROFILE_OBS(the exact lower ProfileResult)
PAIR_BINDING with PAIR_RESULT
  -> PAIR_OBS(the exact lower PairValidationResult)
PAIR_BINDING with EVAL_RESULT
  -> EVAL_OBS(the exact pair-owned occurrence result)
MIGRATION with MIGRATION_STATUS
  -> MIGRATION_OBS(ADMITTED|NOT_ADMITTED)
COMPATIBILITY_CLAIM with COMPATIBILITY_STATUS
  -> COMPATIBILITY_OBS(ADMITTED|NOT_ADMITTED)
SEMANTIC_EXTENSION with SEMANTIC_EXTENSION_STATUS
  -> SEMANTIC_EXTENSION_OBS(ADMITTED|NOT_ADMITTED)
CERTIFICATE with IDENTITY_PRESENCE
  -> IDENTITY_PRESENT(the exact CertificateKey)
CERTIFICATE with CERTIFICATE_STATUS
  -> CERTIFICATE_OBS(ADMITTED|REJECTED_NONDECISIVE)
RESULT with VALUE_RESULT | TERM_RESULT | EVAL_RESULT | PROFILE_RESULT |
            PAIR_RESULT | MIGRATION_STATUS | COMPATIBILITY_STATUS |
            SEMANTIC_EXTENSION_STATUS | CERTIFICATE_STATUS
  -> the correspondingly tagged exact lower observation, or the exact
     LOWER_EVALUATION_ERROR/LOWER_REASONING_ERROR carried by that result
MODEL_CONTRACT, ALIAS, AUTHORITY_FACT, LEXICAL_BINDING, CHOICE_BINDING,
TRUST_POLICY, TRUST_ROOT, CONTRACT_SPEC, REQUEST, CARRIER
  -> INVALID_OBSERVATION for every observation kind
every listed key tag with any other observation kind
  -> INVALID_OBSERVATION
```

Thus `observationAt` covers every `DependencyKey` constructor, including the
K1 syntax-facet `PROFILE` and `PAIR` tags. Separately carried operation roots
may be validation references, but no logical relation can inspect their records,
contracts, trust permissions, authority, lexical/choice state, or
environments. Any invalid result makes the `ContractSpec` malformed before
its relation is evaluated.

Let the finite proper-dependency graph in the exact universe `U` be acyclic.
For `(c,x)`, construct `dependencyObservations(c,x,U)` in any topological
order of the sub-DAG induced by `support(c)`: apply each pure deterministic
input projection and observation producer only after every predecessor it
uses has been derived. Each producer depends solely on `x` and already fixed
predecessor observations. Therefore, by induction over any two valid
topological orders, every minimal node has the same value and each later node
has the same predecessor map and value; all valid orders produce the same
exact finite `DependencyObservationEnvironment`. The resulting map domain is
exactly `support(c)`, and equality is domain plus complete value equality at
every key. If finiteness, acyclicity, purity, determinism, predecessor-only
dependence, or this confluence premise fails, the `ContractSpec` is malformed.
The relation is then invoked as
`c.logical_relation(x,dependencyObservations(c,x,U))`.

A missing Delta declaration makes observation derivation malformed. A missing
required binding/profile/pair meaning makes its owner open and the outer
relation is not invoked. A missing service/capability makes evaluability
missing; a missing certificate or admission record grants no admission. A
lower `TERM_ERROR`, `Eval.ERROR`, profile error, or exact admission error is
retained as the corresponding typed lower observation. An interface failure
aborts observation construction and is projected by the total role mapping in
§5.4; it is never an absent observation or an invented logical result. These
rules are exact for empty support as well: the sole observation environment is
the empty map.

This is a well-founded semantic stratification, not an opaque handle. A
relation may observe only results/values for its exact admitted support, and
never equality or contents of the environment that contains it. Every
logical-contract field uses this rule: type admission; literal/function/
predicate and occurrence meanings; profile coverage; evidence, access,
unknown and failure behavior; fragments and required evidence; compatibility;
migration; and semantic-extension effects. Trust remains a separate exact
admission premise and is forbidden from every `ContractSpec` support.

Record identity, root ownership, and subject reference are three different
total functions. `RecordIdentity` is the following disjoint finite algebra:

```text
RecordIdentity =
    ABI_RECORD(AbiVersion) | PACKAGE_RECORD(AbiVersion,PluginKey)
  | DECLARATION_RECORD(DeclarationKey)
  | PAIR_DECLARATION_RECORD(EventScopePairKey)
  | BINDING_RECORD(BindingKey) | PAIR_BINDING_RECORD(EventScopePairKey)
  | PROFILE_BINDING_RECORD(ProfileKey)
  | MODEL_CONTRACT_RECORD(ModelContractKey) | ALIAS_RECORD(AliasKey)
  | SERVICE_RECORD(ServiceKey) | CAPABILITY_RECORD(CapabilityKey)
  | CERTIFICATE_RECORD(CertificateKey)
  | AUTHORITY_FACT_RECORD(AuthorityFactKey)
  | MIGRATION_RECORD(MigrationKey)
  | COMPATIBILITY_RECORD(CompatibilityClaimKey)
  | SEMANTIC_EXTENSION_RECORD(SemanticExtensionKey)
  | CONTRACT_SPEC_RECORD(ContractSpecKey)
  | SEMANTIC_ENVIRONMENT_RECORD(SemanticEnvironmentIdentity)
  | TRUST_ENVIRONMENT_RECORD(TrustEnvironmentIdentity)
  | DEPENDENCY_ENVIRONMENT_RECORD(exact DependencyEnvironment identity)
  | OBSERVATION_ENVIRONMENT_RECORD(
      exact DependencyObservationEnvironment identity)
  | TRUST_POLICY_RECORD(TrustPolicyKey) | TRUST_ROOT_RECORD(TrustRootKey)
  | LEXICAL_BINDING_RECORD(LexicalBindingKey)
  | CHOICE_BINDING_RECORD(ChoiceBindingKey)
  | REQUEST_RECORD(RequestIdentity) | RESULT_RECORD(ResultIdentity)
  | LIFECYCLE_RECORD(exact target/request identity)
  | OUTCOME_RECORD(exact Outcome identity)
  | EVENT_VALUE_RECORD(exact EventValue identity)
  | TRACE_EVENT_RECORD(exact TraceEvent identity)
  | SOURCE_RECORD(exact SourceRef identity)
  | AUTHORITY_REF_RECORD(exact AuthorityRef identity)
  | EVIDENCE_RECORD(EvidenceRef)
  | REASON_RECORD(reason sort, exact reason identity)
  | CONFLICT_RECORD(ConflictRef)
```

`recordIdentity(r)` returns the matching constructor for every logical record
listed in §2.1: declaration variants share `DECLARATION_RECORD(r.key)`;
the derived service and trust-policy projections use respectively
`SERVICE_RECORD(r.service_key)` and
`TRUST_POLICY_RECORD(r.trust_policy_key)`; a `CapabilityDescriptor` uses
`CAPABILITY_RECORD(r.capability_key)`; a `TrustEnvironment T` uses
`TRUST_ENVIRONMENT_RECORD(trustEnvironmentIdentity(T))`;
request variants share `REQUEST_RECORD(IDENTITY_OF(r))`; every result and
certificate-admission variant uses
`RESULT_RECORD(requestIdentity,tag,complete-payload-identity)`; every lifecycle
variant uses the exact target/request identity; the remaining equations are
the same-name constructors above. A bare key is already the finite identity of
its named record kind. `DiagnosticExtension`, `Diagnostics`, every diagnostic
field, and every excluded item have `recordIdentity=NONE`. There is no fallback
or producer-selected record identity.

Here every `IDENTITY_OF(r)` is definitionally the finite tuple of all and only
that record's required and derived semantic fields under their displayed exact
equalities: sequences positionally, finite sets by membership, maps by domain
and value, `ContractSpec` relations extensionally, and diagnostics omitted.
It is not an opaque handle, digest, serialization, or equality oracle.

`dependencyRoot` maps each identity to exactly one same-kind tagged key:

```text
ABI_RECORD(a)              -> ABI(a)
PACKAGE_RECORD(_,p)        -> PLUGIN(p)
DECLARATION_RECORD(d)      -> DECLARATION(d)
PAIR_DECLARATION_RECORD(p) -> PAIR_DECLARATION(p)
BINDING_RECORD(b)          -> BINDING(b)
PAIR_BINDING_RECORD(p)     -> PAIR_BINDING(p)
PROFILE_BINDING_RECORD(p)  -> PROFILE_BINDING(p)
MODEL_CONTRACT_RECORD(m)   -> MODEL_CONTRACT(m)
ALIAS_RECORD(a)            -> ALIAS(a)
SERVICE_RECORD(s)          -> SERVICE(s)
CAPABILITY_RECORD(c)       -> CAPABILITY(c)
CERTIFICATE_RECORD(c)      -> CERTIFICATE(c)
AUTHORITY_FACT_RECORD(a)   -> AUTHORITY_FACT(a)
MIGRATION_RECORD(m)        -> MIGRATION(m)
COMPATIBILITY_RECORD(c)    -> COMPATIBILITY_CLAIM(c)
SEMANTIC_EXTENSION_RECORD(x) -> SEMANTIC_EXTENSION(x)
CONTRACT_SPEC_RECORD(c)    -> CONTRACT_SPEC(c)
SEMANTIC_ENVIRONMENT_RECORD(e) -> CARRIER(SEMANTIC_ENVIRONMENT,e)
TRUST_ENVIRONMENT_RECORD(i) -> CARRIER(TRUST_ENVIRONMENT,i)
DEPENDENCY_ENVIRONMENT_RECORD(e) -> CARRIER(DEPENDENCY_ENVIRONMENT,e)
OBSERVATION_ENVIRONMENT_RECORD(e) ->
  CARRIER(DEPENDENCY_OBSERVATION_ENVIRONMENT,e)
TRUST_POLICY_RECORD(t)     -> TRUST_POLICY(t)
TRUST_ROOT_RECORD(t)       -> TRUST_ROOT(t)
LEXICAL_BINDING_RECORD(l)  -> LEXICAL_BINDING(l)
CHOICE_BINDING_RECORD(c)   -> CHOICE_BINDING(c)
REQUEST_RECORD(q)          -> REQUEST(q)
RESULT_RECORD(q)           -> RESULT(q)
LIFECYCLE_RECORD(i)        -> CARRIER(LIFECYCLE,i)
OUTCOME_RECORD(i)          -> CARRIER(OUTCOME,i)
EVENT_VALUE_RECORD(i)      -> CARRIER(EVENT_VALUE,i)
TRACE_EVENT_RECORD(i)      -> CARRIER(TRACE_EVENT,i)
SOURCE_RECORD(i)           -> CARRIER(SOURCE_REF,i)
AUTHORITY_REF_RECORD(i)    -> CARRIER(AUTHORITY_REF,i)
EVIDENCE_RECORD(i)         -> CARRIER(EVIDENCE_REF,i)
REASON_RECORD(sort,i)      -> CARRIER(REASON,(sort,i))
CONFLICT_RECORD(i)         -> CARRIER(CONFLICT,i)
NONE                       -> no root
```

For every logical record `r`, `rootKeys(r)` is the singleton containing
`dependencyRoot(recordIdentity(r))`; it is empty exactly for diagnostics and
excluded items. For a `RecordIdentity i` directly,
`rootKeys(i)={dependencyRoot(i)}` for every displayed constructor and
`rootKeys(NONE)={}`; a wrong payload type is `INVALID_RECORD_IDENTITY`, never
an empty set. In particular, a capability root is
`CAPABILITY(capability_key)`. Its `BINDING_TARGET`, `PROFILE_TARGET`, pair, or
environment target is a subject reference and never a capability root, so a
target cannot create a false self-edge. A declaration has only its declaration
root; its `SymbolKey` or `EventKey` is a separately derived syntax facet, not a
second record root. Pair declaration and pair binding likewise have distinct
roots.

Validation/admission bindings use a second, disjoint relation. The total
root projection is:

```text
validationReferenceRoots(VALIDATION_CERTIFICATE(c)) = {CERTIFICATE(c)}
validationReferenceRoots(VALIDATION_CAPABILITY(v)) =
  {CAPABILITY(v),SERVICE(v.service_key)}
validationReferenceRoots(VALIDATION_TRUST_ROOT(t)) = {TRUST_ROOT(t)}
validationReferenceRoots(V) =
  UNION(validationReferenceRoots(v) for v in V) for a finite set V
```

`validationReferences(r)` is total over logical records. It is empty except
for the following exact constructors and container projections:

```text
EventPairBinding p with INDEPENDENT_COHERENCE_PROOF(_,c,v) ->
  {VALIDATION_CERTIFICATE(c),VALIDATION_CAPABILITY(v)}
CompatibilityClaim c ->
  {VALIDATION_CERTIFICATE(c.certificate_key),
   VALIDATION_CAPABILITY(c.validator_key),
   VALIDATION_TRUST_ROOT(c.trust_root_key)}
MigrationDeclaration m ->
  {VALIDATION_CERTIFICATE(m.certificate_key),
   VALIDATION_CAPABILITY(m.validator_key),
   VALIDATION_TRUST_ROOT(m.trust_root_key)}
SemanticExtension x ->
  {VALIDATION_CERTIFICATE(x.certificate_key),
   VALIDATION_CAPABILITY(x.validator_key),
   VALIDATION_TRUST_ROOT(x.trust_root_key)}
DependencyEnvironment D -> D.validation_references
SemanticEnvironment E -> union over E.pair_bindings and
                         E.semantic_extensions
PluginPackage P -> union over P.pair_bindings, P.compatibility_claims,
                   P.migrations, and P.semantic_extensions
every other logical record -> {}
```

The equations are field projections, never producer-selected links.
`admissionBindingReferences(s,U)` is also total: it is
`validationReferences` of the unique pair binding for pair admission or pair
occurrence, of the embedded migration/compatibility/extension record for
those three subject tags, and of each exact inner subject for reasoning/joint,
certificate-admission, and certificate-validation tags. For discovery it is
the pair binding projection of an admission `PAIR_TARGET`, or the union over
the exact migration/compatibility/extension subjects embedded in an admission
`ENVIRONMENT_JUDGMENT_TARGET`; every other discovery target yields empty. It is empty for all
other Subject variants. A missing or ambiguous pair record returns its exact
open/conflict status rather than an empty set.

Lookup of a validation reference never guesses by display name, alias,
version order, or discovery order. `VALIDATION_CERTIFICATE(c)` uses the exact
`recordAt(CERTIFICATE(c),U)` result: absence is
`NO_CERTIFICATE_ADMISSION`, and unequal same-key records are malformed.
`VALIDATION_CAPABILITY(v)` requires both the unique exact capability and its
derived service projection: absence is `EVALUABILITY_MISSING`, undecided
discovery is `EVALUABILITY_UNKNOWN`, and conflict is malformed.
`VALIDATION_TRUST_ROOT(t)` requires the exact judgment at `t` in the request's
exact `TrustEnvironment`: absent/incompatible/undecided/failed retain their
distinct trust, evaluability, or discovery failure states, and only
`TRUST_ROOT_ADMITTED` is usable. These statuses are evaluated independently;
none is a semantic observation or a fallback for another.

Validation references are mandatory admission inputs but are not semantic
proper references of the four validation-bound semantic records above. Their
certificate/validator/root fields are therefore absent from those records'
`subjectReferences`, `rawProperDependencies`, `properEdges`, semantic
dependency closure, and `ContractSpec` observation support. They remain
present in the separately carried `DependencyEnvironment.validation_references`
and in the operational request/certificate root equations below. A request,
certificate-validation request, or envelope may independently name the same
exact root through its own exhaustive `subjectReferences` equation; that
outgoing operation-carrier edge is not a back-edge from the semantic subject.

`subjectReferences(r)` is also total. The exhaustive equations, grouped only
where field types are identical, are:

```text
declaration -> referenced result/argument/payload type DECLARATION roots and
               CONTRACT_SPEC(admitted_value_domain.contract_key), as present
pair declaration -> member DECLARATION/SYMBOL and controlled EVENT roots
SemanticBinding -> its DECLARATION plus CONTRACT_SPEC roots for meaning,
                   evidence, access, unknown, and error contracts
EventPairBinding -> PAIR_DECLARATION, scope BINDING, occurrence BINDING,
                    MODEL_CONTRACT(occurrence_model_contract_key), and, for
                    independent proof, every occurrence-bundle CONTRACT_SPEC
                    (its certificate/validator are validation references)
ProfileBinding -> CONTRACT_SPEC roots for coverage/evidence/unknown/errors
ModelContract -> exact target semantic root, its four CONTRACT_SPEC roots,
                 and every summarized CAPABILITY
AliasBinding -> the one exact target root
ServiceIdentityRecord -> ABI(abi_version) and PLUGIN(plugin_key)
CapabilityDescriptor -> SERVICE(capability.service_key), every target's exact
                        subject roots, fragment/evidence/failure CONTRACT_SPEC
                        roots, and every required TRUST_ROOT
SemanticEnvironment -> ABI plus roots of every displayed member and every
                       lexical/choice entry; never a TrustEnvironment root
DependencyEnvironment -> its subject roots, association endpoints, and proper
                         closure, explicitly excluding validation references;
                         DependencyObservationEnvironment -> map keys
TrustEnvironment -> TRUST_POLICY plus every referenced TRUST_ROOT
TrustPolicyRecord -> empty; TrustRootRecord -> empty
  (owners are structural and validator/kind/target lists are permissions)
LexicalBinding -> its declared type; ChoiceBindingEntry -> declared type,
                  `CARRIER(SOURCE_REF,...)`, authority fact, and admitted-value
                  declaration roots
ValueAdmission/Function/Predicate/Profile/PairAdmission/AuthorityAdmission/
MigrationAdmission/CompatibilityAdmission/SemanticExtensionAdmission/
Reasoning request -> semanticRequestRoots(request), which contains its
                     subject, named CAPABILITY/SERVICE, exact environment and
                     dependency-environment roots, exact TrustEnvironment
                     carrier, fragment if any, and separately carried service
                     TRUST_ROOT, but excludes validation references
DiscoveryRequest -> semanticRequestRoots(request), which contains its subject,
                    exact semantic/trust-environment roots, and required
                    fragment but no guessed capability/service or validation
                    reference
CertificateValidationRequest -> certificateValidationRoots(request,U)
every result/admission/lifecycle -> REQUEST(its exact request identity)
CertificateEnvelope -> certificateProperReferences(envelope,U), including the
                       exact TrustEnvironment root nested in `request_binding`,
                       subject roots, named producer/validator capabilities
                       and services, trust root, fragment, and dependency
                       roots, but excluding its own certificate start root
CompatibilityClaim -> ABI/source/target key sets and compatibility
                      CONTRACT_SPEC; its certificate/validator/root are
                      validation references
MigrationDeclaration -> source/target environment roots and relation
                        CONTRACT_SPEC; certificate/validator/root are
                        validation references
SemanticExtension -> its exact target and effect/payload CONTRACT_SPEC;
                     certificate/validator/root are validation references
AuthorityFactBinding -> its `CARRIER(AUTHORITY_REF,...)` and
                        `CARRIER(SOURCE_REF,...)` subject roots plus admitted
                        CERTIFICATE evidence roots
Outcome/EventValue/TraceEvent -> exact type/event declaration roots of their
                                 admitted values and events
SourceRef/AuthorityRef/EvidenceRef/reasons/ConflictRef and key-only carriers
  -> exact typed identities embedded in their fields, otherwise empty
PluginPackage -> ABI and roots of every non-diagnostic member
```

No row treats a record's own identity as a subject reference. Each
`ContractSpec c` is its own record with
`subjectReferences(c)=support(c)`, so a containing record points to the
contract-spec root and the contract-spec node points only to lower-level
observation roots. This is what makes the graph stratified.

The identity/proper-reference distinction has two controlled boundary checks.
For an otherwise conforming empty package `P` with ABI `a`, plugin key `p`,
every member set empty, and diagnostics absent,

```text
rootKeys(P) = {PLUGIN(p)}
subjectReferences(P) = {ABI(a)}
rootKeys(P) intersect subjectReferences(P) = {}
```

For a nonempty package, `subjectReferences(P)` adds exactly the roots of its
non-diagnostic members and still never adds `PLUGIN(p)` merely because that is
the package identity. Thus the plugin root remains the package start root,
while the ABI and all members remain proper references.

For every conformant certificate envelope `c`, its identity is likewise a
start root rather than a proper outgoing reference:

```text
rootKeys(c) = {CERTIFICATE(c.certificate_key)}
rootKeys(c) intersect subjectReferences(c) = {}
```

`subjectReferences(c)=certificateProperReferences(c,U)` still contains all
displayed semantic request, subject, capability, validator, trust-root,
fragment, and dependency roots. The candidate certificate and every other
mandatory admission binding remain in `certificateRoots(c,U)`, the separately
carried validation-reference set, and the derived
`CertificateValidationRequest`, where they are explicitly looked up and
validated. Only the envelope's own certificate start root is absent from its
proper references. Therefore envelope formation no longer fails solely on its
own identity edge; after the independent §6.5 validation premises pass, the
envelope can reach `CertificateAdmission.ADMITTED`.

For every conformant `TrustEnvironment T`, its exact carrier identity is also
a start root rather than a proper outgoing reference:

```text
rootKeys(T) = {
  CARRIER(TRUST_ENVIRONMENT,trustEnvironmentIdentity(T))
}
subjectReferences(T) = {TRUST_POLICY(T.trust_policy_key)} union
  {TRUST_ROOT(k) | k in keys(T.root_judgments)}
rootKeys(T) intersect subjectReferences(T) = {}
```

Thus the environment retains its proper references to its exact trust policy
and every referenced trust-root record, while its own carrier root is never a
proper reference. An explicit field that selects that own carrier root remains
a genuine self-dependency and is rejected by the unchanged intersection rule.

Substitution of every `RecordIdentity` constructor into `dependencyRoot` and
the exhaustive `subjectReferences` equations gives an empty root/reference
intersection for every conformant record. The three unintended mandatory
own-root references were the package plugin identity, envelope certificate
identity, and TrustEnvironment carrier identity removed above; no additional
constructor has one. This is not a global root subtraction: if an arbitrary
target or dependency field explicitly selects its containing record's own
root, that genuine semantic self-dependency still has a nonempty intersection
and remains invalid.

```text
rawProperDependencies(r) = subjectReferences(r)
properDependencies(r) = rawProperDependencies(r)
  provided rawProperDependencies(r) intersect rootKeys(r) = {}
properEdges(U) = {
  (a,b) | r is a record in finite exact universe U,
          a in rootKeys(r), b in properDependencies(r)
}
```

Substitution gives the following explicit mandatory-edge audit:

```text
PAIR_BINDING(p) -> PAIR_DECLARATION(p), scope/occurrence BINDING,
                   MODEL_CONTRACT, occurrence-bundle CONTRACT_SPEC roots
MIGRATION(m) -> source/target SEMANTIC_ENVIRONMENT carriers,
                relation CONTRACT_SPEC
COMPATIBILITY_CLAIM(c) -> source/target ABI/key roots,
                          compatibility CONTRACT_SPEC
SEMANTIC_EXTENSION(x) -> exact target root, effect/payload CONTRACT_SPEC roots
```

There is no proper edge from any of those four sources to its validation
certificate, validator capability/service, or trust root. The reverse
semantic edges required for validation remain possible and explicit:
`CERTIFICATE(c)` may point through its bound request to the subject, and a
validator `CAPABILITY(v)` points through its advertised target to the subject.
Because the subject has no proper edge back to `CERTIFICATE(c)` or
`CAPABILITY(v)`, the former mandatory two-node cycles
`PAIR_BINDING/MIGRATION/COMPATIBILITY_CLAIM/SEMANTIC_EXTENSION ->
CERTIFICATE|CAPABILITY -> subject` do not exist. The certificate, capability,
service, and trust-root keys have not been deleted: they are exact mandatory
`ValidationReference`s and operational roots with independent lookup/status
checks. Any genuine semantic self-edge among the displayed semantic targets,
environments, contracts, or their descendants still intersects its own root
or forms a cycle in `properEdges(U)` and is rejected unchanged.

A nonempty intersection is an invalid self-edge. Every displayed
`proper_declaration_dependencies` or `proper_semantic_dependencies` must equal
the exact applicable projection of `properDependencies`; no producer supplies
it. The graph must be finite and acyclic. `dependency_closure(r)` is the unique
least set reachable by one or more proper edges from `rootKeys(r)`, excluding
the roots. Cycle rejection precedes closure. A definitional occurrence lift is
ownership, not a back-edge.

Lookup is total in an exact universe `U=(E,T,packages,request?,result?)`.
`recordAt(k,U)` has one equation for every `DependencyKey` tag:

```text
ABI(a) -> the exact AbiVersion carrier equal to a
PLUGIN(p) -> the exact PluginPackage owner presence for p
DECLARATION(d) -> the unique Declaration with key d
SYMBOL(s) -> the unique function/predicate Declaration with symbol facet s
EVENT(e) -> the unique EventDeclaration with event facet e
PROFILE(p) -> the exact K1 profile syntax facet p
PAIR(p) -> the exact K1 pair syntax facet p
BINDING(b) -> the unique ordinary SemanticBinding, or the unique pair-owned
              OccurrenceBindingProjection, with key b, never both
PAIR_DECLARATION(p) -> the unique EventScopePairDeclaration p
PAIR_BINDING(p) -> the unique EventPairBinding p
PROFILE_BINDING(p) -> the unique ProfileBinding p
SERVICE(s) -> the unique derived ServiceIdentityRecord s
CAPABILITY(c) -> the unique CapabilityDescriptor c
CERTIFICATE(c) -> the unique CertificateEnvelope c
MIGRATION(m) -> the unique MigrationDeclaration m
COMPATIBILITY_CLAIM(c) -> the unique CompatibilityClaim c
MODEL_CONTRACT(m) -> the unique ModelContract m
ALIAS(a) -> the unique AliasBinding a
AUTHORITY_FACT(a) -> the unique admitted AuthorityFactBinding a
LEXICAL_BINDING(l) -> the unique LexicalBinding l
CHOICE_BINDING(c) -> the unique ChoiceBindingEntry c
TRUST_POLICY(t) -> the unique derived TrustPolicyRecord t
TRUST_ROOT(t) -> the unique TrustRootRecord/Judgment entry t
SEMANTIC_EXTENSION(x) -> the unique admitted SemanticExtension x
CONTRACT_SPEC(c) -> the unique ContractSpec c at its enclosing use
REQUEST(q) -> the unique request, including derived certificate-validation
              request, with identity q
RESULT(q) -> the unique result/admission with ResultIdentity q
CARRIER(kind,i) -> the unique non-diagnostic carrier of exactly `kind` and
                   complete logical identity i
```

The `PROFILE` and `PAIR` results are typed syntax-facet presences, not binding
records; derived associations lead to the binding roots. Derived service and
trust-policy projections are never producer-supplied. For every equation the
result type is exactly `PRESENT(the displayed typed record/facet)`,
`ABSENT_REQUIRED_RECORD(the same tag,key)`, or
`MALFORMED(nonempty exact conflicts)`. No tag falls through to a generic
same-name guess.

Missing `DECLARATION`/`SYMBOL`/`EVENT` or pair-declaration records are
malformed. Missing reachable `BINDING`, `PROFILE_BINDING`, or `PAIR_BINDING`
records are open. Missing `SERVICE`/`CAPABILITY` records give evaluability
missing; an undecided lookup remains discovery/evaluability unknown. Missing
`CERTIFICATE`, authority admission, migration, compatibility claim, or
semantic-extension admission grants no admission. Missing a named model
contract leaves its model-facing binding open; a present wrong record is
malformed. Missing lexical/choice/authority
coordinates are respectively malformed or open under K1 closure. No producer
can override a missing-status tag. Duplicate equal records coalesce and any
same-root unequal record is the exact conflict of §8.3.

Equivalently, the missing function is total by tag:

```text
missingStatus(ABI | PLUGIN | DECLARATION | SYMBOL | EVENT |
              PAIR_DECLARATION | required Delta CARRIER) = MALFORMED
missingStatus(BINDING | PROFILE_BINDING | PAIR_BINDING |
              AUTHORITY_FACT | required CHOICE_BINDING) = OPEN_BINDINGS
missingStatus(LEXICAL_BINDING) = MALFORMED_REQUEST or OPEN_BINDINGS according
                                 to the exact K1 closure premise
missingStatus(SERVICE | CAPABILITY) = EVALUABILITY_MISSING
missingStatus(TRUST_POLICY | TRUST_ROOT) = TRUST_ROOT_ABSENT and no use
missingStatus(CERTIFICATE) = NO_CERTIFICATE_ADMISSION
missingStatus(MIGRATION) = NO_MIGRATION
missingStatus(COMPATIBILITY_CLAIM) = NO_COMPATIBILITY
missingStatus(SEMANTIC_EXTENSION) = NO_EFFECT, or INCOMPATIBLE when the
                                    extension was offered as required semantic
missingStatus(MODEL_CONTRACT) = OPEN_BINDINGS(model contract)
missingStatus(ALIAS) = NO_ALIAS unless an exact alias reference required it,
                       in which case MALFORMED(missing alias)
missingStatus(CONTRACT_SPEC) = enclosing owner-layer incompatibility
missingStatus(REQUEST | RESULT) = MALFORMED_REQUEST or protocol failure
missingStatus(non-Delta CARRIER) = its exact formation/closure/protocol family
```

Support, edge, observation, or closure mismatch has the owner-layer outcome:
Delta is `DECLARATION_INVALID`/`MALFORMED`; Sigma is
`BINDING_INCOMPATIBLE`/`MALFORMED(incompatible semantic binding)`; Service is
`CAPABILITY_INCOMPATIBLE` and `EVALUABILITY_MISSING`; a request is
`MALFORMED_REQUEST`; and a certificate is malformed with no conclusion. A
semantic extension follows its declared owner layer. A smaller, larger, cyclic,
or self-containing producer view establishes nothing.

K2 uses K1's recursive syntax `deps` equations unchanged, but exposes them as
the separate `K1SyntaxKey` facet. The total subject algebra is:

```text
Subject =
    CONTRACT_SUBJECT(Contract)
  | FORMULA_SUBJECT(finset(Formula), LexicalScopeIdentity)
  | VALUE_ADMISSION_SUBJECT(DeclarationKey[TYPE], Value)
  | FUNCTION_SUBJECT(SymbolKey[FUNCTION], BindingKey, sequence(Value))
  | PREDICATE_SUBJECT(SymbolKey[PREDICATE], BindingKey, sequence(Value))
  | PROFILE_SUBJECT(ProfileKey, exact typed coverage subject)
  | PAIR_ADMISSION_SUBJECT(EventScopePairKey)
  | PAIR_OCCURRENCE_SUBJECT(EventScopePairKey, Trace)
  | AUTHORITY_ADMISSION_SUBJECT(
      AuthorityFactCandidate, environment_without_fact : SemanticEnvironment)
  | MIGRATION_SUBJECT(MigrationDeclaration)
  | COMPATIBILITY_SUBJECT(CompatibilityClaim)
  | SEMANTIC_EXTENSION_SUBJECT(SemanticExtension)
  | SEMANTIC_ENVIRONMENT_SUBJECT(SemanticEnvironment)
  | RECORD_TARGET_SUBJECT(RecordIdentity)
  | CAPABILITY_TARGET_SUBJECT(CapabilityTarget)
  | DISCOVERY_SUBJECT(CapabilityTarget, JudgmentTag)
  | REASONING_SUBJECT(ReasoningJudgment, exact judgment-specific subject tuple)
  | JOINT_SUBJECT(ReasoningJudgment, nonempty exact subject tuple)
  | CERTIFICATE_ADMISSION_SUBJECT(CertificateKey, Subject)
  | CERTIFICATE_VALIDATION_SUBJECT(
      CertificateKey, RequestIdentity, claimed conclusion, Subject)
  | MODEL_CONTRACT_SUBJECT(ModelContractKey)
  | PACKAGE_SUBJECT(AbiVersion, PluginKey)
```

There is no other request subject. `subjectOf` is exhaustive:

```text
ValueAdmissionRequest -> VALUE_ADMISSION_SUBJECT(type_key,value)
FunctionRequest       -> FUNCTION_SUBJECT(symbol_key,binding_key,arguments)
PredicateRequest      -> PREDICATE_SUBJECT(symbol_key,binding_key,arguments)
ProfileRequest        -> PROFILE_SUBJECT(profile_key,coverage_subject)
PairAdmissionRequest  -> PAIR_ADMISSION_SUBJECT(pair_key)
AuthorityAdmissionRequest -> AUTHORITY_ADMISSION_SUBJECT(
  candidate,environment_without_fact)
MigrationAdmissionRequest -> MIGRATION_SUBJECT(migration)
CompatibilityAdmissionRequest -> COMPATIBILITY_SUBJECT(claim)
SemanticExtensionAdmissionRequest ->
  SEMANTIC_EXTENSION_SUBJECT(extension)
DiscoveryRequest -> DISCOVERY_SUBJECT(target,judgment)
ReasoningRequest -> REASONING_SUBJECT(judgment,subjects), or JOINT_SUBJECT
                    exactly when the judgment tuple spans multiple producers
CertificateEnvelope ->
  CERTIFICATE_ADMISSION_SUBJECT(certificate_key,subjectOf(request_binding))
CertificateValidationRequest -> CERTIFICATE_VALIDATION_SUBJECT(
  certificate_key,original_request_identity,claimed_conclusion,
  original_subject)
```

The companion request projections are also total:

```text
judgmentOf(ValueAdmissionRequest)=VALUE_ADMISSION
judgmentOf(FunctionRequest)=FUNCTION_EVALUATION
judgmentOf(PredicateRequest)=PREDICATE_EVALUATION
judgmentOf(ProfileRequest)=PROFILE_COVERAGE
judgmentOf(PairAdmissionRequest)=EVENT_PAIR_COHERENCE_ADMISSION
judgmentOf(AuthorityAdmissionRequest)=AUTHORITY_FACT_ADMISSION
judgmentOf(MigrationAdmissionRequest)=MIGRATION_RELATION_ADMISSION
judgmentOf(CompatibilityAdmissionRequest)=COMPATIBILITY_CLAIM_ADMISSION
judgmentOf(SemanticExtensionAdmissionRequest)=SEMANTIC_EXTENSION_ADMISSION
judgmentOf(DiscoveryRequest r)=r.judgment
judgmentOf(ReasoningRequest r)=r.judgment
judgmentOf(CertificateValidationRequest v)=v.validator_judgment

roleOf(ValueAdmissionRequest)=VALUE_ADMISSION
roleOf(FunctionRequest)=FUNCTION_EVALUATION
roleOf(PredicateRequest)=PREDICATE_EVALUATION
roleOf(ProfileRequest)=the exact concrete/symbolic role of its capability
roleOf(PairAdmissionRequest)=PAIR_VALIDATION
roleOf(AuthorityAdmissionRequest)=AUTHORITY_VALIDATION
roleOf(MigrationAdmissionRequest)=MIGRATION_VALIDATION
roleOf(CompatibilityAdmissionRequest)=COMPATIBILITY_VALIDATION
roleOf(SemanticExtensionAdmissionRequest)=SEMANTIC_EXTENSION_VALIDATION
roleOf(ReasoningRequest)=REASONING
roleOf(CertificateValidationRequest v)=v.validator_service_role
roleOf(DiscoveryRequest)=INVALID_INVOCATION_ROLE
```

Any profile-role ambiguity or field/descriptor mismatch is malformed before
invocation. These equations enumerate every request/admission branch; there is
no default request kind.

`subjectOfCapabilityTarget` is total and is the only target-to-subject
projection:

```text
subjectOfCapabilityTarget(BINDING_TARGET(k)) =
  CAPABILITY_TARGET_SUBJECT(BINDING_TARGET(k))
subjectOfCapabilityTarget(TYPE_ADMISSION_TARGET(t,e)) =
  CAPABILITY_TARGET_SUBJECT(TYPE_ADMISSION_TARGET(t,e))
subjectOfCapabilityTarget(PROFILE_TARGET(p)) =
  CAPABILITY_TARGET_SUBJECT(PROFILE_TARGET(p))
subjectOfCapabilityTarget(PAIR_TARGET(p)) =
  CAPABILITY_TARGET_SUBJECT(PAIR_TARGET(p))
subjectOfCapabilityTarget(ENVIRONMENT_JUDGMENT_TARGET(j,ss,e)) =
  CAPABILITY_TARGET_SUBJECT(ENVIRONMENT_JUDGMENT_TARGET(j,ss,e))
```

Accordingly, `DISCOVERY_SUBJECT(t,j)` has the exact inner subject
`subjectOfCapabilityTarget(t)` and separately retains `j`; target/judgment
incompatibility is an invalid discovery request rather than an implicit
projection.

`required(s)` is total and returns only frozen K1 keys:

```text
required(CONTRACT_SUBJECT(C)) = the exact K1 Dependencies(C) equations
required(FORMULA_SUBJECT(F,_)) = UNION(deps(f) for f in F)
required(VALUE_ADMISSION_SUBJECT(t,v)) = declDeps_Delta(t,v)
required(FUNCTION_SUBJECT(q,_,args)) =
  sigDeps_Delta(q) union UNION(declDeps_Delta(v) for v in args)
required(PREDICATE_SUBJECT(q,_,args)) =
  sigDeps_Delta(q) union UNION(declDeps_Delta(v) for v in args)
required(PROFILE_SUBJECT(p,x)) = {K1_PROFILE(p)} union deps(x)
required(PAIR_ADMISSION_SUBJECT(p)) = deps(the exact pair p)
required(PAIR_OCCURRENCE_SUBJECT(p,T)) =
  deps(the exact pair p) union deps(e) for every event e in T
required(REASONING_SUBJECT(_,subjects)) = UNION(required(s) for typed subjects)
required(JOINT_SUBJECT(_,subjects)) = UNION(required(s) for every member)
required(CERTIFICATE_ADMISSION_SUBJECT(_,s)) = required(s)
required(CERTIFICATE_VALIDATION_SUBJECT(_,_,_,s)) = required(s)
required(CAPABILITY_TARGET_SUBJECT(BINDING_TARGET(k))) =
  {K1_DECLARATION(k)}
required(CAPABILITY_TARGET_SUBJECT(TYPE_ADMISSION_TARGET(t,_))) =
  {K1_DECLARATION(t)}
required(CAPABILITY_TARGET_SUBJECT(PROFILE_TARGET(p))) = {K1_PROFILE(p)}
required(CAPABILITY_TARGET_SUBJECT(PAIR_TARGET(p))) = {K1_PAIR(p)}
required(CAPABILITY_TARGET_SUBJECT(
  ENVIRONMENT_JUDGMENT_TARGET(_,subjects,_))) =
  UNION(required(s) for every exact typed subject in subjects)
required(DISCOVERY_SUBJECT(target,_)) =
  required(subjectOfCapabilityTarget(target))
required(AUTHORITY_ADMISSION_SUBJECT(candidate,E0)) =
  deps(candidate.authority_fact_key.authority_ref)
  union deps(candidate.authority_fact_key.source_ref)
  union deps(candidate.authority_fact_key.principal)
  union deps(candidate.admission_subject_data)
  union deps(candidate.offered_evidence_refs)
  union required(SEMANTIC_ENVIRONMENT_SUBJECT(E0))
required(SEMANTIC_ENVIRONMENT_SUBJECT(E)) =
  E.mechanically_extracted_dependencies
required(MIGRATION_SUBJECT(m)) =
  required(SEMANTIC_ENVIRONMENT_SUBJECT(m.source_environment))
  union required(SEMANTIC_ENVIRONMENT_SUBJECT(m.target_environment))
required(COMPATIBILITY_SUBJECT(c)) = syntax facets of
  c.source_keys union c.target_keys
required(SEMANTIC_EXTENSION_SUBJECT(x)) =
  required(RECORD_TARGET_SUBJECT(x.target_record_identity))
required(RECORD_TARGET_SUBJECT(r)) =
  UNION(requiredKey(k,U) for k in rootKeys(r))
required(MODEL_CONTRACT_SUBJECT(m)) =
  required(RECORD_TARGET_SUBJECT(MODEL_CONTRACT_RECORD(m)))
required(PACKAGE_SUBJECT(a,p)) =
  required(RECORD_TARGET_SUBJECT(PACKAGE_RECORD(a,p)))
```

Here the universe parameter `U` is implicit only in the three displayed
record-reachability projections. `requiredKey(k,U)` is total: start with the
direct frozen syntax facet shown below, then union every frozen syntax facet
encountered through derived association edges and proper subject-reference
edges. It never returns a K2-only root.

```text
ABI -> {}; PLUGIN(p) -> {K1_PLUGIN(p)}
DECLARATION(d) -> {K1_DECLARATION(d)}; SYMBOL(s) -> {K1_SYMBOL(s)}
EVENT(e) -> {K1_EVENT(e)}; PROFILE(p) -> {K1_PROFILE(p)}
PAIR(p) -> {K1_PAIR(p)}; BINDING(d) -> {K1_DECLARATION(d)}
PAIR_DECLARATION(p)|PAIR_BINDING(p) -> {K1_PAIR(p)}
PROFILE_BINDING(p) -> {K1_PROFILE(p)}
SERVICE|CAPABILITY|CERTIFICATE|MIGRATION|COMPATIBILITY_CLAIM|
MODEL_CONTRACT|ALIAS|AUTHORITY_FACT|LEXICAL_BINDING|CHOICE_BINDING|
TRUST_POLICY|TRUST_ROOT|SEMANTIC_EXTENSION|CONTRACT_SPEC|REQUEST|RESULT|
CARRIER -> {}
```

For every tag, the final value is that direct seed union the seeds reachable
from its unique record and derived associations. An absent record contributes
only the known direct seed and its exact `missingStatus`; ambiguity is
malformed. Thus semantic-extension targets, model subjects, package subjects,
and migration environments have exact frozen-root projections without an
informal “target subject” or “environment subjects” placeholder.

Every K1 `deps` result is lifted tag-for-tag from `K1SyntaxKey` to the matching
`PLUGIN`/`DECLARATION`/`SYMBOL`/`EVENT`/`PROFILE`/`PAIR` dependency key only
for K2 graph traversal; the unlifted set remains visible as
`syntax_root_keys`. Define semantic roots separately:

```text
semanticSubjectRoots(CONTRACT_SUBJECT(_) | FORMULA_SUBJECT(_,_)) = {}
semanticSubjectRoots(value admission) = {DECLARATION(type_key)}
semanticSubjectRoots(function/predicate) = {BINDING(binding_key)}
semanticSubjectRoots(profile) = {PROFILE_BINDING(profile_key)}
semanticSubjectRoots(pair admission/occurrence) =
  {PAIR_DECLARATION(pair_key),PAIR_BINDING(pair_key)}
semanticSubjectRoots(AUTHORITY_ADMISSION_SUBJECT(_,E0)) =
  {dependencyRoot(SEMANTIC_ENVIRONMENT_RECORD(semanticIdentity(E0)))}
semanticSubjectRoots(MIGRATION_SUBJECT(m)) = {MIGRATION(m.migration_key)}
semanticSubjectRoots(COMPATIBILITY_SUBJECT(c)) =
  {COMPATIBILITY_CLAIM(c.claim_key)}
semanticSubjectRoots(SEMANTIC_EXTENSION_SUBJECT(x)) =
  {SEMANTIC_EXTENSION(x.extension_key)}
semanticSubjectRoots(SEMANTIC_ENVIRONMENT_SUBJECT(E)) =
  {dependencyRoot(SEMANTIC_ENVIRONMENT_RECORD(semanticIdentity(E)))}
semanticSubjectRoots(RECORD_TARGET_SUBJECT(r)) = rootKeys(r)
semanticSubjectRoots(CAPABILITY_TARGET_SUBJECT(t)) = targetReferences(t)
semanticSubjectRoots(model contract) = {MODEL_CONTRACT(model_contract_key)}
semanticSubjectRoots(package) = {ABI(abi_version),PLUGIN(plugin_key)}
semanticSubjectRoots(reasoning/joint) = union over the exact typed subjects
semanticSubjectRoots(certificate admission) =
  {CERTIFICATE(certificate_key)} union semanticSubjectRoots(inner subject)
semanticSubjectRoots(certificate validation) =
  {CERTIFICATE(certificate_key),REQUEST(original_request_identity)}
  union semanticSubjectRoots(inner subject)
semanticSubjectRoots(discovery) =
  semanticSubjectRoots(subjectOfCapabilityTarget(target))

trustEnvironmentOf(r) = r.trust_environment
  for every request variant in section 5.1, including DiscoveryRequest and
  CertificateValidationRequest
trustEnvironmentRoot(T) = dependencyRoot(
  TRUST_ENVIRONMENT_RECORD(trustEnvironmentIdentity(T)))

subjectRoots(s) = lift(required(s)) union semanticSubjectRoots(s)
requestFieldRoots(r) =
  {dependencyRoot(recordIdentity(x)) |
     x is a displayed SemanticEnvironment or DependencyEnvironment field of r}
  union {CONTRACT_SPEC(f.contract_key) |
           f is a displayed fragment ContractSpec field of r}
  union {TRUST_ROOT(k) |
           k is in a displayed service_use_trust_root_keys field of r}
semanticRequestRoots(r) = subjectRoots(subjectOf(r)) union
  ({CAPABILITY(r.capability_key),SERVICE(r.capability_key.service_key)}
   when r has capability_key) union
  {trustEnvironmentRoot(trustEnvironmentOf(r))} union requestFieldRoots(r)
requestValidationReferences(r,U) =
  validationReferences(D) when r has the unique displayed
    dependency_environment or complete_dependencies field D,
  admissionBindingReferences(subjectOf(r),U) for a DiscoveryRequest whose
    judgment/target is an admission target,
  {} otherwise
requestRoots(r,U) = semanticRequestRoots(r) union
  validationReferenceRoots(requestValidationReferences(r,U))
certificateValidationRoots(v,U) = subjectRoots(subjectOf(v)) union
  {CERTIFICATE(v.certificate_key),REQUEST(v.original_request_identity),
   CAPABILITY(v.validator_key),SERVICE(v.validator_key.service_key),
   CONTRACT_SPEC(v.fragment.contract_key),
  dependencyRoot(SEMANTIC_ENVIRONMENT_RECORD(
     semanticIdentity(v.semantic_environment))),
   trustEnvironmentRoot(v.trust_environment)} union
  roots of v.complete_dependencies union
  {TRUST_ROOT(k) | k in v.service_use_trust_root_keys} union
  {TRUST_ROOT(v.certificate_admission_trust_root_key)} union
  validationReferenceRoots(v.complete_dependencies.validation_references) union
  validationReferenceRoots(
    admissionBindingReferences(v.original_subject,U))
certificateRoots(c,U) = requestRoots(c.request_binding,U) union
  {CERTIFICATE(c.certificate_key), CAPABILITY(c.capability_key),
   SERVICE(c.capability_key.service_key), CAPABILITY(c.validator_key),
   SERVICE(c.validator_key.service_key), TRUST_ROOT(c.trust_root_key),
   CONTRACT_SPEC(c.fragment.contract_key),
   dependencyRoot(SEMANTIC_ENVIRONMENT_RECORD(
     semanticIdentity(c.environment))),
   trustEnvironmentRoot(trustEnvironmentOf(c.request_binding))} union
  roots of c.dependencies union
  validationReferenceRoots(c.dependencies.validation_references) union
  validationReferenceRoots(
    admissionBindingReferences(subjectOf(c.request_binding),U))
certificateProperReferences(c,U) =
  certificateRoots(c,U) minus {CERTIFICATE(c.certificate_key)}
```

Every displayed root collection is a `finset`, and every `union` has exact set
semantics. The `TrustEnvironment` is separate from, never a field of,
`SemanticEnvironment`; it is nested only through request and certificate
records. When the same trust-environment root is reached both through
`semanticRequestRoots` and an explicit certificate or validation term above, exact
equality coalesces it to one set member rather than a duplicate edge. The root
is nevertheless present in every ordinary request, every admission request,
`DiscoveryRequest`, `CertificateValidationRequest`, and
`CertificateEnvelope` operational root set. Validation-reference roots are
likewise exact operation inputs. These equations do not turn them into proper
edges from pair, migration, compatibility, or extension records; only the
separately enumerated request/validation-request/envelope equations determine
outgoing proper references from those operation carriers.

For the derived validation request,
`DependencyEnvironment(v,U)` starts from
`required(subjectOf(v)) union certificateValidationRoots(v,U)` and traverses the
same associations/proper edges as every other request. Its producer-independence
set is `validationSubjectProducerSet(v.original_subject,U,v.certificate_key,
v.validator_key,the admission root)`. Thus the complete semantic producer set
is used for both ordinary validator service trust and independent certificate
trust, while only the certificate/validator/root validation machinery is
excluded from the thing being validated.

`targetReferences` is total:

```text
BINDING_TARGET(k) -> {BINDING(k)}
TYPE_ADMISSION_TARGET(t,e) ->
  {DECLARATION(t),CARRIER(SEMANTIC_ENVIRONMENT,e)}
PROFILE_TARGET(p) -> {PROFILE_BINDING(p)}
PAIR_TARGET(p) -> {PAIR_DECLARATION(p),PAIR_BINDING(p)}
ENVIRONMENT_JUDGMENT_TARGET(_,subjects,e) ->
  UNION(subjectRoots(s) for each exact typed subject s)
  union {CARRIER(SEMANTIC_ENVIRONMENT,e)}
```

An ill-typed subject tuple returns `INVALID_CAPABILITY_TARGET`; it is never an
empty root set. Capability producers cannot override these equations.

The total, non-asserted producer relation returns a finite set:

```text
producerOf(PluginKey p) = {PLUGIN_PRODUCER(p)}
producerOf(DeclarationKey/SymbolKey/EventKey/ProfileKey/EventScopePairKey/
           BindingKey k)
  = {PLUGIN_PRODUCER(k.plugin_key)}
producerOf(ProfileDimensionKey d) = producerOf(d.profile_key)
producerOf(ServiceKey s) = producerOf(s.plugin_key)
producerOf(CapabilityKey c) = producerOf(c.service_key)
producerOf(CertificateKey c) =
  {PLUGIN_PRODUCER(p)} for PLUGIN_CERTIFICATE_ISSUER(p), or
  {EMBEDDING_POLICY_PRODUCER(t)} for EMBEDDING_POLICY_CERTIFICATE_ISSUER(t)
producerOf(MigrationKey m) = producerOf(m.owner_plugin)
producerOf(CompatibilityClaimKey c) = producerOf(c.owner_plugin)
producerOf(SemanticExtensionKey x) = producerOf(x.owner_plugin)
producerOf(ModelContractKey m) = producerOf(m.target_semantic_identity)
producerOf(AliasKey a) = producerOf(a.owner_plugin)
producerOf(ContractSpecKey c) = producerOf(c.owner_plugin)
producerOf(TrustPolicyKey t) = {EMBEDDING_POLICY_PRODUCER(t)}
producerOf(TrustRootKey r) = producerOf(r.trust_policy_key)
producerOf(AuthorityRef a) = producerOf(a.owner)
producerOf(SourceRef s) = producerOf(s.issuer)
producerOf(AuthorityFactKey a) =
  producerOf(a.authority_ref) union producerOf(a.source_ref)
producerOf(AuthorityFactCandidate a) =
  producerOf(a.authority_fact_key) union
  producerOf(a.admission_subject_data) union
  producerOf(a.offered_evidence_refs)
producerOf(SemanticEnvironment E) =
  UNION(producerOf(r) for every non-diagnostic record r in E)
producerOf(Contract/Formula/Value/finite tuple/set/map x) =
  structural union over every exact owned key, SourceRef, AuthorityRef,
  declaration, binding, profile, pair, service, certificate, migration,
  compatibility, extension, model-contract, trust-policy, and trust-root
  identity occurring in x
producerOf(AbiVersion a) = {ABI_PRODUCER(a)}
producerOf(kernel-owned atom with no owned identity) = {}
producerOf(record r) = producerOf(recordIdentity(r)) union
  structural union of producerOf over its subjectReferences
```

For `IssuerScope`, `CertificateIssuer`, `SemanticTargetIdentity`,
`DependencyKey`, `ValidationReference`, `CapabilityTarget`, `TrustTarget`, `ServiceUseSubject`,
`RecordIdentity`, requests, results, admissions, lifecycle records, and every
other tagged union, `producerOf` is structural recursion over the tag payload.
Finite tuple recursion is positional, finite-set/map recursion is union over
all members/keys/values, and the base equations above terminate. Therefore it
is total for every relevant identity and record, not a plugin claim.

For independence, validation machinery is not part of the thing it validates.
Define `semanticPayload(s)` as the complete Subject payload after removing
only its certificate envelope/key, validator capability/service, and
certificate-admission trust-root fields. Migration retains its key, complete
source and target environments, named relation, and relation contract;
compatibility retains its key, ABI/key sets, and compatibility contract;
extension retains its key, target, owner layer, semantic effect, and payload;
pair retains its declaration, scope, and complete occurrence bundle; authority
admission retains the complete candidate and exact environment without the
candidate fact; certificate admission/validation retains its inner semantic
subject. All other Subjects retain their complete payload.

`producerSubjectReferences(r,gate)` equals `subjectReferences(r)` minus only
edges explicitly tagged by `gate` as its validator `CAPABILITY`/`SERVICE`, its
candidate `CERTIFICATE`, or its certificate-admission `TRUST_ROOT`. It does
not remove any declaration, binding, profile, pair, semantic-contract,
authority, migration, compatibility, semantic-extension, model, source/target
environment, lexical, or choice edge. An ordinary non-validation capability
edge is likewise not silently filtered. Excluded validation producers remain
in request/certificate roots and are checked separately.
For pair, migration, compatibility, and extension records the same named
validation machinery is already absent from `subjectReferences` by the typed
relation above rather than being subtracted after an edge is formed.

```text
producerSubjectRoots(CERTIFICATE_ADMISSION_SUBJECT(_,inner)) =
  producerSubjectRoots(inner)
producerSubjectRoots(CERTIFICATE_VALIDATION_SUBJECT(_,_,_,inner)) =
  producerSubjectRoots(inner)
producerSubjectRoots(s) = semanticSubjectRoots(s)
  for every other Subject variant

producerReachabilityRoots(s) =
  lift(required(s)) union producerSubjectRoots(s)

producerReachable(s,U,gate) = the least exact set containing
  producerReachabilityRoots(s) and closed under every derived association
  edge and every `producerSubjectReferences(recordAt(k,U),gate)` edge from a
  `PRESENT` record at each reached key

subjectProducerSet(s,U,gate) = producerOf(semanticPayload(s)) union
  UNION(producerOf(recordAt(k,U)) for every PRESENT record at every
        k in producerReachable(s,U,gate))

subjectProducerSet(s,U) =
  subjectProducerSet(s,U,NO_VALIDATION_EXCLUSIONS)
validationSubjectProducerSet(s,U,c,v,root) =
  subjectProducerSet(s,U,VALIDATION_EXCLUSIONS(c,v,v.service_key,root))
validationReferenceProducers(VALIDATION_CERTIFICATE(c)) = producerOf(c)
validationReferenceProducers(VALIDATION_CAPABILITY(v)) =
  producerOf(v) union producerOf(v.service_key)
validationReferenceProducers(VALIDATION_TRUST_ROOT(t)) = producerOf(t)
validationBindingProducerSet(s,U) =
  UNION(validationReferenceProducers(x) |
        x in admissionBindingReferences(s,U))
```

For ordinary service use, `gate=NO_VALIDATION_EXCLUSIONS`; for certificate or
admission validation it is the exact gate tuple naming the candidate
certificate, validator capability/service, and certificate-admission root.
Both use this same reachability definition. The resulting set includes the
owners of every reachable declaration, derived syntax-to-binding association,
binding, profile, pair declaration/binding, semantic dependency and
ContractSpec, authority/source, migration source/target environment,
compatibility, semantic extension, model record, lexical/choice coordinate,
reasoning/joint subject, discovery target, and package member. Only the three
explicit validation-root classes above are filtered; semantic roots are never
filtered. `validationBindingProducerSet` is not unioned into the semantic
subject set: its exact certificate, validator/service, and root producers are
compared separately by the mandatory inequalities and exact lookups. This
preserves all validation ownership information without manufacturing a
semantic edge.

This covers exact Contract/formula, value-admission, function, predicate,
profile, pair, authority candidate, migration, compatibility, extension,
reasoning/joint, certificate/admission, model-contract, discovery, environment,
record-target, and package subjects. A plugin-owned key with a missing/inconsistent owner component is
malformed, never an owner-unknown fallback. If the same record identity derives
different producer sets, composition conflicts. A validator capability must
derive exactly one `PLUGIN_PRODUCER`; otherwise it is malformed. Trust-policy
and root owners always derive the same embedding-policy producer, remain
distinct from plugin producers and `ABI_PRODUCER`, and cannot be asserted by a
package field.

The derived association algebra is exhaustive:

```text
association(K1_DECLARATION(d),U) =
  {(DECLARATION(d),BINDING(d))} when d.kind is LITERAL/FUNCTION/PREDICATE
association(K1_SYMBOL(s),U) =
  {(SYMBOL(s),DECLARATION(d)),(SYMBOL(s),BINDING(d))}
  where recordAt(SYMBOL(s),U) uniquely declares d
association(K1_EVENT(e),U) = {(EVENT(e),DECLARATION(d))}
  where d is the unique event declaration
association(K1_PROFILE(p),U) = {(PROFILE(p),PROFILE_BINDING(p))}
association(K1_PAIR(p),U) =
  {(PAIR(p),PAIR_DECLARATION(p)),(PAIR(p),PAIR_BINDING(p))}
association(K1_PLUGIN(p),U) = {(PLUGIN(p),PLUGIN(p)) as identity presence only}
association(k,U) = {} for no other K1SyntaxKey
```

The plugin identity-presence equation adds no graph self-edge; it only checks
presence. Missing or ambiguous symbol/event/pair declaration mapping is
malformed. Binding/profile/pair-binding association targets remain present in
the graph even when their record is absent, producing the exact open state.
Associations are derived bridges, never producer proper edges, and cannot be
supplied, removed, or replaced.

For every `Subject s`, the total environment is:

```text
R = subjectRoots(s)
A = least association edges reachable from lift(required(s))
P = least proper-edge targets reachable from R union RANGE(A)
S = every source reached from R by an association/proper-edge interleaving
V = admissionBindingReferences(s,U) union
    UNION(validationReferences(recordAt(k,U)) for every PRESENT k in S)

DependencyEnvironment(s,U) = (
  syntax_root_keys = required(s),
  subject_root_keys = R,
  binding_association_edges = A,
  expanded_root_keys = R union RANGE(A),
  proper_dependencies = targets of proper edges from reachable sources,
  transitive_dependency_closure =
    every non-root target reachable through any finite association/proper-edge
    interleaving,
  validation_references = V
)
```

`recordAt` is applied at every reachable source. Cycle rejection and the
missing-status rules above precede closure. Requests derive this environment
from `subjectOf(request)`: their semantic graph adds
`semanticRequestRoots`, while validation/discovery lookup additionally uses
the non-proper `requestRoots`. Certificates analogously use
`certificateProperReferences` for their semantic graph and
`certificateRoots` for validation lookup. A derived certificate-validation
request uses `certificateValidationRoots`; none of these operation-root unions
adds a `properEdges` member from the four validation-bound semantic subject
records. Outgoing request/envelope edges remain exactly those listed in the
exhaustive `subjectReferences` equations. The frozen K1 `Dependencies` facet, composition equality,
and full-Contract equivalence remain exactly `syntax_root_keys=required(s)`;
K2 semantic roots, associations, services, certificates, and proper closure do
not rewrite it. `validation_references` is derived, compared by exact finite-set
equality, and never traversed as semantic closure.

A descriptor may carry derived proper dependencies, but validation recomputes
roots, proper edges, and closure. The carried statement must equal the
recomputed set and can never replace `required(C)` or `required(F)`.
Missing declarations are malformed. Valid declarations with missing exact
bindings are open. Exact meanings with no compatible service remain closed but
not evaluable.

`choice_bindings` is recomputed from unique validated Contract choice records
and exact `BIND_CHOICE(choice_id)` authority facts. `chi_C` is then the value
projection of those entries. A missing, supplied alternate, or altered choice
entry makes the request or certificate malformed. `LEXICAL_BINDING` and
`CHOICE_BINDING` keys cover every scope/choice coordinate that a logical
relation can observe.

### 3.4 Exact versions and compatibility limits

Every version occurrence is exact. A compatibility claim can establish only
the dimensions it names, such as logical-record shape acceptance or protocol
request/result preservation, after its validator and exact trust root are
admitted through the compatibility request/result path.
It proves no denotational equivalence, closure, relation, authority, profile
coverage, or key substitutability.

No version ordering selects semantics. “Latest,” a range, a display-name match,
an implicit alias, first-found discovery, and undeclared backward
compatibility are invalid binding rules. Any change to a plugin exact version
changes every owned exact key. A migration may relate old and new keys only
under section 8; it never makes them identical and never mutates the original
Contract.

## 4. Semantic bindings and model-facing contracts

### 4.1 Binding validation and deterministic meaning

For every literal, function, or predicate declaration, at most one
`SemanticBinding` has the derived `BindingKey`. Binding validation requires:

- exact declaration/key/kind and ABI agreement;
- literal denotation returning exactly one value admitted by the declared
  result type;
- function meaning accepting only the declared positional types and returning
  only `TERM_VALUE` of the result type or `TERM_ERROR`;
- predicate meaning accepting only the declared positional types and returning
  exactly K1 `Eval`;
- `permitted_facet_inputs` exactly equal to the declaration's position
  facets, with no implicit anchor;
- complete proper/transitive declaration and semantic dependencies, with
  subject roots kept separate;
- exact section 3.3 support for every meaning/evidence/access/unknown/error
  contract, with `proper_semantic_dependencies` and `dependency_closure`
  equal to the derived union and least fixed point;
- explicit evidence schema and access boundary, including the exact empty
  contract when nothing is accessible;
- for predicates, explicit stable unknown and evaluation-error contracts; for
  literals/functions, `NOT_APPLICABLE` unknown behavior and explicit term
  error behavior;
- the same complete result for the same explicit primary inputs and exact
  finite lower-level `DependencyObservationEnvironment`; the containing
  `Delta`, `Sigma`, binding set, and `SemanticEnvironment` are never relation
  inputs.

The meaning is independent of evaluator availability. An absent binding leaves
closure open; an incompatible present binding is malformed. A service cannot
supply a substitute meaning.

### 4.2 Access and broad-atom boundary

`access_boundary` is a closed list of input positions, admissible evidence
schemas, and referenced semantic dependencies. The service receives exactly
those declared positional values. A `State`, `Trace`, or `EvidenceStore`
is visible only as an anchor-derived value in a declared position. No
predicate request carries a full `Outcome`, Contract, choice map, authority
context, source task, challenge identity, expected answer, hidden target,
undeclared repository state, or evidence outside its schema.

A broad atom is conformant only under the same typed, facet, dependency,
evidence, access, unknown, error, determinism, and capability rules as every
other atom. “The service knows whether it is correct” is neither a meaning
contract nor admissible access. Attempted undeclared access is a protocol
violation and `EVALUATION_ERROR`; an interface that declares privileged
expected access is package-malformed.

### 4.3 Model-facing contract identity

A `ModelContract` is one complete producer-supplied structured projection of
exactly one machine-facing binding. Every ordinary literal/function/predicate
binding requires at least one complete record targeting it; each exact
`ModelContractKey` resolves to exactly one record after equal logical duplicate
coalescing, while different locale/version keys may be additional complete
translations. An `EventPairBinding` is stricter: it names one exact
`occurrence_model_contract_key`, and the package must contain exactly one
record at that key targeting the pair-owned occurrence projection. K2 derives
no document namespace, locale, or document version from T3/A1.

For pair declaration `pd`, pair binding `pb`, occurrence declaration `od`, and
projection `op=OccurrenceBindingProjection(pd,pb,sb)`, occurrence record `m`
is conformant iff every following equality holds:

```text
m.model_contract_key = pb.occurrence_model_contract_key
m.model_contract_key.target_semantic_identity = BINDING_IDENTITY(od.key)
m.model_contract_key.document_namespace =
  pb.occurrence_model_contract_key.document_namespace
m.model_contract_key.locale_identity =
  pb.occurrence_model_contract_key.locale_identity
m.model_contract_key.exact_document_version =
  pb.occurrence_model_contract_key.exact_document_version
m.target_binding_key = od.key = pb.occurrence_binding_key
m.exact_symbol_key = od.symbol_key = pd.occurrence_symbol
m.exact_signature = (Trace)->Bool
m.exact_facet_positions = ({trace})
m.evidence_contract = op.evidence_schema
m.unknown_contract = op.unknown_contract
m.error_contract = op.evaluation_error_contract
m.semantic_contract_reference = op.meaning_contract.contract_key
m.capability_summaries = {
  modelCapabilitySummary(c) |
  c is a conformant package CapabilityDescriptor,
  BINDING_TARGET(od.key) is in c.supported_targets
}
```

`modelCapabilitySummary(c)` is exactly the projection of the seven displayed
`ModelCapabilitySummary` fields from `c`: capability key, service role,
supported judgments, class, sound-fragment key, optional complete-fragment
key, and complete dependency scope. Conversely every summary must have exactly
one conformant descriptor producing that projection and targeting the same
occurrence binding. Summary equality is complete field equality; it states
declared capability only and never current discovery, trust, or availability.
The evidence, unknown, and error contracts are the identical `ContractSpec`
records and roles used by `op`, not paraphrases. The semantic-contract
reference is the exact occurrence meaning-contract key; documentation creates
no second meaning.

The same total field-by-field rule applies to every ordinary-binding record using its
exact declaration signature, facet positions, semantic-contract reference,
and three binding contracts; literals use `NO_SYMBOL_LITERAL`. A pair-named
required key with no record, or no model record targeting an ordinary binding,
leaves the model-facing binding
`OPEN_BINDINGS(model contract)` and makes the package incomplete; one record
with any wrong field is `MALFORMED(model/machine contract mismatch)`; two
unequal records at the same exact key are `CONFLICT(model contract)`.
Additional locales/translations require different complete
`ModelContractKey`s and never satisfy the one pair-named required key. Explanatory
text is optional diagnostic content and creates neither denotation nor
authority.

Model lookup is exact:
`recordAt(MODEL_CONTRACT(pb.occurrence_model_contract_key),U)` returns the
sole conformant record or the exact absent/malformed/conflict status above.
Aliases are permitted only through `AliasBinding`; resolving an alias yields
its recorded target and never performs display-name or version selection.

## 5. Invocation, values, truth, evidence, and failure protocol

### 5.1 Typed requests

```text
ValueAdmissionRequest = (
  abi_version : AbiVersion,
  type_key : DeclarationKey[TYPE],
  value : Value,
  semantic_environment : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  dependency_environment : DependencyEnvironment,
  capability_target : TYPE_ADMISSION_TARGET(
    type_key, semanticIdentity(semantic_environment)),
  capability_key : CapabilityKey
)
FunctionRequest = (
  abi_version : AbiVersion,
  symbol_key : SymbolKey[FUNCTION],
  binding_key : BindingKey,
  semantic_environment : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  dependency_environment : DependencyEnvironment,
  arguments : sequence(Value),
  capability_target : BINDING_TARGET(binding_key),
  capability_key : CapabilityKey
)
PredicateRequest = (
  abi_version : AbiVersion,
  symbol_key : SymbolKey[PREDICATE],
  binding_key : BindingKey,
  semantic_environment : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  dependency_environment : DependencyEnvironment,
  arguments : sequence(Value),
  capability_target : BINDING_TARGET(binding_key),
  capability_key : CapabilityKey
)
ProfileRequest = (
  abi_version : AbiVersion,
  profile_key : ProfileKey,
  semantic_environment : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  coverage_subject : typed profile-specific subject,
  capability_target : PROFILE_TARGET(profile_key),
  capability_key : CapabilityKey
)
PairAdmissionRequest = (
  abi_version : AbiVersion,
  pair_key : EventScopePairKey,
  semantic_environment : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  complete_dependencies : DependencyEnvironment,
  capability_target : PAIR_TARGET(pair_key),
  capability_key : CapabilityKey
)
AuthorityAdmissionRequest = (
  abi_version : AbiVersion,
  candidate : AuthorityFactCandidate,
  environment_without_fact : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  complete_dependencies : DependencyEnvironment,
  capability_target : ENVIRONMENT_JUDGMENT_TARGET(
    AUTHORITY_FACT_ADMISSION, (candidate),
    semanticIdentity(environment_without_fact)),
  capability_key : CapabilityKey
)
MigrationAdmissionRequest = (
  abi_version : AbiVersion,
  migration : MigrationDeclaration,
  semantic_environment : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  complete_dependencies : DependencyEnvironment,
  capability_target : ENVIRONMENT_JUDGMENT_TARGET(
    MIGRATION_RELATION_ADMISSION, (migration),
    semanticIdentity(semantic_environment)),
  capability_key : CapabilityKey
)
CompatibilityAdmissionRequest = (
  abi_version : AbiVersion,
  claim : CompatibilityClaim,
  semantic_environment : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  complete_dependencies : DependencyEnvironment,
  capability_target : ENVIRONMENT_JUDGMENT_TARGET(
    COMPATIBILITY_CLAIM_ADMISSION, (claim),
    semanticIdentity(semantic_environment)),
  capability_key : CapabilityKey
)
SemanticExtensionAdmissionRequest = (
  abi_version : AbiVersion,
  extension : SemanticExtension,
  environment_without_extension : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  complete_dependencies : DependencyEnvironment,
  capability_target : ENVIRONMENT_JUDGMENT_TARGET(
    SEMANTIC_EXTENSION_ADMISSION, (extension),
    semanticIdentity(environment_without_extension)),
  capability_key : CapabilityKey
)
DiscoveryRequest = (
  abi_version : AbiVersion,
  target : exactly one CapabilityTarget,
  judgment : JudgmentTag,
  semantic_environment : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  required_fragment : ContractSpec[Service],
  complete_dependency_scope : finset(DependencyKey)
)

ReceivingRuleTag =
    RECEIVE_REASONING_JUDGMENT | RECEIVE_PROFILE_COVERAGE
  | RECEIVE_PAIR_COHERENCE | RECEIVE_AUTHORITY_FACT
  | RECEIVE_MIGRATION_RELATION | RECEIVE_COMPATIBILITY_CLAIM
  | RECEIVE_SEMANTIC_EXTENSION

CertificateValidationRequest = (
  abi_version : AbiVersion,
  validator_key : CapabilityKey,
  certificate_key : CertificateKey,
  envelope_identity : exact complete CertificateEnvelope identity,
  original_request_identity : RequestIdentity,
  original_subject : Subject,
  original_subject_identity : exact complete Subject identity,
  claimed_conclusion : exact certificate-kind-specific conclusion,
  validator_capability_target : CapabilityTarget,
  validator_judgment : JudgmentTag,
  validator_service_role : ServiceRole,
  fragment : ContractSpec[Service],
  complete_dependencies : DependencyEnvironment,
  semantic_environment : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  receiving_rule : ReceivingRuleTag,
  service_use_trust_root_keys : nonempty finset(TrustRootKey),
  service_use_trust_target : TrustTarget,
  certificate_admission_trust_root_key : TrustRootKey,
  certificate_admission_trust_target : TrustTarget
)
```

`CertificateValidationRequest` is derived after envelope formation and is
distinct from the producer's `request_binding`; a plugin cannot supply it.
For envelope `c`, every field has one exact constructor:

```text
certificateValidationRequest(c) = (
  abi_version = c.request_binding.abi_version,
  validator_key = c.validator_key,
  certificate_key = c.certificate_key,
  envelope_identity = IDENTITY_OF(c),
  original_request_identity = IDENTITY_OF(c.request_binding),
  original_subject = subjectOf(c.request_binding),
  original_subject_identity = IDENTITY_OF(subjectOf(c.request_binding)),
  claimed_conclusion = c.claimed_conclusion,
  validator_capability_target = c.request_binding.capability_target,
  validator_judgment = judgmentOf(c.request_binding),
  validator_service_role = validationRole(c.certificate_kind),
  fragment = c.fragment,
  complete_dependencies = c.dependencies,
  semantic_environment = c.environment,
  trust_environment = trustEnvironmentOf(c.request_binding),
  receiving_rule = receivingRule(c.certificate_kind),
  service_use_trust_root_keys =
    CapabilityDescriptor(c.validator_key).required_trust_roots,
  service_use_trust_target = SERVICE_USE_TRUST_TARGET(
    c.validator_key, judgmentOf(c.request_binding),
    serviceUseSubject(c.request_binding), semanticIdentity(c.environment)),
  certificate_admission_trust_root_key = c.trust_root_key,
  certificate_admission_trust_target = trustTarget(c.request_binding)
)
```

`validationRole` is total: reasoning witness/proof/model/counterexample and
internal/full-contract certificates map to `REASONING`; profile evidence maps
to the exact `PROFILE_CONCRETE|PROFILE_SYMBOLIC` role stated by the original
request; pair certificates map to `PAIR_VALIDATION`; and authority, migration,
compatibility, and semantic-extension certificates map respectively to their
same-named validation roles. `receivingRule` maps the same seven groups to the
seven `ReceivingRuleTag` constructors. Any kind/request ambiguity or mismatch
is a malformed envelope, not a default role.

The derived request conforms iff all displayed equalities hold; its validator
descriptor contains exactly the target, judgment, role, fragment, complete
dependency scope, and required root; its semantic environment equals both the
envelope and original request environment (using the exact target-excluded
environment for authority/extension); its displayed service root set and
certificate-admission root key are admitted for their respective targets; and
its two trust targets are distinct
permissions checked independently even if one root record lists both. The
ordinary validator-use target never substitutes for certificate admission,
and the admission target never establishes service availability.

For pair, migration, compatibility, or semantic-extension validation, it also
requires the exact derived set
`admissionBindingReferences(v.original_subject,U)` to be a subset of the
original admission request's complete derived
`complete_dependencies.validation_references`, while that complete set still
equals §3.3's full `V`. The candidate envelope fields must equal the direct
subject references: the unique direct certificate equals `v.certificate_key`, the
unique direct validator equals `v.validator_key`, and the direct trust root,
when present, equals `v.certificate_admission_trust_root_key`. The same set is
included in `certificateValidationRoots(v,U)` for exact lookup but is not in
the semantic proper-dependency graph. Thus the derived request cannot select a
different certificate, validator, service, or trust root and cannot use a
missing reference as an empty/default binding.

For `ValueAdmissionRequest`, `semantic_environment` must contain the exact type
declaration and lexical and choice coordinates relevant to the
value, and every declaration coordinate observed by
`admitted_value_domain`. Its dependency environment has that type declaration
as a root and exactly the proper-edge closure of the admission contract. The
type-admission descriptor must cover the same environment target and complete
closure. A context-free target, missing support, extra scope entry, or smaller
producer dependency set is malformed and no admission service is invoked.

Every request carries one exact `semantic_environment` and one separate exact
`trust_environment`; neither contains the other. Discovery and invocation
must repeat both records exactly. The target's embedded environment identity,
where present, must equal `semanticIdentity` of that exact semantic
environment. These equalities prevent discovery under one semantic/trust pair
and invocation under another without a recursive type.

The argument sequence length, positions, and admitted types must equal the
exact declaration. `symbol_key` and `binding_key` must name that same
declaration and meaning. The dependency environment must equal the
mechanically derived and transitively closed environment; it is never a
caller-maintained list. The requested capability must advertise the exact
tagged target, judgment, dependency scope, and applicable sound fragment.
The request target must be a member of
`CapabilityDescriptor.supported_targets` and its tag must agree with the
service role. `PairAdmissionRequest.semantic_environment` contains the complete pair,
member, event/type, meaning, and support dependencies. A reasoning request uses
the exact environment/judgment target defined in section 6.2. Target mismatch
is a malformed request; no service is invoked and no similarly named binding,
profile, pair, type, or environment can substitute.

For a candidate `a`,
`environmentWithoutAuthorityFact(E,a.authority_fact_key)` is exactly `E` with
that map key removed from `authority_facts` and every other field unchanged.
An `AuthorityAdmissionRequest` is conformant only when its displayed
environment is this exact projection of the proposed receiving environment,
the candidate's key fields exactly equal the authority/source/principal/role
named by `admission_subject_data`, and neither `required` nor the derived
dependency closure contains `AUTHORITY_FACT(a.authority_fact_key)` as a root.
The candidate key's `AuthorityRef`, `SourceRef`, their structural producers,
and every declaration dependency of its typed subject data remain reachable;
only the not-yet-admitted fact record is absent. If the candidate key already
exists in the supplied pre-admission map, the request is malformed.

Each environment-level admission request carries its complete exact subject,
semantic and trust environments, roots, proper dependencies, and closure. An authority subject is
the exact candidate plus environment without its fact; a migration and compatibility subject is its
full exact record; an extension request contains the full extension while
`environment_without_extension` excludes that unadmitted extension and thus
prevents self-support. Discovery must find the matching admission service
role, `JudgmentTag`, target, fragment, dependency scope, and every required
independently admitted ordinary service-use trust root before validation is
invoked.

For pair, migration, compatibility, and semantic-extension admission, the
request's exact `complete_dependencies.validation_references` must contain the
derived `admissionBindingReferences(subjectOf(request),U)` and every validation
reference of a semantically reached record, with neither omission nor extra
entry. The request's `capability_key` must equal the one
`VALIDATION_CAPABILITY` named by its direct subject. Before discovery, that
reference is fixed; the corresponding `DiscoveryRequest` uses the request's
exact target, judgment, semantic/trust environments, fragment, and dependency
scope, and `EXACT_TARGET_FOUND` may name only that exact capability. The named
`VALIDATION_CERTIFICATE` must resolve to the envelope whose
`request_binding` is this exact admission request, and any direct
`VALIDATION_TRUST_ROOT` must equal that envelope's `trust_root_key`. An
independent pair proof has no direct root field, so its exact root is taken
only from that named envelope; migration, compatibility, and extension require
equality to their separately named root. Missing, conflicting, wrong-kind, or
unequal bindings retain their exact lookup/trust status and no admission
request is invoked. None of these operation checks adds a semantic proper
edge.

A predicate receives only `arguments`. Neither the logical request nor any
capability-dependent projection includes a Contract, full `Outcome`,
`chi_C`, authority context, implicit anchor, or undeclared evidence. A
function has the same access restriction. The environment proves semantic
identity, trust scope, and closure; the invocation projection presented to the
denotational meaning contains only the admitted positional arguments and is not
an extra data channel to that meaning.

Value admission is checked before a value is used. `VALUE_NOT_ADMITTED`
means that the abstract value is outside the declared type relation. If such a
value is used as an argument, event payload, choice, witness component, or
result, the containing object is malformed rather than factually unknown.
`ProfileRequest.coverage_subject` is exactly the typed subject named by the
profile's `coverage_meaning`; its environment must make that subject closed.

### 5.2 Exact results

```text
ValueAdmissionResult =
    VALUE_ADMITTED(type_key, value)
  | VALUE_NOT_ADMITTED(type_key, value)
  | ADMISSION_ERROR(nonempty finset(EvaluationErrorReason))

TermResult =
    TERM_VALUE(value)
  | TERM_ERROR(nonempty finset(EvaluationErrorReason))

Eval =
    VALUE(TRUE | FALSE | UNKNOWN,
          evidence_refs : finset(EvidenceRef),
          unknown_reasons : finset(UnknownReason))
  | ERROR(evaluation_errors : nonempty finset(EvaluationErrorReason),
          evidence_refs : finset(EvidenceRef),
          unknown_reasons : finset(UnknownReason))

FormulaResult = Eval

ProfileResult =
    PROFILE_COMPLETE(profile_key, finset(EvidenceRef))
  | PROFILE_INCOMPLETE(profile_key,
                       nonempty finset(ProfileDimensionKey))
  | PROFILE_UNKNOWN(profile_key,
                    nonempty finset(UnknownReason))
  | EVALUATION_ERROR(nonempty finset(EvaluationErrorReason))
  | REASONING_ERROR(nonempty finset(ReasoningErrorReason))

PairValidationResult =
    PAIR_COHERENCE_ADMITTED(pair_key, certificate_key)
  | PAIR_INCOHERENCE_ADMITTED(
      pair_key, certificate_key, admitted_trace : Trace,
      scope_aggregate_eval : Eval, occurrence_eval : Eval)
  | PAIR_VALIDATION_REJECTED(
      pair_key, nonempty finset(CertificateRejectionReason))
  | EVALUATION_ERROR(nonempty finset(EvaluationErrorReason))
  | REASONING_ERROR(nonempty finset(ReasoningErrorReason))

AuthorityAdmissionResult =
    AUTHORITY_FACT_ADMITTED(authority_fact_key, certificate_key)
  | AUTHORITY_FACT_NOT_ADMITTED(
      authority_fact_key, nonempty finset(CertificateRejectionReason))
  | REASONING_ERROR(nonempty finset(ReasoningErrorReason))
MigrationAdmissionResult =
    MIGRATION_RELATION_ADMITTED(migration_key, certificate_key)
  | MIGRATION_RELATION_NOT_ADMITTED(
      migration_key, nonempty finset(CertificateRejectionReason))
  | EVALUATION_ERROR(nonempty finset(EvaluationErrorReason))
  | REASONING_ERROR(nonempty finset(ReasoningErrorReason))
CompatibilityAdmissionResult =
    COMPATIBILITY_CLAIM_ADMITTED(claim_key, certificate_key)
  | COMPATIBILITY_CLAIM_NOT_ADMITTED(
      claim_key, nonempty finset(CertificateRejectionReason))
  | REASONING_ERROR(nonempty finset(ReasoningErrorReason))
SemanticExtensionAdmissionResult =
    SEMANTIC_EXTENSION_ADMITTED(extension_key, certificate_key)
  | SEMANTIC_EXTENSION_NOT_ADMITTED(
      extension_key, nonempty finset(CertificateRejectionReason))
  | REASONING_ERROR(nonempty finset(ReasoningErrorReason))
```

Result conformance is relative to the exact request and semantic environment,
not merely to these carrier shapes. After positional input admission, derive
`D(c,x,U)=dependencyObservations(c,x,U)` in any valid proper-DAG topological
order (all give the same exact map) and
then the unique denotational result by these total equations:

```text
expectedAdmission(r,E) =
  VALUE_ADMITTED(r.type_key,r.value) iff
    TypeDeclaration(r.type_key).admitted_value_domain.logical_relation(
      r.value,D(admitted_value_domain,r.value,U))=admitted;
  otherwise VALUE_NOT_ADMITTED(r.type_key,r.value)

expectedLiteral(d,b,E) =
  b.meaning_contract.logical_relation(
    d.literal_identity,D(b.meaning_contract,d.literal_identity,U)) : TermResult

expectedFunction(r,E) =
  SemanticBinding(r.binding_key).meaning_contract.logical_relation(
    r.arguments,D(meaning_contract,r.arguments,U)) : TermResult

expectedPredicate(r,E) =
  recordAt(BINDING(r.binding_key),U).meaning_contract.logical_relation(
    r.arguments,D(meaning_contract,r.arguments,U)) : Eval

expectedPairOccurrence(r,E,T) =
  DEFINITIONAL_T3_A1:
    ANY_RESULT({expectedPredicate(scope request for e.event_value,E)
                | e occurs in T});
  INDEPENDENT_COHERENCE_PROOF:
    OccurrenceBindingProjection(pair declaration,pair binding,scope binding)
      .meaning_contract.logical_relation(
        (T),D(meaning_contract,(T),U)), which the admitted
    proof establishes equal to that same complete T3/A1 aggregate for every T

expectedProfile(r,E) =
  ProfileBinding(r.profile_key).coverage_meaning.logical_relation(
    r.coverage_subject,
    D(coverage_meaning,r.coverage_subject,U)) : decisive or unknown ProfileResult
```

The universe `U` contains exactly the request's semantic environment, separate
trust environment, and request-bound records; it is never passed to a logical
relation. Every lookup uses the unique reachable binding established by
section 3.3. For a
pair-owned occurrence `PredicateRequest`, `expectedPredicate` is replaced by
`expectedPairOccurrence` and the trace is the admitted sole positional value.
Thus definitional and independently proved pair meanings have the same
complete-result equality obligation. Literal evaluation has no ordinary v0
service role: the exact literal result is resolved from its Sigma binding during
term evaluation, and binding validation (or any later materialization of that
result) requires equality to `expectedLiteral`.
The expected record is a kernel-side logical validation derivation, not a
request field or invocation input. It is never exposed to the producer as an
expected answer, oracle bit, hidden target, or comparison callback.

For value admission, function application, predicate/pair-occurrence
evaluation, and profile checking,
`RESULT_CONFORMANT(x,r,E)` holds iff (1) `x` has the exact request-permitted
carrier tag, types, and nonempty-set invariants and (2) `x` equals the applicable
expected result as a complete logical record. Equality includes the exact value,
truth, evidence-reference set, unknown-reason set, and evaluation-error set;
returning a different stable evidence or reason identity is semantic inequality,
not a diagnostic difference. Determinism makes the expected result unique.
An exact expected `TERM_ERROR` or `Eval.ERROR` is conformant and is preserved;
it is not repaired into a value or truth.

A carrier-valid but unequal admission, `TermResult`, `Eval`, or profile result
is `MALFORMED_RESULT(SEMANTIC_MISMATCH)` and an invocation protocol failure. The claimed value,
truth, metadata, or admission is discarded. A returned admission-service
`ADMISSION_ERROR`, concrete/symbolic profile error, or other declared
failure-result tag is governed by the descriptor's exact `failure_contract` and
maps by the total section 5.4 role function; it is never a substitute expected
denotation.
Pair, authority, migration, compatibility, semantic-extension, certificate,
and reasoning results are not denotational evaluator results: their conformance
is instead exact request/environment equality plus the kind-specific admitted
conclusion, rejection, decisiveness, and failure rules in sections 6--8. They
must not be compared to a fabricated atom meaning or relabeled across receiving
rules.

`TERM_VALUE` must contain a value admitted at the declared function result
type. `TERM_ERROR` contains no value. A literal binding must yield an
admitted `TERM_VALUE`; literal failure makes the binding incompatible.

For `Eval`, `VALUE(UNKNOWN,...)` requires a nonempty unknown-reason set.
`VALUE(TRUE,...)` and `VALUE(FALSE,...)` may contain unknown reasons
retained from semantically relevant children. Every `ERROR` has a nonempty
evaluation-error set. A predicate service returns one atomic `Eval`; it
cannot apply or replace K1 T1--T4 or A1--A2. The kernel alone performs
connective, grant, requirement, authorization, and acceptance aggregation.

`PROFILE_COMPLETE` requires the evidence demanded by the coverage meaning
and all exact dimensions; an exact empty-dimension profile may therefore have
an empty evidence set.
`PROFILE_INCOMPLETE` requires a known nonempty omitted set.
`PROFILE_UNKNOWN` is completed factual inconclusiveness about coverage.
Concrete checker or protocol failure is `EVALUATION_ERROR`; symbolic checker
or reasoning-protocol failure is `REASONING_ERROR`. These five tags are
pairwise disjoint and none changes acceptance, satisfiability, or intent
completeness.

For `PAIR_INCOHERENCE_ADMITTED`, both `Eval` records are complete values of
the exact K1 algebra, including truth/evidence/unknown/error sets. The trace
must be admitted under the exact request Delta; `scope_aggregate_eval` must be
the exact T3/A1 aggregate of the scope predicate over every event in that
trace; `occurrence_eval` must be the exact
`OccurrenceBindingProjection.meaning_contract` result on that same trace;
and the two records must be unequal. Any missing field, non-admitted trace,
different environment, or equal result records makes the result malformed.
The other admission-result tags echo their request identity and certificate;
their `NOT_ADMITTED` variants are nondecisive and grant no admission.

### 5.3 Stable evidence and reason equality

```text
EvidenceRef = (
  issuer_scope : IssuerScope, evidence_namespace, local_identity,
  schema_binding : ContractSpecKey
)
UnknownReason = (
  issuer_scope : IssuerScope, taxonomy_key, semantic_parameters
)
EvaluationErrorReason = (
  issuer_scope : IssuerScope, taxonomy_key, semantic_parameters
)
ReasoningErrorReason = (
  issuer_scope : IssuerScope, taxonomy_key, semantic_parameters
)
CertificateRejectionReason = (
  issuer_scope : IssuerScope, taxonomy_key, semantic_parameters
)
InterfaceFailureReason = (
  issuer_scope : exactly ABI_REASON_ISSUER,
  reason_code : InterfaceFailureCode,
  capability_identity : CapabilityKey | NO_CAPABILITY,
  request_identity : RequestIdentity | NO_REQUEST,
  expected_contract_identity :
    ExpectedResultContractIdentity | NO_EXPECTED_CONTRACT,
  offending_result_identity : OffendingResultIdentity,
  trust_root_status_reason : TrustRootStatusReason | NO_TRUST_ROOT_STATUS_REASON
)
```

The seven sorts, including `TrustRootStatusReason`, are disjoint. Equality is
exact component equality. Parameters
are typed finite logical records whose equality is defined by their declared
schema; they may contain exact keys, values, result identities, and request or
contract-spec keys, plus the closed `TrustRootStatusReason` only in the exact
request-time root projections of §5.4, but never a `ContractSpec`, logical relation,
`SemanticEnvironment`, `DependencyObservationEnvironment`, or
`TrustEnvironment` record. An untyped message is diagnostic only and cannot be
an identity parameter. Finite sets deduplicate equal members and have no order. Reordering
or repeating a transport occurrence therefore cannot change a result; two
unequal stable identities never coalesce because their prose looks similar.

An `EvidenceRef` identifies support admitted by its exact evidence schema. It
does not embed `TRUE`, success, authority, profile coverage, satisfiability,
or a relation conclusion. An unknown reason identifies what remains
unresolved; it grants no choice. Evaluation and reasoning reasons identify
failure in their own family and prove nothing in any logical family.

### 5.4 Malformed results and interface failures

```text
InterfaceFailure = (
  domain : DECLARATION | BINDING | DISCOVERY |
           CONCRETE_INVOCATION | REASONING_INVOCATION |
           CERTIFICATE_ADMISSION | PAIR_ADMISSION |
           AUTHORITY_ADMISSION | MIGRATION_ADMISSION |
           COMPATIBILITY_ADMISSION | SEMANTIC_EXTENSION_ADMISSION,
  kind : MALFORMED_REQUEST |
         MALFORMED_RESULT(MALFORMED_CARRIER | SEMANTIC_MISMATCH) |
         PROTOCOL_FAILURE | TRANSPORT_FAILURE |
         TRUST_FAILURE | DISCOVERY_FAILURE,
  reasons : nonempty finset(InterfaceFailureReason)
)

InterfaceFailureCode = INTERFACE_FAILURE_CODE(
  exact InterfaceFailure.domain, exact InterfaceFailure.kind)

ExpectedResultContractIdentity =
    DENOTATIONAL_CONTRACT(ContractSpecKey)
  | RECEIVING_RULE(AbiVersion, JudgmentTag, exact Subject identity)
  | DISCOVERY_RULE(AbiVersion, CapabilityTarget, JudgmentTag)

OffendingResultIdentity =
    RESULT_OFFENDER(ResultIdentity)
  | MALFORMED_RESULT_SENTINEL
  | NO_RESULT_SENTINEL
```

`InterfaceFailure` is not a `Truth`, `Eval`, profile result, consistency
result, or relation result. A malformed declaration, binding, or request is
rejected before invocation. A malformed completed result is not repaired,
defaulted, partially accepted, or treated as unknown.

Failure-domain selection is total and fixed:

```text
domainOf(VALUE_ADMISSION | FUNCTION_EVALUATION |
         PREDICATE_EVALUATION | PROFILE_CONCRETE) = CONCRETE_INVOCATION
domainOf(PROFILE_SYMBOLIC | REASONING) = REASONING_INVOCATION
domainOf(PAIR_VALIDATION) = PAIR_ADMISSION
domainOf(AUTHORITY_VALIDATION) = AUTHORITY_ADMISSION
domainOf(MIGRATION_VALIDATION) = MIGRATION_ADMISSION
domainOf(COMPATIBILITY_VALIDATION) = COMPATIBILITY_ADMISSION
domainOf(SEMANTIC_EXTENSION_VALIDATION) = SEMANTIC_EXTENSION_ADMISSION
malformed certificate envelope or certificate receiving-rule failure
  = CERTIFICATE_ADMISSION
pre-invocation declaration, binding, discovery, and trust validation
  = respectively DECLARATION, BINDING, DISCOVERY, and DISCOVERY
```

Every displayed domain accepts every `InterfaceFailure.kind`; the
`INTERFACE_FAILURE_CODE(domain,kind)` product is therefore a stable total code.
Kinds that occur before invocation retain their pre-invocation projection
below rather than being forced through a service role.

The exact expected-contract function is total over requests:

```text
expectedContract(value admission r) =
  DENOTATIONAL_CONTRACT(TypeDeclaration(r.type_key)
                         .admitted_value_domain.contract_key)
expectedContract(function/predicate r) =
  DENOTATIONAL_CONTRACT(recordAt(BINDING(r.binding_key),U)
                         .meaning_contract.contract_key)
expectedContract(profile r) =
  DENOTATIONAL_CONTRACT(ProfileBinding(r.profile_key)
                         .coverage_meaning.contract_key)
expectedContract(discovery r) =
  DISCOVERY_RULE(r.abi_version,r.target,r.judgment)
expectedContract(certificate validation v) =
  RECEIVING_RULE(v.abi_version,v.validator_judgment,
                 v.original_subject)
expectedContract(every reasoning/admission r) =
  RECEIVING_RULE(r.abi_version,judgmentOf(r),subjectOf(r))
```

`capabilityForFailure(r)` is total: it is `NO_CAPABILITY` for discovery,
`r.validator_key` for `CertificateValidationRequest`, and
`r.capability_key` for every other invocation/admission request.
`failureReason(domain,kind,r,offender)` is the sole constructor for an
invocation-bound interface reason. It sets issuer to `ABI_REASON_ISSUER`, code
to `INTERFACE_FAILURE_CODE(domain,kind)`, capability to
`capabilityForFailure(r)`, request identity to
`IDENTITY_OF(r)`, expected contract to `expectedContract(r)`, and offender to
the supplied exact identity, and `trust_root_status_reason` to
`NO_TRUST_ROOT_STATUS_REASON`. Pre-request declaration/binding failures use the
same constructor with `NO_CAPABILITY`, `NO_REQUEST`,
`NO_EXPECTED_CONTRACT`, and `NO_RESULT_SENTINEL`. No message text, traversal
order, service-selected taxonomy, or omitted parameter can alter the reason.

`ABI_ROOT_DISCOVERY_UNRESOLVED` is the fixed ABI taxonomy key for the
request-time discovery projection below. For a concrete discovery or
pre-invocation request `r` and a conforming
`TRUST_ROOT_UNDECIDED(k,H)`, the only request-time uncertainty projection is:

```text
rootUndecidedReason(r,h) = UnknownReason(
  ABI_REASON_ISSUER, ABI_ROOT_DISCOVERY_UNRESOLVED,
  (IDENTITY_OF(r),expectedContract(r),h))
rootUndecidedReasons(r,H) =
  {rootUndecidedReason(r,h) | h in H}
```

The input set is nonempty, every `h.status_code` is exactly
`ROOT_DISCOVERY_UNRESOLVED`, and the constructor is injective in the displayed
tuple, so the result is nonempty after exact deduplication. This set is
conformant only in `DiscoveryResult.DISCOVERY_UNDECIDED` and its discovery
lifecycle projection. It yields `EVALUABILITY_UNKNOWN`; it is forbidden in
`Eval`, `ReasoningResult`, `ProfileResult`, or a public logical conclusion.
Thus a root status reason is not itself a K1 `UnknownReason`, and its one-way
request-time discovery projection cannot turn evaluability uncertainty into
logical/profile unknown or point back into the trust map.

For a conforming `TRUST_ROOT_INCOMPATIBLE(k,H)`, the only request-time
incompatibility projection is:

```text
rootIncompatibilityReason(r,h) = InterfaceFailureReason(
  issuer_scope = ABI_REASON_ISSUER,
  reason_code = INTERFACE_FAILURE_CODE(DISCOVERY,TRUST_FAILURE),
  capability_identity =
    h.implicated_capability when it is not NO_CAPABILITY,
    capabilityForFailure(r) otherwise,
  request_identity = IDENTITY_OF(r),
  expected_contract_identity = expectedContract(r),
  offending_result_identity = NO_RESULT_SENTINEL,
  trust_root_status_reason = h)
rootIncompatibilityReasons(r,H) =
  {rootIncompatibilityReason(r,h) | h in H}
```

This nonempty set is conformant only as the reasons of
`DiscoveryResult.SERVICE_INCOMPATIBLE`; it yields capability incompatibility
and `EVALUABILITY_MISSING`, not an `InterfaceFailure`, invocation failure,
logical unknown, or semantic result. Its reason code records the trust family
without collapsing incompatibility into failed root discovery.

For a concrete discovery or pre-invocation request `r` and a conforming
`TRUST_ROOT_FAILED(k,H)`, `rootFailureReason(r,h)` is the same canonical
constructor except that `trust_root_status_reason=h`; the common reason-code
family selects respectively `PROTOCOL_FAILURE` or `TRANSPORT_FAILURE`.
`rootFailure(r,k,H)` is `InterfaceFailure(DISCOVERY,that-kind,
{rootFailureReason(r,h) | h in H})`. The root-local payloads are nonempty and
distinct by exact equality, so this projection is nonempty and retains the
exact failed root/policy/capability coordinate. Undecided and incompatible
root judgments never use the failure constructor: they use only their two
distinct projections above. This request-time projection points from an
interface failure to a closed root-local reason; no root judgment contains the
resulting request, unknown reason, incompatibility reason, or failure, so every
identity dependency is one-way.

For a malformed result `x`, the constructor is total:

```text
resultFailure(r,x) =
  InterfaceFailure(domainOf(roleOf(r)),
    MALFORMED_RESULT(MALFORMED_CARRIER),
    {failureReason(domainOf(roleOf(r)),that-kind,r,
                   MALFORMED_RESULT_SENTINEL)})
  when x lacks a conforming carrier identity

resultFailure(r,x) =
  InterfaceFailure(domainOf(roleOf(r)),
    MALFORMED_RESULT(SEMANTIC_MISMATCH),
    {failureReason(domainOf(roleOf(r)),that-kind,r,
                   RESULT_OFFENDER(IDENTITY_OF(x)))})
  when x has a carrier identity but differs from the unique denotational
  result or exact receiving rule
```

For a validator result, `r` in these equations is always the derived
`CertificateValidationRequest`, never the producer's original request. Hence
every malformed-result, protocol, transport, or service-failure identity names
the validator capability and validator request; only the later successful
receiving projection names the producer request and conclusion.

The returned value, truth, metadata, admission, or logical conclusion is
discarded in both branches. There is no result identity for malformed carrier
bytes/logical shape, so the fixed sentinel is mandatory; a stable exact result
identity is mandatory for semantic mismatch.

Map every individual interface reason pointwise, then deduplicate by exact K1
reason equality:

```text
toEvaluationReason(role,h) = EvaluationErrorReason(
  ABI_REASON_ISSUER, ABI_INTERFACE_EVALUATION_FAILURE,
  (role,h.reason_code,h.capability_identity,h.request_identity,
   h.expected_contract_identity,h.offending_result_identity,
   h.trust_root_status_reason))

toReasoningReason(role,h) = ReasoningErrorReason(
  ABI_REASON_ISSUER, ABI_INTERFACE_REASONING_FAILURE,
  (role,h.reason_code,h.capability_identity,h.request_identity,
   h.expected_contract_identity,h.offending_result_identity,
   h.trust_root_status_reason))

evaluationReasons(role,F) = {toEvaluationReason(role,h) | h in F.reasons}
reasoningReasons(role,F)  = {toReasoningReason(role,h) | h in F.reasons}
```

Because `F.reasons` is nonempty and both constructors are total, each mapped
set is nonempty; equal mapped reasons coalesce and no unequal reason is removed.
The complete service-role projection is:

| Service role | Exact projection of any invocation-bound `InterfaceFailure F` |
|---|---|
| `VALUE_ADMISSION` | `ADMISSION_ERROR(evaluationReasons(role,F))` |
| `FUNCTION_EVALUATION` | `TERM_ERROR(evaluationReasons(role,F))`; only A2 later projects it at an atom |
| `PREDICATE_EVALUATION` | `Eval.ERROR(evaluationReasons(role,F),{},{})` |
| `PROFILE_CONCRETE` | `ProfileResult.EVALUATION_ERROR(evaluationReasons(role,F))` |
| `PROFILE_SYMBOLIC` | `ProfileResult.REASONING_ERROR(reasoningReasons(role,F))` |
| `REASONING` | `ReasoningResult.REASONING_ERROR(reasoningReasons(role,F))` |
| `PAIR_VALIDATION` | `PairValidationResult.REASONING_ERROR(reasoningReasons(role,F))` |
| `AUTHORITY_VALIDATION` | `AuthorityAdmissionResult.REASONING_ERROR(reasoningReasons(role,F))` |
| `MIGRATION_VALIDATION` | `MigrationAdmissionResult.REASONING_ERROR(reasoningReasons(role,F))` |
| `COMPATIBILITY_VALIDATION` | `CompatibilityAdmissionResult.REASONING_ERROR(reasoningReasons(role,F))` |
| `SEMANTIC_EXTENSION_VALIDATION` | `SemanticExtensionAdmissionResult.REASONING_ERROR(reasoningReasons(role,F))` |

The same reasoning set is first recorded as
`CertificateAdmission.REASONING_ERROR` when the failed invocation is a
certificate-validator step, then projected only to the request binding's
role-specific reasoning-error tag. A conformant explicit concrete validation
result may still carry its declared `EVALUATION_ERROR`; this is a semantic
result tag, not an interface-failure mapping and cannot be invented for an
interface failure.

`PROTOCOL_FAILURE` and `TRANSPORT_FAILURE` use the same role table with their
distinct codes. `MALFORMED_RESULT(MALFORMED_CARRIER)` and
`MALFORMED_RESULT(SEMANTIC_MISMATCH)` therefore deterministically become K1
evaluation errors for the four evaluation roles and K1 reasoning errors for
the seven reasoning/admission roles. A trust failure before invocation remains
the exact root/discovery lifecycle failure and produces no K1 result; root
absence/incompatibility maps to `EVALUABILITY_MISSING`, root uncertainty to
`EVALUABILITY_UNKNOWN`, and trust protocol/transport failure to
`DISCOVERY_FAILED`. A discovery failure likewise remains
`DiscoveryResult.DISCOVERY_FAILURE`, with no evaluability or K1 result. If a
trust/discovery/protocol failure occurs after an exact role is already
invocable, it is invocation-bound and the role table applies. Thus every
domain/kind and service role has exactly one projection without converting
absence, uncertainty, malformedness, or failure into logical unknown.

## 6. Capabilities, reasoning requests, and certificate admission

### 6.1 Capability classes and fragments

Every `CapabilityDescriptor` has exactly one class:

| Class | Sound/complete contract |
|---|---|
| `CONCRETE_EVALUATION_ONLY` | Sound only for declared concrete invocations; it makes no symbolic completeness claim. |
| `PARTIAL_SYMBOLIC_REASONING` | Every admitted decisive result is sound within `sound_fragment`; completion may be inconclusive. |
| `COMPLETE_FOR_DECLARED_FRAGMENT` | Every admitted result is sound within `sound_fragment`; `complete_fragment` is present and is a subset of it; every valid in-complete-fragment request must complete decisively or return `REASONING_ERROR`. |

The descriptor binds the exact ABI/plugin/service/capability versions,
supported judgments, a nonempty exact supported-target set, fragments,
complete dependency scope, required evidence, required exact trust-root keys, and failure
contract. Discovery and invocation require simultaneous exact agreement of
service role, judgment, one echoed tagged target, semantic environment and its
identity, trust environment, fragments, dependency scope, and every required
root's exact `SERVICE_USE_TRUST_TARGET`. An asserted conclusion outside the sound
fragment is non-conformant. A dependency not covered by
`dependency_scope` makes the capability incompatible with the request.
`service_role` determines whether invocation failure is an evaluation,
reasoning, or pair-admission failure; it cannot change K1 result meaning.
`complete_fragment` is absent exactly for the concrete-only and partial
classes; absence never implies completeness.
No capability is compatible for an ordinary request merely because its
descriptor lists a root key: request-time external admission, exact service-use
scope, and service-use producer independence are all mandatory. Root absence,
incompatibility, or scope mismatch gives capability incompatibility and
`EVALUABILITY_MISSING`; root uncertainty gives `EVALUABILITY_UNKNOWN`; root
validation/discovery failure stays an interface failure. None is a returned
semantic result.

### 6.2 Reasoning request taxonomy

```text
ReasoningJudgment =
    CONSISTENCY
  | FORMULA_ENTAILMENT
  | FORMULA_EQUIVALENCE
  | ACCEPTANCE_ENTAILMENT
  | ACCEPTANCE_EQUIVALENCE
  | FULL_CONTRACT_EQUIVALENCE
  | EVAL_FUNCTION_EQUALITY_DERIVATION

ReasoningRequest = (
  abi_version : AbiVersion,
  judgment : exactly one ReasoningJudgment,
  subjects : exact judgment-specific subject tuple,
  semantic_environment : SemanticEnvironment,
  trust_environment : TrustEnvironment,
  required_fragment : ContractSpec[Service],
  complete_dependencies : DependencyEnvironment,
  capability_target : ENVIRONMENT_JUDGMENT_TARGET(
    judgment, subjects, semanticIdentity(semantic_environment)),
  capability_key : CapabilityKey
)
```

The first six tags name exactly one public K1 consistency or relation taxonomy
member. `EVAL_FUNCTION_EQUALITY_DERIVATION` is the separate internal role
for `f ==Eval g`; it is not a public relation.

A Contract-level request requires every subject Contract to be `CLOSED`.
Formula and internal `==Eval` requests require
`CLOSED_FORMULA_ENV`. Subjects determine the complete mechanical
dependencies, `Delta`, `Sigma`, derived `chi_C`, and lexical scope.
The request semantic environment must equal them exactly, and its exact trust
environment must satisfy the equality and ordinary service-use trust rule in
section 5.1. An alternate or missing
`chi_C`, narrower dependency set, unbound variable, or open semantic key
makes the request non-conformant.
The tagged capability target must equal the exact tuple derived from the other
request fields and must be a member of the descriptor's nonempty supported
target set. This single equality is also the joint-scope check: a local binding
target or an environment target with fewer subjects/dependencies is
incompatible and cannot be invoked for the joint request.

Subject shape and order are exact:

| Judgment | Subjects | Closure premise |
|---|---|---|
| `CONSISTENCY` | one Contract | that Contract is `CLOSED` |
| `FORMULA_ENTAILMENT` | ordered pair `(f,g)` | `CLOSED_FORMULA_ENV({f,g})` |
| `FORMULA_EQUIVALENCE` | pair `(f,g)` | `CLOSED_FORMULA_ENV({f,g})` |
| `ACCEPTANCE_ENTAILMENT` | ordered pair `(C1,C2)` | both Contracts are `CLOSED` |
| `ACCEPTANCE_EQUIVALENCE` | pair `(C1,C2)` | both Contracts are `CLOSED` |
| `FULL_CONTRACT_EQUIVALENCE` | pair `(C1,C2)` | both Contracts are `CLOSED` |
| `EVAL_FUNCTION_EQUALITY_DERIVATION` | pair `(f,g)` | `CLOSED_FORMULA_ENV({f,g})` |

### 6.3 Reasoning results and decisiveness

```text
ReasoningResult =
    ADMITTED_JUDGMENT(judgment, CertificateKey)
  | COMPLETED_INCONCLUSIVE(nonempty finset(UnknownReason))
  | EVALUATION_ERROR(nonempty finset(EvaluationErrorReason))
  | REASONING_ERROR(nonempty finset(ReasoningErrorReason))
```

For `CONSISTENCY`, admitted judgments are `CONSISTENCY_SAT` with an
admitted satisfying witness or `CONSISTENCY_UNSAT` with a sound proof/core.
For each public relation, they are its correctly namespaced
`RELATION_PROVED` or `RELATION_DISPROVED`. For internal
`EVAL_FUNCTION_EQUALITY_DERIVATION`, the sole admitted conclusion is
`INTERNAL_EVAL_EQUAL`.

`ReasoningResult` records an invocation outcome; it is not the total public
logical-evidence coordinate. For any valid closed consistency or relation
request with no admitted decisive core/plugin evidence or counterexample, that
public coordinate is respectively `CONSISTENCY_UNKNOWN` or
`RELATION_UNKNOWN`, including when capability discovery is absent or
undecided. Evaluability is reported independently. A failed invocation is the
exception: its error yields no conclusion for that invocation.

A partial capability, or a request outside its declared complete fragment, may
return `COMPLETED_INCONCLUSIVE`; the kernel maps it only to the applicable
`CONSISTENCY_UNKNOWN` or `RELATION_UNKNOWN`. Profile checkers instead return
the exact `ProfileResult` through `ProfileRequest`.
Concrete evaluation-only capability cannot assert a universal symbolic proof
unless its declared judgment itself is a concrete witness/counterexample
validation.

A complete in-fragment request must return an admitted decisive judgment.
`COMPLETED_INCONCLUSIVE`, “no result,” an omitted certificate, or an
inadmissible certificate is a complete-fragment protocol violation that yields
the canonical `NO_RESULT_SENTINEL` §5.4 `REASONING_ERROR`, never logical/profile
unknown. Service/interface failure is pointwise mapped to canonical reasoning
reasons and yields no judgment. A concrete evaluator error encountered
while validating a concrete subject yields `EVALUATION_ERROR` and no
judgment; it is neither inconclusive reasoning nor a counterexample.

### 6.4 Certificate kinds

```text
CertificateKind =
    SATISFYING_WITNESS
  | CONTRADICTION_PROOF
  | MODEL
  | DECISIVE_LOGICAL_COUNTEREXAMPLE
  | ENTAILMENT_PROOF
  | TRUTH_BEHAVIOR_EQUIVALENCE_PROOF
  | EVAL_FUNCTION_EQUALITY_DERIVATION
  | FULL_CONTRACT_EQUIVALENCE_PROOF
  | FULL_CONTRACT_INEQUALITY_EVIDENCE
  | PROFILE_COVERAGE_EVIDENCE
  | EVENT_PAIR_COHERENCE_PROOF
  | EVENT_PAIR_INCOHERENCE_COUNTEREXAMPLE
  | AUTHORITY_FACT_ATTESTATION
  | MIGRATION_RELATION_PROOF
  | COMPATIBILITY_CLAIM_PROOF
  | SEMANTIC_EXTENSION_VALIDATION

AbstractionClass = CONCRETE | SYMBOLIC | ABSTRACT

CertificateEnvelope = (
  certificate_key : CertificateKey,
  certificate_kind : CertificateKind,
  request_binding : ReasoningRequest | ProfileRequest |
                    PairAdmissionRequest | AuthorityAdmissionRequest |
                    MigrationAdmissionRequest |
                    CompatibilityAdmissionRequest |
                    SemanticExtensionAdmissionRequest,
  subjects : exact certificate-kind-specific subject tuple,
  environment : SemanticEnvironment,
  capability_key : CapabilityKey,
  fragment : ContractSpec[Service],
  dependencies : DependencyEnvironment,
  claimed_conclusion : exact certificate-kind-specific conclusion,
  validator_key : CapabilityKey,
  trust_root_key : TrustRootKey,
  abstraction_class : AbstractionClass,
  payload : typed logical value,
  evidence_refs : finset(EvidenceRef)
)
```

`request_binding` is the exact `ReasoningRequest` for a reasoning
certificate, the exact `ProfileRequest` for profile evidence, and the exact
`PairAdmissionRequest` for pair admission, and the exact authority, migration,
compatibility, or semantic-extension admission request for those certificate
kinds. In every case its target must be an exact
member of the validator descriptor's supported-target set. `payload` is a typed logical value whose type and
equality are fixed by the validator capability's `required_evidence`
contract; it is not an untyped or byte-level escape hatch.

A satisfying witness binds a closed Contract, an admitted abstract
`Outcome`, validated evidence, and that Contract's derived `chi_C`, and
must make `AcceptEval=VALUE(TRUE,...)`. It may be abstract and is never an
execution artifact. A contradiction proof covers the full closed subject and
its nonempty premises. A model supports only the conclusion validated for it.

A decisive logical counterexample must meet the exact K1 determinate
TRUE/FALSE pattern for its named relation. `UNKNOWN` is never such a
counterexample. Entailment and truth-behavior equivalence proofs establish the
strong universal property for their exact taxonomy member. A certificate for
one kind or relation cannot be relabeled.

`EVENT_PAIR_INCOHERENCE_COUNTEREXAMPLE` is distinct from
`DECISIVE_LOGICAL_COUNTEREXAMPLE`. It binds one exact pair request and
environment, one admitted trace, the exact T3/A1 scope aggregate, and the
exact unequal occurrence `Eval`, including every truth, evidence, unknown,
and error set. Its admitted conclusion is only the typed
`PAIR_INCOHERENCE_ADMITTED` result. The same exact complete pair-equality
validator may directly return that typed negative result. A generic rejection,
logical counterexample, sample mismatch, or validator failure cannot be
relabeled as pair incoherence.

| Certificate use | Exact admissible conclusion |
|---|---|
| `SATISFYING_WITNESS` or a full accepted `MODEL` | closed-Contract `AcceptEval=VALUE(TRUE,...)` with admitted evidence gives only `CONSISTENCY_SAT` |
| `CONTRADICTION_PROOF` | sound proof/core over the complete closed Contract gives only `CONSISTENCY_UNSAT` |
| formula entailment counterexample | one admitted outcome with `f=TRUE,g=FALSE` gives only formula-entailment disproof |
| formula equivalence counterexample | one admitted outcome with opposite determinate TRUE/FALSE values gives only formula-equivalence disproof |
| acceptance entailment counterexample | one admitted outcome with `C1=TRUE,C2=FALSE` gives only acceptance-entailment disproof |
| acceptance equivalence counterexample | one admitted outcome with opposite determinate TRUE/FALSE acceptance gives only acceptance-equivalence disproof |
| `ENTAILMENT_PROOF` | strong universal definite-truth preservation for the exact formula or acceptance taxonomy gives only its named proof |
| `TRUTH_BEHAVIOR_EQUIVALENCE_PROOF` | universal equality of Truth behavior, including matching UNKNOWN branches, gives only its named formula/acceptance proof |
| full-Contract proof | equality of Hard under internal `==Eval`, authorization result functions, Choices/bindings, Origins/authority, exact Dependencies, and empty Open facets gives only full-Contract equivalence |
| `FULL_CONTRACT_INEQUALITY_EVIDENCE` | definite unequal structural facet or unequal non-error VALUE output, including unknown metadata; concrete ERROR instead gives evaluation error |
| `PROFILE_COVERAGE_EVIDENCE` | exact complete coverage or exact known omitted dimensions under the bound coverage meaning |
| event-pair coherence/incoherence certificate | only the exact typed positive or negative `PairValidationResult` for its pair/environment |
| authority, migration, compatibility, or semantic-extension certificate | only the exact admission or relation named by its kind, subject, and environment |

### 6.5 Exact admission relation

`trustTarget` is total over every certificate-producing request:

```text
PairAdmissionRequest r -> PAIR_TRUST_TARGET(r.pair_key)
AuthorityAdmissionRequest r ->
  AUTHORITY_TRUST_TARGET(r.candidate.authority_fact_key)
MigrationAdmissionRequest r ->
  MIGRATION_TRUST_TARGET(r.migration.migration_key)
CompatibilityAdmissionRequest r ->
  COMPATIBILITY_TRUST_TARGET(r.claim.claim_key)
SemanticExtensionAdmissionRequest r ->
  SEMANTIC_EXTENSION_TRUST_TARGET(r.extension.extension_key)
ReasoningRequest r -> JUDGMENT_TRUST_TARGET(r.judgment,r.subjects)
ProfileRequest r -> JUDGMENT_TRUST_TARGET(PROFILE_COVERAGE,
                                          (r.profile_key,r.coverage_subject))
CertificateValidationRequest v -> v.certificate_admission_trust_target
ValueAdmissionRequest | FunctionRequest | PredicateRequest | DiscoveryRequest
  -> INVALID_TRUST_TARGET (these request kinds cannot bind a certificate)
```

`serviceUseTrustTarget` is separately total for every invocable request by
§2.3 and is invalid for a discovery-only request. Thus all six admission
`TrustTarget` tags, `JUDGMENT_TRUST_TARGET`, and
`SERVICE_USE_TRUST_TARGET` have typed constructors and no fallback branch.

`CertificateAdmission` has five disjoint tags:

```text
ADMITTED(certificate_key, admitted_conclusion)
MALFORMED_ENVELOPE(nonempty finset(InterfaceFailureReason))
REJECTED_NONDECISIVE(certificate_key,
                     nonempty finset(CertificateRejectionReason))
EVALUATION_ERROR(certificate_key,
                 nonempty finset(EvaluationErrorReason))
REASONING_ERROR(certificate_key,
                nonempty finset(ReasoningErrorReason))
```

Admission first checks exact envelope formation. Failure yields
`MALFORMED_ENVELOPE`; the object is not a certificate and proves nothing.
A formed envelope deterministically constructs the separate typed
`CertificateValidationRequest` in §5.1. Its lifecycle is total: exact
validator discovery plus both trust checks yields `INVOCABLE_FOR(v)`;
absence, incompatibility, uncertainty, or discovery failure produces the
ordinary independent discovery coordinate and no admission; a conformant
completed invocation replaces it with exactly one `CertificateAdmission` tag;
and malformed, protocol, transport, or validator failure replaces it with
`INVOCATION_FAILED` using `v.validator_key` and `IDENTITY_OF(v)` in every
canonical reason. A formed envelope must then match closure, request identity, target,
capability, exact semantic/trust environments, fragment, complete dependencies
and supports, validator identity, and one exact `trust_root_key`. Before any
validator is invoked, ordinary discovery must establish every descriptor root
under the request's exact `serviceUseTrustTarget`; independently, the request's
`TrustEnvironment` must contain `TRUST_ROOT_ADMITTED` for the envelope key and the root
must list this validator, certificate kind, and exact
`trustTarget(request_binding)`: respectively the pair, authority, migration,
compatibility, or extension key for those admission requests, or
`JUDGMENT_TRUST_TARGET(judgment,subjects)` for a reasoning request. The descriptor
must list that key in `required_trust_roots`; if it is used for both purposes,
its permitted target set must contain both exact targets. All service-use and certificate producer-independence
inequalities in section 2.3 must hold. Missing, incompatible, wrong-scope, or
self-trusting roots yield `REJECTED_NONDECISIVE` with no invocation or
admission. A separately trusted validator whose sound fragment covers the
kind and exact environment then checks the payload. Descriptor/root equality
alone is never sufficient.

For an admission subject with mandatory validation bindings, formation also
requires exact successful lookup of every member of
`admissionBindingReferences(subjectOf(c.request_binding),U)`. The direct
certificate must be `c.certificate_key`, the direct validator must be
`c.validator_key`, and a direct root must be `c.trust_root_key`; the pair-proof
case derives the last only from this envelope. These references occur in
`requestRoots`, `certificateRoots`, and `certificateValidationRoots` for
lookup, discovery, and both trust gates, while `certificateProperReferences`
removes only the envelope's own candidate-certificate start root. A missing
certificate grants no admission, a missing validator is evaluability missing,
an undecided validator/root is evaluability unknown, a failed root lookup is
the exact request-time discovery failure, an incompatible root grants no use,
and any same-key conflict or cross-field mismatch is malformed. No case falls
back to another reference or converts a validation reference into a semantic
proper edge.
`REJECTED_NONDECISIVE` means the formed object did not establish its claim and
yields no logical conclusion, including no negation of the claim. Concrete
witness/counterexample validation that encounters a K1
`ERROR` yields `EVALUATION_ERROR`; validator/service/protocol failure is
the exact §5.4 role-projected `REASONING_ERROR` with canonical ABI reasons.
Malformed/unequal validator output is discarded before this projection. Both
families yield no conclusion. A proof-system identity or integrity signature can
identify bytes in a later representation, but never proves semantic validity
by itself.

`ADMITTED` is the only conclusion-bearing tag. Its
`admitted_conclusion` is itself exact and kind-specific: it distinguishes an
admitted proof/witness from an admitted decisive counterexample or exact
inequality. Only the latter can establish a named semantic falsity or
incompatibility under the receiving K1 rule. Malformed, rejected, stale,
incomplete, or failed validation can make the envelope or containing package
nonconformant, but cannot establish the opposite of its claimed semantics.
The receiving boundary projects an admitted certificate into exactly one of
`PairValidationResult`, `AuthorityAdmissionResult`,
`MigrationAdmissionResult`, `CompatibilityAdmissionResult`,
`SemanticExtensionAdmissionResult`, or `ReasoningResult`; cross-projection is
malformed. Only `EVENT_PAIR_INCOHERENCE_COUNTEREXAMPLE` or the same exact
complete equality validator's typed negative result can set a pair binding to
incompatible.

Evidence admission follows K1 §5.2--§5.4: evaluator error proves nothing;
reasoning error proves nothing; an abstract witness is not a constructed
outcome-producing procedure; absence of proof is not SAT, UNSAT, entailment,
equivalence, or completeness; and local certificates do not become joint
certificates.

### 6.6 Separate internal `==Eval` role

An `EVAL_FUNCTION_EQUALITY_DERIVATION` certificate must prove, for every
admitted outcome and valuation under one exact `Delta`, `Sigma`,
mechanically derived `chi_C`, and lexical scope:

1. identical complete `Eval` tag and truth;
2. identical evidence-reference set;
3. identical unknown-reason set;
4. identical evaluation-error set; and
5. identical exact free-dependency set.

Its admitted conclusion is only `INTERNAL_EVAL_EQUAL`. It may be a premise
for derived-form preservation, a stronger public formula/acceptance
equivalence proof, or one facet of a full-Contract proof. It never directly
renders `RELATION_PROVED`, and relabeling it as logical or full-Contract
equivalence without every receiving-rule premise is non-conformant. In a
concrete comparison, an encountered `ERROR` yields
`EVALUATION_ERROR`, not equality or inequality.

## 7. Events, profiles, provenance, authority, and cross-plugin composition

### 7.1 Event values and immutable classification

```text
EventValue = (event_key, payload)
TraceEvent = (event_value, actor?)
Trace = finite sequence(TraceEvent)
```

An event value is admitted only by the exact event declaration and payload
type. `actor`, when present, is an admitted `Principal`; absence is a
distinct value. The event class is read only from the immutable
`EventDeclaration`. A caller-supplied class is excluded.

K1 authorization uses only trace events whose declaration says
`CONTROLLED`. Such an event with no actor has no matching grant. An actor
different from a grant's named principal likewise has no match. Neither case
changes event admission or class; authorization evaluates according to K1
A1/T2/T3 and may be false, unknown, or error.

### 7.2 Non-circular EventScopePair admission

K2 v0 admits a pair by either of two exact paths.

First derive one complete ordinary-binding-shaped view. In the equations below,
`pd` is the exact pair declaration, `pb` the exact pair binding, `sb` the
ordinary scope `SemanticBinding`, and `od` is the unique predicate declaration
selected by `pd.occurrence_symbol`. Failure to find exactly these records, or
any key/signature mismatch, is pair-binding incompatibility.

```text
OccurrenceBindingProjection(pd,pb,sb) = (
  binding_key = od.key,
  declaration_key = od.key,
  binding_kind = PREDICATE,
  meaning_contract = occurrenceBundle(pd,pb,sb).meaning_contract,
  permitted_facet_inputs = occurrenceBundle(pd,pb,sb).permitted_facet_inputs,
  proper_semantic_dependencies =
    occurrenceBundle(pd,pb,sb).proper_semantic_dependencies,
  dependency_closure = occurrenceBundle(pd,pb,sb).dependency_closure,
  evidence_schema = occurrenceBundle(pd,pb,sb).evidence_schema,
  access_boundary = occurrenceBundle(pd,pb,sb).access_boundary,
  unknown_contract = occurrenceBundle(pd,pb,sb).unknown_contract,
  evaluation_error_contract =
    occurrenceBundle(pd,pb,sb).evaluation_error_contract,
  determinism_rule = SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT
)

occurrenceMeaningIdentity(pd,pb,sb) =
  OccurrenceBindingProjection(pd,pb,sb).meaning_contract.contract_key
occurrenceBindingIdentity(pd,pb,sb) =
  IDENTITY_OF(every displayed field of OccurrenceBindingProjection(pd,pb,sb))

occurrenceBundle(pd,pb,sb) when pb.admission=DEFINITIONAL_T3_A1 = (
  meaning_contract = T3_A1_MEANING_LIFT(pd,sb.meaning_contract),
  permitted_facet_inputs = ({trace}),
  evidence_schema = T3_A1_EVIDENCE_LIFT(pd,sb.evidence_schema),
  access_boundary = T3_A1_ACCESS_LIFT(pd,sb.access_boundary),
  unknown_contract = T3_A1_UNKNOWN_LIFT(pd,sb.unknown_contract),
  evaluation_error_contract =
    T3_A1_ERROR_LIFT(pd,sb.evaluation_error_contract),
  determinism_rule = SAME_SEMANTIC_INPUTS_SAME_COMPLETE_RESULT,
  proper_semantic_dependencies = T3_A1_DEPENDENCY_LIFT(pd,sb),
  dependency_closure = least acyclic proper closure of that exact set
)

occurrenceBundle(pd,pb,sb) when pb.admission=
  INDEPENDENT_COHERENCE_PROOF(bundle,certificate,validator) = bundle
```

Every named lift has an exact, non-configurable meaning. Its
`ContractSpecKey` is derived from `(pd.pair_key,od.key,the displayed lift tag)`
under `pd.pair_key.plugin_key`; its observation queries and support are derived
by §3.3 and cannot be supplied. `T3_A1_MEANING_LIFT` has primary domain
`Trace`, observes only the exact scope binding through one
`EVAL_RESULT_SEQUENCE` query, and maps the resulting finite sequence to
`ANY_RESULT` under frozen T3/A1. `T3_A1_EVIDENCE_LIFT` specifies exact union of
all scope evidence. `T3_A1_UNKNOWN_LIFT` specifies exact union/retention of all
scope unknown reasons and the nonempty invariant for an unknown result.
`T3_A1_ERROR_LIFT` specifies exact union and dominance of all scope evaluation
errors. `T3_A1_ACCESS_LIFT` exposes only the sole trace-derived positional
value; it permits the observation derivation to pass each event's
`event_value` to the scope meaning and exposes no actor, full `Outcome`,
Contract, authority context, or undeclared evidence. `T3_A1_DEPENDENCY_LIFT`
is exactly `{PAIR_DECLARATION(pd.pair_key),BINDING(sb.binding_key)}` plus the
roots of the five lifted `ContractSpec`s and their derived supports, with the
occurrence binding root excluded. The producer-supplied model record named by
`pb.occurrence_model_contract_key` is separately validated by the complete
field equations in §4.3; T3/A1 supplies no document namespace, locale, or
document version.
Empty trace therefore yields `VALUE(FALSE,{},{})`; multi-event equality covers
truth, evidence, unknowns, and errors.

The projection has every `SemanticBinding` field exactly once. Its declaration
must satisfy `od.symbol_key=pd.occurrence_symbol`, and its binding and
declaration keys must both equal `pb.occurrence_binding_key=od.key`; hence its
predicate kind, symbol, exact meaning-contract identity, and complete derived
binding identity are structural rather than pair-producer assertions. Two
projections are equal iff every displayed ordinary field is equal under the
exact `ContractSpec` and finite-collection equalities of §3.3.

**Definitional path.** `DEFINITIONAL_T3_A1` makes the occurrence meaning
definitionally equal to:

```text
occurrence(T) =
  ANY_RESULT({
    scope(e.event_value) | e occurs in T
  })
```

The ABI owns the displayed lift construction; the producer supplies no
occurrence field. The exact frozen T3/A1 rule gives empty trace
`VALUE(FALSE,{},{})`, unions evidence/unknown/error sets over every event,
lets any error dominate, otherwise lets TRUE decide while retaining collected
unknown metadata, and handles multi-event traces without traversal-order
effects. `scope` must return `VALUE(FALSE,{},{})` for every event key
outside `controlled_keys`.

**Independent-proof path.** `INDEPENDENT_COHERENCE_PROOF` permits distinct
scope and occurrence meanings only when its
`OccurrenceSemanticContractBundle` is complete: it must have the exact
occurrence declaration/key/kind, sole trace facet/access boundary, evidence,
unknown, error, determinism, and derived support/closure shown above. Omission or inequality of any field
leaves no projection and makes the pair binding incompatible. An admitted
`EVENT_PAIR_COHERENCE_PROOF` must establish full-`Eval` equality between this
bundle's relation and `T3_A1_MEANING_LIFT` for every admitted trace. Its
`PAIR_VALIDATION` capability must cover
every admitted trace and complete `Eval` field, bind the exact pair/members/
controlled keys/environment, and use an already admitted exact trust root and
producer-independent validator under sections 2.3 and 6.5. Neither validator
soundness nor trust may depend on the pair producer, its claim, the unadmitted
pair, or a service supplied by that producer.

The bundle's certificate and validator fields project exactly to
`{VALIDATION_CERTIFICATE(c),VALIDATION_CAPABILITY(v)}`. They are mandatory in
the pair admission request, named envelope, derived validation request, and
their operational root/lookup sets, but neither is a
`PAIR_BINDING(p)->CERTIFICATE(c)|CAPABILITY(v)` proper edge. The envelope and
validator descriptor may still point to the pair through their exact request
and target; because the pair has no proper edge back, neither mandatory
two-node cycle exists. Missing/conflicting certificate lookup, missing/
undecided validator discovery, or root status remains exact under §§3.3/6.5;
no other proof or validator is selected.

Successful admission binds the exact pair meanings. A bare claim is malformed.
For either path, `pb.occurrence_model_contract_key` must resolve to the unique
package `ModelContract` validated field-by-field in §4.3; missing, wrong, or
conflicting records receive that section's exact open/malformed/conflict
status. `recordAt(BINDING(od.key),U)`
then returns exactly `OccurrenceBindingProjection(pd,pb,sb)`, and every
occurrence `PredicateRequest`, result-equality check, dependency closure, and
model-facing lookup uses that record. An ordinary `SemanticBinding(od.key)` is
forbidden even if extensionally equal and conflicts under §8.3.
Missing binding/proof/validator leaves the coherence binding open; a missing
validator capability may additionally yield `EVALUABILITY_MISSING`, and
undecided discovery yields `EVALUABILITY_UNKNOWN`. Validator/protocol failure
is `REASONING_ERROR` with no admission, so closure remains open. A malformed,
stale, incomplete, or `REJECTED_NONDECISIVE` proof likewise establishes no
pair truth value: the pair remains unadmitted/open, while its envelope or
package may separately be nonconformant. The pair binding becomes
incompatible/malformed only after the typed negative result defined next.
A caller cannot alter controlled keys, attach unrelated members, or supply
another occurrence meaning after admission.

The negative transition is exact. A conformant `PairValidationResult` can
carry `PAIR_INCOHERENCE_ADMITTED` only from an admitted
`EVENT_PAIR_INCOHERENCE_COUNTEREXAMPLE`, or directly from the same exact
complete equality validator. It contains the exact admitted trace and the two
unequal complete `Eval` records described in section 5.2. That typed negative
sets `BINDING_INCOMPATIBLE` and makes the pair semantic binding malformed.
By contrast, an ordinary occurrence invocation whose returned carrier is
shape-valid but unequal to the already bound definitional or independent
meaning is only `MALFORMED_RESULT(SEMANTIC_MISMATCH)`/evaluation error under §5.4; its returned
truth is discarded and it is not a pair-incoherence certificate.
Every generic `REJECTED_NONDECISIVE`, unavailable validator, undecided
discovery, or validation failure instead leaves the pair open; none is a
negative pair result.

### 7.3 Profiles

A `ProfileBinding` owns one exact finite set of versioned dimensions and
one coverage meaning. Profile closure requires the binding and all its
mechanical dependencies; service discovery is separate.

For an exact closed request:

| Condition | Result |
|---|---|
| every dimension covered with admitted evidence | `PROFILE_COMPLETE` |
| known nonempty omitted dimension set | `PROFILE_INCOMPLETE` |
| compatible checker was invoked and conformantly completes without deciding coverage | `PROFILE_UNKNOWN` |
| concrete checker/invocation/protocol failure | `EVALUATION_ERROR` |
| symbolic checker/reasoning protocol failure | `REASONING_ERROR` |

The first three tags are conformant only when the complete record equals the
unique `coverage_meaning.logical_relation` result under the exact request
subject/environment. Shape alone cannot choose complete, incomplete, or
unknown; mismatch is `MALFORMED_RESULT(SEMANTIC_MISMATCH)` and no profile judgment.
An absent profile meaning is `OPEN_BINDINGS`, not unknown. An absent
compatible/root-usable checker is `EVALUABILITY_MISSING`, and undecidable checker/root
discovery is `EVALUABILITY_UNKNOWN`; neither is `PROFILE_UNKNOWN` and neither
produces any profile result. No profile
result certifies intent completeness or changes Contract acceptance,
satisfiability, or authority.

### 7.4 Provenance and authority

```text
SourceRef = (
  issuer : IssuerScope, source_kind, stable_source_identity, provenance_facts
)
AuthorityRef = (
  owner : IssuerScope, authority_namespace, stable_attestation_identity
)
AuthorityFactCandidate = (
  authority_fact_key : AuthorityFactKey,
  admission_subject_data : exact finite typed attestation subject value,
  offered_evidence_refs : finset(EvidenceRef)
)
AuthorityFactBinding = (
  authority_fact_key : AuthorityFactKey,
  admitted_attestation_refs : nonempty finset(CertificateKey)
)
```

`SourceRef` is a self-contained immutable provenance value: its exact issuer,
kind, stable identity, and provenance facts require no later lookup for
closure. If source binding cannot form one, representation is
`UNRESOLVED` before Contract formation. A `SourceRef` never grants
authority.

`AuthorityFactKey` is exactly the K1 semantic tuple
`(AuthorityRef, SourceRef, Principal, NormativeRole)`, where
`NormativeRole` is `REQUIRE`, `AUTHORIZE`, or
`BIND_CHOICE(choice_id)`. `AuthorityFactBinding` identity is exactly that key.
Certificate references are admission evidence, never a fifth fact-identity or
normative field. `AuthorityFactCandidate` is not a Sigma fact and is never
inserted merely because it is formed. Its admission subject is exactly
`AUTHORITY_ADMISSION_SUBJECT(candidate,environment_without_fact)`, with the
target-excluded environment defined by §5.1. Closure/adoption accepts a fact only after an
`AUTHORITY_FACT_ATTESTATION` certificate validates that exact tuple under an
already admitted scoped trust root. The exact validator producer is disjoint
from the validation-filtered producer set of that exact non-self-rooting
subject; the root's
derived embedding-policy producer is disjoint from that set, the validator,
and certificate producer. These sets are structural, not fact fields. A missing
certificate or validator leaves the fact open. A malformed or rejected
attestation may make its envelope/package nonconformant but proves no invalid
authority fact and produces no `AuthorityFactBinding`; it is retained only as
its separate certificate/admission result. Validator failure is reasoning
error with no fact.

The validator is discoverable only through service role
`AUTHORITY_VALIDATION`, judgment `AUTHORITY_FACT_ADMISSION`, and the exact
environment target in `AuthorityAdmissionRequest`; a successful receiving
result is only `AUTHORITY_FACT_ADMITTED`. Thus the target-excluded admission environment and
target are closed and invocable, while rejection/failure has no normative
effect.

Only after the exact receiving result
`AUTHORITY_FACT_ADMITTED(candidate.authority_fact_key,certificate_key)` may the
receiver construct
`AuthorityFactBinding(candidate.authority_fact_key,{certificate_key})` and
insert it into the authority map. `AUTHORITY_FACT_NOT_ADMITTED`, malformed or
invalid evidence, certificate rejection, and evaluation/reasoning/interface
failure insert no entry. Post-admission composition then groups by the exact
four-tuple key: equal keys union only independently admitted certificate keys;
different keys remain separate. This ordering defines duplicate handling
after admission and prevents an offered fact from supporting itself.

Composition groups admitted attestations by exact `AuthorityFactKey`. Multiple
independently admitted attestations for one key coalesce by set union of their
nonempty `admitted_attestation_refs`; unequal certificate sets neither
conflict, create distinct normative facts, nor multiply normative force.
Different fact keys remain different facts. An alleged binding with an empty
set, an unadmitted reference, or a certificate admitted for another key is
incompatible and contributes no fact. Evaluation
evidence, a plugin signature, registration, documentation, provenance, or a
model/reasoner conclusion cannot create the tuple. Trust establishes
authenticity/validity of the tuple; it cannot redefine the role.

The sole `chi_C` remains mechanically derived from Contract choice records
whose value, controller, source, and exact `BIND_CHOICE` authority validate.
No witness, request, certificate, authority service, or plugin can override it.

### 7.5 Cross-plugin composition

Composition takes order-independent set union of exact records and then
validates duplicates/conflicts under section 8. All declaration, binding,
profile, pair, authority, and dependency identities remain visible. No plugin
redefines kernel conjunction, grants, or acceptance.

A joint consistency, entailment, equivalence, or internal `==Eval` conclusion
requires one compatible capability whose exact
`ENVIRONMENT_JUDGMENT_TARGET`, sound fragment, and dependency scope cover the
complete exact joint subjects and every shared dependency. A profile conclusion
instead requires its exact `PROFILE_TARGET` and a checker dependency scope
covering the complete exact coverage subject and all of that subject's shared
dependencies. Separate local
results, models, witnesses, or certificates never compose into a joint
conclusion.

For a valid closed consistency or public-relation request, K1's logical
evidence coordinate is simultaneous with evaluability. If no admitted
decisive core derivation, plugin proof/witness, or decisive counterexample
exists, the public logical status is `CONSISTENCY_UNKNOWN` or
`RELATION_UNKNOWN`. Consequently an absent/outside-fragment compatible joint
capability yields `EVALUABILITY_MISSING` plus that logical unknown; discovery
unable to decide yields `EVALUABILITY_UNKNOWN` plus that logical unknown. A
compatible partial capability invoked and completing inconclusively yields the
same logical unknown with `EVALUABILITY_AVAILABLE` and a different lifecycle
history. No local result is promoted in any branch.

Complete in-fragment requests remain decisive or return `REASONING_ERROR`.
An invocation, validator, or protocol failure yields its error and no
conclusion for that failed invocation, rather than a fabricated unknown.
Profiles remain intentionally different: absent/outside/undecided checker
discovery produces only the evaluability coordinate and no profile result;
`PROFILE_UNKNOWN` requires a compatible invoked checker completing
inconclusively. Internal `==Eval` likewise remains an evidence object, not a
public logical status.

Trust is equally scoped: trusting each local producer for its local fragment
does not trust their combination. A joint certificate binds its validator and
already admitted exact root to the whole dependency environment and target.

## 8. Discovery, compatibility, migration, and conflict handling

### 8.1 Discovery results and transitions

`DiscoveryResult` is exactly one of:

```text
EXACT_TARGET_FOUND(target, nonempty finset(CapabilityKey))
EXACT_TARGET_ABSENT(target)
DISCOVERY_UNDECIDED(target, nonempty finset(UnknownReason))
INCOMPATIBLE_DECLARATION(target, nonempty finset(ConflictRef))
INCOMPATIBLE_BINDING(target, nonempty finset(ConflictRef))
TARGET_PRESENT_SERVICE_ABSENT(target, requested_judgment)
SERVICE_OUTSIDE_FRAGMENT(target, capability_key, requested_fragment)
SERVICE_INCOMPATIBLE(target, capability_key,
                     nonempty finset(InterfaceFailureReason))
DISCOVERY_FAILURE(target, PROTOCOL_FAILURE | TRANSPORT_FAILURE,
                  nonempty finset(InterfaceFailureReason))
```

`ConflictRef=(conflict_kind,involved_identities)`, where the second
component is a nonempty finite set of exact record identities. Its equality is
the tag plus set equality, independent of discovery/composition order.

Every result echoes exactly the request's one tagged `target`; a different or
omitted target is a malformed discovery result. `EXACT_TARGET_FOUND` carries
at least one capability whose service role, judgment, target membership,
semantic-environment identity, fragment, dependency scope, and every required
ordinary service-use root all match the request's exact semantic/trust
environments together. When the target's declaration/meaning
is present but no such service exists, discovery returns
`TARGET_PRESENT_SERVICE_ABSENT`. `EXACT_TARGET_ABSENT` leaves a binding,
profile, or pair requirement open; an absent required type declaration remains
malformed under declaration validation. `DISCOVERY_UNDECIDED` maps to
`EVALUABILITY_UNKNOWN` only when declarations/meanings needed for closure
are already known; it never guesses them. The two incompatible tags fail
loudly. Meaning-present/service-absent and outside-fragment map to
`EVALUABILITY_MISSING` for the exact request. `SERVICE_INCOMPATIBLE`, including
root absent, incompatible, wrong-scope, or non-independent, does likewise; a
root-incompatible branch carries exactly §5.4's nonempty
`rootIncompatibilityReasons`. Root uncertainty yields
`DISCOVERY_UNDECIDED(rootUndecidedReasons)`/`EVALUABILITY_UNKNOWN`; trust
protocol/transport failure uses the exact §5.4 `rootFailure` projection and
yields `DISCOVERY_FAILURE`, not a capability or
semantic result. `DISCOVERY_FAILURE` gives no
evaluability status and sets `DiscoveryState` to
`DISCOVERY_FAILED(InterfaceFailure[DISCOVERY])`; failure is not uncertainty.

For a valid closed consistency or relation subject, missing/outside discovery
and undecided discovery simultaneously retain the public logical unknown when
no decisive evidence exists. This coordinate is independent of evaluability.
Profile discovery produces no profile result until a compatible checker is
invoked.

After discovery, invocation/result transitions remain distinct:

| Observation | Exact transition/result |
|---|---|
| compatible evaluator found | `CAPABILITY_DISCOVERED` then request validation |
| installed service has absent/incompatible/out-of-scope/non-independent root | `CAPABILITY_INCOMPATIBLE`, `EVALUABILITY_MISSING`, and no invocation |
| required root is undecided or its discovery fails | `DISCOVERY_UNDECIDED`/`EVALUABILITY_UNKNOWN`, or `DISCOVERY_FAILED` with no evaluability result; no invocation |
| partial or out-of-complete-fragment reasoning completes inconclusively | `COMPLETED_INCONCLUSIVE` and applicable logical/profile unknown |
| any conformant decisive value/truth/profile/admission/reasoning result | replace `INVOCABLE_FOR` with `COMPLETED(exact result)` and project its exact family |
| complete in-fragment reasoning completes inconclusively | reasoning protocol failure and `REASONING_ERROR` |
| concrete evaluator returns conformant error | `EVALUATION_ERROR` |
| reasoner returns conformant failure | `REASONING_ERROR` |
| invocation transport/protocol failure | `InterfaceFailure`, mapped by service role as section 5.4 |
| malformed or semantically unequal result | exact malformed-carrier or semantic-mismatch result failure, invocation protocol failure, and total role mapping; returned semantics discarded |

Discovery is only a logical interface. No process manager, protocol
implementation, dynamic loader, package source, service endpoint, scheduler,
or topology is selected.

### 8.2 Compatibility and explicit migration

```text
CompatibilityClaim = (
  claim_key : CompatibilityClaimKey,
  source_abi : AbiVersion,
  target_abi : AbiVersion,
  source_keys : finset(DependencyKey),
  target_keys : finset(DependencyKey),
  compatibility_contract : ContractSpec[Service],
  certificate_key : CertificateKey,
  validator_key : CapabilityKey,
  trust_root_key : TrustRootKey
)
MigrationDeclaration = (
  migration_key : MigrationKey,
  source_environment : SemanticEnvironment,
  target_environment : SemanticEnvironment,
  semantic_relation : FULL_CONTRACT_EQUIVALENCE |
                      ACCEPTANCE_EQUIVALENCE |
                      FORMULA_EQUIVALENCE |
                      EXPLICIT_SEMANTIC_CHANGE,
  relation_contract : ContractSpec[Sigma],
  certificate_key : CertificateKey,
  validator_key : CapabilityKey,
  trust_root_key : TrustRootKey
)
SemanticExtension = (
  extension_key : SemanticExtensionKey,
  target_record_identity : RecordIdentity,
  owner_layer : Delta | Sigma | Service,
  semantic_effect : ContractSpec[owner_layer],
  payload : ContractSpec[owner_layer],
  certificate_key : CertificateKey,
  validator_key : CapabilityKey,
  trust_root_key : TrustRootKey
)
```

Each validator is discovered and invoked through its exact admission request.
Compatibility uses `COMPATIBILITY_VALIDATION`, judgment
`COMPATIBILITY_CLAIM_ADMISSION`, and `COMPATIBILITY_CLAIM_PROOF`;
migration uses `MIGRATION_VALIDATION`, `MIGRATION_RELATION_ADMISSION`, and
`MIGRATION_RELATION_PROOF`; extension uses
`SEMANTIC_EXTENSION_VALIDATION`, `SEMANTIC_EXTENSION_ADMISSION`, and
`SEMANTIC_EXTENSION_VALIDATION`. Each environment-level target carries the
full exact subject and environment. `source_keys` and `target_keys` are finite
exact sets, and both semantic environments are complete typed records from
section 2. The exact already admitted `trust_root_key` must authorize that
validator, kind, and target. For each of the migration, compatibility, and
extension Subjects, the validator producer is disjoint from its exact
`subjectProducerSet`, and the root embedding-policy producer is disjoint from
that set plus the validator/certificate producers. All are derived from typed
keys; no record owns,
redefines, or self-validates trust.

For each record `z` in these three families,
`validationReferences(z)` is exactly its named certificate, validator, and
trust-root triple. This set is mandatory in its derived dependency environment
and every admission/discovery/certificate-validation lookup path, and the
certificate envelope must bind that exact request, validator, and root. It is
not in `subjectReferences(z)` or `properDependencies(z)`. Consequently the
semantic proper edges are only compatibility-to-ABI/key/contract,
migration-to-source/target-environment/relation-contract, and
extension-to-target/effect/payload. Although the certificate and validator
capability have required reverse paths to the subject, none of the three
subjects has a mandatory proper edge back to them. Genuine cycles among the
semantic environments, targets, contracts, or other semantic dependencies
remain malformed.

For migration `m`, the admission request's
`semantic_environment` is exactly `m.target_environment`; its target embeds
`semanticIdentity(m.target_environment)`. The source remains present as the
complete `m.source_environment` field inside the migration subject. Its
dependency environment has both
`SEMANTIC_ENVIRONMENT_SUBJECT(m.source_environment)` and
`SEMANTIC_ENVIRONMENT_SUBJECT(m.target_environment)` roots, and `required`
is exactly the union of their two frozen syntax-root sets. Producer
reachability starts from that union plus the `MIGRATION(m.migration_key)` root
and traverses all associations/proper semantic references in both
environments. The named validation triple is checked separately against the
request, discovered validator, envelope, and trust map and never enlarges that
semantic reachability. A request that substitutes, merges, omits, or reverses
these environments or validation bindings is malformed.

A `CompatibilityClaim` names exact source/target ABI and key sets, the
specific protocol dimensions claimed compatible, a validator, and a trust
basis. It can allow a later representation to accept a record shape or result
algebra under those dimensions. It never equates source and target keys or
proves semantic preservation.

The claim is usable only after exact discovery, a conformant
`CompatibilityAdmissionRequest`, certificate admission, and
`COMPATIBILITY_CLAIM_ADMITTED`. Absent/undecided validator discovery gives the
ordinary evaluability coordinate and no compatibility. Malformed or
`COMPATIBILITY_CLAIM_NOT_ADMITTED` evidence grants no claim; validator failure
gives `REASONING_ERROR` and no claim.

A `MigrationDeclaration` names exact source and target semantic
environments, one semantic relation, a relation-appropriate certificate,
validator, and already admitted exact trust root. Permitted relations are:

- `FULL_CONTRACT_EQUIVALENCE`, requiring all six K1 facets;
- `ACCEPTANCE_EQUIVALENCE`, which does not preserve origins or every facet;
- `FORMULA_EQUIVALENCE`, which applies only to the named closed formula
  environment;
- `EXPLICIT_SEMANTIC_CHANGE`, which asserts no preservation and requires new
  source-to-semantics representation assessment.

Every migration produces a new explicit Contract/binding record that names the
target exact keys; the original Contract and identity remain unchanged. Even a
proved equivalent migration cannot silently rebind. A changed source-language
binding, authority, choice, profile, pair, origin, or dependency requires a new
representation judgment. A mere protocol compatibility claim, alias, version
ordering, or integrity digest is not a migration.

A malformed or `REJECTED_NONDECISIVE` migration certificate establishes no
relation and authorizes no migrated binding; it does not establish semantic
change or inequality either. Validator failure yields `REASONING_ERROR` and no
migration. Only an admitted certificate for the exact named relation permits
the new explicit target record, while the source remains untouched.

A semantic extension is admitted only after exact discovery, a conformant
`SemanticExtensionAdmissionRequest` whose environment excludes the unadmitted
extension, certificate admission, and `SEMANTIC_EXTENSION_ADMITTED`. Unknown,
unsupported, unvalidated, malformed, or
`SEMANTIC_EXTENSION_NOT_ADMITTED` extensions are incompatible and have no
effect. Validator failure gives `REASONING_ERROR` and no admission; failure is
not extension meaning or logical unknown.

### 8.3 Duplicate and conflict rules

Composition groups records by exact identity, independent of input order.

1. Byte-for-byte identity is not required because v0 has no bytes; complete
   logical equality is required.
2. Equal complete required/derived-semantic fields coalesce to one logical
   record. `Diagnostics`, including every `DiagnosticExtension`, is invisible
   to this grouping and to K1 validation; diagnostic values may be independently
   retained, unioned, or dropped and never affect the equality decision.
3. Except for the authority-attestation evidence union in rule 6, same
   identity with any unequal required/derived semantic field is a conflict.
   This includes kind, signature, facet, value-admission, event
   class, controlled-key set, meaning, evidence/access/unknown/error contract,
   profile dimension/coverage meaning, pair admission, dependency closure,
   model contract field/capability summary, capability target/fragment/trust,
   authority fact key, migration, and semantic extension
   effect.
4. Different exact identities never shadow one another. Display equality does
   not create a duplicate.
5. An occurrence binding independently duplicated beside a pair-owned
   occurrence meaning conflicts even if sampled results agree.
6. After admission, `AuthorityFactBinding` is the sole special coalescence:
   candidates and rejected/failed attestations never enter this grouping. Records with the
   same exact `AuthorityFactKey` union their nonempty sets of independently
   admitted attestation references. Unequal evidence sets are not a conflict;
   unequal fact keys remain distinct facts, and unadmitted references produce
   no binding.

A conflict returns the relevant `MALFORMED`,
`INCOMPATIBLE_DECLARATION`, or `INCOMPATIBLE_BINDING` state and no later
record wins. Registration order, discovery order, retry order, and “first
found” have no role.

### 8.4 Extensions and unknown fields

Semantic and diagnostic extensions are disjoint record variants in disjoint
locations. `PluginPackage.semantic_extensions` contains only
`SemanticExtension`. Its exact key is owned by one plugin and version; its
exact target, owner layer, semantic-effect contract, payload contract, and
certificate/validator/trust root are all `REQUIRED_SEMANTIC`. The
effect/payload supports and proper-edge closure are recomputed by section 3.3.
Only the exact request/result/admission path in section 8.2 grants effect. An
unrecognized, unsupported, or unvalidated semantic extension makes the
target/package incompatible and cannot be ignored.

`Diagnostics.extensions` contains only `DiagnosticExtension`. Its optional
grouping identity and payload are `OPTIONAL_DIAGNOSTIC`, invisible to every K1
validator and excluded from semantic duplicate/conflict equality. A consumer
may retain or drop the entire record or either diagnostic value without any
declaration, closure, evaluability, truth, profile, relation, authority,
migration, or certificate effect. A diagnostic extension cannot carry an
`SemanticExtensionKey`, owner layer, semantic effect, semantic target, or
validator.
Neither variant may occur in the other's location.

An extension cannot add a kernel connective, status, authority role, alternate
choice/dependency rule, implicit service, or hidden input. An unrecognized
ordinary field is malformed rather than an extension. Unknown semantically
relevant content is therefore never silently ignored.

## 9. K1 obligation coverage and adversarial conformance cases

### 9.1 Complete K1 §8 obligation coverage

Every row below maps one row of K1 §8. The remaining choices are
representation-only and grant no semantic work to a later stage.

| # | Frozen K1 §8 obligation | Exact ABI records | Validation/lifecycle rule | Cases | Remaining representation-only choice |
|---:|---|---|---|---|---|
| 1 | `Delta` type/value/literal/signature/facet/event/pair declarations remain distinct from meanings/services; ill-typed choices are malformed | six declaration records, `EventScopePairDeclaration`, targeted `ValueAdmissionRequest/Result` | declaration/support validation precedes independent binding/discovery coordinates | A01,A07,A12,A13 | byte representation excluded |
| 2 | model-facing and machine-facing contracts share one exact semantic key | `SemanticBinding`, producer-named complete `ModelContract`, exact `ModelCapabilitySummary`, `AliasBinding` | exactly one named record; all occurrence/ordinary fields and summaries project exactly; missing is model-open, wrong malformed, unequal duplicate conflict | A05,A13 | presentation rendering excluded |
| 3 | function/atom meanings match `Delta`, return the exact bound `TermResult/Eval`, receive only declared facets, and retain mechanically extracted dependencies | `SemanticBinding`, role-tagged stratified `ContractSpec`, total owner/role observation matrix, finite lower observations, exhaustive Subjects/roots and dependency environment | total `observationAt`/`recordAt`; any topological order confluent by pure predecessor induction; no hidden capability/authority/choice channel; exact result/access conformance | A06,A08,A09,A10,A18 | invocation transport excluded |
| 4 | every `EventScopePair` has typed members, immutable controlled keys, and exact empty/multi-event full-result coherence | pair declaration/binding, complete `OccurrenceBindingProjection`, named T3/A1 semantic lifts, producer-named occurrence model record, pair request/result, positive proof and typed incoherence certificate | ordinary occurrence semantics are derived/complete; document identity is supplied and fully checked separately; proof certificate/validator are mandatory non-proper validation references with exact lookup, eliminating their semantic back-cycles; full-Eval proof uses complete producer reachability; only typed admitted inequality is incompatible | A12,A13 | certificate byte form excluded |
| 5 | concrete evaluators preserve the exact bound `Eval`, stable evidence/reason identities, and declared dependencies | semantic/trust-environment-bound `PredicateRequest`, `Eval`, evidence/reason records | exact algebra, nonempty invariants, complete equality to the bound/derived logical relation, and malformed-result failure | A09,A10,A11,A13 | evidence storage excluded |
| 6 | capabilities bind exact targets, sound/complete fragments, dependencies, independently admitted nonempty ordinary-use trust roots, and concrete/partial/complete class | descriptor/targets, total `subjectOfCapabilityTarget`, `ServiceUseSubject`, exact environments, discovery results, complete `subjectProducerSet` | reachability starts from required plus semantic roots and traverses all associations/proper semantic edges; the same complete set gates ordinary and certificate service trust; complete in-fragment decisiveness | A02,A09,A15,A16,A19 | service location excluded |
| 7 | witnesses/proofs/models/counterexamples/relations bind exact typed closure/environment and never override `chi_C`; internal `==Eval` remains separate | `ReasoningRequest/Result`, envelope, derived `CertificateValidationRequest`, `CertificateAdmission`, typed environment and validation-reference algebra | independent exact non-proper certificate/validator/root bindings, validator target/role/fragment/dependencies/environments and two trust targets; failures bind validator request/key and closed root-local status where applicable; strong proof/decisive countermodel; no choice observation | A13,A17,A18,A20 | proof payload encoding excluded |
| 8 | evaluator failures and reasoning failures remain distinct and yield no logical/profile conclusion | canonical `InterfaceFailureReason`, exact expected/offending identities, `TermResult`, `Eval`, `ProfileResult`, `ReasoningResult` | total pointwise eleven-role mapping; carrier malformed and semantic mismatch distinct; returned semantics discarded; trust/discovery pre-invocation maps to no K1 result | A10,A15,A16,A17 | transport error representation excluded |
| 9 | exact profiles, pairs, syntax-associated semantic bindings, and recursive dependencies participate in closure/composition/full equivalence; profile unknown and errors remain distinct | profile/pair bindings and targets, expanded dependency environment, environment-bound exact profile result | recomputed syntax/association/proper closure; profile declaration is not required but binding absence is open; invoked checker alone can yield exact profile unknown | A01,A06,A13,A15 | checker transport excluded |
| 10 | joint claims need one capability covering the whole cross-plugin dependency set | joint environment/judgment target, `CapabilityDescriptor`, reasoning request/certificate | absent/undecidable target yields evaluability missing/unknown simultaneously with logical unknown absent decisive evidence; invoked/failure branches remain distinct | A19 | service orchestration excluded |
| 11 | `SourceRef` is self-contained provenance; only validated `AuthorityRef` tuples adopt or bind choice | typed-owner refs, exact `AuthorityFactCandidate`, target-excluded environment, post-admission coalesced binding | candidate fact is absent from required/closure and cannot self-root; complete structural producers remain; only `AUTHORITY_FACT_ADMITTED` inserts, then equal four-tuple keys union evidence | A14,A18 | attestation encoding excluded |

Coverage count: **11 of 11 K1 §8 rows**, with no frozen semantic obligation
left unresolved.

### 9.2 Abstract key convention

The cases use only fresh abstract identities. `Pα@1`, `Pβ@1`, and
`Pγ@2` are distinct exact `PluginKey` values; `Tα` is a type key;
`fα` and `qα` are exact function/predicate keys; `eα` is an event key;
`Rα` is a profile key; `Sα` is a capability key; and `v0`, `v1`
are abstract typed values. Greek labels are not display-name binding rules.

### 9.3 Exactly twenty adversarial conformance cases

| ID | Exact abstract inputs | Interface objects and lifecycle states | Expected validation and K0/K1 status family | Semantic information lost by conflation | Forbidden shortcut | K1 obligation exercised |
|---|---|---|---|---|---|---|
| K2-A01 | reference `qα` with no declaration; exact valid declaration `qβ` with no binding; exact `ProfileKey Rα` with no profile binding; the §3.3 empty package `P` with ABI `a`, plugin key `p`, every member set empty, and diagnostics absent | first invalid plus all later blocked; second declared+binding absent+later blocked; profile is declaration-not-required+binding absent+later blocked; package has start root `{PLUGIN(p)}` and proper references `{ABI(a)}` | first `MALFORMED`; second `WELL_FORMED+OPEN_BINDINGS`; profile `OPEN_BINDINGS` without invented Delta; package root/reference intersection is empty and package-conformant; no omitted coordinate | target-kind declaration applicability, semantic closure, and package identity versus proper references | let meaning/service create a declaration, invent profile Delta, leave later state implicit, or add the package's own plugin root as an outgoing dependency | Delta/Sigma separation, total lifecycle, and proper package edges |
| K2-A02 | one exact `qα` binding and service `Sα` under an admitted exact service-use root and one exact `TrustEnvironment` carrier root; same binding with no service or an absent/out-of-scope root | the ordinary request roots include `CARRIER(TRUST_ENVIRONMENT,trustEnvironmentIdentity(T))`; bound+discovered+invocable versus capability absent/incompatible+invocation blocked | all can be closed; available versus `EVALUABILITY_MISSING` | denotation, exact trust-environment identity/root, root-qualified availability, and invocation | omit the trust-environment carrier root, call absent/unevaluable meaning absent/false, or accept listed root without external scope admission | service/trust separation |
| K2-A03 | exact valid declaration and bound meaning `Pα@1/qα`; v1 discovery reports service absent, failure, or undecided; separate v2 exposes `Pα@2/qα/Sβ` | absent, exact `DISCOVERY_FAILED(failure)`, and undecided are distinct total states; v2 target unequal | missing, no evaluability status on failure, or evaluability unknown; no truth and no v2 substitution | exact version, absence, failure, and uncertainty | latest/range/display/v2 fallback or failure-as-unknown | exact version/discovery |
| K2-A04 | two keys share display label but differ in owner namespace, plugin, or function/predicate kind | two distinct declared identities or kind conflict if forced under one key | coexist when keys differ; `MALFORMED` on kind collision | owner and kind | display-name equality or shadowing | namespacing/kind |
| K2-A05 | exact `qα` binding and producer-named complete model key; variants have no named record, old signature/version, incomplete/wrong capability summary, or unequal duplicate | exact one record projects every signature/facet/contract/reference/summary field | missing is `OPEN_BINDINGS(model contract)`; wrong is `MALFORMED(model/machine contract mismatch)`; unequal same-key records conflict; no rebind | complete compiler-visible contract versus denotation/capability declaration | infer locale/version from T3/A1, trust prose/alias, or accept partial summary | matching identity |
| K2-A06 | frozen roots `{K1_SYMBOL(qα),K1_DECLARATION(Tα),K1_PLUGIN(Pα@1)}`; role-tagged `qα` meaning observes lower `dβ`; variants omit binding, use invalid owner/role/key/kind cell, or alter association/cycle | kernel retains frozen roots, validates exact ContractRole matrix, derives all associations/proper reachability, and constructs the same exact observation map in every topological order | missing/ambiguous declaration malformed; missing binding open; invalid/mismatched support or failed purity/determinism/confluence malformed; no association is producer-supplied | frozen syntax, role-specific observation boundary, semantic reachability and order-independent lower results | smaller support, hidden authority/choice/capability observation, unique-order dependence, or environment-consuming relation | mechanical dependencies |
| K2-A07 | admitted `v0:Tα`; non-admitted `v1` used as choice alternative, argument, payload, or result | type declaration has `BINDING_NOT_REQUIRED`; contextual admission validates first and invalidates every use of second | well typed versus `MALFORMED` or evaluation protocol error; all later coordinates explicit | typed membership versus Sigma binding | ignore unused ill-typed value, require a meaning binding, or coerce | type/value admission |
| K2-A08 | `PREDICATE_MEANING` has final/evidence values at declared positions; variants query trust, capability, authority, lexical/choice state, or full Outcome | only declared typed primary positions and allowed lower semantic observations reach the meaning; structural checks stay outside | exact expected `Eval` versus matrix-malformed binding/request or invocation error | explicit facet/value channel versus hidden state | implicit Outcome, `chi_C`, authority, discovery, or evidence side channel | facet/access boundary |
| K2-A09 | broad `qα:(Tα,State,EvidenceStore)->Bool` with exact `PREDICATE_MEANING`, finite allowed lower observations, complete semantic/trust roots; variants request oracle/capability state or return unequal `Eval` | legitimate request derives one confluent observation map solely from positional input and completes only with exact expected result; forbidden query is malformed | exact truth/error versus package/request malformed or canonical semantic-mismatch evaluation error | reusable denotation versus privileged lookup/evaluator-selected truth | expected-answer/challenge branch, capability/discovery observation, unrooted use, or shape-only acceptance | anti-oracle and exact result binding |
| K2-A10 | bound `fα` expects `TERM_ERROR({te})`; bound `qα` expects `VALUE(UNKNOWN,{}, {u})`; another expects `ERROR({ee},{},{})`; adversary returns malformed carrier or shape-valid unequal metadata | exact results complete; each failure binds ABI issuer, code, capability/request/expected contract, and sentinel or result identity before total role projection | term evaluation error (A2 at atom); factual unknown; predicate error; malformed carrier/semantic mismatch maps deterministically to evaluation error and discards returned semantics | exact denotation, term failure, truth, metadata, interface-failure kind and predicate failure | encode term error as unknown/error as false, accept carrier shape, choose prose reason, or expose unequal result | exact result/failure algebra |
| K2-A11 | `VALUE(TRUE,{e1,e2},{u1})` represented with repeated/reordered references | one logical set-valued result | exact equality after deduplication; unequal identities remain | stable support/reason identity | list order or message-text equality | A1/A2 set semantics |
| K2-A12 | exact controlled `eα` declaration and payload; traces with matching actor, absent actor, wrong actor; attempted caller flag `OBSERVATIONAL` | events admitted; actor affects matching grants; flag rejected | matching grant may authorize; absent/wrong actor has no match; flag malformed | immutable class versus actor matching | witness/caller control flag | event/authorization |
| K2-A13 | empty/multi-event pair; complete semantic lift/bundle; exact producer-named occurrence model record; exact non-proper certificate/validator validation references; derived validation request and complete producer set; missing/wrong/conflicting model/reference, failed validator, unequal invocation, or typed incoherence | occurrence projection supplies all semantic fields; separate model record is field-complete; pair semantic proper edges exclude certificate/validator while operation roots/lookups retain both; validator service/admission targets are independent; only typed incoherence sets incompatible | bound; model-open/malformed/conflict; missing/conflicting validation reference has its exact no-admission/evaluability/malformed state; pair open plus evaluability/error on validation failure; ordinary unequal result is evaluation error; typed negative is incompatible | occurrence denotation, exact documentation identity, validation binding versus semantic dependency, validator admission, result mismatch and incoherence | derive document namespace/version, partial bundle/model, turn proof bindings into proper back-edges, choose fallback proof/validator, use producer-local validator, or infer pair falsity from mismatch/rejection | EventScopePair coherence/result equality |
| K2-A14 | typed refs and `AuthorityFactCandidate a`; exact `E0` with `a.key` absent; two independently admitted attestations; variants preinsert fact or provide invalid/rejected evidence | admission subject/required/closure exclude `AUTHORITY_FACT(a.key)` but retain ref/data/environment producers; only admitted result constructs binding; later equal keys union evidence | source retained; preinsert/self-root malformed; no map entry on rejection/failure; post-admission one normative fact | origin, candidate, validation evidence and admitted Sigma fact | use candidate fact as its own root, insert before admission, fifth-field identity, or authority from source/wording | provenance/authority |
| K2-A15 | Sigma-only profile `Rα` with dimensions `{d1,d2}` and no invented Delta; exact semantic/trust environments; checker with admitted service-use root: exact full evidence, missing `d2`, unresolved coverage, concrete failure, or symbolic failure | declaration-not-required+bound; every exact result/failure replaces invocable with a completed/failure state; absent/incompatible/uncertain root is separate discovery/evaluability only | complete, incomplete, profile unknown, evaluation error, reasoning error; binding absence is open and service/root absence gives no profile result | target applicability, exact coverage status, trust, failure and availability | invent profile declaration or treat absence/root failure/result mismatch as incomplete/unknown | profile boundary/total lifecycle |
| K2-A16 | concrete-only, partial-symbolic, and complete-fragment descriptors with exact environments/nonempty service-use roots; in/out-of-fragment requests; complete in-fragment “no result” | root-qualified capability-specific invocability and every completion replaces invocable | concrete exact result only; partial/outside may be relation unknown; forbidden completion is `REASONING_ERROR`; root incompatibility is evaluability missing | trust-qualified soundness versus completeness | unknown from complete in-fragment or descriptor root list as admission | capability relativity |
| K2-A17 | exact certificate and derived `CertificateValidationRequest` naming validator key/target/judgment/role, original request/subject/conclusion, fragment, complete dependencies/environments, exact TrustEnvironment identity/root, closed root-local non-admission reasons, receiving rule and two trust targets; stale/relabel/failure variants | envelope root is `{CERTIFICATE(c)}` while its proper references exclude that identity; certificate and validation roots contain the exact deduplicated `CARRIER(TRUST_ENVIRONMENT,trustEnvironmentIdentity(T))`; root judgments cannot contain request/result/failure/environment carriers; exact discovery/lifecycle uses the complete semantic producer set for both trust checks; completion is one CertificateAdmission; request-time failure identity names root coordinate and validator key/request | empty envelope and TrustEnvironment root/reference intersections and non-recursive trust identity permit formation and exact successful validation reaches `ADMITTED`; otherwise distinct root undecided/failure/incompatibility, named SAT/UNSAT/relation/internal conclusion, or no judgment/error | envelope and TrustEnvironment identities versus proper dependencies, root-local status versus request failure, producer request versus independent validator invocation/evidence kind/trust/failure identity | add either record's own root as a proper edge, put request/result/failure/environment identity in a root reason, omit the trust-environment carrier or one target/root, validate through producer request, use producer capability in failure, or expose internal equality publicly | certificate admission |
| K2-A18 | closed Contract derives `chi_C(c)=v0` from admitted choice/authority records; request/witness supplies `v1`; variant Sigma contract queries `CHOICE_BINDING` or authority status | typed coordinates validate outside denotational ContractSpec; override/query is malformed; evaluation applies fixed `chi_C` before meaning invocation | judgments use only `v0`; evidence multiplicity does not change choice; hidden observation never runs | controller/authority choice versus denotational inputs and evidence | request-selected choice, choice/authority observation, or certificate-selected fact | mechanical `chi_C` |
| K2-A19 | closed joint subject `{qα,qβ,Tγ}` whose required roots associate to all reachable bindings/profiles/pairs/contracts; local targets, joint root undecided, rooted joint partial/complete targets, or failure | `subjectProducerSet` starts from required plus semantic roots and traverses all associations/proper references; same set gates ordinary service trust; local/undecided discovery does not invoke | missing gives evaluability missing plus logical unknown; undecided gives both unknown coordinates; admitted joint witness gives SAT; failure gives reasoning error | complete joint semantic ownership/trust/evidence versus local fragments | conjoin local results, omit association-reachable producer, or trust root against smaller set | cross-plugin scope/trust |
| K2-A20 | migration with exact source/target environments; compatibility/extension record target; exact non-proper certificate/validator/root triples; derived certificate-validation requests and complete roots; alias/latest/unvalidated/conflicting-reference variants | required is exact union of source/target frozen roots; semantic reachability traverses both environments and record target without validation back-edges; separate validation references remain mandatory in request/discovery/certificate lookup and trust roots; validator request/two trust targets exact; migration creates new binding | only admitted named relation/claim/extension; missing/conflicting validation reference retains exact no-admission/evaluability/trust/malformed status; rejected proof none; missing/unknown extension exact status; original unchanged | source versus target environment, record target, validation binding versus semantic dependency, validation request, identity and semantic relation | undefined target subject, omit one environment/producer/root/reference, turn validation into a proper back-edge, mutate original, or discovery-order substitute | migration/version/extension |

Case count: **20** (`K2-A01`--`K2-A20`).

### 9.4 Ten complete interface traces

#### Trace K2-A01 — declaration absent versus meaning absent

1. A Contract-derived dependency names exact predicate `qα`.
2. With no `PredicateDeclaration(qα)`, declaration validation stops at
   `DECLARATION_INVALID`; the remaining exact states are
   `BINDING_BLOCKED_BY_DECLARATION`,
   `DISCOVERY_BLOCKED_BY_DECLARATION`, and
   `INVOCATION_BLOCKED_BY_DECLARATION`. The final structural status is
   `MALFORMED(missing declaration)`.
3. In the controlled variant, exact `qβ` has a well-typed predicate
   declaration, so its first coordinate is `DECLARED`.
4. No `SemanticBinding(qβ)` is found, producing
   `BINDING_ABSENT`, `DISCOVERY_BLOCKED_BY_BINDING`, and
   `INVOCATION_BLOCKED_BY_BINDING`. Discovery cannot make it bound.
5. Final statuses are `WELL_FORMED` and
   `OPEN_BINDINGS(qβ semantic contract)`; no truth or consistency request is
   valid.
6. For exact `ProfileKey Rα`, declaration applicability instead yields
   `DECLARATION_NOT_REQUIRED`. With no `ProfileBinding(Rα)`, the remaining
   coordinates are the same binding-absent/discovery-blocked/invocation-blocked
   states and the final status is `OPEN_BINDINGS`; no Delta profile declaration
   is invented.
7. Independently, the §3.3 empty package `P` with ABI `a`, plugin key `p`,
   every member set empty, and diagnostics absent has
   `rootKeys={PLUGIN(p)}` and `subjectReferences={ABI(a)}`. Their intersection
   is empty, so package identity is the start root and does not make the empty
   declaration-only package malformed.

#### Trace K2-A05 — model/machine mismatch

1. Exact predicate `qα` is declared with argument sequence
   `(Tα,State)` and facets `({}, {final})`.
2. Its unique `SemanticBinding(qα)` matches and reaches
   `SEMANTICALLY_BOUND`.
3. One exact complete `ModelContractKey` targets the binding. Exactly one record
   at that key must match target, symbol, full signature/facets, evidence/unknown/error
   contracts, semantic-contract key, and the bidirectional exact summaries of
   every descriptor targeting `qα`.
4. No record leaves `OPEN_BINDINGS(model contract)`. A record stating one
   argument, an old version, or an incomplete/foreign capability summary is
   `MALFORMED(model/machine contract mismatch)`. Two unequal records at that
   key are `CONFLICT(model contract)`.
5. Validation precedes discovery; explanatory prose, inferred locale/version,
   and aliases cannot repair any branch. The valid machine meaning is never
   silently rebound and no mismatched request is issued.

#### Trace K2-A09 — broad meaning versus oracle

1. `qα` is declared with exact typed arguments
   `(Tα,State,EvidenceStore)` and only final/evidence facet positions.
2. Its binding gives an exact `PREDICATE_MEANING` role, deterministic reusable denotation, dependency closure,
   evidence schema, access list, and honest unknown/error contracts.
3. A compatible evaluator is discovered only after the request's exact
   semantic/trust environments and an externally admitted root permit the
   capability, predicate judgment, binding-use subject, and environment
   identity. A conformant request exposes to the meaning only the three
   positional values.
4. The owner/role matrix rejects service/capability/discovery/trust,
   authority, lexical, and choice queries. Allowed lower semantic queries are
   pure deterministic functions of positional input, so every topological
   order produces the same finite observation map. The returned `Eval` must
   equal the unique complete result from that map, including
   evidence/unknown/error sets. It replaces
   `INVOCABLE_FOR` with `COMPLETED(exact Eval)` and yields only the matching K1
   truth/error status.
5. In the adversarial variant, the binding or request asks for an expected
   result, hidden target, challenge identity, full Outcome, capability state,
   authority fact, or choice value. The excluded/matrix-invalid
   field/access is detected before or during invocation.
6. Final status for that variant is package/request malformed or
   `EVALUATION_ERROR(undeclared access)`, with no logical conclusion.
7. A shape-valid but unequal `Eval` instead produces
   `MALFORMED_RESULT(SEMANTIC_MISMATCH)`. The canonical ABI reason binds the
   predicate capability, request, expected meaning-contract identity, and
   offending result identity; pointwise role projection gives a nonempty
   evaluation-error set. No returned truth is observable.

#### Trace K2-A10 — term error, factual unknown, and predicate error

1. Exact declarations, associated reachable meanings, semantic/trust
   environments, and root-compatible evaluator capabilities for function `fα`
   and predicate `qα` validate.
2. The bound function's unique expected result is `TERM_ERROR({te})`; exact
   equality validates, replaces `INVOCABLE_FOR` with completed term error, and
   a containing atom projects it to evaluation error without invoking its
   predicate.
3. A separate bound predicate's unique expected result is
   `VALUE(UNKNOWN,{}, {u})`; complete equality and nonempty `{u}` validate,
   replace invocable with completed `Eval`, and render `TRUTH_UNKNOWN`.
4. A third predicate's expected `ERROR({ee},{},{})` validates by complete
   equality, replaces invocable with completed `Eval.ERROR`, and renders
   `EVALUATION_ERROR` with no truth.
5. A malformed carrier uses `MALFORMED_RESULT(MALFORMED_CARRIER)` and the fixed
   sentinel. A shape-valid unequal value, truth, evidence, unknown, or error
   set uses `MALFORMED_RESULT(SEMANTIC_MISMATCH)` and the offending-result
   identity. Both reasons bind the canonical ABI issuer, exact capability,
   request, and expected contract; pointwise deduplication stays nonempty and
   the total role table emits the exact evaluation-error carrier (a function
   error is projected only by a containing atom). Returned semantics vanish.
6. The final families remain distinct; no state stays invocable and no
   conversion, default, or connective-local plugin aggregation occurs.

#### Trace K2-A13 — event-pair coherence

1. The exact pair declaration validates distinct typed scope/occurrence
   predicates, nonempty immutable controlled keys, and derived facets.
2. In the definitional branch, the ABI constructs
   `OccurrenceBindingProjection` with exact occurrence key/declaration/kind,
   trace-only facet/access, named meaning/evidence/unknown/error/dependency and
   semantic lifts, then derives T3/A1 for every trace. The pair binding
   separately names one complete producer-supplied occurrence
   `ModelContractKey`; §4.3 validates every record and capability-summary field
   without deriving document namespace/locale/version. Empty, multi-event, truth,
   evidence, unknown, and error branches are bound exactly.
3. In the independent branch, a complete `OccurrenceSemanticContractBundle`
   supplies the same ordinary semantic fields; any omission/conflict is
   incompatible. The same separately named model-record rule applies.
   The proof fields derive exactly one `VALIDATION_CERTIFICATE` and one
   `VALIDATION_CAPABILITY`; the complete dependency environment carries both
   separately. The pair's semantic proper edges contain its declaration,
   scope/occurrence bindings, model, bundle contracts, and supports but neither
   validation reference, so the reverse certificate-request and
   capability-target paths cannot close a pair/certificate or pair/capability
   cycle.
   Discovery then forms a derived `CertificateValidationRequest` for a
   separately trusted complete pair validator at the exact `PAIR_TARGET`; an independently owned, already
   admitted root set covers both the validator's exact ordinary
   capability/judgment/pair/environment use and its producer-independent
   certificate kind/admission target. Producer reachability starts at all
   required pair/member/event roots plus semantic roots and traverses every
   association/proper reference. Structural `producerOf` makes the
   validator disjoint from that complete set and the embedding-policy
   root producer distinct from both. The certificate binds the whole pair/environment and is
   admitted before `SEMANTICALLY_BOUND`.
4. `recordAt(BINDING occurrence)` returns only the exact projection. Every
   occurrence invocation and required `ModelContract` uses it under the same
   semantic/trust environments and admitted service-use root; its relation
   consumes only the topologically confluent scope-`Eval` sequence. The admitted
   independent proof makes its complete result equal to the T3/A1 aggregate.
5. A bare claim or malformed envelope is nonconformant but proves no
   incoherence. A stale, incomplete, or `REJECTED_NONDECISIVE` proof and a
   missing proof/validator leave `OPEN_BINDINGS`, with exact no-admission or
   missing/unknown evaluability; a same-key conflict is malformed and no
   fallback proof/validator is selected. Validator failure yields `REASONING_ERROR`
   and no admission, again leaving the pair open.
6. A shape-valid occurrence `Eval` unequal to the bound meaning is only
   `MALFORMED_RESULT(SEMANTIC_MISMATCH)` with canonical predicate-role
   evaluation reasons, no returned truth, and no pair-negative
   admission. A typed `EVENT_PAIR_INCOHERENCE_COUNTEREXAMPLE`, or the same complete
   equality validator's typed negative result, binds one exact admitted trace
   plus its unequal complete scope-aggregate and occurrence `Eval` records.
   Only receiving `PAIR_INCOHERENCE_ADMITTED` makes the pair incompatible and
   `MALFORMED`; generic rejection never does.
7. Only either successful non-circular admission branch reaches pair-bound
   closure and permits a conditional-event Contract to close.

#### Trace K2-A15 — profile outcome separation

1. Target applicability gives `DECLARATION_NOT_REQUIRED` for Sigma-only `Rα`;
   `Rα` then binds exact dimensions `{d1,d2}`, coverage meaning, evidence
   schema, semantic dependencies, and failure contracts. The Contract
   explicitly requires it and is otherwise closed.
2. Binding absence would give `BINDING_ABSENT`/`OPEN_BINDINGS` without a Delta
   declaration. With the binding present, service or required-root absence/
   incompatibility gives `EVALUABILITY_MISSING`, root uncertainty gives
   `EVALUABILITY_UNKNOWN`, and neither produces a profile result.
3. With a root-compatible checker under exact semantic/trust environments,
   complete equality to coverage meaning for both dimensions yields
   `PROFILE_COMPLETE`; known omission of `d2` yields
   `PROFILE_INCOMPLETE`; undecidable coverage yields
   `PROFILE_UNKNOWN`.
4. A concrete checker failure yields `EVALUATION_ERROR`; a symbolic checker
   failure yields `REASONING_ERROR`.
5. Each returned exact tag replaces `INVOCABLE_FOR` with its completed state;
   failures replace it with their exact failure/completed-error state. A
   shape-valid unequal coverage result is the canonical semantic-mismatch
   failure and maps by checker role, not to profile truth.
6. Each is a distinct final family, and none changes acceptance,
   satisfiability, or intent completeness.

#### Trace K2-A16 — capability class and fragment

1. All exact subject declarations and associated reachable meanings validate,
   then the same closed subject, semantic/trust environments, and exact
   mechanically derived dependency environment are formed.
2. A concrete-only descriptor validates concrete invocation but supplies no
   universal proof conclusion.
3. Each descriptor's nonempty required roots must be externally admitted for
   the exact capability/judgment/subject/environment use; root incompatibility
   prevents invocation and yields `EVALUABILITY_MISSING`.
4. A partial-symbolic descriptor covers the sound fragment; an inconclusive
   completion becomes the applicable logical unknown.
5. A complete-fragment descriptor receives an in-complete-fragment request
   whose dependencies are wholly covered. A decisive admitted certificate
   yields its named judgment.
6. Every decisive or permitted nondecisive result replaces `INVOCABLE_FOR`.
   If that service instead returns “no result,” result validation converts the
   protocol violation to a canonical no-result-sentinel reasoning reason and
   `REASONING_ERROR`, never logical/profile unknown.
   An out-of-complete-fragment request may be inconclusive under the sound
   fragment.

#### Trace K2-A17 — certificate kind and exact environment

1. Exact declarations, meanings, stratified observations, closure, exhaustive
   subject/certificate/capability/service roots, and dependency environment
   validate.
2. A certificate envelope binds them, one kind, claimed conclusion,
   validator, exact semantic/trust environments, one already admitted exact
   certificate-scoped trust root, and abstraction class. Formation derives a
   separate `CertificateValidationRequest` containing the validator key,
   certificate/envelope identity, original request/subject/conclusion,
   validator target/judgment/role, fragment, complete dependencies and
   environments, the exact
   `CARRIER(TRUST_ENVIRONMENT,trustEnvironmentIdentity(T))` root, receiving
   rule, and both exact trust targets.
3. The envelope has root `{CERTIFICATE(c)}` and only its request, subject,
   capability, validator, trust-root, fragment, and dependency proper
   references, so its root/reference intersection is empty. The certificate
   root remains in the derived validation request and certificate roots. The
   nested request, envelope, and derived validation roots also contain the
   same exact TrustEnvironment carrier root; finite-set union coalesces those
   occurrences to one member. The TrustEnvironment's own proper references
   remain only its `TRUST_POLICY` and referenced `TRUST_ROOT` records, so its
   root/reference intersection is also empty. Every non-admitted map value
   carries only the closed root-local status code, policy/root keys, and
   optional capability key; no request, result, failure, or environment
   carrier can point back from the map into this request/envelope structure.
4. Ordinary validator discovery and certificate admission use the same
   complete producer reachability from required plus semantic roots, excluding
   only the named validation certificate/capability/service/root. Both exact
   independence checks pass before invocation. Kind-specific admission checks
   the strong proof or decisive counterexample rule; only its matching named
   judgment is emitted.
5. With every exact validation premise satisfied, the lifecycle completes as
   `CertificateAdmission.ADMITTED`; its receiving rule emits only the exact
   kind-specific conclusion.
6. An internal `==Eval` derivation instead emits only
   `INTERNAL_EVAL_EQUAL`.
7. A stale environment, missing root/dependency, producer assertion, `UNKNOWN` offered as a logical
   counterexample, evaluator/reasoning error, or relabeled certificate is
   rejected or errors and produces no relation/consistency conclusion. An
   undecided root uses only its exact one-way `rootUndecidedReasons` projection
   and remains evaluability unknown; an incompatible root uses only
   `rootIncompatibilityReasons` and remains evaluability missing; a failed root
   lookup projects its exact closed root-local reason into a request-time
   discovery failure. None modifies the trust map. An invocation interface
   failure maps
   pointwise to canonical reasoning reasons that name
   the validator capability and derived validator-request identity, never the
   producer capability/request.

#### Trace K2-A19 — joint dependency scope

1. Exact declarations and bindings from `Pα@1` and `Pβ@1` compose; the
   joint formula's mechanical environment includes both plus shared `Tγ`.
   Producer reachability starts from every frozen required root plus the joint
   semantic roots, traverses syntax-to-binding associations and all proper
   declaration/binding/profile/pair/semantic references, and yields the exact
   complete owner set used by service-root independence.
2. Form exactly one `ReasoningRequest` with judgment `CONSISTENCY`, the closed
   joint Contract as subject, exact semantic/trust environments, and
   `ENVIRONMENT_JUDGMENT_TARGET(CONSISTENCY,subject,semanticIdentity(semantic_environment))`.
3. Variant (a) discovers only local binding/environment targets. None equals
   or has a root scoped to the joint target/environment, so final simultaneous coordinates are
   `EVALUABILITY_MISSING` and `CONSISTENCY_UNKNOWN`; local admitted results do
   not compose. Variant (a2) cannot decide discovery and yields
   `EVALUABILITY_UNKNOWN` with that same logical unknown.
4. Variant (b) discovers an exact joint partial capability whose externally
   admitted root covers that exact capability/judgment/joint subject/environment,
   invokes it, and it
   conformantly completes inconclusively. It yields the same
   `CONSISTENCY_UNKNOWN` with `EVALUABILITY_AVAILABLE` and a different
   lifecycle history.
5. Variant (c) discovers an exact rooted joint complete in-fragment capability whose
   dependency scope covers `{qα,qβ,Tγ}`. Its admitted satisfying witness gives
   the named decisive status `CONSISTENCY_SAT`.
6. Every completion replaces `INVOCABLE_FOR`. Variant (d) invokes that exact
   joint capability but the service/protocol
   fails; the final result is `REASONING_ERROR` and no consistency conclusion.

#### Trace K2-A20 — explicit migration

1. Source and target declarations and bindings validate, and environments
   `Pα@1` and `Pα@2` remain distinct exact identities.
2. A plugin-owned migration names both, one semantic relation, its exact
   `MIGRATION`, plus an exact separately carried validation triple naming its
   `CERTIFICATE`, validator `CAPABILITY`/`SERVICE`, and trust-root roots. Its
   required set is exactly the union of the source/target
   environment frozen roots, and reachability traverses both full environments.
   The migration's semantic proper edges end at those environments and its
   relation contract; the certificate/validator/root triple is not traversed,
   so their required reverse subject paths create no back-cycle. Compatibility
   and extension use the analogous semantic/validation split.
   A derived certificate-validation request binds the exact target environment,
   original migration subject, receiving rule, and both trust targets.
   `producerOf` derives every owner and the already admitted
   embedding-policy root is producer-independent. Exact
   compatibility and semantic-extension variants form their own environment
   targets and discover their required validator roles.
3. Certificate admission establishes only that named relation. Migration
   forms a new Contract/binding that explicitly names target keys; source
   identity remains unchanged.
4. If semantic or representation facets change, the required new binding or
   representation judgment is recorded.
5. Alias, latest-version, first-found, display equality, an omitted/
   conflicting validation reference, absent/rejected certificate, or discovery
   order supplies no admission and never selects a fallback. An unknown or
   unvalidated semantic extension is incompatible rather than ignored; other
   final states remain source-bound, open/missing, or conflicting as
   applicable.

Trace count: **10**: `K2-A01`, `K2-A05`, `K2-A09`, `K2-A10`,
`K2-A13`, `K2-A15`, `K2-A16`, `K2-A17`, `K2-A19`, and
`K2-A20`.

## 10. K3 input boundary and K2 acceptance checklist

### 10.1 Compact input packet

The accepted logical protocol identity is the exact abstract value
`K2_ABI_V0 = (contract-ir.plugin.logical-abi, (0))`. The representation
decision is transport-neutral; canonical byte encoding and process
interoperability are excluded.

Plugin-owned extension points are limited to:

- exact types/value admission, literals, functions, predicates, immutable
  events, and event-scope pairs in `Delta`;
- exact literal/function/predicate meanings, evidence/access/unknown/error
  contracts, profiles, model contracts, provenance/authority facts, and pair
  coherence in `Sigma`;
- exact evaluator, checker, reasoner, and pair-validator capabilities in the
  service layer; and
- explicit aliases, compatibility contracts, migrations, required semantic
  extensions, and droppable diagnostic extensions under section 8.

The fixed obligations carried forward are the exact declaration, binding,
dependency, invocation, value/truth/evidence/failure, capability, certificate,
ordinary-service trust, internal `==Eval`, event, profile, provenance, authority, composition,
version, migration, duplicate, conflict, discovery, and extension rules in
sections 1--9, plus all twenty accepted `K2-A01`--`K2-A20` cases.

The only allowed later design task named here is to choose a minimal
coding-domain vocabulary and demonstrate it against the accepted kernel and
this ABI. This sentence is a boundary statement, not a handoff, path,
dispatch, mutation grant, execution authorization, or choice of any domain
type or symbol.

Inherited exclusions and stop conditions remain: no kernel semantic change,
task-specific branch, hidden expected mapping, undeclared access, authority
shortcut, choice/dependency override, local-to-joint promotion, error-as-truth,
implementation, planning, execution, model behavior, prompt work, benchmark,
held-out access, or unsupported completeness claim. Any need for one returns
the design conflict to main.

### 10.2 K2 acceptance checklist

- [x] The document has exactly the ten required top-level sections in order.
- [x] It makes one transport-neutral logical-ABI decision and explicitly
  disclaims byte/process interoperability.
- [x] Equality, identity, omissions, defaults, order, duplicates, unknown
  fields, extensions, and conflicts are exact.
- [x] Declaration, semantic binding, and service ownership are unique and
  projectable; total target-kind applicability includes
  `DECLARATION_NOT_REQUIRED`, and every completion/failure leaves no coordinate
  omitted or invocable.
- [x] `producerOf` and `subjectProducerSet` are total structural finite-set
  functions for every key, record, environment, request, certificate, and
  admission subject; reachability starts at frozen required plus semantic
  roots and traverses every derived association/proper semantic reference;
  explicit validator/certificate/root machinery is a separately exact typed
  producer set rather than a semantic edge (and is filtered only where an
  explicit certificate carrier is reached), the same complete semantic set
  gates ordinary and certificate trust, typed owners are never assertions,
  and conflicts fail.
- [x] The exhaustive ledger assigns every logical record/field exactly one of
  `REQUIRED_SEMANTIC`, `DERIVED`, `OPTIONAL_DIAGNOSTIC`, or
  `EXCLUDED`; its 129 rows count 96/26/2/5 respectively under the stated body-row
  convention, and diagnostics affect
  no K1 judgment or semantic duplicate equality.
- [x] Declarations cover types/value admission, literals, typed functions and
  predicates, facets, immutable events, and exact companion pairs.
- [x] Dependencies and `chi_C` are mechanical derived views and cannot be
  omitted, replaced, or overridden; frozen K1 syntax roots are retained
  separately, every semantic declaration/symbol has a total non-overridable
  association to its exact reachable binding; exhaustive record/subject roots
  include services, capabilities, certificates, migrations, compatibility,
  model contracts, aliases, complete migration source/target environments,
  package/model projections, and record targets through total `requiredKey`;
  missing bindings remain open; exact `ValidationReference` projections and
  lookup statuses remain mandatory in `DependencyEnvironment`, request,
  discovery, certificate-validation, certificate, and trust operation roots
  without entering semantic proper closure; producer proper edges stay
  separate; the constructor audit keeps package and certificate
  identities as start roots rather than mandatory proper self-references,
  gives every exact TrustEnvironment its own carrier start root with only
  `TRUST_POLICY`/`TRUST_ROOT` proper references, and preserves that root in
  every ordinary/admission/discovery/certificate request and envelope;
  finite-set union deduplicates repeated nested occurrences; the explicit edge
  audit removes mandatory pair/migration/compatibility/extension validation
  back-cycles, while genuine explicit semantic self-dependencies and every
  semantic cycle retain their exact failure.
- [x] Every `ContractSpec` is a finite exact non-recursive specification whose
  exact owner/use `ContractRole` selects a total dependency-key/observation
  matrix; Sigma denotations have no service/discovery/trust/authority/lexical/
  choice channel, runtime/facet values enter only through typed primary input,
  support is extensional, and pure deterministic predecessor-only observation
  producers give the same exact map in every topological order. Neither an
  environment nor another contract/relation enters the relation domain.
- [x] Meanings, model contracts, typed invocation, results, evidence/reasons,
  failures, capabilities, and discovery preserve all K1 boundaries; every
  invocation binds exact semantic/trust environments, every denotational result
  equals its unique complete bound logical relation through its lower-level
  observation projection, semantic mismatch is
  `MALFORMED_RESULT(SEMANTIC_MISMATCH)`, and every descriptor/query/result validates one exact
  binding/type/profile/pair/environment target with role, judgment, fragment,
  dependency and trust scope.
- [x] Complete in-fragment reasoning is decisive or a reasoning error;
  internal `==Eval` is not a public relation.
- [x] Every certificate binds exact closure, environment, capability,
  dependencies, conclusion, validator, independently admitted scoped trust
  root, producer independence, and abstraction class; a separate derived typed
  validation request fixes validator target/judgment/role, original identity,
  receiving rule, complete environments/dependencies, the exact deduplicated
  TrustEnvironment carrier root, exact admission binding references, and two
  trust targets;
  the envelope's certificate identity is not its own proper edge, its exact
  root/reference intersection is empty, successful validation can reach
  `ADMITTED`, validator failures name the validator key/request, and external
  bootstrap is non-circular and grants no K1 normative role.
- [x] Every ordinary service use requires a nonempty externally admitted root
  permitting the exact capability, judgment, service-use subject, and derived
  semantic-environment identity with producer independence; the finite
  `TrustTarget`/`CapabilityTarget` design is non-recursive; every non-admitted
  root judgment uses only an exact closed root-local status reason that cannot
  contain a request/result/failure/environment carrier; root absence,
  incompatibility, uncertainty, or failure remains distinct and produces only
  its exact evaluability/discovery state or request-time failure projection.
- [x] Event-pair admission is non-circular and covers empty/multi-event truth,
  evidence, unknown, and error behavior; `OccurrenceBindingProjection` derives
  every ordinary semantic-binding field through named lifts or a complete
  independently proved bundle; the pair names a separate complete exact
  producer-supplied occurrence model record and capability summaries, with no
  derived document namespace/locale/version; its proof certificate/validator
  remain mandatory non-proper validation references with exact no-fallback
  lookup; a second ordinary binding is forbidden,
  malformed/rejected evidence leaves it open, and only a typed admitted trace
  with two unequal complete `Eval` records establishes incompatibility.
- [x] Every interface failure has a canonical ABI-issued domain/kind reason
  binding capability, request, expected contract, and exact offender or fixed
  sentinel, with an exact closed root-local coordinate only for request-time
  root incompatibility/failure projections; pointwise deduplicated mappings are total/nonempty for all eleven
  roles, discard malformed/unequal results, and preserve evaluation versus
  reasoning versus pre-invocation trust/discovery boundaries.
- [x] Profiles preserve complete/incomplete/unknown/evaluation-error/reasoning-
  error distinctions and cannot certify intent completeness.
- [x] Provenance grants no authority; `SourceRef` and `AuthorityRef` have exact
  typed producers, `AuthorityFactCandidate` is validated against an exact
  environment without its fact and cannot include that fact as required/root,
  only admission constructs/inserts `AuthorityFactBinding`, and independently
  admitted equal four-tuple attestations then coalesce as evidence.
- [x] Joint reasoning requires one capability covering the whole exact
  cross-plugin dependency and ordinary-use trust environment; for valid closed logical judgments,
  absence/undecidable discovery yields evaluability missing/unknown together
  with logical unknown absent decisive evidence, while profile unknown remains
  invocation-only.
- [x] Version skew, migration, duplicates, disjoint semantic/diagnostic
  extensions, exact compatibility/migration/extension validation triples and
  acyclic semantic paths, discovery
  uncertainty/failure, absent services, and conflicts have no silent fallback.
- [x] All 11 K1 §8 obligations, exactly 20 adversarial cases, and exactly the
  ten required complete traces are covered.
- [x] Only the opaque receipt `K1-HO-GATE-20260828-A` was received; no
  held-out content, annotation, path, hash, history, log, indirect store, or
  other source was searched, inspected, inferred, requested, or reproduced.
- [x] No external artifact or checksum exists.
- [x] No implementation, domain symbol catalog, downstream handoff/path,
  execution behavior, benchmark claim, or downstream authority was created.
- [x] No K2 stop condition was encountered.

K2's conclusion is only that this logical interface is internally coherent
with the accepted K0/K1 boundary. It does not establish universal semantic
adequacy or any operational property.
