"""IndustryOR problem 059: A symmetric seven-location traveling salesman tour."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_059") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        upper_triangle = [
            [86, 49, 57, 31, 69, 50], [68, 79, 93, 24, 5], [16, 7, 72, 67],
            [90, 69, 1], [86, 59], [81],
        ]
        distance = {}
        for i, row in enumerate(upper_triangle, start=1):
            for j, value in enumerate(row, start=i + 1):
                distance[i, j] = distance[j, i] = value
        locations = range(1, 8)
        stops = range(2, 8)
        visit = model.addVars(distance.keys(), vtype=GRB.BINARY, name="visit")
        rank = model.addVars(stops, lb=1, ub=len(stops), name="rank")
        for i in locations:
            model.addConstr(visit.sum(i, "*") == 1)
            model.addConstr(visit.sum("*", i) == 1)
        for i in stops:
            for j in stops:
                if i != j:
                    model.addConstr(rank[i] + 1 <= rank[j] + len(stops) * (1 - visit[i, j]))
        model.setObjective(visit.prod(distance), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
