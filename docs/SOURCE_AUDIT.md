# Source audit

## Paper identity

The paper under audit is [arXiv:2601.12238](https://arxiv.org/abs/2601.12238),
OpenReview `U1bxeLQLaK`, by Sharan Sahu, Cameron J. Hogan, and Martin T. Wells.
The committed PDF and source archive were retrieved for the v4 evidence run on
2026-07-23. The arXiv record has since advanced to v5; this repository does
not silently mix v5 text into v4 numerical evidence.

The pinned files are:

| File | SHA-256 |
| --- | --- |
| [`docs/primary.pdf`](../docs/primary.pdf) | `415533d734236070ec5180fdcf6fcc9454dc55a20913f219b5d7f1be19776032` |
| [`docs/arxiv_source.tar`](../docs/arxiv_source.tar) | `89ad9ad897d3f9a0210ceab3e61adb356bf32edaa49621c0234a426aef3b3fa9` |

## What is and is not available

The archive contains `main.tex`, `appendix.tex`, TeX definitions, the
bibliography, and paper figures. It does not contain an executable author
experiment repository, a lockfile for the paper's experiments, raw per-seed
metrics, or the missing implementation details for all Section 4 model
classes. The repository therefore uses a clean-room implementation for the
finite audits and labels source-scale claims that cannot be reproduced exactly
as `BLOCKED`.

The presence of figures in the source archive is not treated as raw numerical
evidence. Figures are useful for source interpretation; the current gate relies
on the committed CSV/JSON evidence and independent recomputation instead.

## Source anchors used by the contracts

The claim contracts record the exact `main.tex`/`appendix.tex` ranges used for
each audit. The current evaluator-visible evidence is under
[`release/huggingface-space/evidence`](../release/huggingface-space/evidence),
and every claim page links its source audit, method, raw results, checker,
negative control, and limitations.

## Integrity rule

Do not replace the pinned PDF/source archive without changing
`sources.json`, the claim contracts, and the gate output together. A newer
arXiv revision may be useful for a future audit, but it is a different source
snapshot and must receive a new evidence run.
