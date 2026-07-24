import math

from exact_contracts import minimax_terms


def test_minimax_terms_match_closed_form_specialization():
    statistical, inertia = minimax_terms(
        beta=0.9,
        sigma=1.0,
        mu=1.0,
        smoothness=10.0,
        variation=100.0,
        horizon=10_000,
        p=math.inf,
        q=1.0,
        dimension=100,
    )
    expected_statistical = (
        (1.0 - 0.9) ** (-2.0 / 3.0)
        * 100.0 ** (2.0 / 3.0)
        * 10_000.0 ** (1.0 / 3.0)
    )
    expected_inertia = (
        (1.0 - 0.9) ** -2.0
        * 10.0**2.0
        * 100.0**2.0
        * 10_000.0**-1.0
    )
    assert abs(statistical - expected_statistical) / expected_statistical < 1e-12
    assert abs(inertia - expected_inertia) / expected_inertia < 1e-12


def test_inertia_term_has_stronger_beta_exponent():
    low = minimax_terms(
        beta=0.5, sigma=1.0, mu=1.0, smoothness=10.0,
        variation=100.0, horizon=10_000, p=math.inf, q=1.0, dimension=100,
    )
    high = minimax_terms(
        beta=0.9, sigma=1.0, mu=1.0, smoothness=10.0,
        variation=100.0, horizon=10_000, p=math.inf, q=1.0, dimension=100,
    )
    assert high[1] / low[1] > high[0] / low[0]
