"""Evaluate the beta-dependent Theorem-3.3 and Theorem-3.9 certificates."""
from __future__ import annotations

import csv
from pathlib import Path

from theory_certificates import block_switch_regret, jump_response_time, stationary_hb_variance, theorem33_drift_term, theorem33_stability_cap

ROOT=Path(__file__).resolve().parents[2]


def main() -> None:
    rows=[]
    for beta in (.50,.75,.90,.95,.99,.995,.999):
        cap=theorem33_stability_cap(1.,1.,beta)
        gamma=.8*cap
        response=jump_response_time(1.,gamma,beta)
        rows.append({"beta":beta,"one_minus_beta":1-beta,"stability_cap":cap,"gamma":gamma,"theorem33_drift_floor":theorem33_drift_term(1.,gamma,beta,.01),"stationary_hb_variance":stationary_hb_variance(1.,gamma,beta,.8),"jump_response_steps":response,"block_switch_regret":block_switch_regret(1.,gamma,beta,block_length=max(4*response,20),blocks=8)})
    with (ROOT/"outputs"/"theory_certificates.csv").open("w",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print("certificate rows",len(rows),"response ratio",rows[-1]["jump_response_steps"]/rows[0]["jump_response_steps"])


if __name__ == "__main__":
    main()
