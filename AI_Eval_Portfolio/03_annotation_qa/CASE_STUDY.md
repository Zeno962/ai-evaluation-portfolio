# Case study · Auditing sentiment labels without hiding data defects

## Problem

A useful annotation audit must distinguish label disagreement from corrupted input. Duplicate IDs can silently overwrite records, absent rows can distort denominators, and invalid labels can pollute metrics.

## Dataset and method

The batch contains 80 unique texts with 20 proposed references per class. It spans factual statements, negation, contrast, functional failures, sarcasm, expectations and aspect conflict. Sixteen submission labels are deliberately changed, four per reference class. The submission simulates incoming data; it is not a person's annotation history.

The standard-library audit first validates all three tables and their ID sets, then produces agreement, a complete 4×4 confusion matrix, per-class precision/recall/F1, macro-F1 and case-level discrepancies. A separate verifier regenerates the published results; tests cover valid and invalid data, metric arithmetic and command-line behavior.

## Findings

The submitted batch matches 64 of 80 references (80.0% agreement). MIXED errors collapse opposing aspects to one pole; neutral errors infer sentiment from timestamps or specifications; negation and expectation cases expose context mistakes. [QA report](QA_REPORT.md) connects each flagged item to its text and reference rationale.

The audit reports discrepancies for review rather than rewriting the submission. Structural errors stop the audit before metrics are produced. No “after correction” accuracy is reported because no independent relabeling was performed.

## Limits

Balanced references and seeded errors make this a software and methodology demonstration. Agreement against these references does not measure annotator skill, inter-rater reliability or production prevalence. Borderline labels require independent review before use as a benchmark. The audit compares labels; it does not infer sentiment or adjudicate text automatically.
