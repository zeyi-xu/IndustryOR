"""Preserve the original command for running the IndustryOR evaluator."""

from eval import main
from eval_utils.objectives import check_problem as check_problem


if __name__ == "__main__":
    raise SystemExit(main())
