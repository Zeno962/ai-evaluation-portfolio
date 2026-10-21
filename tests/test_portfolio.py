"""Verify published calculations and severity behavior independently of report rendering."""
import importlib.util
import json
import math
import statistics
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('verify',ROOT/'tools/verify_portfolio.py')
verify=importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class PortfolioTests(unittest.TestCase):
    def test_ranking_perfect_and_reversed(self):
        self.assertAlmostEqual(verify.ranking_metrics([3,2,1,0])['ndcg_at_4'],1)
        ideal=7+3/math.log2(3)+1/math.log2(4)
        reversed_dcg=1/math.log2(3)+3/math.log2(4)+7/math.log2(5)
        self.assertAlmostEqual(verify.ranking_metrics([0,1,2,3])['ndcg_at_4'],reversed_dcg/ideal)
        self.assertEqual(verify.ranking_metrics([3,2,1,0])['precision_at_4'],.5)

    def test_zero_gain_ranking(self):
        self.assertEqual(verify.ranking_metrics([0,0,0,0]),dict(ndcg_at_4=0,precision_at_4=0))

    def test_critical_gate_overrides_total(self):
        self.assertEqual(verify.pair_preference(dict(critical_error='true',total='7'),dict(critical_error='false',total='5')),'B')

    def test_equal_totals_tie(self):
        self.assertEqual(verify.pair_preference(dict(critical_error='false',total='8'),dict(critical_error='false',total='8')),'TIE')

    def test_data_relationships(self):
        self.assertEqual(verify.search_results()['grade_distribution'],dict.fromkeys(('0','1','2','3'),8))
        self.assertEqual(verify.llm_results()['preferences'],dict(A=6,B=6,TIE=4))
        self.assertEqual(verify.llm_results()['both_rejected'],['L14'])

    def test_qa_fixture_counts_and_matrix(self):
        q=verify.qa.audit(verify.Q/'cases.csv',verify.Q/'reference_labels.csv',verify.Q/'submitted_labels.csv')
        self.assertEqual(q['confusion_matrix'],{
            'POSITIVE':{'POSITIVE':16,'NEGATIVE':1,'NEUTRAL':1,'MIXED':2},
            'NEGATIVE':{'POSITIVE':2,'NEGATIVE':16,'NEUTRAL':2,'MIXED':0},
            'NEUTRAL':{'POSITIVE':2,'NEGATIVE':2,'NEUTRAL':16,'MIXED':0},
            'MIXED':{'POSITIVE':2,'NEGATIVE':2,'NEUTRAL':0,'MIXED':16}})
        expected=(32/42+32/41+32/39+32/38)/4
        self.assertAlmostEqual(q['macro_f1'],expected)

    def test_closed_reference_calculations_and_formats(self):
        cases={c['case_id']:c for c in verify.rows(verify.L/'cases.csv')}
        self.assertEqual(240*(1-.15)+12,216)
        self.assertEqual(float(cases['L01']['candidate_a'].split(';')[0]),216)
        self.assertEqual(json.loads(cases['L02']['candidate_b']),dict(owner='Ada',due=None))
        self.assertEqual((120-100)/100,.2)
        self.assertLessEqual(len(cases['L04']['candidate_b'].split()),18)
        self.assertEqual(len(cases['L05']['candidate_a'].splitlines()),2)
        self.assertNotIn('refund',cases['L05']['candidate_a'].lower())
        self.assertEqual(cases['L09']['candidate_b'],'Bayo')
        self.assertEqual(cases['L13']['candidate_a'],'84')
        self.assertEqual(statistics.median([2,4,9,11]),6.5)
        self.assertTrue(cases['L14']['candidate_b'].startswith('6.5 '))
        self.assertEqual(2*30-45,15)

    def test_committed_reports_current_and_links_resolve(self):
        r=subprocess.run([sys.executable,str(ROOT/'tools/verify_portfolio.py'),'--check'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)


if __name__=='__main__':
    unittest.main()
