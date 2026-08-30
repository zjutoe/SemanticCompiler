# Contract IR kernel and plugin design process

> Status: K0 through K3-S are accepted and complete. K3-X is eligible for just-in-time handoff design but has no handoff or mutation authority yet; K4 remains roadmap-only.

The accepted semantic authority is the [Contract IR Minimal Kernel and Coding Plugin Research Plan](../docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md), exact blob `01f959bc55f644a376f8ffa6059e9e77936be77c`, plus the [K3-S/K3-X plan amendment](../docs/plans/K3_Semantics_and_Executable_Spike_Amendment.md), exact blob `7f1c3627245ec0c0fc86df64f77e374d104649a0`. Their acceptance records are the [original plan review](../docs/reviews/kernel_plugin/Contract_IR_Kernel_Plugin_Plan_3f7fc69_review.md) and [amendment review](../docs/reviews/kernel_plugin/K3_SX_Plan_19379b3_review.md).

## Accepted K0 result

The [accepted K0 handoff](handoffs/K0_scope_status_and_challenges.md), exact blob `914f1bb56792e20765b63b4a63f3db2a244cf560`, produced [K0 Semantic Design Inputs v0](K0_Semantic_Design_Inputs_v0.md). The exact deliverable blob `e86e184300a6620fb6fe25062635d9bc7cb410a1` passed [independent review](../docs/reviews/kernel_plugin/K0_Design_Inputs_6ad555e_review.md).

K0 froze the design inputs for K1; it did not select the kernel calculus, plugin ABI, coding symbols, evaluator implementation, or execution architecture. The [accepted K1 handoff](handoffs/K1_kernel_calculus_and_semantics.md), exact blob `ded68369ecc2d06ac2e3ddcf9ca20cb9e928b058`, and opaque [held-out gate receipt](K1_Held_Out_Gate_Receipt.md) governed the exact K1 execution.

## Accepted K1 result

The [K1 kernel calculus and denotational semantics](K1_Kernel_Calculus_and_Denotational_Semantics_v0.md), exact blob `d928010319c2c3bd08a94e1856cfca24dc2ae39e`, passed [independent full-stage review](../docs/reviews/kernel_plugin/K1_Kernel_Calculus_f3418a6_review.md). It freezes the minimal kernel semantics, relative-minimality ledger, exact logical and failure boundaries, and K2 semantic obligations within the accepted K0 scope. It defines no serialization, plugin ABI, coding symbol catalog, or implementation.

## Accepted K2 result

The [K2 versioned plugin ABI and reasoning interface](K2_Versioned_Plugin_ABI_and_Reasoning_Interface_v0.md), exact blob `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`, passed [independent milestone-end scientific acceptance](../docs/reviews/kernel_plugin/K2_Plugin_ABI_5b6f157_review.md). It freezes the transport-neutral versioned plugin interface, exact lifecycle and failure rules, trust and certificate boundary, responsibility ledger, K1 coverage map, and K3 input boundary. It defines no byte serialization, implementation, coding vocabulary, benchmark, or K3 authority.

## Accepted K3-S result

The [K3-S minimal coding-plugin semantics](K3_S_Minimal_Coding_Plugin_Semantics_v0.md), exact blob `31e9ffbaedcf7c1531a0a614078479f7cfefb1fe`, passed [independent scientific acceptance](../docs/reviews/kernel_plugin/K3_S_Semantics_ced9082_review.md). It freezes the smallest accepted coding vocabulary and a finite 102-entry semantic packet for K3-X. It establishes representability only; it defines no executable kernel, parser, planner, repository operation, or performance claim.

## Stage roadmap

| Stage | Objective | Status |
|---|---|---|
| K0 | Scope, statuses, seed challenges, held-out procedure, anti-oracle rules | Accepted and complete |
| K1 | Kernel calculus and denotational semantics | Accepted and complete |
| K2 | Versioned plugin ABI and reasoning interface | [Accepted and complete](../docs/reviews/kernel_plugin/K2_Plugin_ABI_5b6f157_review.md) |
| K3-S | Minimal coding-plugin semantics | [Accepted and complete](../docs/reviews/kernel_plugin/K3_S_Semantics_ced9082_review.md) |
| K3-X | Finite in-memory toy kernel and accepted toy coding plugin | Eligible for just-in-time handoff design; no handoff yet |
| K4 | Held-out semantic closure and manual binding assessment | Roadmap only |

Execution requires an accepted handoff plus a separate main-thread binding of the exact clean source commit, handoff blob, allowed mutation path, verification commands, and output roots. Only one writer may hold the mutation lease, and the writer does not commit. K2 completion and the plan amendment grant no K3-S or K3-X mutation authority; each stage requires its own just-in-time handoff and independent review.
