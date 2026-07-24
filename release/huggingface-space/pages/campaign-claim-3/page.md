# Campaign Claim 3 — full-dimensional stable tracking

Verdict: **VERIFIED**

This replaces the previous one-dimensional proxy with a faithful
full-dimensional witness for the theorem's existential drift-heavy regime:

- dimension `100`;
- 20 deterministic seeds;
- 5,000 steps;
- normalized random-walk drift with step norm `0.01`;
- `β ∈ {0.5, 0.9, 0.95, 0.98}`;
- SGD uses its sufficient cap; HB and NAG use 80% of the paper's stronger cap.

SGD is below HB and NAG by more than two standard errors at every tested beta.
At `β=0.98`, mean tail squared tracking error is:

| SGD | HB | NAG |
|---:|---:|---:|
| `0.002417` | `0.236482` | `0.231877` |

An independent characteristic-polynomial checker obtains slow-mode half-life
exponent `0.999845` against `κ/(1−β)`. A stationary deterministic negative
control requires HB acceleration.

This is a stochastic witness for an existential regime, not an empirical proof
of universal ordering. Appendix E.6 derives the HB response construction but
does not supply the analogous Nesterov proof; NAG is tested experimentally.

## Evidence

- [claim contract](../../evidence/claim_3/claim_contract.json)
- [source audit](../../evidence/claim_3/source_audit.md)
- [method](../../evidence/claim_3/method.md)
- [evaluation](../../evidence/claim_3/EVAL.md)
- [summary](../../evidence/claim_3/stability_summary.csv)
- [all trials](../../evidence/claim_3/stability_trials.csv)
- [independent checker](../../evidence/claim_3/independent_checker.json)
- [independent spectral data](../../evidence/claim_3/independent_spectral_checker.csv)
- [negative control](../../evidence/claim_3/negative_control.json)
- [limitations](../../evidence/claim_3/limitations.md)
- [run metadata](../../evidence/claim_3/run_metadata.json)

