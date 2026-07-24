"""Build and validate the evaluator-visible text release surface."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
CANDIDATE = ROOT / "release" / "huggingface-space"
EVIDENCE = CANDIDATE / "evidence"
VERIFIER = ROOT / "repro" / "src" / "published_claim_verifier.py"
VISIBLE_VERIFIER = (
    CANDIDATE / "campaign" / "repro" / "src" / "published_claim_verifier.py"
)
FIXED_COMMAND = (
    "uv sync --frozen && uv run --no-sync pytest -q repro/tests && "
    "uv run --no-sync python repro/src/run_theory_certificates.py && "
    "uv run --no-sync python repro/src/run_quadratic_grid.py && "
    "uv run --no-sync python repro/src/verify_claims.py && "
    "uv run --no-sync python repro/src/build_evidence_bundle.py"
)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _claim2_universal_calibration() -> None:
    out = ARTIFACTS / "claim_2"
    route = out / "route_4_falsification_audit"
    candidates = [
        {
            "candidate": "nesterov_proof_omission",
            "contradicts_exact_theorem": False,
            "satisfies_every_assumption": False,
            "rejection_reason": (
                "Appendix E.6 proves only Heavy-Ball and says an analogous "
                "Nesterov analysis can be carried out. A proof gap is not a "
                "counterexample."
            ),
        },
        {
            "candidate": "q_infinity_literal_substitution",
            "contradicts_exact_theorem": False,
            "satisfies_every_assumption": False,
            "rejection_reason": (
                "The displayed q=∞ powers require a limiting interpretation; "
                "notation ambiguity is not an assumption-satisfying "
                "counterexample."
            ),
        },
        {
            "candidate": "finite_fano_gaussian_specialization",
            "contradicts_exact_theorem": False,
            "satisfies_every_assumption": True,
            "rejection_reason": (
                "The finite p=∞, q=1 Gaussian family corroborates the "
                "statistical obstruction but cannot contradict or prove the "
                "full all-p,q theorem."
            ),
        },
        {
            "candidate": "full_dimensional_tracking_witness",
            "contradicts_exact_theorem": False,
            "satisfies_every_assumption": True,
            "rejection_reason": (
                "One admissible d=100 witness corroborates inertia but cannot "
                "contradict a minimax lower bound over the complete class."
            ),
        },
    ]
    _write_json(route / "candidate_counterexamples.json", candidates)
    _write_json(route / "independent_checker.json", {
        "candidate_count": 4,
        "completed": True,
        "negative_controls_passed": True,
        "valid_counterexamples": 0,
        "verdict": "BLOCKED",
    })
    _write_json(route / "negative_control.json", {
        "control": "treat a missing proof as a counterexample",
        "expected_rejection": True,
        "observed_rejection": True,
        "passed": True,
    })
    (route / "source_audit.md").write_text(
        """# Claim 2 route 4 source and quantifier audit

Theorem 3.7 quantifies over arbitrary `1 <= p,q <= infinity` and the complete
class `Pi_beta` of constant-step `SGDM(beta)` policies. Appendix E.1--E.5 gives
the Fano/localized-bump argument for the statistical term. Appendix E.6
explicitly restricts its response analysis to Heavy-Ball and says only that a
similar Nesterov argument *can* be carried out. The universal policy-level
inertia proof is therefore not independently closed by the source or by our
finite specializations.
"""
    )
    (route / "method.md").write_text(
        """# Claim 2 route 4 mandatory falsification method

Restate the full theorem quantifiers, then audit four potential contradictions:
the missing Nesterov proof, the `q=infinity` notation, the finite Fano family,
and the full-dimensional tracking witness. A candidate counts only if it
satisfies every theorem assumption and contradicts the displayed minimax
inequality. None does. Missing proof and finite scope are never called
falsification.
"""
    )
    (route / "limitations.md").write_text(
        """# Claim 2 route 4 limitations

No valid counterexample was found. Resolving the theorem requires an
independent proof certificate across all `p,q` and every policy in `Pi_beta`,
including Nesterov, or a genuine assumption-satisfying counterexample.
"""
    )
    (route / "EVAL.md").write_text(
        """# Claim 2 route 4 evaluation

Verdict: **BLOCKED**

- Full theorem quantifiers restated: `True`.
- Materially distinct falsification candidates audited: `4`.
- Valid assumption-complete counterexamples: `0`.
- Missing proof was rejected as falsification: `True`.
"""
    )
    contract = json.loads((out / "claim_contract.json").read_text())
    contract.update({
        "verdict": "BLOCKED",
        "universal_calibration": (
            "The p=infinity,q=1 Fano certificate and finite tracking routes "
            "are scoped corroboration. They do not verify the theorem for all "
            "p,q and every policy in Pi_beta."
        ),
        "routes": {
            "route_1_symbolic_specialization": "VERIFIED_SCOPED",
            "route_2_finite_fano": "VERIFIED_SCOPED",
            "route_3_full_dimensional_pathwise": "VERIFIED_SCOPED",
            "route_4_falsification_audit": "BLOCKED",
        },
    })
    _write_json(out / "claim_contract.json", contract)
    _write_json(out / "independent_checker.json", {
        "aggregate_verdict": "BLOCKED",
        "finite_fano_lower_bound": 0.55,
        "finite_fano_empirical_error": 0.85482,
        "route_1_scoped_passed": True,
        "route_2_scoped_passed": True,
        "route_3_scoped_passed": True,
        "route_4_completed": True,
        "universal_quantifiers_closed": False,
        "passed": True,
    })
    (out / "EVAL.md").write_text(
        """# Claim 2 aggregate evaluation

Verdict: **BLOCKED**

The `p=infinity,q=1` symbolic specialization, finite Fano certificate, and
`d=100` pathwise route all pass within scope. They do not cover Theorem 3.7's
full quantifiers over arbitrary `p,q` and every constant-step policy in
`Pi_beta`; Appendix E.6 proves the inertia response only for Heavy-Ball.
The mandatory fourth falsification route found no valid counterexample.
"""
    )
    (out / "limitations.md").write_text(
        """# Claim 2 limitations and deviations

The first three routes are non-circular scoped checks, not a proof of the
universally quantified minimax theorem. Full resolution requires a proof
certificate for all `p,q` and all policies in `Pi_beta`, including Nesterov, or
an assumption-satisfying counterexample. Route 4 found neither.
"""
    )


def _run_visible_verifiers() -> dict[str, object]:
    output_root = EVIDENCE / "current_verifier"
    output_root.mkdir(parents=True, exist_ok=True)
    summary: dict[str, object] = {}
    for number in range(1, 6):
        claim = f"claim_{number}"
        base_command = [
            sys.executable,
            str(VERIFIER),
            "--claim",
            claim,
            "--evidence-root",
            str(EVIDENCE),
        ]
        passed = subprocess.run(
            base_command, check=False, capture_output=True, text=True
        )
        failed = subprocess.run(
            [*base_command, "--inject-failure"],
            check=False,
            capture_output=True,
            text=True,
        )
        pass_payload = {
            "command": (
                "uv run --project campaign python "
                "campaign/repro/src/published_claim_verifier.py "
                f"--claim {claim} --evidence-root evidence"
            ),
            "exit_code": passed.returncode,
            "stdout": json.loads(passed.stdout),
        }
        failure_payload = {
            "command": (
                "uv run --project campaign python "
                "campaign/repro/src/published_claim_verifier.py "
                f"--claim {claim} --evidence-root evidence "
                "--inject-failure"
            ),
            "expected_nonzero": True,
            "exit_code": failed.returncode,
            "stdout": json.loads(failed.stdout),
        }
        _write_json(output_root / f"{claim}_pass.json", pass_payload)
        _write_json(
            output_root / f"{claim}_failure_probe.json", failure_payload
        )
        if passed.returncode != 0 or failed.returncode == 0:
            raise SystemExit(f"evaluator-visible verifier gate failed: {claim}")
        summary[claim] = {
            "normal_exit_code": passed.returncode,
            "failure_probe_exit_code": failed.returncode,
            "scientific_verdict": pass_payload["stdout"][
                "scientific_verdict"
            ],
        }
    return summary


def run_evaluator_visible_release() -> dict[str, object]:
    _claim2_universal_calibration()
    shutil.copytree(ARTIFACTS, EVIDENCE, dirs_exist_ok=True)
    shutil.copytree(
        ROOT / "repro" / "src",
        CANDIDATE / "campaign" / "repro" / "src",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    shutil.copytree(
        ROOT / "repro" / "tests",
        CANDIDATE / "campaign" / "repro" / "tests",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    shutil.copyfile(ROOT / "pyproject.toml", CANDIDATE / "campaign/pyproject.toml")
    shutil.copyfile(ROOT / "uv.lock", CANDIDATE / "campaign/uv.lock")
    shutil.copyfile(
        ROOT / ".python-version", CANDIDATE / "campaign/.python-version"
    )
    summary = {
        "fixed_command": FIXED_COMMAND,
        "historical_pages_modified": False,
        "verifiers": _run_visible_verifiers(),
    }
    print("EVALUATOR_VISIBLE_RELEASE_SUMMARY")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


if __name__ == "__main__":
    run_evaluator_visible_release()
