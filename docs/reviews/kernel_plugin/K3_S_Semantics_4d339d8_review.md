# K3-S semantic repair 5 review

- Verdict: `REJECT`
- Bound base commit: `31f5e4aae06d00e80399264a7104f90b4d681861`
- Reviewed commit: `4d339d80034357f72f66b2883e847363fb37252f`
- Reviewed range: `31f5e4aae06d00e80399264a7104f90b4d681861..4d339d80034357f72f66b2883e847363fb37252f`
- Reviewed path: `KernelPlugin/K3_S_Minimal_Coding_Plugin_Semantics_v0.md`
- Reviewed blob: `98758f456ec16a09c84a5a927a9caed0af8949f1`
- Reviewed size: 5,024 lines, 310,806 bytes
- Review mode: fresh independent strict read-only scientific review

## Decision

The fifth repair closes the trust-root, evidence-container,
PredicateRequest-field, tiny type-admission, and equal-duplicate defects. It
also removes the predicate capability descriptor from the SERVICE variant,
but does not rebuild every model record that depends on that descriptor. The
unequal duplicate remains independently declaration-malformed. K3-S is
therefore rejected on two local fixture defects; accepted K1 and K2 remain
sufficient and unchanged.

## Blocking findings

1. All eight predicate `ModelContract` records retain the capability summary
   for `CAP(predicates)`, while the SERVICE and CAPABILITY variants remove the
   descriptor that uniquely supports that summary. K2 requires exact
   bidirectional descriptor/summary conformance, so these variants are
   `MALFORMED(model/machine contract mismatch)`, not isolated conformant
   `EVALUABILITY_MISSING` fixtures. The SIGMA_CONTRACT_SPEC and
   SERVICE_CONTRACT_SPEC variants similarly change a binding or descriptor
   without rebuilding model records that project the old record. Repair must
   rebuild every affected model and package variant, eliminate all stale
   nested summaries/projections, and rederive the complete row outcomes.

2. `d_bad` changes the three-argument `DP(task_accepts)` declaration into a
   two-argument declaration but retains all other fields, including the
   three-position facet sequence and signature-derived data. It is malformed
   before duplicate grouping, so the forward and reverse conflict universes
   do not isolate unequal records at one exact identity. Repair must construct
   an independently field-conformant unequal declaration, rebuild its facets
   and every signature-derived dependency, derive a new exact conflict, and
   recompute both order-independent authoritative maps.

These defects violate K2 model/descriptor, declaration-formation, duplicate,
and set-composition rules; K3-S handoff criteria 7, 11, and 12; and amendment
checks 4, 10, 11, and 12.

## Verified repairs and coverage

The empty-map TRUST_ROOT reconstruction now has no same-key root judgment; the
EVIDENCE reconstruction removes `vr0`, `i0`, and `H0` with `e0`; `Q_t_empty`
uses the exact `dependency_environment` field and rebuilt carriers; the tiny
type-admission relation returns abstract `admitted`/`not_admitted`; and the
equal-duplicate presentations use a complete dependency-closed universe.
There is no regression in the initial through repair-3 findings.

The exact structure still has ten ordered sections, 19 K0 rows, 18 adversarial
cases, eight worked traces, 13 check mappings, 42 missing rows, 65 ledger rows
split `24/13/15/8/5`, 52 separation rows, 176 balanced fence markers, and a
final newline. Tagged replay isolation, trust/certificate producer separation,
total admission algebras, identity/version rules, unknown/error separation,
ambient-access prohibition, and limited K1/K2 claims otherwise remain intact.

## Status

K3-S remains unaccepted. A bounded sixth repair may change only the K3-S
semantic deliverable, must close the two findings without changing accepted
K1/K2, preserve all required cardinalities, and receive another frozen-commit
independent review. K3-X remains undispatched; this record grants no handoff,
implementation, or execution authority.
