"""IndustryOR problem 086: Truck rentals for refrigerated and dry cargo."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_086") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        type_a = model.addVar(vtype=GRB.INTEGER, name="type_a")
        type_b = model.addVar(vtype=GRB.INTEGER, name="type_b")
        model.addConstr(20 * type_a + 30 * type_b >= 3000)
        model.addConstr(40 * type_a + 30 * type_b >= 4000)
        # Distance is common to both truck types. Cost is reported per kilometer.
        model.setObjective(30 * type_a + 40 * type_b, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
