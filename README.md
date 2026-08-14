# ICML 2026 Reproduction: Momentum SGD under Nonstationary Drift

This repository is a clean-room, claim-by-claim audit of [*On the Provable
Suboptimality of Momentum SGD in Nonstationary Stochastic
Optimization*](https://arxiv.org/abs/2601.12238), associated with OpenReview
paper [`U1bxeLQLaK`](https://openreview.net/forum?id=U1bxeLQLaK).

- Authors: Sharan Sahu, Cameron J. Hogan, and Martin T. Wells
- Venue: ICML 2026
- Canonical repository: [`MachineLearning-Nerd/icml26-momentum-sgd-nonstationary-optimization`](https://github.com/MachineLearning-Nerd/icml26-momentum-sgd-nonstationary-optimization)
- Paper source pinned by this audit: arXiv `2601.12238v4`
- Latest arXiv record: [arXiv:2601.12238](https://arxiv.org/abs/2601.12238)

## Status

`SCOPED_PASS` — `VERIFIED_SCOPED_WITH_FALSIFIED_AND_BLOCKED_CLAIMS`

The committed evidence is internally consistent, but the scientific outcome
is mixed. Claims 1 and 3 are verified within their stated finite scopes. Claim
2 remains blocked by universal theorem quantifiers, Claim 4 is falsified as
the imported conjunction, and Claim 5 remains blocked because the source does
not specify enough finite-experiment detail for an exact replication.

The strict paper-level status is `NOT_READY`: this is not a complete replication
of every theorem quantifier or every Section 4 model class. The previous live
judge score was `3/10`; this repository claims no new evaluator score and makes
no score forecast. A passing publication gate means that the evidence and its
negative controls are reproducible, not that every paper claim passed.

The canonical machine-readable gate is
[`publication_gate.json`](publication_gate.json), with an identical copy at
[`outputs/publication_gate.json`](outputs/publication_gate.json). The claim
ledger is in [`docs/CLAIM_EVIDENCE.md`](docs/CLAIM_EVIDENCE.md).

## What the paper does

The paper studies SGD, Polyak Heavy-Ball (HB), and Nesterov momentum while the
optimizer tracks a time-varying strongly convex and smooth optimum. Its main
path is:

1. decompose tracking error into transient, stochastic-noise, and drift terms;
2. derive momentum-dependent stability and inertia effects;
3. prove information-theoretic lower-bound mechanisms for nonstationary
   stochastic optimization; and
4. use drifting quadratic, linear/logistic, and MLP experiments to illustrate
   regimes in which stale-gradient averaging hurts tracking.

This repository reimplements auditable mathematical and finite numerical
contracts from the paper. The arXiv source archive contains the paper TeX and
figures but no executable author experiment repository; see
[`docs/SOURCE_AUDIT.md`](docs/SOURCE_AUDIT.md).

## Claim-to-evidence summary

| Claim | Paper statement audited | How the result is produced | Current outcome |
| --- | --- | --- | --- |
| C1 | Theorem 3.3: momentum initialization amplification of order `(1-β)⁻²` and noise-floor amplification of order `(1-β)⁻¹` relative to SGD | `repro/src/claim1_regression.py`, `verify_tracking.py`, and `verify_c0_transient.py` produce the raw transient/noise JSON; the independent checker recomputes both log-log slopes from those files | **VERIFIED_SCOPED** — slopes `2.115` and `0.987` |
| C2 | Theorem 3.7: statistical exponent `2/3` and inertia exponent `2` for all stated `p,q` and policies | `exact_contracts.py`, `pathwise_contracts.py`, `run_theory_certificates.py`, and the full-dimensional route produce symbolic, Fano, tracking, and negative-control evidence; the route-4 audit tests candidate counterexamples | **BLOCKED** — finite/scoped routes pass, but the universal policy-level theorem is not closed |
| C3 | In an existential drift-heavy regime, stable SGD can track better than HB and NAG | `remaining_contracts.py` and `run_quadratic_grid.py` produce `d=100`, 20-seed, 5,000-step raw trials; the checker validates caps, dimensions, horizons, seeds, row count, and two-SE separation | **VERIFIED_SCOPED** — at `β=.98`, SGD `0.002417`, HB `0.236482`, NAG `0.231877` |
| C4 | Imported conjunction about a `(1-β)⁻²` horizon and the absence of the coupling from SGD | `exact_contracts.py` and `pathwise_contracts.py` produce coefficient, horizon, and pathwise coupling audits; the checker tests the displayed source formula and the narrower interpretation separately | **FALSIFIED AS WRITTEN** — displayed horizon slope is `2`, and SGD also has a coupling term; the narrower momentum-specific coefficient is verified |
| C5 | Section 4 systematically shows drift, `β`, and condition number worsening HB/NAG across reported models | `remaining_contracts.py` produces moment-matched, raw-minibatch, exact-spectral, and falsification-audit routes; the checker requires four routes and an assumption-complete counterexample before falsifying | **BLOCKED** — routes disagree and author implementation details are unavailable |

The verifier returns exit code `0` when each expected verdict is supported by
its shipped evidence. It deliberately returns a scientific verdict of
`BLOCKED` or `FALSIFIED` where appropriate; those are not silently converted
to passes.

## Repository contents

| Path | Purpose |
| --- | --- |
| `docs/primary.pdf` | Pinned arXiv v4 PDF used for the source audit |
| `docs/arxiv_source.tar` | Pinned TeX/figure source archive |
| `repro/src/` | Clean-room producers, contracts, independent checker, and gates |
| `repro/tests/` | Focused recurrence, contract, and visibility tests |
| `.openresearch/artifacts/` | Provenance and raw claim artifacts produced during the campaign |
| `release/huggingface-space/evidence/` | Evaluator-visible copy of the current text evidence |
| `outputs/` | Hash-bound summaries, manifests, and gate outputs |
| `reports/momentum-nonstationary/report.md` | Illustrated technical report |
| `notebooks/momentum_nonstationary.py` | Self-contained marimo walkthrough of the core finite result |

## Branch map

The published branch set is intentionally descriptive. The old `orx/*` names
are retained only in the migration audit so that the original experiment
history remains traceable. The exact mapping and purpose of every branch are
in [`docs/BRANCH_AUDIT.md`](docs/BRANCH_AUDIT.md).

| Published branch family | Role |
| --- | --- |
| `main` | Canonical README, source pins, current claim ledger, and publication gate |
| `baseline/*` | Frozen starting point and accepted baseline regression |
| `audit/*` | Theory, pathwise, and mandatory falsification audits |
| `regression/*` | Cumulative regression of accepted evidence |
| `experiment/*` | Condition-number and full-dimensional experiment routes |
| `release/*` | Evaluator-visible, candidate, and final release snapshots |

Branch names describe the work; they do not imply that a branch's scientific
outcome is a full paper replication.

## Reproduce the scoped gate

Create a Python 3.12 environment, install the locked dependencies, and run the
deterministic gate:

```bash
uv sync --frozen
uv run --no-sync python repro/src/publication_gate.py
```

The default gate reads the committed evidence, runs the focused tests, runs the five independent
claim verifiers plus their injected-failure probes, rebuilds the deterministic
hash manifest, and writes both gate copies. It does not require a GPU, a
Hugging Face token, private paths, or a data download.

The older full campaign command remains available for historical comparison:

```bash
uv sync --frozen && uv run --no-sync pytest -q repro/tests && \
uv run --no-sync python repro/src/run_theory_certificates.py && \
uv run --no-sync python repro/src/run_quadratic_grid.py && \
uv run --no-sync python repro/src/verify_claims.py && \
uv run --no-sync python repro/src/build_evidence_bundle.py
```

Those generators can take several minutes on CPU. The default publication gate
is intentionally evidence-first and fail-closed; optional reruns are described
in [`docs/PUBLICATION_GATE.md`](docs/PUBLICATION_GATE.md).

## Citation

```bibtex
@article{sahu2026provable,
  title        = {On the Provable Suboptimality of Momentum SGD in Nonstationary Stochastic Optimization},
  author       = {Sahu, Sharan and Hogan, Cameron J. and Wells, Martin T.},
  journal      = {arXiv preprint arXiv:2601.12238},
  year         = {2026},
  eprint       = {2601.12238},
  archivePrefix = {arXiv}
}
```

## Thank you

Thank you to Sharan Sahu, Cameron J. Hogan, and Martin T. Wells for developing
and sharing this analysis of momentum under distribution shift. The explicit
separation of transient, noise, and drift effects gives reproduction work a
useful structure: each mathematical feature can be audited independently, and
uncertainty in the experimental protocol can be reported instead of guessed.

## Scope limits

- The source archive has no executable author experiment repository, so the
  numerical work here is clean-room code rather than an author-code rerun.
- C2 checks important finite and specialized routes but does not prove every
  `p,q` theorem quantifier or every policy in `Π_β`.
- C3 is one declared full-dimensional stochastic witness, not a universal
  claim about all nonstationary objectives.
- C5 does not promote incomplete experimental specifications into a pass or a
  falsification; the reported model-class results remain unreplicated.
- The old three-claim `6/6` baseline is preserved in Git history; the current
  `outputs/` files have been replaced by the authoritative five-claim verdict.
- `score_forecast` is intentionally `null`; no external evaluator score is
  claimed.
