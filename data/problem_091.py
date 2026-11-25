"""IndustryOR problem 091: School-trip buses and minibuses."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_091") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        buses = model.addVar(ub=10, vtype=GRB.INTEGER, name="buses")
        minibuses = model.addVar(ub=8, vtype=GRB.INTEGER, name="minibuses")
        model.addConstr(buses + minibuses <= 9)
        model.addConstr(50 * buses + 40 * minibuses >= 400)
        model.setObjective(800 * buses + 600 * minibuses, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
