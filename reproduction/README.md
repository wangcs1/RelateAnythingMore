# RelateAnything 复现工作区

先读 [完整实验报告](reports/完整实验报告.md)，浏览 [可视化与全部对比入口](reports/index.html)。

初次阅读建议打开 [附术语解释版报告](reports/完整实验报告_附术语解释版.md)，正文与原版一致，附12节术语解释和56类关系中文对照。独立附录见 [术语解释附录](reports/术语解释附录.md)。主报告更新后可执行 `python reproduction/scripts/make_glossary_copy.py` 同步副本；完整重跑也会自动生成。

2026-10-16审查迭代：已完整重跑所有既有条件，新增 [审查修订与新增实验](reports/审查修订与新增实验.md)、[E01b完整语义/整网对照](reports/E01b_semantic_review.html) 和 [可携证据包说明](reports/证据包使用说明.md)。R01输出在output/R01_review，实际加载分支在output/loading，每阶段起止时间/命令/退出码/完整日志在output/execution。E01b仍为事后助手重标，独立人审未完成。

## 目录

```text
reproduction/
  scripts/       可执行实验、诊断、作图及报告脚本
  configs/       运行前固定的样本规则、词表、扰动与种子
  manifests/     样本索引、环境、资源/脚本哈希、指导文件快照
  output/        每实验JSON/JSONL/NPZ、对比输入图与日志
  figures/       PNG和SVG汇报图
  reports/       完整报告、全部双方HTML、20分钟分享材料
  archive/       上轮evaluation及阅读文档，保留原内容
  todo.md        本轮任务进度
```

根目录的 `RelateAnything` 是未修改的官方源码，`models` 与 `data` 是既有官方权重和完整PSG资源，`.venv-eval` 是隔离环境。它们不重复复制进实验文件夹，版本与哈希由manifest绑定。顶层两份指导文件保留作为用户输入，快照放入manifests。

## 重跑

```powershell
Set-Location D:\relateAny
& .\reproduction\scripts\run_all.ps1
```

脚本依次执行：资源与样本manifest → V01/E01/T01 → B01/E02/E03/E04 → 全部图表/报告。使用已有独立环境和本地权重/数据，不进行训练或VLM生成。完整重跑覆盖同名实验结果，旧archive不覆盖。输出日志在 `output/logs`。

也可以单独执行：

```powershell
. .\reproduction\scripts\activate.ps1
python reproduction/scripts/attention_vocab.py
python reproduction/scripts/trace_sample.py
python reproduction/scripts/benchmark_interventions.py
python reproduction/scripts/render_report.py
```

准备脚本需要先有本轮固定资源；不是从空机器自动下载所有依赖的安装器。新机器先建立Python3.12隔离环境、CUDA13版Torch并恢复manifest锁定资源，再根据requirements快照安装。冻结文件含editable源仓库记录，应以本地官方checkout安装 `pip install -e ./RelateAnything`。

## 查验你实际执行了什么

- `configs/experiments.json`：固定变量、干预、种子、选择与解释判据。
- `manifests/samples.json`：24词表样本与300图索引，均不按模型成功与否挑选。
- `output/B01_baseline`：2179张记录、官方和独立主指标一致。
- `output/E01_vocabulary`：所有短语分项分数、文本cos、词表替换实际前向差异、正反向对诊断。
- `output/V01_attention`：主体/客体/union/contact所有head权重和真实场景feature map，显式/快速注意力精度审计。
- `output/T01_trace`：真实PSG原始标注到pack/targets、两阶段采样重放、整网中间张量、全部56词分项分数、全部400对排名、三组整网词表替换和原向/反向对照、逐GT评测。详见 [T01完整图文页](reports/T01_detailed.html)。
- `output/E02_box_perturbation`：25个条件，300图各条件完整GT诊断及前三seed统计。
- `output/E03_pair_weight`：全test固定logits的w=0与w=1比较。
- `output/E04_image_evidence`：5种输入条件、300图配对预测。
- `reports`：29个完整配对条件页面，展示双方GT、top20和每GT全部诊断；原始JSONL另保留top100。E01全部6候选均展示。
- `manifests/context_review.json`：24例语境审查说明，非独立人工真值，不是RA-4M生成质量评估。

## 归档说明

`archive/evaluation` 是历史成果快照，不作为新的重跑入口。移动后历史脚本里原来的ROOT和evaluation路径不再适用，旧报告的相对链接也可能只适用于原布局；当前报告、脚本和资源manifest是本轮有效入口。旧训练准备继续位于工作区之外的 `D:\relateAny_training_removed_20261010`，本轮没有恢复或使用。
