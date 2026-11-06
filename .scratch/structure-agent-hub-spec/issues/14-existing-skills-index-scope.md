# 哪些现有结构专业 Skill 可以纳入 Hub 索引

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: resolved
Assignee: punkwen
Blocked by: 05,06,13
Parent: ../map.md

## Question

在 [现有结构专业 Skill 的来源与公开引用条件是什么](13-existing-skills-provenance.md) 取证之后，与用户共同确定 Hub 索引的确切范围：

- 在既定索引意向下确认相关 `StructureDev` 条目的确切目标与版本，依据审查结果判断 OpenSees 候选（如 `opensees-tcl-expert`）等能否纳入；未获确认或未通过审查的条目排除。
- 对每个拟索引条目确认第一方权属或许可，记录用户声明与证据的对应关系；第三方材料另须完成权利、声明保留义务、可兼容的分发方式与公开历史审查，[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) 的边界继续适用。
- 记录仍未知、须排除或不满足条件的条目及理由；不得把「候选」表述为已批准。
- 与 [仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md#answer) 一致：默认保持该仓库独立、只索引、不复制 Skill 或随附文档，也不维护第二份副本；除非用户在此明确改变，否则不重开该决定。
- 索引本身需要的最小信息（如名称、来源链接、版本锚点、依赖声明、已验证状态）只在此确认范围，不规定格式或安装自动化。

本票不执行迁移、复制、再分发或部署，也不声称任何条目已获授权或已可用。

参考票：[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md)、[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md)、[现有结构专业 Skill 的来源与公开引用条件是什么](13-existing-skills-provenance.md)。

## Answer

用户于 2026-11-06 逐项确认以下索引范围（HITL 结论）。本票是 planning-only 决策：未迁移、未复制、未再分发、未部署，也不声称任何条目已获授权或已可用。

### 1. 索引形态：公开索引，只写非敏感私有标识

- Hub 索引随 Hub 公开发布（与[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) §1 一致），但条目**不写 `tigerkin-skills` 的远端 URL**：其 Gitee 公开可见性未核实（票 13 §5），写 URL 等于 Hub 为一份可能含 CSI 文档、许可证号与个人数据的仓库背书。
- 条目以「名称 + 仓库内相对路径 + 提交锚点 + 树哈希」定位，均为非敏感标识，不构成再分发。
- 若将来核实该仓库可公开访问，是否补写 URL 须另作决定，不在本票自动生效。

### 2. 纳入策略：只纳入用户声明为第一方自撰且正文无第三方材料的条目

- 票 13 已证明 12 项候选**无一**满足「可公开引用」的许可条件（无 LICENSE/SPDX/`license` frontmatter，第三方材料权利一律 `NOASSERTION`）。因此纳入不以「许可已证实」为前提，而以「用户声明第一方自撰 + 证据未检出第三方正文复制」为前提。
- 用户声明与证据的对应关系逐条记录在 §4；声明是权属主张，不是法律结论，也不改变票 13 的 `NOASSERTION` 事实层。
- 含第三方正文、或含按[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) §5 属永不发布项的样例文件的条目，整项排除，不做「部分索引」。

### 3. 索引最小字段（不规定格式与安装自动化）

每个条目至少包含：

| 字段 | 本票确认的取值口径 |
|---|---|
| 名称 | Skill 目录名 |
| 来源路径 | `tigerkin-skills` 仓库内 `skills/structure-software-dev/<name>` |
| 版本锚点 | 仓库提交 `c244fda622650715c8269784535e256a74b54a8b`（2026-07-27） |
| 树哈希 | 该 Skill 目录的 git 树哈希（票 13 §4 表已备齐） |
| 依赖声明 | 如实记录「无 MCP 依赖声明」；文本声明的软件前提单列 |
| 验证状态 | 当前一律「未验证」——票 13 全部为静态阅读，未运行任何软件 |

格式与安装自动化留待[一键部署应承诺什么行为与验收结果](08-deployment-contract.md)。

### 4. 纳入清单（1 项）

| Skill | 树哈希 | 用户声明 | 证据对应 | 依赖 | 验证状态 |
|---|---|---|---|---|---|
| `midas-api` | `619293792ce5fdce088c2a1b7acbf009f4cb8966` | 用户声明：**完全独立编写**，未参考、未摘录官方在线手册（端点清单来自实际调用/自建记录） | 2 个文件（`SKILL.md` 5,442 B、`references/midas-api-endpoints.md` 19,530 B）；票 13 未检出第三方文本复制证据；无版权/许可文本。**与声明并列的反向证据**：`references/midas-api-endpoints.md:3` 自述「Complete catalog of all MIDAS API endpoints」，`:556` 给出官方在线手册链接，整体呈官方手册目录形态——该形态与「完全独立编写」的声明存在张力，本票不裁决，仅并列记录 | 无 MCP 依赖声明；文本声明软件前提为 `localhost:10084` 的 MIDAS API 服务 | 未验证 |

用户明确选择**不做**与官方在线手册的逐字比对；该未做项由「验证状态：未验证」承担。索引条目不得表述为「已证实自撰」或「许可审查通过」——纳入依据是用户声明，且声明与上述文件内证据并列保留。

### 5. 排除清单（11 项，理由只记于本票）

排除理由**不写入 Hub 公开索引**：索引的职责是「可用的有什么」，不是审查台账；且理由指向 CSI 版权、YJK 头文件、许可证号位置等审查目标信息。Hub 索引只列已纳入条目。

| Skill | 排除理由 |
|---|---|
| `opensees-tcl-expert` | 双重排除：(a) 产出 Tcl 脚本，与[OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer) 的 OpenSeesPy 路径不配套；(b) 正文为 PEER 手册中文编译本 + OpenSeesPy 官方文档导出（534 文件），第三方权利 `NOASSERTION`。两条理由独立成立。 |
| `sap2000-api` | 1,817 个 CSI OAPI 文档，无任何版权/许可声明，权利人仅能推断为 CSI → `NOASSERTION`。 |
| `etabs-api-function` | 128 处 CSI 版权声明（2025，All rights reserved），无许可条款 → 再分发权未知。 |
| `yjk-modeling-api` | 厂商接口文档特征材料，无声明 → `NOASSERTION`。 |
| `yjk-modeling-foundation-api` | 文档自述来源于 `gitee.com/yjk-opensource`，上游条款未核验 → `NOASSERTION`。 |
| `yjk-runtime-api-function` | 厂商头文件/宏清单摘录，无声明 → `NOASSERTION`。 |
| `yjk-runtime-api-post-function` | `设计结果接口说明_new.md` 为 C++ 头文件直出（`//dsnPro.h`），厂商 SDK 材料特征明显 → `NOASSERTION`。 |
| `yjk-dsnmodel` | 厂商数据库 schema 文档特征，无声明 → `NOASSERTION`；另有 259 处 `media/` 图片引用悬空（功能性缺陷）。 |
| `dtl-model` | 同上，厂商 schema 文档特征 → `NOASSERTION`。 |
| `sap2000-s2k-expert` | 36 个 `.s2k` 样例中 26 个含 `LicenseNum=`（8 个取值），按[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) §5 属永不发布项；文件名含疑似真实工程名。Skill 正文显式引用这些样例，故整项排除，不做「只索引手册」。 |
| `3d3s-expert` | 6 个 `.3d3s` 样例含第三方导出标记（`Euler2025 SR10`、`Grida R2025`），来源未知；且 3D3S 不在五个 MCP 之列。 |

### 6. 来源唯一化

- 索引来源固定为 `skills/structure-software-dev/`；仓库根 `StructureDev/` 是陈旧副本（票 13 §3），**不再作为索引来源**。
- 本票不执行删除、归档或迁移；`StructureDev/` 的实际处置留待后续，不在本票自动生效。

### 7. 与既有决定的边界

- 保持[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md#answer) 的「只索引、不复制」：Hub 不检出 `tigerkin-skills` 源码、不复制 Skill 或随附文档、不维护第二份副本。本票未改变该决定。
- 不改变[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) 的边界；`GPL-3.0-only` 的第一方确认仍只覆盖五个 MCP 仓库，**不覆盖** `tigerkin-skills` 或其内含材料。
- 索引条目不得被表述为「已批准」「已授权」「可用」；`midas-api` 的纳入是「用户声明自撰 + 未检出第三方正文」，不是许可审查通过。

### 8. 明确不声称

- 不构成公开再分发许可，不构成法律意见。
- 不声称任何 Skill 的技术能力、可用性或与任何客户端的兼容性。
- 不声称 `tigerkin-skills` 的 Git 历史已通过审查（票 13 §8 的审计深度限定继续有效）。
- 不声称已迁移、已复制、已部署或已建立索引文件本身。

### 9. 对后续票的约束

- [一键部署应承诺什么行为与验收结果](08-deployment-contract.md) 可据此范围设计索引格式与安装自动化，但不得扩大纳入范围。
- 将来若要纳入本票排除的条目，须新票或重开本票，并先补齐权利证据；不得以「候选」名义先行索引。
