"""
Advanced Control Panel for Eye Tracking System
==============================================
Full-featured GUI control window with real-time monitoring and controls.

Author: SHA Graduation Project Group 24
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import queue


class AdvancedControlPanel:
    """Comprehensive control panel with live preview and full controls."""
    
    def __init__(self, title="Eye Tracking Control Panel"):
        """Initialize the advanced control panel."""
        self.title = title
        self.running = True
        self.current_frame = None
        self.status_data = {
            'fps': 0,
            'face_detected': False,
            'calibrated': False,
            'cursor_enabled': True,
            'smoothing_enabled': True,
            'gain': 1.0,
            'cursor_pos': (0, 0),
            'calibration_points': 0,
            'mode': 'Tracking'
        }
        
        # Create main window
        self.root = tk.Tk()
        self.root.title(title)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry("800x700")
        self.root.configure(bg='#2b2b2b')
        
        # Create UI components
        self._create_ui()
        
        # Start update thread
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
        
    def _create_ui(self):
        """Create the user interface."""
        # Title bar
        title_frame = tk.Frame(self.root, bg='#1a1a1a', height=50)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            title_frame, 
            text="🎯 Eye Tracking Control Panel",
            font=("Arial", 16, "bold"),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        title_label.pack(pady=10)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Video preview
        left_panel = tk.Frame(main_frame, bg='#2b2b2b')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        preview_label = tk.Label(left_panel, text="Camera Preview", 
                                 font=("Arial", 12, "bold"), bg='#2b2b2b', fg='white')
        preview_label.pack(pady=(0, 5))
        
        self.video_canvas = tk.Label(left_panel, bg='black', width=480, height=360)
        self.video_canvas.pack()
        
        # Right panel - Controls and status
        right_panel = tk.Frame(main_frame, bg='#2b2b2b', width=280)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Status section
        status_frame = tk.LabelFrame(
            right_panel, 
            text="📊 System Status", 
            font=("Arial", 10, "bold"),
            bg='#2b2b2b',
            fg='white',
            relief=tk.GROOVE,
            borderwidth=2
        )
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_labels = {}
        status_items = [
            ('mode', 'Mode'),
            ('fps', 'FPS'),
            ('face', 'Face Detection'),
            ('calibrated', 'Calibration'),
            ('cursor', 'Cursor Control'),
            ('smoothing', 'Smoothing'),
            ('gain', 'Gain'),
            ('position', 'Cursor Position')
        ]
        
        for key, label in status_items:
            frame = tk.Frame(status_frame, bg='#2b2b2b')
            frame.pack(fill=tk.X, padx=10, pady=3)
            
            tk.Label(frame, text=f"{label}:", font=("Arial", 9), 
                    bg='#2b2b2b', fg='#cccccc', width=15, anchor='w').pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text="--", font=("Arial", 9, "bold"),
                                  bg='#2b2b2b', fg='#00ff00', anchor='w')
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.status_labels[key] = value_label
        
        # Calibration controls
        calib_frame = tk.LabelFrame(
            right_panel,
            text="🎯 Calibration",
            font=("Arial", 10, "bold"),
            bg='#2b2b2b',
            fg='white',
            relief=tk.GROOVE,
            borderwidth=2
        )
        calib_frame.pack(fill=tk.X, pady=(0, 10))
        
        btn_style = {'font': ("Arial", 9), 'width': 25, 'height': 2}
        
        self.btn_calib_9 = tk.Button(
            calib_frame, text="9-Point Calibration (C)", 
            command=lambda: self.send_command('c'), **btn_style,
            bg='#4CAF50', fg='white', activebackground='#45a049'
        )
        self.btn_calib_9.pack(padx=10, pady=5)
        
        self.btn_calib_15 = tk.Button(
            calib_frame, text="15-Point Calibration (F)",
            command=lambda: self.send_command('f'), **btn_style,
            bg='#2196F3', fg='white', activebackground='#1976D2'
        )
        self.btn_calib_15.pack(padx=10, pady=5)
        
        self.btn_add_point = tk.Button(
            calib_frame, text="Add Point (R)",
            command=lambda: self.send_command('r'), **btn_style,
            bg='#FF9800', fg='white', activebackground='#F57C00'
        )
        self.btn_add_point.pack(padx=10, pady=5)
        
        self.btn_delete = tk.Button(
            calib_frame, text="Delete Calibration (D)",
            command=lambda: self.send_command('d'), **btn_style,
            bg='#f44336', fg='white', activebackground='#da190b'
        )
        self.btn_delete.pack(padx=10, pady=5)
        
        # System controls
        system_frame = tk.LabelFrame(
            right_panel,
            text="⚙️ System Controls",
            font=("Arial", 10, "bold"),
            bg='#2b2b2b',
            fg='white',
            relief=tk.GROOVE,
            borderwidth=2
        )
        system_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.btn_toggle_cursor = tk.Button(
            system_frame, text="Toggle Cursor (S)",
            command=lambda: self.send_command('s'), **btn_style,
            bg='#9C27B0', fg='white', activebackground='#7B1FA2'
        )
        self.btn_toggle_cursor.pack(padx=10, pady=5)
        
        self.btn_toggle_smooth = tk.Button(
            system_frame, text="Toggle Smoothing (X)",
            command=lambda: self.send_command('x'), **btn_style,
            bg='#00BCD4', fg='white', activebackground='#0097A7'
        )
        self.btn_toggle_smooth.pack(padx=10, pady=5)
        
        self.btn_toggle_gaze = tk.Button(
            system_frame, text="Toggle Raw Gaze Overlay (G)",
            command=lambda: self.send_command('g'), **btn_style,
            bg='#FFEB3B', fg='black', activebackground='#FDD835'
        )
        self.btn_toggle_gaze.pack(padx=10, pady=5)
        
        self.btn_reset_filters = tk.Button(
            system_frame, text="Reset Filters (Z)",
            command=lambda: self.send_command('z'), **btn_style,
            bg='#607D8B', fg='white', activebackground='#455A64'
        )
        self.btn_reset_filters.pack(padx=10, pady=5)
        
        # Gain adjustment
        gain_frame = tk.Frame(system_frame, bg='#2b2b2b')
        gain_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(gain_frame, text="Gain:", font=("Arial", 9),
                bg='#2b2b2b', fg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(gain_frame, text="-", command=lambda: self.send_command('-'),
                 font=("Arial", 12, "bold"), width=3, bg='#555', fg='white').pack(side=tk.LEFT, padx=2)
        
        tk.Button(gain_frame, text="+", command=lambda: self.send_command('+'),
                 font=("Arial", 12, "bold"), width=3, bg='#555', fg='white').pack(side=tk.LEFT, padx=2)
        
        # Quit button
        self.btn_quit = tk.Button(
            right_panel, text="🚪 Quit (Q)",
            command=lambda: self.send_command('q'), **btn_style,
            bg='#212121', fg='white', activebackground='#000000'
        )
        self.btn_quit.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # Thread-safe command queue
        self.command_queue = queue.Queue()
        
        # Bind keyboard shortcuts
        self.root.bind('<KeyPress>', self._on_key_press)
        
    def _update_loop(self):
        """Update the UI in a separate thread."""
        while self.running:
            try:
                self._update_video()
                self._update_status()
                time.sleep(0.03)  # ~30 FPS
            except Exception as e:
                print(f"UI update error: {e}")
                
    def _update_video(self):
        """Update the video preview."""
        if self.current_frame is not None:
            try:
                # Resize frame to fit canvas
                frame = cv2.resize(self.current_frame, (480, 360))
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                photo = ImageTk.PhotoImage(image=image)
                
                self.video_canvas.configure(image=photo)
                self.video_canvas.image = photo
            except Exception as e:
                pass
                
    def _update_status(self):
        """Update status labels."""
        try:
            self.status_labels['mode'].config(text=self.status_data['mode'])
            self.status_labels['fps'].config(text=str(self.status_data['fps']))
            
            # Face detection
            face_text = "✓ Detected" if self.status_data['face_detected'] else "✗ No Face"
            face_color = '#00ff00' if self.status_data['face_detected'] else '#ff0000'
            self.status_labels['face'].config(text=face_text, fg=face_color)
            
            # Calibration
            calib_text = "✓ Calibrated" if self.status_data['calibrated'] else "✗ Not Calibrated"
            calib_color = '#00ff00' if self.status_data['calibrated'] else '#ff9800'
            self.status_labels['calibrated'].config(text=calib_text, fg=calib_color)
            
            # Cursor control
            cursor_text = "ON" if self.status_data['cursor_enabled'] else "OFF"
            cursor_color = '#00ff00' if self.status_data['cursor_enabled'] else '#ff0000'
            self.status_labels['cursor'].config(text=cursor_text, fg=cursor_color)
            
            # Smoothing
            smooth_text = "ON" if self.status_data['smoothing_enabled'] else "OFF"
            self.status_labels['smoothing'].config(text=smooth_text)
            
            # Gain
            self.status_labels['gain'].config(text=f"{self.status_data['gain']:.2f}")
            
            # Position
            pos = self.status_data['cursor_pos']
            self.status_labels['position'].config(text=f"({pos[0]}, {pos[1]})")
        except Exception as e:
            pass
    
    def update_frame(self, frame):
        """Update the current video frame."""
        self.current_frame = frame
        
    def update_status(self, **kwargs):
        """Update status data."""
        self.status_data.update(kwargs)
        
    def send_command(self, cmd):
        """Add command to queue."""
        try:
            self.command_queue.put(cmd, block=False)
            print(f"Command sent: {cmd}")
        except queue.Full:
            print(f"Command queue full, skipping: {cmd}")
        
    def get_command(self):
        """Get next command from queue."""
        try:
            return self.command_queue.get(block=False)
        except queue.Empty:
            return None
    
    def _on_key_press(self, event):
        """Handle keyboard shortcuts."""
        key = event.char.lower()
        if key in ['c', 'f', 'r', 'd', 's', 'x', 'z', 'q', 'g']:
            self.send_command(key)
        elif event.keysym == 'plus' or key == '+':
            self.send_command('+')
        elif event.keysym == 'minus' or key == '-':
            self.send_command('-')
        
    def on_closing(self):
        """Handle window closing."""
        self.running = False
        self.send_command('q')
        self.root.destroy()
        
    def run(self):
        """Start the GUI main loop (call from main thread)."""
        self.root.mainloop()
        
    def close(self):
        """Close the control panel."""
        self.running = False
        try:
            self.root.destroy()
        except:
            pass
