# Kernel and plugin handoff index

Only the next unaccepted stage may have a concrete handoff. A candidate or accepted handoff is not a dispatch: execution still requires an exact main-thread binding packet.

| Stage | Handoff | Status |
|---|---|---|
| K0 | [Scope, status vocabulary, semantic challenges, and anti-oracle boundary](K0_scope_status_and_challenges.md) | `CONSUMED`; [deliverable accepted](../../docs/reviews/kernel_plugin/K0_Design_Inputs_6ad555e_review.md) |
| K1 | [Minimal kernel calculus and denotational semantics](K1_kernel_calculus_and_semantics.md) | `CONSUMED`; [deliverable accepted](../../docs/reviews/kernel_plugin/K1_Kernel_Calculus_f3418a6_review.md) |
| K2 | [Versioned plugin ABI and reasoning interface](K2_versioned_plugin_abi_and_reasoning_interface.md) | `CONSUMED`; [deliverable accepted](../../docs/reviews/kernel_plugin/K2_Plugin_ABI_5b6f157_review.md) |
| K3-S | [Minimal coding-plugin semantics](K3_S_minimal_coding_plugin_semantics.md) | `CONSUMED`; [deliverable accepted](../../docs/reviews/kernel_plugin/K3_S_Semantics_ced9082_review.md) |
| K3-X | [Finite executable kernel and coding-plugin spike](K3_X_finite_executable_spike.md) | Handoff `CONSUMED`; [implementation accepted](../../docs/reviews/kernel_plugin/K3_X_Implementation_326a57f_review.md); [execution binding](K3_X_execution_binding.md) is a review candidate and grants no execution authority |
| K4 | None | Roadmap only |

Historical or superseded handoffs grant no authority. Any unexpected semantic requirement stops the stage and returns to main for plan or handoff repair before work continues.
