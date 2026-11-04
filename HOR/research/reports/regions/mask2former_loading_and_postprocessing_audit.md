# Mask2Former加载与区域后处理审计

## 审计对象和运行范围

本审计使用Transformers 5.14.1，检查当前区域实验实际使用的官方检查点`facebook/mask2former-swin-tiny-coco-panoptic`，revision为`df6b1142ff50c3276559d9d78f35f6a579c75a77`。权重SHA256为`8e154c4f946f4fad9aa511a7d706c89c4254cc6eee28fd932e52c32394c5a29f`。

脚本在CPU加载真实权重，核对实际参数、缓冲、源码调用路径及已保存的500条候选记录。没有读取图像像素、执行图像前向或调用视觉功能；未改变区域推理、端点选择与融合策略。结构化完整证据见[加载及后处理审计JSON](mask2former_loading_audit.json)，其中包括逐缓冲比较、全部重复类别记录、源码全文片段、版本和文件签名。

## 实际加载结果

| 检查项 | 实际结果 |
|---|---|
| 参数设备 | ['cpu'] |
| 缺失参数 | 2项：最终Swin LayerNorm的weight和bias |
| 多余检查点项 | 12项：旧版relative_position_index缓冲 |
| 形状不符 / 加载错误 | 0 / 0 |
| 最终LayerNorm的weight / bias取值 | [1.0] / [0.0] |
| 旧版位置索引与新版重建索引 | 12 / 12组逐元素完全相同 |
| 学习得到的相对位置偏置表 | 12组均与检查点逐元素完全相同 |
| stage1至stage4的输出归一化参数 | 8个weight/bias张量均与检查点逐元素完全相同 |

LayerNorm的weight=1、bias=0是固定初始化值。该设置仍会归一化输入，不能据此将LayerNorm解释为恒等变换。对本实验有效输出的判断依据来自下面的调用路径。

## 最终LayerNorm与实际特征路径

`Mask2FormerForUniversalSegmentation.forward → Mask2FormerModel.forward → Mask2FormerPixelLevelModule.forward → SwinBackbone.forward → SwinModel.forward → SwinEncoder.forward`构成主干调用路径。

SwinModel对编码器的`last_hidden_state`执行最终`self.layernorm`，同时将编码器收集的`reshaped_hidden_states`原样放入返回对象。SwinBackbone通过`outputs.reshaped_hidden_states`取得各stage的二维特征，再分别调用已有权重的`hidden_states_norms.stage1`至`stage4`，构成`feature_maps`。Mask2FormerPixelLevelModule只将这些`feature_maps`交给像素解码器。

最终`self.layernorm`会执行，但它产生的`last_hidden_state`没有被该Backbone的特征输出路径消费，且没有原地修改各stage特征。两项缺失参数因此不改变Mask2Former当前消费的特征。这里的结论限定于当前源码与调用配置；跨Transformers版本的所有数值行为没有在本审计中逐版本比较。

## 位置索引缓冲

检查点保存12个形状为49×49的`attention.self.relative_position_index`。当前Swin根据7×7窗口位置确定性重建索引，保存为2401个元素的非持久缓冲，`persistent=False`使其不进入state_dict。逐一将旧缓冲展平后，与实际加载模型的新缓冲比较，12组全部相同。

相对位置偏置表`relative_position_bias_table`属于学习参数。本审计额外确认12张偏置表及8个stage输出归一化张量均与safetensors中的数值完全相同。加载报告的两类提示没有表明这些有效参数缺失；本检查确认了它们的实际数值。

## 当前区域后处理协议

当前区域实验采用未融合的query区域：每个通过阈值与有效区域检查的Mask2Former查询可以形成一个候选，同一stuff类别可以对应多个互不合并的区域。`label_ids_to_fuse`没有传入，处理器将其设置为空集合。thing表示可区分的物体实例，stuff表示地面、墙面、天空等场景区域。

固定阈值为类别分数>0.35、mask阈值0.5、区域保留比例>0.8；thing类编号为0—79，stuff类编号为80—132。模型返回的查询区域经过像素竞争，随后将每个区域转换为其像素包围矩形。该协议保留了查询层面的stuff区域数量。

完整500条记录包含1,721个stuff候选；23条记录含同一stuff类别的多个查询区域。相对于每张图像每个stuff类别只保留一个区域，共有27个额外区域。这里的数量来自完整候选缓存，尚未经过每张图像最多8个stuff端点的选择。

| stuff类别 | 超过每张图像每个类别一个区域的额外数量 |
|---|---:|
| banner（80） | 1 |
| cardboard（83） | 1 |
| curtain（85） | 1 |
| mirror-stuff（93） | 1 |
| platform（96） | 1 |
| road（100） | 2 |
| shelf（104） | 1 |
| towel（108） | 1 |
| wall-wood（112） | 1 |
| window-other（115） | 1 |
| tree-merged（116） | 1 |
| cabinet-merged（120） | 2 |
| table-merged（121） | 5 |
| floor-other-merged（122） | 5 |
| grass-merged（125） | 1 |
| building-other-merged（129） | 1 |
| wall-other-merged（131） | 1 |

按stuff类别融合会改变区域的包围矩形、候选数量及后续端点选择，相关指标需要在明确的融合协议下重新计算。本次结果仅对应当前未融合协议，没有声称完成融合与未融合的关系指标对照。

## 本机融合实现的源码边界

处理器允许通过`label_ids_to_fuse`指定需要按类别融合的标签。对于当前133类配置，全部stuff标签集合为`set(range(80, 133))`。当前实验的有效集合为空，因此后面描述的融合分支没有参与现有结果。

本机`compute_segments`在每个有效查询后追加一项`segments_info`。指定融合且同一类别出现多次时，代码会再次使用同一个segment ID并继续追加记录，返回列表因而可能包含重复ID。当前区域提取器逐项遍历该列表，未来启用融合时需要保证每个最终区域只产生一个候选。

该函数还把`current_segment_id`同时用于编号递增和旧stuff编号读取：遇到已出现的stuff类别时，将其赋回旧编号；后续遇到新类别时在这个值上递增。如果这个旧编号小于此前已经分配的最大编号，后续新类别可能再次使用已分配ID。本审计只记录这条可复核的静态控制路径，没有运行融合分支，也没有测量它在当前500张图像上出现的频率。

## 源码、版本和复算

| 实际源码文件 | SHA256 |
|---|---|
| [backbone_utils.py](../../../../.venv-eval/Lib/site-packages/transformers/backbone_utils.py) | `9c73b85ceeaeb1e4b088c01b8f9dc74ed28b7a28becfc0711677cc22389f8165` |
| [conversion_mapping.py](../../../../.venv-eval/Lib/site-packages/transformers/conversion_mapping.py) | `cb40dd3862fd187a95948e40945f66a661cc4d64466b6544fc4111fd1bb312a3` |
| [modeling_utils.py](../../../../.venv-eval/Lib/site-packages/transformers/modeling_utils.py) | `d8bf1879d6f582888b6cf47b4d63070260285a3bd1dc94ce7e1373304f74168a` |
| [image_processing_mask2former.py](../../../../.venv-eval/Lib/site-packages/transformers/models/mask2former/image_processing_mask2former.py) | `1f3895d029cb1ad740e0f823d6ffcf01b982924f3db039ec56bd9327c98e0d43` |
| [modeling_mask2former.py](../../../../.venv-eval/Lib/site-packages/transformers/models/mask2former/modeling_mask2former.py) | `c3ccebf3c222c8164b1602044111eec111394055b656b637d9d5f6665f049ba7` |
| [modeling_swin.py](../../../../.venv-eval/Lib/site-packages/transformers/models/swin/modeling_swin.py) | `341b43d6fdd6846ff166a7472ab03a444191b0dee6b387f77d9395d9a925d7e5` |
| [audit_mask2former.py](../../scripts/audit_mask2former.py) | `acd845d6bf1d6c0ffc647740d9eed1c1b53e4fbd8bdac28feb4f8634b1e7de6a` |

JSON证据另保存相关forward函数、初始化函数和后处理函数的源码起始行及完整片段；安装目录中的文件可按上述签名核验。复算脚本为[audit_mask2former.py](../../scripts/audit_mask2former.py)，从仓库根目录执行：

```powershell
.\.venv-eval\Scripts\python.exe HOR\research\scripts\audit_mask2former.py
```

该脚本使用现有隔离环境、官方本地权重和完整候选缓存，在CPU完成参数比较，并重新生成本报告及JSON证据。区域实验结果见[Thing/Stuff端点实验报告](thing_stuff_region_study.md)。
