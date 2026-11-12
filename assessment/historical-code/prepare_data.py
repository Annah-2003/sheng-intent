"""Read-only source ingestion. Review decisions are never generated or overwritten."""
import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook

INTENTS = ['weather_query','datetime_query','alarm_set','calendar_set','calendar_query',
           'lists_createoradd','lists_query','play_music','news_query','qa_definition']
ROOT = Path(__file__).resolve().parent

def normalize(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text)).strip()

def prepare(source):
    dest = ROOT / 'private'
    dest.mkdir(exist_ok=True)
    wb = load_workbook(source, read_only=True, data_only=True)
    ws = wb['Form Responses 1']
    rows = list(ws.values)
    headers = rows[0]
    questions = {}
    for col, header in enumerate(headers):
        match = re.match(r'B([1-5])-Q(10|[1-9])\s*\|', str(header))
        if match:
            questions[col] = tuple(map(int, match.groups()))
    if len(questions) != 50:
        raise ValueError('Expected exactly 50 uniquely identified scenario columns.')
    result, exclusions, corrections = [], [], []
    seen = {}
    for row_no, values in enumerate(rows[1:], 2):
        values = tuple(values) + (None,) * (len(headers) - len(values))
        consent = str(values[1] or '')
        for col, (batch, q) in questions.items():
            original = '' if values[col] is None else str(values[col])
            if not original.strip():
                continue
            text = normalize(original)
            rid = f'T20-R{row_no:03d}-B{batch}Q{q:02d}'
            reasons = []
            if consent != 'Yes, I consent and I am 18 or older':
                reasons.append('participation_consent_not_confirmed')
            if str(values[4]) != f'Batch {batch}':
                reasons.append('batch_mismatch')
            if text.casefold() in {'n/a','na','id ask as it is','id not use sheng'}:
                reasons.append('explicit_non_answer')
            if not any(c.isalpha() for c in text):
                reasons.append('no_letters')
            key = text.casefold()
            duplicate_of = seen.get(key, '')
            if duplicate_of:
                reasons.append('duplicate_text')
            else:
                seen[key] = rid
            flags = ['human_label_and_naturalness_check_required']
            if len(text.split()) <= 3:
                flags.append('short_or_context_dependent')
            if re.search(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b|(?:\+254|0)[17]\d{8}', text):
                reasons.append('possible_personal_information')
            if reasons:
                exclusions.append({'record_id':rid,'reason':';'.join(reasons),'duplicate_of':duplicate_of})
            if original != text:
                corrections.append({'record_id':rid,'original_text':original,'normalized_text':text,
                                    'change':'NFC and whitespace only'})
            result.append(dict(record_id=rid,contributor_code=f'T20-R{row_no:03d}',
                source_cell=f'{ws.title}!{ws.cell(1,col+1).column_letter}{row_no}',
                scenario_id=f'B{batch}-Q{q}',scenario_prompt=headers[col],batch=batch,
                original_text=original,text=text,provisional_label=INTENTS[q-1],
                group_id=f'T20-scenario-B{batch}-Q{q}',
                proposed_split='train' if batch in (1,2) else 'dev' if batch == 3 else 'reserved',
                mechanical_exclusion=';'.join(reasons),duplicate_of=duplicate_of,
                review_flags=';'.join(flags),review_status='pending',
                language='Kiswahili/Sheng code-switching',permission_status='participation_confirmed_release_scope_pending'))
    frame = pd.DataFrame(result)
    frame.to_csv(dest/'candidates.csv',index=False,encoding='utf-8-sig')
    pd.DataFrame(exclusions,columns=['record_id','reason','duplicate_of']).to_csv(dest/'mechanical_exclusions.csv',index=False)
    pd.DataFrame(corrections,columns=['record_id','original_text','normalized_text','change']).to_csv(dest/'normalization_log.csv',index=False,encoding='utf-8-sig')
    review_path=dest/'review_decisions.csv'
    if not review_path.exists():
        review=frame[['record_id','contributor_code','scenario_id','original_text','text','provisional_label','review_flags','mechanical_exclusion']].copy()
        for name in ['decision','final_label','reviewer_code','reviewer_independent_of_author','reason','related_group_override']:
            review[name]=''
        review.to_csv(review_path,index=False,encoding='utf-8-sig')
    summary=dict(source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),
        respondents=len(rows)-1,nonblank_answers=len(frame),
        mechanical_exclusions=len(exclusions),provisional_usable=int(frame.mechanical_exclusion.eq('').sum()),
        counts=pd.crosstab(frame.provisional_label,frame.proposed_split).to_dict(),
        note='No human acceptance, review, public-release permission, or final test score is asserted.')
    (dest/'intake_audit.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
    return frame

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    prepare(parser.parse_args().source)
