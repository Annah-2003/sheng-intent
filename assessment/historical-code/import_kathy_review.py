"""Import the supplied review workbook by source coordinates; preserve all input files."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import pandas as pd
from openpyxl import load_workbook
from finalize_data import digest,key,run
from prepare_data import normalize

ROOT=Path(__file__).resolve().parent

def import_review(workbook,source,output):
    workbook,source,output=map(Path,[workbook,source,output])
    if output.exists():raise ValueError('Choose a NEW import directory.')
    candidates=pd.read_csv(ROOT/'private/candidates.csv',dtype=str,keep_default_na=False)
    lookup={}
    for i,row in candidates.iterrows():
        coord=(int(re.search(r'(\d+)$',row.source_cell).group(1)),row.scenario_id)
        if coord in lookup:raise ValueError('Duplicate candidate source coordinate.')
        lookup[coord]=i
    raw=load_workbook(source,data_only=True).worksheets[0]
    columns={}
    for col,header in enumerate(next(raw.values),1):
        match=re.match(r'(B[1-5]-Q(?:10|[1-9]))\s*\|',str(header))
        if match:columns[match.group(1)]=col
    ws=load_workbook(workbook,data_only=True)['Candidate Records']
    records=list(ws.values)
    decisions=[]
    audit=[]
    seen=set()
    for values in records[1:]:
        row=dict(zip(records[0],values))
        coord=(int(row['original_response_row']),row['prompt_id'])
        if coord not in lookup or coord in seen:raise ValueError('Unknown/duplicate review source coordinate: '+str(coord))
        seen.add(coord)
        match=re.fullmatch(r'response_row_(\d+)_batch_(\d+)_q_(\d+)',row['source_record_id'])
        if not match or (int(match[1]),f'B{match[2]}-Q{match[3]}')!=coord:
            raise ValueError('Inconsistent review source_record_id: '+row['record_id'])
        i=lookup[coord]
        original=raw.cell(coord[0],columns[coord[1]]).value
        if original is None:raise ValueError('Review points to a blank source answer.')
        old=candidates.loc[i,'text']
        candidates.loc[i,'original_text']=str(original)
        candidates.loc[i,'text']=normalize(str(original))
        c=candidates.loc[i]
        decision=str(row['review_decision'] or '').strip().casefold()
        note=str(row['review_notes'] or '').strip()
        edited=key(str(original))!=key(str(row['text'] or ''))
        if edited:
            action='held_edited'; decision_out='discuss'
            reason='Import hold: reviewed wording differs from latest source; excluded pending adjudication.'
        elif decision=='needs_review':
            action='held_pending'; decision_out='discuss'
            reason='Import hold: reviewer left needs_review; excluded for now.'
        elif decision=='rejected':
            action='rejected'; decision_out='exclude'
            reason=note or 'Reviewer marked rejected; detailed reason was not supplied in workbook.'
        elif decision=='accepted' and c.mechanical_exclusion:
            action='held_mechanical'; decision_out='discuss'
            reason='Import hold: existing mechanical exclusion remains: '+c.mechanical_exclusion
        elif decision=='accepted':
            action='accepted'; decision_out='accept'
            reason=note
        else:raise ValueError('Unknown review decision: '+decision)
        if row['label']!=c.provisional_label and not reason:
            raise ValueError('Label changed without note: '+row['record_id'])
        d={name:c[name] for name in ['record_id','contributor_code','scenario_id','original_text',
                                    'text','provisional_label','review_flags','mechanical_exclusion']}
        d.update(decision=decision_out,final_label=row['label'],reviewer_code='T20-KATHY',
            reviewer_independent_of_author='yes',reason=reason,related_group_override='',
            workbook_record_id=row['record_id'],workbook_decision=decision,import_action=action)
        decisions.append(d)
        audit.append(dict(record_id=c.record_id,workbook_record_id=row['record_id'],source_cell=c.source_cell,
            original_export_text=old,latest_source_text=str(original),reviewed_text=str(row['text'] or ''),
            reviewer_decision=decision,import_action=action,reason=reason))
    if len(seen)!=len(candidates):raise ValueError('Not all frozen candidate records appear in review.')
    output.mkdir(parents=True)
    candidates.to_csv(output/'candidates.csv',index=False,encoding='utf-8-sig')
    decisions=pd.DataFrame(decisions)
    decisions.to_csv(output/'review_decisions.csv',index=False,encoding='utf-8-sig')
    pd.DataFrame(audit).to_csv(output/'import_log.csv',index=False,encoding='utf-8-sig')
    config=json.loads((ROOT/'private/finalize_config.json').read_text(encoding='utf-8'))
    config.update(candidates_sha256=digest(output/'candidates.csv'),source_version=digest(source),
        language_confirmed=True,reviewers={'T20-KATHY':dict(competence_confirmed=True,
        independence_checked=True,authored_contributor_codes=[],
        evidence='User identified Kathy as fluent reviewer and confirmed she submitted no responses; workbook decisions imported without model-based relabelling.')})
    (output/'finalize_config.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
    report=run(output/'candidates.csv',output/'review_decisions.csv',output/'finalize_config.json',output/'readiness')
    counts=pd.DataFrame(report['counts'])
    table=counts.pivot(index='label',columns='split',values='accepted').reindex(columns=['train','dev','test'])
    table.to_csv(output/'split_counts.csv')
    summary=dict(workbook_sha256=digest(workbook),source_sha256=digest(source),
        candidate_snapshot_sha256=digest(ROOT/'private/candidates.csv'),
        source_matching='original_response_row + prompt_id; source_record_id cross-checked',
        workbook_decisions=dict(Counter(decisions.workbook_decision)),
        import_actions=dict(Counter(decisions.import_action)),
        accepted=report['accepted'],shortfalls=[r for r in report['counts'] if r['shortfall']],
        unresolved_export_issues=report['errors'],
        note='Original workbooks, original candidate/review CSVs, splits and model are unchanged. Nine new source answers outside the review workbook were not imported. Test means proposed reserved examples, not a final frozen test.')
    (output/'import_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(table.to_string())
    print(json.dumps(summary,indent=2))
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workbook',type=Path,required=True)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    import_review(a.workbook,a.source,a.output)
