# K3-X Repair-11 implementation review

- Candidate: `2b9d826a58a7e12bad33bce0aab4c2ee2ed18313`
- Parent: `f5afbca4654c7cb3534bedc7e0da5d222b6be925`
- Review: independent, strict, read-only, GPT-5.6 Sol high
- Verdict: **REJECT**; no execution binding

## Blocking findings

1. `ContractSubject` and `FormulaSubject` wrap identities/labels rather than exact Contract and formula-set/scope values. `required_subject` dispatches on local names, so a foreign `C_b` identity receives canonical roots; tests duplicate this shortcut.
2. Typed reasoning roots are converted back into lossy `RecordIdentity` values. Declaration roots become wrong-kind `DECLARATION` rather than actual type declarations, symbol roots become nonexistent records, and all reasoning descriptors contain unresolved proper dependencies; tests repeat the same conversion.

The exact six-constructor K1 algebra, typed dependency environments, mixed-root rejection, retained packet, pair, cycle, profile, certificate, and other prior repairs are accepted.

Required repair: make subjects carry exact Contract/formula values and compute required roots extensionally; keep descriptor dependencies typed through resolution or use the exact K2 association/lift path without lossy identity conversion; independently assert every dependency resolves and foreign same-local subjects differ.

Mechanical checks passed: 13/13 tests, 102/102 assertions, 42/42 missing families, AST and diff-check. No evidence, K4, external, or held-out access occurred.
