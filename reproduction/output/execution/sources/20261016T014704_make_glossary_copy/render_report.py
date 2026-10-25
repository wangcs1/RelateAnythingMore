"""Regenerate figures, all paired outputs, Chinese report and presentation."""
import html
import json
import math
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import common as c

plt.rcParams['font.sans-serif']=['Microsoft YaHei','DejaVu Sans']
plt.rcParams['axes.unicode_minus']=False
FIG=c.PROJECT/'figures'; FIG.mkdir(exist_ok=True)
REPORT=c.PROJECT/'reports'; REPORT.mkdir(exist_ok=True)
OUT=c.PROJECT/'output'
STYLE="body{font:16px 'Microsoft YaHei',system-ui;max-width:1500px;margin:auto;padding:24px;background:#f8fafc;color:#172033}h1,h2,h3{line-height:1.4}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}img{max-width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:13px}th,td{border:1px solid #cbd5e1;padding:6px;text-align:left;vertical-align:top}th{background:#e2e8f0}details{background:white;padding:12px;border:1px solid #ddd;margin:10px 0}summary{cursor:pointer;font-weight:600}.warn{color:#9a3412}code{word-break:break-all}a{color:#1d4ed8}section{margin:18px 0}"
def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def rows(path): return [json.loads(s) for s in Path(path).read_text(encoding='utf-8').splitlines()]
def esc(x): return html.escape(str(x))
def page(path,title,body):
    Path(path).write_text(f'<!doctype html><html lang="zh"><meta charset="utf-8"><title>{esc(title)}</title><style>{STYLE}</style><h1>{esc(title)}</h1>{body}</html>',encoding='utf-8')
def table(headers,values):
    return '<table><tr>'+''.join('<th>'+esc(h)+'</th>' for h in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+esc(v)+'</td>' for v in row)+'</tr>' for row in values)+'</table>'
def mdtable(headers,values):
    return '| '+' | '.join(headers)+' |\n|'+'|'.join('---' for _ in headers)+'|\n'+''.join('| '+' | '.join(str(v) for v in row)+' |\n' for row in values)
def pct(v): return f'{100*v:.2f}%'
def plot_save(fig,name):
    fig.savefig(FIG/(name+'.png'),dpi=160,bbox_inches='tight'); fig.savefig(FIG/(name+'.svg'),bbox_inches='tight'); plt.close(fig)

ds=c.RelationDataset(str(c.ROOT/'data/PSG/packed/psg'),'test',resolution=448,max_objects=100)
predicates=ds.predicate_names
e01=load(OUT/'E01_vocabulary/results.json'); att=load(OUT/'V01_attention/results.json')
baseline=load(OUT/'B01_baseline/results.json'); full=rows(OUT/'B01_baseline/predictions.jsonl'); fullmap={r['index']:r for r in full}
e02=load(OUT/'E02_box_perturbation/results.json'); e03=load(OUT/'E03_pair_weight/results.json'); e04=load(OUT/'E04_image_evidence/results.json')
runtime=load(OUT/'B01_baseline/runtime.json'); env=load(c.PROJECT/'manifests/environment.json')

# E01: complete six-phrase scoring tables, original and replacement vocabularies.
vocab_pages=[]
contact=Image.new('RGB',(1200,math.ceil(len(e01['cases'])/4)*245),'white')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
for n,r in enumerate(e01['cases']):
    im,boxes,_=ds.load_raw(r['index']); pair=c.boxed(im,boxes,[r['s'],r['o']])
    pair.thumbnail((295,205)); x=(n%4)*300;y=(n//4)*245
    contact.paste(pair,(x,y)); draw=ImageDraw.Draw(contact)
    draw.text((x+3,y+207),f"{r['case_id']} #{r['s']}->{r['o']}",font=font,fill='black')
    draw.text((x+3,y+226),f"idx={r['index']} GT={r['predicate']}",font=font,fill='black')
    pairfile=OUT/'E01_vocabulary/images'/f"{r['case_id']}_pair.jpg"; c.boxed(im,boxes,[r['s'],r['o']]).save(pairfile)
    scores=r.get('candidates',[])
    fig,axs=plt.subplots(1,2,figsize=(13,4))
    labels=[s['phrase'] for s in scores]; colors=['#2563eb' if s['role']=='positive' else '#ef4444' for s in scores]
    axs[0].barh(labels,[s['predicate_logit'] for s in scores],color=colors); axs[0].invert_yaxis();axs[0].set_title('固定有向物体对：谓词logit')
    axs[1].barh(labels,[s['fused_score'] for s in scores],color=colors);axs[1].invert_yaxis();axs[1].set_xlim(0,1);axs[1].set_title('融合pair logit后的sigmoid分数')
    fig.suptitle(f"{r['case_id']} / image index {r['index']} / #{r['s']} → #{r['o']}");fig.tight_layout();plot_save(fig,'E01_'+r['case_id'])
    details=table(['短语','预设角色','原始谓词logit','谓词sigmoid','pair logit','融合logit','融合分数','排名','文本cos原词','alpha','semantic cos','spatial cos','训练词表精确出现'],
        [[s['phrase'],s['role'],f"{s['predicate_logit']:.6f}",f"{s['predicate_sigmoid']:.6f}",f"{s['pair_logit']:.6f}",f"{s['fused_logit']:.6f}",f"{s['fused_score']:.6f}",s['rank'],f"{s['text_cos_to_original']:.6f}",f"{s['alpha']:.6f}",f"{s['cos_sem']:.6f}",f"{s['cos_spa']:.6f}",s['exact_in_training_vocabulary']] for s in scores])
    swap=table(['集合','完整候选词','逐候选谓词logit','逐候选融合分数','最高分'],[[tag,' / '.join(v['vocabulary']),', '.join(f'{x:.6f}' for x in v['predicate_logits']),', '.join(f'{x:.6f}' for x in v['fused_scores']),v['winner']] for tag,v in r.get('vocabulary_replacements',{}).items()])
    reverse=r.get('reverse_pair_followup',{})
    reverse_table=table(['同一短语','原向谓词logit','反向谓词logit','原向score','反向score'],[[a['phrase'],f"{a['predicate_logit']:.6f}",f"{b['predicate_logit']:.6f}",f"{a['fused_score']:.6f}",f"{b['fused_score']:.6f}"] for a,b in zip(scores,reverse.get('candidates',[]))])
    body=f"<h2>{esc(r['case_id'])} / 图像{esc(r['file_name'])} / #{r['s']}→#{r['o']}</h2><div class='pair'><section><h3>固定图像与有向物体对</h3><img src='../output/E01_vocabulary/images/{r['case_id']}_pair.jpg'></section><section><h3>双方候选：正向/改写 vs 反向/无关控制</h3><img src='../figures/E01_{r['case_id']}.png'></section></div><p>GT原词={esc(r['predicate'])}；slot={r['slot']}；正向组胜出={r.get('positive_winner')}；margin={r.get('margin_logit',0):.6f}。</p>{details}<h3>原始词表与替换/扩充词表：双方完整展示</h3>{swap}<h3>文本向量相似度矩阵</h3>{table(['行/列']+labels,[[labels[i]]+[f'{v:.4f}' for v in row] for i,row in enumerate(r.get('text_cosine_matrix',[]))])}<p class='warn'>正/负是预设研究角色，具体图片未必满足严格同义或互斥；请结合语境审核。分数不等于真实正确概率。</p>"
    body+=f"<h3>后续方向验证：原向#{r['s']}→#{r['o']} vs 反向#{r['o']}→#{r['s']}</h3><p>反向slot={reverse.get('slot')}，选中={reverse.get('selected')}。这是角色方向追查，不计入24例原始实验。</p>{reverse_table}"
    page(REPORT/f'E01_{r["case_id"]}.html',r['case_id'],body)
    vocab_pages.append(f"<details><summary>{esc(r['case_id'])}：winner={esc(r.get('winner'))}</summary>{body}<p><a href='E01_{r['case_id']}.html'>独立页</a></p></details>")
contact.save(FIG/'E01_all24_contact_sheet.jpg')
page(REPORT/'E01_all_cases.html','E01：全部24例，所有表达双方与词表替换',"<p>样本在运行前按GT固定，没有按成功率筛选。所有6个候选及每种替换集合均完整展示。</p>"+''.join(vocab_pages))

# Attention: original and heatmap overlay, individual heads, regions, spatial map.
att_pages=[]
for r in att['cases']:
    im,boxes,_=ds.load_raw(r['index']); base=np.asarray(im.resize((448,448)),dtype=np.float32)/255
    maps=np.load(OUT/'V01_attention'/f"{r['case_id']}.npz")
    fig,axs=plt.subplots(1,len(r['maps'])+1,figsize=(4*(len(r['maps'])+1),4))
    axs[0].imshow(c.boxed(im,boxes,[r['s'],r['o']]));axs[0].set_title('原图与主体/客体框');axs[0].axis('off')
    for ax,(name,weights) in zip(axs[1:],maps.items()):
        avg=weights.mean(0).reshape(28,28)
        heat=np.asarray(Image.fromarray(avg).resize((448,448),Image.Resampling.BILINEAR))
        ax.imshow(base); ax.imshow(heat,cmap='magma',alpha=.45);ax.set_title(name+' query → patch');ax.axis('off')
        xy448=c.pixel_boxes(boxes,(448,448))
        for boxid,col in [(r['s'],'#ef4444'),(r['o'],'#22c55e')]:
            x1,y1,x2,y2=xy448[boxid]
            ax.add_patch(plt.Rectangle((x1,y1),x2-x1,y2-y1,fill=False,edgecolor=col,linewidth=1.5))
    fig.suptitle(r['case_id']+'：SoftSpatialPool真实查询的FP32权重重算（非因果归因）');fig.tight_layout();plot_save(fig,'V01_'+r['case_id'])
    weights=maps['subject'];fig,axs=plt.subplots(2,4,figsize=(13,6)); vmax=weights.max()
    for h,ax in enumerate(axs.flat):
        ax.imshow(weights[h].reshape(28,28),cmap='magma',vmin=0,vmax=vmax);ax.set_title(f'subject head {h}');ax.axis('off')
    fig.tight_layout();plot_save(fig,'V01_heads_'+r['case_id'])
    # Scene feature magnitude plus first three PCA channels; feature input fixed.
    fmap=np.load(OUT/'V01_attention'/f"{r['case_id']}_scene.npz")['feature_map']
    centered=fmap.reshape(-1,fmap.shape[-1])-fmap.reshape(-1,fmap.shape[-1]).mean(0)
    u,sigma,vt=np.linalg.svd(centered,full_matrices=False)
    rgb=(u[:,:3]*sigma[:3]).reshape(28,28,3)
    rgb=(rgb-rgb.min((0,1),keepdims=True))/(np.ptp(rgb,axis=(0,1),keepdims=True)+1e-9)
    fig,axs=plt.subplots(1,3,figsize=(12,4));axs[0].imshow(im);axs[0].set_title('原图');axs[1].imshow(np.linalg.norm(fmap,axis=-1),cmap='viridis');axs[1].set_title('真实场景feature map L2 norm');axs[2].imshow(rgb);axs[2].set_title('真实feature map PCA前三维（仅显示）')
    for ax in axs: ax.axis('off')
    fig.tight_layout();plot_save(fig,'V01_scene_'+r['case_id'])
    body=f"<h2>{r['case_id']} / index={r['index']}</h2><img src='../figures/V01_{r['case_id']}.png'><h3>主体query所有head（同一色标）</h3><img src='../figures/V01_heads_{r['case_id']}.png'>"+table(['区域','框内注意力质量','框内patch占比','归一化熵'],[[name,f"{v['attention_mass_inside_box']:.6f}",f"{v['patch_fraction_inside_box']:.6f}",f"{r['entropy_normalized'][name]:.6f}"] for name,v in r['box_mass'].items()])+f"<p>BF16显式与快速输出最大差：{esc(r['need_weights_vs_fast_output_max_abs'])}；相对最大差：{esc(r.get('need_weights_vs_fast_output_relative_max'))}；FP32最大差：{esc(r.get('fp32_need_weights_vs_fast_output_max_abs'))}。观察hook前后重复前向logit最大差={r['forward_repeat_logit_max_abs']}。</p><p>每head权重和范围[{r['attention_weight_sum_min']:.7f},{r['attention_weight_sum_max']:.7f}]；完整head数据见NPZ。热图透明度与每图色标用于展示，不能把不同图颜色深浅当相同绝对分数。</p>"
    body+=f"<h3>同一张图的真实场景特征图</h3><img src='../figures/V01_scene_{r['case_id']}.png'><p>PCA颜色无类别或语义标签含义；不同图单独归一化，不可跨图直接比较颜色。原feature map保存在对应_scene.npz。</p>"
    bf16=np.load(OUT/'V01_attention'/f"{r['case_id']}_bf16.npz")
    fig,axs=plt.subplots(len(r['maps']),3,figsize=(10,3*len(r['maps'])))
    for row,(name,a) in enumerate(maps.items()):
        aa=a.mean(0).reshape(28,28);bb=bf16[name].mean(0).reshape(28,28);vmax=max(aa.max(),bb.max())
        axs[row,0].imshow(bb,cmap='magma',vmin=0,vmax=vmax);axs[row,0].set_title(name+' BF16显式权重')
        axs[row,1].imshow(aa,cmap='magma',vmin=0,vmax=vmax);axs[row,1].set_title(name+' FP32诊断权重')
        axs[row,2].imshow(np.abs(aa-bb),cmap='viridis');axs[row,2].set_title('绝对差（独立色标）')
        for ax in axs[row]: ax.axis('off')
    fig.tight_layout();plot_save(fig,'V01_precision_'+r['case_id'])
    body+=f"<h3>注意力数值精度对照：两方完整展示</h3><img src='../figures/V01_precision_{r['case_id']}.png'><p>平均每head权重L1差={esc(r.get('bf16_vs_fp32_per_region_mean_head_L1'))}。原模型调用默认need_weights=True，已由观测返回值和profiler核验；BF16显式原调用与need_weights=False替代调用的差异不代表原路径不返回权重。FP32图仍是诊断重算，不是BF16运行时逐位权重。详见R01执行路径审计。</p>"
    att_pages.append(body)
page(REPORT/'V01_attention.html','V01：区域查询、场景patch与注意力',"<p>并排展示原图与各区域query读图位置。权重来自实际q/k/v的FP32重算，保留全部head；不是Grad-CAM，不代表因果贡献。</p>"+''.join(att_pages))

trace=att['traces'][0]; index=trace['index']; s=trace['s'];o=trace['o']; im,boxes,_=ds.load_raw(index)
xy=c.pixel_boxes(boxes,im.size);bi,bj=xy[s],xy[o]
union=[min(bi[0],bj[0]),min(bi[1],bj[1]),max(bi[2],bj[2]),max(bi[3],bj[3])]
inner=[max(bi[0],bj[0]),max(bi[1],bj[1]),min(bi[2],bj[2]),min(bi[3],bj[3])]
contactbox=[min(inner[0],inner[2]),min(inner[1],inner[3]),max(inner[0],inner[2]),max(inner[1],inner[3])]
canvas=c.boxed(im,boxes,[s,o]);draw=ImageDraw.Draw(canvas);draw.rectangle(union,outline='#f59e0b',width=4);draw.rectangle(contactbox,outline='#a855f7',width=4)
canvas.save(FIG/'T01_regions.jpg')
fig,ax=plt.subplots(figsize=(14,8));ax.axis('off')
steps=[f"真实PSG test：{trace['file_name']}\n主体#{s} → {trace['predicate']} → 客体#{o}",
    'VLM生成与训练：未执行\n无逐轮原始记录，不能虚构grow增益；这里只是教学位置',
    f"真实pack/targets：({s}, {o}, {trace['predicate_index']})\nW[{trace['predicate_index']}] = '{trace['W_predicate']}'的512维文本向量",
    f"真实候选槽：{trace['slot']}\n主体、客体、union、contact、19维几何 → 关系上下文",
    f"真实双查询：semantic {trace['query_shapes']['semantic']} / spatial {trace['query_shapes']['spatial']}\ncos_sem={trace['cos_sem']:.4f}, cos_spa={trace['cos_spa']:.4f}, alpha={trace['alpha']:.4f}",
    f"真实logits {trace['logits_shape']}\n[{trace['slot']},{trace['predicate_index']}]={trace['predicate_logit_BF16']:.4f}；pair={trace['pair_logit']:.4f}",
    f"融合分数={trace['fused_score']:.6f}\n此对最佳谓词={trace['fixed_pair_best']}；GT词在对内排名={trace['GT_rank_in_pair']}",
    '真实评测：每对argmax→全图top50→精确GT匹配\n同义合理关系也可能失配；文本替换完整结果见E01']
for j,text in enumerate(steps):
    ax.text(.03 if j%2==0 else .53,.94-(j//2)*.235,text,transform=ax.transAxes,va='top',fontsize=11,
        bbox={'boxstyle':'round,pad=.7','facecolor':'#dbeafe' if j!=1 else '#ffedd5','edgecolor':'#64748b'})
    if j%2==0:
        ax.annotate('',xy=(.50,.90-(j//2)*.235),xytext=(.44,.90-(j//2)*.235),xycoords='axes fraction',arrowprops={'arrowstyle':'->','color':'#64748b','lw':2})
    elif j<7:
        ax.annotate('',xy=(.02,.94-((j+1)//2)*.235),xytext=(.94,.85-(j//2)*.235),xycoords='axes fraction',arrowprops={'arrowstyle':'->','color':'#94a3b8','lw':1.3,'connectionstyle':'angle,angleA=-90,angleB=180,rad=10'})
fig.tight_layout();plot_save(fig,'T01_trace')
flow=Image.open(FIG/'T01_trace.png').convert('RGB');region=Image.open(FIG/'T01_regions.jpg').convert('RGB');scores_image=Image.open(FIG/'E01_riding_1.png').convert('RGB')
region.thumbnail((600,480));flow.thumbnail((1600,950));scores_image.thumbnail((1000,480))
story=Image.new('RGB',(1600,flow.height+500),'white');story.paste(region,(0,0));story.paste(scores_image,(600,0));story.paste(flow,(0,500));story.save(FIG/'T01_main_story.png')
# Canonical T01 results belong to trace_sample.py. Legacy introductory assets
# above are regenerated for old links, then replaced by the executed full trace.
complete_story=FIG/'T01_complete_story.png'
assert complete_story.exists(), 'Run trace_sample.py first'
for legacy_name in ['T01_main_story.png','T01_trace.png']:
    (FIG/legacy_name).write_bytes(complete_story.read_bytes())
(FIG/'T01_trace.svg').write_bytes((FIG/'T01_complete_story.svg').read_bytes())

def triplets(row,limit=20):
    gt={tuple(g) for g in row['gt']}
    return table(['排名','主体→谓词→客体','score','fused logit','是否GT'],[[j+1,f"#{p[0]} → {predicates[p[2]]} → #{p[1]}",f'{p[3]:.6f}',f'{p[4]:.6f}',tuple(p[:3]) in gt] for j,p in enumerate(row['ranked'][:limit])])
def gt_table(row):
    return table(['主体','GT谓词','客体'],[[g[0],predicates[g[2]],g[1]] for g in row['gt']])
def diagnostic_table(row):
    return table(['GT方向','GT谓词','阶段','slot','最佳谓词','GT词logit','pair logit','GT融合logit','GT词对内rank'],
        [[f"#{d['s']}→#{d['o']}",d['gt_predicate'],d['stage'],d['slot'],d['best_predicate'],d['gt_predicate_logit'],d['pair_logit'],d['gt_fused_logit'],d['gt_predicate_rank']] for d in row['diagnostics']])

# Every comparison contains all 300/2179 paired text results, with all GT and
# all GT diagnostics. At least six images per image/box condition are shown.
paired_links=[]
def paired_page(tag,title,original_rows,changed_rows,image_original,image_changed,outputdir):
    orig={r['index']:r for r in original_rows}; parts=[]
    delta=[]
    for changed in changed_rows:
        index=changed['index']; before=orig[index]
        a=before['recall']['50'];b=changed['recall']['50'];delta.append(b-a if a is not None and b is not None else None)
        prefix=f"{index:04d}"
        images_html=''
        if (outputdir/'images'/image_changed.format(index=prefix)).exists():
            basepath='../output/'+str(outputdir.relative_to(OUT)).replace('\\','/')+'/images/'
            images_html=f"<div class='pair'><section><h3>原始输入</h3><img src='{basepath+image_original.format(index=prefix)}'></section><section><h3>对照输入</h3><img src='{basepath+image_changed.format(index=prefix)}'></section></div>"
        text=f"{images_html}<div class='pair'><section><h3>原始：top20</h3>{triplets(before)}<details><summary>原始完整top100</summary>{triplets(before,100)}</details><h3>原始：全部GT的分数与阶段</h3>{diagnostic_table(before)}</section><section><h3>对照：top20</h3>{triplets(changed)}<details><summary>对照完整top100</summary>{triplets(changed,100)}</details><h3>对照：全部GT的分数与阶段</h3>{diagnostic_table(changed)}</section></div><h3>双方共同GT（原始重复记录保留）</h3>{gt_table(before)}"
        parts.append(f"<details><summary>index {index} / {esc(before['file_name'])}：R50 {a} → {b}</summary>{text}</details>")
    page(REPORT/(tag+'.html'),title,"<p>全部配对样本逐项展示原始与对照双方；页面默认top20，可展开完整top100，原始JSONL同时保留top100和全部GT诊断。图像干预/框扰动每条件前6张也展示双方输入。</p>"+''.join(parts))
    dd=[v for v in delta if v is not None]
    return {'tag':tag,'images':len(changed_rows),'improved':sum(v>0 for v in dd),'worse':sum(v<0 for v in dd),'unchanged':sum(v==0 for v in dd),'mean_image_delta':float(np.mean(dd)) if dd else 0}

orig02=rows(OUT/'E02_box_perturbation/original_0.00_seed0/predictions.jsonl')
paired_stats=[]
for condition in e02['conditions']:
    if condition['condition']=='original': continue
    path=OUT/'E02_box_perturbation'/condition['tag']
    r=rows(path/'predictions.jsonl')
    tag='E02_'+condition['tag']; paired_stats.append(paired_page(tag,tag,orig02,r,'{index}_original.jpg','{index}_perturbed.jpg',path))
    paired_links.append((tag+'.html',tag))
orig04=rows(OUT/'E04_image_evidence/original/predictions.jsonl')
for condition in e04['conditions']:
    if condition['condition']=='original': continue
    path=OUT/'E04_image_evidence'/condition['condition'];r=rows(path/'predictions.jsonl')
    tag='E04_'+condition['condition'];paired_stats.append(paired_page(tag,tag,orig04,r,'{index}_original.jpg','{index}_changed.jpg',path));paired_links.append((tag+'.html',tag))
weight0=rows(OUT/'E03_pair_weight/weight0_predictions.jsonl')
paired_stats.append(paired_page('E03_weight0_vs1','E03：全部2179张，weight1与weight0双方完整文本',full,weight0,'{index}_original.jpg','{index}_changed.jpg',OUT/'E03_pair_weight'))
paired_links.append(('E03_weight0_vs1.html','E03：weight1 vs weight0'))
c.save(OUT/'paired_comparison_summary.json',paired_stats)

# Full baseline failure stages are now resolved for all selected pairs, even
# outside top100. Deterministic cases cover each miss stage and success.
failure_cases=[]
for stage in ('wrong_predicate','rank_below50','not_selected','hit50'):
    pool=[r for r in full if len({tuple(g) for g in r['gt']})>=3 and any(d['stage']==stage for d in r['diagnostics'])]
    chosen=pool[:3]
    for r in chosen:
        name=f"{stage}_{r['index']:04d}";im,boxes,_=ds.load_raw(r['index']);c.boxed(im,boxes).save(FIG/(name+'.jpg'))
        failure_cases.append({'stage':stage,'index':r['index'],'file_name':r['file_name']})
        page(REPORT/(name+'.html'),name,f"<img src='../figures/{name}.jpg'><div class='pair'><section><h2>完整GT</h2>{gt_table(r)}</section><section><h2>预测top50</h2>{triplets(r,50)}</section></div><h2>每个GT的采样、谓词与融合定位</h2>{diagnostic_table(r)}")
c.save(OUT/'failure_case_manifest.json',failure_cases)

# Plots and complete numeric condition table; error bars are seed standard
# deviation, not confidence intervals.
fig,axs=plt.subplots(1,3,figsize=(13,4));paper={'R@50':.401,'mR@50':.306,'F1@50':.347}
for ax,k in zip(axs,paper):
    ax.bar(['官方报告','本地完整测试'],[100*paper[k],100*baseline['metrics'][k]],color=['#94a3b8','#2563eb']);ax.set_title(k);ax.set_ylim(0,50)
    for j,v in enumerate([paper[k],baseline['metrics'][k]]): ax.text(j,100*v+.5,f'{100*v:.2f}%',ha='center')
plot_save(fig,'B01_main_table')
agg=[]
for mode in ('translation','scale'):
    fig,axs=plt.subplots(1,3,figsize=(15,4))
    for kind,col in [('spatial','#2563eb'),('semantic','#ef4444')]:
        for ax,metric in zip(axs,['pooled_R50','pair_coverage','selected_predicate_accuracy']):
            xs=[0]+c.CFG[mode+'_levels'];ys=[];sd=[]
            for l in xs:
                rr=[x for x in e02['conditions'] if (x['condition']=='original' if l==0 else x['condition']==mode and x['level']==l)]
                vals=[x['summary']['types'][kind][metric] for x in rr]
                ys.append(100*np.mean(vals));sd.append(100*np.std(vals,ddof=1) if len(vals)>1 else 0)
            ax.errorbar(xs,ys,yerr=sd,marker='o',label=kind,color=col,capsize=3);ax.set_title(metric);ax.set_xlabel(mode+' strength');ax.set_ylabel('%');ax.legend()
    fig.suptitle('固定300张，3 seeds；误差棒=跨seed样本标准差');fig.tight_layout();plot_save(fig,'E02_'+mode)
    for l in c.CFG[mode+'_levels']:
        rr=[x for x in e02['conditions'] if x['condition']==mode and x['level']==l]
        values={k:[x['summary']['metrics'][k] for x in rr] for k in ('R@50','mR@50','F1@50')}
        agg.append({'mode':mode,'level':l,'metrics':{k:{'mean':float(np.mean(v)),'std':float(np.std(v,ddof=1))} for k,v in values.items()},
            'types':{kind:{k:{'mean':float(np.mean([x['summary']['types'][kind][k] for x in rr])),'std':float(np.std([x['summary']['types'][kind][k] for x in rr],ddof=1))} for k in ('pooled_R50','pair_coverage','selected_predicate_accuracy')} for kind in ('spatial','semantic')}})
c.save(OUT/'E02_box_perturbation/aggregate.json',agg)
fig,axs=plt.subplots(1,2,figsize=(13,4))
for ax,kind in zip(axs,('spatial','semantic')):
    ax.bar([r['condition'] for r in e04['conditions']],[100*r['summary']['types'][kind]['pooled_R50'] for r in e04['conditions']],color=['#2563eb','#93c5fd','#93c5fd','#f97316','#ef4444']);ax.set_title(kind+' pooled R@50');ax.tick_params(axis='x',rotation=20)
plot_save(fig,'E04_image_conditions')
fig,ax=plt.subplots(figsize=(8,4));ax.bar(list(baseline['stages']),list(baseline['stages'].values()),color='#2563eb');ax.set_ylabel('去重GT三元组数');ax.tick_params(axis='x',rotation=15);plot_save(fig,'B01_failure_stages')

E01sum=e01['summary']; bmet=baseline['metrics']
att_mean=np.mean([v['attention_mass_inside_box'] for r in att['cases'] for v in r['box_mass'].values()])
att_area=np.mean([v['patch_fraction_inside_box'] for r in att['cases'] for v in r['box_mass'].values()])
max_repeat=max(r['forward_repeat_logit_max_abs'] for r in att['cases'])
doc=["# RelateAnything：官方权重复现与控制变量实验完整报告", "", "日期：2026-10-15。研究问题：换词表能够预测的模型，对图像证据、区域几何和表达变化分别有多敏感？本报告区分论文/仓库报告、本地实测与解释假设。", "", "## 交付范围与组织", "", "已执行B01完整基准、V01注意力、T01贯穿样本、E01表达变化、E02位置/大小扰动、E03关系存在性项和E04图像证据干预。训练、微调、RA-4M/VLM重生成、真实检测器SGDet、其他基准轴均未执行。旧成果完整归档到archive，官方源码保持未改。", "", "目录：scripts可重跑脚本，configs预先固定设计，manifests版本/样本/环境，output原始结果，figures可重生成PNG/SVG，reports本报告及全部双方对比HTML，archive旧成果。大型模型、数据、隔离环境作为外部只读资源引用，不重复复制。", "", "## 环境、数据与协议审计", "", f"GPU：{env['gpu']}；Python {env['python']}；Torch {env['torch']}；CUDA {env['cuda']}。commit `{env['commit']}`，源码git status为空={not bool(env['git_status'].strip())}。权重/配套资源哈希、数据revision、配置SHA256及环境快照见manifests。", "", "作者公开PSG-coco-format完整test原始2186图，经官方转换2179图，13609条关系，56词；全部推理，2177图计分。论文关系统计13623与此仍差14条，未伪造补齐。GT框、448、BF16、batch8、graph_constraint=True、sigmoid、a=1,b=0、pair_weight=1；geo预算400，评测请求500实际400。没有测试集调参。", "", "每个实验记录问题、预设变量、样本、结果和界限；300图均匀抽取全test顺序端点，不按输出挑图。E01按GT关系最早出现选样，为探索性覆盖而非无偏总体估计。空间/语义划分是研究者显式11词静态关系列表，不是官方真值或alpha阈值："+', '.join(c.CFG['spatial_predicates'])+"。sitting on/standing on等带动作关系归semantic；所有曲线解释受此划分限制。", "", "## B01：正式主表对应行重跑", "", "设计：发布ViT-S+最终epoch11/EMA权重，完整公开test，严格谓词匹配。模型targets=None，物体类别不作为输入。官方评分器加独立复算，保证逐图和逐类协议一致。", "", mdtable(['指标','官方报告','本地完整test','差值/百分点'],[[k,pct(v),pct(bmet[k]),f'{100*(bmet[k]-v):+.4f}'] for k,v in paper.items()]), "", "![主表双方](../figures/B01_main_table.png)", "", mdtable(['K','R','mR','F1'],[[k,pct(bmet[f'R@{k}']),pct(bmet[f'mR@{k}']),pct(bmet[f'F1@{k}'])] for k in (20,50,100)]), "", f"独立复算最大差={baseline['max_difference']}；记录{baseline['images']}张，计分{baseline['scored_images']}张。耗时{runtime['seconds']:.2f}s，PyTorch peak allocated={runtime['peak_allocated_gib']:.3f}GiB（包含两个评估器及详细CPU诊断，不含初始化，不是纯模型吞吐或总显存）。", "", "R使用每图去重GT，mR的每图每类分母保留重复标注；F1是R/mR调和平均。不能用 pooled TP/GT替换主表mR。小幅论文差异仍未完全归因，关系数量差异与版本/数值精度需如实报告。", "", "## V01：SoftSpatialPool区域query读取哪些patch", "", "设计：从E01每类前2例固定选12张/例，观察原始MHA q/k/v，不修改模型前向；显式重算全部head的query→patch注意力。显示主体、客体、union、contact，另保留逐head权重NPZ。FP32重算缓解BF16显式MHA/快速SDPA差异，并记录二者误差；不是运行时逐位相同的因果解释。", "", f"12例24个主体/客体query平均框内注意力质量={att_mean:.4f}，对应平均框内patch面积占比={att_area:.4f}；观察hook下重复前向logit最大差={max_repeat}。必须结合逐例数据，不能以平均集中度证明关系语义被理解。", "", "![注意力与原图双方](../figures/V01_riding_1.png)", "", "![所有head](../figures/V01_heads_riding_1.png)", "", "[全部query可视化与精度审计](V01_attention.html)。逐例框内质量/面积、归一化熵、权重和、BF16/FP32差异均已列出。注意力显示读取位置，既非梯度归因也非因果干预；框外注意力可能读取上下文，不能一概当错误。", "", "## T01：一张真实测试图贯穿数据—模型—评测", "", f"使用{trace['file_name']}，主体#{s}、客体#{o}。GT pack与targets三元组({s},{o},{trace['predicate_index']})；W[{trace['predicate_index']}]对应'{trace['predicate']}'的512维文本向量。对应候选槽{trace['slot']}，logits形状{trace['logits_shape']}，GT词在此对排名{trace['GT_rank_in_pair']}。向量、几何、分数见output/T01_trace与V01/traced_vectors.npz。", "", "![主客体union与contact](../figures/T01_regions.jpg)", "", "![贯穿全流程](../figures/T01_trace.png)", "", "这是一张test图，不是本次训练样本。VLM语义/grow/空间轮与几何过滤无原始记录，因此图中明确标未执行/教学位置，不虚构各轮增益；真实部分从现有PSG pack开始。", "", "## E01：固定物体对的表达变化与词表替换", "", "问题：同义改写是否保持正向判断，模型能否区分角色反转和无关表达？设计：riding/holding/on/over/beside/in front of六类各4例，原词+2种改写+2种反向或情境冲突+1种无关表达，同一个候选集合直接比较。固定图像/框/视觉查询/采样对/模板/评分。只缓存视觉查询，文本头使用F32评分以便逐候选控制；它不是重新完整BF16跑主表。", "", "随后分别用原词、改写1、改写2替换正向候选，与同一负控制集合比；扩充集合单独报告。固定短语自身logit不因为候选数增加而改变，但最高排名可能改变。", "", mdtable(['量','本地实测','定义'],[['保留指定对',f"{E01sum['selected']}/{E01sum['total']}",'24个固定有向GT对'],['正向组最高分',pct(E01sum['positive_winner_rate']),'任一正向候选胜出'],['原词高于全部控制',pct(E01sum['original_beats_controls_rate']),'原词单独对比'],['改写分别高于控制',pct(E01sum['paraphrase_each_beats_controls_rate']),'48次改写比较'],['替换正向胜出状态一致',pct(E01sum['replacement_binary_consistency']),'原词vs各改写，共48次'],['平均正负logit间隔',f"{E01sum['mean_logit_margin']:.4f}",'max positive - max control'],['平均正向组内部范围',f"{E01sum['mean_paraphrase_logit_range']:.4f}",'max positive - min positive']]), "", mdtable(['关系','n','正向胜出','平均logit间隔'],[[p,v['n'],pct(v['positive_winner_rate']),f"{v['mean_margin']:.4f}"] for p,v in E01sum['groups'].items()]), "", "![全部预选图](../figures/E01_all24_contact_sheet.jpg)", "", "[全部24例双方：图像、六短语完整分数、排名、词表替换和文本相似度矩阵](E01_all_cases.html)。每个候选同时列谓词logit、谓词sigmoid、pair logit、融合logit/score、alpha、语义/空间cos和训练词表精确出现状态。", "", "解释：原词通常胜过控制，但改写稳定性明显低；文本向量接近不保证视觉查询相对它们分数一致。resting on不一定与on在运动场景等价，ahead of与遮挡深度in front of不同，mounted on可能是安装而非骑乘；控制也不必严格互斥。因此总体是预设短语探针，不是人工认证同义基准。训练词表精确不出现也不证明语义未见。", "", "## E02：位置与大小误差分开控制，三种子", "", "设计：同一300张图、固定GT身份/词表/评分；平移=Gaussian×level×原框宽高，仅变中心；缩放=原宽高×exp(Gaussian×level)，仅变尺寸。levels=.02,.05,.10,.20，各101/202/303三种子。每seed/图的随机值固定，各强度共用噪声，降低比较随机差异。中心clamp[0,1]，尺寸clamp[1e-4,1]，角点可越界，后续遵循官方prompt clamp；裁剪数量留档。共1基线+24扰动条件=25次。", "", "指标：主表R/mR/F1、每类逐图召回、空间/语义去重GT pooled R50、候选对覆盖、已选对内argmax准确率、失败阶段。后3者非官方主表指标，不能混称mR。固定目标身份，不用IoU重匹配，所以不是标准SGDet。", "", "![平移曲线](../figures/E02_translation.png)", "", "![大小曲线](../figures/E02_scale.png)", "", mdtable(['模式','强度','R50均值±SD','mR50均值±SD','F1均值±SD','空间pooled R','语义pooled R'],[[r['mode'],r['level'],*[f"{100*r['metrics'][k]['mean']:.2f}±{100*r['metrics'][k]['std']:.2f}%" for k in ('R@50','mR@50','F1@50')],pct(r['types']['spatial']['pooled_R50']['mean']),pct(r['types']['semantic']['pooled_R50']['mean'])] for r in agg]), "", "误差棒是三个seed的样本标准差，不是95%置信区间；测试样本选择波动未估计。逐seed所有指标、裁剪统计和双方输入/GT/预测在相应HTML与JSONL中；不能用一条总体曲线断言所有关系单调下降。", "", "## E03：存在性项是否帮助跨物体对排序", "", "设计：完整2179图只前向一次，固定全部谓词logit/候选对，分别w=1与w=0在评分阶段重排。两者不校准、不调阈值、仍每对一个谓词。它是推理评分干预，非移除采样器或重新训练消融。", "", mdtable(['pair_weight','R50','mR50','F1','空间pooled R','语义pooled R'],[[w,pct(v['metrics']['R@50']),pct(v['metrics']['mR@50']),pct(v['metrics']['F1@50']),pct(v['types']['spatial']['pooled_R50']),pct(v['types']['semantic']['pooled_R50'])] for w,v in e03.items()]), "", "pair logit对同一对所有谓词加同一常数，因此不能改变此对最佳谓词；会改变跨对top50名额。结果差异定位到排序贡献，不证明其输出经过概率校准。[全部2179张双方GT/预测/分项诊断](E03_weight0_vs1.html)。", "", "## E04：图像证据干预（额外探索）", "", "设计：固定同一300图索引/框/词表，original对照blur(radius12，448像素图)、grayscale、每图每通道空间均值图、循环移位150的其他图像。后者仍保留原图框/GT，制造外观与几何身份不一致。mask/结构/阈值均不变，候选对可随视觉改变，故同时看覆盖与已选对准确率。", "", "![原始与4类干预双方](../figures/E04_image_conditions.png)", "", mdtable(['输入','R50','mR50','F1','空间pooled R','语义pooled R','空间对覆盖','语义对覆盖'],[[r['condition'],*[pct(r['summary']['metrics'][k]) for k in ('R@50','mR@50','F1@50')],*[pct(r['summary']['types'][t][m]) for t,m in [('spatial','pooled_R50'),('semantic','pooled_R50'),('spatial','pair_coverage'),('semantic','pair_coverage')]]] for r in e04['conditions']]), "", "均值图/错配图是分布外输入，结果变化支持对像素输入有依赖，但不能分离纯几何先验、语言先验和可解释视觉推理机制。该模型仍通过视觉骨干处理均值图，不能称其为只用几何训练的baseline。每个条件前6张输入双方及全部300图文本双方见对应HTML。", "", "## 失败定位：用全部采样对logit解决旧记录盲区", "", "新版保留全部GT对应候选槽的原词logit、pair logit、最佳谓词和对内排名，因此以前top100外441条无法判定的问题，现在可区分最佳谓词错还是排名靠后。", "", mdtable(['阶段','去重GT数量'],list(baseline['stages'].items())), "", "![失败阶段](../figures/B01_failure_stages.png)", "", "每类阶段取满足至少3条去重GT的最早3图；所有GT与top50、每GT诊断完整展示，不只放成功截图。合理未标注/更细谓词与真视觉错误需结合图像核验；无标注不等于负例，graph constraint也与多GT谓词冲突。", "", "## 最终标注质量审计的边界", "", "本轮没有RA-4M各轮生成原始日志，也没有调用VLM。因此不报告grow增益/过滤器因果贡献；仅对E01固定24个PSG最终GT关系做语境审查。图像与GT双方完整保留，审核备注见context_review.json（如有）及附录。PSG不是RA-4M，此审计不能外推为RA-4M数据质量。没有第二位人工标注者，任何视觉审查均属单人/助手探索，不能冒充独立人工一致性统计。", "", "## RTX 5070 Ti 16GB：能做到什么程度", "", f"实测：本轮完成{len(ds)}图严格评测、完整pair-weight对照、300图×25种框条件、300图×5种图像条件、24例词表与12例注意力，不需训练卡。主模型参数={runtime['parameters']:,}，可训练参数={runtime['trainable_parameters']:,}；F32权重+梯度+Adam两个moment的粗下界约{runtime['trainable_F32_weight_gradient_Adam_moments_lower_bound_gib']:.3f}GiB，不含激活、EMA、临时attention、输入、词表、CUDA库/缓存与优化器实现额外开销。不能从推理峰值推断训练峰值。", "", "官方docs/training.md：503,754 images/epoch×12，4×A100/global batch128、每rank32，约6小时（这是仓库报告，不是本机测量）；至少6,045,048图像呈现。5070 Ti单卡能合理规划小batch低分辨率训练步骤/小集过拟合、冻结骨干的头部微调、有限子集全模型微调，但本轮未做前反向显存测量，因此具体batch、OOM界限、训练时长与效果不能保证。", "", "完整配方还依赖训练图像、ontology/soft supervision/机会率表/排除名单等已移出的资源，以及受限DINOv3初始化。恢复发布模型做微调不等于原始初始化重训。Adam激活、448到672多尺度、19,103词输出和训练对比损失会增加开销。按单步profile选择batch/分辨率、必要时梯度检查点/冻结，并保持独立验证划分；梯度累积只能近似总梯度batch，不能扩大单次batch-local InfoNCE负集合，不能宣称等价4卡论文配方。", "", "不建议为了考核在本机盲目完整重训或重生成Gemma-26B数据；不存在可靠的4×A100→5070Ti时长换算。若导师要求训练证据，下一阶段先用合法训练划分做1步profile与几十/几百图过拟合，再讨论租卡完整配方。不得把PSG test拿去训练后继续报告零样本复现。", "", "## 可重复执行与查验", "", "```powershell\nSet-Location D:\\relateAny\n& .\\reproduction\\scripts\\run_all.ps1\n```", "", "命令会使用已有.venv-eval/权重/data资源，固定配置执行准备→注意力/词表→正式评测/干预→作图/报告。重跑覆盖同实验输出，不覆盖archive。单独重画：`python reproduction/scripts/render_report.py`。不安装/修改原Conda环境，不训练、不发送外部消息。脚本source hashes与输出索引可查manifest，日志通过run_all保存。", "", "## 所有对比双方的明细入口", ""]
doc += [f"- [{title}]({name})" for name,title in paired_links]
doc += ["", "## 单例失败入口", ""]+[f"- [{r['stage']} / index{r['index']}]({r['stage']}_{r['index']:04d}.html)" for r in failure_cases]
review=load(c.PROJECT/'manifests/context_review.json')
all_gt=Counter(); multiple=0; raw_total=0
for r in full:
    raw_total+=len(r['gt']); unique={tuple(g) for g in r['gt']};all_gt.update(g[2] for g in unique)
    pairpred=defaultdict(set)
    for s0,o0,p0 in unique: pairpred[s0,o0].add(p0)
    multiple+=sum(len(v)>1 for v in pairpred.values())
audit_final={'images':len(full),'raw_relationship_records':raw_total,'unique_relationships':sum(all_gt.values()),'duplicate_records':raw_total-sum(all_gt.values()),
    'multilabel_directed_pairs':multiple,'reviewed_pairs':24,'review_method':review['reviewer'],'not_RA4M':True,'generation_rounds_unavailable':True}
c.save(OUT/'D01_final_annotation_audit/results.json',audit_final)
doc += ["", "## 详细结果附录A：每个框扰动条件与原始基线", "", "此表将25个条件完整列出。每行均使用同一300图，与original直接比较；空间/语义划分见固定配置。", "",
    mdtable(['条件','seed','R50','mR50','F1','空间R50','语义R50','空间候选覆盖','语义候选覆盖','中心裁剪框','尺寸裁剪框'],[[r['tag'],r['seed'],*[pct(r['summary']['metrics'][k]) for k in ('R@50','mR@50','F1@50')],*[pct(r['summary']['types'][t][m]) for t,m in [('spatial','pooled_R50'),('semantic','pooled_R50'),('spatial','pair_coverage'),('semantic','pair_coverage')]],r['clipping']['clipped_centers'],r['clipping']['clipped_extents']] for r in e02['conditions']]),"",
    "解读：候选覆盖与分类/排序分开看。若扰动后候选仍覆盖GT而R下降，不能归因到采样器漏选；应检查已选对最佳谓词和top50排序。小强度不同seed的波动不能作精确因果排序。",
    "", "## 详细结果附录B：配对改善/退化分布", "", "同一图R50差的正负计数；不计无GT图，因而计数总和可能少于输入图数。统计不替代显著性检验。", "",
    mdtable(['对照','输入图数','改善','退化','不变','平均R50差/百分点'],[[r['tag'],r['images'],r['improved'],r['worse'],r['unchanged'],f"{100*r['mean_image_delta']:+.4f}"] for r in paired_stats]),
    "", "## 详细结果附录C：E01逐例汇总与语境审查", "", "所有选例均报告，不能只挑原词胜出的23例。下面注释来自助手视觉检查，非独立人工评测；完整双方分数在HTML。", "",
    mdtable(['样本','图像index','GT原词','6候选最高','原词排名','正负logit间隔','改写logit范围','语境备注'],[[r['case_id'],r['index'],r['predicate'],r.get('winner'),r.get('original_rank'),f"{r.get('margin_logit',0):.4f}",f"{r.get('paraphrase_logit_range',0):.4f}",review['cases'][r['case_id']]] for r in e01['cases']]),
    "", "E01词表替换实际重新安装矩阵并前向文本头，验证共同短语logit最大差小于1e-5；这直接区分分数变化和候选竞争。角色方向追查额外评分反向候选对，双方同短语raw/fused分数见各样本页；它是后续诊断而不是增加独立样本数。",
    "", "## D01：最终标注审计（能做与不能做）", "", mdtable(['项目','实测'],list(audit_final.items())), "", "重复和一对多谓词直接影响严格评测协议。24例语境审查暴露大区域框、远处小人物、动作/静态表达不等价等测量因素；它没有提供独立人标正确率，不能估计PSG总体标注错误率，更不能归因RA-4M语义/grow/过滤各轮增益。",
    "", "## 5070 Ti后续任务的实际边界", "", mdtable(['任务','当前结论','尚需条件'],[
        ['完整公开PSG权重评测及控制实验','已实测完成，单卡足够','已有权重、数据、隔离环境'],
        ['增加更多固定样本/seed或其他可获取基准','显存范围内可逐批执行','数据访问权限及对应协议；运行时间随条件增加'],
        ['冻结骨干的有限数据头部微调','合理的下一步方案，但未实测','正式train/val划分，loss资源，先1步显存和梯度profile'],
        ['小batch全模型微调','可能可行，不能承诺batch或速度','AMP、batch/分辨率profile、必要时检查点、验证集'],
        ['严格4卡A100原配方完整重训','本轮不能宣称具备等价复现','全训练资源、初始化授权、匹配batch-local对比集合与多尺度；通常需更大GPU预算'],
        ['Gemma26B重新生成所有训练标注','不执行，也不建议考核阶段本机承担','仅26B BF16参数就约48.4GiB；量化/卸载会改变配方、速度与结果']]),
    "", "定量预算提示：每rank32、训练K=128、V=19,103，仅[B,K,V] BF16 logits约149.2MiB，不能代表训练总显存；672相比448的patch数量2.25倍，若使用显式二次attention，中间矩阵量可增长约5.06倍，实际实现可能使用节省内存内核。先profile最拥挤框数与最高分辨率，再决定batch，而非根据小图推理峰值猜测。", "", "## 结论证据与尚未证明的主张", "", "官方权重在完整公开PSG test的指标接近报告且独立复核一致；词表接口能工作但改写稳定性不足；框误差和图像干预可改变结果，需要结合分类型/采样指标判断环节。注意力集中不是视觉语义理解的充分证据。本轮没有证明严格训练未见语义泛化、所有数据集迁移、RA-4M生成增益或训练收敛。", "", "脚本保留详尽双方结果的目的，是让每项解释可以回到固定输入、GT、原始输出与明确的控制条件，而不是只展示汇总数字。"]
base02=e02['conditions'][0]['summary']
strong_trans=next(r for r in agg if r['mode']=='translation' and r['level']==.2)
strong_scale=next(r for r in agg if r['mode']=='scale' and r['level']==.2)
doc += ["", "## 最重要的实测发现及解释", "", f"E02原始300图R50={pct(base02['metrics']['R@50'])}；平移0.20的三seed均值={pct(strong_trans['metrics']['R@50']['mean'])}，大小0.20={pct(strong_scale['metrics']['R@50']['mean'])}。两类实验定义不同，强度数字不能当作同等物理误差。", "",
    f"平移0.20：空间pooled R从{pct(base02['types']['spatial']['pooled_R50'])}到{pct(strong_trans['types']['spatial']['pooled_R50']['mean'])}，语义从{pct(base02['types']['semantic']['pooled_R50'])}到{pct(strong_trans['types']['semantic']['pooled_R50']['mean'])}；候选覆盖仍分别{pct(strong_trans['types']['spatial']['pair_coverage']['mean'])}/{pct(strong_trans['types']['semantic']['pair_coverage']['mean'])}。这组证据把主要退化指向候选内谓词/排序而非对覆盖丢失；并不说明所有空间类别更敏感。", "",
    f"E03去掉pair logit后R50变化{100*(e03['0.0']['metrics']['R@50']-e03['1.0']['metrics']['R@50']):+.4f}百分点，mR50变化{100*(e03['0.0']['metrics']['mR@50']-e03['1.0']['metrics']['mR@50']):+.4f}百分点。幅度很小，不支持在这项严格GT框排序任务上宣称pair项必然带来显著收益；不能外推到阈值精确率或其他轴。", "",
    "E04灰度与原图接近，模糊、均值图和图像错配显著下降，说明现有权重的输出依赖图像输入与结构/细节。均值图不是纯几何训练模型，干预也改变候选相关性及场景分布，因此不能据此给出‘视觉关系理解占比’。",
    "", "![贯穿样本完整主图：图像、文本对比、索引与推理](../figures/T01_main_story.png)"]
doc += ["", f"样本计数澄清：E01的24个关系对来自{len({r['index'] for r in e01['cases']})}张独立图像；V01的12个关系对来自{len({r['index'] for r in att['cases']})}张独立图像。同图可能包含不同谓词/物体对，不能把24或12当作独立图像样本量。",
    "", "注意力显示采用每图/每query的归一化色标，框内质量是权重数值总和，亮色不代表跨图统一的绝对贡献。具体支持位置需对照原始图像/编号框而非只看热图。"]
doc += ["", "## V01数值精度附录：不能把诊断热图冒充原运行精确权重", "", "MHA快速SDPA路径不返回权重；我们从它实际输入的query/key/value重算显式权重，并分别保存BF16与FP32两套图。BF16显式与快速输出、FP32显式与快速输出、两精度的权重差均有实测。BF16与FP32的某些单patch权重差明显，不能忽略；主文FP32热图用于稳定诊断，不是原BF16快速执行路径的逐位还原。每个样例在V01页面都有两精度双方及绝对差图。", "",
    mdtable(['关系样例','BF16显式/快速输出max差','对应相对max差','FP32显式/快速max差','两精度权重max差','每区域平均head L1差'],[[r['case_id'],r['need_weights_vs_fast_output_max_abs'],r['need_weights_vs_fast_output_relative_max'],r['fp32_need_weights_vs_fast_output_max_abs'],r['bf16_vs_fp32_attention_max_abs'],r['bf16_vs_fp32_per_region_mean_head_L1']] for r in att['cases']]),"", "注意力图可回答‘数学上该query倾向读取什么patch’，不能直接回答‘哪些像素对最终关系是必要原因’；需要遮挡/干预甚至因果设计补充，E04只是第一步分布外探针。"]
chapter_path=REPORT/'T01_chapter.md'
assert chapter_path.exists(), 'Run trace_sample.py before rendering the complete report'
t01_start=next(j for j,t in enumerate(doc) if t.startswith('## T01：'))
t01_end=next(j for j in range(t01_start+1,len(doc)) if doc[j].startswith('## E01：'))
doc[t01_start:t01_end]=[doc[t01_start], '', chapter_path.read_text(encoding='utf-8'), '']
from review_report import revise
final_report=revise('\n'.join(doc).replace('固定选12张/例','固定选12个关系对（图像可能重复）').replace('12例24个主体/客体query','12个关系对的24个主体/客体query'))
(REPORT/'完整实验报告.md').write_text(final_report,encoding='utf-8')
page(REPORT/'index.html','RelateAnything复现实验总览',"<p><a href='完整实验报告.md'>完整中文报告</a> · <a href='E01_all_cases.html'>E01全部24例</a> · <a href='V01_attention.html'>V01注意力</a></p><img src='../figures/B01_main_table.png'><h2>贯穿样本</h2><img src='../figures/T01_trace.png'><h2>每种条件双方对比</h2>"+''.join(f"<p><a href='{name}'>{esc(title)}</a></p>" for name,title in paired_links)+"<h2>失败定位</h2>"+''.join(f"<p><a href='{r['stage']}_{r['index']:04d}.html'>{esc(r)}</a></p>" for r in failure_cases))
script_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (c.PROJECT/'scripts').glob('*') if p.is_file()}
index_path=REPORT/'index.html'
index_path.write_text(index_path.read_text(encoding='utf-8').replace('<h2>贯穿样本</h2>', '<h2>贯穿样本</h2><p><a href="T01_detailed.html">T01完整实测：原始标注、全部中间量、词表与方向对照、逐GT评测</a></p>'),encoding='utf-8')
index_path.write_text(index_path.read_text(encoding='utf-8').replace('<h2>贯穿样本</h2>','<p><a href="审查修订与新增实验.md">2026-10-16审查修订与新增实测</a> · <a href="E01b_semantic_review.html">E01b语义分层与全部整网对照</a> · <a href="证据包使用说明.md">可携证据包</a></p><h2>贯穿样本</h2>'),encoding='utf-8')
c.save(c.PROJECT/'manifests/script_hashes.json',script_hashes)
slides=["# 20分钟论文分享提纲与讲稿", "", "本材料只引用本轮真实结果，不包含未做的训练/生成结果。", "",
    "1. **2分钟：任务与问题**。展示T01_main_story：输入图像+框，输出有向关系，候选词表不是自由文本生成。问题是视觉/几何/语言各能支持什么证据。",
    "2. **3分钟：数据生成与测量边界**。论文RA-4M语义/grow/空间轮属于论文流程；本轮无原始日志，所以只讲机制示意与PSG最终标注审查。展示粗框/改写语境例，解释未标注不等于负例。",
    "3. **5分钟：真实样本前向**。用T01_regions、V01_riding_1、V01_scene_riding_1讲主体/客体/union/contact→关系查询→W[46]='riding'。展示score=sigmoid(pred_logit+pair_logit)，alpha按谓词而非图像。注意力不是因果归因。",
    f"4. **3分钟：可信基线**。展示B01_main_table：R50={pct(bmet['R@50'])}，mR50={pct(bmet['mR@50'])}，F1={pct(bmet['F1@50'])}。说明2179全推理/2177计分、14关系残差、独立复算0差；本轮官方权重评测，不是重新训练。",
    f"5. **5分钟：自己的对照**。E01原词胜出率{pct(E01sum['original_beats_controls_rate'])}，改写分别胜过控制{pct(E01sum['paraphrase_each_beats_controls_rate'])}，替换一致{pct(E01sum['replacement_binary_consistency'])}；打开失败样本完整六候选。E02展示两种扰动与三seed曲线、候选覆盖高却谓词退化。E03贡献很小；E04像素干预下降，但分布外不能证明因果语义机制。",
    "6. **2分钟：局限与后续**。5070Ti已完成完整基准与多条件探索；训练需正式train/val、损失资源和单步profile，梯度累积不等价单次对比负集合。严格未见语义、RA-4M各轮增益、SGDet和其他轴未证明。", "",
    "## 导师追问时的证据入口", "", "- 你自己做了什么：scripts、configs、manifest、output/logs，全部双方HTML。",
    "- 是否看过GT：GT框作为规定输入，GT关系只用于评分；evaluate中的targets=None。",
    "- 换词表就算开放泛化吗：编码任意短语、跨数据集、严格训练未见语义是三个不同主张。",
    "- 为什么不用Attention证明理解：权重描述读取位置，不直接给因果贡献；显式重算还存在数值差异。",
    "- 为什么不训练：用户限定本轮不训练；已给可行性与资源缺口，不把未做工作包装成收敛证据。"]
(REPORT/'论文分享_20分钟讲稿.md').write_text('\n'.join(slides),encoding='utf-8')
# Keep public figure/page captions aligned with the measured execution route.
v01_path=REPORT/'V01_attention.html'
v01_path.write_text(v01_path.read_text(encoding='utf-8').replace('显式与快速输出最大差','显式与need_weights=False替代输出最大差'),encoding='utf-8')
slides_path=REPORT/'论文分享_20分钟讲稿.md'
slides_path.write_text(slides_path.read_text(encoding='utf-8')+'\n\n## 审查后讲述修订\n\n原E01数字只作为预设短语探针，不称严格同义鲁棒性。E01b事后助手语义分层仍缺独立人审。E03图像级区间跨零。V01原调用默认need_weights=True，profiler见bmm/softmax；FP32是诊断图。正式幻灯片与录屏未交付，不把本讲稿称作演讲验收通过。详见审查修订与新增实验.md。\n',encoding='utf-8')
print(f'Rendered {len(paired_links)} complete paired condition galleries, 24 vocab cases, {len(att["cases"])} attention cases, report and figures.',flush=True)
