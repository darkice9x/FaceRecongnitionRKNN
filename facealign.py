import cv2
import numpy as np

class FaceAlign(object):
    #def __init__(self) -> None:
    #    pass
    def affineMatrix(self, img, nose, leftEyeCenter, rightEyeCenter, scale_aligned=2.5, scale_crop=6):
        nose = np.array(nose, dtype=np.float32)
        left_eye = np.array(leftEyeCenter, dtype=np.float32)
        right_eye = np.array(rightEyeCenter, dtype=np.float32)
        eye_width = right_eye - left_eye
        angle = np.arctan2(eye_width[1], eye_width[0])
        center = nose
        alpha = np.cos(angle)
        beta = np.sin(angle)

        w_aligned = np.linalg.norm(right_eye - left_eye) * scale_aligned
        m = [[alpha, beta, -alpha * center[0] - beta * center[1] + w_aligned * 0.5],
            [-beta, alpha, beta * center[0] - alpha * center[1] + w_aligned * 0.5]]
        img_aligned = cv2.warpAffine(img, np.array(m), (int(w_aligned), int(w_aligned)))
        img_aligned = cv2.resize(img_aligned, (112, 112))

        w_crop = np.linalg.norm(right_eye - left_eye) * scale_crop
        cx, cy = nose
        half = int(w_crop * 0.5)
        x1, y1 = int(cx - half), int(cy - half)
        x2, y2 = int(cx + half), int(cy + half)

        h_img, w_img = img.shape[:2]
        # 경계값 클리핑
        x1 = max(0, x1); y1 = max(0, y1)
        x2 = min(w_img, x2); y2 = min(h_img, y2)

        img_crop = img[y1:y2, x1:x2]
        img_crop = cv2.resize(img_crop, (112, 112))
        return img_crop, img_aligned

    def align(self, img, nose, leftEyeCenter, rightEyeCenter):
        img_crop, img_aligned = self.affineMatrix(img, nose, leftEyeCenter, rightEyeCenter)
        return img_crop, img_aligned
    