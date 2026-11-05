# 三类 Agent 与 MCP 如何支持逐次人工确认

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: punkwen
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

## Answer

已按 [research 证据稿](https://github.com/punkwen/Structure-Agent-Hub/blob/d96123546fc5f77980eccd11e9e77f940e5bc916/.scratch/structure-agent-hub-spec/research/confirmation-capability.md) 取证（2026-11-06）。全部结论为第一方文档与固定版本源码层面，未安装客户端、未执行任何调用。

### 逐次批准与允许清单是不同机制，但只有一家能强制

- Claude Code 2.1.318 与 OpenCode v1 1.19.5 / v2 2.2.5 都有原生逐次调用批准（`ask` 规则），且与允许清单、会话级授权同属一套规则引擎的不同结果：Claude Code 求值顺序固定为 deny → ask → allow 且具体程度不改变顺序；OpenCode 为最后匹配生效。pi 1.5.0 **没有**内建权限系统，官方原文即「does not ask for approval before every tool call」，逐次确认只能由扩展的 `tool_call` 处理器实现。
- 唯一能抵抗权限模式与 allow 规则、做到「每次必答」的是 Claude Code 的私有元数据 `_meta["anthropic/requiresUserInteraction"]`（`acceptEdits`/`auto`/`bypassPermissions` 下仍提示、无 don't-ask-again、allow 规则不生效、`dontAsk` 直接拒绝、非交互 prompt tool 的 allow 被改写为 deny）。它不是 MCP 标准，其他客户端不认。
- OpenCode 的 `always` 会把 `ask` 降级：v1 到会话结束，v2 写**持久**项目 allow 规则。即一次点击即可把逐次确认变成长期放行，`deny` 除外。

### MCP elicitation 不是审批原语

- 规范把 elicitation 定义为服务器向用户**索取数据**：请求是 `message` + 扁平 `requestedSchema`，响应是 `accept`/`decline`/`cancel` 加用户填写内容。协议**没有**字段表达「批准对对象 X 执行操作 Y、参数 Z」，也没有身份或持久记录要求；目标/操作/参数只能塞进自由文本与字段描述。schema 明确不支持嵌套对象与对象数组。
- tools 规范里「人在环」只是 SHOULD，`annotations` 是提示且客户端 MUST 视为不可信。协议层不存在「调用前必须批准」的消息或状态机。
- 2026-07-28 用 MRTR 取代服务器主动请求（`InputRequiredResult` + 重发原请求 + `requestState`），把「这次输入属于哪次调用」结构化，但绑定仍由服务器维护，客户端没有可核验身份凭据。
- 客户端实际支持：Claude Code 自动弹窗并声明 `form`+`url`（v2.1.287+，部分连接仅 form），可用 `Elicitation`/`ElicitationResult` hook 代替或拦截；OpenCode v2 显示表单/链接，关闭即取消；**pi 1.5.0 不支持**——`@earendil-works/pi-mcp@1.5.0` 只注册 `ping` 与 `roots/list`，未声明 elicitation 能力，服务器发 `elicitation/create` 会收到 method-not-found。

### 关联性与可核性

- 客户端层：Claude Code 的 `PreToolUse` 带 `tool_use_id`、`tool_input`、`mcp_server{name,source}`，但**权限决策事件 `PermissionRequest` 不带 `tool_use_id`**，要关联需自行旁路；`updatedInput` 整体替换输入并重新过 deny/ask 规则。pi 的 `tool_call` 带 `toolCallId` 与可变 `input`。OpenCode 未提供等价 hook。
- 没有任何一家提供「确认回执 ↔ 实际执行调用」的协议级绑定，也没有第一方证据证明审批记录含操作者身份、可作审计台账。可用间接材料仅 transcript、`permission_denials` 输出、`/permissions` 规则来源、OpenCode v2 的持久模式规则。
- 票 01 要求的「目标、拟改内容（含原值与新值）、已知影响、分析设置」必须由 MCP 服务器自己组织并放进工具返回或 elicitation 字段，客户端不会替它生成。

### 客户端中介 vs 直连

- 直连服务器发 `tools/call` 绕过全部客户端机制（权限规则、提示、hook、`requiresUserInteraction`），协议不阻止。中介才获得权限门、参数展示、hook 拦截与强制每次必答。
- 中介本身会退化：Claude Code 在 `-p`/SDK/cloud 会话无法弹项目服务器审批而直接加载 `.mcp.json` 服务器；`--permission-prompts none` 会取消无人回答的 elicitation；pi 在 print/JSON 模式 `hasUI=false`，扩展必须自行 fail-closed。

### 明确未知

OpenCode v1 是否支持 elicitation（文档未提及）；OpenCode v2 的 elicitation 是否受 `ask` 约束或可被扩展拦截；Claude Code `PermissionRequest` 缺 `tool_use_id` 是否有其他官方关联手段；pi 扩展权限门在 RPC 模式下的行为；三家 Windows 对话框差异；以及全部三家的审批台账能力。以上均不得据推断宣称已具备。

### 后续验证所需条件

固定版本（Claude Code 2.1.318 / OpenCode v1 1.19.5 或 v2 2.2.5 / pi 1.5.0）装入一次性环境，配一个测试 MCP 服务器（同时具备声明 `requiresUserInteraction` 的工具、发 elicitation 的工具、记录收到的 `tools/call` 参数与 `_meta` 的工具），在 Manual/`ask` 下逐项观测：是否每次重问、提示展示的参数与实际执行是否一致、`always` 后是否不再询问、非交互是否 fail-closed、hook/扩展能否拿到可关联的调用 ID，并检查日志中是否存在可识别操作者的记录。

Research branch: research/hub-spec-confirmation-20261106
Commit: d96123546fc5f77980eccd11e9e77f940e5bc916
Date: 2026-11-06

