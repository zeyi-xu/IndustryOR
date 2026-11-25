"""IndustryOR problem 095: Steel-pipe cutting with frequency-ranked surcharges."""

from itertools import product

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_095") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        sizes = [290, 315, 350, 455]
        demand = [15, 28, 21, 30]
        stock = 1850
        max_pieces = 5
        patterns = []
        for counts in product(range(max_pieces + 1), repeat=len(sizes)):
            length = sum(size * count for size, count in zip(sizes, counts))
            if sum(counts) <= max_pieces and stock - 100 <= length <= stock:
                patterns.append(counts)

        ranks = range(1, 5)
        indices = range(len(patterns))
        at_rank = model.addVars(indices, ranks, vtype=GRB.BINARY, name="at_rank")
        pipes = model.addVars(indices, ranks, vtype=GRB.INTEGER, name="pipes")
        # An optimum never needs more pipes than pieces demanded.
        max_pipes = sum(demand)
        model.addConstrs(at_rank.sum(p, "*") <= 1 for p in indices)
        model.addConstrs(at_rank.sum("*", r) <= 1 for r in ranks)
        model.addConstrs(pipes[p, r] <= max_pipes * at_rank[p, r] for p in indices for r in ranks)
        model.addConstrs(pipes[p, r] >= at_rank[p, r] for p in indices for r in ranks)
        model.addConstrs(pipes.sum("*", r) >= pipes.sum("*", r + 1) for r in range(1, 4))
        for i, required in enumerate(demand):
            cut_pieces = gp.quicksum(patterns[p][i] * pipes.sum(p, "*") for p in indices)
            model.addConstr(cut_pieces >= required)
        # A rank-r pattern costs 1 + r/10 raw-pipe prices per pipe cut.
        model.setObjective(
            gp.quicksum((10 + r) * pipes.sum("*", r) for r in ranks), GRB.MINIMIZE
        )

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal / 10


if __name__ == "__main__":
    print(solve())
