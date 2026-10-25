"""B01/E03 full test; E02 and E04 fixed subset, with full paired records."""
import json
import time
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image, ImageFilter, ImageOps
import common as c

ds,model,E,train_names=c.setup()
manifest=json.loads((c.PROJECT/'manifests/samples.json').read_text(encoding='utf-8'))
subset=manifest['subset']
batchsize=c.CFG['batch_size']
torch.cuda.reset_peak_memory_stats()
full_audits={w:c.Audit(ds.predicate_names,w) for w in c.CFG['pair_weights']}
start=time.perf_counter()
for a in range(0,len(ds),batchsize):
    indices=list(range(a,min(a+batchsize,len(ds))))
    images,boxes,counts,targets=c.collate_fn([ds[i] for i in indices])
    out=c.forward(model,images,boxes,counts)
    for audit in full_audits.values(): audit.update(out,targets,indices,ds)
    if a%(batchsize*25)==0: print(f'B01/E03 {a}/{len(ds)}',flush=True)
torch.cuda.synchronize()
full_results={str(w):a.compute() for w,a in full_audits.items()}
c.save(c.PROJECT/'output/B01_baseline/results.json',full_results['1.0'])
c.write_rows(c.PROJECT/'output/B01_baseline/predictions.jsonl',full_audits[1.0].rows)
c.save(c.PROJECT/'output/E03_pair_weight/results.json',full_results)
c.write_rows(c.PROJECT/'output/E03_pair_weight/weight0_predictions.jsonl',full_audits[0.0].rows)
c.save(c.PROJECT/'output/B01_baseline/runtime.json',{'seconds':time.perf_counter()-start,'images':len(ds),
    'scope':'includes two evaluators, independent audit and per-GT diagnostic CPU logging; excludes initial model/text setup',
    'peak_allocated_gib':torch.cuda.max_memory_allocated()/2**30,'gpu':torch.cuda.get_device_name(),
    'parameters':sum(p.numel() for p in model.parameters()),'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),
    'trainable_F32_weight_gradient_Adam_moments_lower_bound_gib':sum(p.numel() for p in model.parameters() if p.requires_grad)*16/2**30})
del full_audits

def perturb(boxes,counts,indices,mode,level,seed):
    out=boxes.clone()
    stats={'clipped_centers':0,'clipped_extents':0,'boxes':0}
    for b,(index,n) in enumerate(zip(indices,counts.tolist())):
        gen=torch.Generator().manual_seed(seed*100000+index)
        noise=torch.randn(n,2,generator=gen)
        stats['boxes']+=n
        if mode=='translation':
            before=boxes[b,:n,:2]+noise*level*boxes[b,:n,2:]
            stats['clipped_centers']+=int(((before<0)|(before>1)).any(-1).sum())
            out[b,:n,:2]=before.clamp(0,1)
        else:
            before=boxes[b,:n,2:]*torch.exp(noise*level)
            stats['clipped_extents']+=int(((before<1e-4)|(before>1)).any(-1).sum())
            out[b,:n,2:]=before.clamp(1e-4,1)
    return out,stats

conditions=[('original',0.,0)]+[(m,l,s) for m in ('translation','scale') for l in c.CFG[m+'_levels'] for s in c.CFG['perturbation_seeds']]
e02=[]
for ci,(mode,level,seed) in enumerate(conditions):
    audit=c.Audit(ds.predicate_names); stats={'clipped_centers':0,'clipped_extents':0,'boxes':0}
    t=time.perf_counter()
    tag=f'{mode}_{level:.2f}_seed{seed}'
    image_dir=c.PROJECT/'output/E02_box_perturbation'/tag/'images'; image_dir.mkdir(parents=True,exist_ok=True)
    for a in range(0,len(subset),batchsize):
        indices=subset[a:a+batchsize]
        images,boxes,counts,targets=c.collate_fn([ds[i] for i in indices])
        changed,local=perturb(boxes,counts,indices,mode,level,seed) if mode!='original' else (boxes,{'boxes':int(counts.sum()),'clipped_centers':0,'clipped_extents':0})
        for k,v in local.items(): stats[k]+=v
        out=c.forward(model,images,changed,counts)
        audit.update(out,targets,indices,ds)
        for b,index in enumerate(indices):
            if index in subset[:c.CFG['visual_examples_per_condition']]:
                im,raw,_=ds.load_raw(index)
                c.boxed(im,raw).save(image_dir/f'{index:04d}_original.jpg')
                c.boxed(im,changed[b,:counts[b]].numpy()).save(image_dir/f'{index:04d}_perturbed.jpg')
    result={'condition':mode,'level':level,'seed':seed,'tag':tag,'summary':audit.compute(),'clipping':stats,'seconds':time.perf_counter()-t}
    c.save(image_dir.parent/'summary.json',result)
    c.write_rows(image_dir.parent/'predictions.jsonl',audit.rows)
    e02.append(result)
    print(f'E02 {ci+1}/{len(conditions)} {tag} R50={result["summary"]["metrics"]["R@50"]:.4f}',flush=True)
c.save(c.PROJECT/'output/E02_box_perturbation/results.json',{'conditions':e02,'indices':subset,
    'protocol':'translation: Gaussian center shift relative to each box w/h, dimensions unchanged; scale: exp(Gaussian*level) extent changes, centers unchanged. centers clamp[0,1], extents clamp[1e-4,1]; corners may exceed frame, downstream prompt clamps as upstream. Identities and GT fixed. Common random numbers within seed. Not detector IoU matching/SGDet.'})

e04=[]
for mode in c.CFG['image_conditions']:
    audit=c.Audit(ds.predicate_names); t=time.perf_counter()
    image_dir=c.PROJECT/'output/E04_image_evidence'/mode/'images'; image_dir.mkdir(parents=True,exist_ok=True)
    for a in range(0,len(subset),batchsize):
        indices=subset[a:a+batchsize]
        images,boxes,counts,targets=c.collate_fn([ds[i] for i in indices])
        if mode=='original': changed=images
        elif mode=='grayscale': changed=(images*torch.tensor([.299,.587,.114]).view(1,3,1,1)).sum(1,keepdim=True).expand(-1,3,-1,-1).contiguous()
        elif mode=='mean_image': changed=images.mean((2,3),keepdim=True).expand_as(images).contiguous()
        elif mode=='blur':
            changed=torch.stack([torch.from_numpy(np.asarray(Image.fromarray((im.permute(1,2,0).numpy()*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(12)),dtype=np.float32).transpose(2,0,1).copy()/255) for im in images])
        else:
            donor_indices=[subset[(subset.index(i)+len(subset)//2)%len(subset)] for i in indices]
            changed=torch.stack([ds[i][0] for i in donor_indices])
        out=c.forward(model,changed,boxes,counts); audit.update(out,targets,indices,ds)
        for b,index in enumerate(indices):
            if index in subset[:c.CFG['visual_examples_per_condition']]:
                im,raw,_=ds.load_raw(index)
                c.boxed(im,raw).save(image_dir/f'{index:04d}_original.jpg')
                altered=Image.fromarray((changed[b].permute(1,2,0).numpy().clip(0,1)*255).astype(np.uint8))
                c.boxed(altered,boxes[b,:counts[b]].numpy()).save(image_dir/f'{index:04d}_changed.jpg')
    result={'condition':mode,'summary':audit.compute(),'seconds':time.perf_counter()-t}
    c.save(image_dir.parent/'summary.json',result); c.write_rows(image_dir.parent/'predictions.jsonl',audit.rows)
    e04.append(result)
    print(f'E04 {mode} R50={result["summary"]["metrics"]["R@50"]:.4f}',flush=True)
c.save(c.PROJECT/'output/E04_image_evidence/results.json',{'conditions':e04,'indices':subset,
    'protocol':'fixed 300 image IDs/GT boxes. blur radius12 on448 image; grayscale fixed luminance; mean_image each-channel spatial mean; permuted donor rotated150 subset indices with recipient boxes and labels held fixed. OOD interventions; not pure geometry-only trained baseline.'})
print('All benchmark interventions completed.',flush=True)
