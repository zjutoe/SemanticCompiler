# K3-X Repair-8 implementation review

- Candidate: `40447eeaa463b59a1f2d919564065ad0b918b4ad`
- Parent: `75b76afb0c49f1a9772bcf7fd768a3d691e83929`
- Review: independent, strict, read-only, GPT-5.6 Sol high
- Verdict: **REJECT**; no execution binding

## Blocking findings

1. Retained record values remain inexact: selectors use `PATHS_WITH_ROLE` instead of frozen `SELECT_PATHS`; literal models invent symbols; generic function/predicate ContractSpecs have wrong codomains/support; BENV record/key equality is not enforced; authority references/provenance and nested record kinds are incomplete.
2. Confluence now uses retained binding identities, but `E_c/D_c` omit the two required predicates and derive roots/closure from the reduced candidate environment rather than the frozen contract subject.
3. Cycle preserves `event_occurred`, but after removing descriptors it rebuilds only `MODEL_event_matches`; every affected model projection must lose its capability summary.
4. Evolution validates self-derived environments. `E_t` omits the exact nested type/literal closure and coherent extra members are accepted; `D_t` is not derived from the frozen source/target environment.
5. Assertions project identities/outcomes, so retained descriptor, ContractSpec, authority, and BENV value mutations remain invisible; traceability overclaims field exactness.

Pair and exact pair producers remain accepted. Retained confluence identities and event-occurred preservation are fixed.

Required repair: encode exact frozen selector/literal/model/ContractSpec/authority/certificate values; enforce nested identity kinds and envelope key equality; build complete `E_c/D_c`; rebuild every cycle model affected by descriptor removal; build exact `Delta_t`, `required(S_t)`, and `D_t`; add independent complete-value mutations/assertions.

Mechanical checks passed: 13/13 tests, 102/102 assertions, 42/42 missing families, AST, diff, scope and forbidden/oracle scans. No evidence, K4, external, or held-out access occurred.
