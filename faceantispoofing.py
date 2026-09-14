"""TensorFlow Lite inference for MiniFASNet face anti-spoofing with Crop Visualization."""

import argparse
import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter
import time


class AntiSpoofingTFLite:
    """Face anti-spoofing inference using LiteRT Interpreter."""

    def __init__(self, model_path: str, scale: float = 2.7) -> None:
        """Initialize the AntiSpoofingTFLite class.

        Args:
            model_path: Path to the LiteRT / TFLite model file (.tflite).
            scale: Crop scale factor for face region.
        """
        # LiteRT Interpreter 직접 인스턴스화
        self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # 입력/출력 텐서 정보 가져오기
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # 모델 입출력 인덱스 및 형상(Shape) 확인
        self.input_index = self.input_details[0]["index"]
        self.output_index = self.output_details[0]["index"]

        input_shape = self.input_details[0]["shape"]  # e.g., [1, 3, 80, 80] 또는 [1, 80, 80, 3]

        # NCHW / NHWC 레이아웃 판별 및 입력 크기 추출
        if input_shape[1] == 3 or input_shape[1] == 1:
            # NCHW 레이아웃 (Batch, Channels, Height, Width)
            self.is_nchw = True
            self.input_size = (input_shape[2], input_shape[3])
        else:
            # NHWC 레이아웃 (Batch, Height, Width, Channels)
            self.is_nchw = False
            self.input_size = (input_shape[1], input_shape[2])

        self.scale = scale
        print(f"Model Input Size (H, W): {self.input_size}, Layout NCHW: {self.is_nchw}")

    def _xyxy2xywh(self, bbox: list[float]) -> list[int]:
        """Convert [x1, y1, x2, y2] to [x, y, w, h]."""
        x1, y1, x2, y2 = bbox
        return [int(x1), int(y1), int(x2 - x1), int(y2 - y1)]

    def get_crop_box(self, image: np.ndarray, bbox: list[int]) -> list[int]:
        """Calculate scaled crop box coordinates [x1, y1, x2, y2]."""
        src_h, src_w = image.shape[:2]
        x, y, box_w, box_h = bbox

        scale = min((src_h - 1) / box_h, (src_w - 1) / box_w, self.scale)
        new_w = box_w * scale
        new_h = box_h * scale

        center_x = x + box_w / 2
        center_y = y + box_h / 2

        x1 = max(0, int(center_x - new_w / 2))
        y1 = max(0, int(center_y - new_h / 2))
        x2 = min(src_w - 1, int(center_x + new_w / 2))
        y2 = min(src_h - 1, int(center_y + new_h / 2))

        return [x1, y1, x2, y2]

    def _crop_face(self, image: np.ndarray, bbox: list[int]) -> tuple[np.ndarray, list[int]]:
        """Crop and resize face region from image."""
        crop_box = self.get_crop_box(image, bbox)
        x1, y1, x2, y2 = crop_box

        cropped = image[y1 : y2 + 1, x1 : x2 + 1]
        resized = cv2.resize(cropped, self.input_size[::-1])
        return resized, crop_box

    def _preprocess(self, image: np.ndarray, bbox: list[int]) -> tuple[np.ndarray, list[int], np.ndarray]:
        """Preprocess face crop for LiteRT inference."""
        face, crop_box = self._crop_face(image, bbox)
        face_tensor = face.astype(np.float32)

        # 변환된 모델의 레이아웃 형태에 따라 transpose 처리
        if self.is_nchw:
            face_tensor = np.transpose(face_tensor, (2, 0, 1))  # (H, W, C) -> (C, H, W)

        face_tensor = np.expand_dims(face_tensor, axis=0)  # 배치 차원 추가
        return face_tensor, crop_box, face

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Apply softmax to logits."""
        e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return e_x / e_x.sum(axis=1, keepdims=True)

    def predict(self, image: np.ndarray, bbox_xyxy: list[float]) -> dict:
        """Predict if face is real or fake using LiteRT model.

        Returns:
            Dictionary with keys: label, score, bbox (xywh format), crop_box, cropped_face.
        """
        bbox_xywh = self._xyxy2xywh(bbox_xyxy)

        input_tensor, crop_box, cropped_face = self._preprocess(image, bbox_xywh)

        # LiteRT 텐서 데이터 설정 및 추론 수행
        self.interpreter.set_tensor(self.input_index, input_tensor)
        self.interpreter.invoke()
        logits = self.interpreter.get_tensor(self.output_index)

        probs = self._softmax(logits)

        label_idx = int(np.argmax(probs))
        score = float(probs[0, label_idx])

        return {
            "label": "Real" if label_idx == 1 else "Fake",
            "score": score,
            "bbox": bbox_xywh,
            "crop_box": crop_box,
            "cropped_face": cropped_face,
        }