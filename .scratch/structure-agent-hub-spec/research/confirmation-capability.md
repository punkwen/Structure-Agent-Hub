# 三类 Agent 与 MCP 如何支持逐次人工确认：证据研究

> 交付物类型：**research 证据稿，不是 SPEC**。本文只回答问题、固定取证版本、区分已证实能力与未知，不替用户选择确认机制或写规定。
> 票：[三类 Agent 与 MCP 如何支持逐次人工确认](../issues/11-confirmation-capability-evidence.md)（Type: research，Mode: AFK）。
> 检索日期：2026-11-06。证据在 `.scratch/tmp-evidence/`（第一方文档与源码的本地快照）；该目录未纳入 git，仅作工作底稿。

## 1. 取证版本锚点

| 对象 | 锚点 | 来源 |
| --- | --- | --- |
| Claude Code | npm `@anthropic-ai/claude-code` latest = **2.1.318**（2026-11-05 取证，见票 03 稿 §2）；本文证据为 `code.claude.com` 官方文档（2026-11-06 快照） | [CC1] |
| OpenCode v1 | npm `opencode-ai` 1.19.5；文档站 `https://opencode.ai/docs/`（2026-11-06 快照） | [OC1] |
| OpenCode v2 | npm `@opencode/cli` 2.2.5；文档站 `https://opencode.ai/v2/docs/`（2026-11-06 快照） | [OC2] |
| pi | npm `@earendil-works/pi-coding-agent` **1.5.0**（tarball sha512 `xNDZ5kq…`，见 `.scratch/tmp-evidence/pi-ca-meta.json`）；内含 `@earendil-works/pi-mcp@1.5.0`（sha512 `DURw3IwH…`，`pi-mcp-meta.json`） | [PI1][PI2] |
| MCP 规范 | `modelcontextprotocol.io`（2026-07-28 版 + 2025-11-25 tools 页，2026-11-06 快照） | [MCP1][MCP2] |

证据标签沿用票 03 稿：`[文档声明]`＝第一方文档明文，未运行验证；`[已证实]`＝源码/registry 机器可读响应确认；`[推断]`＝多条事实组合，非原文；`[未知]`＝未找到第一方证据，不声称不存在。

- [CC1] `https://code.claude.com/docs/en/{permissions,hooks,mcp,security,tools-reference,cli-reference}.md`
- [OC1] `https://opencode.ai/docs/{permissions,mcp-servers,tools}.md`
- [OC2] `https://opencode.ai/v2/docs/{permissions,mcp-servers}.md`
- [PI1] `@earendil-works/pi-coding-agent@1.5.0` 官方包内 `docs/*.md`（`.scratch/tmp-evidence/pi-ca/package/docs/`）
- [PI2] `@earendil-works/pi-mcp@1.5.0` 包内 `dist/`（`.scratch/tmp-evidence/pi-mcp/package/dist/`）
- [MCP1] `https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr` 与 elicitation 页（快照 `mcp-2026-elicitation.md`）
- [MCP2] `https://modelcontextprotocol.io/specification/2025-11-25/server/tools`（快照 `mcp-tools-2025-11-25.md`）

## 2. 原生逐次批准与其他权限提示的区分

### 2.1 Claude Code

- `[文档声明]` 权限模式：`default`（Manual）「Prompts for permission on first use of each tool」；`acceptEdits` 自动接受文件编辑；`plan` 只读；`auto` 由分类器代审；`dontAsk` 自动拒绝所有本应提示的调用；`bypassPermissions` 跳过提示。模式是**会话级**授权形态，与逐次提示不同层。[CC1]
- `[文档声明]` 规则求值顺序固定 deny → ask → allow，「rule specificity doesn't change the order」；`ask` 规则即「prompt for confirmation whenever Claude Code tries to use the specified tool」。允许清单（allow）与逐次确认（ask）是同一规则引擎的不同结果，且 ask 可压过更具体的 allow。[CC1]
- `[文档声明]` "Yes, and don't ask again" 对 Bash/WebFetch **永久按仓库**写入 `.claude/settings.local.json`；对文件修改**只到会话结束**。即逐次确认可被用户自己降级为长期放行。[CC1]
- `[文档声明]` 唯一强制「每次必答」的手段：MCP 服务器在 `tools/list` 里对单个工具标注 `_meta["anthropic/requiresUserInteraction"]: true`。效果：`acceptEdits`/`auto`/`bypassPermissions` 下仍提示、无 don't-ask-again 选项、匹配的 allow 规则不生效、`dontAsk` 直接拒绝、非交互 `--permission-prompt-tool` 的 allow 被改写为 deny（v2.1.199+）。官方定位即「consent or access-grant step where auto-approval would mean no human ever agreed」。[CC1] 这是 Anthropic 私有扩展，非 MCP 标准，其他客户端不识别。
- `[文档声明]` 组织把 connector 工具设为 `ask` 时同样每次必答且不可记忆。[CC1]

### 2.2 OpenCode

- `[文档声明]` v1：`permission` 配置每规则解析为 `allow`/`ask`/`deny`；`ask`＝「prompt for approval」。逐次确认是规则引擎的一种结果，与允许清单同层。最后匹配生效。[OC1]
- `[文档声明]` v1 `always`（对一次权限提示选择"总是允许"）＝「approve future requests matching the suggested patterns (**for the rest of the current OpenCode session**)」，即会话级降级。[OC1]
- `[文档声明]` v2：`permissions` 有序规则（action/resource/effect），`ask`＝「Wait for a decision from the client」；未匹配默认 `ask`。交互选择 `always`＝「Approve it and **save** the tool's proposed patterns for the project」→「Saved approvals are **durable, project-scoped** allow rules」，仅 deny 永远优先。即一次点击把逐次确认降级为**持久**项目规则。[OC2]
- `[文档声明]` v2 另有 policies 层：可在规则与已存批准之后 hard-deny，「turns allow or ask into deny and never grants access」。[OC2]
- 两版 `--auto`（v1）/auto 类模式（v2 policies 之外）只自动批准本应 ask 的请求，deny 仍生效。[OC1][OC2]

### 2.3 pi

- `[文档声明]` 官方 security 页原文：「it **does not ask for approval before every tool call**」；「Watching the transcript, using project trust, and reviewing changes **do not create a security boundary**」。pi 无内建逐次批准/权限系统。[PI1]
- `[文档声明]` 逐次确认只能由扩展实现：`tool_call` 事件「Can block」，返回 `{ block: true, reason }`；官方示例用 `ctx.ui.confirm` 弹确认框，并按工具 `annotations`（readOnlyHint/destructiveHint/openWorldHint）决定是否询问——且文档明言「The hints are **not verified**」。MCP 调用走同一管线，「Extension `tool_call` and `tool_result` handlers, including permission gates, therefore apply to MCP tools」。[PI1]
- `[文档声明]` `ctx.ui.confirm` 依赖 UI：`hasUI` 在 print/JSON 模式为 `false`，扩展必须自行决定无 UI 时的行为（官方未规定默认，[未知]）。[PI1]
- `[已证实]` pi MCP 客户端（`@earendil-works/pi-mcp@1.5.0` `dist/client.js`）只注册 `ping` 与 `roots/list` 两个服务器→客户端请求处理器；无任何权限门。capabilities 由调用方传入，内建 MCP 扩展 `dist/extensions/mcp/runtime.js` `connectOnce()` 实例化 McpClient 时**未传 capabilities**（仅 name/version/timeout/roots）。[PI2]

## 3. MCP elicitation 能请求什么、返回什么

- `[文档声明]` 定义：服务器经由客户端向用户**索取信息**。form 模式请求＝`message`（人类可读）+ `requestedSchema`（受限 JSON Schema：扁平对象、string/number/boolean/enum，**不支持嵌套对象与对象数组**）；响应＝`action: accept|decline|cancel` + 用户填写 `content`。[MCP1]
- `[文档声明]` 客户端义务：标明哪个服务器在请求、提供清晰的拒绝/取消、form 模式允许用户发送前审阅修改。响应三值语义：accept＝明确批准并提交、decline＝明确拒绝、cancel＝未作选择即关闭。[MCP1]
- `[文档声明]` **协议没有**表达「批准对对象 X 执行操作 Y（参数 Z）」的字段：目标/操作/参数只能由服务器塞进 `message` 自由文本或 schema 字段描述；协议也不要求记录操作者身份或持久化确认。2026-07-28 的 MRTR/`InputRequiredResult` 机制把「这次输入属于哪次调用」结构化（重发原请求 + `requestState`），但绑定关系由服务器自持。[MCP1]
- `[文档声明]` tools 规范「For trust & safety and security, clients MUST consider tool annotations to be untrusted unless they come from trusted servers」；「人在环批准」在 tools 规范只是 SHOULD，协议层无「调用前必须批准」的消息或状态机。[MCP2]
- 客户端实际支持：
  - Claude Code `[文档声明]`：自动弹交互对话框；声明 `elicitation: {form:{}, url:{}}`（协议 2026-07-28 连接，或 v2.1.287+ 的 stdio/sse/http/ws），更旧连接仅 form。可用 `Elicitation` hook 整体接管（程序化应答、跳过对话框）、`ElicitationResult` hook 观察/修改/拦截回包。[CC1]
  - OpenCode `[文档声明]`：v2 明确支持（表单/URL 链接，关闭即 cancel）；**v1 文档未提及 elicitation** [未知]。[OC1][OC2]
  - pi `[已证实]`：**不支持**。客户端无 elicitation 处理器（见 §2.3），服务器发 `elicitation/create` 会收到 method-not-found 错误。[PI2]
- 服务器可标注 `requiresUserInteraction`（Claude Code 专属，见 §2.1）；OpenCode/pi 的等价语义 [未知]。

## 4. 确认请求与实际执行如何关联；身份与记录

- Claude Code `[文档声明]`：`PreToolUse` hook 收 `tool_name`/`tool_input`/`tool_use_id`（MCP 工具另带 `mcp_server{name,source}`）；**权限决策事件 `PermissionRequest` 不带 `tool_use_id`**（「without `tool_use_id`」），且 hook 可用 `updatedInput` 整体替换输入再执行（重新过 deny/ask 规则）。要证明「用户看到的参数＝实际执行的参数」，需旁路记录 PreToolUse 与 PermissionRequest 并自行对齐。[CC1]
- pi `[文档声明]`：`tool_call` 事件带 `toolCallId` 与可变 `input`（mutate 会影响实际执行、后续 handler 可见），天然有调用 ID 关联，但权限门本身是扩展代码而非平台机制。[PI1]
- OpenCode：未提供等价的调用前 hook/事件（v1 只有 permission 规则；v2 有 permissions/policies，均无 per-call 回调文档）[未知]。[OC1][OC2]
- 身份：三家文档均无「审批记录含操作者身份」的第一方证据 [未知]。可用的间接记录材料：Claude Code 会话 transcript JSONL（hook 输入含 `transcript_path`/`session_id`）、`PermissionDenied` hook、`/permissions` 显示规则来源文件；OpenCode v2 持久化 allow 规则本身；pi 的 session 文件。无一方声称这是审计台账。
- 结论 `[推断]`：协议层与三家客户端层都**不存在**「确认回执 ↔ 实际执行调用」的可核绑定；票 01 要求确认前展示「目标、拟改内容（含原值/新值）、已知影响、分析设置」，这组内容只能由 **MCP 服务器自己**组织并放进工具返回/elicitation 字段，客户端不会代为生成。

## 5. 客户端中介 vs 直连（绕过审批）

- `[文档声明]` 直连：任何 MCP 客户端都可直接向服务器发 `tools/call`，绕过全部客户端机制（权限规则、提示、hook、`requiresUserInteraction`）。协议不阻止。[MCP1][MCP2][CC1][OC2][PI1]
- `[文档声明]` 中介的退化路径：
  - Claude Code：`claude -p`/Agent SDK/cloud 会话无法弹项目服务器审批，**直接加载** `.mcp.json` 服务器；`--permission-prompts none`（v2.1.259+）让无人应答的提示直接拒绝；`skipDangerousModePermissionPrompt` + `bypassPermissions` 跳过全部提示。[CC1]
  - pi：print/JSON 模式 `hasUI=false`，`ctx.ui.confirm` 不可用，扩展若不显式处理即静默放行或自担行为。[PI1]
  - OpenCode v2：非交互客户端须自行决定如何处理 approval request（文档原文「Non-interactive clients must decide」），deny 规则仍生效。[OC2]
- 结论：逐次确认的保障强度完全取决于**中介形态**；任何"确认"承诺都须同时指明客户端、模式与配置。

## 6. 版本/配置/作用域条件与未知清单

- 条件：Claude Code `requiresUserInteraction` 生效需 ≥v2.1.199（prompt tool 拒绝路径）；elicitation 双模式声明需 2026-07-28 协议或 v2.1.287+；`--permission-prompts` 需 v2.1.259+。OpenCode 契约必须先绑定 v1/v2 大版本（JSON 形态不兼容，见票 03 稿）。pi 逐次确认依赖扩展，扩展随会话加载，受项目信任门控（`--approve`/`--no-approve`/trust.json）。
- `[未知]`（不得据推断宣称已具备）：OpenCode v1 是否支持 elicitation；OpenCode v2 elicitation 是否受 `ask`/policies 约束、能否被扩展拦截；Claude Code `PermissionRequest` 缺 `tool_use_id` 的官方关联手段；pi 权限扩展在 RPC 模式的行为；三家 Windows 下对话框差异；以及全部三家的审批台账能力。

## 7. 后续运行时验证所需条件

固定版本（Claude Code 2.1.318 / OpenCode v1 1.19.5 与 v2 2.2.5 / pi 1.5.0）装入一次性环境，配一个测试 MCP 服务器，它同时具备：(a) 标注 `requiresUserInteraction` 的工具；(b) 发 form elicitation 的工具；(c) 记录收到的 `tools/call` 参数与 `_meta` 的工具。在 Manual/`ask` 配置下逐项观测：每次是否重问；提示展示的参数与服务器实收是否一致；选"总是允许"后是否不再询问（含跨会话）；非交互模式是否 fail-closed；hook/扩展能否拿到可关联的调用 ID；日志/会话文件中是否存在可识别操作者的记录。
