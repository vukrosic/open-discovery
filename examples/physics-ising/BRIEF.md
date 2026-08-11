# 2D Ising sampling experiment

## Question

Near the finite-size transition of the 2D square-lattice Ising model, does a
Wolff cluster sampler produce lower magnetization autocorrelation than a
single-spin Metropolis sampler at comparable computational cost?

## Frozen protocol

- Square lattice with periodic boundaries and coupling `J = 1`.
- Lattice sizes: `L = 16, 32`.
- Temperatures: `2.0, 2.2, 2.269, 2.4, 2.6`.
- Samplers: Metropolis and Wolff.
- Seeds: `7, 11, 13` for every size, temperature, and sampler.
- Burn-in: `200` sweeps; recorded samples: `500` sweeps.
- One Metropolis sweep attempts `L²` flips. One Wolff sweep grows clusters
  until at least `L²` spins have been flipped.
- Primary outcome: integrated autocorrelation time of signed magnetization at
  `T = 2.269`.
- Secondary outcomes: mean absolute magnetization, energy, susceptibility,
  runtime, and effective independent samples.

## Claim boundary

The result is a finite-size simulation comparison. It does not estimate the
thermodynamic critical point exactly and does not make claims about physical
materials without a model-to-system mapping.

