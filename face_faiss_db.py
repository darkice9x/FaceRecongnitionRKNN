import os
import numpy as np
import faiss

class FaceFaissDB:
    def __init__(self, dim=512, db_path="facefaiss.index", use_gpu=False):
        """
        dim: embedding 차원
        db_path: 저장할 파일 경로
        """
        self.dim = dim
        self.db_path = db_path
        self.names_path = db_path + ".names"
        self.ids = []  # index -> name 매핑

        # Cosine similarity를 위해 normalized vector + IP index 사용
        self.index = faiss.IndexFlatIP(dim)

        if use_gpu:
            res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(res, 0, self.index)

        # 기존 DB 있으면 자동로드
        if os.path.exists(self.db_path) and os.path.exists(self.names_path):
            self.load()
        else:
            print("새로운 FaceFaissDB를 생성합니다.")

    def add(self, name, emb):
        """
        새로운 (name, embedding) 저장 & 자동 저장
        """
        emb = emb.astype('float32')
        emb = emb / np.linalg.norm(emb)

        self.index.add(emb[np.newaxis, :])
        self.ids.append(name)
        #print(f"추가됨: {name}")

        # 자동 저장
        self.save()

    def search(self, query_emb, topk=1):
        """
        query_emb 와 DB 내에서 가장 유사한 topk (name, similarity) 반환
        """
        query_emb = query_emb.astype('float32')
        q = query_emb #/ np.linalg.norm(query_emb)

        D, I = self.index.search(q[np.newaxis, :], topk)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0: continue
            results.append({'name': self.ids[idx], 'feature': float(dist)})
        return results

    def search_by_name(self, name):
        """
        이름으로 등록된 embedding 값을 가져옴
        """
        if name not in self.ids:
            return None
        idx = self.ids.index(name)
        emb = self.index.reconstruct(idx)
        return emb
    
    def save(self):
        faiss.write_index(self.index, self.db_path)
        with open(self.names_path, "w") as f:
            for name in self.ids:
                f.write(name + "\n")
        #print("자동 저장 완료 ✅")

    def load(self):
        self.index = faiss.read_index(self.db_path)
        with open(self.names_path, "r") as f:
            self.ids = [line.strip() for line in f]
        #print(f"DB 로드 완료 ({len(self.ids)}명)")
