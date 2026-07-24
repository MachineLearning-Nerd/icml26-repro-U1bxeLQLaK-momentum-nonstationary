from __future__ import annotations

import json
from pathlib import Path

from evaluator_visible_release import CANDIDATE


ROOT = Path(__file__).resolve().parents[2]


def test_current_verifier_is_first_and_historical_pages_are_labeled() -> None:
    logbook = json.loads((CANDIDATE / "logbook.json").read_text())
    assert logbook["root"]["slug"] == "current-verification"
    titles = [
        str(child["title"]).lower()
        for child in logbook["root"]["children"]
    ]
    assert titles[0].startswith("claim 1")
    assert any("historical rejected baseline" in title for title in titles)


def test_every_claim_page_exposes_the_release_gate() -> None:
    required = (
        "Exact claim and quantifiers",
        "Assumptions and numerical audit",
        "Executable verifier",
        "Pinned environment and fixed command",
        "Raw results shown inline",
        "Independent checker and negative control",
        "Limitations and deviations",
        "Revision, seeds, CPU, and runtime",
        "Failure probe",
    )
    for number in range(1, 6):
        page = (
            CANDIDATE
            / f"pages/campaign-claim-{number}/page.md"
        ).read_text()
        for heading in required:
            assert heading in page, (number, heading)
        for suffix in ("pass.json", "failure_probe.json"):
            assert (
                CANDIDATE
                / "evidence/current_verifier"
                / f"claim_{number}_{suffix}"
            ).is_file()


def test_visibility_matrix_complete() -> None:
    review = json.loads(
        (
            CANDIDATE
            / "evidence/evaluator_blind_review/second_pass.json"
        ).read_text()
    )
    assert review["reviewer_started_from"] == ["README.md", "logbook.json"]
    assert review["all_rows_complete"]
    assert len(review["visibility_matrix"]) == 5
    for row in review["visibility_matrix"]:
        assert all(
            row[field]
            for field in (
                "canonical_page",
                "code_visible",
                "data_inline",
                "raw_link",
                "checker",
                "control",
                "exact_claim_tested",
                "reviewer_verdict",
            )
        )
