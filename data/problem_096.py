"""IndustryOR problem 096: Sulfur blending with a common intermediate tank."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_096") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        tank_ingredients = ["A", "B", "D"]
        products = range(2)
        sulfur_pct = {"A": 3, "B": 1, "D": 1}
        raw_cost = {"A": 6, "B": 16, "D": 15}
        sulfur_limit = [2.5, 1.5]
        # Treat market demand as a sales limit for each optional product.
        demand = [100, 200]
        revenue = dict(enumerate([9, 15]))
        model.Params.NonConvex = 2
        model.Params.MIPGapAbs = 1e-8
        model.Params.FeasibilityTol = 1e-8

        feed = model.addVars(tank_ingredients, ub=sum(demand), name="tank_feed_tons")
        mix = model.addVars(products, ub=dict(enumerate(demand)), name="tank_output_tons")
        direct_c = model.addVars(products, ub=dict(enumerate(demand)), name="direct_c_tons")
        sulfur = model.addVar(lb=1, ub=3, name="tank_sulfur_pct")
        model.addConstr(feed["D"] <= 50)
        model.addConstr(feed.sum() == mix.sum())
        # Both products draw from a blend with the same sulfur fraction.
        model.addConstr(feed.prod(sulfur_pct) == sulfur * mix.sum())
        for j in products:
            tons = mix[j] + direct_c[j]
            model.addConstr(tons <= demand[j])
            model.addConstr(sulfur * mix[j] + 2 * direct_c[j] <= sulfur_limit[j] * tons)
        model.setObjective(
            mix.prod(revenue) + direct_c.prod(revenue) - feed.prod(raw_cost) - 10 * direct_c.sum(),
            GRB.MAXIMIZE,
        )

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
