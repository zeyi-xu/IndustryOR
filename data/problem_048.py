"""IndustryOR problem 048: Warehouse rental contracts spanning several months."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_048") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        demand = [1500, 1000, 2000, 1200]
        rate = {1: 22, 2: 21, 3: 20, 4: 19}
        months = range(len(demand))
        contracts = [
            (start, length)
            for start in months
            for length in rate
            if start + length <= len(demand)
        ]
        area = model.addVars(contracts, name="contract_area")
        for t in months:
            covered_area = gp.quicksum(
                area[start, length]
                for start, length in contracts
                if start <= t < start + length
            )
            model.addConstr(covered_area >= demand[t])
        rent = gp.quicksum(
            length * rate[length] * area[start, length] for start, length in contracts
        )
        model.setObjective(rent, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
