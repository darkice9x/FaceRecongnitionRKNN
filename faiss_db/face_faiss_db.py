import os
import numpy as np
import faiss

class FaceFaissDB:
    def __init__(self, dim=512, db_path="facefaiss.index", use_gpu=False):
        self.dim = dim
        self.db_path = db_path
        self.names_path = db_path + ".names"
        self.ids = []  # index -> name

        # 코사인 유사도 위해 normalized + IP index
        base_index = faiss.IndexFlatIP(dim)
        self.gpu = use_gpu

        if use_gpu:
            res = faiss.StandardGpuResources()
            base_index = faiss.index_cpu_to_gpu(res, 0, base_index)

        # IDMap으로 감싸서 add 시 id값 직접 넣기 가능하게 함
        self.index = faiss.IndexIDMap(base_index)

        # 기존 DB 자동 로드
        if os.path.exists(self.db_path) and os.path.exists(self.names_path):
            self.load()
        else:
            print("새로운 FaceFaissDB를 생성합니다.")

    def add(self, name, emb):
        emb = emb.astype('float32')
        emb = emb / np.linalg.norm(emb)

        # 현재 길이를 id (int) 로 사용
        idx = len(self.ids)
        self.index.add_with_ids(emb[np.newaxis, :], np.array([idx], dtype=np.int64))
        self.ids.append(name)
        print(f"추가됨: {name}")

        self.save()

    def search(self, query_emb, topk=1):
        query_emb = query_emb.astype('float32')
        q = query_emb / np.linalg.norm(query_emb)

        D, I = self.index.search(q[np.newaxis, :], topk)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0: continue
            emb = {'name' : self.ids[idx], 'feature' : float(dist)}
            results.append(emb)
        return results

    def save(self):
        # GPU → CPU 로 저장
        if self.gpu:
            cpu_index = faiss.index_gpu_to_cpu(self.index)
            faiss.write_index(cpu_index, self.db_path)
        else:
            faiss.write_index(self.index, self.db_path)

        with open(self.names_path, "w") as f:
            for name in self.ids:
                f.write(name + "\n")
        print("자동 저장 완료 ✅")

    def load(self):
        self.index = faiss.read_index(self.db_path)
        with open(self.names_path, "r") as f:
            self.ids = [line.strip() for line in f]
        print(f"DB 로드 완료 ({len(self.ids)}명)")
