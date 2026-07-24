
# Claim 3 method

Run a `d=100`, 20-seed, 5000-step diagonal quadratic with a normalized random
walk of fixed step norm `0.01`. SGD uses its own sufficient cap; HB and NAG use
80% of the paper's stronger momentum cap. Every seed's tail and final squared
tracking error is retained. A two-standard-error separation is required at
each beta.

An independent checker computes the slow Heavy-Ball eigenmode directly from
the characteristic polynomial. A stationary deterministic negative control
must show Heavy-Ball acceleration, rejecting “momentum always hurts.”
