"""IndustryOR problem 074: Chemical production with byproduct sales and disposal."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_074") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        product_a = model.addVar(name="product_a")
        product_b = model.addVar(name="product_b")
        sold_c = model.addVar(ub=5, name="sold_c")
        discarded_c = model.addVar(name="discarded_c")
        model.addConstr(2 * product_a + 3 * product_b <= 16)
        model.addConstr(3 * product_a + 4 * product_b <= 24)
        model.addConstr(sold_c + discarded_c == 2 * product_b)
        profit = 4 * product_a + 10 * product_b + 3 * sold_c - 2 * discarded_c
        model.setObjective(profit, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
