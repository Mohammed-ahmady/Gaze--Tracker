"""
Eye-Controlled Mouse using Computer Vision
A production-ready implementation of eye-tracking mouse control using Mediapipe, OpenCV, and PyAutoGUI.

Features:
- Precise eye movement tracking for mouse control
- Blink detection for mouse clicks
- Smooth cursor movement with moving average
- Auto-calibration with 15 points (5x3 grid)
- Screen size adaptation
- Debug visualization
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from collections import deque
import time
import pyttsx3
from typing import Tuple, List, Optional

# Disable PyAutoGUI's fail-safe
pyautogui.FAILSAFE = False


# Initialize text-to-speech engine
def init_tts_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0-1)
    return engine


class EyeControlledMouse:
    def __init__(self):
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Screen dimensions and scaling
        self.screen_width, self.screen_height = pyautogui.size()
        self.scaling_factor = 1.25
        self.display_width = 1920
        self.display_height = 1080
        self.monitor_width = self.display_width
        self.monitor_height = self.display_height

        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Window parameters
        self.window_name = 'Eye Tracking Debug'
        self.is_fullscreen = True
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

        # Get the screen resolution for fullscreen
        self.monitor_width = self.screen_width
        self.monitor_height = self.screen_height

        # Smoothing parameters
        self.smooth_window = 15
        self.x_coords = deque(maxlen=self.smooth_window)
        self.y_coords = deque(maxlen=self.smooth_window)
        self.last_valid_x = None
        self.last_valid_y = None
        self.smooth_factor = 0.3
        
        # Kalman Filter parameters for advanced smoothing
        self.use_kalman_filter = True
        self.kalman_initialized = False
        # State vector: [x, y, vx, vy] (position and velocity)
        self.kalman_state = np.zeros(4)
        # State covariance matrix
        self.kalman_P = np.eye(4) * 1000
        # Process noise covariance
        self.kalman_Q = np.eye(4) * 0.01
        # Measurement noise covariance
        self.kalman_R = np.eye(2) * 10
        # State transition matrix
        self.kalman_F = np.array([
            [1, 0, 1, 0],  # x = x + vx
            [0, 1, 0, 1],  # y = y + vy
            [0, 0, 1, 0],  # vx = vx
            [0, 0, 0, 1]   # vy = vy
        ])
        # Measurement matrix (we only measure position)
        self.kalman_H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])

        # Window state and blink detection
        self.window_state = "normal"
        self.blink_count = 0
        self.last_blink_time = 0
        self.BLINK_TIMEOUT = 1.0

        # Calibration parameters - Enhanced to 15 points (5x3 grid)
        self.calibration_points = [
            # Top row (5 points)
            ((0.1, 0.1), "top left"),
            ((0.325, 0.1), "top quarter left"),
            ((0.5, 0.1), "top center"),
            ((0.675, 0.1), "top quarter right"),
            ((0.9, 0.1), "top right"),
            
            # Middle row (5 points)
            ((0.1, 0.5), "middle left"),
            ((0.325, 0.5), "middle quarter left"),
            ((0.5, 0.5), "center"),
            ((0.675, 0.5), "middle quarter right"),
            ((0.9, 0.5), "middle right"),
            
            # Bottom row (5 points)
            ((0.1, 0.9), "bottom left"),
            ((0.325, 0.9), "bottom quarter left"),
            ((0.5, 0.9), "bottom center"),
            ((0.675, 0.9), "bottom quarter right"),
            ((0.9, 0.9), "bottom right")
        ]
        self.current_calibration_point = 0
        self.frames_per_point = 60
        self.calibration_data = {i: [] for i in range(len(self.calibration_points))}
        self.calibration_frame_count = 0
        self.calibrated = False
        self.calibration_mapping = None
        self.calibration_started = False
        self.tts_engine = init_tts_engine()
        self.last_speech_time = 0
        self.speech_interval = 3.0

        # Blink detection thresholds
        self.blink_threshold = 0.2
        self.both_eyes_closed_time = None
        self.MIN_BLINK_TIME = 0.15
        self.EXIT_BLINK_TIME = 1.0

        # MediaPipe landmark indices
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]

    def calculate_eye_aspect_ratio(self, landmarks: np.ndarray, eye_indices: List[int]) -> float:
        """Calculate the eye aspect ratio for blink detection."""
        points = landmarks[eye_indices]

        # Vertical distances
        v1 = np.linalg.norm(points[1] - points[5])
        v2 = np.linalg.norm(points[2] - points[4])

        # Horizontal distance
        h = np.linalg.norm(points[0] - points[3])

        # Calculate EAR
        ear = (v1 + v2) / (2.0 * h + 1e-6)
        return ear

    def get_iris_position(self, landmarks: np.ndarray, iris_indices: List[int],
                          eye_indices: List[int]) -> Tuple[float, float]:
        """Calculate the relative position of the iris within the eye using simplified ratio approach."""
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

        # Calculate the eye center (horizontal center, vertical center)
        eye_center_x = (eye_left[0] + eye_right[0]) / 2
        eye_center_y = (eye_top[1] + eye_bottom[1]) / 2

        # Calculate horizontal ratio INVERTED (1.0 = extreme right, 0.5 = center, 0.0 = extreme left)
        # This matches screen coordinates where 0 is left, width is right
        horizontal_ratio = (iris_center_x - eye_left[0]) / (eye_width + 1e-6)
        
        # Calculate vertical ratio (0.0 = extreme top, 0.5 = center, 1.0 = extreme bottom)
        vertical_ratio = (iris_center_y - eye_top[1]) / (eye_height + 1e-6)

        # Clamp values to valid range
        horizontal_ratio = np.clip(horizontal_ratio, 0.0, 1.0)
        vertical_ratio = np.clip(vertical_ratio, 0.0, 1.0)

        return horizontal_ratio, vertical_ratio

    def _apply_non_linear_transform(self, value: float) -> float:
        """Apply non-linear transformation to improve edge accuracy."""
        # Center the value around 0
        centered = value - 0.5
        # Apply cubic transformation for better edge response
        transformed = 4 * (centered ** 3) + centered
        # Scale back to 0-1 range
        return (transformed + 1) / 2

    def smooth_coordinates(self, x: float, y: float) -> Tuple[int, int]:
        """Apply advanced smoothing with Kalman Filter to coordinates."""
        if self.use_kalman_filter:
            return self.kalman_filter_update(x, y)
        else:
            # Original smoothing method
            if self.last_valid_x is None:
                self.last_valid_x = x
                self.last_valid_y = y
                self.x_coords.clear()
                self.y_coords.clear()

            # Handle large movements (outlier detection)
            max_delta = 300
            if abs(x - self.last_valid_x) > max_delta or abs(y - self.last_valid_y) > max_delta:
                x = int(self.last_valid_x * 0.7 + x * 0.3)
                y = int(self.last_valid_y * 0.7 + y * 0.3)

            # Apply moving average and exponential smoothing
            self.x_coords.append(x)
            self.y_coords.append(y)
            
            ma_x = np.mean(self.x_coords)
            ma_y = np.mean(self.y_coords)
            
            smoothed_x = int(ma_x * self.smooth_factor + (1 - self.smooth_factor) * self.last_valid_x)
            smoothed_y = int(ma_y * self.smooth_factor + (1 - self.smooth_factor) * self.last_valid_y)

            self.last_valid_x = smoothed_x
            self.last_valid_y = smoothed_y

            return smoothed_x, smoothed_y
    
    def kalman_filter_update(self, measured_x: float, measured_y: float) -> Tuple[int, int]:
        """
        Kalman Filter implementation for smooth and accurate eye tracking.
        
        The Kalman Filter works in two steps:
        1. Prediction: Estimate where the cursor should be based on previous velocity
        2. Update: Correct the prediction using the new measurement
        
        This reduces jitter while maintaining responsiveness.
        """
        # Initialize Kalman filter on first call
        if not self.kalman_initialized:
            self.kalman_state = np.array([measured_x, measured_y, 0, 0])
            self.kalman_initialized = True
            return int(measured_x), int(measured_y)
        
        # PREDICTION STEP
        # Predict next state: x_predicted = F * x_current
        predicted_state = self.kalman_F @ self.kalman_state
        
        # Predict error covariance: P_predicted = F * P * F^T + Q
        predicted_P = self.kalman_F @ self.kalman_P @ self.kalman_F.T + self.kalman_Q
        
        # UPDATE STEP
        # Measurement vector (what we actually observed)
        measurement = np.array([measured_x, measured_y])
        
        # Innovation (difference between measurement and prediction)
        innovation = measurement - (self.kalman_H @ predicted_state)
        
        # Innovation covariance: S = H * P * H^T + R
        S = self.kalman_H @ predicted_P @ self.kalman_H.T + self.kalman_R
        
        # Kalman Gain: K = P * H^T * S^-1
        # This determines how much we trust the measurement vs prediction
        kalman_gain = predicted_P @ self.kalman_H.T @ np.linalg.inv(S)
        
        # Update state estimate: x = x_predicted + K * innovation
        self.kalman_state = predicted_state + kalman_gain @ innovation
        
        # Update error covariance: P = (I - K * H) * P
        I = np.eye(4)
        self.kalman_P = (I - kalman_gain @ self.kalman_H) @ predicted_P
        
        # Extract filtered position
        filtered_x = int(self.kalman_state[0])
        filtered_y = int(self.kalman_state[1])
        
        # Clamp to reasonable values
        filtered_x = max(0, min(filtered_x, self.display_width))
        filtered_y = max(0, min(filtered_y, self.display_height))
        
        return filtered_x, filtered_y

    def start_calibration(self):
        """Initialize the calibration process with voice instruction."""
        if not self.calibration_started:
            self.calibration_started = True
            self.tts_engine.say("Starting eye tracking calibration with 15 points. Please follow the numbered red dots.")
            self.tts_engine.runAndWait()
            time.sleep(1)
            self.announce_current_point()

    def announce_current_point(self):
        """Announce the current calibration point with voice."""
        point_desc = self.calibration_points[self.current_calibration_point][1]
        point_num = self.current_calibration_point + 1
        self.tts_engine.say(f"Please look at the {point_desc} dot, number {point_num}")
        self.tts_engine.runAndWait()
        self.last_speech_time = time.time()

    def calibrate(self, landmarks: np.ndarray) -> None:
        """Collect calibration data for 15-point calibration."""
        if not self.calibrated:
            if not self.calibration_started:
                self.start_calibration()
                return

            current_point = self.calibration_points[self.current_calibration_point][0]
            target_x = int(current_point[0] * self.screen_width)
            target_y = int(current_point[1] * self.screen_height)

            # Repeat voice instruction periodically
            if time.time() - self.last_speech_time > self.speech_interval:
                self.announce_current_point()

            # Get current eye positions
            left_pos = self.get_iris_position(landmarks, self.LEFT_IRIS, self.LEFT_EYE)
            right_pos = self.get_iris_position(landmarks, self.RIGHT_IRIS, self.RIGHT_EYE)

            # Store the eye positions for current calibration point
            self.calibration_data[self.current_calibration_point].append((left_pos, right_pos))
            self.calibration_frame_count += 1

            if self.calibration_frame_count >= self.frames_per_point:
                # Calculate average eye position for current point
                point_data = self.calibration_data[self.current_calibration_point]
                avg_left_x = np.mean([d[0][0] for d in point_data])
                avg_left_y = np.mean([d[0][1] for d in point_data])
                avg_right_x = np.mean([d[1][0] for d in point_data])
                avg_right_y = np.mean([d[1][1] for d in point_data])

                # Store the mapping between eye position and screen coordinates
                if self.calibration_mapping is None:
                    self.calibration_mapping = []
                self.calibration_mapping.append({
                    'screen': current_point,
                    'eye': ((avg_left_x, avg_left_y), (avg_right_x, avg_right_y))
                })

                # Move to next calibration point
                self.current_calibration_point += 1
                self.calibration_frame_count = 0

                # Check if calibration is complete
                if self.current_calibration_point >= len(self.calibration_points):
                    self.calibrated = True
                    # Reset smoothing coordinates after calibration
                    self.last_valid_x = None
                    self.last_valid_y = None
                    self.x_coords.clear()
                    self.y_coords.clear()
                    self.tts_engine.say("Calibration complete. You can now control the mouse with your eyes.")
                    self.tts_engine.runAndWait()
                else:
                    # Announce next point
                    time.sleep(0.5)  # Brief pause between points
                    self.announce_current_point()

    def map_to_screen(self, rel_x: float, rel_y: float) -> Tuple[int, int]:
        """Map relative eye position to screen coordinates using direct ratio mapping with calibration."""
        if not self.calibrated or not self.calibration_mapping:
            # Before calibration, map directly to screen
            screen_x = int(rel_x * self.display_width)
            screen_y = int(rel_y * self.display_height)
            return screen_x, screen_y

        # Use calibration data to adjust the mapping
        # Get calibration values for different positions (using 15-point grid)
        center_point = self.calibration_mapping[7]['eye']  # center (point 8)
        center_x = (center_point[0][0] + center_point[1][0]) / 2
        center_y = (center_point[0][1] + center_point[1][1]) / 2

        left_point = self.calibration_mapping[5]['eye']  # middle left (point 6)
        right_point = self.calibration_mapping[9]['eye']  # middle right (point 10)
        top_point = self.calibration_mapping[2]['eye']    # top center (point 3)
        bottom_point = self.calibration_mapping[12]['eye'] # bottom center (point 13)

        left_x = (left_point[0][0] + left_point[1][0]) / 2
        right_x = (right_point[0][0] + right_point[1][0]) / 2
        top_y = (top_point[0][1] + top_point[1][1]) / 2
        bottom_y = (bottom_point[0][1] + bottom_point[1][1]) / 2

        # Calculate the range of eye movement
        eye_width_range = abs(right_x - left_x)
        eye_height_range = abs(bottom_y - top_y)

        # Normalize the current position relative to calibration
        if eye_width_range > 0:
            normalized_x = (rel_x - left_x) / eye_width_range
        else:
            normalized_x = 0.5

        if eye_height_range > 0:
            normalized_y = (rel_y - top_y) / eye_height_range
        else:
            normalized_y = 0.5

        # Clamp normalized values
        normalized_x = np.clip(normalized_x, 0.0, 1.0)
        normalized_y = np.clip(normalized_y, 0.0, 1.0)

        # Map to screen coordinates with sensitivity adjustment
        sensitivity_x = 1.2
        sensitivity_y = 1.2
        
        # Apply sensitivity around center
        adjusted_x = (normalized_x - 0.5) * sensitivity_x + 0.5
        adjusted_y = (normalized_y - 0.5) * sensitivity_y + 0.5
        
        # Clamp again after sensitivity adjustment
        adjusted_x = np.clip(adjusted_x, 0.0, 1.0)
        adjusted_y = np.clip(adjusted_y, 0.0, 1.0)

        # Convert to screen coordinates
        screen_x = int(adjusted_x * self.display_width)
        screen_y = int(adjusted_y * self.display_height)

        # Ensure coordinates are within screen bounds
        screen_x = max(0, min(screen_x, self.display_width - 1))
        screen_y = max(0, min(screen_y, self.display_height - 1))
        
        return screen_x, screen_y

    def process_frame(self, frame: np.ndarray) -> Tuple[Optional[np.ndarray], bool]:
        """Process a single frame and return the annotated frame and exit flag."""
        frame = cv2.flip(frame, 1)  # Mirror flip
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            return frame, False

        landmarks = np.array([(lm.x * self.frame_width, lm.y * self.frame_height)
                              for lm in results.multi_face_landmarks[0].landmark])

        # Handle calibration
        if not self.calibrated:
            self.calibrate(landmarks)
            cv2.putText(frame, "Calibrating... Keep eyes centered",
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return frame, False

        # Calculate eye aspect ratios
        left_ear = self.calculate_eye_aspect_ratio(landmarks, self.LEFT_EYE)
        right_ear = self.calculate_eye_aspect_ratio(landmarks, self.RIGHT_EYE)

        # Get iris positions
        left_iris_pos = self.get_iris_position(landmarks, self.LEFT_IRIS, self.LEFT_EYE)
        right_iris_pos = self.get_iris_position(landmarks, self.RIGHT_IRIS, self.RIGHT_EYE)

        # Handle blink detection and actions
        both_eyes_closed = (left_ear < self.blink_threshold and
                            right_ear < self.blink_threshold)

        if both_eyes_closed:
            if self.both_eyes_closed_time is None:
                self.both_eyes_closed_time = time.time()
                # Count blink for window toggle
                current_time = time.time()
                if current_time - self.last_blink_time < self.BLINK_TIMEOUT:
                    self.blink_count += 1
                else:
                    self.blink_count = 1
                self.last_blink_time = current_time

                # Handle window toggling
                if self.blink_count >= 3:
                    if self.window_state == "normal":
                        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                        self.window_state = "maximized"
                    else:
                        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                        cv2.resizeWindow(self.window_name, 800, 600)
                        # Center the window on screen
                        x = (self.screen_width - 800) // 2
                        y = (self.screen_height - 600) // 2
                        cv2.moveWindow(self.window_name, x, y)
                        self.window_state = "normal"
                    self.blink_count = 0
            
            elif time.time() - self.both_eyes_closed_time > self.EXIT_BLINK_TIME:
                return frame, True
        else:
            if (self.both_eyes_closed_time is not None and
                    time.time() - self.both_eyes_closed_time < self.EXIT_BLINK_TIME):
                # Left click on left eye blink
                if left_ear < self.blink_threshold:
                    pyautogui.click()
            self.both_eyes_closed_time = None

        # Calculate average horizontal and vertical ratios from both eyes
        avg_x = (left_iris_pos[0] + right_iris_pos[0]) / 2
        avg_y = (left_iris_pos[1] + right_iris_pos[1]) / 2



        # Map to screen coordinates and apply smoothing
        screen_x, screen_y = self.map_to_screen(avg_x, avg_y)
        smooth_x, smooth_y = self.smooth_coordinates(screen_x, screen_y)

        # Scale for actual screen resolution
        scaled_x = int(smooth_x * (self.screen_width / self.display_width))
        scaled_y = int(smooth_y * (self.screen_height / self.display_height))
        
        # Clamp to screen bounds
        scaled_x = max(0, min(scaled_x, self.screen_width - 1))
        scaled_y = max(0, min(scaled_y, self.screen_height - 1))
        
        # Move cursor
        try:
            pyautogui.moveTo(scaled_x, scaled_y, _pause=False)
        except Exception as e:
            print(f"Error moving cursor: {e}")

        # Draw debug visualization
        self.draw_debug_visualization(frame, landmarks, left_ear, right_ear)

        return frame, False

    def set_window_size(self) -> None:
        """Keep window maximized at all times."""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        if not self.is_fullscreen:
            cv2.resizeWindow(self.window_name, self.display_width, self.display_height)
            self.is_fullscreen = True

    def draw_debug_visualization(self, frame: np.ndarray, landmarks: np.ndarray,
                                 left_ear: float, right_ear: float) -> None:
        """Draw debug information on the frame."""
        # Keep window maximized
        self.set_window_size()

        # Draw eye landmarks
        for eye_points in [self.LEFT_EYE, self.RIGHT_EYE]:
            for point in landmarks[eye_points]:
                cv2.circle(frame, (int(point[0]), int(point[1])),
                           2, (0, 255, 0), -1)

        # Draw iris landmarks
        for iris_points in [self.LEFT_IRIS, self.RIGHT_IRIS]:
            for point in landmarks[iris_points]:
                cv2.circle(frame, (int(point[0]), int(point[1])),
                           2, (255, 0, 0), -1)

        # Display EAR values and filter status
        cv2.putText(frame, f"Left EAR: {left_ear:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Right EAR: {right_ear:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display filter status
        filter_status = "Kalman Filter: ON" if self.use_kalman_filter else "Kalman Filter: OFF"
        cv2.putText(frame, filter_status, (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # Draw calibration points during calibration
        if not self.calibrated and self.calibration_started:
            # Create a black background for calibration
            if not self.calibrated:
                frame[:] = (0, 0, 0)  # Black background

            # Draw all 15 calibration points
            for idx, (point, desc) in enumerate(self.calibration_points):
                x = int(point[0] * self.monitor_width)
                y = int(point[1] * self.monitor_height)

                # Make dots larger for full screen
                dot_size = 20 if idx == self.current_calibration_point else 15
                color = (0, 0, 255) if idx == self.current_calibration_point else (128, 128, 128)
                cv2.circle(frame, (x, y), dot_size, color, -1)

                # Draw point number with larger font
                cv2.putText(frame, str(idx + 1), (x - 10, y + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

            # Draw current point instructions with larger font and centered
            current_point_desc = self.calibration_points[self.current_calibration_point][1]
            instruction_text = f"Look at the {current_point_desc} dot #{self.current_calibration_point + 1}"
            progress_text = f"Progress: {self.calibration_frame_count}/{self.frames_per_point} frames"

            # Calculate text size for centering
            text_size = cv2.getTextSize(instruction_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)[0]
            text_x = (self.monitor_width - text_size[0]) // 2

            # Draw centered text with shadow effect
            cv2.putText(frame, instruction_text,
                        (text_x, self.monitor_height - 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            cv2.putText(frame, progress_text,
                        (text_x, self.monitor_height - 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

    def run(self) -> None:
        """Main loop for eye-controlled mouse."""
        print("Starting eye-controlled mouse with 15-point calibration.")
        print("Look straight ahead for calibration.")
        print("Blink left eye for click, both eyes for 1 second to exit.")

        # Set initial window to fullscreen
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame, should_exit = self.process_frame(frame)

            # Show debug window
            if not self.calibrated:
                # For calibration, ensure we're using full screen resolution
                display_frame = np.zeros((self.monitor_height, self.monitor_width, 3), dtype=np.uint8)
                
                # Draw calibration points on black background
                for idx, (point, desc) in enumerate(self.calibration_points):
                    x = int(point[0] * self.monitor_width)
                    y = int(point[1] * self.monitor_height)
                    
                    # Current point is red, others are gray
                    color = (0, 0, 255) if idx == self.current_calibration_point else (128, 128, 128)
                    cv2.circle(display_frame, (x, y), 20, color, -1)
                    cv2.putText(display_frame, str(idx + 1), (x - 10, y + 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
                
                # Add calibration instructions
                if self.calibration_started:
                    text = f"Look at point {self.current_calibration_point + 1}: {self.calibration_points[self.current_calibration_point][1]}"
                    cv2.putText(display_frame, text, (self.monitor_width // 4, self.monitor_height - 50),
                              cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
                
                cv2.imshow(self.window_name, display_frame)
            else:
                # After calibration, show normal debug view
                cv2.resizeWindow(self.window_name, 800, 600)
                cv2.imshow(self.window_name, frame)

            # Check for exit conditions
            if should_exit or cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        self.face_mesh.close()


if __name__ == "__main__":
    eye_mouse = EyeControlledMouse()
    eye_mouse.run()