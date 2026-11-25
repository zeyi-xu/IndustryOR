# IndustryOR GurobiPy benchmark

This repository contains independent GurobiPy formulations for all 99 problems in OptiMind's cleaned IndustryOR CSV. Each script runs on its own and prints the optimal objective value. Script numbers refer to one-based CSV data rows, excluding the header.

## Quick start

Run these commands from the repository root. The committed results were generated with Python 3.14.3 and GurobiPy 14.0.0. The package's bundled license was sufficient for all 99 models. [GurobiPy installation guide](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python)

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python solutions/problem_003.py
.venv/bin/python verify.py 3
.venv/bin/python verify.py --report verification.local.csv
```

Pass row numbers to verify a subset. With no row numbers, `verify.py` checks every row. It compares the computed and reference objectives using `abs(computed - expected) / (1 + abs(expected)) < 1e-6`. The full run returns exit status 1 because three reference values differ, as documented below. [OptiMind evaluation metric](https://arxiv.org/pdf/2509.22979#page=7)

## Repository layout

| Path | Contents |
| --- | --- |
| [data/](data/) | Benchmark CSV, source attribution, and upstream license notices |
| [solutions/](solutions/) | Numbered GurobiPy models with their instance data |
| [verify.py](verify.py) | Objective comparison and optional CSV output |
| [reports/](reports/) | Committed verification results and the note for OptiMind maintainers |

## Verification results

All 99 models reached Gurobi's optimal status. The report records 96 matches and three discrepancies against **OptiMind's cleaned CSV**. [Verification CSV](reports/verification.csv) · [Report for OptiMind maintainers](reports/optimind_industryor_report.md)

The original labels below come from the snapshot recorded in OptiMind's cleaning comparison. CardinalOperations has since revised its own release. [OptiMind comparison](https://github.com/microsoft/OptiGuide/blob/main/optimind/data/comparisons/industryOR_original_vs_ours.html) · [CardinalOperations dataset](https://huggingface.co/datasets/CardinalOperations/IndustryOR/blob/main/IndustryOR.json) · [Revision b008119](https://huggingface.co/datasets/CardinalOperations/IndustryOR/commit/b00811923f167cdf4ae1677c33cd61d4eea78f48)

| Cleaned CSV row | Original label | OptiMind cleaned label | CardinalOperations revision | Computed |
| --- | ---: | ---: | --- | ---: |
| [001](solutions/problem_001.py) | 219,816 | 219,816 | 219,888 | 219,600 |
| [002](solutions/problem_002.py) | 125 | 1,350 | 125 for a two-year question | 225 |
| [030](solutions/problem_030.py) | 1,146.39 | 1,190.38 | 1,190.41 | 1,190.41 |

- **001.** The statement leaves inventory carryover unspecified. An independently checked schedule costs 219,600 yuan and fills every order on time by carrying 3,480 kg of food II from week 1 to week 2 and 240 kg from week 4 to week 6. Passing `allow_advance_production=False` to `solve()` gives 219,888 yuan, matching the CardinalOperations revision.
- **002.** The cleaned formula counts new allocations. Year 1 contributes zero, so the maximum is `9 × 25 = 225`, and a feasible assignment attains it. Counting active stock across years gives 1,325.
- **030.** Exact enumeration of whole-unit production confirms 1,190.41 yuan at the stated hourly rates. The optimum produces 1,430, 500, and 324 units of products I, II, and III for a 3,000.20 yuan margin before 1,809.79 yuan in machine costs. Passing `prorate_full_load_cost=True` to `solve()` uses rates derived from the full-load costs and gives 1,146.4142 yuan. The CardinalOperations revision uses the hourly column.

## Modeling assumptions

| Row | Interpretation used by the script |
| --- | --- |
| 021 and 049 | The objective deducts the stated costs from sales. In row 049, net proceeds are 9,100, while maximizing gross sales would give 77,000. |
| 035 | Travel uses Euclidean distance and one minute per distance unit. The solver minimizes the full-precision distance and reports approximately 175.37294 to two decimal places. |
| 038 | The fleet may use up to two vehicle types. Requiring exactly two types with positive trips raises minimum pollution from 600 to 640. |
| 044 | The profit table gives incremental discounts for successive quantities. |
| 058 | The CSV has question marks where the table should give blend inequalities. The script uses the signs in the original table. [Publisher's solution guide, Table 2-16](https://www.tup.com.cn/upload/books/yz/098013-01.pdf) |
| 067 | Both yards distribute their entire monthly receipts. If receipts can remain at the yards, the minimum transport cost falls from 1,030 to 895 ton-kilometers. |
| 070 | A factory-to-location assignment uses the volume and cost in the corresponding table cells. |
| 096 | Market demand limits sales, giving a profit of 450 thousand yuan. Requiring both demands to be fully met gives 350 thousand yuan. |
