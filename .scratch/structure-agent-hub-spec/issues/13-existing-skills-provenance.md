# 现有结构专业 Skill 的来源与公开引用条件是什么

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: punkwen
Blocked by: 04,05,06
Parent: ../map.md

## Question

针对 [仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md#answer) 已确认为第三个独立 Skill 来源的 `F:/DotNetProgram/tigerkin-skills`，取证其 `StructureDev` 下与结构专业相关的 Skill，回答：Hub 若要索引它们，需要哪些可追溯的来源、权利与依赖证据？

须覆盖：

- 候选清单：先完整列出 `StructureDev` 下可能相关的条目（包括 `opensees-tcl-expert` 及其随附的手册、OpenSeesPy 文档等），不以先验判断排除其他条目；对每条标注是否相关、相关理由与未知项。该仓库根目录另有同名 12 项的 `skills/structure-software-dev/`，须判定两份副本哪一份为准、差异何在，以及本票结论指向哪一份，不得把两份都当作可选来源。
- 来源与版本：记录版本锚点（提交或内容哈希）与取证日期；仅在安全且获准时提供公开链接，否则以非敏感标识引用私有证据。区分事实证据与用户的授权声明或法律判断。
- 权利与许可：各 Skill 与其随附/引用的文档是否带版权声明、许可文本（SPDX 或明确识别的非标准条款）、来源出处与义务；第三方材料（如 OpenSees/OpenSeesPy 文档、手册摘录、示例、数据）逐项标注权利人与未知项，未知记 `NOASSERTION` 之类明确标记，不得当作许可。
- 依赖：Skill 实际声明或隐含依赖的 MCP、运行时、外部软件、随附文档与数据文件；区分已验证与未验证。
- 可访问历史：检查公开可见的 Git 历史中是否含厂商资产、秘密或第三方材料，仅报告存在性与位置，不复制其内容、不暴露秘密。
- 仓库内其他内容：检查仓库根是否存在内嵌的第三方项目或压缩包（如参考 skill 集合的复制件），报告其来源与许可，并明确它们不属于可索引的 Skill 范围。
- 明确不声称：本票不构成公开再分发许可、不声称 `GPL-3.0-only` 覆盖该仓库或其内含材料（[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) 的第一方确认只覆盖五个 MCP），也不声称任何技术能力。

不复制第三方源码或材料，不在研究产物中放入秘密或受保护文件；无法核验的历史和权利须标为未知，不得当作已通过审查。解决本票时按 [tracker 研究资产约定](../../../docs/agents/issue-tracker.md) 使用独立 `research/` 分支并 push，不建 PR、不合并。

参考票：[OpenSees 有哪些可用的集成路径与运行约束](04-opensees-integration-evidence.md)、[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md)、[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md)。

## Answer

已按 [research 证据稿](https://github.com/punkwen/Structure-Agent-Hub/blob/408dc8e70a4d4515f527cdbe1fbe67453f6ef8c5/.scratch/structure-agent-hub-spec/research/skills-provenance.md) 取证（2026-11-06，本机只读静态审计，版本锚点 `c244fda622650715c8269784535e256a74b54a8b`）。全部为事实证据与 `NOASSERTION` 标记，不含权属声明或法律判断；未修改 tigerkin-skills 任何文件。

### 1. 两份副本：以 `skills/structure-software-dev/` 为准

仓库根的 `StructureDev/` 与 `skills/structure-software-dev/` 是同一批 12 个 Skill（各 2,582 个跟踪文件）的一次性整树复制的两份检出，不是两个来源。差异仅 3 项（`dtl-model`、`yjk-dsnmodel` 的 SKILL.md 描述文本更新，`etabs-api-function` 的目录扁平化 + 新增顶层 SKILL.md），全部修订只存在于 `skills/` 份（`17d7b1c2`，2026-07-21）。**本票结论指向 `skills/structure-software-dev/`**；`StructureDev/` 为陈旧副本，其去留留给[哪些现有结构专业 Skill 可以纳入 Hub 索引](14-existing-skills-index-scope.md)/用户处置，本票不动它。

### 2. 候选清单与相关性（12 项全部登记，详见证据稿 §4）

高相关：`opensees-tcl-expert`（536 文件）、`sap2000-api`（1,818）、`etabs-api-function`（133）、`yjk-modeling-api`（22）、`yjk-modeling-foundation-api`（6）、`yjk-runtime-api-function`（10）、`yjk-runtime-api-post-function`（5）。中相关：`yjk-dsnmodel`、`dtl-model`。条件相关：`sap2000-s2k-expert`（36 个真实 s2k 样例，其中 26 个含 `LicenseNum=`）、`midas-api`（未检出第三方文本复制证据，但自撰程度未证实）。低/存疑：`3d3s-expert`（3D3S 不在五个 MCP 之列）。「相关」不是「可索引」。

### 3. 权利与许可：当前无一满足公开引用条件

12 个 Skill 全部无 LICENSE 文件、无 SPDX、无许可 frontmatter。唯一明确权利证据是 ETABS 文档 128 处 CSI 版权声明（2025，All rights reserved，无许可条款）；`sap2000-api` 的 1,817 个 doc 无任何声明（特征指向 CSI，权利人推断）；OpenSees PEER 手册中文编译本 + OpenSeesPy 官方文档 534 文件导出（Berkeley 系，无许可文本）；YJK 六项含厂商头文件/接口文档特征材料。上述第三方材料权利人与许可凡未证实者一律 `NOASSERTION`。`LicenseNum=`（26 个 s2k、8 个不同取值）按[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) §5 属永不发布项。

### 4. 依赖与历史

- MCP 依赖声明：0 处（检索命中均为假阳性）；frontmatter 只有 `name`/`description`。[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md#answer) §4 要求的 MCP 依赖声明尚不存在。
- 文本声明的软件前提（静态阅读，未验证）：SAP2000 OAPI、ETABS v22+/.NET Standard 2.0 的 `ETABSv1.dll`、YJK DLL 系列（建模/基础/运行时/后处理各自不同）、MIDAS `localhost:10084` 服务。
- 历史（18 提交，仅 master）：无厂商二进制；含 MIT 的 mattpocock-skills 中文包（zip+目录，108 文件一致）、两个含中文结构工程书籍/规范文章的 `reference_bundle.zip`（`NOASSERTION`）、s2k 许可证号、`.omc` 个人数据缓存（仅登记位置，不复制内容）。历史审计按文件名与已知名单抽查，未穷尽扫描全部历史 blob 内容。
- Gitee 远端公开可见性**未能核实**（匿名 403/API 404），公开链接条件未知。

### 5. 明确不声称

本票不构成公开再分发许可，不声称 `GPL-3.0-only` 覆盖该仓库或其材料（[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) 的第一方确认只覆盖五个 MCP），不声称任何技术能力或客户端兼容性。范围确认属[哪些现有结构专业 Skill 可以纳入 Hub 索引](14-existing-skills-index-scope.md)。

Research branch: research/hub-spec-skills-provenance-20261106
Commit: 408dc8e70a4d4515f527cdbe1fbe67453f6ef8c5
Date: 2026-11-06

## Comments

- 2026-11-06：本票的 research 提交（`9083d4b`、`6811f36`）因并发会话在同一工作副本切换分支而一度进入 `main` 历史；研究文件已从 `main` 工作树移除（`bc88ac4`），但这两个提交仍是 `main` 的祖先。按 tracker「研究分支不合并」的约定，这属于历史卫生偏差；未重写已公开的 `main`（避免与并发会话冲突），在此登记。研究文件本身只存在于 `research/hub-spec-skills-provenance-20261106`（tip `408dc8e`）。
