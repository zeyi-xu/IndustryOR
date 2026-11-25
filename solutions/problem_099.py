"""IndustryOR problem 099: Maximum bottleneck bandwidth on a path through node C."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_099") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        nodes = ["A", "B", "C", "D", "E"]
        table = [
            [0, 90, 85, 0, 65], [95, 0, 70, 65, 34], [60, 0, 0, 88, 80],
            [67, 30, 25, 0, 84], [0, 51, 0, 56, 0],
        ]
        capacity = {
            (i, j): table[row][col]
            for row, i in enumerate(nodes) for col, j in enumerate(nodes)
            if table[row][col] > 0 and i != "E" and j != "A"
        }
        use = model.addVars(capacity.keys(), vtype=GRB.BINARY, name="use_arc")
        position = model.addVars(nodes, ub=len(nodes) - 1, name="position")
        bandwidth = model.addVar(ub=max(capacity.values()), name="bandwidth")
        for node in nodes:
            incoming, outgoing = use.sum("*", node), use.sum(node, "*")
            supply = 1 if node == "A" else -1 if node == "E" else 0
            model.addConstr(outgoing - incoming == supply)
            model.addConstr(outgoing <= 1)
        model.addConstr(use.sum("C", "*") == 1)
        model.addConstr(position["A"] == 0)
        for (i, j), limit in capacity.items():
            model.addConstr((use[i, j] == 1) >> (position[j] >= position[i] + 1))
            model.addConstr((use[i, j] == 1) >> (bandwidth <= limit))
        model.setObjective(bandwidth, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
