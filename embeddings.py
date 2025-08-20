import numpy as np
import cv2
from math import ceil
from itertools import product as product
from retinaface import RetinaFace
from mobilefacenet import MobileFaceNet
import time

class Embeddings(object):
    def __init__(self,
                 #yolo_model: str,
                 RK3588_RETINA_RKNN_MODEL: str,
                 RK3588_MOBILEFACENET_RKNN_MODEL: str,
                 ) -> None:
        self.retinaface = RetinaFace(RK3588_RETINA_RKNN_MODEL)
        self.mobilefacenet = MobileFaceNet(RK3588_MOBILEFACENET_RKNN_MODEL)

    def get_embeddings(self, image):
        retina_ret = self.retinaface.get_faces(image)
        if retina_ret == None: return None
        embedder_ret = []
        for face in retina_ret:
            embedding = self.mobilefacenet.get_feat(face['face'])
            embedder_ret.append({'score':face['score'], 'embedding':embedding})
        return embedder_ret
    '''
    def cosine_similarity(self, vec1, vec2):
        vec1 = vec1.reshape(1, -1)

        dot_product = np.dot(vec1, vec2.T)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2, axis=1)

        similarity = dot_product / (norm_vec1 * norm_vec2)
        return similarity
    '''
    def cosine_similarity(self, vec1, vec2):
        """
        vec1: (1,128)
        vec2: (1,128)
        """
        # 벡터 정규화
        v1 = vec1 / np.linalg.norm(vec1)
        v2 = vec2 / np.linalg.norm(vec2)

        # 내적 값 = cosine similarity
        return float(np.dot(v1, v2.T))
        
    def compute_sim(self, embedding1, embedding2, thres=0.635):
        distance = self.cosine_similarity(embedding1, embedding2)
        return distance > thres

    def compare_face(self, embedding1, embedding2, thres=0.635):
        #distance = self.cosine_similarity(embedding1, embedding2)
        #return distance[0] > thres, distance[0]
        distance = self.cosine_similarity(embedding1, embedding2)
        return distance > thres, distance
