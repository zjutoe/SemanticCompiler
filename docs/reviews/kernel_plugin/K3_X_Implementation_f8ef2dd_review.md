# K3-X implementation repair 5 review

- Verdict: `REJECT`
- Reviewed range: `98bc2b34dcd19c3ef8ec68e8e0bb646ffb3ba2ef..f8ef2dd1ddd142a9f6ce8d64317998565191f5d2`
- Repair commit: `f8ef2dd1ddd142a9f6ce8d64317998565191f5d2`
- Accepted handoff blob: `889c8bf6fd028d4d51d47642b277715b397d9d1e`
- Prior rejection-record blob: `e21a71cc06908abf783c2e84fb2cee6e95350509`
- Accepted K3-S blob: `31e9ffbaedcf7c1531a0a614078479f7cfefb1fe`
- Accepted K2 blob: `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`
- Review model: `gpt-5.6-sol`, reasoning effort `high`
- Review mode: fresh independent strict read-only implementation audit

## Decision

Repair 5 is rejected and remains ineligible for an execution binding. It adds
standalone pair admission/results, typed confluence and evolution values, a
field-sensitive admission framework, and an acyclic-before-cyclic construction.
Several nested membership and exact-link checks remain incomplete.

## Blocking findings

1. Closed admission still accepts invalid nested values: untyped `PathSet`
   members and `SubjectId` fields, missing `OtherArtifactRole`/`OtherFormat`,
   collapsed string wrappers, and empty behavior conflicts.
2. Pair lacks the complete literal type/literal closure and exact independent
   admission constructor. Evidence issuer/identity and each trust/root producer
   coordinate are not independently required.
3. Both confluence bindings are individually malformed due to facet mismatch,
   yet graph replay succeeds. The package remains reduced, policy owner is inert,
   and the frozen unknown-reason subjects are represented incorrectly.
4. The cycle baseline remains a reduced 29-declaration/five-binding/five-model
   reconstruction rather than an exact retained `PKG_CK` differential with all
   non-cycle records unchanged.
5. Evolution ignores envelope fragment/abstraction class, exact evidence
   identity, and referenced trust-policy presence; generic request/result
   carriers still collapse distinct row protocols.
6. Traceability and several tests claim stronger literal and field coverage
   than they falsify.

## Verified progress

Exact provenance, blobs, sizes, five-path repair scope, clean worktree,
`git diff --check`, final newlines, AST parsing, 13/13 tests, 102/102 domains,
and 42/42 missing families pass. Standalone pair admission/result records,
typed pair/confluence/evolution values, exact full missing-coordinate identities,
result protocol, extensional maps, four-equation verification, typed conflict,
and production-oracle exclusion remain intact.

No evidence run, report, artifact, cache, held-out content, or external access
occurred.

## Repair boundary

Repair 6 remains confined to the six implementation paths. Complete every
closed-type nested membership predicate; port the full pair closure and exact
evidence/producers; make confluence nodes individually valid and consume exact
policy/reason coordinates; construct cycle variants as literal differentials of
the complete retained package; validate every evolution envelope/evidence/policy
link with distinct requests/results; and narrow tests/traceability to real
falsifiers. K1/K2/K3-S, handoff, report, K4, real operations, and held-out
content remain out of scope.
