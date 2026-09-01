# K3-X Repair-6 implementation review

- Candidate: `78d2b1d2e77720c7bb52f07f8982fec07c39064d`
- Range: `88d903b0aa568f7775d784c8adc0f0188ab55ccd..78d2b1d2e77720c7bb52f07f8982fec07c39064d`
- Review: independent, strict, read-only, GPT-5.6 Sol high
- Verdict: **REJECT**
- Execution binding: **not eligible**

## Blocking findings

1. The closed coding type algebra is incomplete. Several retained K3-S packet types, including change, verification, evidence, profile-subject, and event-payload types, have no admission type or nested predicate.
2. Pair admission is inexact. `IndependentCoherenceProof` omits its bundle, several producer coordinates are checked only for non-emptiness rather than exact equality, and `E_p` ABI, `chi_c`, and mechanically extracted dependencies are not validated.
3. Confluence still uses reduced `C_c`, `E_c`, and package markers. Duplicate bindings and invalid ABI/dependency coordinates are accepted; the package is not the retained literal `PKG_CK`.
4. The cycle is only a differential of that reduced synthetic package, not an exact replacement inside the retained `PKG_CK` required by K3-S.
5. Evolution requests may refer to an absent semantic environment and dangling proper dependencies. Package validation does not resolve and validate the exact source/target environments and closure.
6. Tests and traceability therefore overclaim exact producer, environment, retained-package, and cycle coverage.

## Required repair

- Implement every retained K3-S closed type and nested admission predicate.
- Construct one literal retained `PKG_CK` and reuse it for core, confluence, and cycle; make cycle an exact replacement within it.
- Represent and validate exact `C_c`, `E_c`, `D_c`, authority/adoption, ABI, dependency, and producer coordinates.
- Include bundle, certificate, and validator in independent pair proof and require exact producer equations.
- Include, resolve, and traverse exact evolution source/target semantic environments; reject dangling dependencies.
- Add the review counterexamples and limit traceability claims to independently falsified behavior.

## Verification

Mechanical checks passed but do not close the semantic findings:

- 13/13 unit tests
- 102/102 fixture assertions, including 42 base and 42 variant missing rows
- AST parse and `git diff --check`
- exact five-path candidate change, clean worktree, no caches or forbidden access

No evidence run, K4 work, external access, or held-out-content inspection occurred.
