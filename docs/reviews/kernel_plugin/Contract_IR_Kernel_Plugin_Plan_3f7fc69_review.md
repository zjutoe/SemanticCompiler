# Contract IR kernel and coding plugin plan review

- Verdict: `ACCEPT`
- Reviewed range: `787378d3763e584c9e9cc66aa699154641975a6b..3f7fc69a55a526c2dd8298dd9b3966738a5654bb`
- Accepted candidate commit: `3f7fc69a55a526c2dd8298dd9b3966738a5654bb`
- Plan path: `docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md`
- Accepted plan blob: `01f959bc55f644a376f8ffa6059e9e77936be77c`
- Review mode: independent strict read-only milestone-start review

## Reviewed change

The range changes exactly:

```text
README.md
docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md
docs/plans/IR_Design_Memo_v0.md
docs/plans/Semantic_Compiler_Contract_IR_Research_Plan.md
```

It pauses the unmerged controlled-code Phase 1 branch before C1, preserves Phase 0/1 as historical evidence, replaces the current semantic direction with a minimal declarative constraint kernel and versioned plugin boundary, and defines only a coarse K0-K4 progressive design roadmap. It creates no executable handoff or implementation authority.

## Verification

Main and the independent reviewer confirmed:

- candidate parent `787378d3763e584c9e9cc66aa699154641975a6b` is the clean `main` base named by the plan;
- the reviewed commit contains exactly the four documentation paths above;
- no accepted Phase 0 or paused Phase 1 artifact is changed;
- `git diff --check` passes;
- changed local links resolve;
- the plan separates kernel semantics from plugin atoms, truth from evaluation error, structural/profile completeness from intent completeness, and sound capability-relative reasoning from universal decidability;
- the plan preserves just-in-time handoffs and prohibits planning, execution, patch generation, model work, or benchmarks during K0-K4.

## Findings

The independent reviewer returned `ACCEPT` with no findings and no required repair.

The reviewer noted for later K2 design that plugin trust and certificate boundaries, plus cross-plugin proof composition, should be made explicit under the plan's existing soundness and `UNKNOWN` discipline. This is an optional successor-stage design note, not a defect in the reviewed plan.

## Acceptance status

Main accepts the exact plan blob and reviewed range above. The plan is the current semantic authority.

This acceptance does not create a K0 handoff, dispatch K0, or authorize implementation. The next permitted action is just-in-time K0 handoff design against this exact accepted plan, followed by independent handoff review and explicit main-thread binding before any stage work.
