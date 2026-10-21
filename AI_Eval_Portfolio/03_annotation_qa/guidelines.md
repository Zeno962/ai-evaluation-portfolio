# Sentiment annotation guidelines

## Unit and target

Assign one label to the writer's evaluation of the experience or item described in the complete text. Keep all clauses in scope. Do not import facts, reviewer history or assumed expectations. Each synthetic text is a self-contained unit.

| Label | Rule |
|---|---|
| POSITIVE | Praise, satisfaction, favorable comparison or successful resolution without an expressed negative assessment of the actual experience. |
| NEGATIVE | Criticism, dissatisfaction, regret or an explicit functional failure without a positive assessment of the actual experience. |
| NEUTRAL | Description, specification, price, time or status with no evaluative stance or stated functional failure. |
| MIXED | Both favorable and unfavorable assessments of the experience, including different aspects of one item or service. |

## Boundary rules

1. **Functional failure:** repeated crashes, broken goods, lost data and incomplete downloads count as negative outcomes even without “I dislike.” A bare status such as “delivered” is neutral. Failure must be evident in the text, not guessed from a specification.
2. **Negation:** determine what is negated. “Not difficult” is positive; “did not fix the failure” is negative. “No headphone socket” is a neutral specification absent a reaction.
3. **Contrast:** “but” is not sufficient for MIXED. Negative expectations before a favorable actual experience remain POSITIVE. A higher factual price followed by explicit approval is also POSITIVE.
4. **Sarcasm:** use a negative reading only where text-internal evidence is strong, such as “Great, another cancelled appointment after I waited all morning.” The cancellation and wasted time support dissatisfaction. A lone “Great” would not support this inference.
5. **Aspect conflict:** retain both sides when one aspect is praised and another criticized. Do not let the last clause automatically determine the label.
6. **Insufficient context:** flag a text for review when reasonable readings change the label. This dataset has a proposed reference for every text; `review_priority=borderline` identifies decisions most suitable for independent review. It does not claim adjudication has occurred.

The reference CSV records the applied rule per case. References are authored judgments under this policy, not independently established ground truth.
