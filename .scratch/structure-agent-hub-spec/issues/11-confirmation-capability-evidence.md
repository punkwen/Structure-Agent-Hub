# 三类 Agent 与 MCP 如何支持逐次人工确认

Type: research
Labels: wayfinder:research
Mode: AFK
Status: open
Assignee: unassigned
Blocked by: 01,03
Parent: ../map.md

## Question

针对 [首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md#answer) 已要求逐次确认的操作，取证 Claude Code、pi（`earendil-works/pi`）与 OpenCode（按需区分 v1/v2），以及 MCP 自身相关能力，回答：工程师的确认能否、以及如何被绑定到一次具体的模型改动、一次分析运行或一次既有文件覆盖？

须以带版本锚点的第一方文档或源码为据，并区分：

- 原生逐次调用批准，与其他权限提示（如按类别/目录/命令前缀的允许清单、会话级授权）分别是什么，二者不可混同。
- MCP elicitation 等协议层机制实际能请求什么、返回什么，能否表达目标对象、操作与参数。
- 确认请求与实际执行的操作、参数之间如何关联；被确认对象的身份如何确定，人是谁、确认以何种形式记录是否可核。
- 由客户端中介的调用流程，与直接调用 MCP 服务器（绕过客户端审批）的流程，各自能获得什么保障。
- 版本、配置与作用域的适用条件与限制，以及哪些保障无法由第一方证据证明（不得据推断宣称已具备）。

参考票：[首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md)、[三类 Agent 实际支持哪些 Skill 与 MCP 接入方式](03-agent-integration-evidence.md)。本票不规定采用任何特定机制，也不声称任何能力已在运行时验证；不部署客户端、不执行任何调用。取证须如实报告证据缺口，并说明后续若要验证这些保障需要什么条件。
