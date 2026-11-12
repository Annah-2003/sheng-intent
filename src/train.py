"""Run fair development comparisons; test examples are never scored here."""
import json
import platform
import joblib
import pandas as pd
import sklearn
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from src.common import ROOT,INTENTS,classification_score,key,duplicate_key,sha,fingerprint

def train():
    if (ROOT/'models/freeze.json').exists():raise ValueError('Frozen run exists; refusing retraining.')
    data_path=ROOT/'data/processed/reviewed.csv'
    team=pd.read_csv(data_path,dtype=str,keep_default_na=False)
    state=json.loads((ROOT/'reports/readiness.json').read_text())
    if sha(data_path)!=state['reviewed_sha256']:raise ValueError('Reviewed data fingerprint differs.')
    train=team[team.split.eq('train')];dev=team[team.split.eq('dev')]
    if set(train.label)!=set(INTENTS) or set(dev.label)!=set(INTENTS):raise ValueError('Missing train/dev class.')
    if team.groupby('group_id').split.nunique().gt(1).any():raise ValueError('Group leakage.')
    if team.text.map(duplicate_key).duplicated().any():raise ValueError('Duplicate team text.')
    pool_path=ROOT/'data/external/massive/training_pool.csv'
    external_manifest=json.loads((pool_path.parent/'manifest.json').read_text())
    if sha(pool_path)!=external_manifest['training_pool_sha256']:raise ValueError('External pool checksum differs.')
    pool=pd.read_csv(pool_path,dtype=str,keep_default_na=False)
    if not pool.source_partition.eq('train').all() or not pool.language.eq('sw-KE').all():raise ValueError('Invalid external partition/locale.')
    if set(pool.label)-set(INTENTS):raise ValueError('Invalid external labels.')
    if pool.source_record_id.duplicated().any() or pool.text.map(key).duplicated().any():raise ValueError('Duplicate external rows.')
    overlap=pool.text.map(key).isin(set(team.text.map(key)))
    pool=pool[~overlap]
    # This is a fixed, declared comparison, not a sweep over test outcomes.
    sampled={label:pool[pool.label.eq(label)].sample(frac=1,random_state=42) for label in INTENTS}
    if any(len(rows)<50 for rows in sampled.values()):raise ValueError('Not enough external rows after overlap checks.')
    runs={};predictions=[];selected_ids=[]
    model_dir=ROOT/'models';model_dir.mkdir(exist_ok=True)
    for cap,name in [(0,'baseline'),(20,'massive_20'),(50,'massive_50')]:
        extra=pd.concat([sampled[label].head(cap) for label in INTENTS])
        fitting=pd.concat([train[['text','label']],extra[['text','label']]],ignore_index=True)
        model=make_pipeline(TfidfVectorizer(analyzer='char',ngram_range=(2,5)),LogisticRegression(max_iter=1000,random_state=42))
        model.fit(fitting.text,fitting.label)
        dummy=DummyClassifier(strategy='most_frequent').fit(fitting.text,fitting.label)
        scores=classification_score(model,dev,INTENTS)
        dummy_scores=classification_score(dummy,dev,INTENTS)
        pack=dict(model=model,dummy=dummy,language='Kiswahili/Sheng',track='intent',practice=False,
            slot_memory={},data_sha256=fingerprint(team),reviewed_sha256=sha(data_path),condition=name)
        model_path=model_dir/(name+'.joblib');joblib.dump(pack,model_path)
        runs[name]=dict(team_train_rows=len(train),external_train_rows=len(extra),dev_rows=len(dev),
            model=scores,majority_baseline=dummy_scores,model_sha256=sha(model_path))
        p=dev[['record_id','text','label']].copy();p['condition']=name;p['prediction']=model.predict(dev.text)
        predictions.append(p)
        if cap:
            ids=extra[['source_record_id','label']].copy();ids['condition']=name;selected_ids.append(ids)
    # Highest development macro-F1; exact ties prefer fewer external examples.
    winner=max(runs,key=lambda name:(runs[name]['model']['macro_f1'],-runs[name]['external_train_rows']))
    result=dict(status='development_comparison',test_evaluated=False,selected_condition=winner,runs=runs,
        reviewed_sha256=sha(data_path),external_pool_sha256=sha(pool_path),
        removed_external_exact_overlaps=int(overlap.sum()),python=platform.python_version(),sklearn=sklearn.__version__,
        shortfalls=state['shortfalls'],final_test_ready=state['ready_for_final_test'],
        caveats=['Small development set; selection is uncertain.','Read readiness.json for current split minimums; a preparation snapshot is not a final-test result.',
                 'External near-paraphrase overlap cannot be established by exact matching alone.',
                 'Review decisions are inherited from the human workbook; no claim of perfect labels.'])
    (ROOT/'reports/development.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    pd.concat(predictions).to_csv(ROOT/'reports/development_predictions.csv',index=False,encoding='utf-8-sig')
    pd.concat(selected_ids).to_csv(ROOT/'reports/external_selected_ids.csv',index=False)
    (model_dir/'selection.json').write_text(json.dumps(dict(condition=winner,model_sha256=runs[winner]['model_sha256'],
        reviewed_sha256=sha(data_path),test_evaluated=False),indent=2),encoding='utf-8')
    print(pd.DataFrame([dict(condition=name,accuracy=r['model']['accuracy'],macro_f1=r['model']['macro_f1'],
                            external_rows=r['external_train_rows']) for name,r in runs.items()]).to_string(index=False))
    print('Selected on development data:',winner,'; final test not evaluated.')
    return result

if __name__=='__main__':train()
