"""Checks that work from a public checkout without the private assessment dataset."""
import json
import unittest
import joblib
from streamlit.testing.v1 import AppTest
from src.common import ROOT,sha,INTENTS

class PublicAppChecks(unittest.TestCase):
    def test_frozen_model_and_reports_match(self):
        selection=json.loads((ROOT/'models/selection.json').read_text())
        freeze=json.loads((ROOT/'models/freeze.json').read_text())
        final=json.loads((ROOT/'reports/test.json').read_text())
        development=json.loads((ROOT/'reports/development.json').read_text())
        self.assertEqual(freeze,final['freeze'])
        self.assertEqual(freeze['model_sha256'],selection['model_sha256'])
        for name,run in development['runs'].items():
            self.assertEqual(sha(ROOT/'models'/f'{name}.joblib'),run['model_sha256'])
        pack=joblib.load(ROOT/'models'/f"{selection['condition']}.joblib")
        self.assertEqual(set(pack['model'].classes_),set(INTENTS))
        self.assertEqual(pack.get('slot_memory'),{})
        self.assertEqual(final['test_size'],56)

    def test_app_renders_and_predicts_without_private_data(self):
        app=AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
        self.assertFalse(app.exception)
        app.button[0].click().run(timeout=30)
        self.assertTrue(any('Type a request first' in x.value for x in app.info))
        app.text_area[0].set_value('Nichezee doba')
        app.button[0].click().run(timeout=30)
        self.assertFalse(app.exception)
        self.assertTrue(any('Rada thinks' in x.value for x in app.markdown))
        self.assertTrue(any('Simulated response:' in x.value for x in app.info))

if __name__=='__main__':unittest.main()
