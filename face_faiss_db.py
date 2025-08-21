import faiss
import numpy as np
import json
import os

class FaceDB:
    def __init__(self, dim=128, db_path="./"):
        self.dim = dim
        self.db_path = db_path
        self.index_file = os.path.join(db_path, "facefaiss.index")
        self.meta_file = os.path.join(db_path, "meta.json")

        # cosine similarity → inner product index
        self.index = faiss.IndexFlatIP(dim)

        # meta (id → name) 관리
        self.meta = []

        if not os.path.exists(db_path):
            os.makedirs(db_path)
            print("새로운 FaceFaissDB를 생성합니다.")
        else:
            self.load()

    def add(self, name, embedding):
        """embedding: (1,128) or (128,) numpy array"""
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)

        # cosine similarity 위해 L2 normalize
        embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)

        self.index.add(embedding)
        self.meta.append(name)
        self.save()

    def search(self, embedding, threshold=0.635, top_k=1):
        """가장 가까운 얼굴 검색"""
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)

        embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)

        D, I = self.index.search(embedding, top_k)
        results = []
        for idx, score in zip(I[0], D[0]):
            if idx == -1:
                continue
            if score >= threshold:
                results.append({"name": self.meta[idx], "score": float(score)})
        return results

    def search_by_name(self, name):
        """
        이름으로 등록된 embedding 값을 가져옴
        """
        if name not in self.meta:
            return None
        idx = self.meta.index(name)
        emb = self.index.reconstruct(idx)
        return emb
    
    def save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.meta_file, "w") as f:
            json.dump(self.meta, f, ensure_ascii=False)

    def load(self):
        if os.path.exists(self.index_file) and os.path.exists(self.meta_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.meta_file, "r") as f:
                self.meta = json.load(f)
