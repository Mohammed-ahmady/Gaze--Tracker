import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import json

pyautogui.FAILSAFE = False

class EyeTracker:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
        self.cap = cv2.VideoCapture(0)
        self.screen_w, self.screen_h = pyautogui.size()
        self.iris = [474, 475, 476, 477, 469, 470, 471, 472]  # Both eyes
        self.cal_data = []
        print("Eye Tracker Ready - Press 'c' to calibrate, 'q' to quit")

    def get_eye_pos(self, landmarks):
        iris_pts = landmarks[self.iris]
        x = np.mean([p[0] for p in iris_pts]) / 640
        y = np.mean([p[1] for p in iris_pts]) / 480
        return x, y

    def calibrate(self):
        print("Calibration: Look at corners, center, press SPACE")
        points = [(0.1, 0.1), (0.9, 0.1), (0.1, 0.9), (0.9, 0.9), (0.5, 0.5)]
        self.cal_data = []
        
        for i, (px, py) in enumerate(points):
            sx, sy = int(px * self.screen_w), int(py * self.screen_h)
            print(f"Look at point {i+1}/5")
            
            while True:
                ret, frame = self.cap.read()
                if not ret: continue
                
                frame = cv2.flip(frame, 1)
                cv2.circle(frame, (int(px*640), int(py*480)), 30, (0,0,255), -1)
                cv2.putText(frame, f"Point {i+1}/5 - SPACE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                
                results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                if results.multi_face_landmarks:
                    landmarks = np.array([(lm.x*640, lm.y*480) for lm in results.multi_face_landmarks[0].landmark])
                    ex, ey = self.get_eye_pos(landmarks)
                    cv2.putText(frame, "Face OK", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                
                cv2.imshow('Calibration', frame)
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord(' ') and results.multi_face_landmarks:
                    self.cal_data.append({'ex': ex, 'ey': ey, 'sx': sx, 'sy': sy})
                    print(f"✓ Point {i+1}")
                    break
                elif key == 27: return False
        
        with open('cal.json', 'w') as f: json.dump(self.cal_data, f)
        cv2.destroyAllWindows()
        return True

    def predict(self, ex, ey):
        if not self.cal_data: return None, None
        dists = [((ex-p['ex'])**2 + (ey-p['ey'])**2)**0.5 for p in self.cal_data]
        closest = self.cal_data[np.argmin(dists)]
        return closest['sx'], closest['sy']

    def run(self):
        try:
            with open('cal.json') as f: self.cal_data = json.load(f)
            print("Calibration loaded")
        except:
            if not self.calibrate(): return
        
        while True:
            ret, frame = self.cap.read()
            if not ret: break
            
            frame = cv2.flip(frame, 1)
            results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            if results.multi_face_landmarks:
                landmarks = np.array([(lm.x*640, lm.y*480) for lm in results.multi_face_landmarks[0].landmark])
                ex, ey = self.get_eye_pos(landmarks)
                cx, cy = self.predict(ex, ey)
                
                if cx and cy: pyautogui.moveTo(cx, cy)
                cv2.putText(frame, "TRACKING", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            else:
                cv2.putText(frame, "NO FACE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            
            cv2.imshow('Eye Tracker', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): break
            elif key == ord('c'): self.calibrate()
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    EyeTracker().run()