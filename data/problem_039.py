"""IndustryOR problem 039: Carelland's net export value."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_039") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        goods = ["steel", "engines", "electronics", "plastic"]
        prices = dict(zip(goods, [500, 1500, 300, 1200]))
        labor_months = dict(zip(goods, [6, 12, 6, 24]))
        external_cost = dict(zip(goods, [250, 300, 50, 300]))
        inputs = {
            "steel": {"engines": 0.02, "plastic": 0.01},
            "engines": {"steel": 0.8, "electronics": 0.15, "plastic": 0.11},
            "electronics": {"steel": 0.01, "engines": 0.01, "plastic": 0.05},
            "plastic": {"steel": 0.2, "engines": 0.03, "electronics": 0.05},
        }
        produced = model.addVars(goods, name="produced")
        exported = model.addVars(goods, name="exported")
        # Domestic production covers intermediate use of the four named exports.
        # The separate imported inputs are charged in the objective.
        for good in goods:
            internal_use = gp.quicksum(inputs[p].get(good, 0) * produced[p] for p in goods)
            model.addConstr(exported[good] == produced[good] - internal_use)
        model.addConstr(produced["engines"] <= 650_000)
        model.addConstr(produced["plastic"] <= 60_000)
        model.addConstr(produced.prod(labor_months) <= 830_000)
        model.setObjective(exported.prod(prices) - produced.prod(external_cost), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
