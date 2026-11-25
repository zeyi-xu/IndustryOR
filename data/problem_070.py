"""IndustryOR problem 070: Factory-to-location assignment by transportation cost."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_070") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        volume = [[10, 20], [30, 40]]
        unit_cost = [[5, 8], [6, 7]]
        factories, locations = range(2), range(2)
        assign = model.addVars(factories, locations, vtype=GRB.BINARY, name="assign")
        model.addConstrs(assign.sum(i, "*") == 1 for i in factories)
        model.addConstrs(assign.sum("*", j) == 1 for j in locations)
        # Use the factory-to-location data in the table. Each assignment
        # multiplies the volume and rate in its corresponding cells.
        transport_cost = gp.quicksum(
            volume[i][j] * unit_cost[i][j] * assign[i, j]
            for i in factories
            for j in locations
        )
        model.setObjective(transport_cost, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
