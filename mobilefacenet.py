import cv2
import numpy as np
from rknnlite.api import RKNNLite

class MobileFaceNet(object):
    def __init__(self, RK3588_RKNN_MODEL: str) -> None:
        self.rknn = RKNNLite()
        self.rknn.load_rknn(RK3588_RKNN_MODEL)
        self.rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_0_1_2)

#def init():
#    #rknn.load_rknn('./mobilefacenet.rknn')
#    rknn.load_rknn('./mobilefacenet_v2.3.2.rknn')
#    rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_0_1_2)

    def get_feat(self, img):
        img = img[..., ::-1]
        blob = np.expand_dims(img, axis=0)
        net_out = self.rknn.inference(inputs=[blob])[0]
        return net_out