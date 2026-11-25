"""IndustryOR problem 029: Minimum-cost animal feed."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_029") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        feeds = range(5)
        protein = dict(enumerate([3, 2, 1, 6, 18]))
        minerals = dict(enumerate([1, 0.5, 0.2, 2, 0.5]))
        vitamins = dict(enumerate([0.5, 1, 0.2, 2, 0.8]))
        price = dict(enumerate([0.2, 0.7, 0.4, 0.3, 0.8]))
        feed_kg = model.addVars(feeds, name="feed_kg")
        model.addConstr(feed_kg.prod(protein) >= 700)
        model.addConstr(feed_kg.prod(minerals) >= 30)
        model.addConstr(feed_kg.prod(vitamins) >= 100)
        model.setObjective(feed_kg.prod(price), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
