"""
Enhanced Eye Tracker with 15-Point Calibration
==============================================
Production-ready eye tracking system with advanced control panel.

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
import threading

from core.calibration_15point import Calibration15Point
from ui.control_panel import AdvancedControlPanel
from ui.overlay_window import CalibrationOverlay
from ui.setup_wizard import SetupWizard
from ui.raw_gaze_overlay import RawGazeOverlay
from core.eye_tracking_logger import EyeTrackingLogger

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False


class EnhancedEyeTracker:
    """Eye tracking system with 15-point calibration and advanced control panel."""
    
    def __init__(self):
        """Initialize the enhanced eye tracking system."""
        # Initialize logger (with fallback if it fails)
        try:
            self.logger = EyeTrackingLogger()
        except Exception as e:
            print(f"Warning: Logger failed to initialize: {e}")
            self.logger = None
        
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
        
        # Initialize 15-point calibration system
        self.calibration = Calibration15Point(
            screen_width=self.screen_width,
            screen_height=self.screen_height
        )
        
        # Initialize video capture
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise RuntimeError("Failed to open camera")
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Camera initialized: {self.frame_width}x{self.frame_height}")
        
        # Log system information
        if self.logger:
            try:
                self.logger.log_system_info(
                    self.screen_width, self.screen_height,
                    {
                        'width': self.frame_width,
                        'height': self.frame_height,
                        'fps': self.cap.get(cv2.CAP_PROP_FPS)
                    }
                )
            except Exception as e:
                print(f"Logging error: {e}")
        
        # Read test frame
        ret, frame = self.cap.read()
        if not ret or frame is None:
            raise RuntimeError("Camera opened but failed to read frame")
        
        # Cursor control state
        self.cursor_control_enabled = True
        self.smoothing_enabled = True
        
        # Raw gaze overlay
        self.show_raw_gaze = False
        self.raw_gaze_overlay = RawGazeOverlay(self.screen_width, self.screen_height)
        self.raw_gaze_window = None
        
        # Blink detection
        self.blink_threshold = 0.15  # Lower = require more closed eye
        self.last_left_blink_time = 0
        self.blink_cooldown = 0.5
        
        # MediaPipe face mesh indices
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]
        self.NOSE_TIP = 1
        
        # Control panel (will be initialized in run)
        self.control_panel = None
        self.panel_thread = None
        
    def get_eye_relative_pos(self, landmarks: np.ndarray, eye_indices: list, 
                             iris_indices: list) -> Tuple[float, float]:
        """Calculate relative iris position within eye."""
        iris_points = landmarks[iris_indices]
        eye_points = landmarks[eye_indices]

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

        horizontal_ratio = float(np.clip(horizontal_ratio, 0.0, 1.0))
        vertical_ratio = float(np.clip(vertical_ratio, 0.0, 1.0))

        return horizontal_ratio, vertical_ratio
    
    def calculate_eye_aspect_ratio(self, landmarks: np.ndarray, eye_indices: list) -> float:
        """Calculate eye aspect ratio for blink detection."""
        points = landmarks[eye_indices]
        
        # Vertical distances
        v1 = np.linalg.norm(points[1] - points[5])
        v2 = np.linalg.norm(points[2] - points[4])
        
        # Horizontal distance
        h = np.linalg.norm(points[0] - points[3])
        
        # Calculate EAR
        ear = (v1 + v2) / (2.0 * h + 1e-6)
        return ear

    def get_nose_tip(self, landmarks: np.ndarray) -> Tuple[float, float]:
        """Get normalized nose tip coordinates."""
        nose = landmarks[self.NOSE_TIP]
        return float(nose[0] / self.frame_width), float(nose[1] / self.frame_height)

    def run_calibration(self, num_points: int = 21):
        """Run calibration process with overlay."""
        print(f"\nStarting {num_points}-point calibration (with full screen coverage)...")
        
        # Log calibration start
        if self.logger:
            try:
                self.logger.log_calibration_start(num_points, 60)
            except:
                pass
        
        # Start calibration system
        self.calibration.start_calibration(num_points)
        
        # Create overlay
        overlay = CalibrationOverlay()
        
        # Update control panel
        if self.control_panel:
            self.control_panel.update_status(mode='Calibration', calibrated=False)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error reading from camera!")
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                landmarks = np.array([
                    (lm.x * self.frame_width, lm.y * self.frame_height)
                    for lm in results.multi_face_landmarks[0].landmark
                ])
                
                left_iris = self.get_eye_relative_pos(landmarks, self.LEFT_EYE, self.LEFT_IRIS)
                right_iris = self.get_eye_relative_pos(landmarks, self.RIGHT_EYE, self.RIGHT_IRIS)
                nose_tip = self.get_nose_tip(landmarks)
                
                # Log calibration point if new point
                if self.logger and self.calibration.current_frame_count == 0 and self.calibration.current_point_idx < len(self.calibration.calibration_grid):
                    try:
                        px, py = self.calibration.calibration_grid[self.calibration.current_point_idx]
                        self.logger.log_calibration_point(self.calibration.current_point_idx, px, py)
                    except:
                        pass
                
                # Collect calibration frame
                is_complete = self.calibration.collect_calibration_frame(
                    left_iris, right_iris, nose_tip
                )
                
                # Log calibration sample
                if self.logger and self.calibration.current_point_idx < len(self.calibration.calibration_grid):
                    try:
                        px, py = self.calibration.calibration_grid[self.calibration.current_point_idx]
                        self.logger.log_calibration_sample(
                            self.calibration.current_point_idx,
                            left_iris, right_iris, nose_tip,
                            px, py
                        )
                    except:
                        pass
                
                if is_complete:
                    print("✓ Calibration complete!")
                    # Log calibration completion with actual training errors
                    if self.logger:
                        try:
                            self.logger.log_calibration_complete(
                                total_points=len(self.calibration.calibration_grid),
                                training_error={
                                    'x': self.calibration.training_error_x,
                                    'y': self.calibration.training_error_y
                                }
                            )
                        except:
                            pass
                    break
            
            # Render calibration overlay
            try:
                overlay.render(
                    self.calibration.calibration_grid,
                    self.calibration.current_point_idx,
                    self.calibration.current_frame_count,
                    self.calibration.frames_per_point
                )
            except Exception as e:
                print(f"Overlay error: {e}")
            
            # Update control panel
            if self.control_panel:
                self.control_panel.update_frame(frame)
            
            # Check for cancel
            if cv2.waitKey(1) & 0xFF == 27:
                print("\nCalibration cancelled!")
                overlay.close()
                return
        
        overlay.close()
        
        # Update control panel
        if self.control_panel:
            self.control_panel.update_status(
                mode='Tracking', 
                calibrated=True,
                calibration_points=len(self.calibration.calibration_grid)
            )
    
    def start_control_panel(self):
        """Initialize control panel (will run in main thread)."""
        self.control_panel = AdvancedControlPanel("Eye Tracking Control Panel")
    
    def process_tracking_loop(self):
        """Process eye tracking in background thread."""
        # FPS tracking
        fps_counter = 0
        fps_start_time = time.time()
        current_fps = 0
        
        # Tracking state
        last_face_detected = False
        last_prediction = (0, 0)
        
        print("\nEye tracking active. Use control panel to operate.")
        
        while self.control_panel and self.control_panel.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error reading from camera!")
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                last_face_detected = True
                
                landmarks = np.array([
                    (lm.x * self.frame_width, lm.y * self.frame_height)
                    for lm in results.multi_face_landmarks[0].landmark
                ])
                
                left_iris = self.get_eye_relative_pos(landmarks, self.LEFT_EYE, self.LEFT_IRIS)
                right_iris = self.get_eye_relative_pos(landmarks, self.RIGHT_EYE, self.RIGHT_IRIS)
                nose_tip = self.get_nose_tip(landmarks)
                
                # Update raw gaze overlay
                if self.show_raw_gaze:
                    avg_x = (left_iris[0] + right_iris[0]) / 2
                    avg_y = (left_iris[1] + right_iris[1]) / 2
                    self.raw_gaze_overlay.update(avg_x, avg_y)
                
                # Blink detection for click (left eye only)
                # Disable when looking down to prevent false triggers
                avg_eye_y = (left_iris[1] + right_iris[1]) / 2
                looking_down = avg_eye_y > 0.6  # Looking at bottom 40% of screen
                
                left_ear = self.calculate_eye_aspect_ratio(landmarks, self.LEFT_EYE)
                right_ear = self.calculate_eye_aspect_ratio(landmarks, self.RIGHT_EYE)
                
                current_time = time.time()
                # Only trigger blink if NOT looking down
                if not looking_down and left_ear < self.blink_threshold and right_ear >= self.blink_threshold:
                    # Left eye closed, right eye open = click
                    if current_time - self.last_left_blink_time > self.blink_cooldown:
                        pyautogui.click()
                        self.last_left_blink_time = current_time
                        print("✓ Left-eye blink click")
                
                if self.calibration.is_calibrated and self.cursor_control_enabled:
                    screen_x, screen_y = self.calibration.predict_screen_position(
                        left_iris, right_iris, nose_tip, use_smoothing=self.smoothing_enabled
                    )
                    last_prediction = (screen_x, screen_y)
                    
                    # Log tracking frame (only every 10th frame to avoid performance issues)
                    if fps_counter % 10 == 0 and self.logger:
                        try:
                            avg_eye_x = (left_iris[0] + right_iris[0]) / 2
                            avg_eye_y = (left_iris[1] + right_iris[1]) / 2
                            self.logger.log_tracking_frame({
                                'left_eye_x': left_iris[0],
                                'left_eye_y': left_iris[1],
                                'right_eye_x': right_iris[0],
                                'right_eye_y': right_iris[1],
                                'avg_eye_x': avg_eye_x,
                                'avg_eye_y': avg_eye_y,
                                'nose_x': nose_tip[0],
                                'nose_y': nose_tip[1],
                                'predicted_x': screen_x,
                                'predicted_y': screen_y,
                                'smoothed_x': screen_x,
                                'smoothed_y': screen_y,
                                'cursor_x': screen_x,
                                'cursor_y': screen_y,
                                'face_detected': True,
                                'left_ear': left_ear,
                                'right_ear': right_ear,
                                'blink_detected': False,
                                'smoothing_enabled': self.smoothing_enabled,
                                'gain': self.calibration.output_gain,
                                'mode': 'tracking'
                            })
                        except Exception as e:
                            pass  # Don't let logging errors break tracking
                    
                    try:
                        pyautogui.moveTo(screen_x, screen_y)
                    except Exception as e:
                        print(f"Cursor error: {e}")

                
                # Draw iris tracking
                for idx in self.LEFT_IRIS + self.RIGHT_IRIS:
                    point = landmarks[idx]
                    cv2.circle(frame, (int(point[0]), int(point[1])), 2, (0, 255, 0), -1)
            else:
                last_face_detected = False
            
            # Calculate FPS
            fps_counter += 1
            if time.time() - fps_start_time > 1.0:
                current_fps = fps_counter
                fps_counter = 0
                fps_start_time = time.time()
            
            # Update control panel
            if self.control_panel:
                self.control_panel.update_frame(frame)
                self.control_panel.update_status(
                    fps=current_fps,
                    face_detected=last_face_detected,
                    calibrated=self.calibration.is_calibrated,
                    cursor_enabled=self.cursor_control_enabled,
                    smoothing_enabled=self.smoothing_enabled,
                    gain=self.calibration.output_gain,
                    cursor_pos=last_prediction,
                    mode='Tracking'
                )
                
                # Handle commands from control panel
                cmd = self.control_panel.get_command()
                if cmd:
                    self.handle_command(cmd, results)
            
            # Show raw gaze overlay
            if self.show_raw_gaze:
                self._update_raw_gaze_window()
            
            time.sleep(0.001)
        
        # Cleanup
        print("\nCleaning up and saving logs...")
        if self.logger:
            try:
                self.logger.analyze_and_save()
                self.logger.close()
            except Exception as e:
                print(f"Error saving logs: {e}")
        self.cap.release()
        cv2.destroyAllWindows()
        self.face_mesh.close()
        print("✓ Eye tracking system closed")
    
    def _update_raw_gaze_window(self):
        """Update raw gaze overlay window."""
        if self.raw_gaze_window is None:
            cv2.namedWindow("Raw Gaze Overlay", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("Raw Gaze Overlay", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty("Raw Gaze Overlay", cv2.WND_PROP_TOPMOST, 1)
            self.raw_gaze_window = True
        
        # Get BGR overlay directly
        overlay_bgr = self.raw_gaze_overlay.render()
        
        # Display
        cv2.imshow("Raw Gaze Overlay", overlay_bgr)
        cv2.setWindowProperty("Raw Gaze Overlay", cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)  # Process window events
    
    def run(self):
        """Main eye tracking loop - runs control panel in main thread."""
        # Initialize control panel (main thread)
        print("\nInitializing control panel...")
        self.start_control_panel()
        
        if not self.control_panel:
            print("ERROR: Failed to start control panel!")
            return
        
        # Load or start calibration
        if not self.calibration.load_calibration_data():
            print("\nNo saved calibration found.")
            
            # Run setup wizard
            wizard = SetupWizard(self.screen_width, self.screen_height)
            setup_complete = wizard.run(self.cap)
            
            if setup_complete:
                print("\nStarting 21-point calibration...")
                self.run_calibration(num_points=21)
            else:
                print("\nSkipped setup wizard. Starting calibration anyway...")
                self.run_calibration(num_points=21)
        else:
            print("\n✓ Loaded saved calibration")
            self.control_panel.update_status(calibrated=True)
        
        if not self.calibration.is_calibrated:
            print("\nERROR: Calibration required but not completed")
            return

        # Start tracking in background thread
        self.tracking_thread = threading.Thread(target=self.process_tracking_loop, daemon=True)
        self.tracking_thread.start()
        
        # Run control panel in main thread (required for Tkinter)
        print("\nStarting control panel GUI...")
        self.control_panel.run()
    
    def handle_command(self, cmd, results):
        """Handle commands from control panel."""
        if cmd == 'c':
            print("\nStarting 9-point calibration...")
            self.run_calibration(num_points=9)
            
        elif cmd == 'f':
            print("\nStarting 21-point calibration (full coverage)...")
            self.run_calibration(num_points=21)
            
        elif cmd == 'r':
            if results and results.multi_face_landmarks:
                landmarks = np.array([
                    (lm.x * self.frame_width, lm.y * self.frame_height)
                    for lm in results.multi_face_landmarks[0].landmark
                ])
                left_iris = self.get_eye_relative_pos(landmarks, self.LEFT_EYE, self.LEFT_IRIS)
                right_iris = self.get_eye_relative_pos(landmarks, self.RIGHT_EYE, self.RIGHT_IRIS)
                nose_tip = self.get_nose_tip(landmarks)
                
                cursor_x, cursor_y = pyautogui.position()
                print(f"\nAdding calibration point at ({cursor_x}, {cursor_y})")
                # Note: Would need to add incremental calibration method
                
        elif cmd == 's':
            self.cursor_control_enabled = not self.cursor_control_enabled
            status = "ENABLED" if self.cursor_control_enabled else "DISABLED"
            print(f"\nCursor control {status}")
            
        elif cmd == 'd':
            try:
                if os.path.exists(self.calibration.calibration_file):
                    os.remove(self.calibration.calibration_file)
                if os.path.exists(self.calibration.model_file):
                    os.remove(self.calibration.model_file)
            except Exception as e:
                print(f"Error deleting files: {e}")
            
            self.calibration.is_calibrated = False
            print("\nStarting fresh 21-point calibration...")
            self.run_calibration(num_points=21)
        
        elif cmd == 'z':
            self.calibration.reset_smoothing_filters()
            print("\nSmoothing filters reset")

        elif cmd == '+' or cmd == '=':
            self.calibration.adjust_output_gain(0.1)
            print(f"\nGain increased to {self.calibration.output_gain:.2f}")

        elif cmd == '-' or cmd == '_':
            self.calibration.adjust_output_gain(-0.1)
            print(f"\nGain decreased to {self.calibration.output_gain:.2f}")

        elif cmd == 'x':
            self.smoothing_enabled = not self.smoothing_enabled
            print(f"\nSmoothing {'ENABLED' if self.smoothing_enabled else 'DISABLED'}")
        
        elif cmd == 'g':
            self.show_raw_gaze = not self.show_raw_gaze
            if self.show_raw_gaze:
                print("\nRaw gaze overlay ENABLED")
            else:
                print("\nRaw gaze overlay DISABLED")
                if self.raw_gaze_window:
                    cv2.destroyWindow("Raw Gaze Overlay")
                    self.raw_gaze_window = None
                self.raw_gaze_overlay.reset()
            
        elif cmd == 'q':
            print("\nSaving calibration...")
            self.calibration.save_calibration_data()
            if self.logger:
                try:
                    print("Generating analysis report...")
                    self.logger.analyze_and_save()
                    self.logger.close()
                except Exception as e:
                    print(f"Error saving logs: {e}")
            if self.control_panel:
                self.control_panel.close()
            self.running = False


def main():
    """Main entry point."""
    print("╔" + "="*58 + "╗")
    print("║" + " "*8 + "Enhanced Eye Tracking System (21-Point)" + " "*9 + "║")
    print("║" + " "*8 + "SHA Graduation Project Group 24 (2025/2026)" + " "*7 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        tracker = EnhancedEyeTracker()
        tracker.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
