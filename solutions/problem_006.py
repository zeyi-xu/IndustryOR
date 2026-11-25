"""IndustryOR problem 006: Quarterly production with inventory and backorders."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_006") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        products, quarters = range(3), range(4)
        demand = [[1500, 1000, 2000, 1200], [1500, 1500, 1200, 1500], [1000, 2000, 1500, 2500]]
        hours = [2, 4, 3]
        delay_cost = [20, 20, 10]
        production = model.addVars(products, quarters, vtype=GRB.INTEGER, name="production")
        inventory = model.addVars(products, quarters, vtype=GRB.INTEGER, name="inventory")
        backlog = model.addVars(products, quarters, vtype=GRB.INTEGER, name="backlog")
        model.addConstr(production[0, 1] == 0)
        for t in quarters:
            model.addConstr(gp.quicksum(hours[p] * production[p, t] for p in products) <= 15_000)
            for p in products:
                prev = inventory[p, t - 1] - backlog[p, t - 1] if t else 0
                model.addConstr(
                    inventory[p, t] - backlog[p, t] == prev + production[p, t] - demand[p][t]
                )
        for p in products:
            model.addConstr(inventory[p, 3] == 150)
            model.addConstr(backlog[p, 3] == 0)
        delay_penalties = gp.quicksum(
            delay_cost[p] * backlog[p, t] for p in products for t in quarters
        )
        model.setObjective(5 * inventory.sum() + delay_penalties, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
