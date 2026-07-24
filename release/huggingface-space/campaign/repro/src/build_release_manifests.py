"""Validate the additive Space candidate and build the publication allowlist."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "release" / "huggingface-space"
MANIFESTS = ROOT / "release" / "manifests"
JUDGED = MANIFESTS / "judged-files.tsv"
TEXT_SUFFIXES = {
    "",
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".jsonl",
    ".lock",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".tsv",
    ".txt",
}
SECRET_PATTERNS = {
    "hugging_face_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "github_token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_judged() -> dict[str, dict[str, str | int]]:
    result: dict[str, dict[str, str | int]] = {}
    for line in JUDGED.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        digest, size, relative = line.split("\t", 2)
        result[relative] = {"sha256": digest, "bytes": int(size)}
    return result


def _candidate_files() -> dict[str, dict[str, str | int]]:
    return {
        path.relative_to(CANDIDATE).as_posix(): {
            "sha256": _digest(path),
            "bytes": path.stat().st_size,
        }
        for path in sorted(CANDIDATE.rglob("*"))
        if path.is_file()
    }


def _write_tsv(
    path: Path,
    rows: dict[str, dict[str, str | int]],
    heading: list[str],
) -> None:
    lines = [*heading, "# columns: sha256\tbytes\tpath"]
    lines.extend(
        f"{value['sha256']}\t{value['bytes']}\t{relative}"
        for relative, value in rows.items()
    )
    path.write_text("\n".join(lines) + "\n")


def _validate_logbook() -> dict[str, int]:
    payload = json.loads((CANDIDATE / "logbook.json").read_text())
    if payload["space_id"] != "DineshAI/U1bxeLQLaK":
        raise SystemExit("candidate targets the wrong Space")
    slugs: set[str] = set()
    pages = 0

    def visit(node: dict[str, object]) -> None:
        nonlocal pages
        slug = str(node["slug"])
        if slug in slugs:
            raise SystemExit(f"duplicate logbook slug: {slug}")
        slugs.add(slug)
        page = CANDIDATE / str(node["file"])
        if not page.is_file():
            raise SystemExit(f"missing logbook page: {page}")
        pages += 1
        for child in node.get("children", []):
            visit(child)

    visit(payload["root"])
    return {"page_count": pages, "unique_slug_count": len(slugs)}


def _validate_machine_files() -> dict[str, int]:
    json_count = 0
    csv_count = 0
    for path in sorted((CANDIDATE / "evidence").rglob("*")):
        if path.suffix == ".json":
            json.loads(path.read_text())
            json_count += 1
        elif path.suffix == ".csv":
            with path.open(newline="") as handle:
                reader = csv.reader(handle)
                if next(reader, None) is None:
                    raise SystemExit(f"empty CSV: {path}")
            csv_count += 1
    return {"validated_json_files": json_count, "validated_csv_files": csv_count}


def _secret_scan(paths: list[str]) -> dict[str, object]:
    findings: list[dict[str, str]] = []
    for relative in paths:
        path = CANDIDATE / relative
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append({"path": relative, "pattern": name})
    result = {
        "scanned_text_file_count": len(paths),
        "finding_count": len(findings),
        "findings": findings,
        "passed": not findings,
    }
    if findings:
        raise SystemExit("secret-shaped material found; see secret-scan.json")
    return result


def main() -> None:
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    judged = _read_judged()
    candidate = _candidate_files()
    missing = sorted(set(judged) - set(candidate))
    modified = sorted(
        path
        for path in set(judged) & set(candidate)
        if judged[path]["sha256"] != candidate[path]["sha256"]
    )
    if missing:
        raise SystemExit(f"candidate is missing judged paths: {missing}")
    if modified != ["logbook.json"]:
        raise SystemExit(
            "unexpected changes to judged files; only logbook.json may be additive: "
            f"{modified}"
        )

    _write_tsv(
        MANIFESTS / "candidate-files.tsv",
        candidate,
        [
            "# Candidate Hugging Face Space manifest",
            "# space_id: DineshAI/U1bxeLQLaK",
        ],
    )
    subset = {
        "space_id": "DineshAI/U1bxeLQLaK",
        "judged_revision": "9db6b4452399d8ef19e3f8ca479a627060819fb3",
        "old_file_count": len(judged),
        "candidate_file_count": len(candidate),
        "old_file_set_is_subset": not missing,
        "missing_old_paths": missing,
        "content_identical_old_files": len(judged) - len(modified),
        "intentionally_modified_old_files": modified,
        "all_old_page_files_content_identical": all(
            judged[path]["sha256"] == candidate[path]["sha256"]
            for path in judged
            if path.startswith("pages/")
        ),
        "passed": not missing and modified == ["logbook.json"],
    }
    (MANIFESTS / "subset-check.json").write_text(
        json.dumps(subset, indent=2, sort_keys=True) + "\n"
    )

    changed_or_new = sorted(
        path
        for path, value in candidate.items()
        if path not in judged or value["sha256"] != judged[path]["sha256"]
    )
    non_text = [
        path
        for path in changed_or_new
        if (CANDIDATE / path).suffix.lower() not in TEXT_SUFFIXES
    ]
    undecodable = []
    for path in changed_or_new:
        try:
            (CANDIDATE / path).read_text()
        except UnicodeDecodeError:
            undecodable.append(path)
    if non_text or undecodable:
        raise SystemExit(
            f"new/changed upload paths must be text; non_text={non_text}, "
            f"undecodable={undecodable}"
        )
    (MANIFESTS / "hf-upload-allowlist.txt").write_text(
        "\n".join(changed_or_new) + "\n"
    )
    upload_rows = {path: candidate[path] for path in changed_or_new}
    _write_tsv(
        MANIFESTS / "hf-upload-sha256.tsv",
        upload_rows,
        [
            "# Exact text-only Hugging Face upload manifest",
            "# target: DineshAI/U1bxeLQLaK",
        ],
    )

    logbook = _validate_logbook()
    machine = _validate_machine_files()
    secret_scan = _secret_scan(changed_or_new)
    (MANIFESTS / "secret-scan.json").write_text(
        json.dumps(secret_scan, indent=2, sort_keys=True) + "\n"
    )
    summary = {
        "candidate_manifest_sha256": _digest(
            MANIFESTS / "candidate-files.tsv"
        ),
        "upload_manifest_sha256": _digest(
            MANIFESTS / "hf-upload-sha256.tsv"
        ),
        "upload_file_count": len(changed_or_new),
        "subset_check": subset,
        "logbook_validation": logbook,
        "machine_file_validation": machine,
        "secret_scan": secret_scan,
        "passed": (
            subset["passed"]
            and secret_scan["passed"]
            and logbook["page_count"] == logbook["unique_slug_count"]
        ),
    }
    (MANIFESTS / "release-validation.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not summary["passed"]:
        raise SystemExit("release validation failed")


if __name__ == "__main__":
    main()
