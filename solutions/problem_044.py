"""IndustryOR problem 044: Production with decreasing marginal profit tiers."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_044") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        products = range(3)
        # Interpret the table as incremental discounts. The tuple holds the
        # tier width and its marginal profit per piece. Higher-margin tiers
        # fill first because a product uses the same resources in every tier.
        tiers = [
            [(40, 10), (60, 9), (50, 8), (GRB.INFINITY, 7)],
            [(50, 6), (50, 4), (GRB.INFINITY, 3)],
            [(100, 5), (GRB.INFINITY, 4)],
        ]
        resource_use = [[1, 2, 1], [10, 4, 5], [3, 2, 1]]
        capacity = [100, 700, 400]
        keys = [(p, t) for p in products for t in range(len(tiers[p]))]
        units = model.addVars(
            keys, ub={(p, t): tiers[p][t][0] for p, t in keys},
            vtype=GRB.INTEGER, name="units_in_tier",
        )
        for limit, usage in zip(capacity, resource_use):
            model.addConstr(gp.quicksum(usage[p] * units.sum(p, "*") for p in products) <= limit)
        profit = gp.quicksum(tiers[p][t][1] * units[p, t] for p, t in keys)
        model.setObjective(profit, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
