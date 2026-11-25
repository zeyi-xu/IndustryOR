"""IndustryOR problem 033: Packing freight into containers."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_033") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        demand = {"A": 120, "B": 90, "C": 300, "D": 90, "E": 120}
        weight = {"A": 50, "B": 100, "C": 40, "D": 60, "E": 65}  # hundredths of a ton
        containers = range(demand["D"] // 12)
        used = model.addVars(containers, vtype=GRB.BINARY, name="used")
        has_a = model.addVars(containers, vtype=GRB.BINARY, name="has_a")
        packed = model.addVars(containers, demand.keys(), vtype=GRB.INTEGER, name="packed")
        model.addConstrs(packed.sum("*", p) == quantity for p, quantity in demand.items())
        for i in containers:
            load = gp.quicksum(weight[p] * packed[i, p] for p in demand)
            model.addConstr(load >= 1800 * used[i])
            model.addConstr(load <= 6000 * used[i])
            model.addConstr(packed[i, "D"] >= 12 * used[i])
            model.addConstr(packed[i, "A"] <= demand["A"] * has_a[i])
            model.addConstr(packed[i, "C"] >= has_a[i])
        model.addConstrs(used[i - 1] >= used[i] for i in containers if i)
        model.setObjective(used.sum(), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
