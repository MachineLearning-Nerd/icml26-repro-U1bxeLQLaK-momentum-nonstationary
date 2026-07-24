# 2026-07-23 claim-by-claim campaign

This additive campaign responds to the live `3/10` verdict for
`DineshAI/U1bxeLQLaK@9db6b4452399d8ef19e3f8ca479a627060819fb3`.
It preserves every page from that judged revision and adds stricter
machine-checkable evidence. It does **not** claim a new judge score.

| Claim | Previous points | New evidence verdict | What changed |
|---|---:|---:|---|
| 1 | 2/2 | **VERIFIED** | Existing full-credit evidence is preserved and rerun |
| 2 | 0/2 | **VERIFIED** | Exact minimax decomposition, finite Fano certificate, and independent pathwise route |
| 3 | 1/2 | **VERIFIED** | Replaces the 1D proxy with `d=100`, 20 seeds, 5,000 steps |
| 4 | 0/2 | **FALSIFIED** as imported | Exact source audit plus separately verified narrower coefficient interpretation |
| 5 | 0/2 | **BLOCKED** | Three verification routes plus mandatory falsification audit |

## Fixed command

```bash
uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py
```

All formal runs use one repository `.venv`, Python `3.12.11`, and the committed
`pyproject.toml` / `uv.lock`. Compute was local 8-core Apple-silicon CPU. No GPU
or Hugging Face compute was used.

## Source and integrity

- arXiv source: `2601.12238v4`
- retrieval date: `2026-07-23`
- source archive SHA-256:
  `89ad9ad897d3f9a0210ceab3e61adb356bf32edaa49621c0234a426aef3b3fa9`
- PDF SHA-256:
  `415533d734236070ec5180fdcf6fcc9454dc55a20913f219b5d7f1be19776032`
- HTML SHA-256:
  `2b97b7d91336a16b7bd7800d3f8ed96ebd17a89474fb36e4c6991e378d7a47ec`
- winning scientific Git SHA:
  `61faf82dbc11f46c01b156f8b60ef68bc70d5450`

The source archive contains no executable author experiment repository.
Missing implementation details are recorded as limitations rather than guessed
into a pass.

