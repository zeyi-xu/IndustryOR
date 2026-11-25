"""IndustryOR problem 082: Eight-hour restaurant waiter shifts."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_082") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        demand = [4, 8, 10, 7, 12, 4]
        periods = range(len(demand))
        staff = model.addVars(periods, vtype=GRB.INTEGER, name="starts")
        model.addConstrs(staff[t] + staff[(t - 1) % len(demand)] >= demand[t] for t in periods)
        model.setObjective(staff.sum(), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
