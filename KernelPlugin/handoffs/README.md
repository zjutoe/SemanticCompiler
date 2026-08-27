# Kernel and plugin handoff index

Only the next unaccepted stage may have a concrete handoff. A candidate or accepted handoff is not a dispatch: execution still requires an exact main-thread binding packet.

| Stage | Handoff | Status |
|---|---|---|
| K0 | [Scope, status vocabulary, semantic challenges, and anti-oracle boundary](K0_scope_status_and_challenges.md) | `READY_TO_BIND`; [accepted exact blob](../../docs/reviews/kernel_plugin/K0_Handoff_59d2799_review.md), not dispatched |
| K1-K4 | None | Roadmap only |

Historical or superseded handoffs grant no authority. Any unexpected semantic requirement stops the stage and returns to main for plan or handoff repair before work continues.
