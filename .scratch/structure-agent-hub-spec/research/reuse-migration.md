# 参考 Hub 与五个现有 MCP 带来哪些复用和迁移约束

> **研究稿，不是 SPEC。** 对应票 [参考 Hub 与五个现有 MCP 带来哪些复用和迁移约束](../issues/02-reuse-migration-evidence.md)。
> 本文只呈现**来源事实**与**未确定事项**，不含任何方案拍板、推荐或结论性取舍。许可证部分只做文本证据，不构成法律意见。

- 检索日期：**2026-11-05**（所有外部事实在该日一次性抓取；引用 URL 见 §7）
- 固定参考仓库 SHA：`56705e07ce6e99f0d5a0d0c7b5e28b6b2c0bc973`（`Cai-aa/CAE-Agent-Hub`，commit 日期 2026-10-27T12:55:57Z；抓取时 `main` 仍等于该 SHA）
- 本仓库基线：`main` @ `b37a3e536b3c204a3747381585f3570e0c075dbe`，跟踪文件仅 `README.md`、`LICENSE`(GPL-3.0)、`.gitignore`、`docs/agents/issue-tracker.md` 与 `.scratch/structure-agent-hub-spec/**`；`MCP/`、`Skill/`、`scripts/` 与 `docs/` 其余部分为空骨架

---

## 1. 问题

固定参考仓库 SHA 后，哪些组织、Skill/注册/发布模式确实存在；五个独立工程的运行时、桥接、外部引用、路径、已有 Skill/客户端配置与许可证证据，给源码纳入/迁移和目录设计带来什么约束？只交事实与选项，不替用户决定合仓/移动/索引或许可证。

## 2. 取证范围与方法

- **第一方来源优先**：参考 Hub 用 GitHub REST + `raw.githubusercontent.com` 在固定 SHA 上读取（tree、README、LICENSE、代表性 Skill/MCP 文件、脚本、CI、tags/releases）；本地五仓为只读文件取证（README、`Directory.Build.props`/`.targets`、`*.csproj`、`*.slnx`、`global.json`、`docs/mcp-loading.md`、`docs/skills/**`、in-tree 客户端配置）与只读 git 查询（`rev-parse`/`log`/`status`/`ls-files`/`remote`）。
- **客户端/SDK 文档**：先 Context7 `resolve_library_id` + `query_docs`，再逐一核对第一方官方源（见 §3.3、§3.4）。
- **明确未做**：未构建/测试/格式化；未启动或安装任何商业软件；未修改任何仓库、票、地图、源码、用户配置或 git identity；未递归扫描父目录；未复制任何 DLL 或文件；未开 PR/分支/commit。
- **取证偏差（如实记录）**：一次正则扫描越界命中了每仓 `AGENTS.md`/`CLAUDE.md`。它们不是本报告的证据来源；路径与登记事实以 README、工程清单及 `mcp-loading.md` 为准，不采用其中的 agent 指令。

## 3. 主要发现

### 3.1 参考 Hub（固定 SHA `56705e0`）

- 整树 3115 项（2649 blob，未截断）。顶层：`MCP/`(2452 项)、`Skill/`(337)、`assets/`(166)、`models/`(93)、`viewer/`(46)、`Subagent/`(3)、`cfd_agent/`(5)、`docs/`(3)、`scripts/`(2)、`.github/`(4)。
- **根目录只有 4 个文件**：`.gitignore`、`LICENSE`、`README.md`、`README.zh-CN.md` → **不存在根一键安装器/根配置**。
- **MCP 生态是 Python**：`MCP/` 下 589 个 `.py`、**0 个 `.cs`**。逐适配器自包含（各自 README、`pyproject.toml`/`requirements.txt`、example 配置）；仅少数带安装/注册脚本，例如 `MCP/ANSA/install_ansa_bridge.ps1`、`MCP/ANSA/register_codex_mcp.ps1`、`MCP/FEP-Agent-Hub/scripts/install.ps1`、`MCP/FEP-Agent-Hub/scripts/register-codex.ps1`。无仓库级安装器。
- **Skill 组织模式**（`Skill/`）：337 项，含 59 个 `SKILL.md`、27 个 `metadata.json`；部分目录另有 `references/`、assets、`UPSTREAM*.md`，不能推断每个 Skill 都有这些文件。README 明确写入模式：把完整 Skill 目录拷进 agent 的 skill 目录，并给出 Codex(`$env:USERPROFILE\.codex\skills`) 示例；`Skill/abaqus/README.md` 另列 Claude Code(`.claude\skills`)、Claude Desktop(仅 MCP 配置)、Cursor 的用法。Skill 是指令目录，不是求解器二进制。
- **逐适配器独立注册、无统一格式**：`MCP/Abaqus/examples/mcp_config.example.json`、`MCP/Adams/client-config.example.json` 用 `mcpServers` JSON；`MCP/ANSA/examples/codex_config.example.toml` 用 `[mcp_servers.ansa]` TOML；`register_codex_mcp.ps1` 直接改写 `~/.codex/config.toml`（或 `$CODEX_HOME`）。即**同一仓库内已并存多种客户端配置形状**。
- **许可证并不单一**：根 `LICENSE` = MIT（`Copyright (c) 2026 Thompson Labs`）；但树内另有逐组件 `LICENSE`（`MCP/Abaqus`、`MCP/Abaqus（2020）`、`MCP/Adams`、`MCP/FEP-Agent-Hub`、`MCP/Ansys/PyAnsys/*`、`MCP/CST/vendor/cst-runtime-cli`）与 27 个 `UPSTREAM.md` / 若干 `UPSTREAM_LICENSE`。抽样 `metadata.json`：Abaqus 系列 `"license":"NOASSERTION"`、`"license_class":"restricted"`、`"distribution":"restricted"`（来源 `github.com/JaimeCernuda/abaqus-scripting`），CST 系列 `"distribution":"internal"`、`"source":"local"`；`abaqus-static-analysis/UPSTREAM_LICENSE` 为 MIT（`Copyright (c) 2024 majiayu000`）。`Skill/abaqus/README.md` 自述："这些是第三方公开 Skill；再分发修改版或商业打包前，请核对上游仓库与许可条款。"
- **CI 是逐适配器、按路径过滤**：`.github/workflows/adams-check.yml`、`fep-agent-hub-test.yml`（`paths:` 限定 `MCP/<X>/**`、`Skill/<X>/**`），无仓库级流水线。
- **发布**：存在 tag/release `v1.0.0`、`v1.0.1`、`v1.0.2`。
- **OpenSees / pi / OpenCode 的取证边界**：整树路径对 `opensees`、`pi/`、`opencode` 的匹配数均为 0，所查 README 与代表性脚本也未给出相应接入；本次未穷读全部文件正文，不能据此穷尽性断言整个仓库没有任何相关内容，更不能把这些支持当作已提供。
- `Subagent/` 仅 2 文件（README + `hypermesh-meshing.md`）；`docs/` 仅 `simulation-atlas.md`、`simulation-showcase.md`。

### 3.2 五个本地工程（只读事实）

共同点：各自是**独立 `.git` 仓库**，分支 `master`，远端均为 `https://gitee.com/punkwen/tgk-<name>.git`；语言 C#/.NET；stdio MCP 宿主均用 `ModelContextProtocol.Core`；分层 `Contracts`/`Core`/`Mcp`(+`tests`)；`.slnx` 解决方案 + `Directory.Build.props`(+`.targets`) 用 `$(MSBuildThisFileDirectory)` 共享。

| 仓库 | TFM / 平台 | MCP 宿主依赖 | 桥接 / 运行时 | 本机/厂商二进制（**已被 git 跟踪**） | LICENSE 文件 | HEAD（分支 master） | 工作区状态 |
|---|---|---|---|---|---|---|---|
| `tgk-midas-mcp` | `net8.0`（TFM 非 Windows 限定；完整工作流平台未实测） | `ModelContextProtocol.Core` 1.2.0 | HTTP `http://localhost:10084` + `MAPI-Key` 头；不启动 MIDAS | 无 | 无 | `e5f129d`（2026-08-10） | 干净 |
| `tgk-rhino-mcp` | `net8.0-windows` x64 | 1.2.0 | 双件：外部 exe + Rhino 内 `.rhp` 插件，named pipe `tgk-rhino-mcp-{user}` | `lib/RhinoCommon.dll`（3.6 MB；`Private=false`） | 无 | `b9d95bd`（2026-08-11） | 干净 |
| `tgk-sap2000-mcp` | `net8.0-windows` x64 | 1.4.1 | SAP2000 OAPI/COM，单线程串行 | `lib/SAP2000v1.dll`（`Private=true`） | 无 | `18a7996`（2026-08-28） | **脏**：`.zcode/config.json` 被删（工作区 ` D`） |
| `tgk-yjk-modeling-mcp` | `net48` x64（Windows-only） | 1.2.0 | 直接引用 YJK SDK 生成 `.ydb`；不启动 YJK | `lib/yjks/**` 28 文件（27 DLL + `YJK_SSCS.YDB`）、`lib/yjks_8.1/**` 28 文件（27 DLL + `YJK_SSCS.YDB`）、`lib/yjks_8.1_depend/**` 5 文件（3 DLL + 2 txt） | 无 | `b5507bb`（2026-08-13） | **脏**：34 个已跟踪文件被修改，其中 `lib/` 内 25 个（24 DLL + `YJK_SSCS.YDB`），其余 9 个为 `Directory.Build.props`、`README.md`、`README.en.md`、`docs/dev.md`、`docs/mcp-loading.md`、`opencode.json`、`script/build-debug.bat`、`script/build-release.bat`、`src/Tgk.Yjk.Modeling.Core/Tgk.Yjk.Modeling.Core.csproj` |
| `tgk-etabs-mcp` | `net8.0-windows` x64 | 1.2.0 | ETABS OAPI/COM，专用 STA 线程；需 ETABS v22+ | `lib/ETABSv1.dll` | 无 | `ab3c6b2`（2026-08-10） | 干净 |

补充事实：

- `sap2000`/`etabs`/`yjk` 均有 `Directory.Build.targets`，用 `$(MSBuildThisFileDirectory)lib\` 通配把 `lib/**` 复制到输出目录；`midas` **无 `lib/`**，无此目标。
- `sap2000` 内含一个实验子项目 `sap-temp-workdir/reflect-mcp`（`reflect-mcp.csproj` 用 `ModelContextProtocol.AspNetCore` 1.4.1 + `FrameworkReference Microsoft.AspNetCore.App`），其 `Program.cs` 第 3 行硬编码 `I:\DotNetProgram\Nuget\Packages`。
- `yjk` Core 另引 `Microsoft.VisualBasic`(TextFieldParser) 与 NuGet `Microsoft.Data.Sqlite` 8.0.0；其 `.scratch/from-csv-batch-import` 记录了 net472 依赖与许可讨论（CsvHelper 双许可 MS-PL/Apache-2.0 被"最小依赖"约束否决）。
- `global.json` 仅 `midas`/`sap2000`/`etabs` 有，固定 SDK `9.0.201`（`rollForward: latestFeature`）；`rhino`/`yjk` 无该文件。
- **外部引用（Junction 目标）**：对 `TigerkinProgram` 及父目录 Junction 邻居名（`tgk-3d3s`/`tgk-core`/`tgk-csi`/`tgk-geometry`/`tgk-mesh`/`tgk-rhino3dm`/`tgk-seismic`/`tgk-slab-comfort-core`/`tgk-yjk-core`）做全仓文本搜索（含被 gitignore 的文件，排除 `.git/`），**零命中**。源码/工程文件也未引用同名目录。→ 就文本证据而言，**没有**这五个工程依赖父目录 Junction 目标的迹象；工程内部只用 `..\` 相对引用与 `lib/` 本地 DLL。
- **硬编码机器路径**：README、`docs/mcp-loading.md`、in-tree 客户端配置中存在盘根绝对路径（如 `G:\DotNetProgram\<repo>`、`I:\DotNetProgram\<repo>`）。本轮 C# 源码扫描匹配到 `sap-temp-workdir/reflect-mcp/Program.cs` 的 `I:\DotNetProgram\Nuget\Packages`；不把有限匹配提升为对所有运行/构建路径的穷尽证明。
- **已有 Skill**：`midas`/`sap2000`/`etabs`/`yjk` 各有一枚 operator 型 Skill 于 `docs/skills/<tool>-…/SKILL.md`（+`references/`：`mcp-loading.md`、`*_spec.json`、`workflows.md`）；`yjk` 另有 `.trae/skills/yjk-modeling-foundation-api/SKILL.md`；`rhino` 的指定 `docs/skills/**` 路径未发现 Skill，不据此断言树外或其他目录没有技能。这些已查 Skill 的定位是如何操作该 MCP，与参考 Hub 的领域/工作流型 Skill（如 `abaqus-static-analysis` 的 8 步流程 + 验收检查点）不同。
- **已有客户端配置（in-tree，只记形状，不含任何凭据值）**：
  - `rhino`：`docs/examples/claw-settings.rhino-modeling.json` → `{"mcpServers":{"rhino-modeling":{command,args,env,toolCallTimeoutMs}}}`；`docs/mcp-loading.md` 列 tigerkin-claw 读取 `%USERPROFILE%\.tigerkinclaw\settings.json`、`<workspace>\.claw\settings.json`、`<workspace>\.claw\settings.local.json`、以及 `%USERPROFILE%\.tigerkinclaw\mcps\<workspace-id>\settings.json`。
  - `yjk`：`opencode.json` → `{"mcp":{"tgk-yjk-modeling":{"type":"local","command":[...],"enabled":true}}}`（`$schema: opencode.ai/config.json`）；`.claude/settings.local.json` 仅 `permissions`，**不含 MCP**。
  - `sap2000`：`.zcode/config.json`（**被跟踪**，内容为 `{"mcp":{"servers":{}}}`）；`tgk-sap2000-mcp.code-workspace`。
  - `etabs`：`.zcode/plans/*.md`（仅计划文件）；`docs/skills/etabs-mcp-operator/references/mcp-loading.md` 同时给 ZCode(`.zcode/config.json` 的 `mcp.servers`) 与 tigerkin-claw(`mcpServers`) 两种形状。
  - `midas`：无 in-tree 客户端配置；`docs/mcp-loading.md` 给 ZCode/Claude Code 形状 `{"mcp":{"servers":{name:{type,command,args,cwd,timeoutMs}}}}`。
  - 参考 Hub 与本地工程的客户端配置形状各异：ZCode `mcp.servers{type,command,args,cwd,timeoutMs}`；tigerkin-claw `mcpServers{command,args,env,toolCallTimeoutMs}`；opencode `mcp{name:{type:"local",command:[...],enabled}}`；Codex `mcp_servers.<name>`(TOML)。
- 凭据机制（只记机制与变量名，不含任何值）：`midas` 的 `MAPI-Key` 由用户从 MIDAS GUI 取得、经 `open_session`/`check_midas_environment` 的 `session_options` 传入并作为 HTTP 头，缺失时返回 `MAPI_KEY_REQUIRED`；参考 Hub 的 `MCP/ANSA` 用 `LOCALAPPDATA` 下的 `bridge.json` 携带 64 位十六进制 bearer token，并由 `register_codex_mcp.ps1` 校验、`examples/codex_config.example.toml` 仅以环境变量名引用（`ANSA_MCP_BRIDGE_CONFIG`）。两处均未在本票证据中出现实际值。

### 3.3 MCP C# SDK（Context7 → 第一方核对）

- Context7 `resolve` → `/modelcontextprotocol/csharp-sdk`（Source Reputation: High，1349 snippets）。`query` 返回 getting-started 内容。
- **第一方核对**（`github.com/modelcontextprotocol/csharp-sdk`，`docs/concepts/getting-started.md`）：三个包定位——`ModelContextProtocol.Core`＝只要 client 或**低层 server** API、依赖最少；`ModelContextProtocol`＝hosting/DI/stdio 服务（多数项目起点）；`ModelContextProtocol.AspNetCore`＝HTTP 服务。
- 与本地的对应：五仓均用 **`ModelContextProtocol.Core`**（低层）并手写 `StdioServerTransport` + 反射式工具注册——与 Core 的"低层 server API"定位一致，**未见冲突**。
- 事实：SDK 版本**混用**（`1.2.0` vs `1.4.1`）；`ModelContextProtocol.AspNetCore` 仅出现在 `sap2000` 的实验子项目。

### 3.4 客户端文档核对（Context7 → 第一方；**仅作旁证**，完整客户端能力属票 [三类 Agent 实际支持哪些 Skill 与 MCP 接入方式](../issues/03-agent-integration-evidence.md)）

- **Claude Code**：Context7 `/anthropics/claude-code` 返回 `.mcp.json` 示例与插件结构；核对第一方 `plugins/README.md` 确认 plugin 布局含 `skills/` 与 `.mcp.json`。细节以 `docs.claude.com` 为准。
- **Codex**：Context7 `/openai/codex` 返回 `codex-rs/config/src/mcp_types.rs`(`RawMcpServerConfig`: `command,args,env,env_vars,cwd,startup_timeout_sec,tool_timeout_sec,…`)；核对第一方 `learn.chatgpt.com` 配置参考确认 `mcp_servers.<id>.command/args/env/env_vars/cwd`。与本地 `mcp_servers.<name>` 用法一致。

## 4. 对后续决策的约束（事实约束，非取舍）

- **C1｜跨仓库历史**：五个工程是各自独立的 `.git`（不同 HEAD、不同脏状态），其中 `yjk` 工作区有 34 个已跟踪文件被修改（含 DLL）。任何"纳入源码"动作都同时面对**跨仓库历史**与**未提交状态**，不是单纯文件复制；方式选择（合并/子模块/子树/复制/索引）会改变可追溯性与可复现性。
- **C2｜厂商二进制已在版本控制内**：4/5 仓已把厂商 DLL 提交进 `lib/`（`RhinoCommon.dll`、`SAP2000v1.dll`、`ETABSv1.dll`、YJK 系列 `lib/yjks`+`lib/yjks_8.1`+`lib/yjks_8.1_depend` 共 57 个 DLL）；`midas` 无。集中到一个公开仓库会把它们一并带上，除非显式排除。
- **C3｜运行模型不统一**：`midas`＝HTTP+Key；`rhino`＝外部 exe + Rhino 内插件 + named pipe；`sap2000`/`etabs`＝COM + 本机 DLL + Windows x64；`yjk`＝`net48` + 原生 YJK SDK + 生成 `ydb`。**不存在单一 runtime 假设**。
- **C4｜已发现的路径耦合主要在文档/配置层**：绝对路径存在于 README/`mcp-loading.md`/in-tree 客户端配置；本轮另匹配到 `reflect-mcp/Program.cs` 一处源码路径。若部署产物或启动目录改变，旧绝对路径须重生成或修订，不能假定仍有效；保留独立引用时则需按实际位置判断。
- **C5｜无共享代码证据**：对父目录 Junction 目标零引用；各工程仅 `..\` 与 `lib/` 自包含。**"每个 MCP 自包含"有证据，"共享代码库"没有证据支撑**。
- **C6｜已查的两类 Skill 侧重点不同**：本地样本是 operator 型（怎么用该 MCP）；参考 Hub 样本包含领域/工作流型（如静态分析 8 步 + 验收）。参考 Hub 中 `SKILL.md` 与可选的 `metadata.json`、`references/`、`UPSTREAM*.md` 共置是已观察到的组织形态，不代表每个 Skill 都有同样附件或只能属于单一类别。
- **C7｜"参考 Hub 是 MIT"≠"其内含物都可自由再分发"**：根 MIT + 逐组件 LICENSE/UPSTREAM_LICENSE + `metadata.json` 标注 `NOASSERTION`/`restricted`/`internal`，其自述亦要求再分发前核对上游。每个纳入物需各自的许可证据。
- **C8｜五仓缺许可文本**：五个工程**没有** `LICENSE`/`COPYING`，README 也无许可声明（文本证据缺失）。是否补声明、选何种许可属权属问题。
- **C9｜三处许可文本并列，兼容性不在文本证据内**：本仓库 `LICENSE` 文本＝GPL-3.0；参考 Hub 根 `LICENSE` 文本＝MIT（`Copyright (c) 2026 Thompson Labs`）；五个本地工程无许可文本。文本之外的分发/兼容含义本票不判定，**不提供法律保证**。
- **C10｜客户端格式碎片化且已实际并存**：ZCode / tigerkin-claw / opencode / Claude Code / Codex 形状各异，本地工程已同时出现 claw、opencode、ZCode 三种。
- **C11｜SDK 版本混用**（1.2.0 / 1.4.1）与两处不同包选择（Core 用于本地服务、AspNetCore 仅一处实验）。
- **C12｜参考 Hub 尚不能被当作已完成的一键部署/OpenSees/pi/OpenCode 模板**：所查根目录没有统一安装器，路径、README 与代表性脚本未提供这些支持的证据；已观察到的模式是逐适配器 README + example config + 少数 register 脚本 + 按路径过滤 CI。此结论限于本次取证范围。
- **C13｜发布节奏差异**：参考 Hub 有 tag/release（v1.0.0–v1.0.2）；五个本地工程只见 HEAD，无 tag 证据。

## 5. 选项（只列事实约束下的可选路径，**不做选择**）

- **源码归属/目录层面**（受 C1–C5 约束；归属决策在票 [哪些源码、依赖与产物可以纳入和分发](../issues/05-distribution-boundary.md) 与 [仓库如何组织，Skill 与 MCP 如何分工](../issues/06-repository-skill-boundary.md)）：(a) 整合源码进单一仓库；(b) 保留独立仓库 + 索引/清单；(c) 外部引用（子模块/子树）；(d) 以上混合。四者的事实差异见 §4。
- **可借鉴的组织形态**（事实存在，**非推荐**）：`MCP/<Tool>/` 每适配器自包含 README + example config（+可选 register 脚本）；`Skill/<tool>/<stage>/<skill>/` 含 `SKILL.md`+`metadata.json`+`references/`+`UPSTREAM*.md`；`Subagent/`；逐适配器按路径过滤的 CI；"根许可 + 逐组件许可/上游归属"并存。
- **迁移方式（合仓/移动/索引/许可/历史保留）本身留 HITL**，本票不拍板。

## 6. 未确定事项

1. 五个工程的实际授权利（无 `LICENSE`/`COPYING`、README 无声明）——权属由人确认，缺授权不得当作许可。
2. `yjk` 工作区 34 个已跟踪修改（其中 24 个 DLL + 1 个 `YJK_SSCS.YDB`）的意图与去留；本票不代入 git 操作。
3. 厂商 DLL（RhinoCommon / SAP2000v1 / ETABSv1 / YJK 系列）的再分发权属——本票只记"存在与依赖"证据。
4. 参考 Hub 许可混合的**逐文件**结论（仅抽样 `metadata.json` 与 `LICENSE`，未穷举 59 个 Skill）。
5. 五仓原始 git 历史的保留/切断取舍。
6. 客户端支持边界（含 pi 的具体项目核实与各客户端版本）——属票 [三类 Agent 实际支持哪些 Skill 与 MCP 接入方式](../issues/03-agent-integration-evidence.md)。
7. 参考 Hub 的领域 Skill 模式能否复用于结构工程场景——属票 [首批结构工程场景与 Hub 成功标准是什么](../issues/01-first-workflows.md) / [仓库如何组织，Skill 与 MCP 如何分工](../issues/06-repository-skill-boundary.md)。
8. 未跟踪/树外内容（如 `rhino/.scratch/`、`yjk/tmp/`、`output/`、生成物、各仓 `.omx/`/`.omo/`/`.trae/` 等）未审计；本票只覆盖已跟踪内容 + 目录清单。
9. `sap2000` 工作区被删的已跟踪文件 `.zcode/config.json`（内容为空的 `mcp.servers`）是否应从 HEAD 恢复，未判定。

## 7. 第一方引用（可点击）

**参考 Hub（固定 SHA）**

- Tree：https://api.github.com/repos/Cai-aa/CAE-Agent-Hub/git/trees/56705e07ce6e99f0d5a0d0c7b5e28b6b2c0bc973?recursive=1
- Commit：https://api.github.com/repos/Cai-aa/CAE-Agent-Hub/commits/56705e07ce6e99f0d5a0d0c7b5e28b6b2c0bc973
- README：https://github.com/Cai-aa/CAE-Agent-Hub/blob/56705e07ce6e99f0d5a0d0c7b5e28b6b2c0bc973/README.md
- LICENSE：https://github.com/Cai-aa/CAE-Agent-Hub/blob/56705e07ce6e99f0d5a0d0c7b5e28b6b2c0bc973/LICENSE
- Skill 索引：https://github.com/Cai-aa/CAE-Agent-Hub/blob/56705e07ce6e99f0d5a0d0c7b5e28b6b2c0bc973/Skill/README.md ；Abaqus 索引/客户端用法：https://github.com/Cai-aa/CAE-Agent-Hub/blob/56705e07ce6e99f0d5a0d0c7b5e28b6b2c0bc973/Skill/abaqus/README.md
- 代表 Skill（含 frontmatter/工作流）：https://github.com/Cai-aa/CAE-Agent-Hub/blob/56705e07ce6e99f0d5a0d0c7b5e28b6b2c0bc973/Skill/abaqus/analysis/abaqus-static-analysis/SKILL.md ；其 `metadata.json`（`NOASSERTION`/`restricted`）与 `UPSTREAM_LICENSE`(MIT)：同目录下 `metadata.json`、`UPSTREAM_LICENSE`
- 逐适配器注册/配置示例：`MCP/Abaqus/examples/mcp_config.example.json`、`MCP/Adams/client-config.example.json`、`MCP/ANSA/examples/codex_config.example.toml`、`MCP/ANSA/register_codex_mcp.ps1`、`MCP/ANSA/install_ansa_bridge.ps1`、`MCP/FEP-Agent-Hub/scripts/install.ps1`（均在 `https://github.com/Cai-aa/CAE-Agent-Hub/tree/56705e07ce6e99f0d5a0d0c7b5e28b6b2c0bc973/…`）
- CI：`.github/workflows/adams-check.yml`、`.github/workflows/fep-agent-hub-test.yml`；Tags/Releases：https://api.github.com/repos/Cai-aa/CAE-Agent-Hub/tags?per_page=10 、https://api.github.com/repos/Cai-aa/CAE-Agent-Hub/releases?per_page=10
- Subagent/README：https://github.com/Cai-aa/CAE-Agent-Hub/blob/56705e07ce6e99f0d5a0d0c7b5e28b6b2c0bc973/Subagent/README.md

**MCP C# SDK（第一方）**

- Getting started / 包选择 / stdio server：https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/getting-started.md
- Transports（`StdioServerTransport`）：https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/transports/transports.md
- 包清单：https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/PACKAGE.md
- NuGet：`ModelContextProtocol.Core`、`ModelContextProtocol`、`ModelContextProtocol.AspNetCore`

**客户端（旁证，第一方）**

- Claude Code 插件结构（含 `skills/`、`.mcp.json`）：https://github.com/anthropics/claude-code/blob/main/plugins/README.md
- Codex `mcp_servers` 配置参考：https://learn.chatgpt.com/docs/config-file/config-reference ；schema 源：https://github.com/openai/codex/blob/main/codex-rs/config/src/mcp_types.rs

**本地工程（只读，逐仓根目录）**

- 根目录：`F:/DotNetProgram/tgk-midas-mcp`、`tgk-rhino-mcp`、`tgk-sap2000-mcp`、`tgk-yjk-modeling-mcp`、`tgk-etabs-mcp`。主要证据文件：`README.md`、`README.en.md`、`Directory.Build.props`、`Directory.Build.targets`、`src/**/*.csproj`、`*.slnx`、`global.json`、`docs/mcp-loading.md`、`docs/skills/**/SKILL.md`、`opencode.json`、`.zcode/config.json`、`docs/examples/claw-settings.rhino-modeling.json`；git 事实来自 `git rev-parse/log/status/ls-files/remote`（本地路径，非公开 URL）。
