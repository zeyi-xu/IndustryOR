"""IndustryOR problem 057: Yarra Valley fruit acreage."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_057") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        crops = ["apples", "pears", "oranges", "lemons"]
        profit = dict(zip(crops, [2000, 1800, 2200, 3000]))
        acres = model.addVars(crops, name="acres")
        grown = model.addVars(crops, vtype=GRB.BINARY, name="grown")
        model.addConstr(acres.sum() <= 120)
        model.addConstr(grown.sum() <= 2)
        model.addConstrs(acres[c] <= 120 * grown[c] for c in crops)
        model.addConstr(acres["apples"] >= 2 * acres["pears"])
        model.addConstr(acres["apples"] >= 3 * acres["lemons"])
        model.addConstr((grown["lemons"] == 1) >> (acres["oranges"] == 2 * acres["lemons"]))
        model.setObjective(acres.prod(profit), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
