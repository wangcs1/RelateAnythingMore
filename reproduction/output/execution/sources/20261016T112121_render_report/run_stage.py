"""Run one stage with exact command, timestamps, hashes, log and exit status."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone, timedelta

ROOT=Path(__file__).resolve().parents[2]
script=sys.argv[1]
assert Path(script).name==script and script.endswith('.py')
path=ROOT/'reproduction/scripts'/script
assert path.is_file()
SHANGHAI=timezone(timedelta(hours=8))
def now(): return datetime.now(SHANGHAI).isoformat()
run_id=datetime.now(SHANGHAI).strftime('%Y%m%dT%H%M%S')+'_'+path.stem
out=ROOT/'reproduction/output/execution';out.mkdir(exist_ok=True,parents=True)
env=dict(os.environ,REPRO_RUN_ID=run_id,PYTHONUTF8='1',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
command=[sys.executable,'-u',str(path),*sys.argv[2:]]
record={'run_id':run_id,'start':now(),'command':command,'cwd':str(ROOT),'script_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'config_sha256':hashlib.sha256((ROOT/'reproduction/configs/experiments.json').read_bytes()).hexdigest(),
        'common_sha256':hashlib.sha256((path.parent/'common.py').read_bytes()).hexdigest(),
        'log':str((out/(run_id+'.log')).relative_to(ROOT)),'end':None,'exit_code':None}
manifest=out/(run_id+'.json')
snapshot=out/'sources'/run_id;snapshot.mkdir(parents=True,exist_ok=True)
for source in sorted((ROOT/'reproduction/scripts').glob('*')):
    if source.is_file(): (snapshot/source.name).write_bytes(source.read_bytes())
record['script_source_snapshot']=str(snapshot.relative_to(ROOT))
manifest.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
with (out/(run_id+'.log')).open('w',encoding='utf-8') as log:
    child=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8')
    for line in child.stdout:
        print(line,end='',flush=True);log.write(line);log.flush()
    code=child.wait()
record.update(end=now(),exit_code=code)
manifest.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(code)
