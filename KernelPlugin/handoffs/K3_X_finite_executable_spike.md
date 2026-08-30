# K3-X handoff — finite executable kernel and coding-plugin spike

> Status: candidate handoff created just in time after accepted K3-S. It grants
> no mutation or execution authority until independently reviewed, accepted,
> and separately bound by main.

## 1. Frozen authority and stage boundary

- Handoff base commit: `8cbd9463c3d3c30508ce5bed96d7792beb9bed2f`
- Accepted K3-S result commit:
  `ced9082aa1494c30f5458d1bffc2eee04b3bbc37`
- Accepted K3-S blob: `31e9ffbaedcf7c1531a0a614078479f7cfefb1fe`
- K3-S acceptance-record blob:
  `f3b025bef8ef93bb8433bcc1de6e7bc1ad65fe3e`
- Accepted K3-S handoff blob:
  `f3019df041df07da1bfef6f92858bacdc7f4ab9d`
- Governing amendment blob:
  `7f1c3627245ec0c0fc86df64f77e374d104649a0`
- Accepted K2 blob: `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`
- Accepted K1 blob: `d928010319c2c3bd08a94e1856cfca24dc2ae39e`
- Accepted K0 blob: `e86e184300a6620fb6fe25062635d9bc7cb410a1`
- Governing plan blob: `01f959bc55f644a376f8ffa6059e9e77936be77c`
- Held-out prerequisite: opaque receipt `K1-HO-GATE-20260828-A`
- Stage: `K3-X`
- Predecessor: accepted K3-S
- Successor: K4, which remains undispatched

K3-X asks one question: can the exact finite K2/K3-S slice already accepted be
constructed and replayed without inventing a semantic rule? It is a feasibility
probe, not a general Contract IR implementation.

## 2. Sole mutation lease and exact paths

One delegated writer may create or modify only these paths:

```text
KernelPlugin/k3x/__init__.py
KernelPlugin/k3x/reference.py
KernelPlugin/k3x/coding_plugin.py
KernelPlugin/k3x/fixtures.py
KernelPlugin/k3x/test_reference.py
KernelPlugin/k3x/TRACEABILITY.md
```

All paths must be committed source or documentation. No generated cache,
coverage file, temporary result, external dataset, model file, or ignored input
may enter the evidence boundary. The writer does not commit. Any needed path,
dependency, semantic branch, or fixture outside this list stops the stage and
returns to main.

The implementation uses Python 3 and only the standard library. It may use
frozen dataclasses, enums, tuples, frozensets, and pure functions. It must not
add a package dependency, build system, serialization format, command-line
interface, service process, or configuration layer.

## 3. Explicitly permitted implementation slice

`reference.py` implements only the K2 operations exercised by the accepted
K3-S packet:

1. exact structural identity with owner/plugin namespace, kind, and exact
   version components;
2. immutable logical records and record identities needed by the packet;
3. order-independent composition: equal complete records coalesce, unequal
   complete records at one exact identity produce an exact conflict, and no
   later record wins;
4. package/owner, declaration shape, type-admission, binding, model-summary,
   ContractSpec role/support, dependency, validation-reference, and exact
   version checks used by the fixtures;
5. finite proper-dependency graph validation, cycle rejection, deterministic
   topological evaluation, and exact complete observation maps;
6. exact record lookup and the 42 accepted `missingStatus` branches;
7. the five accepted trust states and their distinct lifecycle/evaluability
   projections;
8. capability discovery, exact target and fragment matching, invocation/result
   equality, canonical malformed-result and failure separation, and the packet
   lifecycle transitions;
9. exact per-entry replay of the accepted 102-entry tagged packet.

The module does not implement every K1/K2 constructor. Unsupported constructors
fail loudly with an explicit `NotImplementedError` or a typed finite-profile
rejection before a semantic judgment is returned. It contains no fixture ID,
challenge ID, expected-status table, or branch on test names.

`coding_plugin.py` implements only the accepted K3-S closed value algebra and
the exact finite meanings exercised by the packet:

- `snapshot_of`, `changes_between`, and `observe`;
- `observations_equal`, `verification_passed`, `task_accepts`,
  `dependency_metadata_changed`, `event_matches`, `event_occurred`, and
  `refresh_scope`;
- implementation-evidence profile projection;
- the accepted event/evidence/value admissions and total observation/evidence
  projections.

Every function consumes only its explicit typed arguments and the lower
observation map authorized by its ContractSpec. It performs no filesystem,
process, environment, network, clock, randomness, import-time discovery, or
hidden global-state access.

`fixtures.py` directly constructs the accepted finite records. It must expose
the exact closed `FixtureId` algebra and exactly 102 self-contained entries:

```text
1 CORE_DEFINITIONAL
1 PAIR_INDEPENDENT
5 TRUST_BRANCH
42 MISSING_BASE
42 MISSING_VARIANT
2 CONFLUENCE_ORDER
1 PROPER_CYCLE_REJECTION
4 PERMUTATION
2 DUPLICATE_EQUAL
2 DUPLICATE_CONFLICT
```

Fixture construction may contain expected values only in a separately named
test-assertion map. The kernel and coding-plugin modules may not import that
map. No fixture may use an expected result as evaluator input.

## 4. Required executable checks

`test_reference.py` must define exactly these thirteen top-level test methods,
named `test_k3x_01_...` through `test_k3x_13_...`, in this order:

1. construct one well-formed, closed, evaluable coding Contract whose exact
   final-state and verification constraints return `TRUE`;
2. coalesce independently constructed equal identities, preserve distinct
   owner/plugin/kind identities, and reject an unequal kind at one exact key;
3. accept exact semantic-version agreement and reject a version mismatch with
   no fallback;
4. distinguish declaration present, binding absent, and capability absent;
5. retain mandatory validation references outside the proper DAG, admit the
   independent pair proof, and reject the tagged genuine proper cycle;
6. replay admitted, absent, undecided, incompatible, and failed trust fixtures
   to usable service, exact missing, `EVALUABILITY_UNKNOWN`,
   `EVALUABILITY_MISSING`, and discovery protocol/transport failure without a
   fabricated result;
7. keep plugin `FALSE`, logical `UNKNOWN`, evaluation error, reasoning error,
   and malformed result distinct;
8. distinguish forbidden and authorized trace events without converting
   evaluability into authority;
9. produce identical complete observation maps/results/statuses for both valid
   dependency orders and identical composition for all four package/record
   permutations;
10. coalesce equal duplicates and produce the same exact conflict for unequal
    duplicates in both input orders;
11. assert all 42 base records present and all 42 variants have the exact
    accepted missing-status family;
12. replay all 102 tagged fixtures, asserting exact equality to the separate
    expected-output map and asserting the map domains are identical;
13. reject attempted undeclared repository, evidence, or hidden
    expected-answer access before using a truth result.

Tests may share pure construction helpers but no test may call a production
function with its expected status, expected truth, fixture ID, or challenge ID.
Check 12 must call the same public replay operation used by the other tests.

## 5. Exact semantic invariants

The implementation and tests must preserve these non-negotiable boundaries:

- formation, closure, evaluability, lifecycle, logical truth, profile result,
  authority, and admission remain separate typed coordinates;
- false, unknown, evaluation failure, reasoning failure, malformed input,
  missing input, incompatibility, and discovery failure never collapse;
- exact version equality is required; there is no newest, compatible-looking,
  alias, first-found, or fallback selection;
- service availability never creates a declaration or meaning, and a meaning
  never creates a service or trust root;
- model capability summaries and descriptors agree bidirectionally;
- semantic proper dependencies, validation references, package ownership, and
  producer/trust independence remain distinct;
- cycle rejection uses mechanically derived proper support, not a synthetic
  fixture flag;
- duplicate/conflict behavior depends only on complete record equality and
  exact identity, never input order;
- evidence may support a result but never substitutes for truth or authority;
- abstract satisfying witnesses and profile completeness remain distinct;
- no coding operation mutates a real repository or executes a real command.

Any ambiguity for which two reasonable implementations yield different
K1/K2/K3-S judgments is a stop condition. The writer must report the exact
clause and competing results rather than choosing one.

## 6. Traceability requirement

`TRACEABILITY.md` must contain:

- one row for each of the thirteen checks;
- the exact production function(s), fixture constructor(s), and test method;
- exact accepted K2 section(s) and K3-S section/record(s);
- the expected status/result and the implemented failure branch;
- an exhaustive list of K2/K3-S branches intentionally not implemented.

Every nontrivial conditional in `reference.py` and `coding_plugin.py` must map
to at least one traceability row. Representation-only helpers need not receive
a semantic claim.

## 7. Forbidden scope

K3-X must not add or perform:

- natural-language parsing, source binding, prompting, model inference or
  training, planning, search, patch generation, or benchmark evaluation;
- real repository, filesystem, process, shell-command, network, service,
  database, clock, randomness, concurrency, retry, or deployment behavior;
- a general K1/K2 serializer, loader, plugin discovery protocol, proof system,
  or claim that arbitrary extensional relations are computable;
- challenge-specific production branches, embedded expected decisions, golden
  patches, expected outputs, or hidden fixture maps;
- performance, completeness, universal coding adequacy, natural-language
  correctness, or real-agent safety claims;
- K4 handoff, held-out content, external artifacts, or downstream authority.

`pathlib`, `os`, `subprocess`, `socket`, networking libraries, dynamic import,
`eval`, `exec`, randomness, and time APIs are forbidden in the four Python
implementation/test modules unless the reviewer establishes a standard-library
test-discovery-only use with no semantic visibility. Prefer not to import them.

## 8. Diagnostic verification before freeze

The writer must run, from the clean bound base plus its one-path-set diff:

```text
python -m unittest KernelPlugin.k3x.test_reference -v
python -m compileall -q KernelPlugin/k3x
git diff --check
git diff --name-only
git status --short
```

It must also report:

- exactly 13 required test methods and their pass count;
- exactly 102 fixture IDs and 102 expected-output keys;
- exactly 42 missing-base and 42 missing-variant entries;
- zero production references to fixture IDs, challenge IDs, or expected maps;
- zero forbidden imports/calls;
- exact line/byte counts and Git blob IDs for every allowed file;
- no untracked or ignored input outside the six allowed paths.

These runs are diagnostic only. They are not K3-X evidence and cannot support
acceptance before the separate execution binding in section 10.

## 9. Freeze and implementation review gate

Main freezes the completed six-path implementation in a commit before review.
The independent read-only implementation reviewer receives only the accepted
handoff, exact implementation commit/range, six file blobs, diagnostics, and
governing K2/K3-S blobs. It must review:

- semantic/implementation consistency for every implemented branch;
- absence of fixture-ID logic, hidden expected inputs, ambient access, version
  fallback, last-writer behavior, or unimplemented branch masquerading as a
  semantic result;
- exact packet construction, deterministic composition, dependency/cycle,
  trust, lifecycle, result, and missing-status behavior;
- test independence and whether assertions actually falsify incorrect
  implementations;
- traceability completeness and overclaim boundaries.

Review findings are repaired only in the six paths, committed as new history,
and independently re-reviewed. Main accepts the implementation only after a
decisive review with no blocker.

## 10. Separate execution binding and result gate

Implementation acceptance does not authorize an evidence run. Main must next
create and commit a separate exact K3-X execution binding that names:

- the accepted clean implementation commit and every implementation/test blob;
- the exact Python executable identity available in the repository environment;
- the exact two test/compile commands;
- the committed fixture and expected-output constructors;
- the sole report destination
  `docs/reports/kernel_plugin/K3_X_Executable_Spike_Report.md`;
- no other output root, external input, network, held-out access, or side
  effect.

The evidence run must start from the clean committed binding state, verify the
bound implementation blobs, execute each command once, and write only the
report. The report records command exit status, all 13 checks, packet counts,
source/binding provenance, intentionally unimplemented branches, and the
limited allowed conclusion. Main freezes the report and obtains an independent
final result review before accepting K3-X.

## 11. Acceptance and allowed conclusion

K3-X is acceptable only if:

- all thirteen checks and all 102 tagged replays pass from the exact bound
  clean source;
- the independent implementation review and final result review find no
  semantic mismatch, leakage, hidden oracle, or unsupported claim;
- every malformed, missing, unknown, incompatible, failed, false, authority,
  and profile distinction above remains observable and exact;
- the report names every unimplemented K2/K3-S branch and all exact provenance;
- no unauthorized path, input, artifact, external access, or side effect
  occurs.

Passing K3-X establishes only that the accepted, explicitly enumerated finite
K2/K3-S vertical slice is executable and reproducible. It does not establish
complete K2 implementability, universal coding semantics, natural-language
translation correctness, real repository safety, planner performance, or a
benefit over another IR.

This handoff creates no K4 authority. Any K4 handoff remains just-in-time after
accepted K3-X and separate user authorization where required.

## 12. Writer return packet

The writer returns:

1. base commit and all six final blob IDs and sizes;
2. concise architecture and semantic-branch map;
3. exact diagnostic commands and exit summaries;
4. the 13/102/42/42 counts and traceability coverage;
5. forbidden-import, hidden-fixture, path-scope, diff, and EOF checks;
6. every intentionally unimplemented branch;
7. any ambiguity or stop condition;
8. confirmation of no commit, external artifact, held-out access, or
   unauthorized mutation.

