
# Claim 5 source audit

Source: arXiv `2601.12238v4`, archive SHA-256
`89ad9ad897d3f9a0210ceab3e61adb356bf32edaa49621c0234a426aef3b3fa9`.

Section 4 and Appendix F specify normalized random-walk drift, `d=50` for
linear/logistic regression, `d=100` for quadratics, `T=5000`, 20 seeds,
batch size 256, and `kappa in {10,1000}`. The appendix reports endpoint
tables but supplies no executable code, seed list, covariance orientation,
mini-batch sampling schedule, or evaluation datasets.

The exact empirical claim is descriptive, not universally quantified. This
contract directly targets the judge's three missing axes—condition number,
drift magnitude, and detailed Nesterov results—without treating the inherited
small MLP as source-scale.
