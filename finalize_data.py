"""Apply genuine review decisions and validate a private contribution export.

Default: inspect only. --export publishes a NEW local output directory, never trains/tests.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unicodedata
import pandas as pd

ROOT = Path(__file__).resolve().parent
INTENTS = ['weather_query','datetime_query','alarm_set','calendar_set','calendar_query',
           'lists_createoradd','lists_query','play_music','news_query','qa_definition']
FIELDS = ['record_id','language','text','label','source_dataset','source_version',
          'source_record_id','source_url','source_method','licence_or_permission',
          'contributor_code','reviewer_code','review_status','group_id','split']

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def key(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text).strip().casefold())

def read_csv(path, required):
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = set(required) - set(frame.columns)
    if missing:
        raise ValueError(f'{Path(path).name}: missing columns {sorted(missing)}')
    if frame.record_id.str.strip().eq('').any() or frame.record_id.duplicated().any():
        raise ValueError(f'{Path(path).name}: missing or duplicate record IDs')
    return frame.set_index('record_id', drop=False)

def inspect(candidates, decisions, config):
    c = read_csv(candidates, ['record_id','text','original_text','provisional_label',
        'contributor_code','scenario_id','group_id','proposed_split','mechanical_exclusion','source_cell'])
    d = read_csv(decisions, ['record_id','text','original_text','provisional_label',
        'contributor_code','scenario_id','decision','final_label','reviewer_code',
        'reviewer_independent_of_author','reason','related_group_override'])
    errors, dispositions, rows = [], [], []
    if set(c.index) != set(d.index):
        errors.append('Review/candidate IDs differ: missing '+str(sorted(set(c.index)-set(d.index)))+
                      '; unknown '+str(sorted(set(d.index)-set(c.index))))
    # Overrides JOIN whole scenario groups; they cannot split one prompt family apart.
    parent = {g:g for g in c.group_id}
    def find(g):
        while parent[g] != g:
            parent[g] = parent[parent[g]]
            g = parent[g]
        return g
    def join(a,b):
        a,b = find(a),find(b)
        parent[max(a,b)] = min(a,b)
    overrides = {}
    for rid in sorted(set(c.index) & set(d.index)):
        source, review = c.loc[rid], d.loc[rid]
        for name in ['text','original_text','provisional_label','contributor_code','scenario_id']:
            if source[name] != review[name]:
                errors.append(f'{rid}: source {name} changed in the reviewer file; adjudicate separately')
        override = review.related_group_override.strip()
        if override:
            if override in overrides:
                join(source.group_id, overrides[override])
            else:
                overrides[override] = source.group_id
    groups = {}
    for _, source in c.iterrows():
        groups.setdefault(find(source.group_id), set()).add(source.proposed_split)
    for group, splits in groups.items():
        if len(splits) > 1:
            errors.append(f'{group}: related scenarios cross proposed splits {sorted(splits)}; resolve before export')
    for rid in sorted(set(c.index) & set(d.index)):
        source, review = c.loc[rid], d.loc[rid]
        decision = review.decision.strip().casefold()
        disposition = decision or 'pending'
        dispositions.append({'record_id':rid,'decision':disposition,'reason':review.reason,
                             'mechanical_exclusion':source.mechanical_exclusion})
        if decision not in {'','accept','exclude','discuss'}:
            errors.append(f'{rid}: unknown decision {decision!r}')
            continue
        if decision in {'exclude','discuss'}:
            if not review.reason.strip() or not review.reviewer_code.strip():
                errors.append(f'{rid}: {decision} needs reviewer_code and reason')
        if decision != 'accept':
            continue  # Pending/discussed/excluded records never enter the contribution file.
        if source.mechanical_exclusion:
            errors.append(f'{rid}: mechanical exclusion remains; cannot accept without separate adjudication')
        label, reviewer = review.final_label.strip(), review.reviewer_code.strip()
        independent = review.reviewer_independent_of_author.strip().casefold()
        if label not in INTENTS:
            errors.append(f'{rid}: accepted row needs a valid final_label')
        if label != source.provisional_label and not review.reason.strip():
            errors.append(f'{rid}: label change needs a reason')
        registry = config.get('reviewers', {}).get(reviewer, {})
        if not reviewer or registry.get('competence_confirmed') is not True:
            errors.append(f'{rid}: actual competent reviewer must be confirmed in config')
        author = source.contributor_code
        authored = registry.get('authored_contributor_codes', [])
        if not isinstance(authored,list):
            errors.append(f'{rid}: reviewer authored_contributor_codes must be a list')
            authored=[]
        if independent == 'yes':
            status = 'independently_reviewed'
            if registry.get('independence_checked') is not True or reviewer == author or author in authored:
                errors.append(f'{rid}: reviewer independence is unconfirmed or conflicts with authorship')
        elif independent == 'no' and reviewer == author:
            status = 'self_reviewed'
        else:
            status = 'unconfirmed'
            errors.append(f'{rid}: accepted review must be confirmed independent or genuinely self-authored')
        split = {'train':'train','dev':'dev','reserved':'test'}.get(source.proposed_split,'')
        if not split:
            errors.append(f'{rid}: invalid proposed split')
        if split == 'test' and status != 'independently_reviewed':
            errors.append(f'{rid}: test record needs independent review')
        rows.append(dict(record_id=rid,language=config.get('language',''),text=source.text,
            label=label,source_dataset=config.get('source_dataset',''),
            source_version=config.get('source_version',''),source_record_id=rid,
            source_url=config.get('source_url','not_applicable'),source_method='original_human',
            licence_or_permission=config.get('licence_or_permission',''),contributor_code=author,
            reviewer_code=reviewer,review_status=status,group_id=find(source.group_id),split=split))
    result = pd.DataFrame(rows, columns=FIELDS)
    if not result.empty:
        duplicates = result.text.map(key).duplicated(keep=False)
        if duplicates.any():
            errors.append('Accepted duplicate texts: '+', '.join(result.loc[duplicates,'record_id']))
    counts = []
    for label in INTENTS:
        for split, minimum in [('train',15),('dev',5),('test',5)]:
            n = int(((result.label == label) & (result.split == split)).sum())
            counts.append(dict(label=label,split=split,accepted=n,minimum=minimum,shortfall=max(0,minimum-n)))
    for field in ['language','source_dataset','source_version','licence_or_permission']:
        if not str(config.get(field,'')).strip():
            errors.append(f'Config: {field} must be supplied from actual records')
    if config.get('language_confirmed') is not True:
        errors.append('Config: confirm the language/variety description')
    if config.get('permission_confirmed_for_assessment') is not True:
        errors.append('Config: permission for intended assessment use is not confirmed')
    evidence = config.get('permission_evidence_path','')
    if not evidence or not Path(evidence).is_file() or Path(evidence).stat().st_size == 0:
        errors.append('Config: supply an existing non-empty private permission-evidence file')
    expected = config.get('candidates_sha256','')
    if expected != digest(candidates):
        errors.append('Config: candidate snapshot hash is missing or differs')
    report = dict(ready_for_export=not errors and all(x['shortfall']==0 for x in counts),
        input_candidates=len(c),accepted=len(result),
        decisions=pd.Series([x['decision'] for x in dispositions]).value_counts().to_dict(),
        errors=errors,counts=counts,
        input_sha256={'candidates':digest(candidates),'decisions':digest(decisions)},
        note='Unreviewed, discussed and excluded records are omitted. No training or final evaluation is run. Assessment clearance is not public-release clearance.')
    return result, report, pd.DataFrame(dispositions)

def run(candidates, decisions, config_path, report_dir, output=None, validator=None):
    config = json.loads(Path(config_path).read_text(encoding='utf-8-sig'))
    frame, report, dispositions = inspect(candidates, decisions, config)
    report_dir = Path(report_dir)
    report_dir.mkdir(parents=True,exist_ok=True)
    (report_dir/'readiness.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    pd.DataFrame(report['counts']).to_csv(report_dir/'class_counts.csv',index=False)
    dispositions.to_csv(report_dir/'decision_log.csv',index=False,encoding='utf-8-sig')
    print(f"Accepted: {report['accepted']}; ready for export: {report['ready_for_export']}")
    print(f"Issues: {len(report['errors'])}; class/split shortfalls: {sum(x['shortfall']>0 for x in report['counts'])}")
    print('Report:',report_dir/'readiness.json')
    if output is not None:
        if not report['ready_for_export']:
            raise ValueError('Export blocked. Resolve readiness.json; no final data was written.')
        output = Path(output).resolve()
        if output.exists():
            raise ValueError('Output already exists. Use a new version directory; frozen exports are not overwritten.')
        validator = Path(validator).resolve()
        if not validator.is_file():
            raise ValueError('Official validator not found')
        output.parent.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
            staging = Path(tmp)/'dataset'
            staging.mkdir()
            path = staging/'contribution.csv'
            frame.to_csv(path,index=False,encoding='utf-8')
            check = subprocess.run([sys.executable,str(validator),'--track','intent','--data',str(path)],
                                   capture_output=True,text=True,encoding='utf-8')
            (report_dir/'validator.txt').write_text(check.stdout+check.stderr,encoding='utf-8')
            if check.returncode:
                raise ValueError('Official validation failed; no final export published. See validator.txt.')
            manifest=dict(status='reviewed_data_validated_not_evaluated',rows=len(frame),
                contribution_sha256=digest(path),inputs=report['input_sha256'],
                config_sha256=digest(config_path),validator_sha256=digest(validator),
                permission_evidence_sha256=digest(config['permission_evidence_path']),
                public_release_cleared=config.get('public_release_cleared') is True)
            (staging/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
            os.rename(staging,output)
        print('Validated private dataset:',output)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidates',type=Path,default=ROOT/'private/candidates.csv')
    p.add_argument('--decisions',type=Path,default=ROOT/'private/review_decisions.csv')
    p.add_argument('--config',type=Path,default=ROOT/'private/finalize_config.json')
    p.add_argument('--report-dir',type=Path,default=ROOT/'private/readiness')
    p.add_argument('--export',type=Path,help='NEW private directory to receive contribution.csv and manifest')
    p.add_argument('--validator',type=Path,default=(ROOT/'datathon-starter-kit/validate.py' if (ROOT/'datathon-starter-kit').exists() else ROOT/'validate.py'))
    args=p.parse_args()
    try:
        run(args.candidates,args.decisions,args.config,args.report_dir,args.export,args.validator)
    except (ValueError,KeyError,OSError) as exc:
        print('STOP:',exc,file=sys.stderr)
        sys.exit(1)
