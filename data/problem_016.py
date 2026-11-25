"""IndustryOR problem 016: Quarterly purchasing, sales and warehouse capacity."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_016") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        months = range(3)
        buy_price = dict(enumerate([8, 6, 9]))
        sell_price = dict(enumerate([9, 8, 10]))
        buy = model.addVars(months, name="buy")
        sell = model.addVars(months, name="sell")
        inventory = model.addVars(months, name="inventory_end")
        previous = 200
        for t in months:
            model.addConstr(previous + buy[t] <= 500)
            model.addConstr(inventory[t] == previous + buy[t] - sell[t])
            previous = inventory[t]
        model.setObjective(sell.prod(sell_price) - buy.prod(buy_price), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
