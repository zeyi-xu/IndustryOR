"""IndustryOR problem 036: Microcomputer production with weekly processing goals."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_036") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        model_a = model.addVar(lb=10, vtype=GRB.INTEGER, name="model_a")
        model_b = model.addVar(lb=15, vtype=GRB.INTEGER, name="model_b")
        overtime = model.addVar(name="process_ii_overtime_hours")
        profit = 300 * model_a + 450 * model_b
        model.addConstr(profit >= 10_000)
        model.addConstr(4 * model_a + 6 * model_b == 150, name="process_i_hours")
        model.addConstr(
            3 * model_a + 2 * model_b == 70 + overtime, name="process_ii_hours"
        )
        model.setObjective(profit, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
