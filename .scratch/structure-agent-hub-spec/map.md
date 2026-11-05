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
- [哪些源码、依赖与产物可以纳入和分发](issues/05-distribution-boundary.md#answer): 经核验的第一方内容拟按 GPL-3.0-only 发布；厂商依赖及 OpenSees 按需自备、凭据不发布，第三方依赖与产物须逐项审查。
- [首批结构工程场景与 Hub 成功标准是什么](issues/01-first-workflows.md#answer): 结构工程师优先，五个现有 MCP 各有代表实例，受控操作并以五例全部实测通过作为核心可用标准。
- [仓库如何组织，Skill 与 MCP 如何分工](issues/06-repository-skill-boundary.md#answer): 五个 MCP 独立、Hub 索引；Skill 按工作流与来源分归属，确认保障和现有 Skill 审查另行跟踪。
- [OpenSees MCP 首批能力应止于哪里](issues/07-opensees-capability-scope.md#answer): 首批只走 OpenSeesPy 跑用户 Python 脚本；runner 写状态文件判完成（不靠日志 token）；不解析结果、不并发、不装运行时；不计入五例核心门槛，仓库起源另票。

## Not yet specified

已选场景中尚可能出现需要进一步决策的结构工程数据语义或模型操作约束；不预设统一模型、单位/坐标转换或跨软件流程。待有可明确提问的独立问题时再建票，若确认不需要则清除。

## Out of scope

本 effort 的交付物为 SPEC，不执行工程搬迁、MCP/Skill 开发或实际客户端部署；这些行为在 SPEC 形成后另行实施。
