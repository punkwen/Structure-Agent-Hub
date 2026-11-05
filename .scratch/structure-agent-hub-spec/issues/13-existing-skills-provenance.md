# 现有结构专业 Skill 的来源与公开引用条件是什么

Type: research
Labels: wayfinder:research
Mode: AFK
Status: open
Assignee: unassigned
Blocked by: 04,05,06
Parent: ../map.md

## Question

针对 [仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md#answer) 已确认为第三个独立 Skill 来源的 `F:/DotNetProgram/tigerkin-skills`，取证其 `StructureDev` 下与结构专业相关的 Skill，回答：Hub 若要索引它们，需要哪些可追溯的来源、权利与依赖证据？

须覆盖：

- 候选清单：先完整列出 `StructureDev` 下可能相关的条目（包括 `opensees-tcl-expert` 及其随附的手册、OpenSeesPy 文档等），不以先验判断排除其他条目；对每条标注是否相关、相关理由与未知项。
- 来源与版本：记录版本锚点（提交或内容哈希）与取证日期；仅在安全且获准时提供公开链接，否则以非敏感标识引用私有证据。区分事实证据与用户的授权声明或法律判断。
- 权利与许可：各 Skill 与其随附/引用的文档是否带版权声明、许可文本（SPDX 或明确识别的非标准条款）、来源出处与义务；第三方材料（如 OpenSees/OpenSeesPy 文档、手册摘录、示例、数据）逐项标注权利人与未知项，未知记 `NOASSERTION` 之类明确标记，不得当作许可。
- 依赖：Skill 实际声明或隐含依赖的 MCP、运行时、外部软件、随附文档与数据文件；区分已验证与未验证。
- 可访问历史：检查公开可见的 Git 历史中是否含厂商资产、秘密或第三方材料，仅报告存在性与位置，不复制其内容、不暴露秘密。
- 明确不声称：本票不构成公开再分发许可、不声称 `GPL-3.0-only` 覆盖该仓库或其内含材料（[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) 的第一方确认只覆盖五个 MCP），也不声称任何技术能力。

不复制第三方源码或材料，不在研究产物中放入秘密或受保护文件；无法核验的历史和权利须标为未知，不得当作已通过审查。解决本票时按 [tracker 研究资产约定](../../../docs/agents/issue-tracker.md) 使用独立 `research/` 分支并 push，不建 PR、不合并。

参考票：[OpenSees 有哪些可用的集成路径与运行约束](04-opensees-integration-evidence.md)、[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md)、[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md)。
