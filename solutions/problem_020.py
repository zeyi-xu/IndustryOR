"""IndustryOR problem 020: Dining-table orders from three suppliers."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_020") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        orders_a = model.addVar(vtype=GRB.INTEGER, name="orders_a")
        orders_b = model.addVar(vtype=GRB.INTEGER, name="orders_b")
        orders_c = model.addVar(vtype=GRB.INTEGER, name="orders_c")
        use_a = model.addVar(vtype=GRB.BINARY, name="use_a")
        use_b = model.addVar(vtype=GRB.BINARY, name="use_b")
        tables_a, tables_b, tables_c = 20 * orders_a, 15 * orders_b, 15 * orders_c
        model.addConstr(tables_a + tables_b + tables_c >= 150)
        model.addConstr(tables_a + tables_b + tables_c <= 600)
        model.addConstr(tables_a <= 600 * use_a)
        model.addConstr(tables_b <= 600 * use_b)
        model.addConstr(orders_b >= 2 * use_a)
        model.addConstr(orders_c >= use_b)
        model.setObjective(120 * tables_a + 110 * tables_b + 100 * tables_c, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
