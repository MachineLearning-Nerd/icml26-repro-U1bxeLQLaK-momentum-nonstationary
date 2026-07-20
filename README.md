# On the Provable Suboptimality of Momentum SGD in Nonstationary Stochastic Optimization

Full-scope reproduction of all three active ICML 2026 challenge claims for
OpenReview `U1bxeLQLaK` / arXiv `2601.12238`.

- C1 independently evaluates the explicit beta-dependent Theorem-3.3 stability
  cap and drift floor, then directly measures the post-shift response window.
- C2 reruns the complete Appendix-F/Table-1 drifting-quadratic protocol: three
  step sizes, four momenta, three noise variances, all SGD/HB/NAG methods, 20
  seeds and 5,000 steps at d=100—108 method cells and 2,160 full trials.
- C3 constructs the theorem’s deterministic block-switching quadratic mechanism
  directly and verifies its beta-dependent inertia window and cumulative regret.

The arXiv source archive contains paper assets but no executable experiment
repository.  This is therefore a clean-room implementation of the equations and
fully stated Appendix-F protocol, not a proxy benchmark.  The archive TeX Table
1 and the rendered PDF differ numerically; the current source-archive protocol
is pinned and the rerun agrees with that TeX table’s scale. This discrepancy is
documented, not hidden.

## Run

```bash
PYTHONPATH=repro/src .venv/bin/pytest -q repro/tests
PYTHONPATH=repro/src .venv/bin/python repro/src/run_theory_certificates.py
PYTHONPATH=repro/src .venv/bin/python repro/src/run_quadratic_grid.py
PYTHONPATH=repro/src .venv/bin/python repro/src/verify_claims.py
```
