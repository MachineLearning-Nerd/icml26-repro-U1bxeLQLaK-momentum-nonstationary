# Current verification — evaluator evidence gate

This is the canonical entrypoint for the current candidate. The previous live
score remains **3/10**; none of the verdicts below is a new evaluator score.

The current executable verifier is
[`campaign/repro/src/published_claim_verifier.py`](../../campaign/repro/src/published_claim_verifier.py),
introduced in the pre-migration Git history at commit
`a56ee4ac2bb961ee1459245e3a0a3d91b9c73560`. It reads only published evidence,
imports no experiment generator, and supersedes every historical page-embedded
verifier.

| Claim | Current evidence verdict | Canonical page | Normal exit | Failure-probe exit |
|---|---:|---|---:|---:|
| 1 | **VERIFIED** | [Claim 1](#/campaign-claim-1) | `0` | `1` |
| 2 | **BLOCKED** | [Claim 2](#/campaign-claim-2) | `0` | `1` |
| 3 | **VERIFIED** | [Claim 3](#/campaign-claim-3) | `0` | `1` |
| 4 | **FALSIFIED** as imported | [Claim 4](#/campaign-claim-4) | `0` | `1` |
| 5 | **BLOCKED** | [Claim 5](#/campaign-claim-5) | `0` | `1` |

Claim 2 was downgraded by the universal-theorem calibration: three scoped
routes do not close Theorem 3.7 for every `p,q` and every policy in `Pi_beta`.
The mandatory fourth falsification audit found no valid counterexample.

## Fixed command and pinned environment

```bash
uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py
```

- [pyproject.toml](../../campaign/pyproject.toml)
- [uv.lock](../../campaign/uv.lock)
- [.python-version](../../campaign/.python-version)
- Python `3.12.11`; one repository `.venv`; local 8-core Apple-silicon CPU.
- No GPU or Hugging Face compute was used.

## Evaluator-blind reviews

- [First pass — not release-ready](../../evidence/evaluator_blind_review/first_pass.json)
- [Second pass — current visibility matrix](../../evidence/evaluator_blind_review/second_pass.json)

## Historical safety

The exact previously judged page and evidence files remain byte-identical.
They are navigated below as **Historical rejected baseline** and are not the
default verification run. The original README is preserved at
[historical/judged-README.md](../../historical/judged-README.md).
