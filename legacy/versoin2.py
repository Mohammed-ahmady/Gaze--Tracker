import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# إعداد mediapipe iris
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,  # ضروري علشان يجيب البؤبؤ (iris landmarks)
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# إعداد pyautogui
pyautogui.FAILSAFE = False
screen_w, screen_h = pyautogui.size()

# فتح الكاميرا
cap = cv2.VideoCapture(0)
blink_cooldown = 1.0
last_blink_time = 0

def euclidean_dist(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def get_ear(eye_landmarks):
    A = euclidean_dist(eye_landmarks[1], eye_landmarks[5])
    B = euclidean_dist(eye_landmarks[2], eye_landmarks[4])
    C = euclidean_dist(eye_landmarks[0], eye_landmarks[3])
    ear = (A + B) / (2.0 * C)
    return ear

print("✅ Eye Tracking Mouse (Iris Version - Enhanced)")
print("➡ Move only your eyes to control cursor")
print("➡ Blink to click")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    h, w, _ = frame.shape

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0].landmark

        # نقاط العين اليمنى واليسرى
        right_eye_ids = [33, 160, 158, 133, 153, 144]
        left_eye_ids = [362, 385, 387, 263, 373, 380]
        right_iris_ids = [468, 469, 470, 471]
        left_iris_ids = [473, 474, 475, 476]

        right_eye = [(int(face_landmarks[i].x * w), int(face_landmarks[i].y * h)) for i in right_eye_ids]
        left_eye = [(int(face_landmarks[i].x * w), int(face_landmarks[i].y * h)) for i in left_eye_ids]
        right_iris = [(int(face_landmarks[i].x * w), int(face_landmarks[i].y * h)) for i in right_iris_ids]
        left_iris = [(int(face_landmarks[i].x * w), int(face_landmarks[i].y * h)) for i in left_iris_ids]

        # مركز البؤبؤ
        (rx, ry), r_radius = cv2.minEnclosingCircle(np.array(right_iris))
        (lx, ly), l_radius = cv2.minEnclosingCircle(np.array(left_iris))
        center_x = int((rx + lx) / 2)
        center_y = int((ry + ly) / 2)
        avg_radius = int((r_radius + l_radius) / 2)

        # رسم البؤبؤ (للتوضيح البصري)
        cv2.circle(frame, (int(rx), int(ry)), int(r_radius), (255, 0, 0), 2)
        cv2.circle(frame, (int(lx), int(ly)), int(l_radius), (255, 0, 0), 2)
        cv2.circle(frame, (center_x, center_y), 3, (0, 0, 255), -1)

        # تكبير حركة البؤبؤ (Zoom mapping)
        eye_center_x = np.interp(center_x, [w * 0.3, w * 0.7], [0, screen_w])
        eye_center_y = np.interp(center_y, [h * 0.3, h * 0.7], [0, screen_h])

        # حركة أكثر ثباتًا
        pyautogui.moveTo(eye_center_x, eye_center_y, duration=0.1)

        # حساب EAR للرمش
        right_ear = get_ear(right_eye)
        left_ear = get_ear(left_eye)
        ear = (right_ear + left_ear) / 2.0

        if ear < 0.2:
            qcurrent_time = time.time()
            if current_time - last_blink_time > blink_cooldown:
                pyautogui.click()
                last_blink_time = current_time
                cv2.putText(frame, "Blink Detected - Click!", (50, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 2)

    cv2.imshow("Eye Tracking Mouse - Iris Enhanced", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()