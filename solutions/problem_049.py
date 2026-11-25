"""IndustryOR problem 049: Six-month purchasing and sales with warehouse capacity."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_049") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        months = range(6)
        buy_price = dict(enumerate([28, 24, 25, 27, 23, 23]))
        sell_price = dict(enumerate([29, 24, 26, 28, 22, 25]))
        buy = model.addVars(months, name="buy")
        sell = model.addVars(months, name="sell")
        stock = model.addVars(months, name="closing_stock")
        previous = 200
        for t in months:
            model.addConstr(previous + buy[t] <= 500)
            model.addConstr(stock[t] == previous + buy[t] - sell[t])
            previous = stock[t]
        # Interpret total revenue as net trading proceeds after purchases.
        model.setObjective(sell.prod(sell_price) - buy.prod(buy_price), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
