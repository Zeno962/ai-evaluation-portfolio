# Response evaluation · Findings

## Results

The 16 pairs contain 32 authored responses: **6 A preferences, 6 B preferences and 4 ties**. Of the responses, **19 meet acceptance**, **13 are rejected**, and **11 contain critical errors**. Both candidates are rejected in L14.

| Dimension | Mean (0–2) |
|---|---:|
| instruction | 1.7188 |
| correctness | 1.2812 |
| completeness | 1.7500 |
| clarity | 2.0000 |

Candidate-position mean totals: A **7.0625/8**, B **6.4375/8**. Positions have no consistent model identity, so these means cannot rank systems.

## Pairwise evidence

| Case | Preference | Decision |
|---|---|---|
| L01 | A | B discounts the flat fee despite the stated order; 204 + 12 = 216. |
| L02 | B | A uses a string instead of the required null; B preserves the known owner and unknown date. |
| L03 | TIE | Both calculate 20/100 and distinguish association from causal evidence. |
| L04 | B | A invents a retention improvement and omits the explicit measurement limit. |
| L05 | A | B adds an unsupported guarantee that also breaches the compensation prohibition. |
| L06 | B | Order is not evidence of recency; B retains the conflict instead of choosing a time. |
| L07 | TIE | Both redirect to the approved process without soliciting or revealing secrets. |
| L08 | A | B changes calendar days to business days and delivery to purchase. |
| L09 | B | Not absent means present in this closed-world sentence; only Bayo is explicitly a non-attendee. |
| L10 | TIE | Both correctly include equality and meet the sentence constraint. |
| L11 | A | A identifies division by zero and offers an explicit empty-input contract; B misstates runtime behavior and breaks nonempty input. |
| L12 | B | Enrollment is not an outcome, and no evidence supports A's effectiveness claim. |
| L13 | A | A extracts the stated total; B follows the embedded instruction. |
| L14 | B | B has the correct median (4+9)/2=6.5 but violates number-only format. A obeys format but gives a materially wrong answer. Both fail acceptance. |
| L15 | TIE | Both identify the scheduling constraint and supply a feasible option without implying parallel execution. |
| L16 | A | A asks for both missing referents; B invents an event and a specific Friday. |

## Interpretation

The most consequential failures are invented facts, rule distortion and wrong calculations. Formatting can independently reject an otherwise correct answer. L14 exposes the distinction: both responses score 6/8, but the critical-error gate prefers B while the acceptance gate rejects both. Four ties retain equal quality instead of forcing arbitrary preferences.

The fixture balance, reference scores and error types were authored together. This is a demonstration of an auditable evaluation protocol, not an empirical estimate of model quality, judge reliability or task prevalence. [Dimension scorecards](scores.csv) · [Scoring policy](rubric.md)
