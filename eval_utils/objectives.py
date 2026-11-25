"""Solve an IndustryOR instance and compare its objective with the reference."""

from importlib import import_module
from math import isfinite
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOLERANCE = 1e-6


def check_problem(number: int, expected: float, model_file: str | None = None) -> dict:
    filename = f"problem_{number:03d}.py" if model_file is None else model_file
    path = Path(filename)
    result = {
        "problem": f"{number:03d}",
        "file": f"data/{filename}",
        "expected": expected,
        "computed": "",
        "absolute_error": "",
        "status": "MISSING",
        "detail": "",
    }
    if path.name != filename or path.suffix != ".py" or not path.stem.isidentifier():
        result.update(status="ERROR", detail=f"Invalid Python model filename {filename!r}")
        return result
    if not (ROOT / result["file"]).is_file():
        return result

    try:
        computed = float(import_module(f"data.{path.stem}").solve())
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
