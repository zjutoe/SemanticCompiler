# K3-X Repair-10 implementation review

- Candidate: `d09ffdea58ca74d91b02556bd923498aa48c0ae8`
- Parent: `67470d2fdada8d710a8152d099b9e95c2e7ca65c`
- Review: independent, strict, read-only, GPT-5.6 Sol high
- Verdict: **REJECT**; no execution binding

## Blocking findings

1. K1 roots use invalid constructors (`K1_SIGNATURE`, `K1_FACETS`, `K1_LITERAL`, `K1_FORMULA`, `K1_AUTHORITY`) instead of the exact six K2 `K1SyntaxKey` constructors. `expanded_root_keys` also incorrectly mixes syntax-root and record-identity values instead of typed `DependencyKey` lifts.
2. Reasoning targets remain untyped and descriptor dependencies harvest embedded identities rather than computing `required(subject)` for every typed subject plus the semantic-environment carrier. Bounds, confluence, and lexical descriptors therefore omit exact subject roots; tests repeat the same shortcut.

Auxiliary supports, binding/profile targets, trust roots, certificate key equality, exact profile, retained values, pair, and cycle are accepted by this review.

Required repair: implement the closed six-constructor `K1SyntaxKey`, typed DependencyKey lifting and exact expanded-root equations; make ReasoningTarget subjects closed typed values and derive exhaustive required subject roots independently for bounds/confluence/lexical targets; add invalid-tag, mixed-root, bare-string, and omitted-subject counterexamples.

Mechanical checks passed: 13/13 tests, 102/102 assertions, 42/42 missing families, AST and diff-check. No evidence, K4, external, or held-out access occurred.
