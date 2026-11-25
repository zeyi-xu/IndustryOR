"""IndustryOR problem 038: Urban freight using at most two vehicle types."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_038") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        vehicles = ["motorcycle", "small_truck", "large_truck"]
        capacity = dict(zip(vehicles, [10, 20, 50]))
        pollution = dict(zip(vehicles, [40, 70, 100]))
        trip_limit = dict(zip(vehicles, [8, 20, 20]))
        trips = model.addVars(vehicles, vtype=GRB.INTEGER, name="trips")
        used = model.addVars(vehicles, vtype=GRB.BINARY, name="used")
        model.addConstrs(trips[v] <= trip_limit[v] * used[v] for v in vehicles)
        model.addConstrs(trips[v] >= used[v] for v in vehicles)
        # Interpret the choice of two transport methods as an upper limit.
        model.addConstr(used.sum() <= 2)
        model.addConstr(trips.sum() <= 20)
        model.addConstr(trips.prod(capacity) >= 300)
        model.setObjective(trips.prod(pollution), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
