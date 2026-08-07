# Mathematics mode

Use this mode for conjectures, proofs, counterexamples, formalization,
symbolic computation, and numerical exploration.

## Field-specific tools

- **Definition ledger:** freeze every object, condition, convention, and domain
  used by the claim.
- **Conjecture normalizer:** rewrite the statement with explicit quantifiers and
  boundary cases.
- **Example generator:** construct small, extreme, symmetric, and degenerate
  cases.
- **Counterexample search:** use reasoning, enumeration, symbolic algebra, or
  numerical search to try to falsify the statement.
- **Lemma map:** break the target into dependencies and mark which steps are
  proved, assumed, cited, or unresolved.
- **Proof-attempt log:** preserve failed approaches and the exact obstruction.
- **Computation checker:** independently verify algebra or finite cases while
  recording code, precision, and range.
- **Formal-verification bridge:** when useful, translate a stable statement or
  lemma into Lean, Coq, Isabelle, or another proof assistant.

## Evidence language

Numerical agreement, symbolic simplification, and exhaustive checks over a
finite range are evidence, not a proof of an unrestricted theorem. Label every
result as a proof, conditional proof, cited theorem, verified finite case,
numerical observation, counterexample, or open step.

## Useful first experiments

- test the smallest and boundary cases;
- search systematically for a counterexample;
- verify whether the proposed lemma is already known under another name;
- isolate the first unsupported step in a proof attempt.
