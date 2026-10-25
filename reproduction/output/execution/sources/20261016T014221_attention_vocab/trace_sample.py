"""T01: observational, executable PSG annotation -> model -> evaluator trace.

No official source edits, generation, training, or test-time tuning. All forwards
use targets=None. Slot supervision is constructed separately for teaching only.
"""
import csv
import hashlib
import html
import json
import numpy as np
import torch
import torch.nn.functional as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import common as c
from relsgg.training.losses import build_slot_targets
from relsgg.model.geometry import RelGeomEncoder

OUT=c.PROJECT/'output/T01_trace'
FIG=c.PROJECT/'figures'
REPORT=c.PROJECT/'reports'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams['font.sans-serif']=['Microsoft YaHei','DejaVu Sans']
plt.rcParams['axes.unicode_minus']=False
index,s,o,p=20,6,24,46
ds,model,E,train_names=c.setup()
im,raw_boxes,raw_rels=ds.load_raw(index)
images,boxes,counts,targets=c.collate_fn([ds[index]])
meta=[int(x) for x in ds.img_meta[index]]
iid,w,h,b0,nb,r0,nr=meta
source=json.loads((c.ROOT/'data/PSG/test_coco.json').read_text(encoding='utf-8'))
raw_objects=[a for a in source['annotations'] if a['image_id']==iid][:nb]
raw_relations=[r for r in source['rel_annotations'] if r['image_id']==iid]
catnames={x['id']:x['name'] for x in source['categories']}
predmap={x['id']:i for i,x in enumerate(source['rel_categories'])}
idmap={a['id']:j for j,a in enumerate(raw_objects)}
objects=[]
for j,a in enumerate(raw_objects):
    x,y,bw,bh=a['bbox']
    norm=np.array([(x+bw/2)/w,(y+bh/2)/h,bw/w,bh/h])
    assert np.max(np.abs(norm-raw_boxes[j]))<1e-6
    objects.append({'local':j,'global_id':a['id'],'category':catnames[a['category_id']],
                    'raw_xywh':a['bbox'],'packed_cxcywh':raw_boxes[j].tolist(),'absolute_row':b0+j})
mapped=[[idmap[r['subject_id']],idmap[r['object_id']],predmap[r['predicate_id']]] for r in raw_relations]
assert mapped==targets[0]['relations'].tolist()==raw_rels[:,:3].tolist()
c.save(OUT/'source_records.json',{'image':next(x for x in source['images'] if x['id']==iid),
    'objects':raw_objects,'relations':raw_relations,'rel_categories':source['rel_categories'],
    'packed_meta':meta,'resolved_objects':objects,'resolved_relations':mapped,
    'targets':{k:v.tolist() if torch.is_tensor(v) else v for k,v in targets[0].items()}})
del source

# Capture actual executed tensors. Copies preserve BF16 values; no recomputation
# replaces the original model forward. Each handle is removed after one forward.
cap={};handles=[]
def store(name,value):
    if torch.is_tensor(value): cap[name]=value.detach().cpu().clone()
def hook(name):
    def observe(module,args,output): store(name,output)
    return observe
def pool_hook(module,args,kwargs,output):
    j=sum(k.startswith('pool_output_') for k in cap)
    store(f'pool_output_{j}',output);store(f'pool_boxes_{j}',args[1]);store('F_map',args[0])
handles.append(model.spatial_pool.register_forward_hook(pool_hook,with_kwargs=True))
names={'geo_encoder':'geo_encoded','pair_proj':'pair_projected','rel_transformer':'relation_context',
       'deformable_read':'deformable_context','rel_interaction':'interaction_context',
       'compose_norm':'q_sem','spa_proj':'q_spa','sampler.geo_scorer':'geo_scores',
       'sampler.f_sub':'sampler_zs','sampler.f_obj':'sampler_zo',
       'vocab_head.proj':'semantic_projection','sub_text_proj':'subject_projection','obj_text_proj':'object_projection'}
for path,name in names.items(): handles.append(model.get_submodule(path).register_forward_hook(hook(name)))
def pair_pre(module,args): store('pair_input',args[0])
def geo_pre(module,args):
    store('sub_boxes',args[0]);store('obj_boxes',args[1])
def trans_pre(module,args,kwargs): store('box_tokens',kwargs['box_tokens'])
handles.extend([model.pair_proj.register_forward_pre_hook(pair_pre),model.geo_encoder.register_forward_pre_hook(geo_pre),
    model.rel_transformer.register_forward_pre_hook(trans_pre,with_kwargs=True)])
print('T01: original BF16 forward with observational hooks',flush=True)
out=c.forward(model,images,boxes,counts)
for handle in handles: handle.remove()
repeat=c.forward(model,images,boxes,counts)
repeat_diff=float((out['logits']-repeat['logits']).abs().max())
assert repeat_diff==0
slots={(int(a),int(b)):k for k,(a,b,v) in enumerate(zip(out['sub_idx'][0],out['obj_idx'][0],out['valid_mask'][0])) if v}
slot=slots[s,o];K=out['logits'].shape[1]

# Replay the sampler from its real captured MLP outputs in the original dtype.
gs=cap['geo_scores'].cuda().squeeze(-1)
valid=(~torch.eye(nb,device='cuda',dtype=torch.bool)).reshape(1,-1)
geo_masked=gs.masked_fill(~valid,torch.finfo(gs.dtype).min/2)
top1=geo_masked.topk(min(model.sampler.geo_budget,nb*nb),dim=1).indices
zs=cap['sampler_zs'].cuda();zo=cap['sampler_zo'].cuda()
with torch.inference_mode(), torch.autocast('cuda',dtype=torch.bfloat16):
    rel=(zs[:,top1[0]//nb]*zo[:,top1[0]%nb]).sum(-1)/(model.sampler.rel_dim**.5)
top2=rel.topk(K,dim=1).indices
flat=top1.gather(1,top2)
assert torch.equal(flat//nb,out['sub_idx']) and torch.equal(flat%nb,out['obj_idx'])
assert torch.equal(rel.gather(1,top2),out['pair_logits'])
geometry_position=int((top1[0]==s*nb+o).nonzero()[0])+1
geo_value=float(gs[0,s*nb+o]);geo_strict_rank=int((gs[valid]>geo_value).sum())+1

aud=c.Audit(ds.predicate_names);aud.update(out,targets,[index],ds)
audit=aud.rows[0];metrics=aud.compute()
lg=out['logits'][0].float().cpu();pair=out['pair_logits'][0].float().cpu()
fused=lg+pair[:,None];best,bestpred=fused.max(-1)
order=best.topk(len(best)).indices.tolist();rank={k:j+1 for j,k in enumerate(order)}
gtset={tuple(x) for x in mapped}
allpairs=[]
for j in range(K):
    a=int(out['sub_idx'][0,j]);b=int(out['obj_idx'][0,j]);pred=int(bestpred[j])
    allpairs.append({'slot':j,'s':a,'o':b,'geometry_logit':float(gs[0,a*nb+b]),
        'pair_logit':float(pair[j]),'best_id':pred,'best_predicate':ds.predicate_names[pred],
        'predicate_logit':float(lg[j,pred]),'fused_logit':float(best[j]),
        'score':float(torch.sigmoid(best[j])),'image_rank':rank[j],'is_GT':(a,b,pred) in gtset})

W=model.vocab_head.W.detach().float().cpu();alpha=model.vocab_head.current_alpha().detach().float().cpu()
qs=cap['q_sem'].float();qp=cap['q_spa'].float()
sem=F.normalize(qs[0,slot],dim=-1)@W.T
spa=F.normalize(qp[0,slot],dim=-1)@W.T
scale=float(model.vocab_head.logit_scale.detach().exp().clamp(max=100));bias=float(model.vocab_head.logit_bias.detach())
mix=(1-alpha)*sem+alpha*spa
reconstructed=mix*scale+bias
scores=[]
for j,name in enumerate(ds.predicate_names):
    scores.append({'id':j,'phrase':name,'cos_sem_FP32':float(sem[j]),'cos_spa_FP32':float(spa[j]),
        'alpha':float(alpha[j]),'mixed_cos_FP32':float(mix[j]),'scale':scale,'bias':bias,
        'logit_FP32_reconstruction':float(reconstructed[j]),'logit_actual_BF16':float(lg[slot,j]),
        'fused_logit':float(fused[slot,j]),'score':float(torch.sigmoid(fused[slot,j])),
        'within_pair_rank':int((lg[slot]>lg[slot,j]).sum())+1})

# Full end-to-end vocabulary replacement, with identical visual inputs. Unlike
# E01's cached-query head test, this exercises every module again.
words=['riding','riding on','mounted on','carrying a rider','being ridden by','eating',
       'above','below','beside','on','driving on']
wordE=c.encode_texts_student(words,str(c.ROOT/'models/relsgg-vits16plus/text_student.pt'),templates=c.TRAIN_TEMPLATES)
variants={};variant_arrays={}
for tag,vocab in [('expanded',words),('synonym_only',['riding on','being ridden by','eating']),
                 ('original_control',['riding','being ridden by','eating'])]:
    model.vocab_head.set_vocabulary_matrix(vocab,wordE[[words.index(v) for v in vocab]])
    model.reparameterize()
    vh=model.compose_norm.register_forward_hook(hook('variant_q_sem'))
    outv=c.forward(model,images,boxes,counts);vh.remove()
    assert torch.equal(outv['sub_idx'],out['sub_idx']) and torch.equal(outv['obj_idx'],out['obj_idx'])
    qdiff=float((cap['variant_q_sem'].float()-qs).abs().max());assert qdiff==0
    vlg=outv['logits'][0].float().cpu();vpair=outv['pair_logits'][0].float().cpu()
    vf=vlg+vpair[:,None];vb,vp=vf.max(-1);vo=vb.topk(K).indices.tolist()
    srank=vo.index(slot)+1;reverse=slots.get((o,s))
    candidates=[]
    for j,word in enumerate(vocab):
        candidates.append({'phrase':word,'forward_logit':float(vlg[slot,j]),
            'forward_score':float(torch.sigmoid(vf[slot,j])),
            'reverse_logit':float(vlg[reverse,j]) if reverse is not None else None,
            'reverse_score':float(torch.sigmoid(vf[reverse,j])) if reverse is not None else None})
    variants[tag]={'vocabulary':vocab,'queries_max_difference':qdiff,'pairs_identical':True,
        'winner':vocab[int(vp[slot])],'image_rank':srank,'reverse_slot':reverse,'candidates':candidates,
        'top50':[[int(outv['sub_idx'][0,k]),int(outv['obj_idx'][0,k]),vocab[int(vp[k])],float(torch.sigmoid(vb[k]))] for k in vo[:50]]}
    secondary=slots[24,31];secondary_reverse=slots.get((31,24))
    variants[tag]['bicycle_road']={'slot':secondary,'reverse_slot':secondary_reverse,
        'winner':vocab[int(vp[secondary])],'image_rank':vo.index(secondary)+1,
        'candidates':[{'phrase':word,'forward_logit':float(vlg[secondary,j]),
            'forward_score':float(torch.sigmoid(vf[secondary,j])),
            'reverse_logit':float(vlg[secondary_reverse,j]) if secondary_reverse is not None else None,
            'reverse_score':float(torch.sigmoid(vf[secondary_reverse,j])) if secondary_reverse is not None else None}
            for j,word in enumerate(vocab)]}
    variant_arrays[tag+'_logits']=vlg.numpy()
    print('T01: full vocabulary forward',tag,flush=True)
model.vocab_head.set_vocabulary_matrix(ds.predicate_names,E);model.reparameterize()

# Executed pure target mapping, not a training forward/backward or its result.
hot,slotw=build_slot_targets(out['sub_idx'],out['obj_idx'],out['valid_mask'],targets,len(W))
assert bool(hot[0,slot,p]) and int(hot.sum())==len(mapped)
arrays={k:v.float().numpy() for k,v in cap.items() if not k.startswith('variant_')}
geom19=RelGeomEncoder.features(boxes[:,s],boxes[:,o])[0].numpy()
arrays.update(W=W.numpy(),alpha=alpha.numpy(),images=images.numpy(),boxes=boxes.numpy(),
    logits=lg.numpy(),pair_logits=pair.numpy(),sub_idx=out['sub_idx'].cpu().numpy(),obj_idx=out['obj_idx'].cpu().numpy(),
    valid_mask=out['valid_mask'].cpu().numpy(),slot_multi_hot=hot.cpu().numpy(),main_pair_geometry_19=geom19,**variant_arrays)
np.savez_compressed(OUT/'tensors.npz',**arrays)

def csvsave(name,records):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
csvsave('all_56_predicates.csv',scores);csvsave('all_400_pairs.csv',sorted(allpairs,key=lambda x:x['image_rank']))
c.save(OUT/'vocabulary_comparisons.json',variants)
c.save(OUT/'evaluation.json',{'image':audit,'metrics':metrics,'all_pairs':allpairs})

# Images and features: crops only illustrate the boxes. The model actually pools
# global patch features with biased attention; it does not encode these crops.
xy=c.pixel_boxes(raw_boxes,im.size)
union=np.r_[np.minimum(xy[s,:2],xy[o,:2]),np.maximum(xy[s,2:],xy[o,2:])]
inner=np.r_[np.maximum(xy[s,:2],xy[o,:2]),np.minimum(xy[s,2:],xy[o,2:])]
contact=np.r_[np.minimum(inner[:2],inner[2:]),np.maximum(inner[:2],inner[2:])]
regions={'subject':xy[s],'object':xy[o],'union':union,'contact':contact}
im.save(OUT/'original.jpg');c.boxed(im,raw_boxes).save(OUT/'all_boxes.jpg')
Image.fromarray((images[0].permute(1,2,0).numpy()*255).round().astype(np.uint8)).save(OUT/'actual_input_448.png')
pairimage=c.boxed(im,raw_boxes,[s,o]);draw=ImageDraw.Draw(pairimage)
draw.line((tuple(xy[s].reshape(2,2).mean(0)),tuple(xy[o].reshape(2,2).mean(0))),fill='#f97316',width=4)
pairimage.save(OUT/'directed_pair.jpg')
fig,axs=plt.subplots(2,4,figsize=(17,8))
for j,(name,b) in enumerate(regions.items()):
    overlay=im.copy();d=ImageDraw.Draw(overlay);d.rectangle(tuple(b),outline=['red','blue','orange','purple'][j],width=4)
    crop=im.crop(tuple(b));crop.save(OUT/(name+'_crop.png'))
    axs[0,j].imshow(overlay);axs[1,j].imshow(crop)
    axs[0,j].set_title(name+'：全图位置');axs[1,j].set_title('裁剪示意（非实际模型输入）')
    axs[0,j].axis('off');axs[1,j].axis('off')
fig.tight_layout();fig.savefig(FIG/'T01_four_regions.png',dpi=150);plt.close(fig)
vectors={'subject':cap['pool_output_0'][0,s].float().numpy(),'object':cap['pool_output_0'][0,o].float().numpy(),
    'union':cap['pool_output_1'][0,slot].float().numpy(),'contact':cap['pool_output_1'][0,K+slot].float().numpy()}
fig,axs=plt.subplots(2,2,figsize=(14,8))
axs[0,0].imshow(im);axs[0,0].set_title('原始图像');axs[0,0].axis('off')
energy=np.linalg.norm(cap['F_map'].float().numpy()[0],axis=-1)
z=axs[0,1].imshow(energy);fig.colorbar(z,ax=axs[0,1]);axs[0,1].set_title('实际场景 patch 特征 L2 范数（非 attention）')
mat=np.stack(list(vectors.values()));z=axs[1,0].imshow(mat,aspect='auto',cmap='coolwarm');fig.colorbar(z,ax=axs[1,0])
axs[1,0].set_yticks(range(4),list(vectors));axs[1,0].set_title('四区域特征：全部通道、同一色标')
for key,v in [('q_sem',qs[0,slot].numpy()),('q_spa',qp[0,slot].numpy()),('W[riding]',W[p].numpy())]:
    axs[1,1].plot(F.normalize(torch.tensor(v),dim=0).numpy()[:64],label=key,alpha=.8)
axs[1,1].legend();axs[1,1].set_title('归一化查询/文本向量前64维；完整512维见 NPZ')
fig.tight_layout();fig.savefig(FIG/'T01_features.png',dpi=150);plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(16,5));vs=variants['expanded']['candidates']
x=np.arange(len(vs));axs[0].bar(x-.18,[v['forward_logit'] for v in vs],.36,label=f'#{s}→#{o}')
axs[0].bar(x+.18,[v['reverse_logit'] for v in vs],.36,label=f'#{o}→#{s}')
axs[0].set_xticks(x,[v['phrase'] for v in vs],rotation=65);axs[0].legend();axs[0].set_title('同一图片：原向/反向，所有候选逐项对照')
chosen=sorted(scores,key=lambda x:x['within_pair_rank'])[:12]
axs[1].barh([v['phrase'] for v in chosen],[v['logit_actual_BF16'] for v in chosen]);axs[1].invert_yaxis();axs[1].set_title('原始56词表：该物体对 top12')
fig.tight_layout();fig.savefig(FIG/'T01_score_comparison.png',dpi=150);plt.close(fig)

# A standalone presentation figure with actual values in every executed stage.
fig=plt.figure(figsize=(18,15));grid=fig.add_gridspec(2,2,height_ratios=[1,1.55])
ax=fig.add_subplot(grid[0,0]);ax.imshow(pairimage);ax.axis('off');ax.set_title(f'固定真实样本 {iid}：#{s} rider → riding → #{o} bicycle')
ax=fig.add_subplot(grid[0,1]);ax.barh([a['phrase'] for a in vs],[a['forward_logit'] for a in vs],label='原向',alpha=.8)
ax.scatter([a['reverse_logit'] for a in vs],np.arange(len(vs)),marker='x',color='red',label='反向')
ax.invert_yaxis();ax.legend();ax.set_title('新词表：整网重跑，原/反向全部候选')
ax=fig.add_subplot(grid[1,:]);ax.axis('off')
steps=[('1 原始标注与身份',f'PSG test / {nb}框 / {nr}关系\n全局ID {raw_objects[s]["id"]}→{raw_objects[o]["id"]}\n局部 #{s}→#{o} / 原始记录已保存'),
       ('2 pack → Dataset',f'box offset={b0}, relation offset={r0}\ntargets.relations=({s},{o},{p})\n35框/5关系逐项断言一致'),
       ('3 场景与四区域',f'输入448×448 → patch 28×28×384\nsubject/object/union/contact各384维\n拼接19维几何编码 → 2048维pair输入'),
       ('4 候选对采样',f'1190有效有向对 → geometry top400\n主线geometry位置={geometry_position} → 视觉slot={slot}\npair logit={float(pair[slot]):.6f}；重放逐元素一致'),
       ('5 上下文 → 两个查询','pair_proj → transformer → deformable\n→ relation interaction → q_sem/q_spa\n两查询均512维；全部中间张量已保存'),
       ('6 匹配 W[46] = riding',f'W为56×512文本矩阵，alpha={float(alpha[p]):.6f}\nsemantic/spatial cos={float(sem[p]):.4f}/{float(spa[p]):.4f}\n实际logit={float(lg[slot,p]):.6f}（F32解读有舍入差）'),
       ('7 新词表与方向对照','扩展11词 / 原词3词 / 同义替换3词\n全部重跑整网；候选对一致，query差=0\n分数及全图top50全部留存'),
       ('8 评测，不只看成功主线',f'riding对内第1，全图第{rank[slot]}，score={scores[p]["score"]:.7f}\n全图5条GT命中2条：R@50=0.4\n2条谓词替换，1条排名154；双评分器一致')]
for j,(title,body) in enumerate(steps):
    col=j%2;row=j//2;x=.02+.51*col;y=.95-.245*row
    ax.text(x,y,title+'\n'+body,transform=ax.transAxes,ha='left',va='top',fontsize=12,
            bbox={'boxstyle':'round,pad=.7','facecolor':'#eef5ff' if j!=7 else '#ecfdf5','edgecolor':'#64748b'})
    if j%2==0:
        ax.annotate('',xy=(.50,y-.055),xytext=(.43,y-.055),xycoords='axes fraction',arrowprops={'arrowstyle':'->','lw':2,'color':'#64748b'})
    elif j<7:
        ax.annotate('',xy=(.02,y-.195),xytext=(.77,y-.12),xycoords='axes fraction',arrowprops={'arrowstyle':'->','lw':1.4,'color':'#94a3b8','connectionstyle':'angle,angleA=-90,angleB=180,rad=8'})
fig.suptitle('T01：同一样本从真实标注到最终评测（未训练；PSG无对应VLM生成履历）',fontsize=19)
fig.tight_layout();fig.savefig(FIG/'T01_complete_story.png',dpi=170,bbox_inches='tight');fig.savefig(FIG/'T01_complete_story.svg',bbox_inches='tight');plt.close(fig)

# Visual evidence for all three missed GTs, including the same image for both
# the GT statement and actual prediction; do not silently omit failures.
fig,axs=plt.subplots(3,2,figsize=(15,15))
for row,(a,b,g) in enumerate([g for g in mapped if tuple(g) not in {tuple(v[:3]) for v in audit['ranked'][:50]}]):
    j=slots[a,b];bp=int(bestpred[j]);view=c.boxed(im,raw_boxes,[a,b])
    axs[row,0].imshow(view);axs[row,1].imshow(view)
    axs[row,0].set_title(f'GT: #{a} → {ds.predicate_names[g]} → #{b}\nGT logit={float(lg[j,g]):.5f}，对内rank={int((lg[j]>lg[j,g]).sum())+1}')
    axs[row,1].set_title(f'实际: #{a} → {ds.predicate_names[bp]} → #{b}\n全图rank={rank[j]}，pair logit={float(pair[j]):.5f}')
    for ax in axs[row]: ax.axis('off')
fig.tight_layout();fig.savefig(FIG/'T01_missed_GT_comparison.png',dpi=140);plt.close(fig)

feature_stats=[]
for name,v in vectors.items():
    feature_stats.append([name,list(v.shape),float(np.linalg.norm(v)),float(v.min()),float(v.max()),v[:8].round(5).tolist()])
checks={'raw_box_mapping_max_abs':float(max(np.max(np.abs(np.array([(a['bbox'][0]+a['bbox'][2]/2)/w,
    (a['bbox'][1]+a['bbox'][3]/2)/h,a['bbox'][2]/w,a['bbox'][3]/h])-raw_boxes[j])) for j,a in enumerate(raw_objects))),
    'relations_raw_pack_target_equal':True,'sampler_replay_indices_and_logits_equal':True,
    'hook_vs_plain_forward_max_abs':repeat_diff,'official_independent_metric_max_abs':metrics['max_difference'],
    'slot_multi_hot_count':int(hot.sum()),'all_vocabulary_query_max_abs':max(v['queries_max_difference'] for v in variants.values())}
result={'index':index,'image_id':iid,'file_name':ds.file_names[index],'s':s,'o':o,'p':p,'slot':slot,
    'meta':meta,'geometry_topk_position':geometry_position,'geometry_strict_rank':geo_strict_rank,
    'geometry_logit':geo_value,'pair_logit':float(pair[slot]),'image_rank':rank[slot],
    'riding':scores[p],'metrics':metrics['metrics'],'checks':checks,
    'tensor_shapes':{k:list(v.shape) for k,v in arrays.items()},'feature_stats':feature_stats,
    'observed_dtypes':{k:str(v.dtype) for k,v in cap.items() if not k.startswith('variant_')},
    'data_source':'PSG public test; not an RA-4M generation record',
    'training':'no training; build_slot_targets executed separately as a teaching mapping',
    'vlm':'not available for this PSG sample; no generated text substituted for raw records'}
c.save(OUT/'detailed_results.json',result)
c.save(OUT/'results.json',result)

# Produce one substantive chapter in Markdown and HTML from the same values.
md=[];ht=[]
def para(text): md.extend([text,'']);ht.append('<p>'+html.escape(text)+'</p>')
def heading(text): md.extend(['### '+text,'']);ht.append('<h2>'+html.escape(text)+'</h2>')
def table(headers,rows):
    rows=list(rows)
    md.extend(['| '+' | '.join(headers)+' |','|'+'|'.join('---' for _ in headers)+'|'])
    md.extend('| '+' | '.join(str(x).replace('|','/') for x in row)+' |' for row in rows);md.append('')
    ht.append('<table><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</table>')
def picture(path,title): md.extend([f'![{title}]({path})','']);ht.append(f'<h3>{html.escape(title)}</h3><img src="{path}">')
heading('T01.1 设计、固定样本与证据边界')
para('研究问题：同一张图的一个真实关系，能否从原始全局标注 ID 一直追踪到最终召回判定？固定此前 E01 的 riding_1，不根据本次分数重新选成功图片。观测变量是中间张量；对照变量仅为词表和主客体方向。全部前向使用官方权重、448输入、BF16、targets=None，不改网络、不训练、不调阈值。')
para(f'样本 index={index}，image_id={iid}，{im.width}×{im.height}，{nb}个GT框、{nr}条关系。主线 #{s}（{objects[s]["category"]}）→riding→#{o}（{objects[o]["category"]}），另追踪 bicycle→driving on→road 的相对位置/交互关系。driving on不是纯几何空间真值，不把 above/below/beside 候选冒充GT。')
para('这张图来自PSG测试集，不是RA-4M训练样本。不存在属于它的Gemma语义轮/grow轮/空间轮原始记录，所以无法诚实展示“该图的VLM原文→清洗后增量”。此处展示实际PSG原始JSON→官方pack→Dataset链；RA-4M三轮生成属于另一条数据生产链，不能串成这张图的履历。训练标签映射单独执行纯函数作为教学示意，未计算训练loss、反向或更新权重。这遵循指导文件第9.2及第10节对真实记录的要求。')
picture('../figures/T01_complete_story.png','同一样本贯穿全流程主图：各阶段均填入实际执行值')
picture('../output/T01_trace/all_boxes.jpg','原图全部35个固定编号框（无省略）')
picture('../output/T01_trace/directed_pair.jpg','主线有向物体对：红/蓝编号框，橙线连接主体与客体中心')
heading('T01.2 原始JSON、坐标转换与pack逐项对齐')
para(f'img_meta[20]={meta}，顺序为 image_id,width,height,box_offset,box_count,relation_offset,relation_count。局部对象j位于 boxes[{b0}+j]；关系位于 rels[{r0}:{r0+nr}]。原始annotation.id是跨图片全局ID，不能直接作为模型物体索引。按官方pack保留的原始顺序建立 global_id→local_id；predicate_id也必须按rel_categories文件顺序映射。所有框的误差和全部关系一致性均用断言检查。')
para('转换公式：原始像素xywh=(x,y,w,h) → ((x+w/2)/640,(y+h/2)/428,w/640,h/428)。448×448直接方形缩放，横纵比例不同但归一化坐标不变。不是letterbox，不对关系方向做水平翻转。')
table(['local索引','全局annotation.id','类别','原始像素xywh','归一化cxcywh','boxes绝对行'],[[v['local'],v['global_id'],v['category'],v['raw_xywh'],[round(x,6) for x in v['packed_cxcywh']],v['absolute_row']] for v in objects])
table(['原始relation.id','原始subject_id','原始object_id','原始predicate_id','pack/target三元组','谓词字符串'],[[r['id'],r['subject_id'],r['object_id'],r['predicate_id'],v,ds.predicate_names[v[2]]] for r,v in zip(raw_relations,mapped)])
para(f'Dataset实际输出 images={list(images.shape)}，float32范围[{float(images.min()):.4f},{float(images.max()):.4f}]；boxes={list(boxes.shape)}，counts={counts.tolist()}。targets的relations/rel_flags/rel_weights/entity_labels/src完整保存于source_records.json。类别只用于标注解释；该次模型输入没有类别标签，targets也没有传给模型。')
picture('../output/T01_trace/actual_input_448.png','实际送入模型的448×448方形缩放图；与上方原图对照')
heading('T01.3 采样：1190个有向非自身对如何变为400个槽位')
para(f'{nb}×{nb}={nb*nb}个栅格项，去除{nb}个自配对剩{nb*(nb-1)}对。先用19维几何特征的MLP取top400，再以视觉相关性对这400对重排；final_budget也是400，因此本样本第二阶段只重排、不再次减少有效对。真实geo_scorer、f_sub、f_obj输出被保存，按原BF16数值重放两次topk；最终索引及pair logits逐元素完全相等。targets=None，没有GT或反向对强制保留。')
para(f'主线平坦索引={s}×{nb}+{o}={s*nb+o}；geometry logit={geo_value:.8f}，实际geometry topk位置={geometry_position}（严格大于它的分数个数+1为{geo_strict_rank}；BF16同分时不能用排序计数冒充实际topk次序）；视觉重排后slot={slot}（0起始），pair logit={float(pair[slot]):.8f}。相关性公式为 sum(f_sub(v_s)*f_obj(v_o))/sqrt({model.sampler.rel_dim})。')
table(['GT三元组','谓词','采样slot','pair logit','是否保留'],[[g,ds.predicate_names[g[2]],slots.get(tuple(g[:2])),float(pair[slots[tuple(g[:2])]]) if tuple(g[:2]) in slots else None,tuple(g[:2]) in slots] for g in mapped])
para('全部400对的几何分数、pair logit、最佳谓词、融合分数和全图排名都保存于all_400_pairs.csv；不只展示成功的一个槽位。')
table(['19维几何特征编号/含义','软限幅后的实际值'],[[f'{j} / {name}',f'{float(v):.8f}'] for j,(name,v) in enumerate(zip(['dx','dy','log_wr','log_hr','log_ar','log_as','log_ao','IoU','s_in','o_in','asp_s','asp_o','cos_theta','sin_theta','delta_cy','fill_s','fill_o','r_iou','r_contact'],geom19))])
para('几何特征使用官方10*tanh(x/10)软限幅，所以表内fill=1的默认值也会略小于1。混合精度并不表示每个张量均为BF16：实际MLP投影有BF16输出，autocast下的相关性归约为FP32；采样重放保留原dtype及autocast上下文，避免额外BF16舍入改变槽位次序。每个观测张量的dtype见detailed_results.json。')
heading('T01.4 四区域、场景特征与关系上下文')
picture('../figures/T01_four_regions.png','四区域逐一展示：全图框位置与独立裁剪双方对照')
table(['区域','像素xyxy'],[[name,[round(float(x),4) for x in b]] for name,b in regions.items()])
para('union取两框外包络。contact取面对边：max左上/min右下后求中心、宽高取绝对值；重叠时是交集，不重叠时是间隙。它是几何区域，不是人体姿态估计得到的真实接触点。上面的裁剪只帮助理解区域；实际模型对整图patch特征做SoftSpatialPool，query带区域偏置，不是把四张裁剪分别送入骨干。')
picture('../figures/T01_features.png','实际场景与区域特征：统一尺度的完整通道及查询片段')
table(['实际区域向量','shape','L2范数','最小值','最大值','前8维'],feature_stats)
table(['真实观测张量','shape'],[[name,list(cap[name].shape)] for name in ['F_map','pool_output_0','pool_output_1','geo_encoded','box_tokens','pair_input','pair_projected','relation_context','deformable_context','interaction_context','q_sem','q_spa']])
para('pair_input按subject、object、union、contact、geo顺序拼接，再经pair_proj。relation transformer读取全图与4个角点token；deformable_read以四区域为anchors读取；rel_interaction让关系对结合全局场景互动。每一步都保存真实输出，不用手画一个“关系特征”方框代替证据。向量通道没有单独可命名的语义，范数/热图只用于数值检查，不能据此宣称某通道代表骑行。')
para('区域attention另见V01_attention页面的riding_1部分：原图、四区域heatmap、各head和BF16/FP32差异均已保留。attention展示query读取位置，不等于最终预测的因果归因。')
picture('../figures/V01_riding_1.png','同一对物体：原图与subject/object/union/contact实际query注意力对照（FP32诊断重算）')
picture('../figures/V01_heads_riding_1.png','同一对物体的全部attention heads；注意色标按各图归一化')
heading('T01.5 双查询与W：把每一个分数拆开算')
para(f'语义查询 q_sem=compose_norm(proj(r)+g_s*sub_text_proj(v_s)+g_o*obj_text_proj(v_o))，实际gate={model.compose_gate.detach().float().cpu().tolist()}；空间查询q_spa=spa_proj(concat(r,geo))。两者均512维。W形状={list(W.shape)}，W[46]是文本编码器对“riding”及官方模板编码后安装的单位文本向量，不是类别编号46的可训练分类器列；前16维={W[p,:16].tolist()}。完整查询、W和alpha已保存，下面每个词都给两分支数值。')
para(f'cos_p=(1-alpha_p)*cos(q_sem,W[p])+alpha_p*cos(q_spa,W[p])；logit=cos_p*{scale:.8f}+({bias:.8f})；最终score=sigmoid(logit+pair_logit)。alpha依赖文本谓词，非本图的可视化attention。FP32解读时riding：semantic cos={float(sem[p]):.8f}，spatial cos={float(spa[p]):.8f}，alpha={float(alpha[p]):.8f}，重构logit={float(reconstructed[p]):.8f}；实际BF16前向logit={float(lg[slot,p]):.8f}，差={float(lg[slot,p]-reconstructed[p]):+.8f}。这是dtype和矩阵运算舍入差异，实际评测始终使用前向值，不用FP32讲解值替换。')
table(['id/词','semantic cos(F32)','spatial cos(F32)','alpha','混合cos(F32)','重构logit(F32)','实际logit(BF16)','融合score','对内rank'],[[f"{v['id']} / {v['phrase']}",*[f"{v[k]:.6f}" for k in ['cos_sem_FP32','cos_spa_FP32','alpha','mixed_cos_FP32','logit_FP32_reconstruction','logit_actual_BF16','score']],v['within_pair_rank']] for v in sorted(scores,key=lambda v:v['within_pair_rank'])])
heading('T01.6 新词表：实际整网重跑与方向反转双方完整展示')
para('这是本次新增的完整整网前向，不是只拿已缓存query做示意：分别安装扩展11词、仅同义替换3词、原词控制3词，然后用同样图像和框重新运行。三次的候选对索引完全相同，q_sem最大差均为0。空间候选above/below/beside仅测试候选竞争，不计为PSG真值，也不把mounted on自动认定为每个语境下等价。')
picture('../figures/T01_score_comparison.png','原向/反向全部11候选对照，及原56词表top12')
for tag,v in variants.items():
    para(f"词表条件 {tag}：{v['vocabulary']}；原向winner={v['winner']}；在该词表下的全图关系对排名={v['image_rank']}；反向slot={v['reverse_slot']}。同一词在原向和反向的pair logit不同，因此同时展示谓词logit与融合score。")
    table(['候选短语',f'#{s}→#{o} logit',f'#{o}→#{s} logit',f'#{s}→#{o} score',f'#{o}→#{s} score'],[[a['phrase'],*[f'{a[k]:.7f}' if a[k] is not None else '未采样' for k in ['forward_logit','reverse_logit','forward_score','reverse_score']]] for a in v['candidates']])
v=variants['expanded']['bicycle_road']
para(f'同图第二条支线：#24 bicycle→#31 road，GT为driving on；扩展词表下winner={v["winner"]}，全图rank={v["image_rank"]}。此处特别比较一般支撑关系on、动作driving on及above/below/beside等空间候选；反向若没有被几何采样选中明确标注未采样，而不人为强制加入。')
table(['全部扩展短语','#24→#31 logit','#31→#24 logit','#24→#31 score','#31→#24 score'],[[a['phrase'],*[f'{a[k]:.7f}' if a[k] is not None else '未采样' for k in ['forward_logit','reverse_logit','forward_score','reverse_score']]] for a in v['candidates']])
para('新词表没有重新训练，也没有统一的GT同义词标注；不能把其11词下的胜出率当作原56类R@50。它检验的是当前图与固定物体对的字符串替换/方向敏感性；完整各条件top50和400×V logits也已保存。比较不同大小矩阵的BF16结果时，共同词可能有微小舍入差，不能将其解释为视觉查询发生变化。')
heading('T01.7 真正的评测判定：对内第一不等于全图命中')
para('本协议graph_constraint=True：每个采样物体对只保留最佳一个谓词，再按predicate logit+pair logit在整张图跨对排序取K。用官方SGClsEvaluator及独立集合交集实现双算；以下显示所有5条GT，未命中项也保留。GT精确匹配subject index、object index、predicate index；不存在文本同义宽松匹配。')
grows=[]
for g in mapped:
    j=slots.get(tuple(g[:2]));bp=int(bestpred[j]) if j is not None else None
    grows.append([g,ds.predicate_names[g[2]],j,ds.predicate_names[bp] if bp is not None else None,rank.get(j),
        *[(j is not None and bp==g[2] and rank[j]<=k) for k in [20,50,100]]])
table(['全部GT','GT词','slot','该对最佳词','该对全图rank','hit20','hit50','hit100'],grows)
picture('../figures/T01_missed_GT_comparison.png','全部3条漏召回：每一行同时展示GT与实际预测双方')
para('具体失败一：#12→looking at→#13被采样且对内最佳正确，但全图排154，top100仍未命中；其predicate logit=-0.25470，pair logit=-1.40863，属于排序失败。失败二：#16→driving on→#31，实际最佳on排44，GT词对内第9；进入top50也因严格谓词不同而失败。失败三：#24→driving on→#31同样被on替代，on排58且GT词第9；单纯扩大K也不能使graph constraint保留的on变为driving on。两种机制不同，不能统称采样漏对。')
table(['K','本图R@K','本图mR@K','本图F1@K'],[[k,*[f"{metrics['metrics'][f'{m}@{k}']:.8f}" for m in ['R','mR','F1']]] for k in [20,50,100]])
para(f'主线riding在56词表中对内排名={scores[p]["within_pair_rank"]}，全图排名={rank[slot]}，最终score={scores[p]["score"]:.9f}。本图宏平均仅用于讲解，不是2179图总体指标；全局mR需要累积每类在各图的召回后再按类平均，不能简单平均各图mR。')
baseline_row=next(json.loads(line) for line in (c.PROJECT/'output/B01_baseline/predictions.jsonl').open(encoding='utf-8') if json.loads(line)['index']==index)
para(f'与既有B01的区别：B01使用batch8，本次为方便诊断使用batch1。B01主线score={next(v[3] for v in baseline_row["ranked"] if v[:3]==[s,o,p]):.9f}，本次={scores[p]["score"]:.9f}；批形状引起混合精度微小数值差，不能宣称与B01 logits逐位相同。本图B01与T01的R20/R50/R100均为0.4，主线排名均为2。官方主表仍保留原B01完整结果，不拿T01替换。')
table(['全图rank','slot','subject→predicate→object','predicate logit','pair logit','融合score','精确GT'],[[v['image_rank'],v['slot'],f"#{v['s']}→{v['best_predicate']}→#{v['o']}",f"{v['predicate_logit']:.6f}",f"{v['pair_logit']:.6f}",f"{v['score']:.7f}",v['is_GT']] for v in sorted(allpairs,key=lambda v:v['image_rank'])[:50]])
para('语境解释：这张拥挤车队图中，骑手与自行车有明确骑乘交互，road框提供道路语境；遮挡使“具体哪位骑手对应哪辆车”仍需按编号检查。骑手→骑车的高分符合图像，但高分不证明模型理解了因果动作。top50中大量未标注关系不能一律认定为错误；反过来，GT若被不同最佳词替代，即使语义看起来合理，严格协议仍判漏召回。以上逐GT表给出是采样、谓词选择还是全图排序造成的结果，不凭单个成功关系推广整体。')
heading('T01.8 教学监督映射、核查结果与复跑入口')
para(f'单独调用官方build_slot_targets（纯标签映射，无训练）得到multi_hot shape={list(hot.shape)}，共{int(hot.sum())}个正单元；主线[0,{slot},46]=True，其余未标注单元不等于经过人工确认的负例。用此测试样本说明张量结构不授权训练；未执行训练forward、loss、backward或optimizer.step，也不声称训练采样强制GT策略在此推理中生效。')
table(['核查项','实测'],checks.items())
para('复跑：在工作区执行 .\\reproduction\\scripts\\run_all.ps1 -Stages trace_sample.py,render_report.py,verify_artifacts.py 。独立脚本trace_sample.py是唯一新增诊断入口，不改官方源码。原始证据包括source_records.json、tensors.npz、all_56_predicates.csv、all_400_pairs.csv、vocabulary_comparisons.json、evaluation.json、detailed_results.json；均位于output/T01_trace。')
md.extend(['[T01独立完整图文页](T01_detailed.html) · [原始标注](../output/T01_trace/source_records.json) · [全部56词分数CSV](../output/T01_trace/all_56_predicates.csv) · [全部400对CSV](../output/T01_trace/all_400_pairs.csv) · [张量NPZ](../output/T01_trace/tensors.npz) · [V01对应注意力](V01_attention.html)',''])
ht.append('<p>'+ ' · '.join(f'<a href="{path}">{title}</a>' for title,path in [('原始JSON','../output/T01_trace/source_records.json'),('56词CSV','../output/T01_trace/all_56_predicates.csv'),('400对CSV','../output/T01_trace/all_400_pairs.csv'),('完整张量','../output/T01_trace/tensors.npz'),('V01注意力','V01_attention.html')])+'</p>')
(REPORT/'T01_chapter.md').write_text('\n'.join(md),encoding='utf-8')
style="body{font:16px 'Microsoft YaHei',sans-serif;max-width:1550px;margin:auto;padding:24px;color:#182435}p{line-height:1.85}img{max-width:100%}table{border-collapse:collapse;width:100%;font-size:13px;margin:18px 0}td,th{border:1px solid #cbd5e1;padding:7px;text-align:left;word-break:break-word}th{background:#e2e8f0}h2{margin-top:40px}"
(REPORT/'T01_detailed.html').write_text('<!doctype html><html lang="zh"><meta charset="utf-8"><title>T01 同一样本全链路实测</title><style>'+style+'</style><h1>T01：同一样本从原始标注到最终评测</h1>'+''.join(ht)+'</html>',encoding='utf-8')
manifest={v.name:hashlib.sha256(v.read_bytes()).hexdigest() for v in OUT.iterdir() if v.is_file() and v.name!='artifact_hashes.json'}
c.save(OUT/'artifact_hashes.json',manifest)
print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
