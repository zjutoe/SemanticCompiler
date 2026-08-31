# K3-X implementation repair 4 review

- Verdict: `REJECT`
- Reviewed range: `287404be3fe615b3cfaf87c0651a854aa8d9c15e..8108451a61941e7453c4d377e7af32f58fb640ea`
- Repair commit: `8108451a61941e7453c4d377e7af32f58fb640ea`
- Accepted handoff blob: `889c8bf6fd028d4d51d47642b277715b397d9d1e`
- Prior rejection-record blob: `be2ed64aa71f1ad016f7b6473b458b44f05ac9ab`
- Accepted K3-S blob: `31e9ffbaedcf7c1531a0a614078479f7cfefb1fe`
- Accepted K2 blob: `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`
- Review model: `gpt-5.6-sol`, reasoning effort `high`
- Review mode: fresh independent strict read-only implementation audit

## Decision

Repair 4 is rejected and remains ineligible for an execution binding. It closes
exact 42-coordinate identity matching, rooted type dependencies, substantially
fuller pair/confluence/cycle/evolution structures, and their principal removal
tests. Five remaining paths still admit malformed or inert protocol data.

## Blocking findings

1. Type admission still checks a constructor tag stored in the ContractSpec,
   not the exact field-sensitive finite membership relation. A forged
   `TaskSpec` payload containing an arbitrary object is admitted.
2. Pair request data embeds certificate-admission and result values instead of
   resolving standalone records. Exact validator identities, occurrence
   binding/bundle distinction, model signatures/facets, and capability
   dependency scope remain incomplete or unvalidated.
3. Confluence still uses surrogate observation nodes and untyped reasoning
   results. Removing its service or corrupting root owner, certificate kinds,
   and adoption leaves evaluation successful.
4. The cycle has complete type admission but still omits the full retained
   service-free package, declarations, bindings, environments, and explicitly
   required cycle-model variants. The cycle has not been isolated against the
   complete frozen acyclic baseline.
5. Evolution proof dispatch still uses row strings/local names, and validation
   omits admitted-root equality, trusted validators, certificate kinds, owner,
   adoption, service/fragments/evidence, producer independence, admission, and
   receiving result.

## Verified progress

Exact provenance, blobs and sizes, four-path repair scope, clean worktree,
`git diff --check`, final newlines, AST parsing, 13/13 tests, 102/102 domains,
and 42/42 missing families pass. Full target/consumer/replacement/context
identity matching now rejects same-local foreign owner, namespace, and version.

Earlier result-protocol, non-admitted-result, closed-value, extensional-map,
four-equation verification, typed-conflict, and independent literal assertion
repairs remain intact. Production contains no fixture/challenge/assertion-map
reference or forbidden ambient access. No evidence run, report, held-out access,
or artifact was created.

## Repair boundary

Repair 5 remains confined to the six accepted implementation paths. Implement
exact finite field-sensitive type admission; remove answer-bearing pair request
fields and resolve exact admission/result records; consume complete confluence
service/trust/reasoning/lifecycle coordinates; reconstruct and compare the full
cycle baseline; and replace evolution row tags with exact typed subjects,
proofs, trust, admission, and result validation. K1/K2/K3-S, the handoff, report,
K4, real operations, and held-out content remain out of scope.
