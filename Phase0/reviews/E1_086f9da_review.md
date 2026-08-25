# E1 implementation review

- Stage: `E1`
- Package: shared semantics, elaborator, runtime, backend, and E1 tests
- Verdict: `ACCEPT`
- Reviewed commit/range: `d8ffeb0301d53f3fd55b649bf1ebff3b7cf30bd5..086f9da0519977e55af7d63b98032ab1e207e22f`
- Accepted implementation HEAD: `086f9da0519977e55af7d63b98032ab1e207e22f`
- Initial implementation commit: `2e5a913ec6e0a4074b46c1e90f0e2330d19fa8c0`
- Repair commits: `f9401ca35c397609ee385d2f67c1913cefc8fb68`, `39cca216a85d8afad2d44cc643dd2068f102ace5`, `9e1e9837544132fd8f39376b632e00b93195c37d`, `086f9da0519977e55af7d63b98032ab1e207e22f`
- Implementation executor: `gpt-5.5`, reasoning effort `xhigh`
- Handoff path: `Phase0/handoffs/E1_shared_semantics_elaborator_runtime.md`
- Handoff blob SHA: `764ff2c0e1d731752ba80249bcf0f179d4820a3e`
- Handoff contract review: `Phase0/reviews/E1_3fe1e40_review.md`
- Accepted predecessor implementation: `70de224c6cdc40b8a0f5c2f35fe7d934987a9e31`

## Intended implementation

The accepted range changes exactly:

```text
Phase0/implementation/backend.py
Phase0/implementation/elaboration.py
Phase0/implementation/runtime.py
Phase0/tests/test_e1_elaboration_and_runtime.py
```

It implements the E1 Gold-canonical shared backend: deterministic elaboration and authority derivation, finite joint completion, hard validity, managed-effect authorization, minimal witnesses, executor coverage, one-shot sufficient ASK, closed decisions, and exact execution results when the supporting trajectories determine one post-state/effect sequence. It does not implement A/B adapters, the C path, tracing, runners, or experiment outputs.

## Verification

- `git hash-object Phase0/handoffs/E1_shared_semantics_elaborator_runtime.md` -> `764ff2c0e1d731752ba80249bcf0f179d4820a3e`.
- `git diff --name-status d8ffeb0301d53f3fd55b649bf1ebff3b7cf30bd5..086f9da0519977e55af7d63b98032ab1e207e22f` -> exactly the four allowed paths above.
- `python -m unittest Phase0.tests.test_e0_dialect_and_fixtures Phase0.tests.test_e1_elaboration_and_runtime` -> 23 tests passed, exit 0.
- `git diff --check d8ffeb0301d53f3fd55b649bf1ebff3b7cf30bd5..086f9da0519977e55af7d63b98032ab1e207e22f` -> pass.
- Final fresh reviewer reran the tests with bytecode disabled, verified malformed trajectory-ID failure routes, and confirmed a clean worktree.
- External artifacts and checksums: none; E1 creates no run output and all versioned evidence is Git-bound.

## Review findings and repairs

The initial independent review rejected `2e5a913ec6e0a4074b46c1e90f0e2330d19fa8c0` because ASK sufficiency could treat a branch without a producible nonempty conflict witness as closed, and directly constructed malformed term tags, enum members, source roles, and knowledge metadata could reach ordinary decisions. Repair `f9401ca35c397609ee385d2f67c1913cefc8fb68` added semantic closure checks and explicit elaboration-boundary failures.

The next fresh review confirmed those repairs but rejected the range because empty trajectory/completion fibers could still produce vacuous clause witnesses, and static constraints did not verify that their manifest predicate had `INITIAL` scope. Repair `39cca216a85d8afad2d44cc643dd2068f102ace5` made empty fibers fail loudly, excluded them from ASK closure, enforced static predicate scope, and added exact counterexamples.

The following fresh review rejected the range because integer values could exploit Python boolean equality in static-context filtering, and malformed cross-constraint pairs could leak raw `TypeError`. Repair `9e1e9837544132fd8f39376b632e00b93195c37d` added bounded systematic validation of the handoff-owned elaboration input records, exact boolean checks, safe cross-record shape validation, and direct-dataclass regressions.

The next fresh review confirmed those repairs but found that malformed `candidate_trajectory_ids` could still leak raw runtime errors or accept a mutable list. Repair `086f9da0519977e55af7d63b98032ab1e207e22f` now validates the exact `tuple[str, ...]` boundary before hashing or lookup and preserves distinct malformed, duplicate, and unknown-ID failure reasons.

A new independent reviewer accepted the complete repaired range with no findings and no required repair.

## Acceptance status

Main accepts exactly the implementation range ending at `086f9da0519977e55af7d63b98032ab1e207e22f`. E1 is complete. This record does not generate or dispatch E2; the E2 handoff must be created just in time from the accepted E1 interfaces and findings, then independently accepted before any E2 mutation authority exists.
