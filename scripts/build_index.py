from __future__ import annotations
from twin.config import TwinConfig
from twin.ingest import load_raw_texts
from twin.chunking import chunk_text
from twin.store import ensure_db, insert_chunks
from twin.embed import Embedder
from twin.retrieve import VectorIndex

def main() -> None:
    cfg = TwinConfig()
    cfg.db_dir.mkdir(parents=True, exist_ok=True)

    ensure_db(cfg.sqlite_path)

    raw = load_raw_texts(cfg.raw_dir)
    if not raw:
        print(f"No .txt/.md files found in {cfg.raw_dir}")
        print("Drop some files in data/raw/ and rerun.")
        return

    all_chunks = []
    for source, text in raw:
        chunks = chunk_text(text, source, cfg.chunk_size, cfg.chunk_overlap)
        for c in chunks:
            all_chunks.append((c.source, c.chunk_id, c.text))

    row_ids = insert_chunks(cfg.sqlite_path, all_chunks)

    embedder = Embedder(cfg.embedding_model)
    vectors = embedder.encode([c[2] for c in all_chunks])

    vi = VectorIndex(vectors.shape[1])
    vi.add(vectors, row_ids)
    vi.save(cfg.faiss_index_path, cfg.faiss_meta_path)

    print("✅ Index built!")
    print(f"Chunks stored: {len(all_chunks)}")
    print(f"SQLite: {cfg.sqlite_path}")
    print(f"FAISS: {cfg.faiss_index_path}")

if __name__ == "__main__":
    main()
