"""IndustryOR problem 072: Li family trip selection."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_072") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        cost = {"Alice": 1000, "Bob": 900, "Charlie": 600, "Diana": 500, "Ella": 700}
        take = model.addVars(cost.keys(), vtype=GRB.BINARY, name="take")
        model.addConstr(take.sum() >= 2)
        model.addConstr(take.sum() <= 3)
        model.addConstr(take["Bob"] == 1)
        model.addConstr(take["Alice"] + take["Diana"] <= 1)
        model.addConstr(take["Bob"] + take["Charlie"] <= 1)
        model.addConstr(take["Charlie"] <= take["Diana"])
        model.addConstr(take["Diana"] <= take["Ella"])
        model.setObjective(take.prod(cost), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
