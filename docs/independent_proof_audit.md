# Independent theorem and protocol audit

Source PDF: arXiv `2601.12238`, SHA-256
`415533d734236070ec5180fdcf6fcc9454dc55a20913f219b5d7f1be19776032`.
Source archive: SHA-256
`89ad9ad897d3f9a0210ceab3e61adb356bf32edaa49621c0234a426aef3b3fa9`.

## C1 — explicit drift amplification

Theorem 3.3 requires
`gamma <= mu(1-beta)^2/(4L^2)`.  Its simplified Equation 3.5 has drift floor

`((2+beta)^2 Delta^2)/(gamma^2 mu^2)`

up to the theorem’s universal comparison constant.  Substituting `gamma=.8` of
the stability cap creates the explicit beta divergence, rather than merely
plotting an optimizer failure. Across beta `.5` to `.999` the independently
evaluated floor rises by `8.994e10` and the direct post-jump response time rises
from 8 to 4,011 steps.  The product `(1-beta)*response_time` stays within 1.02,
confirming the `1/(1-beta)` inertia-window mechanism.

The stationary variance decreases under this deliberately conservative cap
because its step size shrinks; the audit does not mislabel that fact as a
contradiction. The claim is the drift/stability penalty, which the direct
response recurrence isolates.

## C2 — source-scale drifting-quadratic experiment

Appendix F specifies a normalized Gaussian target walk with fixed step `.01`,
`d=100`, 20 independent runs, and `T=5000`.  The objective is
`f_t(theta)=.5 ||theta-theta*_t||^2`; gradients add independent
`N(0,sigma^2 I)` noise.  The grid has gammas `{.01,.05,.10}`, betas
`{.50,.90,.95,.99}`, and noise variances `{.1,.5,.8}`. The generalized source
updates are implemented exactly: HB uses `(beta1,beta2)=(0,beta)`, NAG uses
`(beta,0)`.

All 108 method cells and all 2,160 source-scale trials are retained. In all 36
matched `(gamma,beta,sigma^2)` scenarios, SGD’s final mean tracking error is
strictly smaller than both HB and NAG. A stationary deterministic control with
beta=.5 shows HB can accelerate transient convergence, preventing an overbroad
“momentum always hurts” interpretation.

The rendered PDF’s Table 1 numbers differ from the archived `appendix.tex`
numbers (for example its first entry is about 1.036 vs 0.056 in the archive).
The live claim is qualitative and the archive supplies the executable-level
protocol; both the source discrepancy and all clean-room raw results are kept
in the bundle.

## C3 — lower-bound inertia mechanism

Theorem 3.9’s lower bound includes an inertia-limited term under the same
stability constraint.  Independently of the paper’s proof text, the audit takes
the stated one-dimensional hard quadratic after a jump `0 -> 1` and evolves
the exact Heavy-Ball two-state recurrence. It then alternates `+1/-1` target
blocks and sums the instantaneous quadratic regret. This is a constructive
certificate of stale-gradient lag: at beta=.999 the response window and
eight-block regret are respectively 501.375x and 526.97x those at beta=.5.
The response scaling and positive regret at every beta supply the claimed
information/inertia obstruction’s finite hard-instance mechanism.
