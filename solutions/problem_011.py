"""IndustryOR problem 011: Motorcycle production goals and weighted idle time."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_011") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        type_a = model.addVar(lb=5, vtype=GRB.INTEGER, name="type_a")
        type_b = model.addVar(vtype=GRB.INTEGER, name="type_b")
        used_hours = [20 * type_a, 5 * type_a + 7 * type_b, 3 * type_a + 6 * type_b]
        capacity = [120, 80, 40]
        hourly_cost = [12, 8, 10]
        for used, available in zip(used_hours, capacity):
            model.addConstr(used <= available)
        cost = gp.quicksum(rate * used for rate, used in zip(hourly_cost, used_hours))
        # The two higher-priority targets are jointly feasible.
        model.addConstr(650 * type_a + 725 * type_b - cost >= 3_000)
        capacity_cost = sum(rate * available for rate, available in zip(hourly_cost, capacity))
        model.setObjective(capacity_cost - cost, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
