"""IndustryOR problem 051: Eight-hour bus crew shifts."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_051") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        requirements = [60, 70, 60, 50, 20, 30]
        periods = range(len(requirements))
        start = model.addVars(periods, vtype=GRB.INTEGER, name="crew_starting")
        model.addConstrs(
            start[t] + start[(t - 1) % len(requirements)] >= requirements[t] for t in periods
        )
        model.setObjective(start.sum(), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
