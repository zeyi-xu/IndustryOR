"""IndustryOR problem 079: Hiring workers to staff alternative crews."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_079") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        # Each crew composition lists skilled workers and laborers.
        composition = {
            (0, 0): (1, 0), (0, 1): (1, 2),
            (1, 0): (1, 0), (1, 1): (0, 1),
            (2, 0): (0, 5), (2, 1): (1, 3),
        }
        # Requirements measure the combined effective person-hours of crew members.
        required_person_hours = [8400, 10_800, 18_000]
        skilled = model.addVar(ub=400, vtype=GRB.INTEGER, name="skilled")
        laborers = model.addVar(ub=800, vtype=GRB.INTEGER, name="laborers")
        hours = model.addVars(composition.keys(), name="crew_hours")
        for task, required in enumerate(required_person_hours):
            effective_work = gp.quicksum(
                sum(crew) * hours[k] for k, crew in composition.items() if k[0] == task
            )
            model.addConstr(effective_work >= required)
        skilled_hours = gp.quicksum(crew[0] * hours[k] for k, crew in composition.items())
        laborer_hours = gp.quicksum(crew[1] * hours[k] for k, crew in composition.items())
        model.addConstr(skilled_hours <= 42 * skilled)
        model.addConstr(laborer_hours <= 36 * laborers)
        model.setObjective(100 * skilled + 80 * laborers, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
