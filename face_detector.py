import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceDetector:
    def __init__(self):
        # Load MediaPipe FaceLandmarker model
        base_options = python.BaseOptions(
            model_asset_path="face_landmarker.task"
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=5
        )

        self.detector = vision.FaceLandmarker.create_from_options(options)

    def detect_faces(self, frame):
        """
        Detect faces and return bounding boxes as (x, y, w, h)
        """

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to MediaPipe Image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Run detection
        result = self.detector.detect(mp_image)

        faces = []

        if result.face_landmarks:
            h, w, _ = frame.shape

            for landmarks in result.face_landmarks:
                # Convert normalized landmarks to pixel coords
                x_coords = [int(lm.x * w) for lm in landmarks]
                y_coords = [int(lm.y * h) for lm in landmarks]

                # Safe padded bounding box
                x_min = max(min(x_coords) - 20, 0)
                y_min = max(min(y_coords) - 20, 0)

                x_max = min(max(x_coords) + 20, w)
                y_max = min(max(y_coords) + 20, h)

                box_w = x_max - x_min
                box_h = y_max - y_min

                faces.append((x_min, y_min, box_w, box_h))

        return faces
'''
import cv2
import mediapipe as mp


class FaceDetector:
    def __init__(self):
        self.face_mesh = mp.mediapipe.tasks.python.vision.FaceMesh(
            refine_landmarks = True,
            min_detection_confidence = 0.7
            )
    def dectect_faces(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        faces = []
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h, w, _ = frame.shape
                x_coords = [int(lm.x* w) for lm in face_landmarks.landmark]
                y_coords = [int(lm.y* h) for lm in face_landmarks.landmark]


                x = min(x_coords)
                y = min(y_coords)

                w_box = max(x_coords) - x
                h_box = max(y_coords) - y


                faces.append((x, y, w_box, h_box))
        return faces
'''