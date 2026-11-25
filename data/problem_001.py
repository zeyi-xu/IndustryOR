"""IndustryOR problem 001: Food production and staff training."""

import gurobipy as gp
from gurobipy import GRB


def solve(allow_advance_production: bool = True) -> float:
    """Minimize wages and delay penalties, with free inventory carryover by default.

    Inventory and backlog start and finish at zero. Only the original skilled
    workers serve as trainers or work overtime.
    """
    with gp.Model("industryor_001") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        weeks = range(8)
        training_starts = range(7)
        products = range(2)
        demand = [
            [10_000, 10_000, 12_000, 12_000, 16_000, 16_000, 20_000, 20_000],
            [6_000, 7_200, 8_400, 10_800, 10_800, 12_000, 12_000, 12_000],
        ]
        rates = [10, 6]
        delay_cost = [0.5, 0.6]

        trainees = model.addVars(training_starts, vtype=GRB.INTEGER, name="trainees_start")
        trainers = model.addVars(training_starts, vtype=GRB.INTEGER, name="trainers_start")
        overtime = model.addVars(weeks, vtype=GRB.INTEGER, name="overtime_workers")
        production = model.addVars(products, weeks, name="production_kg")
        # The corrected question permits unlimited carryover at no cost.
        stock_limit = GRB.INFINITY if allow_advance_production else 0
        inventory = model.addVars(products, weeks, ub=stock_limit, name="inventory_kg")
        backlog = model.addVars(products, weeks, name="backlog_kg")
        model.addConstr(trainees.sum() == 50, name="train_50_workers")
        model.addConstrs(
            (trainees[t] <= 3 * trainers[t] for t in training_starts),
            name="trainees_per_trainer",
        )

        wage_cost = 0
        for t in weeks:
            # A cohort trains for two full weeks and then joins regular production.
            in_training = range(max(0, t - 1), min(t + 1, len(training_starts)))
            teaching = gp.quicksum(trainers[k] for k in in_training)
            learning = gp.quicksum(trainees[k] for k in in_training)
            graduates = gp.quicksum(trainees[k] for k in range(max(0, t - 1)))
            model.addConstr(teaching + overtime[t] <= 50, name=f"skilled_workers[{t}]")
            model.addConstr(
                gp.quicksum(production[p, t] / rates[p] for p in products)
                <= 40 * (50 - teaching + graduates) + 20 * overtime[t],
                name=f"production_hours[{t}]",
            )
            wage_cost += 50 * 360 + 180 * overtime[t] + 120 * learning + 240 * graduates
            for p in products:
                prior_stock = inventory[p, t - 1] - backlog[p, t - 1] if t else 0
                model.addConstr(
                    inventory[p, t] - backlog[p, t]
                    == prior_stock + production[p, t] - demand[p][t],
                    name=f"stock_balance[{p},{t}]",
                )
        for p in products:
            model.addConstr(inventory[p, weeks[-1]] == 0, name=f"ending_stock[{p}]")
            model.addConstr(backlog[p, weeks[-1]] == 0, name=f"ending_backlog[{p}]")
        delay_penalties = gp.quicksum(
            delay_cost[p] * backlog[p, t] for p in products for t in weeks
        )
        model.setObjective(
            wage_cost + delay_penalties,
            GRB.MINIMIZE,
        )

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
