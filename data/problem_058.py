"""IndustryOR problem 058: Candy blending with ingredient percentages."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_058") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        ingredients, grades = range(3), range(3)
        supply = [2000, 2500, 1200]
        unit_cost = [2, 1.5, 1]
        selling_price = [3.40, 2.85, 2.25]
        processing_fee = [0.50, 0.40, 0.30]
        mix = model.addVars(ingredients, grades, name="ingredient_kg")
        model.addConstrs(mix.sum(i, "*") <= supply[i] for i in ingredients)

        # The comparison signs come from Table 2-16 in the publisher's solution guide.
        # https://www.tup.com.cn/upload/books/yz/098013-01.pdf
        model.addConstr(mix[0, 0] >= 0.60 * mix.sum("*", 0))
        model.addConstr(mix[0, 1] >= 0.15 * mix.sum("*", 1))
        for j, cap in enumerate([0.20, 0.60, 0.50]):
            model.addConstr(mix[2, j] <= cap * mix.sum("*", j))
        profit = gp.quicksum(
            (selling_price[j] - processing_fee[j] - unit_cost[i]) * mix[i, j]
            for i in ingredients for j in grades
        )
        model.setObjective(profit, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
