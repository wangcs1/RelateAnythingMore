import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt


HOR_DIR = Path(__file__).resolve().parent
REPORTS = HOR_DIR / "reports"
OUTPUT = HOR_DIR / "output"
EXPERIMENT = OUTPUT / "random500"
MARKER = "<!-- HOR_COMPLETE_RESULTS -->"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 ** 2), b""):
            result.update(block)
    return result.hexdigest()


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)] +
                     ["| " + " | ".join(str(value).replace("|", "/").replace("\n", " ")
                                         for value in row) + " |" for row in rows])


def percent(value):
    return "无分母" if value is None else f"{100 * value:.2f}%"


def copy_result(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def verify_links():
    parser = MarkdownIt("commonmark")
    references = 0
    documents = list(REPORTS.rglob("*.md"))
    for path in documents:
        pending = list(parser.parse(path.read_text(encoding="utf-8")))
        while pending:
            token = pending.pop()
            pending.extend(token.children or [])
            for attribute in ("href", "src"):
                reference = token.attrGet(attribute)
                if reference is None:
                    continue
                parsed = urlsplit(reference)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = (path.parent / unquote(parsed.path)).resolve()
                if not target.is_relative_to(REPORTS.resolve()):
                    raise ValueError(f"Report reference outside reports: {path}: {reference}")
                if not target.is_file():
                    raise FileNotFoundError(f"Broken report reference: {path}: {reference}")
                references += 1
    return {"markdown_documents": len(documents), "local_references_checked": references}


def verify_bundle():
    manifest = load(REPORTS / "evidence/report_inventory.json")
    for row in manifest["files"]:
        path = REPORTS / row["path"]
        if path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            raise ValueError(f"Published artifact mismatch: {path}")
    checked = verify_links()
    print(json.dumps({"passed": True, "files_hashed": len(manifest["files"]), **checked},
                     ensure_ascii=False, indent=2))


def write_inventory():
    files = [path for path in sorted(REPORTS.rglob("*")) if path.is_file() and path.name != "report_inventory.json"]
    save(REPORTS / "evidence/report_inventory.json", {
        "files": [{"path": path.relative_to(REPORTS).as_posix(), "bytes": path.stat().st_size,
                   "sha256": digest(path)} for path in files],
        "inventory_excludes_itself": True})


def export():
    verification = load(EXPERIMENT / "verification.json")
    if verification.get("passed") is not True or verification["images"] != 500:
        raise ValueError("A successful 500-image experiment verification is required")
    evaluations = load(EXPERIMENT / "evaluation.json")
    manifest = load(EXPERIMENT / "sample_manifest.json")
    records = [json.loads(line) for line in (EXPERIMENT / "predictions.jsonl").read_text(encoding="utf-8").splitlines()]
    if [record["index"] for record in records] != manifest["indices"] or len(records) != 500:
        raise ValueError("Sample and prediction records differ")
    modes = {"detected": "自动检测框完整枚举", "gt_boxes": "真实框完整枚举", "official400": "真实框400候选"}
    rankings = {"relations": "空间与语义各保留一个谓词", "single_predicate_top50": "每对只保留一个谓词"}
    details = {key: {row["index"]: row for row in value["per_image"]} for key, value in evaluations.items()}
    copied = []
    for filename in ("evaluation.json", "detection_summary.json", "runtime.json", "sample_manifest.json",
                     "verification.json", "report_example_selection.json"):
        copy_result(EXPERIMENT / filename, REPORTS / "evidence" / filename)
        copied.append(filename)
    copy_result(OUTPUT / "run.log", REPORTS / "evidence/run.log")
    for record in records:
        index = record["index"]
        for kind in ("detected", "gt"):
            name = f"{index:04d}_{kind}.jpg"
            copy_result(EXPERIMENT / "images" / name, REPORTS / "assets" / name)
        save(REPORTS / "evidence/cases" / f"{index:04d}.json", record)
        path = REPORTS / "cases" / f"{index:04d}.md"
        content = path.read_text(encoding="utf-8").partition(MARKER)[0]
        content = content.replace("../../output/random500/images/", "../assets/")
        content = content.replace("原始分数和全部人相关物体对的两类预测见 `output/random500/predictions.jsonl`；所有参与前向的物体对与56个谓词 logits 见 `output/random500/logits/`。",
                                  f"原始记录、全部人相关物体对的两项预测与分项分数见 [逐图证据 JSON](../evidence/cases/{index:04d}.json)。全部56类 logits 保留于本机 HOR/output/random500/logits/。")
        sections = [content.rstrip(), "", MARKER, "", "## 六组条件的完整输出对照", "",
                    "以下保留同一图片三种框与候选模式、两种谓词输出规则的全部 Top50。框编号各自在所属模式内解释。", ""]
        for mode, title in modes.items():
            prediction = record[mode]
            for ranking, label in rankings.items():
                sections += [f"### {title}：{label}", "",
                             table(["排名", "主语编号与类别", "谓词", "宾语编号与类别", "分组", "排序分数", "predicate logit", "pair logit"],
                                   [[number, f"#{row['subject_id']} {row['subject_label']}", row["predicate"],
                                     f"#{row['object_id']} {row['object_label']}", row["stream"],
                                     f"{row['score']:.7f}", f"{row['predicate_logit']:.7f}", f"{row['pair_logit']:.7f}"]
                                    for number, row in enumerate(prediction[ranking], 1)]), ""]
                diagnosis = details[f"{mode}/{ranking}"].get(index)
                if diagnosis:
                    sections += [f"GT 命中：{diagnosis['hits50']}/{diagnosis['gt_count']}，R@50={percent(diagnosis['R@50'])}。", "",
                                 table(["GT主语", "GT谓词", "GT宾语", "结果阶段", "匹配主语框", "匹配宾语框"],
                                       [[row["subject_id"], row["predicate"], row["object_id"], row["stage"],
                                         row["matching_subject_ids"], row["matching_object_ids"]] for row in diagnosis["diagnostics"]]), ""]
                else:
                    sections += ["没有人相关 GT，本条件的召回率无分母。", ""]
        path.write_text("\n".join(sections), encoding="utf-8")
    main_report = REPORTS / "HOR_500张实验报告.md"
    content = main_report.read_text(encoding="utf-8").partition(MARKER)[0]
    content = content.replace("../output/random500/images/", "assets/")
    content += "\n\n" + MARKER + "\n\n## 完整成果与核验附件\n\n"
    content += "[成果检查与交付说明](成果检查与交付说明.md)提供全部19组评测、500份逐图完整对照、单张图片实例和核验记录。报告配图位于 reports/assets，可随仓库直接查阅。\n"
    main_report.write_text(content, encoding="utf-8")
    single_source = OUTPUT / "single_example"
    single = load(single_source / "relations.json")
    for filename in ("relations.json", "objects.jpg", "result.md"):
        copy_result(single_source / filename, REPORTS / "single_example" / filename)
    rows = []
    for key, item in evaluations.items():
        rows.append([key, item["scored_images"], item["unique_gt"],
                     *[percent(item["metrics"][name]) for name in ("R@20", "R@50", "mR@50", "pooled_R@50")],
                     item["hits"].get("50", 0)])
    lines = ["# HOR 成果检查与交付说明", "", f"整理时间：{datetime.now().astimezone().isoformat()}。实验执行时间以原始 runtime.json 为准。", "",
             "## 可直接查阅的成果", "",
             "- [500张实验报告](HOR_500张实验报告.md)：实验设计、主要结果、检测覆盖、失败阶段、类别明细和案例。",
             "- [500张完整索引](500张图片索引.md)：全部图片的两组编号图、三种候选模式、两种输出规则、全部Top50及GT逐条核验。",
             "- [逐图CSV](逐图结果.csv)：逐图数量和召回率。",
             "- [单张新图片示例](single_example/result.md)：输入图片的编号框及50条输出；[完整JSON](single_example/relations.json)。",
             "- [随机抽样清单](evidence/sample_manifest.json)：随机种子、500张索引、文件名和运行配置。",
             "- [完整评测数据](evidence/evaluation.json)：19组条件或分组的全部数值、逐图诊断和类别结果。",
             "- [检测统计](evidence/detection_summary.json)、[实际运行环境与摘要](evidence/runtime.json)、[运行日志](evidence/run.log)。",
             "- [独立实验核验](evidence/verification.json)：6组指标独立复算、1000次人物对覆盖检查、550个完整logit文件检查。",
             "- [案例选择规则](evidence/report_example_selection.json)：主报告6个案例的确定性选择。", "",
             "500份逐图证据JSON位于 evidence/cases，保留原始预测记录，包括完整人物对、两类最佳谓词、全部对象编号、坐标、类别、GT、六组Top50和分项分数。每份逐图页面提供对应链接。", "",
             "## 全部评测条件与分组", "",
             table(["条件或分组", "有GT图片", "GT数量", "R@20", "R@50", "mR@50", "汇总R@50", "命中GT"], rows), "",
             "不同方向分组采用同一Top50并允许重叠。class_agnostic只检查框位置及谓词，其他检测条件要求物体类别一致。完整定义见主报告及脚本。", "",
             "## 核验范围", "",
             "本次整理不执行新的模型推理。已有结果重新通过 HOR/verify.py 核验；新增的整理脚本检查成果副本与原文件的对应关系、全部报告的本地链接、图片数量和逐图数量。", "",
             "模型、缓存、完整56类logit张量和批次预测JSONL保留在本机忽略目录 HOR/output 与 HOR/models。报告目录已包含可读成果、原始逐图记录、抽样清单和核验材料。HTML文件继续由根目录规则忽略。", "",
             "查看报告和图片无需GPU。重新计算原始logit一致性需要恢复本机模型及实验张量；报告文件摘要核验只需要 Python 和 markdown-it-py。", "",
             "```powershell", ".\\.venv-eval\\Scripts\\python.exe HOR/export_reports.py --verify-only", "```", "",
             "报告文件摘要见 [文件清单](evidence/report_inventory.json)。重新生成命令为 HOR/run.ps1 -SkipInference；完整推理为 HOR/run.ps1。", ""]
    (REPORTS / "成果检查与交付说明.md").write_text("\n".join(lines), encoding="utf-8")
    write_inventory()
    links = verify_links()
    pictures = list((REPORTS / "assets").glob("*.jpg"))
    cases = list((REPORTS / "cases").glob("*.md"))
    if len(pictures) != 1000 or len(cases) != 500:
        raise ValueError("The report must contain 1000 numbered images and 500 detailed cases")
    for record in records:
        index = record["index"]
        if load(REPORTS / "evidence/cases" / f"{index:04d}.json") != record:
            raise ValueError(f"Exported record differs: {index}")
    for filename in copied:
        if digest(EXPERIMENT / filename) != digest(REPORTS / "evidence" / filename):
            raise ValueError(f"Copied experiment evidence differs: {filename}")
    checked = {"passed": True, "checked_at": datetime.now(timezone.utc).isoformat(),
               "experiment_created": load(EXPERIMENT / "runtime.json")["created"],
               "numbered_images": len(pictures), "case_reports": len(cases),
               "raw_case_records": len(records), "evaluation_conditions_and_groups": len(evaluations),
               "complete_rankings_per_case": len(modes) * len(rankings),
               "single_example_relations": len(single["relations"]), **links,
               "exporter_sha256": digest(Path(__file__)), "GPU_inference_rerun": False}
    save(REPORTS / "evidence/delivery_verification.json", checked)
    write_inventory()
    verify_bundle()


def main():
    parser = argparse.ArgumentParser(description="Export and verify portable HOR reports")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        verify_bundle()
    else:
        export()


if __name__ == "__main__":
    main()
