"""Build the deterministic hash-bound evidence manifest."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = ROOT / "outputs"

TEXT_SUFFIXES = {".csv", ".json", ".jsonl", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}
EXCLUDED_OUTPUTS = {
    "artifact_manifest.json",
    "evidence_bundle.jsonl",
    "PUBLICATION_GATE_PASSED.json",
    "CUMULATIVE_SCIENCE_GATE.json",
    "publication_gate.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _add_if_file(paths: set[Path], relative: str) -> None:
    candidate = ROOT / relative
    if candidate.is_file():
        paths.add(candidate)


def bundle_paths() -> list[Path]:
    paths: set[Path] = set()
    for relative in (
        "README.md",
        "STATUS.md",
        "sources.json",
        "pyproject.toml",
        "uv.lock",
        ".python-version",
        "docs/primary.pdf",
        "docs/arxiv_source.tar",
    ):
        _add_if_file(paths, relative)

    for directory in (
        ROOT / "docs",
        ROOT / "repro" / "src",
        ROOT / "repro" / "tests",
        ROOT / ".openresearch" / "artifacts",
        ROOT / "release" / "huggingface-space" / "evidence",
        ROOT / "release" / "huggingface-space" / "pages",
    ):
        if not directory.exists():
            continue
        for candidate in directory.rglob("*"):
            if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES:
                paths.add(candidate)

    for candidate in OUTPUTS.iterdir():
        if candidate.is_file() and candidate.name not in EXCLUDED_OUTPUTS:
            if candidate.suffix.lower() in TEXT_SUFFIXES:
                paths.add(candidate)

    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def main() -> None:
    report = json.loads((OUTPUTS / "claim_verification.json").read_text())
    files = []
    for path in bundle_paths():
        files.append({
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })

    manifest = {
        "type": "manifest",
        "paper": "U1bxeLQLaK",
        "arxiv": "2601.12238",
        "source_pdf_sha256": "415533d734236070ec5180fdcf6fcc9454dc55a20913f219b5d7f1be19776032",
        "source_archive_sha256": "89ad9ad897d3f9a0210ceab3e61adb356bf32edaa49621c0234a426aef3b3fa9",
        "claim_count": report["claim_count"],
        "claims": report["claims"],
        "file_count": len(files),
    }
    bundle = OUTPUTS / "evidence_bundle.jsonl"
    lines = [json.dumps(manifest, sort_keys=True)]
    lines.extend(json.dumps({"type": "file", **entry}, sort_keys=True) for entry in files)
    bundle.write_text("\n".join(lines) + "\n")

    artifact_files = [
        entry for entry in files
        if entry["path"].startswith(".openresearch/artifacts/")
    ]
    (OUTPUTS / "artifact_manifest.json").write_text(
        json.dumps(artifact_files, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        "bundle": bundle.relative_to(ROOT).as_posix(),
        "bundle_bytes": bundle.stat().st_size,
        "bundle_sha256": sha256(bundle),
        "file_count": len(files),
        "artifact_file_count": len(artifact_files),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
