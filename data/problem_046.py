"""IndustryOR problem 046: Farm land, livestock and outside labor."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_046") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        crops = ["soybeans", "corn", "wheat"]
        autumn_labor = dict(zip(crops, [20, 35, 10]))
        spring_labor = dict(zip(crops, [50, 75, 40]))
        crop_profit = dict(zip(crops, [175, 300, 120]))
        hectares = model.addVars(crops, name="hectares")
        cows = model.addVar(ub=32, vtype=GRB.INTEGER, name="cows")
        chickens = model.addVar(ub=3000, vtype=GRB.INTEGER, name="chickens")
        outside_autumn = model.addVar(vtype=GRB.INTEGER, name="outside_autumn_days")
        outside_spring = model.addVar(vtype=GRB.INTEGER, name="outside_spring_days")
        model.addConstr(hectares.sum() + 1.5 * cows <= 100)
        model.addConstr(400 * cows + 3 * chickens <= 15_000)
        model.addConstr(
            hectares.prod(autumn_labor) + 100 * cows + 0.6 * chickens + outside_autumn <= 3500
        )
        model.addConstr(
            hectares.prod(spring_labor) + 50 * cows + 0.3 * chickens + outside_spring <= 4000
        )
        outside_income = 1.8 * outside_autumn + 2.1 * outside_spring
        income = hectares.prod(crop_profit) + 400 * cows + 2 * chickens + outside_income
        model.setObjective(income, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
