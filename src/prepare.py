"""Create a reviewed subset and readiness report. No splitting by score or fabricated review."""
import json
import subprocess
import sys
import pandas as pd
from src.common import ROOT,INTENTS,key,duplicate_key,sha

FIELDS=['record_id','language','text','label','source_dataset','source_version','source_record_id',
        'source_url','source_method','licence_or_permission','contributor_code','reviewer_code',
        'review_status','group_id','split']

def prepare():
    data=ROOT/'data';report_dir=ROOT/'reports'
    report_dir.mkdir(exist_ok=True)
    c=pd.read_csv(data/'review/candidates.csv',dtype=str,keep_default_na=False)
    d=pd.read_csv(data/'review/decisions.csv',dtype=str,keep_default_na=False)
    meta=json.loads((data/'review/metadata.json').read_text(encoding='utf-8'))
    if meta.get('language_confirmed') is not True or not str(meta.get('language','')).strip():
        raise ValueError('Confirm the actual language/variety before preparing accepted data.')
    if sha(data/'raw/responses.xlsx')!=meta.get('source_version'):
        raise ValueError('Raw response workbook differs from the recorded source version.')
    if c.record_id.duplicated().any() or d.record_id.duplicated().any() or set(c.record_id)!=set(d.record_id):
        raise ValueError('Candidate/review IDs must be unique and match exactly.')
    if sha(data/'review/candidates.csv')!=meta['candidates_sha256']:
        raise ValueError('Candidate snapshot differs from recorded metadata.')
    merged=c.merge(d,on='record_id',suffixes=('_source','_review'),validate='one_to_one')
    for field in ['text','original_text','contributor_code','scenario_id','provisional_label']:
        if not merged[field+'_source'].eq(merged[field+'_review']).all():
            raise ValueError('Source/review mismatch: '+field)
    if set(d.decision)-{'accept','exclude','discuss',''}:
        raise ValueError('Unknown review decision.')
    selected=merged[merged.decision.eq('accept')].copy()
    if not selected.mechanical_exclusion_source.eq('').all():raise ValueError('Accepted mechanical exclusion.')
    rows=[]
    for _,r in selected.iterrows():
        registry=meta.get('reviewers',{}).get(r.reviewer_code,{})
        if registry.get('competence_confirmed') is not True:raise ValueError('Unconfirmed competent reviewer.')
        author=r.contributor_code_source
        if r.reviewer_independent_of_author=='yes':
            if registry.get('independence_checked') is not True or author==r.reviewer_code or author in registry.get('authored_contributor_codes',[]):
                raise ValueError('Invalid reviewer independence.')
            status='independently_reviewed'
        elif r.reviewer_independent_of_author=='no' and author==r.reviewer_code:status='self_reviewed'
        else:raise ValueError('Unconfirmed review status.')
        if r.final_label not in INTENTS:raise ValueError('Invalid intent.')
        if r.final_label!=r.provisional_label_source and not r.reason.strip():raise ValueError('Label change needs a reason.')
        if str(r.related_group_override).strip():raise ValueError('Resolve related group overrides in source grouping before preparing.')
        split={'train':'train','dev':'dev','reserved':'test'}.get(r.proposed_split)
        if not split:raise ValueError('Unknown split.')
        if split=='test' and status!='independently_reviewed':raise ValueError('Test must be independent.')
        per_record=meta.get('record_sources',{}).get(r.record_id,{})
        if per_record and per_record.get('permission_confirmed_for_assessment') is not True:
            raise ValueError('Follow-up record permission is unconfirmed: '+r.record_id)
        rows.append(dict(record_id=r.record_id,language=meta['language'],text=r.text_source,label=r.final_label,
            source_dataset=per_record.get('source_dataset',meta['source_dataset']),source_version=per_record.get('source_version',meta['source_version']),source_record_id=r.record_id,
            source_url=meta.get('source_url','not_applicable'),source_method='original_human',
            licence_or_permission=per_record.get('licence_or_permission',meta.get('licence_or_permission')) or 'assessment_scope_pending',
            contributor_code=author,reviewer_code=r.reviewer_code,review_status=status,group_id=r.group_id,split=split))
    frame=pd.DataFrame(rows,columns=FIELDS)
    if frame.empty:raise ValueError('No reviewed accepted records.')
    if frame.text.map(duplicate_key).duplicated().any():raise ValueError('Duplicate accepted text.')
    if frame.groupby('group_id').split.nunique().gt(1).any():raise ValueError('Related groups cross splits.')
    if frame.text.str.contains(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b|(?:\+254|0)[17]\d{8}',regex=True).any():
        raise ValueError('Possible contact details need review.')
    counts=pd.crosstab(frame.label,frame.split).reindex(index=INTENTS,columns=['train','dev','test'],fill_value=0)
    shortages=[dict(label=label,split=split,have=int(counts.loc[label,split]),need=n)
               for label in INTENTS for split,n in [('train',15),('dev',5),('test',5)] if counts.loc[label,split]<n]
    permission_path=data/'review/permission.md'
    permission=(meta.get('permission_confirmed_for_assessment') is True and bool(str(meta.get('licence_or_permission','')).strip())
                and permission_path.is_file() and bool(permission_path.read_text(encoding='utf-8').strip()))
    output=data/'processed/reviewed.csv'
    if (ROOT/'models/freeze.json').exists():raise ValueError('A frozen run exists; create a deliberate new experiment before changing data.')
    frame.to_csv(output,index=False)
    counts.to_csv(report_dir/'split_counts.csv')
    official=subprocess.run([sys.executable,str(ROOT/'src/starter/validate.py'),'--track','intent','--data',str(output)],
                            capture_output=True,text=True,encoding='utf-8')
    (report_dir/'validation.txt').write_text(official.stdout+official.stderr,encoding='utf-8')
    state=dict(accepted=len(frame),split_totals={s:int(counts[s].sum()) for s in counts},shortfalls=shortages,
        permission_for_assessment_confirmed=permission,public_release_confirmed=meta.get('public_release_cleared') is True,
        official_validator_passed=official.returncode==0,ready_for_final_test=not shortages and permission and official.returncode==0,
        reviewed_sha256=sha(output),decisions_sha256=sha(data/'review/decisions.csv'),
        evidence_sha256={name:sha(data/path) for name,path in {
            'raw':'raw/responses.xlsx','review_workbook':'review/workspace.xlsx','candidates':'review/candidates.csv',
            'decisions':'review/decisions.csv','metadata':'review/metadata.json','permission':'review/permission.md'}.items()},
        holds=d.import_action.value_counts().to_dict(),status='reviewed_subset_development_only',test_evaluated=False)
    (report_dir/'readiness.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
    print(counts.to_string());print(json.dumps(state,indent=2))
    return state

if __name__=='__main__':prepare()
