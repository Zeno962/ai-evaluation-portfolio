# Response evaluation protocol

Read the prompt as the reference contract. Score each candidate against that contract before comparing candidates. A/B identify only positions within one fixture; there is no model mapping, hidden randomization or independent blinded review.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Instruction | Major explicit constraint breached | Partial compliance or minor structured-value mismatch | All explicit instructions followed |
| Correctness | Materially wrong or unsupported core claim | Local representation issue without a false core answer | Supported by the closed reference or reproducible calculation |
| Completeness | Core task absent or unusable | A required element is missing | All requested substantive elements are present |
| Clarity | Incoherent | Readable with substantial avoidable ambiguity | Clear and concise enough for the task |

Completeness measures coverage, not truth; a complete but wrong response can score 2 for coverage and 0 for correctness. Do not award accuracy merely because prose is fluent. A null-versus-TBD schema violation can score 1 for instruction and correctness because the unknown state is still recognizable; invented substantive values score 0 for correctness.

## Acceptance and pairwise preference

Total = sum of the four scores, maximum 8. Mark a critical error for a materially false core answer, invented evidence, unauthorized promise, or execution of an embedded untrusted instruction. Every correctness score of 0 in these fixtures is critical.

A response is accepted only if there is no critical error, instruction=2, correctness=2 and all dimensions >=1. Acceptance is stricter than relative preference.

Select preference with this deterministic order:

1. Prefer the candidate without a critical error.
2. If both have the same critical status, prefer the higher total.
3. If totals are equal, record TIE. Do not invent stylistic tiebreakers.

This policy deliberately makes a correct, format-breaking response preferable to a format-compliant false answer. Both can still be rejected, as L14 demonstrates. The gate is suitable for these closed tasks; a production evaluation would need task-specific severity rules and independently calibrated judgments.

## Evidence

Each pair has a rationale citing prompt constraints or a calculation. Scorecards retain that comparative evidence for both candidates. Scores and references were prepared together as demonstration judgments; they are not measurements from independent annotators. Balanced positions and ties prevent a trivial all-A presentation but do not establish absence of position bias in real judges.
