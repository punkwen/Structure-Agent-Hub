# OpenSees / OpenSeesPy 集成路径与运行约束（证据研究）

> 本文件是 wayfinder research 票[OpenSees 有哪些可用的集成路径与运行约束](../issues/04-opensees-integration-evidence.md)的证据稿，**不是 SPEC**。只回答第一方资料支持什么、冲突在哪里、哪些仍未知；不替用户选择 Python/C#、MCP 运行时、首批功能、协议、服务形态或部署策略，不把任何选项写成规定。

## 1. 问题

票内原始问题：

> 第一方 OpenSees/OpenSeesPy 资料支持什么调用/执行方式、版本与平台、安装/许可/打包约束；本机已知 `OpenSees3.8.0-x64.exe/` 仅为解压安装包，不能当 MCP 源码。哪些路径可用于未来 MCP，差异与未知是什么？不选范围，不开发 MCP。

本稿拆成以下证据子问题：

1. OpenSees 底层框架、Tcl/CLI 可执行程序、OpenSeesPy 与「未来 MCP」之间的边界是什么？
2. 第一方资料明确给出哪些调用/执行方式？
3. 官方可执行程序与 PyPI 包的版本、平台、架构、Python 兼容性事实与冲突是什么？
4. 安装、打包、LICENSE/版权条款及可再分发限制写了什么？不得从「open source」「free」等标签推断。
5. 进程状态、任务隔离与结果文件有哪些文档约束？哪些并发/隔离/路径语义没有第一方依据？
6. 是否存在第一方 MCP 实现或 MCP 契约？哪些事实只能标为推断/未知？
7. 这些证据会给后续决策带来哪些**约束和并列选项**（不选择）？

## 2. 检索日期与取证范围

- **检索日期：2026-11-05。** 外部网页为当日读取；未安装、启动、构建、测试或运行求解器。
- **Context7 路由（先索引，再核对官方源）**：
  - `resolve_library_id("OpenSeesPy", ...)` → `/zhuminjie/openseespydoc`（Source Reputation: High，2256 snippets）；`resolve_library_id("OpenSees", ...)` 也优先返回同一 OpenSeesPy 文档库，未检索到单独的 OpenSees 核心 Tcl 文档库。
  - 按工具规则做 3 次 `query_docs`：① pip/Python/platform/version；② Tcl/CLI 命令行与输入文件；③ `wipe`/recorder/进程状态与输出。第 ② 次未返回可直接作事实终点的 CLI 调用页，只返回并行命令、recorder/logFile 片段；随后改用第一方 wiki 与 commit-pinned 源码核对。
  - Context7 仅用于发现，不作为事实终点；下文每个决定相关事实均回到第一方网页、发布包元数据或仓库文件。
- **第一方来源范围**：`opensees.berkeley.edu` 官方站/旧 wiki；`opensees.github.io/OpenSeesDocumentation` 官方 GitHub Pages 文档；GitHub `OpenSees/*` 组织仓库；OpenSeesPy 维护者仓库 `zhuminjie/OpenSeesPy`、`zhuminjie/OpenSeesPyDoc` 及 PyPI 发布包 `openseespy*` 元数据。GitHub/PyPI API 作为第一方发布/仓库元数据端点。
- **固定点**：commit-pinned 引用使用读取时的分支 tip：[OpenSees/OpenSees master 955ceb0](https://api.github.com/repos/OpenSees/OpenSees/commits/master)（2026-10-31）、[zhuminjie/OpenSeesPy openseespy e62f4bc](https://api.github.com/repos/zhuminjie/OpenSeesPy/commits/openseespy)（2026-10-28，同时是 tag `v3.8.0.4`）、[zhuminjie/OpenSeesPyDoc master ce0d8f1](https://api.github.com/repos/zhuminjie/OpenSeesPyDoc/commits/master)（2026-05-20）、[OpenSees/OpenSeesDocumentation master 8a6641e](https://api.github.com/repos/OpenSees/OpenSeesDocumentation/commits/master)（2026-10-23）。PyPI 固定检查 `3.8.0.0` 版本（wheel 上传时间 2026-03-18）。HTML 文档页为实时页面，未由页面本身给出构建 SHA。
- **排除/未做**：未扫描本地父目录找新工程；未把用户所述 `OpenSees3.8.0-x64.exe/` 当作源码工程；未读取 AGENTS.md/CLAUDE.md 等代理上下文文件；未改地图、票、源码、用户配置或 git identity；未修改本仓库分支/commit；未安装/启动商业软件；未运行 build/test/formatter；未评估第三方 MCP 实现或论文（站点搜索曾出现第三方 `opensees-mcp`，按票要求排除，不作为证据）。
- **证据标记**：
  - `[已证实]` = 第一方页面/文件/API 中被直接读取到的文本或元数据；**不代表运行时验证**。
  - `[文档声明]` = 第一方文档明确声明，但本轮未安装/运行/复现。
  - `[推断]` = 由已列事实推导、第一方资料未直接这样说。
  - `[未知]` = 在本次第一方取证范围内没有找到依据，或第一方资料互相冲突且未解决。
  - `[用户给定]` = 用户已确认的本机事实，本轮未重新扫描。

## 3. 主要发现

### 3.1 底层求解器、解释器与未来 MCP 的边界

- `[已证实]` 官方旧 wiki 把 OpenSees 描述为 C++ **软件框架**而不是「一个 code」；「A framework is NOT an executable」，并说多数用户使用 `OpenSees.exe`。同一页列出 `OpenSees.exe`（顺序计算）、`OpenSeesSP.exe`、`OpenSeesMP.exe`（并行），并强调提交给解释器的文件「not input files … You are creating and submitting PROGRAMS」。[S4] [S3] 官方 User 页同样说这些 applications 是扩展了 Tcl 的 interpreters，并链接到 Python 解释器文档。[S3]
- `[已证实]` 现代官方命令文档说 Tcl 与 Python 被扩展了 **IDENTICAL** 新命令、参数相同，差别只是语言写法；命令手册把核心抽象列为 Model Generator / Domain / Analysis / Recorders，其中 Domain 保存当前与上次 commit 状态，Analysis 移动状态，Recorders 负责输出。[S6] [S7]
- `[已证实]` OpenSeesPy 文档首页及其仓库源文件称 OpenSeesPy 是 OpenSees 的 **Python 3 interpreter**，最小脚本用 `import openseespy.opensees as ops`、`ops.wipe()`、`ops.model(...)`、`ops.printModel()`。[S19] [S20]
- `[推断]` 以上资料描述的是**求解器/解释器及其命令**，不是 MCP server。若未来要提供 MCP，MCP 工具/传输/会话/资源映射会是另一层集成代码；第一方资料没有把它定义为 `OpenSees.exe` 或 `import openseespy` 自带能力。此推断由「文档只列解释器/命令」与 §3.7 的 MCP 检索共同得出，不是官方声明。
- `[用户给定]` 本机 `OpenSees3.8.0-x64.exe/` 只是解压安装包，不是 MCP 源码，也不是本轮的新工程。`[已证实]` 官方下载页也把同名下载件描述为「downloaded file once extracted is a folder」，其中 `bin` 文件夹含 `OpenSees.exe`。[S1] 本稿不据此推断该本地目录里还有源码项目。
- `[文档声明]` 旧 wiki 的介绍页使用「community-based, open-source software」「OpenSource」等措辞；但授权事实以 §3.5 的 LICENSE/COPYRIGHT/官方条款为准，不能由标签推断商用或再分发权限。[S4]

### 3.2 路径 A：Tcl / 命令行可执行程序

- `[已证实]` 第一方 wiki「Run OpenSees」列出三种执行方式：交互式在 `OpenSees >` 提示符输入；在提示符用 `source inputFile.tcl` 执行外部 Tcl 文件；在 MS-DOS/Unix 提示符用 **batch mode** `OpenSees inputFile.tcl`。同页要求先把 `OpenSees.exe` 所在目录加入 PATH，并 `cd` 到 tcl 文件所在目录。[S2] `Introduction To Tcl` 说明 `source` 从文件读取 Tcl 命令，像交互输入一样求值；Tcl 还提供变量、`argv`/`argc`、文件 I/O。[S5]
- `[已证实]` commit-pinned C++ 源码与上述 wiki 互相印证：`main()` 调用 `g3TclMain(...)`；`g3TclMain` 把第一个不以 `-` 开头的命令行参数作为 startup script，脚本模式执行 `Tcl_EvalFile`/`EvalFileWithParameters`，随后 `goto done`；若 Tcl 求值失败，把 `errorInfo` 写 stderr 并置 `exitCode = 1`。源码还出现 `-suppressOutput`、`-noHeader` 参数，但用户文档页没有给出完整 CLI flag 契约。[S43] [S44]
- `[已证实]` 官方下载页写明「Current version is: 3.8.0」，「We are only now releasing 64 bit applications」；提供 Windows 64-bit `OpenSees3.8.0-x64.exe`，以及 Mac Intel `x86_64` 与 ARM 两个 tar.gz。页面没有列出 Linux 预编译可执行程序。[S1] 现代 Tcl 安装页说 OpenSees **不包含通常由安装器完成的 PATH 设置**，需要手工改环境变量；下载页可能需要输入 email/注册。[S8] 官方 build 文档则说明源码可用 CMake 在 Windows、MacOS、不同 Linux 上构建，并列出编译器、Python 3.11、Conan 1.x、MUMPS 等依赖。[S9]
- `[文档声明]` 官方 User/Introduction 页列出 `OpenSeesSP.exe`、`OpenSeesMP.exe` 并行解释器；本票未把它们作为独立 MCP 路径评估。[S3] [S4]
- `[未知]` 第一方用户文档未找到：完整 CLI flag 表、stdout/stderr 正式格式、除源码所示外的退出码约定、取消/超时、并发请求、同一进程多租户、Tcl runtime 版本、结果文件沙箱/覆盖规则。源码中的 `-suppressOutput`/`-noHeader` 不足以组成稳定公开 CLI 契约。

### 3.3 路径 B：OpenSeesPy（Python 导入/脚本）

- `[已证实]` PyPI `openseespy 3.8.0.0` 发布页及 JSON 元数据说这是「meta-package that automatically installs the correct platform-specific package」；安装命令 `pip install openseespy`，导入 `import openseespy.opensees as ops`；`requires_dist` 按 `platform_system` 条件依赖 `openseespywin>=3.8.0.0`（Windows）、`openseespylinux>=3.8.0.0`（Linux）、`openseespymac>=3.8.0.0`（Darwin）。[S14] [S15] 文档源文件的最小脚本与导入名一致。[S20]
- `[已证实]` `openseespy 3.8.0.0` 自身的 wheel 是 `py3-none-any`（2792 bytes）；实际平台包分别为：Windows `openseespywin-3.8.0.0-py3-none-win_amd64.whl`（描述明确 Windows x86_64）、Linux `openseespylinux-3.8.0.0-py3-none-any.whl`、macOS `openseespymac-3.8.0.0-py3-none-macosx_13_0_arm64.whl`（描述明确 Apple Silicon/arm64）。三者 `license` 字段均为 `LICENSE.md`。[S15] [S16] [S17] [S18]
- `[已证实]` OpenSeesPy 文档首页源码用替换变量 `|opspy_version| = 3.8.0.0`、`|python_version| = 3.12`；渲染页写「Version 3.8.0.0 is released for Linux, Windows, and Mac (ARM64)!」「Python 3.12 is required.」。[S19] [S20] [S21] 安装文档分别给出 Windows/Linux/Mac 的 `python -m pip install openseespy` / `python3 -m pip install openseespy` / `python3.8 -m pip install openseespy` 和 `--upgrade` 命令；Mac 页单独写「Install Python 3.8」。[S27] [S28] [S29] [S30]
- `[已证实]` 除 `recorder -file` 外，OpenSeesPy 文档列出「Output Commands」并声明这些命令不改变 OpenSees 内部状态；其中包括 `nodeDisp`、`printModel`、`version`、`logFile` 等。`nodeDisp` 官方页给出 Python 例子 `disp1 = nodeDisp(nodeTag,1)`，返回当前节点位移。[S41] [S42] `logFile(filename, '-append', '-noEcho')` 把消息/错误写文件，默认打印到 terminal 或 Jupyter。[S40]
- `[文档声明]` 官方首页把 OpenSeesPy 称为「Python 3 interpreter of OpenSees」，并在 Important 段给出授权声明（见 §3.5）。[S19] [S20] PyPI 描述没有列出「必须同时安装独立 `OpenSees.exe`」；本轮也没有运行验证，因此这一点保持 `[未知]`，不写成结论。

### 3.4 版本、平台、架构与 Python 兼容性：事实与冲突

| 项目 | 第一方证据 | 分类 / 限制 |
| --- | --- | --- |
| Tcl/CLI 可执行程序版本 | 官方下载页：当前 `3.8.0`；Windows 64-bit；Mac `x86_64` 与 `ARM`；未列 Linux 预编译包。[S1] | `[已证实]` 页面状态；CLI 路径不依赖 Python 版本。 |
| OpenSeesPy 发布版本 | PyPI 项目页/3.8.0.0 发布页：`3.8.0.0`；文档首页同版本。[S14] [S48] [S19] | `[已证实]` 发布元数据；OpenSeesPy 仓库另有 tag `v3.8.0` 至 `v3.8.0.4`，最新 tip 是 `v3.8.0.4`，但 PyPI latest 仍为 `3.8.0.0` [S47]；**版本映射未知**。 |
| OpenSeesPy 平台/架构 | 文档首页：Linux、Windows、Mac (ARM64)；Windows 包 `win_amd64`/描述 x86_64；Mac 包 `macosx_13_0_arm64`/描述 Apple Silicon；Linux wheel tag 为 `py3-none-any`，文件名不编码 CPU 架构。[S19] [S16] [S17] [S18] | `[文档声明]` + `[已证实]` 元数据。Intel Mac 的 PyPI 包、Linux CPU 架构未由本次证据确定；Intel Mac 只出现在官方 **可执行程序** 下载页。[S1] |
| Python 兼容性：文档索引 | `sub.txt`：`python_version = 3.12`；首页：「Python 3.12 is required.」[S21] [S19] | `[文档声明]`；本轮未运行验证。 |
| Python 兼容性：PyPI 元数据 | `openseespy 3.8.0.0`：`requires_python >=3.10`；`openseespywin` 与 `openseespylinux`：`>=3.12` 且 Windows classifier 含 Python 3.12；`openseespymac`：`>=3.10`。[S14] [S15] [S16] [S17] [S18] | `[已证实]` 元数据；**与首页、Mac 安装页、build 文档冲突**。 |
| Python 兼容性：其他第一方页面 | Mac 安装页写 Python 3.8 [S30]；官方 build 文档写 Python 3.11，并警告「Python 3.12 or newer is not supported by OpenSeesPy currently. Python 3.10 or older version may work.」[S9]；维护者 `pip/build_pip.py` 在 `openseespy` 分支写 `python_requires='>=3.6'` 且条件依赖为精确版本 [S26]。 | `[文档声明]` / `[已证实]` 源码；这些不是同一发布物/同一上下文，不能据此裁定 wheel 的实际 ABI。 |
| `3.8.0` 与 `3.8.0.0` 的关系 | 官方可执行程序为 `3.8.0`；PyPI/docs 为 `3.8.0.0`；OpenSeesPy 仓库 tag 另有 `v3.8.0`–`v3.8.0.4`。[S1] [S14] [S19] [S47] | `[未知]`：未找到第一方映射说明，不能推断二者同源、同特性或同 commit。 |

**结论性限制（不是选择）**：第一方资料对 Python 版本给出互相冲突的声明；本轮没有安装/导入 wheel，故 Python 3.10/3.11/3.12 的实际可运行性、具体 wheel ABI、Mac Intel 支持、Linux CPU 架构均为 `[未知]`，需要后续在目标环境实测或向维护者确认。

### 3.5 安装、许可证与可再分发限制

- `[已证实]` `OpenSees/OpenSees` 与 `zhuminjie/OpenSeesPy` GitHub 仓库元数据均显示 `License: Other` / `NOASSERTION`，不是 GitHub 自动识别的 SPDX 标准许可证。[S10] [S22] 不能把该标签或 wiki 的「open source」措辞当作授权结论。
- `[已证实]` commit-pinned `OpenSees/OpenSees/COPYRIGHT` 与 `zhuminjie/OpenSeesPy/COPYRIGHT` 的正文一致，核心条款为：UC Regents 版权；教育/研究/非营利实体可在 **noncommercial purposes only** 下 use/reproduction/modification/distribution；其他实体仅可为 **internal purposes only** 做 use/reproduction/modification；所有 copies/modifications 必须保留版权通知及后续段落；把软件纳入 **products for commercial distribution** 需联系 UC Berkeley Office of Technology Licensing 取得许可；无担保、无维护义务、无专利明示许可、研究用途风险自负。[S11] [S25]
- `[已证实]` 官方 `Copyright and License` 文档页给出 1999–2020 版全文，开头概括「free for anybody to use, with the exception being that if you sell software that includes OpenSees source code you must obtain a license」，并额外包含 BSD 风格条款：源码再分发保留通知/条件/免责声明；二进制再分发在文档或随附材料中复现；不得用版权持有人或贡献者名义背书/推广衍生产品。[S12] 旧 copyright 页面则是 1999–2000 措辞，写「Permission to incorporate this software into commercial products may be obtained…」。[S13] **两份官方条款的年份和措辞不完全一致；`docs license.html` 还含 `COPYRIGHT` 文件中没有的 BSD 风格段落。** 本稿不合并、不解释、不给法律意见。
- `[已证实]` OpenSeesPy 文档首页、其 `.rst` 源文件、`pip/README.md` 与 commit-pinned `pip/openseespy/LICENSE.md` 都写明：「OpenSeesPy is free for research, education, and internal use. Commercial redistribution of OpenSeesPy, such as, but not limited to, an application or cloud-based service that uses `import openseespy`, requires a license similar to that required for commercial redistribution of OpenSees.exe.」[S19] [S20] [S23] [S24] 联系对象在文档首页是 UC Berkeley（商业许可细节）/Dr. Minjie Zhu（其他问题），而 `LICENSE.md` 写联系 Dr. Minjie Zhu 获取 commercial licensing details；联系点差异未解决。[S19] [S24]
- `[推断]` 未来若 Hub 以可执行程序、wheel、云服务或应用形式再分发/嵌入 OpenSees/OpenSeesPy，§3.5 条款至少构成需要查证的前置条件；但「Hub 的具体发布方式是否属于 commercial redistribution」「internal use 边界」「是否需单独商业许可」属于法律/权属决策，第一方条款没有替本项目判定，本稿也不判定。
- `[未知]` 是否可把官方 `OpenSees.exe`、Mac/Linux 可执行程序或 PyPI wheel 纳入 Hub 仓库/发布产物；商业 DLL/依赖、密钥、用户本机提供与分发边界；如何处理 GPL-3.0 Hub 与 UC Regents 自定义条款之间的关系；UC Berkeley/维护者是否给出针对本项目的书面许可。以上均需后续 HITL/授权核查。

### 3.6 进程状态、任务隔离与结果文件

- `[已证实]` 命令手册把状态拆为 Domain（模型当前/上次 commit 状态）、Analysis（状态推进）、Recorders（输出），并说解释器命令绑定到 C++ procedure。[S7] OpenSeesPy 输出命令索引明确写「Get outputs from OpenSees. These commands don’t change internal states of OpenSees.」[S41]
- `[已证实]` 现代官方 `wipe` 文档：`wipe()` 清除 domain objects、recorders、analysis objects，把 Domain time 重置为 `0.0`；用于不退出/重启解释器而「start over」，例子包括不同模型使用同一地震动。[S33] OpenSeesPy 文档同样写销毁所有模型/分析/recorders，删除元素、节点、约束、荷载、材料对象。[S37] `wipeAnalysis()` 只销毁 analysis objects，**不**重置 Domain time，**不**改变模型状态，荷载仍活跃；文档还警告命令名不能有空格，否则变成 `wipe`。[S34] [S38]
- `[已证实]` `remove` 文档可 `remove recorders`、`remove recorder $tag`，或删除 element/node/loadPattern/parameter/sp/mp。[S36] `exit()` 文档写「terminate the application, invoking the necessary destructors」，用于确保文件关闭、并行解释器正确 shutdown；旧 wiki 同样说 `exit` 确保 files get closed。[S35]
- `[已证实]` `recorder` 文档说输出可去 screen、files、databases 或 remote processes (TCP/IP)，返回 `>0` tag 或 `-1` 失败。[S31] Node Recorder 文档规定 `-file`/`-xml`/`-binary`/`-tcp` 只能选其一；`-file $filename` 指定输出文件；`-closeOnWrite` 每次写打开/关闭文件，会变慢，但可观察进度，因为典型情况下「files are only written to disk when the operating system feels like it」；示例同时给 Tcl 与 Python 写法。[S32] OpenSeesPy `recorder` 页列出 node/element/envelope/pvd/background/collapse 等 recorderType 及返回 tag。[S39]
- `[已证实]` Tcl/CLI wiki 要求 `cd` 到脚本目录后运行；Tcl 文件 I/O 示例用相对文件名 `tmp.out`。[S2] [S5] 但第一方文档没有给出正式的路径解析、覆盖、权限、沙箱或清理契约；`-closeOnWrite` 与 `exit` 的文件关闭说明是少数明确写出的约束。
- `[推断]` 若未来 MCP 复用一个长驻解释器，第一方资料中唯一清楚的「从头开始」命令是 `wipe()`；若以一次任务一个进程为界，`exit()`/进程结束是文档给出的受控析构和文件关闭路径。两者只是由文档推出的**可能边界**，不是本稿的选择，也不构成并发隔离保证。
- `[未知]` 未找到第一方文档说明：同一解释器内并发任务/线程安全、多租户会话 ID、任务取消/超时、状态快照/恢复、stdout/stderr 正式 schema、CLI 退出码的用户文档（源码仅见 Tcl error → `exitCode=1`）、结果文件 schema、同名文件并发写、相对/绝对路径解析规则、文件清理和保留策略、如何把 recorder 文件映射为 MCP 资源。文档只给命令，不给 MCP 结果契约。

### 3.7 第一方 MCP 检索

- `[已证实]` GitHub API 仓库搜索 `org:OpenSees MCP` 返回 `total_count: 0`；`org:OpenSees "Model Context Protocol" in:readme` 也返回 `total_count: 0`。[S45] [S46] 官方站/命令文档、OpenSeesPy 文档首页与维护者 README 在所查页面中没有定义 MCP tool、transport、session、resource 或 result contract。[S3] [S6] [S7] [S19] [S20] [S22]
- `[未知]` 上述搜索覆盖 GitHub 仓库名/描述/README 与本次列出的文档页，**不证明**整个 OpenSees 生态不存在第三方或未来 MCP；站点搜索出现的第三方 `opensees-mcp` 与论文按票排除，未作技术或许可证评估。第一方是否计划发布 MCP，本次资料未给出答案。
- `[推断]` 因此「未来 MCP」在本阶段只能作为独立集成层来讨论；把 `OpenSees.exe`、`OpenSeesPy` 或本机解压安装包称作「现有 MCP」没有第一方依据。

## 4. 对后续决策的约束和选项（不做选择）

> 下表只把事实转写成**条件约束**和**并列选项**。任何一行都不是 SPEC 条款、推荐、默认或验收标准；也不选择 Python/C#、首批能力或协议。

| 决定相关事实 | 对后续决策的约束 | 并列选项（均非本文选择） | 本文不决定 |
| --- | --- | --- | --- |
| 官方资料只给 Tcl/CLI 解释器与 Python 解释器命令；未给第一方 MCP 契约。[S3] [S4] [S6] [S7] [S19] [S45] [S46] | 未来 MCP 若出现，其工具/传输/状态/结果语义需要另有来源或由后续决策定义；不能写成 OpenSees 自带能力。 | 以 CLI batch mode 为被包裹的求解器入口；以 `import openseespy` 的 Python 进程为被包裹入口；另行评估第三方 MCP；从源码构建自定义入口。 | 选哪条路径、是否新建 MCP、用何种运行时语言、暴露哪些首批能力。 |
| 本机 `OpenSees3.8.0-x64.exe/` 是解压安装包；官方页也说解压后得到 `bin/OpenSees.exe`。[S1] | 该目录不能作为 MCP 源码或源码迁移对象；其作为二进制前置条件的定位仍待定。 | 把官方可执行程序列为用户本机前置条件；把 PyPI 包列为 pip 前置条件；把源码构建列为另一前置条件；三者可分别评估授权。 | 是否纳入/分发二进制、是否移动目录、是否引用本机路径。 |
| 可执行程序 `3.8.0` 与 PyPI `3.8.0.0`、仓库 tag `v3.8.0.4` 并存；Python 版本声明冲突。[S1] [S9] [S14] [S15] [S16] [S17] [S18] [S19] [S21] [S26] [S30] [S47] | 后续任何兼容性承诺都要先固定具体发布物、OS/arch、Python 解释器并实测/确认；不能把「3.8.0 == 3.8.0.0」或「Python 3.12 required」直接写进 SPEC。 | 固定 `OpenSees.exe 3.8.0` 的版本矩阵；固定 `openseespy 3.8.0.0` 与某一 Python 版本；固定源码 tag；或以「用户自备、版本待验」为边界。 | 目标平台、Python/C#、版本承诺、是否支持 Intel Mac/Linux 架构。 |
| UC Regents 自定义版权条款与 OpenSeesPy 商业再分发声明明确存在，且官方页面措辞有差异。[S11] [S12] [S13] [S19] [S20] [S23] [S24] [S25] | 「free/open source」不能当商用/再分发许可；若后续选择分发、嵌入或云服务，授权核查是前置条件，不是实现细节。 | 仅内部使用；由用户本机提供运行时；向 UC Berkeley/维护者取得商业许可；完全不纳入需再分发的二进制；把授权判断交由后续 HITL 票。 | 权属/分发边界、是否商用、联系谁、是否接受条款。 |
| 状态由 Domain/Analysis/Recorders 表达；`wipe`/`wipeAnalysis`/`remove`/`exit` 有明确语义；未找到并发/多租户隔离契约。[S7] [S31] [S33] [S34] [S35] [S36] [S37] [S38] [S39] | 后续若承诺多任务或长驻会话，需要额外定义/验证任务边界；文档本身只支持顺序「start over」和受控退出，不能据此声称并发隔离。 | 长驻解释器 + 任务间 `wipe()`；每任务新进程 + `exit()`/析构；单任务单进程；把隔离契约留待实测/设计。 | 进程模型、并发上限、会话语义、取消/超时、验收方式。 |
| 输出可到文件、XML/binary、TCP、screen/database；`logFile` 写消息；部分命令直接返回值；`exit` 负责关闭文件；无正式结果 schema。[S31] [S32] [S35] [S40] [S41] [S42] | 后续若把结果暴露给用户/MCP，需决定文件生命周期、路径、格式和资源映射；第一方资料只给 recorder/log/query 命令。 | 读取 `-file` 结果文件；使用 TCP/database recorder；使用 `logFile`；使用 `nodeDisp` 等 in-process 返回；自定义后处理。 | 首批输出、结果格式、文件命名、清理/保留、MCP 资源接口。 |
| 第一方仓库搜索未发现 MCP；第三方实现未评估。[S45] [S46] | 不能把「已有官方 MCP」当作已证实事实；也不能把第三方存在/不存在当成本轮结论。 | 后续单独调研第三方 MCP；基于两条求解器路径设计新集成层；等待第一方发布。 | 是否采用第三方、是否造协议、是否开发服务。 |

## 5. 未确定事项 / 仍缺前提

1. **用户/后续票尚未给出的前提**：[首批结构工程场景与 Hub 成功标准是什么](../issues/01-first-workflows.md)、[哪些源码、依赖与产物可以纳入和分发](../issues/05-distribution-boundary.md)、[OpenSees MCP 首批能力应止于哪里](../issues/07-opensees-capability-scope.md)、[一键部署应承诺什么行为与验收结果](../issues/08-deployment-contract.md)；是否选择 Python/C# 或其他运行时语言；是否计划 SaaS/云服务；是否允许把二进制或 wheel 纳入发布物。
2. **版本映射**：官方 `OpenSees 3.8.0` 可执行程序、PyPI `openseespy 3.8.0.0`、OpenSeesPy 仓库 tag `v3.8.0`–`v3.8.0.4` 之间是否同源、同 commit、同命令覆盖，第一方资料未说明。
3. **Python 兼容性冲突未解决**：`3.12 required` vs PyPI `>=3.10`/`>=3.12`、Mac 安装页 `3.8`、build 文档 `3.11` 且警告 3.12 不支持、维护者构建脚本 `>=3.6`。本轮没有安装/导入/运行，不能裁定实际 ABI。
4. **平台/架构缺口**：Linux wheel 的 CPU 架构未由 wheel tag 给出；Intel Mac 是否可用 pip 包未知；Windows ARM/x86、其他 macOS 版本下限（`macosx_13_0_arm64` 以外的支持矩阵）未知；官方可执行程序下载页未提供 Linux 预编译包。
5. **CLI 契约缺口**：用户文档没有完整 flag/stdout/stderr/退出码/取消/超时规范；源码只证明脚本文件模式、部分 flag 与 Tcl error 的 `exitCode=1`。
6. **状态与隔离缺口**：没有第一方并发、多租户、线程安全、会话 ID、快照/恢复、任务取消契约；`wipe()`/`exit()` 不能替代隔离规范。
7. **结果文件缺口**：没有第一方路径解析、覆盖、权限、并发写、文件 schema、清理/保留、MCP 资源映射契约；`-closeOnWrite` 与 `exit` 只覆盖缓冲/关闭的部分行为。
8. **授权缺口**：两个官方版权页面年份/措辞不同；`license.html` 含 BSD 风格段落而 `COPYRIGHT` 文件不含；OpenSeesPy 商业许可联系点在文档首页与 `LICENSE.md` 不同；本项目是否构成 commercial redistribution、能否打包/再分发、与 Hub GPL-3.0 的关系均需人/法务确认。本稿不是法律意见，也未联系权利方。
9. **MCP 缺口**：第一方仓库搜索未发现 MCP，但搜索范围不是全生态穷尽；第三方 MCP 实现/论文未评估；未来 MCP 的工具、传输、资源与验收没有第一方依据。
10. **本机事实边界**：未重新扫描 `OpenSees3.8.0-x64.exe/`，未扫描父目录找工程，未读取代理上下文文件，未检查用户配置；本机实际文件清单、版本、依赖、可执行性均不在本轮证据内。
11. **未运行验证**：未安装、启动、构建、测试、format 或运行任何求解器；所有运行时行为、性能、错误码、输出文件内容都是 `[未知]` 或 `[文档声明]`。

## 6. 可点击第一方引用

| ID | 第一方来源 |
| --- | --- |
| S1 | [OpenSees User Download / 3.8.0 可执行程序分发][S1] |
| S2 | [OpenSeesWiki: Getting Started -- Run OpenSees][S2] |
| S3 | [OpenSeesWiki: OpenSees User][S3] |
| S4 | [OpenSeesWiki: Introduction to OpenSees][S4] |
| S5 | [OpenSeesWiki: Introduction To Tcl][S5] |
| S6 | [OpenSees Documentation: OpenSees Interpreters][S6] |
| S7 | [OpenSees Documentation: Command Manual][S7] |
| S8 | [OpenSees Documentation: Tcl install][S8] |
| S9 | [OpenSees Documentation: Building Application][S9] |
| S10 | [GitHub: OpenSees/OpenSees 源码仓库][S10] |
| S11 | [OpenSees/OpenSees @ 955ceb0: COPYRIGHT][S11] |
| S12 | [OpenSees Documentation: Copyright and License][S12] |
| S13 | [opensees.berkeley.edu: developer/copyright.php][S13] |
| S14 | [PyPI: openseespy 3.8.0.0 发布页][S14] |
| S15 | [PyPI JSON: openseespy 3.8.0.0][S15] |
| S16 | [PyPI JSON: openseespywin 3.8.0.0][S16] |
| S17 | [PyPI JSON: openseespylinux 3.8.0.0][S17] |
| S18 | [PyPI JSON: openseespymac 3.8.0.0][S18] |
| S19 | [OpenSeesPy Documentation: The OpenSeesPy Library][S19] |
| S20 | [OpenSeesPyDoc @ ce0d8f1: index.rst][S20] |
| S21 | [OpenSeesPyDoc @ ce0d8f1: src/sub.txt][S21] |
| S22 | [GitHub: zhuminjie/OpenSeesPy 维护者仓库][S22] |
| S23 | [zhuminjie/OpenSeesPy: pip/README.md][S23] |
| S24 | [zhuminjie/OpenSeesPy @ e62f4bc: pip/openseespy/LICENSE.md][S24] |
| S25 | [zhuminjie/OpenSeesPy: COPYRIGHT][S25] |
| S26 | [zhuminjie/OpenSeesPy: pip/build_pip.py][S26] |
| S27 | [OpenSeesPy Documentation: PyPi (Windows, Linux, Mac)][S27] |
| S28 | [OpenSeesPy Documentation: PyPi (Windows)][S28] |
| S29 | [OpenSeesPy Documentation: PyPi (Linux)][S29] |
| S30 | [OpenSeesPy Documentation: PyPi (Mac)][S30] |
| S31 | [OpenSees Documentation: recorder Command][S31] |
| S32 | [OpenSees Documentation: Node Recorder][S32] |
| S33 | [OpenSees Documentation: wipe Command][S33] |
| S34 | [OpenSees Documentation: wipeAnalysis Command][S34] |
| S35 | [OpenSees Documentation: exit Command][S35] |
| S36 | [OpenSees Documentation: remove Command][S36] |
| S37 | [OpenSeesPy Documentation: wipe command][S37] |
| S38 | [OpenSeesPy Documentation: wipeAnalysis command][S38] |
| S39 | [OpenSeesPy Documentation: recorder command][S39] |
| S40 | [OpenSeesPy Documentation: logFile command][S40] |
| S41 | [OpenSeesPy Documentation: Output Commands][S41] |
| S42 | [OpenSees Documentation: nodeDisp Command][S42] |
| S43 | [OpenSees/OpenSees @ 955ceb0: SRC/tcl/tclMain.cpp][S43] |
| S44 | [OpenSees/OpenSees @ 955ceb0: SRC/tcl/tclAppInit.cpp][S44] |
| S45 | [GitHub API: org:OpenSees MCP repository search][S45] |
| S46 | [GitHub API: org:OpenSees "Model Context Protocol" in:readme search][S46] |
| S47 | [GitHub API: zhuminjie/OpenSeesPy tags][S47] |
| S48 | [PyPI: openseespy project/latest][S48] |

[S1]: https://opensees.berkeley.edu/OpenSees/user/download.php
[S2]: https://opensees.berkeley.edu/wiki/index.php/Getting_Started_with_OpenSees_--_Run_OpenSees
[S3]: https://opensees.berkeley.edu/wiki/index.php/OpenSees_User
[S4]: https://opensees.berkeley.edu/wiki/index.php/Introduction_to_OpenSees
[S5]: https://opensees.berkeley.edu/wiki/index.php/Introduction_To_Tcl
[S6]: https://opensees.github.io/OpenSeesDocumentation/user/interpreters.html
[S7]: https://opensees.github.io/OpenSeesDocumentation/user/userManual.html
[S8]: https://opensees.github.io/OpenSeesDocumentation/user/tclInstall.html
[S9]: https://opensees.github.io/OpenSeesDocumentation/developer/build.html
[S10]: https://github.com/OpenSees/OpenSees
[S11]: https://raw.githubusercontent.com/OpenSees/OpenSees/955ceb0a55f7b5764856ea82fc9a9cc7f07a1eea/COPYRIGHT
[S12]: https://opensees.github.io/OpenSeesDocumentation/developer/license.html
[S13]: https://opensees.berkeley.edu/OpenSees/developer/copyright.php
[S14]: https://pypi.org/project/openseespy/3.8.0.0/
[S15]: https://pypi.org/pypi/openseespy/3.8.0.0/json
[S16]: https://pypi.org/pypi/openseespywin/3.8.0.0/json
[S17]: https://pypi.org/pypi/openseespylinux/3.8.0.0/json
[S18]: https://pypi.org/pypi/openseespymac/3.8.0.0/json
[S19]: https://openseespydoc.readthedocs.io/en/latest/index.html
[S20]: https://raw.githubusercontent.com/zhuminjie/OpenSeesPyDoc/ce0d8f1ded3c722119c44d5b3a2073c9dce47828/index.rst
[S21]: https://raw.githubusercontent.com/zhuminjie/OpenSeesPyDoc/ce0d8f1ded3c722119c44d5b3a2073c9dce47828/src/sub.txt
[S22]: https://github.com/zhuminjie/OpenSeesPy
[S23]: https://github.com/zhuminjie/OpenSeesPy/blob/openseespy/pip/README.md
[S24]: https://raw.githubusercontent.com/zhuminjie/OpenSeesPy/e62f4bc82b1e2c67d2675962184e820aa93a865f/pip/openseespy/LICENSE.md
[S25]: https://raw.githubusercontent.com/zhuminjie/OpenSeesPy/openseespy/COPYRIGHT
[S26]: https://raw.githubusercontent.com/zhuminjie/OpenSeesPy/openseespy/pip/build_pip.py
[S27]: https://openseespydoc.readthedocs.io/en/latest/src/pypi.html
[S28]: https://openseespydoc.readthedocs.io/en/latest/src/pypiwin.html
[S29]: https://openseespydoc.readthedocs.io/en/latest/src/pypilinux.html
[S30]: https://openseespydoc.readthedocs.io/en/latest/src/pypimac.html
[S31]: https://opensees.github.io/OpenSeesDocumentation/user/manual/output/recorder.html
[S32]: https://opensees.github.io/OpenSeesDocumentation/user/manual/output/NodeRecorder.html
[S33]: https://opensees.github.io/OpenSeesDocumentation/user/manual/misc/wipe.html
[S34]: https://opensees.github.io/OpenSeesDocumentation/user/manual/misc/wipeAnalysis.html
[S35]: https://opensees.github.io/OpenSeesDocumentation/user/manual/misc/exit.html
[S36]: https://opensees.github.io/OpenSeesDocumentation/user/manual/misc/remove.html
[S37]: https://openseespydoc.readthedocs.io/en/latest/src/wipe.html
[S38]: https://openseespydoc.readthedocs.io/en/latest/src/wipeAnalysis.html
[S39]: https://openseespydoc.readthedocs.io/en/latest/src/recorder.html
[S40]: https://openseespydoc.readthedocs.io/en/latest/src/logFile.html
[S41]: https://openseespydoc.readthedocs.io/en/latest/src/outputcmds.html
[S42]: https://opensees.github.io/OpenSeesDocumentation/user/manual/misc/nodeDisp.html
[S43]: https://raw.githubusercontent.com/OpenSees/OpenSees/955ceb0a55f7b5764856ea82fc9a9cc7f07a1eea/SRC/tcl/tclMain.cpp
[S44]: https://raw.githubusercontent.com/OpenSees/OpenSees/955ceb0a55f7b5764856ea82fc9a9cc7f07a1eea/SRC/tcl/tclAppInit.cpp
[S45]: https://api.github.com/search/repositories?q=org%3AOpenSees+MCP&per_page=100
[S46]: https://api.github.com/search/repositories?q=org%3AOpenSees+%22Model+Context+Protocol%22+in%3Areadme&per_page=100
[S47]: https://api.github.com/repos/zhuminjie/OpenSeesPy/tags?per_page=20
[S48]: https://pypi.org/project/openseespy/
