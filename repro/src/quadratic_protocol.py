"""Clean-room Appendix-F drifting-quadratic protocol for U1bxeLQLaK.

The implementation follows the source's actual finite experiment: d=100,
delta_rw=.01, 20 independent runs, 5,000 updates, three gammas, four betas,
and three noise variances.  It retains the paper's generalized SGDM equations:
HB has (beta1,beta2)=(0,beta), NAG has (beta,0).
"""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

import numpy as np


@dataclass(frozen=True)
class QuadraticProtocol:
    dimension: int = 100
    seeds: int = 20
    horizon: int = 5000
    drift: float = .01
    mu: float = 1.0
    gammas: tuple[float, ...] = (.01, .05, .10)
    betas: tuple[float, ...] = (.50, .90, .95, .99)
    noise_variances: tuple[float, ...] = (.1, .5, .8)


def target_walk(rng: np.random.Generator, protocol: QuadraticProtocol) -> np.ndarray:
    """Normalized Gaussian random walk, including the t=0 target."""
    delta = rng.normal(size=(protocol.horizon, protocol.dimension))
    delta *= protocol.drift / np.linalg.norm(delta, axis=1, keepdims=True)
    return np.concatenate([np.zeros((1, protocol.dimension)), np.cumsum(delta, axis=0)], axis=0)


def run_method(target: np.ndarray, *, method: str, gamma: float, beta: float, noise_variance: float, seed: int, mu: float = 1.0) -> float:
    """One exact source-protocol run; return final squared tracking error."""
    rng = np.random.default_rng(seed)
    theta = target[0].copy()
    theta_prev = theta.copy()  # zero velocity buffer
    psi_prev = theta.copy()
    std = sqrt(noise_variance)
    for current_target in target[1:]:
        if method == "sgd":
            grad = mu * (theta - current_target) + rng.normal(scale=std, size=theta.shape)
            theta_next = theta - gamma * grad
        elif method == "hb":
            psi = theta
            grad = mu * (psi - current_target) + rng.normal(scale=std, size=theta.shape)
            theta_next = psi - gamma * grad + beta * (psi - psi_prev)
            psi_prev = psi
        elif method == "nag":
            psi = theta + beta * (theta - theta_prev)
            grad = mu * (psi - current_target) + rng.normal(scale=std, size=theta.shape)
            theta_next = psi - gamma * grad
        else:
            raise ValueError(method)
        theta_prev, theta = theta, theta_next
    return float(np.sum((theta - target[-1]) ** 2))


def run_cell(*, gamma: float, beta: float, noise_variance: float, method: str, protocol: QuadraticProtocol) -> list[float]:
    """Run 20 independent full-length trials with source-compatible shared drift."""
    values=[]
    for seed in range(protocol.seeds):
        target = target_walk(np.random.default_rng(260112238 + seed), protocol)
        values.append(run_method(target, method=method, gamma=gamma, beta=beta, noise_variance=noise_variance, seed=260112238 + 100_000*({"sgd":0,"hb":1,"nag":2}[method]) + 1_000*int(gamma*100) + 100*int(beta*100) + int(noise_variance*10) + seed, mu=protocol.mu))
    return values
