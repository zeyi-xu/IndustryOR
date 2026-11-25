"""IndustryOR problem 017: Fabric production and overtime goals."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_017") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        curtain = model.addVar(lb=70_000, ub=70_000, name="curtain_meters")
        clothing = model.addVar(lb=45_000, ub=45_000, name="clothing_meters")
        overtime = model.addVar(ub=10, name="overtime_hours")
        # All higher-priority goals can be met simultaneously.
        model.addConstr((curtain + clothing) / 1000 == 110 + overtime)
        model.setObjective(overtime, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
