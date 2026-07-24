# Campaign Claim 5 — Section 4 condition-number audit

Verdict: **BLOCKED**

## Exact claim and quantifiers

Section 4 reports a finite empirical pattern—not a universal theorem—across
quadratics, linear regression, logistic regression, and a teacher–student MLP:
increasing drift, momentum `beta`, or condition number `kappa` systematically
worsens HB and NAG tracking while SGD is comparatively robust.

The missing judged component is the `kappa in {10,1000}` comparison with
source-scale dimension, horizon, seed count, batch size, drift, beta, spectrum,
and endpoint step sizes. Because no author code fixes the remaining
normalization and data-path choices, a clean-room disagreement is not
automatically a counterexample to the exact finite author experiment. Source
anchors: `main.tex:657-760` and `appendix.tex:3711-3940`.

## Assumptions and numerical audit

All three verification routes use the disclosed linear-regression protocol:

| Item | Value |
|---|---:|
| Dimension | `50` |
| Horizon | `5,000` |
| Runs | `20` |
| Batch size | `256` |
| Drift step | `0.01` |
| Label-noise variance | `0.5` |
| Condition numbers | `10`, `1000` |
| Methods | SGD, HB, NAG |
| β for κ audit | source endpoint |

Route 1 uses exact conditional mini-batch moments; route 2 generates literal
Gaussian covariates and labels; route 3 solves the linear covariance recurrence
exactly. Route 2 retains all `120/120` finite trials. Route 3 has maximum
Lyapunov residual `2.71e-19`.

See the [claim contract](../../evidence/claim_5/claim_contract.json) and
[source audit](../../evidence/claim_5/source_audit.md).

## Executable verifier

- [Current standalone verifier](../../campaign/repro/src/published_claim_verifier.py)
- [All four routes](../../campaign/repro/src/remaining_contracts.py)
- [Quadratic implementation](../../campaign/repro/src/quadratic_protocol.py)
- [Route tests](../../campaign/repro/tests/test_remaining_contracts.py)
- [Recurrence tests](../../campaign/repro/tests/test_recurrences.py)

## Pinned environment and fixed command

[pyproject.toml](../../campaign/pyproject.toml),
[uv.lock](../../campaign/uv.lock), and
[.python-version](../../campaign/.python-version) pin Python `3.12`.

```bash
uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py
```

## Raw results shown inline

Endpoint error ratio `kappa=1000 / kappa=10`:

| Route | HB | NAG | SGD | Result |
|---|---:|---:|---:|---|
| Exact-moment Gaussian oracle | `0.0178909` | `0.0693054` | `1.15849` | opposite HB/NAG direction |
| Literal raw mini-batches | `0.0183067` | `0.0707293` | `1.08564` | opposite HB/NAG direction |
| Exact spectral covariance | `0.0301903` | `0.0874964` | `1.18482` | opposite HB/NAG direction |

Ratios below one mean the high-κ endpoint improved momentum tracking in every
clean-room route. Download:

- [Route 1 summary](../../evidence/claim_5/route_1_moment_matched/linear_moment_matched_summary.csv)
  and [all trials](../../evidence/claim_5/route_1_moment_matched/linear_moment_matched_trials.csv)
- [Route 2 summary](../../evidence/claim_5/route_2_raw_minibatch/raw_minibatch_summary.csv)
  and [all trials](../../evidence/claim_5/route_2_raw_minibatch/raw_minibatch_trials.csv)
- [Route 3 summary](../../evidence/claim_5/route_3_exact_spectral/spectral_summary.csv)
  and [mode covariances](../../evidence/claim_5/route_3_exact_spectral/mode_covariances.csv)
- [Route 4 candidate audit](../../evidence/claim_5/route_4_falsification_audit/candidate_counterexamples.csv)

The mandatory fourth route audited four proposed contradictions. Exactly
`0/4` satisfy every assumption and contradict the exact descriptive claim.

## Independent checker and negative control

The [aggregate checker](../../evidence/claim_5/independent_checker.json)
confirms all four route verdicts are BLOCKED. Route-level independent checkers
and mutation controls are linked from their evaluations:
[route 1](../../evidence/claim_5/route_1_moment_matched/EVAL.md),
[route 2](../../evidence/claim_5/route_2_raw_minibatch/EVAL.md),
[route 3](../../evidence/claim_5/route_3_exact_spectral/EVAL.md), and
[route 4](../../evidence/claim_5/route_4_falsification_audit/EVAL.md).

The [aggregate stationary control](../../evidence/claim_5/negative_control.json)
requires HB acceleration, preventing an overbroad “momentum always hurts”
interpretation. Route 4 rejects assumption-violating and merely missing-data
“counterexamples.”

## Failure probe

- [Normal audit-verifier output](../../evidence/current_verifier/claim_5_pass.json):
  exit code `0`; it verifies the internally consistent **BLOCKED** record.
- [Injected false exact-counterexample output](../../evidence/current_verifier/claim_5_failure_probe.json):
  exit code `1`, failing `no_valid_exact_counterexample`.

## Limitations and deviations

No executable author pipeline exists. The clean-room routes do not reproduce
the source-scale logistic-regression or 13,057-parameter MLP paths, and the
finite source statement leaves normalization choices unresolved. Therefore
the strong three-route disagreement is neither VERIFIED nor FALSIFIED.
Unblocking requires the author pipeline or enough missing details to identify
the exact finite experiment. See
[limitations](../../evidence/claim_5/limitations.md).

## Revision, seeds, CPU, and runtime

- Scientific evidence Git SHA:
  `61faf82dbc11f46c01b156f8b60ef68bc70d5450`.
- Current verifier code commit:
  `a56ee4ac2bb961ee1459245e3a0a3d91b9c73560`.
- Deterministic seed interval recorded by the aggregate route:
  `260112810` through `260113800`; exact per-route rules are in source and raw
  metadata.
- Python `3.12.11`; 8 CPU cores; macOS arm64.
- Recorded Claim 5 route runtime: `346.682136459` seconds.
- [Complete run metadata](../../evidence/claim_5/run_metadata.json)
- [Method](../../evidence/claim_5/method.md) and
  [aggregate evaluation](../../evidence/claim_5/EVAL.md)
