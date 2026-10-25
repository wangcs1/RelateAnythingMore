"""V01 attention, E01 wording, and a traced real test example. No training."""
import json
import time
import types
import numpy as np
import torch
import common as c

ds,model,E,train_names=c.setup()
cases=json.loads((c.PROJECT/'manifests/samples.json').read_text(encoding='utf-8'))['e01']
start=time.perf_counter()
words=list(dict.fromkeys(w for g in c.CFG['e01_groups'].values() for w in g['positive']+g['negative']))
word_E=c.encode_texts_student(words,str(c.ROOT/'models/relsgg-vits16plus/text_student.pt'),templates=c.TRAIN_TEMPLATES)
word_index={w:i for i,w in enumerate(words)}
cache={}
captures={}
original=model.vocab_head.score_query_dual

def observed(this,q_sem,q_spa):
    captures['q_sem']=q_sem.detach().float().cpu()
    captures['q_spa']=q_spa.detach().float().cpu()
    return original(q_sem,q_spa)

model.vocab_head.score_query_dual=types.MethodType(observed,model.vocab_head)
attention_inputs=[]
scene_capture={}
def scene_pre(module,args,kwargs):
    if 'feature_map' not in scene_capture:
        scene_capture['feature_map']=args[0].detach().float().cpu().numpy()[0]
def pool_pre(module,args,kwargs):
    attention_inputs.append({k:v.detach().clone() if torch.is_tensor(v) else v for k,v in kwargs.items()})

rows=[]; attention_rows=[]; traces=[]
for case_number,case in enumerate(cases):
    index=case['index']
    if index not in cache:
        model.vocab_head.set_vocabulary_matrix(ds.predicate_names,E); model.reparameterize()
        images,boxes,counts,targets=c.collate_fn([ds[index]])
        attention_inputs.clear()
        hook=model.spatial_pool.cross_attn.register_forward_pre_hook(pool_pre,with_kwargs=True)
        out=c.forward(model,images,boxes,counts)
        hook.remove()
        cache[index]={'out':{k:v.cpu() if torch.is_tensor(v) else v for k,v in out.items()},
                      'q_sem':captures['q_sem'].clone(),'q_spa':captures['q_spa'].clone(),'boxes':boxes,'targets':targets}
        image,raw_boxes,_=ds.load_raw(index)
        image_dir=c.PROJECT/'output/E01_vocabulary/images'
        image_dir.mkdir(parents=True,exist_ok=True)
        c.boxed(image,raw_boxes).save(image_dir/f'{index:04d}_all_boxes.jpg')
    item=cache[index]; out=item['out']
    pairslots={(int(s),int(o)):j for j,(s,o,v) in enumerate(zip(out['sub_idx'][0],out['obj_idx'][0],out['valid_mask'][0])) if v}
    slot=pairslots.get((case['s'],case['o']))
    result={**case,'slot':slot,'selected':slot is not None,'context_status':'GT-backed expression group; contextual equivalence/opposition requires visual review; not certified by independent human annotators'}
    if slot is not None:
        vocab=case['positive']+case['negative']
        W=word_E[[word_index[w] for w in vocab]].cuda()
        model.vocab_head.set_vocabulary_matrix(vocab,W); model.reparameterize()
        qs=item['q_sem'][0,slot].cuda(); qp=item['q_spa'][0,slot].cuda()
        with torch.inference_mode():
            alpha=model.vocab_head.current_alpha()
            sem=torch.nn.functional.normalize(qs,dim=-1)@model.vocab_head.W.T
            spa=torch.nn.functional.normalize(qp,dim=-1)@model.vocab_head.W.T
            lg=model.vocab_head.score_query_dual(qs[None],qp[None])[0]
            pair=out['pair_logits'][0,slot].float().cuda()
            fused=lg+pair
        lg=lg.cpu().tolist(); fs=torch.sigmoid(fused).cpu().tolist(); ps=torch.sigmoid(torch.tensor(lg)).tolist()
        order=sorted(range(len(vocab)),key=lambda j:-lg[j]); rank={j:i+1 for i,j in enumerate(order)}
        scores=[{'phrase':w,'role':'positive' if j<3 else 'negative_control','negative_type':None if j<3 else case['neg_types'][j-3],
            'predicate_logit':lg[j],'predicate_sigmoid':ps[j],'pair_logit':float(pair),'fused_logit':float(fused[j]),'fused_score':fs[j],
            'rank':rank[j],'cos_sem':float(sem[j]),'cos_spa':float(spa[j]),'alpha':float(alpha[j]),
            'text_cos_to_original':float(W[j]@W[0]),'exact_in_training_vocabulary':w in train_names} for j,w in enumerate(vocab)]
        result.update({'candidates':scores,'winner':vocab[order[0]],'positive_winner':order[0]<3,
            'original_rank':rank[0],'margin_logit':max(lg[:3])-max(lg[3:]),'paraphrase_logit_range':max(lg[:3])-min(lg[:3]),
            'positive_vs_negative_successes':sum(lg[j]>max(lg[3:]) for j in range(3)),
            'original_above_controls':lg[0]>max(lg[3:]),'paraphrases_above_controls':[lg[j]>max(lg[3:]) for j in (1,2)],
            'text_cosine_matrix':(W@W.T).cpu().tolist()})
        # Separate vocabulary replacement, using the same queries and same pair.
        swaps={}
        for tag,new_vocab in [('original',[vocab[0],*vocab[3:]]),('synonym1',[vocab[1],*vocab[3:]]),('synonym2',[vocab[2],*vocab[3:]]),('expanded',vocab)]:
            ids=[vocab.index(w) for w in new_vocab]
            model.vocab_head.set_vocabulary_matrix(new_vocab,W[ids]);model.reparameterize()
            with torch.inference_mode():
                actual=model.vocab_head.score_query_dual(qs[None],qp[None])[0].cpu()
            difference=float((actual-torch.tensor([lg[j] for j in ids])).abs().max())
            assert difference<1e-5, difference
            swaps[tag]={'vocabulary':new_vocab,'predicate_logits':[lg[j] for j in ids],'fused_scores':[fs[j] for j in ids],
                'winner':max(new_vocab,key=lambda w:lg[vocab.index(w)]),'winner_is_positive':max(ids,key=lambda j:lg[j])<3,
                'actual_replacement_forward_max_logit_difference':difference}
        result['vocabulary_replacements']=swaps
        reverse_slot=pairslots.get((case['o'],case['s']))
        result['reverse_pair_followup']={'selected':reverse_slot is not None,'slot':reverse_slot,'s':case['o'],'o':case['s'],
            'note':'role-direction follow-up validation; not a second independent E01 sample'}
        if reverse_slot is not None:
            model.vocab_head.set_vocabulary_matrix(vocab,W);model.reparameterize()
            with torch.inference_mode():
                rev=model.vocab_head.score_query_dual(item['q_sem'][0,reverse_slot].cuda()[None],item['q_spa'][0,reverse_slot].cuda()[None])[0]
            revpair=float(out['pair_logits'][0,reverse_slot])
            result['reverse_pair_followup'].update({'pair_logit':revpair,'candidates':[{'phrase':w,'predicate_logit':float(rev[j]),'fused_score':float(torch.sigmoid(rev[j]+revpair))} for j,w in enumerate(vocab)]})
    rows.append(result)
    # Re-run official installed PSG vocabulary for attention; observational hook only.
    if sum(x['predicate']==case['predicate'] for x in cases[:case_number+1])<=2:
        model.vocab_head.set_vocabulary_matrix(ds.predicate_names,E); model.reparameterize()
        images,boxes,counts,targets=c.collate_fn([ds[index]])
        attention_inputs.clear()
        scene_capture.clear()
        scene_hook=model.spatial_pool.register_forward_pre_hook(scene_pre,with_kwargs=True)
        hook=model.spatial_pool.cross_attn.register_forward_pre_hook(pool_pre,with_kwargs=True)
        second=c.forward(model,images,boxes,counts); hook.remove()
        scene_hook.remove()
        pairslots={(int(s),int(o)):j for j,(s,o,v) in enumerate(zip(second['sub_idx'][0],second['obj_idx'][0],second['valid_mask'][0])) if v}
        slot=pairslots.get((case['s'],case['o']))
        blocks=[]; discrepancies=[]; bf16_blocks=[]; fp32_discrepancies=[]; output_relative=[]
        for inp in attention_inputs:
            with torch.inference_mode(),torch.autocast('cuda',dtype=torch.bfloat16):
                fast,_=model.spatial_pool.cross_attn(**inp,need_weights=False)
                slow,weights=model.spatial_pool.cross_attn(**inp,need_weights=True,average_attn_weights=False)
            discrepancies.append(float((fast-slow).abs().max()))
            output_relative.append(float((fast-slow).abs().max()/fast.abs().max().clamp(min=1e-6)))
            bf16_blocks.append(weights[0].float().cpu().numpy())
            inp32={k:v.float() if torch.is_tensor(v) and v.is_floating_point() else v for k,v in inp.items()}
            with torch.inference_mode():
                fast32,_=model.spatial_pool.cross_attn(**inp32,need_weights=False)
                slow32,weights32=model.spatial_pool.cross_attn(**inp32,need_weights=True,average_attn_weights=False)
            fp32_discrepancies.append(float((fast32-slow32).abs().max()))
            blocks.append(weights32[0].cpu().numpy())
        # first pooling call is N object queries; second is concatenated union/contact.
        maps={'subject':blocks[0][:,case['s']], 'object':blocks[0][:,case['o']]}
        maps_bf16={'subject':bf16_blocks[0][:,case['s']], 'object':bf16_blocks[0][:,case['o']]}
        if slot is not None:
            K=second['sub_idx'].shape[1]
            maps.update({'union':blocks[1][:,slot],'contact':blocks[1][:,K+slot]})
            maps_bf16.update({'union':bf16_blocks[1][:,slot],'contact':bf16_blocks[1][:,K+slot]})
        dest=c.PROJECT/'output/V01_attention'; dest.mkdir(parents=True,exist_ok=True)
        np.savez_compressed(dest/f'{case["case_id"]}.npz',**maps)
        np.savez_compressed(dest/f'{case["case_id"]}_bf16.npz',**maps_bf16)
        np.savez_compressed(dest/f'{case["case_id"]}_scene.npz',feature_map=scene_capture['feature_map'])
        entropy={name:float(-(a*np.log(np.maximum(a,1e-12))).sum(-1).mean()/np.log(a.shape[-1])) for name,a in maps.items()}
        inside={}
        cx,cy,w,h=boxes[0,case['s']].numpy(); xs=(np.arange(28)+.5)/28; yy,xx=np.meshgrid(xs,xs,indexing='ij')
        for name,boxid in [('subject',case['s']),('object',case['o'])]:
            cx,cy,w,h=boxes[0,boxid].numpy()
            mask=((xx>=cx-w/2)&(xx<=cx+w/2)&(yy>=cy-h/2)&(yy<=cy+h/2)).reshape(-1)
            a=maps[name].mean(0)
            inside[name]={'attention_mass_inside_box':float(a[mask].sum()),'patch_fraction_inside_box':float(mask.mean()),'patches_inside':int(mask.sum())}
        attention_rows.append({**case,'slot':slot,'maps':list(maps),'entropy_normalized':entropy,'box_mass':inside,
            'attention_weight_sum_min':float(min(a.sum(-1).min() for a in maps.values())),
            'attention_weight_sum_max':float(max(a.sum(-1).max() for a in maps.values())),
            'need_weights_vs_fast_output_max_abs':discrepancies,
            'need_weights_vs_fast_output_relative_max':output_relative,
            'fp32_need_weights_vs_fast_output_max_abs':fp32_discrepancies,
            'bf16_vs_fp32_attention_max_abs':[float(np.max(np.abs(a-b))) for a,b in zip(blocks,bf16_blocks)],
            'bf16_vs_fp32_per_region_mean_head_L1':{name:float(np.abs(a-maps_bf16[name]).sum(-1).mean()) for name,a in maps.items()},
            'forward_repeat_logit_max_abs':float((out['logits'].float()-second['logits'].float().cpu()).abs().max()),
            'note':'Displayed weights recomputed in FP32 from captured actual q/k/v. BF16 versus FP32 attention and fast versus explicit MHA errors recorded; original BF16 model forward unchanged. Heads retained, averaged only for display; not bit-identical runtime attribution.'})
        if case_number==0 and slot is not None:
            q=cache[index]['q_sem'][0,slot]; qp=cache[index]['q_spa'][0,slot]
            W=model.vocab_head.W.detach().float().cpu()
            alpha=model.vocab_head.alpha.detach().float().cpu()
            sem=torch.nn.functional.normalize(q,dim=-1)@W.T; spa=torch.nn.functional.normalize(qp,dim=-1)@W.T
            raw=second['logits'][0,slot].float().cpu(); pair=float(second['pair_logits'][0,slot]); p=ds.predicate_names.index(case['predicate'])
            trace={**case,'sample_is_test_not_train':True,'vlm_original':'not available: no claim of regenerated RA-4M annotation',
                'training_mapping':'teaching schematic only; no training performed','gt_records':targets[0]['relations'].tolist(),
                'predicate_index':p,'W_shape':list(W.shape),'W_predicate':case['predicate'],'W_first16':W[p,:16].tolist(),
                'query_shapes':{'semantic':list(q.shape),'spatial':list(qp.shape)},'slot':slot,'logits_shape':list(second['logits'].shape),
                'pair_logit':pair,'alpha':float(alpha[p]),'cos_sem':float(sem[p]),'cos_spa':float(spa[p]),
                'predicate_logit_BF16':float(raw[p]),'fused_score':float(torch.sigmoid(raw[p]+pair)),
                'fixed_pair_best':ds.predicate_names[int(raw.argmax())],
                'GT_rank_in_pair':int((raw>raw[p]).sum())+1,'boxes_cxcywh':boxes[0].tolist()}
            traces.append(trace)
            np.savez_compressed(dest/'traced_vectors.npz',q_sem=q.numpy(),q_spa=qp.numpy(),W=W.numpy(),alpha=alpha.numpy())
    print(f'E01/V01 {case_number+1}/{len(cases)} {case["case_id"]} selected={slot is not None}',flush=True)

model.vocab_head.score_query_dual=original
valid=[r for r in rows if r['selected']]
groups={p:[r for r in valid if r['predicate']==p] for p in c.CFG['e01_groups']}
summary={'selected':len(valid),'total':len(rows),'positive_winner_rate':float(np.mean([r['positive_winner'] for r in valid])),
    'original_beats_controls_rate':float(np.mean([r['original_above_controls'] for r in valid])),
    'paraphrase_each_beats_controls_rate':float(np.mean([v for r in valid for v in r['paraphrases_above_controls']])),
    'replacement_binary_consistency':float(np.mean([r['vocabulary_replacements']['original']['winner_is_positive']==r['vocabulary_replacements'][tag]['winner_is_positive'] for r in valid for tag in ('synonym1','synonym2')])),
    'mean_logit_margin':float(np.mean([r['margin_logit'] for r in valid])),
    'mean_paraphrase_logit_range':float(np.mean([r['paraphrase_logit_range'] for r in valid])),
    'groups':{p:{'n':len(g),'positive_winner_rate':float(np.mean([r['positive_winner'] for r in g])) if g else None,
        'mean_margin':float(np.mean([r['margin_logit'] for r in g])) if g else None} for p,g in groups.items()}}
c.save(c.PROJECT/'output/E01_vocabulary/results.json',{'summary':summary,'cases':rows,'vocabulary':words,'templates':c.TRAIN_TEMPLATES,'seed':42,
    'elapsed_seconds':time.perf_counter()-start,'protocol':'24 GT-backed preselected fixed directed pairs; frozen visual queries, F32 text-head comparison; margins do not establish human correctness or unseen semantics.'})
c.save(c.PROJECT/'output/V01_attention/results.json',{'cases':attention_rows,'traces':traces,'protocol':'prehook observes actual MHA q/k/v; no changed forward; explicitly recomputed weights, heads retained; observational not causal'})
print('Attention and vocabulary artifacts complete.',flush=True)
