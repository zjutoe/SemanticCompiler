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

The bound environment launcher is `/usr/bin/env`, SHA-256
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

The exact amended commands are:

```text
/usr/bin/env -i LC_ALL=C.UTF-8 LANG=C.UTF-8 /opt/anaconda3/bin/python -E -S -B -m unittest KernelPlugin.k3x.test_reference -v
/usr/bin/env -i LC_ALL=C.UTF-8 LANG=C.UTF-8 /opt/anaconda3/bin/python -E -S -B -c "import ast, pathlib; paths = ('KernelPlugin/k3x/__init__.py', 'KernelPlugin/k3x/reference.py', 'KernelPlugin/k3x/coding_plugin.py', 'KernelPlugin/k3x/fixtures.py', 'KernelPlugin/k3x/test_reference.py'); [ast.parse(pathlib.Path(path).read_text(encoding='utf-8'), filename=path) for path in paths]"
```

Before dispatch, main must bind an exact execution `HEAD`. Preflight requires
that exact `HEAD`, the accepted implementation blobs, the independently
accepted binding and amendment blobs at their exact paths, both runtime hashes,
exact equality of the operator's complete exported environment to the two fixed
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
