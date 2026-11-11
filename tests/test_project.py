import json
from pathlib import Path
import unittest
import shutil
import tempfile
from unittest.mock import patch
import joblib
import pandas as pd
from src.common import ROOT,key,duplicate_key,sha,INTENTS
from src.evaluate import evaluate
from sklearn.metrics import accuracy_score,f1_score

class ProjectChecks(unittest.TestCase):
    def test_reviewed_subset_is_traceable_and_separated(self):
        data=pd.read_csv(ROOT/'data/processed/reviewed.csv',keep_default_na=False)
        decisions=pd.read_csv(ROOT/'data/review/decisions.csv',keep_default_na=False)
        state=json.loads((ROOT/'reports/readiness.json').read_text())
        self.assertEqual(len(data),state['accepted'])
        self.assertEqual(set(data.record_id),set(decisions.loc[decisions.decision.eq('accept'),'record_id']))
        self.assertFalse(data.text.map(duplicate_key).duplicated().any())
        self.assertTrue(data.groupby('group_id').split.nunique().eq(1).all())
        self.assertEqual(sha(ROOT/'data/processed/reviewed.csv'),state['reviewed_sha256'])
        self.assertTrue(data.loc[data.split.eq('test'),'review_status'].eq('independently_reviewed').all())

    def test_external_training_only_and_nested_samples(self):
        pool=pd.read_csv(ROOT/'data/external/massive/training_pool.csv',dtype=str,keep_default_na=False)
        selected=pd.read_csv(ROOT/'reports/external_selected_ids.csv',dtype=str)
        self.assertTrue(pool.source_partition.eq('train').all())
        self.assertEqual(set(pool.label),set(INTENTS))
        self.assertTrue(set(selected.source_record_id)<=set(pool.source_record_id))
        a=set(selected.loc[selected.condition.eq('massive_20'),'source_record_id'])
        b=set(selected.loc[selected.condition.eq('massive_50'),'source_record_id'])
        self.assertEqual(len(a),200);self.assertEqual(len(b),500);self.assertTrue(a<=b)

    def test_models_results_and_selection_agree(self):
        r=json.loads((ROOT/'reports/development.json').read_text())
        selected=json.loads((ROOT/'models/selection.json').read_text())
        self.assertFalse(r['test_evaluated'])
        self.assertEqual(selected['condition'],r['selected_condition'])
        for name,run in r['runs'].items():
            path=ROOT/'models'/(name+'.joblib')
            self.assertEqual(sha(path),run['model_sha256'])
            model=joblib.load(path)
            self.assertEqual(model['condition'],name)
            self.assertEqual(set(model['model'].classes_),set(INTENTS))
            state=json.loads((ROOT/'reports/readiness.json').read_text())
            self.assertEqual(run['dev_rows'],state['split_totals']['dev'])

    def test_saved_development_scores_reproduce(self):
        report=json.loads((ROOT/'reports/development.json').read_text())
        predictions=pd.read_csv(ROOT/'reports/development_predictions.csv')
        team=pd.read_csv(ROOT/'data/processed/reviewed.csv')
        dev=team[team.split.eq('dev')]
        for name,run in report['runs'].items():
            saved=predictions[predictions.condition.eq(name)]
            self.assertEqual(set(saved.record_id),set(dev.record_id))
            self.assertEqual(len(saved),len(dev))
            pack=joblib.load(ROOT/'models'/(name+'.joblib'))
            self.assertEqual(list(pack['model'].predict(dev.text)),list(saved.prediction))
            self.assertAlmostEqual(accuracy_score(saved.label,saved.prediction),run['model']['accuracy'])
            self.assertAlmostEqual(f1_score(saved.label,saved.prediction,labels=INTENTS,average='macro',zero_division=0),run['model']['macro_f1'])

    def test_final_evaluation_blocked_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);state=self.evaluation_fixture(root)
            state['ready_for_final_test']=False
            (root/'reports/readiness.json').write_text(json.dumps(state))
            with patch('src.evaluate.ROOT',root):
                with self.assertRaisesRegex(ValueError,'Final test BLOCKED'):evaluate()
            self.assertFalse((root/'models/freeze.json').exists())
            self.assertFalse((root/'reports/test.json').exists())
            self.assertFalse((root/'reports/test_predictions.csv').exists())

    def evaluation_fixture(self,destination):
        paths=['reports/readiness.json','models/selection.json','data/processed/reviewed.csv',
            'data/raw/responses.xlsx','data/review/workspace.xlsx','data/review/candidates.csv',
            'data/review/decisions.csv','data/review/metadata.json','data/review/permission.md',
            'src/starter/validate.py','src/starter/core.py']
        for relative in paths:
            target=destination/relative;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/relative,target)
        state=json.loads((destination/'reports/readiness.json').read_text())
        state['ready_for_final_test']=True  # Deliberately forged flag; must not bypass checks.
        (destination/'reports/readiness.json').write_text(json.dumps(state))
        return state

    def test_stale_review_evidence_blocks_even_with_ready_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.evaluation_fixture(root)
            with (root/'data/review/decisions.csv').open('a') as f:f.write('\n')
            with patch('src.evaluate.ROOT',root):
                with self.assertRaisesRegex(ValueError,'evidence changed'):evaluate()
            self.assertFalse((root/'models/freeze.json').exists())

    def test_forged_ready_flag_cannot_bypass_actual_class_minimums(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);state=self.evaluation_fixture(root)
            meta_path=root/'data/review/metadata.json'
            meta=json.loads(meta_path.read_text());meta['permission_confirmed_for_assessment']=True
            meta_path.write_text(json.dumps(meta))
            state['evidence_sha256']['metadata']=sha(meta_path)
            csv_path=root/'data/processed/reviewed.csv'
            data=pd.read_csv(csv_path)
            # Deliberately make one dev class short even when the real project is ready.
            subset=data[data.split.eq('dev') & data.label.eq('lists_createoradd')]
            data=data.drop(subset.index[4:]) if len(subset)>4 else data
            data.to_csv(csv_path,index=False)
            state['reviewed_sha256']=sha(csv_path)
            selection_path=root/'models/selection.json'
            selection=json.loads(selection_path.read_text());selection['reviewed_sha256']=sha(csv_path)
            selection_path.write_text(json.dumps(selection))
            (root/'reports/readiness.json').write_text(json.dumps(state))
            with patch('src.evaluate.ROOT',root):
                with self.assertRaisesRegex(ValueError,'fails the official validator'):evaluate()
            self.assertFalse((root/'models/freeze.json').exists())
            self.assertFalse((root/'reports/test.json').exists())

if __name__=='__main__':unittest.main()
