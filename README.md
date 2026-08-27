# Semantic Compiler

The project is redesigning Contract IR around a minimal declarative constraint kernel and versioned domain plugins. The current semantic authority is the [Contract IR Kernel and Coding Plugin Research Plan](docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md), accepted for exact plan blob `01f959bc55f644a376f8ffa6059e9e77936be77c` after [independent review](docs/reviews/kernel_plugin/Contract_IR_Kernel_Plugin_Plan_3f7fc69_review.md).

Current status:

- Phase 0 is complete but is historical engineering evidence for its frozen finite kernel, not current semantic authority.
- The controlled-code Phase 1 milestone is paused after accepted C0 commit `4e3135b` on branch `milestone/phase1-controlled-code-planning`; no C1 handoff was created, and the branch was not merged into `main`.
- Phase 0/1 source may later be reused or discarded only after the new kernel and plugin contracts are accepted. No deletion is currently authorized or needed.
- The former [IR Design Memo v0](docs/plans/IR_Design_Memo_v0.md) and [Semantic Compiler Contract IR Research Plan](docs/plans/Semantic_Compiler_Contract_IR_Research_Plan.md) are preserved as historical design context, not current execution authority.
- [`docs/reviews/`](docs/reviews/README.md) contains the current plan acceptance record and historical advisory review input.

No implementation stage is currently authorized. A [K0 handoff candidate](KernelPlugin/handoffs/K0_scope_status_and_challenges.md) now exists for independent review; it grants no mutation or dispatch authority unless accepted and explicitly bound.
