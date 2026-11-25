"""IndustryOR problem 019: Bright Future Toys product mix."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_019") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        products = ["robots", "cars", "blocks", "dolls"]
        plastic = dict(zip(products, [30, 10, 20, 15]))
        electronics = dict(zip(products, [8, 5, 3, 2]))
        margin = dict(zip(products, [15, 8, 12, 5]))
        amount = model.addVars(products, vtype=GRB.INTEGER, name="quantity")
        make_robots = model.addVar(vtype=GRB.BINARY, name="make_robots")
        make_cars = model.addVar(vtype=GRB.BINARY, name="make_cars")
        model.addConstr(amount.prod(plastic) <= 1200)
        model.addConstr(amount.prod(electronics) <= 800)
        model.addConstr(amount["robots"] <= (1200 // plastic["robots"]) * make_robots)
        model.addConstr(amount["dolls"] <= (1200 // plastic["dolls"]) * (1 - make_robots))
        model.addConstr(amount["cars"] <= (1200 // plastic["cars"]) * make_cars)
        model.addConstr(amount["blocks"] >= make_cars)
        model.addConstr(amount["dolls"] <= amount["cars"])
        model.setObjective(amount.prod(margin), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
