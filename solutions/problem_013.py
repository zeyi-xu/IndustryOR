"""IndustryOR problem 013: Sunshine Valley crop acreage."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_013") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        crops = ("corn", "wheat", "soybean", "sorghum")
        corn, wheat, soybean, sorghum = [model.addVar(name=crop) for crop in crops]
        model.addConstr(corn + wheat + soybean + sorghum <= 100)
        model.addConstr(corn >= 2 * wheat)
        model.addConstr(soybean >= 0.5 * sorghum)
        model.addConstr(wheat == 3 * sorghum)
        profit = 1500 * corn + 1200 * wheat + 1800 * soybean + 1600 * sorghum
        model.setObjective(profit, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
