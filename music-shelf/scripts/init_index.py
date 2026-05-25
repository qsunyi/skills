#!/usr/bin/env python3
"""Initialize MusicShelf SQLite indexes for one or more library roots.

Usage:
  python scripts/init_index.py /path/to/Music_无损 [/path/to/Music_mp3 ...]

For each library root, this script creates:
  <library-root>/.library_index/music_index.db

It is safe to run repeatedly.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    library TEXT NOT NULL,
    artist TEXT,
    normalized_artist TEXT,
    album TEXT NOT NULL,
    normalized_album TEXT NOT NULL,
    year TEXT,
    format TEXT,
    relative_path TEXT NOT NULL,
    source_dir TEXT,
    status TEXT DEFAULT 'active',
    fingerprint TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    library TEXT NOT NULL,
    artist TEXT,
    normalized_artist TEXT,
    album TEXT,
    normalized_album TEXT,
    track TEXT NOT NULL,
    normalized_track TEXT NOT NULL,
    track_no TEXT,
    format TEXT,
    duration REAL,
    relative_path TEXT NOT NULL,
    source_dir TEXT,
    status TEXT DEFAULT 'active',
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS processed_dirs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_dir TEXT NOT NULL,
    mode TEXT NOT NULL,
    result TEXT NOT NULL,
    run_id INTEGER,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode TEXT NOT NULL,
    source_root TEXT,
    target_root TEXT,
    started_at TEXT DEFAULT CURRENT_TIMESTAMP,
    finished_at TEXT,
    status TEXT DEFAULT 'running',
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_albums_artist_album
    ON albums(normalized_artist, normalized_album);
CREATE INDEX IF NOT EXISTS idx_albums_relative_path
    ON albums(relative_path);
CREATE INDEX IF NOT EXISTS idx_tracks_artist_track
    ON tracks(normalized_artist, normalized_track);
CREATE INDEX IF NOT EXISTS idx_tracks_artist_album
    ON tracks(normalized_artist, normalized_album);
CREATE INDEX IF NOT EXISTS idx_tracks_relative_path
    ON tracks(relative_path);
CREATE INDEX IF NOT EXISTS idx_processed_dirs_source_dir
    ON processed_dirs(source_dir);
"""


def initialize_library(library_root: Path) -> Path:
    library_root = library_root.expanduser().resolve()
    if not library_root.exists() or not library_root.is_dir():
        raise FileNotFoundError(f"Library root does not exist or is not a directory: {library_root}")

    index_dir = library_root / ".library_index"
    index_dir.mkdir(parents=True, exist_ok=True)
    db_path = index_dir / "music_index.db"

    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.execute(
            "INSERT INTO metadata(key, value) VALUES('schema_version', '1') "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value"
        )
        conn.execute(
            "INSERT INTO metadata(key, value) VALUES('library_root', ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (str(library_root),),
        )
        conn.execute(
            "INSERT INTO metadata(key, value) VALUES('library_name', ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (library_root.name,),
        )
        conn.commit()
    finally:
        conn.close()

    return db_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize MusicShelf SQLite indexes.")
    parser.add_argument("library_roots", nargs="+", help="Library root directories to initialize.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    created = []
    for root in args.library_roots:
        db_path = initialize_library(Path(root))
        created.append(db_path)
    for db_path in created:
        print(db_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
