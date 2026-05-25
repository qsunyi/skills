# MusicShelf SQLite 索引说明

这个文档解释 `scripts/init_index.py` 会创建的本地 SQLite 索引结构。

## 索引位置

每个库各自维护自己的索引：

```text
Music_无损/.library_index/music_index.db
Music_mp3/.library_index/music_index.db
```

## 初始化方式

```bash
python scripts/init_index.py "/path/to/Music_无损" "/path/to/Music_mp3"
```

这个脚本可以重复运行；如果数据库和表已经存在，会直接复用。

## 表结构

### metadata

保存数据库自身的元信息。

关键键值：

- `schema_version`
- `library_root`
- `library_name`

### albums

一条记录对应一个正式专辑目录。

建议语义：

- `library`：当前属于哪一个库，例如 `Music_无损` 或 `Music_mp3`
- `artist` / `normalized_artist`：原始歌手名与规范化歌手名
- `album` / `normalized_album`：原始专辑名与规范化专辑名
- `year`：年份，允许为空
- `format`：目录格式标记，例如 `FLAC`、`APE+CUE`
- `relative_path`：相对库根目录的路径
- `source_dir`：来源目录路径，便于回溯
- `status`：记录状态
- `fingerprint`：可选的目录级指纹
- `updated_at`：最近更新时间

### tracks

一条记录对应一首歌曲文件。

建议语义：

- `track` / `normalized_track`：原始曲名与规范化曲名
- `track_no`：轨道号
- `duration`：时长，允许为空
- 其余字段与 `albums` 同理

### processed_dirs

记录哪些源头目录已经处理过。

建议语义：

- `source_dir`：源头目录
- `mode`：`full` 或 `incremental`
- `result`：`ok`、`partial`、`failed`
- `run_id`：关联批次执行记录
- `updated_at`：记录更新时间

### runs

记录每次执行批次。

建议语义：

- `mode`：`full` 或 `incremental`
- `source_root`：本次执行的源头目录
- `target_root`：本次执行的目标库目录
- `started_at` / `finished_at`
- `status`
- `notes`

## 默认索引

脚本默认创建这些索引：

- `albums(normalized_artist, normalized_album)`
- `albums(relative_path)`
- `tracks(normalized_artist, normalized_track)`
- `tracks(normalized_artist, normalized_album)`
- `tracks(relative_path)`
- `processed_dirs(source_dir)`

## 双库联查原则

因为 `Music_无损` 和 `Music_mp3` 各自维护数据库，所以真正判断一首歌是否“双库都存在”时，要跨两个数据库联查。

最低统一字段：

- `normalized_artist`
- `normalized_album`
- `normalized_track`

## 为什么不用 JSONL 作为主索引

MusicShelf 需要：

- 增量处理
- 重复检测
- 年份补查
- 回刷规范化
- 高频查询

在这种场景里，SQLite 比 `JSONL + 内存索引` 更简单、更稳定，也更容易维护。