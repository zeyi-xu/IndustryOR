"""IndustryOR problem 050: Regular and contract nurse shift costs."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_050") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        requirements = [10, 15, 25, 20, 18, 12]
        periods = range(len(requirements))
        # The statement gives no separate limit on regular nurse availability.
        regular = model.addVars(periods, vtype=GRB.INTEGER, name="regular_nurses")
        contract = model.addVars(periods, vtype=GRB.INTEGER, name="contract_nurses")
        for t in periods:
            previous = (t - 1) % len(requirements)
            covering_nurses = regular[t] + contract[t] + regular[previous] + contract[previous]
            model.addConstr(covering_nurses >= requirements[t])
        model.setObjective(8 * (10 * regular.sum() + 15 * contract.sum()), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
