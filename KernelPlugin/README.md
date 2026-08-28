# Contract IR kernel and plugin design process

> Status: K0 and K1 are accepted and complete. The K2 handoff is accepted and `READY_TO_BIND`, but is not dispatched and grants no mutation authority.

The accepted semantic authority is the [Contract IR Minimal Kernel and Coding Plugin Research Plan](../docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md), exact blob `01f959bc55f644a376f8ffa6059e9e77936be77c`. Its [acceptance record](../docs/reviews/kernel_plugin/Contract_IR_Kernel_Plugin_Plan_3f7fc69_review.md) binds reviewed range `787378d3763e584c9e9cc66aa699154641975a6b..3f7fc69a55a526c2dd8298dd9b3966738a5654bb`.

## Accepted K0 result

The [accepted K0 handoff](handoffs/K0_scope_status_and_challenges.md), exact blob `914f1bb56792e20765b63b4a63f3db2a244cf560`, produced [K0 Semantic Design Inputs v0](K0_Semantic_Design_Inputs_v0.md). The exact deliverable blob `e86e184300a6620fb6fe25062635d9bc7cb410a1` passed [independent review](../docs/reviews/kernel_plugin/K0_Design_Inputs_6ad555e_review.md).

K0 froze the design inputs for K1; it did not select the kernel calculus, plugin ABI, coding symbols, evaluator implementation, or execution architecture. The [accepted K1 handoff](handoffs/K1_kernel_calculus_and_semantics.md), exact blob `ded68369ecc2d06ac2e3ddcf9ca20cb9e928b058`, and opaque [held-out gate receipt](K1_Held_Out_Gate_Receipt.md) governed the exact K1 execution.

## Accepted K1 result

The [K1 kernel calculus and denotational semantics](K1_Kernel_Calculus_and_Denotational_Semantics_v0.md), exact blob `d928010319c2c3bd08a94e1856cfca24dc2ae39e`, passed [independent full-stage review](../docs/reviews/kernel_plugin/K1_Kernel_Calculus_f3418a6_review.md). It freezes the minimal kernel semantics, relative-minimality ledger, exact logical and failure boundaries, and K2 semantic obligations within the accepted K0 scope. It defines no serialization, plugin ABI, coding symbol catalog, or implementation.

## Stage roadmap

| Stage | Objective | Status |
|---|---|---|
| K0 | Scope, statuses, seed challenges, held-out procedure, anti-oracle rules | Accepted and complete |
| K1 | Kernel calculus and denotational semantics | Accepted and complete |
| K2 | Versioned plugin ABI and reasoning interface | [Handoff accepted](../docs/reviews/kernel_plugin/K2_Handoff_2b5aa0c_review.md); `READY_TO_BIND`, not dispatched |
| K3 | Minimal coding plugin | Roadmap only |
| K4 | Held-out semantic closure and manual binding assessment | Roadmap only |

Execution requires an accepted handoff plus a separate main-thread binding of the exact clean source commit, handoff blob, allowed mutation path, verification commands, and output roots. Only one writer may hold the mutation lease, and the writer does not commit. K2 handoff acceptance grants no K2 mutation authority by itself.
