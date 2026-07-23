import numpy as np

from remaining_contracts import (
    _solve_discrete_covariance,
    _stationary_acceleration_control,
)


def test_least_squares_minibatch_covariance_factorization():
    rng = np.random.default_rng(9)
    dimension = 4
    batch = 16
    sigma2 = 0.5
    diagonal = np.geomspace(1.0, 10.0, dimension)
    error = rng.normal(size=dimension)
    mean_gradient = diagonal * error
    target = (
        (error @ mean_gradient + sigma2) * np.diag(diagonal)
        + np.outer(mean_gradient, mean_gradient)
    ) / batch
    draws = 250_000
    z_vector = rng.normal(size=(draws, dimension))
    z_scalar = rng.normal(size=draws)
    noise = (
        np.sqrt((error @ mean_gradient + sigma2) / batch)
        * np.sqrt(diagonal)
        * z_vector
        + mean_gradient * z_scalar[:, None] / np.sqrt(batch)
    )
    observed = np.cov(noise, rowvar=False)
    assert np.allclose(observed, target, rtol=0.025, atol=0.01)


def test_stationary_control_rejects_momentum_always_hurts():
    result = _stationary_acceleration_control()
    assert result["gamma_within_claimed_cap"]
    assert result["hb_accelerates"]


def test_discrete_covariance_solver_has_small_residual():
    transition = np.array([[0.8, 0.1], [-0.2, 0.5]])
    innovation = np.diag([0.03, 0.01])
    covariance, residual = _solve_discrete_covariance(
        transition, innovation
    )
    assert residual < 1e-12
    assert np.linalg.eigvalsh(covariance).min() >= 0.0
