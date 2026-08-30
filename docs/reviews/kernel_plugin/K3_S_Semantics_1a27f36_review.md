# K3-S semantic repair 2 review

- Verdict: `REJECT`
- Reviewed repair range: `7a09eb7f35fcec7f1cac5d04e2cf2c91d1e80ee8..1a27f36acf1240e8a1dbb159aa26f2a49cbdff41`
- Repaired path: `KernelPlugin/K3_S_Minimal_Coding_Plugin_Semantics_v0.md`
- Repaired blob: `0756510d90818337286a017188622432524a0112`
- Repaired size: 3,136 lines / 207,899 bytes
- Prior rejection blobs: `f2d92830685cb4acb8071fd1bb16cc519af00fd7`, `6e013d31c5554490459575a84d73cd8d54fdbcdf`
- Accepted handoff blob: `f3019df041df07da1bfef6f92858bacdc7f4ab9d`
- Accepted K2 blob: `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`
- Review mode: fresh independent strict read-only milestone-end semantic audit

## Decision

Repair 2 is rejected. It closes the direct-task, typed observation/evidence,
snapshot-binding, profile, dependency-role, trust-state, observation-wrapper,
lifecycle, and authority-record-expansion defects. The remaining failures are
exact K2 record/field construction errors, not K1/K2 design gaps.

## Blocking findings

1. `MC(...)` is a `ModelContractKey`, but several finite universes contain
   those bare keys where K2 requires complete `ModelContract` records. The
   supposedly complete packet also omits `PluginPackage(ABI0,CK)` and complete
   packages for retained service/certificate owners. Therefore model/package
   closure and the corresponding missing tests do not start from valid input.
2. Several Service `ContractSpec`s do not provide literal legal per-key query
   maps. Whole target/pair closures include K2-forbidden `MODEL_CONTRACT` and
   `CONTRACT_SPEC` observation keys. Pair relations consume a semantic bundle,
   while evolution relations consume `SemanticEnvironment` or `AliasBinding`;
   these are forbidden primary-input values. Replace them with legal finite
   typed admission-subject values and exact projections, then recompute all
   enclosing records.
3. The missing matrix references choice and authority baselines that are not
   members of `FIXTURE_X/PACKET_X`; its extraneous lexical branch remains a
   prose modification rather than a named complete environment/request.
   Enumerate one complete baseline and one complete modified variant for every
   removal branch.
4. Final producer sets omit the already admitted authority chain
   (`AVK`/`ATP`) reachable through authority fact bindings. The evolution set
   also omits `ABI_PRODUCER(ABI0)`. Recompute mechanically and state the exact
   same sets in constructions, traces, requests, and independence checks.

Ledger repair is also required: use K2 `PairValidationResult`, not the
nonexistent `PairAdmissionResult`, and state exactly two pair validation
references rather than three.

## Verified properties

The reviewer confirmed clean exact lineage, a one-path diff, exact blobs and
size, final newline, and `git diff --check`. Mechanical structure remains
valid: ten sections, 19 K0 rows, 18 cases, eight traces, 13 K3-X mappings, 65
ten-cell ledger rows split `24/13/15/8/5`, 52 syntactically bijective
separator labels, and 138 balanced fences. Every governing input and final
line was read; no held-out content was accessed beyond opaque receipt
`K1-HO-GATE-20260828-A`.

## Repair boundary

Repair 3 remains limited to the K3-S deliverable. It must replace bare keys and
prose closures with literal complete records, use only legal K2 ContractSpec
inputs/query keys, supply exact package and missing-test baselines, recompute
producer sets, preserve all required cardinalities, and receive another
frozen-commit independent review. K3-X remains undispatched.
