"""Compare Gurobi objective values with the selected IndustryOR dataset."""

import argparse
import csv
from pathlib import Path

from eval_utils.objectives import ROOT, check_problem


DATASETS = {
    "corrected": ROOT / "data" / "industryor_corrected.csv",
    "upstream": ROOT / "data" / "optimind_cleaned_classified_industryor.csv",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "problems", metavar="ID", nargs="*", type=int, help="One-based CSV row numbers"
    )
    parser.add_argument(
        "--dataset",
        choices=DATASETS,
        default="corrected",
        help="Reference dataset (default: corrected)",
    )
    parser.add_argument("--report", type=Path, help="Save the results as a CSV")
    args = parser.parse_args()

    with DATASETS[args.dataset].open(encoding="utf-8", newline="") as file:
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
