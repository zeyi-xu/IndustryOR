"""IndustryOR problem 043: Shipping through capacitated transshipment stations."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_043") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        sites = range(2)
        supply, demand = [100, 150], [80, 120]
        first_cost, second_cost = [[2, 3], [4, 1]], [[3, 2], [1, 4]]
        fixed = dict(enumerate([10, 15]))
        inbound = model.addVars(sites, sites, name="inbound")
        outbound = model.addVars(sites, sites, name="outbound")
        open_station = model.addVars(sites, vtype=GRB.BINARY, name="open_station")
        for i in sites:
            model.addConstr(inbound.sum(i, "*") <= supply[i])
            model.addConstr(outbound.sum("*", i) == demand[i])
            model.addConstr(inbound.sum("*", i) == outbound.sum(i, "*"))
            model.addConstr(outbound.sum(i, "*") <= 100 * open_station[i])
        cost = open_station.prod(fixed) + gp.quicksum(
            first_cost[i][j] * inbound[i, j] + second_cost[i][j] * outbound[i, j]
            for i in sites for j in sites
        )
        model.setObjective(cost, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
