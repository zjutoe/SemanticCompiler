# Semantic Compiler

The project is redesigning Contract IR around a minimal declarative constraint kernel and versioned domain plugins. The current semantic authority is the [Contract IR Kernel and Coding Plugin Research Plan](docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md), accepted for exact plan blob `01f959bc55f644a376f8ffa6059e9e77936be77c` after [independent review](docs/reviews/kernel_plugin/Contract_IR_Kernel_Plugin_Plan_3f7fc69_review.md).

Current status:

- Phase 0 is complete but is historical engineering evidence for its frozen finite kernel, not current semantic authority.
- The controlled-code Phase 1 milestone is paused after accepted C0 commit `4e3135b` on branch `milestone/phase1-controlled-code-planning`; no C1 handoff was created, and the branch was not merged into `main`.
- Phase 0/1 source may later be reused or discarded only after the new kernel and plugin contracts are accepted. No deletion is currently authorized or needed.
- The former [IR Design Memo v0](docs/plans/IR_Design_Memo_v0.md) and [Semantic Compiler Contract IR Research Plan](docs/plans/Semantic_Compiler_Contract_IR_Research_Plan.md) are preserved as historical design context, not current execution authority.
- [`docs/reviews/`](docs/reviews/README.md) contains the current plan, K0/K1 handoff, and K0 deliverable acceptance records plus historical advisory review input.

K0 is complete. Its [semantic design inputs](KernelPlugin/K0_Semantic_Design_Inputs_v0.md) passed [independent review](docs/reviews/kernel_plugin/K0_Design_Inputs_6ad555e_review.md) for exact blob `e86e184300a6620fb6fe25062635d9bc7cb410a1`. The [K1 handoff](KernelPlugin/handoffs/K1_kernel_calculus_and_semantics.md) passed [independent review](docs/reviews/kernel_plugin/K1_Handoff_dd87c79_review.md), and the opaque [held-out gate receipt](KernelPlugin/K1_Held_Out_Gate_Receipt.md) records that its pre-dispatch prerequisite passed. K1 is `READY_TO_BIND` but has not been bound or dispatched.
