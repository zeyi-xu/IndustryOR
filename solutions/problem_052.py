"""IndustryOR problem 052: Zhang family trip selection."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_052") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        cost = {
            "Harry": 1200,
            "Hermione": 1650,
            "Ron": 750,
            "Fred": 800,
            "George": 800,
            "Ginny": 1500,
        }
        take = model.addVars(cost.keys(), vtype=GRB.BINARY, name="take")
        model.addConstr(take.sum() >= 3)
        model.addConstr(take.sum() <= 4)
        model.addConstr(take["Ginny"] == 1)
        model.addConstr(take["Harry"] + take["Fred"] <= 1)
        model.addConstr(take["Harry"] + take["George"] <= 1)
        model.addConstr(take["George"] <= take["Fred"])
        model.addConstr(take["George"] <= take["Hermione"])
        model.setObjective(take.prod(cost), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
