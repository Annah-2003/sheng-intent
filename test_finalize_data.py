"""Synthetic software-test fixtures only; never used as contribution or model data."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import pandas as pd
from finalize_data import INTENTS, digest, inspect, run

class FinalizeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.c=self.root/'c.csv'
        self.d=self.root/'d.csv'
        candidates,decisions=[],[]
        for label in INTENTS:
            for n in range(25):
                split='train' if n<15 else 'dev' if n<20 else 'reserved'
                rid=f'{label}-{n}'
                text=f'SOFTWARE FIXTURE {label} sample {n}'
                row=dict(record_id=rid,text=text,original_text=text,provisional_label=label,
                    contributor_code='author',scenario_id=f'{label}-{split}',
                    group_id=f'{label}-{split}',proposed_split=split,
                    mechanical_exclusion='',source_cell='fixture')
                candidates.append(row)
                decisions.append(dict(row,decision='accept',final_label=label,reviewer_code='reviewer',
                    reviewer_independent_of_author='yes',reason='',related_group_override=''))
        self.cf=pd.DataFrame(candidates)
        self.df=pd.DataFrame(decisions)
        self.save()
        evidence=self.root/'permission.txt'
        evidence.write_text('Synthetic test fixture; not actual permission evidence.')
        self.config=dict(language='sw-KE',language_confirmed=True,source_dataset='software_fixture',
            source_version='fixture',licence_or_permission='fixture_only',
            permission_confirmed_for_assessment=True,permission_evidence_path=str(evidence),
            candidates_sha256=digest(self.c),reviewers={'reviewer':dict(competence_confirmed=True,
                independence_checked=True,authored_contributor_codes=[])})

    def save(self):
        self.cf.to_csv(self.c,index=False)
        self.df.to_csv(self.d,index=False)

    def check(self):
        self.save()
        return inspect(self.c,self.d,self.config)[1]

    def test_valid_minimum(self):
        report=self.check()
        self.assertTrue(report['ready_for_export'],report['errors'])
        self.assertEqual(report['accepted'],250)

    def test_pending_never_accepted(self):
        self.df['decision']=''
        report=self.check()
        self.assertEqual(report['accepted'],0)
        self.assertFalse(report['ready_for_export'])

    def test_changed_source_blocks(self):
        self.df.loc[0,'text']='silently rewritten'
        self.assertTrue(any('source text changed' in e for e in self.check()['errors']))

    def test_authored_test_blocks(self):
        self.config['reviewers']['reviewer']['authored_contributor_codes']=['author']
        self.assertTrue(any('conflicts with authorship' in e for e in self.check()['errors']))

    def test_related_scenarios_cannot_cross(self):
        self.df.loc[0,'related_group_override']='shared'
        self.df.loc[20,'related_group_override']='shared'
        self.assertTrue(any('cross proposed splits' in e for e in self.check()['errors']))

    def test_duplicate_and_hash_blocks(self):
        self.cf.loc[20,'text']=self.cf.loc[0,'text'].upper()+'  '
        self.df.loc[20,'text']=self.cf.loc[20,'text']
        report=self.check()
        self.assertTrue(any('duplicate texts' in e for e in report['errors']))
        self.assertTrue(any('snapshot hash' in e for e in report['errors']))

    def test_permissions_block(self):
        self.config['permission_confirmed_for_assessment']=False
        self.assertFalse(self.check()['ready_for_export'])

    def test_invalid_and_missing_decisions_block(self):
        self.df.loc[0,'decision']='approved'
        self.df=self.df.iloc[:-1]
        report=self.check()
        self.assertTrue(any('IDs differ' in e for e in report['errors']))
        self.assertTrue(any('unknown decision' in e for e in report['errors']))

    def test_export_official_validator_and_no_overwrite(self):
        config=self.root/'config.json'
        config.write_text(json.dumps(self.config),encoding='utf-8')
        validator=Path(__file__).parent/'datathon-starter-kit/validate.py'
        if not validator.exists():
            validator=Path(__file__).parent/'validate.py'
        out=self.root/'output'
        with contextlib.redirect_stdout(io.StringIO()):
            run(self.c,self.d,config,self.root/'report',out,validator)
            with self.assertRaisesRegex(ValueError,'already exists'):
                run(self.c,self.d,config,self.root/'report',out,validator)
        exported=pd.read_csv(out/'contribution.csv')
        self.assertEqual(len(exported),250)
        self.assertEqual(set(exported.split),{'train','dev','test'})
        self.assertEqual(json.loads((out/'manifest.json').read_text())['contribution_sha256'],digest(out/'contribution.csv'))

if __name__=='__main__':
    unittest.main()
