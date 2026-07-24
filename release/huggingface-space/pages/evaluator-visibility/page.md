# Evaluator-blind visibility review

The first review began from a clean download at Git
`8382d0f78c480d6ef2408a3d2313e9e4873b688b`, used only `README.md`,
`pages/index.md`, `logbook.json`, and reachable links, and found every claim
not release-ready. Its complete opened-file record is
[downloadable here](../../evidence/evaluator_blind_review/first_pass.json).

After navigation, inline evidence, code, environment, and failure-probe fixes,
the same constrained traversal was repeated. Its opened-file record and
machine-readable matrix are
[downloadable here](../../evidence/evaluator_blind_review/second_pass.json).

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | `#/campaign-claim-1` | yes | yes | yes | yes | yes | yes | RELEASE-READY |
| 2 | `#/campaign-claim-2` | yes | yes | yes | yes | yes | yes | RELEASE-READY as BLOCKED |
| 3 | `#/campaign-claim-3` | yes | yes | yes | yes | yes | yes | RELEASE-READY for existential contract |
| 4 | `#/campaign-claim-4` | yes | yes | yes | yes | yes | yes | RELEASE-READY as FALSIFIED |
| 5 | `#/campaign-claim-5` | yes | yes | yes | yes | yes | yes | RELEASE-READY as BLOCKED |

“Release-ready as BLOCKED” means the evaluator can inspect why the scientific
claim remains unresolved. It does not forecast points.
