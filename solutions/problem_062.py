"""IndustryOR problem 062: Produce trips by horse, bicycle or handcart."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_062") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        horse = model.addVar(lb=8, vtype=GRB.INTEGER, name="horse_trips")
        bicycle = model.addVar(vtype=GRB.INTEGER, name="bicycle_trips")
        handcart = model.addVar(vtype=GRB.INTEGER, name="handcart_trips")
        choose_bicycle = model.addVar(vtype=GRB.BINARY, name="choose_bicycle")
        model.addConstr((choose_bicycle == 0) >> (bicycle == 0))
        model.addConstr((choose_bicycle == 1) >> (handcart == 0))
        model.addConstr(55 * horse + 30 * bicycle + 40 * handcart >= 1000)
        model.addConstr(80 * horse <= 1000)
        model.setObjective(80 * horse, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
