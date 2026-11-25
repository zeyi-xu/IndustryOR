"""IndustryOR problem 085: Dog-food production with ingredient and packaging costs."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_085") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        meaties = model.addVar(ub=90_000, vtype=GRB.INTEGER, name="meaties")
        yummies = model.addVar(vtype=GRB.INTEGER, name="yummies")
        grains = 2 * meaties + 3 * yummies
        meat = 3 * meaties + 1.5 * yummies
        model.addConstr(grains <= 400_000)
        model.addConstr(meat <= 300_000)
        revenue = 2.80 * meaties + 2.00 * yummies
        cost = 0.20 * grains + 0.50 * meat + 0.25 * meaties + 0.20 * yummies
        model.setObjective(revenue - cost, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
