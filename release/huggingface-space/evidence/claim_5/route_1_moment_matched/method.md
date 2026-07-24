
# Claim 5 method

Use the source dimensions, seed count, horizon, batch size, normalized
random-walk target, log-spaced covariance spectrum, and fixed method-matched
settings for a streaming Gaussian-design least-squares risk. For efficient CPU
execution, sample a Gaussian gradient oracle whose conditional mean and
covariance exactly equal those of the 256-example least-squares mini-batch:

`E[g|e]=Sigma e` and
`Cov(g|e)=((e' Sigma e + sigma^2)Sigma + (Sigma e)(Sigma e)')/B`.

Run separate kappa, drift, and beta sweeps for SGD, HB, and NAG, retaining every
seed. The checker requires endpoint degradation and SGD to be best at
`kappa=1000`. A stationary deterministic control must favor HB.
