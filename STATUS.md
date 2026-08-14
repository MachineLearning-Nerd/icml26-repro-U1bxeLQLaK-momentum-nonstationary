# Status

- Paper: `U1bxeLQLaK` — *On the Provable Suboptimality of Momentum SGD in Nonstationary Stochastic Optimization*
- Authors: Sharan Sahu, Cameron J. Hogan, and Martin T. Wells
- Scope: five current claim contracts; clean-room evidence; no author executable repository released in the pinned source archive
- Evidence gate: `SCOPED_PASS`
- Overall scientific status: `VERIFIED_SCOPED_WITH_FALSIFIED_AND_BLOCKED_CLAIMS`
- Strict paper-level status: `NOT_READY`
- Previous live evaluator score: `3/10` (historical; no new score claimed)

## Current claim verdicts

| Claim | Verdict | Reason boundary |
| --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | Both expected scaling slopes are independently recomputed from raw JSON |
| C2 | `BLOCKED_UNIVERSAL_QUANTIFIERS` | Specialized finite routes pass, but all `p,q` and policy quantifiers are not closed |
| C3 | `VERIFIED_SCOPED` | Full-dimensional finite witness satisfies the declared stability and seed contract |
| C4 | `FALSIFIED_AS_WRITTEN_WITH_NARROWER_COMPONENT_VERIFIED` | The conjunction disagrees with the displayed source formula; the narrower momentum coefficient survives |
| C5 | `BLOCKED_PROTOCOL_UNDERSPECIFIED` | Four routes and a mandatory falsification audit do not establish an exact source-scale replication |

The current verifier's `passed` field means that the expected scientific
verdict is supported by the shipped evidence. It is not a count of paper
claims that passed.

## Evidence and provenance

- PDF: `docs/primary.pdf`, SHA-256 `415533d734236070ec5180fdcf6fcc9454dc55a20913f219b5d7f1be19776032`
- Source archive: `docs/arxiv_source.tar`, SHA-256 `89ad9ad897d3f9a0210ceab3e61adb356bf32edaa49621c0234a426aef3b3fa9`
- Paper/source metadata: [`sources.json`](sources.json)
- Claim ledger: [`docs/CLAIM_EVIDENCE.md`](docs/CLAIM_EVIDENCE.md)
- Branch migration: [`docs/BRANCH_AUDIT.md`](docs/BRANCH_AUDIT.md)
- Gate procedure: [`docs/PUBLICATION_GATE.md`](docs/PUBLICATION_GATE.md)

## Reproduction boundary

The default gate is local CPU and evidence-first. It validates the pinned
source hashes, five evaluator-facing verifiers, five injected-failure probes,
focused tests, and the deterministic evidence manifest. It does not rerun the
full historical campaign by default. The paper's universal theorem proof,
source-scale logistic/MLP experiments, and an external evaluator score remain
outside the verified scope.
