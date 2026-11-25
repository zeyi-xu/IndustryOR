"""IndustryOR problem 080: Minimum street length occupied on two sides."""

import gurobipy as gp
from gurobipy import GRB


def solve(left_limit_meters: float | None = None) -> float:
    with gp.Model("industryor_080") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        lengths = [40, 45, 50, 41, 24, 52, 37, 35, 32, 45, 23, 33, 38, 46, 30]  # decimeters
        cars = range(len(lengths))
        on_left = model.addVars(cars, vtype=GRB.BINARY, name="on_left")
        footprint = model.addVar(name="footprint")
        left = on_left.prod(dict(enumerate(lengths)))
        right = sum(lengths) - left
        model.addConstr(footprint >= left)
        model.addConstr(footprint >= right)
        if left_limit_meters is not None:
            model.addConstr(left <= 10 * left_limit_meters)
        model.setObjective(footprint, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal / 10


if __name__ == "__main__":
    print(solve())
