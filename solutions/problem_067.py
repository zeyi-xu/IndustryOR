"""IndustryOR problem 067: Coal distribution to three residential areas."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_067") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        yard_minimum = [80, 100]
        demand = [55, 75, 50]
        distance = [[10, 5, 6], [4, 8, 15]]
        yards, areas = range(2), range(3)
        tons = model.addVars(yards, areas, name="tons")
        # Assume both yards dispatch their entire monthly receipts. Outbound
        # tonnage then inherits the receiving minimums.
        model.addConstrs(tons.sum(i, "*") >= yard_minimum[i] for i in yards)
        model.addConstrs(tons.sum("*", j) == demand[j] for j in areas)
        ton_kilometers = gp.quicksum(distance[i][j] * tons[i, j] for i in yards for j in areas)
        model.setObjective(ton_kilometers, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
