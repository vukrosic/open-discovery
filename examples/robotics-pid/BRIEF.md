# Robotics PID tuning experiment

## 1. What question is being asked?

Can an automatically searched PID controller make a simulated one-joint robot
arm track a target angle more accurately than a fixed hand-tuned controller
while remaining stable under unseen disturbances?

## 2. What inputs and permissions exist?

The input is a deterministic one-joint plant with inertia `J=1.0`, damping
`b=1.2`, Euler step `dt=0.01`, torque clipped to `[-8,8]`, and five-second
episodes. Two development episodes tune gains and three frozen holdout episodes
test them. There is no random number, external data, network, or physical
actuation.

## 3. What can be changed?

The agent may search the gain grid `Kp ∈ {2.5,4.0,5.5}`,
`Ki ∈ {0.4,1.0,1.6}`, and `Kd ∈ {0.05,0.15,0.30}`, or propose another
controller candidate. The plant, episodes, baseline gains, and holdout data
remain fixed for the comparison.

The candidate interface is a new `candidates/candidate-NNN/solution.py`
defining `choose_gains(dev_episodes, score)`. The evaluator exposes only the
development episodes and scorer; it keeps holdout episodes evaluator-owned.

## 4. How is success measured?

The primary measure is mean holdout angle RMSE. A candidate succeeds only if it
is stable on every holdout episode and has strictly lower RMSE than the
baseline. Overshoot, settling time, and control energy are reported as
trade-offs.

## 5. What evidence was produced?

The run preserves the tuning grid, per-episode metrics, trajectory and
comparison SVGs, a JSON summary, and a run receipt with the protocol hash.

## 6. What is missing or uncertain?

The arm is a toy simulation and the result covers only this plant and these
disturbances. It does not establish that the gains are optimal, safe,
transferable, or better on physical hardware.

## 7. When must the agent stop and ask a human?

Stop if the plant, controller interface, disturbance episodes, safety bounds, or
success metric are missing or materially unclear. Never imply physical safety
or hardware validation from the simulation.
