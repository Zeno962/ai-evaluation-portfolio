"""Behavioral tests for validation, metrics and the command-line interface."""
import contextlib
import csv
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'AI_Eval_Portfolio/03_annotation_qa/audit.py'
spec=importlib.util.spec_from_file_location('audit',SCRIPT)
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.cases=self.base/'cases.csv'
        self.reference=self.base/'reference.csv'
        self.submitted=self.base/'submitted.csv'
        self.put(self.cases, [('case_id','text'),('a','Helpful'),('b','Bad'),('c','Fast but broken'),('d','Arrived at noon')])
        self.put(self.reference,[('case_id','reference_label','rationale'),('a','POSITIVE','Praise'),('b','NEGATIVE','Criticism'),('c','MIXED','Both'),('d','NEUTRAL','Fact')])
        self.put(self.submitted,[('case_id','submitted_label'),('a','POSITIVE'),('b','POSITIVE'),('c','MIXED'),('d','NEUTRAL')])

    def put(self,path,records):
        with path.open('w',encoding='utf-8',newline='') as f:
            csv.writer(f).writerows(records)

    def run_audit(self):
        return audit.audit(self.cases,self.reference,self.submitted)

    def test_known_confusion_and_metrics(self):
        r=self.run_audit()
        self.assertEqual((r['cases'],r['matches'],r['mismatches_count']),(4,3,1))
        self.assertEqual(r['confusion_matrix']['NEGATIVE']['POSITIVE'],1)
        self.assertAlmostEqual(r['agreement'],.75)
        self.assertAlmostEqual(r['per_class']['POSITIVE']['precision'],.5)
        self.assertAlmostEqual(r['per_class']['POSITIVE']['recall'],1)
        self.assertAlmostEqual(r['per_class']['POSITIVE']['f1'],2/3)
        self.assertAlmostEqual(r['macro_f1'],(2/3+0+1+1)/4)
        self.assertEqual(r['mismatches'][0]['case_id'],'b')

    def test_perfect_submission(self):
        self.put(self.submitted,[('case_id','submitted_label'),('a','POSITIVE'),('b','NEGATIVE'),('c','MIXED'),('d','NEUTRAL')])
        r=self.run_audit()
        self.assertEqual(r['agreement'],1)
        self.assertEqual(r['macro_f1'],1)
        self.assertEqual(r['mismatches'],[])

    def test_zero_support_and_predictions(self):
        self.put(self.cases,[('case_id','text'),('a','Good')])
        self.put(self.reference,[('case_id','reference_label','rationale'),('a','POSITIVE','Praise')])
        self.put(self.submitted,[('case_id','submitted_label'),('a','POSITIVE')])
        r=self.run_audit()
        self.assertEqual(r['per_class']['MIXED']['precision'],0)
        self.assertEqual(r['per_class']['MIXED']['recall'],0)
        self.assertEqual(r['per_class']['MIXED']['f1'],0)
        self.assertEqual(r['macro_f1'],.25)

    def test_all_wrong_submission(self):
        self.put(self.submitted,[('case_id','submitted_label'),('a','NEGATIVE'),('b','NEUTRAL'),('c','POSITIVE'),('d','MIXED')])
        r=self.run_audit()
        self.assertEqual(r['agreement'],0)
        self.assertEqual(r['macro_f1'],0)

    def test_duplicate_ids_in_every_input(self):
        for path in (self.cases,self.reference,self.submitted):
            original=path.read_text(encoding='utf-8')
            with self.subTest(path=path.name):
                path.write_text(original+original.splitlines()[1]+'\n',encoding='utf-8')
                with self.assertRaisesRegex(ValueError,'duplicate case_id'):
                    self.run_audit()
                path.write_text(original,encoding='utf-8')

    def test_missing_ids_in_both_label_files(self):
        for path in (self.reference,self.submitted):
            original=path.read_text(encoding='utf-8')
            with self.subTest(path=path.name):
                path.write_text('\n'.join(original.splitlines()[:-1])+'\n',encoding='utf-8')
                with self.assertRaisesRegex(ValueError,'IDs differ'):
                    self.run_audit()
                path.write_text(original,encoding='utf-8')

    def test_extra_ids(self):
        with self.submitted.open('a',encoding='utf-8') as f:
            f.write('extra,NEUTRAL\n')
        with self.assertRaisesRegex(ValueError,'extra='):
            self.run_audit()

    def test_invalid_label_in_both_files(self):
        for path in (self.reference,self.submitted):
            original=path.read_text(encoding='utf-8')
            with self.subTest(path=path.name):
                path.write_text(original.replace('POSITIVE','positive'),encoding='utf-8')
                with self.assertRaisesRegex(ValueError,'invalid'):
                    self.run_audit()
                path.write_text(original,encoding='utf-8')

    def test_empty_dataset(self):
        self.cases.write_text('case_id,text\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'empty dataset'):
            self.run_audit()

    def test_empty_file(self):
        self.cases.write_text('',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'headers'):
            self.run_audit()

    def test_duplicate_headers(self):
        self.cases.write_text('case_id,text,text\na,b,c\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'duplicate headers'):
            self.run_audit()

    def test_missing_required_column(self):
        self.reference.write_text('case_id,reference_label\na,POSITIVE\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'required columns'):
            self.run_audit()

    def test_blank_text(self):
        self.cases.write_text('case_id,text\na,\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'blank or padded text'):
            self.run_audit()

    def test_blank_id(self):
        self.cases.write_text('case_id,text\n,Something\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'blank or padded case_id'):
            self.run_audit()

    def test_blank_rationale(self):
        self.reference.write_text('case_id,reference_label,rationale\na,POSITIVE,\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'blank or padded rationale'):
            self.run_audit()

    def test_padded_label(self):
        self.submitted.write_text('case_id,submitted_label\na, POSITIVE\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'blank or padded'):
            self.run_audit()

    def test_extra_csv_field(self):
        self.cases.write_text('case_id,text\na,hello,extra\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'wrong field count'):
            self.run_audit()

    def test_missing_csv_field(self):
        self.cases.write_text('case_id,text\na\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'wrong field count'):
            self.run_audit()

    def test_malformed_quote(self):
        self.cases.write_text('case_id,text\na,"unclosed\n',encoding='utf-8')
        with self.assertRaises(csv.Error):
            self.run_audit()

    def test_bom_and_unicode_and_quoted_newline(self):
        self.put(self.cases,[('case_id','text'),('a','Café, good\nservice'),('b','Bad'),('c','Both'),('d','Fact')])
        original=self.cases.read_text(encoding='utf-8')
        self.cases.write_text(original,encoding='utf-8-sig')
        self.assertEqual(self.run_audit()['cases'],4)

    def test_row_order_does_not_change_result(self):
        expected=self.run_audit()
        text=self.submitted.read_text(encoding='utf-8').splitlines()
        self.submitted.write_text('\n'.join(text[:1]+list(reversed(text[1:])))+'\n',encoding='utf-8')
        self.assertEqual(self.run_audit(),expected)

    def test_cli_valid_json_from_other_directory(self):
        r=subprocess.run([sys.executable,str(SCRIPT),'--format','json'],cwd=self.base,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        result=json.loads(r.stdout)
        self.assertEqual((result['cases'],result['matches'],result['mismatches_count']),(80,64,16))

    def test_cli_custom_paths(self):
        r=subprocess.run([sys.executable,str(SCRIPT),'--cases',str(self.cases),'--reference',str(self.reference),'--submitted',str(self.submitted),'--format','json'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout)['agreement'],.75)

    def test_cli_invalid_input_is_nonzero(self):
        output,error=io.StringIO(),io.StringIO()
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(error):
            status=audit.main(['--cases',str(self.base/'missing.csv')])
        self.assertEqual(status,2)
        self.assertEqual(output.getvalue(),'')
        self.assertIn('Audit input error',error.getvalue())


if __name__=='__main__':
    unittest.main()
