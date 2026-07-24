
# Claim 5 route 2 method

Generate every 256-example Gaussian mini-batch explicitly. The same covariates,
labels, target path, initialization, and base step size are shared by SGD, HB,
and NAG within each seed. Retain per-seed tail and final squared parameter
tracking error. Require all trials to remain finite, both momentum methods to
worsen by at least 20% at kappa 1000, and SGD to have the lowest high-kappa
mean. The independent checker reads only the saved summary.
