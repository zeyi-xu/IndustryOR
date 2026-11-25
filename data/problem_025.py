"""IndustryOR problem 025: Staffing eight-hour convenience-store shifts."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_025") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        requirements = [10, 15, 25, 20, 18, 12]
        periods = range(len(requirements))
        start = model.addVars(periods, vtype=GRB.INTEGER, name="staff_starting")
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
