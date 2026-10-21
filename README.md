# Kenneth Ambrose · AI Evaluation Portfolio

Search quality, response evaluation and annotation QA through three reproducible case studies.

| Project | Evidence | Start here |
|---|---|---|
| Search relevance | 32 judgments across 8 query groups; partial matches, ambiguous intent and evidence limits | [Case study](AI_Eval_Portfolio/01_search_relevance/CASE_STUDY.md) |
| LLM response evaluation | 16 paired comparisons, 32 dimension-level scorecards, critical-error gates and ties | [Case study](AI_Eval_Portfolio/02_llm_evaluation/CASE_STUDY.md) |
| Annotation quality assurance | 80 texts, four sentiment classes, a validated audit tool and automated tests | [Case study](AI_Eval_Portfolio/03_annotation_qa/CASE_STUDY.md) |

The work emphasizes traceable decisions: each judgment connects a written rule to visible evidence, and every reported calculation can be regenerated from the included data.

## Explore the work

- [Search rubric and decision boundaries](AI_Eval_Portfolio/01_search_relevance/rubric.md) · [Ratings](AI_Eval_Portfolio/01_search_relevance/reference_ratings.csv) · [Findings](AI_Eval_Portfolio/01_search_relevance/ANALYSIS.md)
- [Response scoring protocol](AI_Eval_Portfolio/02_llm_evaluation/rubric.md) · [Scorecards](AI_Eval_Portfolio/02_llm_evaluation/scores.csv) · [Findings](AI_Eval_Portfolio/02_llm_evaluation/ANALYSIS.md)
- [Annotation guidelines](AI_Eval_Portfolio/03_annotation_qa/guidelines.md) · [QA findings](AI_Eval_Portfolio/03_annotation_qa/QA_REPORT.md) · [Audit tool](AI_Eval_Portfolio/03_annotation_qa/audit.py)

## Reproduce

Use Python 3.10 or later from the repository root. No third-party packages, API keys or network access are required.

```bash
python -m unittest discover -s tests -v
python tools/verify_portfolio.py --check
python AI_Eval_Portfolio/03_annotation_qa/audit.py
```

`verify_portfolio.py` validates data relationships and scores, recalculates metrics, checks local Markdown links and compares the committed reports with regenerated output. Run it without `--check` to regenerate the reports after editing the data.

## Scope and provenance

These are constructed demonstration datasets and reference judgments. Candidate A/B responses are authored comparison fixtures, not outputs from named models. The sentiment submission contains deliberately seeded errors. The reference judgments are not independent human ground truth, and the reported agreement is not an annotator performance score. No client data, model API experiments, external adjudication, live search tests or business outcomes are represented.

The portfolio demonstrates evaluation methods and executable analysis; it makes no claim of independent personal annotation or completion of client projects. Counts and findings describe only the supplied fixtures.

## Contact

Kenneth Ambrose · Abuja, Nigeria · [Email](mailto:kennethambrose962@gmail.com) · [GitHub](https://github.com/Zeno962)
