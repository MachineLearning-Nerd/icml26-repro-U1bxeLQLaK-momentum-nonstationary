
# Claim 3 source audit

Source: arXiv `2601.12238v4`, archive SHA-256
`89ad9ad897d3f9a0210ceab3e61adb356bf32edaa49621c0234a426aef3b3fa9`.

Theorem 3.7 is existential and minimax over constant-step `SGDM(beta)`
policies. Appendix E.6 proves the inertia construction explicitly for
Heavy-Ball and says only that a similar Nesterov analysis *can* be carried out.
The paper's sufficient finite-time cap is
`gamma <= mu(1-beta)^2/(4L^2)`; its lower-bound theorem uses the looser
constant-hidden form `gamma <= c0(1-beta)^2/L`.

The machine contract therefore checks an admissible drift-heavy witness, the
exact Heavy-Ball response mechanism, and both momentum implementations. It does
not turn the paper's unproved Nesterov sentence into a formal theorem.
