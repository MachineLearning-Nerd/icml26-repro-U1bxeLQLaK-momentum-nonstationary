# Campaign Claim 5 — four condition-number routes

Verdict: **BLOCKED**

The missing condition-number component was tested through three materially
different faithful interpretations:

| Route | HB `κ=1000/κ=10` | NAG `κ=1000/κ=10` | SGD `κ=1000/κ=10` |
|---|---:|---:|---:|
| Exact-moment Gaussian oracle | `0.0178909` | `0.0693054` | `1.15849` |
| Literal raw mini-batches | `0.0183067` | `0.0707293` | `1.08564` |
| Exact spectral covariance | `0.0301903` | `0.0874964` | `1.18482` |

Every HB/NAG ratio is below one, meaning the high-condition-number endpoint
improved tracking—the opposite of the paper's reported direction. The raw
route retains all 120 finite trials. The spectral route has maximum Lyapunov
residual `2.71e-19`.

This disagreement is not promoted to a falsification. The empirical claim is
finite and descriptive, and no executable author implementation resolves the
remaining normalization/data-path ambiguity. The mandatory fourth route
audited four possible counterexamples against the exact assumptions; zero were
valid assumption-complete contradictions.

## Evidence

- [aggregate contract](../../evidence/claim_5/claim_contract.json)
- [aggregate evaluation](../../evidence/claim_5/EVAL.md)
- [aggregate source audit](../../evidence/claim_5/source_audit.md)
- [route 1 evaluation](../../evidence/claim_5/route_1_moment_matched/EVAL.md)
- [route 2 evaluation](../../evidence/claim_5/route_2_raw_minibatch/EVAL.md)
- [route 3 evaluation](../../evidence/claim_5/route_3_exact_spectral/EVAL.md)
- [route 4 evaluation](../../evidence/claim_5/route_4_falsification_audit/EVAL.md)
- [route 4 candidate audit](../../evidence/claim_5/route_4_falsification_audit/candidate_counterexamples.csv)
- [independent checker](../../evidence/claim_5/independent_checker.json)
- [negative control](../../evidence/claim_5/negative_control.json)
- [limitations](../../evidence/claim_5/limitations.md)
- [run metadata](../../evidence/claim_5/run_metadata.json)

