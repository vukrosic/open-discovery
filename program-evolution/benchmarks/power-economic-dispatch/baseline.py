"""Readable integer economic-dispatch baseline for three generators."""


def dispatch(demand, capacities, linear_costs, quadratic_costs):
    best = None
    for first in range(capacities[0] + 1):
        for second in range(capacities[1] + 1):
            third = demand - first - second
            if third < 0 or third > capacities[2]:
                continue
            generation = (first, second, third)
            cost = sum(
                linear_costs[i] * generation[i]
                + quadratic_costs[i] * generation[i] * generation[i]
                for i in range(3)
            )
            candidate = (cost, generation)
            if best is None or candidate < best:
                best = candidate
    if best is None:
        raise ValueError("demand is infeasible")
    return {"generation": list(best[1]), "cost": best[0]}
