"""IndustryOR problem 014: Protein maximization with vegetable packs."""

import gurobipy as gp
from gurobipy import GRB


def solve() -> float:
    with gp.Model("industryor_014") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        proteins = ["chicken", "salmon", "tofu"]
        vegetables = ["broccoli", "carrots", "spinach", "pepper", "mushrooms"]
        foods = proteins + vegetables
        protein = dict(zip(foods, [23, 20, 8, 2.8, 0.9, 2.9, 1, 3.1]))
        cost = dict(zip(foods, [3, 5, 1.5, 1.2, 0.8, 1.5, 1, 2]))
        servings = model.addVars(proteins, name="protein_100g")
        packs = model.addVars(vegetables, vtype=GRB.INTEGER, name="vegetable_packs")
        chosen = model.addVars(vegetables, vtype=GRB.BINARY, name="vegetable_chosen")
        model.addConstrs(packs[v] >= chosen[v] for v in vegetables)
        model.addConstrs(packs[v] <= 8 * chosen[v] for v in vegetables)
        model.addConstr(chosen.sum() >= 3)
        model.addConstr(servings.sum() + packs.sum() <= 8)
        model.addConstr(servings.prod(cost) + packs.prod(cost) <= 20)
        model.setObjective(servings.prod(protein) + packs.prod(protein), GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
