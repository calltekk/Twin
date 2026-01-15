from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass
class TextChunk:
    text: str
    source: str
    chunk_id: int

_whitespace_re = re.compile(r"\s+")

def clean_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = _whitespace_re.sub(" ", text).strip()
    return text

def chunk_text(text: str, source: str, chunk_size: int, overlap: int) -> list[TextChunk]:
    text = clean_text(text)
    if not text:
        return []

    chunks: list[TextChunk] = []
    start = 0
    cid = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(TextChunk(text=chunk, source=source, chunk_id=cid))
            cid += 1
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks
