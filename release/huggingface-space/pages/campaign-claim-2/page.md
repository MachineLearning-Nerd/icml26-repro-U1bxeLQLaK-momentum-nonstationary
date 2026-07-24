# Campaign Claim 2 — minimax decomposition

Verdict: **VERIFIED**

Theorem 3.7 is audited as a restricted minimax statement over constant-step
`SGDM(β)` policies. The valid `p=∞, q=1` specialization yields:

- statistical-term beta exponent: `0.6666666667`;
- inertia-term beta exponent: `2.0000000000`;
- low-variation statistical dominance for every tested beta: `true`;
- high-variation inertia dominance for every tested beta: `true`.

A separate information-theoretic route uses 16 Gaussian hypotheses observed
through four noisy gradients. The finite Fano lower bound is `0.55`; 50,000
deterministic trials give optimal-classifier error
`0.854820 ± 0.001575` (one SE). Three optimizer-query trajectories yield the
same residual transcript after subtracting the known query.

The independent pathwise route also requires SGD to beat HB and NAG in every
source-scale stability scenario. A stationary control requires HB to
accelerate, rejecting “momentum always hurts.”

## Evidence

- [claim contract](../../evidence/claim_2/claim_contract.json)
- [source audit](../../evidence/claim_2/source_audit.md)
- [method](../../evidence/claim_2/method.md)
- [evaluation](../../evidence/claim_2/EVAL.md)
- [theory grid](../../evidence/claim_2/theory_grid.csv)
- [Fano certificate](../../evidence/claim_2/fano_certificate.json)
- [Fano Monte Carlo](../../evidence/claim_2/fano_monte_carlo.json)
- [independent checker](../../evidence/claim_2/independent_checker.json)
- [negative control](../../evidence/claim_2/negative_control.json)
- [limitations](../../evidence/claim_2/limitations.md)
- [run metadata](../../evidence/claim_2/run_metadata.json)

