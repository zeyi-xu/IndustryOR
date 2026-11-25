"""IndustryOR problem 054: Course selection with categories and prerequisites."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_054") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        categories = [
            ["calculus", "or", "data", "statistics", "forecasting"],
            ["or", "statistics", "simulation", "forecasting"],
            ["data", "simulation", "programming"],
        ]
        courses = sorted({course for category in categories for course in category})
        take = model.addVars(courses, vtype=GRB.BINARY, name="take")
        for category in categories:
            model.addConstr(gp.quicksum(take[c] for c in category) >= 2)
        prerequisites = {
            "data": "programming",
            "simulation": "programming",
            "statistics": "calculus",
            "forecasting": "statistics",
        }
        model.addConstrs(take[c] <= take[p] for c, p in prerequisites.items())
        model.setObjective(take.sum(), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
