# K3-S semantic candidate review

- Verdict: `REJECT`
- Reviewed range: `2790f9dfca3c178e162b7ce2d1db2ebf000f8f56..5e1e473a6af321d688a2b8b7fb59445f669fb770`
- Candidate path: `KernelPlugin/K3_S_Minimal_Coding_Plugin_Semantics_v0.md`
- Candidate blob: `dc63e48e7d72b5f004cd9dd44a75eafe75c1f52f`
- Candidate size: 1,199 lines / 96,699 bytes
- Accepted handoff blob: `f3019df041df07da1bfef6f92858bacdc7f4ab9d`
- Accepted K2 blob: `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`
- Review mode: fresh independent strict read-only milestone-end semantic audit

## Decision

The exact candidate is rejected. Its structure and provenance are valid, but
six semantic constructibility gaps prevent K3-S acceptance. None requires a
K1 or K2 repair; the accepted K2 interface already contains the mechanisms
needed for a bounded K3-S repair.

## Blocking findings

1. `task_accepts` declares one lower observation for `observe` and one for
   `verification_passed`, but a general `TaskSpec` may require zero, one, or
   several calls to each lower meaning. The K2 observation map therefore
   cannot represent the stated denotation. Repair it as a direct extensional
   meaning or introduce exact batch operations, and use a separate
   constructible independent DAG for the order-confluence fixture.
2. The coding values do not exhaustively determine size, format, selector,
   observation, or event-pattern judgments. Define complete tagged
   constructors, fields, admission/equality rules, and exact ContractSpec
   projections/relations. Do not reuse `Format` as an unrelated storage-choice
   sort without a separating justification.
3. `verification_passed(VerificationSpec,EvidenceStore)` cannot establish that
   a record belongs to the current final snapshot. Include the supplied
   snapshot or exact snapshot identity and propagate the signature/facet,
   access, binding, model, capability, trace, and fixture changes.
4. The C11 contradiction certificate and C19 witness claim lack a constructible
   producer-independent K2 admission path. Add exact validator, certificate,
   request/result, validation-reference, and trust-scope records, or bind C19
   to a fully specified non-certificate K1 witness route.
5. The claimed exhaustive minimality ledger groups or omits introduced value
   and payload fields and misclassifies supplied validator/certificate records
   as wholly derived. Account for every introduced field or constructor
   exactly once and strengthen the existing 18 separating cases with
   subvariants.
6. The K3-X packet does not freeze complete pair-proof, five-state trust,
   missing-record, or topological-order fixtures. Enumerate complete finite K2
   records, exact reason/scope payloads, producer sets, and expected statuses.

## Verified properties

The reviewer independently confirmed the exact lineage, one-path diff, blob,
size, final newline, clean worktree, and `git diff --check`. It also confirmed
the required mechanical counts: ten ordered top-level sections, 19 K0 rows,
18 adversarial rows, eight traces, 13 K3-X mappings, and a 34-row ledger split
`7/11/6/5/5`. Every governing input and candidate line was read. No held-out
content was accessed; only opaque receipt `K1-HO-GATE-20260828-A` was used.

## Repair boundary

The repair may change only the K3-S deliverable under the already accepted
handoff. It must preserve all exact cardinalities, remain semantic-only, add
no implementation or execution authority, and receive a new frozen-commit
independent review. K3-X remains undispatched.
