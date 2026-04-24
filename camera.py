import cv2


class CameraHandler:
    def __init__(self):
        # Open default camera (0 = laptop/USB camera)
        self.capture = cv2.VideoCapture(0)

        # Set resolution
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Check camera opened successfully
        if not self.capture.isOpened():
            raise Exception("Camera could not be opened")

    def get_frame(self):
        """
        Capture and return a single frame
        """

        ret, frame = self.capture.read()

        if not ret or frame is None:
            return None

        # Mirror frame (selfie mode)
        frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        """
        Safely release camera resource
        """
        if self.capture is not None and self.capture.isOpened():
            self.capture.release()