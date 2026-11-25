# Three reference answer discrepancies in OptiMind IndustryOR

Hi OptiMind team,

We solved independent GurobiPy 14.0.0 formulations for all 99 problems in your cleaned IndustryOR CSV. All reached optimality, and 96 objective values matched the reference answers. Row numbers below start at 1 after the header. [Cleaned IndustryOR CSV](https://github.com/microsoft/OptiGuide/blob/main/optimind/data/optimind_cleaned_classified_industryor.csv)

- **001 · Food production and worker training.** The CSV gives **219,816 yuan**. With all orders cleared by week 8, the minimum is **219,600** with free inventory carryover and **219,888** with zero carryover. The statement leaves the carryover rule open.
- **002 · Annual allocation and training.** The CSV gives **1,350**. The formula counts the new units put into service each year. Year 1 contributes zero and the other nine years can each contribute 25, giving an attainable optimum of **225**. Summing the entire active stock over the ten years gives **1,325** under the same fleet and training rules.
- **030 · Two-stage production, original IndustryOR ID 31.** The CSV gives **1,190.38 yuan**. At the listed hourly rates, a feasible schedule earns **1,190.41 yuan**, with 3,000.20 yuan in margin before 1,809.79 yuan in machine costs. Exact enumeration confirms this optimum, which also appears in the June 2025 upstream correction. [CardinalOperations correction](https://huggingface.co/datasets/CardinalOperations/IndustryOR/commit/8b0d8a536845b804233b62eccec12a597005d0b4)

Could you confirm the intended inventory rule for row 001 and the objective for row 002, and review the reference for row 030? We can share runnable GurobiPy models for all three.

Thanks for taking a look.
