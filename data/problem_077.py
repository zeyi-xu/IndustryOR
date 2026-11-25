"""IndustryOR problem 077: Overtime for meeting the shoe-sales goal."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_077") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        full_time = model.addVar(name="full_time_overtime")
        part_time = model.addVar(name="part_time_overtime")
        regular_sales = 5 * 160 * 5 + 4 * 80 * 2
        model.addConstr(regular_sales + 5 * full_time + 2 * part_time >= 5500)
        model.setObjective(full_time + part_time, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
