"""Fix sample manifests and resource hashes before measuring outcomes."""
import hashlib
import platform
import subprocess
from datetime import datetime, timezone, timedelta
import common as c
import torch

ds=c.RelationDataset(str(c.ROOT/"data/PSG/packed/psg"),"test",resolution=448,max_objects=100)
selected=[]
for predicate,group in c.CFG["e01_groups"].items():
    p=ds.predicate_names.index(predicate)
    for i in range(len(ds)):
        _,_,rels=ds.load_raw(i)
        matches=sorted({tuple(map(int,r[:3])) for r in rels if int(r[2])==p})
        if matches:
            s,o,_=matches[0]
            selected.append({"case_id":f"{predicate.replace(' ','_')}_{sum(x['predicate']==predicate for x in selected)+1}",
                "index":i,"file_name":ds.file_names[i],"s":s,"o":o,"predicate":predicate,**group})
            if sum(x["predicate"]==predicate for x in selected)==c.CFG["e01_samples_per_group"]: break
c.save(c.PROJECT/"manifests/samples.json",{"e01":selected,"subset":c.subset_indices(ds),"test_images":len(ds),"type_partition":c.CFG["spatial_definition"]})
resources={}
for path in [*sorted((c.ROOT/"models/relsgg-vits16plus").glob('*')),c.ROOT/"data/PSG/test_coco.json",c.PROJECT/"configs/experiments.json"]:
    if path.is_file():
        h=hashlib.sha256()
        with path.open('rb') as f:
            while b:=f.read(4*1024**2): h.update(b)
        resources[str(path.relative_to(c.ROOT))]={"bytes":path.stat().st_size,"sha256":h.hexdigest()}
commit=subprocess.check_output(['git','-C',str(c.ROOT/'RelateAnything'),'rev-parse','HEAD'],text=True).strip()
status=subprocess.check_output(['git','-C',str(c.ROOT/'RelateAnything'),'status','--short'],text=True)
gpu=subprocess.check_output(['nvidia-smi','--query-gpu=name,memory.total,memory.free,driver_version','--format=csv,noheader'],text=True).strip()
c.save(c.PROJECT/'manifests/environment.json',{"created":datetime.now(timezone(timedelta(hours=8))).isoformat(),"python":platform.python_version(),"platform":platform.platform(),"torch":torch.__version__,"cuda":torch.version.cuda,"gpu":gpu,"commit":commit,"git_status":status,"resources":resources,"weights_revision":"2db90096be5217bdc7a9003c042950f45723d105","dataset_revision":"8a7e2f92840de2d267244c3ea26fa2daa0772120","command":"python reproduction/scripts/prepare.py"})
(c.PROJECT/'manifests/requirements-lock.txt').write_text(subprocess.check_output([__import__('sys').executable,'-m','pip','freeze'],text=True),encoding='utf-8')
print(f'Prepared {len(selected)} vocabulary cases and {len(c.subset_indices(ds))} perturbation/intervention images.',flush=True)
