# K3-S semantic repair 1 review

- Verdict: `REJECT`
- Reviewed repair range: `9a89ebd9b868a496a8b75436b3de0415bade2c77..4b3d2f717d0c6b71028903d1a2bd23e166e6f048`
- Repaired deliverable: `KernelPlugin/K3_S_Minimal_Coding_Plugin_Semantics_v0.md`
- Repaired blob: `4676b21d17dfb9fa8995dd4c37e5649866cbc726`
- Repaired size: 2,046 lines / 148,088 bytes
- Initial rejection record blob: `f2d92830685cb4acb8071fd1bb16cc519af00fd7`
- Accepted handoff blob: `f3019df041df07da1bfef6f92858bacdc7f4ab9d`
- Accepted K2 blob: `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`
- Review mode: fresh independent strict read-only milestone-end semantic audit

## Decision

Repair 1 is rejected. It correctly made `task_accepts` direct and
snapshot-bound verification constructible, substantially completed the value
algebra, and introduced explicit reasoning certificate records. Several exact
fixtures and extensional relations remain nonconstructible or nondeterminate.
No K1 or K2 repair is required.

## Confirmed closed prior finding

The verification predicate now receives the current supplied repository
snapshot, selects only records with its exact snapshot identity, and carries
that change through its declaration, facets, access contract, binding, model,
capability, traces, and fixtures.

## Blocking repair findings

1. The confluence observation map contains bare `TermResult` values instead of
   K2 `TERM_OBS(TermResult)` values, and its final lifecycle vector contains
   both `INVOCABLE_FOR` and `COMPLETED` even though invocation state is
   disjoint and completion replaces invocability.
2. Observation remains nondeterminate: behavior views have no merge/conflict
   rule across artifacts; metric requests do not select a metric-keyed value;
   per-view allowed value constructors are incomplete; combined path/role
   selection has no total equation; and `EvidenceStore` has no exact finite
   record/reference projection.
3. `C_b`, `C_c`, and `C_w` refer to admitted authority adoption without
   enumerating the producer-independent K2 authority attestation,
   certificate, validator, trust, reception, and `AuthorityFactBinding`
   records needed for closed reasoning subjects.
4. The ledger omits supplied requests and pair-proof payload/reference fields,
   while cited adversarial subvariants are labels rather than complete finite
   separating fixtures.
5. The K3-X missing fixture uses a plugin value as a nonexistent K2 carrier,
   has no genuine free-variable lexical request, supplies only bare
   migration/compatibility/extension/alias keys, and leaves several request,
   result, environment, lifecycle, package, and ordering records as prose
   placeholders. Its named package families are not finite enumerated record
   sequences.
6. Profile coverage does not define exact evidence predicates for the two
   dimensions or total complete/omitted/unknown/error behavior.
7. `dependency_metadata_changed` does not specify the role equation for
   `CREATED`, `DELETED`, and both sides of `MODIFIED`.

The token `NETWORK_ANY` also needs the notation-only correction to the defined
`NET_ANY` macro.

## Verified properties

The reviewer confirmed exact lineage, one-path diff, blobs, size, clean
worktree, final newline, and `git diff --check`. Mechanical counts are valid:
ten ordered sections, 19 K0 rows, 18 adversarial cases, eight traces, 13 K3-X
mappings, 52 ledger rows split `23/10/8/6/5`, ten cells per ledger row, and 74
balanced fences. Every governing input and repaired line was read; no held-out
content was accessed beyond opaque receipt `K1-HO-GATE-20260828-A`.

## Repair boundary

Repair 2 remains limited to the K3-S deliverable under the accepted handoff.
It must use only exact K2 record kinds, make every retained extensional
relation total, enumerate every K3-X fixture as finite constructor-complete
records, preserve the required section/challenge/case/trace/check counts, and
receive another frozen-commit independent review. K3-X remains undispatched.
