"""Integration check using temporary synthetic software fixtures, never real test data."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import joblib
import pandas as pd
from compare_massive import compare
from finalize_data import FIELDS,INTENTS
from prepare_massive import sha

class CompareTests(unittest.TestCase):
    def test_validated_data_three_conditions_and_no_test_vocabulary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            team=[]
            for label in INTENTS:
                for n in range(25):
                    split='train' if n<15 else 'dev' if n<20 else 'test'
                    text=f'SOFTWARE FIXTURE {label} {n}'
                    if split=='test':text+=' NEVERSEENTESTTOKEN'
                    row={field:'fixture' for field in FIELDS}
                    row.update(record_id=f'{label}-{n}',text=text,label=label,split=split,
                        group_id=f'{label}-{split}',language='sw-KE',source_method='original_human',
                        review_status='independently_reviewed',contributor_code='author',reviewer_code='reviewer')
                    team.append(row)
            data=root/'contribution.csv'
            pd.DataFrame(team).to_csv(data,index=False)
            (root/'manifest.json').write_text(json.dumps(dict(status='reviewed_data_validated_not_evaluated',contribution_sha256=sha(data))))
            external=root/'external';external.mkdir()
            rows=[dict(text=f'EXTERNAL FIXTURE {label} {n}',label=label,language='sw-KE',
                       source_partition='train',source_record_id=f'external-{label}-{n}',group_id=f'ext-{label}-{n}')
                  for label in INTENTS for n in range(51)]
            pool=external/'training_pool.csv';pd.DataFrame(rows).to_csv(pool,index=False)
            (external/'manifest.json').write_text(json.dumps(dict(training_pool_sha256=sha(pool))))
            output=root/'comparison'
            with contextlib.redirect_stdout(io.StringIO()):compare(data,external,output)
            table=pd.read_csv(output/'comparison.csv')
            self.assertEqual(table.external_train_rows.tolist(),[0,200,500])
            for condition in table.condition:
                pack=joblib.load(output/condition/'model.joblib')
                vocab=pack['model'][0].vocabulary_
                self.assertNotIn('neve',vocab)
                self.assertFalse(json.loads((output/condition/'dev_metrics.json').read_text())['test_evaluated'])
            with self.assertRaisesRegex(ValueError,'NEW comparison'):
                compare(data,external,output)
            (root/'manifest.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'validated export'):
                compare(data,external,root/'other-output')

if __name__=='__main__':unittest.main()
