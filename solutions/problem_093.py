"""IndustryOR problem 093: Gasoline blending with tiered crude-oil purchasing."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_093") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        grades = ("I", "II")
        price = {"I": 4800, "II": 5600}
        min_a = {"I": 0.50, "II": 0.60}
        crude_a = model.addVars(grades, name="crude_a")
        crude_b = model.addVars(grades, name="crude_b")
        purchased = model.addVars(range(3), ub=500, name="purchased_in_tier")
        tier_open = model.addVars([1, 2], vtype=GRB.BINARY, name="tier_open")
        for tier in (1, 2):
            model.addConstr(purchased[tier] <= 500 * tier_open[tier])
            model.addConstr(purchased[tier - 1] >= 500 * tier_open[tier])
        for g in grades:
            model.addConstr(crude_a[g] >= min_a[g] * (crude_a[g] + crude_b[g]))
        model.addConstr(crude_a.sum() <= 500 + purchased.sum())
        model.addConstr(crude_b.sum() <= 1000)
        # Only additional crude A has a specified acquisition cost.
        cost = purchased.prod({0: 10_000, 1: 8000, 2: 6000})
        model.setObjective(crude_a.prod(price) + crude_b.prod(price) - cost, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
