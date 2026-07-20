"""Fail-closed claim gate for all three live U1bxeLQLaK claims."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def float_rows(path: Path) -> list[dict[str, float | str]]:
    with path.open(newline="") as handle:
        rows=[]
        for row in csv.DictReader(handle):
            rows.append({key:(float(value) if key not in {"method"} else value) for key,value in row.items()})
        return rows


def main() -> None:
    theory=float_rows(ROOT/"outputs"/"theory_certificates.csv")
    grid=float_rows(ROOT/"outputs"/"quadratic_full_grid.csv")
    # C1: Eq. 3.5's explicit drift term under the theorem's stability cap must
    # grow sharply with beta, while the direct post-shift response length grows
    # in the associated inertia window.
    low,high=theory[0],theory[-1]
    response_products=[r["jump_response_steps"]*r["one_minus_beta"] for r in theory]
    c1=all(theory[i]["theorem33_drift_floor"]<theory[i+1]["theorem33_drift_floor"] and theory[i]["jump_response_steps"]<theory[i+1]["jump_response_steps"] for i in range(len(theory)-1)) and high["theorem33_drift_floor"]/low["theorem33_drift_floor"]>1e9 and max(response_products)/min(response_products)<1.02
    by_key={(r["gamma"],r["beta"],r["noise_variance"],r["method"]):r for r in grid}
    scenarios=[]
    for gamma in (.01,.05,.1):
        for beta in (.5,.9,.95,.99):
            for noise in (.1,.5,.8):
                sgd=by_key[(gamma,beta,noise,"sgd")]["mean_final_error"]
                hb=by_key[(gamma,beta,noise,"hb")]["mean_final_error"]
                nag=by_key[(gamma,beta,noise,"nag")]["mean_final_error"]
                scenarios.append((sgd,hb,nag))
    c2=len(grid)==108 and all(r["seeds"]==20 and r["dimension"]==100 and r["horizon"]==5000 and r["drift"]==.01 for r in grid) and all(s<h and s<n for s,h,n in scenarios)
    # C3: finite block switching realizes the lower-bound mechanism: every
    # stability-tuned beta has a nonzero switching regret and the exact response
    # window is proportional to 1/(1-beta), not a numerical artifact.
    c3=all(r["block_switch_regret"]>0 for r in theory) and high["block_switch_regret"]>100*low["block_switch_regret"] and high["jump_response_steps"]/low["jump_response_steps"]>400
    claims={
      "C1_explicit_drift_amplification":{"passed":bool(c1),"beta_low":low["beta"],"beta_high":high["beta"],"drift_floor_ratio":high["theorem33_drift_floor"]/low["theorem33_drift_floor"],"response_time_ratio":high["jump_response_steps"]/low["jump_response_steps"]},
      "C2_drift_dominated_sgd_beats_momentum":{"passed":bool(c2),"full_method_cells":len(grid),"full_trials":len(grid)*20,"sgd_wins":sum(s<h and s<n for s,h,n in scenarios),"scenarios":len(scenarios)},
      "C3_inertia_lower_bound_mechanism":{"passed":bool(c3),"block_regret_ratio":high["block_switch_regret"]/low["block_switch_regret"],"inertia_window_ratio":high["jump_response_steps"]/low["jump_response_steps"],"source_theorem":"Theorem 3.9"}
    }
    report={"paper":"U1bxeLQLaK","claim_count":3,"verified_claims":sum(x["passed"] for x in claims.values()),"possible_points":6,"earned_points":2*sum(x["passed"] for x in claims.values()),"all_claims_complete":all(x["passed"] for x in claims.values()),"claims":claims}
    (ROOT/"outputs"/"claim_verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    if not report["all_claims_complete"]:raise SystemExit("claim gate failed")


if __name__=="__main__":main()
