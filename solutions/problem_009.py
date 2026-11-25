"""IndustryOR problem 009: Haus Toys production mix."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_009") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        products = ["trucks", "airplanes", "boats", "trains"]
        wood = dict(zip(products, [12, 20, 15, 10]))
        steel = dict(zip(products, [6, 3, 5, 4]))
        profit = dict(zip(products, [5, 10, 8, 7]))
        quantity = model.addVars(products, vtype=GRB.INTEGER, name="quantity")
        make_trucks = model.addVar(vtype=GRB.BINARY, name="make_trucks")
        make_boats = model.addVar(vtype=GRB.BINARY, name="make_boats")
        model.addConstr(quantity.prod(wood) <= 890)
        model.addConstr(quantity.prod(steel) <= 500)
        model.addConstr(quantity["trucks"] <= (890 // wood["trucks"]) * make_trucks)
        model.addConstr(quantity["trains"] <= (890 // wood["trains"]) * (1 - make_trucks))
        model.addConstr(quantity["boats"] <= (890 // wood["boats"]) * make_boats)
        model.addConstr(quantity["airplanes"] >= make_boats)
        model.addConstr(quantity["boats"] <= quantity["trains"])
        model.setObjective(quantity.prod(profit), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
