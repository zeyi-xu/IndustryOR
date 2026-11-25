"""IndustryOR problem 030: Two-stage production with hourly processing rates."""

import gurobipy as gp
from gurobipy import GRB


def solve(prorate_full_load_cost: bool = False) -> float:
    """Maximize profit using the hourly column or prorated full-load costs.

    The two cost columns imply different hourly rates. The default uses the
    rates given explicitly and returns profit in yuan.
    """
    with gp.Model("industryor_030") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        products = range(3)
        stages = [("A1", "A2"), ("B1", "B2", "B3")]
        hours = {
            "A1": {0: 5, 1: 10}, "A2": {0: 7, 1: 9, 2: 12},
            "B1": {0: 6, 1: 8}, "B2": {0: 4, 2: 11}, "B3": {0: 7},
        }
        capacity = dict(zip(hours, [6000, 10_000, 4000, 7000, 4000]))
        # Work in cents to preserve the precision of the stated hourly rates.
        hourly_cost = dict(zip(hours, [5, 3, 6, 11, 5]))
        if prorate_full_load_cost:
            full_load_cost = dict(zip(hours, [300, 321, 250, 783, 200]))
            hourly_cost = {
                machine: 100 * full_load_cost[machine] / capacity[machine]
                for machine in hours
            }
        margin = dict(enumerate([125 - 25, 200 - 35, 280 - 50]))
        processed = model.addVars(
            [(m, p) for m in hours for p in hours[m]], vtype=GRB.INTEGER, name="processed"
        )
        output = model.addVars(products, vtype=GRB.INTEGER, name="output")
        for p in products:
            for stage in stages:
                stage_output = gp.quicksum(processed[m, p] for m in stage if p in hours[m])
                model.addConstr(stage_output == output[p])
        cost = 0
        for m, estimates in hours.items():
            used = gp.quicksum(time * processed[m, p] for p, time in estimates.items())
            model.addConstr(used <= capacity[m])
            cost += hourly_cost[m] * used
        model.setObjective(output.prod(margin) - cost, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal / 100


if __name__ == "__main__":
    print(solve())
