"""IndustryOR problem 021: Monthly production line activation."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_021") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        products = range(3)
        demand = [5300, 4500, 5400]
        daily_quota = [500, 450, 550]
        min_batch = [20, 20, 16]
        activation_cost = dict(enumerate([170_000, 150_000, 100_000]))
        margin = dict(enumerate([124 - 73.30, 109 - 52.90, 115 - 65.40]))
        units = model.addVars(products, name="hundred_kg")
        active = model.addVars(products, vtype=GRB.BINARY, name="line_active")
        model.addConstrs(units[p] <= demand[p] * active[p] for p in products)
        model.addConstrs(units[p] >= min_batch[p] * active[p] for p in products)
        model.addConstr(gp.quicksum(units[p] / daily_quota[p] for p in products) <= 22)
        # Interpret revenue net of the production and activation costs in the prompt.
        model.setObjective(units.prod(margin) - active.prod(activation_cost), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
