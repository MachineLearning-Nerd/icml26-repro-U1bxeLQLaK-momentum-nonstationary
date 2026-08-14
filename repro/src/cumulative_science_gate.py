"""Validate the current five-claim evidence and source pins."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = ROOT / "outputs"
EVIDENCE = ROOT / "release" / "huggingface-space" / "evidence"
VERIFIER = ROOT / "repro" / "src" / "published_claim_verifier.py"

EXPECTED = {
    "claim_1": "VERIFIED",
    "claim_2": "BLOCKED",
    "claim_3": "VERIFIED",
    "claim_4": "FALSIFIED",
    "claim_5": "BLOCKED",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def run_verifier(claim: str, inject_failure: bool) -> tuple[int, dict[str, Any]]:
    command = [
        sys.executable,
        str(VERIFIER),
        "--claim",
        claim,
        "--evidence-root",
        str(EVIDENCE),
    ]
    if inject_failure:
        command.append("--inject-failure")
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"{claim} verifier did not emit JSON: {completed.stderr}"
        ) from error
    return completed.returncode, payload


def current_claim_report(verifiers: dict[str, dict[str, Any]]) -> dict[str, Any]:
    statuses = {
        "C1": "VERIFIED_SCOPED",
        "C2": "BLOCKED_UNIVERSAL_QUANTIFIERS",
        "C3": "VERIFIED_SCOPED",
        "C4": "FALSIFIED_AS_WRITTEN_WITH_NARROWER_COMPONENT_VERIFIED",
        "C5": "BLOCKED_PROTOCOL_UNDERSPECIFIED",
    }
    evidence = {
        "C1": "release/huggingface-space/evidence/claim_1",
        "C2": "release/huggingface-space/evidence/claim_2",
        "C3": "release/huggingface-space/evidence/claim_3",
        "C4": "release/huggingface-space/evidence/claim_4",
        "C5": "release/huggingface-space/evidence/claim_5",
    }
    claim_rows = {}
    for number in range(1, 6):
        claim = f"claim_{number}"
        claim_rows[f"C{number}"] = {
            "status": statuses[f"C{number}"],
            "scientific_verdict": verifiers[claim]["scientific_verdict"],
            "evidence_root": evidence[f"C{number}"],
            "verifier_passed": verifiers[claim]["passed"],
        }
    return {
        "paper": "U1bxeLQLaK",
        "claim_count": 5,
        "claims": claim_rows,
        "verified_claims": 2,
        "earned_points": None,
        "possible_points": None,
        "all_claims_complete": False,
        "overall_status": "VERIFIED_SCOPED_WITH_FALSIFIED_AND_BLOCKED_CLAIMS",
        "strict_status": "NOT_READY",
        "score_forecast": None,
    }


def main() -> None:
    sources = json.loads((ROOT / "sources.json").read_text())
    paper = sources["paper"]
    source = sources["paper_source"]
    require(paper["openreview_id"] == "U1bxeLQLaK", "paper identity mismatch")
    require(paper["arxiv_id"] == "2601.12238", "arXiv identity mismatch")
    require(
        sha256(ROOT / source["pdf_path"]) == source["pdf_sha256"],
        "paper PDF hash changed",
    )
    require(
        sha256(ROOT / source["source_archive_path"])
        == source["source_archive_sha256"],
        "source archive hash changed",
    )
    require(EVIDENCE.is_dir(), "evaluator-visible evidence root is missing")
    require(VERIFIER.is_file(), "independent verifier is missing")

    normal: dict[str, dict[str, Any]] = {}
    probes: dict[str, dict[str, Any]] = {}
    for claim, expected in EXPECTED.items():
        normal_exit, normal_payload = run_verifier(claim, False)
        probe_exit, probe_payload = run_verifier(claim, True)
        require(normal_exit == 0, f"{claim} normal verifier failed")
        require(probe_exit != 0, f"{claim} failure probe was accepted")
        require(normal_payload["passed"], f"{claim} normal payload failed")
        require(not probe_payload["passed"], f"{claim} probe payload passed")
        require(
            normal_payload["scientific_verdict"] == expected,
            f"{claim} verdict changed: {normal_payload['scientific_verdict']}",
        )
        normal[claim] = normal_payload
        probes[claim] = probe_payload

    report = current_claim_report(normal)
    report["source"] = {
        "pdf_sha256": source["pdf_sha256"],
        "source_archive_sha256": source["source_archive_sha256"],
        "evidence_arxiv_version": paper["evidence_arxiv_version"],
    }
    report["verifiers"] = {
        claim: {
            "normal_exit_code": 0,
            "failure_probe_exit_code": 1,
            "normal": normal[claim],
            "failure_probe": probes[claim],
        }
        for claim in EXPECTED
    }
    report["limitations"] = [
        "Theorem 3.7 universal p,q and all-policy quantifiers are not independently closed.",
        "The source archive has no executable author experiment repository.",
        "Section 4 source-scale logistic/MLP results and raw per-seed metrics are unavailable.",
        "No external evaluator score or score forecast is claimed.",
    ]
    (OUTPUTS / "claim_verification.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    (OUTPUTS / "CUMULATIVE_SCIENCE_GATE.json").write_text(
        json.dumps({
            "paper": report["paper"],
            "gate_version": "scoped-v1",
            "status": "SCOPED_PASS",
            "strict_status": report["strict_status"],
            "overall_status": report["overall_status"],
            "claims": report["claims"],
            "claim_count": report["claim_count"],
            "verified_claims": report["verified_claims"],
            "earned_points": report["earned_points"],
            "possible_points": report["possible_points"],
            "source": report["source"],
            "verifier_exit_codes": {
                claim: {
                    "normal": 0,
                    "failure_probe": 1,
                }
                for claim in EXPECTED
            },
            "score_forecast": None,
            "limitations": report["limitations"],
        }, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        "status": "SCOPED_PASS",
        "overall_status": report["overall_status"],
        "claims": report["claims"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
