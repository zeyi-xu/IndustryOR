"""IndustryOR problem 089: Revenue from two clothing bundles."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_089") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        package_a = model.addVar(lb=20, vtype=GRB.INTEGER, name="package_a")
        package_b = model.addVar(lb=10, vtype=GRB.INTEGER, name="package_b")
        model.addConstr(package_a + 3 * package_b == 200, name="clear_shirt_stock")
        model.addConstr(2 * package_a + package_b == 100, name="clear_pants_stock")
        model.setObjective(30 * package_a + 50 * package_b, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
