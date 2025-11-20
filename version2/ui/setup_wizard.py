"""
Pre-Calibration Setup Wizard
============================
Interactive overlay that guides user through optimal camera and head positioning.

Author: SHA Graduation Project Group 24
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Tuple, Optional


class SetupWizard:
    """Interactive setup wizard for optimal calibration positioning."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize setup wizard."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Face mesh indices
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.NOSE_TIP = 1
        self.FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
                          397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
                          172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
        
        # Optimal ranges (realistic for accessibility)
        self.OPTIMAL_DISTANCE_MIN = 40  # cm
        self.OPTIMAL_DISTANCE_MAX = 80  # cm
        self.OPTIMAL_FACE_WIDTH_MIN = 0.15  # of frame width
        self.OPTIMAL_FACE_WIDTH_MAX = 0.35  # of frame width
        self.OPTIMAL_CENTER_TOLERANCE = 0.20  # 20% tolerance
        self.OPTIMAL_TILT_MAX = 15  # degrees
        
    def estimate_distance(self, face_width_px: float, frame_width: int) -> float:
        """Estimate distance from camera based on face width."""
        face_width_ratio = face_width_px / frame_width
        
        # Empirical formula: distance (cm) = K / ratio
        # K calibrated for typical webcam with 6.3cm IPD
        K = 8.0
        estimated_distance = K / (face_width_ratio + 0.001)
        
        return float(np.clip(estimated_distance, 5, 200))
        
    def calculate_head_tilt(self, left_eye: np.ndarray, right_eye: np.ndarray) -> float:
        """Calculate head tilt angle in degrees."""
        dy = right_eye[1] - left_eye[1]
        dx = right_eye[0] - left_eye[0]
        angle = np.degrees(np.arctan2(dy, dx))
        
        if angle > 90:
            angle = angle - 180
        elif angle < -90:
            angle = angle + 180
        return angle
        
    def check_positioning(self, landmarks: np.ndarray, frame_width: int, 
                         frame_height: int) -> dict:
        """Analyze face position and provide feedback."""
        # Get key points
        left_eye = np.mean(landmarks[self.LEFT_EYE], axis=0)
        right_eye = np.mean(landmarks[self.RIGHT_EYE], axis=0)
        nose = landmarks[self.NOSE_TIP]
        
        # Calculate face metrics
        face_width_px = np.linalg.norm(right_eye - left_eye)
        face_center_x = (left_eye[0] + right_eye[0]) / 2
        face_center_y = (left_eye[1] + right_eye[1]) / 2
        
        # Check 1: Distance
        distance = self.estimate_distance(face_width_px, frame_width)
        distance_ok = self.OPTIMAL_DISTANCE_MIN <= distance <= self.OPTIMAL_DISTANCE_MAX
        
        # Check 2: Centered
        center_x_ratio = abs(face_center_x - frame_width/2) / frame_width
        center_y_ratio = abs(face_center_y - frame_height/2) / frame_height
        centered = (center_x_ratio < self.OPTIMAL_CENTER_TOLERANCE and 
                   center_y_ratio < self.OPTIMAL_CENTER_TOLERANCE)
        
        # Check 3: Head tilt
        tilt = self.calculate_head_tilt(left_eye, right_eye)
        tilt_ok = abs(tilt) < self.OPTIMAL_TILT_MAX
        
        # Check 4: Face size
        face_width_ratio = face_width_px / frame_width
        size_ok = self.OPTIMAL_FACE_WIDTH_MIN <= face_width_ratio <= self.OPTIMAL_FACE_WIDTH_MAX
        
        # All checks
        ready = distance_ok and centered and tilt_ok and size_ok
        
        return {
            'distance': distance,
            'distance_ok': distance_ok,
            'centered': centered,
            'center_x': face_center_x,
            'center_y': face_center_y,
            'tilt': tilt,
            'tilt_ok': tilt_ok,
            'size_ok': size_ok,
            'face_width_ratio': face_width_ratio,
            'ready': ready,
            'left_eye': left_eye,
            'right_eye': right_eye,
            'nose': nose
        }
        
    def _draw_camera_overlay(self, canvas, status, landmarks, cam_w, cam_h,
                            offset_x, offset_y, display_w, display_h, scale):
        """Draw positioning guides on camera feed area."""
        center_x = offset_x + display_w // 2
        center_y = offset_y + display_h // 2
        
        # Center crosshair
        cv2.line(canvas, (center_x - 40, center_y), (center_x + 40, center_y),
                (0, 255, 255), 3)
        cv2.line(canvas, (center_x, center_y - 40), (center_x, center_y + 40),
                (0, 255, 255), 3)
        cv2.circle(canvas, (center_x, center_y), 60, (0, 255, 255), 3)
        
        # Optimal zone
        zone_w = int(display_w * 0.4)
        zone_h = int(display_h * 0.4)
        zone_x1 = center_x - zone_w // 2
        zone_y1 = center_y - zone_h // 2
        zone_x2 = center_x + zone_w // 2
        zone_y2 = center_y + zone_h // 2
        
        zone_color = (0, 255, 0) if status['ready'] else (128, 128, 128)
        cv2.rectangle(canvas, (zone_x1, zone_y1), (zone_x2, zone_y2), zone_color, 3)
        
        # Face position indicator
        if 'center_x' in status:
            face_x_cam = status['center_x']
            face_y_cam = status['center_y']
            
            face_x = int(offset_x + (face_x_cam / cam_w) * display_w)
            face_y = int(offset_y + (face_y_cam / cam_h) * display_h)
            
            color = (0, 255, 0) if status['centered'] else (0, 165, 255)
            cv2.circle(canvas, (face_x, face_y), 15, color, -1)
            cv2.circle(canvas, (face_x, face_y), 18, (255, 255, 255), 2)
            
            if not status['centered']:
                cv2.arrowedLine(canvas, (face_x, face_y), (center_x, center_y),
                              (0, 200, 255), 3, tipLength=0.2)
        
        cv2.rectangle(canvas, (offset_x, offset_y), 
                     (offset_x + display_w, offset_y + display_h),
                     (80, 80, 80), 2)
    
    def _draw_status_panel(self, canvas, status, cam_w, cam_h):
        """Draw status panel with checks."""
        # Title
        cv2.rectangle(canvas, (0, 0), (self.screen_width, 140), (40, 40, 40), -1)
        cv2.putText(canvas, "Pre-Calibration Setup Wizard", (30, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        
        # Status checks
        y_start = 200
        x_pos = 30
        line_height = 60
        
        # Distance
        dist_color = (0, 255, 0) if status['distance_ok'] else (0, 0, 255)
        dist_icon = "✓" if status['distance_ok'] else "✗"
        dist_text = f"{dist_icon} Distance: {status['distance']:.0f}cm"
        if not status['distance_ok']:
            dist_text += " [Target: 40-80cm]"
        cv2.putText(canvas, dist_text, (x_pos, y_start),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, dist_color, 2)
        
        # Centered
        y_start += line_height
        center_color = (0, 255, 0) if status['centered'] else (0, 165, 255)
        center_icon = "✓" if status['centered'] else "✗"
        center_text = f"{center_icon} Position: " + ("Centered" if status['centered'] else "Align to center")
        cv2.putText(canvas, center_text, (x_pos, y_start),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, center_color, 2)
        
        # Tilt
        y_start += line_height
        tilt_color = (0, 255, 0) if status['tilt_ok'] else (255, 165, 0)
        tilt_icon = "✓" if status['tilt_ok'] else "✗"
        tilt_text = f"{tilt_icon} Head Tilt: {abs(status['tilt']):.1f}°"
        if not status['tilt_ok']:
            tilt_text += " [Straighten]"
        cv2.putText(canvas, tilt_text, (x_pos, y_start),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, tilt_color, 2)
        
        # Size
        y_start += line_height
        size_color = (0, 255, 0) if status['size_ok'] else (0, 0, 255)
        size_icon = "✓" if status['size_ok'] else "✗"
        if not status['size_ok']:
            if status['face_width_ratio'] < self.OPTIMAL_FACE_WIDTH_MIN:
                size_text = f"{size_icon} Distance: Move CLOSER"
            else:
                size_text = f"{size_icon} Distance: Move BACK"
        else:
            size_text = f"{size_icon} Distance: Optimal"
        cv2.putText(canvas, size_text, (x_pos, y_start),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, size_color, 2)
        
        # Overall status
        bottom_y = self.screen_height - 60
        if status['ready']:
            cv2.rectangle(canvas, (0, self.screen_height - 120), 
                         (self.screen_width, self.screen_height), (0, 100, 0), -1)
            cv2.putText(canvas, "✓ ALL CHECKS PASSED - Press SPACE to calibrate",
                       (self.screen_width // 2 - 550, bottom_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        else:
            cv2.rectangle(canvas, (0, self.screen_height - 120), 
                         (self.screen_width, self.screen_height), (60, 60, 60), -1)
            cv2.putText(canvas, "Adjust positioning | Press ESC to skip",
                       (self.screen_width // 2 - 400, bottom_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 200), 2)
        
    def run(self, cap: cv2.VideoCapture) -> bool:
        """Run setup wizard."""
        print("\n" + "="*60)
        print("PRE-CALIBRATION SETUP WIZARD")
        print("="*60)
        print("Position yourself for optimal calibration:")
        print("  ✓ Distance: 40-80 cm from camera")
        print("  ✓ Position: Face centered in frame")
        print("  ✓ Head: Straight, minimal tilt")
        print("\nPress SPACE when ready, ESC to skip")
        print("="*60 + "\n")
        
        cv2.namedWindow("Setup Wizard", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Setup Wizard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading camera!")
                return False
                
            frame = cv2.flip(frame, 1)
            cam_h, cam_w = frame.shape[:2]
            
            canvas = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)
            
            # Scale camera feed
            max_display_w = int(self.screen_width * 0.6)
            max_display_h = int(self.screen_height * 0.6)
            
            scale_w = max_display_w / cam_w
            scale_h = max_display_h / cam_h
            scale = min(scale_w, scale_h)
            
            display_w = int(cam_w * scale)
            display_h = int(cam_h * scale)
            
            offset_x = (self.screen_width - display_w) // 2
            offset_y = (self.screen_height - display_h) // 2
            
            frame_resized = cv2.resize(frame, (display_w, display_h))
            canvas[offset_y:offset_y+display_h, offset_x:offset_x+display_w] = frame_resized
            
            # Process face
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                landmarks = np.array([
                    (lm.x * cam_w, lm.y * cam_h)
                    for lm in results.multi_face_landmarks[0].landmark
                ])
                
                status = self.check_positioning(landmarks, cam_w, cam_h)
                
                self._draw_camera_overlay(canvas, status, landmarks, cam_w, cam_h, 
                                         offset_x, offset_y, display_w, display_h, scale)
                self._draw_status_panel(canvas, status, cam_w, cam_h)
                
            else:
                text_x = offset_x + display_w // 2 - 200
                text_y = offset_y + display_h // 2
                cv2.putText(canvas, "NO FACE DETECTED", (text_x, text_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                cv2.putText(canvas, "Position yourself in camera view", 
                           (text_x - 80, text_y + 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            cv2.imshow("Setup Wizard", canvas)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                print("Setup wizard skipped")
                cv2.destroyWindow("Setup Wizard")
                return False
            elif key == 32:  # SPACE
                if results.multi_face_landmarks and status['ready']:
                    print("\n✓ Setup complete! Starting calibration...")
                    cv2.destroyWindow("Setup Wizard")
                    return True
                else:
                    print("⚠ Complete all checks first")
        
        return False
