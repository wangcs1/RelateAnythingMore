import argparse
from pathlib import Path

from PIL import Image

from pipeline import HumanRelationPipeline, draw_objects, save_json, sha256


def main():
    parser = argparse.ArgumentParser(description="Extract human-related relations from one image")
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", default="HOR/output/single")
    args = parser.parse_args()
    image_path = Path(args.image).resolve()
    image = Image.open(image_path).convert("RGB")
    pipeline = HumanRelationPipeline()
    result, _ = pipeline.predict(image)
    result.update({"image": str(image_path), "image_sha256": sha256(image_path),
                   "image_size": list(image.size), "predicates": pipeline.predicates})
    destination = Path(args.output)
    save_json(destination / "relations.json", result)
    draw_objects(image, result["objects"], destination / "objects.jpg")
    lines = ["# 人相关关系抽取", "", f"图片：`{image_path.name}`。人的框编号：`{result['human_ids']}`。", "",
             "![编号框](objects.jpg)", "", "分数用于排序，Top50 候选需要结合原图判断。", "",
             "| 排名 | 主语编号与类别 | 关系 | 宾语编号与类别 | 分数 |", "|---|---|---|---|---|"]
    for row in result["relations"]:
        lines.append(f"| {row['rank']} | #{row['subject_id']} {row['subject_label']} | {row['predicate']} | "
                     f"#{row['object_id']} {row['object_label']} | {row['score']:.5f} |")
    (destination / "result.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"status={result['status']}; people={result['human_ids']}; relations={len(result['relations'])}; output={destination}")


if __name__ == "__main__":
    main()
