"""IndustryOR problem 008: Assignment of four tasks to workers."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_008") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        hours = [[9, 4, 3, 7], [4, 6, 5, 6], [5, 4, 7, 5], [7, 5, 2, 3], [10, 6, 7, 4]]
        workers, tasks = range(5), range(4)
        assign = model.addVars(workers, tasks, vtype=GRB.BINARY, name="assign")
        model.addConstrs(assign.sum(i, "*") <= 1 for i in workers)
        model.addConstrs(assign.sum("*", j) == 1 for j in tasks)
        total_hours = gp.quicksum(
            hours[i][j] * assign[i, j] for i in workers for j in tasks
        )
        model.setObjective(total_hours, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
