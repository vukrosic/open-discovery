---
name: formalize-math
description: Translate an informal theorem, conjecture, mathematical argument, or proof into a faithful formal statement and attempt machine-checked verification with an available proof assistant, preferring Lean when suitable. Use when the user asks to formalize mathematics, verify a proof, encode a claim in Lean or another prover, test a conjecture, find a counterexample, or diagnose why a formal proof does not check.
---

# Formalize Math

Produce a checked artifact or an exact failure state. Treat semantic fidelity and
proof-assistant acceptance as separate obligations: a weak or altered statement
does not verify the original claim, and an unchecked argument is not a proof.

## Establish the claim

Preserve the user's original claim verbatim. Resolve notation from supplied
context and state every choice that can change the meaning, including:

- domains, types, quantifier order, and variable dependencies;
- definitions, equality notions, boundary cases, and side conditions;
- imported results and any classical, choice, extensionality, or decidability
  assumptions.

Before proving, write the candidate formal statement and a short interpretation
map from each material informal phrase to its formal counterpart. Label semantic
fidelity as `faithful`, `conditional`, or `unresolved`, with the reason. Ask one
question only if incompatible readings would materially change the theorem and
context cannot select one safely. Otherwise choose the narrowest defensible
reading and expose it.

Do not silently weaken, strengthen, or repair the statement to make a proof
work. Record every later statement revision as a semantic change, explain why it
was made, and reassess fidelity before treating its proof as relevant.

## Choose the checking environment

Inspect the existing project and installed commands first. Reuse its pinned
proof-assistant version and dependencies when present. Prefer Lean for ordinary
theorem-proving work when it is suitable and locally available; otherwise use a
locally available assistant appropriate to the domain, such as Rocq/Coq,
Isabelle, or Agda. Do not substitute an SMT result, numeric experiment, or
language type-check for proof-assistant kernel acceptance without clearly
changing the claim.

Do not install a large toolchain or fetch substantial dependencies without
explicit authority. If no suitable checker is available, still produce a
reviewable source draft when useful, but label it unverified and report the
missing executable or environment exactly.

Work in the user-specified location or a clearly owned scratch directory. Do
not alter an existing proof project merely to accommodate the theorem. Keep the
artifact minimal and compatible with the detected project rather than importing
large libraries for convenience.

## Attempt verification

Seek an obvious counterexample before investing in a proof when the claim is a
conjecture, contains suspicious edge cases, or proof search exposes a likely
gap. Use symbolic reasoning, bounded enumeration, or a model finder as
appropriate. A finite search is evidence, not a general proof, unless the
formalized domain is itself finite and exhaustively checked by the assistant.

Then create the smallest source artifact that states the selected theorem and
attempts its proof. Compile or check it with the assistant's normal command.
Capture:

- assistant and exact version;
- source file, project or lock context, imports, and command;
- exit status, diagnostics, warnings, and target declaration name;
- placeholders, newly introduced axioms, admitted facts, oracle-like tactics,
  or other trusted-base extensions;
- the axioms or assumptions reported for the final theorem when the assistant
  can expose them.

Reject `sorry`, `admit`, proof holes, or a newly declared proposition used as an
axiom as completion. Do not hide warnings or bypasses behind a successful exit
code. Re-run the final source from a clean invocation and inspect the actual
output before assigning a checked status.

If proof search fails, preserve the strongest useful artifact: a faithful
statement with diagnostics, a minimized counterexample, or a partial proof with
the exact remaining goals. Do not invent lemmas, library names, commands, or
successful checks.

## Report the result

Return the artifact and a compact verification receipt containing:

1. original claim and formal statement;
2. semantic-fidelity label, interpretation choices, and exposed assumptions;
3. one outcome: `VERIFIED`, `COUNTEREXAMPLE`, `FORMALIZED_NOT_VERIFIED`, or
   `BLOCKED`;
4. checker, version, imports, command, exit status, warnings, axioms, and
   placeholder scan;
5. any remaining gap and the narrowest claim justified by the evidence.

Use `VERIFIED` only when the faithful or explicitly conditional statement was
accepted by the proof assistant with no undisclosed holes. Kernel acceptance
proves the encoded theorem relative to its logic, imports, and exposed axioms;
it does not by itself establish that the encoding matches the user's intent.
Use `COUNTEREXAMPLE` only when the witness actually violates the formalized
claim and report whether that fact was machine-checked. Never call a plausible
paper proof, generated script, successful parsing step, bounded test, or
unexecuted source a machine-checked proof.
