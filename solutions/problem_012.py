"""IndustryOR problem 012: Plastic-container production with substitution."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_012") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        demand = [500, 550, 700, 900, 400, 300]
        unit_cost = [5, 8, 10, 12, 16, 18]
        sizes = range(len(demand))
        arcs = [(i, j) for i in sizes for j in sizes if i >= j]
        supply = model.addVars(arcs, vtype=GRB.INTEGER, name="allocated")
        active = model.addVars(sizes, vtype=GRB.BINARY, name="equipment_active")
        model.addConstrs(supply.sum("*", j) == demand[j] for j in sizes)
        model.addConstrs(supply.sum(i, "*") <= sum(demand[:i + 1]) * active[i] for i in sizes)
        variable_cost = gp.quicksum(unit_cost[i] * supply.sum(i, "*") for i in sizes)
        model.setObjective(1_200 * active.sum() + variable_cost, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
