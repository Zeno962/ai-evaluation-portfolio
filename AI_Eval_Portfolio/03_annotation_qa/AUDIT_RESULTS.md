# Annotation QA · Reproducible audit results

Generated from the committed synthetic texts, references and seeded submission.

```text
Cases: 80 | Matches: 64 | Mismatches: 16
Agreement with references: 80.0%
Macro-F1 (four labels): 0.8013
Confusion matrix: rows=reference; columns=submitted
reference,POSITIVE,NEGATIVE,NEUTRAL,MIXED
POSITIVE,16,1,1,2
NEGATIVE,2,16,2,0
NEUTRAL,2,2,16,0
MIXED,2,2,0,16
Submitted -> reference mismatches:
  Q003: MIXED -> POSITIVE
  Q004: NEGATIVE -> POSITIVE
  Q011: MIXED -> POSITIVE
  Q012: NEUTRAL -> POSITIVE
  Q021: NEUTRAL -> NEGATIVE
  Q025: POSITIVE -> NEGATIVE
  Q028: POSITIVE -> NEGATIVE
  Q036: NEUTRAL -> NEGATIVE
  Q041: POSITIVE -> NEUTRAL
  Q048: NEGATIVE -> NEUTRAL
  Q057: POSITIVE -> NEUTRAL
  Q060: NEGATIVE -> NEUTRAL
  Q061: POSITIVE -> MIXED
  Q063: NEGATIVE -> MIXED
  Q068: NEGATIVE -> MIXED
  Q078: POSITIVE -> MIXED
```

[Machine-readable results](audit_results.json) · [Interpretation](QA_REPORT.md)
