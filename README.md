Passport Photo Auto-Capture System (Kivy + OpenCV + MediaPipe + SQLite)

An intelligent desktop application that automatically captures passport-compliant photos when the user is correctly positioned, eyes are open, the face is detected, and the image is sharp enough for quality standards.

Built with Python, Kivy UI, OpenCV, MediaPipe Face Mesh, and SQLite logging.

🚀 Features
Real-time webcam preview inside a Kivy interface
Automatic face detection using MediaPipe Face Mesh
Eye-open detection before capture
Blur detection using Laplacian variance
Automatic face crop to passport framing
Resize to passport dimensions
Raw photo + final passport photo saving
SQLite database logging of every capture attempt
Dynamic UI background support
Fully automated — no button press required
🧠 How It Works
Camera stream opens inside the app
Face landmarks are detected in real time
System checks:
Face present
Eyes open for a number of frames
Image is not blurry
If all conditions pass:
Face is cropped
Image resized to passport standard
Images saved
Event logged to database
🗂️ Project Structure
project/
│
├── main.py
├── camera.py
├── face_detector.py
├── eye_detector.py
├── visionai_passport.py
├── database.py
├── util.py
│
├── assets/
│   └── backgrounds/
│
├── output/
│   ├── raw/
│   └── passport/
│
└── passport_logs.db
⚙️ Requirements
Python 3.10+
Webcam
Good lighting environment
Install dependencies
pip install opencv-python mediapipe kivy numpy
▶️ Run the App
python main.py

The system starts the camera and waits for the correct capture conditions.

🗃️ SQLite Logging

Every capture attempt is recorded in passport_logs.db:

id	timestamp	raw_image	passport_image	status	blur_score

This allows auditing and quality analysis of captures.

⚠️ Capture Environment Requirements (Important)

This system depends heavily on good lighting for accurate computer vision.

✅ Required
Bright room lighting or daylight
Light facing the user’s face
Plain/light background
Camera steady
User looking straight ahead
Eyes open for a few seconds
❌ Will Cause Poor Results
Dim or dark rooms
Backlighting (light behind user)
Face shadows
Movement or shaking camera

Low light can cause failed detection or poor passport quality. This is a computer vision limitation, not a software bug.

🧩 Technologies Used
Python
OpenCV
MediaPipe
Kivy
SQLite
💡 Use Cases
Passport photo booths
Automated ID photo systems
Computer vision research projects
Smart camera applications
👤 Author

Adeola Odunewu
Hackney, London
Python • Machine Learning • Computer Vision • Kivy UI
