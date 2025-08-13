import numpy as np
import cv2
import os
# import matplotlib
# matplotlib.use('Agg')
# import urllib.request
# from matplotlib import gridspec
# from matplotlib import pyplot as plt
# from PIL import Image
# from tensorflow.python.platform import gfile
from rknn.api import RKNN
from PIL import Image
from sklearn import preprocessing
from scipy.spatial.distance import pdist, squareform

# rknn-toolkit2에서는 mxnet을 지원않함

os.environ['RKNN_DRAW_DATA_DISTRIBUTE']="1"
def compute_cos_dis(x, y):
    cos_dist= (x* y)/(np.linalg.norm(x)*(np.linalg.norm(y)))
    return cos_dist.sum()


cfg_facenet_pytorch_onnx = {
    'modelType':"onnx",
    'model': './weights/mobilefacenet2.onnx',
    'inputs' : "input0",
    'input_size_list':[[3, 160, 160]],
    'outputs':['output0'],
    'mean_values':[[0, 0, 0]],
    'std_values':[[255, 255, 255]],
    'input_img_size':(160,160)
}

cfg_facenet_mxnet_caffe = {
    'modelType':"caffe",
    'model': './weights/mobilefacenet.prototxt',
    'blob' : './weights/mobilefacenet.caffemodel',
    'inputs' : "input0",
    'input_size_list':[[3, 112, 112]],
    'outputs':['output0'],
    'mean_values':[[127.5, 127.5, 127.5]],
    'std_values':[[128, 128, 128]],
    'input_img_size':(112,112)
}
cfg_facenet_mxnet = {
    'modelType':"mxnet",
    'inputs' : "input0",
    'input_size_list':[[3, 112, 112]],
    'outputs':['output0'],
    'mean_values':[[0, 0, 0]],
    'std_values':[[1, 1, 1]],
    'symbol' : './weights/model_mobilefacenet-symbol.json',
    'params' : './weights/model_mobilefacenet-0200.params',
    'input_img_size':(112,112)
}

if __name__ == '__main__':

    cfg = cfg_facenet_mxnet_caffe
    im_file = './9.jpg'
    BUILD_QUANT = False
    RKNN_MODEL_PATH = './mobilefacenet.rknn'
    if BUILD_QUANT:
        RKNN_MODEL_PATH = './mobilefacenet_quant.rknn'

    # Create RKNN object
    rknn = RKNN()

    print('--> config model')
    rknn.config(mean_values=cfg['mean_values'], std_values=cfg['std_values'],target_platform='rk3588')

    print('done')
    print('--> Loading model')
    if cfg['modelType'] == "caffe":
        # Load caffe model
        print("load caffe model proto[%s] weights[%s]"%(cfg['model'],cfg['blob']))
        ret = rknn.load_caffe(model=cfg['model'],blobs=cfg['blob'])
        if ret != 0:
            print('Load model failed! Ret = {}'.format(ret))
            exit(ret)
    elif cfg['modelType'] == "onnx":
        print("load onnx model model[%s] inputs[%s] input_size_list[%s] outputs[%s]"
                % (cfg['model'],cfg['inputs'],cfg['input_size_list'],cfg['outputs']))
        ret = rknn.load_onnx(model=cfg['model'],
                                inputs=cfg['inputs'],
                                input_size_list=cfg['input_size_list'],
                                outputs=cfg['outputs'])
        if ret != 0:
            print('Load retinaface failed!')
            exit(ret)
    elif cfg['modelType'] == "mxnet":# # Load mxnet model
        print("load mxnet model symbol[%s] params[%s] input_size_list[%s]" % (cfg['symbol'], cfg['params'], cfg['input_size_list']))
        ret = rknn.load_mxnet(cfg['symbol'], cfg['params'], cfg['input_size_list'])
        if ret != 0:
            print('Load mxnet model failed!')
            exit(ret)
        print('done')
    elif cfg['modelType'] == "keras":# # Load mxnet model
        ret = rknn.load_keras(model=cfg['model'])
        if ret != 0:
            print('Load keras model failed!')
            exit(ret)
        print('done')
    else:
        print('Load mxnet failed!')
        exit(-1)
    print('done')

    # Build model
    print('--> Building model')
    ret = rknn.build(do_quantization=BUILD_QUANT, dataset=None)
    if ret != 0:
        print('Build model failed!')
        exit(ret)
    print('done')

    # Export rknn model
    print('--> Export RKNN model')
    ret = rknn.export_rknn(RKNN_MODEL_PATH)

    if ret != 0:
        print('Export rknn failed!')
        exit(ret)
    print('done')

    rknn.release()

