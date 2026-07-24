import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # When momentum becomes inertia

    **Evidence first.** This notebook embeds the completed reproduction's
    central `d=100`, 20-seed, 5,000-step result. It does not rerun the
    expensive campaign to display the answer.
    """)
    return


@app.cell
def _():
    tracking = {
        "beta": [0.50, 0.90, 0.95, 0.98],
        "SGD": [0.00245659, 0.00240787, 0.00244902, 0.00241738],
        "HB": [0.02073346, 0.08778866, 0.15085792, 0.23648238],
        "NAG": [0.01932324, 0.09761358, 0.14277205, 0.23187712],
    }
    tracking_sem = {
        "SGD": [0.00001995, 0.00001719, 0.00001948, 0.00001608],
        "HB": [0.00039205, 0.00197578, 0.00543075, 0.00733156],
        "NAG": [0.00033568, 0.00342932, 0.00244883, 0.00603664],
    }
    return tracking, tracking_sem


@app.cell
def _(tracking, tracking_sem):
    import matplotlib.pyplot as plt

    colors = {"SGD": "#2b6cb0", "HB": "#c05621", "NAG": "#805ad5"}
    figure, axis = plt.subplots(figsize=(8, 4.5))
    for method in ("SGD", "HB", "NAG"):
        axis.errorbar(
            tracking["beta"],
            tracking[method],
            yerr=[2 * value for value in tracking_sem[method]],
            marker="o",
            linewidth=2,
            capsize=3,
            label=method,
            color=colors[method],
        )
    axis.set_yscale("log")
    axis.set_xlabel("Momentum parameter β")
    axis.set_ylabel("Tail squared tracking error (mean ± 2 SE)")
    axis.set_title("Stable tuning under normalized random-walk drift")
    axis.legend(ncols=3)
    axis.grid(alpha=0.2)
    figure.tight_layout()
    figure
    return


@app.cell
def _(mo):
    mo.md(r"""
    The blue curve is essentially flat near `0.0024`. HB and NAG are
    already about eight times worse at `β=0.5` and roughly 96–98 times
    worse at `β=0.98`. Every optimizer uses a step size inside its declared
    theorem stability cap.

    ## The central mechanism

    Momentum carries a velocity state. In a stationary problem that state
    can point consistently downhill and accelerate convergence. When the
    optimum drifts, old gradients can instead point toward where the
    optimum *used to be*. The paper predicts that this inertia becomes
    increasingly expensive as `β → 1`.

    This distinction is why the reproduction includes a stationary negative
    control: HB must accelerate there. Without that control, “momentum is
    always bad” could masquerade as evidence for the drift-specific claim.
    """)
    return


@app.cell
def _(mo):
    beta = mo.ui.slider(
        start=0.50,
        stop=0.98,
        step=0.01,
        value=0.90,
        label="Explore β",
    )
    beta
    return (beta,)


@app.cell
def _(beta, mo):
    one_minus = 1.0 - beta.value
    mo.md(
        f"""
        At **β = {beta.value:.2f}**:

        - physical momentum-memory scale: `1/(1−β) = {1 / one_minus:.2f}`
        - squared drift-noise amplification: `1/(1−β)² = {1 / one_minus**2:.2f}`

        These are mechanisms and bound coefficients, not a prediction that
        every empirical error must equal either number.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Claim-by-claim outcome

    | Claim | Verdict | Key evidence |
    |---|---:|---|
    | 1: Theorem 3.3 beta exponents | **VERIFIED** | preserved transient slope `2.115`; noise slope `0.987` |
    | 2: minimax statistical + inertia terms | **BLOCKED** | scoped exponents/Fano pass; universal policy quantifier remains open |
    | 3: stable SGD wins in a drift-heavy regime | **VERIFIED** | full-dimensional experiment shown above |
    | 4: imported high-probability conjunction | **FALSIFIED** | SGD coupling is present; displayed horizon exponent is `2`, not `1` |
    | 5: broad empirical condition-number claim | **BLOCKED** | three routes disagree, fourth route finds no assumption-complete counterexample |

    “BLOCKED” is deliberate. The paper does not provide executable code for
    its finite empirical pipeline, and its condition-number statement is
    descriptive rather than universally quantified. A numerical
    disagreement is therefore not automatically a falsification.
    """)
    return


@app.cell
def _():
    condition_number_routes = {
        "Moment-matched": {"SGD": 1.15849, "HB": 0.01789, "NAG": 0.06931},
        "Raw mini-batch": {"SGD": 1.08564, "HB": 0.01831, "NAG": 0.07073},
        "Exact spectral": {"SGD": 1.18482, "HB": 0.03019, "NAG": 0.08750},
    }
    return (condition_number_routes,)


@app.cell
def _(condition_number_routes, mo):
    rows = []
    for route, values in condition_number_routes.items():
        rows.append(
            {
                "Route": route,
                "SGD κ ratio": values["SGD"],
                "HB κ ratio": values["HB"],
                "NAG κ ratio": values["NAG"],
            }
        )
    mo.ui.table(rows, selection=None)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Each ratio is tracking error at `κ=1000` divided by error at `κ=10`.
    All three HB/NAG routes are below one—the opposite of the reported
    direction. They remain a documented divergence rather than a claimed
    contradiction because the missing author implementation prevents an
    assumption-complete match.

    ## Reproducing the formal evidence

    The repository pins one Python environment with `uv.lock`. The formal
    command is:

    ```bash
    uv sync --frozen && uv run --no-sync pytest -q repro/tests && uv run --no-sync python repro/src/run_theory_certificates.py && uv run --no-sync python repro/src/run_quadratic_grid.py && uv run --no-sync python repro/src/verify_claims.py && uv run --no-sync python repro/src/build_evidence_bundle.py
    ```

    That command regenerates the raw machine-readable evidence. This
    notebook is the bounded tutorial surface; it is not itself a claim
    verifier.
    """)
    return


if __name__ == "__main__":
    app.run()
