# IndustryOR statement corrections

This edition corrects the statements and reference answers for problems **001** and **002** in OptiMind's cleaned IndustryOR dataset. The row numbers start at 1 after the CSV header. [OptiMind snapshot](../optimind_cleaned_classified_industryor.csv) · [Corrected dataset](../industryor_corrected.csv)

| Row | Original IndustryOR reference | OptiMind reference | Corrected reference | Statement change |
| --- | ---: | ---: | ---: | --- |
| [001](../../solutions/problem_001.py) | 219,816 yuan | 219,816 yuan | **219,600 yuan** | Specify free inventory carryover, clear all orders and inventory by week 8, and define training and overtime eligibility. |
| [002](../../solutions/problem_002.py) | 125 | 1,350 | **225** | Define the ten-year objective as immediate assignments from new deliveries and specify operator availability and equipment transfers. |

The original references come from the historical snapshot in OptiMind's comparison. [OptiMind cleaning comparison](https://github.com/microsoft/OptiGuide/blob/main/optimind/data/comparisons/industryOR_original_vs_ours.html)

## 001 · Food production and worker training

The OptiMind statement gave costs for late deliveries and left advance production and inventory carryover unspecified. The revised statement specifies zero initial and final inventory and backlog, unlimited free carryover, two-week training cohorts, and overtime for original workers available for production. All 50 original workers stay employed throughout the horizon and 50 trainees complete training by week 8.

A feasible plan costs 219,600 yuan and fills all orders on time by carrying 3,480 kg of food II from week 1 to week 2 and 240 kg from week 4 to week 6. Gurobi finds this cost optimal for the revised statement. The no-carryover variant gives 219,888 yuan, the value in the CardinalOperations revision. [CardinalOperations revision](https://huggingface.co/datasets/CardinalOperations/IndustryOR/commit/b00811923f167cdf4ae1677c33cd61d4eea78f48)

## 002 · Equipment allocation and training

The OptiMind prompt defined $x_t$ as immediate assignments among that year's deliveries and described its sum as active unit-years. The revised prompt uses industrial equipment and defines the objective as $\sum_{t=1}^{10} x_t$ for immediate assignments. It specifies when operators qualify and when equipment can move from training to operations.

Year 1 contributes zero because the operator pool starts empty. A feasible plan keeps the first 25 machines in training throughout the horizon, qualifying 125 operators each year. This supports assigning all 25 new machines to operations in each of years 2 through 10 and attains the upper bound of $9 \times 25 = 225$. Summing the entire active fleet across years gives 1,325 under the same rules. The CardinalOperations reference of 125 belongs to its two-year prompt. [CardinalOperations dataset](https://huggingface.co/datasets/CardinalOperations/IndustryOR/blob/main/IndustryOR.json)
