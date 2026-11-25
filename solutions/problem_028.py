"""IndustryOR problem 028: Recruiting and assignment across two cities."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_028") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        cities = ["Donghai", "Nanjiang"]
        specialties = [1, 2, 3]
        jobs = [(city, s) for city in cities for s in specialties]
        requirements = dict(zip(jobs, [1000, 2000, 1500, 2000, 1000, 1000]))
        qualified = [(1, 2), (2, 3), (1, 3), (1, 3), (2, 3), (3,)]
        preferred_specialty = [1, 2, 1, 3, 3, 3]
        preferred_city = ["Donghai", "Donghai", "Nanjiang", "Nanjiang", "Donghai", "Nanjiang"]
        assignments = [
            (i, city, s)
            for i, skills in enumerate(qualified)
            for city in cities
            for s in skills
        ]
        hired = model.addVars(assignments, vtype=GRB.INTEGER, name="hired")
        model.addConstrs(hired.sum(i, "*", "*") <= 1500 for i in range(len(qualified)))
        model.addConstrs(
            hired.sum("*", city, s) == demand for (city, s), demand in requirements.items()
        )
        specialty_matches = gp.quicksum(
            hired[i, city, s] for i, city, s in assignments if s == preferred_specialty[i]
        )
        city_matches = gp.quicksum(
            hired[i, city, s] for i, city, s in assignments if city == preferred_city[i]
        )
        model.addConstr(specialty_matches >= 4000)
        model.addConstr(city_matches >= 4000)
        # Use the preferred city as the worker's origin for the move count.
        model.setObjective(hired.sum() - city_matches, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
