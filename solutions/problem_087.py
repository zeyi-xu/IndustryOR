"""IndustryOR problem 087: Ending fertilizer inventory after meeting demand."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_087") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        liquid = model.addVar(vtype=GRB.INTEGER, name="liquid_production")
        solid = model.addVar(vtype=GRB.INTEGER, name="solid_production")
        ending_liquid = 30 + liquid - 75
        ending_solid = 90 + solid - 95
        model.addConstr(ending_liquid >= 0)
        model.addConstr(ending_solid >= 0)
        model.addConstr(50 * liquid + 24 * solid <= 40 * 60)
        model.addConstr(30 * liquid + 33 * solid <= 35 * 60)
        model.setObjective(ending_liquid + ending_solid, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
