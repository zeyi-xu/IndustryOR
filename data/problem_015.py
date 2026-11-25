"""IndustryOR problem 015: Purchasing and repairing tools over ten stages."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_015") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        demand = [3, 5, 2, 4, 6, 5, 4, 3, 2, 1]
        stages = range(len(demand))
        duration = {"slow": 3, "fast": 1}
        repair_cost = {"slow": 1, "fast": 3}
        repair_starts = [
            (method, t)
            for method, delay in duration.items()
            for t in stages
            if t + delay < len(demand)
        ]
        buy = model.addVars(stages, vtype=GRB.INTEGER, name="buy")
        repair = model.addVars(repair_starts, vtype=GRB.INTEGER, name="repair")
        ready = model.addVars(stages, vtype=GRB.INTEGER, name="ready_inventory")
        for t in stages:
            repair_quantity = gp.quicksum(repair.get((method, t), 0) for method in duration)
            model.addConstr(repair_quantity <= demand[t])
            arrivals = gp.quicksum(
                repair.get((method, t - delay), 0) for method, delay in duration.items()
            )
            prev = ready[t - 1] if t else 0
            model.addConstr(ready[t] == prev + buy[t] + arrivals - demand[t])
        total_repair_cost = gp.quicksum(
            repair_cost[m] * repair[m, t] for m, t in repair_starts
        )
        model.setObjective(10 * buy.sum() + total_repair_cost, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
