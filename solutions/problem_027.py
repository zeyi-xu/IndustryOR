"""IndustryOR problem 027: Three-year cash flow across four investment projects."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_027") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        annual = model.addVars(range(3), name="annual_project")
        project_2 = model.addVar(ub=150_000, name="project_2")
        project_3 = model.addVar(ub=200_000, name="project_3")
        project_4 = model.addVar(ub=100_000, name="project_4")
        model.addConstr(annual[0] + project_2 == 300_000)
        model.addConstr(annual[1] + project_3 == 1.2 * annual[0])
        model.addConstr(annual[2] + project_4 == 1.2 * annual[1] + 1.5 * project_2)
        model.setObjective(1.2 * annual[2] + 1.6 * project_3 + 1.4 * project_4, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
