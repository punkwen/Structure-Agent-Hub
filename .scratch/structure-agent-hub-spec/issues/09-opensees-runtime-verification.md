# 核验选定 OpenSees 运行路径的版本兼容性

Type: task
Labels: wayfinder:task
Mode: AFK
Status: open
Assignee: unassigned
Blocked by: 05,07
Parent: ../map.md

## Question

本票是未来决策的前置核验，不是 MCP 实现任务。在 [哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md) 明确分发许可、[OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md) 明确首批任务与集成路径后，对所选精确发布物（可执行程序版本、wheel 或源码 tag）、操作系统/CPU 架构与解释器版本执行一次最小实际调用（加载或启动、一个最小模型或命令、一次输出读取），记录实际版本、输入、输出与错误证据，并裁定 [OpenSees 有哪些可用的集成路径与运行约束](04-opensees-integration-evidence.md) 所述版本/平台文档冲突对该目标环境是否成立。只核验该单一目标，不遍测未知平台、不改 MCP/Skill、不把失败当成功；下载/许可等前提缺失时明确记录并保持阻塞。结果作为 [一键部署应承诺什么行为与验收结果](08-deployment-contract.md) 可用性承诺的事实，不替人选择支持范围。
