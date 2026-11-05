# 三类 Agent 实际支持哪些 Skill 与 MCP 接入方式：证据研究

> 交付物类型：**research 证据稿，不是 SPEC**。本文只回答问题、固定取证版本、列出事实对后续决策的约束与可验证选项；**不替用户选择部署策略、作用域、目录、客户端版本或扩展路径**，也不把任何选择写成规定。
> 票：[三类 Agent 实际支持哪些 Skill 与 MCP 接入方式](../issues/03-agent-integration-evidence.md)（Type: research，Assignee: punkwen）。
> 未来发布的分支/路径由主会话集成 owner 处理：`research/hub-spec-agent-integration-20261105` → `.scratch/structure-agent-hub-spec/research/agent-integration.md`。

---

## 1. 问题

1. Claude Code、pi（须核实具体项目而非同名产品）、OpenCode 当前各自**原生**支持哪些 Skill 与 MCP 接入方式？
2. 精确配置路径、JSON 形态、project/user 作用域、技能目录与格式、环境变量/密钥、加载与刷新（重载）机制是什么？
3. 哪些能力**需要额外扩展/外部 CLI**？原生与第三方边界在哪里？
4. pi 原生不支持的能力不得假设存在；若只能靠扩展/外部 CLI，须明确边界与可验证选择，但不替用户选。
5. 部署时**保护现有配置**的可行机制、官方限制与实际成功判据（仅官方事实，不设计安装器）。
6. 锁定取证版本或 SHA/日期；若文档未证明幂等/卸载，明说未知。
7. 约束：不改地图/票/源码/用户配置/git identity；不安装或启动商业软件、不构建/测试、不搜索代理上下文文件（AGENTS.md/CLAUDE.md 等）；客户端/SDK/CLI 文档先用 Context7 resolve/query，再核对第一方源。

---

## 2. 检索日期与取证版本锁定

- **检索日期：2026-11-05**（所有「当前」「latest」均指该日检索结果）。[S5][S23][S32][S7][S26][S27][S47]
- 文档站为**在线更新、无内建版本锁**；Claude Code 文档含大量最低版本门槛（如 v2.1.221、v2.1.246、v2.1.309），OpenCode 文档按 v1/v2 分站。凡带版本门槛的能力均标为 `[文档声明]`，未做运行时验证。[S1][S2][S17]

| 对象 | 锁定的取证锚点 | 来源 |
| --- | --- | --- |
| Claude Code | 官方仓 `anthropics/claude-code` `main` HEAD = `26382c08758260c9f5deb2019d8fe851f89fa9ae`（commit 2026-11-04T00:02:42Z） | [S5][S6] |
| Claude Code | npm `@anthropic-ai/claude-code` `latest` = **2.1.318**（`SEE LICENSE IN README.md`，非 MIT） | [S7] |
| OpenCode | 官方仓 `anomalyco/opencode` 默认分支 `dev` HEAD = `6bd47192ac97527e9fdc5e64c36fd4730aec2acd`（2026-11-05T14:48:48Z） | [S23][S24] |
| OpenCode v1 | npm `opencode-ai` `latest` = **1.19.5**；文档站 `https://opencode.ai/docs/…` | [S26][S11][S12][S13] |
| OpenCode v2 | npm `@opencode/cli` `latest` = **2.2.5**（bin 同时暴露 `opencode` 与 `opencode2`）；文档站 `https://opencode.ai/v2/docs/…` | [S27][S15][S16][S17][S18] |
| pi | 官方仓 `earendil-works/pi` `main` HEAD = `55a5c6914570e2ae31ca36297654483bbbf46883`（2026-11-05T13:20:32Z，MIT） | [S31][S32] |
| pi | `packages/coding-agent/package.json` 版本 **1.5.0**；npm `@earendil-works/pi-coding-agent` `dist-tags.latest` = **1.5.0**（另有 `legacy-node20: 0.74.2`） | [S35][S47] |
| pi | 1.5.0 CHANGELOG 日期 2026-11-02；Skills 系统 0.19.0（2025-12-12）、`SKILL.md` 约定 0.20.0（2025-12-13）、MCP 内置扩展 0.99.0（2026-09-29） | [S44] |

**推断（非文档原文）**：OpenCode v2 在线文档正文与 `dev` 固定 SHA 下的 `services/www/src/docs/content/mcp-servers.mdx` 一致，但官方未给出「文档提交 ↔ npm 版本」映射，故 v2 行为与 2.2.5 的对应关系记为 `[推断]`，不视为已锁定。[S17][S19][S27]

---

## 3. 取证范围与方法

- **Context7 先行（仅作索引，不作事实终点）**：
  - resolve → `/anthropics/claude-code`、`/anomalyco/opencode`、`/earendil-works/pi`；
  - 另返回同名/邻近库：`/isamu/claude`、`/pjbrito/claude-code-docs`、`/websites/opencode_ai`、`/malhashemi/opencode-skills`（第三方 OpenCode Skills 插件）、`/dicklesworthstone/pi_agent_rust`（Rust 实现）、`/sky-valley/pi`（Go 移植）、`/websites/pi_dev`。**这些同名项目未作为本研究证据**；研究对象由下方第一方身份来源锁定。
  - 对三个主库分别 query 了「skills / MCP config / identity / packages / extensions / MCP native」等单一主题，再逐条回到第一方源核对。
- **第一方源**：官方仓固定 SHA 的 Markdown/TypeScript 源码、官方仓 REST API（仓库/分支/目录树）、官方 npm registry 元数据、官方文档站（`code.claude.com`、`opencode.ai`、`opencode.ai/v2/docs`、`pi.dev/docs/latest`）、官方 CHANGELOG。
- **未做**：未安装/启动任何客户端或商业软件；未运行构建、测试、格式化；未改任何用户配置、地图、票、源码、git identity；未读取或搜索 AGENTS.md/CLAUDE.md 等代理上下文文件（仅读取了任务指定的 `skill://research`、`local://structure-hub-charting-brief.md` 与票文件）。
- Claude Code 仓根目录列表包含 `CHANGELOG.md`、`plugins/`、`mods/`、`examples/`、`scripts/`、`Script/`、`feed.xml` 等，**未见顶层 `src/` 实现目录**；因此本文把 CLI 运行时行为视为官方文档声明而非源码级验证。[S10] `[推断]`

### 证据标签

| 标签 | 含义 |
| --- | --- |
| `[已证实]` | 由固定 SHA 源码、机器可读 API/registry 响应，或文档与源码一致确认。 |
| `[文档声明]` | 第一方文档明文写出；因约束未安装/运行客户端，未做运行时验证。 |
| `[推断]` | 由多条事实组合得出，非文档原文。 |
| `[未知]` | 本次取证范围内未找到第一方证据；**不声称该能力/文档不存在**。 |

---

## 4. 身份核实（避免同名混用）

### 4.1 pi = `badlogic/pi-mono` → `earendil-works/pi-mono` → `earendil-works/pi`，子包 `packages/coding-agent`

- `[已证实]` GitHub API `GET /repos/badlogic/pi-mono` 返回仓库 id `1035029907`、`name: "pi"`、`full_name: "earendil-works/pi"`；浏览器打开 `https://github.com/badlogic/pi-mono` 也渲染为 `# earendil-works/pi`。即旧地址是官方重定向，不是另一个产品。[S29][S30]
- `[已证实]` `GET /repos/badlogic/pi-mono/contents/packages/coding-agent` 重定向到 `earendil-works/pi` 同名目录，列出 `package.json`、`docs/`、`src/`、`CHANGELOG.md` 等；本票核查的旧地址 `badlogic/pi-mono/packages/coding-agent` 确实属于该仓库谱系，用户原始需求只称「pi」。[S33]
- `[已证实]` 中间名证据：npm `@earendil-works/pi-coding-agent@0.74.0` 的 `homepage` = `https://github.com/earendil-works/pi-mono#readme`、`repository.url` = `git+https://github.com/earendil-works/pi-mono.git`、`repository.directory` = `packages/coding-agent`；CHANGELOG 明确记载「Updated repository links and package references for the move to `earendil-works/pi-mono` and `@earendil-works/*` package scopes」，更早条目链接仍为 `badlogic/pi-mono/issues/...`。[S47][S44]
- `[已证实]` 当前身份：`packages/coding-agent/package.json` 的 `name` = `@earendil-works/pi-coding-agent`，`repository.directory` = `packages/coding-agent`，`repository.url` = `git+https://github.com/earendil-works/pi.git`，`author` = `Mario Zechner`，`engines.node >= 22.19.0`，`bin.pi` 存在。[S35]
- `[已证实]` 官方 README 自称 "Pi is a minimal, extensible agent harness"，列出 `packages/coding-agent` 为 "Interactive coding agent CLI"，安装命令 `npm install -g --ignore-scripts @earendil-works/pi-coding-agent`，文档域 `https://pi.dev/docs/latest`；README 仍以 `badlogic/pi-skills`、`pi-mono` sessions、`@badlogicgames` 署名关联原作者。[S34][S48]
- **结论**：本票的「pi coding agent」= `@earendil-works/pi-coding-agent`（`packages/coding-agent`），仓库 `earendil-works/pi`，是 `badlogic/pi-mono` 的续体。**不混用** Context7 返回的 Rust/Go 同名项目。[S34][S35][S29]

### 4.2 OpenCode = `sst/opencode` → `anomalyco/opencode`

- `[已证实]` `GET /repos/sst/opencode` 返回 id `975734319`、`full_name: "anomalyco/opencode"`；`GET /repos/anomalyco/opencode` 描述 "The open source coding agent."、homepage `https://opencode.ai`、默认分支 `dev`、MIT。[S24][S25]
- `[已证实]` 官方仓同时存在 **v1 / v2 两条发布线与两套文档**：npm `opencode-ai@1.19.5`（`/docs/…`）与 `@opencode/cli@2.2.5`（`/v2/docs/…`）；v2 安装页列出 `npm install -g @opencode/cli`、Homebrew `anomalyco/tap/opencode-v2`、Docker `ghcr.io/anomalyco/opencode:2.0.0`。`https://opencode.ai/docs/v2/mcp-servers/` 返回 404，正确 v2 路径为 `https://opencode.ai/v2/docs/mcp-servers/`。[S26][S27][S15][S17]

### 4.3 Claude Code

- `[已证实]` `anthropics/claude-code`，homepage `https://code.claude.com/docs/en/overview`，`license: null`（npm 显示 `SEE LICENSE IN README.md`），默认分支 `main`。[S6][S7]

---

## 5. Claude Code

### 5.1 原生 Skill

- `[文档声明]` 原生支持 **Agent Skills**（`SKILL.md` + YAML frontmatter + Markdown 正文）；遵循 `agentskills.io` 开放标准，并扩展 invocation control、subagent 执行、动态上下文注入。自定义命令 `.claude/commands/deploy.md` 已合并进 skills，旧文件仍可用。[S1]
- `[文档声明]` 技能位置与作用域（原文表格）：[S1#where-skills-live]
  | 作用域 | 路径 | 生效范围 |
  | --- | --- | --- |
  | Enterprise | 管理设置目录下的 `.claude/skills/<skill-name>/SKILL.md` | 组织部署到的所有用户 |
  | Personal（user） | `~/.claude/skills/<skill-name>/SKILL.md` | 本机所有项目（不含 Cowork/云会话） |
  | Project | `.claude/skills/<skill-name>/SKILL.md` | 本仓库会话，可提交共享 |
  | Nested | `<subdir>/.claude/skills/<name>/SKILL.md` | 在该子目录及其下启动的会话 |
  | Additional directory | `--add-dir` 目录内的 `.claude/skills/...` | 该会话 |
  | Plugin | `<plugin>/skills/<name>/SKILL.md` | 插件启用处，命令 `/plugin-name:skill-name` |
  | claude.ai account | 账户同步技能 | Cowork/云/登录账户的终端会话 |
- `[文档声明]` 项目技能从启动目录向上到仓库根逐级加载；worktree 仅搜到 worktree 根；嵌套技能在 Claude 首次读/写该子目录文件时才加载，可用 `/add-dir` 提前加载；目录名冲突时以 `<dir>:<name>` 区分。[S1][S8]
- `[文档声明]` 格式：`SKILL.md` 首行必须是 `---`，否则整份按正文处理；frontmatter 字段全可选，仅 `description` 推荐；字段含 `name`、`description`、`when_to_use`、`argument-hint`、`arguments`、`disable-model-invocation`、`user-invocable`、`allowed-tools`、`disallowed-tools`、`model`、`effort`、`context`、`agent`、`background`、`hooks`、`paths`、`shell`、`metadata`、`license`、`compatibility`。可移植（claude.ai 上传/Skills API）字段仅 `name` / `description` / `license` / `compatibility` / `metadata` / `allowed-tools`，多余字段会硬报错。[S1#frontmatter-reference]
- `[文档声明]` 目录名（或 frontmatter `name`）即 `/name` 命令名；支持配套文件（`reference.md`、`scripts/`）；`${CLAUDE_SKILL_DIR}`、`${CLAUDE_PROJECT_DIR}`、`${CLAUDE_SESSION_ID}` 等字符串替换。[S1]
- `[文档声明]` 插件结构第一方示例：`plugin-name/` 含 `.claude-plugin/plugin.json`、`commands/`、`agents/`、`skills/`、`hooks/`、`.mcp.json`、`README.md`；插件根目录 `.mcp.json` 或 `plugin.json` 内联 `mcpServers` 可随插件分发 MCP 服务器。[S9][S2]
- `[已证实]` 源码/CHANGELOG 级别的补充：项目 `.claude/skills` 被 git 忽略/未跟踪时仍加载；`allowed-tools` 在 managed `allowManagedPermissionRulesOnly` 下的行为有修复记录；嵌套目录技能发现与名称冲突处理有 CHANGELOG 条目。[S8]

### 5.2 原生 MCP

- `[文档声明]` 原生 MCP 客户端；支持 stdio、`http`（`streamable-http` 别名）、已弃用 `sse`、`ws`；`"type": "sdk"` 仅 SDK host/桌面应用可注册，配置文件中出现会被跳过。[S2]
- `[文档声明]` 配置路径与 JSON 形态：
  - project：仓库根 `.mcp.json`，`{"mcpServers":{"<name>":{...}}}`；
  - local（默认）/ user：`~/.claude.json`（Claude Code 自管文件，官方称「you don't need to edit it」，含账户信息、MCP 配置、per-project trust 决定）；local 写在 `projects["/abs/path"].mcpServers` 下；
  - managed：`managed-mcp.json`（macOS `/Library/Application Support/ClaudeCode/managed-mcp.json`；Linux/WSL `/etc/claude-code/managed-mcp.json`；Windows `C:\Program Files\ClaudeCode\managed-mcp.json`），格式同 `.mcp.json`；
  - plugin：插件根 `.mcp.json` 或 `plugin.json` 内联 `mcpServers`。[S2][S3][S4][S9]
- `[文档声明]` 三种安装作用域（`-s` / `--scope`）：[S2#mcp-installation-scopes]
  | Scope | 存储 | 加载范围 | 团队共享 |
  | --- | --- | --- | --- |
  | `local`（默认） | `~/.claude.json` 当前项目条目 | 仅当前项目 | 否 |
  | `project` | 项目根 `.mcp.json` | 仅当前项目（可提交共享） | 是 |
  | `user` | `~/.claude.json` 顶层 | 本机所有项目 | 否 |
- `[文档声明]` 同名优先级：`local > project > user > plugin > claude.ai connectors`（`managedMcpServers` 更高）；**整条 server entry 取自最高优先级源，字段不跨作用域合并**。[S2][S4]
- `[文档声明]` 服务器条目字段：`command` / `args` / `env` / `cwd`（stdio）；`url` / `headers` / `oauth` / `headersHelper` / `timeout` / `alwaysLoad`（http/sse/ws）；`type` 缺省时按 stdio 解析，故「有 `url` 无 `type`」是配置错误。[S2]
- `[文档声明]` `${VAR}` 与 `${VAR:-default}` 可在 `command` / `args` / `env` / `url` / `headers` 展开；未设置且无默认值时配置仍加载并保留字面量 `${VAR}`，`claude mcp list` 报缺变量警告；空字符串算「已设置」；**远端 `url`/`headers` 中的凭据类变量（如 `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN`、`AWS_BEARER_TOKEN_BEDROCK`、`HTTPS_PROXY`、`NPM_TOKEN`）被强制读为空**，`${VAR}` 引用在 CLI/`mcp` 输出中按名显示不回显明文。[S2#environment-variable-expansion-in-mcp-json]
- `[文档声明]` 插件路径占位符 `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` / `${CLAUDE_PROJECT_DIR}`；stdio 子进程自动获得 `CLAUDE_PROJECT_DIR`；`claude mcp add --env KEY=VALUE` 可注入环境变量。[S2]

### 5.3 重载、环境变量/密钥、官方限制

- `[文档声明]` **Settings 热重载**：Claude Code 监视 `~/.claude/settings.json`、`.claude/settings.json`、`.claude/settings.local.json`、managed settings 并在运行会话中重载（含 `permissions`、`hooks`、`apiKeyHelper`），触发 `ConfigChange` hook；但 `model`、`effortLevel`、`modelSettings` 等只读一次的键需 `/model` `/effort` 或重启；managed settings 从 MDM/console 到达按调度而非即时。[S3]
- `[文档声明]` **Skills 热重载**：`~/.claude/skills/`、项目 `.claude/skills/`、`--add-dir` 内 `.claude/skills/` 的 `SKILL.md` 增删改在会话内自动生效（bare mode 除外）；会话启动后才新建的顶层 skills 目录需 `/reload-skills`，且之后每次改动都要再跑；插件 skill 的 `hooks/`、`.mcp.json`、`agents/`、`output-styles/` 改动需 `/reload-plugins`。[S1#edit-a-skill-during-a-session]
- `[文档声明]` **MCP 重载**：`/mcp` 可 Reconnect、`/mcp reconnect all` 可重试所有失败服务器；`list_changed` 通知在交互会话自动刷新工具表；`managedMcpServers` 的增删/改在已运行的交互会话中自动连接/重连/断开（非交互 `-p` 保留到结束）。**[未知]** 手工编辑 `.mcp.json` 或 `~/.claude.json` 后「运行中会话是否自动重建连接」未见第一方明文。[S2][S4]
- `[文档声明]` 密钥/凭据：OAuth client secret 存系统 keychain（macOS）或凭据文件，**不在配置里**；`claude mcp logout <name>` 清凭据；`claude mcp remove` 删除本地 OAuth token/客户端注册但**不在授权服务器吊销**（须先 `logout` 再 `remove`）。[S2]
- `[文档声明]` 环境变量：`CLAUDE_CONFIG_DIR`（改 `~/.claude` 位置）、`CLAUDE_CODE_SYNC_SKILLS=1`、`MCP_TIMEOUT`、`MCP_TOOL_TIMEOUT`、`MAX_MCP_OUTPUT_TOKENS`、`ENABLE_TOOL_SEARCH`、`MCP_SDK_GENERATION`、`MCP_PROTOCOL_NEGOTIATION`；项目级 `.claude/settings.json` 的 `env` **不能**设置 `CLAUDE_CONFIG_DIR`、`CLAUDE_CODE_TMPDIR`、`TMPDIR`/`TMP`/`TEMP`（须放 shell/user/managed）。[S2][S3][S8]
- `[文档声明]` `headersHelper` 是任意 shell 命令，项目 `.mcp.json` / local scope 的 helper 仅在接受该目录的 trust dialog 后执行；仓库/插件提供的 helper 会被剥离名字含 `TOKEN/SECRET/PASSWORD/KEY/AUTH` 的环境变量。[S2]
- `[文档声明]` 官方限制（部署相关）：
  - 安装 Claude Code **不会创建任何 settings 文件**；settings 为严格 JSON（`//`、尾逗号都是语法错），坏文件在启动时报 `Settings Error`/`Settings Warning`，`~/.claude.json` 解析失败会备份到 `~/.claude/backups/.claude.json.corrupted.<timestamp>`。[S3]
  - Windows：`~/.claude` = `%USERPROFILE%\.claude`；**Windows 上 `.claude/settings.local.json` 与 `.claude/settings.json` 同放（不按仓库根定位）**。[S3]
  - project `.mcp.json` 服务器在交互会话需审批；`claude mcp reset-project-choices` 可重置；**`claude -p` / Agent SDK / cloud 会话无法弹窗，会直接加载 project 服务器**；未 trust 的克隆仓库里，提交到 `.claude/settings.json` 的 `enableAllProjectMcpServers` / `enabledMcpjsonServers` 被忽略，服务器停在 `⏸ Pending approval`。[S2]
  - `managed-mcp.json` 存在时用户不能增删改用其他 MCP；`--mcp-config` / `--strict-mcp-config` 在工作站会直接启动失败并报 `You cannot dynamically configure MCP servers when an enterprise MCP config is present`。[S4]
  - 同名同 scope 再 `claude mcp add` **失败**（`MCP server sentry already exists in local config`），即该 add 非幂等。[S2]
  - 保留名（`workspace`、`claude-in-chrome`、`computer-use`、`Claude Preview`、`Claude Browser`）会被跳过；服务器名仅允许字母数字 `-` `_`。[S2]

### 5.4 官方给出的「实际成功判据」

- `[文档声明]` `claude mcp add` 打印 `Added ...` 表示**配置已写入**；`claude mcp list` 显示 `✔ Connected` / `! Needs authentication` / `✘ Failed to connect` / `⏸ Pending approval`；`claude mcp get <name>` 看细节与 `Issue:`；`/mcp` 显示工具数与 cached/connected 状态；`/status` 的 `Setting sources` 列出已加载 settings 文件；`claude doctor`（终端只读安装诊断）列被拒绝项；`/skills` 列已加载技能；`/plugin` 管理插件服务器。[S1][S2][S3]
- `[文档声明]` managed 配置的官方验证两步：`claude mcp list` 只列受管服务器；`claude mcp add --transport http test https://example.com/mcp` 应被企业策略拒绝（无需真实 URL）。[S4]

---

## 6. OpenCode（v1 与 v2 **并存且 JSON 形态不兼容**）

> 这是本研究最重要的决策约束：官方同日提供两套文档、两个 npm 包、两套 MCP/Skill 配置形态。下文分别列出，**不选择**。

### 6.1 v1（`opencode-ai` / `https://opencode.ai/docs/…`）

**Skills** `[文档声明]` [S11]
- 目录：project `.opencode/skills/<name>/SKILL.md`、`~/.config/opencode/skills/<name>/SKILL.md`，兼容 `.claude/skills/`、`~/.claude/skills/`、`.agents/skills/`、`~/.agents/skills/`；项目路径从 cwd 向上到 git worktree。
- `SKILL.md` 必须 YAML frontmatter，`name`（必需）、`description`（必需，1–1024 字符）、`license` / `compatibility` / `metadata` 可选；未知字段忽略；`name` 须 `^[a-z0-9]+(-[a-z0-9]+)*$`、1–64 字符、且**必须与目录名一致**；OpenCode 1 不用 metadata 控制斜杠命令或自动选择。
- 通过原生 `skill` 工具按需加载：工具描述含 `<available_skills>`，`skill({ name: "git-release" })`；`opencode.json` 的 `permission.skill` 支持 `allow`/`deny`/`ask` 与通配符，可在 agent frontmatter / `agent.<id>.permission` 覆盖，也可用 `tools: { skill: false }` 关闭。

**MCP** `[文档声明]` [S12][S13][S14]
- 配置 `opencode.json` / `opencode.jsonc`（JSONC 允许注释与尾逗号），`$schema: https://opencode.ai/config.json`；`mcp` 下**直接以服务器名为键**：
  ```jsonc
  { "mcp": { "srv": { "type": "local", "command": ["npx","-y","pkg"], "environment": { "K": "v" }, "enabled": true } } }
  ```
  local 字段：`type:"local"`、`command`（数组）、`cwd`、`environment`、`enabled`、`timeout`（默认 30000ms）；remote：`type:"remote"`、`url`、`enabled`、`headers`、`oauth`（`{clientId,clientSecret,scope}` 或 `false`）、`timeout`。
- `enabled:false` 可保留配置但不启动；`tools` / `agent.<id>.tools` 可用 glob 全局或按 agent 关掉 MCP 工具。
- 环境变量替换 `{env:VAR}`（如 `"Authorization": "Bearer {env:MY_API_KEY}"`）；OAuth token 存 `~/.local/share/opencode/mcp-auth.json`；provider 凭据存 `~/.local/share/opencode/auth.json`。
- CLI：`opencode mcp add`（交互式向导）、`opencode mcp list` / `ls`（列出配置与连接状态）、`opencode mcp auth [name]` / `auth list`、`opencode mcp logout [name]`、`opencode mcp debug <name>`；`opencode debug config` 输出解析后配置。[S12][S13][S14]
- 配置优先级（**合并而非替换**，后者覆盖冲突键）：`① .well-known/opencode 远端默认 → ② ~/.config/opencode/opencode.json 全局 → ③ OPENCODE_CONFIG 自定义文件 → ④ 项目根 opencode.json → ⑤ .opencode/ 目录（agents/commands/plugins）→ ⑥ OPENCODE_CONFIG_CONTENT 内联 → ⑦ 系统 managed 文件（macOS `/Library/Application Support/opencode/`、Linux `/etc/opencode/`、Windows `%ProgramData%\opencode`）→ ⑧ macOS MDM `ai.opencode.managed`（最高、用户不可覆盖）`；`OPENCODE_CONFIG_DIR` 指定额外配置目录且可覆盖；`opencode.json` 可安全提交 Git。[S13]
- `[文档声明]` `autoupdate`：v1 文档写「Updates are never installed automatically」，只通知、由 `/update` 或 `opencode upgrade` 安装。[S13]

### 6.2 v2（`@opencode/cli` / `https://opencode.ai/v2/docs/…`）

**Skills** `[文档声明]` [S18]
- 默认目录 `.opencode/skills/<skill-id>/SKILL.md`；自动搜索表：global `~/.config/opencode/skills`、global 兼容 `~/.claude/skills` `~/.agents/skills`、project `.opencode/skills`、project 兼容 `.claude/skills` `.agents/skills`；markdown 文件须在 source 根（如 `skills/review.md`），`SKILL.md` 可嵌套（如 `skills/git-release/SKILL.md`）；含 `SKILL.md` 的目录即一个 skill 不再向内搜；隐藏项与 `node_modules` 跳过；扫描最深 6 层。
- 前置元数据**全部可选**：`name` 只是显示名，`description` 决定模型可见性；`metadata.opencode/autoinvoke:false` 或 `disable-model-invocation:true` 隐藏；`license`/`compatibility` 接受但不解释；**ID 由路径派生、区分大小写**，frontmatter `name` 无需匹配目录，v2 当前不强制 kebab 正则/1–64 长度/description 上限。
- `skills` 数组（任意 `opencode.json(c)`）可追加本地目录或 HTTP catalog（基址 `index.json`，需 `version` 递增刷新缓存）；数组跨配置文件**合并而非替换**；Console 工作区也可共享技能。
- 加载：每步只把 ID/name/description 列给模型，模型以 `skill` 工具 `{"id":"git-release"}` 载入正文，或用户提示中 `@skill-id`；载入时检查 `permissions` 中 `action:"skill"` 的 `allow`/`ask`/`deny`，并按 source 优先级覆盖同名 ID（内置 → `.claude` → `.agents` → 全局 → 项目 → 显式 `skills` 配置）。
- `[已证实]` 固定 SHA 源码 `packages/core/src/config/plugin/skill.ts`：v2 技能插件订阅 Watcher 文件变更（100ms debounce）后 `refresh()` + `ctx.skill.reload()`，并订阅 `config.updated` 事件重扫；即 v2 技能目录在会话内可热更新。**用户文档未以文字声明该行为**，本文据源码标为已证实（v2 源码）。[S22]

**MCP** `[文档声明]` [S17][S19][S20]
- **形态与 v1 不兼容**：`mcp.servers.<name>`（v2 明确写「V2 does not place server names directly under `mcp`」）；用 `disabled:true` 而非 `enabled:false`；同名 server 对象被更高优先级配置**整体替换**（不是字段合并）。
  ```jsonc
  { "$schema": "https://opencode.ai/config.json",
    "mcp": { "servers": { "everything": {
      "type": "local", "command": ["npx","-y","@modelcontextprotocol/server-everything"],
      "cwd": ".", "environment": { "MCP_API_KEY": "{env:MCP_API_KEY}" }, "disabled": true } } } }
  ```
- local 字段：`type`、`command`、`cwd`、`environment`、`disabled`、`codemode`（默认 true）、`timeout`（`startup`/`catalog`/`execution`）、`protocol`（`legacy` 默认 / `auto` / `2026-07-28`）、`pool`；remote：`type:"remote"`、`url`、`headers`、`oauth`、`disabled`、`codemode`、`timeout`、`protocol`、`pool`。[S17][S20]
- OAuth 默认开启，`oauth:false` 关闭；v2 用 **snake_case** `client_id` / `client_secret` / `scope` / `callback_port` / `redirect_uri` / `auth_server_metadata_url`（v1 为 camelCase `clientId`/`clientSecret`）；CIMD 文档 URL `https://opencode.ai/oauth/opencode/client.json`；凭据「stored outside project configuration」。[S17][S20]
- CLI：`opencode mcp add <name> --url <url>`（project），`--global` 写全局配置；`opencode mcp add <name> -- <command> [args]`，`--env KEY=VALUE` 可重复、`--header` 可重复；`opencode mcp list`；`opencode mcp auth <name>`；`/mcps` 交互登录。成功判据官方示例 `✓ context7  connected`；`needs authentication` 时需 `/mcps` 或 `opencode mcp auth` 登录。[S17]
- `[已证实]` 固定 SHA 的 `packages/schema/src/mcp.ts` 用 Effect Schema 定义 `LocalConfig`/`RemoteConfig`（含 `disabled`、`codemode`、`protocol`、`pool`、`OAuthConfig` 的 snake_case 字段）与状态 `connected|pending|disabled|failed|needs_auth`；`packages/core/src/config/variable.ts` 实现 `{env:VAR}` 与 `{file:path}` 文本替换（缺文件/缺变量替换为空并记警告，避免一处坏引用毁掉整份配置）。[S20][S21]

**v2 配置与保护** `[文档声明]` [S16]
- 位置：系统目录（macOS `/Library/Application Support/opencode`、Linux `/etc/opencode`、Windows `%ProgramData%\opencode`）可放 `opencode.json(c)` 及 `agents/`、`commands/`、`skills/`、`plugins/`；用户 `~/.config/opencode/opencode.json(c)`；项目 `<dir>/opencode.json(c)` 或 `<dir>/.opencode/opencode.json(c)`。
- 发现顺序：从 cwd 向文件系统根，先按「远→近」合并直接 `opencode.json(c)`，再按同顺序合并 `.opencode/` 内文件；**每个 `.opencode` 配置覆盖所有直接配置**；系统 managed 优先级最高；MDM `ai.opencode.managed` 再覆盖系统目录。非冲突设置保留。
- `policies`（有序 `action`/`resource`/`effect`）可 deny provider / hard-deny permission / **block an MCP server, skill, or plugin**；官方明确："Settings alone cannot stop users from adding providers, MCP servers, agents, or plugins; use policies in managed configuration to enforce restrictions."
- `permissions` 为有序数组（v1 是 `permission` 对象）；`watcher.ignore` 控制文件监听忽略；`update: "auto"` 时「Automatic installation does not restart a running server. Restart it manually to activate the installed update.」

### 6.3 OpenCode 重载与未知项

- `[已证实]` v2 技能由源码 watcher + `config.updated` 热重扫（见 6.2）。[S22]
- `[未知]` v1/v2 的 **`opencode.json` / `mcp` 配置修改后，运行中的 MCP 连接是否自动重建、是否必须重启**：本次查证的 v1 config / v1 mcp / v1 cli / v2 config / v2 mcp 文档均未给出明确规则（`grep reload|restart|hot.?reload|takes effect` 在 v2 MCP 页无匹配，v1 config 页仅命中与配置重载无关的 `watcher.ignore`）。[S13][S17]
- `[未知]` `opencode mcp add` 对同名服务器的重复行为、以及完整部署的幂等/卸载，均未在第一方文档中检索到声明。[S14][S17]
- `[未知]` 未检索到与 Claude Code workspace trust / pi project trust 等价的「项目配置需显式信任」关卡；不声称不存在（v2 有 policies 与 managed 配置）。

---

## 7. pi（`@earendil-works/pi-coding-agent`）

### 7.1 原生 Skill（第一方，非第三方插件）

- `[已证实]` CHANGELOG：0.19.0（2025-12-12）加入 Skills system，支持 `~/.claude/skills/*/SKILL.md`、`~/.codex/skills/`、`~/.pi/agent/skills/`、`.pi/skills/`，系统提示只列 name/description、模型用 read 工具按需载入；0.20.0（2025-12-13）**破坏性变更**改用 `SKILL.md` 目录约定（迁移：`~/.pi/agent/skills/foo.md` → `foo/SKILL.md`）。[S44]
- `[文档声明]` 当前 1.5.0 文档：Pi 实现 [Agent Skills specification](https://agentskills.io/specification)；技能是「含 `SKILL.md` 的目录」，frontmatter 后接指令；字段 `name`/`description`/`license`/`compatibility`/`metadata` + 实验性 `allowed-tools` + `disable-model-invocation`；名称小写字母数字连字符、≤64 字符、description ≤1024；**malformed `SKILL.md` 与缺 description 的技能不加载**，无效字段多为警告而非启动失败；同名冲突保留先发现者并警告；Pi 不要求 `name` 与目录名一致。[S36][S46]
- `[文档声明]` 目录：用户技能 `<agent-dir>/skills`（默认 `~/.pi/agent/skills`）、项目 `.pi/skills`；另支持 Agent Skills 位置 `~/.agents/skills/` 与 `.agents/skills/`（项目 `.agents/skills` 从 cwd 向祖先到仓库根）；`settings.json` 的 `skills` 数组可加文件/目录（支持 `!glob`、`+path`、`-path`）；Pi package 可用常规 `skills/` 目录或 `package.json` 的 `pi.skills` 清单；`enableSkillCommands` 控制是否注册 `/skill:name`；`--no-skills` 关闭（0.19.0 记录）。[S36][S38][S39][S41][S44]
- `[已证实]` 固定 SHA 源码 `src/core/skills.ts`：`loadSkills()` 默认从 `agentDir/skills`（user）与 `<cwd>/.pi/skills`（project）加载；目录含 `SKILL.md` 即停止递归，否则载入根级 `.md` 并递归；跳过 `.` 开头与 `node_modules`；用 `<available_skills>` XML 注入系统提示。[S46]
- `[文档声明]` 启动只把 name/description/path 放系统提示，模型匹配后读 `SKILL.md`；`/skill:name` 可强制；`/reload` 在会话内编辑技能后重扫；验证方式「从技能可发现位置启动 Pi，检查 startup diagnostics 与 `/skill:name` 命令」。[S36][S38]
- `[文档声明]` 项目技能可让模型运行脚本/改文件，官方要求「先审阅陌生技能及配套文件，再授予 project trust」；Pi 明确**不自带权限系统**，工具与扩展以启动进程权限运行，project trust 不约束工具调用。[S36][S40][S34]

### 7.2 原生 MCP：**内置扩展（first-party built-in extension），不是必须安装的第三方组件**

- `[已证实]` CHANGELOG 0.99.0（2026-09-29）：「Added codemode, tool search, and **MCP support as built-in extensions**. … MCP servers over stdio or streamable HTTP, with OAuth, come from `mcp.json` (global, or per project once trusted) or `pi.registerMcpServer()` and are managed with `/mcp` and `pi mcp add|remove|list|login|logout`」。[S44]
- `[已证实]` `settings.md` / `extensions.md`：内置扩展名为 `builtin:mcp`（另有 `builtin:llama.cpp`、`builtin:codemode`、`builtin:tool-search`），**默认加载**；`extensions: ["-builtin:mcp"]` 或 `pi config` 可禁用；`--no-mcp` 单次运行禁用；`pi mcp` shell 命令**始终**用内置实现、不加载扩展。[S39][S43][S37]
- `[已证实]` 官方仓内第一方 MCP 客户端包 `@earendil-works/pi-mcp`（`packages/mcp/README.md`）声明「does not depend on the official MCP SDK or other pi packages」，`packages/coding-agent/package.json` 直接依赖 `@earendil-works/pi-mcp@1.5.0`；其协议面为 MCP `2025-11-25`（兼容 2025-06-18 / 2025-03-26 / 2024-11-05），**不支持** legacy HTTP+SSE、sampling、tasks、batch JSON-RPC。[S45][S35]
- `[文档声明]` 配置路径/JSON 形态：用户 `~/.pi/agent/mcp.json`，项目 `.pi/mcp.json`（**仅 project trust 授予后读取**）；形状与其他 MCP 客户端一致：
  ```json
  { "mcpServers": {
      "filesystem": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "."] },
      "docs": { "url": "https://example.com/mcp", "headers": { "Authorization": "Bearer ${DOCS_TOKEN}" } } } }
  ```
  stdio 用 `command`/`args`/`env`/`cwd`；HTTP 用 `url`/`headers`/`oauth`；两者支持 `timeout`（秒，默认 60）、`enabled:false`、`exposure`（`codemode` 默认 / `deferred` / `direct` / `hidden`）、`toolExposure`、`description`；`type` 可选且只能是 `stdio` / `http` / `streamable-http`，**`sse` 被拒绝**；**legacy SSE transport 不支持**。[S37]
- `[文档声明]` 密钥：`env` / `headers` 值支持 `${VAR}`；也支持整值命令 `"Authorization": "!echo Bearer $(gh auth token)"`；`oauth.clientSecret` 可用环境变量或命令；OAuth token 存 `~/.pi/agent/mcp-auth.json`，provider 凭据存 `<agent-dir>/auth.json`；日志 `~/.pi/agent/mcp.log`（>5MB 轮转为 `mcp.log.1`）。官方建议「把个人服务器与含凭据的服务器放用户级文件，项目文件只放项目必需且仅在可信项目」。[S37][S38][S49]
- `[文档声明]` 作用域/覆盖：project 同名条目**整体替换** user 条目；但若 project 条目不含 `command`/`url`/`type`，则只覆盖 `enabled`/`exposure`/`toolExposure`，**保留** user 条目的 `env`/`headers`/`auth` 等；`/mcp` 的 enable/exposure 变更「saved to the file that defines the server without replacing unrelated content」；`pi mcp add --local/-l` 写项目配置，默认写用户级；`pi mcp add` 文档措辞为「**Add or replace** a … server in `mcp.json`」。[S37][S42]
- `[文档声明]` 重载：会话外增删改服务器后须 `/reload`；`/mcp` 可 inspect / sign in / reconnect / change exposure / enable-disable；shell 命令 `pi mcp add|remove|list|login|logout` 不加载扩展；`pi mcp list` **连接每一个 enabled server 并打印 state/tools/errors，配置非法或 enabled server 未连接时退出码 1**。[S37][S42]
- `[文档声明]` 环境变量：`PI_CODING_AGENT_DIR`（改 agent 目录，默认 `~/.pi/agent`）、`PI_CODING_AGENT_SESSION_DIR`、`PI_PACKAGE_DIR`、`PI_OFFLINE`、`PI_SELF_UPDATE_COMMAND`、`PI_TELEMETRY`、`PI_CODEMODE_MAX_WORKERS` 等；provider 凭据另见 `providers.md`。[S49][S38]

### 7.3 pi 原生 / 扩展 / 第三方边界（可验证，不选择）

| 能力 | 第一方「原生」事实 | 扩展/外部边界 | 证据 |
| --- | --- | --- | --- |
| Skills | 内置 skills 系统，`~/.pi/agent/skills`（agent-dir）、项目 `.pi/skills`、`.agents/skills`、`SKILL.md`；`/skill:name`；`/reload` | Pi packages（`pi install npm:/git:/local`）可分发技能；属第一方扩展机制，不是第三方必需项 | [S36][S41][S44] |
| MCP | `builtin:mcp` 默认启用，读 `mcp.json`（stdio + streamable HTTP + OAuth），`pi mcp` CLI、`/mcp` | `pi.registerMcpServer()` 可在扩展内**按会话**注册同名形状服务器，**注册不持久化，每次加载需重新注册**；`mcp.json` 同名优先 | [S37][S43][S44] |
| MCP 替换 | 官方明确「An installed extension that registers `/mcp`, such as `pi-mcp-adapter`, replaces the built-in MCP support」：此时 Pi **不再读 `mcp.json`** | `pi-mcp-adapter` 是第三方：`nicobailon/pi-mcp-adapter`，npm `pi-mcp-adapter@7.0.1`，作者 Nico Bailon，MIT，含 `pi` manifest 与 `pi-package` 关键字；**不是 earendil-works/badlogic 官方包，也不是启用 MCP 的前置条件** | [S37][S50][S51] |
| 其他客户端配置 | **不原生读取** `.mcp.json` / `opencode.json` MCP 配置；官方给「Migrate configuration from another client」转换表（Claude Desktop/Code/Cursor 直接拷 `mcpServers`；OpenCode 需 `type:"local"`→stdio、`command` 数组拆 `command`+`args`、`environment`→`env`、`{env:NAME}`→`${NAME}`） | 转换由人/脚本完成，Pi 不代做 | [S37] |
| 权限/沙箱 | 无内建权限系统；project trust 只控制项目资源加载，不沙箱工具调用 | 官方建议容器/沙箱（Gondolin 扩展 / Docker / OpenShell）或扩展实现权限门 | [S34][S40] |
| 版本门槛 | Skills ≥0.19.0；`SKILL.md` 目录约定 ≥0.20.0（破坏性）；MCP ≥0.99.0 | 更旧版本（含 npm `legacy-node20: 0.74.2`）**不能假设**有原生 MCP | [S44][S47] |

- `[文档声明]` **project trust 是官方硬门槛**：`.pi/settings.json`、`.pi/mcp.json`、`.pi/extensions|skills|prompts|themes`、`.pi/SYSTEM.md`、`.pi/APPEND_SYSTEM.md`、项目 `.agents/skills` 出现即需信任决定；裸 `.pi` 目录不需要；print/JSON/RPC 无提示时 `defaultProjectTrust: "always"` 才加载，`"ask"`/`"never"` 跳过；可用 `--approve` / `--no-approve` 单次覆盖；已保存决定在 `~/.pi/agent/trust.json`，`/trust` 可保存；`defaultProjectTrust` **只能写在 agent-directory settings**；信任前仍会读项目 `sessionDir` 与不受信任控制的 context files。[S40][S39]
- `[文档声明]` Pi package 治理：个人安装写 `~/.pi/agent/settings.json`，`--local/-l` 写 `.pi/settings.json`（仅 trust 后读）；`pi install npm:…@1.0.0` / `git:…@v1` / `./local`；`pi list`、`pi remove <source>`（`pi uninstall` 为其别名）、`pi update --extensions`；本地路径不复制；失败包会跳过并在下次启动/`/reload` 重试；项目包要审阅后再授予信任。[S41][S42]
- `[文档声明]` 官方已知配置脆弱点（CHANGELOG 修复记录）：`mcp.json` 以 UTF-8 BOM 开头会导致整份解析失败、跳过全部服务器并使 `pi mcp add`/`remove` 失败；另有一条 `pi install`/`pi remove` 在 agent 目录经符号链接时把嵌套条目写进 npm lockfile 的修复。[S44]

### 7.4 pi 的「实际成功判据」（官方）

- `[文档声明]` `pi mcp list`：连接所有 enabled server 并打印 state/tools/errors；退出码 1 = 有非法条目或 enabled server 未连接（可作脚本判据）；`/mcp` 显示状态、工具数、exposure、配置来源；`pi mcp list --json` 另有 `resources` 布尔字段。[S37][S42][S44]
- `[文档声明]` 技能：从可发现位置启动后看 startup diagnostics 与 `/skill:name`；改完 `/reload`。[S36][S38]
- `[文档声明]` 配置：`/settings`、`pi config`（列内置扩展，Tab 切 scope）、`/trust`、`/mcp`；手动改 settings/keybindings/instructions/resources 后 `/reload`。[S38][S39][S41]

---

## 8. 部署时保护现有配置：官方机制 / 官方限制 / 实际成功判据

> 仅复述第一方事实，**不设计安装器、不选写入方式**。「幂等/卸载」的结论见 §8.4。

### 8.1 已被官方文档证明的「隔离/不覆盖」机制

| 客户端 | 官方机制（事实） | 证据 |
| --- | --- | --- |
| Claude Code | settings 5 级优先级（managed > CLI `--settings` > project local > shared project > user），**list 键合并而非覆盖**；`--settings` 仅当次会话、不写文件；`.claude/settings.local.json` 由 Claude Code 自动加全局 git exclude，个人覆盖不进提交；`CLAUDE_CONFIG_DIR` 可整体搬走 `~/.claude` | [S3] |
| Claude Code | MCP `local` scope 落在 `~/.claude.json` 的当前项目条目，与 project `.mcp.json`、user 顶层互不覆盖；`disabledMcpServers` / `enabledMcpServers` 按项目在 `~/.claude.json` 记录开关而不删配置；`claude mcp reset-project-choices` 只重置审批 | [S2] |
| Claude Code | `managed-mcp.json` 独占控制、`managedMcpServers` 下发、`allowedMcpServers`/`deniedMcpServers` 白/黑名单；`--strict-mcp-config` 只加载 `--mcp-config` 传入的服务器 | [S4] |
| OpenCode v1 | 配置文件**合并而非替换**，非冲突键保留；`OPENCODE_CONFIG`（额外文件）、`OPENCODE_CONFIG_DIR`（额外目录）、`OPENCODE_CONFIG_CONTENT`（内联）提供不改写既有文件的覆盖层；`enabled:false` 保留服务器配置但停用 | [S13][S12] |
| OpenCode v2 | `disabled:true` 保留配置不连接；`policies` 可 block MCP/skill/plugin；系统 managed 目录与 MDM 优先级最高；非冲突设置保留 | [S16][S17] |
| pi | `PI_CODING_AGENT_DIR` 整体改 agent 目录（默认 `~/.pi/agent`）；project override-only 条目只覆盖 `enabled`/`exposure`/`toolExposure` 且**保留** `env`/`headers`/`auth`；`/mcp` 的状态/暴露变更「without replacing unrelated content」写入定义该服务器的文件；`enabled:false` 保留条目不连接 | [S49][S37] |
| pi | 用户级与项目级分离；项目 `.pi/*` 需 project trust 才加载；`--approve`/`--no-approve` 单次决定；personal 与 project 包声明分写 `~/.pi/agent/settings.json` 与 `.pi/settings.json` | [S38][S40][S41] |

### 8.2 官方限制（会破坏「不碰既有配置」的假设）

- `[文档声明]` Claude Code：`~/.claude.json` 是 Claude Code 自管文件（官方口径「you don't need to edit it」）；`claude mcp add` 同名同 scope 直接报错；project `.mcp.json` 需审批且未 trust 文件夹会忽略仓库内提交的自动批准键；`claude mcp remove` 删本地 OAuth 但**不吊销**授权服务器 token；`headersHelper` 受 trust 与凭据剥离规则约束。[S2][S3][S4]
- `[文档声明]` Claude Code：Windows 上 `~/.claude` = `%USERPROFILE%\.claude`，且 `.claude/settings.local.json` 不按仓库根定位；project `env` 不能设置若干目录类变量。[S3][S8]
- `[文档声明]` OpenCode：v1 与 v2 的 MCP JSON 形态、`enabled`/`disabled`、OAuth 字段大小写、skills 权限对象/数组全不兼容；v2 同名 server 对象是**整体替换**；v2 官方明说单靠 settings 无法阻止用户新增 MCP/skill/plugin，须用 policies；v1 的 managed 路径与 v2 的系统目录需管理员/root 写权限。[S12][S16][S17]
- `[文档声明]` OpenCode：`update:"auto"` 安装更新**不会自动重启**正在运行的 server，须手动重启才生效。[S16]
- `[文档声明]` pi：`builtin:mcp` 可被 `pi-mcp-adapter` 类扩展整体替换，替换后 Pi 不读 `mcp.json`；`pi.registerMcpServer()` 注册不持久化；`sse`/legacy SSE 不支持；项目资源受 trust 门禁；无内建权限/沙箱；`mcp.json` 带 BOM 在受影响版本会整体失效。[S37][S43][S40][S44]
- `[文档声明]` 三者共同：官方都建议密钥走环境变量/凭据文件而非共享配置，但实现不同——Claude Code 对远端 `url`/`headers` 的凭据类变量**强制读空**；OpenCode 用 `{env:NAME}` / `{file:path}`（缺值替换为空）；pi 用 `${VAR}` / 整值 `!command`。[S2][S21][S37]

### 8.3 官方给出的「实际成功判据」（可直接作为验收观测项，非本文设计）

- Claude Code：`claude mcp add` 的 `Added ...`；`claude mcp list` 的 `✔ Connected`；`claude mcp get <name>`；`/mcp` 工具数/状态；`/status` 的 `Setting sources`；`claude doctor`；`/skills`；`/reload-skills`；`/reload-plugins`。[S1][S2][S3]
- OpenCode v1：`opencode mcp list` / `ls`（连接状态）、`opencode mcp auth list`、`opencode mcp debug <name>`、`opencode debug config`（解析后配置）、v1 技能 `skill` 工具的 `<available_skills>` 与 `skill({name})`。[S12][S14][S11]
- OpenCode v2：`opencode mcp list`（示例 `✓ context7  connected`）、`/mcps`、`opencode mcp auth <name>`、`opencode debug config`、技能 `skill` 工具 `{"id":"..."}` 与 `@skill-id`。[S16][S17][S18]
- pi：`pi mcp list`（连所有 enabled server；退出码 1 = 非法/未连接）、`pi mcp list --json`、`/mcp`、startup diagnostics + `/skill:name`、`/reload`、`pi config`、`/trust`。[S37][S42][S36][S41]

### 8.4 幂等性与卸载：**未证明，记为未知**

- `[文档声明]` 已找到的**逐项**移除/回滚命令：`claude mcp remove <name>` / `claude mcp reset-project-choices` / 删除技能目录 / `/plugin uninstall`；`opencode mcp logout [name]`（清 OAuth 凭据）；`pi mcp remove <server>`（**保留**已存 OAuth 凭据，与 Claude Code 相反）、`pi mcp logout <server>`、`pi remove <source>` / `pi uninstall <source>`（别名）、`pi config` 禁用内置扩展。[S1][S2][S14][S42][S41]
- `[文档声明]` 与幂等相关的**唯一**明确措辞：`pi mcp add` 官方定义为「**Add or replace** a … server in `mcp.json`」；Claude Code 同名同 scope 再 `claude mcp add` **失败**。[S42][S2]
- `[未知]` **三者均未找到第一方文档声明「一次部署整体是幂等的」（重复执行结果完全一致、无重复条目/无重复副作用）**，也未找到「一键卸载/回滚整次部署并恢复原有全部配置」的官方命令或流程。本次检索覆盖：三家的 skills/mcp/settings/config/cli/managed/packages/security 文档、固定 SHA 的相关源码与 CHANGELOG 关键条目，以及 `idempotent` / `uninstall` 定向检索。故 **幂等性与完整卸载能力记为未知，不得在部署契约里当作已承诺行为**。

---

## 9. 对后续决策的约束与选项（**不做选择**）

### 9.1 事实约束（写契约时必须计入，不是建议）

- **C1 版本/形态分歧**：OpenCode 官方同日并行 v1（`opencode-ai@1.19.5`，`mcp.<name>`/`enabled`/`oauth.clientId`）与 v2（`@opencode/cli@2.2.5`，`mcp.servers`/`disabled`/`oauth.client_id`），且 skills 的 frontmatter 必需性、权限对象/数组、ID 规则都不同。任何「精确 JSON 形态」的契约都必须先绑定目标大版本。[S11][S12][S16][S17][S18][S26][S27]
- **C2 最低版本门槛**：pi 原生 Skills ≥0.19.0、`SKILL.md` 目录约定 ≥0.20.0（破坏性）、原生 MCP ≥0.99.0；`legacy-node20@0.74.2` 不具备原生 MCP。Claude Code 文档大量能力带 v2.1.x 门槛。[S44][S47][S1][S2]
- **C3 信任/审批门禁**：Claude Code project `.mcp.json` 需交互审批 + workspace trust（`-p`/SDK/cloud 无提示直接加载）；pi 项目 `.pi/*` 需 project trust（print/JSON/RPC 由 `defaultProjectTrust` 或 `--approve` 决定）；OpenCode 未在查证文档中见等价门禁。[S2][S40]
- **C4 原生/第三方边界**：pi 的 MCP 是**官方内置扩展** `builtin:mcp`（默认启用，读 `mcp.json`），`pi-mcp-adapter` 是**第三方可选替换**，启用 MCP 不依赖它；`pi.registerMcpServer()` 是会话级、不持久化。[S37][S43][S44][S50][S51]
- **C5 密钥不得进共享配置**：三家机制互不相同，且 Claude Code 对远端 `url`/`headers` 的凭据类变量强制读空。[S2][S21][S37][S4]
- **C6 协议面不统一**：Claude Code 有 v1/v2 runtime（v2 支持 MCP 2026-07-28）；OpenCode v2 `protocol` 可选 `legacy`/`auto`/`2026-07-28`；pi `@earendil-works/pi-mcp` 声明 `2025-11-25` 且不支持 legacy SSE。[S2][S20][S45]
- **C7 重载语义不对齐**：Claude Code settings/skills 有文档化热重载；pi 明确 `/reload`；OpenCode v2 技能热更新由源码证实但 v1/v2 的 MCP 配置运行时重载未知。[S3][S1][S22][S37][S13][S17]
- **C8 幂等/卸载未知**（§8.4）：不能把「可重复执行、可完整回退」当作既有能力。

### 9.2 可验证选项（并列列出，**本文不选择、不排序、不推荐**）

| 编号 | 待由人决定的维度 | 官方已存在的可验证选项 | 证据 |
| --- | --- | --- | --- |
| O1 | 目标客户端与版本 | Claude Code 2.1.318 / OpenCode v1 1.19.5 / OpenCode v2 2.2.5 / pi 1.5.0（或 `legacy-node20 0.74.2`） | [S7][S26][S27][S47] |
| O2 | 作用域 | Claude Code `local`/`project`/`user`/managed；OpenCode global/project/system-managed/remote `.well-known`；pi agent-dir(user)/`.pi`(project, trust-gated) | [S2][S13][S16][S38] |
| O3 | 配置写入方式 | 官方 CLI（`claude mcp add` / `opencode mcp add` / `pi mcp add`）vs 直接编辑 `.mcp.json`、`opencode.json(c)`、`mcp.json`、`settings.json`；两者的重载/审批语义不同 | [S2][S17][S37] |
| O4 | Skill 分发形态 | 目录 `SKILL.md`；Claude Code plugin（`skills/` + `.mcp.json`）；OpenCode v2 `skills` 数组本地目录/HTTP catalog、v1 `permission.skill`；pi packages（`pi install`，`pi.skills` 清单） | [S9][S18][S11][S41] |
| O5 | pi 的 MCP 路径 | ① 内置 `builtin:mcp` + `mcp.json`（默认、持久化）② `pi.registerMcpServer()` 扩展注册（会话级）③ 第三方 `pi-mcp-adapter` 替换（替换后不读 `mcp.json`）④ `--no-mcp`/`-builtin:mcp` 禁用 | [S37][S43][S39][S50] |
| O6 | 保护既有配置 | Claude Code `--settings` 会话级 / `CLAUDE_CONFIG_DIR` / `disabledMcpServers` 保留条目；OpenCode `OPENCODE_CONFIG`/`_DIR`/`_CONTENT`、v1 `enabled:false`、v2 `disabled:true`、v2 `policies`；pi `PI_CODING_AGENT_DIR`、project override-only 条目、`enabled:false` | [S3][S2][S13][S16][S49][S37] |
| O7 | 验收观测 | `claude mcp list`+`/mcp`+`/skills`+`/status`；`opencode mcp list`+`debug config`+`skill` 工具；`pi mcp list`(exit 1)+`/mcp`+`/reload`+startup diagnostics | [S1][S2][S14][S16][S17][S37][S42] |
| O8 | 更新/卸载是否纳入承诺 | 官方只提供逐项 remove/logout/uninstall 与部分 add 的替换语义；整体幂等/回滚无第一方证明 → 只能作为「未知」处理或由人另行要求证据 | [S2][S14][S42][S41] |

---

## 10. 未确定事项（明确列为未知，不填补）

1. **完整部署幂等性 / 整体卸载或回滚**：三家均无第一方证明（§8.4）。
2. **Claude Code**：手工编辑 `.mcp.json` / `~/.claude.json` 后运行中会话是否自动重建 MCP 连接；`claude mcp add` 在无人值守且仓库未 trust 时的确切交互结果（仅知 `-p`/SDK/cloud 会跳过 project 审批提示）。
3. **OpenCode**：v1 与 v2 的 `opencode.json` / `mcp` 配置改动后是否热重载、是否必须重启；`opencode mcp add` 同名重复行为；文档提交 ↔ npm 版本映射；是否存在与 Claude Code/pi 等价的项目信任门禁。
4. **pi**：`~/.claude/skills`、`~/.codex/skills` 在 1.5.0 是否仍全部加载——0.19.0 CHANGELOG 明确列出，1.5.0 `skills.md` 只明确 `~/.agents/skills` / `.agents/skills`，源码 `skills.ts` 的默认路径只有 `<agent-dir>/skills` 与 `.pi/skills`；三者一致性未从源码完全对齐，标 `[文档声明]` + `[未知]`。[S44][S36][S46]
5. **Claude Code 源码级验证**：公开仓不含顶层 `src/` 实现目录，CLI 运行时行为仅由官方文档声明，未做源码/运行时复核。[S10]
6. **平台细节**：本机为 Windows；已查到 Claude Code 的 `%USERPROFILE%\.claude` 与 managed MCP 路径、OpenCode 的 `%ProgramData%\opencode`、pi 的 PowerShell 安装命令，但**三家在 Windows 上对 `~` 展开、符号链接、路径大小写、stdio 进程组终止的具体差异**未逐项验证（Claude Code 明确给出 Windows stdio 停止方式：先关 stdin，300ms 后结束进程树）。[S3][S4][S13][S34][S2]
7. **许可证/分发**：Claude Code npm `license = "SEE LICENSE IN README.md"`（非 MIT），OpenCode/pi 为 MIT；本票未展开许可证条款，留待[哪些源码、依赖与产物可以纳入和分发](../issues/05-distribution-boundary.md)处理。[S7][S24][S31]
8. **未验证**：未安装任何客户端、未运行任何命令、未做真实连接/技能加载/热重载实验；所有能力判断为文档与固定 SHA 源码层面的证据。

---

## 11. 可点击第一方引用

> 编号在正文中以 `[Snn]` 引用。全部为第一方（官方文档站、官方仓固定 SHA 源码/文档、官方仓 API、官方 npm registry）。

**Claude Code**
- [S1] https://code.claude.com/docs/en/skills （Markdown 版 https://code.claude.com/docs/en/skills.md ）
- [S2] https://code.claude.com/docs/en/mcp （ https://code.claude.com/docs/en/mcp.md ）
- [S3] https://code.claude.com/docs/en/settings
- [S4] https://code.claude.com/docs/en/managed-mcp
- [S5] https://api.github.com/repos/anthropics/claude-code/branches/main
- [S6] https://api.github.com/repos/anthropics/claude-code
- [S7] https://registry.npmjs.org/@anthropic-ai%2Fclaude-code/latest
- [S8] https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- [S9] https://github.com/anthropics/claude-code/blob/main/plugins/README.md
- [S10] https://api.github.com/repos/anthropics/claude-code/contents/

**OpenCode**
- [S11] https://opencode.ai/docs/skills/
- [S12] https://opencode.ai/docs/mcp-servers/
- [S13] https://opencode.ai/docs/config/
- [S14] https://opencode.ai/docs/cli/
- [S15] https://opencode.ai/v2/docs/
- [S16] https://opencode.ai/v2/docs/config/
- [S17] https://opencode.ai/v2/docs/mcp-servers/
- [S18] https://opencode.ai/v2/docs/skills/
- [S19] https://raw.githubusercontent.com/anomalyco/opencode/6bd47192ac97527e9fdc5e64c36fd4730aec2acd/services/www/src/docs/content/mcp-servers.mdx
- [S20] https://raw.githubusercontent.com/anomalyco/opencode/6bd47192ac97527e9fdc5e64c36fd4730aec2acd/packages/schema/src/mcp.ts
- [S21] https://raw.githubusercontent.com/anomalyco/opencode/6bd47192ac97527e9fdc5e64c36fd4730aec2acd/packages/core/src/config/variable.ts
- [S22] https://raw.githubusercontent.com/anomalyco/opencode/6bd47192ac97527e9fdc5e64c36fd4730aec2acd/packages/core/src/config/plugin/skill.ts
- [S23] https://api.github.com/repos/anomalyco/opencode/branches/dev
- [S24] https://api.github.com/repos/anomalyco/opencode
- [S25] https://api.github.com/repos/sst/opencode
- [S26] https://registry.npmjs.org/opencode-ai/latest
- [S27] https://registry.npmjs.org/@opencode%2Fcli/latest

**pi**
- [S29] https://github.com/badlogic/pi-mono （重定向到 https://github.com/earendil-works/pi ）
- [S30] https://api.github.com/repos/badlogic/pi-mono
- [S31] https://api.github.com/repos/earendil-works/pi
- [S32] https://api.github.com/repos/earendil-works/pi/branches/main
- [S33] https://api.github.com/repos/badlogic/pi-mono/contents/packages/coding-agent
- [S34] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/README.md
- [S35] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/package.json
- [S36] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/skills.md
- [S37] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/mcp.md
- [S38] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/configuration.md
- [S39] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/settings.md
- [S40] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/security.md
- [S41] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/packages.md
- [S42] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/cli.md
- [S43] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/extensions.md
- [S44] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/CHANGELOG.md
- [S45] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/mcp/README.md
- [S46] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/src/core/skills.ts
- [S47] https://registry.npmjs.org/@earendil-works%2Fpi-coding-agent
- [S48] https://pi.dev/docs/latest
- [S49] https://raw.githubusercontent.com/earendil-works/pi/55a5c6914570e2ae31ca36297654483bbbf46883/packages/coding-agent/docs/environment-variables.md
- [S50] https://registry.npmjs.org/pi-mcp-adapter/latest （第三方包元数据，仅用于界定边界）
- [S51] https://github.com/nicobailon/pi-mcp-adapter （第三方项目，仅用于界定边界）

**Context7 索引（非第一方事实终点，仅记录检索路径）**：resolve 得 `/anthropics/claude-code`、`/anomalyco/opencode`、`/earendil-works/pi`；query 主题为 skills / MCP config / identity / packages / extensions / native MCP。索引中出现的 `/malhashemi/opencode-skills`、`/dicklesworthstone/pi_agent_rust`、`/sky-valley/pi`、`/websites/pi_dev`、`/isamu/claude`、`/pjbrito/claude-code-docs` 未作为本研究证据。
