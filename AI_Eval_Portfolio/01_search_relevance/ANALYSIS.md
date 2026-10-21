# Search relevance · Findings

## Coverage

The dataset contains **32 results across 8 queries**. Grade counts: 0: 8, 1: 8, 2: 8, 3: 8. **14** decisions carry review flags.

The eight grade-2 cases cover incomplete specificity, a navigation step, unknown pickup, regular versus date-specific hours, secondary intent, an omitted preservation explanation, unknown access and generic repair details. These cases make the boundary between useful partial evidence and failed constraints explicit.

## Ranking summary

| Query | nDCG@4 | Precision@4 (grade >=2) |
|---|---:|---:|
| G01 | 0.843 | 0.500 |
| G02 | 0.972 | 0.500 |
| G03 | 0.759 | 0.500 |
| G04 | 0.736 | 0.500 |
| G05 | 0.835 | 0.500 |
| G06 | 0.951 | 0.500 |
| G07 | 0.681 | 0.500 |
| G08 | 0.714 | 0.500 |

Mean nDCG@4 is **0.811**; mean precision@4 is **0.500**. Baseline ranks vary independently of CSV row order and are hypothetical. nDCG captures where useful results are displaced; precision stays at 0.500 because each four-result pool includes two grades >=2. Reordering by the same reference labels would be circular and is not presented as a measured improvement.

## Sensitivity and evidence limits

S05-2 would move from 2 to 3 under confirmed car intent. That conditional alternative does not change the published primary-intent metrics. Unknown accessibility or inventory is recorded as a review flag rather than silently treated as a verified fact.

Only snippets were evaluated. These authored references do not establish page quality, calibrated confidence, evaluator accuracy, production retrieval quality or inter-rater agreement. [Rating evidence](reference_ratings.csv) · [Method](rubric.md)
