---
title: "Repro - Momentum SGD under Nonstationary Drift"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-U1bxeLQLaK
---

# Evaluator-visible evidence surface

This directory is the committed, evaluator-facing text surface for the GitHub
repository [`MachineLearning-Nerd/icml26-momentum-sgd-nonstationary-optimization`](https://github.com/MachineLearning-Nerd/icml26-momentum-sgd-nonstationary-optimization).
Start with the **[current evaluator verification](#/current-verification)**.

The current release contains five claim contracts:

| Claim | Current verdict |
| --- | --- |
| 1 | **VERIFIED** within the finite scaling contract |
| 2 | **BLOCKED** by unresolved universal quantifiers |
| 3 | **VERIFIED** for the declared full-dimensional witness |
| 4 | **FALSIFIED** as the imported conjunction |
| 5 | **BLOCKED** by underspecified source-scale protocol details |

The previous judged pages remain available under **Historical rejected
baseline**. They are preserved provenance, not the current result. The current
standalone checker is
[`campaign/repro/src/published_claim_verifier.py`](campaign/repro/src/published_claim_verifier.py);
its normal run and injected-failure outputs are linked from each current claim
page.

The previous live judge score was `3/10`. This candidate claims no new score.
