"""
Raw Gaze Overlay - Liquid Visual Indicator
=========================================
Shows raw eye gaze position with liquid-like visual effect.

Author: SHA Graduation Project Group 24
"""

import cv2
import numpy as np
from collections import deque
from typing import Tuple


class RawGazeOverlay:
    """Liquid-effect overlay showing raw gaze position."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize raw gaze overlay."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Trail effect (liquid motion)
        self.trail_length = 15
        self.gaze_trail = deque(maxlen=self.trail_length)
        
        # Liquid blob parameters
        self.blob_base_radius = 30
        self.pulse_speed = 0.1
        self.pulse_phase = 0
        
        # Transparency
        self.alpha = 0.7
        
        # Color gradient (cyan to blue)
        self.color_start = np.array([255, 255, 0])  # Cyan
        self.color_end = np.array([255, 100, 0])    # Blue
        
    def update(self, raw_x: float, raw_y: float):
        """
        Update gaze position.
        
        Args:
            raw_x: Raw horizontal gaze ratio (0-1)
            raw_y: Raw vertical gaze ratio (0-1)
        """
        # Convert ratio to screen coordinates
        screen_x = int(raw_x * self.screen_width)
        screen_y = int(raw_y * self.screen_height)
        
        # Clamp to screen bounds
        screen_x = max(0, min(self.screen_width - 1, screen_x))
        screen_y = max(0, min(self.screen_height - 1, screen_y))
        
        # Add to trail
        self.gaze_trail.append((screen_x, screen_y))
        
        # Update pulse animation
        self.pulse_phase += self.pulse_speed
        if self.pulse_phase > 2 * np.pi:
            self.pulse_phase = 0
    
    def _draw_liquid_blob(self, overlay: np.ndarray, x: int, y: int, 
                          radius: float, opacity: float, color: np.ndarray):
        """Draw a single liquid blob with gradient."""
        # Create gradient effect
        for r in range(int(radius), 0, -2):
            ratio = r / radius
            current_opacity = int(opacity * 255 * ratio)
            current_color = tuple(map(int, color * ratio))
            
            cv2.circle(overlay, (x, y), r, current_color, -1)
    
    def render(self) -> np.ndarray:
        """
        Render the liquid gaze overlay.
        
        Returns:
            BGR overlay image (black background with colored blob)
        """
        # Create black canvas
        overlay = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)
        
        if len(self.gaze_trail) == 0:
            return overlay
        
        # Draw trail with fading effect
        for i, (x, y) in enumerate(self.gaze_trail):
            # Calculate trail properties
            trail_ratio = i / len(self.gaze_trail)  # 0 (oldest) to 1 (newest)
            
            # Fade older positions
            opacity = trail_ratio * 0.6  # Max 60% for trail
            radius = int(self.blob_base_radius * (0.3 + trail_ratio * 0.7))
            
            # Color gradient along trail (BGR format)
            color = self.color_start * (1 - trail_ratio) + self.color_end * trail_ratio
            color_bgr = tuple(map(int, color))
            
            # Draw trail blob with decreasing intensity
            for r in range(radius, 0, -3):
                r_ratio = r / radius
                intensity = opacity * r_ratio
                trail_color = tuple(int(c * intensity) for c in color_bgr)
                cv2.circle(overlay, (x, y), r, trail_color, -1)
        
        # Draw current position with pulse effect
        if len(self.gaze_trail) > 0:
            current_x, current_y = self.gaze_trail[-1]
            
            # Pulsing radius
            pulse = np.sin(self.pulse_phase)
            pulse_radius = int(self.blob_base_radius * (1.0 + pulse * 0.3))
            
            # Outer glow (larger, more transparent)
            glow_radius = int(pulse_radius * 1.8)
            for r in range(glow_radius, pulse_radius, -4):
                r_ratio = (r - pulse_radius) / (glow_radius - pulse_radius)
                intensity = 0.3 * (1 - r_ratio)
                glow_color = (int(255 * intensity), int(200 * intensity), 0)
                cv2.circle(overlay, (current_x, current_y), r, glow_color, -1)
            
            # Main blob (cyan/yellow bright)
            for r in range(pulse_radius, 0, -2):
                r_ratio = r / pulse_radius
                intensity = r_ratio * 0.7 + 0.3
                blob_color = (int(255 * intensity), int(255 * intensity), 0)
                cv2.circle(overlay, (current_x, current_y), r, blob_color, -1)
            
            # Center highlight (white core)
            core_radius = max(3, int(pulse_radius * 0.3))
            cv2.circle(overlay, (current_x, current_y), core_radius, (255, 255, 255), -1)
            
            # Outer ring (white)
            ring_thickness = max(2, int(pulse_radius * 0.1))
            cv2.circle(overlay, (current_x, current_y), pulse_radius, (255, 255, 255), ring_thickness)
        
        return overlay
    
    def reset(self):
        """Clear the gaze trail."""
        self.gaze_trail.clear()
        self.pulse_phase = 0
