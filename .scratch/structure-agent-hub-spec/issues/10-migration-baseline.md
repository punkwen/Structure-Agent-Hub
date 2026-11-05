# 五个现有 MCP 的迁移基线与历史如何保留

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: resolved
Assignee: punkwen
Blocked by: 06
Parent: ../map.md

## Question

在目录组织与纳入方式定下后，迁移以哪个提交或工作区快照为基线，如何保留原仓库历史、未提交修改/删除及必需的未跟踪内容；哪些文档/启动配置中的绝对路径应同步更新，旧目录何时可退役，怎样验收不丢内容且调用链不断？用户决定，不能默认丢弃工作区、恢复 SAP2000 删除或替 YJK 提交。依据见 [参考 Hub 与五个现有 MCP 带来哪些复用和迁移约束](02-reuse-migration-evidence.md)，目录前提见 [仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md)。

## Answer

用户于 2026-11-06 确认以下设计（HITL 结论）。本票仍是 planning-only 的决策票：本轮未迁移或搬迁任何仓库、未改动五个 MCP 工程、未做备份/恢复演练、未审计历史或未跟踪内容、未运行任何 MCP 或厂商软件、未部署客户端、未写 SPEC 正文。以下均为未来实施时必须满足的要求，不代表已经完成或已通过验收。

### 1. 基线与工作区状态

- 五个现有 MCP 继续留在当前 `F:/DotNetProgram/tgk-...` 本地工作目录；Hub 的 `MCP/` 只做索引，不使用 submodule、不检出源码，与[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md#answer)一致。
- 本票不规划原工作目录的退役；未来是否物理迁移或退役须另行决策，不因通过验收而自动发生。
- 实际实施时，先确认并记录每个仓库的真实 HEAD 与选定提交，再单独捕获并保留当时的已暂存/未暂存修改与删除。2026-11-05/06 的观察不作为选定的最终基线。
- 不自动恢复 SAP2000 已跟踪的 `.zcode/config.json` 删除；不替用户提交 YJK 的修改。哪些脏改动进入公开发布须另行审查并由用户确认，不能从「已保留」推断为「可发布」。

### 2. 未跟踪/忽略内容与私有归档

- 对未跟踪与忽略的材料做清单与分类；未确认的材料原地保留，不删除。用户确认必需的材料以私有方式保存。
- 完整保留可恢复的原仓库历史与本地引用、stash/reflog 及必要的 Git 对象依赖，并单独保留实际的 index/worktree 状态。
- 含秘密的 `.git` 配置与厂商/秘密数据只进入受访问控制的私有归档，绝不隐式公开。
- 制作两份受保护的私有归档副本，置于相互独立的物理介质；不做自动云上传。若无法取得独立介质，须如实标记备份冗余不完整，不得判为通过。原目录保持不动。

### 3. 公开历史与分发

- 未来公开发布时，只有当每个选定公开 ref 可达的全部历史及其他公开对象都满足[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer)的分发、授权与秘密约束，才保留原历史；否则以完全审计过的干净基线新建公开历史。改写历史不是可隐含作出的用户决定。
- 完整原历史与来源映射私有保留；映射仅在另行批准后才公开。默认只发布明确选定并审计过的初始公开 ref，不发布全部分支/标签，其余留在私有归档待另行审查。
- 公开可访问的历史、ref 与发布产物中不得含厂商 SDK/DLL、YJK 数据或秘密。现有 Gitee 可见性未知：本轮对 Rhino 与 ETABS 的公开页面请求均返回 HTTP 403，不足以判定为私有；发布前须检查实际可访问的原仓库与目标历史。若发现既有暴露，报告并请用户决定，不擅自修改或删除旧远端。不得声称公开合规或审计已完成；前述[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer)的素材、归属与许可审查同样适用。

### 4. 路径审计

- 审计范围限于活跃/受支持的 README、MCP 加载文档、Skill 引用、启动示例与实际配置；脚本/源码仅在其属于受支持调用链时纳入。
- 按实际环境与客户端能力更新，不盲目把所有路径改写为 `F:`，也不假定所有 `G:`/`I:` 路径在任何环境都已失效。用户/私有客户端配置的改动需另行确认；详细安装与注册仍属[一键部署应承诺什么行为与验收结果](08-deployment-contract.md)。
- 不批量改动历史记录、生成/用户产物或未使用的实验。已观察到的静态样本（非穷尽、非运行时故障证据）：MIDAS `F:/DotNetProgram/tgk-midas-mcp/README.md:50,52`；Rhino `F:/DotNetProgram/tgk-rhino-mcp/docs/examples/claw-settings.rhino-modeling.json:4`；SAP2000 `F:/DotNetProgram/tgk-sap2000-mcp/docs/mcp-loading.md:16,22`；YJK `F:/DotNetProgram/tgk-yjk-modeling-mcp/opencode.json:7`（该文件本地已修改，不得覆盖）；ETABS `F:/DotNetProgram/tgk-etabs-mcp/docs/skills/etabs-mcp-operator/references/mcp-loading.md:16,22`。SAP2000 实验目录 `sap-temp-workdir/reflect-mcp/Program.cs:3` 含 NuGet 路径，仅当确属受支持调用链时才纳入。

### 5. 验收

- 保留验收：建立清单，在隔离位置私有恢复，比对原仓库的 refs/Git/index/已暂存/未暂存/删除状态与选定文件的相对路径及内容哈希，报告差异且不覆盖源。仅有备份存在不算已验证可恢复。
- 调用链验收：每个 MCP 用实际相关客户端 → MCP → 宿主/必需依赖，跑一个结果可验证的代表场景；缺少运行时或软件即判为未验证，不得判为通过。
- [首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md#answer)的五个场景与核心可用门槛继续适用；模型改动与分析运行仍须逐次明确同意，并遵守既有副本/不覆盖规则。以上是未来计划，不构成当前运行成功的声明。

### 6. 范围与当前证据

- 范围仅限五个现有 MCP；OpenSees 新仓库见[OpenSees MCP 的仓库起源与首发基线如何确定](15-opensees-mcp-repository-origin.md)，部署/安装范围与机制仍属[一键部署应承诺什么行为与验收结果](08-deployment-contract.md)。
- 当前已核验证据：本轮在根目录 reparse 检查后，以 `GIT_OPTIONAL_LOCKS=0 git status --short --untracked-files=normal`（禁用 fsmonitor）观察，2026-11-06 MIDAS、Rhino、ETABS 普通状态为空，SAP2000 为 ` D .zcode/config.json`，YJK 有 34 个已跟踪修改（含厂商二进制/数据与 `opencode.json`）。普通状态不含忽略文件，故不得声称已审计忽略内容。[参考 Hub 与五个现有 MCP 带来哪些复用和迁移约束](02-reuse-migration-evidence.md#answer)指向的固定提交 `2fd0270` 是历史证据，不是今日选定基线。
- 已知限制：示例使用 `G:`/`I:` 而当前工作目录在 `F:`，但未做端到端运行测试，不能断言示例在其他环境必然失效。