from __future__ import annotations
from pathlib import Path

def read_text_file(path: Path) -> str:
    # Best-effort reading
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")

def load_raw_texts(raw_dir: Path) -> list[tuple[str, str]]:
    """
    Returns list of (source_name, text).
    MVP: supports .txt and .md
    """
    items: list[tuple[str, str]] = []
    for p in sorted(raw_dir.glob("**/*")):
        if p.is_file() and p.suffix.lower() in {".txt", ".md"}:
            items.append((str(p.relative_to(raw_dir)), read_text_file(p)))
    return items
