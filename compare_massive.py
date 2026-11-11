"""Compare contribution-only vs added MASSIVE on dev; never evaluate test rows."""
import argparse
import json
from pathlib import Path
import sys
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import make_pipeline

ROOT=Path(__file__).resolve().parent
if (ROOT/'datathon-starter-kit').exists():sys.path.insert(0,str(ROOT/'datathon-starter-kit'))
from core import INTENTS,classification_score,fingerprint
from validate import check
from prepare_massive import norm,sha

def compare(data,external,output):
    data,external,output=map(Path,[data,external,output])
    if output.exists():raise ValueError('Choose a NEW comparison output directory.')
    # Require the export pipeline's real validated-data manifest; no practice-mode shortcut.
    frozen=json.loads((data.parent/'manifest.json').read_text(encoding='utf-8'))
    if frozen.get('status')!='reviewed_data_validated_not_evaluated' or frozen['contribution_sha256']!=sha(data):
        raise ValueError('Reviewed data does not match the validated export manifest.')
    team=check(str(data),False,'intent')
    tr=team[team.split.eq('train')]
    dev=team[team.split.eq('dev')]
    if set(tr.group_id)&set(dev.group_id):raise ValueError('Team scenario leakage.')
    manifest=json.loads((external/'manifest.json').read_text(encoding='utf-8'))
    pool_path=external/'training_pool.csv'
    if sha(pool_path)!=manifest['training_pool_sha256']:raise ValueError('External pool fingerprint differs.')
    pool=pd.read_csv(pool_path,dtype=str,keep_default_na=False)
    if not pool.source_partition.eq('train').all() or not pool.language.eq('sw-KE').all():
        raise ValueError('External pool contains unsupported locale/partition.')
    if set(pool.label)-set(INTENTS) or pool.source_record_id.duplicated().any():
        raise ValueError('Invalid external labels or duplicated source IDs.')
    # Exact overlap uses all team texts, including held-out text, only as a leakage exclusion.
    team_keys=set(team.text.map(lambda x:norm(x).casefold()))
    overlap=pool.text.map(lambda x:norm(x).casefold()).isin(team_keys)
    pool=pool[~overlap].copy()
    if pool.text.map(lambda x:norm(x).casefold()).duplicated().any():raise ValueError('Duplicate external text.')
    selected={label:pool[pool.label.eq(label)].sample(frac=1,random_state=42) for label in INTENTS}
    if any(len(rows)<50 for rows in selected.values()):raise ValueError('Need 50 external rows per intent after overlap removal.')
    output.mkdir(parents=True)
    summary=[]
    for cap in [0,20,50]:
        extra=pd.concat([selected[label].head(cap) for label in INTENTS])
        train=pd.concat([tr[['text','label']],extra[['text','label']]],ignore_index=True)
        model=make_pipeline(TfidfVectorizer(analyzer='char',ngram_range=(2,5)),
                            LogisticRegression(max_iter=1000,random_state=42))
        model.fit(train.text,train.label)
        dummy=DummyClassifier(strategy='most_frequent').fit(train.text,train.label)
        scores=classification_score(model,dev,INTENTS)
        baseline=classification_score(dummy,dev,INTENTS)
        name='team_only' if cap==0 else f'team_plus_{cap}_per_intent'
        out=output/name;out.mkdir()
        result=dict(condition=name,team_train_rows=len(tr),external_train_rows=len(extra),
            dev_rows=len(dev),test_evaluated=False,model=scores,majority_baseline=baseline,
            contribution_sha256=sha(data),external_pool_sha256=sha(pool_path),
            removed_external_exact_overlaps=int(overlap.sum()),
            warning='Development comparison only. Near-duplicate/source-group review remains a human check.')
        (out/'dev_metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        extra[['source_record_id','group_id','label']].to_csv(out/'external_selected_ids.csv',index=False)
        pred=dev[['record_id','text','label']].copy();pred['prediction']=model.predict(dev.text)
        pred.to_csv(out/'dev_predictions.csv',index=False,encoding='utf-8-sig')
        # Kept outside deployment artifacts. A deliberate final freeze/promotion is a later step.
        joblib.dump(dict(model=model,dummy=dummy,language=team.language.iloc[0],practice=False,
            track='intent',data_sha256=fingerprint(team),slot_memory={},experiment=name),out/'model.joblib')
        summary.append(dict(condition=name,external_train_rows=len(extra),accuracy=scores['accuracy'],macro_f1=scores['macro_f1']))
    pd.DataFrame(summary).to_csv(output/'comparison.csv',index=False)
    print(pd.DataFrame(summary).to_string(index=False))
    print('Development only. No test predictions or website updates were made.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path,required=True)
    p.add_argument('--external',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    compare(a.data,a.external,a.output)
