from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class TwinConfig:
    project_root: Path = Path(__file__).resolve().parents[1]
    raw_dir: Path = project_root / "data" / "raw"
    db_dir: Path = project_root / "data" / "db"

    sqlite_path: Path = db_dir / "twin.sqlite"
    faiss_index_path: Path = db_dir / "faiss.index"
    faiss_meta_path: Path = db_dir / "faiss_meta.npy"

    # Embedding model (local)
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Chunking
    chunk_size: int = 700        # characters
    chunk_overlap: int = 120     # characters
