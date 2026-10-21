"""Validate and audit a sentiment-label batch using only the Python standard library."""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

LABELS = ('POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED')
BASE = Path(__file__).resolve().parent


def load_table(path, required):
    """Return rows keyed by case_id; reject malformed rows rather than normalizing them."""
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream, strict=True)
        headers = reader.fieldnames
        if not headers or len(headers) != len(set(headers)):
            raise ValueError(f'{Path(path).name}: missing or duplicate headers')
        if not set(required).issubset(headers):
            raise ValueError(f'{Path(path).name}: required columns: {", ".join(required)}')
        rows = {}
        for line, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'{Path(path).name}:{line}: wrong field count')
            for column in required:
                if not row[column].strip() or row[column] != row[column].strip():
                    raise ValueError(f'{Path(path).name}:{line}: blank or padded {column}')
            cid = row['case_id']
            if cid in rows:
                raise ValueError(f'{Path(path).name}:{line}: duplicate case_id {cid}')
            rows[cid] = row
    if not rows:
        raise ValueError(f'{Path(path).name}: empty dataset')
    return rows


def validate_labels(rows, column):
    for cid, row in rows.items():
        if row[column] not in LABELS:
            raise ValueError(f'{cid}: invalid {column} {row[column]!r}')


def safe_ratio(numerator, denominator):
    """Zero-denominator class metrics are reported as 0 by explicit convention."""
    return numerator / denominator if denominator else 0.0


def audit(cases_path, reference_path, submitted_path):
    cases = load_table(cases_path, ('case_id', 'text'))
    reference = load_table(reference_path, ('case_id', 'reference_label', 'rationale'))
    submitted = load_table(submitted_path, ('case_id', 'submitted_label'))
    for name, rows in [('reference', reference), ('submitted', submitted)]:
        if set(rows) != set(cases):
            missing = sorted(set(cases) - set(rows))
            extra = sorted(set(rows) - set(cases))
            raise ValueError(f'{name} IDs differ: missing={missing}, extra={extra}')
    validate_labels(reference, 'reference_label')
    validate_labels(submitted, 'submitted_label')
    matrix = {actual: {predicted: 0 for predicted in LABELS} for actual in LABELS}
    mismatches = []
    for cid in sorted(cases):
        actual = reference[cid]['reference_label']
        predicted = submitted[cid]['submitted_label']
        matrix[actual][predicted] += 1
        if actual != predicted:
            mismatches.append(dict(case_id=cid, submitted=predicted, reference=actual,
                                   text=cases[cid]['text'], rationale=reference[cid]['rationale']))
    per_class = {}
    for label in LABELS:
        tp = matrix[label][label]
        support = sum(matrix[label].values())
        predicted_count = sum(matrix[actual][label] for actual in LABELS)
        per_class[label] = dict(support=support, predicted=predicted_count,
                                precision=safe_ratio(tp, predicted_count),
                                recall=safe_ratio(tp, support),
                                f1=safe_ratio(2 * tp, support + predicted_count))
    n = len(cases)
    matches = n - len(mismatches)
    return dict(cases=n, matches=matches, mismatches_count=len(mismatches),
                agreement=matches/n, mismatch_rate=len(mismatches)/n,
                reference_distribution=dict(Counter(reference[c]['reference_label'] for c in sorted(cases))),
                confusion_orientation='rows=reference; columns=submitted', confusion_matrix=matrix,
                per_class=per_class, macro_f1=sum(x['f1'] for x in per_class.values())/len(LABELS),
                zero_division=0, mismatches=mismatches)


def text_report(result):
    lines = [f"Cases: {result['cases']} | Matches: {result['matches']} | Mismatches: {result['mismatches_count']}",
             f"Agreement with references: {result['agreement']:.1%}",
             f"Macro-F1 (four labels): {result['macro_f1']:.4f}",
             'Confusion matrix: rows=reference; columns=submitted',
             'reference,' + ','.join(LABELS)]
    lines += [label + ',' + ','.join(str(result['confusion_matrix'][label][p]) for p in LABELS) for label in LABELS]
    lines.append('Submitted -> reference mismatches:')
    lines += [f"  {m['case_id']}: {m['submitted']} -> {m['reference']}" for m in result['mismatches']]
    return '\n'.join(lines) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, default=BASE/'cases.csv')
    parser.add_argument('--reference', type=Path, default=BASE/'reference_labels.csv')
    parser.add_argument('--submitted', type=Path, default=BASE/'submitted_labels.csv')
    parser.add_argument('--format', choices=('text', 'json'), default='text')
    args = parser.parse_args(argv)
    try:
        result = audit(args.cases, args.reference, args.submitted)
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f'Audit input error: {error}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.format == 'json' else text_report(result), end='\n' if args.format == 'json' else '')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
