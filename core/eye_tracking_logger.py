"""
Comprehensive Logging System for Eye Tracking
============================================
Logs all calibration data, predictions, eye positions, and system state.

Author: SHA Graduation Project Group 24
"""

import logging
import json
import csv
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple


class EyeTrackingLogger:
    """Comprehensive logger for eye tracking system."""
    
    def __init__(self, log_dir: str = "logs"):
        """Initialize logger."""
        # Create timestamp for this session
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create session directory
        self.log_dir = Path(log_dir)
        self.session_dir = self.log_dir / f"session_{self.session_id}"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup file paths in session directory
        self.main_log_file = self.session_dir / "session.log"
        self.calibration_log_file = self.session_dir / "calibration.json"
        self.tracking_csv_file = self.session_dir / "tracking.csv"
        self.errors_log_file = self.session_dir / "errors.log"
        self.analysis_file = self.session_dir / "analysis.txt"
        
        # Setup main logger
        self.logger = logging.getLogger('EyeTracking')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(self.main_log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        
        # Calibration data storage
        self.calibration_data = {
            'session_id': self.session_id,
            'start_time': datetime.now().isoformat(),
            'screen_width': 0,
            'screen_height': 0,
            'calibration_points': [],
            'raw_samples': [],
            'model_info': {},
            'training_results': {}
        }
        
        # Tracking data CSV
        self.csv_file = open(self.tracking_csv_file, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow([
            'timestamp', 'frame_count',
            'left_eye_x', 'left_eye_y', 'right_eye_x', 'right_eye_y',
            'avg_eye_x', 'avg_eye_y', 'nose_x', 'nose_y',
            'predicted_x', 'predicted_y', 'smoothed_x', 'smoothed_y',
            'cursor_x', 'cursor_y', 'face_detected',
            'left_ear', 'right_ear', 'blink_detected',
            'smoothing_enabled', 'gain', 'mode'
        ])
        
        # Frame counter
        self.frame_count = 0
        self.calibration_frame_count = 0
        
        # Error tracking
        self.error_logger = logging.getLogger('Errors')
        self.error_logger.setLevel(logging.ERROR)
        eh = logging.FileHandler(self.errors_log_file, encoding='utf-8')
        eh.setFormatter(formatter)
        self.error_logger.addHandler(eh)
        
        self.logger.info("="*80)
        self.logger.info(f"Eye Tracking Session Started - ID: {self.session_id}")
        self.logger.info("="*80)
    
    def log_system_info(self, screen_width: int, screen_height: int, camera_info: Dict[str, Any]):
        """Log system information."""
        self.logger.info(f"Screen Resolution: {screen_width}x{screen_height}")
        self.logger.info(f"Camera Resolution: {camera_info.get('width', 'N/A')}x{camera_info.get('height', 'N/A')}")
        self.logger.info(f"Camera FPS: {camera_info.get('fps', 'N/A')}")
        
        self.calibration_data['screen_width'] = screen_width
        self.calibration_data['screen_height'] = screen_height
        self.calibration_data['camera_info'] = camera_info
    
    def log_calibration_start(self, num_points: int, frames_per_point: int):
        """Log calibration start."""
        self.logger.info("")
        self.logger.info("="*80)
        self.logger.info(f"CALIBRATION STARTED - {num_points} points, {frames_per_point} frames/point")
        self.logger.info("="*80)
        
        self.calibration_data['num_points'] = num_points
        self.calibration_data['frames_per_point'] = frames_per_point
        self.calibration_data['calibration_points'] = []
        self.calibration_data['raw_samples'] = []
        self.calibration_frame_count = 0
    
    def log_calibration_point(self, point_idx: int, screen_x: int, screen_y: int):
        """Log when moving to new calibration point."""
        self.logger.info(f"Calibration Point {point_idx + 1}: Screen({screen_x}, {screen_y})")
        
        self.calibration_data['calibration_points'].append({
            'point_idx': point_idx,
            'screen_x': screen_x,
            'screen_y': screen_y,
            'samples': []
        })
    
    def log_calibration_sample(self, point_idx: int, left_eye: Tuple[float, float],
                               right_eye: Tuple[float, float], nose: Tuple[float, float],
                               screen_x: int, screen_y: int):
        """Log individual calibration sample."""
        self.calibration_frame_count += 1
        
        sample = {
            'frame': self.calibration_frame_count,
            'point_idx': point_idx,
            'left_eye': list(left_eye),
            'right_eye': list(right_eye),
            'nose': list(nose),
            'screen_x': screen_x,
            'screen_y': screen_y,
            'timestamp': datetime.now().isoformat()
        }
        
        self.calibration_data['raw_samples'].append(sample)
        
        if point_idx < len(self.calibration_data['calibration_points']):
            self.calibration_data['calibration_points'][point_idx]['samples'].append(sample)
    
    def log_calibration_complete(self, total_points: int = None, training_error: Dict[str, float] = None):
        """Log calibration completion."""
        self.logger.info("")
        self.logger.info("="*80)
        self.logger.info("CALIBRATION COMPLETE")
        self.logger.info("="*80)
        self.logger.info(f"Total samples collected: {len(self.calibration_data['raw_samples'])}")
        
        if training_error:
            self.logger.info(f"Training Error X: {training_error.get('x', 0):.2f} pixels")
            self.logger.info(f"Training Error Y: {training_error.get('y', 0):.2f} pixels")
            self.calibration_data['training_results'] = training_error
        
        self.logger.info("="*80)
        
        self.calibration_data['end_time'] = datetime.now().isoformat()
        
        # Save calibration data to JSON immediately
        with open(self.calibration_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.calibration_data, f, indent=2)
        
        self.logger.info(f"Calibration data saved to: {self.calibration_log_file}")
    
    def log_tracking_frame(self, data: Dict[str, Any]):
        """Log tracking frame data."""
        self.frame_count += 1
        
        # Write to CSV
        self.csv_writer.writerow([
            datetime.now().isoformat(),
            self.frame_count,
            data.get('left_eye_x', ''),
            data.get('left_eye_y', ''),
            data.get('right_eye_x', ''),
            data.get('right_eye_y', ''),
            data.get('avg_eye_x', ''),
            data.get('avg_eye_y', ''),
            data.get('nose_x', ''),
            data.get('nose_y', ''),
            data.get('predicted_x', ''),
            data.get('predicted_y', ''),
            data.get('smoothed_x', ''),
            data.get('smoothed_y', ''),
            data.get('cursor_x', ''),
            data.get('cursor_y', ''),
            data.get('face_detected', False),
            data.get('left_ear', ''),
            data.get('right_ear', ''),
            data.get('blink_detected', False),
            data.get('smoothing_enabled', True),
            data.get('gain', 1.0),
            data.get('mode', 'tracking')
        ])
        
        # Log every 100 frames to main log
        if self.frame_count % 100 == 0:
            self.logger.info(f"Frame {self.frame_count}: "
                           f"Eye({data.get('avg_eye_x', 0):.3f}, {data.get('avg_eye_y', 0):.3f}) → "
                           f"Screen({data.get('cursor_x', 0)}, {data.get('cursor_y', 0)})")
    
    def log_error(self, error_type: str, message: str, exception: Exception = None):
        """Log error."""
        self.error_logger.error(f"{error_type}: {message}")
        if exception:
            self.error_logger.error(f"Exception: {str(exception)}")
            import traceback
            self.error_logger.error(traceback.format_exc())
        
        self.logger.error(f"{error_type}: {message}")
    
    def log_event(self, event: str, details: str = ""):
        """Log general event."""
        self.logger.info(f"EVENT: {event}" + (f" - {details}" if details else ""))
    
    def analyze_and_save(self):
        """Analyze collected data and save analysis."""
        analysis = []
        analysis.append("="*80)
        analysis.append(f"Eye Tracking Analysis - Session {self.session_id}")
        analysis.append("="*80)
        analysis.append("")
        
        # Calibration analysis
        if self.calibration_data.get('calibration_points'):
            analysis.append("CALIBRATION ANALYSIS:")
            analysis.append("-" * 40)
            
            num_points = len(self.calibration_data['calibration_points'])
            total_samples = len(self.calibration_data['raw_samples'])
            
            analysis.append(f"Calibration Points: {num_points}")
            analysis.append(f"Total Samples: {total_samples}")
            analysis.append(f"Samples per Point: {total_samples // num_points if num_points > 0 else 0}")
            analysis.append("")
            
            # Training results
            if 'training_results' in self.calibration_data:
                tr = self.calibration_data['training_results']
                error_x = tr.get('error_x', None)
                error_y = tr.get('error_y', None)
                
                if error_x is not None:
                    analysis.append(f"Training Error X: {error_x:.2f} px")
                else:
                    analysis.append("Training Error X: N/A")
                    
                if error_y is not None:
                    analysis.append(f"Training Error Y: {error_y:.2f} px")
                else:
                    analysis.append("Training Error Y: N/A")
                    
                analysis.append("")
            
            # Per-point analysis
            analysis.append("Per-Point Variability:")
            for pt in self.calibration_data['calibration_points']:
                samples = pt.get('samples', [])
                if samples:
                    left_x_vals = [s['left_eye'][0] for s in samples]
                    left_y_vals = [s['left_eye'][1] for s in samples]
                    right_x_vals = [s['right_eye'][0] for s in samples]
                    right_y_vals = [s['right_eye'][1] for s in samples]
                    
                    left_x_std = np.std(left_x_vals)
                    left_y_std = np.std(left_y_vals)
                    right_x_std = np.std(right_x_vals)
                    right_y_std = np.std(right_y_vals)
                    
                    analysis.append(f"  Point {pt['point_idx']+1} ({pt['screen_x']}, {pt['screen_y']}): "
                                  f"L_std({left_x_std:.4f}, {left_y_std:.4f}) "
                                  f"R_std({right_x_std:.4f}, {right_y_std:.4f})")
            analysis.append("")
        
        # Tracking analysis
        analysis.append("TRACKING ANALYSIS:")
        analysis.append("-" * 40)
        analysis.append(f"Total tracking frames: {self.frame_count}")
        analysis.append("")
        
        # Recommendations
        analysis.append("RECOMMENDATIONS:")
        analysis.append("-" * 40)
        
        if 'training_results' in self.calibration_data:
            error_x = self.calibration_data['training_results'].get('error_x', 0)
            error_y = self.calibration_data['training_results'].get('error_y', 0)
            
            if error_x > 50 or error_y > 50:
                analysis.append("⚠ HIGH TRAINING ERROR - Calibration quality is poor!")
                analysis.append("  - Head may have moved during calibration")
                analysis.append("  - Distance from camera may have changed")
                analysis.append("  - Lighting may have been inconsistent")
                analysis.append("  → Recommendation: Recalibrate with stable head position")
            elif error_x > 30 or error_y > 30:
                analysis.append("⚠ MODERATE TRAINING ERROR - Calibration could be better")
                analysis.append("  → Recommendation: Consider recalibrating")
            else:
                analysis.append("✓ GOOD TRAINING ERROR - Calibration quality is acceptable")
            
            if error_y > error_x * 1.5:
                analysis.append("⚠ VERTICAL ERROR >> HORIZONTAL ERROR")
                analysis.append("  - Model struggling with vertical mapping")
                analysis.append("  - You may not be looking at top/bottom points during calibration")
                analysis.append("  → Recommendation: Focus more on top and bottom edge points")
        
        analysis.append("")
        analysis.append("="*80)
        analysis.append(f"Log files saved in: {self.session_dir.absolute()}")
        analysis.append(f"  - Main log: {self.main_log_file.name}")
        analysis.append(f"  - Calibration: {self.calibration_log_file.name}")
        analysis.append(f"  - Tracking CSV: {self.tracking_csv_file.name}")
        analysis.append(f"  - Errors: {self.errors_log_file.name}")
        analysis.append("="*80)
        
        # Save analysis
        with open(self.analysis_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(analysis))
        
        self.logger.info("")
        self.logger.info('\n'.join(analysis))
        
        return '\n'.join(analysis)
    
    def close(self):
        """Close logger and save analysis."""
        # Save calibration data to JSON
        if self.calibration_data.get('raw_samples'):
            with open(self.calibration_log_file, 'w', encoding='utf-8') as f:
                json.dump(self.calibration_data, f, indent=2)
        
        self.csv_file.close()
        
        # Generate and save analysis
        analysis = self.analyze_and_save()
        
        self.logger.info("")
        self.logger.info("="*80)
        self.logger.info(f"Session Ended - Total Frames: {self.frame_count}")
        self.logger.info("="*80)
        
        print("\n" + "="*80)
        print(f"📊 ANALYSIS SAVED TO: {self.analysis_file}")
        print("="*80)
        print(analysis)
        
        # Close handlers
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)
        
        for handler in self.error_logger.handlers[:]:
            handler.close()
            self.error_logger.removeHandler(handler)
