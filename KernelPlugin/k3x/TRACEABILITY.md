# K3-X finite-slice traceability

This package implements only the 102 self-contained universes enumerated by
accepted K3-S §9.1. `FIXTURE_PACKET_X` is semantic input; the disjoint
`FIXTURE_EXPECTED_X` map is test-only assertion data. `replay` receives only a
`Universe`, never an identifier or assertion value.

## Thirteen required checks

| check | production functions | constructors | exact test method | accepted basis | expected result and implemented failure branch |
|---:|---|---|---|---|---|
| 1 | `snapshot_of`, `observe`, `verification_passed`, `task_accepts`, `validate_contract_spec`, `evaluate_contract`, `replay` | `_core_universe` | `test_k3x_01_closed_evaluable_coding_contract_true` | K2 §§2.4, 4.1–4.2, 5.1–5.2; K3-S §§2.1–2.2, 4.1–4.3, 9.1, 9.6 (`CORE_DEFINITIONAL`) | entry-local authoritative composition, `WELL_FORMED`, `CLOSED`, `EVALUABILITY_AVAILABLE`, `COMPLETED`, exact `Eval(TRUE)`; invalid value/schema/access or incomplete ContractSpec yields typed term/evaluation error or `MALFORMED` before truth |
| 2 | `compose_records` | `_record`, `_core_universe`, `_duplicate_universe` | `test_k3x_02_structural_identity_and_kind_collision` | K2 §§3.1, 8.3; K3-S §§3.1, 4.4, 8 (`K3S-A01`, `K3S-A14`), 9.5–9.6 | independently equal records coalesce, exact owner/plugin/kind variants remain distinct; unequal complete records at one identity yield one order-independent `ConflictRef`, never last-writer selection |
| 3 | `exact_version_agreement`, `validate_model_descriptor`, `evaluate_contract` | `_core_universe` | `test_k3x_03_exact_version_and_model_agreement_no_fallback` | K2 §§3.4, 4.3, 8.2; K3-S §§3.1, 4.3–4.4, 8 (`K3S-A02`, `K3S-A16`), 9.6 | exact `(1)=(1)` succeeds; `(1)!=(2)`, model/target version mismatch, summary/descriptor mismatch, or owner mismatch is `MALFORMED` with no selection or fallback |
| 4 | `evaluate_contract` | `_core_universe` | `test_k3x_04_declaration_binding_and_capability_are_independent` | K2 §§2.4, 8.1; K3-S §§4.2–4.3, 8 (`K3S-A03`, `K3S-A09`), 9.6 | absent declaration is malformed; absent binding is `OPEN_BINDINGS`; absent capability remains closed and is `EVALUABILITY_MISSING` |
| 5 | `topological_order`, `validate_dependency_graph`, `validate_pair`, `replay` | `_pair_universe`, `_cycle_universe` | `test_k3x_05_pair_validation_refs_independence_and_cycle` | K2 §§3.3, 7.2; K3-S §§3.4, 6.2–6.3, 8 (`K3S-A15`), 9.2, 9.5–9.6 | exact two non-proper validation references and four mutually independent producer roles admit the exact `PairValidationResult`; absent/extra refs, validation in the proper DAG, incomplete/equal producer roles, or a mechanical proper cycle yields `MALFORMED` |
| 6 | `project_trust`, `replay` | `_trust_universe` | `test_k3x_06_five_trust_states_remain_distinct` | K2 §§2.3–2.4, 5.4, 8.1; K3-S §§6.2–6.3, 8 (`K3S-A03`, `K3S-A13`), 9.3, 9.6 | admitted gives the sole invocable result; absent/incompatible give exact missing; undecided gives `EVALUABILITY_UNKNOWN`; failed gives `DISCOVERY_FAILED`; every non-admitted branch has no fabricated K1 result |
| 7 | `task_accepts`, `verification_passed`, `implementation_evidence_profile`, `project_interface_failure` | `_core_universe` plus local typed counterexamples | `test_k3x_07_false_unknown_and_failure_families_do_not_collapse` | K2 §§5.2–5.4, 6.3; K3-S §§2.1–2.2, 4.1, 6.1–6.3, 8 (`K3S-A10`, `K3S-A11`), 9.6 | `FALSE`, logical `UNKNOWN`, evaluation error, reasoning error, and malformed result are unequal typed outcomes; empty failure reasons are malformed and domain-specific failures never become truth |
| 8 | `event_matches`, `event_occurred`, `refresh_scope`, `dependency_metadata_changed` | local admitted event/change values | `test_k3x_08_trace_truth_and_authority_are_independent` | K2 §7.1; K3-S §§2.1–2.2, 5.1–5.3, 8 (`K3S-A06`, `K3S-A07`), 9.6 | exact forbidden/authorized event matches and refresh/change facts are logical truth only; authority remains a distinct judgment and evaluability never grants it; unsupported pattern tags reject explicitly |
| 9 | `topological_order`, `evaluate_observation_graph`, `compose_records`, `replay` | `_confluence_universe`, `_permutation_universe` | `test_k3x_09_confluence_and_all_four_permutations` | K2 §§1.1, 3.3, 7.5, 8.3; K3-S §§4.1–4.2, 8 (`K3S-A09`, `K3S-A14`, `K3S-A15`), 9.5–9.6 | both valid node orders yield the identical complete observation map, inconclusive result, lifecycle, and five-status tuple; all two-by-two package/record presentations yield identical composition; missing/duplicate graph nodes reject |
| 10 | `compose_records`, `replay` | `_duplicate_universe` | `test_k3x_10_equal_duplicates_and_conflicts_are_order_independent` | K2 §§1.1, 8.3; K3-S §§4.4, 8 (`K3S-A14`), 9.5–9.6 | equal forward/reverse duplicates coalesce; unequal forward/reverse duplicates yield the identical exact conflict with `MALFORMED`/`NOT_APPLICABLE` |
| 11 | `record_at`, `missing_status`, `replay` | `_missing_row` for every `MissingKind` | `test_k3x_11_all_42_missing_baselines_and_variants` | K2 §§2.4, 3.3; K3-S §§4.4, 6.3, 8 (`K3S-A03`, `K3S-A15`, `K3S-A16`), exhaustive §9.4 and §9.6 | all 42 baselines have authoritative count one and `PRESENT`; all 42 reconstructed variants have count zero and the exact malformed/open/evaluability/trust/no-admission/protocol family; lexical, lifecycle, and conflict replacements are literal records, not prose additions |
| 12 | `replay`, all production functions reached by typed requests | `_build_packet` and every constructor above | `test_k3x_12_every_tagged_universe_replays_independently` | K2 §§1.1, 3.3, 5.2; K3-S §§9.1–9.6 (`FIXTURE_PACKET_X`, `FIXTURE_EXPECTED_X`) | exact equal domains of cardinality 102 and exact independent replay equality; package/conflict malformation is returned before request evaluation, and unsupported request types raise `FiniteProfileError` |
| 13 | `enforce_declared_access`, `invoke_with_declared_access` | local pure meaning and three undeclared facet sets | `test_k3x_13_undeclared_ambient_access_precedes_truth` | K2 §§3.3, 4.2, 5.1; K3-S §§1.2, 2.2, 4.1, 8 (`K3S-A05`, `K3S-A09`, `K3S-A17`), 9.6 | repository, undeclared evidence, and hidden assertion access each raises `UndeclaredAccessError` before the meaning can run or a truth can be consumed |

## Conditional-to-check index

Every semantic conditional in the production modules is covered by at least
one row above:

- `snapshot_of`, `changes_between`, `_selected`, `observe`,
  `observations_equal`, `_criterion_result`, `task_accepts`: checks 1, 7, and
  9 (value admission, change/selection/projection, equality, and all eight
  criterion branches);
- `_evidence_map`, `verification_passed`, `_conjoin`,
  `implementation_evidence_profile`: checks 1 and 7 (schema/reference/current
  snapshot selection, duplicate conflict, decisive/unknown aggregation, task
  dominance, and both profile dimensions);
- `dependency_metadata_changed`, `event_matches`, `event_occurred`,
  `refresh_scope`: check 8 (both metadata roles, all seven pattern tags, trace
  aggregation, and exact refresh classification);
- `enforce_declared_access`, `invoke_with_declared_access`: check 13 (access
  rejection precedes callable validation and invocation);
- `admit_typed_value`, `validate_declaration_shape`, `validate_binding`,
  `exact_version_agreement`, `validate_packages`, `validate_contract_spec`,
  `validate_model_descriptor`, `evaluate_contract`: checks 1–4 and 12 (exact
  type/tag, declaration facets/dependencies, binding closure, version,
  ownership/member, query/support/role, summary, and lifecycle branches);
- `compose_records`, `topological_order`, `validate_dependency_graph`,
  `evaluate_observation_graph`: checks 2, 5, 9, and 10 (coalescence/conflict,
  readiness/cycle, node-domain/kind dispatch, and complete maps);
- `project_trust`, `project_interface_failure`, `validate_pair`: checks 5–7
  (five trust states, empty-reason malformation, four failure domains, exact
  refs, graph separation, and producer independence);
- `missing_status`, `record_at`, `replay`: checks 11–12 (all 42 absence
  coordinates, present/conflicting lookup, package-first rejection, and every
  typed request dispatch branch).

Dataclass field checks, exact tuple/map conversions, enum construction, and
stable sorting are representation checks and make no additional semantic
claim.

## Intentionally unimplemented branches

The following is the exhaustive exclusion boundary for this spike. Each item
raises `FiniteProfileError`/`FiniteCodingProfileError` when it reaches a public
finite-profile operation, or has no constructor/export in this package:

- every literal, target, request, capability, ContractSpec role, observation
  projection, criterion relation, event pattern, and result not enumerated by
  the accepted packet;
- general cross-plugin joint reasoning and public relation services;
- evolution records beyond the accepted `m`, `c`, `x0`, and `x1` admission
  coordinates, including any additional migration, compatibility, alias, or
  extension meaning;
- authority facts beyond the six accepted authority fixtures, and certificate
  kinds/targets beyond the pair, authority, evolution, bounds, and witness
  records enumerated by K3-S;
- constructors and K2 branches not required by the thirteen checks, including
  a general Contract IR, serializer, loader, discovery transport, proof system,
  or arbitrary extensional-relation evaluator;
- natural-language parsing or source binding, prompting, model inference or
  training, planning, search, patch generation, benchmark evaluation, and
  golden/hidden answer handling;
- byte serialization, real repository or filesystem state, real commands or
  processes, environment access, network/service/database activity, clocks,
  randomness, concurrency, retries, deployment, mutation, or scheduling;
- cross-entry union/catalog replay, implicit package-member closure,
  first/last/newest/compatible-looking selection, version fallback, and
  concurrent mutable or cached state;
- K4 work, held-out content, external artifacts, execution evidence, and any
  downstream handoff or authority.

These omissions are profile boundaries, not semantic rejections of K1, K2, or
K3-S. Passing diagnostics establishes only executable reproducibility of the
enumerated finite slice.
