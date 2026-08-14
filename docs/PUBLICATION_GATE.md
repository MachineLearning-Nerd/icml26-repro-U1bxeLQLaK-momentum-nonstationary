# Publication gate

The default gate is deliberately small and fail-closed. It validates the
current evidence already committed to the repository; it does not pretend to
rerun unavailable author code.

## Checks

`repro/src/publication_gate.py` performs these checks:

1. validates the pinned PDF and source-archive hashes in `sources.json`;
2. runs the independent verifier for Claims 1–5 against the evaluator-visible
   evidence;
3. runs one injected-failure probe for every claim and requires a nonzero exit;
4. runs the focused `repro/tests` suite;
5. rebuilds the deterministic hash-bound evidence bundle; and
6. writes identical `publication_gate.json` and `outputs/publication_gate.json`
   files.

The resulting `publication_gate_passed: true` means the audit machinery is
healthy. The `claims` map is the scientific result and may contain `BLOCKED`
or `FALSIFIED` outcomes. `strict_status: NOT_READY` remains until the missing
universal proof coverage and source-scale experiments are addressed.

## Optional historical reruns

The original campaign producers remain in `repro/src/`. The long command in
the root README reruns theory certificates, the quadratic grid, the original
claim verifier, and the legacy bundle builder. It is CPU work and may overwrite
historical outputs, so it is not part of the default gate.

No Hugging Face token, private dataset, GPU, or network download is needed for
the default gate.
