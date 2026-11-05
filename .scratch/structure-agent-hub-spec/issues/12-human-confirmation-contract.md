# 如何落实工程师逐次确认的保障与验收

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: open
Assignee: unassigned
Blocked by: 01,06,11
Parent: ../map.md

## Question

在 [三类 Agent 与 MCP 如何支持逐次人工确认](11-confirmation-capability-evidence.md) 的取证之后，与工程师共同确定逐次确认如何落实为可检查的保障与验收，包括：

- 是否需要技术性闸门（在执行前由机制拦截），还是以流程与文档约束为主；二者各自承担什么。
- 责任归属落在哪里：Skill、MCP、Agent 客户端配置或使用方约定。
- 确认与实际操作、参数、目标对象及版本修订之间如何对应；目标在确认后发生变化时如何处理。
- 能力限制、绕过客户端的直接调用、部分执行或失败时如何处置与报告。
- 这些保障如何被验收，以及由谁在什么条件下判定成立。

须保留 [首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md#answer) 已经要求的人工确认：每项独立模型改动、每次分析运行前均须工程师逐次明确确认，覆盖已有文件另行确认，YJK 一次完整预览后的创建可只确认一次；确认前须展示目标、拟改内容（必要时含原值与新值）、已知影响与分析设置，未知影响如实标注；工程有未保存内容时，须先由工程师选择「使用当前会话状态另存副本」或「使用已保存文件」，选择前不覆盖原文件。本票不预设技术设计，也不修改上述已定要求；如何与 [仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md) 的职责划分衔接，由用户判断。

参考票：[首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md)、[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md)、[三类 Agent 与 MCP 如何支持逐次人工确认](11-confirmation-capability-evidence.md)。
