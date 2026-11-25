"""IndustryOR problem 097: Production with material limits and paid overtime."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_097") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        a = model.addVar(vtype=GRB.INTEGER, name="product_a")
        b = model.addVar(vtype=GRB.INTEGER, name="product_b")
        overtime = model.addVar(name="overtime")
        model.addConstr(6 * a + 12 * b <= 200)
        model.addConstr(8 * a + 20 * b <= 300)
        model.addConstr(11 * a + 24 * b <= 300 + overtime)
        model.setObjective(5000 * a + 11_000 * b - 100 * overtime, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
