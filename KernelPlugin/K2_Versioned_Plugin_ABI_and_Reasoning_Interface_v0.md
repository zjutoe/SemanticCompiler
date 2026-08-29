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
| `BINDING_CONFORMANT(b,Delta)` | `b` has the unique key derived from its exact declaration, matches that declaration, has every logical contract's exact derived support and complete semantic closure, a deterministic typed meaning, explicit facet/evidence/access/unknown/error contracts, and no service field. |
| `SERVICE_CONFORMANT(s,Delta,Sigma)` | `s` names exact ABI/plugin/service/capability identities, a nonempty exact tagged target set, only conformant bindings, exact supported judgments/fragments/dependencies/required trust roots/failure behavior with derived support, and no declaration or meaning. |
| `REQUEST_CONFORMANT(r,E)` | `r` is well typed, names one exact tagged capability target and compatible capability, contains the complete derived dependency/support environment `E`, validates role, judgment, target, fragments and scopes together, supplies no forbidden context or alternate choice map, and lies in the claimed fragment when decisiveness is required. |
| `RESULT_CONFORMANT(x,r)` | `x` is a permitted result tag for `r`, satisfies all typing and nonempty-set invariants, and uses stable evidence/reason identities; a complete in-fragment request is decisive. |
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

`ContractSpec` is an exact logical contract value
`(contract_key, owner_layer, domain, codomain, logical_relation,
dependency_support)`.
`owner_layer` is exactly one of `Delta`, `Sigma`, or `Service`;
`domain`, `codomain`, and the mathematical relation are part of logical
equality. `dependency_support` is a derived part of equality under the total
support rule in section 3.3, never a producer assertion. Value-admission,
meaning, coverage, evidence, access, unknown, failure, fragment, trust-root, and
validation contracts below are typed `ContractSpec` values owned by the layer
that names them.

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
CertificateKey    = (issuer_scope, certificate_namespace, local_identity)
MigrationKey      = (owner_scope, migration_namespace, local_identity,
                     exact_migration_version)
SemanticExtensionKey = (owner_plugin, extension_namespace, local_name,
                        exact_extension_version)
ProfileDimensionKey = (profile_key, dimension_name)
ModelContractKey    = (target_semantic_identity, document_namespace,
                       locale_identity, exact_document_version)
CompatibilityClaimKey = (owner_scope, claim_namespace, local_identity,
                         exact_claim_version)
ProducerIdentity = (producer_namespace, producer_identity, exact_version)
TrustPolicyKey = (embedding_policy_namespace, local_policy_identity,
                  exact_policy_version)
TrustRootKey = (trust_policy_key, root_namespace, local_root_identity,
                exact_root_version)
AuthorityFactKey = (authority_ref : AuthorityRef, source_ref : SourceRef,
                    principal : Principal, normative_role : NormativeRole)
ContractIdentity = IDENTITY_OF(exact complete Contract logical record)
LexicalScopeIdentity = (judgment_or_binder_kind, exact subject tuple)
LexicalBindingKey = (scope_identity : LexicalScopeIdentity, variable : Variable,
                     declared_type : DeclarationKey[TYPE])
ChoiceBindingKey = (contract_identity : ContractIdentity,
                    choice_id : ChoiceId)
TrustTarget =
    PAIR_TRUST_TARGET(EventScopePairKey)
  | AUTHORITY_TRUST_TARGET(AuthorityFactKey)
  | MIGRATION_TRUST_TARGET(MigrationKey)
  | COMPATIBILITY_TRUST_TARGET(CompatibilityClaimKey)
  | SEMANTIC_EXTENSION_TRUST_TARGET(SemanticExtensionKey)
  | JUDGMENT_TRUST_TARGET(JudgmentTag, exact subject tuple)
DependencyKey =
    ABI(AbiVersion) | PLUGIN(PluginKey) | DECLARATION(DeclarationKey)
  | SYMBOL(SymbolKey) | EVENT(EventKey) | PROFILE(ProfileKey)
  | PAIR(EventScopePairKey) | BINDING(BindingKey)
  | AUTHORITY_FACT(AuthorityFactKey)
  | LEXICAL_BINDING(LexicalBindingKey)
  | CHOICE_BINDING(ChoiceBindingKey)
  | TRUST_POLICY(TrustPolicyKey)
  | TRUST_ROOT(TrustRootKey)
  | SEMANTIC_EXTENSION(SemanticExtensionKey)

CapabilityTarget =
    BINDING_TARGET(BindingKey)
  | TYPE_ADMISSION_TARGET(DeclarationKey[TYPE], SemanticEnvironment)
  | PROFILE_TARGET(ProfileKey)
  | PAIR_TARGET(EventScopePairKey)
  | ENVIRONMENT_JUDGMENT_TARGET(
      judgment : JudgmentTag,
      subjects : exact judgment-specific subject tuple,
      environment : SemanticEnvironment)
```

The five `CapabilityTarget` tags are disjoint. Their payloads compare by exact
logical equality, including exact versions, subject order where the judgment
is ordered, complete environment fields, and derived dependency/support
fields. A binding target is the sole target for literal/function/predicate
evaluation; a type-admission target is the sole target for invoked value
admission; profile and pair targets are likewise kind-specific. The
environment/judgment tag is the sole target for consistency, logical
relations, internal `==Eval`, authority, migration, compatibility, semantic
extension, and other whole-environment admission. A type-admission target
includes its complete exact environment; no binding-only or context-free type
target can stand for one of these kinds.

`BindingKey` is derived, not independently selected: the sole semantic
binding for a semantic-bearing declaration has exactly that
`DeclarationKey`. A different meaning requires a different exact plugin
version and hence a different declaration and binding key. There is never more
than one meaning for one exact declaration in a composed environment.

The logical record roles are:

| Role | Exact record |
|---|---|
| protocol/package | `AbiVersion`, `PluginPackage` |
| identities | the key records above, `EvidenceRef`, reason identities, `SourceRef`, `AuthorityRef`, `AuthorityFactKey`, `TrustRootKey`, derived `ContractIdentity`/`LexicalScopeIdentity`, `LexicalBindingKey`, `ChoiceBindingKey`, `ProfileDimensionKey` |
| declarations | `TypeDeclaration`, `LiteralDeclaration`, `FunctionDeclaration`, `PredicateDeclaration`, `EventDeclaration`, `EventScopePairDeclaration` |
| meanings | `SemanticBinding`, `EventPairBinding`, `ProfileBinding`, `ModelContract`, `AliasBinding`, `AuthorityFactBinding` |
| services | `CapabilityDescriptor` |
| environment | `SemanticEnvironment`, `DependencyEnvironment`, `TrustEnvironment`, `LexicalBinding`, `ChoiceBindingEntry` |
| requests | `ValueAdmissionRequest`, `FunctionRequest`, `PredicateRequest`, `ProfileRequest`, `PairAdmissionRequest`, `AuthorityAdmissionRequest`, `MigrationAdmissionRequest`, `CompatibilityAdmissionRequest`, `SemanticExtensionAdmissionRequest`, `DiscoveryRequest`, `ReasoningRequest` |
| results | `ValueAdmissionResult`, `TermResult`, `Eval`, derived `FormulaResult`, `ProfileResult`, `PairValidationResult`, `AuthorityAdmissionResult`, `MigrationAdmissionResult`, `CompatibilityAdmissionResult`, `SemanticExtensionAdmissionResult`, `DiscoveryResult`, `ReasoningResult`, `InterfaceFailure` |
| evidence | `CertificateEnvelope`, `CertificateAdmission`, `TrustRootRecord`, `TrustRootJudgment` |
| logical contracts | `ContractSpec` |
| events/provenance | `EventValue`, `TraceEvent`, `SourceRef`, `AuthorityRef`, `AuthorityFactBinding` |
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
  admission :
    DEFINITIONAL_T3_A1
    | INDEPENDENT_COHERENCE_PROOF(
        occurrence_meaning_contract : ContractSpec[Sigma],
        certificate_key : CertificateKey,
        validator_key : CapabilityKey),
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

ModelContract = (
  model_contract_key, target_binding_key,
  exact_symbol_key?,
  exact_signature, exact_facet_positions,
  evidence_contract : ContractSpec[Sigma],
  unknown_contract : ContractSpec[Sigma],
  error_contract : ContractSpec[Sigma],
  capability_summaries : finset(CapabilityKey),
  semantic_contract_reference :
    BindingKey|ProfileKey|EventScopePairKey,
  explanatory_text?
)
AliasBinding = (
  alias_namespace, alias_atom, exact_target_key,
  target_kind, target_exact_version
)
CapabilityDescriptor = (
  capability_key, abi_version, plugin_key,
  service_role : VALUE_ADMISSION | FUNCTION_EVALUATION |
                 PREDICATE_EVALUATION | PROFILE_CONCRETE |
                 PROFILE_SYMBOLIC | REASONING | PAIR_VALIDATION |
                 AUTHORITY_VALIDATION | MIGRATION_VALIDATION |
                 COMPATIBILITY_VALIDATION |
                 SEMANTIC_EXTENSION_VALIDATION,
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
  trust_environment : TrustEnvironment,
  lexical_bindings : finite map LexicalBindingKey -> LexicalBinding,
  choice_bindings : finite map ChoiceBindingKey -> ChoiceBindingEntry,
  mechanically_extracted_dependencies : finset(DependencyKey),
  chi_C : finite map ChoiceId -> Value
)
DependencyEnvironment = (
  root_keys : finset(DependencyKey),
  proper_dependencies : finset(DependencyKey),
  transitive_dependency_closure : finset(DependencyKey)
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
  owner : ProducerIdentity,
  trusted_validators : nonempty finset(CapabilityKey),
  permitted_certificate_kinds : nonempty finset(CertificateKind),
  permitted_targets : nonempty finset(TrustTarget),
  adoption : V0_EXTERNAL_TRUST_PREMISE
)
TrustRootJudgment =
    TRUST_ROOT_ADMITTED(TrustRootRecord)
  | TRUST_ROOT_ABSENT(TrustRootKey)
  | TRUST_ROOT_INCOMPATIBLE(
      TrustRootKey, nonempty finset(InterfaceFailureReason))
TrustEnvironment = (
  trust_policy_key : TrustPolicyKey,
  policy_owner : ProducerIdentity,
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
`authority_facts` contains only admitted, key-grouped bindings with their
nonempty unioned attestation-reference sets.
`semantic_extensions` contains only extensions with an exact admitted result;
an offered but unvalidated extension remains outside the environment and makes
its target incompatible under section 8.

Trust is an independently owned embedding-policy input. `TrustRootKey` and
`TrustPolicyKey` compare componentwise, including exact versions. For every
root referenced by a descriptor, certificate, or admission record,
`TrustEnvironment.root_judgments` contains exactly one judgment. Omission is
`TRUST_ROOT_ABSENT`; an unequal record for the same key is
`TRUST_ROOT_INCOMPATIBLE`; neither permits validation. A root is usable only
under `TRUST_ROOT_ADMITTED`, only for a listed validator, certificate kind,
and exact target. Admission additionally requires the root key's policy
component to equal `TrustEnvironment.trust_policy_key`, the record owner to
equal `policy_owner`, and `adoption=V0_EXTERNAL_TRUST_PREMISE`; mismatch is the
incompatible judgment. A listed validator is not thereby available or sound; all
ordinary descriptor, fragment, support, and invocation checks still apply.
`TrustTarget` equality is tag and payload equality. Its five auxiliary tags
use the exact subject key; `JUDGMENT_TRUST_TARGET` uses the complete exact
reasoning subject tuple but deliberately excludes `SemanticEnvironment` and
all trust fields. The admission request independently binds the complete exact
environment. This separation scopes roots to an exact semantic subject without
making a root recursively contain the trust environment that contains it.

`V0_EXTERNAL_TRUST_PREMISE` is an explicit v0 conformance premise adopted by
the embedding policy owner outside plugin packages and discovered services.
No plugin package, certificate, provenance value, K1 authority fact, or
service can produce, modify, or validate a root. In particular, the service
authorized by a root is never invoked to admit that root. A trust root has no
`NormativeRole` and cannot `REQUIRE`, `AUTHORIZE`, or `BIND_CHOICE`.
Bootstrap terminates at the adopted external input, not a plugin assertion.

For pair, authority, migration, compatibility, and semantic-extension
admission, `producerOf(validator_key)`, `producerOf(certificate_key)`, the
root `owner`, and every producer of the admission subjects are exact
`ProducerIdentity` values. Conformance requires the validator producer to be
outside the subject-producer set, and the embedding policy/root owner to
differ from every subject and validator producer. A certificate issuer may be
a subject producer, but that fact grants no trust and cannot relax the
independent validator/root checks. These
independence inequalities, plus an already admitted exact root scoped to that
validator, kind, and target, are mandatory. Equality between a
producer-supplied trust claim and a descriptor is neither trust nor admission.

For literal bindings, `meaning_contract` returns one admitted value and
`unknown_contract` is exactly `NOT_APPLICABLE`. For functions it maps
positional admitted values to `TermResult` and has
`unknown_contract=NOT_APPLICABLE`. For predicates it maps positional
admitted values to the exact K1 `Eval`. Evidence and access contracts may be
the exact empty contract, but never omitted. A pair-derived occurrence meaning
is owned only by `EventPairBinding`; a second ordinary predicate meaning for
that occurrence key conflicts.

`SemanticEnvironment.lexical_bindings` is the exact finite
variable/type/value environment admitted for the request. Its mechanical
dependencies and `chi_C` fields are recomputed from the closed subject; they
are never accepted as caller assertions. `DependencyEnvironment` is the
judgment-specific projection separating subject roots, proper outgoing edges,
and their transitive closure.

Every `CapabilityDescriptor.supported_targets` member must agree with its
`service_role`, one `supported_judgments` member, its fragments, and its exact
dependency scope. A `FUNCTION_EVALUATION` or `PREDICATE_EVALUATION` service
can name only the matching `BINDING_TARGET`; `VALUE_ADMISSION` only a
`TYPE_ADMISSION_TARGET` carrying the same environment; profile roles only
`PROFILE_TARGET`; pair validation
only `PAIR_TARGET`; and environment-level reasoning/admission only the exact
`ENVIRONMENT_JUDGMENT_TARGET`. Cross-kind targets make the descriptor
incompatible.
`AUTHORITY_VALIDATION`, `MIGRATION_VALIDATION`,
`COMPATIBILITY_VALIDATION`, and `SEMANTIC_EXTENSION_VALIDATION` require,
respectively, the matching four admission `JudgmentTag` values and the full
subject/environment shapes in section 5.1; `REASONING` cannot substitute for
one of those validation roles.

### 2.4 Independent lifecycle state

For each required key and requested judgment, the lifecycle is the product of
four total independent coordinates, not a registration sequence. Every
coordinate always has exactly one variant, including after an earlier invalid,
irrelevant, or failed coordinate:

```text
DeclarationState =
    DECLARATION_INVALID(nonempty finset(InterfaceFailureReason))
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
    EVALUATION | REASONING | REASONING_PROTOCOL | PROTOCOL | TRANSPORT
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

| Condition | Lifecycle result | K0/K1 public family |
|---|---|---|
| required declaration missing, ill-typed, kind-confused, or conflicting | `DECLARATION_INVALID+BINDING_BLOCKED_BY_DECLARATION+DISCOVERY_BLOCKED_BY_DECLARATION+INVOCATION_BLOCKED_BY_DECLARATION` | `MALFORMED`; no coordinate is omitted |
| exact declaration valid and its kind has no Sigma binding, including type admission | `DECLARED+BINDING_NOT_REQUIRED`; discovery is independently required or not required by the requested judgment | `WELL_FORMED`; `BINDING_NOT_REQUIRED` is not closure |
| exact declaration valid, required meaning absent | `DECLARED+BINDING_ABSENT+DISCOVERY_BLOCKED_BY_BINDING+INVOCATION_BLOCKED_BY_BINDING` | `WELL_FORMED+OPEN_BINDINGS` |
| binding conflicts with declaration, or typed `PAIR_INCOHERENCE_ADMITTED` is received | `DECLARED+BINDING_INCOMPATIBLE+DISCOVERY_BLOCKED_BY_BINDING+INVOCATION_BLOCKED_BY_BINDING` | `MALFORMED(incompatible semantic binding)` |
| declaration/binding valid and no service judgment was requested | `DISCOVERY_NOT_REQUIRED+INVOCATION_NOT_REQUIRED` | no evaluability or result family is fabricated |
| exact meaning valid, requested service absent | `SEMANTICALLY_BOUND+CAPABILITY_ABSENT+INVOCATION_BLOCKED_BY_DISCOVERY` | closed if nothing else is open; `EVALUABILITY_MISSING` |
| discovery cannot decide | `DISCOVERY_UNDECIDED+INVOCATION_BLOCKED_BY_DISCOVERY` | `EVALUABILITY_UNKNOWN`; no invocation |
| discovery protocol or transport fails | `DISCOVERY_FAILED(failure)+INVOCATION_BLOCKED_BY_DISCOVERY` | exact discovery failure and no evaluability status; failure is not uncertainty |
| service incompatible or outside requested fragment | corresponding discovery state plus `INVOCATION_BLOCKED_BY_DISCOVERY` | `EVALUABILITY_MISSING` for that exact request |
| compatible service found and all request premises pass | `INVOCABLE_FOR(r)` | `EVALUABILITY_AVAILABLE`; no truth/relation follows |
| compatible service found but request validation fails | `NOT_INVOCABLE(reasons)` | malformed request; no invocation result |
| concrete invocation fails | `INVOCATION_FAILED(EVALUATION,...)` | `EVALUATION_ERROR`; no truth/profile/relation |
| reasoning invocation fails | `INVOCATION_FAILED(REASONING,...)` | `REASONING_ERROR`; no consistency/profile/relation |
| compatible partial or out-of-complete-fragment service is invoked and conformantly completes inconclusively | `COMPLETED(inconclusive)` | applicable logical unknown, or `PROFILE_UNKNOWN` for a profile checker |
| complete in-fragment service completes inconclusively | `INVOCATION_FAILED(REASONING_PROTOCOL,...)` | `REASONING_ERROR`, never logical/profile unknown |

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
| `CertificateKey.{issuer_scope,certificate_namespace,local_identity}` | `REQUIRED_SEMANTIC` | Service | stable certificate identity | certificate issuer | admission validator | exact issuer-scoped equality | bound environment supplies version | malformed certificate | reasoning | A17 |
| `MigrationKey.{owner_scope,migration_namespace,local_identity,exact_migration_version}` | `REQUIRED_SEMANTIC` | Sigma | explicit evolution identity | migration author | migration validator | component equality | exact source/target remain separate | no migration | compatibility | A20 |
| `SemanticExtensionKey.{owner_plugin,extension_namespace,local_name,exact_extension_version}` | `REQUIRED_SEMANTIC` | owning layer | namespaced semantic extension identity | extension owner | package validator | component equality | exact owner/version | no extension | compatibility | A20 |
| `ProducerIdentity.{producer_namespace,producer_identity,exact_version}`; `TrustPolicyKey.{embedding_policy_namespace,local_policy_identity,exact_policy_version}`; `TrustRootKey.{trust_policy_key,root_namespace,local_root_identity,exact_root_version}` | `REQUIRED_SEMANTIC` | embedding policy | exact independent trust ownership/root identity | embedding policy | certificate/admission gates | component equality and producer independence | versions exact | root absent, no admission | trust/reasoning | A17 |
| `AuthorityFactKey.{authority_ref,source_ref,principal,normative_role}` | `REQUIRED_SEMANTIC` | Sigma | exact four-tuple fact identity | authority subject former | closure/adoption/choice | tuple equality | referenced identities exact | open/no fact | closure/reasoning | A14 |
| `ContractIdentity`; `LexicalScopeIdentity.{judgment_or_binder_kind,subjects}`; `LexicalBindingKey.{scope_identity,variable,declared_type}`; `ChoiceBindingKey.{contract_identity,choice_id}` | `DERIVED` | K1 carrier | exact observable subject/scope/choice coordinate identity | exact subject derivation | support/closure/reasoning | complete logical subject identity then component equality | subject/type exact | cannot be supplied | structure/closure | A18 |
| `ContractSpec.{contract_key,owner_layer,domain,codomain,logical_relation}`; `ModelContractKey.{target_semantic_identity,document_namespace,locale_identity,exact_document_version}`; `CompatibilityClaimKey.{owner_scope,claim_namespace,local_identity,exact_claim_version}` | `REQUIRED_SEMANTIC` | record-declared | exact logical contract and auxiliary identities | owning declarer | applicable validator | typed extensional equality | enclosing exact versions bind | malformed if required | structure | A05 |
| `ContractSpec.dependency_support` | `DERIVED` | contract owner | total exact free dependencies | section 3.3 extensional rule | every dependency consumer | recompute `freeDependencies(logical_relation)` | enclosing contract identity/version | cannot be producer-supplied | layer-specific structure/closure/evaluability | A06 |
| `DependencyKey.{tag,exact_key}` | `DERIVED` | K1 carrier | kind-separated exact dependency | mechanical extraction | closure/request/certificate | tag and key equality | key version exact | cannot be supplied | structure/closure | A06 |
| `CapabilityTarget.{tag,payload}` | `REQUIRED_SEMANTIC` | Service | exact binding/type/profile/pair/environment target | service/request former | discovery/invocation/admission | tag-specific payload equality | every payload version exact | target/service absent | evaluability/protocol | A03 |
| `TrustTarget.{tag,payload}` | `REQUIRED_SEMANTIC` | embedding policy | exact non-recursive validator subject scope | embedding policy owner | certificate admission | tag/payload equality plus full request environment check | subject versions exact | root unusable | trust/reasoning | A17 |
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
| `EventPairBinding.{pair_key,scope_binding_key,occurrence_binding_key,admission}` | `REQUIRED_SEMANTIC` | Sigma | full-result pair coherence | meaning/proof author | closure/conditional forms | section 7 admission | exact pair bindings | open | closure/reasoning | A13 |
| `EventPairBinding.{proper_semantic_dependencies,dependency_closure}` | `DERIVED` | Sigma | pair/member/event/support proper dependencies | pair validator | closure/request | root excluded then least closure | set exact; no pair self-edge | cannot be omitted | structure/closure | A13 |
| `ProfileBinding.{profile_key,dimensions,coverage_meaning,evidence_schema,unknown_contract,evaluation_error_contract,reasoning_error_contract}` | `REQUIRED_SEMANTIC` | Sigma | exact profile-relative meaning | profile author | closure/checker | profile conformance | exact ProfileKey | open | closure/profile | A15 |
| `ProfileBinding.{proper_semantic_dependencies,dependency_closure}` | `DERIVED` | Sigma | proper support and full profile dependencies | section 3.3/environment validator | closure/checker | root excluded then least closure | set exact; no profile self-edge | cannot be omitted | structure/closure | A06 |
| `ModelContract.{model_contract_key,target_binding_key,exact_symbol_key,exact_signature,exact_facet_positions,evidence_contract,unknown_contract,error_contract,capability_summaries,semantic_contract_reference}` | `REQUIRED_SEMANTIC` | Sigma | same model/machine meaning | documentation author | binding analysis | exact projection match | target exact/versioned | stale/missing document is mismatch | structure | A05 |
| `ModelContract.explanatory_text` | `OPTIONAL_DIAGNOSTIC` | Diagnostic | wording creates no denotation/authority | documentation author | human/model presentation | target noninterference | not identity | no semantic effect | none | A05 |
| `AliasBinding.{alias_namespace,alias_atom,exact_target_key,target_kind,target_exact_version}` | `REQUIRED_SEMANTIC` | Sigma | explicit target-preserving alias | alias author | discovery/binding analysis | exact target validation | alias never substitutes version | no alias | structure | A04 |
| `CapabilityDescriptor.{capability_key,abi_version,plugin_key,service_role,capability_class,supported_judgments,supported_targets,sound_fragment,complete_fragment,dependency_scope,required_evidence,required_trust_roots,failure_contract}` | `REQUIRED_SEMANTIC` | Service | capability-relative targeted admission | service declarer | discovery/request/certificate | role/judgment/target/fragment/scope/root conformance | exact service/plugin/ABI/targets/roots | evaluability missing | evaluability/reasoning/trust | A16 |
| `CapabilityDescriptor.{proper_semantic_dependencies,dependency_closure}` | `DERIVED` | Service | exact proper support of fragments/evidence/roots/failure | section 3.3 | discovery/request/certificate | roots/proper edges then least closure | target/key versions exact | cannot be supplied | capability incompatible/evaluability | A06 |
| `SemanticEnvironment.{abi_version,declarations,pair_declarations,bindings,pair_bindings,profile_bindings,authority_facts,semantic_extensions,trust_environment,lexical_bindings}` | `REQUIRED_SEMANTIC` | projected | one fully typed exact Delta/Sigma/trust/scope | kernel request former plus embedding policy | closure/request/certificate | exact typed set/map equality and closure | exact keys/versions | open/malformed/root absent | structure/closure/trust | A17 |
| `SemanticEnvironment.{choice_bindings,mechanically_extracted_dependencies,chi_C}` | `DERIVED` | K1 carrier | choice records/dependencies/map cannot be overridden | kernel derivation | requests/certificates | recomputation equality | Contract-bound | cannot be supplied | structure/closure | A06 |
| `DependencyEnvironment.{root_keys,proper_dependencies,transitive_dependency_closure}` | `DERIVED` | K1 carrier | roots separate from total proper-edge closure | kernel extraction | service/admission | exact root/proper/least-closure equality; reject self/cycle | exact sets | cannot be reduced | structure | A06 |
| `LexicalBinding.{lexical_binding_key,admitted_value}`; `ChoiceBindingEntry.{choice_binding_key,declared_type,admitted_value,controller,source_ref,authority_fact_key}` | `REQUIRED_SEMANTIC` | K1 carrier | exact typed scope and Contract choice records | subject/Contract former | environment/support/chi derivation | type, controller, source and authority checks | subject/key versions exact | malformed/open | structure/closure | A18 |
| `TrustRootRecord.{trust_root_key,owner,trusted_validators,permitted_certificate_kinds,permitted_targets,adoption}`; `TrustEnvironment.{trust_policy_key,policy_owner}` | `REQUIRED_SEMANTIC` | embedding policy | independent exact v0 trust premise and scope | embedding policy owner | certificate/admission gates | exact versions, external adoption, scope and independence | policy/root versions exact | root absent, no admission | trust/reasoning | A17 |
| `TrustRootJudgment.{TRUST_ROOT_ADMITTED.record,TRUST_ROOT_ABSENT.key,TRUST_ROOT_INCOMPATIBLE.{key,reasons}}`; `TrustEnvironment.root_judgments` | `DERIVED` | embedding policy validation | total root admission state | trust environment validator | certificate/admission gates | exact map and judgment derivation for every referenced root | exact TrustRootKey | cannot be omitted/defaulted | trust/reasoning | A17 |
| `ValueAdmissionRequest.{abi_version,type_key,value,environment,dependency_environment,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | projected Delta/Service | typed contextual targeted value admission | request former | admission service | type, environment, support, target, role, fragment and scope together | exact type/environment/capability | malformed or evaluability missing | protocol/evaluation/evaluability | A07 |
| `FunctionRequest.{abi_version,symbol_key,arguments}`; `PredicateRequest.{abi_version,symbol_key,arguments}` | `REQUIRED_SEMANTIC` | Delta | exact positional typed invocation | kernel request former | evaluator | signature/admission | exact symbol/version | malformed request | protocol | A07 |
| `FunctionRequest.{binding_key,dependency_environment}`; `PredicateRequest.{binding_key,dependency_environment}` | `REQUIRED_SEMANTIC` | Sigma | exact meaning/dependencies | kernel request former | evaluator | binding/environment match | binding exact | not invocable | closure | A06 |
| `FunctionRequest.{capability_target,capability_key}`; `PredicateRequest.{capability_target,capability_key}` | `REQUIRED_SEMANTIC` | Service | requested exact binding-target evaluator | kernel request former | evaluator/discovery | role/judgment/target/fragment/scope match | exact capability/target | evaluability missing | evaluability | A02 |
| `ProfileRequest.{abi_version,profile_key,environment,coverage_subject}` | `REQUIRED_SEMANTIC` | Sigma | exact profile/check subject | kernel request former | checker | closure/profile match | exact profile | open/not invocable | closure/profile | A15 |
| `ProfileRequest.{capability_target,capability_key}` | `REQUIRED_SEMANTIC` | Service | exact profile-target checker class | kernel request former | checker | role/judgment/target/fragment/scope match | exact capability/profile target | evaluability missing | evaluability | A15 |
| `PairAdmissionRequest.{abi_version,pair_key,environment,complete_dependencies,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | projected Sigma/Service | exact pair-target admission | kernel request former | pair validator | pair closure plus role/judgment/target/fragment/scope | exact pair/environment/capability | open/evaluability missing | closure/reasoning | A13 |
| `AuthorityAdmissionRequest.{abi_version,authority_fact_key,environment,complete_dependencies,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | projected Sigma/Service | exact authority-fact admission subject | request former | authority validator | closed env, exact target/scope/root/independence | exact fact/environment/capability | open/no fact | closure/reasoning/trust | A14 |
| `MigrationAdmissionRequest.{abi_version,migration,environment,complete_dependencies,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | projected Sigma/Service | exact migration relation admission | request former | migration validator | exact subject/env/target/scope/root/independence | exact migration/environment/capability | no migration | compatibility/reasoning | A20 |
| `CompatibilityAdmissionRequest.{abi_version,claim,environment,complete_dependencies,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | Service | exact compatibility-claim admission | request former | compatibility validator | exact subject/env/target/scope/root/independence | exact claim/environment/capability | no compatibility | compatibility/reasoning | A20 |
| `SemanticExtensionAdmissionRequest.{abi_version,extension,environment_without_extension,complete_dependencies,capability_target,capability_key}` | `REQUIRED_SEMANTIC` | projected owner/Service | exact non-self-supporting extension admission | request former | extension validator | subject excluded from env; exact target/scope/root/independence | exact extension/environment/capability | incompatible/no effect | compatibility/reasoning | A20 |
| `DiscoveryRequest.{abi_version,target,judgment,required_fragment,complete_dependency_scope}` | `REQUIRED_SEMANTIC` | Service | one exact tagged capability query | kernel request former | discovery interface | role/judgment/target/fragment/scope together | exact target/versions | malformed request | discovery | A03 |
| `ReasoningRequest.{abi_version,judgment,subjects,environment,required_fragment,complete_dependencies}` | `REQUIRED_SEMANTIC` | Sigma | one K1 judgment/exact environment | kernel request former | reasoner | closure/taxonomy/dependency check | exact subjects/env | malformed/open | structure/reasoning | A18 |
| `ReasoningRequest.{capability_target,capability_key}` | `REQUIRED_SEMANTIC` | Service | exact environment/judgment-target request | kernel request former | reasoner | role/judgment/target/fragment/scope match | exact capability/target | evaluability missing | evaluability | A16 |
| `LifecycleState.{declaration_state,binding_state,discovery_state,invocation_state}` | `DERIVED` | K1 carrier | independent lifecycle product | validation relation | status mapper | recompute all four coordinates | exact required key/request | cannot be supplied | coordinate-specific | A01 |
| `DeclarationState.DECLARATION_INVALID.reasons`; `DeclarationState.DECLARED` | `DERIVED` | Delta validation | structural coordinate and exact reason set | declaration validator | lifecycle | total declaration rules/set equality | exact declaration versions | cannot be supplied | structure | A01 |
| `BindingState.BINDING_BLOCKED_BY_DECLARATION`; `BindingState.BINDING_NOT_REQUIRED`; `BindingState.BINDING_ABSENT`; `BindingState.BINDING_INCOMPATIBLE.reasons`; `BindingState.SEMANTICALLY_BOUND` | `DERIVED` | Sigma validation | total closure coordinate and exact reason set | binding validator | lifecycle | exact declaration/binding/support/coherence precedence | exact binding versions | cannot be supplied/omitted | closure/structure | A01 |
| `DiscoveryState.DISCOVERY_BLOCKED_BY_DECLARATION`; `DiscoveryState.DISCOVERY_BLOCKED_BY_BINDING`; `DiscoveryState.DISCOVERY_NOT_REQUIRED`; `DiscoveryState.DISCOVERY_FAILED.failure`; `DiscoveryState.DISCOVERY_UNDECIDED.reasons`; `DiscoveryState.CAPABILITY_ABSENT`; `DiscoveryState.CAPABILITY_INCOMPATIBLE.reasons`; `DiscoveryState.CAPABILITY_OUTSIDE_FRAGMENT`; `DiscoveryState.CAPABILITY_DISCOVERED` | `DERIVED` | Service validation | total discovery coordinate, exact failure/uncertainty separation | discovery result validation | lifecycle | exact earlier states plus target/role/judgment/fragment/scope | exact target/capability versions | cannot be supplied/omitted | evaluability/discovery/protocol | A02 |
| `InvocationState.INVOCATION_BLOCKED_BY_DECLARATION`; `InvocationState.INVOCATION_BLOCKED_BY_BINDING`; `InvocationState.INVOCATION_BLOCKED_BY_DISCOVERY`; `InvocationState.INVOCATION_NOT_REQUIRED`; `InvocationState.NOT_INVOCABLE.reasons`; `InvocationState.INVOCABLE_FOR.exact_request`; `InvocationState.COMPLETED.conformant_result`; `InvocationState.INVOCATION_FAILED.{failure_family,reasons}` | `DERIVED` | request/result validation | total invocation coordinate with exact request/result/failure payload | request/result validators | lifecycle/status mapper | exact earlier states/request/result equality and nonempty reasons | request-bound | cannot be supplied/omitted | evaluation/reasoning/protocol | A16 |
| `ValueAdmissionResult.VALUE_ADMITTED.{type_key,value}` | `REQUIRED_SEMANTIC` | Delta | admitted typed value | admission service | request validator | exact request type and membership | request-bound | malformed result | protocol | A07 |
| `ValueAdmissionResult.VALUE_NOT_ADMITTED.{type_key,value}` | `REQUIRED_SEMANTIC` | Delta | rejected typed-domain membership | admission service | request validator | exact request type and nonmembership | request-bound | malformed result | protocol | A07 |
| `ValueAdmissionResult.ADMISSION_ERROR.evaluation_errors` | `REQUIRED_SEMANTIC` | Delta | admission failure, not nonmembership | admission service | request validator | nonempty stable error set | request-bound | malformed result | evaluation/protocol | A07 |
| `TermResult.TERM_VALUE.value` | `REQUIRED_SEMANTIC` | K1 carrier | admitted term value | function meaning/service | term evaluator | declared result-type admission | request-bound | malformed result | protocol | A10 |
| `TermResult.TERM_ERROR.evaluation_errors` | `REQUIRED_SEMANTIC` | K1 carrier | term error with no value | function meaning/service | term evaluator | nonempty stable error set | request-bound | malformed result | evaluation/protocol | A10 |
| `Eval.VALUE.{truth,evidence_refs,unknown_reasons}` | `REQUIRED_SEMANTIC` | K1 carrier | exact truth plus complete metadata | predicate service | kernel connective evaluator | truth/tag and UNKNOWN-nonempty invariants | request-bound | malformed result | evaluation/protocol | A10 |
| `Eval.ERROR.{evaluation_errors,evidence_refs,unknown_reasons}` | `REQUIRED_SEMANTIC` | K1 carrier | evaluation failure and complete metadata | predicate service | kernel connective evaluator | nonempty error/set invariants | request-bound | malformed result | evaluation/protocol | A10 |
| `FormulaResult` | `DERIVED` | K1 carrier | kernel formula result is exact Eval | kernel T1--T4/A1--A2 | truth/acceptance boundary | definitional equality to Eval | environment-bound | cannot be independently supplied | evaluation | A10 |
| `ProfileResult.PROFILE_COMPLETE.{profile_key,evidence_refs}` | `REQUIRED_SEMANTIC` | K1 carrier | exact full coverage | checker | profile boundary | exact profile/all dimensions/evidence | request-bound | malformed result | profile | A15 |
| `ProfileResult.PROFILE_INCOMPLETE.{profile_key,missing_dimensions}` | `REQUIRED_SEMANTIC` | K1 carrier | known omission | checker | profile boundary | exact profile/nonempty known dimensions | request-bound | malformed result | profile | A15 |
| `ProfileResult.PROFILE_UNKNOWN.{profile_key,unknown_reasons}` | `REQUIRED_SEMANTIC` | K1 carrier | invoked conformant inconclusiveness | checker | profile boundary | exact profile/nonempty stable reasons | request-bound | malformed result | profile | A15 |
| `ProfileResult.EVALUATION_ERROR.evaluation_errors` | `REQUIRED_SEMANTIC` | K1 carrier | concrete profile failure | checker | profile boundary | nonempty stable error set | request-bound | malformed result | evaluation | A15 |
| `ProfileResult.REASONING_ERROR.reasoning_errors` | `REQUIRED_SEMANTIC` | K1 carrier | symbolic profile failure | checker | profile boundary | nonempty stable error set | request-bound | malformed result | reasoning | A15 |
| `PairValidationResult.PAIR_COHERENCE_ADMITTED.{pair_key,certificate_key}` | `REQUIRED_SEMANTIC` | Sigma admission | exact positive pair binding | pair validator | pair binding/lifecycle | exact request and admitted coherence kind | pair/request-bound | no admission | reasoning | A13 |
| `PairValidationResult.PAIR_INCOHERENCE_ADMITTED.{pair_key,certificate_key,admitted_trace,scope_aggregate_eval,occurrence_eval}` | `REQUIRED_SEMANTIC` | Sigma admission | typed exact pair-negative result | pair validator | binding lifecycle | admitted trace, exact T3/A1 aggregate, unequal complete Eval records | pair/request-bound | no incompatibility | evaluation/reasoning | A13 |
| `PairValidationResult.PAIR_VALIDATION_REJECTED.{pair_key,rejection_reasons}`; `PairValidationResult.EVALUATION_ERROR.evaluation_errors`; `PairValidationResult.REASONING_ERROR.reasoning_errors` | `REQUIRED_SEMANTIC` | K1 carrier | generic rejection/failure proves no pair result | pair validator | pair lifecycle | echoed pair and nonempty exact reason/error sets | pair/request-bound | pair remains open | evaluation/reasoning | A13 |
| `AuthorityAdmissionResult.{AUTHORITY_FACT_ADMITTED.{authority_fact_key,certificate_key},AUTHORITY_FACT_NOT_ADMITTED.{authority_fact_key,rejection_reasons},REASONING_ERROR.reasoning_errors}` | `REQUIRED_SEMANTIC` | Sigma admission | exact fact admission or no fact | authority validator | authority map/closure | exact request/certificate and nonempty rejection/error sets | fact/request-bound | no fact | closure/reasoning | A14 |
| `MigrationAdmissionResult.{MIGRATION_RELATION_ADMITTED.{migration_key,certificate_key},MIGRATION_RELATION_NOT_ADMITTED.{migration_key,rejection_reasons},EVALUATION_ERROR.evaluation_errors,REASONING_ERROR.reasoning_errors}` | `REQUIRED_SEMANTIC` | Sigma admission | exact migration relation result | migration validator | migration boundary | exact request/certificate and nonempty sets | migration-bound | no migration | compatibility/evaluation/reasoning | A20 |
| `CompatibilityAdmissionResult.{COMPATIBILITY_CLAIM_ADMITTED.{claim_key,certificate_key},COMPATIBILITY_CLAIM_NOT_ADMITTED.{claim_key,rejection_reasons},REASONING_ERROR.reasoning_errors}` | `REQUIRED_SEMANTIC` | Service admission | exact compatibility result | compatibility validator | compatibility boundary | exact request/certificate and nonempty sets | claim-bound | no compatibility | compatibility/reasoning | A20 |
| `SemanticExtensionAdmissionResult.{SEMANTIC_EXTENSION_ADMITTED.{extension_key,certificate_key},SEMANTIC_EXTENSION_NOT_ADMITTED.{extension_key,rejection_reasons},REASONING_ERROR.reasoning_errors}` | `REQUIRED_SEMANTIC` | owning layer admission | exact extension effect admission | extension validator | package/target | exact request/certificate and nonempty sets | extension-bound | incompatible/no effect | compatibility/reasoning | A20 |
| `DiscoveryResult.EXACT_TARGET_FOUND.{target,matching_capabilities}` | `REQUIRED_SEMANTIC` | Service | exact compatible capability found | discovery interface | lifecycle | echoed target plus nonempty jointly matching set | request-bound exact target | malformed result | discovery/protocol | A02 |
| `DiscoveryResult.EXACT_TARGET_ABSENT.target` | `REQUIRED_SEMANTIC` | Service | exact target absent | discovery interface | lifecycle | echoed target and target-kind absence | request-bound exact target | malformed result | discovery | A01 |
| `DiscoveryResult.DISCOVERY_UNDECIDED.{target,reasons}` | `REQUIRED_SEMANTIC` | Service | exact discovery uncertainty | discovery interface | lifecycle | echoed target/nonempty stable reasons | request-bound exact target | malformed result | discovery | A03 |
| `DiscoveryResult.INCOMPATIBLE_DECLARATION.{target,conflicts}`; `DiscoveryResult.INCOMPATIBLE_BINDING.{target,conflicts}` | `REQUIRED_SEMANTIC` | Service | exact incompatibility family | discovery interface | lifecycle | echoed target/nonempty exact conflicts | request-bound exact target | malformed result | structure/compatibility | A04 |
| `DiscoveryResult.TARGET_PRESENT_SERVICE_ABSENT.{target,requested_judgment}` | `REQUIRED_SEMANTIC` | Service | meaning/target present but service absent | discovery interface | lifecycle | echoed target/exact judgment/no compatible service | request-bound exact target | malformed result | evaluability | A03 |
| `DiscoveryResult.SERVICE_OUTSIDE_FRAGMENT.{target,capability_key,requested_fragment}` | `REQUIRED_SEMANTIC` | Service | exact service fragment mismatch | discovery interface | lifecycle | echoed target/exact capability/fragment | request-bound exact target | malformed result | evaluability | A16 |
| `DiscoveryResult.DISCOVERY_FAILURE.{target,failure_kind,reasons}` | `REQUIRED_SEMANTIC` | Service | discovery protocol/transport failure | discovery interface | lifecycle | echoed target/exact failure tag/nonempty reasons | request-bound exact target | malformed result | discovery/protocol/transport | A03 |
| `ReasoningResult.ADMITTED_JUDGMENT.{judgment,certificate_key}` | `REQUIRED_SEMANTIC` | K1 carrier | exact admitted decisive judgment | reasoner/admission | kernel reasoning boundary | request taxonomy and admitted certificate | request-bound | malformed result | reasoning/protocol | A16 |
| `ReasoningResult.COMPLETED_INCONCLUSIVE.unknown_reasons` | `REQUIRED_SEMANTIC` | K1 carrier | invoked partial/outside-complete inconclusiveness | reasoner | kernel reasoning boundary | nonempty reasons plus compatible invoked capability | request-bound | malformed result | reasoning/protocol | A19 |
| `ReasoningResult.EVALUATION_ERROR.evaluation_errors` | `REQUIRED_SEMANTIC` | K1 carrier | concrete validation failure | reasoner/admission | kernel reasoning boundary | nonempty stable errors | request-bound | malformed result | evaluation | A17 |
| `ReasoningResult.REASONING_ERROR.reasoning_errors` | `REQUIRED_SEMANTIC` | K1 carrier | service/validator/protocol failure | reasoner/admission | kernel reasoning boundary | nonempty stable errors | request-bound | malformed result | reasoning | A16 |
| `EvidenceRef.{issuer_scope,evidence_namespace,local_identity,schema_binding}`; all reason records `UnknownReason`, `EvaluationErrorReason`, `ReasoningErrorReason`, `CertificateRejectionReason`, and `InterfaceFailureReason` fields `{issuer_scope,taxonomy_key,semantic_parameters}` | `REQUIRED_SEMANTIC` | K1 carrier | stable set-member identities | meaning/service/validator | result/certificate validators | component equality against owning Sigma/Service contract | issuer and referenced contract exact | malformed result | evaluation/reasoning/protocol | A11 |
| `ConflictRef.{conflict_kind,involved_identities}` | `REQUIRED_SEMANTIC` | K1 carrier | exact order-independent conflict identity | composition validator | discovery/lifecycle | tag plus exact set equality | involved versions exact | no conflict | structure/compatibility | A20 |
| `CertificateEnvelope.{certificate_key,certificate_kind,request_binding,subjects,environment,capability_key,fragment,dependencies,claimed_conclusion,validator_key,trust_root_key,abstraction_class,payload,evidence_refs}` | `REQUIRED_SEMANTIC` | Service | exact proof admission | certificate issuer | admission | kind-specific rule, exact root scope and producer independence | exact env/capability/root | no admission | trust/reasoning | A17 |
| `CertificateAdmission.ADMITTED.{certificate_key,admitted_conclusion}` | `REQUIRED_SEMANTIC` | K1 carrier | admitted proof/witness/counterexample remains kind-specific | trusted validator | kernel judgment gate | exact certificate/kind/conclusion receiving rule | certificate-bound | no admission | reasoning | A17 |
| `CertificateAdmission.MALFORMED_ENVELOPE.reasons` | `REQUIRED_SEMANTIC` | K1 carrier | malformed object proves nothing | envelope validator | package/lifecycle | nonempty interface-failure reasons | no semantic certificate identity required | no admission | protocol | A13 |
| `CertificateAdmission.REJECTED_NONDECISIVE.{certificate_key,rejection_reasons}` | `REQUIRED_SEMANTIC` | K1 carrier | rejected evidence proves neither claim nor negation | trusted validator | kernel judgment gate | nonempty stable rejection reasons | certificate-bound | no admission | reasoning/nonconformance | A13 |
| `CertificateAdmission.EVALUATION_ERROR.{certificate_key,evaluation_errors}` | `REQUIRED_SEMANTIC` | K1 carrier | concrete validator failure proves nothing | trusted validator | kernel judgment gate | nonempty stable errors | certificate-bound | no admission | evaluation | A17 |
| `CertificateAdmission.REASONING_ERROR.{certificate_key,reasoning_errors}` | `REQUIRED_SEMANTIC` | K1 carrier | validator/protocol failure proves nothing | trusted validator | kernel judgment gate | nonempty stable errors | certificate-bound | no admission | reasoning | A17 |
| `EventValue.{event_key,payload}`; `TraceEvent.{event_value,actor?}` | `REQUIRED_SEMANTIC` | Delta | typed event and optional actor | outcome former | outcome/auth/pair | event admission | exact EventKey | malformed outcome | evaluation | A12 |
| `SourceRef.{issuer_scope,source_kind,stable_source_identity,provenance_facts}`; `AuthorityRef.{authority_namespace,stable_attestation_identity}` | `REQUIRED_SEMANTIC` | Sigma | provenance separate from authority | binding/authority source | Origins/closure | self-contained/exact | issuer/attestation identity exact | source unresolved before Contract; authority open | representation/closure | A14 |
| `AuthorityFactBinding.authority_fact_key` | `REQUIRED_SEMANTIC` | Sigma | exact adoption/choice fact identity | authority subject former | closure/adoption | exact admitted tuple | AuthorityFactKey exact | open/no fact | closure/reasoning | A14 |
| `AuthorityFactBinding.admitted_attestation_refs` | `DERIVED` | Sigma admission | nonempty union of independently admitted evidence | authority validators/composition | closure/audit | group by fact key and union admitted certificate refs | certificate sets not identity | no fact if empty | closure/reasoning | A14 |
| `CompatibilityClaim.{claim_key,source_abi,target_abi,source_keys,target_keys,compatibility_contract,certificate_key,validator_key,trust_root_key}` | `REQUIRED_SEMANTIC` | Service | protocol compatibility only | claimant | discovery/migration | exact request/result/certificate/root admission | versions remain distinct | no compatibility | compatibility/reasoning | A20 |
| `MigrationDeclaration.{migration_key,source_environment,target_environment,semantic_relation,relation_contract,certificate_key}` | `REQUIRED_SEMANTIC` | Sigma | explicit semantics-preserving/change relation | migration author | binding analysis | support plus certificate admission | source/target exact | no migration | compatibility/reasoning | A20 |
| `MigrationDeclaration.{validator_key,trust_root_key}` | `REQUIRED_SEMANTIC` | Service | independently trusted migration validation | migration author | certificate gate | exact target/root scope and producer independence | exact capability/root version | no migration | compatibility/reasoning | A20 |
| `SemanticExtension.{extension_key,target_record_identity,owner_layer,semantic_effect,payload}` | `REQUIRED_SEMANTIC` | declared owner | explicit semantic extension | extension owner | package validator | exact support, target and owner rule | exact namespace/version | no extension | compatibility | A20 |
| `SemanticExtension.{certificate_key,validator_key,trust_root_key}` | `REQUIRED_SEMANTIC` | Service | independently trusted semantic-extension validation | extension owner | package validator | exact admission target/root scope and producer independence | exact certificate/capability/root versions | incompatible if absent/unadmitted | compatibility/reasoning | A20 |
| `InterfaceFailure.{domain,kind,reasons}` | `REQUIRED_SEMANTIC` | K1 carrier | failure outside truth | interface boundary | lifecycle/status mapper | nonempty/domain mapping | request-bound | no logical result | protocol/transport | A10 |
| challenge IDs, expected mappings/results, gold Contracts, hidden targets, undeclared outcome/evidence access, caller `chi_C`, caller replacement dependencies, caller event-class flags | `EXCLUDED` | Excluded | anti-oracle and frozen K1 ownership | none | none | presence rejects | never identity | always absent | malformed | A06 |
| implicit aliases, wildcard/`latest` versions, discovery-order or first-found selection, silent shadowing, unrecognized fields | `EXCLUDED` | Excluded | exact identity/conflict behavior | none | none | presence/use rejects | no equality role | always absent | compatibility/protocol | A20 |
| byte encoding, field serialization order, service endpoint as a semantic field, loader, repository, retry scheduler, deployment topology | `EXCLUDED` | Excluded | no K1 semantic role | none | none | outside v0 | no identity role | always absent | transport outside ABI | A03 |
| request IDs, timestamps, logs, timing, retry counters, display names outside `Diagnostics` | `EXCLUDED` | Excluded | cannot affect judgment | none | none | presence in semantic record rejects | no identity role | always absent | protocol | A11 |
| independent occurrence meaning beside a pair-owned occurrence binding; bare pair-coherence claim | `EXCLUDED` | Excluded | non-circular exact coherence | none | none | conflict/reject | no valid identity | always absent | structure/reasoning | A13 |
<!-- LEDGER-END -->

Ledger counts: **94 `REQUIRED_SEMANTIC`; 20 `DERIVED`; 2
`OPTIONAL_DIAGNOSTIC`; 5 `EXCLUDED`** (121 rows). The reproducible convention
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

Every `ContractSpec.logical_relation` is interpreted over explicit primary
inputs and an exact semantic-environment assignment `E` indexed by
`DependencyKey`. Lookup is total over the typed environment: `ABI` selects the
exact ABI coordinate; a plugin tag selects exact declared owner-identity
presence; declaration, symbol, and event tags select exact Delta records;
binding, profile, and extension tags select exact Sigma
records; `PAIR(k)` selects the typed product of its Delta pair declaration and
Sigma pair binding states; and
`AUTHORITY_FACT(k)`, `LEXICAL_BINDING(k)`, `CHOICE_BINDING(k)`, and
`TRUST_POLICY(k)` selects the trust-policy identity/owner and
`TRUST_ROOT(k)` selects the exact correspondingly typed map value. A missing
key has the exact absent coordinate value. No generic pair, untyped scope,
attestation-certificate, or implicit-choice coordinate exists.

Equality of relation observations is equality of the complete typed relation,
including every result, evidence, reason, and error field, not sampled
agreement. Define the following total operation for every logical relation
`L`, including empty and constant relations:

```text
freeDependencies(L) = {
  d : DependencyKey |
  there exist admitted primary inputs x and coordinate-typed candidate
  assignments E1,E2 on the same exact key domain such that
  E1 and E2 agree at every key except d, and
  L(x,E1) and L(x,E2) are unequal complete logical relations
}

support(ContractSpec c) = freeDependencies(c.logical_relation)
```

Thus `freeDependencies` is empty for a constant contract. For every `L`, if
two environments agree on `freeDependencies(L)`, `L` is extensionally
invariant between them; conversely every key in the set has the displayed
separating environments. This defines exact semantic support, rather than a
producer-selected over-approximation. A `ContractSpec` is conformant only when
this set is finite and its derived `dependency_support` field is exactly that
set. The field is recomputed from the relation and cannot be supplied,
certified, narrowed, or enlarged by its producer.

Candidate-assignment formation checks exact key kind/version and record type,
and applies Delta admission to every embedded `Value`; it does not consult
`L`, `dependency_support`, a semantic
dependency list, any capability, or any certificate. The definition therefore
has no support-validation or trust recursion.

This rule is the logical ABI's non-self-asserted support validator. It is a
total extensional conformance rule, not a capability, certificate, trust
claim, or additional service. A later representation may use a separately
trusted decision procedure or proof certificate to establish the equality,
but that artifact must prove this fixed relation and cannot define its own
support, validate itself, or introduce a new semantic dependency. Failure to
establish the equality rejects the enclosing record in the layer-specific
family below.

Every logical contract-bearing field is typed `ContractSpec`, so support is
total for value-admission domains; literal/function/predicate and occurrence
meanings; profile coverage; evidence, access, unknown and failure contracts;
sound and complete fragments; required evidence; compatibility; migration;
and semantic-extension effect/payload contracts. Trust is instead an exact
independently admitted `TRUST_ROOT` coordinate. No prose, bare list,
diagnostic value, or producer trust assertion participates.

Record identity and outgoing dependency are disjoint. Define exact root sets:

```text
rootKeys(declaration d)        = its DECLARATION key and any SYMBOL or EVENT
                                 identity declared by d
rootKeys(pair declaration d)   = {PAIR(d.pair_key)}
rootKeys(semantic binding b)   = {BINDING(b.binding_key)}
rootKeys(profile binding p)    = {PROFILE(p.profile_key)}
rootKeys(pair binding p)       = {PAIR(p.pair_key)}
rootKeys(authority fact a)     = {AUTHORITY_FACT(a.authority_fact_key)}
rootKeys(lexical binding l)    = {LEXICAL_BINDING(l.lexical_binding_key)}
rootKeys(choice binding c)     = {CHOICE_BINDING(c.choice_binding_key)}
rootKeys(trust root t)         = {TRUST_ROOT(t.trust_root_key)}
rootKeys(trust environment t)  = {TRUST_POLICY(t.trust_policy_key)}
rootKeys(semantic extension x) = {SEMANTIC_EXTENSION(x.extension_key)}
```

For other records, `rootKeys` is the exact semantic subject identities in the
record target; identity-only keys outside `DependencyKey`, such as a
certificate or service key, anchor no semantic-environment edge.
`subjectReferences(r)` contains every typed semantic coordinate named by a
non-identity field. A binding references its declaration and contract
supports; a profile references dimensions and contract supports but not its
own profile key; a pair references member bindings, event/type coordinates,
and independent occurrence support but not its own pair key; an authority
fact's attestation references are evidence rather than fact dependencies; and
a capability references targets, fragments, required evidence, required trust
roots, and failure support.
For a `TrustRootRecord`, `subjectReferences` and proper dependencies are empty:
validator/kind/target lists are embedding-policy permissions, not claims whose
semantics are supplied by those services or subjects. This is the
well-founded bootstrap base.

```text
rawProperDependencies(r) =
  subjectReferences(r) union
  UNION(support(c) for every ContractSpec c in r)

properDependencies(r) = rawProperDependencies(r)
  provided rawProperDependencies(r) intersect rootKeys(r) = {}
```

A nonempty intersection is an invalid self-edge; it is rejected rather than
included, subtracted, or treated as mandatory. Each displayed
`proper_declaration_dependencies` or `proper_semantic_dependencies` is a
derived view and must equal `properDependencies(r)`. A producer-supplied
smaller, larger, or self-containing set is rejected even if signed.

The direct graph contains exactly `(a,b)` for `a in rootKeys(r)` and
`b in properDependencies(r)`. Roots anchor records but are not outgoing
edges. The graph over the exact environment must be finite; missing targets
receive the ordinary layer-specific absent state; and every directed cycle is
invalid. `dependency_closure(r)` is the unique least set of proper targets
reachable by one or more direct edges from `rootKeys(r)` and excludes those
roots. Cycle rejection precedes closure, so the definition is total and
well-founded over proper edges only. A definitional occurrence construction is
ownership, not a back-edge.

Support, proper-edge, or closure mismatch has an exact outcome: in a value-admission/type
declaration it is `DECLARATION_INVALID`/`MALFORMED`; in a Sigma meaning,
profile, pair, authority, or migration it is
`BINDING_INCOMPATIBLE`/`MALFORMED(incompatible semantic binding)`; in a
capability or compatibility claim it is `CAPABILITY_INCOMPATIBLE` and therefore
`EVALUABILITY_MISSING` for that request; in a request it is
`MALFORMED_REQUEST`; and in a certificate envelope it is malformed-certificate
rejection with no claimed conclusion. A semantic extension follows its
declared owner layer: Delta invalid, Sigma binding-incompatible, or Service
capability-incompatible. A smaller producer list, even one signed by that
producer, establishes none of these conformance judgments.

K2 uses K1's recursive syntax `deps` equations unchanged. Syntax-derived keys
are subject roots, not producer-declared outgoing edges. The interface
projection `DependencyEnvironment` is derived as follows:

```text
required(C) =
  UNION(deps(attributed_clause) for every attributed clause in C)
  UNION(deps(choice) for every choice in C)
  UNION(deps(profile) for every explicit ProfileKey requirement)
  UNION(deps(pair) for every explicit EventScopePair requirement)

required(F) =
  UNION(deps(formula) for every formula in F)

DependencyEnvironment(subject) = (
  root_keys = required(subject),
  proper_dependencies = UNION(
    properDependencies(recordAt(k)) for k in required(subject)),
  transitive_dependency_closure = least proper-edge reachability from
    required(subject)
)
```

For each root, declaration and semantic proper dependencies are closed
transitively. A pair root's closure includes both symbols and bindings, owners,
controlled events/declarations, payload/signature types, and coherence binding
without a pair self-edge. A profile root's closure includes dimensions,
coverage-meaning dependencies, and their closure without a profile self-edge.
Authority, lexical, choice, trust, and semantic-extension coordinates enter
the same closure whenever the subject observes them.

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
- the same complete result for the same exact declaration, semantic inputs,
  `Delta`, `Sigma`, derived `chi_C`, and lexical scope.

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

A `ModelContract` is a structured projection of exactly one machine-facing
binding. Its signature, facet positions, evidence boundary, unknown/error
behavior, and semantic-contract reference must equal that binding and its
declaration. Its capability summaries may name only conformant capabilities
for the same target; summaries do not promise current availability.

Package conformance requires at least one matching `ModelContract` for every
literal, function, and predicate binding and every pair-owned occurrence
binding. `exact_symbol_key` is absent exactly for a literal binding and
present with the exact symbol otherwise. For an occurrence binding,
`semantic_contract_reference` is its exact `EventScopePairKey`; for an
ordinary binding it is the exact `BindingKey`. Additional translated records
are optional and must retain the same exact target.

Missing required structured information, a stale target version, an unequal
signature/facet/evidence/error statement, or a capability from another meaning
is `MALFORMED(model/machine contract mismatch)`. Explanatory wording is
diagnostic and creates neither a second denotation nor authority. Translations
are separate `ModelContract` records that preserve the same exact target.
Aliases are permitted only through `AliasBinding`; resolving an alias yields
its recorded target and never performs display-name or version selection.

## 5. Invocation, values, truth, evidence, and failure protocol

### 5.1 Typed requests

```text
ValueAdmissionRequest = (
  abi_version : AbiVersion,
  type_key : DeclarationKey[TYPE],
  value : Value,
  environment : SemanticEnvironment,
  dependency_environment : DependencyEnvironment,
  capability_target : TYPE_ADMISSION_TARGET(type_key, environment),
  capability_key : CapabilityKey
)
FunctionRequest = (
  abi_version : AbiVersion,
  symbol_key : SymbolKey[FUNCTION],
  binding_key : BindingKey,
  dependency_environment : DependencyEnvironment,
  arguments : sequence(Value),
  capability_target : BINDING_TARGET(binding_key),
  capability_key : CapabilityKey
)
PredicateRequest = (
  abi_version : AbiVersion,
  symbol_key : SymbolKey[PREDICATE],
  binding_key : BindingKey,
  dependency_environment : DependencyEnvironment,
  arguments : sequence(Value),
  capability_target : BINDING_TARGET(binding_key),
  capability_key : CapabilityKey
)
ProfileRequest = (
  abi_version : AbiVersion,
  profile_key : ProfileKey,
  environment : SemanticEnvironment,
  coverage_subject : typed profile-specific subject,
  capability_target : PROFILE_TARGET(profile_key),
  capability_key : CapabilityKey
)
PairAdmissionRequest = (
  abi_version : AbiVersion,
  pair_key : EventScopePairKey,
  environment : SemanticEnvironment,
  complete_dependencies : DependencyEnvironment,
  capability_target : PAIR_TARGET(pair_key),
  capability_key : CapabilityKey
)
AuthorityAdmissionRequest = (
  abi_version : AbiVersion,
  authority_fact_key : AuthorityFactKey,
  environment : SemanticEnvironment,
  complete_dependencies : DependencyEnvironment,
  capability_target : ENVIRONMENT_JUDGMENT_TARGET(
    AUTHORITY_FACT_ADMISSION, (authority_fact_key), environment),
  capability_key : CapabilityKey
)
MigrationAdmissionRequest = (
  abi_version : AbiVersion,
  migration : MigrationDeclaration,
  environment : SemanticEnvironment,
  complete_dependencies : DependencyEnvironment,
  capability_target : ENVIRONMENT_JUDGMENT_TARGET(
    MIGRATION_RELATION_ADMISSION, (migration), environment),
  capability_key : CapabilityKey
)
CompatibilityAdmissionRequest = (
  abi_version : AbiVersion,
  claim : CompatibilityClaim,
  environment : SemanticEnvironment,
  complete_dependencies : DependencyEnvironment,
  capability_target : ENVIRONMENT_JUDGMENT_TARGET(
    COMPATIBILITY_CLAIM_ADMISSION, (claim), environment),
  capability_key : CapabilityKey
)
SemanticExtensionAdmissionRequest = (
  abi_version : AbiVersion,
  extension : SemanticExtension,
  environment_without_extension : SemanticEnvironment,
  complete_dependencies : DependencyEnvironment,
  capability_target : ENVIRONMENT_JUDGMENT_TARGET(
    SEMANTIC_EXTENSION_ADMISSION, (extension),
    environment_without_extension),
  capability_key : CapabilityKey
)
DiscoveryRequest = (
  abi_version : AbiVersion,
  target : exactly one CapabilityTarget,
  judgment : JudgmentTag,
  required_fragment : ContractSpec[Service],
  complete_dependency_scope : finset(DependencyKey)
)
```

For `ValueAdmissionRequest`, `environment` must contain the exact type
declaration, trust environment, lexical and choice coordinates relevant to the
value, and every declaration coordinate observed by
`admitted_value_domain`. Its dependency environment has that type declaration
as a root and exactly the proper-edge closure of the admission contract. The
type-admission descriptor must cover the same environment target and complete
closure. A context-free target, missing support, extra scope entry, or smaller
producer dependency set is malformed and no admission service is invoked.

The argument sequence length, positions, and admitted types must equal the
exact declaration. `symbol_key` and `binding_key` must name that same
declaration and meaning. The dependency environment must equal the
mechanically derived and transitively closed environment; it is never a
caller-maintained list. The requested capability must advertise the exact
tagged target, judgment, dependency scope, and applicable sound fragment.
The request target must be a member of
`CapabilityDescriptor.supported_targets` and its tag must agree with the
service role. `PairAdmissionRequest.environment` contains the complete pair,
member, event/type, meaning, and support dependencies. A reasoning request uses
the exact environment/judgment target defined in section 6.2. Target mismatch
is a malformed request; no service is invoked and no similarly named binding,
profile, pair, type, or environment can substitute.

Each environment-level admission request carries its complete exact subject,
environment, roots, proper dependencies, and closure. An authority subject is
the exact `AuthorityFactKey`; a migration and compatibility subject is its
full exact record; an extension request contains the full extension while
`environment_without_extension` excludes that unadmitted extension and thus
prevents self-support. Discovery must find the matching admission service
role, `JudgmentTag`, target, fragment, dependency scope, and independently
admitted trust root before validation is invoked.

A predicate receives only `arguments`. Neither the logical request nor any
capability-dependent projection includes a Contract, full `Outcome`,
`chi_C`, authority context, implicit anchor, or undeclared evidence. A
function has the same access restriction. The environment proves semantic
identity and closure; it is not an extra data channel to the meaning.

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
trace; `occurrence_eval` must be the occurrence predicate on that same trace;
and the two records must be unequal. Any missing field, non-admitted trace,
different environment, or equal result records makes the result malformed.
The other admission-result tags echo their request identity and certificate;
their `NOT_ADMITTED` variants are nondecisive and grant no admission.

### 5.3 Stable evidence and reason equality

```text
EvidenceRef = (
  issuer_scope, evidence_namespace, local_identity, schema_binding
)
UnknownReason = (
  issuer_scope, taxonomy_key, semantic_parameters
)
EvaluationErrorReason = (
  issuer_scope, taxonomy_key, semantic_parameters
)
ReasoningErrorReason = (
  issuer_scope, taxonomy_key, semantic_parameters
)
CertificateRejectionReason = (
  issuer_scope, taxonomy_key, semantic_parameters
)
InterfaceFailureReason = (
  issuer_scope, taxonomy_key, semantic_parameters
)
```

The six sorts are disjoint. Equality is exact component equality. Parameters
are typed finite logical records whose equality is defined by their declared
schema; an untyped message is diagnostic only and cannot be an identity
parameter. Finite sets deduplicate equal members and have no order. Reordering
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
  kind : MALFORMED_REQUEST | MALFORMED_RESULT |
         PROTOCOL_FAILURE | TRANSPORT_FAILURE,
  reasons : nonempty finset(InterfaceFailureReason)
)
```

`InterfaceFailure` is not a `Truth`, `Eval`, profile result, consistency
result, or relation result. A malformed declaration, binding, or request is
rejected before invocation. A malformed completed result is not repaired,
defaulted, partially accepted, or treated as unknown.

At the K1 boundary, a concrete evaluator's protocol or transport failure maps
to the applicable nonempty `EvaluationErrorReason`: at a function boundary
it yields `TERM_ERROR`, and at a predicate or concrete-profile boundary it
yields `EVALUATION_ERROR`. A reasoning service, symbolic profile service, or
certificate validator failure maps to nonempty `ReasoningErrorReason` and
`REASONING_ERROR`. A discovery protocol/transport failure remains
`DISCOVERY_FAILURE` and yields no evaluability result. Thus transport and
protocol failures remain distinguishable from logical unknown, ordinary
absence, and completed inconclusiveness.

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
service role, judgment, one echoed tagged target, fragments, and dependency
scope. An asserted conclusion outside the sound
fragment is non-conformant. A dependency not covered by
`dependency_scope` makes the capability incompatible with the request.
`service_role` determines whether invocation failure is an evaluation,
reasoning, or pair-admission failure; it cannot change K1 result meaning.
`complete_fragment` is absent exactly for the concrete-only and partial
classes; absence never implies completeness.

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
  environment : SemanticEnvironment,
  required_fragment : ContractSpec[Service],
  complete_dependencies : DependencyEnvironment,
  capability_target : ENVIRONMENT_JUDGMENT_TARGET(
    judgment, subjects, environment),
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
The request environment must equal them exactly. An alternate or missing
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
`REASONING_ERROR`, never logical/profile unknown. Service failure is also
reasoning error and yields no judgment. A concrete evaluator error encountered
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
A formed envelope must then match closure, request identity, target,
capability, fragment, complete dependencies and supports, validator identity,
and one exact `trust_root_key`. Before any validator is invoked, the request's
`TrustEnvironment` must contain `TRUST_ROOT_ADMITTED` for that key; the root
must list this validator, certificate kind, and exact
`trustTarget(request_binding)`: respectively the pair, authority, migration,
compatibility, or extension key for those admission requests, or
`JUDGMENT_TRUST_TARGET(judgment,subjects)` for a reasoning request. The descriptor
must list that key in `required_trust_roots`; and all producer-independence
inequalities in section 2.3 must hold. Missing, incompatible, wrong-scope, or
self-trusting roots yield `REJECTED_NONDECISIVE` with no invocation or
admission. A separately trusted validator whose sound fragment covers the
kind and exact environment then checks the payload. Descriptor/root equality
alone is never sufficient.
`REJECTED_NONDECISIVE` means the formed object did not establish its claim and
yields no logical conclusion, including no negation of the claim. Concrete
witness/counterexample validation that encounters a K1
`ERROR` yields `EVALUATION_ERROR`; validator/service/protocol failure is
`REASONING_ERROR`. Both yield no conclusion. A proof-system identity or integrity signature can
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

**Definitional path.** `DEFINITIONAL_T3_A1` makes the occurrence meaning
definitionally equal to:

```text
occurrence(T) =
  ANY_RESULT({
    scope(e.event_value) | e occurs in T
  })
```

The ABI owns this construction; the producer supplies no independent
occurrence denotation. The exact frozen T3/A1 rule gives empty trace
`VALUE(FALSE,{},{})`, unions evidence/unknown/error sets over every event,
lets any error dominate, otherwise lets TRUE decide while retaining collected
unknown metadata, and handles multi-event traces without traversal-order
effects. `scope` must return `VALUE(FALSE,{},{})` for every event key
outside `controlled_keys`.

**Independent-proof path.** `INDEPENDENT_COHERENCE_PROOF` permits distinct
scope and occurrence meanings only with an admitted
`EVENT_PAIR_COHERENCE_PROOF`. Its `PAIR_VALIDATION` capability must cover
every admitted trace and complete `Eval` field, bind the exact pair/members/
controlled keys/environment, and use an already admitted exact trust root and
producer-independent validator under sections 2.3 and 6.5. Neither validator
soundness nor trust may depend on the pair producer, its claim, the unadmitted
pair, or a service supplied by that producer.

Successful admission binds the exact pair meanings. A bare claim is malformed.
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

An absent profile meaning is `OPEN_BINDINGS`, not unknown. An absent
compatible checker is `EVALUABILITY_MISSING`, and undecidable checker
discovery is `EVALUABILITY_UNKNOWN`; neither is `PROFILE_UNKNOWN` and neither
produces any profile result. No profile
result certifies intent completeness or changes Contract acceptance,
satisfiability, or authority.

### 7.4 Provenance and authority

```text
SourceRef = (
  issuer_scope, source_kind, stable_source_identity, provenance_facts
)
AuthorityRef = (
  authority_namespace, stable_attestation_identity
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
normative field. Closure/adoption accepts a fact only after an
`AUTHORITY_FACT_ATTESTATION` certificate validates that exact tuple under an
already admitted scoped trust root and a producer-independent validator. A missing
certificate or validator leaves the fact open. A malformed or rejected
attestation may make its envelope/package nonconformant but proves no invalid
authority fact and produces no `AuthorityFactBinding`; it is retained only as
its separate certificate/admission result. Validator failure is reasoning
error with no fact.

The validator is discoverable only through service role
`AUTHORITY_VALIDATION`, judgment `AUTHORITY_FACT_ADMISSION`, and the exact
environment target in `AuthorityAdmissionRequest`; a successful receiving
result is only `AUTHORITY_FACT_ADMITTED`. Thus the admission environment and
target are closed and invocable, while rejection/failure has no normative
effect.

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
DISCOVERY_FAILURE(target, PROTOCOL_FAILURE | TRANSPORT_FAILURE,
                  nonempty finset(InterfaceFailureReason))
```

`ConflictRef=(conflict_kind,involved_identities)`, where the second
component is a nonempty finite set of exact record identities. Its equality is
the tag plus set equality, independent of discovery/composition order.

Every result echoes exactly the request's one tagged `target`; a different or
omitted target is a malformed discovery result. `EXACT_TARGET_FOUND` carries
at least one capability whose service role, judgment, target membership,
fragment, and scope all match together. When the target's declaration/meaning
is present but no such service exists, discovery returns
`TARGET_PRESENT_SERVICE_ABSENT`. `EXACT_TARGET_ABSENT` leaves a binding,
profile, or pair requirement open; an absent required type declaration remains
malformed under declaration validation. `DISCOVERY_UNDECIDED` maps to
`EVALUABILITY_UNKNOWN` only when declarations/meanings needed for closure
are already known; it never guesses them. The two incompatible tags fail
loudly. Meaning-present/service-absent and outside-fragment map to
`EVALUABILITY_MISSING` for the exact request. `DISCOVERY_FAILURE` gives no
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
| partial or out-of-complete-fragment reasoning completes inconclusively | `COMPLETED_INCONCLUSIVE` and applicable logical/profile unknown |
| complete in-fragment reasoning completes inconclusively | reasoning protocol failure and `REASONING_ERROR` |
| concrete evaluator returns conformant error | `EVALUATION_ERROR` |
| reasoner returns conformant failure | `REASONING_ERROR` |
| invocation transport/protocol failure | `InterfaceFailure`, mapped by service role as section 5.4 |

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
  target_record_identity : DependencyKey,
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
validator, kind, and target and satisfy producer independence; no record owns,
redefines, or self-validates trust.

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
   capability target/fragment/trust, authority fact key, migration, and semantic extension
   effect.
4. Different exact identities never shadow one another. Display equality does
   not create a duplicate.
5. An occurrence binding independently duplicated beside a pair-owned
   occurrence meaning conflicts even if sampled results agree.
6. `AuthorityFactBinding` is the sole special coalescence: records with the
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
| 2 | model-facing and machine-facing contracts share one exact semantic key | `SemanticBinding`, `ModelContract`, `AliasBinding` | exact projection equality; stale/mismatched document is malformed | A05 | presentation rendering excluded |
| 3 | function/atom meanings match `Delta`, return `TermResult/Eval`, receive only declared facets, and retain mechanically extracted dependencies | `SemanticBinding`, binding-target function/predicate requests, `ContractSpec`, `DependencyEnvironment` | total extensional support plus binding/access/request/result conformance and closure recomputation | A06,A08,A09,A10 | invocation transport excluded |
| 4 | every `EventScopePair` has typed members, immutable controlled keys, and exact empty/multi-event full-result coherence | pair declaration/binding, pair request/result, positive proof and typed incoherence certificate | definitional T3/A1 or independently rooted complete proof; generic rejection stays open, only typed admitted trace/full-`Eval` inequality is incompatible | A12,A13 | certificate byte form excluded |
| 5 | concrete evaluators preserve exact `Eval`, stable evidence/reason identities, and declared dependencies | `PredicateRequest`, `Eval`, evidence/reason records | exact algebra, nonempty invariants, set equality, malformed-result failure | A10,A11 | evidence storage excluded |
| 6 | capabilities bind exact targets, sound/complete fragments, dependencies, independently admitted trust-root requirements, and concrete/partial/complete class | `CapabilityDescriptor`, `CapabilityTarget`, `TrustEnvironment`, `DiscoveryRequest/Result` | role, judgment, target, fragment, scope, root scope, and producer independence validate together; complete in-fragment decisiveness | A02,A03,A16 | service location excluded |
| 7 | witnesses/proofs/models/counterexamples/relations bind exact typed closure/environment and never override `chi_C`; internal `==Eval` remains separate | `ReasoningRequest/Result`, `CertificateEnvelope/Admission`, typed `SemanticEnvironment` | §6 kind-specific admission; strong proof/decisive countermodel; derived choice map and exact lexical/choice/authority/trust coordinates | A17,A18 | proof payload encoding excluded |
| 8 | evaluator failures and reasoning failures remain distinct and yield no logical/profile conclusion | `InterfaceFailure`, `TermResult`, `Eval`, `ProfileResult`, `ReasoningResult` | service-role mapping; no unknown/default conversion | A10,A15,A16 | transport error representation excluded |
| 9 | exact profiles, pairs, and recursive dependencies participate in closure/composition/full equivalence; profile unknown and errors remain distinct | profile/pair bindings and targets, dependency environment, profile result | recomputed closure; absence is evaluability-only; invoked checker alone can yield profile unknown | A06,A13,A15 | checker transport excluded |
| 10 | joint claims need one capability covering the whole cross-plugin dependency set | joint environment/judgment target, `CapabilityDescriptor`, reasoning request/certificate | absent/undecidable target yields evaluability missing/unknown simultaneously with logical unknown absent decisive evidence; invoked/failure branches remain distinct | A19 | service orchestration excluded |
| 11 | `SourceRef` is self-contained provenance; only validated `AuthorityRef` tuples adopt or bind choice | `SourceRef`, `AuthorityRef`, `AuthorityFactKey`, coalesced `AuthorityFactBinding` | source adds no authority; producer-independent root admission validates the exact tuple; multiple admitted attestations union as evidence | A14,A18 | attestation encoding excluded |

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
| K2-A01 | reference `qα` with no declaration; separately, exact valid declaration `qβ` with no binding | first has invalid plus explicit binding/discovery/invocation blocked states; second has absent plus explicit discovery/invocation blocked states | first `MALFORMED`; second `WELL_FORMED+OPEN_BINDINGS`; no omitted coordinate | formation versus semantic closure | let meaning/service create a declaration or leave later state implicit | Delta/Sigma separation |
| K2-A02 | one exact `qα` binding with compatible `Sα`; same binding with no service | bound+discovered+invocable versus bound+capability absent+invocation blocked | both can be closed; available versus `EVALUABILITY_MISSING` | denotation, availability, and invocation | call absent/unevaluable meaning absent or false | service separation |
| K2-A03 | exact valid declaration and bound meaning `Pα@1/qα`; v1 discovery reports service absent, failure, or undecided; separate v2 exposes `Pα@2/qα/Sβ` | absent, exact `DISCOVERY_FAILED(failure)`, and undecided are distinct total states; v2 target unequal | missing, no evaluability status on failure, or evaluability unknown; no truth and no v2 substitution | exact version, absence, failure, and uncertainty | latest/range/display/v2 fallback or failure-as-unknown | exact version/discovery |
| K2-A04 | two keys share display label but differ in owner namespace, plugin, or function/predicate kind | two distinct declared identities or kind conflict if forced under one key | coexist when keys differ; `MALFORMED` on kind collision | owner and kind | display-name equality or shadowing | namespacing/kind |
| K2-A05 | exact conformant `qα` binding; model contract names old signature or `Pα@2` | binding is bound; document mismatch prevents package conformance | `MALFORMED(model/machine contract mismatch)`; no rebind | compiler-visible contract versus denotation | trust prose/alias to select meaning | matching identity |
| K2-A06 | syntax roots are `{qα,Tα,Pα@1}`; producer supplies `{qα}`, substitutes `Tβ`, or adds a binding/profile/pair self-edge | exact roots remain identity; proper edges/closure are recomputed and unequal or cyclic input is invalid | malformed request/record; Contract closure uses the full well-founded proper-edge graph | root identity, authority/lexical/choice/trust coordinates, and proper transitive dependencies | caller-maintained smaller support or mandatory self-edge | mechanical dependencies |
| K2-A07 | admitted `v0:Tα`; non-admitted `v1` used as choice alternative, argument, payload, or result | type declaration has `BINDING_NOT_REQUIRED`; contextual admission validates first and invalidates every use of second | well typed versus `MALFORMED` or evaluation protocol error; all later coordinates explicit | typed membership versus Sigma binding | ignore unused ill-typed value, require a meaning binding, or coerce | type/value admission |
| K2-A08 | predicate declaration has final-derived value at position 1 and evidence-derived value at 2; service attempts full Outcome/extra evidence access | declared request is invocable; attempted access violates boundary | conformant `Eval` versus `EVALUATION_ERROR`/package malformed | explicit facets and evidence schema | implicit Outcome/context channel | facet/access boundary |
| K2-A09 | broad `qα:(Tα,State,EvidenceStore)->Bool` with explicit reusable meaning; variant requests expected result or hidden target | first bound/invocable; oracle variant excluded and package-malformed | legitimate exact `Eval` versus no conformant binding | abstraction versus privileged lookup | expected-answer/challenge branch | anti-oracle binding |
| K2-A10 | `fα` returns `TERM_ERROR({te})`; `qα` returns `VALUE(UNKNOWN,{}, {u})`; another invocation returns `ERROR({ee},{},{})` | three conformant completed tags | term evaluation error; factual truth unknown; predicate evaluation error | term failure, truth, and predicate failure | encode term error as unknown or error as false | exact result algebra |
| K2-A11 | `VALUE(TRUE,{e1,e2},{u1})` represented with repeated/reordered references | one logical set-valued result | exact equality after deduplication; unequal identities remain | stable support/reason identity | list order or message-text equality | A1/A2 set semantics |
| K2-A12 | exact controlled `eα` declaration and payload; traces with matching actor, absent actor, wrong actor; attempted caller flag `OBSERVATIONAL` | events admitted; actor affects matching grants; flag rejected | matching grant may authorize; absent/wrong actor has no match; flag malformed | immutable class versus actor matching | witness/caller control flag | event/authorization |
| K2-A13 | pair with empty/multi-event full-`Eval` branches; definitional/admitted proof; malformed/stale/rejected proof, missing/failed validator; or exact `EVENT_PAIR_INCOHERENCE_COUNTEREXAMPLE` carrying one admitted trace and two unequal complete `Eval` records | positive result binds; generic rejection/missing/failure stays open; only typed `PAIR_INCOHERENCE_ADMITTED` sets binding incompatible | bound; `OPEN_BINDINGS` plus evaluability; `REASONING_ERROR` with no admission; or `MALFORMED(incompatible semantic binding)` only for typed negative | generic certificate rejection versus complete pair incoherence | infer pair falsity from rejection, producer assertion, sample, or logical counterexample | EventScopePair coherence |
| K2-A14 | self-contained source `srcα`; exact `AuthorityFactKey`; two independent admitted attestations `{ca1}` and `{ca2}`; source alone/unadmitted attestation variants | provenance is separate; equal fact keys coalesce evidence to `{ca1,ca2}`; invalid evidence produces no fact | origin retained; one normative fact can adopt/bind only after independent trust-root admission | origin, fact identity, and admission evidence | fifth-field identity, evidence-set conflict, or authority from wording/signature/evaluation | provenance/authority |
| K2-A15 | exact profile `Rα` with dimensions `{d1,d2}`; after a compatible checker is discovered and invoked: full evidence, known missing `d2`, conformant unresolved coverage, concrete failure, or symbolic failure | five distinct completed/failure states; absent/undecidable checker discovery is separate evaluability only | complete, incomplete, profile unknown, evaluation error, reasoning error; absence gives no profile result | coverage status versus failure/availability | treat absence/service failure as incomplete/unknown | profile boundary |
| K2-A16 | concrete-only, partial-symbolic, and complete-fragment descriptors; in/out-of-fragment requests; complete in-fragment “no result” | capability-specific invocability and completion | concrete result only; partial/outside may be relation unknown; forbidden completion is `REASONING_ERROR` | soundness versus completeness | unknown from complete in-fragment service | capability relativity |
| K2-A17 | exact witness/proof/counterexample/internal `==Eval` certificate; stale environment or relation relabel | first admitted only for own kind; stale/relabel rejected | named SAT/UNSAT/relation/internal conclusion or no judgment | evidence kind/environment | reuse stale proof or expose internal equality as public proof | certificate admission |
| K2-A18 | closed Contract has exact `ChoiceBindingKey(c)` referencing admitted `AuthorityFactKey` and derives `chi_C(c)=v0`; request/witness supplies `v1`; duplicate attestations support the same fact | typed choice/authority coordinates validate and attestations coalesce; override malformed | closure and judgments use only `v0`; evidence multiplicity does not change choice | controller/authority choice binding versus attestation evidence | request-selected choice or certificate-set-selected fact | mechanical `chi_C` |
| K2-A19 | one closed joint consistency subject depending on `{qα,qβ,Tγ}` with no decisive core evidence; (a) only local targets, (a2) joint discovery undecided, (b) exact joint partial target completes inconclusively, (c) exact joint complete target returns admitted witness, (d) invocation fails | (a)/(a2) no invocation; (b)--(d) exact joint environment target invoked | (a) `EVALUABILITY_MISSING+CONSISTENCY_UNKNOWN`; (a2) `EVALUABILITY_UNKNOWN+CONSISTENCY_UNKNOWN`; (b) available plus the same logical unknown; (c) `CONSISTENCY_SAT`; (d) `REASONING_ERROR` and no conclusion for that invocation | independent evaluability, logical evidence, invocation history, and failure | conjoin local results or make logical unknown invocation-only | cross-plugin scope |
| K2-A20 | explicit migration `Pα@1` to `Pα@2`; exact compatibility and semantic-extension subjects with their admission targets/certificates; aliases/latest/first-found and unvalidated extension variants | each validator is discoverable/invocable only through its exact judgment/target and independent root; migration yields a new explicit binding | admitted named relation/claim/extension only; rejected proof grants none; unknown/unvalidated extension is incompatible | identity, protocol compatibility, semantic relation, and extension effect | mutate original, discovery-order substitute, or silently ignore extension | migration/version/extension |

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

#### Trace K2-A05 — model/machine mismatch

1. Exact predicate `qα` is declared with argument sequence
   `(Tα,State)` and facets `({}, {final})`.
2. Its unique `SemanticBinding(qα)` matches and reaches
   `SEMANTICALLY_BOUND`.
3. A model contract targets `qα` but states one argument or a different
   version.
4. Model-contract projection validation detects inequality before discovery;
   explanatory prose and aliases cannot repair it.
5. The package final status is
   `MALFORMED(model/machine contract mismatch)`; the valid machine meaning
   is not silently rebound and no request is issued.

#### Trace K2-A09 — broad meaning versus oracle

1. `qα` is declared with exact typed arguments
   `(Tα,State,EvidenceStore)` and only final/evidence facet positions.
2. Its binding gives a deterministic reusable denotation, dependency closure,
   evidence schema, access list, and honest unknown/error contracts.
3. A compatible evaluator is discovered; a conformant request contains only
   the three positional values, exact binding/dependencies, and capability.
4. A conformant `Eval` validates and yields the matching K1 truth/error
   status.
5. In the adversarial variant, the binding or request asks for an expected
   result, hidden target, challenge identity, or full Outcome. The excluded
   field/access is detected before or during invocation.
6. Final status for that variant is package/request malformed or
   `EVALUATION_ERROR(undeclared access)`, with no logical conclusion.

#### Trace K2-A10 — term error, factual unknown, and predicate error

1. Exact declarations and meanings for function `fα` and predicate `qα`
   validate, and compatible evaluator capabilities are discovered.
2. A conformant function request returns
   `TERM_ERROR({te})`; a containing atom projects it to evaluation error and
   does not invoke its predicate.
3. A separate conformant predicate request returns
   `VALUE(UNKNOWN,{}, {u})`; nonempty `{u}` validates and renders
   `TRUTH_UNKNOWN`.
4. A third predicate invocation returns `ERROR({ee},{},{})`; nonempty
   `{ee}` validates and renders `EVALUATION_ERROR` with no truth.
5. The three final families remain distinct; no conversion, default, or
   connective-local plugin aggregation occurs.

#### Trace K2-A13 — event-pair coherence

1. The exact pair declaration validates distinct typed scope/occurrence
   predicates, nonempty immutable controlled keys, and derived facets.
2. In the definitional branch, the scope binding validates and the ABI derives
   the occurrence result by T3/A1 for every trace. Empty, multi-event, true,
   false, unknown, evidence, and error branches are therefore bound exactly.
3. In the independent branch, discovery finds a separately trusted complete
   pair validator for the exact `PAIR_TARGET`; an independently owned, already
   admitted root covers its producer-independent validator, certificate kind,
   and target. The certificate binds the whole pair/environment and is
   admitted before `SEMANTICALLY_BOUND`.
4. A bare claim or malformed envelope is nonconformant but proves no
   incoherence. A stale, incomplete, or `REJECTED_NONDECISIVE` proof and a
   missing proof/validator leave `OPEN_BINDINGS`, with applicable
   missing/unknown evaluability. Validator failure yields `REASONING_ERROR`
   and no admission, again leaving the pair open.
5. A typed `EVENT_PAIR_INCOHERENCE_COUNTEREXAMPLE`, or the same complete
   equality validator's typed negative result, binds one exact admitted trace
   plus its unequal complete scope-aggregate and occurrence `Eval` records.
   Only receiving `PAIR_INCOHERENCE_ADMITTED` makes the pair incompatible and
   `MALFORMED`; generic rejection never does.
6. Only either successful non-circular admission branch reaches pair-bound
   closure and permits a conditional-event Contract to close.

#### Trace K2-A15 — profile outcome separation

1. The exact plugin identity and every declaration dependency validate;
   `Rα` then binds exact dimensions `{d1,d2}`, coverage meaning, evidence
   schema, semantic dependencies, and failure contracts. The Contract
   explicitly requires it and is otherwise closed.
2. Discovery absence gives `EVALUABILITY_MISSING` and no profile result.
3. With a compatible checker, evidence for both dimensions yields
   `PROFILE_COMPLETE`; known omission of `d2` yields
   `PROFILE_INCOMPLETE`; undecidable coverage yields
   `PROFILE_UNKNOWN`.
4. A concrete checker failure yields `EVALUATION_ERROR`; a symbolic checker
   failure yields `REASONING_ERROR`.
5. Each is a distinct final family, and none changes acceptance,
   satisfiability, or intent completeness.

#### Trace K2-A16 — capability class and fragment

1. All exact subject declarations and meanings validate, then the same closed
   subject and exact mechanically derived dependency environment are formed.
2. A concrete-only descriptor validates concrete invocation but supplies no
   universal proof conclusion.
3. A partial-symbolic descriptor covers the sound fragment; an inconclusive
   completion becomes the applicable logical unknown.
4. A complete-fragment descriptor receives an in-complete-fragment request
   whose dependencies are wholly covered. A decisive admitted certificate
   yields its named judgment.
5. If that service instead returns “no result,” result validation converts the
   protocol violation to `REASONING_ERROR`, never logical/profile unknown.
   An out-of-complete-fragment request may be inconclusive under the sound
   fragment.

#### Trace K2-A17 — certificate kind and exact environment

1. Exact declarations, meanings, closure, capability, subject, and mechanical
   dependency environment validate.
2. A certificate envelope binds them, one kind, claimed conclusion,
   validator, one already admitted exact scoped trust root, and abstraction
   class; producer-independence checks pass before validator invocation.
3. Kind-specific admission checks the strong proof or decisive counterexample
   rule. If admitted, only the matching named judgment is emitted.
4. An internal `==Eval` derivation instead emits only
   `INTERNAL_EVAL_EQUAL`.
5. A stale environment, missing dependency, `UNKNOWN` offered as a logical
   counterexample, evaluator/reasoning error, or relabeled certificate is
   rejected or errors and produces no relation/consistency conclusion.

#### Trace K2-A19 — joint dependency scope

1. Exact declarations and bindings from `Pα@1` and `Pβ@1` compose; the
   joint formula's mechanical environment includes both plus shared `Tγ`.
2. Form exactly one `ReasoningRequest` with judgment `CONSISTENCY`, the closed
   joint Contract as subject, and exact
   `ENVIRONMENT_JUDGMENT_TARGET(CONSISTENCY,subject,environment)`.
3. Variant (a) discovers only local binding/environment targets. None equals
   the joint target, so final simultaneous coordinates are
   `EVALUABILITY_MISSING` and `CONSISTENCY_UNKNOWN`; local admitted results do
   not compose. Variant (a2) cannot decide discovery and yields
   `EVALUABILITY_UNKNOWN` with that same logical unknown.
4. Variant (b) discovers an exact joint partial capability, invokes it, and it
   conformantly completes inconclusively. It yields the same
   `CONSISTENCY_UNKNOWN` with `EVALUABILITY_AVAILABLE` and a different
   lifecycle history.
5. Variant (c) discovers an exact joint complete in-fragment capability whose
   dependency scope covers `{qα,qβ,Tγ}`. Its admitted satisfying witness gives
   the named decisive status `CONSISTENCY_SAT`.
6. Variant (d) invokes that exact joint capability but the service/protocol
   fails; the final result is `REASONING_ERROR` and no consistency conclusion.

#### Trace K2-A20 — explicit migration

1. Source and target declarations and bindings validate, and environments
   `Pα@1` and `Pα@2` remain distinct exact identities.
2. A migration names both, one semantic relation, its exact certificate,
   validator, and already admitted producer-independent trust root. Exact
   compatibility and semantic-extension variants form their own environment
   targets and discover their required validator roles.
3. Certificate admission establishes only that named relation. Migration
   forms a new Contract/binding that explicitly names target keys; source
   identity remains unchanged.
4. If semantic or representation facets change, the required new binding or
   representation judgment is recorded.
5. Alias, latest-version, first-found, display equality, absent/rejected
   certificate, or discovery order supplies no admission. An unknown or
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
internal `==Eval`, event, profile, provenance, authority, composition,
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
  projectable; lifecycle coordinates remain independent.
- [x] The exhaustive ledger assigns every logical record/field exactly one of
  `REQUIRED_SEMANTIC`, `DERIVED`, `OPTIONAL_DIAGNOSTIC`, or
  `EXCLUDED`; its 121 rows count 94/20/2/5 respectively under the stated body-row
  convention, and diagnostics affect
  no K1 judgment or semantic duplicate equality.
- [x] Declarations cover types/value admission, literals, typed functions and
  predicates, facets, immutable events, and exact companion pairs.
- [x] Dependencies and `chi_C` are mechanical derived views and cannot be
  omitted, replaced, or overridden; roots are not edges, self-edges/cycles are
  invalid, and every logical contract has total exact support and well-founded
  proper-edge closure across authority, lexical, choice, trust, and other
  observable coordinates.
- [x] Meanings, model contracts, typed invocation, results, evidence/reasons,
  failures, capabilities, and discovery preserve all K1 boundaries; every
  descriptor/query/result validates one exact binding/type/profile/pair/
  environment target with role, judgment, fragment and scope.
- [x] Complete in-fragment reasoning is decisive or a reasoning error;
  internal `==Eval` is not a public relation.
- [x] Every certificate binds exact closure, environment, capability,
  dependencies, conclusion, validator, independently admitted scoped trust
  root, producer independence, and abstraction class; external bootstrap is
  non-circular and grants no K1 normative role.
- [x] Event-pair admission is non-circular and covers empty/multi-event truth,
  evidence, unknown, and error behavior; malformed/rejected evidence leaves it
  open and only a typed admitted trace with two unequal complete `Eval`
  records can establish incompatibility.
- [x] Profiles preserve complete/incomplete/unknown/evaluation-error/reasoning-
  error distinctions and cannot certify intent completeness.
- [x] Provenance grants no authority; `AuthorityFactKey` is the exact semantic
  tuple, and independently admitted attestations coalesce as evidence without
  changing or duplicating the normative fact.
- [x] Joint reasoning requires one capability covering the whole exact
  cross-plugin dependency environment; for valid closed logical judgments,
  absence/undecidable discovery yields evaluability missing/unknown together
  with logical unknown absent decisive evidence, while profile unknown remains
  invocation-only.
- [x] Version skew, migration, duplicates, disjoint semantic/diagnostic
  extensions, exact compatibility/extension validation paths, discovery
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
