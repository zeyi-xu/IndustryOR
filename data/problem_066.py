"""IndustryOR problem 066: Seasonal production with rented warehouse overflow."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_066") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        products, months = range(2), range(6)
        demand = [
            [30_000, 30_000, 30_000, 100_000, 100_000, 100_000],
            [15_000, 15_000, 15_000, 50_000, 50_000, 50_000],
        ]
        production_cost = [4.50, 7.00]
        volume = [0.2, 0.4]
        production = model.addVars(products, months, vtype=GRB.INTEGER, name="production")
        stock = model.addVars(products, months, vtype=GRB.INTEGER, name="stock")
        own_storage = model.addVars(months, ub=15_000, name="own_cubic_meters")
        rented_storage = model.addVars(months, name="rented_cubic_meters")
        for t in months:
            model.addConstr(production.sum("*", t) <= 120_000)
            for p in products:
                previous = stock[p, t - 1] if t else 0
                model.addConstr(stock[p, t] == previous + production[p, t] - demand[p][t])
            stored_volume = gp.quicksum(volume[p] * stock[p, t] for p in products)
            model.addConstr(own_storage[t] + rented_storage[t] == stored_volume)
        cost = gp.quicksum(production_cost[p] * production.sum(p, "*") for p in products)
        model.setObjective(cost + own_storage.sum() + 1.5 * rented_storage.sum(), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
