# 三类 Agent 与 MCP 如何支持逐次人工确认：证据研究

> 交付物类型：**research 证据稿，不是 SPEC**。只回答问题、固定取证版本、列出事实与证据缺口；**不选择机制、不设计部署契约、不声称任何能力已在运行时验证**。
> 票：[三类 Agent 与 MCP 如何支持逐次人工确认](../issues/11-confirmation-capability-evidence.md)（Type: research，Assignee: punkwen）。
> 检索日期：**2026-11-06**。所有「当前」均指该日检索结果。

---

## 1. 问题与判定口径

票 01 要求：每项独立的模型改动、每次分析运行前，工程师逐次明确确认；确认前展示目标、拟改内容（必要时含原值与新值）、已知影响、分析设置；未知影响须标注为未知；覆盖已有文件须另行明确确认。

因此本稿把「确认能否绑定到一次具体操作」拆成四个可分别取证的问题：

1. **粒度**：客户端是否存在「每次调用都要人答一次」的原生机制，且它与「按类别/目录/命令前缀的允许清单」「会话级授权」是不同机制。
2. **表达力**：确认请求能否携带目标对象、操作与参数（结构化，而非仅自由文本）。
3. **关联性**：确认请求与被确认的那次调用/参数如何对应；被确认对象的身份如何确定。
4. **可核性**：人是谁、确认以何种形式记录，是否有第一方证据。

证据标签沿用票 03 的口径：`[已证实]`（固定 SHA 源码/机器可读元数据/文档与源码一致）、`[文档声明]`（第一方文档明文，未运行时验证）、`[推断]`、`[未知]`。

---

## 2. 结论摘要

- **原生逐次调用批准**：Claude Code 与 OpenCode（v1/v2）都有，且与允许清单/会话授权是**不同机制**；pi 1.5.0 **没有**内建权限系统，逐次确认只能由扩展实现。`[文档声明]`/`[已证实]`
- **强制每次必答**：只有 Claude Code 提供服务器可声明的「每次调用都必须人答」标记（`_meta["anthropic/requiresUserInteraction"]`），且它是 Anthropic 私有元数据，不是 MCP 标准；OpenCode 的 `ask` 可被「always」升级为持久允许规则；pi 无原生等价物。`[文档声明]`
- **MCP elicitation 不是审批原语**：它是「服务器向用户索取数据」的请求，返回 `accept/decline/cancel` 加用户填写内容；协议**没有**字段表达「批准对对象 X 执行操作 Y、参数 Z」，也没有身份或持久记录要求。目标/操作/参数只能由服务器塞进自由文本 `message` 与扁平 schema 的属性名/描述里。`[已证实]`（规范原文）
- **关联性**：协议层把 elicitation 嵌在服务器处理某次调用的上下文里（2025-11-25 及更早为服务器发起请求；2026-07-28 为 `InputRequiredResult` 重试），所以**服务器**知道自己在问哪次调用；但**客户端**没有标准字段把「这次确认」绑定到「即将发出的 `tools/call` 参数」，也没有标准回执。`[已证实]`+`[推断]`
- **可核性**：三家均无第一方证据证明「谁在何时批准了哪次具体调用」的持久审计记录；Claude Code 有 transcript 与 `permission_denials` 输出，但文档未声明其为带身份的审批台账。`[未知]`
- **客户端中介 vs 直连**：客户端中介才获得权限门、UI、hook 与 `requiresUserInteraction` 强制；直接对 MCP 服务器发 `tools/call` 绕过全部客户端机制，协议不阻止。`[已证实]`

---

## 3. 取证版本锚点

| 对象 | 锚点 | 来源 |
| --- | --- | --- |
| MCP 规范 | `2025-06-18`、`2025-11-25`、`2026-07-28` 三版 elicitation 与 tools 页 | [S1][S2][S3][S4][S5][S6] |
| Claude Code | npm `@anthropic-ai/claude-code` `latest` = **2.1.318**；文档站 `code.claude.com/docs`（在线更新，无版本锁） | [S7][S8] |
| OpenCode v1 | npm `opencode-ai` `latest` = **1.19.5**；`https://opencode.ai/docs/…` | [S9][S10][S11] |
| OpenCode v2 | npm `@opencode/cli` `latest` = **2.2.5**；`https://opencode.ai/v2/docs/…` | [S12][S13][S14] |
| pi | 仓 `earendil-works/pi` `main` = `55a5c6914570e2ae31ca36297654483bbbf46883`；`@earendil-works/pi-coding-agent` **1.5.0**；`@earendil-works/pi-mcp` **1.5.0** | [S15][S16][S17][S18] |

Claude Code 公开仓不含顶层 `src/`，其运行时行为只能按官方文档记为 `[文档声明]`（同票 03 的结论）。OpenCode v2 文档与 npm 版本的对应关系官方未给出映射，仍按 `[推断]` 处理。

---

## 4. MCP 协议层：能请求什么、返回什么

### 4.1 elicitation 是「索取数据」，不是「请求批准」

`[已证实]` 规范原文把 elicitation 定义为「servers request additional information from users through the client」，请求体是 `message`（人类可读说明）+ `requestedSchema`（JSON Schema），响应是 `{action: "accept"|"decline"|"cancel", content?}`。[S1][S2]

- **没有**「批准/拒绝某个操作」的语义字段：`accept` 只表示「用户提交了这些字段值」，`decline` 表示「用户明确拒绝提供」，`cancel` 表示「用户未作选择就关闭」。服务器要把它当批准用，必须自己解释 `accept` 的含义。`[已证实]`
- **没有**目标对象/操作/参数的协议字段。能表达的全部是 `message` 自由文本，加上扁平 schema 的属性名、`title`、`description`。`[已证实]`
- schema 被刻意限制为**扁平对象 + 原始类型**：string/number/boolean/enum；2025-11-25 起增加 `pattern`、`default`、`oneOf`/`anyOf` 枚举与多选数组；嵌套对象、对象数组、其他高级 JSON Schema 特性**明确不支持**。[S1][S2]
- 客户端**必须**在初始化时声明 `elicitation` 能力；2025-11-25 起分 `form`/`url` 两种模式，空对象等价于仅 `form`；服务器**不得**发送客户端未声明的模式。[S2]
- 规范明确「实现可以按任何界面形式暴露 elicitation，协议本身不规定交互模型」——即**是否弹窗、弹什么、是否可批量批准，全由客户端决定**。[S1][S2]

### 4.2 2026-07-28 的破坏性变化

`[已证实]` 2026-07-28 版用 **Multi Round-Trip Requests (MRTR)** 取代服务器主动请求：服务器**必须**通过 `InputRequiredResult` 返回 `elicitation/create` 等请求，客户端收集输入后**重发原请求**并附带结果；旧的服务器主动请求模式不再支持。[S3][S4]

- 客户端能力从初始化握手移到每个请求的 `_meta.io.modelcontextprotocol/clientCapabilities`。[S3]
- 该版新增服务器义务：「Servers **MUST** bind elicitation requests to the client and user identity」，并要求 URL 模式不得把凭据回传给客户端。[S3]
- 对确认绑定的意义：MRTR 让「这次输入属于哪次调用」在**协议层**有了结构（重发同一请求 + `requestState`），比 2025-11-25 的「服务器在调用处理中顺手发请求」更强；但绑定仍由**服务器**维护，客户端没有可核验的身份凭据。`[已证实]`+`[推断]`

### 4.3 tools 层：人在环只是 SHOULD

`[已证实]` tools 规范写明工具是 **model-controlled**，并给出安全建议：「there **SHOULD** always be a human in the loop with the ability to deny tool invocations」，应用 **SHOULD** 提供确认提示、明确展示暴露了哪些工具。[S5][S6]

- 这是**建议**，不是协议强制；协议没有「调用前必须获得批准」的消息或状态机。`[已证实]`
- `annotations`（`readOnlyHint`、`destructiveHint`、`idempotentHint`、`openWorldHint`）是**提示**，且规范要求客户端「**MUST** consider tool annotations to be untrusted unless they come from trusted servers」。[S5]
- 因此「这个工具必须每次人工确认」在 MCP 标准里**没有**表达方式；Claude Code 的 `requiresUserInteraction` 是厂商私有 `_meta` 扩展（见 §5.3）。`[已证实]`

---

## 5. Claude Code（2.1.318）

### 5.1 原生逐次调用批准，与允许清单/会话授权是不同机制

`[文档声明]` 权限系统分层：Manual（配置值 `default`）模式「Prompts for permission on first use of each tool」；提示里可给「Yes, and don't ask again」，对 Bash/WebFetch 会**永久**写入 `.claude/settings.local.json`（按仓库），对文件修改则**仅到会话结束**。[S19]

- 规则求值顺序固定为 **deny → ask → allow**，首个匹配决定结果，**具体程度不改变顺序**；allow 规则无法从 deny 规则里挖例外。[S19]
- 因此「逐次批准」与「允许清单」是同一套规则引擎的两种结果：`ask` 规则强制每次询问，`allow` 规则跳过询问，`deny` 直接阻断。会话级授权（"for the rest of the session"）是提示里的另一个选项，与保存规则不同。[S19]
- 权限模式会整体改变基线：`acceptEdits` 自动接受工作目录内编辑与常见文件系统命令；`auto` 由分类器代替人审；`dontAsk` 把「本会询问」的调用**直接拒绝**；`bypassPermissions` 跳过提示。[S19][S20]

### 5.2 MCP 工具如何进入这套机制

`[文档声明]` MCP 工具以 `mcp__<server>__<tool>` 命名参与同一套规则；allow 规则的通配只允许出现在字面 `mcp__<server>__` 前缀之后，deny/ask 规则可用 `mcp__*` 等工具名通配。[S19]

- 参数级匹配（`Tool(param:value)`）**不适用于 MCP 工具**：加载设置时会跳过带括号的 `mcp__` 规则，并在启动时报告为无效设置。[S19]
- 即：Claude Code 的规则粒度是**工具名**，不是「这次调用的参数」。参数只出现在提示界面与 hook 输入里。`[文档声明]`

### 5.3 唯一「每次必答」的机制是厂商私有元数据

`[文档声明]` 服务器可在 `tools/list` 条目里设 `_meta["anthropic/requiresUserInteraction"] = true`（必须是 JSON 布尔 `true`），效果：[S21]

- 每次调用都显示权限提示，**即使**在 `acceptEdits`、`auto`、`bypassPermissions` 模式；
- 不提供「don't ask again」；匹配的 allow 规则**也不能**跳过；
- `dontAsk` 模式下直接拒绝；
- 非交互 + `--permission-prompt-tool` 时，prompt tool 返回的 `allow` 会被改写成 deny（`MCP tool requires user interaction; not supported via --permission-prompt-tool`）；
- Agent SDK 的 `canUseTool` 回调**能**收到并批准（因为 SDK 应用被期望展示给用户）；
- hook 返回 `"allow"` 时仍然提示（v2.1.292+）。

这是**Anthropic 私有**字段，不是 MCP 标准；其他客户端不认它。`[已证实]`（文档明示为 `anthropic/` 命名空间）

### 5.4 确认请求与执行参数的关联

`[文档声明]` 两个 hook 事件提供不同信息：[S22]

| 事件 | 触发时机 | 携带 | 能否决定 |
| --- | --- | --- | --- |
| `PreToolUse` | 每次工具调用前（无论是否需要权限） | `tool_name`、`tool_input`、`tool_use_id`、MCP 时另有 `mcp_server{name, source}`（v2.1.274+） | allow/deny/ask/defer，可 `updatedInput` |
| `PermissionRequest` | 即将向人询问时（或本会因无人可问而自动拒绝时） | `tool_name`、`tool_input`、`mcp_server`、`permission_suggestions`；**没有 `tool_use_id`** | `decision.behavior` allow/deny、`updatedInput`、`updatedPermissions`、`message`、`interrupt` |

- `updatedInput` 会**整体替换**输入对象，且替换后**重新**过 deny/ask 规则；hook 返回 `allow` 不能覆盖匹配的 deny 规则。[S22]
- 关键缺口：**权限决策事件本身不带 `tool_use_id`**，只有 `PreToolUse` 带。要把「人批准的那次」与「实际执行的那次」对上，需要自己用 `PreToolUse` 的 `tool_use_id` 做旁路关联。`[文档声明]`+`[推断]`

### 5.5 elicitation 在 Claude Code 里的实际形态

`[文档声明]` 服务器发起的 elicitation 会**自动**弹出终端对话框，无需配置；form 模式显示服务器定义的字段，URL 模式询问是否打开链接。[S21]

- 声明的能力：2026-07-28 连接、以及 2025-11-25 及更早版本上用户配置的 stdio/sse/http/ws 服务器，声明 `elicitation: {form:{}, url:{}}`（需 v2.1.287+）；其他连接（如 claude.ai connectors）只声明裸 `{}`，即仅 form 模式。[S21]
- `Elicitation` hook 可**代替人**回答（`accept`+`content` / `decline` / `cancel`），此时不弹窗；`ElicitationResult` hook 在用户回答后、回传服务器前可观察/修改/阻断。[S22]
- 非交互场景：`--permission-prompts none` 时，无人回答的 elicitation 会被**取消**；非交互会话中，请求输入的任务会被要求取消。[S21][S23]
- 注意：elicitation 的 `accept` 与「批准执行某操作」在协议上无关（§4.1）；Claude Code 文档也没有把它描述为审批机制。`[已证实]`

### 5.6 可核性

`[文档声明]` 存在 transcript（含 `tool_use_id`）、`--output-format stream-json` 的 `permission_denied` 系统消息与最终 `permission_denials` 列表、`/permissions` 对话框（列出规则及其来源文件）。[S19][S23]

`[未知]` 未找到第一方声明：审批记录包含**操作者身份**、可作为审计台账、或能证明「某次具体调用由某人批准」。提示上的 Tab 注释是发给模型的说明，不是记录。[S19]

---

## 6. OpenCode（v1 1.19.5 / v2 2.2.5）

### 6.1 v1：`permission` 对象 + once/always/reject

`[文档声明]` `permission` 配置按工具名给 `allow`/`ask`/`deny`，支持对象语法按输入模式细分（`bash` 按命令、`edit` 按路径），**最后匹配的规则生效**；`--auto` 自动批准所有非 deny 请求。[S10]

- 询问时三个结果：`once`（仅本次）、`always`（**本会话内**批准匹配的建议模式）、`reject`。[S10]
- 默认宽松：多数权限 `allow`，`doom_loop` 与 `external_directory` 为 `ask`。[S10]
- MCP 工具用 `<server>_<tool>` 形式的通配控制，例如 `"mymcp_*": "ask"`。[S11]
- `[未知]` v1 的 MCP 文档与 config 文档中**未出现** elicitation 相关说明；不能据此断言 v1 不支持，只能记为未取证。

### 6.2 v2：有序规则数组 + 持久化批准

`[文档声明]` v2 改为 `permissions` 有序数组，每条 `{action, resource, effect}`，**最后匹配生效**，无匹配则 `ask`；MCP 工具的动作名是 `<server>_<tool>`，Code Mode 另有 `execute`。[S13]

- 批准三选一：`once`、`always`（**保存为项目级持久 allow 规则**，由工具提出模式）、`reject`（拒绝该会话内**所有**待决请求）。保存的规则**永不覆盖**配置的 `deny`。[S13]
- 与 v1 的关键差异：v1 的 `always` 只到会话结束，v2 的 `always` 是**持久**的。这直接影响「逐次确认」能否被一次点击降级为长期放行。`[文档声明]`
- 非交互客户端必须自行决定如何处理批准请求；配置的 `deny` 始终生效。[S13]
- v2 的 MCP 文档明确支持 elicitation：「Servers can ask for input during a call through MCP elicitation. OpenCode shows the request as a form, or as a link to open for URL requests」，关闭表单即取消。[S14]
- `[未知]` v2 文档未说明 elicitation 与权限规则的关系（是否受 `ask` 约束、能否被 hook 拦截），也未提供等价于 Claude Code `Elicitation` hook 的扩展点。

### 6.3 关联性与可核性

`[文档声明]` v2 在 `tools/call` 的 `_meta["ai.opencode/sessionID"]` 里带会话 ID，便于服务器侧关联会话。[S14]

`[未知]` 未找到第一方证据说明：批准记录是否持久、是否含操作者身份、是否能与具体调用参数对应。v2 的持久批准保存的是**模式**（如 `shell: git status *`），不是某次调用的参数快照。`[文档声明]`+`[推断]`

---

## 7. pi（1.5.0）

### 7.1 没有内建权限系统

`[已证实]` 官方安全文档原文：「Pi can read, change, and execute files with the permissions of the account that started it, and **it does not ask for approval before every tool call**」；project trust 只控制启动时加载哪些项目资源，「does not limit what tool calls can access or affect」。[S24]

- 官方给出的安全边界是**操作系统/容器隔离**，不是审批。[S24]
- 因此 pi 上不存在「原生逐次调用批准」；票 01 要求的逐次确认在 pi 上**只能由扩展实现**。`[已证实]`

### 7.2 扩展能实现什么

`[文档声明]` 扩展可订阅 `tool_call` 事件（工具执行前，可阻断），`event.input` 可变且修改会作用于实际执行；返回 `{block: true, reason}` 阻断；`ctx.ui.confirm()` 弹确认框；官方把「Permission gates (confirm before `rm -rf`, `sudo`, etc.)」列为示例用途。[S25]

- `ctx.hasUI` 在 print（`-p`）与 JSON 模式下为 `false`，此时对话框方法不可用——扩展必须自行决定无 UI 时是拒绝还是放行。[S25]
- MCP 调用**经过**同一条工具管线，所以扩展的 `tool_call`/`tool_result` 处理器（含权限门）对 MCP 工具生效；codemode 发起的调用带 `parentToolCallId`。[S26]
- `pi.getAllTools()` 暴露服务器声明的 `readOnlyHint`/`destructiveHint`/`idempotentHint`/`openWorldHint`，文档明说「Permission extensions can use these hints to decide which calls require confirmation」。[S26]

### 7.3 pi 不支持 MCP elicitation

`[已证实]` 发布包 `@earendil-works/pi-mcp@1.5.0` 的 `McpClient` 只注册 `ping` 与 `roots/list` 两个服务器→客户端请求处理器；未注册的方法一律回 JSON-RPC `methodNotFound`。`ClientCapabilities` 类型里虽有 `elicitation?` 字段，但 pi 的 MCP 运行时构造客户端时只传 `name`/`version`/`requestTimeoutMs`/`roots`，**不声明** elicitation 能力。[S17][S18][S27]

- 结论：服务器若向 pi 发 `elicitation/create`，会收到 method-not-found；pi 侧没有可用的协议层确认通道。`[已证实]`（基于 1.5.0 发布包 dist 代码）
- 与票 03 的结论一致：pi 的 MCP 协议面为 `2025-11-25`，sampling/tasks 等不在核心内。[S18]

### 7.4 关联性与可核性

`[文档声明]` `tool_call` 事件带 `toolName`、`toolCallId`、`input`，因此扩展可以把「确认」与「具体调用 ID + 参数」绑定，并在阻断时给出理由。[S25]

`[未知]` 该绑定完全由扩展作者实现；pi 不提供审批记录、身份或审计。`[已证实]`（无内建权限系统即无内建记录）

---

## 8. 横向对比：四个问题分别的答案

### 8.1 粒度

| 客户端 | 原生逐次批准 | 与允许清单/会话授权的关系 | 能否强制「每次必答」 |
| --- | --- | --- | --- |
| Claude Code | 有（Manual 模式首次使用每工具询问；`ask` 规则每次询问） | 同一规则引擎的三种结果；"don't ask again" 可永久或会话级放行 | 能，但仅通过私有 `_meta["anthropic/requiresUserInteraction"]` |
| OpenCode v1 | 有（`ask`） | 同一 `permission` 配置；`always` 到会话结束 | 不能：`always` 可把 `ask` 降级为会话内放行 |
| OpenCode v2 | 有（`ask`） | 同一 `permissions` 数组；`always` 写**持久**项目规则 | 不能：`always` 可持久降级；`deny` 不可被覆盖 |
| pi 1.5.0 | **无** | 无内建权限系统 | 只能由扩展实现，且无 UI 模式需自行 fail-closed |

### 8.2 表达力

- 协议层（elicitation）：只能表达「请提供这些扁平字段」，目标/操作/参数只能塞进 `message` 与字段描述。`[已证实]`
- 客户端层（权限提示）：Claude Code 的提示展示 `tool_input`（hook 输入里可见完整参数），OpenCode 的提示展示工具与建议模式；两者都不是结构化「操作 + 参数 + 影响」对象。`[文档声明]`
- 因此票 01 要求的「展示目标、拟改内容（含原值与新值）、已知影响、分析设置」**必须由 MCP 服务器自己组织**（例如把预览放进工具返回或 elicitation 的 `message`/字段），客户端不会替它生成。`[推断]`

### 8.3 关联性

- 协议层：2025-11-25 及更早，elicitation 嵌在服务器处理某次调用的过程中，**服务器**知道对应关系，客户端没有标准字段；2026-07-28 的 MRTR 用「重发原请求 + `requestState`」把关系结构化，但仍是服务器侧状态。`[已证实]`
- 客户端层：Claude Code 的 `PreToolUse` 带 `tool_use_id`，`PermissionRequest` **不带**；OpenCode 未提供等价 hook；pi 的 `tool_call` 带 `toolCallId`。`[文档声明]`
- 结论：**没有任何一家**提供「确认回执 ↔ 实际执行调用」的协议级绑定；能做到的是客户端内部 UI 与 hook 层面的关联。`[已证实]`+`[推断]`

### 8.4 可核性（人是谁、记录在哪）

- 三家均**未**提供第一方证据证明：审批记录含操作者身份、可导出为审计台账、或能证明某次调用由某人批准。`[未知]`
- 可用的间接材料：Claude Code 的 transcript 与 `permission_denials` 输出、`/permissions` 规则来源；OpenCode v2 的持久 allow 规则（记录的是模式，不是单次批准）；pi 无内建记录。`[文档声明]`

### 8.5 客户端中介 vs 直连

- 直连 MCP 服务器发 `tools/call` **绕过**全部客户端机制：权限规则、提示、hook、`requiresUserInteraction` 都不参与。协议不阻止，也没有「必须经客户端」的约束。`[已证实]`
- 客户端中介才获得：权限门、UI 展示参数、hook 拦截/改写、`requiresUserInteraction` 强制、以及（Claude Code）非交互时的 fail-closed 行为。`[文档声明]`
- 反向风险：Claude Code 在 `-p`/SDK/cloud 会话中**无法**弹出项目服务器审批，会直接加载 `.mcp.json` 服务器；`--permission-prompts none` 会取消无人回答的 elicitation。即「中介」本身在非交互场景下会退化。`[文档声明]`

---

## 9. 对后续决策的约束与证据缺口

### 9.1 事实约束

- **C1** 逐次确认在 Claude Code 与 OpenCode 上是**配置结果**（`ask` 规则），不是不可绕过的属性；只有 Claude Code 的私有 `requiresUserInteraction` 能抵抗模式与 allow 规则。`[文档声明]`
- **C2** OpenCode v2 的 `always` 会写**持久**项目规则，一次点击即可把逐次确认降级为长期放行；v1 只到会话结束。`[文档声明]`
- **C3** pi 没有内建权限系统，逐次确认必须由扩展实现，且 print/JSON 模式无 UI。`[已证实]`
- **C4** MCP elicitation 不能表达「批准操作 X、参数 Y」；它只能索取数据。把它当审批用，语义由服务器自行定义，客户端不保证任何审批含义。`[已证实]`
- **C5** 没有任何一家的第一方证据支持「确认记录含身份、可审计」。`[未知]`
- **C6** 直连服务器绕过全部客户端保障；「必须经客户端」不是协议约束。`[已证实]`
- **C7** 票 01 要求的展示内容（原值/新值/影响/分析设置）必须由 MCP 服务器组织，客户端只负责展示 `tool_input` 或 elicitation 字段。`[推断]`

### 9.2 明确未知（不得据推断宣称已具备）

1. 三家均无「审批台账」的第一方证据（身份、时间、被批准的具体参数）。
2. OpenCode v1 是否支持 elicitation：文档未提及，未取证。
3. OpenCode v2 的 elicitation 是否受 `ask` 规则约束、能否被扩展拦截：文档未说明。
4. Claude Code 的 `PermissionRequest` 为何不带 `tool_use_id`、是否有其他官方关联手段：文档未说明。
5. pi 扩展实现的权限门在 RPC 模式下的行为：`hasUI` 为 `true`，但对话框经 JSON 协议，未验证。
6. 三家在 Windows 上的对话框/终端行为差异：未验证。
7. 全部结论均为文档与固定版本源码层面，**未安装客户端、未执行任何调用**。

### 9.3 若要验证这些保障，需要什么

- 固定版本（Claude Code 2.1.318 / OpenCode v1 1.19.5 或 v2 2.2.5 / pi 1.5.0）装入一次性环境；
- 一个测试 MCP 服务器，同时具备：声明 `requiresUserInteraction` 的工具、发送 elicitation 的工具、记录收到的 `tools/call` 参数与 `_meta` 的工具；
- 在 Manual/`ask` 下逐项观测：是否每次重问、提示中展示的参数是否与实际执行一致、`always` 后是否不再询问、非交互模式下是否 fail-closed、hook/扩展能否拿到可关联的调用 ID；
- 检查 transcript / 日志中是否存在可识别操作者的记录。

---

## 10. 第一方引用

**MCP 规范**
- [S1] https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation
- [S2] https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation
- [S3] https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- [S4] https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr
- [S5] https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- [S6] https://modelcontextprotocol.io/specification/2026-07-28/server/tools

**Claude Code**
- [S7] https://registry.npmjs.org/@anthropic-ai%2Fclaude-code/latest
- [S8] https://code.claude.com/docs/en/overview
- [S19] https://code.claude.com/docs/en/permissions
- [S20] https://code.claude.com/docs/en/permission-modes
- [S21] https://code.claude.com/docs/en/mcp
- [S22] https://code.claude.com/docs/en/hooks
- [S23] https://code.claude.com/docs/en/headless

**OpenCode**
- [S9] https://registry.npmjs.org/opencode-ai/latest
- [S10] https://opencode.ai/docs/permissions/
- [S11] https://opencode.ai/docs/tools
- [S12] https://registry.npmjs.org/@opencode%2Fcli/latest
- [S13] https://opencode.ai/v2/docs/permissions/
- [S14] https://opencode.ai/v2/docs/mcp-servers/

**pi**
- [S15] https://api.github.com/repos/earendil-works/pi/branches/main
- [S16] https://registry.npmjs.org/@earendil-works%2Fpi-coding-agent/latest
- [S17] https://registry.npmjs.org/@earendil-works%2Fpi-mcp/1.5.0
- [S18] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/mcp/README.md
- [S24] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/security.md
- [S25] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/extensions.md
- [S26] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/mcp.md
- [S27] `@earendil-works/pi-mcp@1.5.0` 发布包 `dist/client.js`（`requestHandlers` 仅 `ping`/`roots/list`；未知方法回 `methodNotFound`）与 `@earendil-works/pi-coding-agent@1.5.0` 发布包 `dist/extensions/mcp/runtime.js`（构造 `McpClient` 时只传 `name`/`version`/`requestTimeoutMs`/`roots`）
