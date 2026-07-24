# Campaign Claim 2 — minimax decomposition

Verdict for the full theorem contract: **BLOCKED**

Scoped results: three non-circular routes pass, but they do not close the
universal theorem quantifiers. The mandatory fourth falsification route found
no valid counterexample.

## Exact claim and quantifiers

Theorem 3.7 fixes arbitrary `1 <= p,q <= infinity`, defines
`alpha=1+d/p`, and takes

```text
inf over every constant-step policy pi in Pi_beta
sup over every G with GVar_p,q(G) <= V_T
R_T^pi(G).
```

For `gamma <= c0(1-beta)^2/L`, it lower-bounds this minimax risk by the
maximum of a statistical term and an inertia term, with beta exponents
`2/(alpha q+2)` and `2/(alpha q)`. The exact anchors are
`main.tex:600-638` and `appendix.tex:2373-3710`.

The current contract does **not** replace “all `p,q` and every policy” with one
Gaussian family. Appendix E.6 explicitly proves the inertia response for
Heavy-Ball and says only that a similar Nesterov analysis can be carried out.
That unresolved universal policy step is why the aggregate verdict is BLOCKED.

## Assumptions and numerical audit

The scoped `p=infinity, q=1` statistical route uses:

| Quantity | Value |
|---|---:|
| Strong convexity `mu` | `1` |
| Dimension | `8` |
| Gaussian hypotheses | `16` |
| Samples per hypothesis | `4` |
| Noise `sigma` | `1` |
| Realized gradient-variation budget | `0.230367274176739` |
| Budget upper bound | `0.230367274176969` |
| Recomputed maximum pairwise KL | `0.554517744447956` |
| Optimizer-independent residual transcript | `true` |

The [claim contract](../../evidence/claim_2/claim_contract.json) records the
full quantifier gap rather than silently specializing the theorem.

## Executable verifier

- [Current standalone verifier](../../campaign/repro/src/published_claim_verifier.py)
- [Symbolic/source specialization](../../campaign/repro/src/exact_contracts.py)
- [Finite Fano and pathwise route](../../campaign/repro/src/pathwise_contracts.py)
- [Full-dimensional stability route](../../campaign/repro/src/remaining_contracts.py)
- [Universal calibration and route 4](../../campaign/repro/src/evaluator_visible_release.py)
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

| Route | Scope | Direct result | Verdict |
|---|---|---:|---:|
| 1 | symbolic `p=∞,q=1` specialization | statistical exponent `0.6666667`; inertia exponent `2.0000000` | scoped pass |
| 2 | 16-way finite Fano family | lower bound `0.55`; empirical optimal error `0.854820 ± 0.001575` | scoped pass |
| 3 | `d=100`, 20-index pathwise witness | SGD below HB/NAG in every tested β | scoped pass |
| 4 | full-quantifier falsification audit | `0/4` valid assumption-complete counterexamples | BLOCKED |

The formula-evaluated [theory grid](../../evidence/claim_2/theory_grid.csv) is
only a visualization of the displayed terms. It is **not** used as independent
scaling evidence. The information-theoretic evidence is the independently
checked [Fano certificate](../../evidence/claim_2/fano_certificate.json) and
[50,000-trial raw Monte Carlo](../../evidence/claim_2/fano_monte_carlo.json).
The route-4 candidates are downloadable as
[JSON](../../evidence/claim_2/route_4_falsification_audit/candidate_counterexamples.json).

## Independent checker and negative control

The [aggregate independent checker](../../evidence/claim_2/independent_checker.json)
reports that all three scoped routes pass, route 4 is complete, and
`universal_quantifiers_closed=false`.

The finite-route control is a stationary deterministic quadratic: HB error
`0.0314254730` versus SGD `0.1953661516`, rejecting “momentum always hurts.”
Route 4 separately rejects treating a missing proof as a counterexample.
See [route-4 control](../../evidence/claim_2/route_4_falsification_audit/negative_control.json).

## Failure probe

- [Normal audit-verifier output](../../evidence/current_verifier/claim_2_pass.json):
  exit code `0`; it verifies the internally consistent **BLOCKED** record.
- [Injected invalid-Fano-bound output](../../evidence/current_verifier/claim_2_failure_probe.json):
  exit code `1`, failing `finite_fano_bound_below_empirical_error`.

An exit code `0` here verifies the published audit and its BLOCKED conclusion;
it does not turn the universal theorem into a pass.

## Limitations and deviations

The first three routes cover a valid specialization and two finite witnesses.
They are not a proof certificate for every `p,q` and every policy in
`Pi_beta`. Route 4 found no valid falsification. Full resolution needs a
policy-complete derivation including Nesterov, or an assumption-satisfying
counterexample. See [limitations](../../evidence/claim_2/limitations.md) and
[route-4 evaluation](../../evidence/claim_2/route_4_falsification_audit/EVAL.md).

## Revision, seeds, CPU, and runtime

- Scientific evidence Git SHA:
  `61faf82dbc11f46c01b156f8b60ef68bc70d5450`.
- Current verifier code commit:
  `a56ee4ac2bb961ee1459245e3a0a3d91b9c73560`.
- Deterministic seeds: `260112238`, `260112239`.
- Python `3.12.11`; 8 CPU cores; macOS arm64.
- Recorded route runtime: `21.870315125` seconds.
- [Complete run metadata](../../evidence/claim_2/run_metadata.json)
- [Source audit](../../evidence/claim_2/source_audit.md),
  [method](../../evidence/claim_2/method.md), and
  [aggregate evaluation](../../evidence/claim_2/EVAL.md)
