"""IndustryOR problem 037: Three-product permutation flow shop."""

from itertools import combinations

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_037") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        duration = [[2, 3, 1], [4, 2, 3], [3, 5, 2]]
        products, machines = range(3), range(3)
        horizon = sum(map(sum, duration))
        start = model.addVars(products, machines, ub=horizon, name="start")
        makespan = model.addVar(ub=horizon, name="makespan")
        for i in products:
            for m in range(2):
                model.addConstr(start[i, m + 1] >= start[i, m] + duration[i][m])
            model.addConstr(makespan >= start[i, 2] + duration[i][2])
        for i, j in combinations(products, 2):
            before = model.addVar(vtype=GRB.BINARY, name=f"before_{i}_{j}")
            for m in machines:
                model.addConstr((before == 1) >> (start[j, m] >= start[i, m] + duration[i][m]))
                model.addConstr((before == 0) >> (start[i, m] >= start[j, m] + duration[j][m]))
        model.setObjective(makespan, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
