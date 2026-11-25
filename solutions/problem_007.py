"""IndustryOR problem 007: Container transport from warehouses to ports."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_007") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        supply = [10, 12, 20, 24, 18, 40]
        demand = [20, 15, 25, 33, 21]
        distance = [
            [290, 115, 355, 715, 810],
            [380, 340, 165, 380, 610],
            [505, 530, 285, 220, 450],
            [655, 450, 155, 240, 315],
            [1010, 840, 550, 305, 95],
            [1072, 1097, 747, 372, 333],
        ]
        warehouses, ports = range(len(supply)), range(len(demand))
        containers = model.addVars(warehouses, ports, vtype=GRB.INTEGER, name="containers")
        trips = model.addVars(warehouses, ports, vtype=GRB.INTEGER, name="loaded_truck_trips")
        model.addConstrs(containers.sum(i, "*") <= supply[i] for i in warehouses)
        model.addConstrs(containers.sum("*", j) == demand[j] for j in ports)
        model.addConstrs(
            (containers[i, j] <= 2 * trips[i, j] for i in warehouses for j in ports),
            name="truck_capacity",
        )
        model.addConstrs(
            (trips[i, j] <= containers[i, j] for i in warehouses for j in ports),
            name="nonempty_trip",
        )
        # The quoted cost is per container-kilometer. The fleet size is unspecified.
        model.setObjective(
            30 * gp.quicksum(distance[i][j] * containers[i, j] for i in warehouses for j in ports),
            GRB.MINIMIZE,
        )

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
