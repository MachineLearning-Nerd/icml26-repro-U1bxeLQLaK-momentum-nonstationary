"""Build reader-facing figures from the frozen text evidence snapshot."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
IMAGES = ROOT / "reports" / "momentum-nonstationary" / "images"

COLORS = {
    "sgd": "#2b6cb0",
    "hb": "#c05621",
    "nag": "#805ad5",
    "statistical": "#2f855a",
    "inertia": "#c53030",
}


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def _style() -> None:
    plt.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 180,
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.22,
        "legend.frameon": False,
    })


def claim3_headline() -> None:
    rows = _csv(ARTIFACTS / "claim_3" / "stability_summary.csv")
    figure, axis = plt.subplots(figsize=(7.2, 4.4))
    for method in ("sgd", "hb", "nag"):
        selected = sorted(
            (row for row in rows if row["method"] == method),
            key=lambda row: float(row["beta"]),
        )
        betas = [float(row["beta"]) for row in selected]
        means = [
            float(row["mean_tail_squared_tracking_error"]) for row in selected
        ]
        sems = [
            float(row["sem_tail_squared_tracking_error"]) for row in selected
        ]
        axis.errorbar(
            betas,
            means,
            yerr=[2.0 * value for value in sems],
            marker="o",
            linewidth=2,
            capsize=3,
            label=method.upper(),
            color=COLORS[method],
        )
    axis.set_yscale("log")
    axis.set_xlabel("Momentum parameter β")
    axis.set_ylabel("Tail squared tracking error (mean ± 2 SE)")
    axis.set_title(
        "Full-dimensional stable tuning: SGD separates from HB and NAG"
    )
    axis.legend(ncols=3)
    axis.text(
        0.02,
        0.12,
        "d=100 · 20 seeds · T=5,000 · normalized random-walk drift",
        transform=axis.transAxes,
        color="#4a5568",
    )
    figure.tight_layout()
    figure.savefig(IMAGES / "headline-claim3-tracking.png", bbox_inches="tight")
    plt.close(figure)


def claim2_regimes() -> None:
    rows = _csv(ARTIFACTS / "claim_2" / "theory_grid.csv")
    figure, axis = plt.subplots(figsize=(7.2, 4.4))
    for beta, linestyle in ((0.5, "-"), (0.9, "--"), (0.98, ":")):
        selected = sorted(
            (
                row for row in rows
                if abs(float(row["beta"]) - beta) < 1e-12
            ),
            key=lambda row: float(row["variation_budget"]),
        )
        variation = [float(row["variation_budget"]) for row in selected]
        statistical = [float(row["statistical_term"]) for row in selected]
        inertia = [float(row["inertia_term"]) for row in selected]
        axis.plot(
            variation,
            statistical,
            linestyle=linestyle,
            marker="o",
            color=COLORS["statistical"],
            label=f"statistical, β={beta:g}",
        )
        axis.plot(
            variation,
            inertia,
            linestyle=linestyle,
            marker="s",
            color=COLORS["inertia"],
            label=f"inertia, β={beta:g}",
        )
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel("Gradient-variation budget")
    axis.set_ylabel("Theorem 3.7 term (hidden constant set to 1)")
    axis.set_title("The minimax decomposition crosses into an inertia regime")
    axis.legend(ncols=2, fontsize=8)
    figure.tight_layout()
    figure.savefig(IMAGES / "claim2-two-regimes.png", bbox_inches="tight")
    plt.close(figure)


def claim4_audit() -> None:
    checks = json.loads(
        (ARTIFACTS / "claim_4" / "generator_checks.json").read_text()
    )
    labels = [
        "Momentum/SGD\ncoupling ratio",
        "Displayed bound\nhorizon",
        "Physical velocity\nmemory",
    ]
    observed = [
        checks["momentum_to_sgd_coupling_ratio_exponent"],
        checks[
            "theorem36_displayed_horizon_exponent_after_stability_substitution"
        ],
        checks["velocity_memory_horizon_exponent"],
    ]
    claimed = [2.0, 1.0, 1.0]
    positions = np.arange(len(labels))
    width = 0.36
    figure, axis = plt.subplots(figsize=(7.2, 4.4))
    axis.bar(
        positions - width / 2,
        claimed,
        width,
        color="#a0aec0",
        label="Imported claim",
    )
    axis.bar(
        positions + width / 2,
        observed,
        width,
        color=["#2f855a", "#c53030", "#2b6cb0"],
        label="Source-derived",
    )
    axis.set_xticks(positions, labels)
    axis.set_ylabel("Exponent versus 1/(1−β)")
    axis.set_title("Claim 4: one coefficient agrees, the literal conjunction does not")
    axis.axhline(1.0, color="#4a5568", linewidth=0.8, alpha=0.5)
    axis.legend()
    for index, value in enumerate(observed):
        axis.text(
            index + width / 2,
            value + 0.04,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    axis.set_ylim(0.0, 2.35)
    figure.tight_layout()
    figure.savefig(IMAGES / "claim4-source-audit.png", bbox_inches="tight")
    plt.close(figure)


def claim5_routes() -> None:
    paths = [
        (
            "Moment-matched",
            ARTIFACTS
            / "claim_5"
            / "route_1_moment_matched"
            / "generator_checks.json",
            "kappa_endpoint_error_ratios",
        ),
        (
            "Raw mini-batch",
            ARTIFACTS
            / "claim_5"
            / "route_2_raw_minibatch"
            / "generator_checks.json",
            "endpoint_kappa_ratios",
        ),
        (
            "Exact spectral",
            ARTIFACTS
            / "claim_5"
            / "route_3_exact_spectral"
            / "generator_checks.json",
            "endpoint_kappa_ratios",
        ),
    ]
    labels: list[str] = []
    ratios: dict[str, list[float]] = {method: [] for method in METHODS}
    for label, path, field in paths:
        value = json.loads(path.read_text())[field]
        labels.append(label)
        for method in METHODS:
            ratios[method].append(float(value[method]))
    positions = np.arange(len(labels))
    width = 0.24
    figure, axis = plt.subplots(figsize=(7.2, 4.4))
    for offset, method in enumerate(METHODS):
        axis.bar(
            positions + (offset - 1) * width,
            ratios[method],
            width,
            label=method.upper(),
            color=COLORS[method],
        )
    axis.axhline(
        1.0,
        color="#1a202c",
        linestyle="--",
        linewidth=1.2,
        label="No κ effect",
    )
    axis.set_yscale("log")
    axis.set_xticks(positions, labels)
    axis.set_ylabel("Error ratio: κ=1000 / κ=10")
    axis.set_title("Claim 5: three routes disagree with the reported κ direction")
    axis.legend(ncols=4, fontsize=8)
    figure.tight_layout()
    figure.savefig(IMAGES / "claim5-kappa-routes.png", bbox_inches="tight")
    plt.close(figure)


METHODS = ("sgd", "hb", "nag")


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    _style()
    claim3_headline()
    claim2_regimes()
    claim4_audit()
    claim5_routes()
    for path in sorted(IMAGES.glob("*.png")):
        print(f"{path.relative_to(ROOT)} {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
