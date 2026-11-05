# OpenSees MCP 首批能力应止于哪里

Type: grilling
Labels: wayfinder:grilling
Mode: HITL
Status: resolved
Assignee: punkwen
Blocked by: 01,04,06
Parent: ../map.md

## Question

对已选任务，OpenSees MCP 首批需暴露哪些用户可观察能力与输出，采用哪条有证据的集成路径、哪些人工/运行前置要求、如何验收，哪些能力明确不属于首批？不在此实现。

参考票：[首批结构工程场景与 Hub 成功标准是什么](01-first-workflows.md)、[OpenSees 有哪些可用的集成路径与运行约束](04-opensees-integration-evidence.md)、[仓库如何组织，Skill 与 MCP 如何分工](06-repository-skill-boundary.md)。

## Answer

用户于 2026-11-06 确认（「Q1-openseespy，其余按推荐」→「Q6'–Q10 按推荐」）以下首批边界。本票是 planning-only 的 HITL 决策票：本轮未开发 MCP/Skill、未写 SPEC 正文、未安装或运行 OpenSeesPy、未搬迁工程、未部署客户端。以下是规划要求，不代表已有实现。

### 1. 集成路径与输入工件

- 首批只采用 **OpenSeesPy** 路径：用户自备 Python 解释器，脚本 `import openseespy.opensees as ops`。
- 输入工件是 **Python 脚本**，不是 Tcl deck。MCP 不解析、不生成、不转换 Tcl，不包裹 `OpenSees.exe`。
- Tcl/CLI 入口不属于首批；04 已证实两条入口互斥。
- 后果：候选 Skill `opensees-tcl-expert` 产出 Tcl，与本 MCP 不配套；其索引（13/14）不构成 OpenSeesPy 能力。OpenSeesPy 专用 Skill 属新增内容，不在本票范围。

### 2. 首批用户可观察能力

- **(a) 只读检视**：读取用户给定的 Python 脚本文件与目录内容，不执行。
- **(b) 隔离执行**：新建运行目录，以子进程执行脚本；返回运行目录路径、目录内产物清单（路径/大小，以目录枚举为准，不要求脚本额外声明）、合并日志（stdout+stderr 按行交织）、exit code（仅记录）。
- 排除：结构化建模工具（节点/单元/材料/荷载）与结果文件 schema 解析/后处理。前者与 Skill 职责重复且 06 不预造统一抽象；后者需先有第一方结果 schema，而 04 未找到。

### 3. 完成判据（防假绿）

- marker 由 **MCP 自己的 runner** 发出：`runner.py` 以 `runpy.run_path` 执行用户脚本，脚本无异常返回后才打印 ASCII marker `TGC_DONE` 并 exit 0；异常则打印 traceback、不打印 marker、exit 1。
- 判据：日志出现 `TGC_DONE` 才算「脚本无异常跑到结尾」；未出现即失败，即使 exit 0。`SystemExit(0)` 视为完成，`SystemExit(非 0)` 视为失败。
- **marker 不等于求解成功**：`ops.analyze()` 返回负值、OpenSees `WARNING` 只打印不抛异常时，runner 仍会发 marker。因此 MCP 必须原样回传日志中的 OpenSees `Error`/`WARNING` 行，不得把 marker 表述为「求解成功」；求解断言由脚本/Skill 负责。
- exit code 与 traceback 仅作附加信号，不与 marker 等价。
- 之所以不由用户脚本手写 marker：会造成作者漏写时的假阴性，也会让 marker 退化成脚本自证成功；Python 异常本就会传播，wrapper 判完成更可信。CLI 的末行 marker 纪律来自 Tcl 吞错，不适用于此路径。

### 4. 进程、隔离与部分失败

- 每次执行新建独立运行目录；子进程 CWD = 运行目录（recorder 相对路径落在 CWD）。
- 每次一个全新子进程，串行；不并发、不复用长驻解释器、不跨任务保持状态。
- 超时：杀掉进程，如实报告已产生的输出、运行目录与未知状态；不声称回滚。
- 部分失败：报告已执行内容、产物路径与未知状态；没有依据不得声称已回滚。

### 5. 人工确认与安全

- 每次执行前逐次确认（沿用 01）：展示目标脚本路径、运行目录与已知影响；技术强制手段未定，属 12。
- 输入脚本只读，不修改。
- 产物只写入运行目录；不覆盖运行目录外的已有文件。
- 运行时缺失或无法 import 即停并报告，不猜路径、不回退到其他解释器、不自动安装。

### 6. 运行前置

- 用户自备 Python 解释器与可 import 的 `openseespy`；MCP 只检测，不安装/升级，不再分发（05）。
- 本票不承诺版本：精确发布物与解释器版本由 09 实测钉死；本票只要求「可导入，版本以 09 结论为准」。
- 候选事实（2026-11-06 本机）：CPython 3.12.9 为唯一解释器、无 venv；`openseespy` 未安装；numpy 2.5.2 已装。04 记录 PyPI `openseespy 3.8.0.0` 的 win 包要求 ≥3.12，但官方文档/构建页对 3.12 的支持声明互相冲突，均未实测。

### 7. 验收

- 一个最小可复查正例：悬臂或门式刚架，解析解为参照，容差事先声明；脚本自带求解断言，runner 发 marker。
- 两个负例：脚本抛异常（无 marker，判失败）；`openseespy` 不可导入（明确失败并报告解释器路径与 import 错误）。
- 不计入 01 的五例核心门槛；通过只证明该实例在该环境的工作流可用，不等于结构安全或替代工程师判断。
- 具体参照数值与容差由 09 给出运行时事实后选定。

### 8. 明确不属于首批

- Tcl/CLI 入口与 Tcl deck。
- 结构化建模工具；结果文件 schema 解析、后处理与绘图。
- 并发、多租户、长驻解释器/会话、任务取消语义（首批只有超时杀进程）。
- 自动安装/升级/打包/分发 OpenSees 或 OpenSeesPy。
- `OpenSeesSP`/`OpenSeesMP` 并行入口。
- 非 Windows 平台的支持承诺（无运行证据）。
- GUI 与云服务化。

### 9. 与其他票的关系

- 新开 [OpenSees MCP 的仓库起源与首发基线如何确定](15-opensees-mcp-repository-origin.md)；10 的票面限定五个现有 MCP，不能容纳新仓库。
- 09 的核验对象据此变为「Python 解释器 + `openseespy` 可导入性」，不再是 exe/wheel/tag 的版本映射。
- 08 依赖本票的能力与前置边界。

### 10. 未决定 / 未验证

- 未安装、未运行 OpenSeesPy；脚本能否跑通任何求解未知。
- `TGC_DONE` 之外能否从日志可靠识别 OpenSees `Error`/`WARNING` 行，未实测；09 须覆盖，否则「marker + 日志扫描」仍可能失明。
- 工具命名、MCP 传输、超时值、运行目录位置、日志上限等实现细节不在本票。

## Comments

- 2026-11-06 第一轮：用户选择 Q1 = OpenSeesPy，覆盖推荐 ①（CLI batch）；Q2–Q5 按推荐（首批能力 a+b、逐次确认、单进程串行、不计入核心门槛且独立仓库）。
- 2026-11-06 复核指正：上一轮把 exit code 当成功判据错误。本机同 build（`3.8.0 64-Bit 6e552935`）实测：正常 deck 与含 `invalid command name` 的 deck 均 `exit 0`；`1>/dev/null` 后 banner、`puts`、报错仍在 → 全部输出走 stderr，stdout 为空。该事实只说明 CLI 的 exit code 不可作判据，不适用于 OpenSeesPy 子进程。
- 2026-11-06 第二轮：用户确认 Q6'–Q10（runner 发 marker；运行目录 + 产物清单 + 合并日志；检测不安装；新建独立仓库；一正两负验收）。runner 语义用本地纯 Python 验证：`runpy.run_path` 无异常 → marker；异常 → traceback 且无 marker；`SystemExit(0)` 算完成，`SystemExit(非 0)` 算失败。
