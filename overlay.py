"""
Calibration Overlay (Windows)
----------------------------
Transparent, always-on-top overlay that draws calibration dots at true
screen coordinates during the calibration phase.

Notes:
- Uses Tkinter with a transparent color key on Windows.
- Renders per-frame via .update() (no blocking mainloop).
- If overlay can't be created, caller should gracefully fall back to
  an OpenCV fullscreen window.
"""

import tkinter as tk

try:
    import pyautogui
except Exception:
    pyautogui = None


class CalibrationOverlay:
    def __init__(self):
        # Create root window
        self.root = tk.Tk()
        self.root.title("Calibration Overlay")
        self.root.overrideredirect(True)  # Remove title bar/borders
        self.root.attributes("-topmost", True)

        # Detect screen size
        if pyautogui:
            sw, sh = pyautogui.size()
        else:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
        self.screen_width = sw
        self.screen_height = sh

        # Transparent background color (Windows only)
        self.transparent_color = "magenta"
        try:
            # Fullscreen sized window at (0,0)
            self.root.geometry(f"{sw}x{sh}+0+0")
            # Create a canvas with a solid color we make transparent
            self.canvas = tk.Canvas(self.root, width=sw, height=sh,
                                    highlightthickness=0, bg=self.transparent_color)
            self.canvas.pack(fill=tk.BOTH, expand=True)
            # Make that color transparent
            self.root.wm_attributes("-transparentcolor", self.transparent_color)
        except tk.TclError as e:
            # If transparentcolor not supported, raise to let caller fallback
            self.root.destroy()
            raise RuntimeError(f"Transparent overlay not supported: {e}")

        # Colors and styles
        self.color_completed = "#00FF00"  # Green
        self.color_current_wait = "#FF0000"  # Red
        self.color_upcoming = "#808080"  # Gray
        self.color_ring = "#FFFFFF"  # White outline
        self.color_progress = "#FFFF00"  # Yellow progress arc

        # State
        self._closed = False

        # ESC closes overlay (caller may fallback to OpenCV UI)
        self.root.bind("<Escape>", self._on_esc)

    def _on_esc(self, event=None):
        self.close()

    def render(self, grid, current_idx: int, current_frame_count: int, frames_per_point: int):
        if self._closed:
            raise RuntimeError("Overlay is closed")

        # Clear previous frame
        self.canvas.delete("all")

        # Draw dots
        for i, (norm_x, norm_y) in enumerate(grid):
            x = int(norm_x * self.screen_width)
            y = int(norm_y * self.screen_height)

            if i < current_idx:
                # Completed points (green + ring)
                r = 15
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.color_completed, outline="")
                self.canvas.create_oval(x - (r+3), y - (r+3), x + (r+3), y + (r+3), outline=self.color_ring, width=3)

            elif i == current_idx:
                # Current point: red (waiting) then pulsing green (collecting)
                progress = current_frame_count / max(frames_per_point, 1)
                if progress < 0.2:
                    color = self.color_current_wait
                    r = 20
                else:
                    color = self.color_completed
                    # Pulse radius for feedback
                    import math
                    r = int(20 + 10 * math.sin(progress * 4 * math.pi))

                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")
                self.canvas.create_oval(x - (r+3), y - (r+3), x + (r+3), y + (r+3), outline=self.color_ring, width=3)

                # Progress arc
                extent = int(360 * progress)
                self.canvas.create_arc(x - 35, y - 35, x + 35, y + 35,
                                       start=0, extent=extent, style=tk.ARC,
                                       outline=self.color_progress, width=3)

                # Point index label
                self.canvas.create_text(x, y + 30, text=str(i + 1), fill=self.color_ring, font=("Segoe UI", 12, "bold"))
            else:
                # Upcoming points (gray)
                r = 12
                self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                        outline=self.color_upcoming, width=2)
                self.canvas.create_text(x, y + 20, text=str(i + 1), fill=self.color_upcoming, font=("Segoe UI", 10))

        # Non-blocking refresh
        self.root.update_idletasks()
        self.root.update()

    def close(self):
        if not self._closed:
            try:
                self.root.destroy()
            except Exception:
                pass
            self._closed = True
