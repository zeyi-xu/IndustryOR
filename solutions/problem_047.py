"""IndustryOR problem 047: Microcomputer production with discounted overtime output."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_047") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        regular_a = model.addVar(vtype=GRB.INTEGER, name="regular_a")
        regular_b = model.addVar(vtype=GRB.INTEGER, name="regular_b")
        overtime_a = model.addVar(vtype=GRB.INTEGER, name="overtime_a")
        overtime_b = model.addVar(vtype=GRB.INTEGER, name="overtime_b")
        total_a, total_b = regular_a + overtime_a, regular_b + overtime_b
        profit = 300 * regular_a + 450 * regular_b + 280 * overtime_a + 425 * overtime_b
        model.addConstr(total_a >= 10)
        model.addConstr(total_b >= 15)
        model.addConstr(profit >= 10_000)
        model.addConstr(4 * total_a + 6 * total_b == 150)
        model.addConstr(3 * regular_a + 2 * regular_b == 70)
        model.addConstr(3 * overtime_a + 2 * overtime_b <= 30)
        model.setObjective(profit, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
