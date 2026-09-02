# K3-X execution-command isolation amendment

Status: `REVIEW_CANDIDATE`. This amendment changes only the K3-X evidence
command boundary. It grants no execution authority by itself.

## Problem

The accepted K3-X handoff used `python -B`. `-B` prevents bytecode writes but
does not disable interpreter startup through `site`, `sitecustomize`, user site,
or `.pth` files. Those ambient inputs are outside the finite evidence boundary.

## Normative repair

For K3-X diagnostic and evidence execution, every accepted handoff occurrence
of `python -B` is superseded by an exact empty-environment launcher, two fixed
locale values, and the exact bound interpreter followed by `-E -S -B`:

- `-E` ignores all `PYTHON*` environment variables;
- `-S` disables automatic `site`, `sitecustomize`, user-site, and `.pth`
  processing;
- `-B` disables bytecode/cache writes.

The bound environment launcher is `/usr/bin/env`, version
`env (GNU coreutils) 9.5`, SHA-256
`190c360452d515eac29236055581587f162d5b53f56104df169fc51d5c4661c9`.
It supplies exactly `LC_ALL=C.UTF-8` and `LANG=C.UTF-8`; no other environment
variable reaches Python. Before `/usr/bin/env` is executed, the operator process
must itself expose exactly those same two exported variables and no others.
This complete equality check occurs in the already-running operator process,
before launcher `exec`; checking a denylist is insufficient. Any additional or
missing exported variable is a reportable preflight failure, so loader,
auditing, debugging, tuning, Python, user, shell, and locale inputs cannot reach
the launcher implicitly.

The working directory remains the exact repository root, so the committed
`KernelPlugin` package remains importable without `PYTHONPATH` or site startup.
No other command, semantic check, fixture, expected result, or conclusion is
changed.

The operator shell is `/usr/bin/zsh` 5.9, SHA-256
`288d795a07cd3d2fbbd8f7ead127a5428153a02203f83bd19cda3b50b03cc697`,
started by the execution substrate exactly as shell binary `/usr/bin/zsh`,
non-interactively with repository working directory and no login mode. In this
mode zsh reads `zshenv` but no later startup file. The execution substrate must
provide pre-start `HOME=/home/mye` and no `ZDOTDIR`; both are exact pre-start
conditions checked and recorded before shell creation.
The unavoidable global `/etc/zshenv` is bound at 510 bytes with SHA-256
`69ed780cdba8e32191af71649c8b7529f0aa1e83c28325dbfcd45d139eb3fbc2`;
`/home/mye/.zshenv` and `/etc/zshenv.zwc` must be absent. Any mismatch is a
preflight failure. These conditions bind the only startup content selectable
before the builtin prelude.
The exact amended commands include a builtin-only prelude: remove every
exported variable, make `SHLVL` and `_` non-exported, export the two locale
values, assert the complete exported-name set, then use zsh `exec -c` so the
`/usr/bin/env` dynamic loader inherits an empty environment. `env -i` injects
only the two fixed locale values into Python.

The exact amended commands are:

```text
unset ${(k)parameters[(R)*-export*]}; typeset +x SHLVL _; export LC_ALL=C.UTF-8 LANG=C.UTF-8; exported_names=(${(k)parameters[(R)*-export*]}); [[ ${(j: :)${(on)exported_names}} == 'LANG LC_ALL' ]] || exit 125; exec -c /usr/bin/env -i LC_ALL=C.UTF-8 LANG=C.UTF-8 /opt/anaconda3/bin/python -E -S -B -m unittest KernelPlugin.k3x.test_reference -v
unset ${(k)parameters[(R)*-export*]}; typeset +x SHLVL _; export LC_ALL=C.UTF-8 LANG=C.UTF-8; exported_names=(${(k)parameters[(R)*-export*]}); [[ ${(j: :)${(on)exported_names}} == 'LANG LC_ALL' ]] || exit 125; exec -c /usr/bin/env -i LC_ALL=C.UTF-8 LANG=C.UTF-8 /opt/anaconda3/bin/python -E -S -B -c "import ast, pathlib; paths = ('KernelPlugin/k3x/__init__.py', 'KernelPlugin/k3x/reference.py', 'KernelPlugin/k3x/coding_plugin.py', 'KernelPlugin/k3x/fixtures.py', 'KernelPlugin/k3x/test_reference.py'); [ast.parse(pathlib.Path(path).read_text(encoding='utf-8'), filename=path) for path in paths]"
```

Before dispatch, main must bind an exact execution `HEAD`. Preflight requires
that exact `HEAD`, the accepted implementation blobs, the independently
accepted binding and amendment blobs at their exact paths, the exact zsh, env,
and Python paths/hashes/versions, the bound global zshenv
size/hash, absence of `/etc/zshenv.zwc` and the user zshenv, exact pre-start
`HOME=/home/mye`, absence of `ZDOTDIR`, and the
non-interactive/non-login operator mode, exact equality of the operator's complete exported environment to the two fixed
locale entries, clean tracked/untracked status, an absent sole report
path, and no K3-X caches. Ancestry alone is insufficient.

If preflight fails and the report path is absent, no evidence command runs and
the sole failure report records the mismatch. If the report path already exists
or is dirty, the operator writes nothing and escalates to main. If a command
fails, execution stops; the sole failure report records that command once and
every later command as `NOT_RUN`. “Exactly once” applies only to commands
reached in the ordered execution. The report remains the only authorized write
in success or reportable failure.

This amendment does not permit dependencies, external inputs, network,
held-out access, additional output, source repair, retry, or K4 work.
