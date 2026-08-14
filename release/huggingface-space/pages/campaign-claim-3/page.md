# Campaign Claim 3 — full-dimensional stable tracking

Verdict for the explicit existential contract: **VERIFIED**

## Exact claim and quantifiers

The tested statement is existential: under the stability restriction
`gamma <= c(1-beta)^2/L`, there exists a drift-dominated, uniformly
strongly-convex and smooth nonstationary regime in which vanilla SGD has lower
tracking error than HB and NAG.

The experiment supplies one admissible full-dimensional stochastic witness at
`beta in {0.5,0.9,0.95,0.98}`. It does **not** assert universal optimizer
ordering. Appendix E.6 proves the response construction for Heavy-Ball and
states, without supplying, an analogous Nesterov proof. NAG is therefore a
scoped experimental witness. Source anchors:
`main.tex:612-638`, `appendix.tex:3409-3710`, and
`appendix.tex:3714-3765`.

## Assumptions and numerical audit

| Item | Published value |
|---|---:|
| Dimension | `100` |
| Strong convexity `mu` | `1` |
| Smoothness `L` | `10` |
| Condition number | `10` |
| Horizon | `5,000` |
| Raw trajectory indices | `0..19` |
| Drift | normalized Gaussian random walk, step norm `0.01` |
| Gradient-noise standard deviation | `0.02` |
| HB/NAG step size | `0.8 * mu(1-beta)^2/(4L^2)` |
| Published raw rows | `240` |
| Rows inside declared caps | `240/240` |

The [claim contract](../../evidence/claim_3/claim_contract.json) contains the
logical scope and numerical domain. The per-row `gamma`, `stability_cap`, and
`gamma_within_cap` fields are in the raw CSV.

## Executable verifier

- [Current standalone verifier](../../campaign/repro/src/published_claim_verifier.py)
- [Experiment and generator](../../campaign/repro/src/remaining_contracts.py)
- [Quadratic update implementation](../../campaign/repro/src/quadratic_protocol.py)
- [Contract tests](../../campaign/repro/tests/test_remaining_contracts.py)
- [Recurrence tests](../../campaign/repro/tests/test_recurrences.py)

## Pinned environment and fixed command

[pyproject.toml](../../campaign/pyproject.toml),
[uv.lock](../../campaign/uv.lock), and
[.python-version](../../campaign/.python-version) pin Python `3.12`.

```bash
uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py
```

## Raw results shown inline

Mean tail squared tracking error ± one SE:

| β | SGD | HB | NAG |
|---:|---:|---:|---:|
| .50 | `0.0024566 ± 0.0000200` | `0.0207335 ± 0.0003921` | `0.0193232 ± 0.0003357` |
| .90 | `0.0024079 ± 0.0000172` | `0.0877887 ± 0.0019758` | `0.0976136 ± 0.0034293` |
| .95 | `0.0024490 ± 0.0000195` | `0.1508579 ± 0.0054308` | `0.1427721 ± 0.0024488` |
| .98 | `0.0024174 ± 0.0000161` | `0.2364824 ± 0.0073316` | `0.2318771 ± 0.0060366` |

SGD plus two SE is below both momentum means minus two SE at every beta.
Download the [12-row summary](../../evidence/claim_3/stability_summary.csv),
[all 240 raw rows](../../evidence/claim_3/stability_trials.csv), and
[independent spectral data](../../evidence/claim_3/independent_spectral_checker.csv).

## Independent checker and negative control

The [independent checker](../../evidence/claim_3/independent_checker.json)
reads the raw CSV and verifies all caps and separations. Its separate
characteristic-polynomial calculation gives a slow-mode half-life exponent
`0.9998450158` against `kappa/(1-beta)`.

The [stationary deterministic control](../../evidence/claim_3/negative_control.json)
requires HB to accelerate: squared error `0.0314254730` versus SGD
`0.1953661516`. This rejects the overbroad interpretation that momentum always
hurts.

## Failure probe

- [Normal verifier output](../../evidence/current_verifier/claim_3_pass.json):
  exit code `0`; 240 rows, caps, dimensions, horizons, and separations pass.
- [Injected cap-violation output](../../evidence/current_verifier/claim_3_failure_probe.json):
  exit code `1`, failing `all_steps_within_declared_caps`.

## Limitations and deviations

This is one full-dimensional witness for an existential regime, not a proof of
a universal ordering. The spectrum is a controlled diagonal quadratic.
Heavy-Ball has a source proof; NAG is experimentally tested because the source
does not close its analogous proof. See
[limitations](../../evidence/claim_3/limitations.md).

## Revision, seeds, CPU, and runtime

- Pre-migration scientific evidence SHA:
  `61faf82dbc11f46c01b156f8b60ef68bc70d5450`.
- Pre-migration verifier source SHA:
  `a56ee4ac2bb961ee1459245e3a0a3d91b9c73560`.
- RNG stream seeds:
  `260112738, 260122738, 260132738, 260113138, 260123138, 260133138,`
  `260113188, 260123188, 260133188, 260113218, 260123218, 260133218`.
- Each RNG stream contains 20 indexed trajectories (`0..19`).
- Python `3.12.11`; 8 CPU cores; macOS arm64.
- Recorded claim runtime: `16.946585875` seconds.
- [Complete run metadata](../../evidence/claim_3/run_metadata.json)
- [Source audit](../../evidence/claim_3/source_audit.md),
  [method](../../evidence/claim_3/method.md), and
  [evaluation](../../evidence/claim_3/EVAL.md)
