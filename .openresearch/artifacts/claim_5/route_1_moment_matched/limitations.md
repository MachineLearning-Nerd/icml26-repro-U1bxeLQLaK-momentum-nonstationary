
# Claim 5 limitations and deviations

- No author code was linked in the paper source. The linear-regression oracle
  is Gaussian and moment-matched to the exact raw mini-batch gradient; it does
  not reproduce its higher moments.
- This new route does not claim a source-scale MLP reproduction. The judged
  logbook's small MLP remains preserved as earlier evidence only.
- Logistic regression is not rerun here. Its Bernoulli oracle cannot be
  reconstructed exactly from the paper's incomplete implementation details.
- Consequently, a passing route is substantial evidence for the missing
  kappa/drift/NAG factors, but the campaign should assign MEDIUM—not HIGH—
  confidence to the broad all-model Claim 5.
