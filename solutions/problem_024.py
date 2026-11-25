"""IndustryOR problem 024: Allocation across one-year and two-year investments."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_024") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        one_year = model.addVars(range(3), name="one_year_investment")
        two_year = model.addVars(range(2), name="two_year_investment")
        # Each quoted gain is paid in addition to the invested principal.
        model.addConstr(one_year[0] + two_year[0] == 100_000)
        model.addConstr(one_year[1] + two_year[1] == 1.7 * one_year[0])
        model.addConstr(one_year[2] == 1.7 * one_year[1] + 3 * two_year[0])
        model.setObjective(1.7 * one_year[2] + 3 * two_year[1], GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
