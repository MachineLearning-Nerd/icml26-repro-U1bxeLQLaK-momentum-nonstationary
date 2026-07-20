# Status

- Paper: `U1bxeLQLaK` — *On the Provable Suboptimality of Momentum SGD in Nonstationary Stochastic Optimization*
- Owner: `codex-momentum-nonstationary-three-claims`
- State: `queued_for_hf_publication`
- Effective contract: 3 anchored claims / 6 possible points
- Primary source: arXiv `2601.12238`, PDF SHA-256 `415533d734236070ec5180fdcf6fcc9454dc55a20913f219b5d7f1be19776032`
- Source archive SHA-256: `89ad9ad897d3f9a0210ceab3e61adb356bf32edaa49621c0234a426aef3b3fa9`

## Current step

All three claims pass: 3/3 verified, 6/6 points. The full Appendix-F/Table-1
drifting-quadratic grid completed 108 method cells / 2,160 full 5,000-step
trials; SGD beats HB and NAG in all 36 matched scenarios. The independent
Theorem-3.3/3.9 certificates and all six tests pass. Evidence bundle:
`outputs/evidence_bundle.jsonl` (35,953 bytes, SHA-256
`b2fc0a41882bb941b707023dc7a06c783a34869a8f6a6d8fdfb2659b7fb05c11`).

## Next action

Public GitHub commit `6833699` is pushed and canonical backlog entry 55 was
added atomically. The single shared publisher owns Hugging Face Space creation,
artifact upload, and public readback; do not start a competing publisher.

## Blockers

None known. The source archive contains paper assets but no released executable
experiment code, so the simulation is a clean-room implementation of the
explicit Appendix-F protocol.
