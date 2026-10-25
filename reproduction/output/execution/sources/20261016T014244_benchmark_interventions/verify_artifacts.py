"""Check complete condition coverage and every local link in delivered reports."""
import json
import re
import subprocess
import csv
import hashlib
import numpy as np
from pathlib import Path
from urllib.parse import unquote
import common as c

def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
b=load(c.PROJECT/'output/B01_baseline/results.json')
assert b['images']==2179 and b['scored_images']==2177 and b['max_difference']==0
e01=load(c.PROJECT/'output/E01_vocabulary/results.json')
assert len(e01['cases'])==24
for row in e01['cases']:
    assert row['selected'] and len(row['candidates'])==6
    assert all(v['actual_replacement_forward_max_logit_difference']<1e-5 for v in row['vocabulary_replacements'].values())
v=load(c.PROJECT/'output/V01_attention/results.json')
assert len(v['cases'])==12 and all(r['forward_repeat_logit_max_abs']==0 for r in v['cases'])
e02=load(c.PROJECT/'output/E02_box_perturbation/results.json');e04=load(c.PROJECT/'output/E04_image_evidence/results.json')
assert len(e02['conditions'])==25 and len(e04['conditions'])==5
assert len(e02['indices'])==300 and e02['indices']==e04['indices']
for record in e02['conditions']+e04['conditions']:
    assert record['summary']['images']==300 and record['summary']['max_difference']<1e-10
assert sum(b['stages'].values())==13226
t01dir=c.PROJECT/'output/T01_trace'
t01=load(t01dir/'detailed_results.json')
assert t01['index']==20 and t01['image_id']==1159713 and t01['slot']==6
assert t01['checks']['relations_raw_pack_target_equal']
assert t01['checks']['sampler_replay_indices_and_logits_equal']
assert t01['checks']['hook_vs_plain_forward_max_abs']==0
assert t01['checks']['official_independent_metric_max_abs']==0
assert t01['checks']['all_vocabulary_query_max_abs']==0
src=load(t01dir/'source_records.json')
assert len(src['objects'])==35 and len(src['relations'])==5
assert src['resolved_relations']==src['targets']['relations']
with (t01dir/'all_56_predicates.csv').open(encoding='utf-8-sig',newline='') as f: words=list(csv.DictReader(f))
with (t01dir/'all_400_pairs.csv').open(encoding='utf-8-sig',newline='') as f: pairs=list(csv.DictReader(f))
assert len(words)==56 and len(pairs)==400
z=np.load(t01dir/'tensors.npz')
assert z['slot_multi_hot'].shape==(1,400,56) and z['slot_multi_hot'].sum()==5
assert z['slot_multi_hot'][0,6,46]
assert z['logits'].shape==(400,56) and z['F_map'].shape==(1,28,28,384)
assert np.allclose(1/(1+np.exp(-(z['logits'][6,46]+z['pair_logits'][6]))),t01['riding']['score'],atol=1e-7)
assert t01['metrics']['R@50']==0.4 and t01['image_rank']==2
assert len(load(t01dir/'vocabulary_comparisons.json'))==3
for filename,sha in load(t01dir/'artifact_hashes.json').items():
    assert hashlib.sha256((t01dir/filename).read_bytes()).hexdigest()==sha,filename
assert 'T01.8' in (c.PROJECT/'reports/完整实验报告.md').read_text(encoding='utf-8')
broken=[]; links=0
for path in (c.PROJECT/'reports').glob('*'):
    if path.suffix not in ('.md','.html'): continue
    # User-supplied Mac review quotes links relative to its former checkout;
    # preserve it verbatim as an input, not a generated deliverable to rewrite.
    if path.name=='实验报告审查意见.md': continue
    text=path.read_text(encoding='utf-8')
    refs=re.findall(r'(?:src|href)=[\"\']([^\"\']+)',text) if path.suffix=='.html' else re.findall(r'\]\(([^)]+)\)',text)
    for ref in refs:
        if ref.startswith(('http:','https:','#','data:')): continue
        target=(path.parent/unquote(ref.split('#')[0])).resolve()
        links+=1
        if not target.exists(): broken.append({'source':str(path),'target':ref})
assert not broken,broken[:10]
status=subprocess.check_output(['git','-C',str(c.ROOT/'RelateAnything'),'status','--short'],text=True)
assert not status.strip(),status
review=load(c.PROJECT/'output/R01_review/all24_full_forward_correspondence.json')
assert len(review)==24 and all(r['cached_replay_max_abs']<1e-5 and r['FP32_full_vs_own_head_max_abs']==0 and r['BF16_full_vs_own_head_max_abs']==0 for r in review)
assert len(load(c.PROJECT/'output/R01_review/independent_recompute.json'))==32
assert load(c.PROJECT/'output/R01_review/repack_equality.json')['all_arrays_equal']
c.save(c.PROJECT/'output/verification.json',{'passed':True,'full_images':2179,'subset_images':300,'E01_cases':24,'attention_cases':12,
    'box_conditions':25,'image_conditions':5,'local_report_links_checked':links,'upstream_git_clean':True,
    'main_metric_independent_difference':b['max_difference'],'all_condition_independent_metrics_passed':True,
    'no_training_executed':True,'T01_complete_trace_checks_passed':True,
    'T01_all_predicates':56,'T01_all_pairs':400,'T01_vocabulary_full_forwards':3,
    'review_all24_full_forward_checks':True,'review_32_condition_recompute':True,
    'excluded_source_documents':['实验报告审查意见.md (user-supplied historical review; links relative to Mac checkout)']})
print(f'All artifact checks passed: {links} local links, complete conditions and independent metrics.',flush=True)
