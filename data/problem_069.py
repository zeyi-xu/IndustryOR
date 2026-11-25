"""IndustryOR problem 069: An asymmetric four-city traveling salesman tour."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_069") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        cost = [[0, 10, 20, 12], [10, 0, 5, 10], [20, 5, 0, 8], [15, 12, 8, 0]]
        cities = range(len(cost))
        stops = range(1, len(cost))
        arcs = [(i, j) for i in cities for j in cities if i != j]
        visit = model.addVars(arcs, vtype=GRB.BINARY, name="visit")
        rank = model.addVars(stops, lb=1, ub=len(stops), name="rank")
        for i in cities:
            model.addConstr(visit.sum(i, "*") == 1)
            model.addConstr(visit.sum("*", i) == 1)
        for i in stops:
            for j in stops:
                if i != j:
                    model.addConstr(rank[i] + 1 <= rank[j] + len(stops) * (1 - visit[i, j]))
        model.setObjective(gp.quicksum(cost[i][j] * visit[i, j] for i, j in arcs), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
