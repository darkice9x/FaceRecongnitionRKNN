# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np
#import yaml
from rknn.api import RKNN


DATASET = './dataset.txt'
TARGET = 'RK3588'
quan = '_i8'

def export_rknn(ONNX_MODEL, QUANTIZE_ON):
    rknn = RKNN(verbose=True)

    rknn.config(
        mean_values=[[104, 117, 123]], std_values=[[1, 1, 1]],
        #quantized_algorithm='normal',
        #quantized_method='channel',
        # optimization_level=2,
        #compress_weight=False,  # 压缩模型的权值，可以减小rknn模型的大小。默认值为False。
        # single_core_mode=True,
        # model_pruning=False,  # 修剪模型以减小模型大小，默认值为False。
        target_platform='rk3588'
    )
    rknn.load_onnx(
        model=ONNX_MODEL,
#	input_size_list=[1,3,64,64]
#        outputs=[
#            '/model.22/Mul_2_output_0', '/model.22/Split_output_1',
#        ]
    )
    ONNX_MODEL1 = os.path.splitext(ONNX_MODEL)[0]
    if QUANTIZE_ON :
        quan = '_i8'
    else:
        quan = ''

    RKNN_MODEL = f'{ONNX_MODEL1}-{TARGET}{quan}.rknn'
    rknn.build(do_quantization=QUANTIZE_ON, dataset=DATASET, rknn_batch_size=1)
    rknn.export_rknn(RKNN_MODEL)

    # # 精度分析
    # rknn.accuracy_analysis(
    #     inputs=['/home/tm1/D/workspace/onnx2rknn_YOLOv8/onnx_model/official/zidane.jpg'],
    #     output_dir="./snapshot",
    #     target=None
    # )
    rknn.release()

if __name__ == '__main__':
    
    ONNX_MODEL = './RetinaFace_mobile320.onnx'
    # 转换模型
    rknn = export_rknn(ONNX_MODEL, True)
    rknn = export_rknn(ONNX_MODEL, False)

