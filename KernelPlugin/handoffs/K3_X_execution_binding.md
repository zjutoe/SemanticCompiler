# K3-X finite executable spike: exact execution binding

Status: `REVIEW_CANDIDATE`. This document grants no execution authority until
its exact committed version and the execution-command amendment are
independently accepted and main separately dispatches that accepted binding.

The normative command isolation and early-failure rules are amended by
`KernelPlugin/handoffs/K3_X_execution_command_amendment.md`.

## 1. Bound accepted implementation

- accepted implementation commit: `326a57f23ba2934f9cb27d0cd5380643325c1a52`
- implementation acceptance commit: `dd167e98d70deecb48ca912e678ca22cc7c7e5d5`
- accepted implementation review:
  `docs/reviews/kernel_plugin/K3_X_Implementation_326a57f_review.md`
- governing K3-X handoff blob:
  `889c8bf6fd028d4d51d47642b277715b397d9d1e`
- governing K3-S blob:
  `31e9ffbaedcf7c1531a0a614078479f7cfefb1fe`
- governing K2 blob:
  `1ea0d9fb014bf983c4c84f35e0c88590bd9e9ab4`

The six accepted implementation/test blobs are:

| Path | Git blob |
|---|---|
| `KernelPlugin/k3x/__init__.py` | `a102ff21b6de7c3bedaffd75ee9f84af831c85a2` |
| `KernelPlugin/k3x/reference.py` | `ec6fe703248a1ff8ba2977b25280d8fc2fd65862` |
| `KernelPlugin/k3x/coding_plugin.py` | `55dc9d587f054a8f476191e72e60519ebd155f40` |
| `KernelPlugin/k3x/fixtures.py` | `5c0aab81abf478768232b9b796f91074491ad9df` |
| `KernelPlugin/k3x/test_reference.py` | `d4488cc1347a8173378e7a83b19f3d031cd8cc95` |
| `KernelPlugin/k3x/TRACEABILITY.md` | `284f9ed3a2eae9fc04c8e51f01fa501e6869383e` |

Any mismatch is a stop condition. No source repair is authorized by this
binding.

## 2. Bound runtime

- executable: `/opt/anaconda3/bin/python`
- executable SHA-256:
  `8f463543ee031f1c8804f869624bebcf3927c56d3e30b3217b4489a31d01ac32`
- version: `3.13.9 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 19:16:10) [GCC 11.2.0]`
- working directory: `/home/mye/src/llm/SemanticCompiler`
- empty-environment launcher: `/usr/bin/env`
- launcher SHA-256:
  `190c360452d515eac29236055581587f162d5b53f56104df169fc51d5c4661c9`
- Python-visible environment: exactly `LC_ALL=C.UTF-8`, `LANG=C.UTF-8`

Main's later dispatch must name one exact execution `HEAD` containing the
accepted binding and amendment. Preflight must require that exact `HEAD`; an
arbitrary descendant is forbidden. The pre-existing ignored repository-root `.ruff_cache/` is explicitly
excluded from all inputs and must not be read, changed, copied, hashed, or
reported as evidence. Its presence does not authorize an isolated checkout or
another output root.

## 3. Bound constructors and domains

The committed fixture constructor is
`KernelPlugin.k3x.fixtures._build_fixture_packet`, exposed read-only by
`fixture_packet()`. The committed independent expected constructor is
`KernelPlugin.k3x.fixtures._build_expected_assertions`, backed by the static
`_EXPECTED_REPLAY_ASSERTIONS_LITERAL` and its complete immutable node graph.

The expected finite domains are exactly:

- 13 top-level unittest methods;
- 102 fixture IDs and 102 expected assertion keys;
- 42 missing-base and 42 missing-variant entries;
- 3,740 reachable complete-value assertion nodes.

No fixture, expected assertion, unlisted environment variable, ignored file, external
artifact, or held-out content outside these committed records is an input.

## 4. Exact evidence commands

After verifying the source commit, six blobs, runtime path, runtime hash, clean
tracked/untracked status, and absence of K3-X cache files, execute each command
exactly once and in this order:

```text
/usr/bin/env -i LC_ALL=C.UTF-8 LANG=C.UTF-8 /opt/anaconda3/bin/python -E -S -B -m unittest KernelPlugin.k3x.test_reference -v
/usr/bin/env -i LC_ALL=C.UTF-8 LANG=C.UTF-8 /opt/anaconda3/bin/python -E -S -B -c "import ast, pathlib; paths = ('KernelPlugin/k3x/__init__.py', 'KernelPlugin/k3x/reference.py', 'KernelPlugin/k3x/coding_plugin.py', 'KernelPlugin/k3x/fixtures.py', 'KernelPlugin/k3x/test_reference.py'); [ast.parse(pathlib.Path(path).read_text(encoding='utf-8'), filename=path) for path in paths]"
```

The exact launcher, fixed environment, and `-E -S -B` are mandatory. The syntax command parses the five exact Python files
in memory and writes nothing. Neither command may be retried, filtered, wrapped
by another launcher, or replaced after failure. A nonzero exit is evidence and
a stop condition, not repair authority.

## 5. Sole output and report content

The sole authorized write, whether preflight/command execution succeeds or
fails, is:

`docs/reports/kernel_plugin/K3_X_Executable_Spike_Report.md`

On success, the report must record:

- this binding commit and the accepted implementation commit;
- all six source blobs and the Python executable identity/hash/version;
- each exact command reached, one execution, exit status, and concise result;
- every later command not reached after failure, recorded as `NOT_RUN`;
- all thirteen named checks and their pass/fail status;
- the exact 102/102, 42/42, and 3,740-node counts;
- confirmation that the tracked worktree was clean before execution and only
  the report became modified/untracked afterward;
- confirmation of no K3-X cache/bytecode, network, external input, held-out
  access, ignored-input use, retry, or other output;
- the intentionally unimplemented branches copied from the accepted
  `TRACEABILITY.md` boundary;
- only this conclusion: the accepted explicitly enumerated finite K2/K3-S
  vertical slice executed reproducibly under the bound runtime.

On reportable preflight or command failure, the report instead records:

- the exact mismatch or failing command and its exit status/output summary;
- reached commands exactly once and later commands/checks as `NOT_RUN`;
- unavailable counts as `NOT_VERIFIED`;
- actual pre/post worktree status and any observed unauthorized output;
- no positive reproducibility or scientific conclusion.

If the report path exists or is dirty at preflight, write nothing and return the
conflict to main; overwriting or appending is forbidden.

The report must not claim complete K2 implementability, universal coding
semantics, natural-language translation correctness, real-repository safety,
planner performance, or superiority over another IR.

## 6. Forbidden scope and stop conditions

This binding authorizes no source edit, cache creation, dependency installation,
filesystem/process/network semantics, model call, benchmark, serialization,
external artifact, held-out access, K4 work, additional report, or commit by the
operator. It does not authorize changing this binding.

If any bound commit, blob, executable/launcher, hash, accepted binding/amendment
blob, command, environment, path, constructor, domain, clean-state condition,
or side-effect boundary does not match, run no evidence command and use the
failure schema when the report path is absent. Stop after the first command
that fails or creates an unauthorized output, and write only the failure report
with later commands marked `NOT_RUN`.

## 7. Result gate

Main freezes the sole report in a commit. A fresh GPT-5.6 Sol high agent then
reviews the accepted binding, exact report commit/range, source/runtime
provenance, command-once record, counts, absence of side effects, and limited
conclusion. K3-X is accepted only after that independent result review returns
`ACCEPT` with no blocker. This binding creates no K4 authority.
