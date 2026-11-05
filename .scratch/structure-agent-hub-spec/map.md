# 结构专业 AI Skill + MCP Hub SPEC 地图

Labels: wayfinder:map

## Destination

形成结构专业 AI Skill + MCP Hub 的 SPEC，覆盖现有五个 MCP 的纳入方案、仓库与能力组织、OpenSees 扩充及 Claude Code/pi/OpenCode 部署契约。可交接程度由决策票逐步确定。

## Notes

planning only；本轮不写 SPEC 正文或执行源码搬迁；用户列出五个工程，口述四个已按列名五个核实。必须读取 wayfinder；处理 grilling 票读取 grilling/domain-modeling；涉及接口/目录读取 codebase-design；research 票读取 research。tracker：[Issue tracker: Local Markdown](../../docs/agents/issue-tracker.md)。不将未回答建议写为共识。
范围例外：允许在授权与集成路径的阻塞票解决后，进行选定 OpenSees 运行时的最小兼容性核验，仅为后续决策提供证据；不开发 MCP/Skill、不迁移工程、不部署客户端。本轮建图不执行该核验。

## Decisions so far

- [OpenSees 有哪些可用的集成路径与运行约束](issues/04-opensees-integration-evidence.md#answer): 第一方资料证实 Tcl/CLI 与 OpenSeesPy 两条入口，但版本映射与授权措辞冲突，仅有文档证据。
- [三类 Agent 实际支持哪些 Skill 与 MCP 接入方式](issues/03-agent-integration-evidence.md#answer): pi 已核实为 earendil-works/pi 且当前版本内置 MCP 与原生 Skills；OpenCode v1/v2 配置形态不兼容，整体部署幂等与卸载尚未获第一方证据证明。
- [参考 Hub 与五个现有 MCP 带来哪些复用和迁移约束](issues/02-reuse-migration-evidence.md#answer): 五仓运行时/桥接与已有 Skill、客户端配置形状各异，均缺许可文本，YJK/SAP2000 工作区存在未提交状态。

## Not yet specified

首批场景明确后可能显现的结构工程特有数据语义与模型操作约束；当前不足以精确提问，不预造统一模型、单位/坐标转换或跨软件流程。若后续发现不需要则清除，清晰问题再毕业成票。

## Out of scope

本 effort 的交付物为 SPEC，不执行工程搬迁、MCP/Skill 开发或实际客户端部署；这些行为在 SPEC 形成后另行实施。
