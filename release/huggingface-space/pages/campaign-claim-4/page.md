# Campaign Claim 4 — exact source audit

Verdict for the exact imported conjunction: **FALSIFIED**

Verdict for the narrower momentum-specific coefficient interpretation:
**VERIFIED**

The displayed formulas establish three distinct facts:

1. Theorem 3.5 contains the vanilla-SGD coupling term
   `γ²σ²D_t² log(2T/δ)`. Coupling is therefore not literally absent.
2. Theorem 3.6 contains `γ²σ²D_lag²/(1−β)²`. Its coefficient relative to the
   matched SGD form has exponent `2.000000`.
3. Substituting Theorem 3.6's own stability scaling into its displayed
   exponential gives a forgetting-horizon exponent of `2.000000`, not `1`.

The exact imported claim is conjunctive, so facts 1 and 3 falsify it. The
beta-specific momentum amplification remains correct.

An independent pathwise route samples 40,000 paired Gaussian trials at seven
beta values. It obtains a squared-envelope exponent `2.00000007`, beta-neutral
SGD exponent numerically zero, minimum prespecified 95% coverage `0.95075`,
and physical velocity-memory exponent `1.09091`.

## Evidence

- [aggregate contract](../../evidence/claim_4/claim_contract.json)
- [aggregate source audit](../../evidence/claim_4/source_audit.md)
- [aggregate evaluation](../../evidence/claim_4/EVAL.md)
- [source coefficient audit](../../evidence/claim_4/coefficient_audit.csv)
- [source horizon audit](../../evidence/claim_4/horizon_audit.csv)
- [pathwise coupling data](../../evidence/claim_4/pathwise_coupling.csv)
- [pathwise summary](../../evidence/claim_4/coupling_summary.json)
- [independent checker](../../evidence/claim_4/independent_checker.json)
- [negative controls](../../evidence/claim_4/negative_control.json)
- [limitations](../../evidence/claim_4/limitations.md)

The two interpretations are retained separately under
`evidence/claim_4/route_1_source_contract/` and
`evidence/claim_4/route_2_pathwise_coefficient/`.

