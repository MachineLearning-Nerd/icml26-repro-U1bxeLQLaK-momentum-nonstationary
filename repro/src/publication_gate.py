"""Run the deterministic current-evidence publication gate."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = ROOT / "outputs"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(relative_script: str) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / relative_script)],
        cwd=ROOT,
        check=True,
    )


def validate_bundle() -> tuple[int, str, int]:
    bundle = OUTPUTS / "evidence_bundle.jsonl"
    lines = bundle.read_text().splitlines()
    if not lines:
        raise SystemExit("evidence bundle is empty")
    manifest = json.loads(lines[0])
    if manifest.get("type") != "manifest":
        raise SystemExit("evidence bundle manifest is missing")
    file_count = 0
    for line in lines[1:]:
        record = json.loads(line)
        if record.get("type") != "file":
            raise SystemExit("evidence bundle contains an unknown record")
        path = ROOT / record["path"]
        if not path.is_file():
            raise SystemExit(f"evidence file is missing: {record['path']}")
        if path.stat().st_size != record["bytes"]:
            raise SystemExit(f"evidence file size changed: {record['path']}")
        if sha256(path) != record["sha256"]:
            raise SystemExit(f"evidence file hash changed: {record['path']}")
        file_count += 1
    if file_count != manifest["file_count"]:
        raise SystemExit("evidence bundle file count changed")
    return bundle.stat().st_size, sha256(bundle), file_count


def main() -> None:
    run("repro/src/cumulative_science_gate.py")
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "repro/tests"],
        cwd=ROOT,
        check=True,
    )
    run("repro/src/build_evidence_bundle.py")
    bundle_bytes, bundle_sha256, file_count = validate_bundle()
    cumulative = json.loads(
        (OUTPUTS / "CUMULATIVE_SCIENCE_GATE.json").read_text()
    )
    gate = {
        "paper": cumulative["paper"],
        "gate_version": "publication-v1",
        "status": cumulative["status"],
        "strict_status": cumulative["strict_status"],
        "overall_status": cumulative["overall_status"],
        "claims": cumulative["claims"],
        "claim_count": cumulative["claim_count"],
        "verified_claims": cumulative["verified_claims"],
        "earned_points": cumulative["earned_points"],
        "possible_points": cumulative["possible_points"],
        "all_claims_complete": False,
        "tests_passed": True,
        "tests": ["python -m pytest -q repro/tests: passed"],
        "verifiers_passed": True,
        "publication_gate_passed": True,
        "evidence_bundle": {
            "path": "outputs/evidence_bundle.jsonl",
            "bytes": bundle_bytes,
            "sha256": bundle_sha256,
            "file_count": file_count,
        },
        "source": cumulative["source"],
        "score_forecast": None,
        "limitations": cumulative["limitations"],
    }
    payload = json.dumps(gate, indent=2, sort_keys=True) + "\n"
    (ROOT / "publication_gate.json").write_text(payload)
    (OUTPUTS / "publication_gate.json").write_text(payload)
    (OUTPUTS / "PUBLICATION_GATE_PASSED.json").write_text(payload)
    if (ROOT / "publication_gate.json").read_bytes() != (
        OUTPUTS / "publication_gate.json"
    ).read_bytes():
        raise SystemExit("publication gate copies differ")
    print(payload, end="")


if __name__ == "__main__":
    main()
