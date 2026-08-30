# K3-S semantic repair 4 review

- Verdict: `REJECT`
- Bound base commit: `cb870d03be2e3fb6a49fc641634880bc002c1717`
- Reviewed commit: `3cf08e8934d66432c8a1eb285642bd4239efa192`
- Reviewed range: `cb870d03be2e3fb6a49fc641634880bc002c1717..3cf08e8934d66432c8a1eb285642bd4239efa192`
- Reviewed path: `KernelPlugin/K3_S_Minimal_Coding_Plugin_Semantics_v0.md`
- Reviewed blob: `a936a83db2e122274a768da220867497591f270c`
- Reviewed size: 4,976 lines, 308,171 bytes
- Review mode: fresh independent strict read-only scientific review

## Decision

The fourth repair closes the earlier first-order admission-subject and
cross-entry fixture-isolation defects. Its tagged packet, exact key shapes,
package-order presentations, and repeated equal ABI records are compatible
with accepted K2. K3-S is nevertheless rejected because six finite fixtures
do not have the K2 judgments claimed for them. These are local K3-S fixture
defects; the review found no need to change accepted K1 or K2.

## Blocking findings

1. The `SERVICE` missing row removes only
   `ServiceIdentityRecord(SK(predicates))` while retaining
   `CapabilityDescriptor(CAP(predicates))`. K2 uniquely re-derives the same
   service record from that descriptor, so the asserted authoritative count
   transition and absent `recordAt` result do not occur. The repair must remove
   or rebuild every descriptor targeting that service as well as the derived
   carrier.

2. The `TRUST_ROOT` variant replaces the admitted root with
   `TRUST_ROOT_ABSENT(TR)`, which is still a judgment record at the queried
   root. It therefore cannot also satisfy
   `recordAt(...)=ABSENT_REQUIRED_RECORD`. The repair must either remove that
   root entry and all references that require it, or make the row explicitly
   test admitted-to-absent-judgment replacement without claiming record
   absence.

3. The `EVIDENCE` reconstruction removes `e0`, `i0`, and `H0` but leaves the
   complete `vr0` record containing `e0`. This violates the row-local
   reconstruction rule and leaves a stale nested occurrence. The repair must
   remove or rebuild `vr0` and every dependent evidence container.

4. `Q_t_empty` substitutes a nonexistent PredicateRequest field named
   `complete_dependencies`; K2 names that field `dependency_environment`.
   The stale `D_t` therefore remains and the value gains an illegal field, so
   the semantic-environment variant is not a conformant K2 universe. The
   repair must substitute `dependency_environment:=D_t_empty`.

5. The tiny permutation admission contracts use codomain
   `ValueAdmissionResult` and return `VALUE_ADMITTED` or
   `VALUE_NOT_ADMITTED`. K2 requires the declaration admission relation itself
   to return the abstract membership judgments `admitted` or `not_admitted`;
   request/result machinery performs the later wrapper conversion. The repair
   must restore that layer boundary.

6. The duplicate fixtures compose only `ABI0` and copies of the
   `DP(task_accepts)` declaration. They omit its owner package, referenced type
   declarations, admission contracts, and recursive dependency closure.
   Consequently the claimed `WELL_FORMED` equal-duplicate result is false and
   the conflict cases do not isolate duplicate behavior. Each ordering must be
   embedded in one complete dependency-closed universe and its expected record
   map recomputed.

These defects violate amendment checks 9--12 and K3-S handoff acceptance
criteria 11--12.

## Prior findings and verified coverage

The review re-derived all four prior rejection records. The initial candidate's
findings 1--5 are closed; repair-1 findings 1--4 and 6 are closed; all four
repair-2 findings are closed. From repair 3, the admission-subject closure and
cross-entry tagging defects are closed, and exact permutation identities,
packages, dependencies, and orders are present. Row-local missing fixtures and
the permutation's admission semantics remain open as stated above. Repeated
equal `ABI0` inputs correctly coalesce under K2 and are not a defect.

The exact structure still satisfies ten top-level sections, 19 K0 rows, 18
adversarial cases, eight worked traces, 13 K3-X mappings, 42 missing rows, 65
ledger rows split `24/13/15/8/5`, 52 separator rows, 176 balanced fence
markers, and a final newline. The review found no additional blocker in the
ambient-access prohibition, core deterministic meanings, authority/trust
producer independence, or K1 status ownership. The phrase “all six sorts”
after enumerating seven sorts is a nonblocking editorial count error.

## Status

K3-S remains unaccepted. A bounded fifth repair may change only the K3-S
semantic deliverable, must address all six findings, preserve the accepted
K1/K2 boundary and required cardinalities, and receive another frozen-commit
independent review. K3-X remains undispatched; this record grants no
implementation or execution authority.
