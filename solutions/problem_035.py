"""IndustryOR problem 035: Capacitated vehicle routing with delivery time windows."""

from math import dist

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_035") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        coordinates = [
            (40, 50), (45, 68), (45, 70), (42, 66), (42, 68), (42, 65), (40, 69),
            (40, 66), (38, 68), (38, 70), (35, 66), (35, 69), (25, 85), (22, 75),
            (22, 85), (20, 80), (20, 85), (18, 75), (15, 75), (15, 80), (30, 50),
        ]
        demand = [
            0, 10, 30, 10, 10, 10, 20, 20, 20, 10, 10,
            10, 20, 30, 10, 40, 40, 20, 20, 10, 10,
        ]
        windows = [
            (0, 1236), (912, 967), (825, 870), (65, 146), (727, 782), (15, 67),
            (621, 702), (170, 225), (255, 324), (534, 605), (357, 410), (448, 505),
            (652, 721), (30, 92), (567, 620), (384, 429), (475, 528), (99, 148),
            (179, 254), (278, 345), (10, 73),
        ]
        nodes = range(len(coordinates))
        customers = range(1, len(coordinates))
        service = [0] + [90] * len(customers)
        capacity = 200

        # Use Euclidean distance and one minute of travel per distance unit.
        distance = {
            (i, j): dist(coordinates[i], coordinates[j])
            for i in nodes
            for j in nodes
            if i != j
        }
        arcs = [
            (i, j)
            for (i, j), length in distance.items()
            if windows[i][0] + service[i] + length <= windows[j][1]
        ]
        route = model.addVars(arcs, vtype=GRB.BINARY, name="route")
        start = model.addVars(
            customers, lb={i: windows[i][0] for i in customers},
            ub={i: windows[i][1] for i in customers}, name="service_start",
        )
        load = model.addVars(
            customers, lb={i: demand[i] for i in customers}, ub=capacity, name="delivered"
        )
        for i in customers:
            model.addConstr(route.sum(i, "*") == 1)
            model.addConstr(route.sum("*", i) == 1)
        model.addConstr(route.sum(0, "*") <= 5)
        model.addConstr(route.sum(0, "*") == route.sum("*", 0))

        for i, j in arcs:
            elapsed = service[i] + distance[i, j]
            if i == 0:
                model.addConstr((route[i, j] == 1) >> (start[j] >= elapsed))
            elif j == 0:
                model.addConstr((route[i, j] == 1) >> (start[i] + elapsed <= windows[0][1]))
            else:
                model.addConstr((route[i, j] == 1) >> (start[j] >= start[i] + elapsed))
                model.addConstr((route[i, j] == 1) >> (load[j] >= load[i] + demand[j]))
        model.setObjective(route.prod(distance), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        # The published distance is reported to two decimal places.
        return round(model.ObjVal, 2)


if __name__ == "__main__":
    print(solve())
