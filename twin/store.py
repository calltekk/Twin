from __future__ import annotations
import sqlite3
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ChunkRow:
    id: int
    source: str
    chunk_id: int
    text: str

SCHEMA = """
CREATE TABLE IF NOT EXISTS chunks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  chunk_id INTEGER NOT NULL,
  text TEXT NOT NULL
);
"""

def ensure_db(sqlite_path: Path) -> None:
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(sqlite_path) as con:
        con.execute(SCHEMA)
        con.commit()

def insert_chunks(sqlite_path: Path, chunks: list[tuple[str, int, str]]) -> list[int]:
    """
    chunks: [(source, chunk_id, text), ...]
    returns inserted row ids
    """
    with sqlite3.connect(sqlite_path) as con:
        cur = con.cursor()
        cur.executemany(
            "INSERT INTO chunks (source, chunk_id, text) VALUES (?, ?, ?)",
            chunks,
        )
        con.commit()
        if not chunks:
            return []
        # cursor.lastrowid can be None after executemany on some pythons/DB drivers;
        # use SQLite's last_insert_rowid() which returns the last row id for the connection
        last_id_row = con.execute("SELECT last_insert_rowid()").fetchone()
        last_id = last_id_row[0] if last_id_row is not None else None
        if last_id is None:
            # fallback: return empty list (shouldn't normally happen)
            return []
        start_id = int(last_id) - len(chunks) + 1
        return list(range(start_id, start_id + len(chunks)))

def fetch_chunks_by_ids(sqlite_path: Path, ids: list[int]) -> list[ChunkRow]:
    if not ids:
        return []
    qmarks = ",".join("?" for _ in ids)
    with sqlite3.connect(sqlite_path) as con:
        rows = con.execute(
            f"SELECT id, source, chunk_id, text FROM chunks WHERE id IN ({qmarks})",
            ids,
        ).fetchall()
    # preserve requested order
    by_id = {r[0]: ChunkRow(*r) for r in rows}
    return [by_id[i] for i in ids if i in by_id]
