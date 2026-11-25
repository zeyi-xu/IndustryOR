"""Compare Gurobi objective values with the cleaned IndustryOR CSV."""

import argparse
import csv
from importlib import import_module
from math import isfinite
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "optimind_cleaned_classified_industryor.csv"
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "problems", metavar="ID", nargs="*", type=int, help="One-based CSV row numbers"
    )
    parser.add_argument("--report", type=Path, help="Save the results as a CSV")
    args = parser.parse_args()

    with DATA.open(encoding="utf-8", newline="") as file:
        expected = [float(row["answer"]) for row in csv.DictReader(file)]
    problems = args.problems or range(1, len(expected) + 1)
    if any(not 1 <= number <= len(expected) for number in problems):
        parser.error(f"Problem IDs must be between 1 and {len(expected)}")

    results = []
    for number in problems:
        result = check_problem(number, expected[number - 1])
        results.append(result)
        print(
            f"{result['problem']} {result['status']:8} "
            f"expected={result['expected']!s} computed={result['computed']!s} {result['detail']}",
            flush=True,
        )

    if args.report:
        with args.report.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=list(results[0]))
            writer.writeheader()
            writer.writerows(results)

    matches = sum(result["status"] == "MATCH" for result in results)
    print(f"{matches}/{len(results)} objectives match.")
    return 0 if matches == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
