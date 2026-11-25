"""IndustryOR problem 073: Project scheduling with a machine rental interval."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_073") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        duration = {"A": 4, "B": 3, "C": 5, "D": 2, "E": 10, "F": 10, "G": 1}
        precedence = [
            ("A", "G"), ("A", "D"), ("E", "F"), ("G", "F"), ("D", "C"), ("F", "C"), ("F", "B")
        ]
        start = model.addVars(duration.keys(), name="start_day")
        finish = model.addVar(name="project_finish")
        for before, after in precedence:
            model.addConstr(start[after] >= start[before] + duration[before])
        for activity, days in duration.items():
            model.addConstr(finish >= start[activity] + days)
        rental_days = start["B"] + duration["B"] - start["A"]
        # The daily project charge accrues over the elapsed project duration.
        model.setObjective(1000 * finish + 5000 * rental_days, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
