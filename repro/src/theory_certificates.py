"""Independent recurrence certificates for the two theorem-level claims."""
from __future__ import annotations

import numpy as np


def theorem33_stability_cap(mu: float, L: float, beta: float) -> float:
    return mu * (1-beta)**2 / (4*L**2)


def theorem33_drift_term(mu: float, gamma: float, beta: float, delta: float) -> float:
    """The explicit drift floor in source Eq. (3.5), omitting the universal <= constant."""
    return ((2+beta)**2 * delta**2) / (gamma**2 * mu**2)


def hb_transition(mu: float, gamma: float, beta: float) -> np.ndarray:
    return np.array([[1+beta-gamma*mu, -beta], [1., 0.]])


def stationary_hb_variance(mu: float, gamma: float, beta: float, noise_variance: float) -> float:
    """Solve the independent 2x2 discrete Lyapunov equation exactly."""
    A = hb_transition(mu, gamma, beta)
    Q = np.array([[gamma**2 * noise_variance, 0.], [0., 0.]])
    vec = np.linalg.solve(np.eye(4) - np.kron(A, A), Q.reshape(4))
    return float(vec.reshape(2,2)[0,0])


def jump_response_time(mu: float, gamma: float, beta: float, threshold_fraction: float = .5, max_steps: int = 5_000_000) -> int:
    """Deterministic HB response after a target jump 0 -> 1.

    Returns the first time |x_t-1| <= threshold_fraction, a direct finite
    certificate for the inertia-window mechanism used in the lower bound.
    """
    x = previous = 0.0
    for step in range(1, max_steps + 1):
        x_next = x - gamma * mu * (x - 1.0) + beta * (x - previous)
        previous, x = x, x_next
        if abs(x - 1.0) <= threshold_fraction:
            return step
    raise RuntimeError("response did not reach threshold")


def block_switch_regret(mu: float, gamma: float, beta: float, block_length: int, blocks: int, amplitude: float = 1.0) -> float:
    """Exact deterministic 1D block-switching quadratic regret."""
    x = previous = 0.0
    regret = 0.0
    for block in range(blocks):
        target = amplitude if block % 2 == 0 else -amplitude
        for _ in range(block_length):
            regret += .5 * mu * (x-target)**2
            x_next = x - gamma * mu * (x-target) + beta * (x-previous)
            previous, x = x, x_next
    return regret
