"""IndustryOR problem 041: Fuel cost for two steel furnaces."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_041") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        furnaces, methods = range(2), range(2)
        duration = [2, 3]
        fuel = [50, 70]
        runs = model.addVars(furnaces, methods, name="furnace_runs")
        # Furnaces operate in parallel, with each run using one method.
        for f in furnaces:
            model.addConstr(gp.quicksum(duration[m] * runs[f, m] for m in methods) <= 12)
        model.addConstr(10 * runs.sum() >= 30)
        fuel_cost = gp.quicksum(fuel[m] * runs[f, m] for f in furnaces for m in methods)
        model.setObjective(fuel_cost, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
