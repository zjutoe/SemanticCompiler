# Kernel and plugin handoff index

Only the next unaccepted stage may have a concrete handoff. A candidate or accepted handoff is not a dispatch: execution still requires an exact main-thread binding packet.

| Stage | Handoff | Status |
|---|---|---|
| K0 | [Scope, status vocabulary, semantic challenges, and anti-oracle boundary](K0_scope_status_and_challenges.md) | `CONSUMED`; [deliverable accepted](../../docs/reviews/kernel_plugin/K0_Design_Inputs_6ad555e_review.md) |
| K1 | [Minimal kernel calculus and denotational semantics](K1_kernel_calculus_and_semantics.md) | `READY_TO_BIND`; [handoff accepted](../../docs/reviews/kernel_plugin/K1_Handoff_dd87c79_review.md), [held-out gate passed](../K1_Held_Out_Gate_Receipt.md), not dispatched |
| K2-K4 | None | Roadmap only |

Historical or superseded handoffs grant no authority. Any unexpected semantic requirement stops the stage and returns to main for plan or handoff repair before work continues.
