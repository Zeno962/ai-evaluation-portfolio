# Case study · Response preference with explicit acceptance gates

## Problem

A fluent response can fabricate evidence, distort a rule or violate a precise output constraint. A preference label alone hides which failure determined the decision and whether the preferred answer is usable.

## Design

Sixteen closed-reference prompt pairs contain 32 authored responses. The scorecards separate instruction, correctness, coverage and clarity, then apply a critical-error gate before total score. Six preferences favor A, six favor B, and four are ties. This balance is intentional fixture design, not a model comparison result.

## Key decisions

**L01: order of operations.** The flat fee follows the discount, giving 240 × 0.85 + 12 = 216. The alternative calculation discounts the fee and fails correctness despite fluent reasoning.

**L03 and L12: evidence sufficiency.** An observed visit increase does not establish causation; enrollment without outcomes cannot establish effectiveness. L03 permits a tie between two appropriately qualified answers. L12 rejects an unsupported treatment claim.

**L14: preference is not acceptance.** A returns an incorrect median in the required format. B computes 6.5 but adds prohibited explanation. Both total six points, yet B wins because A has a critical correctness error. Neither meets the acceptance contract.

**L16: ambiguity.** The missing event and calendar date require clarification. Assuming a team meeting and the coming Friday invents context.

## Results and interpretation

[Analysis](ANALYSIS.md) derives all totals, acceptance counts, preference counts and dimension means directly from the CSVs. Evidence is auditable at the row level. The fixtures support discussion of evaluation policy and error severity; they do not rank models or estimate real-world failure rates. There were no model calls, repeated samples, external raters or statistical generalization.
