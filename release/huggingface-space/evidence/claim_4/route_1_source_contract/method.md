# Claim 4 method

The generator transcribes both displayed high-probability coefficients,
evaluates their ratio across seven beta values, and separately evaluates:

1. the forgetting horizon implied by Theorem 3.6's displayed exponential after
   substituting its own stability scaling; and
2. the physical Heavy-Ball velocity-memory horizon `beta^t <= 0.05`.

An independent checker reads only the CSV/JSON outputs and rederives every
reported exponent. Negative controls mutate the momentum coefficient and the
vanilla-SGD coupling indicator and must be rejected.
