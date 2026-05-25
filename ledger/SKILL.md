---
name: ledger
description: 当用户需要创建、记录、跟踪、更新任务清单、todo list、todo item、主线/分支任务状态、优先级、阻塞项、下一步行动或进行任务归档时使用。适用于长期任务管理、Relay Mesh 协作、main relay / branch relay 派发与回收、阶段性推进、状态审计和任务收束。用户层对象仍使用 todo list / todo item，自然语言可直接说“创建一个 todo list”“加一个 todo”“更新这个 todo”。
argument-hint: 这次要创建或更新的 todo list / todo item 的重点是什么？
type: productivity
author: Roy <qsunyi@qq.com>
version: 1.2.2
---

# Ledger

## Purpose

Ledger 是面向任务状态管理的台账 skill。

它不是普通的聊天总结，也不是 relay 的替代品。它的职责是：

- 创建 todo list；
- 记录 todo item；
- 跟踪任务状态；
- 更新优先级、阻塞、下一步行动；
- 在 Relay Mesh 中维护 main / branch 任务的状态账本，默认集中在一个主 TODO.md 中；
- 为后续 agent 提供可审计、可引用、可回流的任务状态面板。

一句话理解：

- `relay` 负责上下文与知识接力；
- `ledger` 负责任务与执行状态台账。

## User-facing language

虽然 skill 名叫 `ledger`，但用户层对象仍然使用自然语言：

- `todo list`
- `todo item`
- `todo`

因此用户可以自然地说：

- “创建一个 todo list”
- “加一个新的 todo”
- “更新这个 todo”
- “把这个任务标成 blocked”
- “看看当前 todo list”

不要强迫用户改口去说“ledger item”或“ledger entry”，除非在结构化说明里确实有必要。

## When to use

当用户需要以下动作时使用：

- 创建任务清单；
- 新增 todo 项；
- 更新 todo 项状态；
- 调整优先级；
- 记录 blocker；
- 指定下一步行动；
- 跟踪某个主线或 branch 的任务分配；
- 对完成项进行归档；
- 汇总当前任务面板；
- 在 Relay Mesh 中记录 main relay / branch relay 对应的任务状态。

## Non-goals

Ledger 默认不负责：

- 替代 relay 写上下文交接文档；
- 复制长篇聊天记录；
- 承担详细调试日志全文；
- 生成项目计划正文、PRD 正文或 ADR 正文。

如果用户需要交接上下文，优先使用 `relay`；
如果用户需要追踪任务状态，优先使用 `ledger`。

## Core model

Ledger 维护两层对象：

1. **todo list**：任务容器；
2. **todo item**：任务条目。

## Display mode

Ledger 应同时维护两层表达：

1. **Canonical structure**：稳定字段与任务状态语义；
2. **Human-facing view**：便于日常扫读的 Markdown dashboard 视图。

默认情况下，写入项目级 `TODO.md` 时，优先采用 **Human-facing view**，除非用户明确要求更详细的结构化格式。

### View policy

- 项目级默认视图优先面向人类扫读，而不是面向程序序列化；
- 默认使用 Markdown dashboard 风格，而不是原始字段堆叠视图；
- 当任务进入 blocked、merge-back、archive 或需要精确审计时，可临时增加更详细字段；
- 不要让默认视图长期过载。

## Default visual style

项目级 `TODO.md` 默认采用以下视觉风格：

### 1. 顶部使用概览区

固定使用：

- `## 🧭 Overview`

概览区优先放：

- Project
- Type
- Focus
- Main relay

不要在概览区堆太多字段。

### 2. 主线与子线分区

默认使用：

- `## 🔷 Main`
- `## 🌿 Branches`

如果当前项目没有 branch，可仅保留 Main。

### 3. 任务使用卡片头格式

默认使用：

```md
### [-] T-02 · 任务标题
```

规则：

- 状态符号放最前面；
- task id 紧跟其后；
- 标题保持简短；
- 用 `·` 分隔 ID 与标题。

### 4. summary 使用 quote block

例如：

```md
> summary: 已完成第一轮盘点，下一步收束建议。
```

规则：

- summary 应尽量控制为 1 句话；
- 用于快速扫读；
- 不替代 `next`；
- 不写成长段落。

### 5. branch 信息提升到卡片头区域

对于 branch task，建议把 branch 与 summary 一起放在 quote block 中：

```md
> branch: `structure-audit`
> summary: ...
```

### 6. 默认展示字段顺序固定

推荐顺序：

1. `next`
2. `priority`
3. `blocker`
4. `relay`
5. `parent`（仅子任务）
6. 其他必要字段

### 7. 空状态区块默认折叠

对于以下区块：

- Blocked
- Done
- Dropped
- Archived

当区块为空时，默认省略，除非用户明确要求显示完整状态面板。

### 8. Relay Mesh Links 单独成区

默认使用：

- `## 🔗 Relay Mesh Links`

用于集中呈现：

- main relay
- branch relay 映射
- 尚未拆出 relay 的 branch 说明

### 9. Notes 保持轻量

默认使用：

- `## 📝 Notes`

只放规则性说明与少量约束，不重复任务正文。

### 10. Legend 放在底部

默认使用：

- `## 🧩 Legend`

例如：

- `[ ]` todo
- `[-]` doing
- `[!]` blocked
- `[x]` done
- `[~]` dropped
- `[>]` archived

### Visual consistency rules

- 同一份 `TODO.md` 中，任务卡片格式必须保持一致；
- 不要混用旧字段堆叠风格与新卡片头风格；
- 除非用户明确要求，否则优先使用 dashboard 视图。

## Update hygiene

当更新现有 `TODO.md` 时，优先 patch 已有卡片，而不是追加一份新的字段块。

### Patch rules

- 优先原位更新已有任务卡片；
- 不要重复添加已存在字段；
- 如果卡片中已存在以下字段，则应修改原字段，而不是再次插入：
  - `branch`
  - `summary`
  - `next`
  - `priority`
  - `blocker`
  - `relay`
  - `parent`
- 保持字段顺序稳定，不要在同一张卡片中来回变换顺序；
- 除非用户明确要求重写整张卡片，否则不要用“追加新字段块”的方式更新同一任务。

### Merge-back update rules

当 branch task merge-back 到 main 时，建议按以下顺序更新：

1. 先更新 branch relay，使其包含结论、建议与 merge-back 指向；
2. 再更新 main relay，吸收 branch 的结论；
3. 最后更新 `TODO.md` 中对应任务的状态、summary 与 next；
4. 如果任务进入 done：
   - 优先保留原卡片并更新状态符号；
   - 优先将 `next` 改为后续增量维护说明；
   - 如需增加 Done 区块，只写简短汇总，不要复制整张卡片。

### Duplicate prevention

- 不要让同一张卡片出现重复的 `branch:`、`summary:` 或其他核心字段；
- 不要同时保留两份互相冲突的同任务描述；
- 如果自动 patch 失败，宁可重写单张卡片，也不要留下重复字段。

### Recommended statuses

第一版统一使用以下状态：

- `todo`
- `doing`
- `blocked`
- `done`
- `dropped`
- `archived`

说明：

- `dropped`：明确不再继续，但保留记录；
- `archived`：已完成或已结束的条目被归档后使用。

### Required fields for each todo item

每个 todo item 至少应包含：

- `id`
- `title`
- `status`
- `priority`
- `next_step`
- `blocker`
- `related_relay`
- `branch`
- `note`

### Strongly recommended fields

建议尽量包含：

- `created_at`
- `updated_at`
- `owner`
- `depends_on`
- `completion_criteria`
- `archive_reason`

## Task ID policy

每个 todo item 必须分配一个稳定、简短、唯一的 task ID。

### Default format

默认使用：

- `T-01`
- `T-02`
- `T-03`

### Mesh-aware format

如果当前任务明显属于某个 Relay Mesh，可使用带前缀格式：

- `CHK-01`
- `CHK-02`
- `SCRAPE-01`
- `NOTE-01`

其中前缀应与 relay 的 `mesh-prefix` 尽量保持一致。

### ID rules

- ID 一旦分配，默认不再改名；
- title 可以修改，但 ID 应保持稳定；
- relay 与 ledger 之间的交叉引用优先使用 task ID；
- 不要只靠 title 做关联。

## State change and audit trail

Ledger 不是一次性待办清单，而是任务状态账本。

因此每次关键状态变更，至少应记录：

- 新状态；
- 变更原因；
- 更新时间；
- 如果适用，变更人与分支。

### Minimum change note format

例如：

- `blocked — 缺少 API key，等待用户提供`
- `doing — branch relay 已派发到 RELAY-checkout-login-redirect.md`
- `done — 已修复并通过 smoke test`

### Optional changelog

如果任务较复杂，建议为条目维护轻量 changelog，例如：

- `2026-05-24: status todo -> doing, 开始由 checkout 分支处理`
- `2026-05-24: status doing -> blocked, 缺少 staging token`
- `2026-05-25: status blocked -> doing, 用户已提供 token`
- `2026-05-25: status doing -> done, smoke test 通过`

## Relay Mesh integration

Ledger 与 Relay Mesh 应显式联动。

### Relationship model

- `main relay`：承载上下文主线；
- `branch relay`：承载某个专项分支上下文；
- `ledger`：维护这些主线/分支背后的任务状态账本。

### Recommended linkage

每个 todo item 可关联：

- `branch`: 当前由哪个 branch 负责；
- `related_relay`: 对应哪个 relay 文件；
- `depends_on`: 依赖哪个 task ID；
- `owner`: 当前由哪个角色或 agent 负责。

示例：

```yaml
id: CHK-02
title: 修复登录跳转
status: doing
priority: high
next_step: 验证 callback 参数在生产构建中的行为
blocker: ""
branch: checkout-login-redirect
related_relay: /private/tmp/RELAY-checkout-login-redirect.md
owner: branch specialist
depends_on: [CHK-01]
completion_criteria: 登录后稳定跳转到 dashboard，smoke test 通过
note: doing — branch relay 已派发并完成首次复现
```

### Merge-back behavior

当某个 branch relay 完成并 merge-back 到 main relay 时，ledger 应同步体现：

- branch 对应任务是否完成；
- 哪些 blocker 被解除；
- 是否影响主线优先级；
- 是否应关闭、归档或继续维护该 branch 任务。

### Branch task policy

默认情况下，ledger 不需要为每条 branch 单独创建一个 TODO 文件。

更推荐的方式是：

- 使用一个项目级 `TODO.md` 作为总台账；
- 将 branch 任务作为其中的二级任务、子任务，或带 `parent` / `branch` 字段的条目存在；
- 用 `related_relay` 指向对应的 branch relay 文件。

这样做的原因是：

- ledger 的核心是统一总面板，而不是多账本并行；
- relay 适合多文件分支接力，ledger 更适合集中管理任务状态；
- 可以减少主 TODO 与 branch TODO 之间的同步负担；
- 更容易一眼看清主线与分支的状态关系。

只有在以下情况，才建议拆出独立 branch TODO：

- 某个 branch 已长期独立推进；
- 某个 branch 已接近子项目规模；
- 主 TODO 已明显过载；
- 用户明确要求拆分。

## Storage and file policy

Ledger 可以使用单文件或结构化多段文档，但第一版推荐优先简单、稳定、可读。

### Recommended default filenames

- 项目级总台账：`<project-root>/TODO.md`
- 临时任务级：`/private/tmp/TODO-<short-topic>.md`

默认情况下，Relay Mesh 的 branch 任务也应维护在同一个项目级 `TODO.md` 中，而不是每个 branch 再拆一个独立 TODO 文件。

### Naming principles

- 与 relay 的 mesh-prefix 尽量一致（如果存在临时文件）；
- 名字保持简短、可读、kebab-case；
- 不要使用过泛名称如 `todo.md`、`misc.md`、`temp.md` 作为临时文件名；
- 项目内统一使用 `TODO.md`，避免项目里散落多个同类文件；
- branch 任务默认作为 `TODO.md` 中的子任务或带 `branch` / `parent` 字段的子项存在；
- 只有当 branch 已显著独立、长期存在或用户明确要求时，才考虑拆出独立 branch TODO 文件。

## Preferred dashboard template

除非用户明确要求其他格式，否则项目级 `TODO.md` 推荐优先采用以下 dashboard 结构：

```md
# TODO

## 🧭 Overview
- Project: `...`
- Type: `...`
- Focus: `...`
- Main relay: `...`

## 🔷 Main

### [-] T-01 · 主任务标题
> summary: 一句话说明当前状态。

- next: ...
- priority: high
- blocker: none
- relay: `...`

## 🌿 Branches

### [ ] T-02 · 子任务标题
> branch: `branch-name`
> summary: 一句话说明当前状态。

- next: ...
- priority: medium
- blocker: none
- relay: `...`
- parent: `T-01`

## 🔗 Relay Mesh Links
- main relay → `...`
- branch relay (`T-02`) → `...`

## 📝 Notes
- ...

## 🧩 Legend
- [ ] todo
- [-] doing
- [!] blocked
- [x] done
- [~] dropped
- [>] archived
```

### Section guidance for dashboard view

#### 🧭 Overview

写清：

- 当前 list 服务于哪个项目/主线；
- 当前最重要的 1~3 个任务；
- 是否存在活跃 branch；
- main relay 在哪里。

#### 🔷 Main

放当前 main task 或主线任务卡片。默认优先展示：

- doing 的 main task；
- 当前最关键的 main task；
- 与 branch 直接关联的上层任务。

#### 🌿 Branches

放 branch task 卡片。默认优先展示：

- 活跃 branch；
- 需要独立 relay 的 branch；
- 即将 merge-back 或正在 blocked 的 branch。

#### 🔗 Relay Mesh Links

集中列出：

- main relay；
- branch relay 映射；
- 尚未拆出 relay 的 branch 说明。

#### 📝 Notes

只保留必要说明、约束与使用约定，不复制长文上下文。

#### 🧩 Legend

放状态符号说明，保持简洁。

## Todo item template

在 dashboard 视图中，推荐使用卡片头版模板：

```md
### [-] CHK-02 · 修复登录跳转
> branch: `checkout-login-redirect`
> summary: 已完成首次复现，当前在验证 callback 参数行为。

- next: 验证 callback 参数在生产构建中的行为
- priority: high
- blocker: none
- relay: `/private/tmp/RELAY-checkout-login-redirect.md`
- parent: `CHK-01`
```

当需要更重的审计信息时，再补充完整字段，例如：

- `depends_on`
- `owner`
- `completion_criteria`
- `updated_at`
- `archive_reason`
- 轻量 changelog

对于 done / dropped / archived 项，可简化展示，但不要丢失 ID 与结论。

## Supported operations

### 1. Create

用于创建：

- 新的 todo list；
- 新的主线 TODO；
- 新的 branch TODO；
- 新的 todo item。

### 2. Record

用于：

- 登记新任务；
- 写入初始状态；
- 记录 relay 关系；
- 记录 owner / branch / completion criteria。

### 3. Track

用于：

- 汇总任务状态；
- 查找 blocked 项；
- 找出最高优先级任务；
- 查看 branch 与 main 的对应关系。

### 4. Update

用于：

- 改状态；
- 改优先级；
- 改 next_step；
- 写 blocker；
- 追加 changelog；
- 更新 relay 路径；
- 在 merge-back 后同步主线状态。

### 5. Archive

用于：

- 收起已完成项；
- 归档 dropped 项；
- 清理过时 branch；
- 保留历史，但减少活跃视图噪音。

### 6. Reprioritize

用于：

- 重新排列优先级；
- 在 blocker 解除后提升任务；
- 在主线计划变化时重排 branch 顺序。

## Archive policy

归档时应保留最小必要信息：

- ID
- 标题
- 最终状态
- 归档原因
- 归档时间
- 如有必要，关联 relay 或关键文件

### Example

```md
- [x] CHK-02 | 修复登录跳转
  - final_status: done
  - archived_reason: 已完成并 merge-back 到 main relay
  - archived_at: 2026-05-25
  - relay: /private/tmp/RELAY-checkout-login-redirect.md
```

## Auto-summary behavior

当用户要求“看看当前 todo list”“总结一下当前任务状态”时，ledger 应优先总结：

- doing 项；
- blocked 项；
- 最需要推进的 next step；
- 是否存在 branch 未 merge-back；
- 是否存在过多未归档的 done 项。

## Decision table

| 用户表达 / 场景 | 默认动作 | 是否触发 ledger | 说明 |
| --- | --- | --- | --- |
| “创建一个 todo list” | 创建 list | 是 | 典型显式触发 |
| “加一个新的 todo” | 新增 todo item | 是 | 典型显式触发 |
| “更新这个 todo” | 更新 item | 是 | 典型显式触发 |
| “把这个任务标成 blocked” | 更新状态 | 是 | ledger 负责状态管理 |
| “看看当前 todo list” | 汇总 list | 是 | 任务状态总览 |
| “给这个 branch 记一个任务” | 新增 branch todo | 是 | Relay Mesh 典型用法 |
| “重新排一下优先级” | reprioritize | 是 | ledger 负责优先级 |
| “把完成的项归档” | archive | 是 | 归档行为 |
| “帮我做个 relay” | 转到 relay | 否 | 这是上下文接力，不是任务台账 |
| “总结一下当前问题” | 普通总结或 relay（视上下文） | 否 | 不默认触发 ledger |

## Examples

### Should trigger

- “创建一个 todo list，管理 checkout 主线”
- “加一个新的 todo：修登录跳转”
- “更新 CHK-02，把状态改成 blocked”
- “看看当前 todo list，按优先级汇总”
- “把 checkout 分支的完成项归档”

### Relay Mesh examples

- “为 checkout 主线创建一个 TODO.md，并登记 main relay 与两个 branch relay”
- “给 checkout-login-redirect branch 增加一个二级 todo”
- “A 分支 merge-back 后，把相关任务状态同步回 main todo list”
- “找出哪些 branch tasks 还没 merge-back”
- “把 payment webhook 作为 checkout 主任务下的子任务登记到 TODO.md”

### Should not trigger by default

- “继续”
- “接着做”
- “先别停”
- “帮我做个 relay”
- “总结一下当前上下文”

## Opening behavior

一旦确认要执行 ledger，先用 1 句话说明接下来会做什么，再开始创建或更新文件。

推荐开场风格：

- “我来建一个 todo list，并把当前任务整理成 ledger。”
- “我先把这些 todo 项登记到 ledger，再给你看当前状态。”
- “我会更新这个 todo list，并同步它和 relay 的关系。”

要求：

- 简短；
- 明确这是任务台账，不是 relay；
- 如果用户没指定路径，按默认命名规则选择文件位置。

## Style rules

- 默认中文；
- 用户层仍然优先使用 todo / todo list 的自然说法；
- 系统层结构可使用 ledger / item / archive / branch / mesh-prefix 等术语；
- 不要复制大段聊天记录；
- 不要把 relay 全文抄到 ledger；
- 强调状态、下一步、blocker、依赖、归档原因；
- 尽量保持条目短、稳、可扫描。

## Anti-patterns

以下做法是错误的：

- 把 ledger 写成聊天摘要；
- 不分配 task ID；
- 只有状态，没有状态原因；
- 不写 next_step；
- 不写 blocker；
- Relay Mesh 中不记录 branch / related_relay；
- done 项永远堆在 active 视图里不归档；
- 完成 merge-back 后，main 与 branch 状态不同步；
- 每次更新都覆盖掉历史而不保留最小审计痕迹。

## Compatibility notes

- 第一版就同时考虑创建、记录、跟踪、更新、归档、优先级重排与 Relay Mesh 协作；
- 如果用户只想维护一个简单 todo list，也可以轻量使用，不必启用全部字段；
- 如果历史 TODO 文件没有 task ID，可在第一次系统化更新时补齐；
- 如果历史文件不是 `TODO.md`，更新时可兼容旧路径；若新建，则优先使用默认命名。

## Changelog

- `v1.2.2`
  - 新增 `Update hygiene`，明确更新现有 dashboard 卡片时应原位 patch，而不是追加重复字段；
  - 新增 `Merge-back update rules`，明确 branch relay → main relay → TODO.md 的推荐更新顺序；
  - 新增重复字段防护规则，避免同一卡片出现重复 `branch:` / `summary:` 等核心字段。

- `v1.2.1`
  - 清理旧的 `Active Items / Blocked Items / Done Items` 遗留说明；
  - 将相关章节语义统一为新的 dashboard 视图：`Overview / Main / Branches / Relay Mesh Links / Notes / Legend`。

- `v1.2.0`
  - 新增 `Display mode`，明确区分 canonical structure 与 human-facing dashboard view；
  - 新增 `Default visual style`，定义项目级 `TODO.md` 的默认卡片头样式、summary quote block、主线/子线分区与空区块折叠规则；
  - 将 `List structure` 升级为 `Preferred dashboard template`；
  - 将 `Todo item template` 升级为卡片头版模板。

- `v1.1.0`
  - 将 ledger 的默认策略调整为单一项目级 `TODO.md` 为主；
  - 明确 Relay Mesh 的 branch 任务默认作为 `TODO.md` 中的子任务或带 `parent` / `branch` 字段的子项存在；
  - 将独立 branch TODO 文件降级为例外情况，仅在 branch 长期独立、规模过大或用户明确要求时使用。

- `v1.0.0`
  - 初始版本；
  - 采用 skill 名 `ledger`，用户层继续使用 `todo list` / `todo item`；
  - 第一版同时纳入创建、记录、跟踪、更新、归档、重排优先级、状态审计与 Relay Mesh 协作；
  - 引入 task ID、状态原因、可选 changelog、branch / related_relay / depends_on / owner 等字段；
  - 支持项目级 TODO、临时 TODO、mesh 主线 TODO、mesh 子线 TODO 命名策略。
