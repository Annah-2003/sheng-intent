"""Check the local submission files and recorded model hashes."""
from pathlib import Path
import argparse,hashlib,json,re,sys

def check(root,strict=False):
    errors=[];pending=[]
    required=['README.md','app.py','requirements.txt','ANNOTATION_GUIDE.md','taxonomy.csv','docs/DATASET_CARD.md',
        'docs/QUALITY_REPORT.md','docs/SOURCE_LOG.csv','docs/TEAM.md','docs/DATA_ACCESS.md',
        'docs/RESULTS.md','docs/REPRODUCIBILITY.md','models/selection.json','models/freeze.json',
        'reports/test.json','reports/development.json','reports/split_counts.csv']
    for name in required:
        if not (root/name).is_file():errors.append('Missing '+name)
    readme=(root/'README.md').read_text(encoding='utf-8') if (root/'README.md').exists() else ''
    if 'VIDEO_LINK_TO_ADD' in readme:pending.append('Add and independently verify the recorded video URL.')
    access=(root/'docs/DATA_ACCESS.md').read_text(encoding='utf-8') if (root/'docs/DATA_ACCESS.md').exists() else ''
    if 'ASSESSMENT_ACCESS_TO_ADD' in access or 'TEAM_TO_COMPLETE' in access:
        pending.append('Add the dataset location and retrieval steps.')
    for path in (root/'docs').glob('*.md'):
        text=path.read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if '://' not in link and not link.startswith('#') and not (path.parent/link.split('#')[0]).exists():
                errors.append(f'Broken local link in {path.name}: {link}')
    manifest_path=root/'SUBMISSION_MANIFEST.json'
    if manifest_path.exists():
        manifest=json.loads(manifest_path.read_text())
        for name,expected in manifest['checksums'].items():
            path=root/name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                errors.append('Manifest checksum mismatch: '+name)
        if not re.fullmatch('[0-9a-f]{40}',manifest.get('source_commit_sha','')):
            errors.append('Invalid full source SHA.')
    else:pending.append('Generate the exact source-SHA/file-checksum manifest when packaging.')
    if not errors:
        selected=json.loads((root/'models/selection.json').read_text());final=json.loads((root/'reports/test.json').read_text())
        freeze=json.loads((root/'models/freeze.json').read_text())
        if freeze!=final['freeze'] or freeze['model_sha256']!=selected['model_sha256']:errors.append('Frozen model/result mismatch.')
        model=root/'models'/f"{selected['condition']}.joblib"
        if hashlib.sha256(model.read_bytes()).hexdigest()!=freeze['model_sha256']:errors.append('Selected model checksum mismatch.')
    result={'structural_errors':errors,'pending_file_details':pending,'local_file_checks_passed':not errors and not pending,
        'manual_checks':['Check the repository and data links while signed out.','Check the supplied video link.','Open the official Team 20 submission PR.']}
    print(json.dumps(result,indent=2))
    return 1 if errors else (2 if strict and pending else 0)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--strict',action='store_true');a=p.parse_args()
    sys.exit(check(a.root.resolve(),a.strict))
