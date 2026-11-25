"""IndustryOR problem 068: Cutting ten-meter steel bars to length."""

from itertools import product

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_068") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        lengths = [3, 4]
        required = [90, 60]
        stock_length = 10
        choices = [range(stock_length // length + 1) for length in lengths]
        patterns = [
            counts for counts in product(*choices)
            if 0 < sum(count * length for count, length in zip(counts, lengths)) <= stock_length
        ]
        bars = model.addVars(range(len(patterns)), vtype=GRB.INTEGER, name="bars_cut")
        for i, demand in enumerate(required):
            cut_pieces = gp.quicksum(counts[i] * bars[k] for k, counts in enumerate(patterns))
            model.addConstr(cut_pieces == demand)
        model.setObjective(bars.sum(), GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
