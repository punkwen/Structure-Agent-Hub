# OpenSees 有哪些可用的集成路径与运行约束

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: punkwen
Blocked by: none
Parent: ../map.md

## Question

第一方 OpenSees/OpenSeesPy 资料支持什么调用/执行方式、版本与平台、安装/许可/打包约束；本机已知 OpenSees3.8.0-x64.exe/ 仅为解压安装包，不能当 MCP 源码。哪些路径可用于未来 MCP，差异与未知是什么？不选范围，不开发 MCP。

## Answer

已按 [research 证据稿](https://github.com/punkwen/Structure-Agent-Hub/blob/6edf74aa9dc6fcc55fc9b70a84cba5bfffa1345e/.scratch/structure-agent-hub-spec/research/opensees-integration.md) 取证（2026-11-05）：第一方资料支持两类未来入口——Tcl/CLI 可执行程序的交互、`source` 与 batch 模式，以及 `import openseespy` 的 Python 解释器；官方可执行程序 `3.8.0`、PyPI `openseespy 3.8.0.0` 与仓库 tag 之间的版本映射、Python 兼容性声明（3.8/3.10/3.11/3.12）以及 `COPYRIGHT`、`license.html`、`LICENSE.md` 的授权措辞互相冲突。以上均为文档与发布元数据证据，未安装、未运行、未向权利方确认，不构成运行时或授权保证；详细证据与并列选项只在该资产中，不复制于此。

Research branch: research/hub-spec-opensees-20261105
Commit: 6edf74aa9dc6fcc55fc9b70a84cba5bfffa1345e
Date: 2026-11-05
