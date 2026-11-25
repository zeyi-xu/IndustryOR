"""IndustryOR problem 063: Hiring a research and development team."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_063") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        candidates = ["F", "G", "H", "I", "J"]
        salary = dict(zip(candidates, [12_000, 15_000, 18_000, 5000, 10_000]))
        skill = dict(zip(candidates, [2, 3, 4, 1, 2]))
        experience = dict(zip(candidates, [1, 2, 2, 5, 4]))
        hire = model.addVars(candidates, vtype=GRB.BINARY, name="hire")
        model.addConstr(hire.prod(salary) <= 40_000)
        model.addConstr(hire.sum() <= 4)
        model.addConstr(hire.prod(skill) >= 8)
        model.addConstr(hire.prod(experience) >= 8)
        model.addConstr(hire["G"] + hire["J"] <= 1)
        model.setObjective(hire.prod(salary), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
