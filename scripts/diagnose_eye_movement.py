"""
Eye Movement Range Diagnostic Tool
===================================
This tool shows you in real-time how much your eyes are actually moving
according to the camera detection.
"""

import cv2
import mediapipe as mp
import numpy as np
from collections import deque

class EyeMovementDiagnostic:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Iris indices
        self.LEFT_IRIS = [474, 475, 476, 477, 478]
        self.RIGHT_IRIS = [469, 470, 471, 472, 473]
        self.LEFT_EYE = [33, 133, 160, 159, 158, 144]
        self.RIGHT_EYE = [362, 263, 387, 386, 385, 380]
        
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Track min/max eye positions
        self.eye_x_min = 1.0
        self.eye_x_max = 0.0
        self.eye_y_min = 1.0
        self.eye_y_max = 0.0
        
        # History for visualization
        self.history_x = deque(maxlen=100)
        self.history_y = deque(maxlen=100)
    
    def get_eye_relative_pos(self, landmarks, eye_indices, iris_indices):
        """Get eye position relative to eye boundaries."""
        eye_points = np.array([[landmarks[i][0], landmarks[i][1]] for i in eye_indices])
        iris_points = np.array([[landmarks[i][0], landmarks[i][1]] for i in iris_indices])
        
        iris_center_x = np.mean([p[0] for p in iris_points])
        iris_center_y = np.mean([p[1] for p in iris_points])
        
        eye_left = eye_points[0]
        eye_right = eye_points[3]
        eye_top = np.mean([eye_points[1], eye_points[2]], axis=0)
        eye_bottom = np.mean([eye_points[4], eye_points[5]], axis=0)
        
        eye_width = np.linalg.norm(eye_right - eye_left)
        eye_height = np.linalg.norm(eye_bottom - eye_top)
        
        horizontal_ratio = (iris_center_x - eye_left[0]) / (eye_width + 1e-6)
        vertical_ratio = (iris_center_y - eye_top[1]) / (eye_height + 1e-6)
        
        return float(np.clip(horizontal_ratio, 0.0, 1.0)), float(np.clip(vertical_ratio, 0.0, 1.0))
    
    def run(self):
        """Run diagnostic tool."""
        print("\n" + "="*80)
        print("EYE MOVEMENT RANGE DIAGNOSTIC")
        print("="*80)
        print("\nInstructions:")
        print("1. Look at the camera")
        print("2. Move your eyes to EXTREME positions:")
        print("   - Look AS FAR UP as possible")
        print("   - Look AS FAR DOWN as possible")
        print("   - Look AS FAR LEFT as possible")
        print("   - Look AS FAR RIGHT as possible")
        print("3. Try all 4 corners")
        print("4. Press 'Q' to quit and see results")
        print("\nThe display shows:")
        print("  - Current eye position (green crosshair)")
        print("  - Min/Max ranges detected (red lines)")
        print("  - Real-time values")
        print("\n" + "="*80 + "\n")
        
        cv2.namedWindow("Eye Movement Diagnostic", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Eye Movement Diagnostic", 800, 600)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            # Create visualization canvas
            viz = np.zeros((600, 800, 3), dtype=np.uint8)
            
            if results.multi_face_landmarks:
                landmarks = np.array([
                    (lm.x * self.frame_width, lm.y * self.frame_height)
                    for lm in results.multi_face_landmarks[0].landmark
                ])
                
                left_eye = self.get_eye_relative_pos(landmarks, self.LEFT_EYE, self.LEFT_IRIS)
                right_eye = self.get_eye_relative_pos(landmarks, self.RIGHT_EYE, self.RIGHT_IRIS)
                
                avg_x = (left_eye[0] + right_eye[0]) / 2
                avg_y = (left_eye[1] + right_eye[1]) / 2
                
                # Update min/max
                self.eye_x_min = min(self.eye_x_min, avg_x)
                self.eye_x_max = max(self.eye_x_max, avg_x)
                self.eye_y_min = min(self.eye_y_min, avg_y)
                self.eye_y_max = max(self.eye_y_max, avg_y)
                
                # Add to history
                self.history_x.append(avg_x)
                self.history_y.append(avg_y)
                
                # Draw visualization
                # Background grid
                for i in range(0, 800, 100):
                    cv2.line(viz, (i, 0), (i, 600), (30, 30, 30), 1)
                for i in range(0, 600, 100):
                    cv2.line(viz, (0, i), (800, i), (30, 30, 30), 1)
                
                # Center lines
                cv2.line(viz, (400, 0), (400, 600), (50, 50, 50), 2)
                cv2.line(viz, (0, 300), (800, 300), (50, 50, 50), 2)
                
                # Draw min/max boundaries (red)
                x_min_px = int(self.eye_x_min * 800)
                x_max_px = int(self.eye_x_max * 800)
                y_min_px = int(self.eye_y_min * 600)
                y_max_px = int(self.eye_y_max * 600)
                
                cv2.line(viz, (x_min_px, 0), (x_min_px, 600), (0, 0, 255), 2)  # Left boundary
                cv2.line(viz, (x_max_px, 0), (x_max_px, 600), (0, 0, 255), 2)  # Right boundary
                cv2.line(viz, (0, y_min_px), (800, y_min_px), (0, 0, 255), 2)  # Top boundary
                cv2.line(viz, (0, y_max_px), (800, y_max_px), (0, 0, 255), 2)  # Bottom boundary
                
                # Draw current position (green crosshair)
                curr_x = int(avg_x * 800)
                curr_y = int(avg_y * 600)
                cv2.line(viz, (curr_x - 20, curr_y), (curr_x + 20, curr_y), (0, 255, 0), 3)
                cv2.line(viz, (curr_x, curr_y - 20), (curr_x, curr_y + 20), (0, 255, 0), 3)
                cv2.circle(viz, (curr_x, curr_y), 5, (0, 255, 0), -1)
                
                # Draw history trail
                if len(self.history_x) > 1:
                    for i in range(1, len(self.history_x)):
                        x1 = int(self.history_x[i-1] * 800)
                        y1 = int(self.history_y[i-1] * 600)
                        x2 = int(self.history_x[i] * 800)
                        y2 = int(self.history_y[i] * 600)
                        alpha = i / len(self.history_x)
                        color = (int(100 * alpha), int(150 * alpha), int(200 * alpha))
                        cv2.line(viz, (x1, y1), (x2, y2), color, 1)
                
                # Display text info
                x_range = self.eye_x_max - self.eye_x_min
                y_range = self.eye_y_max - self.eye_y_min
                
                cv2.putText(viz, "Eye Movement Diagnostic", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                cv2.putText(viz, f"Current Position: ({avg_x:.3f}, {avg_y:.3f})", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                cv2.putText(viz, f"X Range: {self.eye_x_min:.3f} to {self.eye_x_max:.3f} = {x_range:.3f}", (10, 100),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                cv2.putText(viz, f"Y Range: {self.eye_y_min:.3f} to {self.eye_y_max:.3f} = {y_range:.3f}", (10, 130),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                # Status indicators
                x_status = "GOOD" if x_range > 0.5 else ("MODERATE" if x_range > 0.3 else "POOR")
                y_status = "GOOD" if y_range > 0.4 else ("MODERATE" if y_range > 0.25 else "POOR")
                x_color = (0, 255, 0) if x_range > 0.5 else ((0, 255, 255) if x_range > 0.3 else (0, 0, 255))
                y_color = (0, 255, 0) if y_range > 0.4 else ((0, 255, 255) if y_range > 0.25 else (0, 0, 255))
                
                cv2.putText(viz, f"Horizontal: {x_status}", (10, 170), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, x_color, 2)
                cv2.putText(viz, f"Vertical: {y_status}", (10, 200),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, y_color, 2)
                
                # Instructions
                cv2.putText(viz, "Move eyes to EXTREME positions!", (10, 550),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
                cv2.putText(viz, "Press 'Q' to quit", (10, 580),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            else:
                cv2.putText(viz, "NO FACE DETECTED", (200, 300),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            
            cv2.imshow("Eye Movement Diagnostic", viz)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        self.face_mesh.close()
        
        # Final report
        print("\n" + "="*80)
        print("DIAGNOSTIC RESULTS")
        print("="*80)
        print(f"\nX Range: {self.eye_x_min:.4f} to {self.eye_x_max:.4f}")
        print(f"  Span: {self.eye_x_max - self.eye_x_min:.4f} ", end="")
        if self.eye_x_max - self.eye_x_min > 0.5:
            print("✅ EXCELLENT")
        elif self.eye_x_max - self.eye_x_min > 0.3:
            print("✓ GOOD")
        else:
            print("❌ POOR - Camera not detecting full horizontal movement")
        
        print(f"\nY Range: {self.eye_y_min:.4f} to {self.eye_y_max:.4f}")
        print(f"  Span: {self.eye_y_max - self.eye_y_min:.4f} ", end="")
        if self.eye_y_max - self.eye_y_min > 0.4:
            print("✅ EXCELLENT")
        elif self.eye_y_max - self.eye_y_min > 0.25:
            print("✓ GOOD")
        else:
            print("❌ POOR - Camera not detecting full vertical movement")
        
        print("\nRecommendations:")
        if self.eye_x_max - self.eye_x_min < 0.3 or self.eye_y_max - self.eye_y_min < 0.25:
            print("  ⚠️ Your eye movement range is limited!")
            print("  Possible causes:")
            print("    - Camera angle/position not optimal")
            print("    - Lighting issues")
            print("    - Not moving eyes to extreme positions")
            print("    - Glasses reflection")
            print("  ")
            print("  Solutions:")
            print("    - Adjust camera to be level with eyes")
            print("    - Improve front lighting")
            print("    - Really STRAIN eyes to look at extreme positions")
            print("    - Remove glasses or adjust to avoid reflections")
        else:
            print("  ✅ Eye movement detection looks good!")
            print("  The issue during calibration must be technique - really look at each point!")
        
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    diagnostic = EyeMovementDiagnostic()
    diagnostic.run()
