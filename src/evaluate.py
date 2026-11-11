"""Freeze and score the selected model once, only after final-data gates pass."""
import json
import subprocess
import sys
import joblib
import pandas as pd
from src.common import ROOT,sha,INTENTS,classification_score

def evaluate():
    out=ROOT/'reports/test.json'
    freeze_path=ROOT/'models/freeze.json'
    if out.exists() or freeze_path.exists():raise ValueError('Final evaluation/freeze already exists; refusing a repeat.')
    state=json.loads((ROOT/'reports/readiness.json').read_text())
    if not state['ready_for_final_test']:
        raise ValueError('Final test BLOCKED: resolve split minimums, assessment permission and official validation first.')
    # Recheck current evidence rather than trusting a stale/manual readiness edit.
    paths={'raw':'data/raw/responses.xlsx','review_workbook':'data/review/workspace.xlsx',
        'candidates':'data/review/candidates.csv','decisions':'data/review/decisions.csv',
        'metadata':'data/review/metadata.json','permission':'data/review/permission.md'}
    for name,relative in paths.items():
        evidence=ROOT/relative
        if not evidence.is_file() or sha(evidence)!=state.get('evidence_sha256',{}).get(name):
            raise ValueError('Final test BLOCKED: evidence changed since readiness check: '+name)
    metadata=json.loads((ROOT/'data/review/metadata.json').read_text(encoding='utf-8'))
    if metadata.get('permission_confirmed_for_assessment') is not True or metadata.get('language_confirmed') is not True:
        raise ValueError('Final test BLOCKED: current permission/language confirmation is incomplete.')
    data_path=ROOT/'data/processed/reviewed.csv'
    selection=json.loads((ROOT/'models/selection.json').read_text())
    if sha(data_path)!=selection['reviewed_sha256'] or sha(data_path)!=state['reviewed_sha256']:
        raise ValueError('Dataset changed since training.')
    validation=subprocess.run([sys.executable,str(ROOT/'src/starter/validate.py'),'--track','intent','--data',str(data_path)],
        capture_output=True,text=True,encoding='utf-8')
    if validation.returncode:
        raise ValueError('Final test BLOCKED: current dataset fails the official validator. '+validation.stderr.strip().splitlines()[-1])
    path=ROOT/'models'/(selection['condition']+'.joblib')
    if sha(path)!=selection['model_sha256']:raise ValueError('Model fingerprint differs.')
    frame=pd.read_csv(data_path,dtype=str,keep_default_na=False)
    pack=joblib.load(path)
    test=frame[frame.split.eq('test')]
    freeze=dict(condition=selection['condition'],model_sha256=sha(path),reviewed_sha256=sha(data_path))
    # Exclusive creation records the freeze before any test prediction can be made.
    with freeze_path.open('x',encoding='utf-8') as f:json.dump(freeze,f,indent=2)
    result=dict(status='final_test',test_size=len(test),selected_condition=selection['condition'],
        model=classification_score(pack['model'],test,INTENTS),
        majority_baseline=classification_score(pack['dummy'],test,INTENTS),freeze=freeze)
    out.write_text(json.dumps(result,indent=2),encoding='utf-8')
    p=test[['record_id','text','label']].copy();p['prediction']=pack['model'].predict(test.text)
    p.to_csv(ROOT/'reports/test_predictions.csv',index=False,encoding='utf-8-sig')
    print('Final test saved. Do not tune against these results.')

if __name__=='__main__':evaluate()
