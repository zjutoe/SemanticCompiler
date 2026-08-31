# K3-X implementation review

- Verdict: `REJECT`
- Reviewed range: `4f964dc1e0b3f3466f8241cb488d3c5e81e5a667..4836322fa23d4f91bbc1fd78b9b039101b7875a3`
- Implementation commit: `4836322fa23d4f91bbc1fd78b9b039101b7875a3`
- Accepted handoff blob: `889c8bf6fd028d4d51d47642b277715b397d9d1e`
- Accepted K3-S blob: `31e9ffbaedcf7c1531a0a614078479f7cfefb1fe`
- Accepted K2 blob: `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`
- Review mode: independent strict read-only implementation audit

## Decision

The first implementation is rejected and is not eligible for an execution
binding. Its 13 tests and 102 replays pass, but they do not yet demonstrate that
the accepted K2/K3-S records determine the results.

## Blocking findings

1. Replay trusts decisive fields already embedded in request objects. Removing
   the authoritative records and packages from core, pair, admitted-trust, and
   cycle fixtures still produces their expected decisions. Typed requests must
   instead reference records and environments whose resolved contents derive
   formation, closure, evaluability, trust, admission, and dependency results.
2. The 102 fixtures summarize rather than construct the accepted K3-S packet.
   Missing rows use generic carrier pairs and hard-coded status families; the
   cycle graph is supplied rather than mechanically derived; duplicate, pair,
   trust, confluence, and permutation fixtures omit required literal context.
   Port the exact row-local universes and reconstructed containers and remove
   status-by-kind shortcuts.
3. The coding plugin uses open strings and generic tuples rather than the
   accepted closed tagged values. Observation drops absent and wrong-role
   selections; criterion tags are admitted incorrectly; profile error and
   coverage projection are wrong; duplicate event fields use last-writer
   behavior. Implement the exact admission and total K3-S equations.
4. Validators omit decisive descriptor/model/package fields, and tests do not
   falsify many branches claimed by traceability. Complete the exact field
   projections and add independent negative assertions for every claimed
   semantic branch.

## Verified properties

The reviewer verified the exact clean six-path range, blobs, sizes, final
newlines, and `git diff --check`. The in-memory syntax check and all 13 tests
pass, and the fixture family arithmetic is exactly 102 with identical fixture
and expected-map domains. Production modules contain no fixture ID, challenge
ID, expected-map reference, forbidden ambient import, or external call;
composition itself is order-independent.

The pre-existing ignored `.ruff_cache/` was neither read nor modified and is
not an implementation-review blocker. A later evidence run must use an isolated
clean checkout or explicitly exclude it from the input boundary.

## Repair boundary

Repair remains limited to the accepted six implementation paths. K1, K2, K3-S,
the handoff, evidence report, held-out data, K4, external access, and real
repository/process behavior remain out of scope. Freeze the repair in a new
commit and obtain another independent implementation review before creating an
execution binding.
