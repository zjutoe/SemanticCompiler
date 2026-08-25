# Phase 0 execution contract

The [Phase 0 Engineering Exploration Plan](IR_Design_Memo_v0_Phase0_Engineering_Exploration_Plan.md) is the unique semantic and engineering authority. Execution authority descends in this order:

1. engineering-plan invariants;
2. the currently bound stage handoff;
3. implementation details.

Any conflict blocks execution and returns to main. An executor may not repair, reinterpret, or work around a plan or handoff conflict.

## Stage dependency and classification

| Stage | Classification | Predecessor | Handoff availability | Blocks Phase 0 exit |
|---|---|---|---|---|
| E0 | Blocking | None | `ACCEPTED` at `70de224`; see `reviews/E0_70de224_review.md` | Yes |
| E1 | Blocking | E0 | `ACCEPTED` at `086f9da`; see `reviews/E1_086f9da_review.md` | Yes |
| E2 | Blocking | E1 | `ACCEPTED` at `bb85d23`; see `reviews/E2_bb85d23_review.md` | Yes |
| E3 | Blocking | E2 | Contract-accepted `READY_TO_BIND` handoff; package `3d77419`, see `reviews/E3_3d77419_review.md`; not dispatched | Yes |
| E4 | Blocking | E3 | Generate only after exact E3 acceptance | Yes |
| E5 | Optional | E4 | Generate only after exact E4 acceptance and explicit optional-scope authorization | No |

The blocking sequence is `E0 -> E1 -> E2 -> E3 -> E4`. E5 may start only after accepted E4 and never blocks Phase 0 exit.

## Just-in-time handoff rule

Only the next unaccepted executable stage has a current concrete handoff document. Historical accepted handoffs remain committed for provenance but grant no new mutation authority. Downstream handoffs are deliberately absent because implementation and review may discover constraints that must shape the next stage. After a stage is independently accepted, main first incorporates any accepted interface, fixture, or contract changes, then writes and reviews the successor handoff against that exact state.

A dependency roadmap may retain later stage names and coarse objectives, but it is not executable authority. No agent may infer missing downstream instructions from an old plan, a temporary draft, or a predecessor handoff. Unexpected findings stop the current stage and return to main for contract repair before any successor handoff is generated.

## Branch, dispatch, and mutation lease

Phase 0 uses one milestone branch created from a clean `main`, sequential stage commits, and no history rewriting. A dispatch is valid only when the main thread binds all of the following:

- exact source commit;
- exact handoff path and handoff blob SHA;
- predecessor accepted commit or reviewed range, where applicable;
- exact allowed mutation paths;
- exact verification commands and output roots.

A branch name alone is not a binding. Only one writer may hold the repository mutation lease. Main owns semantic contracts, scheduling, the commit gate, review resolution, and acceptance. The writer edits only allowed paths, verifies the stage, returns the prescribed evidence, and does not commit. Main freezes the stage diff in a new commit.

## Review, repair, and acceptance

After the stage diff is frozen, an independent read-only reviewer receives only the exact handoff and blob SHA, reviewed commit or range, completed verification, and bound artifacts. The reviewer stays read-only. A rejection produces a separate repair commit followed by a fresh independent review; reviewed history is never rewritten.

Accepted review records belong in [`Phase0/reviews/`](reviews/README.md), must name the exact reviewed commit or range, and use:

```text
E<N>_<short-reviewed-sha>_review.md
```

No placeholder review records are created before a real review.

## Stage invariants

No stage may broaden its scope, patch a predecessor, change the engineering plan or a handoff, hide fallback/default/retry behavior, or import Gold/expected fixture modules on a normal production path. Contract conflicts block and return to main.

Formal or recorded runs require a clean, committed worktree and must record the exact source commit. Git binds tracked source, fixtures, configuration, launchers, and tests; do not maintain parallel hashes for them. Evidence outside Git, including external datasets, weights, fixed uncommitted inputs, and run artifacts, must be bound by path and checksum.

See the [handoff index](handoffs/README.md) for the current executable handoff and the non-binding stage roadmap.
