"""IndustryOR problem 065: Tabletop golf toy production mix."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_065") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        toys = ["high", "mid", "low"]
        demand = dict(zip(toys, [50, 80, 150]))
        labor = dict(zip(toys, [17, 10, 2]))
        inspection = dict(zip(toys, [8, 4, 2]))
        profit = dict(zip(toys, [300, 200, 100]))
        quantity = model.addVars(toys, ub=demand, vtype=GRB.INTEGER, name="quantity")
        model.addConstr(quantity.prod(labor) <= 1000)
        model.addConstr(quantity.prod(inspection) <= 500)
        model.setObjective(quantity.prod(profit), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
