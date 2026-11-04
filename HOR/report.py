import csv
import json
from pathlib import Path

from pipeline import HOR_DIR, CONFIG, save_json


OUTPUT = HOR_DIR / "output/random500"
REPORTS = HOR_DIR / "reports"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def percentage(value):
    return "无分母" if value is None else f"{value * 100:.2f}%"


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)] +
                     ["| " + " | ".join(str(value).replace("|", "/").replace("\n", " ") for value in row) + " |" for row in rows])


def relation_text(row, objects):
    names = {item["id"]: item["label"] for item in objects}
    return f"#{row['subject_id']} {names[row['subject_id']]} → {row['predicate']} → #{row['object_id']} {names[row['object_id']]}"


def main():
    REPORTS.mkdir(exist_ok=True)
    cases_dir = REPORTS / "cases"
    cases_dir.mkdir(exist_ok=True)
    records = [json.loads(line) for line in (OUTPUT / "predictions.jsonl").read_text(encoding="utf-8").splitlines()]
    evaluation = load(OUTPUT / "evaluation.json")
    detection = load(OUTPUT / "detection_summary.json")
    runtime = load(OUTPUT / "runtime.json")
    details = {mode: {row["index"]: row for row in evaluation[f"{mode}/relations"]["per_image"]}
               for mode in ("detected", "gt_boxes", "official400")}
    case_index = []
    csv_rows = []
    for record in records:
        index = record["index"]
        content = [f"# 图片 {index:04d}：{record['file_name']}", "",
                   f"随机样本序号：{record['sample_position']}。图片 SHA256：`{record['image_sha256']}`。", "",
                   "红色框表示人，蓝色框表示其他物体。两个模式分别保留自身框编号，可依据位置比较对应对象。", "",
                   "## 自动检测框与输出", "",
                   f"![自动检测编号框](../../output/random500/images/{index:04d}_detected.jpg)", "",
                   f"人的框编号：`{record['detected']['human_ids']}`。状态：`{record['detected']['status']}`。", ""]
        for mode, title in (("detected", "自动检测"), ("gt_boxes", "真实框")):
            result = record[mode]
            if mode == "gt_boxes":
                content += ["## 真实框与输出", "",
                            f"![真实编号框](../../output/random500/images/{index:04d}_gt.jpg)", "",
                            f"人的框编号：`{result['human_ids']}`。", ""]
            content += [f"### {title}全部物体框", "",
                        table(["编号", "类别", "是否为人", "检测分数", "像素坐标 xyxy"],
                              [[item["id"], item["label"], item["is_person"],
                                "GT" if item["detection_score"] is None else f"{item['detection_score']:.4f}",
                                ", ".join(f"{value:.1f}" for value in item["box_xyxy"])] for item in result["objects"]]), "",
                        f"### {title} Top50 人相关候选", "",
                        f"评分物体对：{result['candidate_pairs']}；人相关物体对：{result['human_pairs_scored']}；"
                        f"输出关系：{len(result['relations'])}。", "",
                        table(["排名", "主语编号与类别", "关系", "宾语编号与类别", "类型", "人与人", "排序分数", "原始融合 logit"],
                              [[row["rank"], f"#{row['subject_id']} {row['subject_label']}", row["predicate"],
                                f"#{row['object_id']} {row['object_label']}", row["stream"], row["human_human"],
                                f"{row['score']:.5f}", f"{row['fused_logit']:.4f}"] for row in result["relations"]]), ""]
            diagnosis = details[mode].get(index)
            content += [f"### {title}逐条人相关 GT 核验", ""]
            if diagnosis:
                content += [f"R@50：{percentage(diagnosis['R@50'])}；命中 {diagnosis['hits50']}/{diagnosis['gt_count']}。", "",
                            table(["GT 主语编号", "GT 关系", "GT 宾语编号", "结果阶段", "匹配预测主语编号", "匹配预测宾语编号"],
                                  [[row["subject_id"], row["predicate"], row["object_id"], row["stage"],
                                    row["matching_subject_ids"], row["matching_object_ids"]] for row in diagnosis["diagnostics"]]), ""]
            else:
                content += ["本图没有人相关 GT，R@50 无分母；预测候选继续展示。", ""]
        content += ["## 全部人相关 GT", "",
                    table(["主语编号与类别", "关系", "宾语编号与类别"],
                          [[f"#{row['subject_id']} {record['ground_truth_objects'][row['subject_id']]['label']}", row["predicate"],
                            f"#{row['object_id']} {record['ground_truth_objects'][row['object_id']]['label']}"] for row in record["ground_truth_relations"]]), "",
                    "原始分数和全部人相关物体对的两类预测见 `output/random500/predictions.jsonl`；"
                    "所有参与前向的物体对与56个谓词 logits 见 `output/random500/logits/`。", ""]
        (cases_dir / f"{index:04d}.md").write_text("\n".join(content), encoding="utf-8")
        row = {"index": index, "file_name": record["file_name"], "GT_people": len(record["gt_boxes"]["human_ids"]),
               "detected_people": len(record["detected"]["human_ids"]), "GT_relations": len(record["ground_truth_relations"]),
               "predicted_relations": len(record["detected"]["relations"]),
               "detected_R50": details["detected"].get(index, {}).get("R@50"),
               "GT_boxes_R50": details["gt_boxes"].get(index, {}).get("R@50")}
        csv_rows.append(row)
        case_index.append([record["sample_position"], f"[{index:04d}](cases/{index:04d}.md)",
                           record["file_name"], row["GT_people"], row["detected_people"], row["GT_relations"],
                           row["predicted_relations"], percentage(row["detected_R50"]), percentage(row["GT_boxes_R50"])])
    with (REPORTS / "逐图结果.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(csv_rows[0]))
        writer.writeheader()
        writer.writerows(csv_rows)
    (REPORTS / "500张图片索引.md").write_text("# 500张随机图片的完整结果\n\n" +
        table(["抽样序号", "图片详情", "文件名", "GT 人数", "检测人数", "人相关 GT", "预测候选", "自动检测 R50", "真实框 R50"], case_index) + "\n", encoding="utf-8")
    summary_rows = []
    for mode in ("detected", "gt_boxes", "official400"):
        for ranking in ("relations", "single_predicate_top50"):
            item = evaluation[f"{mode}/{ranking}"]
            summary_rows.append([mode, "空间/动作各一项" if ranking == "relations" else "每对一个谓词",
                                 item["scored_images"], item["unique_gt"],
                                 *[percentage(item["metrics"][key]) for key in ("R@20", "R@50", "mR@50", "pooled_R@50")],
                                 item["hits"]["50"]])
    lines = ["# HOR：人相关关系抽取与500张随机图片测试", "",
             "## 任务与输入输出", "",
             "输入一张图片，检测并编号其中的人和其他物体，使用已有 RelateAnything 官方权重预测有向关系，"
             "返回主语编号、主语类别、关系、宾语编号、宾语类别与分数。筛选条件为关系任一端是 person；人与人关系单独标记。", "",
             "采用 Faster R-CNN ResNet50 FPN V2 官方 COCO 检测权重，检测阈值0.35，单图最多40个检测框；"
             "关系输入分辨率448，CUDA BF16，关系词表沿用 PSG 的56个谓词。检测器以 CUDA FP32 执行。", "",
             "对保留的全部框枚举所有有向非自身物体对，然后筛选人相关关系。每对分别保留11个空间谓词中的最高分与45个其他谓词中的最高分，"
             "合并排序后最多输出50项。该分组沿用显式配置；动作组也包含 carrying、wearing 等语义关系，空间/动作标签仅用于组织输出。", "",
             "分数为 sigmoid(predicate_logit + pair_logit)，仅用于排序。本任务没有在 HOR 上校准概率或验证置信度阈值，"
             "默认保留候选以方便尽量发现关系。高分也可能有错误；数量达到50不代表存在50条真实交互。", "",
             "## 抽样与实验设计", "",
             f"随机种子 `{CONFIG['seed']}`，从本地公开 PSG test 的2179张图片中均匀无放回抽取500张。"
             "抽样使用标准库 random.Random(seed).sample；图片顺序、文件名和配置保存在 sample_manifest.json。"
             "抽样不读取关系真值，也不按人物数量或模型表现选择图片。", "",
             "三组实验使用完全相同的500张图：", "",
             "1. `detected`：只使用图片检测框与检测类别，完成可直接用于新图片的流程。", 
             "2. `gt_boxes`：使用 PSG 提供的真实框和类别识别人，完整枚举物体对，测量框已知条件下的关系能力。",
             "3. `official400`：使用同一真实框，恢复400候选预算，再筛选人相关关系，诊断有限候选预算的影响。", "",
             "所有模型前向均设置 targets=None。真实关系仅用于预测完成后的评测。人物类别用于识别哪些关系需要输出，"
             "关系模型本身只接收图像和框。枚举更多物体对会改变关系之间的注意力上下文，因此 HOR 的枚举模式具有自身的预测结果。", "",
             "## 测试集构成与检测结果", "",
             table(["项目", "数量或比例"], [
                 ["GT 人物框", detection["GT_people"]],
                 ["自动检测人物框", detection["detected_people"]],
                 ["IoU≥0.5且类别正确的人物框命中", detection["matched_GT_people_IoU05_class_aware"]],
                 ["人物框召回率", percentage(detection["person_box_recall"])],
                 ["GT 包含人物的图片", detection["GT_person_images"]],
                 ["自动检测包含人物的图片", detection["detected_person_images"]],
                 ["GT 有人的图片中检测到人的图片", detection["positive_images_with_person_detected"]],
                 ["GT 没有标注人物的图片", detection["GT_no_person_images"]],
                 ["GT 无人但检测到人的图片", detection["no_person_images_with_detection"]],
                 ["人相关GT涉及的去重端点", detection["human_GT_relation_unique_endpoints"]],
                 ["同类别且IoU≥0.5匹配的端点", detection["matched_endpoints"]],
                 ["关系端点召回率", percentage(detection["endpoint_recall"])],
                 ["位于检测器类别范围内的GT端点", detection["endpoints_in_detector_vocabulary"]],
                 ["类别范围内端点的匹配数量", detection["matched_endpoints_in_detector_vocabulary"]],
                 ["类别范围内端点的召回率", percentage(detection["covered_vocabulary_endpoint_recall"])]]), "",
             f"500张中有{detection['GT_person_images']}张标注人物，252张包含至少一条人相关关系标注。"
             "这两个数量采用不同计数条件；没有关系标注的图片继续处理与展示。", "",
             "GT 人数仅统计当前 PSG 转换版本保留的框。GT 无人的图片检测到人，需结合图像判断其正确性；未标注对象可能仍真实存在。", "",
             "检测器只覆盖 COCO 物体类别，PSG 中的道路、草地、天空、墙壁等区域可能缺少检测框。"
             "这类关系端点缺失会直接限制图片输入流程的召回率。", "",
             "## 完整关系召回结果", "",
             table(["框与候选模式", "输出规则", "有 GT 图片", "人相关 GT", "R@20", "R@50", "mR@50", "汇总 R@50", "命中 GT"], summary_rows), "",
             "R@K：每张有对应 GT 的图片中，前K条候选命中的去重人相关 GT 比例，再对图片取平均。"
             "mR@K：先计算每张图每类谓词的召回，再按谓词类别平均。汇总 R@K：全部命中数量除以全部去重 GT 数量。"
             "无对应 GT 的图片不进入这些分母，继续计入500张处理数量。", "",
             "自动检测匹配同时要求主语、宾语框各自 IoU≥0.5、类别一致且谓词一致，方向必须相同。"
             "真实框模式直接比较原始编号与谓词。框编号从0开始；同图检测模式和GT模式各自编号，禁止直接跨模式比较编号。", "",
             "本任务使用人相关候选自己的 Top50，且允许一对两个类型的谓词；指标名称在本报告中对应 HOR 协议。"
             "先前论文复现的全图单谓词 Top50 具有不同的输出范围。", "",
             "## 人与其他物体、人与人及关系方向", ""]
    group_rows = []
    for mode in ("detected", "gt_boxes"):
        for group in ("human_nonhuman", "human_human", "human_subject", "human_object"):
            value = evaluation[f"{mode}/{group}"]
            group_rows.append([mode, group, value["scored_images"], value["unique_gt"],
                               percentage(value["metrics"]["R@50"]), percentage(value["metrics"]["mR@50"])])
    lines += [table(["模式", "GT 分组", "有GT图片", "GT数量", "R@50", "mR@50"], group_rows), "",
              "方向分组可以重叠：人与人关系同时属于人作为主语和人作为宾语。分组评测沿用同一份人相关 Top50 输出。", "",
              "## 失败阶段", ""]
    stage_names = ("hit50", "endpoint_missing_or_wrong_class", "endpoints_collapsed_to_same_box", "pair_not_selected", "wrong_predicate", "rank_below50")
    lines += [table(["模式", *stage_names], [[mode, *[evaluation[f"{mode}/relations"]["failure_stages"].get(stage, 0)
                 for stage in stage_names]] for mode in ("detected", "gt_boxes", "official400")]), "",
              "endpoint_missing_or_wrong_class：GT端点没有同类别且 IoU≥0.5 的预测框。endpoints_collapsed_to_same_box：两个GT端点只能匹配同一个检测框，无法组成非自身物体对。pair_not_selected：存在两个不同的匹配端点，但该人相关物体对未进入候选。"
              "wrong_predicate：端点与候选存在，但对应类型的最佳谓词错误。rank_below50：该类型最佳谓词正确但未进入 Top50。", "",
              "## 谓词类别明细", ""]
    predicates = load(HOR_DIR.parent / "data/PSG/packed/psg/test/meta.json")["predicates"]
    perclass = []
    for predicate_id, item in evaluation["gt_boxes/relations"]["per_class"].items():
        detected_item = evaluation["detected/relations"]["per_class"][predicate_id]
        perclass.append([predicates[int(predicate_id)], item["gt"], detected_item["hits50"], item["hits50"],
                         percentage(detected_item["image_macro_R@50"]), percentage(item["image_macro_R@50"])])
    lines += [table(["谓词", "GT 数量", "自动检测命中", "真实框命中", "自动检测类别召回", "真实框类别召回"], perclass), "",
              "## 可查验案例", "",
              "[500张图片完整索引](500张图片索引.md)逐图提供两个模式的编号框、全部物体信息、全部 Top50 候选和逐条GT失败阶段。"
              "[逐图结果CSV](逐图结果.csv)可按人物数量、召回率或输出数量筛选。", ""]
    useful = [record for record in records if record["ground_truth_relations"]]
    successful = sorted(useful, key=lambda record: (-details["detected"][record["index"]]["R@50"], record["index"]))[:3]
    failed = sorted(useful, key=lambda record: (details["detected"][record["index"]]["R@50"],
                                               -details["gt_boxes"][record["index"]]["R@50"], record["index"]))[:3]
    selected = []
    for record in successful + failed:
        if record["index"] not in [item["index"] for item in selected]:
            selected.append(record)
    save_json(OUTPUT / "report_example_selection.json", {"policy": "three highest detected R50; three lowest detected R50 with highest GT-box R50 tie-break; index tie-break",
                                                        "indices": [item["index"] for item in selected]})
    for record in selected:
        index = record["index"]
        d, g = details["detected"][index], details["gt_boxes"][index]
        lines += [f"### 图片 {index:04d}：{record['file_name']}", "",
                  f"自动检测命中 {d['hits50']}/{d['gt_count']}，R@50={percentage(d['R@50'])}；"
                  f"真实框命中 {g['hits50']}/{g['gt_count']}，R@50={percentage(g['R@50'])}。", "",
                  f"![自动检测框](../output/random500/images/{index:04d}_detected.jpg)", "",
                  f"![真实框](../output/random500/images/{index:04d}_gt.jpg)", "",
                  "全部人相关 GT：", "",
                  table(["关系"], [[relation_text(row, record["ground_truth_objects"])] for row in record["ground_truth_relations"]]), "",
                  "自动检测前10条候选：", "",
                  table(["候选关系", "排序分数"], [[relation_text(row, record["detected"]["objects"]), f"{row['score']:.5f}"]
                        for row in record["detected"]["relations"][:10]]), "",
                  "真实框前10条候选：", "",
                  table(["候选关系", "排序分数"], [[relation_text(row, record["gt_boxes"]["objects"]), f"{row['score']:.5f}"]
                        for row in record["gt_boxes"]["relations"][:10]]), "",
                  f"详细错误阶段和全部输出：[图片 {index:04d}](cases/{index:04d}.md)。", ""]
    single_lengths = [len(record["detected"]["relations"]) for record in records]
    lines += ["## 当前流程的能力与限制", "",
              f"500张共输出 {sum(single_lengths)} 条自动检测候选，{sum(number == 50 for number in single_lengths)} 张达到50条上限。"
              f"无候选图片 {sum(number == 0 for number in single_lengths)} 张。完整人相关物体对的两类预测保存在 JSONL 中，可在本地查看 Top50 之外的候选。", "",
              "当前关系词表固定56类，可以覆盖拿着、骑着、穿着、看着、站在、坐在等关系。"
              "检测漏框、40框上限、固定词表、空间/动作各保留一个谓词和 Top50 上限都会限制完整性。"
              "同类型内同时发生的多个动作可能被最高分动作替代。", "",
              f"自动检测框的严格 R@50 为{percentage(evaluation['detected/relations']['metrics']['R@50'])}，"
              f"只检查框位置与谓词、忽略物体类别时为{percentage(evaluation['detected/class_agnostic']['metrics']['R@50'])}。"
              "严格指标中的检测类别错误会额外影响关系匹配。", "",
              "PSG 标注存在未标注关系，预测与GT不一致的候选需要人工核查。"
              "本次报告提供可重复的召回测试和原始证据；候选列表的真实正确率与所有实际交互的完整率仍需独立人工标注。", "",
              "PSG 图像来源与 COCO 检测预训练可能重叠，因此检测结果用于验证当前管线，不构成检测器在独立图像域的泛化评测。"
              "真实框模式提供额外标注信息，实际新图片使用自动检测模式。", "",
              "## 运行与资源记录", "",
              table(["项目", "实测"], [[key, value] for key, value in runtime.items() if key not in ("sources_sha256", "resources_sha256")]), "",
              "运行时间包含两组真实框前向、自动检测与关系前向、张量保存和1000张编号图保存；"
              "可直接用于新图的自动流程仅包含检测与关系两个步骤。模型初始化和权重摘要记录在 runtime.json。", "",
              "命令与执行日志见 `HOR/output/run.log`。脚本、配置、样本清单和原始输出均保留在 HOR。", ""]
    (REPORTS / "HOR_500张实验报告.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {len(records)} detailed cases and report: {REPORTS / 'HOR_500张实验报告.md'}")


if __name__ == "__main__":
    main()
