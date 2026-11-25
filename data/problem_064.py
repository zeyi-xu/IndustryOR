"""IndustryOR problem 064: Workshop hours for microwave ovens and water heaters."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_064") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        microwaves = model.addVar(lb=80, vtype=GRB.INTEGER, name="microwaves")
        heaters = model.addVar(lb=50, vtype=GRB.INTEGER, name="heaters")
        hours_a = 2 * microwaves + heaters
        hours_b = microwaves + 3 * heaters
        inspection = 30 * microwaves + 50 * heaters
        model.addConstr(inspection <= 5500)
        model.addConstr(hours_a >= 250)
        model.addConstr(hours_a <= 250 + 20)
        model.addConstr(hours_b >= 150)
        model.setObjective(80 * hours_a + 20 * hours_b + inspection, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
