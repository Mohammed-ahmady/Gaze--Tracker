# Version 1 - User Manual
## Basic Eye Tracking System

### Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Getting Started](#getting-started)
5. [Calibration Process](#calibration-process)
6. [Using the System](#using-the-system)
7. [Advanced Settings](#advanced-settings)


---

## Introduction

Welcome to the Basic Eye Tracking System (Version 1). This system allows you to control your computer's mouse cursor using only your eye movements, with blink detection for clicking.

**What it does:**
- Tracks your eye movements to control the cursor
- Detects blinks for mouse clicks
- Provides voice-guided calibration
- Works with any standard webcam

**What you need:**
- A working webcam
- Python 3.8 or higher
- About 5 minutes for initial setup

---

## System Requirements

### Minimum Requirements
- **Operating System:** Windows 10/11, Linux, or Mac OS
- **Python:** Version 3.8 or higher
- **RAM:** 4GB minimum
- **Webcam:** Any USB or built-in webcam (720p minimum)
- **Processor:** Dual-core CPU
- **Screen:** Any resolution supported

### Recommended Setup
- **RAM:** 8GB or more
- **Webcam:** 1080p for better accuracy
- **Processor:** Quad-core CPU
- **Lighting:** Desk lamp or good natural light

---

## Installation Guide

### Step 1: Check Python Installation
Open a terminal/command prompt and run:
```bash
python --version
```
You should see Python 3.8 or higher. If not, download from [python.org](https://www.python.org).

### Step 2: Navigate to Version 1 Folder
```bash
cd path/to/GazeAssistsudo/version1
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- OpenCV (computer vision)
- MediaPipe (face tracking)
- PyAutoGUI (cursor control)
- NumPy (calculations)
- pyttsx3 (text-to-speech)
- Pillow (image processing)

**Installation time:** 2-5 minutes depending on internet speed.

### Step 4: Verify Installation
```bash
python -c "import cv2, mediapipe, pyautogui; print('Installation successful!')"
```

If you see "Installation successful!", you're ready to go!

---

## Getting Started

### First Time Setup

1. **Position Your Camera:**
   - Place camera at eye level
   - Sit 30-50 cm (12-20 inches) from screen
   - Ensure your face is well-lit
   - Avoid backlighting (don't sit with window behind you)

2. **Test Your Camera:**
   Run this quick test:
   ```bash
   python -c "import cv2; cap = cv2.VideoCapture(0); ret, frame = cap.read(); print('Camera OK' if ret else 'Camera FAILED'); cap.release()"
   ```

3. **Run the Program:**
   ```bash
   python main.py
   ```

### What Happens on First Run

1. **Window Opens:** A debug window shows your camera feed
2. **Voice Guidance:** You'll hear "Starting eye tracking calibration..."
3. **Calibration Begins:** A fullscreen black window with 9 red dots appears
4. **Follow Instructions:** Voice will guide you through each calibration point

---

## Calibration Process

### Understanding Calibration

Calibration teaches the system where you're looking. It maps your eye positions to screen locations.

### The 9 Calibration Points

Points are numbered 1-9 in this pattern:
```
1 ---- 2 ---- 3
|      |      |
4 ---- 5 ---- 6
|      |      |
7 ---- 8 ---- 9
```

### Step-by-Step Calibration

**Before You Start:**
- Sit comfortably in your normal working position
- Keep your head still (don't move it during calibration)
- Only move your EYES, not your head

**During Calibration:**

1. **Point 1 appears** (top-left corner, RED)
   - Voice says: "Please look at the top left dot, number 1"
   - Look DIRECTLY at the red dot
   - Keep looking at it for 2 seconds
   - Dot automatically moves to next position

2. **Point 2-9 repeat** the same process
   - Each point turns red when active
   - Previous points turn gray
   - Voice announces each point
   - Progress shown: "Progress: 30/60 frames"

3. **Calibration Complete:**
   - Voice says: "Calibration complete. You can now control the mouse with your eyes."
   - Debug window shrinks to normal size
   - You can now control the cursor!

### Tips for Accurate Calibration

✅ **DO:**
- Keep head completely still
- Look DIRECTLY at the center of each dot
- Move eyes to EXTREME positions at corners
- Wait for the voice prompt before moving eyes
- Blink normally between points

❌ **DON'T:**
- Move your head
- Look near the dot instead of at it
- Rush through points
- Change your sitting position
- Adjust the camera mid-calibration

### Recalibration

The system saves your calibration. But you should recalibrate if:
- You moved the camera
- You changed your sitting position
- Accuracy has decreased
- Different lighting conditions
- Different user

To recalibrate: Close the program and restart it (calibration runs on each start).

---

## Using the System

### Basic Controls

Once calibrated:

1. **Move Cursor:**
   - Just look where you want the cursor to go
   - Cursor follows your gaze with smooth movement

2. **Click:**
   - **Blink LEFT eye only** (keep right eye open)
   - System performs a left-click

3. **Toggle Debug Window:**
   - **Blink 3 times rapidly** to switch between fullscreen and normal window

4. **Exit:**
   - **Close both eyes for 1 second**, OR
   - **Press ESC key**

### Understanding the Debug Window

The debug window shows:
- **Live camera feed** (mirrored)
- **Green dots:** Eye landmarks
- **Blue dots:** Iris landmarks
- **Text overlay:** Eye Aspect Ratio (EAR) values

**EAR Values:**
- Normal (eyes open): ~0.25-0.35
- Blinking: <0.20
- System triggers click when left EAR <0.20

### Best Practices

**For Smooth Tracking:**
- Keep head relatively still
- Make deliberate eye movements
- Don't move eyes too quickly
- Look where you want to go

**For Accurate Clicks:**
- Blink deliberately with left eye
- Keep right eye open
- Don't blink too rapidly
- Wait 0.5 seconds between clicks (cooldown period)

**For Long Sessions:**
- Take breaks every 20 minutes
- Recalibrate if accuracy drops
- Ensure consistent lighting
- Stay in same seated position

---

## Troubleshooting

### Problem: "Camera FAILED" error

**Symptoms:** Program won't start, camera error message

**Solutions:**
1. Check camera is connected and working
2. Close other programs using camera (Zoom, Skype, etc.)
3. Try different camera index:
   - Edit `main.py`
   - Change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`
4. Check camera permissions in OS settings

---

### Problem: Cursor is shaky/jittery

**Symptoms:** Cursor jumps around, not smooth

**Solutions:**
1. **Improve lighting:**
   - Add a desk lamp
   - Avoid harsh shadows on face
   - Ensure even lighting

2. **Adjust smoothing:**
   - Edit `main.py`
   - Find line: `self.smooth_window = 15`
   - Increase to `20` or `25` for smoother movement
   - Higher = smoother but slower response

3. **Check camera quality:**
   - Clean camera lens
   - Ensure camera is in focus
   - Try better webcam if available

---

### Problem: Can't reach screen edges/corners

**Symptoms:** Cursor won't go to far left/right/top/bottom

**Solutions:**
1. **Recalibrate with better technique:**
   - During calibration, look at EXTREME positions
   - Feel your eyes strain to reach corners
   - Look BEYOND the dots, not just at them

2. **Adjust sensitivity:**
   - Edit `main.py`
   - Find lines: `sensitivity_x = 1.2` and `sensitivity_y = 1.2`
   - Increase to `1.5` or `1.8`
   - Higher = more cursor movement per eye movement

3. **Check camera position:**
   - Move camera closer to eye level
   - Ensure face is centered in view

---

### Problem: Blink clicks not working

**Symptoms:** Blinking doesn't trigger clicks

**Solutions:**
1. **Blink more deliberately:**
   - Close left eye completely
   - Keep right eye open
   - Hold for 0.2 seconds

2. **Adjust threshold:**
   - Edit `main.py`
   - Find line: `self.blink_threshold = 0.2`
   - Increase to `0.25` or `0.3` (easier to trigger)

3. **Check debug window:**
   - Watch "Left EAR" value
   - Should drop below threshold when blinking
   - If not, increase threshold

---

### Problem: Too many false clicks

**Symptoms:** Clicks happen when not blinking

**Solutions:**
1. **Adjust threshold:**
   - Edit `main.py`
   - Find line: `self.blink_threshold = 0.2`
   - Decrease to `0.15` or `0.18` (harder to trigger)

2. **Adjust cooldown:**
   - Edit `main.py`
   - Find line: `self.blink_cooldown = 0.5`
   - Increase to `1.0` (more time between clicks)

---

### Problem: Low FPS / Laggy

**Symptoms:** Debug window shows <20 FPS, slow response

**Solutions:**
1. **Close other applications**
2. **Reduce smoothing:**
   - Change `self.smooth_window` from `15` to `7`
3. **Lower camera resolution:**
   - Edit `main.py`
   - Add after camera initialization:
     ```python
     self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
     self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
     ```

---

### Problem: "ModuleNotFoundError"

**Symptoms:** Program won't start, missing package error

**Solutions:**
```bash
pip install -r requirements.txt --force-reinstall
```

If specific package missing:
```bash
pip install opencv-python mediapipe pyautogui numpy pyttsx3
```

---

## Advanced Settings

### Adjusting Parameters

All settings are in `main.py`. Search for these variables:

#### Smoothing
```python
self.smooth_window = 15        # Moving average window (7-25)
self.smooth_factor = 0.3       # Exponential smoothing (0.1-0.5)
```

#### Sensitivity
```python
sensitivity_x = 1.2            # Horizontal sensitivity (0.8-2.0)
sensitivity_y = 1.2            # Vertical sensitivity (0.8-2.0)
```

#### Blink Detection
```python
self.blink_threshold = 0.2     # Blink trigger threshold (0.15-0.3)
self.blink_cooldown = 0.5      # Time between clicks (0.3-1.0)
self.MIN_BLINK_TIME = 0.15     # Minimum blink duration
self.EXIT_BLINK_TIME = 1.0     # Both eyes closed duration to exit
```

#### Calibration
```python
self.frames_per_point = 60     # Frames per calibration point (30-90)
```

### Camera Settings

```python
self.cap = cv2.VideoCapture(0) # Camera index (0, 1, 2...)
self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
self.cap.set(cv2.CAP_PROP_FPS, 30)
```

---

## FAQ

### Q: How accurate is the cursor control?
**A:** Typically ±50 pixels after good calibration. Accuracy improves with practice and proper setup.

### Q: Can I use this for gaming?
**A:** Not recommended. The system is designed for productivity tasks, not rapid movements required in games.

### Q: Does it work with glasses?
**A:** Yes, but accuracy may be reduced by 10-20%. Remove glasses for best results if possible.

### Q: How long does calibration take?
**A:** About 20-30 seconds for all 9 points.

### Q: Can multiple people use it?
**A:** Each person needs their own calibration. Calibration is saved, so you don't need to recalibrate each time.

### Q: What if my head moves slightly?
**A:** Small movements (±2-3cm) are tolerated. Large movements require recalibration.

### Q: Can I use it lying down?
**A:** Not recommended. The system works best with upright seated position.

### Q: Does it drain battery?
**A:** Moderate CPU usage (~30-40%). Comparable to a video call application.

### Q: Is my camera data saved?
**A:** No. All processing is local. No video or images are saved.

### Q: Can I right-click or drag?
**A:** Version 1 only supports left-click. See Version 2 for advanced features.

---

## Support

If you encounter issues not covered here:

1. **Check requirements:** Ensure all dependencies installed
2. **Recalibrate:** Many issues solved by fresh calibration
3. **Check camera:** Test with another webcam application
4. **Review code:** Comments in `main.py` explain each section
5. **Compare with Version 2:** Enhanced version has better accuracy

---

## Keyboard Shortcuts Summary

| Key/Action | Function |
|------------|----------|
| Left eye blink | Left click |
| Both eyes closed (1s) | Exit program |
| 3 rapid blinks | Toggle fullscreen/normal window |
| ESC | Force exit |

---

**Version:** 1.0 (Basic)  
**Author:** SHA Graduation Project Group 24  
**Academic Year:** 2025/2026
