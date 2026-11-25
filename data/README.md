# Data provenance and attribution

Both bundled CSVs contain 99 problems in the same row order. The corrected CSV's `model_file` column identifies the corresponding Python model in this directory.

- **Corrected IndustryOR.** The local edition updates the statements and objectives for rows 001 and 002. Its SHA-256 is `90d61ca7dc93e4dcb946da692fb3a77d959b870e1e624116659d7893bdc7591b`. [Corrected CSV](industryor_corrected.csv) · [Statement changes](comparisons/industryor_optimind_vs_corrected.md)
- **OptiMind cleaned IndustryOR.** This byte-for-byte upstream snapshot has SHA-256 `fd80b3061e13edc040a7ff395f4f664fd761ad26b651e5dc8dcbbd7d3a48b427`. [Bundled snapshot](optimind_cleaned_classified_industryor.csv) · [OptiMind source CSV](https://github.com/microsoft/OptiGuide/blob/main/optimind/data/optimind_cleaned_classified_industryor.csv)

CardinalOperations introduced IndustryOR with *ORLM*. The OptiMind authors released the cleaned adaptation and a comparison documenting changes to the original dataset. [ORLM paper](https://arxiv.org/abs/2405.17743) · [OptiMind paper](https://arxiv.org/abs/2509.22979) · [Cleaning comparison](https://github.com/microsoft/OptiGuide/blob/main/optimind/data/comparisons/industryOR_original_vs_ours.html)

## Upstream license notices

The original IndustryOR dataset is released under **CC BY-NC 4.0**, which requires attribution and limits reuse to noncommercial purposes. [CardinalOperations dataset card](https://huggingface.co/datasets/CardinalOperations/IndustryOR) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

The OptiMind project includes a Microsoft MIT license notice. A copy of that upstream notice is preserved here. [OptiMind notice](OPTIMIND-LICENSE)
