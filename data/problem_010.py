"""IndustryOR problem 010: Supermarket site coverage."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_010") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        coverage = {
            "A": "ACEGHI", "B": "BHI", "C": "ACGHI", "D": "DJ",
            "E": "AEG", "F": "FJK", "G": "ACEG", "H": "ABCHI",
            "I": "ABCHI", "J": "DFJKL", "K": "FJKL", "L": "JKL",
        }
        open_store = model.addVars(coverage.keys(), vtype=GRB.BINARY, name="open_store")
        for area in coverage:
            covering_sites = [site for site, covered in coverage.items() if area in covered]
            model.addConstr(gp.quicksum(open_store[site] for site in covering_sites) >= 1)
        model.setObjective(open_store.sum(), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
