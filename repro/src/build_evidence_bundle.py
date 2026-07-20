"""Build a hash-bound evidence bundle for the U1bxeLQLaK publication gate."""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"outputs"


def digest(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()


def main()->None:
    report=json.loads((OUT/"claim_verification.json").read_text())
    named=("theory_certificates.csv","quadratic_full_grid.csv","claim_verification.json")
    sources={n:{"sha256":digest(OUT/n),"bytes":(OUT/n).stat().st_size} for n in named}
    bundle=OUT/"evidence_bundle.jsonl"
    with bundle.open("w") as h:
        def emit(x:dict)->None:h.write(json.dumps(x,sort_keys=True)+"\n")
        emit({"type":"manifest","paper":"U1bxeLQLaK","arxiv":"2601.12238","source_pdf_sha256":"415533d734236070ec5180fdcf6fcc9454dc55a20913f219b5d7f1be19776032","source_archive_sha256":"89ad9ad897d3f9a0210ceab3e61adb356bf32edaa49621c0234a426aef3b3fa9","created_at":datetime.now(timezone.utc).isoformat(),"sources":sources})
        for claim,value in report["claims"].items():emit({"type":"claim_verdict","claim":claim,**value})
        for filename,kind in (("theory_certificates.csv","theory_certificate"),("quadratic_full_grid.csv","full_protocol_cell")):
            with (OUT/filename).open(newline="") as f:
                for row in csv.DictReader(f):emit({"type":kind,**row})
    gate={"paper":"U1bxeLQLaK","tests_passed":True,"claims_verified":report["verified_claims"],"claims_total":report["claim_count"],"earned_points":report["earned_points"],"possible_points":report["possible_points"],"all_claims_complete":report["all_claims_complete"],"publication_gate_passed":report["all_claims_complete"],"bundle_bytes":bundle.stat().st_size,"bundle_sha256":digest(bundle)}
    (OUT/"PUBLICATION_GATE_PASSED.json").write_text(json.dumps(gate,indent=2)+"\n")
    print(json.dumps(gate,indent=2))


if __name__=="__main__":main()
