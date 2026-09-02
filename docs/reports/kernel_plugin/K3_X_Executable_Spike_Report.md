# K3-X finite executable spike report

## Result

**PASS.** The accepted, explicitly enumerated finite K2/K3-S vertical slice
executed reproducibly under the bound runtime. This is the only conclusion
authorized by the execution binding.

## Provenance and preflight

- exact execution HEAD: `780e4b84ca8772b7b9eb42f265a68c24d5264bb8`
- accepted implementation: `326a57f23ba2934f9cb27d0cd5380643325c1a52`
- implementation acceptance: `dd167e98d70deecb48ca912e678ca22cc7c7e5d5`
- accepted execution binding: `e4054740931452129775132341c4c5475b888f9a`
- binding acceptance at execution HEAD:
  `docs/reviews/kernel_plugin/K3_X_Execution_Binding_e405474_review.md`
- binding blob at execution HEAD:
  `41aeaa561252abbb5ce111ac8dae34db4babad80`
- command-amendment blob at execution HEAD:
  `7d7badbbe525b2a203364b47023bdecea43c5919`

Accepted implementation blobs:

| Path | Git blob |
|---|---|
| `KernelPlugin/k3x/__init__.py` | `a102ff21b6de7c3bedaffd75ee9f84af831c85a2` |
| `KernelPlugin/k3x/reference.py` | `ec6fe703248a1ff8ba2977b25280d8fc2fd65862` |
| `KernelPlugin/k3x/coding_plugin.py` | `55dc9d587f054a8f476191e72e60519ebd155f40` |
| `KernelPlugin/k3x/fixtures.py` | `5c0aab81abf478768232b9b796f91074491ad9df` |
| `KernelPlugin/k3x/test_reference.py` | `d4488cc1347a8173378e7a83b19f3d031cd8cc95` |
| `KernelPlugin/k3x/TRACEABILITY.md` | `284f9ed3a2eae9fc04c8e51f01fa501e6869383e` |

Runtime boundary:

- operator shell: `/usr/bin/zsh`, version
  `zsh 5.9 (x86_64-redhat-linux-gnu)`, SHA-256
  `288d795a07cd3d2fbbd8f7ead127a5428153a02203f83bd19cda3b50b03cc697`
- operator mode: non-interactive, non-login, execution-substrate shell binary
- pre-start `HOME=/home/mye`; `ZDOTDIR` absent
- `/etc/zshenv`: 510 bytes, SHA-256
  `69ed780cdba8e32191af71649c8b7529f0aa1e83c28325dbfcd45d139eb3fbc2`
- `/etc/zshenv.zwc` and `/home/mye/.zshenv`: absent
- environment launcher: `/usr/bin/env`, version
  `env (GNU coreutils) 9.5`, SHA-256
  `190c360452d515eac29236055581587f162d5b53f56104df169fc51d5c4661c9`
- Python: `/opt/anaconda3/bin/python`, version
  `3.13.9 | packaged by Anaconda, Inc. | (main, Oct 21 2025, 19:16:10) [GCC 11.2.0]`,
  SHA-256
  `8f463543ee031f1c8804f869624bebcf3927c56d3e30b3217b4489a31d01ac32`
- zsh builtin prelude reduced the complete exported environment to exactly
  `LANG=C.UTF-8` and `LC_ALL=C.UTF-8`; `exec -c` gave `/usr/bin/env` an empty
  loader environment; `env -i` supplied exactly those two values to Python;
  `-E -S -B` disabled Python environment, site startup, and bytecode writes.

Preflight verified the exact HEAD, binding/amendment blobs, six source blobs,
three runtime identities, startup inputs/exclusions, absent report path, clean
tracked/untracked state, and absence of K3-X caches. The repository-root
`.ruff_cache/` predated the run, was explicitly excluded, and was neither read
nor changed. A malformed orchestration request before the bound preflight was
rejected before process creation; it executed no command and wrote nothing.

## Command executions

Each reached evidence command ran exactly once, in order.

1. Unittest command:

   ```text
   unset ${(k)parameters[(R)*-export*]}; typeset +x SHLVL _; export LC_ALL=C.UTF-8 LANG=C.UTF-8; exported_names=(${(k)parameters[(R)*-export*]}); [[ ${(j: :)${(on)exported_names}} == 'LANG LC_ALL' ]] || exit 125; exec -c /usr/bin/env -i LC_ALL=C.UTF-8 LANG=C.UTF-8 /opt/anaconda3/bin/python -E -S -B -m unittest KernelPlugin.k3x.test_reference -v
   ```

   Exit status: `0`. Result: `Ran 13 tests in 116.539s — OK`.

2. In-memory AST command:

   ```text
   unset ${(k)parameters[(R)*-export*]}; typeset +x SHLVL _; export LC_ALL=C.UTF-8 LANG=C.UTF-8; exported_names=(${(k)parameters[(R)*-export*]}); [[ ${(j: :)${(on)exported_names}} == 'LANG LC_ALL' ]] || exit 125; exec -c /usr/bin/env -i LC_ALL=C.UTF-8 LANG=C.UTF-8 /opt/anaconda3/bin/python -E -S -B -c "import ast, pathlib; paths = ('KernelPlugin/k3x/__init__.py', 'KernelPlugin/k3x/reference.py', 'KernelPlugin/k3x/coding_plugin.py', 'KernelPlugin/k3x/fixtures.py', 'KernelPlugin/k3x/test_reference.py'); [ast.parse(pathlib.Path(path).read_text(encoding='utf-8'), filename=path) for path in paths]"
   ```

   Exit status: `0`. Result: all five bound Python files parsed in memory;
   stdout/stderr were empty.

## Thirteen checks

| Check | Result |
|---|---|
| 01 core definitional and closed coding values | PASS |
| 02 exact-identity equal coalescence and conflict | PASS |
| 03 exact versions and complete descriptor validation | PASS |
| 04 declaration, binding, and capability are derived | PASS |
| 05 pair producers, validation references, and proper cycle | PASS |
| 06 five trust, lifecycle, and discovery branches | PASS |
| 07 false/unknown/errors/malformed/profile projection | PASS |
| 08 trace truth, event admission, and change metadata | PASS |
| 09 confluence, ContractSpec graph errors, and permutations | PASS |
| 10 duplicate equal/conflict order independence | PASS |
| 11 all 42 literal missing reconstructions | PASS |
| 12 all 102 replays without identifier/assertion input | PASS |
| 13 declared access and static-oracle exclusions | PASS |

Observed finite domains:

- fixture IDs / expected assertion keys: `102 / 102`
- missing-base / missing-variant entries: `42 / 42`
- reachable complete-value assertion nodes: `3,740`

## Side effects and exclusions

The tracked worktree was clean before execution. After both commands it was
still clean, with no K3-X `__pycache__`, `.pyc`, network access, external input,
held-out access, ignored-input use, retry, or other generated output. This
report is the sole authorized write and the sole post-run worktree change.

No source repair, dependency installation, model call, real filesystem or
process semantic operation, benchmark, external artifact, K4 work, or held-out
content access occurred.

## Intentionally unimplemented

The implementation fails loudly outside these finite constructors. It does
not implement:

- any K1/K2 declaration, binding, ContractSpec role, model, descriptor,
  service, trust, certificate, authority, evolution, observation, evidence,
  event, profile, or request constructor not instantiated by the packet and
  adversarial subtests;
- general cross-plugin joint reasoning, public relation services, arbitrary
  dependency graphs, arbitrary executable relations, proof checking, or
  discovery beyond the five closed trust projections;
- authority admission beyond the six frozen fixture attestations (only the two
  confluence bindings are evaluated as a graph), evolution beyond the four
  missing-matrix requirement families, certificate judgments beyond the core
  bounds envelope, evolution chains, and independent pair case, or profiles
  beyond the retained implementation-evidence coordinate;
- serialization/loading, natural-language parsing, source binding, prompting,
  model inference/training, planning, search, patch generation, benchmark
  evaluation, or a general Contract IR;
- filesystem/repository mutation, command/process execution, environment,
  network/service/database access, clock, randomness, concurrency, retry,
  deployment, external artifacts, held-out content, or downstream/K4 work.

Passing K3-X does not establish complete K2 implementability, universal coding
semantics, natural-language translation correctness, real-repository safety,
planner performance, or superiority over another IR.
