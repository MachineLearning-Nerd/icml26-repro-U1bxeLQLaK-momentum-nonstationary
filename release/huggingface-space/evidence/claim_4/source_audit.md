
# Claim 4 aggregate source audit

The exact imported claim is a conjunction. Theorem 3.5 contains the
vanilla-SGD term `gamma^2 sigma^2 D_t^(2) log(2T/delta)`, so drift--noise
coupling is not literally absent there. Theorem 3.6 contains the matched
momentum coefficient `gamma^2 sigma^2 D_lag^(2)/(1-beta)^2`; that narrower
relative amplification is present. But substituting the theorem's own
stability scaling into its displayed exponential gives a forgetting horizon
of order `(1-beta)^-2`, rather than `(1-beta)^-1`.

The source-contract and pathwise interpretations are retained separately under
`route_1_source_contract/` and `route_2_pathwise_coefficient/`.
