"""IndustryOR problem 075: Timber purchases, sales and storage by quarter."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_075") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        quarters = range(4)
        # Use cubic meters for pricing, consistent with sales and storage volumes.
        purchase = [410, 430, 460, 450]
        sale = [425, 440, 465, 455]
        max_sales = [100, 140, 200, 160]
        pairs = [(i, j) for i in quarters for j in quarters if i <= j]
        volume = model.addVars(pairs, name="ten_thousand_cubic_meters")
        for t in quarters:
            model.addConstr(volume.sum("*", t) <= max_sales[t])
            # In-quarter sales can ship directly. Only carryover uses warehouse capacity.
            model.addConstr(gp.quicksum(volume[i, j] for i, j in pairs if i <= t < j) <= 20)
        profit = {}
        for i, j in pairs:
            storage_cost = 70 + 100 * (j - i) if i < j else 0
            profit[i, j] = sale[j] - purchase[i] - storage_cost
        model.setObjective(volume.prod(profit), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
