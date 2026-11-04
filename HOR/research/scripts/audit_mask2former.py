import ast
from collections import Counter
import hashlib
import inspect
import json
import os
from pathlib import Path

from safetensors import safe_open
import torch
import transformers
from transformers import AutoImageProcessor, Mask2FormerForUniversalSegmentation
from transformers.models.mask2former import image_processing_mask2former, modeling_mask2former
from transformers.models.swin import modeling_swin
from transformers.utils import logging


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "HOR/research/reports/regions"
EVIDENCE_PATH = REPORT_DIR / "mask2former_loading_audit.json"
REPORT_PATH = REPORT_DIR / "mask2former_loading_and_postprocessing_audit.md"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def file_record(path):
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size,
            "sha256": digest(path)}


def function_record(function):
    function = inspect.unwrap(function)
    path = Path(inspect.getsourcefile(function)).resolve()
    lines, first_line = inspect.getsourcelines(function)
    return {"path": path.relative_to(ROOT).as_posix(), "first_line": first_line,
            "source": "".join(lines)}


def new_backbone_key(old_key):
    return old_key.replace(".encoder.encoder.", ".encoder.swin.encoder.").replace(
        ".attention.self.relative_position_", ".attention.relative_position_bias.relative_position_")


def candidate_audit(path, labels, expected_images):
    with path.open(encoding="utf-8") as handle:
        records = [json.loads(line) for line in handle if line.strip()]
    require(len(records) == expected_images, "Candidate audit requires the complete fixed image sample")
    require(len({record["index"] for record in records}) == expected_images, "Candidate image indices repeat")
    total_stuff = 0
    extra_by_class = Counter()
    repeated_images = []
    for record in records:
        stuff = [item for item in record["candidates"] if item["source"] == "mask2former_stuff"]
        total_stuff += len(stuff)
        counts = Counter(item["source_category_id"] for item in stuff)
        repeats = {category: count for category, count in counts.items() if count > 1}
        if repeats:
            extra_by_class.update({category: count - 1 for category, count in repeats.items()})
            repeated_images.append({
                "index": record["index"], "file_name": record["file_name"],
                "repeated_classes": [{"category_id": category, "label": labels[str(category)],
                                      "region_count": repeats[category],
                                      "regions": [item for item in stuff if item["source_category_id"] == category]}
                                     for category in sorted(repeats)]})
    return {"source": file_record(path), "images": len(records), "stuff_candidates": total_stuff,
            "images_with_repeated_stuff_class": len(repeated_images),
            "extra_regions_beyond_one_per_class": sum(extra_by_class.values()),
            "extra_regions_by_class": [{"category_id": category, "label": labels[str(category)], "extra": count}
                                       for category, count in sorted(extra_by_class.items())],
            "repeated_images": repeated_images}


def report_link(path, line=None):
    target = Path(os.path.relpath(ROOT / path, REPORT_DIR)).as_posix()
    return target if line is None else f"{target}:{line}"


def build_report(evidence):
    loading = evidence["actual_cpu_loading"]
    buffer_checks = evidence["checkpoint_checks"]["relative_position_indices"]
    candidates = evidence["unfused_candidate_inventory"]
    config = evidence["postprocessing_protocol"]["thresholds"]
    lines = [
        "# Mask2Former加载与区域后处理审计", "",
        "## 审计对象和运行范围", "",
        f"本审计使用Transformers {evidence['environment']['transformers']}，检查当前区域实验实际使用的官方检查点`{evidence['checkpoint']['repository']}`，revision为`{evidence['checkpoint']['revision']}`。权重SHA256为`{evidence['checkpoint']['weights']['sha256']}`。",
        "",
        "脚本在CPU加载真实权重，核对实际参数、缓冲、源码调用路径及已保存的500条候选记录。没有读取图像像素、执行图像前向或调用视觉功能；未改变区域推理、端点选择与融合策略。结构化完整证据见[加载及后处理审计JSON](mask2former_loading_audit.json)，其中包括逐缓冲比较、全部重复类别记录、源码全文片段、版本和文件签名。", "",
        "## 实际加载结果", "",
        "| 检查项 | 实际结果 |", "|---|---|",
        f"| 参数设备 | {loading['parameter_device_types']} |",
        f"| 缺失参数 | {len(loading['missing_keys'])}项：最终Swin LayerNorm的weight和bias |",
        f"| 多余检查点项 | {len(loading['unexpected_keys'])}项：旧版relative_position_index缓冲 |",
        f"| 形状不符 / 加载错误 | {len(loading['mismatched_keys'])} / {len(loading['error_msgs'])} |",
        f"| 最终LayerNorm的weight / bias取值 | {loading['final_layernorm_weight_unique']} / {loading['final_layernorm_bias_unique']} |",
        f"| 旧版位置索引与新版重建索引 | {len(buffer_checks)} / {len(buffer_checks)}组逐元素完全相同 |",
        "| 学习得到的相对位置偏置表 | 12组均与检查点逐元素完全相同 |",
        "| stage1至stage4的输出归一化参数 | 8个weight/bias张量均与检查点逐元素完全相同 |", "",
        "LayerNorm的weight=1、bias=0是固定初始化值。该设置仍会归一化输入，不能据此将LayerNorm解释为恒等变换。对本实验有效输出的判断依据来自下面的调用路径。", "",
        "## 最终LayerNorm与实际特征路径", "",
        "`Mask2FormerForUniversalSegmentation.forward → Mask2FormerModel.forward → Mask2FormerPixelLevelModule.forward → SwinBackbone.forward → SwinModel.forward → SwinEncoder.forward`构成主干调用路径。",
        "",
        "SwinModel对编码器的`last_hidden_state`执行最终`self.layernorm`，同时将编码器收集的`reshaped_hidden_states`原样放入返回对象。SwinBackbone通过`outputs.reshaped_hidden_states`取得各stage的二维特征，再分别调用已有权重的`hidden_states_norms.stage1`至`stage4`，构成`feature_maps`。Mask2FormerPixelLevelModule只将这些`feature_maps`交给像素解码器。",
        "",
        "最终`self.layernorm`会执行，但它产生的`last_hidden_state`没有被该Backbone的特征输出路径消费，且没有原地修改各stage特征。两项缺失参数因此不改变Mask2Former当前消费的特征。这里的结论限定于当前源码与调用配置；跨Transformers版本的所有数值行为没有在本审计中逐版本比较。", "",
        "## 位置索引缓冲", "",
        "检查点保存12个形状为49×49的`attention.self.relative_position_index`。当前Swin根据7×7窗口位置确定性重建索引，保存为2401个元素的非持久缓冲，`persistent=False`使其不进入state_dict。逐一将旧缓冲展平后，与实际加载模型的新缓冲比较，12组全部相同。",
        "",
        "相对位置偏置表`relative_position_bias_table`属于学习参数。本审计额外确认12张偏置表及8个stage输出归一化张量均与safetensors中的数值完全相同。加载报告的两类提示没有表明这些有效参数缺失；本检查确认了它们的实际数值。", "",
        "## 当前区域后处理协议", "",
        "当前区域实验采用未融合的query区域：每个通过阈值与有效区域检查的Mask2Former查询可以形成一个候选，同一stuff类别可以对应多个互不合并的区域。`label_ids_to_fuse`没有传入，处理器将其设置为空集合。thing表示可区分的物体实例，stuff表示地面、墙面、天空等场景区域。",
        "",
        f"固定阈值为类别分数>{config['score_threshold']}、mask阈值{config['mask_threshold']}、区域保留比例>{config['overlap_mask_area_threshold']}；thing类编号为0—79，stuff类编号为80—132。模型返回的查询区域经过像素竞争，随后将每个区域转换为其像素包围矩形。该协议保留了查询层面的stuff区域数量。",
        "",
        f"完整{candidates['images']}条记录包含{candidates['stuff_candidates']:,}个stuff候选；{candidates['images_with_repeated_stuff_class']}条记录含同一stuff类别的多个查询区域。相对于每张图像每个stuff类别只保留一个区域，共有{candidates['extra_regions_beyond_one_per_class']}个额外区域。这里的数量来自完整候选缓存，尚未经过每张图像最多8个stuff端点的选择。", "",
        "| stuff类别 | 超过每张图像每个类别一个区域的额外数量 |", "|---|---:|"]
    for item in candidates["extra_regions_by_class"]:
        lines.append(f"| {item['label']}（{item['category_id']}） | {item['extra']} |")
    lines.extend(["", "按stuff类别融合会改变区域的包围矩形、候选数量及后续端点选择，相关指标需要在明确的融合协议下重新计算。本次结果仅对应当前未融合协议，没有声称完成融合与未融合的关系指标对照。", "",
                  "## 本机融合实现的源码边界", "",
                  "处理器允许通过`label_ids_to_fuse`指定需要按类别融合的标签。对于当前133类配置，全部stuff标签集合为`set(range(80, 133))`。当前实验的有效集合为空，因此后面描述的融合分支没有参与现有结果。", "",
                  "本机`compute_segments`在每个有效查询后追加一项`segments_info`。指定融合且同一类别出现多次时，代码会再次使用同一个segment ID并继续追加记录，返回列表因而可能包含重复ID。当前区域提取器逐项遍历该列表，未来启用融合时需要保证每个最终区域只产生一个候选。", "",
                  "该函数还把`current_segment_id`同时用于编号递增和旧stuff编号读取：遇到已出现的stuff类别时，将其赋回旧编号；后续遇到新类别时在这个值上递增。如果这个旧编号小于此前已经分配的最大编号，后续新类别可能再次使用已分配ID。本审计只记录这条可复核的静态控制路径，没有运行融合分支，也没有测量它在当前500张图像上出现的频率。", "",
                  "## 源码、版本和复算", "",
                  "| 实际源码文件 | SHA256 |", "|---|---|"])
    for source in evidence["source_files"]:
        lines.append(f"| [{Path(source['path']).name}]({report_link(source['path'])}) | `{source['sha256']}` |")
    lines.extend(["", "JSON证据另保存相关forward函数、初始化函数和后处理函数的源码起始行及完整片段；安装目录中的文件可按上述签名核验。复算脚本为[audit_mask2former.py](../../scripts/audit_mask2former.py)，从仓库根目录执行：", "",
                  "```powershell", ".\\.venv-eval\\Scripts\\python.exe HOR\\research\\scripts\\audit_mask2former.py", "```", "",
                  "该脚本使用现有隔离环境、官方本地权重和完整候选缓存，在CPU完成参数比较，并重新生成本报告及JSON证据。区域实验结果见[Thing/Stuff端点实验报告](thing_stuff_region_study.md)。", ""])
    return "\n".join(lines)


def main():
    config_path = ROOT / "HOR/research/configs/region_study.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    model_dir = ROOT / config["detector"]["local_directory"]
    weight_path = model_dir / config["detector"]["weights_file"]
    require(digest(weight_path) == config["detector"]["weights_sha256"], "Checkpoint SHA256 differs from region configuration")
    model_config = json.loads((model_dir / "config.json").read_text(encoding="utf-8"))
    region_path = ROOT / "HOR/research/scripts/region_study.py"
    region_tree = ast.parse(region_path.read_text(encoding="utf-8"))
    postprocess_calls = [node for node in ast.walk(region_tree) if isinstance(node, ast.Call)
                         and isinstance(node.func, ast.Attribute)
                         and node.func.attr == "post_process_panoptic_segmentation"]
    require(len(postprocess_calls) == 1, "Expected exactly one panoptic postprocessing call")
    require("label_ids_to_fuse" not in {keyword.arg for keyword in postprocess_calls[0].keywords},
            "Region protocol changed; audit the new fusion policy explicitly")

    logging.disable_progress_bar()
    logging.set_verbosity_error()
    torch.set_default_device("cpu")
    model, loading_info = Mask2FormerForUniversalSegmentation.from_pretrained(
        model_dir, local_files_only=True, output_loading_info=True)
    model.eval()
    processor = AutoImageProcessor.from_pretrained(model_dir, local_files_only=True)
    parameters = dict(model.named_parameters())
    buffers = dict(model.named_buffers())
    norm = model.model.pixel_level_module.encoder.swin.layernorm
    devices = sorted({parameter.device.type for parameter in parameters.values()})
    require(devices == ["cpu"], "Audit must load all parameters on CPU")
    expected_missing = {"model.pixel_level_module.encoder.swin.layernorm.weight",
                        "model.pixel_level_module.encoder.swin.layernorm.bias"}
    require(set(loading_info["missing_keys"]) == expected_missing, "Unexpected missing checkpoint parameters")
    require(not loading_info["mismatched_keys"] and not loading_info["error_msgs"], "Checkpoint loading failed")
    require(norm.weight.detach().unique().tolist() == [1.0] and norm.bias.detach().unique().tolist() == [0.0],
            "Unexpected initialization of the final Swin LayerNorm")
    index_checks, bias_checks, stage_norm_checks = [], [], []
    with safe_open(weight_path, framework="pt", device="cpu") as checkpoint:
        keys = list(checkpoint.keys())
        index_keys = [key for key in keys if key.endswith("relative_position_index")]
        bias_keys = [key for key in keys if key.endswith("relative_position_bias_table")]
        stage_keys = [key for key in keys if ".hidden_states_norms." in key]
        require(len(index_keys) == len(bias_keys) == 12 and len(stage_keys) == 8,
                "Unexpected checkpoint index, bias table, or stage-normalization layout")
        for key in index_keys:
            new_key = new_backbone_key(key)
            original = checkpoint.get_tensor(key)
            rebuilt = buffers[new_key]
            equal = torch.equal(original.reshape(-1), rebuilt.reshape(-1))
            require(equal, f"Relative position index differs: {key}")
            index_checks.append({"checkpoint_key": key, "current_buffer_key": new_key,
                                 "checkpoint_shape": list(original.shape), "current_shape": list(rebuilt.shape),
                                 "equal_after_flatten": equal,
                                 "persistent_in_state_dict": new_key in model.state_dict()})
        for key in bias_keys + stage_keys:
            new_key = new_backbone_key(key)
            original = checkpoint.get_tensor(key)
            loaded = parameters[new_key]
            equal = torch.equal(original, loaded)
            require(equal, f"Learned checkpoint parameter differs: {key}")
            row = {"checkpoint_key": key, "current_parameter_key": new_key,
                   "shape": list(original.shape), "equal": equal}
            (bias_checks if key in bias_keys else stage_norm_checks).append(row)
    unexpected = sorted(loading_info["unexpected_keys"])
    require(len(unexpected) == 12 and all(key.endswith("relative_position_index") for key in unexpected),
            "Unexpected checkpoint keys extend beyond deterministic position-index buffers")

    functions = {
        "pixel_level_forward": modeling_mask2former.Mask2FormerPixelLevelModule.forward,
        "swin_model_forward": modeling_swin.SwinModel.forward,
        "swin_backbone_forward": modeling_swin.SwinBackbone.forward,
        "swin_relative_position_init": modeling_swin.SwinRelativePositionBias.__init__,
        "swin_relative_position_builder": modeling_swin.SwinRelativePositionBias._create_relative_position_index,
        "base_weight_initializer": transformers.modeling_utils.PreTrainedModel._init_weights,
        "panoptic_postprocess": type(processor).post_process_panoptic_segmentation,
        "compute_segments": image_processing_mask2former.compute_segments,
    }
    function_sources = {name: function_record(function) for name, function in functions.items()}
    backbone_source = function_sources["swin_backbone_forward"]["source"]
    require("outputs.reshaped_hidden_states" in backbone_source and "outputs.last_hidden_state" not in backbone_source,
            "SwinBackbone output path changed")
    require("self.hidden_states_norms[stage](hidden_state)" in backbone_source,
            "Per-stage feature normalization path changed")
    pixel_source = function_sources["pixel_level_forward"]["source"]
    require("self.encoder(pixel_values).feature_maps" in pixel_source, "Mask2Former feature consumer changed")
    compute_source = function_sources["compute_segments"]["source"]
    require("current_segment_id = stuff_memory_list[pred_class]" in compute_source
            and "current_segment_id += 1" in compute_source and "segments.append(" in compute_source,
            "Installed fusion control flow changed; revise the bounded source analysis")
    source_paths = {ROOT / record["path"] for record in function_sources.values()}
    package_root = Path(transformers.__file__).resolve().parent
    source_paths.update({package_root / "backbone_utils.py", package_root / "conversion_mapping.py", Path(__file__).resolve()})
    evidence = {
        "environment": {"transformers": transformers.__version__, "torch": torch.__version__,
                        "processor_class": type(processor).__name__, "processor_module": type(processor).__module__},
        "checkpoint": {"repository": config["detector"]["repository"], "revision": config["detector"]["revision"],
                       "weights": file_record(weight_path), "config": file_record(model_dir / "config.json"),
                       "preprocessor_config": file_record(model_dir / "preprocessor_config.json"),
                       "tensor_key_count": len(keys), "window_size": model_config["backbone_config"]["window_size"]},
        "actual_cpu_loading": {"parameter_device_types": devices,
                               "missing_keys": sorted(loading_info["missing_keys"]), "unexpected_keys": unexpected,
                               "mismatched_keys": sorted(loading_info["mismatched_keys"]),
                               "error_msgs": loading_info["error_msgs"],
                               "final_layernorm_weight_unique": norm.weight.detach().unique().tolist(),
                               "final_layernorm_bias_unique": norm.bias.detach().unique().tolist()},
        "checkpoint_checks": {"relative_position_indices": index_checks, "learned_relative_bias_tables": bias_checks,
                              "stage_output_normalizations": stage_norm_checks},
        "feature_path": {"pixel_decoder_uses_backbone_feature_maps": True,
                         "backbone_uses_reshaped_hidden_states_and_loaded_stage_norms": True,
                         "final_swin_layernorm_output_consumed_by_feature_maps": False},
        "postprocessing_protocol": {"label_ids_to_fuse_argument_provided": False, "effective_fusion_label_ids": [],
                                    "definition": "unfused query regions; multiple regions of one stuff class are retained",
                                    "configuration_source": file_record(config_path),
                                    "thing_class_ids": [0, 79], "stuff_class_ids": [80, 132],
                                    "thresholds": {name: config["detector"][name] for name in
                                                   ("score_threshold", "mask_threshold", "overlap_mask_area_threshold")},
                                    "region_call_source": file_record(region_path),
                                    "call_line": postprocess_calls[0].lineno},
        "fusion_source_analysis": {"scope": "static installed-source control flow; fusion branch was not executed",
                                   "repeated_segments_info_entries_possible": True,
                                   "segment_id_reuse_possible_after_revisited_stuff_then_new_class": True},
        "unfused_candidate_inventory": candidate_audit(ROOT / "HOR/research/output/regions/mask2former_candidates.jsonl",
                                                       model_config["id2label"], config["dataset"]["expected_images"]),
        "source_files": [file_record(path) for path in sorted(source_paths)], "function_sources": function_sources,
        "execution_scope": {"device": "cpu", "image_forward_passes": 0, "pixel_images_opened": 0,
                            "gpu_inference_passes": 0, "fusion_branch_executed": False},
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PATH.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(build_report(evidence), encoding="utf-8")
    print(json.dumps({"missing_parameter_count": len(loading_info["missing_keys"]),
                      "equal_relative_position_indices": len(index_checks),
                      "equal_learned_bias_tables": len(bias_checks), "equal_stage_norm_tensors": len(stage_norm_checks),
                      "unfused_stuff_candidates": evidence["unfused_candidate_inventory"]["stuff_candidates"],
                      "images_with_repeated_stuff_class": evidence["unfused_candidate_inventory"]["images_with_repeated_stuff_class"],
                      "extra_stuff_regions": evidence["unfused_candidate_inventory"]["extra_regions_beyond_one_per_class"],
                      "report": REPORT_PATH.relative_to(ROOT).as_posix(),
                      "evidence": EVIDENCE_PATH.relative_to(ROOT).as_posix()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
