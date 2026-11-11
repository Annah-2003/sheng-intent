"""Development-only experiment. Does not read reserved rows into model fitting/scoring."""
import hashlib
import json
import platform
import sys
from pathlib import Path
import joblib
import pandas as pd
import sklearn
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'datathon-starter-kit'))
from core import INTENTS, classification_score

def train():
    source=ROOT/'private/candidates.csv'
    df=pd.read_csv(source,keep_default_na=False)
    usable=df[df.mechanical_exclusion.eq('')].copy()
    tr=usable[usable.proposed_split.eq('train')].rename(columns={'provisional_label':'label'})
    dev=usable[usable.proposed_split.eq('dev')].rename(columns={'provisional_label':'label'})
    assert set(tr.label)==set(dev.label)==set(INTENTS), 'Missing class in train/dev.'
    assert not set(tr.group_id)&set(dev.group_id), 'Scenario leakage.'
    assert not set(tr.text.str.casefold())&set(dev.text.str.casefold()), 'Duplicate leakage.'
    out=ROOT/'artifacts/preliminary'
    out.mkdir(parents=True,exist_ok=True)
    # Exactly the starter baseline. Later comparisons must use development data only.
    model=make_pipeline(TfidfVectorizer(analyzer='char',ngram_range=(2,5)),
                        LogisticRegression(max_iter=1000,random_state=42))
    model.fit(tr.text,tr.label)
    dummy=DummyClassifier(strategy='most_frequent').fit(tr.text,tr.label)
    result=dict(status='PRELIMINARY_UNREVIEWED',split_policy='B1+B2 train; B3 dev; B4+B5 reserved',
        train_rows=len(tr),dev_rows=len(dev),test_evaluated=False,
        model=classification_score(model,dev,INTENTS),majority_baseline=classification_score(dummy,dev,INTENTS),
        python=platform.python_version(),sklearn=sklearn.__version__,
        input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        limitations=['Provisional scenario labels can be wrong.',
                    'Same respondent may have submitted more than once; identities were not collected.',
                    'Near-duplicate semantic groups still need human review.',
                    'Reserved batches may not meet final class minimums after review.'])
    joblib.dump(dict(model=model,dummy=dummy,language='Kiswahili/Sheng',track='intent',
                     status=result['status'],data_sha256=result['input_sha256']),out/'model.joblib')
    (out/'dev_metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    predictions=dev[['record_id','text','label']].copy()
    predictions['prediction']=model.predict(dev.text)
    predictions['correct']=predictions.label.eq(predictions.prediction)
    predictions.to_csv(out/'dev_predictions.csv',index=False,encoding='utf-8-sig')
    pd.DataFrame(result['model']['report']).T.to_csv(out/'dev_per_label.csv')
    pd.DataFrame(result['model']['confusion_matrix'],index=INTENTS,columns=INTENTS).to_csv(out/'dev_confusion_matrix.csv')
    print(json.dumps({k:result[k] for k in ['status','train_rows','dev_rows','test_evaluated']},indent=2))
    print(f"Dev accuracy {result['model']['accuracy']:.3f}; macro-F1 {result['model']['macro_f1']:.3f}")
    print(f"Majority dev macro-F1 {result['majority_baseline']['macro_f1']:.3f}")
    return result

if __name__=='__main__':
    train()
