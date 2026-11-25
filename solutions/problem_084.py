"""IndustryOR problem 084: Machine and craftsman production capacity."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_084") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        x = model.addVar(lb=10, vtype=GRB.INTEGER, name="product_x")
        y = model.addVar(vtype=GRB.INTEGER, name="product_y")
        machine_minutes = 13 * x + 19 * y
        craft_minutes = 20 * x + 29 * y
        model.addConstr(machine_minutes <= 40 * 60)
        model.addConstr(craft_minutes <= 35 * 60)
        processing_cost = (10 * machine_minutes + 2 * craft_minutes) / 60
        model.setObjective(20 * x + 30 * y - processing_cost, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
