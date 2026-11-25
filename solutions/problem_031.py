"""IndustryOR problem 031: Workshop hours for three-component assemblies."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_031") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        capacity = [100, 150, 80, 200]
        rate = [[10, 15, 5], [15, 10, 5], [20, 5, 10], [10, 15, 20]]
        workshops, components = range(4), range(3)
        pieces = model.addVars(workshops, components, vtype=GRB.INTEGER, name="components")
        assemblies = model.addVar(vtype=GRB.INTEGER, name="assemblies")
        for i in workshops:
            hours_used = gp.quicksum(pieces[i, j] / rate[i][j] for j in components)
            model.addConstr(hours_used <= capacity[i])
        for j in components:
            model.addConstr(pieces.sum("*", j) >= assemblies)
        model.setObjective(assemblies, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
