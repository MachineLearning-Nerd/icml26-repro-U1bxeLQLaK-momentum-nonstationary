# Claim 4 source-contract evaluation

Verdict: **FALSIFIED**

- Momentum/SGD drift--noise coefficient ratio exponent:
  `2.000000000000`.
- Vanilla-SGD displayed bound contains a drift--noise coupling: `True`.
- Theorem 3.6 displayed forgetting-horizon exponent after its own stability
  substitution: `2.000000000000`, not `1`.
- Separate physical velocity-memory exponent: `1.090909`.

The exact imported claim is conjunctive. Two clauses contradict the displayed
source formulas, so this route falsifies that exact wording while preserving
the correct momentum-specific coefficient amplification.
