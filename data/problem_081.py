"""IndustryOR problem 081: Shopping-mall tenant mix."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_081") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        area = [250, 350, 800, 400, 500]
        per_store_profit = [
            {1: 9, 2: 8, 3: 7}, {1: 10, 2: 9}, {1: 27, 2: 21, 3: 20},
            {0: 0, 1: 16, 2: 10}, {1: 17, 2: 15, 3: 12},
        ]
        types = range(len(area))
        choices = [(i, n) for i in types for n in per_store_profit[i]]
        choose = model.addVars(choices, vtype=GRB.BINARY, name="choose_store_count")
        model.addConstrs(choose.sum(i, "*") == 1 for i in types)
        model.addConstr(gp.quicksum(n * area[i] * choose[i, n] for i, n in choices) <= 5000)
        model.setObjective(
            0.20 * gp.quicksum(n * per_store_profit[i][n] * choose[i, n] for i, n in choices),
            GRB.MAXIMIZE,
        )

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
