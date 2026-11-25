"""IndustryOR problem 005: Fiber maximization with food choices."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_005") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        protein = ["salmon", "beef", "pork"]
        vegetables = ["okra", "carrots", "celery", "cabbage"]
        foods = protein + vegetables
        price_per_100g = dict(zip(foods, [4, 3.6, 1.8, 2.6, 1.2, 1.6, 2.3]))
        fiber_per_100g = dict(zip(vegetables, [3.2, 2.7, 1.6, 2]))
        grams = model.addVars(foods, ub=600, name="grams")
        selected = model.addVars(foods, vtype=GRB.BINARY, name="selected")
        for food in foods:
            model.addConstr(grams[food] >= selected[food])
            model.addConstr(grams[food] <= 600 * selected[food])
        model.addConstr(gp.quicksum(selected[food] for food in protein) == 1)
        model.addConstr(gp.quicksum(selected[food] for food in vegetables) >= 2)
        model.addConstr(grams.sum() == 600)
        model.addConstr(grams.prod(price_per_100g) <= 15 * 100)
        model.setObjective(grams.prod(fiber_per_100g) / 100, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
