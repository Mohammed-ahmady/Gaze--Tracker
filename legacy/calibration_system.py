"""
Advanced Multi-Stage Calibration System for Eye-Controlled Mouse
=================================================================

This module implements a high-precision, personalized eye tracking calibration system
with the following features:
- Multi-point calibration (9-25 points)
- Polynomial regression for non-linear eye-to-screen mapping
- Kalman filtering for jitter reduction
- Head motion compensation
- Incremental recalibration
- Cross-session persistence
- Real-time visual feedback

Author: SHA Graduation Project Group 24
Supervisor: Dr. Mohammed Hussien
Date: October 2025
"""

import cv2
import numpy as np
import json
import os
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from scipy.interpolate import Rbf
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
import pickle


@dataclass
class CalibrationPoint:
    """Represents a single calibration point with eye and screen data."""
    screen_x: int
    screen_y: int
    left_iris_x: float
    left_iris_y: float
    right_iris_x: float
    right_iris_y: float
    head_x: float  # Nose tip X for head motion compensation
    head_y: float  # Nose tip Y for head motion compensation
    timestamp: str


class KalmanFilter:
    """
    1D Kalman Filter for smoothing gaze coordinates.
    Reduces jitter while maintaining responsiveness to real movements.
    """
    
    def __init__(self, process_variance=1e-5, measurement_variance=1e-1):
        """
        Initialize Kalman filter.
        
        Args:
            process_variance: How much we expect the true state to change (lower = smoother)
            measurement_variance: Measurement noise level (higher = more smoothing)
        """
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0
        
    def update(self, measurement: float) -> float:
        """
        Update filter with new measurement.
        
        Args:
            measurement: New measured value
            
        Returns:
            Filtered estimate
        """
        # Prediction
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance
        
        # Update
        blending_factor = priori_error_estimate / (priori_error_estimate + self.measurement_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate
        
        return self.posteri_estimate
    
    def reset(self):
        """Reset filter state."""
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0


class ExponentialMovingAverage:
    """
    Exponential Moving Average filter for coordinate smoothing.
    Alternative to Kalman filter with simpler implementation.
    """
    
    def __init__(self, alpha=0.3):
        """
        Initialize EMA filter.
        
        Args:
            alpha: Smoothing factor (0-1). Lower = smoother, higher = more responsive
        """
        self.alpha = alpha
        self.value = None
        
    def update(self, measurement: float) -> float:
        """Update filter with new measurement."""
        if self.value is None:
            self.value = measurement
        else:
            self.value = self.alpha * measurement + (1 - self.alpha) * self.value
        return self.value
    
    def reset(self):
        """Reset filter state."""
        self.value = None


class AdvancedCalibrationSystem:
    """
    Main calibration system implementing multi-stage personalized eye tracking calibration.
    """
    
    def __init__(self, screen_width: int, screen_height: int, 
                 calibration_file: str = "calibration_data.json",
                 model_file: str = "calibration_model.pkl"):
        """
        Initialize calibration system.
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            calibration_file: Path to save/load calibration data
            model_file: Path to save/load trained model
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.calibration_file = calibration_file
        self.model_file = model_file
        
        # Calibration points configuration
        self.calibration_grid = self._generate_calibration_grid(9)  # 9-point by default
        self.current_point_idx = 0
        self.calibration_data: List[CalibrationPoint] = []
        self.frames_per_point = 60  # 2 seconds at 30 FPS
        self.current_frame_count = 0
        self.temp_data_buffer = []
        
        # Calibration state
        self.is_calibrated = False
        self.is_calibrating = False
        
        # Mapping models
        self.x_model = None  # Polynomial regression for X coordinate
        self.y_model = None  # Polynomial regression for Y coordinate
        self.rbf_x = None    # Radial Basis Function for X (alternative)
        self.rbf_y = None    # Radial Basis Function for Y (alternative)
        self.poly_features = None
        
        # Smoothing filters
        self.kalman_x = KalmanFilter()
        self.kalman_y = KalmanFilter()
        self.ema_x = ExponentialMovingAverage(alpha=0.4)
        self.ema_y = ExponentialMovingAverage(alpha=0.4)

        # Output gain to adjust cursor movement amplitude (1.0 = neutral)
        self.output_gain = 1.0
        
        # Head motion compensation baseline
        self.head_baseline_x = None
        self.head_baseline_y = None
        
        # Performance metrics
        self.calibration_error_pixels = 0.0
        self.last_predicted_x = None
        self.last_predicted_y = None
        
        # Visual feedback
        self.window_name = "Eye Tracking Calibration"
        self.point_color = (0, 0, 255)  # Red
        self.active_color = (0, 255, 0)  # Green
        self.text_color = (255, 255, 255)  # White
        
    def _generate_calibration_grid(self, num_points: int = 9) -> List[Tuple[float, float]]:
        """
        Generate calibration grid points as normalized coordinates (0-1).
        
        Args:
            num_points: Number of calibration points (9, 13, 16, or 25)
            
        Returns:
            List of (x, y) normalized coordinates
        """
        if num_points == 9:
            # 3x3 grid
            return [
                (0.1, 0.1), (0.5, 0.1), (0.9, 0.1),  # Top row
                (0.1, 0.5), (0.5, 0.5), (0.9, 0.5),  # Middle row
                (0.1, 0.9), (0.5, 0.9), (0.9, 0.9)   # Bottom row
            ]
        elif num_points == 13:
            # 9-point + 4 additional points
            return [
                (0.1, 0.1), (0.5, 0.1), (0.9, 0.1),
                (0.1, 0.5), (0.5, 0.5), (0.9, 0.5),
                (0.1, 0.9), (0.5, 0.9), (0.9, 0.9),
                (0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)
            ]
        elif num_points == 16:
            # 4x4 grid
            return [(x, y) for y in [0.1, 0.4, 0.6, 0.9] 
                    for x in [0.1, 0.4, 0.6, 0.9]]
        elif num_points == 25:
            # 5x5 grid for maximum precision
            return [(x, y) for y in [0.1, 0.3, 0.5, 0.7, 0.9] 
                    for x in [0.1, 0.3, 0.5, 0.7, 0.9]]
        else:
            raise ValueError("num_points must be 9, 13, 16, or 25")
    
    def start_calibration(self, num_points: int = 9):
        """
        Start the calibration process.
        
        Args:
            num_points: Number of calibration points to use
        """
        self.calibration_grid = self._generate_calibration_grid(num_points)
        self.current_point_idx = 0
        self.calibration_data = []
        self.temp_data_buffer = []
        self.current_frame_count = 0
        self.is_calibrating = True
        self.is_calibrated = False
        
        # Reset filters
        self.kalman_x.reset()
        self.kalman_y.reset()
        self.ema_x.reset()
        self.ema_y.reset()
        
        print(f"\n{'='*60}")
        print(f"Starting {num_points}-Point Calibration")
        print(f"{'='*60}")
        print("Instructions:")
        print("1. Look at each RED dot when it appears")
        print("2. Keep your head still and focus on the dot")
        print("3. The dot will turn GREEN when data is being collected")
        print("4. Stay focused until the dot disappears")
        print(f"{'='*60}\n")
    
    def collect_calibration_frame(self, left_iris: Tuple[float, float], 
                                   right_iris: Tuple[float, float],
                                   nose_tip: Tuple[float, float]) -> bool:
        """
        Collect calibration data for one frame.
        
        Args:
            left_iris: (x, y) normalized coordinates of left iris center
            right_iris: (x, y) normalized coordinates of right iris center
            nose_tip: (x, y) normalized coordinates of nose tip (for head compensation)
            
        Returns:
            True if calibration is complete, False otherwise
        """
        if not self.is_calibrating or self.current_point_idx >= len(self.calibration_grid):
            return True
        
        # Get current target point
        target_norm = self.calibration_grid[self.current_point_idx]
        target_x = int(target_norm[0] * self.screen_width)
        target_y = int(target_norm[1] * self.screen_height)
        
        # Store data in temporary buffer
        self.temp_data_buffer.append({
            'left_iris': left_iris,
            'right_iris': right_iris,
            'nose_tip': nose_tip
        })
        
        self.current_frame_count += 1
        
        # After collecting enough frames, compute average and store
        if self.current_frame_count >= self.frames_per_point:
            # Compute average of collected data (reduces noise)
            avg_left_x = np.mean([d['left_iris'][0] for d in self.temp_data_buffer])
            avg_left_y = np.mean([d['left_iris'][1] for d in self.temp_data_buffer])
            avg_right_x = np.mean([d['right_iris'][0] for d in self.temp_data_buffer])
            avg_right_y = np.mean([d['right_iris'][1] for d in self.temp_data_buffer])
            avg_nose_x = np.mean([d['nose_tip'][0] for d in self.temp_data_buffer])
            avg_nose_y = np.mean([d['nose_tip'][1] for d in self.temp_data_buffer])
            
            # Create calibration point
            cal_point = CalibrationPoint(
                screen_x=target_x,
                screen_y=target_y,
                left_iris_x=avg_left_x,
                left_iris_y=avg_left_y,
                right_iris_x=avg_right_x,
                right_iris_y=avg_right_y,
                head_x=avg_nose_x,
                head_y=avg_nose_y,
                timestamp=datetime.now().isoformat()
            )
            
            self.calibration_data.append(cal_point)
            
            print(f"✓ Point {self.current_point_idx + 1}/{len(self.calibration_grid)} completed")
            print(f"  Screen: ({target_x}, {target_y})")
            print(f"  Eyes: L({avg_left_x:.3f}, {avg_left_y:.3f}), R({avg_right_x:.3f}, {avg_right_y:.3f})")
            
            # Move to next point
            self.current_point_idx += 1
            self.current_frame_count = 0
            self.temp_data_buffer = []
            
            # Check if calibration is complete
            if self.current_point_idx >= len(self.calibration_grid):
                self.is_calibrating = False
                self._train_mapping_model()
                return True
        
        return False
    
    def _train_mapping_model(self):
        """
        Train polynomial regression model to map eye coordinates to screen coordinates.
        Uses both polynomial features and radial basis functions for robust mapping.
        """
        print(f"\n{'='*60}")
        print("Training Calibration Model...")
        print(f"{'='*60}")
        
        if len(self.calibration_data) < 4:
            print("ERROR: Not enough calibration points. Need at least 4.")
            return
        
        # Extract features and targets
        # Features: [left_iris_x, left_iris_y, right_iris_x, right_iris_y, head_x, head_y]
        X = np.array([
            [p.left_iris_x, p.left_iris_y, p.right_iris_x, p.right_iris_y, p.head_x, p.head_y]
            for p in self.calibration_data
        ])
        
        # Targets: screen coordinates
        y_x = np.array([p.screen_x for p in self.calibration_data])
        y_y = np.array([p.screen_y for p in self.calibration_data])
        
        # Set head baseline for motion compensation
        self.head_baseline_x = np.mean([p.head_x for p in self.calibration_data])
        self.head_baseline_y = np.mean([p.head_y for p in self.calibration_data])
        
        print(f"Training data: {len(self.calibration_data)} points")
        print(f"Head baseline: ({self.head_baseline_x:.3f}, {self.head_baseline_y:.3f})")
        
        # Method 1: Polynomial Regression (degree 2 for non-linear mapping)
        try:
            self.poly_features = PolynomialFeatures(degree=2, include_bias=True)
            X_poly = self.poly_features.fit_transform(X)
            
            # Train separate models for X and Y with Ridge regularization
            self.x_model = Ridge(alpha=1.0)
            self.y_model = Ridge(alpha=1.0)
            
            self.x_model.fit(X_poly, y_x)
            self.y_model.fit(X_poly, y_y)
            
            # Calculate training error
            pred_x = self.x_model.predict(X_poly)
            pred_y = self.y_model.predict(X_poly)
            
            errors = np.sqrt((pred_x - y_x)**2 + (pred_y - y_y)**2)
            self.calibration_error_pixels = np.mean(errors)
            
            print(f"✓ Polynomial model trained")
            print(f"  Mean calibration error: {self.calibration_error_pixels:.2f} pixels")
            print(f"  Max error: {np.max(errors):.2f} pixels")
            
        except Exception as e:
            print(f"ERROR training polynomial model: {e}")
            return
        
        # Method 2: Radial Basis Function (RBF) interpolation (backup method)
        try:
            # Use average of left and right iris for RBF
            iris_x = (X[:, 0] + X[:, 2]) / 2
            iris_y = (X[:, 1] + X[:, 3]) / 2
            
            self.rbf_x = Rbf(iris_x, iris_y, y_x, function='multiquadric', smooth=5)
            self.rbf_y = Rbf(iris_x, iris_y, y_y, function='multiquadric', smooth=5)
            
            print(f"✓ RBF interpolation model trained (backup)")
            
        except Exception as e:
            print(f"Warning: RBF training failed: {e}")
        
        self.is_calibrated = True
        print(f"{'='*60}")
        print("✓ Calibration Complete!")
        print(f"{'='*60}\n")
        
        # Auto-save calibration
        self.save_calibration_data()
    
    def predict_screen_position(self, left_iris: Tuple[float, float],
                                right_iris: Tuple[float, float],
                                nose_tip: Tuple[float, float],
                                use_smoothing: bool = True) -> Tuple[int, int]:
        """
        Predict screen coordinates from eye landmarks.
        
        Args:
            left_iris: (horizontal_ratio, vertical_ratio) of left iris (0-1 range)
            right_iris: (horizontal_ratio, vertical_ratio) of right iris (0-1 range)
            nose_tip: (x, y) normalized coordinates of nose tip
            use_smoothing: Whether to apply Kalman/EMA smoothing
            
        Returns:
            (screen_x, screen_y) predicted screen coordinates
        """
        if not self.is_calibrated or self.x_model is None:
            # Return center if not calibrated
            return self.screen_width // 2, self.screen_height // 2
        
        # Average both eyes for combined gaze position
        combined_x = (left_iris[0] + right_iris[0]) / 2.0
        combined_y = (left_iris[1] + right_iris[1]) / 2.0
        
        # Use calibration data to normalize based on observed extremes during calibration
        if self.calibration_data and len(self.calibration_data) >= 9:
            # Get calibration extremes (center, left, right, top, bottom points)
            # Assuming standard 9-point grid: indices 0-8 correspond to grid positions
            try:
                center_point = self.calibration_data[4]  # center
                center_x = (center_point.left_iris_x + center_point.right_iris_x) / 2.0
                center_y = (center_point.left_iris_y + center_point.right_iris_y) / 2.0

                left_point = self.calibration_data[3]  # middle left
                right_point = self.calibration_data[5]  # middle right
                top_point = self.calibration_data[1]    # top center
                bottom_point = self.calibration_data[7] # bottom center

                left_x = (left_point.left_iris_x + left_point.right_iris_x) / 2.0
                right_x = (right_point.left_iris_x + right_point.right_iris_x) / 2.0
                top_y = (top_point.left_iris_y + top_point.right_iris_y) / 2.0
                bottom_y = (bottom_point.left_iris_y + bottom_point.right_iris_y) / 2.0

                # Calculate the range of eye movement during calibration
                eye_width_range = abs(right_x - left_x)
                eye_height_range = abs(bottom_y - top_y)

                # Normalize the current position relative to calibration extremes
                if eye_width_range > 0.01:
                    normalized_x = (combined_x - left_x) / eye_width_range
                else:
                    normalized_x = 0.5

                if eye_height_range > 0.01:
                    normalized_y = (combined_y - top_y) / eye_height_range
                else:
                    normalized_y = 0.5

                # Clamp normalized values
                normalized_x = np.clip(normalized_x, 0.0, 1.0)
                normalized_y = np.clip(normalized_y, 0.0, 1.0)

                # Apply sensitivity adjustment around center
                sensitivity_x = 1.2
                sensitivity_y = 1.2
                
                adjusted_x = (normalized_x - 0.5) * sensitivity_x + 0.5
                adjusted_y = (normalized_y - 0.5) * sensitivity_y + 0.5
                
                # Clamp again after sensitivity
                adjusted_x = np.clip(adjusted_x, 0.0, 1.0)
                adjusted_y = np.clip(adjusted_y, 0.0, 1.0)

                # Apply output gain
                if self.output_gain != 1.0:
                    adjusted_x = 0.5 + (adjusted_x - 0.5) * self.output_gain
                    adjusted_y = 0.5 + (adjusted_y - 0.5) * self.output_gain
                    adjusted_x = np.clip(adjusted_x, 0.0, 1.0)
                    adjusted_y = np.clip(adjusted_y, 0.0, 1.0)

                # Convert to screen coordinates
                pred_x = adjusted_x * self.screen_width
                pred_y = adjusted_y * self.screen_height
            except (IndexError, AttributeError):
                # Fallback if calibration data structure is incomplete
                pred_x = combined_x * self.screen_width
                pred_y = combined_y * self.screen_height
        else:
            # Direct mapping if insufficient calibration data
            pred_x = combined_x * self.screen_width
            pred_y = combined_y * self.screen_height
        
        # Apply smoothing filters if enabled
        if use_smoothing:
            pred_x = self.kalman_x.update(pred_x)
            pred_y = self.kalman_y.update(pred_y)
            
            # Double smoothing with EMA for extra stability
            pred_x = self.ema_x.update(pred_x)
            pred_y = self.ema_y.update(pred_y)
        
        # Clamp to screen boundaries
        pred_x = int(np.clip(pred_x, 0, self.screen_width - 1))
        pred_y = int(np.clip(pred_y, 0, self.screen_height - 1))
        
        # Store for incremental recalibration
        self.last_predicted_x = pred_x
        self.last_predicted_y = pred_y
        
        return pred_x, pred_y

    # ----- Runtime tuning helpers -----
    def set_output_gain(self, gain: float):
        """Set movement gain (typical range 0.5 - 3.0)."""
        self.output_gain = float(max(0.1, min(gain, 5.0)))

    def adjust_output_gain(self, delta: float):
        """Adjust movement gain incrementally."""
        self.set_output_gain(self.output_gain + delta)

    def set_ema_alpha(self, alpha: float):
        """Adjust EMA smoothing responsiveness (0-1, higher = more responsive)."""
        a = max(0.0, min(alpha, 1.0))
        self.ema_x.alpha = a
        self.ema_y.alpha = a
    
    def draw_calibration_interface(self, frame: np.ndarray) -> np.ndarray:
        """
        Draw calibration interface on frame.
        
        Args:
            frame: Input frame to draw on
            
        Returns:
            Frame with calibration interface drawn
        """
        if not self.is_calibrating:
            return frame
        
        # Create fullscreen canvas
        canvas = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)
        
        # Draw all calibration points (gray)
        for i, (norm_x, norm_y) in enumerate(self.calibration_grid):
            x = int(norm_x * self.screen_width)
            y = int(norm_y * self.screen_height)
            
            if i < self.current_point_idx:
                # Completed points (green)
                cv2.circle(canvas, (x, y), 15, (0, 255, 0), -1)
                cv2.circle(canvas, (x, y), 18, (255, 255, 255), 2)
            elif i == self.current_point_idx:
                # Current point (animated red/green)
                progress = self.current_frame_count / self.frames_per_point
                if progress < 0.2:
                    # Red - waiting
                    color = self.point_color
                    radius = 20
                else:
                    # Green - collecting
                    color = self.active_color
                    radius = int(20 + 10 * np.sin(progress * np.pi * 4))
                
                cv2.circle(canvas, (x, y), radius, color, -1)
                cv2.circle(canvas, (x, y), radius + 3, (255, 255, 255), 3)
                
                # Progress circle
                angle = int(360 * progress)
                cv2.ellipse(canvas, (x, y), (35, 35), 0, 0, angle, (255, 255, 0), 3)
                
                # Point number
                cv2.putText(canvas, str(i + 1), (x - 10, y + 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            else:
                # Upcoming points (gray)
                cv2.circle(canvas, (x, y), 12, (128, 128, 128), 2)
                cv2.putText(canvas, str(i + 1), (x - 8, y + 8),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
        
        # Draw instructions
        instructions = [
            f"Calibration: Point {self.current_point_idx + 1}/{len(self.calibration_grid)}",
            f"Progress: {int(self.current_frame_count / self.frames_per_point * 100)}%",
            "Look at the RED dot and keep your head still",
            "Press ESC to cancel"
        ]
        
        y_offset = 50
        for i, text in enumerate(instructions):
            cv2.putText(canvas, text, (50, y_offset + i * 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.text_color, 2)
        
        return canvas
    
    def add_incremental_calibration_point(self, left_iris: Tuple[float, float],
                                          right_iris: Tuple[float, float],
                                          nose_tip: Tuple[float, float],
                                          actual_x: int, actual_y: int):
        """
        Add a single calibration point for incremental recalibration.
        Useful for correcting drift during use.
        
        Args:
            left_iris: Left iris normalized coordinates
            right_iris: Right iris normalized coordinates
            nose_tip: Nose tip normalized coordinates
            actual_x: Actual screen X coordinate where user is looking
            actual_y: Actual screen Y coordinate where user is looking
        """
        # Create new calibration point
        new_point = CalibrationPoint(
            screen_x=actual_x,
            screen_y=actual_y,
            left_iris_x=left_iris[0],
            left_iris_y=left_iris[1],
            right_iris_x=right_iris[0],
            right_iris_y=right_iris[1],
            head_x=nose_tip[0],
            head_y=nose_tip[1],
            timestamp=datetime.now().isoformat()
        )
        
        # Add to calibration data
        self.calibration_data.append(new_point)
        
        print(f"✓ Added incremental calibration point at ({actual_x}, {actual_y})")
        
        # Retrain model with updated data
        self._train_mapping_model()
    
    def save_calibration_data(self, filename: Optional[str] = None):
        """
        Save calibration data and model to files.
        
        Args:
            filename: Optional custom filename for calibration data
        """
        if filename is None:
            filename = self.calibration_file
        
        # Save calibration points as JSON
        try:
            data = {
                'screen_width': self.screen_width,
                'screen_height': self.screen_height,
                'calibration_points': [asdict(p) for p in self.calibration_data],
                'head_baseline_x': self.head_baseline_x,
                'head_baseline_y': self.head_baseline_y,
                'calibration_error': self.calibration_error_pixels,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✓ Calibration data saved to {filename}")
        
        except Exception as e:
            print(f"ERROR saving calibration data: {e}")
        
        # Save trained models as pickle
        try:
            model_data = {
                'x_model': self.x_model,
                'y_model': self.y_model,
                'poly_features': self.poly_features,
                'rbf_x': self.rbf_x,
                'rbf_y': self.rbf_y
            }
            
            with open(self.model_file, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"✓ Calibration models saved to {self.model_file}")
        
        except Exception as e:
            print(f"ERROR saving models: {e}")
    
    def load_calibration_data(self, filename: Optional[str] = None) -> bool:
        """
        Load calibration data and model from files.
        
        Args:
            filename: Optional custom filename for calibration data
            
        Returns:
            True if successful, False otherwise
        """
        if filename is None:
            filename = self.calibration_file
        
        # Check if files exist
        if not os.path.exists(filename) or not os.path.exists(self.model_file):
            print("No saved calibration found. Please calibrate first.")
            return False
        
        # Load calibration data
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Verify screen size matches
            if data['screen_width'] != self.screen_width or data['screen_height'] != self.screen_height:
                print(f"WARNING: Saved calibration is for different screen size!")
                print(f"  Saved: {data['screen_width']}x{data['screen_height']}")
                print(f"  Current: {self.screen_width}x{self.screen_height}")
                print("Please recalibrate for accurate results.")
                return False
            
            # Reconstruct calibration points
            self.calibration_data = [
                CalibrationPoint(**point) for point in data['calibration_points']
            ]
            
            self.head_baseline_x = data.get('head_baseline_x')
            self.head_baseline_y = data.get('head_baseline_y')
            self.calibration_error_pixels = data.get('calibration_error', 0.0)
            
            print(f"✓ Loaded {len(self.calibration_data)} calibration points")
            print(f"  Calibration error: {self.calibration_error_pixels:.2f} pixels")
            print(f"  Calibrated on: {data.get('timestamp', 'Unknown')}")
        
        except Exception as e:
            print(f"ERROR loading calibration data: {e}")
            return False
        
        # Load models
        try:
            with open(self.model_file, 'rb') as f:
                model_data = pickle.load(f)
            
            self.x_model = model_data['x_model']
            self.y_model = model_data['y_model']
            self.poly_features = model_data['poly_features']
            self.rbf_x = model_data.get('rbf_x')
            self.rbf_y = model_data.get('rbf_y')
            
            self.is_calibrated = True
            print(f"✓ Calibration models loaded successfully")
            return True
        
        except Exception as e:
            print(f"ERROR loading models: {e}")
            return False
    
    def get_calibration_quality_metrics(self) -> Dict:
        """
        Calculate and return calibration quality metrics.
        
        Returns:
            Dictionary with quality metrics
        """
        if not self.is_calibrated or len(self.calibration_data) == 0:
            return {}
        
        # Recalculate predictions for all calibration points
        errors = []
        for point in self.calibration_data:
            pred_x, pred_y = self.predict_screen_position(
                (point.left_iris_x, point.left_iris_y),
                (point.right_iris_x, point.right_iris_y),
                (point.head_x, point.head_y),
                use_smoothing=False  # Don't smooth for accuracy measurement
            )
            
            error = np.sqrt((pred_x - point.screen_x)**2 + (pred_y - point.screen_y)**2)
            errors.append(error)
        
        return {
            'mean_error_pixels': np.mean(errors),
            'std_error_pixels': np.std(errors),
            'max_error_pixels': np.max(errors),
            'min_error_pixels': np.min(errors),
            'num_calibration_points': len(self.calibration_data),
            'screen_resolution': f"{self.screen_width}x{self.screen_height}",
            'error_percentage': (np.mean(errors) / np.sqrt(self.screen_width**2 + self.screen_height**2)) * 100
        }
    
    def reset_smoothing_filters(self):
        """Reset all smoothing filters. Call when making sudden movements."""
        self.kalman_x.reset()
        self.kalman_y.reset()
        self.ema_x.reset()
        self.ema_y.reset()


# Example usage and integration
if __name__ == "__main__":
    print("Advanced Calibration System - Test Mode")
    print("=" * 60)
    
    # Initialize calibration system
    cal_system = AdvancedCalibrationSystem(
        screen_width=1920,
        screen_height=1080
    )
    
    # Try to load existing calibration
    if cal_system.load_calibration_data():
        print("\n✓ Using saved calibration")
        metrics = cal_system.get_calibration_quality_metrics()
        print("\nCalibration Quality:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
    else:
        print("\n⚠ No saved calibration found")
        print("Run full calibration with your eye tracking system")
    
    print("\n" + "=" * 60)
    print("Calibration system ready for integration")
