# K3-S semantic repair 3 review

- Verdict: `REJECT`
- Reviewed repair range: `92df657a064cf33aa12b234661242e4af285ef8a..4617907d6d8c9da207bbbe232089008822fd9b04`
- Repaired path: `KernelPlugin/K3_S_Minimal_Coding_Plugin_Semantics_v0.md`
- Repaired blob: `92dee65a89c482034022b07db8e67b7a8bb7b290`
- Repaired size: 4,518 lines / 281,193 bytes
- Latest prior rejection blob: `4272fa9addefaf4f7d6a3fb346f6d8f85e971992`
- Accepted handoff blob: `f3019df041df07da1bfef6f92858bacdc7f4ab9d`
- Accepted K2 blob: `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`
- Review mode: fresh independent strict read-only milestone-end semantic audit

## Decision

Repair 3 is rejected. Complete model records, packages, typed Service
ContractSpecs, pair-result typing, validation references, and producer-set
repairs are substantially correct. Four local K3-S fixture/type defects remain;
none requires a K1 or K2 change.

## Blocking findings

1. `ServiceAdmissionSubject` is not closed because pair-domain, compared-field,
   and authority-attestation fields use undefined or prose sorts. Define a
   finite first-order field algebra, or replace redundant fields with fixed
   tags, and propagate only the required declaration/literal/binding/model
   records.
2. The §9.4 missing matrix still performs no-op or stale-copy deletions through
   nested package/environment/request/result records. Some substitutions are
   invalid (`chi_C` not recomputed, nonexistent declaration `exact_version`
   field, `AuthorityFactKey` confused with `AuthorityFactBinding`). Replace the
   shared mega-baseline with one self-contained valid universe per row, one
   authoritative target occurrence, one retained reference, and one exact
   reconstructed variant. Verify symmetric difference and `recordAt` status.
3. `PACKET_X` is a bare union of mutually incompatible same-identity package,
   pair-binding, and conflict variants. Redefine it as a finite tagged map from
   fixture/check identity to one exact conformant universe; alternatives must
   never be composed into one K2 universe.
4. The tiny permutation type keys have the wrong `DeclarationKey` tuple shape
   and the presentations omit `ABI0`. Use exact type keys ending in `TYPE`,
   include the ABI carrier, recompute declaration dependencies, and state the
   exact composition/result for all four permutations.

## Verified properties

The reviewer confirmed exact lineage, one-path diff, blob, size, clean
worktree, final newline, and `git diff --check`. Mechanical structure remains
valid: ten sections, 19 C rows, 18 A rows, eight traces, 13 mappings, 65 ledger
rows split `24/13/15/8/5`, 52 separator labels, 42 missing rows, 50 Delta
ContractSpecs, explicit package records/sequences, 156 balanced fences, exact
producer sets, `PairValidationResult`, and exactly two pair validation
references. Every governing input and final line was read; held-out use stayed
at opaque receipt `K1-HO-GATE-20260828-A` only.

## Repair boundary

Repair 4 is limited to the admission-subject field algebra, tagged fixture
packet partitioning, §9.4 per-row universes, and §9.5 tiny permutations, plus
the directly affected ledger/separators/mappings. Preserve accepted semantics
and all required cardinalities. K3-X remains undispatched and another exact
commit review is mandatory.
