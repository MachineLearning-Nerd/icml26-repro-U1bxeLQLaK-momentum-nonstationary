
# Claim 4 aggregate evaluation

Verdict: **FALSIFIED**

- Exact imported conjunction: **FALSIFIED**.
- Narrower momentum-specific coefficient interpretation: **VERIFIED**.
- Momentum/SGD coefficient ratio exponent: `2.000000`.
- Theorem 3.6 displayed forgetting-horizon exponent after its own stability
  substitution: `2.000000`, not `1`.
- Physical velocity-memory exponent: `1.090909`.
- Vanilla-SGD displayed bound contains drift--noise coupling: `True`.
- Minimum pathwise 95% envelope coverage: `0.950750`.

The exact claim is falsified because two conjuncts conflict with the displayed
source formulas. This does not erase the separately verified beta-specific
amplification.
