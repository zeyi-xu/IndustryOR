"""IndustryOR problem 076: Parts assignment with machine setup and compatibility."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_076") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        parts = range(1, 11)
        machines = ["A", "B", "C"]
        setup = dict(zip(machines, [100, 135, 200]))
        increment = dict(zip(machines, [0, 5, 10]))
        assign = model.addVars(parts, machines, vtype=GRB.BINARY, name="assign")
        active = model.addVars(machines, vtype=GRB.BINARY, name="active")
        model.addConstrs(assign.sum(p, "*") == 1 for p in parts)
        model.addConstrs(assign[p, m] <= active[m] for p in parts for m in machines)
        model.addConstr(assign[1, "A"] + assign[2, "A"] == 1)
        model.addConstr(assign[3, "A"] == 1)
        model.addConstr(assign[4, "B"] == 1)
        model.addConstr(assign[5, "C"] == 1)
        model.addConstr(assign.sum("*", "C") <= 3)
        cost = gp.quicksum((10 * p + increment[m]) * assign[p, m] for p in parts for m in machines)
        model.setObjective(active.prod(setup) + cost, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
