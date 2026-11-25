"""Solve an IndustryOR instance and compare its objective with the reference."""

from importlib import import_module
from math import isfinite
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOLERANCE = 1e-6


def check_problem(number: int, expected: float) -> dict:
    module_name = f"problem_{number:03d}"
    result = {
        "problem": f"{number:03d}",
        "file": f"solutions/{module_name}.py",
        "expected": expected,
        "computed": "",
        "absolute_error": "",
        "status": "MISSING",
        "detail": "",
    }
    if not (ROOT / result["file"]).is_file():
        return result

    try:
        computed = float(import_module(f"solutions.{module_name}").solve())
        if not isfinite(computed):
            raise ValueError(f"Non-finite objective {computed}")
    except Exception as exc:
        result.update(status="ERROR", detail=f"{type(exc).__name__}: {exc}")
        return result

    error = abs(computed - expected)
    result.update(
        computed=computed,
        absolute_error=error,
        status="MATCH" if error / (1 + abs(expected)) < TOLERANCE else "MISMATCH",
    )
    return result
