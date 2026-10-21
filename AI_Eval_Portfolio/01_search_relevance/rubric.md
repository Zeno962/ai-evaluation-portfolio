# Search relevance rubric

Assess the visible title and snippet against the interpreted need. Do not infer page contents, stock, authenticity or freshness.

| Grade | Decision rule |
|---|---|
| 3 | Directly satisfies the primary task and all explicit constraints in the supplied metadata. |
| 2 | Substantially useful, but a key detail is unknown, another step is needed, or it serves a plausible secondary intent. |
| 1 | Topic or supporting resource matches, but an explicit constraint fails or the main action is absent. |
| 0 | No material support for the task or any plausible interpretation. |

## Decision boundaries

- Distinguish **unknown** from **contradicted** constraints. Unknown pickup timing can earn 2; explicit pickup in the wrong city earns at most 1.
- A step toward a destination is 2 when it visibly links to the desired portal; news about the institution is 1.
- For ambiguous queries, record the primary interpretation before rating. A substantial match to a plausible secondary interpretation can earn 2. Confirmed user intent can change the grade; document that condition rather than silently changing the interpretation.
- Grade 3 is a metadata relevance decision. A source may receive 3 and still require authenticity, stock or accessibility verification before use.
- Date-specific needs outrank old topical matches. A regular schedule with unknown exceptions is 2; a clearly historical schedule is at most 1.

Confidence is `high` for clear rule application and `medium` where intent or evidence remains unresolved. Review flags identify the missing evidence; they are not automatic score penalties. Repeated flags can guide targeted review.

## Ranking calculation

For each four-result query, gain is `2**rating - 1`; DCG@4 is the sum of gain/log2(rank+1). IDCG uses descending reference grades from the same pool. nDCG is DCG/IDCG (0 if all gains are zero). Precision@4 counts grades >=2 divided by four. These are descriptive calculations against the authored references, not measured retrieval quality or evaluator agreement.
