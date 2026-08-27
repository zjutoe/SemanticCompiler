# Contract IR kernel and plugin design process

> Status: the governing plan and exact K0 handoff blob are accepted; K0 is `READY_TO_BIND` but has not been bound or dispatched.

The accepted semantic authority is the [Contract IR Minimal Kernel and Coding Plugin Research Plan](../docs/plans/Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md), exact blob `01f959bc55f644a376f8ffa6059e9e77936be77c`. Its [acceptance record](../docs/reviews/kernel_plugin/Contract_IR_Kernel_Plugin_Plan_3f7fc69_review.md) binds reviewed range `787378d3763e584c9e9cc66aa699154641975a6b..3f7fc69a55a526c2dd8298dd9b3966738a5654bb`.

## Current stage

K0 is the only stage with a concrete handoff. The [accepted K0 handoff](handoffs/K0_scope_status_and_challenges.md) freezes only the design-input package: research scope, semantic status vocabulary, seed challenges, held-out selection procedure, and anti-oracle rules. Its exact blob `914f1bb56792e20765b63b4a63f3db2a244cf560` passed [independent review](../docs/reviews/kernel_plugin/K0_Handoff_59d2799_review.md).

The accepted handoff is `READY_TO_BIND`, not executable authority: it grants no mutation permission until main issues a separate exact binding packet. K1-K4 remain roadmap-only; no handoff may be created for them before exact K0 deliverable acceptance.

## Stage roadmap

| Stage | Objective | Status |
|---|---|---|
| K0 | Scope, statuses, seed challenges, held-out procedure, anti-oracle rules | Handoff accepted; `READY_TO_BIND`, not dispatched |
| K1 | Kernel calculus and denotational semantics | Roadmap only |
| K2 | Versioned plugin ABI and reasoning interface | Roadmap only |
| K3 | Minimal coding plugin | Roadmap only |
| K4 | Held-out semantic closure and manual binding assessment | Roadmap only |

Execution requires an accepted handoff plus a separate main-thread binding of the exact clean source commit, handoff blob, allowed mutation path, verification commands, and output roots. Only one writer may hold the mutation lease, and the writer does not commit.
