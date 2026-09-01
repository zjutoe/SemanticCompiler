# K3-X Repair-12 implementation review

- Candidate: `720d45f5e1f53b544e8959cdd431886d16a4cf50`
- Parent: `d0d03acc64b6b059df7f5eb3c4e50c0ae6004773`
- Review: independent, strict, read-only, GPT-5.6 Sol high
- Verdict: **REJECT**; no execution binding

## Blocking findings

1. Dependency resolution fabricates absent `E_b/E_c/E_lex` records from names and exempts unresolved trust roots; canonical compositions omit several carriers/roots while validation passes.
2. Pair-target associations omit the matching pair binding, and syntax associations do not handle occurrence bundles, so retained occurrence symbols cannot derive exact environments.
3. Tests call the same fallback resolver and share production factories, masking phantom roots; traceability overclaims unresolved-root rejection. `ModelCapabilitySummary.dependency_scope` also remains untyped.

Exact Contract/Formula subjects and structural required-root extraction are materially repaired.

Required repair: remove all synthesized/fallback roots and trust exceptions; include every carrier/root as an authoritative record and require exact `recordAt`; make pair targets and syntax association occurrence-aware; type model summary dependency scopes; use independent literal test data/resolution and add absent environment/trust/pair-binding/occurrence counterexamples.

Mechanical checks passed: 13/13 tests, 102/102 assertions, 42/42 missing families, AST and diff-check. No evidence, K4, external, or held-out access occurred.
