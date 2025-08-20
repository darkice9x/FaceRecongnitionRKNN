import mxnet as mx
from mxnet.contrib import onnx as onnx_mxnet
import numpy as np

# Define paths to your MXNet model files
sym_file = './weights/model_mobilefacenet-symbol.json'
params_file = './weights/model_mobilefacenet-0200.params'

# Define input shape and data type (e.g., for an image classification model)
input_shape = (1, 3, 224, 224) # Batch size, channels, height, width
input_type = np.float32

# Define the output ONNX file path
onnx_file = './mobilefacenet.onnx'

# Export the model
onnx_mxnet.export_model(sym_file, params_file, [input_shape], input_type, onnx_file)

print(f"MXNet model exported to ONNX at: {onnx_file}")