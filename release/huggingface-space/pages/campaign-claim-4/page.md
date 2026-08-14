# Campaign Claim 4 — exact high-probability source audit

Verdict for the exact imported conjunction: **FALSIFIED**

Verdict for the narrower momentum-specific coefficient statement:
**VERIFIED**

## Exact claim and quantifiers

The imported claim says that, for every `t in [T]`, `delta in (0,1)`, and
admissible constant step size under conditional sub-Gaussian gradient noise,
Theorem 3.6 has:

1. an inertia horizon of order `(1-beta)^-1`;
2. drift-noise coupling proportional to `(1-beta)^-2`; and
3. both features absent from the vanilla-SGD Theorem 3.5 bound.

It is a conjunction, so one false conjunct falsifies it. Source anchors:
`main.tex:501-557` and `appendix.tex:1629-2368`.

## Assumptions and numerical audit

- Conditional sub-Gaussian gradient noise along both `theta_t` and `psi_t`.
- `gamma <= min{1/L, mu(1-beta)^2/(4L^2)}`.
- Zero momentum initialization `theta_-1=theta_0`.
- Source audit grid:
  `beta={.5,.6,.7,.8,.9,.95,.98}` with `mu=1`, `L=10`, and
  `gamma=0.2(1-beta)^2/L`.
- Pathwise route: 40,000 paired Gaussian trials per beta, deterministic seeds
  `260112238` and `260112239`.

The exact assumptions are recorded in the
[claim contract](../../evidence/claim_4/claim_contract.json) and
[source audit](../../evidence/claim_4/source_audit.md).

## Executable verifier

- [Current standalone verifier](../../campaign/repro/src/published_claim_verifier.py)
- [Exact formula/source route](../../campaign/repro/src/exact_contracts.py)
- [Independent pathwise route](../../campaign/repro/src/pathwise_contracts.py)
- [Exact-contract tests](../../campaign/repro/tests/test_exact_contracts.py)
- [Pathwise tests](../../campaign/repro/tests/test_pathwise_contracts.py)

## Pinned environment and fixed command

[pyproject.toml](../../campaign/pyproject.toml),
[uv.lock](../../campaign/uv.lock), and
[.python-version](../../campaign/.python-version) pin Python `3.12`.

```bash
uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py
```

## Raw results shown inline

The decisive evidence is source algebra, not a formula-generated slope plot:

```text
Theorem 3.5 contains:
  gamma^2 sigma^2 D_t^(2) log(2T/delta)

Theorem 3.6 contains:
  gamma^2 sigma^2 D_lag^(2)/(1-beta)^2 log(2T/delta)

Theorem 3.6 contraction rate:
  gamma^2 mu^2/[4(1-beta)^2].

Substitute gamma=c(1-beta)^2:
  rate = c^2 mu^2 (1-beta)^2/4,
  so the reciprocal displayed forgetting horizon is Theta((1-beta)^-2).
```

Thus the SGD bound does contain coupling, and the displayed post-substitution
horizon exponent is `2`, not `1`. The narrower momentum/SGD coefficient ratio
does have exponent `2`.

| β | coefficient ratio | displayed horizon | physical 5% memory |
|---:|---:|---:|---:|
| .50 | `4` | `40,000` | `4.3219` |
| .80 | `25` | `250,000` | `13.4251` |
| .90 | `100` | `1,000,000` | `28.4332` |
| .95 | `400` | `4,000,000` | `58.4040` |
| .98 | `2500` | `25,000,000` | `148.2837` |

Download the [coefficient audit](../../evidence/claim_4/coefficient_audit.csv),
[horizon audit](../../evidence/claim_4/horizon_audit.csv), and
[40,000-trial pathwise data](../../evidence/claim_4/pathwise_coupling.csv).
The coefficient/horizon grids check arithmetic and serialization; they are not
treated as independent complexity evidence.

## Independent checker and negative control

The [independent checker](../../evidence/claim_4/independent_checker.json)
recomputes the source algebra and pathwise coefficient:

- coefficient-ratio exponent `1.9999999999999998`;
- displayed-horizon exponent `2.0000000000000013`;
- pathwise momentum coefficient exponent `2.0000000652`;
- beta-neutral SGD control exponent approximately `0`.

The [negative controls](../../evidence/claim_4/negative_control.json) reject
changing exponent `2 -> 1`, reject erasing the SGD source term, and require
the cross term to be exactly zero at zero drift.

## Failure probe

- [Normal verifier output](../../evidence/current_verifier/claim_4_pass.json):
  exit code `0`.
- [Injected beta-neutral momentum coefficient](../../evidence/current_verifier/claim_4_failure_probe.json):
  exit code `1`, failing `coefficient_ratio_slope_is_two`.

## Limitations and deviations

FALSIFIED applies only to the exact imported conjunction. The narrower claim
that momentum adds a `(1-beta)^-2` coefficient relative to the matched
beta-neutral SGD form is VERIFIED. “Inertia horizon” is used for both the
displayed contraction horizon and physical velocity memory; these are kept
separate. See [limitations](../../evidence/claim_4/limitations.md).

## Revision, seeds, CPU, and runtime

- Pre-migration scientific evidence SHA:
  `61faf82dbc11f46c01b156f8b60ef68bc70d5450`.
- Pre-migration verifier source SHA:
  `a56ee4ac2bb961ee1459245e3a0a3d91b9c73560`.
- Deterministic seeds: `260112238`, `260112239`.
- Python `3.12.11`; 8 CPU cores; macOS arm64.
- Recorded aggregate route runtime: `21.870315125` seconds.
- [Complete run metadata](../../evidence/claim_4/run_metadata.json)
- [Method](../../evidence/claim_4/method.md) and
  [evaluation](../../evidence/claim_4/EVAL.md)
