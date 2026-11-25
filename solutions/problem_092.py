"""IndustryOR problem 092: Milk allocation between two dairy products."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_092") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        for_a = model.addVar(name="barrels_for_a1")
        for_b = model.addVar(name="barrels_for_a2")
        kg_a, kg_b = 3 * for_a, 4 * for_b
        model.addConstr(for_a + for_b <= 50)
        model.addConstr(12 * for_a + 8 * for_b <= 480)
        model.addConstr(kg_a <= 100)
        model.setObjective(24 * kg_a + 16 * kg_b, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
