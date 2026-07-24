"""Independent, evaluator-facing verifier for the published text evidence.

This program reads only files shipped in the Hugging Face Space candidate.  It
does not import the experiment generators.  A deliberate ``--inject-failure``
mode mutates one decisive observable per claim and must exit nonzero.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


def _json(path: Path) -> Any:
    return json.loads(path.read_text())


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def _slope(xs: list[float], ys: list[float]) -> float:
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    numerator = sum(
        (x - x_mean) * (y - y_mean) for x, y in zip(xs, ys, strict=True)
    )
    denominator = sum((x - x_mean) ** 2 for x in xs)
    return numerator / denominator


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _claim_1(root: Path, inject: bool) -> tuple[str, dict[str, Any]]:
    transient_path = root / "claim_1" / "transient_results.json"
    noise_path = root / "claim_1" / "noise_floor_results.json"
    transient = _json(transient_path)
    noise = _json(noise_path)
    x_transient = [
        math.log(1.0 / (1.0 - float(row["beta"])))
        for row in transient["lifted_operator"]
    ]
    if inject:
        y_transient = x_transient.copy()
    else:
        y_transient = [
            math.log(float(row["G^2"])) for row in transient["lifted_operator"]
        ]
    transient_slope = _slope(x_transient, y_transient)
    noise_rows = [
        row for row in noise["noise_floor"] if float(row["beta"]) > 0.0
    ]
    noise_slope = _slope(
        [
            math.log(float(row["1/(1-beta)"]))
            for row in noise_rows
        ],
        [math.log(float(row["floor/SGD"])) for row in noise_rows],
    )
    checks = {
        "all_lifted_operators_stable": all(
            float(row["rho(M)"]) < 1.0
            for row in transient["lifted_operator"]
        ),
        "noise_floor_slope": noise_slope,
        "noise_slope_in_interval_0.9_1.1": 0.9 <= noise_slope <= 1.1,
        "plain_sgd_transient_growth_is_one": math.isclose(
            float(transient["sgd_transient_growth_G"]), 1.0, abs_tol=1e-12
        ),
        "transient_slope": transient_slope,
        "transient_slope_in_interval_1.9_2.3": (
            1.9 <= transient_slope <= 2.3
        ),
    }
    checks["passed"] = all(
        value for key, value in checks.items()
        if isinstance(value, bool) and key != "passed"
    )
    checks["input_sha256"] = {
        "noise_floor_results.json": _digest(noise_path),
        "transient_results.json": _digest(transient_path),
    }
    return "VERIFIED", checks


def _claim_2(root: Path, inject: bool) -> tuple[str, dict[str, Any]]:
    fano_path = root / "claim_2" / "fano_certificate.json"
    monte_path = root / "claim_2" / "fano_monte_carlo.json"
    route_path = (
        root
        / "claim_2"
        / "route_4_falsification_audit"
        / "candidate_counterexamples.json"
    )
    contract_path = root / "claim_2" / "claim_contract.json"
    fano = _json(fano_path)
    monte = _json(monte_path)
    candidates = _json(route_path)
    contract = _json(contract_path)
    fano_bound = float(fano["fano_misclassification_lower_bound"])
    empirical_error = float(monte["empirical_ml_error"])
    if inject:
        fano_bound = 0.99
    checks = {
        "aggregate_contract_is_blocked": contract["verdict"] == "BLOCKED",
        "finite_fano_assumptions_satisfied": bool(
            fano["assumptions_satisfied"]
        ),
        "finite_fano_bound_below_empirical_error": (
            fano_bound <= empirical_error
        ),
        "optimizer_independent_transcript": bool(
            fano["optimizer_independent_transcript"]
        ),
        "route_4_candidate_count": len(candidates),
        "route_4_has_no_valid_exact_counterexample": not any(
            bool(row["contradicts_exact_theorem"]) for row in candidates
        ),
    }
    checks["passed"] = all(
        value for key, value in checks.items()
        if isinstance(value, bool) and key != "passed"
    ) and checks["route_4_candidate_count"] == 4
    checks["input_sha256"] = {
        "claim_contract.json": _digest(contract_path),
        "fano_certificate.json": _digest(fano_path),
        "fano_monte_carlo.json": _digest(monte_path),
        "route_4/candidate_counterexamples.json": _digest(route_path),
    }
    return "BLOCKED", checks


def _claim_3(root: Path, inject: bool) -> tuple[str, dict[str, Any]]:
    summary_path = root / "claim_3" / "stability_summary.csv"
    trials_path = root / "claim_3" / "stability_trials.csv"
    summary = _csv(summary_path)
    trials = _csv(trials_path)
    if inject:
        trials[0]["gamma_within_cap"] = "False"
    by_beta: dict[float, dict[str, tuple[float, float]]] = {}
    for row in summary:
        beta = float(row["beta"])
        by_beta.setdefault(beta, {})[row["method"]] = (
            float(row["mean_tail_squared_tracking_error"]),
            float(row["sem_tail_squared_tracking_error"]),
        )
    separated = []
    for methods in by_beta.values():
        sgd_mean, sgd_sem = methods["sgd"]
        hb_mean, hb_sem = methods["hb"]
        nag_mean, nag_sem = methods["nag"]
        separated.append(
            sgd_mean + 2.0 * sgd_sem
            < min(hb_mean - 2.0 * hb_sem, nag_mean - 2.0 * nag_sem)
        )
    checks = {
        "all_steps_within_declared_caps": all(
            row["gamma_within_cap"] == "True" for row in trials
        ),
        "dimensions_are_100": {int(row["dimension"]) for row in trials}
        == {100},
        "horizons_are_5000": {int(row["horizon"]) for row in trials}
        == {5000},
        "raw_trial_rows": len(trials),
        "seed_indices_are_0_through_19": {
            int(row["seed"]) for row in trials
        } == set(range(20)),
        "two_sem_separation_at_every_beta": all(separated),
    }
    checks["passed"] = all(
        value for key, value in checks.items()
        if isinstance(value, bool) and key != "passed"
    ) and checks["raw_trial_rows"] == 240
    checks["input_sha256"] = {
        "stability_summary.csv": _digest(summary_path),
        "stability_trials.csv": _digest(trials_path),
    }
    return "VERIFIED", checks


def _claim_4(root: Path, inject: bool) -> tuple[str, dict[str, Any]]:
    coefficient_path = root / "claim_4" / "coefficient_audit.csv"
    horizon_path = root / "claim_4" / "horizon_audit.csv"
    contract_path = root / "claim_4" / "claim_contract.json"
    coefficients = _csv(coefficient_path)
    horizons = _csv(horizon_path)
    contract = _json(contract_path)
    x_values = [
        math.log(1.0 / float(row["one_minus_beta"]))
        for row in coefficients
    ]
    if inject:
        ratio_values = [1.0 for _ in coefficients]
    else:
        ratio_values = [
            float(row["momentum_to_sgd_ratio"]) for row in coefficients
        ]
    coefficient_slope = _slope(
        x_values, [math.log(value) for value in ratio_values]
    )
    horizon_slope = _slope(
        x_values,
        [
            math.log(float(row["theorem36_displayed_forgetting_horizon"]))
            for row in horizons
        ],
    )
    checks = {
        "coefficient_ratio_slope": coefficient_slope,
        "coefficient_ratio_slope_is_two": math.isclose(
            coefficient_slope, 2.0, abs_tol=1e-6
        ),
        "displayed_horizon_slope": horizon_slope,
        "displayed_horizon_slope_is_two_not_one": math.isclose(
            horizon_slope, 2.0, abs_tol=1e-6
        ),
        "exact_contract_is_falsified": contract["verdict"] == "FALSIFIED",
        "sgd_reference_coefficient_is_beta_neutral": len({
            round(float(row["sgd_drift_noise_coefficient_without_sigma2"]), 18)
            for row in coefficients
        }) == 1,
    }
    checks["passed"] = all(
        value for key, value in checks.items()
        if isinstance(value, bool) and key != "passed"
    )
    checks["input_sha256"] = {
        "claim_contract.json": _digest(contract_path),
        "coefficient_audit.csv": _digest(coefficient_path),
        "horizon_audit.csv": _digest(horizon_path),
    }
    return "FALSIFIED", checks


def _claim_5(root: Path, inject: bool) -> tuple[str, dict[str, Any]]:
    contract_path = root / "claim_5" / "claim_contract.json"
    checker_path = root / "claim_5" / "independent_checker.json"
    candidates_path = (
        root
        / "claim_5"
        / "route_4_falsification_audit"
        / "candidate_counterexamples.json"
    )
    contract = _json(contract_path)
    checker = _json(checker_path)
    candidates = _json(candidates_path)
    if inject:
        candidates[0]["contradicts_exact_descriptive_claim"] = True
    checks = {
        "aggregate_contract_rule_requires_blocked": (
            "otherwise BLOCKED" in contract["verdict_rule"]
        ),
        "aggregate_verdict_is_blocked": (
            checker["aggregate_verdict"] == "BLOCKED"
        ),
        "four_falsification_candidates_audited": len(candidates) == 4,
        "no_valid_exact_counterexample": not any(
            bool(row["contradicts_exact_descriptive_claim"])
            for row in candidates
        ),
    }
    checks["passed"] = all(
        value for key, value in checks.items()
        if isinstance(value, bool) and key != "passed"
    )
    checks["input_sha256"] = {
        "claim_contract.json": _digest(contract_path),
        "independent_checker.json": _digest(checker_path),
        "route_4/candidate_counterexamples.json": _digest(candidates_path),
    }
    return "BLOCKED", checks


VERIFIERS = {
    "claim_1": _claim_1,
    "claim_2": _claim_2,
    "claim_3": _claim_3,
    "claim_4": _claim_4,
    "claim_5": _claim_5,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim", choices=sorted(VERIFIERS), required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--inject-failure", action="store_true")
    args = parser.parse_args()
    verdict, checks = VERIFIERS[args.claim](
        args.evidence_root, args.inject_failure
    )
    payload = {
        "claim": args.claim,
        "failure_injected": args.inject_failure,
        "passed": bool(checks["passed"]),
        "scientific_verdict": verdict,
        "checks": checks,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if not payload["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
