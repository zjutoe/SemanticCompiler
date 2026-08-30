# K3-S semantic repair 6 review

- Verdict: `REJECT`
- Bound base commit: `f6584fceb76414756693c603fdf88b7a87a91679`
- Reviewed commit: `96fedafd850a6f9c00bb10cbcaeba25562089d0d`
- Reviewed range: `f6584fceb76414756693c603fdf88b7a87a91679..96fedafd850a6f9c00bb10cbcaeba25562089d0d`
- Reviewed path: `KernelPlugin/K3_S_Minimal_Coding_Plugin_Semantics_v0.md`
- Reviewed blob: `6dc9f5274f3badf05df8351d859cc12d3865a05a`
- Reviewed size: 5,170 lines, 319,219 bytes
- Review mode: independent strict read-only scientific review

## Decision

The sixth repair closes the stale model projections in the four reported
predicate package variants and makes the two unequal predicate declarations
field-conformant. A complete reread nevertheless found four further finite
fixture defects: the independent pair package retains unsupported model
capability summaries, conflict carriers are not exactly constructed, reverse
duplicate presentations apply sequence operations to finsets, and the packet
does not contain the required genuine semantic-cycle rejection fixture. These
are bounded K3-S defects; accepted K1 and K2 remain unchanged.

## Blocking findings

1. `MODEL_refresh_scope` and `MODEL_refresh_occurred` retain summaries for
   `CAP(predicates)` inside `Sigma_p` and `PKG_pair_CK`, while the pair-only
   package has no services and `U_PAIR_INDEPENDENT` supplies no predicate
   descriptor. K2 model/descriptor conformance is bidirectional, so this
   packet entry is model/machine malformed instead of the claimed
   `WELL_FORMED,CLOSED`. Repair must use pair-context copies of both models
   with empty capability summaries throughout `Sigma_p`, `PKG_pair_CK`, and
   every derived pair variant.

2. `conflict0=CONFLICT_OF(d,d_bad)` and its alternate use an undefined
   constructor. Because all involved declaration records have the same
   `RecordIdentity`, their involved-identity sets alone do not distinguish the
   two conflicts. K2 requires an exact `ConflictRef` kind and involved-identity
   set. Repair must define a typed, order-independent conflict-kind algebra
   that includes the exact mismatching field coordinate and unordered unequal
   values, construct both complete conflict records, and recompute all
   authoritative maps and the CONFLICT missing row.

3. `DUPLICATE_TYPE_DECLARATIONS` and `DUPLICATE_TYPE_ADMISSIONS` are finsets,
   but the fixture concatenates them with `++` and reverses the result without
   defining an enumeration. Thus the supposed forward/reverse inputs are not
   exact sequences. Repair must define literal ordered declaration and
   admission sequences, derive the package finsets from those sequences, and
   use only typed sequences for composition and reversal.

4. The packet has no exact genuine semantic-cycle rejection entry. Prose says
   that adding both edges is malformed, but supplies no complete rebuilt
   cyclic records, universe, tag, or expected replay value. Amendment check 5
   requires executable rejection of a genuine semantic cycle. Repair must add
   one exact tagged cyclic universe and expected `MALFORMED` replay result;
   existing `K3S-A15` coverage may be reused without adding a case or trace.

## Verified closure and coverage

The SERVICE and CAPABILITY variants now rebuild all eight predicate summaries
to empty; SERVICE_CONTRACT_SPEC rebuilds the summaries from its replacement
descriptor; SIGMA_CONTRACT_SPEC updates the task model semantic reference;
and `d_bad`/`d_bad_alt` are complete three-argument declarations. The
declaration-only duplicate package may omit `d` while supplying it standalone:
K2 requires owner-package presence and exact dependency closure, not exhaustive
owner membership. Its type-admission records and recursive type closure are
otherwise valid.

The exact structure remains ten ordered sections, 19 K0 rows, 18 adversarial
cases, eight traces, 13 mappings, 42 missing rows, 65 ledger rows split
`24/13/15/8/5`, 52 separation rows, 176 balanced fence markers, and a final
newline. Trust-state/status separation, ambient-access prohibition, authority
independence, and earlier repaired missing-row behavior show no additional
regression.

## Status

K3-S remains unaccepted. A bounded seventh repair may change only the K3-S
deliverable, must close all four findings while preserving accepted K1/K2 and
required cardinalities, and must receive another frozen-commit independent
review. K3-X remains undispatched; this record grants no handoff,
implementation, or execution authority.
