"""Shared fixed protocol. No training, no edits to official model code."""
import json
import os
import hashlib
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "reproduction"
sys.path.insert(0, str(ROOT / "RelateAnything"))
from relsgg.checkpoint import load_checkpoint, build_model_from_ckpt
from relsgg.data import RelationDataset, collate_fn
from relsgg.eval.evaluator import SGClsEvaluator
from relsgg.scoring import ScoreContract
from relsgg.text.student import encode_texts_student
from relsgg.vocabulary import TRAIN_TEMPLATES

CFG = json.loads((PROJECT / "configs/experiments.json").read_text(encoding="utf-8"))

def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")

def setup():
    torch.set_num_threads(8)
    torch.manual_seed(CFG["seed"])
    np.random.seed(CFG["seed"])
    assert torch.cuda.is_available(), "CUDA required for measured protocol"
    assert torch.cuda.is_bf16_supported(), 'BF16 is required; do not replace precision'
    os.environ['HF_HUB_OFFLINE']='1'
    os.environ['TRANSFORMERS_OFFLINE']='1'
    ds = RelationDataset(str(ROOT / "data/PSG/packed/psg"), "test", resolution=448, max_objects=100)
    ck = load_checkpoint(str(ROOT / "models/relsgg-vits16plus/model.pth"))
    train_names = list(ck.get("pred_names", []))
    # Released files store stripped EMA under model, not ema_model. Require
    # explicit provenance rather than accepting the loader's implicit fallback.
    assert ck.get('stripped_weights')=='ema' and ck.get('model'), 'Expected published stripped EMA'
    assert ck.get('backbone_config'), 'Embedded backbone config required; no network initialization'
    model = build_model_from_ckpt(ck, weights='raw', strict=True)
    loaded=model.state_dict(); sd=ck['model']
    missing=sorted(set(loaded)-set(sd)); unexpected=sorted(set(sd)-set(loaded))
    assert set(missing)<= {'W_obj'} and not unexpected,(missing,unexpected)
    mismatched=[k for k in sd if not torch.equal(loaded[k].cpu(),sd[k].cpu())]
    assert not mismatched,mismatched
    loading={'checkpoint_keys':list(ck),'selected_field':'model','stripped_weights':ck['stripped_weights'],
        'epoch':ck.get('epoch'),'strict':True,'missing_keys':missing,'unexpected_keys':unexpected,
        'allowed_missing':['W_obj'],'mismatched_values':mismatched,'verified_tensors':len(sd),
        'embedded_backbone_config':True,'external_backbone_download':False,'device':'cuda','autocast':'bfloat16'}
    model=model.cuda().eval()
    del ck
    E = encode_texts_student(ds.predicate_names, str(ROOT / "models/relsgg-vits16plus/text_student.pt"), templates=TRAIN_TEMPLATES)
    assert (ROOT/'models/relsgg-vits16plus/tokenizer.json').is_file(), 'Local tokenizer required'
    model.vocab_head.set_vocabulary_matrix(ds.predicate_names, E)
    model.reparameterize()
    model.sampler.final_budget = min(500, model.sampler.geo_budget)
    encoded_binding=hashlib.sha256(E.detach().float().cpu().numpy().tobytes()).hexdigest()
    binding=hashlib.sha256(model.vocab_head.W.detach().float().cpu().numpy().tobytes()).hexdigest()
    loading.update({'vocabulary':ds.predicate_names,'templates':TRAIN_TEMPLATES,'W_sha256_array':binding,
                    'encoded_E_sha256_array':encoded_binding,'matrix_note':'W hash after official set_vocabulary_matrix and reparameterize normalization; E hash before installation',
                    'W_shape':list(E.shape),'final_budget':model.sampler.final_budget,'geo_budget':model.sampler.geo_budget})
    run_id=os.environ.get('REPRO_RUN_ID','manual')
    save(PROJECT/'output/loading'/f'{run_id}_{Path(sys.argv[0]).stem}.json',loading)
    print(f"[load-audit] published stripped EMA in model; {len(sd)} tensors equal; missing={missing}; offline CUDA BF16; W={binding}",flush=True)
    return ds, model, E, train_names

def subset_indices(ds):
    return np.linspace(0, len(ds)-1, min(CFG["subset_images"], len(ds)), dtype=int).tolist()

@torch.inference_mode()
def forward(model, images, boxes, counts):
    with torch.autocast("cuda", dtype=torch.bfloat16):
        return model(images.cuda(), boxes.cuda(), counts.cuda(), targets=None)

class Audit:
    """Official metric plus independent image/class macro and failure stages."""
    def __init__(self, predicates, weight=1.0):
        self.predicates = predicates
        self.weight = weight
        self.ev = SGClsEvaluator(topk=[20,50,100], num_predicates=len(predicates), score_mode="sigmoid", graph_constraint=True,
                                 contract=ScoreContract(pair_weight=weight))
        self.rows = []

    def update(self, out, targets, indices, ds):
        self.ev.update(out, targets)
        spatial = set(CFG["spatial_predicates"])
        for b, (t, index) in enumerate(zip(targets, indices)):
            valid = out["valid_mask"][b]
            sub = out["sub_idx"][b][valid].cpu().tolist()
            obj = out["obj_idx"][b][valid].cpu().tolist()
            lg = out["logits"][b][valid].float()
            pl = out["pair_logits"][b][valid].float()
            fused = lg + self.weight*pl[:,None]
            best, pred = fused.max(-1)
            order = best.topk(min(100,len(best))).indices.cpu().tolist()
            pred = pred.cpu().tolist()
            score = torch.sigmoid(best).cpu().tolist()
            logit = best.cpu().tolist()
            ranked = [[sub[j],obj[j],pred[j],score[j],logit[j]] for j in order]
            gt = t["relations"].tolist()
            unique = {tuple(g) for g in gt}
            hitsets = {k:unique & {tuple(p[:3]) for p in ranked[:k]} for k in (20,50,100)}
            pairmap = {(s,o):j for j,(s,o) in enumerate(zip(sub,obj))}
            stages, type_stats = Counter(), {}
            diagnostics=[]
            for s,o,p in sorted(unique):
                j=pairmap.get((s,o))
                if (s,o,p) in hitsets[50]: stage="hit50"
                elif j is None: stage="not_selected"
                elif pred[j] != p: stage="wrong_predicate"
                else: stage="rank_below50"
                stages[stage]+=1
                diagnostics.append({"s":s,"o":o,"gt_predicate":self.predicates[p],"stage":stage,"slot":j,
                    "best_predicate":self.predicates[pred[j]] if j is not None else None,
                    "gt_predicate_logit":float(lg[j,p]) if j is not None else None,
                    "pair_logit":float(pl[j]) if j is not None else None,
                    "gt_fused_logit":float(fused[j,p]) if j is not None else None,
                    "gt_predicate_rank":int((lg[j]>lg[j,p]).sum())+1 if j is not None else None})
            for kind in ("spatial","semantic"):
                g={x for x in unique if (self.predicates[x[2]] in spatial)==(kind=="spatial")}
                selected={x for x in g if x[:2] in pairmap}
                correct={x for x in selected if pred[pairmap[x[:2]]]==x[2]}
                type_stats[kind]={"gt":len(g),"selected":len(selected),"correct_best":len(correct),"hits50":len(g&hitsets[50])}
            self.rows.append({"index":index,"file_name":ds.file_names[index],"box_count":int(ds.img_meta[index,4]),"gt":gt,
                "ranked":ranked,"recall":{str(k):len(hitsets[k])/len(unique) if unique else None for k in hitsets},
                "stages":dict(stages),"types":type_stats,"selected_pairs":[list(p) for p in pairmap],"diagnostics":diagnostics})

    def compute(self):
        metrics=self.ev.compute()
        independent={}
        for k in (20,50,100):
            image_rec=[]
            cls_rec={}
            for r in self.rows:
                gt={tuple(g) for g in r["gt"]}
                if not gt: continue
                hits=gt&{tuple(p[:3]) for p in r["ranked"][:k]}
                image_rec.append(len(hits)/len(gt))
                total=Counter(g[2] for g in r["gt"])
                hit=Counter(g[2] for g in hits)
                for c,n in total.items(): cls_rec.setdefault(c,[]).append(hit[c]/n)
            rr=float(np.mean(image_rec)) if image_rec else 0
            mr=float(np.mean([np.mean(v) for v in cls_rec.values()])) if cls_rec else 0
            independent.update({f"R@{k}":rr,f"mR@{k}":mr,f"F1@{k}":2*rr*mr/(rr+mr) if rr+mr else 0})
        maxdiff=max(abs(metrics[k]-v) for k,v in independent.items())
        assert maxdiff<1e-10, maxdiff
        stages=Counter()
        types={kind:Counter() for kind in ("spatial","semantic")}
        for r in self.rows:
            stages.update(r["stages"])
            for kind in types: types[kind].update(r["types"][kind])
        for kind,v in types.items():
            v.update({"pooled_R50":v["hits50"]/v["gt"] if v["gt"] else 0,
                "pair_coverage":v["selected"]/v["gt"] if v["gt"] else 0,
                "selected_predicate_accuracy":v["correct_best"]/v["selected"] if v["selected"] else 0})
        return {"metrics":metrics,"independent":independent,"max_difference":maxdiff,"images":len(self.rows),
            "scored_images":sum(bool(r["gt"]) for r in self.rows),"stages":dict(stages),"types":types,
            "per_class":{self.predicates[i]:float(np.mean(v)) for i,v in self.ev._per_class_recall[50].items()}}

def write_rows(path, rows):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r,ensure_ascii=False)+"\n")

def pixel_boxes(boxes, size):
    b=np.asarray(boxes).copy()
    xy=np.concatenate([b[:,:2]-b[:,2:]/2,b[:,:2]+b[:,2:]/2],axis=1)
    return xy*np.array([size[0],size[1],size[0],size[1]])

def boxed(image, boxes, ids=None):
    image=image.copy(); draw=ImageDraw.Draw(image)
    xy=pixel_boxes(boxes,image.size)
    colors=["#ef4444","#2563eb","#16a34a","#f97316","#a855f7"]
    for j in (range(len(xy)) if ids is None else ids):
        x1,y1,x2,y2=xy[j]
        if x2<x1 or y2<y1: continue
        col=colors[j%len(colors)]
        draw.rectangle((x1,y1,x2,y2),outline=col,width=3)
        draw.rectangle((max(0,x1),max(0,y1),max(0,x1)+35,max(0,y1)+19),fill=col)
        draw.text((max(0,x1)+1,max(0,y1)+1),f"#{j}",fill="white")
    return image
