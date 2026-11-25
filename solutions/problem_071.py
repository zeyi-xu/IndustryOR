"""IndustryOR problem 071: Commercial real estate portfolio selection."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_071") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        properties = range(1, 5)
        cost = dict(zip(properties, [1_500_000, 2_100_000, 2_300_000, 4_200_000]))
        income = dict(zip(properties, [12_500, 35_000, 23_000, 100_000]))
        buy = model.addVars(properties, vtype=GRB.BINARY, name="buy")
        model.addConstr(buy.prod(cost) <= 7_000_000)
        model.addConstr(buy[3] + buy[4] <= 1)
        model.setObjective(buy.prod(income), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
