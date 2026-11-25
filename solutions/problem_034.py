"""IndustryOR problem 034: Makespan for five batches through three dyeing vats."""

from itertools import combinations

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_034") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        # Durations are measured in tenths of an hour.
        duration = [[30, 10, 10], [20, 15, 10], [30, 12, 13], [20, 20, 20], [21, 20, 30]]
        batches, vats = range(5), range(3)
        horizon = sum(map(sum, duration))
        start = model.addVars(batches, vats, ub=horizon, name="start")
        makespan = model.addVar(ub=horizon, name="makespan")
        for i in batches:
            for v in range(2):
                model.addConstr(start[i, v + 1] >= start[i, v] + duration[i][v])
            model.addConstr(makespan >= start[i, 2] + duration[i][2])
        for i, j in combinations(batches, 2):
            for v in vats:
                before = model.addVar(vtype=GRB.BINARY, name=f"before_{i}_{j}_{v}")
                model.addConstr((before == 1) >> (start[j, v] >= start[i, v] + duration[i][v]))
                model.addConstr((before == 0) >> (start[i, v] >= start[j, v] + duration[j][v]))
        model.setObjective(makespan, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal / 10


if __name__ == "__main__":
    print(solve())
