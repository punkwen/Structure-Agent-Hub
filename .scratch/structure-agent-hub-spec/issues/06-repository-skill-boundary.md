# 仓库如何组织，Skill 与 MCP 如何分工

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: resolved
Assignee: punkwen
Blocked by: 01,02,05
Parent: ../map.md

## Question

为了已选场景，在源码归属/分发约束下如何组织目录与独立发布边界，用户提出的 MCP/ 是否作为源码容器、外部引用或其他角色？Skill 的专业工作流与具体软件操作各负责什么，是否确实需要任何共享接口？不预设 monorepo、不造统一抽象。

参考票：[首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md)、[参考 Hub 与五个现有 MCP 带来哪些复用和迁移约束](02-reuse-migration-evidence.md)、[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md)。

## Answer

用户于 2026-11-06 确认以下设计（HITL 结论），包括 `tigerkin-skills` 作为第三个独立 Skill 来源的归属与权利边界。本票仍是 planning-only 的决策票：本轮未开发 MCP/Skill、未写 SPEC 正文、未搬迁或迁移任何仓库、未做实际运行/客户端/厂商软件验证、未打包或再分发任何产物、未部署客户端。以下职责划分是规划要求，不代表现有实现已经满足。

### 1. 仓库与独立发布边界

- 五个现有 MCP 保持各自独立的 Git 仓库。
- Hub 的 `MCP/` 是索引，不是 MCP 源码容器：不使用 Git submodule，也不在 Hub 内检出 MCP 源码。
- 除 Hub 自有 Skill 与各 MCP 自有 Skill 外，`F:/DotNetProgram/tigerkin-skills` 是第三类独立 Skill 来源，不是 MCP 源码容器；Hub 同样不检出其源码、不复制其 Skill 或随附文档。
- 每个 MCP 可独立构建、版本化和发布；Hub 可单独版本化；不要求一起发布或一起安装。
- 索引的具体格式与安装自动化留待[一键部署应承诺什么行为与验收结果](08-deployment-contract.md)；五个 MCP 的原始仓库历史与源码基线留待[五个现有 MCP 的迁移基线与历史如何保留](10-migration-baseline.md)。

### 2. Skill 的归属与覆盖

- Hub 的 `Skill/` 负责维护和发布 Hub 拥有的专业工作流 Skill，按真实工作流组织。
- 覆盖[首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md)的全部五个实例，并优先贯通 SAP2000 端到端示例。
- 不强制「一个软件一个 Skill」，也不设单一总控 Skill；Skill 的粒度与边界按实际工作流划分。
- 与某个 MCP 紧密耦合的 Skill 可以留在该 MCP 的独立仓库，并由该仓库发布；Hub 只索引，不维护第二份源码副本。
- Hub 或各 MCP 仓库维护的具体 Skill 结合实际工作流逐项确定。
- 第三类来源 `tigerkin-skills` 保持独立；Hub 可以索引其中与 StructureDev 相关的 Skill（包括 `opensees-tcl-expert`），但仅在完成来源、权利、依赖与可访问历史的审计之后。索引不等于复制，Hub 不维护第二份源码或随附文档副本。
- 不得声称 `tigerkin-skills` 仓库、其 Skill 或其内含第三方材料已获 `GPL-3.0-only` 授权；[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) 中的第一方授权确认只覆盖用户明确确认的既有五个 MCP 仓库的第一方内容。
- `opensees-tcl-expert` 只是候选：它既不证明 OpenSees 集成能力，也不证明其内容可再分发；OpenSees 的首批能力范围仍由[OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md)决定。
- 上述审计须逐项记录可追溯的来源、权利、许可、依赖与可公开访问的历史，先由[现有结构专业 Skill 的来源与公开引用条件是什么](13-existing-skills-provenance.md)取证，再由用户在[哪些现有结构专业 Skill 可以纳入 Hub 索引](14-existing-skills-index-scope.md)中确认范围。

### 3. Skill 与 MCP 的职责分工

- Skill 描述专业步骤、检查项与工程师需要作出的判断，指导 Agent 在需要时使用 MCP 的公开能力。
- MCP 实现具体软件操作，包括必要的校验与复合操作。
- 按[首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md#answer)的要求，MCP 负责其适配器特有的只读状态恢复、副本/覆盖相关操作，以及效果、错误与部分失败的如实报告。本票不声称现有实现已达到这些要求。
- Skill 文本不能代替实际行为：若状态恢复失败，按前述场景要求报告，该实例判定为失败。
- 在厂商软件、SDK 与运行时等前置条件满足时，MCP 不得以 Hub 的某个 Skill 或某个特定 Agent 客户端为运行依赖。

### 4. 依赖声明与能力识别

- 每个 Skill 声明实际需要的 MCP（如有）、适用的版本或兼容条件，并区分已验证与未验证的组合。
- 实际预期的 server 及其暴露的能力/工具标识必须可识别；缺失、不匹配或存在歧义时应停止并报告，而不是猜测。
- 未经验证，不声称客户端支持工具命名空间；也不强加统一工具前缀。

### 5. 不预造统一抽象

- 在没有具体且有理由的工作流之前，不新增通用的跨软件工程数据模型或统一操作接口。
- 这不禁止 MCP 协议本身、各 server 自己的契约，或已有的明确可复用跨软件能力。

### 6. 人工确认与技术闸门

- [首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md#answer)规定的人工逐次确认仍然强制有效。
- 是否以及如何用技术手段强制该确认，本票尚未决定：先由[三类 Agent 与 MCP 如何支持逐次人工确认](11-confirmation-capability-evidence.md)取证，再由 HITL 票[如何落实工程师逐次确认的保障与验收](12-human-confirmation-contract.md)作出决定。
- 本票不声称已有技术确认保障；具体能力须基于证据和核验声明，是否要求技术闸门仍由后续决策确定。

### 7. 保留的既有边界与本地静态证据

- 本票不改变[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer)的边界：外部仓库、发行物及其可公开访问的历史，仍须遵守厂商文件、秘密、来源与授权审查要求。
- 安装与注册留待[一键部署应承诺什么行为与验收结果](08-deployment-contract.md)；迁移基线、原历史与工作区改动留待[五个现有 MCP 的迁移基线与历史如何保留](10-migration-baseline.md)。
- 关于第 4 节，可核对的本地静态证据是：SAP2000 与 ETABS 都注册了同名工具 `open_session`（`F:/DotNetProgram/tgk-sap2000-mcp/src/Tgk.Sap2000.Mcp/McpToolHost.cs:26`、`F:/DotNetProgram/tgk-etabs-mcp/src/Tgk.Etabs.Mcp/McpToolHost.cs:26`）；YJK 注册 `yjk_validate_model_spec`（`F:/DotNetProgram/tgk-yjk-modeling-mcp/src/Tgk.Yjk.Modeling.Mcp/Program.cs:79`），而其 Skill 文档写作 `validate_model_spec`（`F:/DotNetProgram/tgk-yjk-modeling-mcp/docs/skills/yjk-modeling-mcp/SKILL.md:17`）。这些只是本地源码静态阅读，不是运行时证明，也不主张客户端实际会发生名称冲突。
