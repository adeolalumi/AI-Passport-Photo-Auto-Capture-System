import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2

from camera import CameraHandler
from face_detector import FaceDetector
from eye_detector import EyeDetector
from visionai_passport import PassportProcessor


class PassportPhotoApp(App):

    def build(self):
        self.title = 'Passport Photo Auto Capture System'

        # UI layout
        self.layout = BoxLayout(orientation='vertical')
        self.image_widget = Image()
        self.layout.add_widget(self.image_widget)

        # ---------------- COMPONENTS ----------------
        self.camera = CameraHandler()
        self.face_detector = FaceDetector()
        self.eye_detector = EyeDetector()
        self.passport_processor = PassportProcessor()

        # ---------------- STATE ----------------
        self.eye_open_frames = 0
        self.required_frames = 45
        self.captured = False

        # Run update loop (30 FPS)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

        return self.layout

    def update(self, dt):
        frame = self.camera.get_frame()

        if frame is None:
            return

        # ---------------- DETECTION ----------------
        faces = self.face_detector.detect_faces(frame)

        eyes_open, left_eye, right_eye = self.eye_detector.are_eyes_open(frame)

        # Eye tracking logic
        if eyes_open:
            self.eye_open_frames += 1
        else:
            self.eye_open_frames = 0
            self.captured = False

        # ---------------- AUTO CAPTURE ----------------
        if self.eye_open_frames >= self.required_frames and not self.captured and faces:

            face_bbox = faces[0]

            raw_cropped = self.passport_processor.crop_face(frame, face_bbox)

            if raw_cropped is not None:

                if not self.passport_processor.is_blurry(raw_cropped):

                    final_photo = self.passport_processor.resize_to_passport(raw_cropped)

                    self.passport_processor.save_raw_photo(raw_cropped)
                    self.passport_processor.save_passport_photo(final_photo)

                    self.captured = True
                    self.eye_open_frames = 0

                else:
                    cv2.putText(
                        frame,
                        "Blurry - Hold steady",
                        (30, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 0, 255),
                        2
                    )

        # ---------------- UI FEEDBACK ----------------
        status = f"Eyes Open: {self.eye_open_frames}/{self.required_frames}"
        color = (0, 255, 0) if eyes_open else (0, 0, 255)

        cv2.putText(frame, status, (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

        if self.captured:
            cv2.putText(frame, "✅ PASSPORT PHOTO CAPTURED!",
                        (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 255, 0),
                        3)

        # ---------------- KIVY DISPLAY ----------------
        buf = cv2.flip(frame, 0).tobytes()

        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt='bgr'
        )

        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image_widget.texture = texture

    def on_stop(self):
        self.camera.release()


if __name__ == '__main__':
    PassportPhotoApp().run()
'''
import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
from camera import CameraHandler
from face_detector import FaceDetector
from eye_detector import EyeDetector
from visionai_passport import PassportProcessor


class PassportPhotoApp(App):
    
    def build(self):
        self.title = 'Passport Photo Auto Capture Sysytem'

        self.layout = BoxLayout(orientation = 'vertical')
        self.image_widget = Image()
        self.layout.add_widget(self.image_widget)

        # Start component

        self.camera = CameraHandler
        self.face_detector = FaceDetector()
        self.eye_detector = EyeDetector()
        self.visionai_passport = PassportProcessor()

        # State

        self.eye_open_frames = 0
        self.required_frames = 45
        self.capturing = False

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return self.layout
    
    def update(self, dt):
        frame = self.camera.get_frame()
        if frame is None:
            return


        # Face detection and Eye detection
        faces = self.face_detector.detect_faces(frame)
        eyes_open = self.eye_detector.are_eyes_open(frame)


        if eyes_open:
            self.eye_open_frames += 1

        else:
            self.eye_open_frames = 0
            self.captured = False


        # auto capture logic
        if (self.eye_open_frames > self.required_frames and not 
           self.captured and faces):
            face_bbox = faces[0]
            raw_cropped = self.visionai_passport.crop_face(frame, face_bbox)

            if not self.visionai_passport.isblurry(raw_cropped):
                final_photo = self.visionai_passport.resize_to_passport(raw_cropped)

                self.visionai_passport.save_raw_photo(raw_cropped)
                self.visionai_passport.save_passport_photo(final_photo)

                self.captured = True
                self.eye_open_frames = 0
            else:
                cv2.putText(frame, "Blurry - Hold steady", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 2)


        # Display feedback
        status = f"Eyes Open: {self.eye_open_frames}/{self.required_frames}"
        color = (0, 255, 0) if eyes_open else (0, 0, 255)


        cv2.putText(frame, status, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

        if self.captured:
            cv2.putText(frame, "✅ PASSPORT PHOTO CAPTURED!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)


        # Convert to kivy texture

        buf = cv2.flip(frame,0).tobytes()
        texture = Texture.create(size =(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt = 'ubyte')
        self.image_widget.texture = texture

    def on_stop(self):
        self.camera.release()

if __name__ == '__main__':
    PassportPhotoApp().run()

    '''