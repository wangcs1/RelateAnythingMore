"""Portable, standard-library-only evidence verification. No GPU/torch needed.

python reproduction/scripts/verify_evidence.py [path/to/evidence.zip]
Without an argument, verify the extracted workspace containing this script.
"""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import statistics
import sys
from urllib.parse import unquote
import zipfile

def main():
    archive=zipfile.ZipFile(sys.argv[1]) if len(sys.argv)>1 else None
    root=Path(__file__).resolve().parents[2]
    def read(name): return archive.read(name) if archive else (root/name).read_bytes()
    def load(name): return json.loads(read(name).decode('utf-8'))
    inventory=load('reproduction/manifests/evidence_inventory.json')
    files=inventory['files'];names={r['path'] for r in files}|{'reproduction/manifests/evidence_inventory.json'}
    for row in files:
        data=read(row['path'])
        assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
    metric_checks=[]
    for item in inventory['conditions']:
        records=[json.loads(x) for x in read(item['predictions']).decode('utf-8').splitlines()]
        result=load(item['summary']);result=result[item['summary_key']] if item.get('summary_key') else result
        recalls={k:[] for k in [20,50,100]};cls={k:defaultdict(list) for k in recalls}
        for r in records:
            gt={tuple(x) for x in r['gt']}
            if not gt: continue
            denom=Counter(x[2] for x in r['gt'])
            for k in recalls:
                hit=gt&{tuple(x[:3]) for x in r['ranked'][:k]}
                recalls[k].append(len(hit)/len(gt));num=Counter(x[2] for x in hit)
                for p,n in denom.items():cls[k][p].append(num[p]/n)
        diff=0.
        for k in recalls:
            rr=statistics.mean(recalls[k]);mr=statistics.mean(statistics.mean(v) for v in cls[k].values())
            for key,value in [(f'R@{k}',rr),(f'mR@{k}',mr),(f'F1@{k}',2*rr*mr/(rr+mr) if rr+mr else 0)]:
                diff=max(diff,abs(result['metrics'][key]-value))
        assert diff<1e-10,(item['name'],diff)
        metric_checks.append({'condition':item['name'],'scored_images':len(recalls[50]),'max_abs':diff})
    links=0
    for row in files:
        path=PurePosixPath(row['path'])
        if path.parent.as_posix()!='reproduction/reports' or path.suffix not in ['.md','.html']:continue
        if path.name in inventory['input_documents_excluded_from_link_checks']:continue
        content=read(row['path']).decode('utf-8')
        refs=re.findall(r'(?:src|href)=[\"\']([^\"\']+)',content) if path.suffix=='.html' else re.findall(r'\]\(([^)]+)\)',content)
        for ref in refs:
            if ref.startswith(('http:','https:','#','data:')):continue
            parts=[]
            for part in (path.parent/PurePosixPath(unquote(ref.split('#')[0]))).parts:
                if part=='..':parts.pop()
                elif part!='.':parts.append(part)
            name='/'.join(parts);assert name in names,name;links+=1
    records=[load(r['path']) for r in files if r['path'].startswith('reproduction/output/execution/') and r['path'].endswith('.json')]
    assert records and all(isinstance(r['exit_code'],int) and r['start'] and r['end'] for r in records)
    latest={}
    for r in sorted(records,key=lambda r:r['start']):latest[Path(r['command'][2]).name]=r
    assert all(r['exit_code']==0 for r in latest.values()),latest
    snapshots_checked=0
    for r in records:
        if 'script_source_snapshot' not in r:continue
        snapshot=r['script_source_snapshot'].replace('\\','/')
        script=r['command'][2].replace('\\','/').split('/')[-1]
        assert hashlib.sha256(read(snapshot+'/'+script)).hexdigest()==r['script_sha256']
        assert hashlib.sha256(read(snapshot+'/common.py')).hexdigest()==r['common_sha256']
        snapshots_checked+=1
    print(json.dumps({'passed':True,'files_hashed':len(files),'conditions_recomputed':len(metric_checks),
        'max_metric_difference':max(r['max_abs'] for r in metric_checks),'local_links_checked':links,
        'execution_records_checked':len(records),'execution_source_snapshots_checked':snapshots_checked,
        'failed_attempts_preserved':sum(r['exit_code']!=0 for r in records),
        'latest_attempt_each_stage_passed':True,'external_weights_and_full_images_not_included':True,
        'requires_GPU':False},ensure_ascii=False,indent=2))
    if archive:archive.close()

if __name__=='__main__':main()
