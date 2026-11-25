"""IndustryOR problem 003: Foldable-table production and workforce planning."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_003") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        months = range(6)
        demand = [20_000, 40_000, 42_000, 35_000, 19_000, 18_500]
        workers = model.addVars(months, vtype=GRB.INTEGER, name="workers")
        hired = model.addVars(months, vtype=GRB.INTEGER, name="hired")
        fired = model.addVars(months, vtype=GRB.INTEGER, name="fired")
        production = model.addVars(months, vtype=GRB.INTEGER, name="production")
        outsource = model.addVars(months, vtype=GRB.INTEGER, name="outsource")
        inventory = model.addVars(months, vtype=GRB.INTEGER, name="inventory")
        backlog = model.addVars(months, vtype=GRB.INTEGER, name="backlog")
        overtime = model.addVars(months, name="overtime_hours")

        previous_workers = 1_000
        previous_net_inventory = 15_000
        for t in months:
            model.addConstr(workers[t] == previous_workers + hired[t] - fired[t])
            model.addConstr(
                inventory[t] - backlog[t]
                == previous_net_inventory + production[t] + outsource[t] - demand[t]
            )
            model.addConstr(5 * production[t] <= 160 * workers[t] + overtime[t])
            model.addConstr(overtime[t] <= 20 * workers[t])
            previous_workers = workers[t]
            previous_net_inventory = inventory[t] - backlog[t]

        model.addConstr(inventory[5] >= 10_000)
        model.addConstr(backlog[5] == 0)
        cost = (
            160 * 30 * workers.sum() + 5_000 * hired.sum() + 8_000 * fired.sum()
            + 90 * production.sum() + 200 * outsource.sum() + 15 * inventory.sum()
            + 35 * backlog.sum() + 40 * overtime.sum()
        )
        # Zero ending backlog means every order in the horizon earns revenue.
        model.setObjective(300 * sum(demand) - cost, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
