
# Claim 4 method

The displayed martingale cross term is sampled in 40,000 paired Gaussian
trials for seven beta values at a single step size stable for the entire
sweep.  The analytic two-sided 95% Gaussian envelope is fixed before sampling.
Squared quantiles are normalized by the matched SGD-form drift energy so the
momentum coefficient remains visible.  A zero-drift control must make the cross
term identically zero, and the SGD control must have beta exponent zero.
