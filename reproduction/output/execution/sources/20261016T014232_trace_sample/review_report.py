"""Render review fixes from actual R01 artifacts; imported by render_report."""
import html
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/'reproduction';OUT=PROJECT/'output/R01_review';REPORT=PROJECT/'reports'
def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def fmt(v): return '未判定/未采样' if v is None else f'{v:.6f}' if isinstance(v,(float,np.floating)) else str(v)
def mdtable(headers,rows):
    return '| '+' | '.join(headers)+' |\n|'+'|'.join('---' for _ in headers)+'|\n'+''.join('| '+' | '.join(fmt(v).replace('|','/') for v in row)+' |\n' for row in rows)+'\n'
def htable(headers,rows):
    return '<table><tr>'+''.join('<th>'+html.escape(h)+'</th>' for h in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(fmt(v))+'</td>' for v in r)+'</tr>' for r in rows)+'</table>'
STYLE="body{font:16px 'Microsoft YaHei',sans-serif;max-width:1500px;margin:auto;padding:24px}p{line-height:1.8}img{max-width:100%}table{border-collapse:collapse;width:100%;font-size:13px;margin:18px 0}th,td{border:1px solid #bbb;padding:7px;text-align:left}th{background:#e2e8f0}section{margin-top:40px}"

def build_chapter():
    lineage=load(OUT/'dataset_lineage.json');sem=load(OUT/'E01b_semantic_strata.json')
    ci=load(OUT/'paired_bootstrap.json');gpu=load(OUT/'all24_full_forward_correspondence.json')
    route=load(OUT/'attention_execution.json');replay=load(OUT/'B01_fixed_batch_replay.json')
    recompute=load(OUT/'independent_recompute.json')
    loads=[load(p) for p in (PROJECT/'output/loading').glob('*benchmark_interventions.json')]
    assert loads;loading=loads[-1]
    e01={r['case_id']:r for r in load(PROJECT/'output/E01_vocabulary/results.json')['cases']}
    annotation=load(PROJECT/'configs/e01b_semantic_review.json')
    parts=['## R01：审查后补充实验与验收（2026-10-16）','',
        '本次保留原实验设计并实际重跑V01/E01、T01、B01/E03、E02全部25条件和E04全部5条件；新增原始标注溯源、32个条件独立复算、24对整网/缓存对应、图像级bootstrap和注意力profiler。旧报告、脚本、清单已在archive/review_20261016_before保留。下面区分已经闭合的证据和仍未满足的更强主张。','',
        '### R01.1 审查要求逐项回应','',
        mdtable(['审查项','本次操作与证据','判定'],[
            ['P0 产物缺失/跨机器链接','Windows原工作区实际存在；完整重跑并保留逐阶段命令、起止时间、退出码和日志；新增可携zip及独立核验脚本','本机闭合；不声称已经在审查者Mac上GPU复跑'],
            ['P0 加载分支/静默降级','显式验证发布文件stripped_weights=ema、内嵌骨干配置、416个参数张量与checkpoint逐项相等；离线CUDA/BF16','本次实际路径已审查，未发现未声明替代'],
            ['P1 E01语义混杂','保留旧24对全部结果为短语探针；新增E01b事后四层语义标签、负控制不确定标记、图像聚类bootstrap','部分闭合；没有独立盲审，严格同义鲁棒性仍未认证'],
            ['P1 排除图片与pack差异','全部2186图逐图链、7张排除及2张未计分清单；官方转换器重新打包逐数组相等','公开版本内部闭合；论文14条差异未归因'],
            ['P1 RA-4M生成审计','明确区分D01的PSG最终标注审查与RA-4M逐轮生成','未执行、可选项；不算完成'],
            ['P2 E02/E04覆盖解释','final_budget=geo_budget=400，视觉相关性只重排几何幸存者','修正；未新增final_budget128研究'],
            ['P2 V01执行路径','观测原调用返回值；同精度默认/显式重放；profiler保存实际算子与Chrome trace','已纠正原快速路径说法'],
            ['P2 文字及方向失败','正间隔+1.0184文字纠正；原向/反向全部短语双分支数值','已修正并补失败诊断'],
            ['训练/其他评测轴/演讲','不训练；未增加A2/A6、真实SGDet、正式幻灯片或录屏','本轮未执行，不填通过']]),
        '### R01.2 权重、文本空间、运行与证据包','',
        f'实际checkpoint含model但不含ema_model；stripped_weights="ema"、epoch=11。官方release/strip_checkpoint.py将发布EMA放在model字段。新入口不再依赖默认EMA缺失时的隐式选择：先要求发布来源标签为ema，再显式取model。载入后核对{loading["verified_tensors"]}个张量，missing={loading["missing_keys"]}，unexpected={loading["unexpected_keys"]}，数值不一致={loading["mismatched_values"]}。W_obj是官方允许的训练缓冲例外，本文件实际没有缺失项。','',
        f'骨干来自checkpoint内嵌配置，HF_HUB_OFFLINE与TRANSFORMERS_OFFLINE均开启；未从外部下载骨干。要求CUDA可用且支持BF16，没有OOM后自动缩小batch/尺寸/预算或换CPU的异常分支。配套学生与本地tokenizer按已有资源哈希核对；56词顺序、模板及矩阵绑定记录在loading日志，实际安装并重参数化后W数组SHA256={loading["W_sha256_array"]}。编码器原始E摘要另记，官方安装时的单位化可能改变末位，因此不混同E和W的字节哈希。','',
        '新启动器run_stage.py将实际命令、Asia/Shanghai时间、结束状态、退出码、脚本/common/配置SHA256与完整输出写入output/execution；运行非零退出会终止流程。旧日志没有追补虚构时间，新证据来自本次完整重跑。GPU复跑与文本缓存比较还逐样本绑定图像/框/权重/配置哈希。','',
        f'B01固定首批index0–7按原batch8及相同补齐形状复跑，top100三元组完全相同，融合logit最大绝对差={replay["fused_logit_max_abs"]}（容差{replay["tolerance"]}）。全部{len(recompute)}个条件从原始逐图预测重算R/mR/F1@20/50/100及失败阶段，最大指标差={max(v["metric_max_abs"] for v in recompute)}。这些验证支持本次执行链，不保证未来任意输入永远没有兼容路径。','',
        '[32条件独立复算](../output/R01_review/independent_recompute.json) · [固定批GPU复跑](../output/R01_review/B01_fixed_batch_replay.json) · [资源与全部产物清单](../manifests/evidence_inventory.json) · [可携证据包使用说明](证据包使用说明.md)','',
        '### R01.3 样本排除和关系数差异逐项溯源','',
        '公开原始JSON共有2186图、13705条关系。按max_objects=40、min_rels=0转换：7图仅1个框且原始无关系，被排除；59条关系引用的对象不在前40个框内，37条为自环，13705−59−37=13609。框不因退化或越界删除而移动索引，14个退化框被保留。Dataset上限100高于pack上限40，未再截框；谓词按文件顺序映射，无OOV丢弃、无几何标签过滤。','',
        mdtable(['排除image_id','文件名','原始框数','原始关系数','原因'],[[r['image_id'],r['file_name'],r['raw_boxes'],r['raw_relations'],'不足2框'] for r in lineage['excluded_images']]),
        mdtable(['Dataset index','image_id','原始框数','原始/pack/loaded关系数','300子集中'],[[r['index'],r['image_id'],r['raw_boxes'],f"{r['raw_relations']}/{r['pack_relations']}/{r['loaded_relations']}",r in lineage['subset_unscored']] for r in lineage['unscored_images']]),
        '两张未计分图仍参与推理，原始关系本来为0，不是解码失败或为提高指标跳样。300图各条件都含index531/image2338128，故均299图计分；完整条件均2177图计分。独立重算逐条件检查未计分索引相同。','',
        '新增诊断重新调用官方pack_split并输出到R01_review/repacked，img_meta、boxes、box_cats、rels四数组和file_names逐元素/逐项相等。本次能归因公开JSON到本地pack的全部96条关系过滤，但论文13623与当前13609仍差14条；当前没有论文原始pack可做差集，不能把“保留14个退化框”误当“解释14条关系差异”。最终定位为当前公开转换版本下的近似指标复现，不能称逐数据完全一致。','',
        '[全部2186图及每条丢弃关系](../output/R01_review/dataset_lineage.json) · [官方重新打包一致性](../output/R01_review/repack_equality.json)','',
        '### R01.4 E01b：语义分层后的事后诊断','',
        '旧E01的58.33%是48个预设改写中胜过控制的比例，混有等义、近义、改变含义和证据不足，现统一称“探索性短语敏感性探针”。不能直接称严格同义鲁棒性。新增E01b没有换样本，也没有声称事前盲审：助手已接触历史分数，重新按原图、编号框、语境解释标记48个改写，并逐控制词标记可判假/不确定。标签文件固定保留，不用分数门槛生成语义标签。','',
        'E=语境等义，N=近义但有额外或不同强调，X=不等义，U=不确定。负控制只在该有向对被助手认为确实不成立时记F，不能因为是反向词就自动作假。分层表的胜出率只用同一对全部3个控制均为F的比较；所有其他结果仍在明细展示，不删除失败。','',
        mdtable(['语义层','全部改写比较数','控制均可判假的比较数','图片聚类数','改写胜出率','原词胜出率','图像聚类95%区间'],[[label,v['all_comparisons'],v['with_confirmed_controls'],v['independent_images'],None if v['win_rate'] is None else 100*v['win_rate'],None if v['original_win_rate'] is None else 100*v['original_win_rate'],None if v['cluster_bootstrap_ci95'] is None else [round(100*x,2) for x in v['cluster_bootstrap_ci95']]] for label,v in sem['summary'].items()]),
        '等义且控制可判假的子集为12个改写比较、9张图，11/12胜出，约91.67%，图像聚类bootstrap区间70%–100%。这与旧58.33%的分母和语义标签均不同，不能说模型“经修复提高了”；模型完全没训练。重采样以图片为单位，同图全部对与改写一起进入，3000次、seed20261016；样本小且事后标注，区间只反映这批探索样本的波动，不消除审查偏差。','',
        '仍缺第二位独立标注者和新样本盲评，因此严格“独立核验的同义鲁棒性”未完成。我们提供助手分层及可供独立复核的完整材料，不把它冒充已认证新基准。各条标签理由、原词、改写、所有负控制、对应图像与全部分数双侧展示于下页。','',
        '[E01b全部24对/48改写的图像与完整候选对照](E01b_semantic_review.html) · [语义标签文件](../configs/e01b_semantic_review.json) · [分层与区间原始结果](../output/R01_review/E01b_semantic_strata.json)','',
        '### R01.5 全24对缓存文本头与同精度整网对应','',
        f'每个原E01样本重新执行BF16视觉前向，安装6词并运行整网，取该次真实q_sem/q_spa按同样dtype和矩阵形状再算文本头；24对逐单元差全为0。另运行完整FP32整网，再用该次自己的FP32查询重算头，24对差也全为0。原E01“BF16视觉查询转FP32文本头”的历史分数与本次复算最大差={max(r["cached_replay_max_abs"] for r in gpu):.9g}，小于1e-5。','',
        'FP32整网可能改变视觉特征与采样顺序，所以必须按(s,o)身份而非沿用槽位对齐。它不是原E01缓存查询的同值替代；我们在全部候选表同时给历史缓存FP32头、复算缓存FP32头、完整BF16、完整FP32四列。只有同一次整网与它自己的查询头，才能主张数值等价。跨精度数值差如实保留。','',
        '[全部24对逐候选四列整网/缓存比较及哈希](E01b_semantic_review.html) · [原始对应结果](../output/R01_review/all24_full_forward_correspondence.json)','',
        '### R01.6 角色反转异常：正确的riding不代表被动表达也正确','',
        'T01的riding在人→自行车方向高分正确，但两个被动/反向表述偏好却反了。以下是同图同对的FP32缓存头结果；分数没有因为修改解释而改写。','']
    trace=next(r for r in gpu if r['case_id']=='riding_1')
    focus=[r for r in trace['candidates'] if r['phrase'] in ['riding','being ridden by','carrying a rider']]
    parts+=[mdtable(['同一短语','人→车logit','车→人logit','人→车semantic cos','车→人semantic cos','alpha','与riding文本cos'],[[r['phrase'],r['recorded_cached_FP32_logit'],r['reverse_cached_FP32_logit'],r['forward_semantic_cos'],r['reverse_semantic_cos'],r['alpha'],r['text_cos_to_original']] for r in focus]),
        '从两分支分解可以定位为：文本编码器确实为这些短语产生不同的向量，但当前图的语义查询与被动/载人文本向量的匹配在原向更高；不是只因pair logit融合导致，因为原始predicate logit已经反向偏好。alpha很小时主要来自语义分支。该结果支持“文本—视觉方向对齐在此失败”的定位；不能单靠这张图将责任唯一归给文本编码器或视觉投影，更不能由余弦差推断训练数据成因。进一步因果归因需独立验证集、受控合成方向样本及训练干预，本轮不做。','',
        '全部24对每个可用反向槽的六短语logit、score与分解均公开，未采样的反向明确标出，不用强制加入GT反向对改变原推理协议。','',
        '[全部方向对照原始结果](../output/R01_review/direction_all_cases.json) · [T01正反向图文原页](T01_detailed.html)','',
        '### R01.7 不确定性：以图片为重采样单位','',
        '固定原始逐图输出，对同一组图片成对有放回抽样；每次重新聚合R、每图每类mR及其调和F1，而非平均现成图级F1。E03采2177张有GT图、3000次；E04采299图、1500次；统一seed20261016。区间为百分位95%区间、未作多重比较校正；本数据上bootstrap不会恢复未知总体或稀有未出现类别，不用它证明所有分布普适。','',
        mdtable(['对照（后者减基准）','指标','点差/百分点','配对95%区间/百分点'],[[tag,key,100*v['point'],[round(100*x,5) for x in v['ci95']]] for tag,rec in ci.items() for key,v in rec['delta'].items()]),
        'E03的R/mR/F1区间均跨0，无法仅凭+0.0859个百分点宣称pair项有益或有害；也不等于证明绝对等效。E04灰度区间也跨0；模糊、均值图、错配图的下降区间在0以下，支持此批样本上的分数/召回依赖图像证据，但分布外干预不能给出“视觉理解占比”。E02原有三seed标准差只反映随机扰动重复的变动，不能称图片抽样置信区间。','',
        '![图像级配对差与95%区间](../figures/R01_bootstrap.png)','',
        '![E03微小差异的放大视图](../figures/R01_E03_bootstrap_zoom.png)','',
        '[配对bootstrap参数与原始结果](../output/R01_review/paired_bootstrap.json)','',
        '### R01.8 预算解释与注意力执行路径的实测纠正','',
        '本协议geo_budget=final_budget=400：几何筛掉的对不会恢复，幸存对又全都进入后续计算，视觉相关性只重排而不删对。E04只换图不换框，几何分数和幸存集合按结构不变；因此其GT候选覆盖相同是预期现象，不能额外表述为“视觉采样器对图像干预很鲁棒”。E02改变框可改变几何候选，须结合候选覆盖与对内分类看。final_budget=128的采样研究未运行，不混进正式主表。','',
        '旧V01把need_weights=False的另算路径称为原快速路径，现纠正。官方SoftSpatialPool.cross_attn调用未传need_weights，默认True。观测原调用确实返回平均头权重；实际输入Q已包含框角点与base_query，K/V已经加入scene_pe；attn_mask=None，本轮不传mask栅格。重新调用同输入的默认路径与原输出相等；BF16显式per-head返回与默认输出相等，头平均权重亦相等。不是凭PyTorch类名猜SDPA内核。','',
        mdtable(['pool调用','原返回权重shape','默认重放/原输出max差','BF16显式/原输出max差','原权重/显式头均值max差','原输出/need_weights=False对照max差'],[[v['block'],v['actual_returned_weight_shape'],v['captured_default_replay_max_abs'],v['default_vs_explicit_perhead_output_max_abs'],v['actual_avg_weights_vs_explicit_head_mean_max_abs'],v['actual_vs_need_weights_false_max_abs']] for v in route['blocks']]),
        '实际默认调用profiler记录包含'+', '.join(v['name'] for v in route['operator_evidence'] if v['name'].startswith('aten::'))+'，没有把人为need_weights=False对照算子混入本次原调用trace。之前0.375/0.25的数值是原显式计算与替代无权重路径的差，不是“原运行权重无法返回”的证据。FP32图仍是诊断重算，BF16/FP32单patch差异仍保留；不再称FP32解决了还原精度问题。','',
        '[执行路径、输入契约与算子清单](../output/R01_review/attention_execution.json) · [实际调用profiler Chrome trace](../output/R01_review/attention_actual_trace.json) · [BF16/FP32双方图](V01_attention.html)','',
        '### R01.9 交付与剩余边界','',
        '报告继续使用完整实验报告.md原路径，本次覆盖更新，术语解释版同步。证据包提供reports、figures、scripts、configs、manifests、逐图预测、张量、日志及固定官方源码与标注数组，保持原目录层级；不能只传Markdown。CPU机器可用标准库核验清单和重算32个条件指标；GPU重跑仍需对应官方权重、完整图像和锁定隔离环境，这些外部大资源的哈希与版本另列，不冒称空机器零依赖复现。','',
        '本轮仍未执行训练、RA-4M逐轮生成审计、额外正式评测轴、真实SGDet、第二人独立语义盲审、正式演讲录屏。论文14条关系差异未归因。可认证表述限定为：本次Windows机器上已审查并复跑这些明确条件，未发现未经声明的权重、数据、设备、精度或协议替代；独立复算与固定样本对应通过。不能签署“所有非训练要求全完成”或“所有未来路径绝无fallback”。','']
    # Honest full candidate display: original + all alternatives and controls.
    body='<p>事后助手重标，非独立盲审。E等义/N近义/X不等义/U不确定；控制F可判假/U不确定。全部24对、48改写及六个候选完整保留。</p>'
    lookup={r['case_id']:r for r in gpu}
    for name,r in e01.items():
        g=lookup[name];label=annotation['cases'][name]
        body+=f'<section><h2>{html.escape(name)} / index={r["index"]} / #{r["s"]}→#{r["o"]}</h2><img src="../output/E01_vocabulary/images/{name}_pair.jpg"><p>{html.escape(annotation["notes"][name])}</p>'
        allrows=[]
        for j,(v,t) in enumerate(zip(r['candidates'],g['candidates'])):
            role='原词' if j==0 else label[j-1]
            allrows.append([v['phrase'],role,v['predicate_logit'],t['replay_cached_FP32_logit'],t['complete_BF16_logit'],t['complete_FP32_logit'],v['fused_score'],t['reverse_cached_FP32_logit'],t['alpha'],t['forward_semantic_cos'],t['reverse_semantic_cos']])
        body+=htable(['完整六短语','语义/控制标签','旧缓存F32 logit','重算缓存F32 logit','完整BF16 logit','完整FP32 logit','原向融合score','反向缓存logit','alpha','原向semantic cos','反向semantic cos'],allrows)
        body+=f'<p>FP32槽位={g["slot_FP32"]}，BF16槽位={g["slot_BF16"]}；按物体对身份对齐，未按槽位硬对齐。独立负控制结论仍需第二位标注者复核。</p></section>'
    (REPORT/'E01b_semantic_review.html').write_text('<!doctype html><html lang="zh"><meta charset="utf-8"><title>E01b 完整语义分层与整网比较</title><style>'+STYLE+'</style><h1>E01b：语境标签、全部候选及整网/缓存对照</h1>'+body+'</html>',encoding='utf-8')
    plt.rcParams['font.sans-serif']=['Microsoft YaHei','DejaVu Sans'];plt.rcParams['axes.unicode_minus']=False
    fig,axs=plt.subplots(1,3,figsize=(16,5));labels=list(ci)
    for ax,metric in zip(axs,['R@50','mR@50','F1@50']):
        for y,name in enumerate(labels):
            v=ci[name]['delta'][metric];point=100*v['point'];lo,hi=[100*x for x in v['ci95']]
            ax.plot([lo,hi],[y,y],color='#2563eb',lw=2);ax.scatter([point],[y],color='#2563eb')
        ax.axvline(0,color='gray',ls='--');ax.set_yticks(range(len(labels)),labels if ax==axs[0] else []);ax.set_title(metric+' 差/百分点');ax.invert_yaxis()
    fig.suptitle('同图配对bootstrap：点估计与95%百分位区间（非跨seed标准差）');fig.tight_layout()
    fig.savefig(PROJECT/'figures/R01_bootstrap.png',dpi=150,bbox_inches='tight');fig.savefig(PROJECT/'figures/R01_bootstrap.svg',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4))
    for j,(key,v) in enumerate(ci['E03_weight0_minus_weight1']['delta'].items()):
        lo,hi=[100*x for x in v['ci95']];ax.plot([lo,hi],[j,j],lw=3,color='#2563eb');ax.scatter([100*v['point']],[j],color='#2563eb')
    ax.axvline(0,color='#ef4444',ls='--');ax.set_yticks([0,1,2],['R@50','mR@50','F1@50']);ax.set_xlabel('w=0减w=1 / 百分点');ax.set_title('E03放大：95%区间均跨0，不能据点差宣称优劣');fig.tight_layout()
    fig.savefig(PROJECT/'figures/R01_E03_bootstrap_zoom.png',dpi=160);plt.close(fig)
    chapter='\n\n'.join(parts)
    (REPORT/'审查修订与新增实验.md').write_text(chapter,encoding='utf-8')
    return chapter

def revise(text):
    replacements={
        '日期：2026-10-15。':'实验始于2026-10-15；审查修订及重新运行日期：2026-10-16。',
        '改写稳定性不足':'预设短语响应存在差异，严格同义鲁棒性仍需独立核验',
        '不是原BF16快速执行路径的逐位还原':'不是原BF16执行的逐位还原',
        '原BF16快速执行路径':'原BF16执行路径',
        '显式/快速注意力精度审计':'原显式调用/替代无权重调用及跨精度诊断',
        '显式重算全部head的query→patch注意力':'以相同输入重算全部head的query→patch注意力',
        'FP32重算缓解BF16显式MHA/快速SDPA差异，并记录二者误差；不是运行时逐位相同的因果解释。':'原调用默认need_weights=True，实际路径由新增profiler核验；FP32是另行诊断，BF16/FP32及need_weights=False替代调用的差异分别记录，不把替代调用误称原路径。',
        'MHA快速SDPA路径不返回权重；我们从它实际输入的query/key/value重算显式权重，并分别保存BF16与FP32两套图。':'本次原MHA调用默认need_weights=True且返回平均权重，实测为bmm/softmax路径。我们从实际query/key/value重算per-head权重，并分别保存BF16与FP32两套图；need_weights=False仅是另算对照。',
        'BF16显式与快速输出、FP32显式与快速输出':'BF16显式与无权重替代输出、FP32显式与无权重替代输出',
        'BF16显式/快速输出max差':'BF16显式/无权重替代输出max差',
        'FP32显式/快速max差':'FP32显式/无权重替代max差',
        '因而同时看覆盖与已选对准确率。':'因而同时看覆盖与已选对准确率；但本轮两阶段预算相等，E04固定框下覆盖不变是结构预期，不是视觉采样鲁棒性的独立证据。',
        '候选对可随视觉改变，故同时看覆盖与已选对准确率。':'本轮两阶段预算均400，固定框下几何候选集合不随图像改变；视觉相关性会重排，覆盖不变是结构预期，仍需比较最佳谓词与全图排序。',
    }
    for a,b in replacements.items(): text=text.replace(a,b)
    chapter=build_chapter()
    marker='## 交付范围与组织'
    notice='## 本次审查修订的结论先读\n\n本报告已按2026-10-15审查意见迭代，并在2026-10-16实际完整重跑。原E01保留为短语探针，不再将58.33%解释为严格同义鲁棒性；新增E01b只是事后助手语义分层，独立盲审仍缺。注意力原路径说法已纠正，样本排除已逐图溯源，E03新增区间跨零。详细证据与验收状态见[R01审查修订与新增实验](审查修订与新增实验.md)。\n\n'
    return text.replace(marker,notice+marker,1)+'\n\n'+chapter
