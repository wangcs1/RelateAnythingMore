"""Bind real resources and outputs, create and self-verify a portable ZIP."""
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[2];PROJECT=ROOT/'reproduction'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(4*1024**2),b''):h.update(block)
    return h.hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
env=load(PROJECT/'manifests/environment.json')
for name,expected in env['resources'].items():
    p=ROOT/Path(name.replace('\\','/'))
    assert p.is_file() and sha(p)==expected['sha256'],name
resources=[]
for p in sorted((ROOT/'models/relsgg-vits16plus').glob('*'))+sorted((ROOT/'data/PSG/images/test').glob('*')):
    if p.is_file():resources.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
save(PROJECT/'manifests/external_resources.json',{'included_in_zip':False,'resources':resources,
    'reason':'weights/full image set remain external; evidence checking does not need them; inference does'})
save(PROJECT/'manifests/script_hashes.json',{p.name:sha(p) for p in (PROJECT/'scripts').glob('*') if p.is_file()})
conditions=[{'name':'B01','predictions':'reproduction/output/B01_baseline/predictions.jsonl','summary':'reproduction/output/B01_baseline/results.json'},
    {'name':'E03_weight0','predictions':'reproduction/output/E03_pair_weight/weight0_predictions.jsonl','summary':'reproduction/output/E03_pair_weight/results.json','summary_key':'0.0'}]
for exp in ['E02_box_perturbation','E04_image_evidence']:
    for row in load(PROJECT/f'output/{exp}/results.json')['conditions']:
        tag=row.get('tag',row['condition'])
        conditions.append({'name':exp+'/'+tag,'predictions':f'reproduction/output/{exp}/{tag}/predictions.jsonl','summary':f'reproduction/output/{exp}/{tag}/summary.json','summary_key':'summary'})
paths=[]
for dirname in ['scripts','configs','manifests','reports','figures','output']:
    for p in (PROJECT/dirname).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name!='evidence_inventory.json':paths.append(p)
paths.extend([PROJECT/'README.md',PROJECT/'todo.md',ROOT/'data/PSG/test_coco.json'])
paths.extend(p for p in (ROOT/'data/PSG/packed/psg/test').glob('*') if p.is_file())
official=subprocess.check_output(['git','-C',str(ROOT/'RelateAnything'),'ls-files'],text=True).splitlines()
paths.extend(ROOT/'RelateAnything'/p for p in official if (ROOT/'RelateAnything'/p).is_file())
assert not subprocess.check_output(['git','-C',str(ROOT/'RelateAnything'),'status','--short'],text=True).strip()
paths=sorted(set(paths))
manifest={'created':datetime.now(timezone(timedelta(hours=8))).isoformat(),'command':'python reproduction/scripts/package_evidence.py',
    'source_root_at_execution':str(ROOT),'paths':'all file paths below are portable POSIX relative paths',
    'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in paths],
    'conditions':conditions,'input_documents_excluded_from_link_checks':['实验报告审查意见.md'],
    'external_resources_manifest':'reproduction/manifests/external_resources.json',
    'limitations':['No external weights or full inference images bundled','No independent second human review','No Mac GPU rerun','No RA-4M stage generation or training']}
inventory=PROJECT/'manifests/evidence_inventory.json';save(inventory,manifest)
if '--inventory-only' in sys.argv:
    print(f'Inventory refreshed: {len(paths)} files. Final packaging must refresh it again after all reports/checks finish.')
    raise SystemExit(0)
subprocess.run([sys.executable,str(PROJECT/'scripts/verify_evidence.py')],check=True)
dest=PROJECT/'delivery';dest.mkdir(exist_ok=True)
archive=dest/'RelateAnything_evidence_20261016.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4) as z:
    for p in paths+[inventory]:z.write(p,p.relative_to(ROOT).as_posix())
subprocess.run([sys.executable,str(PROJECT/'scripts/verify_evidence.py'),str(archive)],check=True)
save(dest/'package_verification.json',{'archive':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive),
    'files':len(paths)+1,'all_file_hashes_and_32_condition_metrics_checked_in_zip':True})
print(f'Portable verified evidence: {archive} ({archive.stat().st_size/2**20:.1f} MiB)',flush=True)
