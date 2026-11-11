"""Prepare external MASSIVE data; never mix it into contribution.csv or run a model."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import random
import re
import tarfile
import unicodedata

ROOT=Path(__file__).resolve().parent
URL='https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz'
CARD='https://huggingface.co/datasets/AmazonScience/massive'
INTENTS=['weather_query','datetime_query','alarm_set','calendar_set','calendar_query',
         'lists_createoradd','lists_query','play_music','news_query','qa_definition']
FIELDS=['record_id','language','text','label','source_dataset','source_version','source_record_id',
        'source_url','source_partition','group_id','licence','data_role']

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def norm(text):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFC',text)).strip()

def write_csv(path, rows, fields):
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader();writer.writerows(rows)

def prepare(archive, output, team_data):
    archive,output,team_data=map(Path,[archive,output,team_data])
    if output.exists():
        raise ValueError('Use a NEW output directory; prepared datasets are not overwritten.')
    if not team_data.is_file():
        raise ValueError('Supply the team text CSV for exact-overlap checking.')
    with team_data.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if 'text' not in (reader.fieldnames or []):raise ValueError('Team CSV needs a text column.')
        team_keys={norm(row['text']).casefold() for row in reader if row['text'].strip()}
    locale_blob=None
    licence_blob=None
    locale_member=None
    with tarfile.open(archive,'r:gz') as tar:
        for member in tar:
            if not member.isfile():continue
            if member.name.endswith('/sw-KE.jsonl') or member.name=='sw-KE.jsonl':
                if locale_blob is not None:raise ValueError('Multiple Kiswahili members found.')
                locale_member=member.name
                locale_blob=tar.extractfile(member).read()
            if Path(member.name).name in {'LICENSE','LICENSE.txt'}:
                licence_blob=tar.extractfile(member).read()
    if locale_blob is None or licence_blob is None:
        raise ValueError('Expected Kiswahili JSONL and release licence not found in archive.')
    licence_text=licence_blob.decode('utf-8-sig')
    if not (b'creativecommons.org/licenses/by/4.0' in licence_blob or
            ('Copyright Amazon.com Inc. or its affiliates.' in licence_text and
             'Attribution 4.0 International' in licence_text[:200])):
        raise ValueError('Unexpected release licence; inspect before proceeding.')
    partitions=Counter()
    candidates=[]
    exclusions=[]
    seen_ids=set()
    for line in locale_blob.decode('utf-8-sig').splitlines():
        source=json.loads(line)
        if source['locale']!='sw-KE':raise ValueError('Wrong locale in source member.')
        partitions[source['partition']]+=1
        if source['partition']!='train' or source['intent'] not in INTENTS:continue
        sid=str(source['id'])
        if sid in seen_ids:raise ValueError('Duplicate upstream training source ID.')
        seen_ids.add(sid)
        text=norm(source['utt'])
        reasons=[]
        if not text:reasons.append('empty')
        if re.search(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b|(?:\+254|0)[17]\d{8}',text):
            reasons.append('possible_contact_details')
        if text.casefold() in team_keys:reasons.append('exact_overlap_with_team_text')
        row=dict(record_id='MASSIVE-1.1-sw-KE-'+sid,language='sw-KE',text=text,
            label=source['intent'],source_dataset='AmazonScience/MASSIVE',source_version='1.1',
            source_record_id=sid,source_url=URL,source_partition='train',
            group_id='MASSIVE-source-'+sid,licence='CC-BY-4.0',data_role='external_training_only')
        if reasons:exclusions.append(dict(source_record_id=sid,reason=';'.join(reasons)))
        else:candidates.append(row)
    # Remove conflicting labels entirely. Keep only one occurrence of same-label duplicate texts.
    groups=defaultdict(list)
    for row in candidates:groups[row['text'].casefold()].append(row)
    clean=[]
    for group in groups.values():
        group.sort(key=lambda row:row['source_record_id'])
        if len({row['label'] for row in group})>1:
            exclusions.extend(dict(source_record_id=row['source_record_id'],reason='duplicate_text_conflicting_labels') for row in group)
        else:
            clean.append(group[0])
            exclusions.extend(dict(source_record_id=row['source_record_id'],reason='duplicate_text_same_label') for row in group[1:])
    clean.sort(key=lambda row:(row['label'],row['source_record_id']))
    counts=Counter(row['label'] for row in clean)
    if set(counts)!=set(INTENTS):raise ValueError('Not all ten target labels survived filtering.')
    output.mkdir(parents=True)
    (output/'LICENSE.txt').write_bytes(licence_blob)
    write_csv(output/'training_pool.csv',clean,FIELDS)
    write_csv(output/'exclusions.csv',exclusions,['source_record_id','reason'])
    samples={}
    # Nested deterministic samples: first 20 rows are a subset of first 50 for each label.
    shuffled={}
    for label in INTENTS:
        rows=[r for r in clean if r['label']==label]
        random.Random(42).shuffle(rows)
        shuffled[label]=rows
    for cap in [20,50]:
        if any(len(shuffled[label])<cap for label in INTENTS):
            samples[str(cap)]={'available':False,'reason':'Insufficient rows in one or more classes'}
            continue
        sample=[row for label in INTENTS for row in shuffled[label][:cap]]
        name=f'train_{cap}_per_intent.csv'
        write_csv(output/name,sample,FIELDS)
        samples[str(cap)]=dict(available=True,file=name,rows=len(sample),sha256=sha(output/name))
    manifest=dict(dataset='MASSIVE',version='1.1',locale='sw-KE',source_url=URL,
        dataset_card=CARD,archive_sha256=sha(archive),locale_member=locale_member,
        locale_sha256=hashlib.sha256(locale_blob).hexdigest(),licence='CC-BY-4.0',
        source_partition_counts=dict(partitions),selected_partition='train',
        selected_labels=INTENTS,team_csv_sha256=sha(team_data),team_unique_texts=len(team_keys),
        rows=len(clean),per_intent=dict(counts),exclusions=dict(Counter(r['reason'] for r in exclusions)),
        training_pool_sha256=sha(output/'training_pool.csv'),samples=samples,
        status='prepared_external_data_not_trained',
        notes=['Upstream dev/test rows were inspected for partition counts only, never selected for training.',
               'Original source IDs, partitions and group IDs retained; no translations or synthetic examples added.',
               'Exact overlap checked against supplied team snapshot; repeat against FINAL reviewed dataset before fitting.',
               'Near-duplicate/source relationships require further checking before experiments.',
               'Upstream labels retained, not independently reviewed by Team 20.',
               'External rows do not count as new team contributions.'])
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--team-data',type=Path,required=True)
    a=p.parse_args()
    prepare(a.archive,a.output,a.team_data)
