"""IndustryOR problem 055: Quarterly grain trading with cash and storage balances."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_055") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        months = range(3)
        buy_price = [2.85, 3.05, 2.90]
        sell_price = [3.10, 3.25, 2.95]
        buy = model.addVars(months, name="buy")
        sell = model.addVars(months, name="sell")
        stock = model.addVars(months, ub=5000, name="ending_stock")
        cash = model.addVars(months, name="ending_cash")
        initial_cash = 20_000
        previous_stock, previous_cash = 1000, initial_cash
        for t in months:
            # Sell eligible stock before accepting and paying for current deliveries.
            model.addConstr(sell[t] <= previous_stock)
            model.addConstr(stock[t] == previous_stock - sell[t] + buy[t])
            net_cash_flow = sell_price[t] * sell[t] - buy_price[t] * buy[t]
            model.addConstr(cash[t] == previous_cash + net_cash_flow)
            previous_stock, previous_cash = stock[t], cash[t]
        model.addConstr(stock[2] == 2000)
        model.setObjective(cash[2] - initial_cash, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
