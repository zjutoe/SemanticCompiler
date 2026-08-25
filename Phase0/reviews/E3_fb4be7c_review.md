# E3 implementation review

- Stage: `E3`
- Package: normal C extraction, referenced-support view, controlled-language bridge, and E3 tests
- Verdict: `ACCEPT`
- Reviewed commit/range: `c3f2c94268c05dae1e57ecc989cdd57836d06fb2..fb4be7c36ae3b8175c39364aa446c82f9f2a5d87`
- Accepted implementation HEAD: `fb4be7c36ae3b8175c39364aa446c82f9f2a5d87`
- Initial implementation commit: `8c942dea1478c41162806e9ec25679681048ec62`
- Repair commit: `fb4be7c36ae3b8175c39364aa446c82f9f2a5d87`
- Handoff path: `Phase0/handoffs/E3_c_real_bridge_path.md`
- Handoff blob SHA: `3d61b7b3404745ab4000a5327a446ce70ece84d2`
- Handoff contract review: `Phase0/reviews/E3_3d77419_review.md`
- Accepted predecessor implementation: `bb85d237f55d685bc718ccdc2d07bf913285b724`

## Intended implementation

The accepted range changes exactly:

```text
Phase0/implementation/content_bridge.py
Phase0/tests/test_e3_content_bridge.py
```

It implements strict atomic-span validation, role-independent lexical extraction, a fresh refs-only support view, and the one four-input structural `beta_C`. Lexical recognition remains separate from manifest-driven member/effect/OPEN-owner validation. F9 normal source and both Gold-C cases enter the same bridge and unchanged backend; unreferenced distractors remain outside the support view.

The implementation does not add learned compilation, alternate bridges, general parsing, entities, fallbacks/retries, E4 tracing/runners/artifacts, or experiment reporting.

## Verification

- `git hash-object Phase0/handoffs/E3_c_real_bridge_path.md` -> `3d61b7b3404745ab4000a5327a446ce70ece84d2`.
- `git diff --name-status c3f2c94268c05dae1e57ecc989cdd57836d06fb2..fb4be7c36ae3b8175c39364aa446c82f9f2a5d87` -> exactly the two allowed paths above.
- `python -B -m unittest Phase0.tests.test_e0_dialect_and_fixtures Phase0.tests.test_e1_elaboration_and_runtime Phase0.tests.test_e2_typed_paths Phase0.tests.test_e3_content_bridge` -> 46 tests passed, exit 0.
- `ruff check --no-cache Phase0/implementation/content_bridge.py Phase0/tests/test_e3_content_bridge.py` -> passed.
- `git diff --check` on the implementation and repair ranges -> passed.
- The final independent reviewer confirmed a clean worktree, exercised all eleven Python `splitlines()` boundary forms, proved malformed mixed envelopes make zero recognition calls, checked that non-ASCII whitespace is not normalized, and confirmed that nonempty actual knowledge assertions cannot falsely project to `[]`.
- External artifacts and checksums: none; E3 creates no recorded-run output and all versioned evidence is Git-bound.

## Findings and repair

The first independent implementation reviewer rejected `8c942dea1478c41162806e9ec25679681048ec62` for two defects:

1. atomic validation rejected only CR/LF, allowing other embedded line boundaries to make a malformed mixed envelope partially process valid spans;
2. the test-local elaboration projection hard-coded empty knowledge assertions, permitting a false-positive exact comparison.

Repair `fb4be7c36ae3b8175c39364aa446c82f9f2a5d87` uses standard `str.splitlines()` semantics to reject all recognized embedded line boundaries before extraction, adds a Unicode mixed-envelope regression, and makes the test projection inspect and explicitly reject unexpected nonempty knowledge assertions.

A new independent strict read-only reviewer accepted the complete repaired range with no findings and no required repair.

The executor's bounded engineering observations were:

1. extraction failures end at `surface/NO_REPRESENTABLE_CONTENT`, while lexically recognized but dialect-unsupported values, effects, and owners end at `adapter_or_bridge/UNSUPPORTED_CONTENT`;
2. C adds source validation, lexical selection state, ref dereferencing/fresh copying, support-view consistency, and manifest/context interpretation checks relative to direct typed paths;
3. the most brittle component is the exact ASCII-space grammar and literal phrase-to-predicate linking.

These observations apply only to the frozen Phase 0 controlled language and are not comparative scientific claims.

## Acceptance status

Main accepts exactly the implementation range ending at `fb4be7c36ae3b8175c39364aa446c82f9f2a5d87`. E3 is complete. Evidence remains limited to Phase 0/F9 and does not establish general natural-language compilation quality.

No E4 handoff is created by this acceptance record. E4 may now be generated just in time from the accepted E3 interfaces and findings, then must receive its own contract review before dispatch.
