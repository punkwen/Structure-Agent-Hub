# 核验选定 OpenSees 运行路径的版本兼容性

Type: task
Labels: wayfinder:task
Mode: AFK
Status: open
Assignee: unassigned
Blocked by: 05,07
Parent: ../map.md

## Question

本票是未来决策的前置核验，不是 MCP 实现任务。前置已满足：[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md) 明确运行时由用户自备、不再分发；[OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer) 选定 OpenSeesPy 路径（用户 Python 解释器 + `import openseespy.opensees`，输入为 Python 脚本，不包裹 `OpenSees.exe`）。

核验目标（单一目标环境：本机 Windows x64 + 已装 CPython 3.12.9）：

1. 记录实际解释器版本与路径；`openseespy` 的安装来源、版本与 `import openseespy.opensees` 是否成功，错误原样记录。
2. 跑一个最小模型（如悬臂或门式刚架）并读取一次输出，记录输入、输出与错误证据；对照 [OpenSees 有哪些可用的集成路径与运行约束](04-opensees-integration-evidence.md) 所述版本/Python 兼容性冲突，裁定其在该环境是否成立。
3. 核实 [OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer) 标为推断的运行时行为：`ops.analyze()` 失败时的返回与日志表现、OpenSees `Error`/`WARNING` 行能否从合并日志可靠识别、recorder 相对路径是否落在进程 CWD。

只核验该单一目标，不遍测未知平台、不改 MCP/Skill、不把失败当成功；下载/许可等前提缺失时明确记录并保持阻塞。结果作为 [一键部署应承诺什么行为与验收结果](08-deployment-contract.md) 可用性承诺与 07 验收参照的事实，不替人选择支持范围。
