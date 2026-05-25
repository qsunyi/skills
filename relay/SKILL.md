---
name: relay
description: 当用户明确要求生成、更新、补全、重写、查看会话或项目交接文档时使用。适用于 /compact 前整理上下文、换 session、长时间暂停后续跑、复杂排障、多文件修改、浏览器自动化、长链路调试或任何需要把当前状态压缩成可继续执行文档的场景。支持 Relay Mesh workflow：可从一个 main relay 派生多个 branch relays，再 merge-back 回主线。仅在用户明确要求时触发，不因上下文偏高而自动执行。高频触发词包括：relay、交接、handoff、续跑文档、继续做的说明、接力摘要、下个 session 怎么接着做、帮我整理当前进展、写个 /compact 前说明、更新 relay 文件。
argument-hint: 下个 session 的重点是什么？
type: productivity
author: Roy <qsunyi@qq.com>
version: 1.4.1
---

# Relay

## Purpose

把当前任务状态压缩成一份 **可续跑、可验证、低重复** 的接力文档，供当前用户、下一个 session 或下一个 agent 继续执行。

Relay 不是聊天摘要，也不是把已经存在的文档再抄一遍。它的目标是：

1. 让下一个接手者快速知道目标是什么；
2. 明确哪些事实已经验证，哪些只是猜测；
3. 让接手者知道改过什么、试过什么、为什么这样做；
4. 降低重复踩坑和重复探索的成本。

## When to use

仅在 **用户明确要求** 时使用，例如：

- “帮我做个 relay”
- “生成一个 handoff / 交接文档”
- “把当前进展整理一下，给下个 session 用”
- “写个 /compact 前的续跑说明”
- “更新一下 relay 文件”
- “看看现在的 relay 该怎么写”

如果只是检测到上下文偏高，但用户没有要求执行 relay：

- 只提醒，不自动写；
- 是否创建或更新 relay，由用户决定。

## User-specified focus

如果用户在请求 relay 时附带了额外重点、范围、参数或下一步方向，应将其视为 **下个 session 的首要关注点**。

常见形式包括：

- “帮我做个 relay，重点放在登录跳转问题”
- “更新 relay，下个 session 先看 CI 失败”
- “写个 /compact 前 relay，重点整理未验证假设”
- “做个 relay，给下一轮主要处理 payment webhook”

执行规则：

1. 优先按这个 focus 组织 relay 的结构与篇幅；
2. `未完成事项` 与 `下一步建议` 必须优先围绕这个 focus 排序；
3. 如果当前主任务比 focus 更宽，需同时写清：
   - 原主任务是什么；
   - 用户要求下个 session 优先关注什么；
4. 如果用户提供的 focus 很模糊，可以合理压缩归纳，但不要擅自改写成不同目标；
5. 如果用户没有提供 focus，则按当前任务的自然下一步来写。

## Audience

relay 默认是写给 **fresh agent / 下一个新 session** 接手用的，而不是写给已经完整参与当前上下文的人。

因此写作时应假设接手方：

- 没看过完整聊天记录；
- 不知道你为什么做出当前决策；
- 需要快速辨别哪里是事实、哪里是猜测；
- 需要一眼看到下一步该做什么。

所以 relay 应尽量做到：

- 自包含但不冗余；
- 能脱离当前会话独立阅读；
- 不依赖“上文提到”“前面说过”这类上下文指代。

## Non-triggers

以下表达**默认不触发** relay，除非用户明确表示要生成或更新交接文档：

- “继续”
- “接着做”
- “往下弄”
- “先别停”
- “你继续排查”
- “总结一下”
- “概括一下当前问题”
- “说说现在进展”

原因：这些表达可能只是要口头汇报、阶段性总结或继续执行，不等于要落盘生成 relay 文档。

如果用户只是想知道当前状态：

- 可以直接用普通回答总结；
- 不要自动写 relay 文件。

只有当用户明确出现以下意图时才正式触发：

- 要为下个 session 留说明；
- 要在 /compact 前保存续跑上下文；
- 要生成、更新、补全、重写交接文档；
- 要把当前状态写入某个 relay / handoff 文件。

## Output location policy

优先级如下：

1. 如果用户指定路径，使用用户指定路径；
2. 如果用户只说“先做个临时 relay”，优先写到 `/private/tmp/RELAY-<short-topic>.md`；
3. 如果存在明确主线，并且当前 relay 属于该主线或其子分支，则优先使用带主线前缀的命名；
4. 如果任务明显属于某个项目，且用户同意写入项目内，则优先写到项目根目录的 `RELAY.md`；
5. 不要默认散落生成多个 relay 文件，除非用户明确要求保留历史版本。

写入前必须先：

- 确认目标路径；
- 如果文件已存在，先读取现有内容，再决定是追加、重写还是局部更新；
- 不要在未检查旧文件的情况下盲写覆盖。

## Core principles

### 1. Prefer references over duplication

如果信息已经稳定存在于以下 artifact 中：

- PRD
- plan
- ADR
- issue
- commit
- diff
- 设计文档
- 测试报告
- 代码文件

则在 relay 中：

- 简要说明其作用；
- 提供路径或链接；
- 不要大段重复粘贴正文。

### 2. Separate facts from assumptions

必须明确区分：

- **已确认事实**：已通过文件、命令、页面状态、测试结果、日志或外部查询验证；
- **待验证假设**：当前推测、未复现判断、怀疑点、可能方向。

绝对不要把推测写成事实。

### 3. Optimize for the next action

relay 不是历史档案，而是“下一步如何继续”的操作说明。

所以要优先保留：

- 下一步建议；
- 当前 blocker；
- 最值得先跑的命令/入口；
- 已踩过的坑；
- 为什么当前选择这个方向。

### 4. Keep it compact but sufficient

要求紧凑，但不能为了短而牺牲可执行性。

省略：

- 无关寒暄；
- 冗长聊天复述；
- 重复的工具原始输出；
- 低价值试错细节。

保留：

- 决策信息；
- 验证结果；
- 文件路径；
- 命令摘要；
- 未完成事项。

## Required structure

除非用户明确要求换格式，否则 relay 至少应包含以下部分：

```md
# Relay

## 用户目标

## 当前状态 / 进度

## 已确认事实

## 待验证假设 / 未决问题

## 已修改文件

## 关键命令与结果

## 相关文档与入口

## 当前决策与原因

## 未完成事项

## 下一步建议

## 避免重复踩坑

## 推荐下个 session 使用的 skills / tools
```

### Section guidance

#### 用户目标
- 用 1~3 句话写清用户要什么；
- 如果目标变更过，写明最新目标。

#### 当前状态 / 进度
- 当前做到哪一步；
- 哪些已经完成；
- 哪些正在进行。

#### 已确认事实
- 只写验证过的信息；
- 最好附验证依据，如文件路径、命令、测试、页面标题、日志结论。

#### 待验证假设 / 未决问题
- 写清楚不确定点；
- 写清为什么怀疑它；
- 写清下一步如何验证。

#### 已修改文件
- 列出绝对路径或项目内明确路径；
- 简述每个文件改了什么；
- 如果只是查看未修改，不要混写到这里。

#### 关键命令与结果
- 不贴整段原始输出；
- 只写“命令 + 结果摘要 + 含义”；
- 对失败命令也应保留有价值的失败原因。

#### 相关文档与入口
- 放 PRD、issue、设计稿、URL、脚本入口、关键目录；
- 用路径或链接引用，不要复制全文。

#### 当前决策与原因
- 说明为什么走当前方案；
- 写清排除过哪些明显备选方案（如有必要）。

#### 未完成事项
- 列待办清单；
- 如果有依赖顺序，按顺序写。

#### 下一步建议
- 优先写“接手后前 1~3 步具体做什么”；
- 最好能让接手者直接开始执行。

#### 避免重复踩坑
- 写清已经无效的方向；
- 写清环境限制、路由错误、已知假阳性、不要重复执行的重命操作。

#### 推荐下个 session 使用的 skills / tools
- 只推荐真正相关的；
- 简述原因；
- 如果没有明显建议，可以写“无特殊要求”。

## Update policy

如果用户要求“更新 relay”而不是新建：

1. 先读取现有 relay；
2. 保留仍然有效的结构；
3. 删除已过时结论或明确标注其失效；
4. 合并最新进展；
5. 避免越更新越臃肿。

必要时可以执行“重写优于增补”：

- 当旧 relay 已严重过时；
- 当结构混乱难以续用；
- 当用户明确要求重写。

## Writing workflow

1. 先确认用户是否真的要执行 relay；
2. 确认目标路径；
3. 读取现有 relay（若存在）；
4. 回顾当前任务的关键证据：目标、进度、文件改动、关键命令、未决问题；
5. 生成结构化 relay；
6. 写入文件；
7. 回答用户时简要说明：
   - 写到了哪里；
   - 是新建还是更新；
   - 下一次接手建议先看哪一节。

## Opening behavior

一旦确认要执行 relay，先用 1 句话说明接下来会做什么，再开始读取/生成/更新文件。

推荐开场风格：

- “我来整理一个 relay，给后续 session 续跑用。”
- “我先把当前状态压成一个 relay 文档，再告诉你写到哪里。”
- “我会按 relay 结构整理当前进展，并区分已确认事实和待验证项。”

开场要求：

- 简短，不要先输出长摘要；
- 明确这是 relay，而不是普通总结；
- 如果用户没给路径，可在开场后自行按 skill 规则选择默认路径，或在必要时补一句说明。
- 生成 `/private/tmp` 下的 relay 文件名时，使用 `RELAY-` 前缀，并优先判断是否存在主线前缀；若存在，则统一带上主线前缀，避免不同会话或不同分支互相覆盖或混淆。

## Style rules

- 默认中文；
- 句子简洁、工程化；
- 优先项目符号；
- 不写空泛表述，如“做了一些调整”“问题基本解决”；
- 不要假装确定；
- 不要把未经验证的记忆、推断或旧上下文写成事实。

## Anti-patterns

以下做法是错误的：

- 在用户没要求时自动创建 relay；
- 复制整段聊天记录充当 relay；
- 大段粘贴 PRD / issue / diff 正文；
- 不区分事实与猜测；
- 不写文件路径；
- 不写下一步建议；
- 只写“已完成/未完成”而没有证据和原因；
- 更新现有 relay 时直接覆盖而不先读取。

## Examples

### Should trigger

- “帮我做个 relay”
- “写个 /compact 前说明，给下个 session 用”
- “更新一下 relay 文件”
- “生成一个交接文档，后面继续做”
- “把当前进展整理成 relay”

### Should trigger with focus

- “帮我做个 relay，重点放在登录跳转问题”
- “更新 relay，下个 session 先看 CI 失败”
- “写个 relay，重点整理未验证假设”
- “做个 /compact 前 relay，下一轮先查 payment webhook”

### Should not trigger by default

- “继续”
- “接着做”
- “先别停”
- “总结一下当前情况”
- “说说现在进展”
- “概括一下这个问题”

### Borderline examples

以下说法可能接近 relay，但默认先按普通总结理解，除非用户明确要求落盘为文档：

- “帮我整理一下思路”
- “给我一个后面继续做的说明”
- “把当前状态记一下”

如果用户后续补充：

- “写到文件里”
- “给下个 session 接着用”
- “做成 relay / handoff”

则正式触发 relay。

## Compatibility notes

- `v1.2.0` 起，relay 正式支持 `argument-hint` 与 User-specified focus；
- 如果用户未提供 focus，relay 仍按当前任务的自然下一步生成，不影响旧用法；
- 旧 relay 文件即使没有 focus 字段，也可以正常读取、更新或重写；
- `v1.1.x` 与更早的 relay 内容若命名规则不同，不视为错误，但新建默认文件时应遵循 `v1.2.0` 的命名策略；
- 项目内历史交接文件如果不是 `RELAY.md`，更新时可按用户意图兼容旧路径；若新建，则优先使用 `RELAY.md`。

## Decision table

| 用户表达 / 场景 | 默认动作 | 是否触发 relay | 说明 |
| --- | --- | --- | --- |
| “继续” / “接着做” / “先别停” | 继续执行当前任务 | 否 | 这是执行指令，不等于生成交接文档 |
| “总结一下当前情况” / “说说现在进展” | 普通文字总结 | 否 | 默认视为口头汇报，不落盘 |
| “帮我整理一下思路” | 普通结构化总结 | 否 | 除非用户明确要求写入文件或给下个 session 用 |
| “帮我做个 relay” | 创建或更新 relay | 是 | 明确触发词 |
| “生成一个 handoff / 交接文档” | 创建或更新 relay | 是 | 与 relay 同义 |
| “写个 /compact 前说明” | 创建或更新 relay | 是 | 默认理解为给后续续跑的文档 |
| “给下个 session 接着用” | 创建或更新 relay | 是 | 明确说明受众是下一 session |
| “写到文件里，后面继续做” | 创建或更新 relay | 是 | 明确要求落盘，且具有续跑意图 |
| “更新 relay，下个 session 先看 CI 失败” | 更新 relay，并设置 focus | 是 | 明确触发 relay，且给出了下个 session 的重点 |
| 只给出 focus，如“重点查 webhook”但未要求 relay | 按当前任务继续 / 必要时普通确认 | 否 | 有重点不等于要生成 relay 文档 |
| 上下文接近 65%，但用户未要求 relay | 只提醒 | 否 | 提醒用户可选择生成 relay，但不自动执行 |
| 用户指定了旧路径且要求更新 | 读取旧文件后更新 | 是 | 兼容历史 relay 路径，不强制迁移 |

## Relay Mesh workflow

Relay Mesh 是 relay 的多分支接力模式。
relay 不只适用于“当前 session 交给下个 session”。它也适用于把主线中的某个子任务（如 A / B / C）拆成一个独立分支，让另一个 fresh agent 聚焦处理，再把结果 relay 回主线。

典型场景：

- 主线任务很大，包含多个子问题；
- 某个子任务需要深钻，不想污染主线上下文；
- 希望另一个 agent 只聚焦某一个 focus task；
- 子任务处理结果还需要回流主线，影响整体计划。

### Roles

在这种模式里，默认有三个角色：

1. **main orchestrator**：负责总目标、拆分 A/B/C、派发 relay、回收结果；
2. **branch specialist**：只围绕一个子任务 focus 深钻执行；
3. **relay document**：作为主线与子线之间的上下文接力包。

### Workflow

#### Step 1: main relay 派发 branch relay

主线可以要求：

- 为任务 A 创建一个专项 relay；
- 明确 focus 是 A；
- 说明这是给另一个 fresh agent 独立接手 A 用的；
- 约束不要展开 B/C，除非它们直接影响 A。

推荐提示词：

```text
帮我创建一个 relay，重点是任务 A：登录跳转问题。

这个 relay 是给另一个 fresh agent 独立接手 A 用的。
请：
1. 把用户目标、当前状态、已确认事实、待验证假设、已修改文件、关键命令与结果、未完成事项、下一步建议都写清楚；
2. 未完成事项和下一步建议优先围绕 A 组织；
3. 不要展开 B、C，除非它们会直接影响 A；
4. 写成一个脱离当前聊天记录也能独立理解的 relay。
```

#### Step 2: 子 agent 接收 relay 并执行 A

子 agent 接到 relay 后，应把自己当成 fresh agent，只基于 relay 接手 A。

推荐提示词：

```text
这是主线拆出来的任务 A relay。
请把自己当成一个 fresh agent，只基于这份 relay 接手任务 A。

先做三件事：
1. 用简短的话复述你理解的 A 的目标、当前状态和 blocker；
2. 说明你接下来准备执行的前 1~3 步；
3. 然后开始处理 A。

如果 relay 缺少关键上下文，请明确指出缺口，不要自行脑补。
除非 B/C 对 A 有直接阻塞，否则不要发散到其他任务。
```

#### Step 3: 子 agent 完成阶段工作后更新 relay

子 agent 处理完一轮 A 后，应更新 A-relay，而不是只给一段口头总结。

推荐提示词：

```text
请更新这个任务 A 的 relay。

要求：
1. 删除已经失效的假设；
2. 增加你刚确认的新事实；
3. 列清楚你改过的文件和验证结果；
4. 明确 A 当前是否完成；
5. 如果未完成，给出下一个 fresh agent 接手 A 时最合理的下一步建议；
6. 如果 A 的结果会影响主线里的 B/C，也单独写出来。
```

#### Step 4: branch relay merge-back 到 main relay

主线拿回更新后的 A-relay 后，不应只复述内容，而应站在 orchestrator 视角吸收结果并调整计划。

推荐提示词：

```text
这是任务 A 更新后的 relay。

请站在 main orchestrator 视角：
1. 总结 A 当前状态；
2. 判断 A 是否完成，还是还要继续单独推进；
3. 说明 A 对 B/C 的影响；
4. 判断主线计划是否需要调整；
5. 如果需要，再建议是否继续为 A 保留单独 relay。
```

### Guidelines

- 子任务 relay 应尽量做成“专项上下文包”，而不是总任务摘要；
- 主线和子线之间要避免状态漂移；如果主线改变了 A 的前提，最好重新生成或更新 A-relay；
- 子线完成后，要把结果真正合并回主线，而不是只把文档放在那里；
- 如果一个子任务长期独立推进，可以持续维护它自己的 relay；
- 如果子任务已经完成并且不再独立推进，可将结论吸收回主线后结束该专项 relay 的生命周期。

## Filename conventions

按场景优先使用：

- 普通临时 relay：`/private/tmp/RELAY-<short-topic>.md`
- 主线临时 relay：`/private/tmp/RELAY-<mesh-prefix>-main.md`
- 子线临时 relay：`/private/tmp/RELAY-<mesh-prefix>-<short-topic>.md`
- 项目续跑：`<project-root>/RELAY.md`

### Temporary relay naming rules

当默认写入 `/private/tmp` 时：

- 文件名必须以 `RELAY-` 开头；
- 默认使用 kebab-case；
- 主题描述优先来自当前任务目标，而不是泛化词；
- 避免使用 `temp`、`misc`、`session`、`todo` 这类信息量过低的名字；
- 如果任务主题很长，压缩到 2~6 个英文词即可。

#### Pattern A: 普通 relay

用于没有明确主线关系的独立 relay：

- `RELAY-<short-topic>.md`

示例：

- `RELAY-fix-login-redirect.md`
- `RELAY-debug-playwright-timeout.md`
- `RELAY-polish-pricing-page.md`

#### Pattern B: 主线 relay

用于一条主线任务的总 relay：

- `RELAY-<mesh-prefix>-main.md`

示例：

- `RELAY-checkout-main.md`
- `RELAY-taobao-scraper-main.md`
- `RELAY-notebooklm-export-main.md`

#### Pattern C: 子线 relay

用于某条主线下的专项子任务 relay：

- `RELAY-<mesh-prefix>-<short-topic>.md`

示例：

- `RELAY-checkout-login-redirect.md`
- `RELAY-checkout-payment-webhook.md`
- `RELAY-checkout-ci-flake.md`
- `RELAY-taobao-scraper-review-api.md`

#### Mesh prefix rules

如果要使用 mesh 前缀，优先级如下：

1. 用户明确指定主线前缀，则直接使用；
2. 如果已有主线 relay 文件名，则子线 relay 沿用同一个前缀；
3. 如果没有明确前缀，则从当前主任务目标中压缩出一个简短英文前缀。

mesh 前缀的目标是：

- 把同一条主线的 relay 自动聚到一起；
- 让主线与子线 relay 在文件名上形成家族关系；
- 不依赖是否存在 A/B/C 编号。

### Project relay naming rules

当写入项目内时：

- 默认文件名使用 `RELAY.md`；
- 放在项目根目录；
- 除非用户要求保留多版本，否则优先维护这一份单一最新 relay。

除非用户要求保留版本历史，否则默认维护单一最新 relay。

## Changelog

- `v1.4.1`
  - 在 description 中显式声明支持 `Relay Mesh workflow`，使入口元数据与正文术语完全一致。

- `v1.4.0`
  - 正式采用 `Relay Mesh` 作为主线-多子线接力模式的术语；
  - 将 `mainline relay` 收敛为更易记的 `main relay`；
  - 将命名规则中的 `mainline-prefix` 统一为 `mesh-prefix`；
  - 将 `Subtask branch workflow` 重命名为 `Relay Mesh workflow`。

- `v1.3.2`
  - 修正文档顶部的 Filename conventions 摘要，使其与新版普通 / 主线 / 子线命名规则保持一致。

- `v1.3.1`
  - 升级临时 relay 命名规则，支持普通 relay / 主线 relay / 子线 relay 三层结构；
  - 增加主线前缀规则，优先用主线前缀串联同一条主线下的 relay，而不依赖 A/B/C 编号。

- `v1.3.0`
  - 增加 Subtask branch workflow，正式支持主线 A/B/C 子任务分叉、专项 relay、子 agent 接手、回流主线的接力模式；
  - 增加主线派发 / 子线接手 / 子线更新 / 主线回收四步 workflow 与推荐提示词。

- `v1.2.2`
  - 增加 Decision table，把常见表达映射到默认动作、是否触发 relay 与说明，便于快速判定。

- `v1.2.1`
  - 增加 Examples，明确触发 / 不触发 / 带 focus 触发 / 边界用法；
  - 增加 Compatibility notes，说明从旧 relay 规则到 `v1.2.x` 的兼容方式。

- `v1.2.0`
  - 增加 `argument-hint`，把“下个 session 的重点”作为显式输入契约；
  - 增加 User-specified focus，明确用户传参数时要将其视为下个 session 的首要关注点；
  - 增加 Audience，强调 relay 是写给 fresh agent / 新 session 接手，而不是写给当前已知上下文的人。

- `v1.1.0`
  - 增加 Non-triggers，减少误触发；
  - 增加 Opening behavior，统一触发后的开场动作；
  - 调整默认文件命名策略：`/private/tmp/RELAY-<short-english-topic>.md` 与项目根目录 `RELAY.md`；
  - 将版本号写入 frontmatter，便于后续维护。
