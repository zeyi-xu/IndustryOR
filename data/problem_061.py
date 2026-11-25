"""IndustryOR problem 061: Restaurant investments under a purchase budget."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_061") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        cost = {"A": 1_600_000, "B": 2_500_000, "C": 1_800_000, "D": 3_000_000}
        income = {"A": 15_000, "B": 40_000, "C": 30_000, "D": 50_000}
        purchase = model.addVars(cost.keys(), vtype=GRB.BINARY, name="purchase")
        model.addConstr(purchase.prod(cost) <= 6_000_000)
        model.addConstr(purchase["A"] + purchase["D"] <= 1)
        model.setObjective(purchase.prod(income), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
