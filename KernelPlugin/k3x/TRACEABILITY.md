# K3-X repair-12 traceability

This file describes the implemented finite profile, not a claim of general K2
execution. `reference.py`, `coding_plugin.py`, and `__init__.py` never receive
a fixture tag or assertion-map value. `fixtures.py` constructs the 102 input
universes and separately declares the literal assertion base plus closed-family
expansions that produce 102 assertion-only projections. Each
projection freezes its authoritative identity tuple, conflict coordinate, and
semantic outcome without reading a constructed universe, manifest, request,
evidence value, result value, or replay.

## Thirteen executable checks

| check | production branch | literal constructor | test method and independent falsifier | governing clause | result / failure |
|---:|---|---|---|---|---|
| 1 | `admit_typed_value`, `admitted_closed_value`, `compose_records`, `validate_packages`, `_validate_retained_ck_exact`, `required_subject`, `contract_dependencies`, `formula_dependencies`, `reasoning_target_roots`, `validate_profile_binding`, `evaluate_invocation`, `observe`, `verification_passed`, `task_accepts` | one literal `PKG_CK`: exact 55 `DELTA_TYPE_X`, 47 `DELTA_LITERAL_X`, 17 `DELTA_SYMBOL_X`, ordinary/pair/profile Sigma records, all model contracts, six field-complete capabilities, exact `BENV/BCERT`, and field-sensitive admission relations; `ContractSubject` contains the complete finite Contract value and `FormulaSubject` contains an exact formula finset plus `LexicalScopeIdentity` | `test_k3x_01_core_definitional_and_closed_coding_values`; independently freezes literal target roots, rejects bare strings, changed exact symbol owner, unresolved typed symbol root, altered lexical scope, a substituted non-semantic carrier, and a lexical target with one formula omitted, while retaining all Repair-10 field/admission falsifiers | K1 §§2.1–2.3; K2 §§2.4, 3.2–3.3, 4.1–4.3, 5.1–5.2; K3-S §§2.1–2.2, 3.2, 4.1, 6.2, 8.2, 9.1, 9.6 check 1 | exact `TRUE`; `required_subject` is structural and extensional over the contained Contract/formulas, never subject identity/local-name dispatch; descriptor roots remain typed and exact changes cannot alias canonical roots |
| 2 | exact `RecordIdentity(kind,key)`, `_record_shape`, `compose_records` | independently equal declarations, kind/owner-distinct identities, unequal same-identity declaration | `test_k3x_02_exact_identity_equal_coalescence_and_conflict`; supplies a wrong value constructor for a declaration identity | K2 §§1.1, 3.1, 8.3; K3-S §§4.3, 9.5–9.6 check 2 | equal coalesces; distinct kind/owner remains distinct; unequal same identity gives one order-independent conflict; wrong record shape raises |
| 3 | `exact_version_agreement`, `validate_model_descriptor`, `dependency_reachability`, `_record_for_dependency`, `_dependency_associations`, `validate_packages`, resolved-ContractSpec dispatch | core model, descriptor, service, fragments, package, ABI, typed target, target-root, dependency-scope, and trust-root identities; all descriptor scope/proper/closure fields are exact `DependencyKey` sets | `test_k3x_03_exact_versions_and_complete_descriptor_validation`; mutates requested/model version, ABI, plugin, judgment, typed target, fragment role, exact typed proper dependency, closure, validation/proper separation, trust-root kind, summary, and relation name | K2 §§3.3–3.4, 4.3, 8.2; K3-S §§4.3, 6, 9.6 check 3 | exact version and known resolved relation only; no descriptor root is downcast to `RecordIdentity`; declaration roots resolve type or ordinary declarations, symbol roots resolve their unique declaration/binding association, and unresolved or wrong-kind roots reject |
| 4 | `_environment`, `validate_binding`, `evaluate_invocation` | reconstructed core package plus reconstructed `SemanticEnvironment` and `DependencyEnvironment` | `test_k3x_04_declaration_binding_and_capability_are_derived`; deletes declaration, binding, capability/model summary, and supplies an empty environment | K2 §§2.4, 3.3, 8.1; K3-S §§4.2–4.4, 9.4, 9.6 check 4 | declaration absence is malformed; binding absence is open; capability absence is evaluability-missing; empty carrier cannot retain the answer |
| 5 | `_proper_graph`, `topological_order`, `_producer_set`, `validate_pair`, `_validate_retained_ck_exact` | accepted pair packet unchanged; cycle removes all six service descriptors and `BENV`, replaces the retained `event_matches` meaning, matching access boundary, and binding, and rebuilds all eleven ordinary model records with empty capability summaries while leaving the `event_occurred` binding byte/value-identical | `test_k3x_05_pair_producers_validation_refs_and_proper_cycle`; preserves all pair falsifiers, proves baseline acyclicity, asserts the complete frozen removed/added/changed identity sets, exact values of all rebuilt models, unchanged `event_occurred`, and equality of every unrelated retained record | K2 §§3.3, 5.1–5.2, 6.4–6.5, 7.2; K3-S §§3, 9.2, 9.5–9.6 check 5 | accepted pair result is preserved; access support remains equal to its rewritten meaning support, every model projection that referenced a removed descriptor is rebuilt, and replacement reachability yields `MALFORMED(dependency cycle)` |
| 6 | `_trust`, `evaluate_invocation` | five separately constructed `Q_t[T_x]` universes with policy/root/environment records | `test_k3x_06_five_trust_lifecycle_and_discovery_branches`; removes root and trust-environment records | K2 §§2.3–2.4, 5.4, 8.1; K3-S §§9.3, 9.6 check 6 | admitted/available; absent/missing; undecided/unknown; incompatible/missing; discovery failure/unknown; no fabricated result |
| 7 | `_conjoin`, `project_interface_failure`, `_coding_projection`, `implementation_evidence_profile` | exact task, verification, implementation-profile evidence and abstract-result values, separate from the `task_accepts` predicate binding | `test_k3x_07_false_unknown_errors_malformed_and_profile_projection`; malformed `Eval`, wrong task result, contract, snapshot, schema, pending dimension, concrete-profile error, and reasoning-result subtests | K1 §§4, 5.3; K2 §§5.2–5.4, 6.3; K3-S §§2.2, 4.1, 9.6 check 7 | false, logical unknown, evaluation error, reasoning-interface error, malformed carrier, and exact two-dimension profile complete/incomplete/unknown remain distinct |
| 8 | `changes_between`, `dependency_metadata_changed`, `event_matches`, `event_occurred`, `refresh_scope` | closed event payload/pattern types and exact created/deleted/modified records | `test_k3x_08_trace_truth_event_admission_and_change_metadata`; false pattern, duplicate-field tuple, wrong payload tag, and non-lock refresh | K1 §§3.2–3.4; K2 §7.1; K3-S §§2.1–2.2, 9.6 check 8 | trace truth is exact and does not imply authority; malformed event construction rejects; change metadata is exact |
| 9 | `K1SyntaxKey`, `DependencyKey`, `lift_syntax_key`, `derive_dependency_environment`, `dependency_reachability`, `validate_contract_spec`, `validate_binding`, `validate_model_descriptor`, `evaluate_observation_graph`, `frozen_confluence_syntax_roots` | shared retained package; `E_c` contains the exact retained callable/literal/authority records and the 27 exact K1 plugin/symbol/declaration roots obtained from the two formula trees; `D_c` contains independently recomputed typed roots, associations, expanded roots, proper targets, and least closure | `test_k3x_09_confluence_contractspec_graph_errors_and_permutations`; independently reconstructs all seven `D_c` fields, rejects invalid `K1_FORMULA`, a raw `RecordIdentity` mixed into expanded roots, a coherent extra valid syntax root, and all retained Repair-10 graph/environment falsifiers | K1 §§2.1–2.3; K2 §§1.1, 2.3, 3.3, 6.1–6.5, 7.5, 8.3; K3-S §§4.2, 6.2–6.3, 9.5–9.6 check 9 | both orders yield the identical complete exact map/result/status; typed syntax roots traverse exact symbol-to-declaration/binding associations and declaration/type dependencies without lossy identity conversion |
| 10 | `compose_records` conflict construction | `duplicate_universe` with ABI/package, the literal 24 type declarations, 24 Delta admissions, three-argument `d/d'/d_bad`, and forward/reverse sequences | `test_k3x_10_duplicate_equal_and_conflict_are_order_independent` | K2 §§1.1, 8.3; K3-S §9.5 and check 10 | equal duplicate coalesces; unequal duplicate produces the same two-record conflict in either order |
| 11 | replay `LookupRequest`, `ResolutionCoordinate`, `_resolve_failed_coordinate`; `_frozen_task_environment_value`, `_frozen_task_values`, `frozen_task_syntax_roots`, `derive_dependency_environment`; typed migration/compatibility/extension/alias and envelope validation | 42 literal rows plus distinct evolution chains; exact `E_t` and the 26 exact K1 plugin/symbol/declaration roots of `required(S_t)`; typed `D_t` fields are recomputed from the predicate subject and exact universe | `test_k3x_11_all_42_literal_missing_reconstructions`; independently reconstructs all seven `D_t` fields and retains every Repair-10 environment, evolution, envelope, producer, and dangling-dependency falsifier | K1 §§2.1–2.3; K2 §§2.3, 3.3, 6.4–6.5, 8.2; K3-S §§8, 9.3–9.4 and check 11 | source and target roots equal exact frozen `E_t`; `D_t` uses only typed K1/Dependency keys, exact associations/proper closure, and empty validation references; all 42 families retain their accepted statuses |
| 12 | public `replay(Universe)` followed only by an assertion-side representation projection | `_build_fixture_packet`: 1 core + 1 pair + 5 trust + 42 bases + 42 variants + 2 confluence + 1 cycle + 4 permutations + 2 equal + 2 conflict; a literal assertion base plus independently declared closed-family expansions freezes all 102 projections | `test_k3x_12_all_102_replays_without_identifier_or_assertion_input`; independently replays every universe, recursively rejects nested `FixtureId`, then proves extra-record, changed-evidence, and changed-`ResultRecord` mutations diverge from the unchanged assertion | K1 §4.8; K2 §§1.1, 3.3, 5.2; K3-S §§9.1, 9.6 check 12 | domains equal and cardinality 102; 42/42 rows; all exact projections equal; evaluator receives no tag or assertion value; each independent mutation breaks equality |
| 13 | `enforce_declared_access`, `invoke_with_declared_access` | finite requested/allowed facet sets | `test_k3x_13_declared_access_and_static_oracle_exclusions`; requests repository, evidence, and hidden-assertion facets independently | K1 §§1.2, 2.2, 3.1; K2 §§3.3, 4.2, 5.1; K3-S §§4.2, 9.6 check 13 | undeclared access raises before a truth result; declared final-only access succeeds |

## Conditional coverage map

The following groups cover every semantic conditional. Representation-only
constructor arity/tag checks are exercised in the row above that owns the
value and fail by `ValueError` before evaluation.

- Coding admission and observation: check 1 covers selector domain, missing
  paths, wrong roles, body/projection mismatch, direct observation, exact
  result tag/domain/coverage, and decisive verification conflict. Check 8
  covers every retained event payload/pattern family plus change kinds.
- Criteria: checks 1 and 7 cover observation equality, nonempty population,
  verification success/missing/conflict, conjunction dominance, and malformed
  `Eval`. The finite implementations of format, size, universal observation,
  lane reproducibility, and adapter correspondence reject empty/incomplete,
  conflicting, or wrong-tag observations through the same typed helpers.
- Evidence/profile: checks 1 and 7 cover schema/reference projection,
  snapshot-bound direct observation, PASS/FAIL/INCONCLUSIVE-or-missing,
  duplicate conflict, exact two-dimension witnesses, pending unknown, exact
  incomplete, wrong contract/snapshot/schema, task-result mismatch, and the
  separate interface failure domains.
- Composition/records: checks 2, 9, 10, and 11 cover complete-kind admission,
  recursive package expansion, equal/unequal identity grouping, package
  owner/category/member/ABI/plugin validation, permutations, and required
  structural consumer-coordinate resolution and exact manifest differences.
- Assertion independence: check 12 compares only after public replay against a
  separately declared literal base and closed-family expansions. Its AST guard excludes manifest,
  construction, evidence, result, replay, composition, and validation reads
  from the assertion builder; three independent mutations demonstrate that
  the table does not move with fixture or result changes.
- Invocation: checks 1, 3, 4, and 6 cover environment identity and closure,
  declaration, binding, model, summary/descriptor, exact version, service,
  fragments, target, dependency/validation/trust projections, all five trust
  branches, argument arity, and direct invocation.
- Dependency/pair: checks 5 and 9 cover missing/wrong binding identities, query-derived
  edges, deterministic ready-node selection, cycles, exact two non-proper
  validation references, certificate subject/judgment, complete producer sets,
  and pair/trust/certificate/validator producer independence.
- Missing/lifecycle: check 11 iterates all 42 literal specifications. Optional versus
  required extension/alias behavior comes from the exact typed migration,
  compatibility, semantic-extension, and alias records; Sigma versus Service ContractSpec behavior comes from
  the binding versus descriptor referrer; lexical excess comes from the
  rebuilt environment; conflict/lifecycle results come from their replacement
  records. No caller-supplied status exists.

## Intentionally unimplemented

The implementation fails loudly outside these finite constructors. It does
not implement:

- any K1/K2 declaration, binding, ContractSpec role, model, descriptor,
  service, trust, certificate, authority, evolution, observation, evidence,
  event, profile, or request constructor not instantiated by the packet and
  adversarial subtests;
- general cross-plugin joint reasoning, public relation services, arbitrary
  dependency graphs, arbitrary executable relations, proof checking, or
  discovery beyond the five closed trust projections;
- authority admission beyond the six frozen fixture attestations (only the two
  confluence bindings are evaluated as a graph), evolution beyond the four
  missing-matrix requirement families, certificate judgments beyond the core
  bounds envelope, evolution chains, and independent pair case, or profiles
  beyond the retained implementation-evidence coordinate;
- serialization/loading, natural-language parsing, source binding, prompting,
  model inference/training, planning, search, patch generation, benchmark
  evaluation, or a general Contract IR;
- filesystem/repository mutation, command/process execution, environment,
  network/service/database access, clock, randomness, concurrency, retry,
  deployment, external artifacts, held-out content, or downstream/K4 work.

Passing this suite establishes only executable consistency for this finite
102-entry K2/K3-S slice.
