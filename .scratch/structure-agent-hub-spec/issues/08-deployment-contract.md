# 一键部署应承诺什么行为与验收结果

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: resolved
Assignee: punkwen
Blocked by: 03,06,07,09,10,12,14
Parent: ../map.md

## Question

基于各客户端事实与已选能力组织，用户执行一次部署操作时选择什么、安装/注册什么、到哪个作用域、怎样处理既有配置/路径/依赖缺失、如何判断能力真正可用；更新/卸载是否属于所承诺行为？哪些平台、客户端、各适配器宿主软件与运行时版本以及非原生扩展是支持边界？由人选择而非本轮默认。

参考票：[首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md)、[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md)、[三类 Agent 实际支持哪些 Skill 与 MCP 接入方式](03-agent-integration-evidence.md)、[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md)、[OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md)、[核验选定 OpenSees 运行路径的版本兼容性](09-opensees-runtime-verification.md)、[五个现有 MCP 的迁移基线与历史如何保留](10-migration-baseline.md)、[如何落实工程师逐次确认的保障与验收](12-human-confirmation-contract.md)、[哪些现有结构专业 Skill 可以纳入 Hub 索引](14-existing-skills-index-scope.md)。

## Answer

用户于 2026-11-06 确认按推荐答案记录（「按推荐答案执行」）。本票是 planning-only 的 HITL 决策票：以下为 SPEC 的部署契约基线，**不是已实现的部署器，也不是运行时验证结果**。本轮未开发部署器或 MCP/Skill、未运行任何客户端命令、未改动任何用户配置、未写 SPEC 正文。

### 1. 支持边界：下限 + 取证锚点，不写精确 pin

- **平台**：仅 Windows x64。无其他平台的运行证据；[OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer) 已排除非 Windows 承诺。
- **Claude Code**：≥ 2.1.318（取证锚点：2026-11-05 npm `latest`）。更低版本一律记为「未验证」，不推断可用。
- **pi**：≥ 1.5.0（取证锚点：2026-11-05 npm `dist-tags.latest`）。能力下限如实并列：原生 MCP ≥ 0.99.0、`SKILL.md` 目录约定 ≥ 0.20.0（破坏性变更）；`legacy-node20` 0.74.2 **不能假定**具备原生 MCP。
- **OpenCode**：首批**不承诺**。官方同日并存 v1（`opencode-ai` 1.19.5）与 v2（`@opencode/cli` 2.2.5），MCP/Skill JSON 形态互不兼容；绑定大版本后仍需实测，故不进入首批承诺面。
- **宿主软件与运行时**：五个 MCP 的宿主软件版本边界**未定**（[五个现有 MCP 的迁移基线与历史如何保留](10-migration-baseline.md#answer) 未选版本，[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) 定为由用户自备）；该边界留待 SPEC 正文与实施阶段逐适配器确定，本票不预设。OpenSees 唯一已验证组合为 **CPython 3.12.9 + openseespy 3.8.0.0**（`openseespywin` 3.8.0.0，`py3-none-win_amd64`，`Requires-Python >=3.12`）；其他解释器/版本组合无证据，标「未验证」。
- 采用「下限 + 锚点」而非精确 pin：精确 pin 会在下一个 npm 版本即过期，而能力门槛本身是区间。

### 2. 一次部署操作的选择面

- 选择面只有两项：**客户端** + **作用域**。
- **不提供逐组件勾选**：一次部署注册的候选集合是**五个现有 MCP + OpenSees**（前者由 [五个现有 MCP 的迁移基线与历史如何保留](10-migration-baseline.md#answer) 固定，后者形态由 [OpenSees MCP 的仓库起源与首发基线如何确定](15-opensees-mcp-repository-origin.md) 决定）；逐组件勾选不提供，因为各组件的前置与可用性尚未逐项验证。
- 部署写入两类内容：
  1. **MCP 注册条目**：`command`/`args` 指向用户已有的可执行文件；**不复制源码、不构建、不打包**（[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md#answer) 的独立仓库边界）。
  2. **Hub 自有 `Skill/` 目录下的 Skill**（当该目录存在已发布 Skill 时）：复制到客户端技能目录——Claude Code `~/.claude/skills/<name>/`（user）或 `.claude/skills/<name>/`（project），pi `~/.pi/agent/skills/<name>/` 或 `.pi/skills/<name>/`。同名目录已存在即停止并报告，不覆盖；写入后须能通过 `/skills`（Claude Code）或 `/skill:<name>`（pi）观测到，否则不算「已加载」。
- **不安装** `midas-api`（[哪些现有结构专业 Skill 可以纳入 Hub 索引](14-existing-skills-index-scope.md#answer) 定为只索引、不复制）。
- 不安装运行时或厂商软件，不写凭据（[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) §4/§5）。

### 3. 作用域与「假绿」防护

- **默认 user 作用域**：Claude Code 必须显式传 `-s user`（`claude mcp add` 的默认是 `local`，同样落在 `~/.claude.json` 但只对当前项目生效，会被误判为已部署）；pi 默认写 `~/.pi/agent/mcp.json`，project 作用域须显式 `--local`/`-l`。
- **project 作用域仅作显式选项**，且必须计入加载门禁：
  - Claude Code 的 project `.mcp.json` 在交互会话停在 `⏸ Pending approval`；未 trust 的克隆仓库中 `enableAllProjectMcpServers`/`enabledMcpjsonServers` 被忽略。
  - pi 的 `.pi/mcp.json` 仅在授予 project trust 后读取。
- 因此两种作用域下，**`Pending approval` / 未信任一律报告为「未部署」**，不得计入成功。部署器不得以「配置已写入」代替「已加载」。

### 4. 写入方式与既有配置

- 一律走**官方 CLI**（`claude mcp add` / `pi mcp add`），**不直接编辑** `~/.claude.json`（Claude Code 自管文件）。
- 写入前先读现有配置：**同名条目已存在即停止并报告，不覆盖、不删除**。
- pi 的 `pi mcp add` 官方语义是「Add or **replace**」，与 Claude Code 的「同名同作用域直接报错」相反；**replace 语义只在人显式确认后使用**。
- 用户/私有客户端配置的改动需另行确认（[五个现有 MCP 的迁移基线与历史如何保留](10-migration-baseline.md#answer) §4）。
- 本机已存在指向五个 MCP 可执行文件的客户端条目（pi 用户级 `mcp.json` 与 Claude Code 用户级配置均有），部署器不得覆盖这些条目；具体条目属用户私有配置，不记入本票。

### 5. 前置缺失的处理

- 流程：**预检全部 → 列出缺失项 → 默认中止**。只有人显式选择，才部署可用子集。
- 不自动安装或升级任何运行时、厂商软件或 SDK（[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer)、[OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer) §6）。
- OpenSees 只检测解释器与 `import openseespy.opensees`；缺失即停，**不猜路径、不回退到其他解释器**。
- 静默部分部署被禁止：它会让「部署成功」不可判定，而三家客户端均无第一方幂等证据，重跑无法保证收敛。

### 6. 可用性三态：部署器只承诺前两态

| 状态 | 判据 | 由谁判定 |
|---|---|---|
| **已写入** | 配置落盘，官方 CLI 返回成功 | 部署器 |
| **已加载** | Claude Code `claude mcp list` 显示 `✔ Connected`；pi `pi mcp list` 退出码 0（官方语义：连接所有 enabled server，非法条目或未连接即退出码 1） | 部署器 |
| **能力可用** | [首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md#answer) 的五个代表实例全部实测通过 | 工程师，部署后人工验收 |

- `Pending approval` / 未信任 / `! Needs authentication` / `✘ Failed to connect` 均**不属于**「已加载」。
- 部署器**不得宣称「能力可用」**；该判定属部署后人工验收。
- OpenSees 附加约束（[核验选定 OpenSees 运行路径的版本兼容性](09-opensees-runtime-verification.md#answer) 实测）：`TGC_DONE` 只表示脚本跑到结尾，**不等于求解成功**——`analyze()` 返回 `-3` 的脚本仍写 `TGC_DONE`，奇异矩阵也可能返回 `0`；**状态文件缺失必须判失败/未知，即使 exit code 为 0**。

### 7. 逐次确认的客户端纵深

- **Claude Code**：部署器**不覆盖**服务器在 `tools/list` 中声明的 `_meta["anthropic/requiresUserInteraction"]`，并在输出中确认该声明存在。该元数据是唯一能抵抗权限模式与 allow 规则、在交互会话中强制每次提示的机制（`dontAsk` 下直接拒绝、非交互下 allow 被改写为 deny，故「每次必答」并非无条件），且为 Claude Code 私有。
- **pi**：首批**不交付** Hub 自撰的 `tool_call` 扩展。这是对 [如何落实工程师逐次确认的保障与验收](12-human-confirmation-contract.md#answer) §2「pi 需扩展 `tool_call` 门」的**显式收窄**，已由用户确认：pi 1.5.0 无内建权限系统（官方原文「does not ask for approval before every tool call」），故 **pi 上客户端层无拦截**；逐次确认仅由 MCP 服务器侧操作单 + 流程约束承担。
- 该缺口是**已知缺口**，列入 §9「明确不声称」，不得表述为 pi 已具备逐次确认保障。
- 依据 [如何落实工程师逐次确认的保障与验收](12-human-confirmation-contract.md#answer) §1：主闸门在 MCP 服务器侧操作单，客户端层只提高可见性与拦截率、**不作为唯一保障**；服务器侧闸门对 pi 的调用同样生效。
- **不交付、不依赖**第三方 `pi-mcp-adapter`。

### 8. 更新、卸载与非原生扩展

- 首批**不承诺**自动更新，**不承诺**一键卸载或回滚。
- 只承诺：部署器**只写自己声明的条目**，并输出一份**可核对的删除清单**，逐条对应官方移除命令（`claude mcp remove` / `pi mcp remove`）。
- 依据 [三类 Agent 实际支持哪些 Skill 与 MCP 接入方式](03-agent-integration-evidence.md#answer)：三家均无第一方「整体幂等」或「一键卸载/回滚」证明，只有逐项 `remove`/`logout`/`uninstall`。把未证明的能力写进契约等于把未知当承诺。
- **非原生扩展**：只认 pi 的官方内置扩展 `builtin:mcp`（默认启用、读 `mcp.json`）。检测到替换型扩展（如 `pi-mcp-adapter`，安装后 pi 不再读 `mcp.json`）即报告为**不支持组合**，不尝试适配。

### 9. 明确不声称

- 不声称部署器已实现、已测试或已发布。
- 不声称任何客户端实测通过：本轮未运行 `claude mcp list` / `pi mcp list`，§6 的观测项仍是文档声明。
- 不声称 pi 具备技术性逐次确认闸门（§7 的已知缺口）。
- 不声称支持 OpenCode、非 Windows 平台，或任何未列出的客户端版本。
- 不声称五个 MCP 的宿主软件版本边界已定。
- 不声称部署幂等、可一键卸载或可回滚。
- 不声称 OpenSees 求解成功；`TGC_DONE` 只表示脚本正常跑到结尾。
- 不声称部署完成等于 [首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md#answer) 的核心工作流可用。

### 10. 对后续的约束

- [OpenSees MCP 的仓库起源与首发基线如何确定](15-opensees-mcp-repository-origin.md) 的部署形态受本票约束：只走 OpenSeesPy、运行时用户自备、不自动安装。
- 实施时须同时满足 [五个现有 MCP 的迁移基线与历史如何保留](10-migration-baseline.md#answer) 的路径审计与私有配置确认要求。
- 本票不扩大 [哪些现有结构专业 Skill 可以纳入 Hub 索引](14-existing-skills-index-scope.md#answer) 的纳入范围。

### 可核对证据

- [三类 Agent 实际支持哪些 Skill 与 MCP 接入方式](03-agent-integration-evidence.md#answer) 及其 [research 证据稿](https://github.com/punkwen/Structure-Agent-Hub/blob/c7949b81bd257bc6d51035311da85f0a017bdf92/.scratch/structure-agent-hub-spec/research/agent-integration.md)（配置路径、作用域、加载门禁、幂等/卸载未知项）。
- [核验选定 OpenSees 运行路径的版本兼容性](09-opensees-runtime-verification.md#answer) 及其 [09-runtime-evidence/](09-runtime-evidence/)（解释器、wheel、`analyze()` 失败语义、状态文件缺失）。
- [如何落实工程师逐次确认的保障与验收](12-human-confirmation-contract.md#answer)、[三类 Agent 与 MCP 如何支持逐次人工确认](11-confirmation-capability-evidence.md#answer)。
- [首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md#answer)、[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer)、[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md#answer)、[OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer)、[五个现有 MCP 的迁移基线与历史如何保留](10-migration-baseline.md#answer)、[哪些现有结构专业 Skill 可以纳入 Hub 索引](14-existing-skills-index-scope.md#answer)。

## Comments

- 2026-11-06 评审后修正（不改变用户已确认的决策方向，只收紧措辞与补齐缺口）：
  - §1 原写「实测锚点」，与 §9「未运行任何客户端命令」自相矛盾；改为「取证锚点」并注明来源是 npm registry 元数据。`legacy-node20` 0.74.2 由「不具备」改为「不能假定具备」，与 03 的原始措辞一致。
  - §1 宿主软件版本边界补明去向（SPEC 正文与实施阶段逐适配器确定），不再只写「未定」。
  - §2 补明一次部署的候选集合（五个现有 MCP + OpenSees），并给 Skill 分发补上目标路径、同名冲突规则与加载观测项——原稿只写「放入客户端技能目录」，既无冲突规则也无验收。
  - §3 补 `-s user`：`claude mcp add` 默认是 `local`，同样写 `~/.claude.json` 但只对当前项目生效，不显式指定会被误判为已部署。
  - §4 删除本机具体条目清单（含 OpenCode 的 `context7`，而 §1 已不承诺 OpenCode），只保留「已存在指向五个 MCP 的条目、不得覆盖」这一约束；具体条目属用户私有配置。
  - §7 把「不交付 pi 扩展」明确标为对 12 §2 的**显式收窄**（原稿只写「已知缺口」，读起来像 12 未要求）；`requiresUserInteraction` 的「每次必答」补上 `dontAsk`/非交互的例外。
  - 认领（`Status: claimed`）是本会话第一项写入，但与 Answer 落在同一提交，未单独成 commit；过程记录不完整，结论状态无误。
