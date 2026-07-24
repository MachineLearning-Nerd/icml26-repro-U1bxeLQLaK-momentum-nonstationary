# Campaign Claim 1 — current accepted-evidence regression

Verdict: **VERIFIED**

## Exact claim and quantifiers

Theorem 3.3 states that, for every `t >= 0`, uniformly strongly monotone and
Lipschitz mean gradients with bounded drift/noise second moments, fixed
`beta in [0,1)`, and
`gamma <= mu(1-beta)^2/(4L^2)`, the displayed momentum tracking bound contains

```text
(1-beta)^-2 exp[-gamma mu t/(1-beta)] ||theta_0-theta*_0||^2
+ (2+beta)^2 Delta^2/(gamma^2 mu^2)
+ sigma^2 gamma/[mu(1-beta)].
```

The exact tested claim is about these displayed beta coefficients compared
with the beta-neutral SGD bound in Theorem 3.1. It is not a claim that a finite
simulation proves the full upper-bound theorem. Source anchors:
`main.tex:373-383` and `main.tex:269-275`.

## Assumptions and numerical audit

| Audit item | Published value |
|---|---:|
| Operator Hessian mode | `h=1` |
| β grid | `0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.98` |
| Step rule | `gamma=0.2(1-beta)^2` |
| Stable lifted operators | `7/7` |
| Plain-SGD transient amplification | `1.0` |
| Noise experiment dimension | `5` |
| Deterministic seed | `0` |

The theorem assumptions and source hashes are in the
[claim contract](../../evidence/claim_1/claim_contract.json) and
[source audit](../../evidence/claim_1/source_audit.md).

## Executable verifier

- [Current standalone verifier](../../campaign/repro/src/published_claim_verifier.py)
- [Current Claim 1 generator/wrapper](../../campaign/repro/src/claim1_regression.py)
- [Accepted transient script](../../campaign/repro/src/verify_c0_transient.py)
- [Accepted noise-floor script](../../campaign/repro/src/verify_tracking.py)
- [Verifier test](../../campaign/repro/tests/test_claim1_regression.py)

The standalone verifier reads only the two raw JSON files below and recomputes
both log-log slopes. It never reads their precomputed `predicted_*` columns.

## Pinned environment and fixed command

[pyproject.toml](../../campaign/pyproject.toml),
[uv.lock](../../campaign/uv.lock), and
[.python-version](../../campaign/.python-version) pin Python `3.12`.

```bash
uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py
```

## Raw results shown inline

| β | `rho(M)` | measured `G²` | noise floor / SGD |
|---:|---:|---:|---:|
| .50 | .88508 | 6.289 | 2.020 |
| .60 | .90506 | 10.457 | — |
| .70 | .92633 | 20.137 | — |
| .80 | .94907 | 49.155 | 4.910 |
| .90 | .97352 | 213.622 | 10.087 |
| .95 | .98648 | 891.367 | 19.218 |
| .98 | .99452 | 5714.591 | 48.472 |

Recomputed transient exponent: `2.1149370789`. Recomputed noise-floor
exponent: `0.9868074461`.

Download [transient raw JSON](../../evidence/claim_1/transient_results.json) and
[noise-floor raw JSON](../../evidence/claim_1/noise_floor_results.json).

## Independent checker and negative control

The [independent checker](../../evidence/claim_1/independent_checker.json)
reports `passed=true`, transient slope `2.1149370789`, noise slope
`0.9868074461`, all operators stable, and SGD amplification `1.0`.

The [negative control](../../evidence/claim_1/negative_control.json) rejects
both exponent mutations: initialization `2 -> 1` and noise `1 -> 2`.

## Failure probe

- [Normal verifier output](../../evidence/current_verifier/claim_1_pass.json):
  exit code `0`.
- [Injected wrong-transient-scaling output](../../evidence/current_verifier/claim_1_failure_probe.json):
  exit code `1`, failing `transient_slope_in_interval_1.9_2.3`.

## Limitations and deviations

The source formula audit verifies what Theorem 3.3 displays. The operator and
noise experiments independently corroborate its two mechanisms but do not
constitute a universal proof of the theorem. The noise experiment is a
five-dimensional well-conditioned quadratic. Full details:
[limitations](../../evidence/claim_1/limitations.md).

## Revision, seeds, CPU, and runtime

- Scientific evidence Git SHA:
  `ca408ac731d288f21cd8ebfc9fb4d5d4ea8a1ef1`.
- Current published-verifier code commit:
  `a56ee4ac2bb961ee1459245e3a0a3d91b9c73560`.
- Seed: `0`.
- Python `3.12.11`; 8 CPU cores; macOS arm64.
- Claim runtime: `21.858946917` seconds.
- [Complete run metadata](../../evidence/claim_1/run_metadata.json)
- [Method](../../evidence/claim_1/method.md) and
  [evaluation](../../evidence/claim_1/EVAL.md)
