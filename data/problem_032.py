"""IndustryOR problem 032: Dividing an inheritance into two shares."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_032") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        # The pair of dogs is a single indivisible item.
        values = [
            25_000, 5000, 20_000, 40_000, 12_000, 12_000, 12_000,
            3000, 6000, 10_000, 15_000, 10_000, 13_000,
        ]
        to_first = model.addVars(range(len(values)), vtype=GRB.BINARY, name="to_first")
        difference = model.addVar(name="difference")
        first_share = to_first.prod(dict(enumerate(values)))
        signed_difference = 2 * first_share - sum(values)
        model.addConstr(difference >= signed_difference)
        model.addConstr(difference >= -signed_difference)
        model.setObjective(difference, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
