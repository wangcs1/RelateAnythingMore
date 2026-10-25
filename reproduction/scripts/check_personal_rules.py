import ast
from collections import Counter
import io
import json
from pathlib import Path
import re
import subprocess
import tokenize


ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reproduction/reports"
AUDIT = ROOT / "reproduction/output/personal_rules"
SCRIPTS = ROOT / "reproduction/scripts"
PHRASES = ("而不是", "而非", "落地", "钉死", "技术栈", "模型栈", "两字版本", "单字版本")


def inspect_python(path):
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(path))
    findings = []

    def add(line, rule, detail):
        findings.append({"path": path.relative_to(ROOT).as_posix(), "line": line,
                         "rule": rule, "detail": detail})

    if ast.get_docstring(tree) is not None:
        add(tree.body[0].lineno, "module_docstring", "Python 文件顶部含 docstring")
    if source.startswith("#!"):
        add(1, "shebang", "Python 文件含 shebang")
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            imports = [child for statement in node.body for child in ast.walk(statement)
                       if isinstance(child, (ast.Import, ast.ImportFrom))]
            if imports:
                add(node.lineno, "try_import", "try-except 包含 import")
            else:
                add(node.lineno, "exception_review", "异常处理分支需要检查是否隐藏错误或替换执行方式")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "tempfile":
                add(node.lineno, "temporary_directory_review", "tempfile 默认路径需要检查，规范禁止读写 /tmp")
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if "/tmp" in node.value:
                add(node.lineno, "tmp_path_review", "字符串含 /tmp，需要检查实际读写目标")
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT and re.search(r"[A-Za-z]", token.string):
            if not re.search(r"[\u4e00-\u9fff]", token.string) and not token.string.startswith("#!"):
                add(token.start[0], "english_comment_review", token.string)
    return findings


def inspect_language(path):
    findings = []
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        matches = [phrase for phrase in PHRASES if phrase in line]
        if "不是" in line and "而是" in line:
            matches.append("不是…而是…")
        if matches:
            findings.append({"path": path.relative_to(ROOT).as_posix(), "line": number,
                             "rule": "language_review", "detail": "、".join(matches)})
    return findings


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    owned_python = sorted(SCRIPTS.glob("*.py"))
    official_names = subprocess.check_output(
        ["git", "-C", str(ROOT / "RelateAnything"), "ls-files"], text=True).splitlines()
    official_python = [ROOT / "RelateAnything" / name for name in official_names if name.endswith(".py")]
    snapshots = sorted((ROOT / "reproduction/output/execution/sources").rglob("*.py"))
    groups = {}
    for name, paths in (("current_scripts", owned_python), ("official_source", official_python),
                        ("execution_snapshots", snapshots)):
        findings = [finding for path in paths for finding in inspect_python(path)]
        groups[name] = {"files_checked": len(paths), "counts": dict(Counter(f["rule"] for f in findings)),
                        "findings": findings}
    documents = sorted((ROOT / "reproduction/reports").glob("*.md"))
    documents += sorted((ROOT / "reproduction/configs").glob("*.md"))
    documents += [ROOT / "reproduction/README.md", ROOT / "README.md"]
    documents = [path for path in documents if path.name != "个人规范检查报告.md"]
    language = [finding for path in documents + owned_python for finding in inspect_language(path)]
    groups["current_language"] = {"files_checked": len(documents) + len(owned_python),
                                  "counts": dict(Counter(f["rule"] for f in language)), "findings": language}
    definite = {"module_docstring", "shebang", "try_import"}
    violations = sum(f["rule"] in definite for group in groups.values() for f in group["findings"])
    result = {"date": "2026-10-25", "compliant": violations == 0 and not language,
              "confirmed_python_violations": violations, "groups": groups,
              "limitations": ["静态检查无法证明过去的 Git 操作、工具使用、测试真实性及全部动态分支符合规范",
                              "英文注释、措辞及异常处理标记需结合语境判断，计数不能直接视为独立违规数量",
                              "历史归档保留在本机；执行源码快照纳入本次检查"]}
    (AUDIT / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 个人规范检查报告", "", "检查日期：2026-10-25。依据：用户指定的 personal-coding-rules 技能。", "",
             "## 检查发现", "", "项目存在违反规范的内容。详细位置、行号和检查类别见 [完整检查结果](../output/personal_rules/results.json)。", ""]
    titles = {"current_scripts": "当前复现脚本", "official_source": "固定版本官方源码",
              "execution_snapshots": "历史执行源码快照", "current_language": "当前文档与脚本文字"}
    for name, group in groups.items():
        lines += ["### " + titles[name], "", f"检查文件数量：{group['files_checked']}。", ""]
        lines += [f"- `{rule}`：{count} 处。" for rule, count in group["counts"].items()]
        if not group["counts"]:
            lines.append("本次静态规则未发现对应问题。")
        lines.append("")
    lines += ["## 当前脚本的具体位置", ""]
    for finding in groups["current_scripts"]["findings"]:
        lines.append(f"- `{finding['path']}:{finding['line']}`：{finding['detail']}。")
    lines += ["", "## 判断范围", "",
              "文件顶部 docstring、shebang 和 try-except 导入具有明确的静态判定依据。英文注释包含术语、工具指令等情况，需人工结合语境判断。异常处理需要检查其实际错误处理方式；tempfile 的目标依赖操作系统与环境变量，静态出现不证明发生过 /tmp 读写。", "",
              "措辞检查涵盖当前报告、术语配置和报告生成脚本。用户提供的审查意见属于输入材料，其文字来源单独保留；完整结果提供文件名以便区分。", "",
              "本次执行规范检查并发布现有项目。已有实验源码、数值结果和历史执行快照保留；规范检查结果不代表全部文件已经整改。后续修改源码后，应重新运行对应验证并刷新证据清单。", "",
              "官方源码通过 Git 子模块固定版本，便于对应模型与实验记录。当前官方源码含规范所禁止的写法；其来源不会消除这些检查发现。", "",
              "静态检查无法判定过去是否使用过 Git 恢复代码、视觉工具、虚构测试结果或未获授权的操作。相关要求必须在每次实际执行中遵循。", "",
              "## 重复检查", "", "```powershell", "python reproduction/scripts/check_personal_rules.py", "```", "",
              "退出码为零表示检查完成。`results.json` 中的 `compliant` 表示本次规则检查的合规状态。", ""]
    (REPORTS / "个人规范检查报告.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"compliant": result["compliant"], "confirmed_python_violations": violations,
                      "groups": {name: group["counts"] for name, group in groups.items()}},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
