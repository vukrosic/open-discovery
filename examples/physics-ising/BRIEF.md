# 2D Ising sampling experiment

## 1. What question is being asked?

Near the finite-size transition of the 2D square-lattice Ising model, does a
Wolff cluster sampler produce lower magnetization autocorrelation than a
single-spin Metropolis sampler at comparable computational cost?

## 2. What inputs and permissions exist?

The experiment has a square lattice with periodic boundaries, coupling `J=1`,
sizes `L=16,32`, temperatures `2.0, 2.2, 2.269, 2.4, 2.6`, and seeds
`7,11,13`. It is a local standard-library simulation with no external data,
network, or physical measurement.

## 3. What can be changed?

The experiment compares the Metropolis and Wolff sampler implementations under
the recorded lattice, temperature, burn-in, and sampling settings. A future
candidate may change the sampler or numerical implementation, but not silently
change the comparison inputs.

## 4. How is success measured?

The primary measure is integrated autocorrelation time of signed magnetization
at `T=2.269`. Runtime and effective independent samples are compared at the
same time, with mean absolute magnetization, energy, and susceptibility as
secondary measures.

## 5. What evidence was produced?

The run preserves a CSV of all 60 combinations, a JSON summary and run receipt,
and SVG plots for autocorrelation and phase-transition behavior.

## 6. What is missing or uncertain?

This is a finite-size model comparison. It does not determine the exact
thermodynamic critical point or describe a real material without a separate
model-to-system mapping.

## 7. When must the agent stop and ask a human?

Stop if the model, sampler definitions, measurement conventions, or compute
budget are materially underspecified. Do not present a simulation output as an
observation of a physical material.
