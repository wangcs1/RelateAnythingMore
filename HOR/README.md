# HOR：人相关关系抽取

给定图片，自动检测并编号人物与物体，调用 RelateAnything 官方权重，返回最多50条人相关有向关系。人物可以位于主语或宾语位置；人与人关系单独标记。

## 查看500张随机图片测试

- [实验报告](reports/HOR_500张实验报告.md)
- [全部500张图片索引](reports/500张图片索引.md)
- [逐图CSV](reports/逐图结果.csv)
- [完整成果与交付核验](reports/成果检查与交付说明.md)：可直接查阅的配图、六组逐图输出、全部评测与单张图片示例。
- `output/random500/predictions.jsonl`：两种框来源、三种候选模式、编号及完整分项输出。
- `output/random500/logits/`：每个参与评分的物体对的全部56类原始分数。
- `output/random500/sample_manifest.json`：固定随机种子、500张图片索引、文件名与配置。
- `output/random500/verification.json`：独立复算与编号、候选覆盖、源码及资源摘要检查。

## 单张新图片

在项目根目录使用已有隔离环境执行：

```powershell
& .\.venv-eval\Scripts\python.exe HOR/infer.py --image 'D:\images\example.jpg' --output HOR/output/my_image
```

输出包括 `relations.json`、带编号的 `objects.jpg` 和可阅读的 `result.md`。编号从0开始；红色表示人，蓝色表示其他物体。

每条关系包括 `subject_id`、`subject_label`、`predicate`、`object_id`、`object_label`、`person_ids`、`human_human`、分项 logit 与排序分数。没有检测到人物或没有第二个对象时返回空列表，并保存对应状态。

## 重复完整测试

```powershell
& .\HOR\run.ps1
```

从完整公开 PSG test 随机抽取500张图片，固定种子20261025，无放回，包含无人的图片。运行自动检测、真实框完整枚举、真实框400候选对照，生成逐图结果与报告，再完成独立核验。

只重新生成报告和核验已有结果：

```powershell
& .\HOR\run.ps1 -SkipInference
```

## 模型和环境

使用已有 `.venv-eval`、CUDA、Torch 与 torchvision，无需修改上游源码或安装额外依赖。关系权重位于项目原有 `models/relsgg-vits16plus/`。新增检测器权重来自 torchvision 官方 Faster R-CNN ResNet50 FPN V2，放在 `HOR/models/`，本机模型目录与缓存由 `.gitignore` 忽略。

原始预测、张量和编号图保留在本机 `HOR/output/`，由 `.gitignore` 忽略。可提交的编号图副本、逐图原始记录、单张图片示例、抽样清单、运行和核验记录归入 `HOR/reports/`。报告中的配图和文件链接均指向该目录内的文件，下载仓库后可以直接查阅。

报告文件摘要与本地链接核验：

```powershell
& .\.venv-eval\Scripts\python.exe HOR/export_reports.py --verify-only
```

```powershell
New-Item -ItemType Directory -Force HOR/models
curl.exe -L --fail -o HOR/models/fasterrcnn_resnet50_fpn_v2_coco-dd69338a.pth https://download.pytorch.org/models/fasterrcnn_resnet50_fpn_v2_coco-dd69338a.pth
```

数据集图片继续使用 `data/PSG/images/test/`，无需复制。只给单张新图片时无需读取测试图片和关系真值；56类词表从已有 PSG meta.json 读取。

## 结果解释

输出范围包含与人有关的空间关系、动作关系、人与人关系。为保留不同类型表达，每个有向物体对分别保留空间组和其他语义组的最佳谓词，再统一排序取 Top50。全部人相关物体对的两项预测继续保存在 JSONL 中。

候选分数只用于排序，实际存在多少交互需要结合原图核查。COCO 检测类别覆盖、检测漏失、最多40框、56类关系词表和 Top50 都会限制完整性。真实框条件和自动检测条件分开评测；原图框编号在每个条件内保持稳定。
