"""R01 review closure: provenance, replay, independent scoring and uncertainty.

Uses original artifacts, never fabricated outputs. Reannotation is explicitly
post-hoc assistant-only, not an independent human certification.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import html
import importlib.util
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys
import numpy as np
import torch
import common as c

OUT=c.PROJECT/'output/R01_review'
OUT.mkdir(parents=True,exist_ok=True)
def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def rows(path): return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines()]
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dataset_audit():
    ds=c.RelationDataset(str(c.ROOT/'data/PSG/packed/psg'),'test',resolution=448,max_objects=100)
    raw=load(c.ROOT/'data/PSG/test_coco.json');ann=defaultdict(list);rels=defaultdict(list)
    for a in raw['annotations']: ann[a['image_id']].append(a)
    for r in raw['rel_annotations']: rels[r['image_id']].append(r)
    indexmap={int(v[0]):i for i,v in enumerate(ds.img_meta)}
    predmap={r['id']:j for j,r in enumerate(raw['rel_categories'])}
    allimages=[];drops=[];empty=[];relations_dropped=[];trimmed=[]
    for im in raw['images']:
        iid=im['id'];objects=ann[iid][:ds.meta['max_objects']];mapping={a['id']:j for j,a in enumerate(objects)}
        kept=[];drop=[]
        for r in rels[iid]:
            a=mapping.get(r['subject_id']);b=mapping.get(r['object_id'])
            reason='outside_first_40_objects_or_unresolved_id' if a is None or b is None else 'self_loop' if a==b else None
            if reason: drop.append({**r,'reason':reason})
            else: kept.append([a,b,predmap[r['predicate_id']]])
        j=indexmap.get(iid)
        record={'image_id':iid,'file_name':im['file_name'],'index':j,'raw_boxes':len(ann[iid]),'pack_boxes':len(objects) if j is not None else 0,
            'raw_relations':len(rels[iid]),'pack_relations':len(kept) if j is not None else 0,'loaded_relations':0,'drop_reason':None}
        if j is None:
            assert len(objects)<2
            record['drop_reason']='fewer_than_2_boxes';drops.append(record)
        else:
            _,_,r=ds.load_raw(j)
            assert np.array_equal(np.asarray(kept,dtype=np.int64).reshape(-1,3),r[:,:3])
            record['loaded_relations']=len(ds[j][2]['relations'])
            assert record['loaded_relations']==len(kept)
            if len(ann[iid])>ds.meta['max_objects']: trimmed.append(record)
            if not kept: record['drop_reason']='no_relations_after_pack_filters';empty.append(record)
        relations_dropped.extend(drop);allimages.append(record)
    subset=load(c.PROJECT/'manifests/samples.json')['subset']
    unscored=[r for r in empty if r['index'] in subset]
    assert len(drops)==7 and len(empty)==2 and len(unscored)==1
    c.save(OUT/'dataset_lineage.json',{'all_images':allimages,'excluded_images':drops,'unscored_images':empty,
        'subset_unscored':unscored,'truncated_images':trimmed,'dropped_relations':relations_dropped,
        'drop_counts':dict(Counter(r['reason'] for r in relations_dropped)),
        'raw_relation_count':len(raw['rel_annotations']),'packed_relation_count':len(ds.rels),
        'converter':{'commit':subprocess.check_output(['git','-C',str(c.ROOT/'RelateAnything'),'rev-parse','HEAD'],text=True).strip(),
            'sha256':sha(c.ROOT/'RelateAnything/training/pack_megasg.py'),'max_objects':40,'min_rels':0,'dataset_max_objects':100},
        'official_reference_pack':'not available locally: paper 13623 vs public converted 13609 remains unresolved; no manufactured annotations'})
    # Independently invoke the actual official packer into a new audit directory.
    spec=importlib.util.spec_from_file_location('official_pack',c.ROOT/'RelateAnything/training/pack_megasg.py')
    pack=importlib.util.module_from_spec(spec);spec.loader.exec_module(pack)
    pack.pack_split('psg','test',c.ROOT/'data/PSG/test_coco.json',c.ROOT/'data/PSG/images/test',OUT/'repacked',40,0,None)
    for name in ['img_meta','boxes','box_cats','rels']:
        assert np.array_equal(np.load(OUT/f'repacked/{name}.npy'),np.load(ds.split_dir/f'{name}.npy')),name
    assert load(OUT/'repacked/file_names.json')==ds.file_names
    c.save(OUT/'repack_equality.json',{'all_arrays_equal':True,'file_order_equal':True,'metadata_drops':load(OUT/'repacked/meta.json')['drops']})
    print('Dataset lineage and official repack verified',flush=True)

def independent_score(records,weight=1.):
    # Recompute K<=100 metrics from retained ranked top100, independently of
    # stored recall; all GT pair diagnostics allow separate failure validation.
    image_rec={k:[] for k in [20,50,100]};classes={k:defaultdict(list) for k in [20,50,100]}
    stages=Counter()
    for r in records:
        gt={tuple(x) for x in r['gt']}
        if not gt: continue
        ranked={k:{tuple(x[:3]) for x in r['ranked'][:k]} for k in image_rec}
        for k in image_rec:
            hits=gt&ranked[k];image_rec[k].append(len(hits)/len(gt))
            den=Counter(x[2] for x in r['gt']);num=Counter(x[2] for x in hits)
            for p,n in den.items(): classes[k][p].append(num[p]/n)
        selected={tuple(x) for x in r['selected_pairs']}
        diag={(x['s'],x['o'],x['gt_predicate']):x for x in r['diagnostics']}
        for a,b,p in gt:
            d=next(x for x in r['diagnostics'] if x['s']==a and x['o']==b and x['gt_predicate']==PREDICATES[p])
            stage='hit50' if (a,b,p) in ranked[50] else 'not_selected' if (a,b) not in selected else 'wrong_predicate' if d['best_predicate']!=PREDICATES[p] else 'rank_below50'
            assert stage==d['stage'];stages[stage]+=1
    metrics={}
    for k in image_rec:
        rr=float(np.mean(image_rec[k]));mr=float(np.mean([np.mean(v) for v in classes[k].values()]))
        metrics.update({f'R@{k}':rr,f'mR@{k}':mr,f'F1@{k}':2*rr*mr/(rr+mr) if rr+mr else 0})
    return metrics,dict(stages)

def bootstrap_metrics(left,right,replicates=3000):
    assert [r['index'] for r in left]==[r['index'] for r in right]
    left=[r for r in left if r['gt']];right=[r for r in right if r['gt']]
    n=len(left);v=len(PREDICATES)
    def arrays(rr):
        rec=[];cls=np.full((n,v),np.nan)
        for j,r in enumerate(rr):
            gt={tuple(x) for x in r['gt']};hit=gt&{tuple(x[:3]) for x in r['ranked'][:50]}
            rec.append(len(hit)/len(gt));den=Counter(x[2] for x in r['gt']);num=Counter(x[2] for x in hit)
            for p,d in den.items(): cls[j,p]=num[p]/d
        return np.asarray(rec),np.nan_to_num(cls),np.isfinite(cls).astype(float)
    la,lc,mask=arrays(left);ra,rc,rm=arrays(right);assert np.array_equal(mask,rm)
    rng=np.random.default_rng(20261016);deltas=[]
    for start in range(0,replicates,100):
        m=min(100,replicates-start)
        counts=np.asarray([np.bincount(rng.integers(n,size=n),minlength=n) for _ in range(m)])
        denom=counts@mask;present=denom>0
        lmr=(np.divide(counts@lc,denom,out=np.zeros_like(denom),where=present).sum(1)/present.sum(1))
        rmr=(np.divide(counts@rc,denom,out=np.zeros_like(denom),where=present).sum(1)/present.sum(1))
        lr=counts@la/n;rr=counts@ra/n
        lf=2*lr*lmr/np.maximum(lr+lmr,1e-20);rf=2*rr*rmr/np.maximum(rr+rmr,1e-20)
        deltas.extend(np.stack([rr-lr,rmr-lmr,rf-lf],axis=1).tolist())
    ci=np.quantile(deltas,[.025,.975],axis=0)
    return {'scored_images':n,'replicates':replicates,'seed':20261016,'resampling_unit':'image; paired rows and all classes retained',
        'delta':{key:{'point':independent_score(right)[0][key]-independent_score(left)[0][key],
                     'ci95':[float(ci[0,j]),float(ci[1,j])]} for j,key in enumerate(['R@50','mR@50','F1@50'])}}

def statistics():
    base=rows(c.PROJECT/'output/B01_baseline/predictions.jsonl');checks=[]
    conditions=[('B01',base,load(c.PROJECT/'output/B01_baseline/results.json')),
        ('E03_w0',rows(c.PROJECT/'output/E03_pair_weight/weight0_predictions.jsonl'),load(c.PROJECT/'output/E03_pair_weight/results.json')['0.0'])]
    for experiment in ['E02_box_perturbation','E04_image_evidence']:
        for cond in load(c.PROJECT/f'output/{experiment}/results.json')['conditions']:
            name=cond.get('tag',cond['condition']);records=rows(c.PROJECT/f'output/{experiment}/{name}/predictions.jsonl')
            conditions.append((experiment+'/'+name,records,cond['summary']))
    sets={}
    for name,rr,summary in conditions:
        met,stages=independent_score(rr)
        diff=max(abs(met[k]-summary['metrics'][k]) for k in met)
        assert diff<1e-10 and stages==summary['stages'],name
        assert [r['index'] for r in rr if not r['gt']]==([r['index'] for r in base if not r['gt']] if len(rr)==2179 else [r['index'] for r in conditions[2][1] if not r['gt']])
        checks.append({'condition':name,'images':len(rr),'scored_images':sum(bool(r['gt']) for r in rr),'metric_max_abs':diff,'stages_equal':True})
        sets[name]=rr
    c.save(OUT/'independent_recompute.json',checks)
    ci={'E03_weight0_minus_weight1':bootstrap_metrics(base,conditions[1][1])}
    b=sets['E04_image_evidence/original']
    for name in ['blur','grayscale','mean_image','permuted']:
        ci['E04_'+name+'_minus_original']=bootstrap_metrics(b,sets['E04_image_evidence/'+name],1500)
    c.save(OUT/'paired_bootstrap.json',ci)
    print('32 conditions independently rescored; paired image bootstrap complete',flush=True)

def semantic_review():
    annotation=load(c.PROJECT/'configs/e01b_semantic_review.json')
    source=load(c.PROJECT/'output/E01_vocabulary/results.json')
    cases=source['cases'];review=[]
    for r in cases:
        labels=annotation['cases'][r['case_id']];v=r['candidates']
        controls_ok=all(x=='F' for x in labels[2:]);maxneg=max(x['predicate_logit'] for x in v[3:])
        for j in [1,2]:
            review.append({'case_id':r['case_id'],'image_index':r['index'],'phrase':v[j]['phrase'],'semantic_label':labels[j-1],
                'controls_labels':labels[2:],'all_controls_certified_false_by_assistant':controls_ok,
                'original_logit':v[0]['predicate_logit'],'paraphrase_logit':v[j]['predicate_logit'],
                'controls_max_logit':maxneg,'beats_controls':v[j]['predicate_logit']>maxneg,
                'original_beats_controls':v[0]['predicate_logit']>maxneg,'note':annotation['notes'][r['case_id']]})
    rng=np.random.default_rng(20261016);summary={}
    for label in ['E','N','X','U']:
        group=[r for r in review if r['semantic_label']==label]
        valid=[r for r in group if r['all_controls_certified_false_by_assistant']]
        images=sorted({r['image_index'] for r in valid});means=[]
        for _ in range(3000):
            sampled=rng.choice(images,len(images),replace=True) if images else []
            res=[r for image in sampled for r in valid if r['image_index']==image]
            if res: means.append(np.mean([r['beats_controls'] for r in res]))
        summary[label]={'all_comparisons':len(group),'with_confirmed_controls':len(valid),'independent_images':len(images),
            'win_rate':float(np.mean([r['beats_controls'] for r in valid])) if valid else None,
            'original_win_rate':float(np.mean([r['original_beats_controls'] for r in valid])) if valid else None,
            'cluster_bootstrap_ci95':np.quantile(means,[.025,.975]).tolist() if means else None}
    c.save(OUT/'E01b_semantic_strata.json',{'protocol':annotation['protocol'],'categories':annotation['categories'],
        'reviewer':'assistant only; previous scores accessible; not independent blind review','post_hoc':True,
        'annotation_sha256':sha(c.PROJECT/'configs/e01b_semantic_review.json'),'summary':summary,'comparisons':review,
        'strict_independently_validated_synonym_robustness':'not established; second human review not available'})
    # Direction wording probe: show all 24 examples, every original/control and
    # all available swapped-pair scores, including adverse evidence.
    direction=[]
    for r in cases:
        rev=r.get('reverse_pair_followup',{})
        for a,b in zip(r['candidates'],rev.get('candidates',[])):
            direction.append({'case_id':r['case_id'],'s':r['s'],'o':r['o'],'phrase':a['phrase'],
                'forward_logit':a['predicate_logit'],'reverse_logit':b['predicate_logit'],
                'forward_score':a['fused_score'],'reverse_score':b['fused_score'],
                'forward_minus_reverse_logit':a['predicate_logit']-b['predicate_logit']})
    c.save(OUT/'direction_all_cases.json',direction)
    print('E01b post-hoc semantics and all-case direction tables saved',flush=True)

def gpu_review():
    ds,model,E,_=c.setup();cases=load(c.PROJECT/'manifests/samples.json')['e01']
    source={r['case_id']:r for r in load(c.PROJECT/'output/E01_vocabulary/results.json')['cases']}
    allwords=list(dict.fromkeys(w for r in cases for w in r['positive']+r['negative']))
    embeddings=c.encode_texts_student(allwords,str(c.ROOT/'models/relsgg-vits16plus/text_student.pt'),templates=c.TRAIN_TEMPLATES)
    records=[];captures={};attinputs=[];attoutputs=[]
    def semhook(m,a,y): captures['sem']=y.detach().clone()
    def spahook(m,a,y): captures['spa']=y.detach().clone()
    def poolhook(m,args,kwargs,out):
        attinputs.append({k:v.detach().clone() if torch.is_tensor(v) else v for k,v in kwargs.items()})
        attoutputs.append((out[0].detach().clone(),out[1].detach().clone() if out[1] is not None else None))
    h1=model.compose_norm.register_forward_hook(semhook);h2=model.spa_proj.register_forward_hook(spahook)
    route=[]
    for n,r in enumerate(cases):
        model.vocab_head.set_vocabulary_matrix(ds.predicate_names,E);model.reparameterize()
        images,boxes,counts,targets=c.collate_fn([ds[r['index']]])
        attinputs.clear();attoutputs.clear()
        h=model.spatial_pool.cross_attn.register_forward_hook(poolhook,with_kwargs=True)
        out=c.forward(model,images,boxes,counts);h.remove()
        slots={(int(a),int(b)):j for j,(a,b,v) in enumerate(zip(out['sub_idx'][0],out['obj_idx'][0],out['valid_mask'][0])) if v}
        j=slots[r['s'],r['o']];qs=captures['sem'].clone();qp=captures['spa'].clone()
        vocab=r['positive']+r['negative'];W=embeddings[[allwords.index(w) for w in vocab]]
        model.vocab_head.set_vocabulary_matrix(vocab,W);model.reparameterize()
        with torch.inference_mode(): cached=model.vocab_head.score_query_dual(qs.float(),qp.float())
        # Complete FP32 network, compared to its own captured FP32 queries.
        with torch.inference_mode(): full32=model(images.cuda(),boxes.cuda(),counts.cuda(),targets=None)
        sem32=captures['sem'].clone();spa32=captures['spa'].clone()
        with torch.inference_mode(): head32=model.vocab_head.score_query_dual(sem32,spa32)
        diff32=float((full32['logits']-head32).abs().max());assert diff32==0
        # BF16 complete forward with installed six-word vocabulary, then replay
        # head in the SAME autocast context and matrix shape, not cached FP32.
        full16=c.forward(model,images,boxes,counts)
        with torch.inference_mode(),torch.autocast('cuda',dtype=torch.bfloat16):
            head16=model.vocab_head.score_query_dual(captures['sem'],captures['spa'])
        diff16=float((full16['logits']-head16).abs().max());assert diff16==0
        assert torch.equal(full16['sub_idx'],out['sub_idx']) and torch.equal(full16['obj_idx'],out['obj_idx'])
        old=torch.tensor([v['predicate_logit'] for v in source[r['case_id']]['candidates']],device='cuda')
        olddiff=float((cached[0,j]-old).abs().max());assert olddiff<1e-5
        items=[]
        reverse=slots.get((r['o'],r['s']))
        with torch.inference_mode():
            alpha=model.vocab_head.current_alpha().detach().cpu()
            text=model.vocab_head.W.detach().float()
            sem=torch.nn.functional.normalize(qs.float(),dim=-1)@text.T
            spa=torch.nn.functional.normalize(qp.float(),dim=-1)@text.T
        for k,word in enumerate(vocab):
            items.append({'phrase':word,'recorded_cached_FP32_logit':float(old[k]),'replay_cached_FP32_logit':float(cached[0,j,k]),
                'complete_BF16_logit':float(full16['logits'][0,j,k]),
                'complete_FP32_logit':float(full32['logits'][0,j,k]),
                'reverse_cached_FP32_logit':float(cached[0,reverse,k]) if reverse is not None else None,
                'alpha':float(alpha[k]),'text_cos_to_original':float(text[k]@text[0]),
                'forward_semantic_cos':float(sem[0,j,k]),'forward_spatial_cos':float(spa[0,j,k]),
                'reverse_semantic_cos':float(sem[0,reverse,k]) if reverse is not None else None,
                'reverse_spatial_cos':float(spa[0,reverse,k]) if reverse is not None else None})
        # FP32 visual execution may reorder pairs; read by identity for the
        # displayed FP32 comparison rather than assuming the same slot.
        p32={(int(a),int(b)):k for k,(a,b,v) in enumerate(zip(full32['sub_idx'][0],full32['obj_idx'][0],full32['valid_mask'][0])) if v}
        j32=p32.get((r['s'],r['o']))
        for k,item in enumerate(items): item['complete_FP32_logit']=float(full32['logits'][0,j32,k]) if j32 is not None else None
        records.append({'case_id':r['case_id'],'index':r['index'],'slot_BF16':j,'slot_FP32':j32,'reverse_slot_BF16':reverse,
            'cached_replay_max_abs':olddiff,'FP32_full_vs_own_head_max_abs':diff32,'BF16_full_vs_own_head_max_abs':diff16,
            'BF16_same_pair_same_queries_max_abs':float((captures['sem']-qs).abs().max()),'candidates':items,
            'binding':{'image_sha256':sha(ds.img_dir/ds.file_names[r['index']]),'boxes_sha256':hashlib.sha256(boxes.numpy().tobytes()).hexdigest(),
                'model_sha256':sha(c.ROOT/'models/relsgg-vits16plus/model.pth'),'config_sha256':sha(c.PROJECT/'configs/experiments.json'),
                'templates':c.TRAIN_TEMPLATES,'precision':'BF16 visual / FP32 cached head'}})
        if n==0:
            for b,(inp,actual) in enumerate(zip(attinputs,attoutputs)):
                with torch.inference_mode(),torch.autocast('cuda',dtype=torch.bfloat16):
                    default=model.spatial_pool.cross_attn(**inp)
                    explicit=model.spatial_pool.cross_attn(**inp,need_weights=True,average_attn_weights=False)
                    noweights=model.spatial_pool.cross_attn(**inp,need_weights=False)
                d=float((default[0]-actual[0]).abs().max());assert d==0
                route.append({'block':b,'input_shapes':{k:list(v.shape) for k,v in inp.items() if torch.is_tensor(v)},
                    'input_keys':list(inp),'default_need_weights':inspect.signature(model.spatial_pool.cross_attn.forward).parameters['need_weights'].default,
                    'actual_returned_weight_shape':list(actual[1].shape) if actual[1] is not None else None,
                    'captured_default_replay_max_abs':d,'default_vs_explicit_perhead_output_max_abs':float((actual[0]-explicit[0]).abs().max()),
                    'actual_vs_need_weights_false_max_abs':float((actual[0]-noweights[0]).abs().max()),
                    'actual_avg_weights_vs_explicit_head_mean_max_abs':float((actual[1]-explicit[1].mean(1)).abs().max())})
            # Profile actual default pooling call only; no change to need_weights.
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.bfloat16):
                with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU,torch.profiler.ProfilerActivity.CUDA]) as prof:
                    model.spatial_pool.cross_attn(**attinputs[0])
            prof.export_chrome_trace(str(OUT/'attention_actual_trace.json'))
            events=[{'name':e.key,'count':e.count} for e in prof.key_averages()]
            c.save(OUT/'attention_execution.json',{'blocks':route,'profiler_events':events,
                'operator_evidence':[e for e in events if any(w in e['name'].lower() for w in ['attention','softmax','bmm','sdpa','flash'])],
                'actual_contract':'Default need_weights=True, weights returned. Need_weights=False was a deliberate diagnostic alternative, not the original forward.'})
        print(f'GPU replay {n+1}/24 {r["case_id"]} cached diff={olddiff:.3g}, full/head 32/16={diff32}/{diff16}',flush=True)
    h1.remove();h2.remove()
    c.save(OUT/'all24_full_forward_correspondence.json',records)
    # Repeat exact first B01 batch against recorded top100 (same batch padding).
    model.vocab_head.set_vocabulary_matrix(ds.predicate_names,E);model.reparameterize()
    images,boxes,counts,targets=c.collate_fn([ds[i] for i in range(8)])
    out=c.forward(model,images,boxes,counts);aud=c.Audit(ds.predicate_names);aud.update(out,targets,list(range(8)),ds)
    prior=rows(c.PROJECT/'output/B01_baseline/predictions.jsonl')[:8];maxdiff=0
    for a,b in zip(aud.rows,prior):
        assert [x[:3] for x in a['ranked']]==[x[:3] for x in b['ranked']]
        maxdiff=max(maxdiff,max(abs(x[4]-y[4]) for x,y in zip(a['ranked'],b['ranked'])))
    assert maxdiff<1e-5
    c.save(OUT/'B01_fixed_batch_replay.json',{'indices':list(range(8)),'same_batch_shape':True,'top100_triplets_identical':True,'fused_logit_max_abs':maxdiff,'tolerance':1e-5})

PREDICATES=load(c.ROOT/'data/PSG/packed/psg/test/meta.json')['predicates']
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--part',choices=['cpu','gpu','all'],default='all');args=parser.parse_args()
    if args.part in ['cpu','all']: dataset_audit();statistics();semantic_review()
    if args.part in ['gpu','all']: gpu_review()
