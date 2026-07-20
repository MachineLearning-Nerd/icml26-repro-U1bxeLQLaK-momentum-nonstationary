"""Run the complete 108-method, 20-seed, 5,000-step Table-1 matrix."""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from quadratic_protocol import QuadraticProtocol, run_cell

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    protocol = QuadraticProtocol()
    rows=[]
    for gamma in protocol.gammas:
        for beta in protocol.betas:
            for noise_variance in protocol.noise_variances:
                for method in ("sgd", "hb", "nag"):
                    values=run_cell(gamma=gamma,beta=beta,noise_variance=noise_variance,method=method,protocol=protocol)
                    row={"gamma":gamma,"beta":beta,"noise_variance":noise_variance,"method":method,"seeds":protocol.seeds,"dimension":protocol.dimension,"horizon":protocol.horizon,"drift":protocol.drift,"mean_final_error":float(np.mean(values)),"std_final_error":float(np.std(values,ddof=1)),"sem_final_error":float(np.std(values,ddof=1)/np.sqrt(protocol.seeds))}
                    rows.append(row)
                    print(method,f"gamma={gamma}",f"beta={beta}",f"sigma2={noise_variance}",f"error={row['mean_final_error']:.6f}",flush=True)
    path=ROOT/"outputs"/"quadratic_full_grid.csv"
    with path.open("w",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(f"completed {len(rows)} source-scale method cells / {len(rows)*protocol.seeds} full trials")


if __name__ == "__main__":
    main()
