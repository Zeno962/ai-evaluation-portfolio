# Search relevance evaluation

32 fictional result snippets across eight query groups show how intent and constraints affect relevance. Each group covers grades 0–3, with a varied hypothetical baseline rank independent of row order. These are calibration fixtures, not real search rankings.

[Case study](CASE_STUDY.md) · [Rubric](rubric.md) · [Cases](cases.csv) · [Judgments](reference_ratings.csv) · [Analysis](ANALYSIS.md) · [Metrics](metrics.json) · [Portfolio](../../README.md)

`cases.csv` includes a stable query ID, interpreted need and baseline rank. `reference_ratings.csv` supplies one rating per result, ordinal confidence, a review flag, rationale and a conditional alternative where needed. Empty alternative fields mean no alternate rating is specified, not proof of certainty.

Ratings describe only the supplied metadata. All entities, snippets and the `.example` domain are fictional; there are no live URLs or verified source claims. Confidence expresses confidence in a rubric decision, not a probability of page quality.
