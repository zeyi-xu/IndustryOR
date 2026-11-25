"""IndustryOR problem 022: Clothing production and equipment activation."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_022") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        products = range(3)
        labor = dict(enumerate([3, 2, 6]))
        material = dict(enumerate([4, 3, 6]))
        margin = dict(enumerate([60, 40, 100]))
        fixed = dict(enumerate([2000, 1500, 1000]))
        quantity = model.addVars(products, vtype=GRB.INTEGER, name="quantity")
        active = model.addVars(products, vtype=GRB.BINARY, name="active")
        model.addConstr(quantity.prod(labor) <= 1500)
        model.addConstr(quantity.prod(material) <= 1600)
        for p in products:
            limit = min(1500 // labor[p], 1600 // material[p])
            model.addConstr(quantity[p] <= limit * active[p])
        model.setObjective(quantity.prod(margin) - active.prod(fixed), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
