"""Validate portfolio datasets and regenerate or check deterministic published reports."""
import argparse
import csv
import importlib.util
import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
P = ROOT/'AI_Eval_Portfolio'
S, L, Q = [P/name for name in ('01_search_relevance', '02_llm_evaluation', '03_annotation_qa')]
spec = importlib.util.spec_from_file_location('annotation_audit', Q/'audit.py')
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rows(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def unique(data, key):
    require(len({row[key] for row in data}) == len(data), f'Duplicate {key}')


def pair_preference(a, b):
    if a['critical_error'] != b['critical_error']:
        return 'B' if a['critical_error'] == 'true' else 'A'
    return 'A' if int(a['total']) > int(b['total']) else 'B' if int(b['total']) > int(a['total']) else 'TIE'


def ranking_metrics(grades):
    def dcg(values):
        return sum((2**grade-1)/math.log2(i+2) for i, grade in enumerate(values))
    ideal = dcg(sorted(grades, reverse=True))
    return dict(ndcg_at_4=dcg(grades)/ideal if ideal else 0.0,
                precision_at_4=sum(g >= 2 for g in grades)/len(grades))


def search_results():
    cases, ratings = rows(S/'cases.csv'), rows(S/'reference_ratings.csv')
    unique(cases,'case_id'); unique(ratings,'case_id')
    require({r['case_id'] for r in cases} == {r['case_id'] for r in ratings}, 'Search IDs differ')
    require(len(cases)==32, 'Search fixture must contain 32 results')
    lookup = {r['case_id']:r for r in ratings}
    for r in ratings:
        require(r['rating'] in ('0','1','2','3'), 'Invalid search grade')
        require(r['confidence'] in ('high','medium','low') and bool(r['rationale'].strip()), 'Invalid search evidence')
        require(bool(r['alternative_rating']) == bool(r['alternative_condition']), 'Incomplete alternative')
        require(not r['alternative_rating'] or r['alternative_rating'] in ('0','1','2','3'), 'Invalid alternative grade')
    groups={}
    for qid in sorted({c['query_id'] for c in cases}):
        group=sorted([c for c in cases if c['query_id']==qid], key=lambda c:int(c['baseline_rank']))
        require([int(c['baseline_rank']) for c in group]==[1,2,3,4], 'Invalid search ranks')
        require(len({c['query'] for c in group}) == 1, 'Inconsistent query text')
        grades=[int(lookup[c['case_id']]['rating']) for c in group]
        groups[qid]=ranking_metrics(grades)
    require(len(groups)==8, 'Search fixture must contain 8 query groups')
    result=dict(cases=len(cases), query_groups=len(groups),
                grade_distribution=dict(sorted(Counter(r['rating'] for r in ratings).items())),
                confidence_distribution=dict(Counter(r['confidence'] for r in ratings)),
                review_flagged=sum(r['review_flag']!='none' for r in ratings),
                per_query=groups, mean_ndcg_at_4=sum(g['ndcg_at_4'] for g in groups.values())/len(groups),
                mean_precision_at_4=sum(g['precision_at_4'] for g in groups.values())/len(groups))
    return result


def llm_results():
    cases,scores,prefs=rows(L/'cases.csv'),rows(L/'scores.csv'),rows(L/'reference_evaluations.csv')
    unique(cases,'case_id'); unique(prefs,'case_id')
    ids={c['case_id'] for c in cases}
    require(ids=={p['case_id'] for p in prefs}=={s['case_id'] for s in scores}, 'LLM IDs differ')
    require(len(cases)==16 and len(scores)==32, 'Invalid LLM fixture size')
    by_pair={}
    dims=('instruction','correctness','completeness','clarity')
    for s in scores:
        key=(s['case_id'],s['candidate'])
        require(s['candidate'] in ('A','B') and key not in by_pair, 'Invalid or duplicate candidate')
        require(all(s[d] in ('0','1','2') for d in dims),'Invalid dimension score')
        values=[int(s[d]) for d in dims]
        require(int(s['total'])==sum(values), 'LLM total mismatch')
        require(s['critical_error'] in ('true','false'), 'Invalid critical flag')
        require(s['correctness']!='0' or s['critical_error']=='true', 'Core false answer must be critical')
        accepted=s['critical_error']=='false' and s['instruction']=='2' and s['correctness']=='2' and min(values)>=1
        require(s['accepted']==str(accepted).lower(), 'Invalid acceptance decision')
        require(bool(s['evidence'].strip()), 'Missing LLM evidence')
        by_pair[key]=s
    for p in prefs:
        require((p['case_id'],'A') in by_pair and (p['case_id'],'B') in by_pair, 'Incomplete pair')
        expected=pair_preference(by_pair[p['case_id'],'A'], by_pair[p['case_id'],'B'])
        require(p['preference']==expected, f"Preference violates rubric: {p['case_id']}")
        require(bool(p['reason'].strip()),'Missing preference reason')
    return dict(pairs=len(cases), responses=len(scores),preferences=dict(Counter(p['preference'] for p in prefs)),
                accepted=sum(s['accepted']=='true' for s in scores), rejected=sum(s['accepted']=='false' for s in scores),
                critical_errors=sum(s['critical_error']=='true' for s in scores),
                mean_by_dimension={d:sum(int(s[d]) for s in scores)/len(scores) for d in dims},
                candidate_mean_total={c:sum(int(s['total']) for s in scores if s['candidate']==c)/len(cases) for c in ('A','B')},
                both_rejected=[cid for cid in sorted(ids) if all(by_pair[cid,c]['accepted']=='false' for c in ('A','B'))])


def json_text(value):
    return json.dumps(value,indent=2,ensure_ascii=False)+'\n'


def reports():
    s=search_results(); l=llm_results()
    q=qa.audit(Q/'cases.csv',Q/'reference_labels.csv',Q/'submitted_labels.csv')
    require(q['cases']==80, 'QA fixture must contain 80 texts')
    require(q['reference_distribution']==dict.fromkeys(qa.LABELS,20),'QA class balance differs')
    require(len({r['text'] for r in rows(Q/'cases.csv')})==q['cases'],'Duplicate QA texts')
    require(l['preferences']==dict(A=6,B=6,TIE=4), 'LLM preference balance differs')
    out={S/'metrics.json':json_text(s),L/'metrics.json':json_text(l),Q/'audit_results.json':json_text(q)}
    out[S/'ANALYSIS.md']=f'''# Search relevance · Findings

## Coverage

The dataset contains **{s['cases']} results across {s['query_groups']} queries**. Grade counts: '''+', '.join(f"{k}: {v}" for k,v in s['grade_distribution'].items())+f'''. **{s['review_flagged']}** decisions carry review flags.

The eight grade-2 cases cover incomplete specificity, a navigation step, unknown pickup, regular versus date-specific hours, secondary intent, an omitted preservation explanation, unknown access and generic repair details. These cases make the boundary between useful partial evidence and failed constraints explicit.

## Ranking summary

| Query | nDCG@4 | Precision@4 (grade >=2) |
|---|---:|---:|
'''+''.join(f"| {k} | {v['ndcg_at_4']:.3f} | {v['precision_at_4']:.3f} |\n" for k,v in s['per_query'].items())+f'''
Mean nDCG@4 is **{s['mean_ndcg_at_4']:.3f}**; mean precision@4 is **{s['mean_precision_at_4']:.3f}**. Baseline ranks vary independently of CSV row order and are hypothetical. nDCG captures where useful results are displaced; precision stays at 0.500 because each four-result pool includes two grades >=2. Reordering by the same reference labels would be circular and is not presented as a measured improvement.

## Sensitivity and evidence limits

S05-2 would move from 2 to 3 under confirmed car intent. That conditional alternative does not change the published primary-intent metrics. Unknown accessibility or inventory is recorded as a review flag rather than silently treated as a verified fact.

Only snippets were evaluated. These authored references do not establish page quality, calibrated confidence, evaluator accuracy, production retrieval quality or inter-rater agreement. [Rating evidence](reference_ratings.csv) · [Method](rubric.md)
'''
    prefs=rows(L/'reference_evaluations.csv')
    out[L/'ANALYSIS.md']=f'''# Response evaluation · Findings

## Results

The {l['pairs']} pairs contain {l['responses']} authored responses: **{l['preferences']['A']} A preferences, {l['preferences']['B']} B preferences and {l['preferences']['TIE']} ties**. Of the responses, **{l['accepted']} meet acceptance**, **{l['rejected']} are rejected**, and **{l['critical_errors']} contain critical errors**. Both candidates are rejected in {', '.join(l['both_rejected'])}.

| Dimension | Mean (0–2) |
|---|---:|
'''+''.join(f'| {d} | {v:.4f} |\n' for d,v in l['mean_by_dimension'].items())+f'''
Candidate-position mean totals: A **{l['candidate_mean_total']['A']:.4f}/8**, B **{l['candidate_mean_total']['B']:.4f}/8**. Positions have no consistent model identity, so these means cannot rank systems.

## Pairwise evidence

| Case | Preference | Decision |
|---|---|---|
'''+''.join(f"| {p['case_id']} | {p['preference']} | {p['reason']} |\n" for p in prefs)+'''
## Interpretation

The most consequential failures are invented facts, rule distortion and wrong calculations. Formatting can independently reject an otherwise correct answer. L14 exposes the distinction: both responses score 6/8, but the critical-error gate prefers B while the acceptance gate rejects both. Four ties retain equal quality instead of forcing arbitrary preferences.

The fixture balance, reference scores and error types were authored together. This is a demonstration of an auditable evaluation protocol, not an empirical estimate of model quality, judge reliability or task prevalence. [Dimension scorecards](scores.csv) · [Scoring policy](rubric.md)
'''
    out[Q/'AUDIT_RESULTS.md']='# Annotation QA · Reproducible audit results\n\nGenerated from the committed synthetic texts, references and seeded submission.\n\n```text\n'+qa.text_report(q)+'```\n\n[Machine-readable results](audit_results.json) · [Interpretation](QA_REPORT.md)\n'
    out[Q/'QA_REPORT.md']=f'''# Annotation QA · Findings

## Batch summary

| Measure | Value |
|---|---:|
| Texts | {q['cases']} |
| Matches | {q['matches']} |
| Discrepancies | {q['mismatches_count']} |
| Agreement with authored references | {q['agreement']:.1%} |
| Discrepancy rate | {q['mismatch_rate']:.1%} |
| Macro-F1 (four fixed labels) | {q['macro_f1']:.4f} |

Each reference class contains 20 items. Confusion matrix rows are references and columns are submissions. Precision = diagonal / predicted count; recall = diagonal / reference support; F1 = 2×diagonal / (support + predicted count). Undefined class ratios are 0, and macro-F1 is the unweighted mean over the four fixed labels. All class supports are nonzero in this batch.

| Reference / Submitted | POSITIVE | NEGATIVE | NEUTRAL | MIXED |
|---|---:|---:|---:|---:|
'''+''.join('| '+label+' | '+' | '.join(str(q['confusion_matrix'][label][p]) for p in qa.LABELS)+' |\n' for label in qa.LABELS)+'''
| Class | Precision | Recall | F1 | Reference support | Predicted count |
|---|---:|---:|---:|---:|---:|
'''+''.join(f"| {label} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1']:.4f} | {m['support']} | {m['predicted']} |\n" for label,m in q['per_class'].items())+'''
## Discrepancy evidence

The following are review findings from the synthetic incoming batch. They are not a record of corrections to an individual's work. The audit leaves submitted data unchanged.

| Case | Submitted | Reference | Text | Rule applied |
|---|---|---|---|---|
'''+''.join(f"| {m['case_id']} | {m['submitted']} | {m['reference']} | {m['text']} | {m['rationale']} |\n" for m in q['mismatches'])+'''
## Review implications

- **Contrast and expectations:** Q003 and Q011 contain context that should not be mistaken for a negative assessment of the actual experience. A contrast word alone does not establish MIXED.
- **Negation and sarcasm:** Q004, Q028 and Q025 require the scope of negation or explicit failure context. The isolated word “Great” cannot override cancellation and wasted time.
- **Neutrality:** Q041, Q048, Q057 and Q060 demonstrate why timestamps, amounts, status messages and missing specifications do not establish sentiment without an evaluation.
- **Aspect conflict:** Q061, Q063, Q068 and Q078 retain both positive and negative evidence instead of choosing a single pole.

These patterns support targeted review of the affected boundaries. The rates reflect intentionally seeded errors and authored references; no real worker accuracy, before/after improvement, independent adjudication or business result is claimed. The audit validates file integrity and compares labels, but does not determine which semantic judgment is objectively true.

[Guidelines](guidelines.md) · [Detailed JSON](audit_results.json) · [Reference rationales](reference_labels.csv)
'''
    return out


def validate_links():
    for path in ROOT.rglob('*.md'):
        text=path.read_text(encoding='utf-8')
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
            if re.match(r'(?:https?://|mailto:|#)',target):
                continue
            target=unquote(target.split('#')[0])
            require((path.parent/target).exists(), f'Broken link in {path.relative_to(ROOT)}: {target}')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Fail if committed reports differ; write nothing')
    args=parser.parse_args(argv)
    try:
        output=reports()
        stale=[]
        for path,content in output.items():
            if args.check:
                if not path.exists() or path.read_text(encoding='utf-8')!=content:
                    stale.append(str(path.relative_to(ROOT)))
            else:
                path.write_text(content,encoding='utf-8')
        require(not stale,'Stale reports: '+', '.join(stale))
        validate_links()
    except (OSError, ValueError, KeyError, csv.Error) as error:
        print(f'Portfolio validation failed: {error}')
        return 1
    print(f'Validated 32 search ratings, 32 response scorecards, 80 QA records and {len(output)} reports.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
