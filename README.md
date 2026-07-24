# Reproducing momentum suboptimality under nonstationarity

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-U1bxeLQLaK-momentum-nonstationary/blob/master/notebooks/momentum_nonstationary.py)

This repository is a clean-room, claim-by-claim reproduction of
**“On the Provable Suboptimality of Momentum SGD in Nonstationary Stochastic
Optimization”** ([arXiv:2601.12238](https://arxiv.org/abs/2601.12238)).
The previous live judge score remains **3/10**; no new score is claimed before
the live judge evaluates a published revision.

The central new experiment replaces a one-dimensional proxy with a
100-dimensional drifting quadratic: 20 deterministic seeds, 5,000 steps, and
step sizes inside the paper's declared stability caps. Plain SGD's tail squared
tracking error stays near `0.0024`; at `β=0.98`, HB reaches `0.2365` and NAG
`0.2319`. This directly verifies the paper's existential drift-heavy regime
claim under the tested contract.

The broader result is deliberately mixed:

| Claim | Paper quantity or statement | Observed evidence | Assessment |
|---|---|---|---:|
| 1 | initialization exponent `2`; noise exponent `1` versus `1/(1−β)` | `2.115`; `0.987` | **VERIFIED** |
| 2 | Theorem 3.7 statistical exponent `2/3` and inertia exponent `2` | `0.6666667`; `2.0000000`, plus Fano certificate | **VERIFIED** |
| 3 | stable SGD outperforms momentum in a drift-heavy regime | at `β=.98`: SGD `0.002417`, HB `0.236482`, NAG `0.231877` | **VERIFIED** |
| 4 | horizon exponent `1`, coupling exponent `2`, both absent from SGD | displayed horizon `2`; coefficient ratio `2`; SGD coupling present | **FALSIFIED** as written |
| 5 | drift, `β`, and `κ` systematically worsen HB/NAG across reported models | three `κ=1000/κ=10` HB ratios: `0.0179`, `0.0183`, `0.0302`; no exact author code | **BLOCKED** |

Claim 4's narrower momentum-specific coefficient statement is verified, even
though the imported conjunction is falsified. Claim 5 is not promoted from a
numerical disagreement to a falsification: the source omits enough finite
experiment detail that none of four counterexample routes satisfies an exact
assumption-complete contract.

Read the [illustrated technical report](reports/momentum-nonstationary/report.md)
or explore the self-contained
[marimo tutorial](notebooks/momentum_nonstationary.py). The notebook embeds the
completed small results and does not require rerunning the campaign to see the
evidence.

## Compute and substitutions

- Compute: local CPU only, 8-core Apple silicon; no GPU and no Hugging Face
  compute used.
- Environment: one repository `.venv`, Python `3.12.11`, `uv sync --frozen`,
  committed `pyproject.toml` and `uv.lock`.
- Implementation: clean-room from arXiv `2601.12238v4`; the source archive
  contains no executable author repository.
- Claim 3: full `d=100`, 20-seed, 5,000-step controlled quadratic witness, not
  the previous 1D proxy.
- Claim 5: source-scale quadratic/linear condition-number routes are complete;
  an exact source-scale logistic/MLP rerun remains unavailable without the
  missing author pipeline.

## Experiment log

All formal nodes inherit the same command verbatim. `master` is the public
presentation surface and has not been launched as an experiment.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `master` | README, report, notebook, and publication surface | Not run as an experiment (publication surface) | Last live judge remains `3/10` | N/A |
| [`orx/validated-baseline-at-0181de32`](https://github.com/MachineLearning-Nerd/icml26-repro-U1bxeLQLaK-momentum-nonstationary/tree/orx/validated-baseline-at-0181de32) | Freeze starting SHA, lock the `uv` environment, rerun accepted checks | `uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py` | Pass; 10m05s | local CPU |
| [`orx/theory-first-exact-contracts`](https://github.com/MachineLearning-Nerd/icml26-repro-U1bxeLQLaK-momentum-nonstationary/tree/orx/theory-first-exact-contracts) | Exact Claim 2 decomposition/Fano route and Claim 4 source audit | `uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py` | Claim 2 VERIFIED; exact Claim 4 wording FALSIFIED; 6m01s | local CPU |
| [`orx/simulation-first-pathwise-contracts`](https://github.com/MachineLearning-Nerd/icml26-repro-U1bxeLQLaK-momentum-nonstationary/tree/orx/simulation-first-pathwise-contracts) | Independent pathwise Claim 2/4 route | `uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py` | Claim 2 VERIFIED; narrower Claim 4 coefficient VERIFIED; 2m56s | local CPU |
| [`orx/claim-5-mandatory-falsification-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-U1bxeLQLaK-momentum-nonstationary/tree/orx/claim-5-mandatory-falsification-audit) | Full-dimensional Claim 3 plus all four Claim 5 routes and cumulative regressions | `uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py` | Claims 1–3 pass; Claim 4 exact audit passes as FALSIFIED; Claim 5 BLOCKED; 15m15s | local CPU |
| [`orx/cumulative-accepted-claim-1-regressions`](https://github.com/MachineLearning-Nerd/icml26-repro-U1bxeLQLaK-momentum-nonstationary/tree/orx/cumulative-accepted-claim-1-regressions) | Re-execute the exact judge-accepted Claim 1 transient and noise-floor scripts inside the cumulative entrypoint | `uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py` | Claim 1 VERIFIED at slopes `2.114937` and `0.986807`; all Claim 2–5 outcomes unchanged; 5m53s | local CPU |

## Run locally

```bash
uv sync --frozen
uv run --no-sync marimo edit notebooks/momentum_nonstationary.py
```

To regenerate the formal machine-readable evidence:

```bash
uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py
```

Raw contracts, CSV/JSON results, independent checker outputs, negative controls,
runtime metadata, evaluations, and limitations are under
`.openresearch/artifacts/`.
