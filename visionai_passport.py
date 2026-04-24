import cv2
import os
import numpy as np
from datetime import datetime


class PassportProcessor:
    def __init__(self):
        self.raw_dir = "saved_photos/raw"
        self.passport_dir = "saved_photos/passport_ready"

        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.passport_dir, exist_ok=True)

    # ------------------ UTILITIES ------------------

    def crop_face(self, frame, bbox, margin=60):
        """
        Crop face safely with margin
        """

        if bbox is None:
            return None

        x, y, w, h = bbox
        h_img, w_img = frame.shape[:2]

        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(w_img, x + w + margin)
        y2 = min(h_img, y + h + margin)

        cropped = frame[y1:y2, x1:x2]

        if cropped.size == 0:
            return None

        return cropped

    def resize_to_passport(self, image):
        return cv2.resize(image, (600, 600), interpolation=cv2.INTER_AREA)

    def is_blurry(self, image, threshold=100.0):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        return variance < threshold

    def save_raw_photo(self, image):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.raw_dir, f"raw_{timestamp}.jpg")
        cv2.imwrite(path, image)
        return path

    def save_passport_photo(self, image):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.passport_dir, f"passport_{timestamp}.jpg")
        cv2.imwrite(path, image)
        print(f"✅ Saved: {path}")
        return path

    # ------------------ IMAGE ENHANCEMENT ------------------

    def auto_enhance(self, image):
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)

        merged = cv2.merge((l, a, b))
        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    def align_by_eyes(self, image, left_eye, right_eye):
        """
        Rotate face so eyes are horizontal
        """

        if left_eye is None or right_eye is None:
            return image

        dx = right_eye[0] - left_eye[0]
        dy = right_eye[1] - left_eye[1]

        angle = np.degrees(np.arctan2(dy, dx))

        h, w = image.shape[:2]
        center = (w // 2, h // 2)

        rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)

        return cv2.warpAffine(
            image,
            rot_mat,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )

    def center_on_canvas(self, face_img):
        """
        Center face on white passport canvas
        """

        canvas = np.ones((600, 600, 3), dtype=np.uint8) * 255

        h, w = face_img.shape[:2]
        scale = 420 / max(h, w)

        resized = cv2.resize(face_img, (int(w * scale), int(h * scale)))

        rh, rw = resized.shape[:2]

        x_offset = (600 - rw) // 2
        y_offset = (600 - rh) // 2

        canvas[y_offset:y_offset + rh, x_offset:x_offset + rw] = resized

        return canvas

    # ------------------ FULL PIPELINE ------------------

    def process_passport(self, frame, bbox, left_eye=None, right_eye=None):
        """
        Full passport processing pipeline
        """

        # Save raw image
        self.save_raw_photo(frame)

        # Crop face
        face = self.crop_face(frame, bbox)

        if face is None:
            print("❌ Face crop failed")
            return None

        # Blur check
        if self.is_blurry(face):
            print("❌ Blurry image - retake photo")
            return None

        # Enhance lighting
        enhanced = self.auto_enhance(face)

        # Eye alignment
        enhanced = self.align_by_eyes(enhanced, left_eye, right_eye)

        # White background (optional step)
        final = self.center_on_canvas(enhanced)

        # Resize final passport image
        passport_img = self.resize_to_passport(final)

        # Save result
        return self.save_passport_photo(passport_img)

'''
import cv2
import os
import numpy as np
from datetime import datetime


class PassportProcessor:
    def __init__(self):
        self.raw_dir = "saved_photos/raw"
        self.passport_dir = "saved_photos/passport_ready"
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.passport_dir, exist_ok=True)

    # ------------------ BASIC UTILITIES ------------------

    def crop_face(self, frame, bbox, margin=60):
        x, y, w, h = bbox
        h_img, w_img = frame.shape[:2]

        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(w_img, x + w + margin)
        y2 = min(h_img, y + h + margin)

        return frame[y1:y2, x1:x2]

    def resize_to_passport(self, image):
        return cv2.resize(image, (600, 600), interpolation=cv2.INTER_AREA)

    def is_blurry(self, image, threshold=100.0):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        return variance < threshold

    def save_raw_photo(self, image):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.raw_dir, f"raw_{timestamp}.jpg")
        cv2.imwrite(path, image)
        return path

    def save_passport_photo(self, image):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.passport_dir, f"passport_{timestamp}.jpg")
        cv2.imwrite(path, image)
        print(f"✅ Passport photo saved: {path}")
        return path

    # ------------------ IMAGE IMPROVEMENTS ------------------

    def auto_enhance(self, image):
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)

        merged = cv2.merge((l, a, b))
        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    def align_by_eyes(self, image, left_eye, right_eye):
        dx = right_eye[0] - left_eye[0]
        dy = right_eye[1] - left_eye[1]
        angle = np.degrees(np.arctan2(dy, dx))

        h, w = image.shape[:2]
        center = (w // 2, h // 2)

        rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, rot_mat, (w, h), flags=cv2.INTER_CUBIC)

    def whiten_background(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        mask_inv = cv2.bitwise_not(mask)

        white_bg = np.ones_like(image, dtype=np.uint8) * 255

        person = cv2.bitwise_and(image, image, mask=mask_inv)
        background = cv2.bitwise_and(white_bg, white_bg, mask=mask)

        return cv2.add(person, background)

    def center_on_canvas(self, face_img):
        canvas = np.ones((600, 600, 3), dtype=np.uint8) * 255

        h, w = face_img.shape[:2]
        scale = 420 / max(h, w)
        resized = cv2.resize(face_img, (int(w * scale), int(h * scale)))

        rh, rw = resized.shape[:2]
        x_offset = (600 - rw) // 2
        y_offset = (600 - rh) // 2

        canvas[y_offset:y_offset + rh, x_offset:x_offset + rw] = resized
        return canvas

    # ------------------ FULL PASSPORT PIPELINE ------------------

    def process_passport(self, frame, bbox, left_eye=None, right_eye=None):
        # Save original
        self.save_raw_photo(frame)

        # Crop
        face = self.crop_face(frame, bbox)

        # Blur rejection
        if self.is_blurry(face):
            print("❌ Image is blurry. Retake photo.")
            return None

        # Lighting correction
        enhanced = self.auto_enhance(face)

        # Eye alignment (if landmarks provided)
        if left_eye and right_eye:
            enhanced = self.align_by_eyes(enhanced, left_eye, right_eye)

        # Background whitening
        whitened = self.whiten_background(enhanced)

        # Proper centering
        centered = self.center_on_canvas(whitened)

        # Final resize safeguard
        passport_img = self.resize_to_passport(centered)

        # Save final
        return self.save_passport_photo(passport_img)
    '''