from __future__ import annotations
import numpy as np
from pathlib import Path
import faiss

class VectorIndex:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)  # cosine if embeddings are normalized
        self.ids: list[int] = []

    def add(self, vectors: np.ndarray, row_ids: list[int]) -> None:
        if vectors.dtype != np.float32:
            vectors = vectors.astype(np.float32)
        self.index.add(vectors)
        self.ids.extend(row_ids)

    def search(self, query_vec: np.ndarray, top_k: int = 6) -> list[tuple[int, float]]:
        if query_vec.ndim == 1:
            query_vec = query_vec.reshape(1, -1)
        scores, idxs = self.index.search(query_vec.astype(np.float32), top_k)
        out: list[tuple[int, float]] = []
        for j, score in zip(idxs[0], scores[0]):
            if j < 0 or j >= len(self.ids):
                continue
            out.append((self.ids[j], float(score)))
        return out

    def save(self, index_path: Path, meta_path: Path) -> None:
        index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(index_path))
        np.save(str(meta_path), np.array(self.ids, dtype=np.int64))

    @staticmethod
    def load(index_path: Path, meta_path: Path) -> "VectorIndex":
        index = faiss.read_index(str(index_path))
        ids = np.load(str(meta_path)).tolist()
        vi = VectorIndex(index.d)
        vi.index = index
        vi.ids = ids
        return vi
