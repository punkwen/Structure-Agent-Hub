# 核验选定 OpenSees 运行路径的版本兼容性

Type: task
Labels: wayfinder:task
Mode: AFK
Status: resolved
Assignee: punkwen
Blocked by: 05,07
Parent: ../map.md

## Question

本票是未来决策的前置核验，不是 MCP 实现任务。前置已满足：[哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md) 明确运行时由用户自备、不再分发；[OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer) 选定 OpenSeesPy 路径（用户 Python 解释器 + `import openseespy.opensees`，输入为 Python 脚本，不包裹 `OpenSees.exe`）。

核验目标（单一目标环境：本机 Windows x64 + 已装 CPython 3.12.9）：

1. 记录实际解释器版本与路径；`openseespy` 的安装来源、精确版本、实际 wheel 文件名与平台 tag（如 `win_amd64`）、元数据 `requires_python` 与该解释器是否匹配，以及 `import openseespy.opensees` 是否成功；错误原样记录。
2. 跑一个最小模型（如悬臂或门式刚架）并读取一次输出，记录输入、输出与错误证据；对照 [OpenSees 有哪些可用的集成路径与运行约束](04-opensees-integration-evidence.md) 所述版本/Python 兼容性冲突，裁定其在该环境是否成立。
3. 核实 [OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer) 标为推断的运行时行为：`ops.analyze()` 失败时的返回与日志表现、OpenSees `Error`/`WARNING` 行能否从合并日志可靠识别、recorder 相对路径是否落在进程 CWD。

只核验该单一目标，不遍测未知平台、不改 MCP/Skill、不把失败当成功；下载/许可等前提缺失时明确记录并保持阻塞。结果作为 [一键部署应承诺什么行为与验收结果](08-deployment-contract.md) 可用性承诺与 [OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer) 验收参照的事实，不替人选择支持范围。

## Answer

2026-11-06 在本机单一目标环境实测完成（AFK）。结论只覆盖该环境；未遍测其他平台/解释器，未改 MCP/Skill，未做结果解析。证据脚本与原始输出在 [09-runtime-evidence/](09-runtime-evidence/)；`runner_probe.py` 按 [OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer) 的 runner 语义执行（`runpy.run_path` + 独立状态文件 + 子进程 CWD = 运行目录）。

### 1. 解释器与安装物

- 解释器：`C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe`，`3.12.9 (tags/v3.12.9:fdb8142, Feb 4 2025, 15:27:58) [MSC v.1942 64 bit (AMD64)]`，`Windows-10-10.0.19045-SP0`，无 venv（`sys.prefix == sys.base_prefix`），numpy 2.5.2，pip 26.3。证据：[runs/import_meta/interpreter.txt](09-runtime-evidence/runs/import_meta/interpreter.txt)。
- 安装前 `openseespy` 不存在：`importlib.util.find_spec('openseespy')` 返回 `None`，`pip show openseespy` 报 `Package(s) not found`。该检查发生在安装前，输出只在本会话终端，未单独落盘。
- 为完成本票核验，执行 `python -m pip install openseespy` 装入该全局解释器（无 venv）；同一命令前把 pip 从 24.3.1 升到 26.3（升级前版本号来自本会话输出，未落盘）。两处系统改动，未安装其他包。
- 实际安装物（`pip download` 取回的 wheel 与 PyPI JSON 一致）：

| 发行物 | wheel 文件名 | tag | `Requires-Python` | 大小 | SHA-256 |
|---|---|---|---|---|---|
| `openseespy`（元包） | `openseespy-3.8.0.0-py3-none-any.whl` | `py3-none-any` | `>=3.10` | 2,792 B | `ce6a43503b737025f763a87bebacb1cc2fbd82a156982647e9e014a11b85fdbd` |
| `openseespywin`（Windows 二进制） | `openseespywin-3.8.0.0-py3-none-win_amd64.whl` | `py3-none-win_amd64` | `>=3.12` | 6,787,016 B | `ee0f48317582641cf06347fe0babd34a230823b56397603c9b5b2d3b96089b73` |

- 元包 `requires_dist` 按平台选子包（Windows → `openseespywin>=3.8.0.0`）；`openseespywin` 无依赖。安装后 `openseespywin/opensees.pyd` 为 17,206,272 B，`RECORD` 记录 `sha256=JbpC4WclJhN9dl2cNjHRQD4JH1T1r825JC-SQ8Y8OpY`。证据：[runs/install_meta/install.txt](09-runtime-evidence/runs/install_meta/install.txt)。
- `import openseespy.opensees` 成功，`ops.version()` 返回字符串 `"3.8.0"`；导入与 `version()` 均不打印 banner（CLI 的 banner 行为不适用于 OpenSeesPy）。无 import 错误可记录。证据：[runs_probe_import.txt](09-runtime-evidence/runs_probe_import.txt)。
- 3.12.9 同时满足元包 `>=3.10` 与 Windows 子包 `>=3.12`，元数据不阻塞安装。注意 wheel 是 `py3-none-win_amd64` 而非 `cp312-cp312-win_amd64`：pip 只校验 `Requires-Python` + 平台，**可安装不等于可导入**；本票只证明 3.12.9 可导入，不证明 3.13+ 可用。

### 2. 最小模型与输出

- 输入：[cantilever.py](09-runtime-evidence/cantilever.py) —— 2 节点 3D 弹性梁悬臂，SI 单位 `E=2.0e11 Pa`、`I=0.2*0.2^3/12=1.3333e-4 m^4`、`L=2 m`、`P=1000 N`，解析解 `PL^3/(3EI)=1.0e-4 m`，容差事先声明为 `1e-9 m`，脚本自带断言。
- 输出：`analyze_rc 0`，`node2_disp2 -9.999999999999996e-05`（解析值 `-9.999999999999998e-05`），`ANALYTIC_CHECK_OK`；recorder 文件 `disp.out` 内容 `1 -0.0001`。证据：[runs/cantilever/run.txt](09-runtime-evidence/runs/cantilever/run.txt)、[runs/cantilever/disp.out](09-runtime-evidence/runs/cantilever/disp.out)、[runs/cantilever/.tgc-run-status.json](09-runtime-evidence/runs/cantilever/.tgc-run-status.json)（`TGC_DONE`）。
- 对 [OpenSees 有哪些可用的集成路径与运行约束](04-opensees-integration-evidence.md) 所述冲突的裁定（仅限本环境）：该票记录的「官方文档/构建页对 Python 3.12 的支持声明互相冲突」在本机被实际 import + 求解证伪（具体 build 页措辞见该票链接的研究资产，不在票面）；元包 `>=3.10` 与 Windows 子包 `>=3.12` 的元数据不一致真实存在，但对 3.12.9 无影响。文档冲突本身未消解，不能据此推断其他版本。

### 3. [OpenSees MCP 首批能力应止于哪里](07-opensees-capability-scope.md#answer) 标为推断的运行时行为

**(a) `ops.analyze()` 失败时的返回与日志**

- 静力求解失败返回**负整数且不抛异常**：奇异矩阵 `-3`、不收敛 `-1`；stderr 出现 `OpenSees > analyze failed, returned: -3 error flag` 一类行。证据：[runs/analyze_failure/run.txt](09-runtime-evidence/runs/analyze_failure/run.txt)、[runs/analyze_failure_extra/run.txt](09-runtime-evidence/runs/analyze_failure_extra/run.txt)。
- 未定义 analysis 类型时 `ops.analyze()` **抛** `opensees.OpenSeesError: See stderr output`，stderr 只有 `WARNING No Analysis type has been specified`。证据：[runs_probe_analyze_failure_stderr.txt](09-runtime-evidence/runs_probe_analyze_failure_stderr.txt)。
- 反例：带质量但无单元约束的节点导致 `FullGenLinLapackSolver::solve() -factorization failed, matrix singular`，`analyze()` 却返回 **0**，且没有 `analyze failed` 行（[runs/analyze_failure_extra/run.txt](09-runtime-evidence/runs/analyze_failure_extra/run.txt)）。因此**返回值也不是成功判据**。
- 经 runner 路径确认：`analyze()` 返回 `-3` 的脚本仍写 `TGC_DONE`（[runs/analyze_failure/.tgc-run-status.json](09-runtime-evidence/runs/analyze_failure/.tgc-run-status.json)）。该票「marker 不等于求解成功」成立。

**(b) `Error`/`WARNING` 行能否从合并日志可靠识别**

- 不能按 token 可靠识别。OpenSees 自身消息主要走 **stderr**，但格式不统一：
  - 有前缀：`WARNING ...`、`ERROR ndm msut be 1, 2 or 3`（原文含拼写错误）。
  - 无前缀：`ndm must be 2 and ndf must be 3`、`insufficient number of arguments`、`Domain::addNode - node with tag 1 already exists in model`、`UniaxialMaterial *getUniaxialMaterial(int tag) - none found with tag: 99`。
  - 多条 WARNING 可**不带换行**拼接：`WARNING DisplacementControl::domainChanged() - zero reference loadStaticAnalysis::setAlgorithm() - ...`，行首锚定的 `^WARNING` 扫描会漏掉后两条。
  - 通道不唯一：LAPACK/Fortran 消息走 **stdout**（`** On entry to DGBSV  parameter number  9 had an illegal value`），见 [runs/crash/stdout.txt](09-runtime-evidence/runs/crash/stdout.txt) 与 [runs/crash/stderr.txt](09-runtime-evidence/runs/crash/stderr.txt)。
- 证据：[runs/error_lines/run.txt](09-runtime-evidence/runs/error_lines/run.txt)、[runs_probe_error_lines_stderr.txt](09-runtime-evidence/runs_probe_error_lines_stderr.txt)、[runs_probe_error_token_stderr.txt](09-runtime-evidence/runs_probe_error_token_stderr.txt)、[runs_probe_error_token_stdout.txt](09-runtime-evidence/runs_probe_error_token_stdout.txt)。
- 结论：MCP 只能原样回传合并日志，不能声称「已识别全部 OpenSees 错误」，也不能把 marker 表述为求解成功；求解断言必须留在脚本/Skill。

**(c) recorder 相对路径**

- 落在**子进程 CWD**：`-file disp.out` 生成在运行目录（子进程 CWD），调用方目录没有该文件；脚本内 `os.getcwd()` 即运行目录。证据：[runs/cantilever/run.txt](09-runtime-evidence/runs/cantilever/run.txt) 首行与 [runs/cantilever/disp.out](09-runtime-evidence/runs/cantilever/disp.out)。

**(d) 合并日志的顺序（附带核验）**

- 子进程 stdout/stderr 指向同一 fd 时，**只有子进程无缓冲**才按真实顺序交织。默认重定向到文件时 `sys.stdout` 为 `write_through=False`（块缓冲），Python print 推迟到进程退出才 flush，日志里 OpenSees stderr 会整体排在脚本 print 之前（[runs/ordering_default/run.txt](09-runtime-evidence/runs/ordering_default/run.txt)）；子进程带 `PYTHONUNBUFFERED=1` 时顺序正确（[runs/ordering_u2/run.txt](09-runtime-evidence/runs/ordering_u2/run.txt)）。缓冲标志对照：[runs/bufcheck_default.txt](09-runtime-evidence/runs/bufcheck_default.txt)、[runs/bufcheck_u.txt](09-runtime-evidence/runs/bufcheck_u.txt)。即：不显式无缓冲启动时，「按行交织」不成立，日志顺序不代表执行顺序。本机 shell 预设了 `PYTHONUNBUFFERED=1`，早期探针因此误判，已用 `env -u` 复测纠正。
- **新发现的风险**：`ops.integrator("NoSuchIntegrator")` 只打印 WARNING，随后 `analyze()` 触发 LAPACK 错误，**进程直接退出、exit code 0、状态文件未写、脚本后续行未执行**。证据：[runs/crash_harness.txt](09-runtime-evidence/runs/crash_harness.txt)（`child_exit_code 0`、`status_file MISSING`）、[runs/crash/child_log.txt](09-runtime-evidence/runs/crash/child_log.txt)。因此「状态文件缺失」必须判为失败/未知，不能按 exit code 0 判成功。

### 4. 未覆盖 / 不构成结论

- 未测其他 Python 版本、其他平台、Tcl/CLI 入口、`OpenSeesSP`/`OpenSeesMP`、并发、结果文件解析。
- 未做授权结论。安装物自带 `LICENSE.md` 原文称「Commercial redistribution of OpenSeesPy ... requires a license similar to that required for commercial redistribution of OpenSees.exe」；这是事实记录，分发边界仍以 [哪些源码、依赖与产物可以纳入和分发](05-distribution-boundary.md#answer) 为准。
- 本票不选择支持范围；[一键部署应承诺什么行为与验收结果](08-deployment-contract.md) 可据此把「3.12.9 + openseespy 3.8.0.0」作为已验证组合，其他组合仍无证据。
