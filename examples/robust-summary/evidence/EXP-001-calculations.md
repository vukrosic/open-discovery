# EXP-001 inputs and calculations

> Constructed teaching data. These are not real sensor observations.

## Frozen inputs

The known center is `10.0` in every case. Absolute error is
`|summary - 10.0|`.

| Case | Spike direction | Five readings |
| --- | --- | --- |
| A | Positive | 9.8, 10.0, 10.1, 10.1, 20.0 |
| B | Positive | 9.9, 10.0, 10.0, 10.2, 20.0 |
| C | Negative | 0.0, 9.9, 10.0, 10.1, 10.2 |
| D | Negative | 0.0, 9.8, 10.0, 10.1, 10.1 |

## Frozen methods

- Baseline: arithmetic mean of all five readings.
- Candidate: remove one largest reading, then take the arithmetic mean of the
  remaining four.

## Exact calculations

| Case | Baseline calculation | Baseline error | Candidate calculation | Candidate error |
| --- | --- | ---: | --- | ---: |
| A | 60.0 / 5 = 12.000 | 2.000 | 40.0 / 4 = 10.000 | 0.000 |
| B | 60.1 / 5 = 12.020 | 2.020 | 40.1 / 4 = 10.025 | 0.025 |
| C | 40.2 / 5 = 8.040 | 1.960 | 30.0 / 4 = 7.500 | 2.500 |
| D | 40.0 / 5 = 8.000 | 2.000 | 29.9 / 4 = 7.475 | 2.525 |

## Aggregate check

- Baseline mean absolute error: `(2.000 + 2.020 + 1.960 + 2.000) / 4 = 1.995`
- Candidate mean absolute error: `(0.000 + 0.025 + 2.500 + 2.525) / 4 = 1.2625`

The candidate has lower average error, but it fails the frozen case-level gate
in C and D. The average therefore cannot justify success.
