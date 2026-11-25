"""IndustryOR problem 060: Production split among four devices with setup costs."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_060") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        devices = range(4)
        setup = dict(enumerate([1000, 920, 800, 700]))
        unit_cost = dict(enumerate([20, 24, 16, 28]))
        capacity = [900, 1000, 1200, 1600]
        active = model.addVars(devices, vtype=GRB.BINARY, name="active")
        units = model.addVars(devices, vtype=GRB.INTEGER, name="units")
        model.addConstr(units.sum() == 2000)
        model.addConstrs(units[i] <= capacity[i] * active[i] for i in devices)
        model.setObjective(active.prod(setup) + units.prod(unit_cost), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
