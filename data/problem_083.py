"""IndustryOR problem 083: Hiring under education and experience requirements."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_083") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        candidates = ["A", "B", "C", "D", "E"]
        salary = dict(zip(candidates, [8100, 20_000, 21_000, 3000, 8000]))
        experience = dict(zip(candidates, [3, 10, 4, 3, 7]))
        hire = model.addVars(candidates, vtype=GRB.BINARY, name="hire")
        model.addConstr(hire.sum() >= 2)
        model.addConstr(hire.sum() <= 3)
        model.addConstr(hire.prod(salary) <= 35_000)
        model.addConstr(hire["B"] + hire["C"] >= 1)
        model.addConstr(hire.prod(experience) >= 12)
        model.addConstr(hire["A"] + hire["E"] <= 1)
        model.setObjective(hire.prod(salary), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
