"""IndustryOR problem 042: Truck dispatch for three raw materials."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_042") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        from_a = model.addVar(vtype=GRB.INTEGER, name="from_a")
        from_b = model.addVar(vtype=GRB.INTEGER, name="from_b")
        model.addConstr(4 * from_a + 7 * from_b >= 240)
        model.addConstr(2 * from_a + 2 * from_b >= 80)
        model.addConstr(6 * from_a + 2 * from_b >= 120)
        model.setObjective(200 * from_a + 160 * from_b, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
