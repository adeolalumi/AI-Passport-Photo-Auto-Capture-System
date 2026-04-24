import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class EyeDetector:
    def __init__(self):
        # Load FaceLandmarker model
        base_options = python.BaseOptions(
            model_asset_path="face_landmarker.task"
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1
        )

        self.detector = vision.FaceLandmarker.create_from_options(options)

        # Eye landmark indices (same as before)
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    # -------- Eye Aspect Ratio (EAR) --------
    def get_ear(self, landmarks, eye_points):
        A = abs(landmarks[eye_points[1]].y - landmarks[eye_points[5]].y)
        B = abs(landmarks[eye_points[2]].y - landmarks[eye_points[4]].y)
        C = abs(landmarks[eye_points[0]].y - landmarks[eye_points[3]].y)

        return (A + B) / (2.0 * C) if C > 0 else 0

    # -------- Eye Check --------
    def are_eyes_open(self, frame, threshold=0.25):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.detector.detect(mp_image)

        if not result.face_landmarks:
            return False, None, None

        landmarks = result.face_landmarks[0]

        left_ear = self.get_ear(landmarks, self.LEFT_EYE)
        right_ear = self.get_ear(landmarks, self.RIGHT_EYE)

        eyes_open = (left_ear > threshold) and (right_ear > threshold)

        # -------- Eye positions --------
        h, w = frame.shape[:2]

        left_eye = (
            int(landmarks[33].x * w),
            int(landmarks[33].y * h)
        )

        right_eye = (
            int(landmarks[263].x * w),
            int(landmarks[263].y * h)
        )

        return eyes_open, left_eye, right_eye