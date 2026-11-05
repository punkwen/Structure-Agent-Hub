# 现有结构专业 Skill 的来源与公开引用条件（证据研究）

> 本文件是 wayfinder research 票[现有结构专业 Skill 的来源与公开引用条件是什么](../issues/13-existing-skills-provenance.md)的证据稿，**不是 SPEC**。只记录 `F:/DotNetProgram/tigerkin-skills` 的来源、版本、权利、依赖与历史事实及未知项；不构成公开再分发许可、法律意见或能力声明；不替用户选择索引范围（该选择属[哪些现有结构专业 Skill 可以纳入 Hub 索引](../issues/14-existing-skills-index-scope.md)）。

- 取证日期：**2026-11-06**，全部为本机只读静态取证；未修改 tigerkin-skills 任何文件，未运行/安装/构建任何软件。
- 版本锚点：`master` @ `c244fda622650715c8269784535e256a74b54a8b`（提交信息 `auto: tigerkin-skills 2026/07/27 周一  4:38:14.61`，2026-07-27T04:38:14+08:00）。工作树干净：`git status --porcelain` 为 0 项；`StructureDev/` 与 `skills/structure-software-dev/` 下无未跟踪/忽略文件。全仓 18 个提交。
- 远端 `https://gitee.com/punkwen/tigerkin-skills.git` 的**公开可见性未能核实**：本环境匿名访问网页返回 403（含浏览器 UA 亦然）、Gitee API v5 返回 404（"Not Found Project"）、`git ls-remote` 需要凭据。按票面要求不提供公开链接，下文以本地路径 + 提交哈希引用。

## 1. 问题

票面三问：(a) `StructureDev` 下 12 个 Skill 的候选清单与相关性；(b) 仓库根同名 12 项的 `skills/structure-software-dev/` 与之谁为准、差异何在；(c) 索引所需的来源/权利/依赖/历史证据与未知项。

## 2. 取证范围与方法

- 只读 git 查询（`rev-parse`/`log`/`ls-files`/`status`/`show` 等）与文件读取；无写入。
- 副本比较：对每个 Skill 目录内全部文件按相对路径排序做 SHA-256 聚合指纹，比较两树；差异者再逐文件 diff。
- 历史扫描：`git log --all --diff-filter=A/D --name-only` 全量文件名清单，按扩展名与关键词（厂商二进制、凭据、zip）筛查；`.s2k` 按 UTF-16/UTF-8/GBK 依次解码后检索 `LicenseNum=`。
- 权利检索：全部跟踪文件查 `SPDX`、`Copyright`、`版权`、常见许可文本；frontmatter 查 `license` 字段。
- 明确未做：未对 2,582 个文件逐字通读（结构化统计 + 定向抽样）；未验证任何运行时；未联系权利方；未评估 Gitee 平台条款。
- 方法偏差（如实记录）：大小写不敏感检索 `mcp` 的两处命中均为假阳性（`BeamCPXS` 函数名含子串 `mCP`；`.skill` 二进制 zip 的随机字节命中），解包逐项复核后确认 0 处真实 MCP 引用。

## 3. 两份副本的判定（先于候选清单）

仓库根同时存在 `StructureDev/`（12 个 Skill，2,582 个跟踪文件，144M）与 `skills/structure-software-dev/`（同名 12 项，同为 2,582 个跟踪文件，144M）。逐文件指纹比较结论：**两者不是两份独立来源，而是同一批内容经一次整树复制的两份检出，且 `skills/structure-software-dev/` 是唯一包含全部后续修订的一份**。

| 维度 | `StructureDev/` | `skills/structure-software-dev/` |
|---|---|---|
| 首次入库 | `238afda1`（2026-05-08 "321"，一次性加入 12 项中的多数） | `17d7b1c2`（2026-07-21 "add"，一次性整树加入） |
| 最后一次内容提交 | `f34371f9`（2026-07-01） | `17d7b1c2`（2026-07-21） |
| 内容差异 | — | 2 个 SKILL.md 含更新的描述文本；etabs 目录结构已扁平化并新增顶层 SKILL.md |
| `.skill` 打包件 | etabs 一份 | etabs 同一份（SHA-256 `353c22b8…` 完全一致） |

逐项差异（共 3 项，其余 9 项两树内容完全一致）：

1. **`dtl-model/SKILL.md`**：`skills/` 份的 description 补充了 `（dtlmodel.ydb）` 文件名；3 处小节标题从「附录 4.3/4.1.1/4.5」改为「dtlModel补.md 附录 …」，与其引用的文档名一致。`docs/dtlModel补.md` 两树逐字节一致。
2. **`yjk-dsnmodel/SKILL.md`**：`skills/` 份 description 从「dsnModel 数据库结构专家」改为「提供dsnModel.ydb文件的表结构查询…」，补充了具体文件名。`references/dsnmodel_data_reference.md` 两树逐字节一致。
3. **`etabs-api-function`**：`StructureDev/` 份多一层同名嵌套目录 `etabs-api-function/etabs-api-function/`（SKILL.md 在嵌套层，顶层只有 `docs/`、打包件、嵌套目录）；`skills/` 份已扁平化为标准布局（顶层 `SKILL.md` + `references/` + `docs/` + 打包件）。两份 `references/**`（130 个文件：128 个分接口文档 + 2 个索引）内容逐字节一致；SKILL.md 内容亦一致（同为 9,969 B，CRLF；与打包件内版本差异仅为行尾归一）。`skills/` 份是结构化整理后的版本。

版本考古：`17d7b1c2` 的文本变更（`dtlModel补.md 附录`、`dsnModel.ydb文件的表结构`）只存在于 `skills/` 份的路径下，`StructureDev/` 全历史从未含这些文本——即修订发生在复制之后、只落在 `skills/` 份。**本票全部结论指向 `skills/structure-software-dev/`**；`StructureDev/` 应视为陈旧副本（其继续存在属于仓库卫生问题，本票只记录不处置）。

## 4. 候选清单（`skills/structure-software-dev/` 下 12 项）

每项给出 git 树哈希（版本锚点）与相关性判断。相关性以[仓库如何组织，Skill 与 MCP 如何分工](../issues/06-repository-skill-boundary.md#answer)的「与 StructureDev 相关、可能进入 Hub 索引」为口径；「相关」不等于「可索引」——权利与许可未知者仍须排除。

| Skill | 树哈希 (`HEAD:skills/structure-software-dev/<n>`) | 文件数 | 相关性 | 依据与未知项 |
|---|---|---|---|---|
| `opensees-tcl-expert` | `cf86185368f2fb8a62bd33993905c42dc969f8c0` | 536 | **相关（高）** | OpenSees Tcl 脚本生成/修改 + OpenSeesPy 命令文档集；与[OpenSees MCP 首批能力应止于哪里](../issues/07-opensees-capability-scope.md#answer)的 OpenSeesPy 路径直接相关。但其能力形态（产出 Tcl 脚本）与 07 票「候选 opensees-tcl-expert 因产出 Tcl 不配套」的既定结论冲突，能否纳入属 14 票决策。第三方材料占比高（见 §6）。 |
| `sap2000-api` | `656e09b5b79e6f86be433e68f23652cf0e15ddc5` | 1,818 | **相关（高）** | SAP2000 OAPI 函数参考（`docs/**` 1,817 个 md）；与 SAP2000 MCP 同软件域。全部 doc 文件无任何版权/许可文本（见 §6），来源未能从内容本身确认。 |
| `etabs-api-function` | `3afd2e33d56d46a50750d3535d249e90386f4820` | 133 | **相关（高）** | ETABS v1 OAPI 参考（126 接口/2,652 方法）+ CSI 版权声明 128 处；与 ETABS MCP 同软件域。 |
| `yjk-modeling-api` | `632237cb6debb95ff87c8699c7c0aeac65955c70` | 22 | **相关（高）** | YJK DataFunc/CsToYjk 建模 API + 18 个 C# 示例；与 YJK MCP 同软件域。文档疑似厂商材料（见 §6）。 |
| `yjk-modeling-foundation-api` | `1e59f03b957efd2527145b9da47550a6f48b8e21` | 6 | **相关（高）** | YJK 基础建模/后处理 API；文档自述来源于 `https://gitee.com/yjk-opensource`（厂商开源组织，访问未核验）。含 `agents/openai.yaml`（OpenAI 界面清单，非 MCP）。 |
| `yjk-runtime-api-function` | `62309be4ed36c02aba18ef55c5743df2e6ac02e0` | 10 | **相关（高）** | YJK C# 运行时 API；references 疑似厂商头文件/文档摘录（见 §6）。 |
| `yjk-runtime-api-post-function` | `8475e624e766b26566f7f139e422a25bfbc1fa26` | 5 | **相关（高）** | YJK 设计结果后处理 P/Invoke；`reference/设计结果接口说明_new.md` 为 C++ 头文件直出文本（`//dsnPro.h`），厂商材料特征明显。 |
| `yjk-dsnmodel` | `e386743216efc9f8cd967b5dfd038a1de974ef87` | 2 | **相关（中）** | dsnModel.ydb 318+ 表参考；reference 文件含 259 处 `media/` 图片引用但仓库内无 `media/` 目录（引用全部悬空），存在 pandoc 转换痕迹（8,834 处 `{width=…}`）。 |
| `dtl-model` | `f42b04d01426dab2c93d55dfac7fe3c13c71e8b2` | 2 | **相关（中）** | dtlModel（dtlmodel.ydb）表结构参考；与 yjk-dsnmodel 同类。 |
| `sap2000-s2k-expert` | `db032c04e5a281606ca38d3bf72382aa2e13a098` | 38 | **相关（条件）** | .s2k 文件格式手册 + 36 个真实 .s2k 示例模型；手册为自研分析成果，但示例文件含 SAP2000 许可证号与疑似真实工程数据（见 §6.4），纳入前须逐文件脱敏审查。 |
| `midas-api` | `619293792ce5fdce088c2a1b7acbf009f4cb8966` | 2 | **相关（条件）** | MIDAS NX REST API 端点目录；SKILL.md 为自研编写，references 指向官方在线手册 URL。权利干净度较高，但与五个 MCP 中 MIDAS 的覆盖关系由 14 票判断。 |
| `3d3s-expert` | `f46f3117956f63e357fbb2c0547e8fac15191b1f` | 8 | **相关（低/存疑）** | 3D3S 文本交换格式关键字参考 + 6 个 .3d3s 样例模型。3D3S 不在五个 MCP 之列；样例含第三方导出标记（`Euler2025 SR10`、`Grida R2025`），来源未知。 |

无关项（不属于本票候选，仅登记存在）：`skills/` 其余 5 类（lbt-dev 20 项 Ladybug/Honeybee、office 7、personal 5、program-dev 2、rhino-grasshopper-dev 5）及仓库根 `DIY/`、`General/`、`LBT/`、`Obsidian/`、`RhinoGHDev/`、`TigerkinClaw/`、`tigerkinforghmax/`、`mattpocock-skills-zh-CN-main/`。其中 `TigerkinClaw/`（6 个 YJK/AutoCAD 工作流 Skill）与 `Obsidian/llm-wiki-yjk-out-check`（YJK 输出审查）在主题上与结构专业相邻，但不在票面圈定的 `StructureDev` 口径内，本票不展开取证；若 14 票需要，应另行取证。

## 5. 来源与版本锚点

- **单一版本锚点**：`skills/structure-software-dev/` @ `c244fda622650715c8269784535e256a74b54a8b`（2026-07-27）。各 Skill 树哈希见 §4 表。全部内容来自本机私有仓库；按票面要求不提供公开链接。
- **作者与身份**：18 个提交的作者名有 3 种写法（`punkwen` 8 次、`q475832547` 9 次、`文志彬` 1 次），**邮箱全部为 `475832547@qq.com`**；与 Hub 仓库的提交身份相同。这是 git 元数据证据，不是权利声明。
- **事实证据与授权声明的区分**：本节全部为 git/文件系统事实。任何"该仓库由我创建/我拥有其内容"的第一方权属主张属于用户声明，本票未收集此类声明；14 票确认权属时须将其与这里的 git 证据对账（作者一致 ≠ 著作权归属）。
- **远程可访问性**：Gitee 远端匿名不可见（见文件头）；本地凭据可 fetch/push。公开引用条件的一部分（"公开链接是否可行"）因此**未知**，标 `NOASSERTION`。

## 6. 权利与许可

### 6.1 仓库整体

- 仓库根与 `skills/structure-software-dev/` 下**无 LICENSE/COPYING/NOTICE 文件**（唯一的 `General/html-ppt/LICENSE` 在无关目录）。README.md/en 是 Gitee 模板占位文本，无许可声明。
- 全部 24 个 SKILL.md frontmatter 只有 `name`/`description`，**无一含 `license` 字段**。
- 仓库根 `.gitignore` 不存在（仅 `mattpocock-skills-zh-CN-main/.gitignore`）；`.omc/state/`（本地 Agent 会话状态，含用户名 `wenzhibin`、历史路径 `I:\DotNetProgram\…`）被跟踪入库——属个人信息入库，登记为发布前须清除项。

### 6.2 第三方权利人与标记（逐 Skill）

| Skill | 第三方材料 | 权利人证据 | 许可文本 | 判定 |
|---|---|---|---|---|
| `etabs-api-function` | `docs/CSI_API_ETABS_v1.md`（249,961 行，自称 "Converted from CHM"）+ `references/docs/**`（128 个分接口文档）+ `.skill` 打包件内同内容 | 明确：Computers and Structures, Inc. (CSI)；133 个文件中 128 个含 "Copyright © Computers and Structures, Inc. 2025. All rights reserved."，5 个例外为 `.skill` 包、`SKILL.md`、`00_Namespace.md`、两个索引 | **无许可文本**；仅版权声明 | 第三方材料成立，权利人明确；**再分发条款未知 → `NOASSERTION`**。CSI OAPI 文档随软件授权分发，默认保留所有权利。 |
| `sap2000-api` | `docs/**` 1,817 个 md（VB6 风格 OAPI 函数参考，含 `SAP2000v1.dll`、`Computers and Structures` 路径/示例） | 内容证据强烈指向 CSI 源（OAPI 文档特征），但**无版权声明** | 无 | 权利人**推断**为 CSI，未经证实 → 权利人 `NOASSERTION`、许可 `NOASSERTION`。1,818 个文件无一含许可文本。 |
| `opensees-tcl-expert` | (a) `OpenSeesCommandLanguageManual.md`：Berkeley PEER 手册（Silvia Mazzoni, Frank McKenna, Michael H. Scott, Gregory L. Fenves et al., v1.7.3, 2006）的**中文编译本**（1390 行）；(b) `openseespy/**` 534 个 md：OpenSeesPy 官方文档（Sphinx `noindex` 标记 317 个；155 个文件含 `opensees.berkeley.edu` wiki 链接）的本地复制 | (a) UC Regents/PEER 作者明确；(b) OpenSees 社区文档，权利人未在文件内声明 | (a) 无；(b) 无（仅 3 个文件提及 Qt license 与 LICENSE.rst 的存在，非本仓文件） | 两类均为第三方材料：权利人 (a) 明确 (b) 推断；许可一律 `NOASSERTION`。OpenSees 官方许可措辞冲突问题另见[OpenSees 有哪些可用的集成路径与运行约束](../issues/04-opensees-integration-evidence.md#answer)，文档材料的再分发权未被该票覆盖。 |
| `yjk-modeling-api` | `docs/建模接口说明.md`（厂商接口文档特征）+ 18 个 ConsoleApp `.cs` 示例 | 无声明；SKILL.md 自述对应盈建科 DLL | 无 | 权利人 `NOASSERTION`（厂商材料推断，未证实）。 |
| `yjk-modeling-foundation-api` | `docs/*.md` 4 个；其一自述来源 `https://gitee.com/yjk-opensource`（厂商开源组织） | 组织名明确，仓库/条款未核验 | 无 | 权利人 `NOASSERTION`；上游 gitee 组织的许可条款**未核验**。 |
| `yjk-runtime-api-function` | `references/*.md` 9 个（API 说明 + 宏定义，`design-result-macros-full.md` 等为宏清单） | 无声明 | 无 | `NOASSERTION`。 |
| `yjk-runtime-api-post-function` | `reference/设计结果接口说明_new.md`（C++ 头文件直出，含 `//dsnPro.h`）+ `设计结果宏定义.md` + 2 个 `.cs` 脚本 | 无声明 | 无 | `NOASSERTION`；头文件直出文本是厂商 SDK 材料特征。与[哪些源码、依赖与产物可以纳入和分发](../issues/05-distribution-boundary.md#answer) §9 的「反编译 YJKAPI.dll」指示项同类风险。 |
| `yjk-dsnmodel` / `dtl-model` | 数据库表结构参考（厂商数据库 schema 文档特征） | 无声明 | 无 | `NOASSERTION`。 |
| `sap2000-s2k-expert` | `docs/sap2000_s2k_manual.md` 自述"基于对多个 .s2k 文件的分析"整理（疑似用户自撰，无声明）；`exapmle/**` 36 个 .s2k 为外部模型文件 | 手册：疑似用户自撰（无声明）；模型：原工程作者未知 | 无 | 手册权利人 `NOASSERTION`（待用户声明）；模型文件见 §6.4。 |
| `midas-api` | SKILL.md + `references/midas-api-endpoints.md` 均为自研编写；后者引用官方在线手册 URL | 未做与官方手册的逐字比对，无直接复制证据 | 无 | 相对干净；仍待用户权属声明确认。 |
| `3d3s-expert` | `docs/dddsss.md`（关键字格式整理）+ `res/**` 6 个 .3d3s 模型（含 `Euler2025 SR10`、`Grida R2025`、`TigerKinPro` 导出标记） | 无声明 | 无 | 文档 `NOASSERTION`；模型文件来源未知。 |

### 6.3 汇总

12 个 Skill 的随附文档全部**无 SPDX 标识、无许可文本、无许可声明字段**。唯一的明确权利证据是 ETABS 文档的 128 处 CSI 版权声明。其余权利人主张均为内容特征推断，一律 `NOASSERTION`。**没有任何一项当前满足"可公开引用/再分发"的许可条件。**

### 6.4 敏感内容登记（不复制内容，仅登记位置）

- **SAP2000 许可证号**：`skills/structure-software-dev/sap2000-s2k-expert/exapmle/` 下 36 个 .s2k 中 **26 个含 `LicenseNum=` 字段**，8 个不同取值（5 位 × 16 文件、20 位 × 10 文件，计数分布 16/4/1×6）。按[哪些源码、依赖与产物可以纳入和分发](../issues/05-distribution-boundary.md#answer) §5，许可证号/激活信息永不发布；这些文件在公开任何历史前须脱敏或排除。
- **疑似真实工程数据**：s2k 文件名含项目性质名称（`医院1-ZJ`、`小学3-QG`、`A-47轴sap模型`、`中震-混凝土无阻尼器` 等）与缩写后缀（-ZJ/-JB/-QG），文件头含保存时间戳；3d3s 样例含 `Euler`/`支架` 等项目名。是否为真实在建/已建工程数据未知 → 标 `NOASSERTION`，纳入前须逐文件审查。
- **个人信息**：`.omc/state/hud-stdin-cache.json` 含 Windows 用户名与历史本机路径（I: 盘）；登记见 §6.1。

## 7. 依赖

- **MCP 依赖：0 处。** 两树全部跟踪文件对 `mcp`/`tgk-` 的检索只有 2 处假阳性（`BeamCPXS` 函数名、`.skill` 二进制随机字节），解包复核后为 0。没有任何 SKILL.md 声明依赖某个 MCP server、工具名或版本；frontmatter 只有 `name`/`description`。按[仓库如何组织，Skill 与 MCP 如何分工](../issues/06-repository-skill-boundary.md#answer) §4 的"声明实际需要的 MCP"要求，这些 Skill 目前**没有可核对的 MCP 依赖声明**（既非"无依赖"的证明，也非"有依赖"的证据）。
- **文本声明的软件前提**（静态阅读，均未运行验证）：
  - `sap2000-api`/`etabs-api-function`：SAP2000/ETABS 本体与 COM/.NET OAPI（`SAP2000v1.dll`、`ETABSv1.dll` 由用户自备）。
  - YJK 六项：YJK 安装与 `CsToYjk.dll`/`APIData.dll`/`DataFuncApplication.dll`/`YJKDesign.dll`，以及 `yjks_csload`/`yjks_csreload` 加载机制。
  - `midas-api`：`localhost:10084` 的 MIDAS API 服务。
  - `opensees-tcl-expert`：无运行时（纯文档）；`3d3s-expert`/`dtl-model`/`sap2000-s2k-expert`/`yjk-dsnmodel`：文件格式类，无运行时。
- **随附数据文件即运行依赖**：技能正文显式引用各自 `docs/`/`references/`/`res/`/`exapmle/`；`yjk-dsnmodel` 引用的 259 张图片缺失（功能性缺陷，非权利问题）。
- **客户端清单**：仅 `yjk-modeling-foundation-api/agents/openai.yaml`（`display_name`/`default_prompt`）；其余 11 个无 manifest。未验证任何客户端实际加载行为。

## 8. 可访问历史

- 18 个提交；内容窗口最早观察到 `238afda1`（2026-05-08），HEAD `c244fda6`（2026-07-27）；仅 `master` 分支、无 tag。多数提交为 `auto:`/`update` 类快照提交。
- **厂商二进制：0。** 全历史新增文件扫描无 `.dll`/`.exe`/`.pyd`/`.lic`/`.pfx`/`.pem`/`.nupkg` 等厂商二进制或凭据类文件（全仓 0 处）。
- 历史与当前树中的第三方/敏感内容（仅报存在性与位置，不复制内容）：
  - `mattpocock-skills-zh-CN-main.zip`（`9f393282` 加入）与同名目录：MIT 第三方 skill 集；
  - `Obsidian/update/llm-wiki-isolation-report-review/reference/reference_bundle.zip`（65 项）与 `llm-wiki-outofcode-report-review/reference/reference_bundle.zip`（143 项，`3467a906` 加入）：中文结构工程书籍/文章/规范文档集合（条目名含《SAP2000 中文版技术指南》、《ETABS结构设计实例详解》、朱炳寅著作、GB 50011 应用分析等）→ 第三方版权材料；
  - `StructureDev/sap2000-s2k-expert/exapmle/*.s2k` 的 `LicenseNum=`（`238afda1` 起存在于当前树与全部后续历史）；
  - `.omc/state/` 两个含本机用户名/路径的缓存文件；
  - 已删除的 `StructureDev/yjk-runtime-api-post-function.skill`（69,788 B zip，`6ddf0c6e` 删除）对象仍可从历史取回。
- 上述内容是否构成"公开暴露"取决于 Gitee 仓库可见性（文件头：未能核实）；若仓库可公开访问，则以上各项现已在公网可见。本票不据此断言合规或不合规。

## 9. 仓库根内嵌的第三方内容（不属于可索引 Skill 范围）

- `mattpocock-skills-zh-CN-main/`（108 文件）+ `mattpocock-skills-zh-CN-main.zip`（187,343 B）：`github.com/mattpocock/skills` 的简体中文本地化（README 自述由 `vinvcn/mattpocock-skills-zh-CN` 维护），`LICENSE` = MIT（Copyright (c) 2026 Matt Pocock）；zip 与目录 108/108 逐字节一致。→ 参考件，不属于 Hub 可索引 Skill。
- 两个 Obsidian `reference_bundle.zip`（§8）：书籍/规范文章集合，权利 `NOASSERTION` → 不属于可索引 Skill；若公开历史含它们，须按[哪些源码、依赖与产物可以纳入和分发](../issues/05-distribution-boundary.md#answer) §8 审查。
- `RhinoGHDev/`（14,289 文件，`gh-api`/`rhino-api` 等）：McNeel Rhino/Grasshopper API 文档导出（文件名含 `License…` 者均为 API 文档页，非许可文本）→ 第三方衍生，不在本票范围，仅报存在。
- `LBT/`（Ladybug Tools honeybee/ladybug 系）、`General/`、`TigerkinClaw/`、`Obsidian/` 其余、`skills/` 其余五类：超出本票 `StructureDev` 范围，未逐项审，仅报告存在；其中 `TigerkinClaw/yjk-*` 等结构相关条目若未来要纳入，须另行取证。

## 10. 对后续决策的约束与并列选项（不选择）

- 索引若指向 `skills/structure-software-dev/<name>`，版本锚点可固定为 `17d7b1c2`（或 HEAD `c244fda6`）；`StructureDev/` 不再作为来源。此为证据判定，最终范围由[哪些现有结构专业 Skill 可以纳入 Hub 索引](../issues/14-existing-skills-index-scope.md)确认。
- 公开发布前须逐项解决的阻断清单（事实，非结论）：CSI ETABS/SAP2000 文档再分发权缺失（SAP2000 连声明都被剥离）、YJK 厂商头文件原文、OpenSees PEER 手册译文与 OpenSeesPy 文档导出、s2k 样例 `LicenseNum=`（票 05 §5 直接禁止发布）、3d3s 模型文件来源、两个第三方 zip、`.omc` 个人数据、Gitee 可见性核实。
- 若 Hub 仅做私有/内部索引（不公开、不复制），票 06 的"只索引"路径不触发上述再分发问题，但仍须满足票 06 的"来源、权利、依赖、可访问历史审计"要求——本票提供了该审计的事实层，权利层缺用户声明。
- 并列选项（由票 14 决定）：(a) 全部 12 项候选待审后逐项确认；(b) 先纳入自编成分明确、无第三方衍生正文的条目；(c) 全部暂不索引直到权利补齐。本票不选。

## 11. 明确不声称

- 本票不构成公开再分发许可；不声称 `GPL-3.0-only` 覆盖 tigerkin-skills 或其内含材料（[哪些源码、依赖与产物可以纳入和分发](../issues/05-distribution-boundary.md#answer) 的第一方确认只覆盖五个 MCP）。
- 不声称任何 Skill 的技术能力、可用性或与任何客户端的兼容性；所有依赖为静态文本阅读。
- 所有 `NOASSERTION` 是"未知/未取证"标记，不是许可，也不是侵权认定。
- Gitee 公开可见性未核实；历史内容仅报存在性，不构成合规判断。

## 附录 A：两份副本逐 Skill 内容指纹（SHA-256 聚合，前 16 hex）

| Skill | `StructureDev/` | `skills/structure-software-dev/` | 一致 |
|---|---|---|---|
| 3d3s-expert | bcf556242a2c74ce | bcf556242a2c74ce | ✓ |
| dtl-model | fd291bd7d7300f6e | 9f13023de60bb82e | ✗（SKILL.md 文本） |
| etabs-api-function | 76b434a0bc23e654 | d57bb10d02162c72 | ✗（布局扁平化） |
| midas-api | 86b7b80c29bf1d90 | 86b7b80c29bf1d90 | ✓ |
| opensees-tcl-expert | a63d29ebb8d3965c | a63d29ebb8d3965c | ✓ |
| sap2000-api | 59a3b387732d965b | 59a3b387732d965b | ✓ |
| sap2000-s2k-expert | 5f7fcd78370d7f2e | 5f7fcd78370d7f2e | ✓ |
| yjk-dsnmodel | 5cfb42800abc401b | 1356718a3877f253 | ✗（SKILL.md 文本） |
| yjk-modeling-api | 6bdb82a7035c5789 | 6bdb82a7035c5789 | ✓ |
| yjk-modeling-foundation-api | d8f16622e6b29e75 | d8f16622e6b29e75 | ✓ |
| yjk-runtime-api-function | 2057fe971e24df88 | 2057fe971e24df88 | ✓ |
| yjk-runtime-api-post-function | 3c3825ca4670211e | 3c3825ca4670211e | ✓ |

指纹方法：对目录内全部跟踪文件按相对路径排序，逐文件 `sha256sum` 后对结果整体再取 SHA-256；覆盖工作树内容（两树均干净，等于 HEAD 内容）。
