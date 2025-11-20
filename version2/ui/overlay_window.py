"""
Calibration Overlay Window
==========================
Transparent fullscreen overlay for displaying calibration points.

Author: SHA Graduation Project Group 24
"""

import tkinter as tk
from typing import Tuple, List


class CalibrationOverlay:
    """Fullscreen transparent overlay for calibration points."""
    
    def __init__(self):
        """Initialize the calibration overlay."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window
        self.overlay = None
        self.canvas = None
        
    def create_overlay(self):
        """Create fullscreen transparent overlay."""
        if self.overlay is not None:
            return
            
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes('-fullscreen', True)
        self.overlay.attributes('-topmost', True)
        self.overlay.configure(bg='black')
        self.overlay.attributes('-alpha', 0.85)
        
        # Get screen dimensions
        screen_width = self.overlay.winfo_screenwidth()
        screen_height = self.overlay.winfo_screenheight()
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.overlay,
            bg='black',
            highlightthickness=0,
            width=screen_width,
            height=screen_height
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
    def render(self, calibration_grid: List[Tuple[int, int]], 
               current_idx: int, current_frame: int, total_frames: int):
        """
        Render calibration points on overlay.
        
        Args:
            calibration_grid: List of (x, y) screen coordinates
            current_idx: Index of current calibration point
            current_frame: Current frame count for this point
            total_frames: Total frames needed per point
        """
        if self.overlay is None:
            self.create_overlay()
            
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw all calibration points
        for idx, (x, y) in enumerate(calibration_grid):
            if idx == current_idx:
                # Current point - large red circle with pulsing effect
                pulse_size = 30 + int(10 * abs((current_frame % 30) - 15) / 15)
                self.canvas.create_oval(
                    x - pulse_size, y - pulse_size,
                    x + pulse_size, y + pulse_size,
                    fill='red', outline='white', width=3
                )
                
                # Progress ring
                progress = (current_frame / total_frames) * 360
                self.canvas.create_arc(
                    x - 40, y - 40, x + 40, y + 40,
                    start=90, extent=-progress,
                    outline='#00ff00', width=4, style=tk.ARC
                )
                
                # Point number
                self.canvas.create_text(
                    x, y,
                    text=str(idx + 1),
                    fill='white',
                    font=('Arial', 20, 'bold')
                )
                
                # Progress text
                progress_pct = int((current_frame / total_frames) * 100)
                self.canvas.create_text(
                    x, y + 70,
                    text=f"Point {idx + 1}/{len(calibration_grid)} - {progress_pct}%",
                    fill='white',
                    font=('Arial', 14, 'bold')
                )
            else:
                # Other points - small gray circles
                size = 15
                color = '#00ff00' if idx < current_idx else '#555555'
                self.canvas.create_oval(
                    x - size, y - size,
                    x + size, y + size,
                    fill=color, outline='white', width=2
                )
                
                # Point number
                self.canvas.create_text(
                    x, y,
                    text=str(idx + 1),
                    fill='white',
                    font=('Arial', 10, 'bold')
                )
        
        # Instructions at bottom
        screen_height = self.overlay.winfo_screenheight()
        screen_width = self.overlay.winfo_screenwidth()
        
        self.canvas.create_text(
            screen_width // 2, screen_height - 100,
            text="Look at the RED circle and hold your gaze steady",
            fill='white',
            font=('Arial', 18, 'bold')
        )
        
        self.canvas.create_text(
            screen_width // 2, screen_height - 60,
            text="Press ESC to cancel calibration",
            fill='#cccccc',
            font=('Arial', 12)
        )
        
        # Update display
        self.overlay.update()
        
    def close(self):
        """Close the overlay window."""
        try:
            if self.overlay:
                self.overlay.destroy()
                self.overlay = None
            if self.root:
                self.root.destroy()
                self.root = None
        except:
            pass
