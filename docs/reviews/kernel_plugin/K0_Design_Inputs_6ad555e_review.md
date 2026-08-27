# K0 semantic design inputs review and acceptance

- Verdict: `ACCEPT`
- Bound source commit: `55551979b6da9936a75aff3e86fe752803b60c60`
- Reviewed range: `55551979b6da9936a75aff3e86fe752803b60c60..6ad555e9b95f615329491f957ef0e4f0cf5a82bf`
- Candidate commit: `ead84f22acbc36c396c99c09b3fefd8c538ead5e`
- Repair commits: `ab74dadf784a9975956dce8379e9733e002cdfce`, `6ad555e9b95f615329491f957ef0e4f0cf5a82bf`
- Deliverable path: `KernelPlugin/K0_Semantic_Design_Inputs_v0.md`
- Accepted deliverable blob: `e86e184300a6620fb6fe25062635d9bc7cb410a1`
- Accepted handoff blob: `914f1bb56792e20765b63b4a63f3db2a244cf560`
- Governing plan blob: `01f959bc55f644a376f8ffa6059e9e77936be77c`
- Review mode: independent strict read-only stage-result review

## Bound execution

Main bound K0 to the exact clean source commit, accepted plan and handoff blobs, and the sole mutation path `KernelPlugin/K0_Semantic_Design_Inputs_v0.md`. One delegated writer created that file and did not commit. No external artifact root was authorized or used.

The deliverable freezes:

- the K0 research scope and exclusions around `Outcome = (PRE, TRACE, FINAL, EVIDENCE)`;
- exact non-overloaded status families;
- nineteen ordinary-language seed semantic challenges;
- ten separating-pair obligations;
- a deterministic held-out selection and pre-K1 freeze procedure;
- anti-oracle and anti-circularity rules;
- K1 input decisions, unresolved questions, and acceptance checks.

## Review and repairs

The first independent review rejected SP-01 because it varied conditionality as well as obligation versus permission. Repair commit `ab74dadf784a9975956dce8379e9733e002cdfce` made the condition and event identical while varying only normative role.

A fresh full review rejected four remaining counterexample defects: K0-C11 allowed a vacuous empty population, while SP-02, SP-03, and SP-05 varied unrelated facts as well as their target distinctions. Repair commit `6ad555e9b95f615329491f957ef0e4f0cf5a82bf` required a nonempty bundle population and replaced the three rows with controlled comparisons.

A third fresh reviewer inspected the complete plan, handoff, and repaired deliverable and returned `ACCEPT` with no findings or required repairs.

## Verification

Main and the final reviewer confirmed:

- exact commits, ancestry, plan, handoff, and deliverable blobs;
- the reviewed range changes only `KernelPlugin/K0_Semantic_Design_Inputs_v0.md`;
- `git diff --check` passes;
- exactly eight required top-level sections appear in order;
- all nineteen challenges contain the eight required fields and cover every required family;
- all ten required distinctions have controlled separating pairs and explicit information-loss statements;
- held-out tasks are selected and frozen before K1, withheld from K1-K3, and later bound separately for K4;
- unknown, error, unrepresentable, unresolved, inconsistency, and profile incompleteness remain distinct;
- no final kernel syntax, plugin ABI, coding symbol catalog, evaluator implementation, prompt, action graph, implementation, K1 handoff, downstream authority, or external artifact was introduced.

## Acceptance status

Main accepts only the exact K0 deliverable blob and reviewed range above. K0 is complete.

This acceptance creates no K1 mutation authority. Under the progressive-stage rule, the next permitted action is just-in-time K1 handoff design, followed by independent review and a separate exact binding before K1 work.
