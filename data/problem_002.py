"""IndustryOR problem 002: Fleet and training capacity in a ten-period allocation exercise."""

import gurobipy as gp
from gurobipy import GRB


def solve(count_active_stock: bool = False) -> float:
    """Maximize immediate placements or, optionally, total active unit-years."""
    with gp.Model("industryor_002") as model:
        model.Params.OutputFlag = 0
        model.Params.Threads = 1
        model.Params.MIPGap = 0

        periods = range(10)
        new_units_per_period = 10 + 15
        new_active = model.addVars(periods, vtype=GRB.INTEGER, name="new_active")
        new_training = model.addVars(periods, vtype=GRB.INTEGER, name="new_training")
        transferred = model.addVars(periods, vtype=GRB.INTEGER, name="transferred")
        active = model.addVars(periods, vtype=GRB.INTEGER, name="active")
        training = model.addVars(periods, vtype=GRB.INTEGER, name="training")
        operators = model.addVars(periods, vtype=GRB.INTEGER, name="operators")

        previous_active = previous_training = previous_operators = 0
        for t in periods:
            model.addConstr(
                new_active[t] + new_training[t] == new_units_per_period,
                name=f"delivery_allocation[{t}]",
            )
            model.addConstr(transferred[t] <= previous_training, name=f"training_transfers[{t}]")
            model.addConstr(
                active[t] == previous_active + new_active[t] + transferred[t],
                name=f"active_stock[{t}]",
            )
            model.addConstr(
                training[t] == previous_training + new_training[t] - transferred[t],
                name=f"training_stock[{t}]",
            )
            # Qualifications earned in one year are available the following year.
            model.addConstr(
                operators[t] == previous_operators + 5 * previous_training,
                name=f"operator_stock[{t}]",
            )
            model.addConstr(active[t] <= operators[t], name=f"operator_capacity[{t}]")
            previous_active = active[t]
            previous_training = training[t]
            previous_operators = operators[t]

        # The corrected question counts immediate placements from new deliveries.
        # Active stock is available for auditing the earlier unit-years wording.
        objective = active.sum() if count_active_stock else new_active.sum()
        model.setObjective(objective, GRB.MAXIMIZE)

        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"Gurobi solve failed with status {model.Status}")
        return model.ObjVal


if __name__ == "__main__":
    print(solve())
