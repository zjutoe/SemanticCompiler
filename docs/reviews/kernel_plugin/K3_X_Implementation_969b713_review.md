# K3-X Repair-9 implementation review

- Candidate: `969b713fdeaad6be68d2930bf0fb6904693121a1`
- Parent: `c91cc0378e013086e79433eb42664f0f19cc73e6`
- Review: independent, strict, read-only, GPT-5.6 Sol high
- Verdict: **REJECT**; no execution binding

## Blocking findings

1. Auxiliary ContractSpecs are inexact: access boundaries omit the lower meaning support and verification evidence schema omits `T(CodingEvidenceEntry)`.
2. Six capability descriptors use declaration identities instead of typed binding/profile targets and omit trust roots from exhaustive proper dependencies.
3. `E_c/D_c` and `E_t/D_t` omit frozen K1 plugin, symbol, declaration, signature, and literal syntax roots; some required sets are still candidate-derived.
4. Evolution accepts a certificate envelope whose enclosing record identity and `certificate_key` disagree.
5. The retained profile is a reused task predicate binding, not the exact two-dimensional `PROFILE_impl` with coverage/evidence/support/unknown/error semantics.

Selector, literal-symbol, authority, BENV, pair, and cycle findings are repaired. Confluence/evolution contents are substantially repaired but their syntax-root semantics remain incomplete.

Required repair: encode exact auxiliary supports and profile; introduce typed capability targets and trust-root-complete dependencies; freeze K1 syntax-root sets independently; enforce envelope record/value key equality; add each adversarial mutation to tests and narrow traceability.

Mechanical checks passed: 13/13 tests, 102/102 assertions, 42/42 missing families, AST and diff-check. No evidence, K4, external, or held-out access occurred.
