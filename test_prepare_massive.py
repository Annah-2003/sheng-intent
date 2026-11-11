"""Software fixtures only; no test examples enter the real training pool."""
import contextlib
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from prepare_massive import INTENTS,prepare

class MassiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.archive=self.root/'fixture.tar.gz'
        self.team=self.root/'team.csv'
        self.team.write_text('text\nFIXTURE weather_query 0\n',encoding='utf-8')
        rows=[dict(id=f'{label}-{n}',locale='sw-KE',partition='train',intent=label,
                   utt=f'FIXTURE {label} {n}') for label in INTENTS for n in range(55)]
        rows.extend([
            dict(id='heldout',locale='sw-KE',partition='test',intent='alarm_set',utt='NEVER TRAIN THIS'),
            dict(id='duplicate',locale='sw-KE',partition='train',intent='alarm_set',utt='fixture alarm_set 0'),
            dict(id='conflict-a',locale='sw-KE',partition='train',intent='alarm_set',utt='SHARED CONFLICT'),
            dict(id='conflict-b',locale='sw-KE',partition='train',intent='play_music',utt='shared conflict')])
        with tarfile.open(self.archive,'w:gz') as tar:
            for name,blob in [('1.1/data/sw-KE.jsonl','\n'.join(map(json.dumps,rows)).encode()),
                              ('1.1/LICENSE',b'https://creativecommons.org/licenses/by/4.0/')]:
                info=tarfile.TarInfo(name);info.size=len(blob);tar.addfile(info,io.BytesIO(blob))

    def test_partition_dedup_overlap_and_balanced_samples(self):
        import csv
        out=self.root/'prepared'
        with contextlib.redirect_stdout(io.StringIO()):
            m=prepare(self.archive,out,self.team)
        self.assertEqual(m['rows'],549)
        self.assertEqual(m['samples']['20']['rows'],200)
        self.assertEqual(m['samples']['50']['rows'],500)
        with (out/'training_pool.csv').open() as f: rows=list(csv.DictReader(f))
        self.assertTrue(all(r['source_partition']=='train' for r in rows))
        self.assertFalse(any(r['source_record_id']=='heldout' for r in rows))
        self.assertFalse(any(r['text'].casefold()=='fixture weather_query 0' for r in rows))
        def ids(cap):
            with (out/f'train_{cap}_per_intent.csv').open() as f:
                return {r['source_record_id'] for r in csv.DictReader(f)}
        self.assertTrue(ids(20)<=ids(50))
        with self.assertRaisesRegex(ValueError,'NEW output'):
            prepare(self.archive,out,self.team)

    def test_missing_team_snapshot_blocks(self):
        with self.assertRaisesRegex(ValueError,'team text CSV'):
            prepare(self.archive,self.root/'out',self.root/'missing.csv')

if __name__=='__main__':unittest.main()
