"""
15-Point Calibration System
===========================
Enhanced calibration with 15 points for improved accuracy.

Author: SHA Graduation Project Group 24
"""

import numpy as np
import json
import pickle
from typing import Tuple, List, Optional
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
import cv2
from collections import deque


class Calibration15Point:
    """15-point calibration system with horizontal mid-points."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize 15-point calibration system.
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Calibration state
        self.is_calibrated = False
        self.calibration_grid = []
        self.current_point_idx = 0
        self.current_frame_count = 0
        self.frames_per_point = 60
        
        # Calibration data storage
        self.calibration_samples = []
        
        # Regression model
        self.model_x = None
        self.model_y = None
        self.poly_features = PolynomialFeatures(degree=3)  # Degree 3 for better vertical accuracy
        self.training_error_x = 0.0
        self.training_error_y = 0.0
        
        # Advanced smoothing (optimized for responsiveness)
        self.smooth_window = 7
        self.x_coords = deque(maxlen=self.smooth_window)
        self.y_coords = deque(maxlen=self.smooth_window)
        self.last_valid_x = None
        self.last_valid_y = None
        self.smooth_factor = 0.5
        
        # Output gain
        self.output_gain = 1.0
        
        # File paths
        self.calibration_file = "calibration_15point.json"
        self.model_file = "calibration_15point.pkl"
        
    def generate_calibration_grid(self, num_points: int = 21) -> List[Tuple[int, int]]:
        """
        Generate calibration grid with proper screen alignment.
        
        21-point grid layout (default):
        1  2  3  4  5     (top row - 5 points at y=0.05)
           6  7  8        (upper mid - 3 points at y=0.3)  
        9  10 11 12 13    (center row - 5 points at y=0.5)
           14 15 16       (lower mid - 3 points at y=0.7)
        17 18 19 20 21    (bottom row - 5 points at y=0.95)
        
        9-point grid layout:
        1  2  3           (top row at y=0.05)
        4  5  6           (middle row at y=0.5)
        7  8  9           (bottom row at y=0.95)
        
        Args:
            num_points: Number of calibration points (9 or 21)
            
        Returns:
            List of (x, y) screen coordinates properly aligned to screen edges
        """
        
        if num_points == 9:
            # Standard 3x3 grid - corners at true edges
            grid_points = []
            # Use 0.05 and 0.95 for better edge coverage
            for row in [0.05, 0.5, 0.95]:
                for col in [0.05, 0.5, 0.95]:
                    x = int(col * self.screen_width)
                    y = int(row * self.screen_height)
                    grid_points.append((x, y))
        else:
            # 15-point enhanced grid with proper alignment
            grid_points = []
            
            # Top row (5 points): far left to far right
            # 0.05, 0.275, 0.5, 0.725, 0.95
            y_pos = int(0.05 * self.screen_height)
            for col in [0.05, 0.275, 0.5, 0.725, 0.95]:
                x = int(col * self.screen_width)
                grid_points.append((x, y_pos))
            
            # Upper middle row (3 points): quarter positions
            # 0.275, 0.5, 0.725
            y_pos = int(0.3 * self.screen_height)
            for col in [0.275, 0.5, 0.725]:
                x = int(col * self.screen_width)
                grid_points.append((x, y_pos))
            
            # Center row (5 points): same as top row
            # 0.05, 0.275, 0.5, 0.725, 0.95
            y_pos = int(0.5 * self.screen_height)
            for col in [0.05, 0.275, 0.5, 0.725, 0.95]:
                x = int(col * self.screen_width)
                grid_points.append((x, y_pos))
            
            # Lower middle row (3 points): quarter positions
            # 0.275, 0.5, 0.725
            y_pos = int(0.7 * self.screen_height)
            for col in [0.275, 0.5, 0.725]:
                x = int(col * self.screen_width)
                grid_points.append((x, y_pos))
            
            # Bottom row (5 points): same as top row for symmetry
            # 0.05, 0.275, 0.5, 0.725, 0.95
            y_pos = int(0.95 * self.screen_height)
            for col in [0.05, 0.275, 0.5, 0.725, 0.95]:
                x = int(col * self.screen_width)
                grid_points.append((x, y_pos))
                
        return grid_points
        
    def start_calibration(self, num_points: int = 21):
        """Start calibration process."""
        self.is_calibrated = False
        self.calibration_grid = self.generate_calibration_grid(num_points)
        self.current_point_idx = 0
        self.current_frame_count = 0
        self.calibration_samples = []
        
    def collect_calibration_frame(self, left_eye: Tuple[float, float],
                                  right_eye: Tuple[float, float],
                                  nose: Tuple[float, float]) -> bool:
        """
        Collect calibration data for current frame.
        
        Args:
            left_eye: (horizontal_ratio, vertical_ratio) for left eye
            right_eye: (horizontal_ratio, vertical_ratio) for right eye
            nose: (x_ratio, y_ratio) for nose tip
            
        Returns:
            True if calibration is complete, False otherwise
        """
        if self.current_point_idx >= len(self.calibration_grid):
            return True
            
        # Get current calibration point
        target_x, target_y = self.calibration_grid[self.current_point_idx]
        
        # Store sample
        self.calibration_samples.append({
            'left_eye': left_eye,
            'right_eye': right_eye,
            'nose': nose,
            'screen_x': target_x,
            'screen_y': target_y,
            'point_idx': self.current_point_idx
        })
        
        self.current_frame_count += 1
        
        # Check if enough frames collected for this point
        if self.current_frame_count >= self.frames_per_point:
            self.current_point_idx += 1
            self.current_frame_count = 0
            
            # Check if calibration complete
            if self.current_point_idx >= len(self.calibration_grid):
                self._train_model()
                return True
                
        return False
        
    def _train_model(self):
        """Train regression model from calibration samples."""
        if len(self.calibration_samples) < 10:
            print("Not enough calibration samples!")
            return
        
        # Group samples by calibration point and average them
        point_data = {}
        for sample in self.calibration_samples:
            point_idx = sample['point_idx']
            if point_idx not in point_data:
                point_data[point_idx] = []
            point_data[point_idx].append(sample)
        
        # Prepare training data with averaged samples per point
        X = []
        y_x = []
        y_y = []
        
        for point_idx, samples in point_data.items():
            # Average all samples for this calibration point
            avg_left_x = np.mean([s['left_eye'][0] for s in samples])
            avg_left_y = np.mean([s['left_eye'][1] for s in samples])
            avg_right_x = np.mean([s['right_eye'][0] for s in samples])
            avg_right_y = np.mean([s['right_eye'][1] for s in samples])
            avg_nose_x = np.mean([s['nose'][0] for s in samples])
            avg_nose_y = np.mean([s['nose'][1] for s in samples])
            
            # Compute additional features for better accuracy
            avg_eye_x = (avg_left_x + avg_right_x) / 2
            avg_eye_y = (avg_left_y + avg_right_y) / 2
            eye_diff_x = avg_right_x - avg_left_x
            eye_diff_y = avg_right_y - avg_left_y
            
            # Enhanced feature set (10 features total)
            features = [
                avg_left_x, avg_left_y,      # Left eye position
                avg_right_x, avg_right_y,    # Right eye position
                avg_eye_x, avg_eye_y,        # Average eye position (main indicator)
                eye_diff_x, eye_diff_y,      # Eye difference (head angle compensation)
                avg_nose_x, avg_nose_y       # Nose position (head position)
            ]
            
            X.append(features)
            y_x.append(samples[0]['screen_x'])
            y_y.append(samples[0]['screen_y'])
            
        X = np.array(X)
        y_x = np.array(y_x)
        y_y = np.array(y_y)
        
        # Create sample weights - emphasize edges and corners
        sample_weights = []
        for i, (px, py) in enumerate(zip(y_x, y_y)):
            # Normalize to 0-1 range
            norm_x = px / self.screen_width
            norm_y = py / self.screen_height
            
            # Distance from center (0 at center, 1 at corners)
            dist_from_center = np.sqrt((norm_x - 0.5)**2 + (norm_y - 0.5)**2)
            
            # Weight: 1.0 for center, up to 5.0 for edges/corners (increased from 4.0)
            weight = 1.0 + dist_from_center * 8.0
            sample_weights.append(weight)
        
        sample_weights = np.array(sample_weights)
        
        print(f"Training with {len(X)} averaged calibration points (edge-weighted)")
        
        # Add polynomial features (degree=3 for non-linear mapping)
        X_poly = self.poly_features.fit_transform(X)
        
        # Train models with sample weights (emphasize edges)
        self.model_x = Ridge(alpha=0.01)  # Very low regularization
        self.model_y = Ridge(alpha=0.01)
        
        self.model_x.fit(X_poly, y_x, sample_weight=sample_weights)
        self.model_y.fit(X_poly, y_y, sample_weight=sample_weights)
        
        # Calculate training accuracy
        pred_x = self.model_x.predict(X_poly)
        pred_y = self.model_y.predict(X_poly)
        error_x = np.mean(np.abs(pred_x - y_x))
        error_y = np.mean(np.abs(pred_y - y_y))
        
        # Store training errors for logging
        self.training_error_x = error_x
        self.training_error_y = error_y
        
        self.is_calibrated = True
        print(f"✓ Calibration complete - Avg error: X={error_x:.1f}px, Y={error_y:.1f}px")
        
    def predict_screen_position(self, left_eye: Tuple[float, float],
                                right_eye: Tuple[float, float],
                                nose: Tuple[float, float],
                                use_smoothing: bool = True) -> Tuple[int, int]:
        """
        Predict screen position from eye gaze.
        
        Args:
            left_eye: (horizontal_ratio, vertical_ratio) for left eye
            right_eye: (horizontal_ratio, vertical_ratio) for right eye
            nose: (x_ratio, y_ratio) for nose tip
            use_smoothing: Whether to apply smoothing
            
        Returns:
            (screen_x, screen_y) predicted cursor position
        """
        if not self.is_calibrated:
            # Fallback to simple mapping
            avg_x = (left_eye[0] + right_eye[0]) / 2
            avg_y = (left_eye[1] + right_eye[1]) / 2
            return int(avg_x * self.screen_width), int(avg_y * self.screen_height)
            
        # Compute same enhanced features as training
        avg_eye_x = (left_eye[0] + right_eye[0]) / 2
        avg_eye_y = (left_eye[1] + right_eye[1]) / 2
        eye_diff_x = right_eye[0] - left_eye[0]
        eye_diff_y = right_eye[1] - left_eye[1]
        
        # Prepare features (same 10 features as training)
        features = np.array([[
            left_eye[0], left_eye[1],
            right_eye[0], right_eye[1],
            avg_eye_x, avg_eye_y,
            eye_diff_x, eye_diff_y,
            nose[0], nose[1]
        ]])
        
        features_poly = self.poly_features.transform(features)
        
        # Predict with error handling for feature mismatch
        try:
            pred_x = self.model_x.predict(features_poly)[0]
            pred_y = self.model_y.predict(features_poly)[0]
        except Exception as e:
            print(f"Prediction error (recalibration needed): {e}")
            # Fallback to simple mapping
            avg_x = (left_eye[0] + right_eye[0]) / 2
            avg_y = (left_eye[1] + right_eye[1]) / 2
            return int(avg_x * self.screen_width), int(avg_y * self.screen_height)
        
        # Apply gain
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        
        pred_x = center_x + (pred_x - center_x) * self.output_gain
        pred_y = center_y + (pred_y - center_y) * self.output_gain
        
        # Advanced smoothing (from main.py)
        if use_smoothing:
            pred_x, pred_y = self._smooth_coordinates(pred_x, pred_y)
            
        # Clamp to screen bounds
        pred_x = max(0, min(self.screen_width - 1, int(pred_x)))
        pred_y = max(0, min(self.screen_height - 1, int(pred_y)))
        
        return pred_x, pred_y
    
    def _smooth_coordinates(self, x: float, y: float) -> Tuple[int, int]:
        """Apply advanced smoothing to coordinates (from main.py)."""
        if self.last_valid_x is None:
            self.last_valid_x = x
            self.last_valid_y = y
            self.x_coords.clear()
            self.y_coords.clear()

        # Handle large movements (outlier detection)
        max_delta = 200
        if abs(x - self.last_valid_x) > max_delta or abs(y - self.last_valid_y) > max_delta:
            x = int(self.last_valid_x * 0.5 + x * 0.5)
            y = int(self.last_valid_y * 0.5 + y * 0.5)

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
        
    def save_calibration_data(self):
        """Save calibration data to file."""
        if not self.is_calibrated:
            return
            
        # Save samples and training errors
        data = {
            'screen_width': self.screen_width,
            'screen_height': self.screen_height,
            'samples': self.calibration_samples,
            'grid': self.calibration_grid,
            'training_error_x': float(self.training_error_x),
            'training_error_y': float(self.training_error_y)
        }
        
        with open(self.calibration_file, 'w') as f:
            json.dump(data, f)
            
        # Save models
        model_data = {
            'model_x': self.model_x,
            'model_y': self.model_y,
            'poly_features': self.poly_features
        }
        
        with open(self.model_file, 'wb') as f:
            pickle.dump(model_data, f)
            
        print(f"✓ Calibration saved to {self.calibration_file}")
        
    def load_calibration_data(self) -> bool:
        """Load calibration data from file."""
        try:
            # Load samples
            with open(self.calibration_file, 'r') as f:
                data = json.load(f)
                
            self.calibration_samples = data['samples']
            self.calibration_grid = [tuple(p) for p in data['grid']]
            
            # Load models
            with open(self.model_file, 'rb') as f:
                model_data = pickle.load(f)
                
            self.model_x = model_data['model_x']
            self.model_y = model_data['model_y']
            self.poly_features = model_data['poly_features']
            
            # Load training errors
            self.training_error_x = data.get('training_error_x', 0.0)
            self.training_error_y = data.get('training_error_y', 0.0)
            
            # Validate feature count (should be 10 for new enhanced model)
            expected_features = 10
            if hasattr(self.poly_features, 'n_features_in_'):
                if self.poly_features.n_features_in_ != expected_features:
                    print(f"⚠ Old calibration format detected ({self.poly_features.n_features_in_} features vs {expected_features} expected)")
                    print("  Please delete old calibration with 'D' command and recalibrate")
                    return False
            
            self.is_calibrated = True
            print(f"✓ Calibration loaded from {self.calibration_file}")
            return True
            
        except Exception as e:
            print(f"Could not load calibration: {e}")
            return False
            
    def reset_smoothing_filters(self):
        """Reset smoothing buffers."""
        self.x_coords.clear()
        self.y_coords.clear()
        self.last_valid_x = None
        self.last_valid_y = None
        
    def adjust_output_gain(self, delta: float):
        """Adjust output gain."""
        self.output_gain = max(0.5, min(2.0, self.output_gain + delta))
        
    def draw_calibration_interface(self, camera_frame):
        """Draw calibration UI on camera frame."""
        if self.current_point_idx >= len(self.calibration_grid):
            return camera_frame
            
        # Create black canvas
        h, w = camera_frame.shape[:2]
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Scale calibration points to frame size
        scale_x = w / self.screen_width
        scale_y = h / self.screen_height
        
        # Draw all points
        for idx, (px, py) in enumerate(self.calibration_grid):
            x = int(px * scale_x)
            y = int(py * scale_y)
            
            if idx == self.current_point_idx:
                # Current point
                cv2.circle(canvas, (x, y), 25, (0, 0, 255), -1)
                cv2.circle(canvas, (x, y), 30, (255, 255, 255), 2)
                cv2.putText(canvas, str(idx + 1), (x - 10, y + 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            elif idx < self.current_point_idx:
                # Completed point
                cv2.circle(canvas, (x, y), 15, (0, 255, 0), -1)
            else:
                # Future point
                cv2.circle(canvas, (x, y), 15, (128, 128, 128), -1)
                
        # Progress text
        progress = f"Point {self.current_point_idx + 1}/{len(self.calibration_grid)}"
        frame_progress = f"{self.current_frame_count}/{self.frames_per_point}"
        
        cv2.putText(canvas, progress, (w // 2 - 100, h - 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(canvas, frame_progress, (w // 2 - 80, h - 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        return canvas
