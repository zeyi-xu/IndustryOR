"""IndustryOR problem 094: Four-week beverage production and stock."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_094") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        weeks = range(4)
        demand = [15, 25, 35, 25]
        capacity = dict(enumerate([30, 40, 45, 20]))
        unit_cost = dict(enumerate([5.0, 5.1, 5.4, 5.5]))
        production = model.addVars(weeks, ub=capacity, name="production")
        stock = model.addVars(weeks, name="ending_stock")
        previous = 0
        for t in weeks:
            model.addConstr(stock[t] == previous + production[t] - demand[t])
            previous = stock[t]
        model.setObjective(production.prod(unit_cost) + 0.2 * stock.sum(), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
