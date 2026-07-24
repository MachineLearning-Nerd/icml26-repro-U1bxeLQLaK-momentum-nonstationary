# Campaign Claim 1 — accepted evidence regression

Verdict: **VERIFIED**

The exact scripts accepted by the previous live judge are now executed inside
the fixed cumulative command, rather than merely preserved as old pages.

- squared worst-case transient-growth slope: `2.1149370789`
  (judged display `2.115`);
- stationary noise-floor slope: `0.9868074461`
  (judged display `0.987`);
- all lifted Heavy-Ball operators stable: `true`;
- plain-SGD transient amplification: `1.0`;
- independent recomputation from raw JSON: `passed`;
- mutated exponents rejected: `passed`.

The transient experiment measures the worst-case amplification of the stable
non-normal lifted Heavy-Ball operator, which is the initialization mechanism
behind the `(1−β)⁻²` coefficient. The noise route measures the separate
`(1−β)⁻¹` stationary floor.

## Evidence

- [claim contract](../../evidence/claim_1/claim_contract.json)
- [source audit](../../evidence/claim_1/source_audit.md)
- [method](../../evidence/claim_1/method.md)
- [evaluation](../../evidence/claim_1/EVAL.md)
- [transient raw output](../../evidence/claim_1/transient_results.json)
- [noise-floor raw output](../../evidence/claim_1/noise_floor_results.json)
- [independent checker](../../evidence/claim_1/independent_checker.json)
- [negative control](../../evidence/claim_1/negative_control.json)
- [limitations](../../evidence/claim_1/limitations.md)
- [run metadata](../../evidence/claim_1/run_metadata.json)

