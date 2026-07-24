import numpy as np

from claim1_regression import _slope
from verify_c0_transient import companion, spectral_radius


def test_judged_transient_operators_stay_stable():
    for beta in (0.5, 0.9, 0.98):
        gamma = 0.2 * (1.0 - beta) ** 2
        assert spectral_radius(companion(beta, gamma, 1.0)) < 1.0


def test_independent_slope_rejects_wrong_exponent():
    inverse_gap = [2.0, 5.0, 10.0, 20.0]
    squared_growth = [value**2 for value in inverse_gap]
    assert np.isclose(_slope(inverse_gap, squared_growth), 2.0)
    assert not 0.7 < _slope(inverse_gap, squared_growth) < 1.4
