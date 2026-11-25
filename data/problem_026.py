"""IndustryOR problem 026: Two-stage production with alternative equipment."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_026") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        products = range(3)
        machines_a = ["A1", "A2"]
        machines_b = ["B1", "B2", "B3"]
        hours = {
            "A1": {0: 5, 1: 10}, "A2": {0: 7, 1: 9, 2: 12},
            "B1": {0: 6, 1: 8}, "B2": {0: 4, 2: 11}, "B3": {0: 7},
        }
        capacity = dict(zip(hours, [6000, 10_000, 4000, 7000, 4000]))
        full_cost = dict(zip(hours, [300, 321, 250, 783, 200]))
        margin = dict(enumerate([1.25 - 0.25, 2.00 - 0.35, 2.80 - 0.50]))
        processed = model.addVars(
            [(m, p) for m in hours for p in hours[m]], vtype=GRB.INTEGER, name="processed"
        )
        output = model.addVars(products, vtype=GRB.INTEGER, name="output")
        for p in products:
            for stage in (machines_a, machines_b):
                stage_output = gp.quicksum(processed[m, p] for m in stage if p in hours[m])
                model.addConstr(stage_output == output[p])
        operating_cost = 0
        for m, estimates in hours.items():
            used = gp.quicksum(time * processed[m, p] for p, time in estimates.items())
            model.addConstr(used <= capacity[m])
            # Prorate the full-capacity operating cost by the hours used.
            operating_cost += full_cost[m] / capacity[m] * used
        model.setObjective(output.prod(margin) - operating_cost, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
