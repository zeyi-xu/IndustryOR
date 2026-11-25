"""IndustryOR problem 056: Minimum trim loss for paper rolls."""

from itertools import product

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_056") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        widths = [5, 7, 9]  # decimeters
        requirements = [1000, 3000, 2000]  # linear meters
        stock_widths = [10, 20]
        patterns = []
        for stock in stock_widths:
            choices = [range(stock // width + 1) for width in widths]
            for counts in product(*choices):
                used = sum(width * count for width, count in zip(widths, counts))
                if 0 < used <= stock:
                    patterns.append((stock - used, counts))

        length = model.addVars(range(len(patterns)), name="length_cut")
        for i, required in enumerate(requirements):
            produced_length = gp.quicksum(
                counts[i] * length[k] for k, (_, counts) in enumerate(patterns)
            )
            model.addConstr(produced_length == required)
        trim_area = gp.quicksum(waste * length[k] / 10 for k, (waste, _) in enumerate(patterns))
        model.setObjective(trim_area, GRB.MINIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
