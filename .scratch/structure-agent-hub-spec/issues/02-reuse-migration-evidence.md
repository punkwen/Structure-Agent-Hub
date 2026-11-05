# 参考 Hub 与五个现有 MCP 带来哪些复用和迁移约束

Type: research
Labels: wayfinder:research
Mode: AFK
Status: resolved
Assignee: punkwen
Blocked by: none
Parent: ../map.md

## Question

固定参考仓库 SHA 后，哪些组织、Skill/注册/发布模式确实存在；五个独立工程的运行时、桥接、外部引用、路径、已有 Skill/客户端配置与许可证证据，给源码纳入/迁移和目录设计带来什么约束？只交事实与选项，不替用户决定合仓/移动/索引或许可证。

## Answer

已按 [research 证据稿](https://github.com/punkwen/Structure-Agent-Hub/blob/2fd0270f65121016e0935dcca633ad06d88a0d0e/.scratch/structure-agent-hub-spec/research/reuse-migration.md) 取证（2026-11-05）：固定参考仓库 SHA 后，其已观察到的模式是逐适配器自包含、无根级一键安装器、客户端配置形状多种并存、许可证文本分层；五个本地工程为各自独立的 `.git` 仓库，运行时与桥接互不相同（HTTP+Key、外部 exe 加宿主内插件与命名管道、COM 加本机 DLL、net48 原生 SDK），已有 Skill 与 in-tree 客户端配置形状不一，五仓均缺 LICENSE/COPYING 文本，且 YJK 工作区有已跟踪文件被修改、SAP2000 工作区有一处已跟踪文件被删除。以上为文本与只读 git 事实，未构建或运行验证；不据此决定纳入、迁移或授权。详细清单与并列选项只在该资产中，不复制于此。

Research branch: research/hub-spec-reuse-migration-20261105
Commit: 2fd0270f65121016e0935dcca633ad06d88a0d0e
Date: 2026-11-05
