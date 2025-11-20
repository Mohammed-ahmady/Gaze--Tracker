"""
Control Window with Live Preview
===============================
Provides a GUI window with camera preview and keyboard control interface.
"""

import cv2
import numpy as np

class ControlWindow:
    def __init__(self, window_name="Eye Tracking Control"):
        """Initialize the control window."""
        self.window_name = window_name
        cv2.namedWindow(window_name)
        
        # Instructions that will be shown on the preview
        self.instructions = [
            "Eye Tracking Controls:",
            "C - Start 9-point calibration",
            "F - Fine 25-point calibration",
            "R - Add single calibration point",
            "S - Toggle cursor control",
            "D - Delete calibration & restart",
            "Z - Reset smoothing filters",
            "Q - Quit application",
            "",
            "Status: Ready"
        ]
        
    def update_preview(self, frame, status_text=None):
        """
        Update the control window with the current frame and status.
        
        Args:
            frame: Current camera frame
            status_text: Optional status message to show
        """
        # Create a copy of the frame to draw on
        display = frame.copy()
        
        # Get frame dimensions
        height, width = display.shape[:2]
        
        # Create semi-transparent overlay for text background
        overlay = display.copy()
        cv2.rectangle(overlay, (10, 10), (300, 220), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, display, 0.5, 0, display)
        
        # Draw instructions
        y = 40
        for line in self.instructions:
            if line == "Status: Ready" and status_text:
                line = f"Status: {status_text}"
            cv2.putText(display, line, (20, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            y += 20
        
        # Show the frame
        cv2.imshow(self.window_name, display)
    
    def get_key(self, delay=1):
        """
        Get keyboard input with timeout.
        
        Args:
            delay: Delay in milliseconds to wait for key
            
        Returns:
            Key pressed as lowercase character, or None if no key pressed
        """
        key = cv2.waitKey(delay) & 0xFF
        if key == 255:  # No key pressed
            return None
        return chr(key).lower()
    
    def close(self):
        """Close the control window."""
        cv2.destroyWindow(self.window_name)