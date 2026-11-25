"""IndustryOR problem 090: Assembly time and minimum product ratio."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_090") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        a = model.addVar(vtype=GRB.INTEGER, name="product_a")
        b = model.addVar(vtype=GRB.INTEGER, name="product_b")
        model.addConstr(12 * a + 25 * b <= 30 * 60)
        model.addConstr(5 * b >= 2 * a)
        model.setObjective(3 * a + 5 * b, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
