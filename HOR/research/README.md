# HOR 研究实验

本目录根据用户提供的《RelateAnything_研究方向评估》建立实验，沿用 HOR 的500张固定随机样本。原始实验保持独立；本目录保存新增配置、脚本、核验和报告。

人工视觉审计、身体部位与真实三维接触标注分别记录来源。来自已有GT的自动复算、预测部位和受控几何实验使用各自的评测协议；受控三维实验不替代真实人体重建。

模型权重、下载数据、缓存和原始运行结果存放于被 Git 忽略的 models、data、.work 和 output 目录。可查验的表格、图表、逐例证据和记录写入 reports。

报告索引见[`reports/README.md`](reports/README.md)。优先查看[`研究方向评估_全量迭代与验收报告.md`](reports/研究方向评估_全量迭代与验收报告.md)，其中逐项区分已执行实验、代理测量、人工流程准备和缺少三维资源的工作。

## 复跑入口

在仓库根目录执行以下命令，会读取本机已经保存的模型输出，重新计算区域、解码、部位、主动补检测与受控三维实验，检查Mask2Former实际加载和未融合区域协议，并核查交付文件。

```powershell
powershell -ExecutionPolicy Bypass -File HOR\research\scripts\run_research.ps1
```

添加 `-RerunModels` 会把已有区域和主动补检测原始输出移动到本机忽略目录 `.work/model_reruns/`，随后完整运行区域模型、关系模型、人体关键点模型与两种局部检测策略，再执行同样的统计检查。归档可恢复，脚本不删除旧结果。需要原HOR固定500张图像、原始logits、下载的COCO/Visual Genome元数据和本地权重；这些大文件没有进入Git。脚本遇到缺少输入或计算失败会立即停止。

人工审计独立执行。空白审查表已经导出，默认复跑不会覆盖表格；填写后需要按[人工审计协议](reports/human_audit/ANNOTATION_PROTOCOL.md)冻结。当前完整交付检查明确要求标签仍为空；未来完成真实审查后，需要同步更新验收状态与检查条件。

环境使用既有隔离目录 `.venv-eval`。运行时软件版本、CUDA设备与全部Python依赖记录在[`environment_snapshot.json`](reports/environment_snapshot.json)，交付文件签名和检查结果分别写入[`delivery_manifest.json`](reports/delivery_manifest.json)与[`delivery_verification.json`](reports/delivery_verification.json)。代码没有安装训练组件或修改系统Python环境。
