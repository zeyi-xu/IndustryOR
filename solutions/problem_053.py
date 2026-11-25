"""IndustryOR problem 053: Product mix across three machines."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_053") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        products = range(3)
        usage = [[8, 2, 10], [10, 5, 8], [2, 13, 10]]
        hours = [300, 400, 420]
        unit_profit = dict(enumerate([3, 2, 2.9]))
        quantity = model.addVars(products, vtype=GRB.INTEGER, name="quantity")
        # Available machine hours are capacity limits for the integer product mix.
        for time, available in zip(usage, hours):
            model.addConstr(quantity.prod(dict(enumerate(time))) <= available)
        model.setObjective(quantity.prod(unit_profit), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
