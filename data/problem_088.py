"""IndustryOR problem 088: Two-product mix with a demand ratio and storage limit."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_088") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        a = model.addVar(vtype=GRB.INTEGER, name="product_a")
        b = model.addVar(vtype=GRB.INTEGER, name="product_b")
        model.addConstr(6 * a + 3 * b <= 40)
        model.addConstr(b >= 3 * a)
        model.addConstr(4 * a + b <= 4 * 4)
        model.setObjective(30 * a + 10 * b, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
