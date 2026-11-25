# IndustryOR GurobiPy benchmark

## Sources and versions

- **Original IndustryOR (ORLM, 2024).** ORLM introduced 100 benchmark problems from eight industries. [ORLM paper](https://arxiv.org/html/2405.17743)
- **CardinalOperations revision.** The maintainers updated the original 100-problem dataset on Hugging Face. [Revised dataset](https://huggingface.co/datasets/CardinalOperations/IndustryOR) · [Dataset revision](https://huggingface.co/datasets/CardinalOperations/IndustryOR/commit/b00811923f167cdf4ae1677c33cd61d4eea78f48)
- **SIRL cleaned edition (2025).** SIRL released a separate cleanup of IndustryOR. [SIRL release notes](https://github.com/Cardinal-Operations/SIRL#news) · [Benchmark files](https://github.com/Cardinal-Operations/SIRL/tree/main/test_data)
- **OptiMind cleaned edition (2025).** Microsoft's classified 99-problem CSV is the direct source for this release. [OptiMind paper](https://arxiv.org/abs/2509.22979v1) · [Source CSV](https://github.com/microsoft/OptiGuide/blob/main/optimind/data/optimind_cleaned_classified_industryor.csv)

The original IndustryOR data are under CC BY-NC 4.0. The repository includes the OptiMind license notice. [IndustryOR dataset card](https://huggingface.co/datasets/CardinalOperations/IndustryOR) · [OptiMind notice](https://github.com/microsoft/OptiGuide/blob/main/optimind/LICENSE)

## Scope of this release

This release covers all **99 OptiMind cases**, including production planning, lot sizing, transportation, and assignment. Each row contains a problem classification, a statement, a numerical reference answer, and a `model_file` entry. The 99 independently implemented GurobiPy models sit alongside the CSV in `data/`. [Corrected CSV](data/industryor_corrected.csv) · [Example model](data/problem_001.py)

## CSV changes and discrepancies

We changed the `question` and `answer` fields in **rows 001 and 002**. The given demands, rates, and quantities carry over, and the revised statements specify the rules used by the models. The other 97 rows retain OptiMind's classification, statement, and reference answer.

| CSV row | Statement and model | OptiMind answer | Our CSV answer | Gurobi optimum |
| --- | --- | ---: | ---: | ---: |
| 001 | The revised statement allows free inventory carryover and requires zero ending stock and backlog. The model enforces weekly stock balances and minimizes wages plus delay penalties. | 219,816 yuan | 219,600 yuan | 219,600 yuan |
| 002 | The revised statement counts new machines assigned to operations upon delivery. The model maximizes that count subject to annual operator availability and fleet balances. | 1,350 | 225 | 225 |
| 030 | The statement and answer come from OptiMind. The model uses the stated hourly processing rates. | 1,190.38 yuan | 1,190.38 yuan | 1,190.41 yuan |

### Earlier IndustryOR releases

- **001.** The original and revised CardinalOperations statements both leave inventory carryover unspecified. The original lists 219,816 yuan. The revised 219,888 yuan matches the model with zero carryover.
- **002.** The original leaves the horizon and objective unclear. The revision asks for a two-year training count and leaves the training allocation unspecified. Both list 125. OptiMind's ten-year rewrite introduces the conflict between immediate assignments and cumulative fleet-years.

[Original and OptiMind comparison](https://github.com/microsoft/OptiGuide/blob/main/optimind/data/comparisons/industryOR_original_vs_ours.html) · [CardinalOperations revision](https://huggingface.co/datasets/CardinalOperations/IndustryOR/blob/main/IndustryOR.json)

## How statements match models

Each row's `model_file` field identifies the corresponding Python script. For example, `problem_001.py` is the model for the first row. Each model encodes the row's input data, decision variables, constraints, and objective. The CSV answer is used by the evaluator for comparison after solving. It counts a match when `abs(computed - answer) / (1 + abs(answer)) < 1e-6`. [Evaluator](eval.py)

All 99 models reached optimality. They match **96 of 99** OptiMind answers and **98 of 99** answers in our CSV. Row 030 is the remaining discrepancy. [Corrected results](reports/verification.csv) · [OptiMind results](reports/verification_upstream.csv) · [Modeling assumptions](https://github.com/zeyi-xu/IndustryOR/blob/efd2a789c8a254b2af3f4b2fcfab36e69f1b84cb/README.md#modeling-assumptions)
