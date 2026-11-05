# 三类 Agent 实际支持哪些 Skill 与 MCP 接入方式

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: punkwen
Blocked by: none
Parent: ../map.md

## Question

Claude Code、pi（核实具体项目而非同名产品）、OpenCode 当前各自原生 Skill 与 MCP 支持、配置位置/格式/作用域、加载与刷新机制是什么，哪些需要额外扩展？区分已证实的能力与限制，为部署契约提供事实；不选部署策略、不改用户配置。

## Answer

已按 [research 证据稿](https://github.com/punkwen/Structure-Agent-Hub/blob/c7949b81bd257bc6d51035311da85f0a017bdf92/.scratch/structure-agent-hub-spec/research/agent-integration.md) 取证（2026-11-05）：pi 身份已核实为 `earendil-works/pi`（旧地址 `badlogic/pi-mono` 是官方重定向、同一谱系，子包 `packages/coding-agent`），当前 1.5.0 具备官方内置 MCP（`builtin:mcp`，≥0.99.0 引入）与原生 Skills（SKILL.md 约定 ≥0.20.0），更旧版本不能假定具备这些能力；Claude Code 的 Skills/MCP 配置位置、格式与 user/project 作用域已取证；OpenCode 官方并存 v1 与 v2 两条发布线，MCP/Skill 配置 JSON 形态互不兼容，契约必须先绑定目标大版本。以上均为文档与固定源码/registry 证据，未部署实测；三家均无第一方证明的整体幂等或卸载保证，不能视为既有能力。详细配置表、版本锚点与并列选项只在该资产中，不复制于此。

Research branch: research/hub-spec-agent-integration-20261105
Commit: c7949b81bd257bc6d51035311da85f0a017bdf92
Date: 2026-11-05
