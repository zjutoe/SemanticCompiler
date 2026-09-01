# K3-X execution-command isolation amendment

Status: `REVIEW_CANDIDATE`. This amendment changes only the K3-X evidence
command boundary. It grants no execution authority by itself.

## Problem

The accepted K3-X handoff used `python -B`. `-B` prevents bytecode writes but
does not disable interpreter startup through `site`, `sitecustomize`, user site,
or `.pth` files. Those ambient inputs are outside the finite evidence boundary.

## Normative repair

For K3-X diagnostic and evidence execution, every accepted handoff occurrence
of `python -B` is superseded by the exact bound interpreter followed by
`-E -S -B`:

- `-E` ignores all `PYTHON*` environment variables;
- `-S` disables automatic `site`, `sitecustomize`, user-site, and `.pth`
  processing;
- `-B` disables bytecode/cache writes.

The working directory remains the exact repository root, so the committed
`KernelPlugin` package remains importable without `PYTHONPATH` or site startup.
No other command, semantic check, fixture, expected result, or conclusion is
changed.

The exact amended commands are:

```text
/opt/anaconda3/bin/python -E -S -B -m unittest KernelPlugin.k3x.test_reference -v
/opt/anaconda3/bin/python -E -S -B -c "import ast, pathlib; paths = ('KernelPlugin/k3x/__init__.py', 'KernelPlugin/k3x/reference.py', 'KernelPlugin/k3x/coding_plugin.py', 'KernelPlugin/k3x/fixtures.py', 'KernelPlugin/k3x/test_reference.py'); [ast.parse(pathlib.Path(path).read_text(encoding='utf-8'), filename=path) for path in paths]"
```

Before dispatch, main must bind an exact execution `HEAD`. Preflight requires
that exact `HEAD`, the accepted implementation blobs, binding/amendment commits,
runtime hash, clean tracked/untracked status, and no K3-X caches.

If preflight fails, no evidence command runs and the sole report records the
preflight failure. If a command fails, execution stops; the sole report records
that command once and every later command as `NOT_RUN`. “Exactly once” applies
only to commands reached in the ordered execution. The report remains the only
authorized write in success or failure.

This amendment does not permit dependencies, external inputs, network,
held-out access, additional output, source repair, retry, or K4 work.
