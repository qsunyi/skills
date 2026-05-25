# MusicShelf

MusicShelf 是一个面向本地音乐库整理的技能与规则集合，用来把混乱的音乐目录整理成可长期维护的正式音乐库。

它的目标不是一次性“搬文件”，而是建立一套可复用、可增量运行、可回刷规范化的整理流程。

## 核心能力

- 艺人优先归档
- 专辑优先于单曲
- 年份前置优先，目标库回刷兜底
- 繁体转简体、乱码清理、半角全角统一后再匹配
- 先做文件名清洗，再压平无意义嵌套目录
- 处理 DVD / 盒装 / 合集 / 混装盘时，先清洗名字再决定归位
- 对明显能自动完成的清洗动作，先做完再复查到零剩余
- 分离 `Music_无损` 与 `Music_mp3`
- 使用 SQLite 建立本地索引
- 支持增量处理
- 源头目录到目标库默认 `copy`
- 目标库内部规范化默认 `move`
- 不自动删除源头曲目目录

## 固定库名

```text
Music_无损
Music_mp3
```

## 索引方案

每个库各自维护 SQLite 索引：

```text
Music_无损/.library_index/music_index.db
Music_mp3/.library_index/music_index.db
```

初始化脚本：

```bash
python scripts/init_index.py "/path/to/Music_无损" "/path/to/Music_mp3"
```

详细表结构见：

- `references/sqlite-schema.md`

## Skill 文件

- `SKILL.md`：技能主文档与执行规则
- `scripts/init_index.py`：SQLite 索引初始化脚本
- `references/sqlite-schema.md`：SQLite 表结构与联查说明

## 使用前提

在真正整理前，必须先确认：

1. 源头目录
2. 目标无损库目录
3. 目标 MP3 库目录
4. 本次是全量整理还是增量整理

如果这些输入不明确，应该先暂停并要求补全，而不是自行猜路径。

## 适合处理的问题

- 乱序下载目录整理入正式库
- 无损/MP3 双库管理
- 专辑补年份
- 合集、精选集、单曲归类
- 历史目标库回刷规范化
- 重复容器目录压平
- 长期增量维护

## 不处理的事

- 云音乐歌单管理
- 流媒体平台操作
- 音频转码工作流（除非明确要求）
- 单纯播放器功能

## 发布状态

当前版本：`0.1.2`

作者：`Roy <qsunyi@qq.com>`
