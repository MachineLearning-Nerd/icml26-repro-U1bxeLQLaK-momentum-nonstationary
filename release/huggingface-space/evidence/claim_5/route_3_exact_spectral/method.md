
# Claim 5 route 3 method

For each of 50 eigenmodes and each optimizer, construct the exact tracking
state matrix driven by target increments and label-gradient noise. Solve the
discrete Lyapunov equation with a direct Kronecker linear solve, sum the error
variance across modes, and independently check every Lyapunov residual.
