import numpy as np


def test_policy_query_cancels_from_quadratic_gradient_transcript():
    rng = np.random.default_rng(7)
    mu = 1.5
    environment = rng.normal(size=5)
    noise = rng.normal(size=(4, 5))
    residuals = []
    for scale in (0.0, 1.0, 10.0):
        query = rng.normal(scale=scale, size=(4, 5))
        gradient = mu * (query - environment) + noise
        residuals.append(gradient - mu * query)
    assert np.allclose(residuals[0], residuals[1])
    assert np.allclose(residuals[0], residuals[2])


def test_momentum_coupling_coefficient_ratio_is_inverse_gap_squared():
    gamma = 1e-5
    for beta in (0.5, 0.9, 0.98):
        sgd = gamma**2
        momentum = gamma**2 / (1.0 - beta) ** 2
        assert momentum / sgd == 1.0 / (1.0 - beta) ** 2
