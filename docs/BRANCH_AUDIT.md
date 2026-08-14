# Branch audit and migration

The original repository used `master` for the presentation surface and
`orx/*` for experiment/release work. Those names exposed internal queue
machinery rather than the scientific role of a branch. The published branch
set keeps every original branch tip but gives each branch a descriptive name.

The hashes below are the original remote tips before the identity and naming
migration. Commit identities are normalized to
`MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>` in the
published history. Because rewriting identities changes commit IDs, use the
final remote branch tip or the tracker entry for post-migration hashes.

| Original branch | Original tip | Published branch | What it does |
| --- | --- | --- | --- |
| `master` | `275d817ddbc3c13ae44911614157ef41fa5aa9b7` | `main` | Canonical README, status, source pins, claim ledger, and publication gate |
| `orx/validated-baseline-at-0181de32` | `7bd23cd65b437a10ca0d742d976e78a365eb0f80` | `baseline/validated-0181de32` | Frozen starting point and accepted baseline regression |
| `orx/theory-first-exact-contracts` | `e1e0d5e826dd16bd600c2f772c62542a17bc07f3` | `audit/theory-exact-contracts` | Exact theorem specialization and source-algebra audit |
| `orx/simulation-first-pathwise-contracts` | `976dbde28907b70eafeed25acf6e10b263890f98` | `audit/pathwise-contracts` | Independent pathwise checks for Claims 2 and 4 |
| `orx/integrated-exact-and-pathwise-evidence` | `64055ad8ee504b81cc958fb15ecb682cdcbd6715` | `audit/integrated-exact-pathwise` | Integrated exact and pathwise evidence branch |
| `orx/claim-5-mandatory-falsification-audit` | `61faf82dbc11f46c01b156f8b60ef68bc70d5450` | `audit/claim-5-falsification` | Full-dimensional Claim 3 and mandatory Claim 5 falsification audit |
| `orx/cumulative-accepted-claim-1-regressions` | `ca408ac731d288f21cd8ebfc9fb4d5d4ea8a1ef1` | `regression/claim-1-accepted` | Cumulative rerun of the previously accepted Claim 1 evidence |
| `orx/full-dimensional-stability-and-robustness` | `eb4d8cb1aa85aa677db78ad7d92a7ffb6c686c58` | `experiment/full-dimensional-stability` | Full-dimensional stability and robustness route |
| `orx/raw-minibatch-condition-number-route` | `d766b6d5692855c1af1727e3dc0a1e7442a30691` | `experiment/kappa-raw-minibatch` | Raw-minibatch condition-number route for Claim 5 |
| `orx/exact-spectral-condition-number-route` | `eb254ad8472d0ccb4f4aecc4dad32fee5ca24fd0` | `experiment/kappa-spectral` | Exact spectral covariance route for Claim 5 |
| `orx/evaluator-visible-evidence-gate` | `4262c042f9f983c31b541f8f5b61b27cdfff2b9a` | `release/evaluator-visible-gate` | Current evidence visibility, independent verifier, and failure probes |
| `orx/publication-ready-evaluator-snapshot` | `062d41865ad288b63c7d5b42c82265fb03c9226a` | `release/evaluator-snapshot` | Evaluator-facing snapshot and provenance record |
| `orx/release-candidate-evidence-and-report` | `62cf19ff8ed8a59405566259db8b9d021dfe3710` | `release/candidate-evidence` | Candidate evidence and technical report |
| `orx/final-cumulative-release-snapshot` | `8382d0f78c480d6ef2408a3d2313e9e4873b688b` | `release/final-snapshot` | Cumulative release snapshot before the evaluator-visible gate |

## Naming rules

- `main` is the only canonical presentation branch.
- `baseline/` records frozen starting points.
- `audit/` records proof, source, and falsification audits.
- `regression/` records reruns of accepted evidence.
- `experiment/` records a specific finite experiment route.
- `release/` records packaging and evaluator-facing surfaces.
- No published branch uses `orx/`, queue IDs, or an opaque generated name.

The branch role is provenance, not a scientific endorsement. The claim ledger
on `main` is the authoritative summary of what the evidence supports.
