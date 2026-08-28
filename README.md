# Semantic Compiler

The project is redesigning Contract IR around a minimal declarative constraint kernel and versioned domain plugins. The current semantic authority is the [Contract IR Kernel and Coding Plugin Research Plan](docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md), accepted for exact plan blob `01f959bc55f644a376f8ffa6059e9e77936be77c` after [independent review](docs/reviews/kernel_plugin/Contract_IR_Kernel_Plugin_Plan_3f7fc69_review.md).

Current status:

- Phase 0 is complete but is historical engineering evidence for its frozen finite kernel, not current semantic authority.
- The controlled-code Phase 1 milestone is paused after accepted C0 commit `4e3135b` on branch `milestone/phase1-controlled-code-planning`; no C1 handoff was created, and the branch was not merged into `main`.
- Phase 0/1 source may later be reused or discarded only after the new kernel and plugin contracts are accepted. No deletion is currently authorized or needed.
- The former [IR Design Memo v0](docs/plans/IR_Design_Memo_v0.md) and [Semantic Compiler Contract IR Research Plan](docs/plans/Semantic_Compiler_Contract_IR_Research_Plan.md) are preserved as historical design context, not current execution authority.
- [`docs/reviews/`](docs/reviews/README.md) contains the current plan, K0--K2 handoff, and K0/K1 deliverable acceptance records plus historical advisory review input.

K0 and K1 are complete. The [K0 semantic design inputs](KernelPlugin/K0_Semantic_Design_Inputs_v0.md) passed [independent review](docs/reviews/kernel_plugin/K0_Design_Inputs_6ad555e_review.md) for exact blob `e86e184300a6620fb6fe25062635d9bc7cb410a1`. The resulting [K1 kernel calculus and denotational semantics](KernelPlugin/K1_Kernel_Calculus_and_Denotational_Semantics_v0.md) passed [independent full-stage review](docs/reviews/kernel_plugin/K1_Kernel_Calculus_f3418a6_review.md) for exact blob `d928010319c2c3bd08a94e1856cfca24dc2ae39e`. The just-in-time [K2 handoff](KernelPlugin/handoffs/K2_versioned_plugin_abi_and_reasoning_interface.md), exact blob `f308543b4c252d739840a96df88abedcde893bbb`, passed [independent review](docs/reviews/kernel_plugin/K2_Handoff_2b5aa0c_review.md) and is `READY_TO_BIND`; it is not dispatched and grants no K2 mutation authority.
