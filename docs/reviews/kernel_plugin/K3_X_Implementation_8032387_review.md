# K3-X Repair-7 implementation review

- Candidate: `80323877057a9537ec7bd6d5907afcca6bf97f20`
- Range: `40a5817faaea9fb0f097fe42e24a035f65a4bb5e..80323877057a9537ec7bd6d5907afcca6bf97f20`
- Review: independent, strict, read-only, GPT-5.6 Sol high
- Verdict: **REJECT**
- Execution binding: **not eligible**

## Blocking findings

1. The shared `PKG_CK` has the requested cardinalities but is generated from reduced builders and contains inexact values: type-admission domains are type-name tuples rather than `Value`, four descriptors are placeholders with empty targets/roots, and authority literals use incorrect roles, principals, provenance, and empty evidence.
2. Confluence still runs on parallel `confluence.*` declarations and bindings. Its `E_c` is reduced, and removing retained-package literals does not affect the result.
3. The cycle incorrectly changes retained `event_occurred`; K3-S changes only `event_matches` and its model projection while `event_occurred` reaches that same-key replacement unchanged.
4. Evolution resolves environment identities but does not validate exact environment contents, member kinds, empty/exact `chi_c`, mechanically extracted dependencies, or environment-derived closure.
5. Tests and traceability overclaim literal package, confluence, cycle, and evolution exactness.

Pair proof, exact producer equality, `E_p`, and `D_p` are accepted by this review. All 55 closed-type predicates exist, but their governing admission ContractSpecs and some retained literals remain inexact.

## Required repair

- Replace generated and placeholder retained rows with exact K3-S values, especially admission domains, services, targets, roots, fragments, models, `BENV`, and authority evidence.
- Make confluence nodes resolve retained ordinary bindings and reconstruct exact `E_c/D_c`; add retained-member deletion tests.
- Leave `event_occurred` byte-for-byte unchanged in the cycle differential.
- Validate exact evolution `SemanticEnvironment` contents and derived closure, including the three review mutations.
- Correct tests and traceability to independently falsify these claims.

Mechanical checks passed: 13/13 tests, 102/102 assertions, 42/42 missing families, AST, diff-check, scope, and forbidden/oracle scans. No evidence, K4, external access, or held-out access occurred.
