# Annotation quality assurance

80 synthetic texts cover four equally represented sentiment classes. A submission with seeded label errors tests whether the audit detects semantic discrepancies while refusing structurally invalid input.

[Case study](CASE_STUDY.md) · [Guidelines](guidelines.md) · [Texts](cases.csv) · [Reference labels](reference_labels.csv) · [Submission](submitted_labels.csv) · [QA report](QA_REPORT.md) · [Audit results](AUDIT_RESULTS.md) · [Portfolio](../../README.md)

From the repository root:

```bash
python AI_Eval_Portfolio/03_annotation_qa/audit.py
python AI_Eval_Portfolio/03_annotation_qa/audit.py --format json
python -m unittest discover -s tests -v
```

Input paths default to the script's directory, so invocation works from any working directory. Custom `--cases`, `--reference` and `--submitted` paths are supported. Exit code 0 means a valid audit completed, even when labels disagree; exit code 2 means invalid input. JSON reports include per-case mismatches and a reference-row/submitted-column confusion matrix.

No rows are silently dropped or repaired. The script validates schema, IDs, nonblank text/rationales, allowed labels and exact ID-set equality before calculating any metrics.
