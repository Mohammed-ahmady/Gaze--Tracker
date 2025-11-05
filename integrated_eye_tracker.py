"""
Integration Module: Eye Tracking with Advanced Calibration
===========================================================

This module integrates the advanced calibration system with MediaPipe eye tracking.
Provides a complete, production-ready eye-controlled mouse implementation.

Author: SHA Graduation Project Group 24
Supervisor: Dr. Mohammed Hussien
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from typing import Tuple
import time
import sys
import os

from calibration_system import AdvancedCalibrationSystem
from control_window import ControlWindow
try:
    from overlay import CalibrationOverlay
except ImportError:
    CalibrationOverlay = None

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False


class CalibratedEyeTracker:
    """
    Eye tracking system with integrated advanced calibration.
    """
    
    def __init__(self):
        """Initialize the calibrated eye tracking system."""
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Initialize calibration system
        self.calibration = AdvancedCalibrationSystem(
            screen_width=self.screen_width,
            screen_height=self.screen_height
        )
        
        # Initialize video capture with DirectShow backend on Windows
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            # Fallback to default backend
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise RuntimeError("Failed to open camera. Please check camera connection and permissions.")
        
        # Set camera properties for optimal eye tracking
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Verify camera properties
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        print(f"Camera initialized: {self.frame_width}x{self.frame_height} @ {actual_fps}fps")
        
        # Read one test frame
        ret, frame = self.cap.read()
        if not ret or frame is None:
            raise RuntimeError("Camera opened but failed to read frame. Try restarting your computer.")
        
        # Cursor control state
        self.cursor_control_enabled = True
        # Smoothing toggle
        self.smoothing_enabled = True
        
        # MediaPipe face mesh indices
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]
        self.NOSE_TIP = 1  # Used for head motion tracking
    
    def get_iris_center(self, landmarks: np.ndarray, iris_indices: list) -> Tuple[float, float]:
        """Compute the iris center in pixel coordinates by averaging iris landmarks."""
        iris_pts = landmarks[iris_indices]
        center_x = np.mean([p[0] for p in iris_pts])
        center_y = np.mean([p[1] for p in iris_pts])
        return float(center_x), float(center_y)

    def get_eye_relative_pos(self, landmarks: np.ndarray, eye_indices: list, iris_indices: list) -> Tuple[float, float]:
        """
        Calculate the relative position of the iris within the eye using ratio approach.
        Returns (horizontal_ratio, vertical_ratio) where:
        - horizontal_ratio: 0.0 = extreme left, 0.5 = center, 1.0 = extreme right
        - vertical_ratio: 0.0 = extreme top, 0.5 = center, 1.0 = extreme bottom
        """
        iris_points = landmarks[iris_indices]
        eye_points = landmarks[eye_indices]

        # Calculate iris center (simple average)
        iris_center_x = np.mean([p[0] for p in iris_points])
        iris_center_y = np.mean([p[1] for p in iris_points])

        # Get eye boundaries
        eye_left = eye_points[0]
        eye_right = eye_points[3]
        
        # Get top and bottom of eye
        eye_top = np.mean([eye_points[1], eye_points[2]], axis=0)
        eye_bottom = np.mean([eye_points[4], eye_points[5]], axis=0)

        # Calculate eye dimensions
        eye_width = np.linalg.norm(eye_right - eye_left)
        eye_height = np.linalg.norm(eye_bottom - eye_top)

        # Calculate horizontal ratio (0.0 = extreme left, 1.0 = extreme right)
        horizontal_ratio = (iris_center_x - eye_left[0]) / (eye_width + 1e-6)
        
        # Calculate vertical ratio (0.0 = extreme top, 1.0 = extreme bottom)
        vertical_ratio = (iris_center_y - eye_top[1]) / (eye_height + 1e-6)

        # Clamp values to valid range
        horizontal_ratio = float(np.clip(horizontal_ratio, 0.0, 1.0))
        vertical_ratio = float(np.clip(vertical_ratio, 0.0, 1.0))

        return horizontal_ratio, vertical_ratio

    def get_nose_tip(self, landmarks: np.ndarray) -> Tuple[float, float]:
        """Get normalized nose tip coordinates (relative to frame width/height)."""
        nose = landmarks[self.NOSE_TIP]
        return float(nose[0] / self.frame_width), float(nose[1] / self.frame_height)

    def run_calibration(self, num_points: int = 9):
        """
        Run the calibration process.
        
        Args:
            num_points: Number of calibration points (9 or 25)
        """
        print(f"\nStarting {num_points}-point calibration...")
        print("Please follow the RED dots with your eyes.")
        print("Keep your head still while looking at each point.")
        
        # Start calibration system
        self.calibration.start_calibration(num_points)
        
        # Try to use overlay, fall back to OpenCV window
        overlay = None
        if CalibrationOverlay is not None:
            try:
                overlay = CalibrationOverlay()
            except Exception as e:
                print(f"Failed to create overlay ({e}), falling back to OpenCV window")
        
        # For tracking face detection
        face_detected_count = 0
        no_face_warning_shown = False
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error reading from camera!")
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                face_detected_count += 1
                no_face_warning_shown = False
                
                # Extract landmarks
                landmarks = np.array([
                    (lm.x * self.frame_width, lm.y * self.frame_height)
                    for lm in results.multi_face_landmarks[0].landmark
                ])
                
                # Get eye-relative iris and nose positions
                left_iris = self.get_eye_relative_pos(landmarks, self.LEFT_EYE, self.LEFT_IRIS)
                right_iris = self.get_eye_relative_pos(landmarks, self.RIGHT_EYE, self.RIGHT_IRIS)
                nose_tip = self.get_nose_tip(landmarks)
                
                # Collect calibration data
                is_complete = self.calibration.collect_calibration_frame(
                    left_iris, right_iris, nose_tip
                )
                
                if is_complete:
                    print("✓ Calibration data collection complete!")
                    break
            else:
                # No face detected
                if not no_face_warning_shown and face_detected_count == 0:
                    print("⚠ WARNING: No face detected! Please position your face in front of the camera.")
                    no_face_warning_shown = True
            
            # Render calibration UI
            if overlay is not None:
                try:
                    overlay.render(
                        self.calibration.calibration_grid,
                        self.calibration.current_point_idx,
                        self.calibration.current_frame_count,
                        self.calibration.frames_per_point,
                    )
                except Exception as e:
                    print(f"Overlay render failed ({e}). Switching to OpenCV window.")
                    if overlay is not None:
                        overlay.close()
                        overlay = None
                        cv2.namedWindow("Calibration", cv2.WINDOW_NORMAL)
                        cv2.setWindowProperty("Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            
            # If no overlay, draw using OpenCV window
            if overlay is None:
                canvas = self.calibration.draw_calibration_interface(frame)
                cv2.imshow("Calibration", canvas)
            
            # Check for cancel
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                print("\nCalibration cancelled!")
                if overlay is not None:
                    overlay.close()
                return
        
        # Cleanup
        if overlay is not None:
            overlay.close()
        else:
            cv2.destroyWindow("Calibration")
    
    def run(self):
        """Main eye tracking loop."""
        # Initialize control window with live preview
        control = ControlWindow("Eye Tracking Control")
        
        print("\nStarting eye tracking...")
        print("Window opened with live preview and controls.")
        
        # Load or start initial calibration (no blocking console input)
        if not self.calibration.load_calibration_data():
            print("\n" + "="*60)
            print("No saved calibration found.")
            print("Starting calibration now...")
            print("="*60)
            self.run_calibration(num_points=9)
        else:
            print("\n✓ Loaded saved calibration.")
            print("Press C (9-point) or F (25-point) in the preview window to recalibrate.")
            print("Press D to delete calibration and start fresh.")
        
        if not self.calibration.is_calibrated:
            print("\n" + "="*60)
            print("ERROR: Calibration required but not completed.")
            print("="*60)
            print("\nPossible reasons:")
            print("  1. Camera not working or blocked")
            print("  2. Face not detected (poor lighting or positioning)")
            print("  3. Calibration was cancelled")
            print("\nPlease fix the issue and try again.")
            print("="*60)
            return

        # FPS calculation
        fps_counter = 0
        fps_start_time = time.time()
        current_fps = 0
        
        # Diagnostic state
        last_face_detected = False
        last_prediction = None
        last_log_time = time.time()
        
        print("\nEye tracking active. Use the control window to operate.")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error reading from camera!")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            # Process face landmarks if detected
            if results.multi_face_landmarks:
                last_face_detected = True
                
                # Extract landmarks
                landmarks = np.array([
                    (lm.x * self.frame_width, lm.y * self.frame_height)
                    for lm in results.multi_face_landmarks[0].landmark
                ])
                
                # Get eye positions
                left_iris = self.get_eye_relative_pos(landmarks, self.LEFT_EYE, self.LEFT_IRIS)
                right_iris = self.get_eye_relative_pos(landmarks, self.RIGHT_EYE, self.RIGHT_IRIS)
                nose_tip = self.get_nose_tip(landmarks)
                
                # Predict screen position
                if self.calibration.is_calibrated and self.cursor_control_enabled:
                    screen_x, screen_y = self.calibration.predict_screen_position(
                        left_iris, right_iris, nose_tip, use_smoothing=self.smoothing_enabled
                    )
                    last_prediction = (screen_x, screen_y)
                    
                    try:
                        pyautogui.moveTo(screen_x, screen_y)
                    except Exception as e:
                        print(f"Cursor move error: {e}")
                
                # Draw iris positions on frame for debugging
                for idx in self.LEFT_IRIS + self.RIGHT_IRIS:
                    point = landmarks[idx]
                    cv2.circle(frame, (int(point[0]), int(point[1])), 2, (255, 0, 0), -1)
            else:
                # No face detected this frame
                last_face_detected = False
            
            # Calculate FPS
            fps_counter += 1
            if time.time() - fps_start_time > 1.0:
                current_fps = fps_counter
                fps_counter = 0
                fps_start_time = time.time()
            
            # Update control window with status
            status_text = f"{'ACTIVE' if self.cursor_control_enabled else 'PAUSED'} | "
            status_text += f"{'Face OK' if last_face_detected else 'No Face!'} | "
            status_text += f"FPS: {current_fps} | Gain: {self.calibration.output_gain:.2f} | Smooth: {'on' if self.smoothing_enabled else 'off'}"
            if last_prediction:
                status_text += f" | Look: ({last_prediction[0]}, {last_prediction[1]})"
            
            control.update_preview(frame, status_text)
            
            # Periodic console log for diagnostics
            if time.time() - last_log_time > 1.0:
                status = "face=yes" if last_face_detected else "face=no"
                pred = f"pred={last_prediction}" if last_prediction else "pred=None"
                print(f"[diag] {status}, fps={current_fps}, control={'on' if self.cursor_control_enabled else 'off'}, {pred}, calibrated={self.calibration.is_calibrated}")
                last_log_time = time.time()
            
            # Handle keyboard input from control window
            key = control.get_key(1)
            if key is None:
                continue
                
            if key == 'c':
                # Recalibrate with 9 points
                print("\nStarting recalibration...")
                self.run_calibration(num_points=9)
                
            elif key == 'f':
                # Fine calibration with 25 points
                print("\nStarting fine calibration (25 points)...")
                self.run_calibration(num_points=25)
                
            elif key == 'r':
                # Add incremental calibration point
                if results.multi_face_landmarks:
                    current_cursor_x, current_cursor_y = pyautogui.position()
                    print(f"\nAdding calibration point at cursor position: ({current_cursor_x}, {current_cursor_y})")
                    self.calibration.add_incremental_calibration_point(
                        left_iris, right_iris, nose_tip,
                        current_cursor_x, current_cursor_y
                    )
                
            elif key == 's':
                # Toggle cursor control
                self.cursor_control_enabled = not self.cursor_control_enabled
                status = "ENABLED" if self.cursor_control_enabled else "DISABLED"
                print(f"\nCursor control {status}")
                
            elif key == 'd':
                # Delete saved calibration files and force recalibration
                try:
                    if os.path.exists(self.calibration.calibration_file):
                        os.remove(self.calibration.calibration_file)
                        print(f"Deleted {self.calibration.calibration_file}")
                    if os.path.exists(self.calibration.model_file):
                        os.remove(self.calibration.model_file)
                        print(f"Deleted {self.calibration.model_file}")
                except Exception as e:
                    print(f"Error deleting calibration files: {e}")
                
                # Reset state and recalibrate
                self.calibration.is_calibrated = False
                print("\nStarting fresh calibration...")
                self.run_calibration(num_points=9)
            
            elif key == 'z':
                # Reset smoothing filters
                self.calibration.reset_smoothing_filters()
                print("\nSmoothing filters reset")

            elif key in ('+', '='):
                # Increase gain
                self.calibration.adjust_output_gain(0.1)
                print(f"\nOutput gain increased to {self.calibration.output_gain:.2f}")

            elif key in ('-', '_'):
                # Decrease gain
                self.calibration.adjust_output_gain(-0.1)
                print(f"\nOutput gain decreased to {self.calibration.output_gain:.2f}")

            elif key == 'x':
                # Toggle smoothing
                self.smoothing_enabled = not self.smoothing_enabled
                print(f"\nSmoothing {'ENABLED' if self.smoothing_enabled else 'DISABLED'}")
                
            elif key == 'q':
                # Save and quit
                print("\nSaving calibration...")
                self.calibration.save_calibration_data()
                control.close()
                print("Exiting...")
                break
            
            elif key == '\x1b':  # ESC
                # Quit without saving
                print("\nExiting without saving...")
                control.close()
                break
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        self.face_mesh.close()
        print("\n✓ Eye tracking system closed")


def test_camera():
    """Test if camera is accessible."""
    print("\nTesting camera access...")
    
    # Try DirectShow first (Windows)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened():
        ret, frame = cap.read()
        cap.release()
        if ret and frame is not None:
            print("✓ Camera is accessible and working!")
            return True
        else:
            print("✗ Camera opens but cannot read frames")
            return False
    
    # Try default backend
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        cap.release()
        if ret and frame is not None:
            print("✓ Camera is accessible (default backend)")
            return True
    
    print("✗ Camera is not accessible!")
    print("\nTroubleshooting steps:")
    print("  1. Check if camera is connected (webcam or laptop camera)")
    print("  2. Close any apps using the camera (Teams, Zoom, Skype, etc.)")
    print("  3. Check Windows Privacy Settings:")
    print("     Settings > Privacy > Camera > Allow apps to access camera")
    print("  4. Try restarting your computer")
    return False


def main():
    """Main entry point."""
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "Advanced Eye-Controlled Mouse System" + " "*11 + "║")
    print("║" + " "*8 + "SHA Graduation Project Group 24 (2025/2026)" + " "*7 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # Optional CLI: --reset-calibration to delete saved calibration on startup
        if any(arg in ("--reset-calibration", "-R") for arg in sys.argv[1:]):
            for path in ("calibration_data.json", "calibration_model.pkl"):
                try:
                    if os.path.exists(path):
                        os.remove(path)
                        print(f"Deleted {path}")
                except Exception as e:
                    print(f"Failed to delete {path}: {e}")

        # Test camera first
        if not test_camera():
            print("\n" + "="*60)
            print("CAMERA TEST FAILED")
            print("="*60)
            print("Please fix camera issues before running the eye tracker.")
            return
        
        print("\nInitializing eye tracker...")
        tracker = CalibratedEyeTracker()
        tracker.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except RuntimeError as e:
        print(f"\n{e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()