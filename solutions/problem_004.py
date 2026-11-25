"""IndustryOR problem 004: Farm animal allocation."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_004") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        cows = model.addVar(lb=10, vtype=GRB.INTEGER, name="cows")
        sheep = model.addVar(lb=20, vtype=GRB.INTEGER, name="sheep")
        chickens = model.addVar(ub=50, vtype=GRB.INTEGER, name="chickens")
        model.addConstr(10 * cows + 5 * sheep + 3 * chickens <= 800, name="manure")
        model.addConstr(cows + sheep + chickens <= 100, name="farm_size")
        model.setObjective(400 * cows + 120 * sheep + 3 * chickens, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
