"""IndustryOR problem 023: Low-pollution shipment of manufactured goods."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_023") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        vehicles = ["truck", "van", "motorcycle", "electric"]
        capacity = dict(zip(vehicles, [100, 80, 40, 60]))
        pollution = dict(zip(vehicles, [100, 50, 10, 0]))
        trips = model.addVars(vehicles, vtype=GRB.INTEGER, name="trips")
        choose_van = model.addVar(vtype=GRB.BINARY, name="choose_van")
        model.addConstr((choose_van == 0) >> (trips["van"] == 0))
        model.addConstr((choose_van == 1) >> (trips["electric"] == 0))
        model.addConstr(trips["truck"] >= 10)
        model.addConstr(trips.prod(capacity) >= 1800)
        model.addConstr(trips.prod(pollution) <= 2000)
        model.setObjective(trips.prod(pollution), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
