# Claim 4 source audit

Source: arXiv `2601.12238v4`, retrieved 2026-07-23 from
`https://export.arxiv.org/e-print/2601.12238` (archive SHA-256
`89ad9ad897d3f9a0210ceab3e61adb356bf32edaa49621c0234a426aef3b3fa9`).

Theorem 3.5 (`main.tex:524-535`) contains the vanilla-SGD concentration term
`gamma^2 sigma^2 D_t^(2) log(2T/delta)`. Therefore drift--noise coupling is
not literally absent from the vanilla bound.

Theorem 3.6 (`main.tex:539-555`) contains
`gamma^2 sigma^2 D_lag^(2)/(1-beta)^2`, so at fixed `gamma` and matched drift
functional its coefficient relative to SGD is exactly `(1-beta)^-2`.

The same displayed theorem forgets initialization at rate
`exp[-gamma^2 mu^2 t/(4(1-beta)^2)]`. Substituting its stability scaling
`gamma=c(1-beta)^2/L` yields a displayed-bound horizon proportional to
`(1-beta)^-2`, not `(1-beta)^-1`. A separate physical velocity-memory horizon
does scale as `(1-beta)^-1`, but that does not repair the exact theorem claim.
