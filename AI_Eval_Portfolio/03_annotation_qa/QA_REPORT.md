# Annotation QA · Findings

## Batch summary

| Measure | Value |
|---|---:|
| Texts | 80 |
| Matches | 64 |
| Discrepancies | 16 |
| Agreement with authored references | 80.0% |
| Discrepancy rate | 20.0% |
| Macro-F1 (four fixed labels) | 0.8013 |

Each reference class contains 20 items. Confusion matrix rows are references and columns are submissions. Precision = diagonal / predicted count; recall = diagonal / reference support; F1 = 2×diagonal / (support + predicted count). Undefined class ratios are 0, and macro-F1 is the unweighted mean over the four fixed labels. All class supports are nonzero in this batch.

| Reference / Submitted | POSITIVE | NEGATIVE | NEUTRAL | MIXED |
|---|---:|---:|---:|---:|
| POSITIVE | 16 | 1 | 1 | 2 |
| NEGATIVE | 2 | 16 | 2 | 0 |
| NEUTRAL | 2 | 2 | 16 | 0 |
| MIXED | 2 | 2 | 0 | 16 |

| Class | Precision | Recall | F1 | Reference support | Predicted count |
|---|---:|---:|---:|---:|---:|
| POSITIVE | 0.7273 | 0.8000 | 0.7619 | 20 | 22 |
| NEGATIVE | 0.7619 | 0.8000 | 0.7805 | 20 | 21 |
| NEUTRAL | 0.8421 | 0.8000 | 0.8205 | 20 | 19 |
| MIXED | 0.8889 | 0.8000 | 0.8421 | 20 | 18 |

## Discrepancy evidence

The following are review findings from the synthetic incoming batch. They are not a record of corrections to an individual's work. The audit leaves submitted data unchanged.

| Case | Submitted | Reference | Text | Rule applied |
|---|---|---|---|---|
| Q003 | MIXED | POSITIVE | I expected little, but the room was excellent. | The negative expectation is background; the actual experience is positive. |
| Q004 | NEGATIVE | POSITIVE | The battery no longer drains overnight; I am delighted. | Negated problem and explicit delight convey improvement. |
| Q011 | MIXED | POSITIVE | The ticket cost more than before, and it was worth every naira. | A higher price is factual context; the explicit value judgment is positive. |
| Q012 | NEUTRAL | POSITIVE | Nothing about the visit disappointed me. | Negating disappointment expresses satisfaction. |
| Q021 | NEUTRAL | NEGATIVE | The app crashed three times while I was saving my work. | Repeated task-blocking crashes imply dissatisfaction under the functional-failure rule. |
| Q025 | POSITIVE | NEGATIVE | Great, another cancelled appointment after I waited all morning. | Great conflicts with explicit cancellation and wasted time; context supports a negative reading. |
| Q028 | POSITIVE | NEGATIVE | The update did not fix the login failure. | The reported failure persists after an attempted fix. |
| Q036 | NEUTRAL | NEGATIVE | The download stopped at 90% on every attempt. | Repeated inability to complete a download is a functional failure. |
| Q041 | POSITIVE | NEUTRAL | The package arrived at noon. | A timestamp alone does not express approval or disapproval. |
| Q048 | NEGATIVE | NEUTRAL | The receipt shows a charge of NGN 5000. | A stated amount alone does not imply a value judgment. |
| Q057 | POSITIVE | NEUTRAL | The tracking page now says delivered. | A status message alone is not praise. |
| Q060 | NEGATIVE | NEUTRAL | The device has no headphone socket. | A negated specification is not itself dissatisfaction. |
| Q061 | POSITIVE | MIXED | The interface looks great, but it is painfully slow. | Design is praised and speed criticized. |
| Q063 | NEGATIVE | MIXED | Setup was easy, but the connection drops often. | Ease is positive; recurring disconnection is a functional failure. |
| Q068 | NEGATIVE | MIXED | The repair worked, but the final bill was unreasonable. | Successful repair and unreasonable cost are both evaluated. |
| Q078 | POSITIVE | MIXED | The form is easy to use, but it lost my saved entries. | Ease is positive and data loss is an explicit functional failure. |

## Review implications

- **Contrast and expectations:** Q003 and Q011 contain context that should not be mistaken for a negative assessment of the actual experience. A contrast word alone does not establish MIXED.
- **Negation and sarcasm:** Q004, Q028 and Q025 require the scope of negation or explicit failure context. The isolated word “Great” cannot override cancellation and wasted time.
- **Neutrality:** Q041, Q048, Q057 and Q060 demonstrate why timestamps, amounts, status messages and missing specifications do not establish sentiment without an evaluation.
- **Aspect conflict:** Q061, Q063, Q068 and Q078 retain both positive and negative evidence instead of choosing a single pole.

These patterns support targeted review of the affected boundaries. The rates reflect intentionally seeded errors and authored references; no real worker accuracy, before/after improvement, independent adjudication or business result is claimed. The audit validates file integrity and compares labels, but does not determine which semantic judgment is objectively true.

[Guidelines](guidelines.md) · [Detailed JSON](audit_results.json) · [Reference rationales](reference_labels.csv)
