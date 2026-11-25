"""IndustryOR problem 045: Minimum-wage computer-lab duty roster."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_045") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        students, days = range(6), range(5)
        available = [
            [6, 0, 6, 0, 7], [0, 6, 0, 6, 7], [4, 8, 4, 0, 5],
            [5, 5, 6, 0, 4], [4, 0, 4, 8, 0], [5, 6, 0, 6, 3],
        ]
        wage = [10.0, 10.0, 9.9, 9.8, 10.8, 11.3]
        minimum_hours = [8, 8, 8, 8, 7, 7]
        hours = model.addVars(students, days, name="hours")
        on_duty = model.addVars(students, days, vtype=GRB.BINARY, name="on_duty")
        for i in students:
            model.addConstr(hours.sum(i, "*") >= minimum_hours[i])
            model.addConstr(on_duty.sum(i, "*") <= 2)
            for d in days:
                model.addConstr(hours[i, d] <= available[i][d] * on_duty[i, d])
        for d in days:
            # Daily availability is given in hours, so shifts can be arranged
            # consecutively to cover the open hours once.
            model.addConstr(hours.sum("*", d) == 14)
            model.addConstr(on_duty.sum("*", d) <= 3)
        payroll = gp.quicksum(wage[i] * hours.sum(i, "*") for i in students)
        model.setObjective(payroll, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
