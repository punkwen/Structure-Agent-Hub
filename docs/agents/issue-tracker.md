# Issue tracker: Local Markdown

本仓库使用本地 Markdown tracker。Wayfinder 地图、决策票及结论以本仓库文件为准，不以 skills 安装目录中的模板为配置。

## Conventions

- 每个 effort 使用 `.scratch/<effort>/`；地图为 `map.md`，子票为 `issues/NN-<slug>.md`，编号从 `01` 开始。
- 标题是人类可读名称；正文引用使用 `[标题](相对路径)`，不使用裸编号代替名称。
- 地图与票只使用 `wayfinder:` 标签。地图为 `Labels: wayfinder:map`；子票为 `Labels: wayfinder:<type>`，另用 `Type:` 记录 `research`、`prototype`、`grilling` 或 `task`。
- `.scratch/` 当前未被 `.gitignore` 忽略；它是可版本化的 tracker，不按临时垃圾处理。每次 commit 均须 push；不得顺带提交无关改动。

## Wayfinding operations

### Map and children

- 地图正文使用 `Destination`、`Notes`、`Decisions so far`、`Not yet specified`、`Out of scope` 五个段落。
- 地图只索引已经关闭的票，不列开放票。子票以 `Parent: ../map.md` 归属地图。
- 子票元数据为 `Type:`、`Labels:`、`Mode:`、`Status:`、`Assignee:`、`Blocked by:`。`Mode: HITL` 表示须与人共同解决，`Mode: AFK` 表示可由代理独立处理；开放且未领取时使用 `Status: open`、`Assignee: unassigned`；无阻塞使用 `Blocked by: none`。
- 决策问题放在 `## Question`；调查材料和原型只放链接，不将答案预写进问题正文。

### Blocking and frontier

- 本地 Markdown 没有原生依赖关系；`Blocked by:` 用逗号分隔阻塞票的两位编号。编号是机器引用，人类正文仍使用标题链接。
- 阻塞票全部为 `Status: resolved` 时，该票无阻塞。因超出范围而关闭使用 `Status: closed-out-of-scope`，移除或改接受影响的依赖，不把它伪装成已解决的决策。
- 查询前沿：扫描同一 effort 的 `issues/`，取 `Status: open`、`Assignee: unassigned` 且无未解决阻塞的票；按编号升序选择。仅加载地图与前沿元数据，按需读取票的全文。

### Claim and resolution

- 开始处理前先保存 `Status: claimed` 与 `Assignee: <驱动该 effort 的开发者>`；认领是开始工作的第一项写入。
- 处理票时读取 `Type:`，并加载地图 Notes 指定的 skill。HITL 票必须通过真实的人类交流解决。
- 结论记录在票末尾的 `## Answer`（本 tracker 的 resolution comment），必要的过程交流追加在 `## Comments`；随后设置 `Status: resolved`。
- 在地图 `Decisions so far` 追加一行 `[票的标题](issues/NN-slug.md#answer): 一行概要`。详细决定只保存在票中。
- 建图时先创建地图和全部可明确提问的票，再进行第二遍链接与阻塞接线；初始 `Decisions so far` 为空。不在建图会话解决 HITL 票。

### Research assets

- 每张研究票使用独立 `research/<name>` 分支，将有来源的发现写在该分支的研究文件中，push 但不创建 PR，也不合并。
- 票记录分支、提交和研究文件的可访问链接；研究结论可以在建图阶段解决，其他类型每个会话最多解决一张。
- 若研究分支因无法访问远端等真实前置条件无法发布，票保留 claimed/open 并明确阻塞原因，不宣称研究已交付。
