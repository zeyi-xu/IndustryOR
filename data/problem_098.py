"""IndustryOR problem 098: Spare components for maximum system reliability."""

from math import exp, log

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_098") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        reliability = [
            [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.6, 0.75, 0.95, 1.0, 1.0, 1.0],
            [0.7, 0.9, 1.0, 1.0, 1.0, 1.0],
        ]
        cost = [20, 30, 40]
        weight = [2, 4, 6]
        components, counts = range(3), range(6)
        choose = model.addVars(components, counts, vtype=GRB.BINARY, name="choose_spares")
        model.addConstrs(choose.sum(i, "*") == 1 for i in components)
        total_cost = gp.quicksum(cost[i] * k * choose[i, k] for i in components for k in counts)
        total_weight = gp.quicksum(
            weight[i] * k * choose[i, k] for i in components for k in counts
        )
        model.addConstr(total_cost <= 150)
        model.addConstr(total_weight <= 20)
        # Maximizing the log of the product preserves the reliability maximizer.
        log_reliability = gp.quicksum(
            log(reliability[i][k]) * choose[i, k] for i in components for k in counts
        )
        model.setObjective(log_reliability, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return exp(model.ObjVal)


if __name__ == "__main__":
    print(solve())
