"""IndustryOR problem 078: Furniture mix under storage and item limits."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_078") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        tables = model.addVar(lb=10, vtype=GRB.INTEGER, name="tables")
        chairs = model.addVar(vtype=GRB.INTEGER, name="chairs")
        bookshelves = model.addVar(lb=20, vtype=GRB.INTEGER, name="bookshelves")
        model.addConstr(5 * tables + 2 * chairs + 3 * bookshelves <= 500)
        model.addConstr(tables + chairs + bookshelves <= 200)
        model.setObjective(80 * tables + 30 * chairs + 60 * bookshelves, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
