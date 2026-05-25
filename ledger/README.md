# ledger

一个用于创建、记录、跟踪、更新任务清单与任务状态台账的 skill。

`ledger` 的职责不是写交接文档，而是维护一个**可持续更新、可审计、可回流**的任务状态面板，用于跟踪 todo list、todo item、主线 / 分支任务状态、优先级、阻塞项和下一步行动。

## 适用场景

适用于以下类型的请求：

- 创建 todo list
- 新增 todo item
- 更新任务状态
- 调整优先级
- 记录 blocker
- 指定下一步行动
- 跟踪主线 / branch 的任务分配
- 归档完成项
- 汇总当前任务面板
- 在 Relay Mesh 中记录 main relay / branch relay 对应的任务状态

常见说法包括：

- “创建一个 todo list”
- “加一个新的 todo”
- “更新这个 todo”
- “把这个任务标成 blocked”
- “看看当前 todo list”

## 不适用场景

`ledger` 默认不负责：

- 替代 `relay` 写上下文交接文档
- 复制长篇聊天记录
- 记录完整调试日志全文
- 代替 PRD / ADR / 计划正文

如果用户需要交接上下文，优先使用 `relay`；
如果用户需要追踪任务状态，优先使用 `ledger`。

## 核心模型

`ledger` 维护两层对象：

1. **todo list**：任务容器
2. **todo item**：任务条目

它默认既要保持稳定字段语义，也要兼顾便于人类扫读的 Markdown dashboard 视图。

## 典型价值

使用 `ledger` 可以：

- 统一记录任务状态
- 让主线 / 分支任务更清晰
- 标准化 blocked / next / priority 等字段
- 降低长期任务推进中的信息漂移
- 为后续 agent 提供可引用的状态台账

## 与其他 skill 的区别

- `relay`：负责上下文与知识接力
- `ledger`：负责任务与执行状态台账

如果用户需要“下个 session 怎么继续”，优先 `relay`；
如果用户需要“当前有哪些任务、各自状态如何”，优先 `ledger`。

## 仓库文件说明

- `SKILL.md`：技能主文档与详细执行规则
- `README.md`：公开仓库入口说明

## 版本

版本以 `SKILL.md` frontmatter 中的顶层 `version` 字段为准。
