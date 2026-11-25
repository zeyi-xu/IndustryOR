"""IndustryOR problem 018: Chair orders from three manufacturers."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_018") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        orders_a = model.addVar(vtype=GRB.INTEGER, name="orders_a")
        orders_b = model.addVar(vtype=GRB.INTEGER, name="orders_b")
        orders_c = model.addVar(vtype=GRB.INTEGER, name="orders_c")
        use_a = model.addVar(vtype=GRB.BINARY, name="use_a")
        use_b = model.addVar(vtype=GRB.BINARY, name="use_b")
        chairs_a, chairs_b, chairs_c = 15 * orders_a, 10 * orders_b, 10 * orders_c
        model.addConstr(chairs_a + chairs_b + chairs_c >= 100)
        model.addConstr(chairs_a + chairs_b + chairs_c <= 500)
        model.addConstr(chairs_a <= 500 * use_a)
        model.addConstr(chairs_b <= 500 * use_b)
        model.addConstr(orders_b >= use_a)
        model.addConstr(orders_c >= use_b)
        model.setObjective(50 * chairs_a + 45 * chairs_b + 40 * chairs_c, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
