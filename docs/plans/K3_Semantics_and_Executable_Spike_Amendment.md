# K3 semantic-plugin and executable-spike plan amendment

> Status: amendment candidate authorized by the user on 2026-08-29. It grants no stage dispatch or mutation authority until independently reviewed and accepted.

## 1. Authority and reason for the amendment

This amendment supplements the accepted
`Contract_IR_Kernel_and_Coding_Plugin_Research_Plan.md`, exact accepted blob
`01f959bc55f644a376f8ffa6059e9e77936be77c`. It changes only the route after
the accepted K2 result:

- accepted K2 result commit:
  `5b6f157a0b374362c1362f239ec45f4050c6b1b0`;
- accepted K2 deliverable blob:
  `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`;
- K2 acceptance commit:
  `08bcd9b87153360234efe0d52754daf2bfbcae4d`.

The accepted plan made K3 semantic-only and deferred every executable checker
until after K4. K2 is now a large transport-neutral logical specification.
Review can establish internal coherence, but cannot by itself show that a
finite, useful vertical slice can be constructed without an ambiguous rule,
undefined ordering, accidental cycle, or hidden fallback. The user therefore
authorized two ordered steps: first freeze a minimal coding plugin, then
implement a toy kernel plus that exact toy plugin as a feasibility probe.

All K0--K2 semantics and acceptance boundaries remain unchanged unless the
probe exposes a contradiction. K4 remains the held-out semantic assessment.

## 2. Revised progressive stages

The original K3 row is replaced by two sequential stages:

| Stage | Objective | Exit question |
|---|---|---|
| K3-S | Define the smallest coding-plugin semantic profile against accepted K1/K2 | Can the selected coding challenges be represented without a coding-specific kernel branch or hidden expected answer? |
| K3-X | Implement one finite executable vertical slice of the accepted K2 ABI and exact K3-S profile | Can the selected records, validation order, lifecycle, plugin calls, and failures be constructed and reproduced without inventing semantics? |
| K4 | Perform the already planned held-out semantic closure and manual natural-language-to-Contract binding assessment | What remains unrepresentable, unresolved, ambiguous, or only capability-relative? |

Only the next unaccepted stage may have a concrete handoff. K3-X receives no
handoff, path, or mutation authority until K3-S is independently reviewed and
accepted. K4 receives none until both K3 stages are accepted.

## 3. K3-S boundary

K3-S is semantic design, not implementation. It must define a deliberately
small coding plugin using accepted K2 records and ownership rules. Its challenge
scope must exercise at least:

- an abstract repository pre-state and final-state;
- a typed path and file-content observation;
- a finite change set over those states;
- an abstract command or test event in the trace;
- verification evidence attached to, but not substituted for, a truth result;
- one broad task-acceptance predicate with an explicit access, evidence,
  unknown, and error contract;
- one forbidden trace condition and one separately authorized trace condition;
- one missing/incompatible symbol or version;
- one plugin-visible contradiction and one deliberately unresolved judgment.

The plugin may use generic state, observation, change, event, and evidence
concepts. `FIX_BUG`, `ADD_FEATURE`, `REFACTOR`, benchmark labels, gold patches,
and expected outputs are not kernel or plugin primitives. No predicate may read
a hidden answer or undeclared field.

K3-S must provide exact symbol identities, versions, types, meanings,
dependencies, model contracts, capability/trust requirements, failure
behavior, a relative-minimality ledger, challenge bindings, and explicit
`UNREPRESENTABLE` or `UNKNOWN` outcomes where appropriate. It may expose a K2
defect; it may not silently repair one inside the coding plugin.

## 4. K3-X executable exception

K3-X is the sole exception to the original plan's pre-K4 implementation ban.
It may implement only a finite reference profile needed to execute the accepted
K3-S fixtures. The permitted vertical slice is:

- direct in-memory construction of the required K2 ABI records;
- exact structural identities, including owner namespace and declaration kind,
  and exact version matching for the selected records;
- declaration, binding, semantic-dependency, validation-reference, lookup,
  lifecycle, capability, trust, invocation, result, and failure checks used by
  the selected fixtures;
- a toy coding plugin implementing only the accepted K3-S types, functions,
  predicates, event meanings, and evidence schemas;
- pure in-memory `PRE`, `TRACE`, `FINAL`, and `EVIDENCE` values and state
  transitions for deterministic tests;
- deterministic conformance fixtures and a traceability matrix from each
  implemented branch to exact K2/K3-S clauses.

K3-X must not add a parser, natural-language compiler, planner, search
algorithm, patch generator, real repository mutation, filesystem-backed coding
operation, operating-system command execution, network access, model training,
model inference, prompt search, benchmark, deployment mechanism, or performance
claim. It must not define a general serialization or claim complete
implementability of extensional K2 relations. Test values are finite logical
fixtures, not hidden oracle answers.

The prototype may choose a simple internal representation, but representation
choices have no semantic authority. If two possible implementations would
produce different K2/K3-S judgments because the specification does not fix the
answer, the stage stops and returns the ambiguity to the owning semantic stage.

## 5. K3-X required executable checks

The accepted handoff must select the smallest fixture set that covers all of
the following:

1. a well-formed, closed, evaluable coding Contract whose final-state and test
   evidence constraints evaluate `TRUE`;
2. independently constructed, structurally equal identities must coalesce;
   identities with identical display/local atoms but different owner/plugin
   namespaces or declaration kinds must remain distinct; forcing two kinds
   under one exact key must reject as a kind conflict;
3. the same semantic meaning with exact version agreement and a
   version-mismatch rejection with no fallback;
4. declaration present versus binding absent versus capability absent;
5. semantic proper dependencies separated from mandatory validation
   references, including rejection of a genuine semantic cycle;
6. five separate trust fixtures: admitted, absent, undecided, incompatible,
   and failed. They must project respectively to usable service, exact missing
   status, `EVALUABILITY_UNKNOWN`, `EVALUABILITY_MISSING`, and the matching
   discovery protocol/transport failure, with no fabricated logical, profile,
   or reasoning result;
7. plugin result `FALSE`, logical `UNKNOWN`, evaluation error, reasoning error,
   and malformed result kept distinct where the selected profile supports them;
8. forbidden versus authorized trace events without converting evaluability
   into authority;
9. at least two valid dependency topological orders must produce identical
   complete observation maps, results, and statuses; at least two package and
   record permutations must do the same;
10. independently constructed equal duplicates must coalesce, while unequal
    records at one exact identity must conflict, independent of input order;
11. exact missing-record statuses for the selected record kinds;
12. deterministic replay of every fixture from a clean committed source tree;
13. a negative fixture proving that undeclared repository, evidence, or hidden
    expected-answer access is rejected.

No fixture may special-case its challenge ID in production logic. Expected
statuses are test assertions derived from cited semantic clauses, not inputs to
the evaluator.

## 6. Acceptance and return conditions

K3-S is accepted only if its coding vocabulary is typed, versioned, minimal
relative to its challenge set, K2-conformant, and free of hidden oracle access.
Its acceptance cannot claim executable feasibility.

K3-X is accepted only if:

- it implements only the accepted finite profile and every implemented branch
  has exact semantic traceability;
- targeted tests cover every required check and pass from a clean committed
  source tree;
- malformed, missing, unknown, incompatible, failed, and false results remain
  distinguishable;
- the implementation contains no fixture-ID branch, fallback symbol/version
  selection, undeclared access, or embedded expected result;
- an independent implementation review finds no mismatch with accepted K2 and
  K3-S;
- every check in section 5 is implemented; its report separately states exactly
  which other K2/K3-S branches were not implemented.

Stop K3-S and return to K2 if the coding profile requires a new kernel meaning,
redefines a K1 status, or cannot use the accepted ABI without ambiguity. Stop
K3-X and return to K2 or K3-S if implementation requires choosing an unspecified
semantic result, changing an accepted identity/dependency/trust rule, or using a
hidden fixture mapping. Ordinary implementation bugs are repaired within K3-X
and independently reviewed before acceptance.

## 7. Allowed conclusions

Passing K3-S may establish only semantic representability for its accepted
coding challenge scope. Passing K3-X may additionally establish that one
explicitly enumerated finite vertical slice is executable and reproducible.

Neither stage establishes complete K2 implementability, universal coding-task
coverage, correctness of natural-language translation, real repository safety,
planner or coding-agent performance, operational proof-system completeness, or
a benefit over another IR. Held-out adequacy remains reserved for K4.

## 8. Provenance and review

- Versioned plans, handoffs, source, fixtures, tests, reports, and review
  records are committed to Git without rewriting reviewed history.
- Every review binds an exact commit or range. The accepted K3-X mutation
  handoff binds the exact accepted base commit and sole allowed mutation paths;
  it cannot name the future implementation commit.
- After the implementation is frozen in a new commit and passes independent
  read-only implementation review, main must issue a separate exact execution
  binding before acceptance evidence is generated. That binding names the
  clean implementation commit, exact test commands, committed fixtures,
  permitted output/report destinations, and expected non-side-effect boundary.
  The final report and result review bind that same execution commit. Developer
  test runs before this gate are diagnostic only and cannot support the stage
  acceptance claim.
- Only one delegated writer may hold a mutation lease. Main freezes changes
  before independent review and owns acceptance and commit gates.
- No untracked or ignored input may affect a K3-X result. No external artifact
  is required by this amendment.
- This amendment grants no handoff or mutation authority by itself.
