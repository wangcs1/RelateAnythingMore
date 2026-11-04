# 人—物关系人工审计协议

## 目的与状态

该审计用于评估关系候选的图像支持、实例归属、可见性与部位证据，并独立记录抽样图像中的关系。当前目录中的 CSV 只有抽样框架和空标签字段；没有任何人工标签，因此不能据此报告准确率、精确率、召回率或标注者一致性。

样本从 HOR 固定随机500条记录的499个不同源图像身份中按独立种子 `20261104` 均匀抽取100张图像。源身份由COCO ID与图像SHA-256识别；唯一一组重复图像只保留首次出现的记录。抽样不按是否有人、是否有GT关系或模型输出筛选。第一阶段只提供原始图像和空白字段；完整关系审查结束并冻结后，才能产生候选表。

## 标注单位

1. `images_blind.csv` 为每张图像预留 A、B 两个独立审查者槽位。分别记录可见人数、整张图像的审查状态、关系标注是否完整及不确定原因；填写匿名审查者编号、ISO 8601时间 `reviewed_at`、版本 `review_version`，并在 `saw_model_outputs` 填写 `no`。
2. `relations_blind.csv` 为每张图像、每位审查者预留独立记录。逐行增加独立识别的主体和宾语实例、描述、边界框、有方向的谓词及可见证据。无关系时明确标记对应图像的 `relation_review_status=complete_no_relations`；至少一条关系时标记 `complete_with_relations` 并填写关系记录。不能把空白误作零关系。
3. 填写两个表格后运行 `--stage freeze`。脚本会检查100张图像均由两位不同审查者完成、两张表中的审查者一致、状态完整、人物端点已指明且边界框位于原始图像范围，再记录两个CSV的SHA-256。任何内容变更都会使下一阶段校验失败。自动检查只能验证字段和流程，无法验证审查者是否真正独立或标注是否正确。
4. 只有冻结成功后，运行 `--stage candidates` 才会生成 `candidate_review.csv`。每个候选复制为 A、B 两个独立审查行；图像内候选顺序已用固定种子打乱，文件不含模型分数与原始排名。
5. 对候选涉及的可见身体部位与对象区域分别填写 `supporting_part` 和 `target_region`。没有足够像素证据时填写不可见或未知；语义上合理不等于图像中可见。

## 独立关系字段

| 字段 | 填写要求 |
|---|---|
| `relation_subject_instance_id` / `relation_object_instance_id` | 审查者自行编号的实例身份；同一图像的同一对象保持相同编号，身份编号不引用模型输出 |
| `relation_subject_description` / `relation_object_description` | 主体与宾语的类别、颜色或位置描述，用于区分多人和同类对象 |
| `relation_subject_is_person` / `relation_object_is_person` | 分别填写 `yes` 或 `no`；每条关系至少一个端点属于人物 |
| `relation_subject_box_xyxy` / `relation_object_box_xyxy` | 原始图像像素坐标，填写JSON数组 `[xmin,ymin,xmax,ymax]`，正面积且位于图像范围 |
| `relation_predicate` | 有方向的关系标签，保留审查者原始用语；后续谓词归一化映射需要独立冻结 |
| `visual_support` | `supported`或明确的未知标签；独立清单中的未知关系单独保存，不能充当召回率的确定真值 |
| `evidence_note` / `visibility` / `uncertainty_reason` | 记录图像证据、可见性与未知原因；未知关系必须填写原因 |

独立关系召回率在审查者完成标注后计算：先冻结谓词归一化和分歧裁决，再以主体与宾语边界框各自IoU≥0.5进行实例匹配，方向和谓词均须一致。当前没有人工标注，也没有形成最终裁决后的参考集合，因此尚无相应召回结果。

## 建议标签

- `visual_judgment`：`supported`（像素支持该实例与有向关系）、`contradicted`（像素反驳）、`unknown_occluded`（相关区域被遮挡）、`unknown_resolution`（分辨率不足）、`ambiguous_instance`（对象或人物归属不明确）、`not_observable`（静态图像不足以判定）。
- `visibility`：`clear`、`partial`、`occluded`、`out_of_frame`、`not_applicable`。
- `part_evidence`：记录可见的身体部位及证据范围。可用术语包括左侧/右侧手部、左侧/右侧前臂、左侧/右侧上臂、躯干、髋部、左侧/右侧大腿、左侧/右侧小腿、左侧/右侧足部、全身、未知；左右均按人物自身解剖方向。
- `target_region`：用对象实例描述和可复核的区域/表面文字描述；确实能标出时记录图像坐标。不得把“holding”直接改写成接触真值。
- `uncertainty_reason`：遮挡、多人混淆、边界不清、动作状态无法从静态图像区分、对象表面不可见或其他具体原因。

## 独立性与一致性

完整关系标注至少由两名不知道模型输出和 PSG GT 的标注者独立完成。候选逐条审查至少由两人独立完成，随后对分歧进行第三人裁决。至少20张图像双重标注以估计关系标签一致性；分别报告原始一致率、类别分布和 Cohen's κ（多标注者时可用 Krippendorff's α）。未知和不可见类别必须保留，不能强行并入反例。

审查前后应记录 CSV SHA-256、标注者匿名 ID、审查日期、文件版本、是否看过模型输出及裁决记录。不要把此协议的建议当作已发生的标注流程。

## 结果计算边界

候选精确率只在预先规定的可判定子集上计算，并同时报告未知/遮挡比例和覆盖率；把未知排除后必须明确分母。关系召回率只能相对于第一阶段独立列出的关系计算，并处理两阶段关系实例匹配。PSG GT 指标另行报告，不与人工支持标签合并。人工审计结果不由模型置信度或候选排名定义。

## 文件说明

- `images_blind.csv`：100张抽样图像、每张图像两个独立审查槽位及完整性状态。
- `relations_blind.csv`：每张图像、每位审查者至少一行；存在关系时按关系追加记录。
- `candidate_review.csv`：完成第一阶段并冻结后生成的去分数、随机排序候选，每候选两个独立审查槽位。
- [`manifest.json`](../../output/human_audit/manifest.json)：本机生成的抽样种子、样本位置与图像哈希；冻结后附两份审查表的哈希。

## 导出流程

当前标签表为空。首次导出只生成盲审阶段文件：

```powershell
.\.venv-eval\Scripts\python.exe HOR\research\scripts\prepare_human_audit.py --stage blind
```

两位审查者独立填完图像与完整关系表后，冻结并生成候选表：

```powershell
.\.venv-eval\Scripts\python.exe HOR\research\scripts\prepare_human_audit.py --stage freeze
.\.venv-eval\Scripts\python.exe HOR\research\scripts\prepare_human_audit.py --stage candidates
```
