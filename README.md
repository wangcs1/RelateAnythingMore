# RelateAnythingMore

RelateAnything 官方权重的 PSG 评测、控制实验、失败案例分析和中文实验报告。

阅读入口：

- [完整实验报告](reproduction/reports/完整实验报告.md)
- [附术语解释版](reproduction/reports/完整实验报告_附术语解释版.md)
- [汇报材料](reproduction/reports/PPT汇报材料_精华总结.md)
- [实验脚本与运行说明](reproduction/README.md)
- [个人规范检查报告](reproduction/reports/个人规范检查报告.md)
- [可视化入口](reproduction/reports/index.html)，下载仓库后使用浏览器打开。

## 获取代码

```powershell
git clone --recurse-submodules https://github.com/wangcs1/RelateAnythingMore.git
Set-Location RelateAnythingMore
```

官方源码以 `RelateAnything/` 子模块固定到 `06766fdf56752ca535fc9b971fca99ce563676d0`。来源与许可证见子模块中的说明和 LICENSE。本仓库保留实验时使用的官方源码版本。

## 核验已有结果

```powershell
python reproduction/scripts/check_personal_rules.py
python reproduction/scripts/verify_evidence.py
```

以上命令使用 Python 标准库。前者检查规范并输出具体发现；退出码为零表示检查完成，合规状态见输出中的 `compliant`。后者校验文件摘要、32个条件的指标、报告链接和执行记录。

Git 保留公开测试标注及转换后的测试数组，便于复算与核验。完整原图、模型权重、`.venv-eval`、历史归档和证据 ZIP 保留在本机，获取方式和文件摘要见 `reproduction/manifests/`。GPU 重跑需要恢复锁定的外部资源及依赖，详细步骤见实验脚本说明。

当前提交包含已有实验结果。本次规范检查执行代码静态分析、结果复算与文件核验；GPU 实验的实际执行日期、命令及源码快照见 `reproduction/output/execution/`。
