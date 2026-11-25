# IndustryOR GurobiPy benchmark

## Overview

This standalone benchmark pairs all 99 problems in OptiMind's cleaned IndustryOR release with independent GurobiPy models. Each model runs on its own and prints the optimal objective value.

## Usage

### Installation

Run these commands from the repository root. The committed results were generated with Python 3.14.3 and GurobiPy 14.0.0. The package's bundled license was sufficient for all 99 models. [GurobiPy installation guide](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python)

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

### Running evaluations

```sh
.venv/bin/python solutions/problem_001.py
.venv/bin/python eval.py 1 2
.venv/bin/python eval.py --report verification.local.csv
.venv/bin/python eval.py --dataset upstream
```

The evaluator defaults to the corrected dataset. Pass row numbers to evaluate a subset or omit them to run all 99. The evaluator compares objectives using `abs(computed - expected) / (1 + abs(expected)) < 1e-6` and exits with status 1 when any row fails to match. The full corrected run reports the known discrepancy on row 030. The original `verify.py` command accepts the same arguments. [OptiMind evaluation metric](https://arxiv.org/pdf/2509.22979#page=7)

## Data and Benchmarks

Both datasets use the fields `problem_class`, `question`, and `answer`. Problem IDs refer to one-based CSV data rows, excluding the header, and match the numbers in the solution filenames.

| Path | Contents |
| --- | --- |
| [data/industryor_corrected.csv](data/industryor_corrected.csv) | Default benchmark dataset |
| [data/optimind_cleaned_classified_industryor.csv](data/optimind_cleaned_classified_industryor.csv) | OptiMind's cleaned dataset, preserved as released |
| [data/comparisons/](data/comparisons/) | Dataset changes and reference answer comparisons |
| [eval.py](eval.py) and [eval_utils/](eval_utils/) | Evaluation command and objective comparison logic |
| [solutions/](solutions/) | Numbered GurobiPy models with their instance data |
| [reports/](reports/) | Verification results and the report for OptiMind maintainers |

The evaluation entry point and comparison directory follow OptiMind's benchmark layout. [OptiMind project](https://github.com/microsoft/OptiGuide/tree/main/optimind)

## Dataset Cleaning Comparisons

**The corrected edition rewrites the statements and updates the reference answers for problems 001 and 002.** Problem 001 specifies free inventory carryover and zero ending inventory and backlog. Problem 002 defines the objective as new machines assigned to operations immediately upon delivery and spells out the timing of training and transfers. [Statement changes and answer comparisons](data/comparisons/industryor_optimind_vs_corrected.md)

## Verification Results

All 99 models reached Gurobi's optimal status in both evaluations.

| Reference dataset | Matches | Rows with discrepancies | Results |
| --- | ---: | --- | --- |
| Corrected IndustryOR | 98/99 | 030 | [Corrected verification](reports/verification.csv) |
| OptiMind cleaned IndustryOR | 96/99 | 001, 002, 030 | [Upstream verification](reports/verification_upstream.csv) |

For row 030, exact enumeration of whole-unit production confirms **1,190.41 yuan** at the stated hourly rates. The optimum produces 1,430, 500, and 324 units of products I, II, and III, giving a 3,000.20 yuan margin before 1,809.79 yuan in machine costs. Both bundled datasets record the OptiMind reference of **1,190.38 yuan** for this row. [GurobiPy model](solutions/problem_030.py) · [CardinalOperations correction](https://huggingface.co/datasets/CardinalOperations/IndustryOR/commit/8b0d8a536845b804233b62eccec12a597005d0b4) · [Report for OptiMind maintainers](reports/optimind_industryor_report.md)

The original IndustryOR snapshot lists 1,146.39 yuan for row 030. The model gives 1,146.4142 yuan with `prorate_full_load_cost=True`, which derives hourly rates from the full-load cost column. [OptiMind cleaning comparison](https://github.com/microsoft/OptiGuide/blob/main/optimind/data/comparisons/industryOR_original_vs_ours.html)

### Modeling assumptions

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

## License

IndustryOR is released under CC BY-NC 4.0. The data directory records the source attribution, dataset changes, and the OptiMind project's MIT notice. [Data provenance and license notices](data/README.md)

## Citation

Cite ORLM for the original IndustryOR benchmark and OptiMind for the cleaned dataset. [ORLM paper](https://arxiv.org/abs/2405.17743) · [OptiMind paper](https://arxiv.org/abs/2509.22979)
