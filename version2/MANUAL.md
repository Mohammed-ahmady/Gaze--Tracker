# Version 2 - User Manual
## Enhanced Eye Tracking System

### Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Quick Start Guide](#quick-start-guide)
5. [Setup Wizard](#setup-wizard)
6. [Calibration Process](#calibration-process)
7. [Control Panel](#control-panel)
8. [Advanced Features](#advanced-features)
9. [Diagnostic Tools](#diagnostic-tools)
10. [Troubleshooting](#troubleshooting)
11. [Performance Optimization](#performance-optimization)
12. [FAQ](#faq)

---

## Introduction

Welcome to the Enhanced Eye Tracking System (Version 2). This advanced system uses machine learning to provide highly accurate eye-controlled cursor movement with comprehensive logging and diagnostic tools.

### Key Improvements Over Version 1
- ✅ **21-point calibration** (vs 9-point) for better edge coverage
- ✅ **Machine learning** (Ridge Regression) instead of simple ratio mapping
- ✅ **10 engineered features** (vs 2) for better accuracy
- ✅ **Advanced smoothing** with outlier detection
- ✅ **Professional control panel** with live video feed
- ✅ **Comprehensive logging** for analysis and debugging
- ✅ **Diagnostic tools** to verify calibration quality
- ✅ **Adjustable gain** and real-time parameter control

### What's New
- **Setup Wizard:** Interactive pre-calibration guide
- **Raw Gaze Overlay:** Debug view showing raw eye positions
- **Session Logging:** Every frame logged for analysis
- **Training Error Metrics:** Know how good your calibration is
- **Analysis Tools:** Automated reports on tracking quality

---

## System Requirements

### Minimum Requirements
- **Operating System:** Windows 10/11, Linux, or Mac OS
- **Python:** Version 3.8 or higher
- **RAM:** 8GB minimum
- **Webcam:** 720p minimum (1080p recommended)
- **Processor:** Quad-core CPU recommended
- **Disk Space:** 500MB for logs and data

### Recommended Setup
- **RAM:** 16GB for smooth operation
- **Webcam:** 1080p 30fps webcam
- **Processor:** Multi-core CPU (i5/Ryzen 5 or better)
- **Display:** 1920x1080 or higher
- **Lighting:** Adjustable desk lamp

### Software Dependencies
- Python 3.8+
- OpenCV 4.8+
- MediaPipe 0.10+
- scikit-learn 1.3+
- NumPy 1.24+
- See `requirements.txt` for complete list

---

## Installation Guide

### Step 1: Verify Python Installation
```bash
python --version
```
Should show Python 3.8 or higher.

### Step 2: Navigate to Version 2 Directory
```bash
cd path/to/GazeAssistsudo/version2
```

### Step 3: Install All Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- **OpenCV:** Computer vision processing
- **MediaPipe:** Face mesh and iris tracking
- **scikit-learn:** Machine learning (Ridge Regression)
- **NumPy/SciPy:** Numerical computations
- **PyAutoGUI:** Cursor control
- **Pillow:** Image processing for GUI
- **pandas/matplotlib:** (Optional) For advanced log analysis

**Installation time:** 3-7 minutes depending on internet speed.

### Step 4: Verify Installation
```bash
python -c "import cv2, mediapipe, numpy, sklearn; print('All packages OK')"
```

### Step 5: Test Camera
```bash
python -c "import cv2; cap = cv2.VideoCapture(0); ret, _ = cap.read(); cap.release(); print('Camera OK' if ret else 'Camera FAILED')"
```

---

## Quick Start Guide

### For Impatient Users

1. **Run the program:**
   ```bash
   python enhanced_tracker.py
   ```

2. **Setup Wizard appears:**
   - Click "Next" through instructions
   - Position yourself correctly
   - Click "Start Calibration"

3. **Calibration:**
   - Black screen with 21 red numbered dots appears
   - Look at each red dot for 2 seconds
   - **IMPORTANT:** Look at EXTREME positions, feel eye strain
   - Wait for all 21 points to complete

4. **Control Panel opens:**
   - Shows live camera feed
   - Eyes now control cursor
   - Left eye blink = Click

5. **Using the system:**
   - Look where you want to go
   - Blink left eye to click
   - Press 'Q' to quit

### First-Time Setup (Detailed)

Follow the [Setup Wizard](#setup-wizard) section for step-by-step guidance.

---

## Setup Wizard

The Setup Wizard runs automatically on first launch if no calibration exists.

### Page 1: Welcome
- **Message:** Introduction to the system
- **Action:** Click "Next"

### Page 2: Camera Position
**Instructions shown:**
- Position camera at eye level
- Maintain 40-60 cm distance
- Ensure good lighting on face
- Avoid backlighting

**Visual Guide:**
```
        [Camera]
           ↕
        40-60 cm
           ↕
      Your Eyes 👀
```

**Action:** Adjust setup, then click "Next"

### Page 3: Lighting Check
**Instructions shown:**
- Check face is well-lit
- No harsh shadows
- Consistent lighting
- Avoid direct sunlight

**Checklist:**
- ✅ Face clearly visible
- ✅ No shadows on eyes
- ✅ Even lighting
- ✅ No glare on glasses (if wearing)

**Action:** Adjust lighting, then click "Next"

### Page 4: Test Detection
**Shows:**
- Live camera feed
- Face detection status
- Iris tracking status

**What to verify:**
- Green box around face = Face detected ✅
- Blue dots on iris = Iris tracked ✅
- Smooth tracking as you move eyes

**Action:** Verify detection works, then click "Next"

### Page 5: Ready for Calibration
**Final checklist:**
- ✅ Comfortable seated position
- ✅ Head will stay still
- ✅ Only eyes will move
- ✅ Ready for 21 calibration points

**Action:** Click "Start Calibration" when ready

### Skipping Setup Wizard
Press **ESC** to skip and go straight to calibration.

---

## Calibration Process

### Understanding 21-Point Calibration

Unlike Version 1's 9 points, Version 2 uses 21 points strategically placed:

**Layout:**
```
Row 1 (y=0.05):  1 ---- 2 ---- 3 ---- 4 ---- 5
Row 2 (y=0.30):  6 ------ 7 ------ 8
Row 3 (y=0.50):  9 --- 10 --- 11 --- 12 --- 13
Row 4 (y=0.70): 14 ----- 15 ----- 16
Row 5 (y=0.95): 17 --- 18 --- 19 --- 20 --- 21
```

**Why 21 points?**
- **Better edge coverage:** 12 points on screen edges
- **Corner accuracy:** 4 extreme corner points
- **Edge weighting:** System gives corners 9× importance
- **Vertical coverage:** 5 rows prevent vertical tracking issues

### Step-by-Step Calibration

**BEFORE Starting:**
1. Sit in your normal working position
2. Get comfortable (you'll be here a while)
3. Position head upright, centered
4. Take a deep breath and relax

**During Calibration:**

1. **Black screen appears** with all 21 dots visible
   - Current point is RED and large
   - Previous points turn gray
   - Point number shown below each dot

2. **For each point:**
   - **Look DIRECTLY at the red dot** (not near it, AT it)
   - **Hold gaze steady** for full 2 seconds
   - **Move eyes to EXTREME positions** at corners/edges
   - Progress shown: "Progress: 45/60 frames"
   - Instruction text at bottom: "Look at the top left dot #1"

3. **Point transitions automatically:**
   - No need to click or press anything
   - Brief pause between points
   - System collects 60 frames per point

4. **Critical for corners (1, 5, 17, 21):**
   - These are EXTREME positions
   - Feel your eyes strain
   - Look BEYOND the dot if possible
   - These receive 9× weight in training

5. **Critical for edges (2-4, 6, 8, 14, 16, 18-20):**
   - Look at extreme top/bottom/left/right
   - These receive 5× weight in training
   - Better here = better overall accuracy

6. **Center points (7, 10-13, 15):**
   - Easier, more comfortable
   - Still look directly at the dot

7. **Calibration completes:**
   - Black screen closes
   - Control panel opens
   - Message: "✓ Calibration complete!"
   - Training errors displayed in console

### What Happens During Calibration

**Data Collection (Per Point):**
- 60 frames collected
- Each frame captures:
  - Left iris position (x, y)
  - Right iris position (x, y)
  - Nose tip position (x, y)
  - 10 engineered features total

**After Collection:**
- All 21 points × 60 frames = 1,260 data samples
- Edge weighting applied:
  - Corners (1, 5, 17, 21): ×9 = 540 effective samples each
  - Edges (2-4, 6, 8, 14, 16, 18-20): ×5 = 300 effective samples each
  - Center (others): ×1 = 60 samples each
- **Machine learning training:**
  - Features transformed to polynomial degree 3
  - Ridge Regression (α=0.01) fitted
  - Model learns eye → screen mapping

**Training Error:**
- Calculated on training data
- Displayed in console: "Training Error: X=25.3px, Y=18.7px"
- **Target:** <40px both X and Y
- **Good:** <30px
- **Excellent:** <20px

### Calibration Tips for Best Results

✅ **CRITICAL - Do This:**
1. **Look at EXTREMES:** Feel your eyes strain at corners
2. **Hold gaze steady:** Don't drift during the 2 seconds
3. **Look DIRECTLY at dots:** Not near them, AT them
4. **Keep head STILL:** Tape a mark on desk if needed
5. **Good lighting:** Even, bright lighting on face

❌ **CRITICAL - Don't Do This:**
1. ❌ Moving your head instead of eyes
2. ❌ Looking "near" the point instead of "at" it
3. ❌ Not moving eyes far enough to extremes
4. ❌ Changing position mid-calibration
5. ❌ Rushing through points

### Verifying Calibration Quality

**Check Console Output:**
```
✓ Calibration complete!
Training Error: X=23.4px, Y=19.2px
```

**Interpretation:**
- X < 40px, Y < 40px = **Good** ✅
- X < 30px, Y < 30px = **Very Good** ✅✅
- X < 20px, Y < 20px = **Excellent** ✅✅✅
- X > 50px or Y > 50px = **Poor** ❌ (recalibrate)

**Run Deep Analysis:**
```bash
python scripts/deep_analysis.py
```

**Look for:**
- Vertical eye range: >0.4 ✅
- Horizontal eye range: >0.5 ✅
- If ranges <0.3: Camera detection issue or insufficient eye movement

---

## Control Panel

The Advanced Control Panel opens after calibration.

### Panel Layout

```
╔════════════════════════════════════════╗
║  Eye Tracking Control Panel            ║
╠════════════════════════════════════════╣
║  [Live Camera Feed]                    ║
║  320x240 pixels                        ║
║  Shows iris tracking in real-time     ║
╠════════════════════════════════════════╣
║  Status Information:                   ║
║  FPS: 28                              ║
║  Mode: Tracking                       ║
║  Face: Detected ✓                     ║
║  Calibrated: Yes (21 points)          ║
║  Cursor: 1024, 768                    ║
║  Gain: 1.00                           ║
║  Smoothing: Enabled                   ║
╠════════════════════════════════════════╣
║  [Controls Help Button]               ║
╚════════════════════════════════════════╝
```

### Status Indicators

**FPS (Frames Per Second):**
- **25-30:** Excellent ✅
- **20-24:** Good ✅
- **15-19:** Acceptable ⚠️
- **<15:** Poor ❌ (check performance)

**Face Detection:**
- **Detected ✓:** Green, system working
- **Not Detected ✗:** Red, move into view

**Calibrated:**
- **Yes (21 points):** Ready to track
- **No:** Need to calibrate

**Cursor Position:**
- Shows current predicted cursor location
- Updates in real-time

**Gain:**
- Current sensitivity multiplier
- Default: 1.00
- Range: 0.5 - 2.0

**Smoothing:**
- **Enabled:** Smooth cursor movement
- **Disabled:** Raw predictions (jerky but responsive)

### Camera Feed Display

The live camera feed shows:
- **Your face** (mirrored)
- **Green dots:** Iris landmarks (real-time tracking)
- **Smooth tracking:** Dots should follow eyes smoothly

**What to watch for:**
- Green dots stable = good tracking ✅
- Green dots jumping = poor lighting or detection ❌
- No green dots = face not detected ❌

---

## Advanced Features

### Feature 1: Raw Gaze Overlay

**Activate:** Press **G** key

**What it shows:**
- Fullscreen transparent overlay
- **Green crosshair:** Current raw eye position (before smoothing)
- **Trail:** Recent eye positions (fading)
- **Coordinate display:** Raw x, y values

**Use cases:**
- Debug calibration accuracy
- See raw eye detection quality
- Verify smooth eye movement tracking
- Compare smoothed vs raw cursor

**Controls:**
- **G:** Toggle on/off
- **ESC:** Close overlay

---

### Feature 2: Adjustable Gain

**Purpose:** Fine-tune cursor sensitivity

**Controls:**
- **+ or =:** Increase gain by 0.1
- **- or _:** Decrease gain by 0.1

**Current gain shown in control panel**

**How it works:**
- Gain = 1.0: Normal sensitivity
- Gain = 1.5: 50% more sensitive (cursor moves farther)
- Gain = 0.7: 30% less sensitive (cursor moves less)

**When to adjust:**
- Can't reach edges: Increase gain
- Overshooting targets: Decrease gain
- Personal preference

**Recommended range:** 0.8 - 1.3

---

### Feature 3: Toggle Smoothing

**Activate:** Press **X** key

**States:**
- **Enabled (default):** Smooth cursor movement, slight lag
- **Disabled:** Direct predictions, jerky but instant

**Status shown in control panel**

**When to disable:**
- Testing raw model accuracy
- Debugging calibration
- Prefer responsive over smooth

**When to enable:**
- Normal usage
- Reading/browsing
- Drawing/design work

---

### Feature 4: Reset Smoothing Filters

**Activate:** Press **Z** key

**What it does:**
- Clears smoothing buffer (7-frame deque)
- Resets outlier detection
- Starts fresh tracking state

**When to use:**
- After big head movement
- Cursor seems "stuck" on old position
- After changing gain
- Tracking feels sluggish

**Effect:** Immediate response to next eye movement

---

### Feature 5: Multiple Calibration Modes

**Quick 9-Point:** Press **C** key
- Faster calibration (~15 seconds)
- 9 points in 3×3 grid
- Good for testing
- Less accurate at edges

**Full 21-Point:** Press **F** key
- Complete calibration (~40 seconds)
- 21 strategically placed points
- Best accuracy
- **Recommended for normal use**

**Fresh Calibration:** Press **D** key
- Deletes saved calibration files
- Starts from scratch
- Use if accuracy is very poor
- Forces full recalibration

---

### Feature 6: Session Logging

**Automatic logging** to `logs/session_YYYYMMDD_HHMMSS/`

**Files created:**

1. **session.log** - Text log
   - All system events
   - Calibration start/stop
   - Errors and warnings
   - Timestamps for everything

2. **calibration.json** - Calibration data
   ```json
   {
     "num_points": 21,
     "points": [...],
     "training_error_x": 23.4,
     "training_error_y": 19.2,
     "timestamp": "2025-11-20 07:00:00"
   }
   ```

3. **tracking.csv** - Tracking frames (sampled)
   - Columns: timestamp, left_eye_x, left_eye_y, right_eye_x, right_eye_y, ...
   - Sampled: Every 10th frame to limit file size
   - Useful for analysis

4. **analysis.txt** - Automatic analysis
   - Generated on program exit
   - Session summary statistics
   - Calibration quality metrics
   - Recommendations

**Accessing logs:**
```bash
cd logs
ls  # List all sessions
cat session_20251120_070000/analysis.txt
```

---

## Diagnostic Tools

### Tool 1: Eye Movement Diagnostic

**Purpose:** Verify camera can detect your full eye movement range

**Run:**
```bash
python scripts/diagnose_eye_movement.py
```

**What it shows:**
- **Live camera feed** with iris tracking
- **Current eye position** (x, y) in real-time
- **Min/Max ranges** for vertical and horizontal
- **Color-coded status:**
  - 🟢 Green: Good range (>0.4 vertical, >0.5 horizontal)
  - 🟡 Yellow: Moderate range (0.3-0.4 vertical, 0.4-0.5 horizontal)
  - 🔴 Red: Poor range (<0.3 vertical, <0.4 horizontal)

**How to use:**
1. Run the tool
2. Move eyes to **EXTREME** positions:
   - Look far left, far right
   - Look as high as possible
   - Look as low as possible
3. Check displayed ranges
4. If ranges are red: Adjust camera/lighting before calibrating

**Sample output:**
```
Eye Position: (0.23, 0.67)
Vertical Range: 0.58 [Good]
Horizontal Range: 0.71 [Good]
```

**Interpretation:**
- Vertical >0.4 AND Horizontal >0.5 = **Ready to calibrate** ✅
- Either range <0.3 = **Fix camera setup first** ❌

**Press ESC to exit**

---

### Tool 2: Deep Session Analysis

**Purpose:** Comprehensive analysis of calibration and tracking quality

**Run:**
```bash
python scripts/deep_analysis.py
```

**Analyzes:** Most recent session in `logs/` folder

**Output sections:**

1. **Session Information:**
   ```
   Session: logs/session_20251120_070000
   Duration: 15 minutes 32 seconds
   ```

2. **Calibration Quality:**
   ```
   Calibration Points: 21
   Total Samples: 1260
   Training Error X: 23.4px [Good]
   Training Error Y: 19.2px [Good]
   ```

3. **Eye Movement Ranges:**
   ```
   Vertical Range: 0.58 [Excellent]
   Horizontal Range: 0.71 [Excellent]
   Eye Span Y: 0.45
   Eye Span X: 0.62
   ```

4. **Per-Point Analysis:**
   ```
   Point 1 (Top-Left Corner):
     Samples: 60
     Stability: 0.03 (very stable)
     Mean Position: (0.12, 0.05)
   
   Point 5 (Top-Right Corner):
     Samples: 60
     Stability: 0.04 (very stable)
     Mean Position: (0.89, 0.05)
   ```

5. **Tracking Quality:**
   ```
   Frames Tracked: 15423
   Average Cursor Movement: 42px per frame
   ```

6. **Recommendations:**
   ```
   ✓ Calibration quality is good
   ✓ Eye movement ranges are excellent
   ✓ Vertical tracking should be accurate
   ⚠ Point 12 shows high variance - may need recalibration
   ```

**When to run:**
- After calibration to verify quality
- If tracking accuracy is poor
- Before recalibrating to see if needed
- For research/debugging

---

### Tool 3: Log Analysis

**Purpose:** Statistical summary of session logs

**Run:**
```bash
python scripts/analyze_logs.py
```

**Shows:**
- Session count
- Average session duration
- Total tracking time
- Calibration frequency
- Error counts

**Useful for:** Long-term usage patterns

---

## Troubleshooting

### Problem: High Training Errors (>50px)

**Symptoms:**
- Console shows: "Training Error: X=90.2px, Y=40.5px"
- Poor cursor accuracy
- Can't reach screen areas

**Diagnosis:**
```bash
python scripts/diagnose_eye_movement.py
```

**Solution path:**

1. **If diagnostic shows poor ranges (<0.3):**
   - **Camera issue or insufficient eye movement**
   - Adjust camera position (closer, eye level)
   - Improve lighting
   - Clean camera lens
   - Move eyes to EXTREME positions during test

2. **If diagnostic shows good ranges (>0.4):**
   - **Calibration technique issue**
   - Delete calibration: Press **D** in control panel
   - Recalibrate with better technique:
     - Look DIRECTLY at each dot
     - Move eyes to EXTREMES at corners
     - Feel eyes strain
     - Hold gaze steady

---

### Problem: Vertical Tracking Poor

**Symptoms:**
- Cursor moves left/right OK
- Can't reach top or bottom of screen
- Analysis shows: "Vertical Range: 0.06 [CRITICAL]"

**Root cause:** Eyes not moving enough vertically during calibration

**Solution:**
1. Run diagnostic tool
2. Look as HIGH as possible (look at ceiling)
3. Look as LOW as possible (look at floor)
4. Check vertical range >0.4
5. If good in diagnostic but bad in calibration:
   - You're not looking at the dots properly during calibration
   - Recalibrate and ACTUALLY look at top row (feel strain looking up)
   - ACTUALLY look at bottom row (feel strain looking down)

---

### Problem: Can't Reach Screen Corners

**Symptoms:**
- Cursor won't go to extreme corners
- Edge tracking poor

**Solution:**
1. **Increase gain:**
   - Press **+** multiple times
   - Try gain 1.3-1.5

2. **Recalibrate with better corner technique:**
   - At corner points (1, 5, 17, 21)
   - Look BEYOND the dot
   - Feel extreme eye strain
   - Hold for full 2 seconds

3. **Check training errors:**
   - Run `python scripts/deep_analysis.py`
   - Look for corner point stability
   - High variance = poor calibration at that corner

---

### Problem: Cursor Jumps/Jittery

**Symptoms:**
- Cursor not smooth
- Random jumps
- Unstable tracking

**Solutions:**

1. **Check FPS:**
   - Control panel shows FPS
   - If <20: Close other apps, reduce load

2. **Verify smoothing enabled:**
   - Press **X** to toggle (should show "Enabled")

3. **Reset filters:**
   - Press **Z** to clear smoothing buffer

4. **Check lighting:**
   - Improve lighting consistency
   - Avoid flickering lights
   - Avoid shadows moving on face

5. **Check camera quality:**
   - Clean lens
   - Ensure focus is good
   - Try higher quality webcam

---

### Problem: False Click Triggers

**Symptoms:**
- Clicks happen when not blinking
- Too many accidental clicks

**Solution:**
- Blink detection is already smart (disabled when looking at bottom 40%)
- If still issue: Edit `enhanced_tracker.py`
- Find: `self.blink_threshold = 0.15`
- Change to: `self.blink_threshold = 0.12` (harder to trigger)

---

### Problem: Clicks Not Working

**Symptoms:**
- Blinking doesn't trigger clicks
- Have to blink multiple times

**Solution:**
1. **Blink technique:**
   - Close LEFT eye completely
   - Keep RIGHT eye open
   - Hold for 0.2 seconds

2. **Adjust threshold:**
   - Edit `enhanced_tracker.py`
   - Find: `self.blink_threshold = 0.15`
   - Change to: `self.blink_threshold = 0.20` (easier to trigger)

3. **Check detection:**
   - Watch control panel camera feed
   - Green dots should disappear on left eye when blinking

---

### Problem: Control Panel Won't Open

**Symptoms:**
- Program starts
- Calibration works
- But no control panel appears

**Solution:**
1. **Check tkinter installation:**
   ```bash
   python -c "import tkinter; print('OK')"
   ```

2. **If error:** Install tkinter:
   - **Windows:** Reinstall Python with tkinter option
   - **Linux:** `sudo apt-get install python3-tk`
   - **Mac:** Should be included

3. **Check threading:**
   - Control panel runs in main thread
   - Tracking runs in background thread
   - Both should start automatically

---

### Problem: Program Crashes on Start

**Symptoms:**
- Error message on startup
- Program exits immediately

**Common causes:**

1. **Missing dependencies:**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

2. **Camera in use:**
   - Close Zoom, Skype, Teams, etc.
   - Only one app can use camera at a time

3. **Permission denied:**
   - Check camera permissions in OS settings
   - Grant permission to Python

4. **Import errors:**
   - Verify all files present:
     - `enhanced_tracker.py`
     - `core/calibration_15point.py`
     - `core/eye_tracking_logger.py`
     - `ui/control_panel.py`, etc.

---

## Performance Optimization

### For Low-End Systems

**Reduce CPU usage:**

1. **Lower camera resolution:**
   Edit `enhanced_tracker.py`:
   ```python
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # From 1280
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # From 720
   ```

2. **Reduce smoothing window:**
   Edit `core/calibration_15point.py`:
   ```python
   maxlen=5  # From 7 in deque initialization
   ```

3. **Disable raw gaze overlay:**
   - Don't press **G** key
   - Overlay costs extra processing

4. **Close control panel camera feed:**
   - Minimize control panel window
   - Reduces rendering overhead

### For High-End Systems

**Maximize accuracy:**

1. **Increase camera resolution:**
   ```python
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
   ```

2. **Increase smoothing:**
   ```python
   maxlen=10  # From 7
   ```

3. **Lower polynomial degree (faster training):**
   Edit `core/calibration_15point.py`:
   ```python
   PolynomialFeatures(degree=2)  # From degree=3
   ```

---

## FAQ

### Q: How much better is Version 2 vs Version 1?
**A:** Approximately 50% better accuracy. Version 1 typical: ±50-80px. Version 2 typical: ±20-40px after good calibration.

### Q: Why 21 points instead of 9?
**A:** Better edge and corner coverage. Version 1's 9 points left large gaps, especially at screen edges. Version 2's 21 points provide complete coverage with edge weighting.

### Q: What's "edge weighting"?
**A:** Corners get 9× more importance in machine learning training, edges get 5×. This makes corner/edge accuracy much better than center.

### Q: Can I use fewer than 21 points?
**A:** Yes, press **C** for quick 9-point calibration. But 21-point (**F** key) is recommended for best accuracy.

### Q: How often should I recalibrate?
**A:** 
- **Daily:** If using many hours per day
- **After setup changes:** Moved camera, changed position, different lighting
- **When accuracy drops:** Noticeable drift or poor accuracy

### Q: What are the log files for?
**A:** Research, debugging, and analysis. You can delete old session folders to save space if you don't need them.

### Q: Can I modify the machine learning model?
**A:** Yes, edit `core/calibration_15point.py`. You can change:
- Polynomial degree (default: 3)
- Ridge alpha (default: 0.01)
- Edge weighting (default: 9×, 5×)

### Q: Why does calibration save training errors now?
**A:** So you can verify calibration quality. Training error <40px means good calibration. >60px means recalibration recommended.

### Q: What if analysis shows "Vertical range: 0.06 [CRITICAL]"?
**A:** Camera can't detect your full eye movement, OR you're not moving eyes enough. Run diagnostic tool to verify, then recalibrate with eyes at EXTREME positions.

### Q: Can I use this for drawing/design work?
**A:** Possible, but requires excellent calibration (training errors <20px). Use 21-point calibration, adjust gain for precision, enable smoothing.

### Q: Does it work with multiple monitors?
**A:** Calibration is for primary monitor only. Cursor can move to secondary monitors but accuracy degrades.

### Q: Can I save multiple calibration profiles?
**A:** Not currently. One calibration saved at a time. Feature could be added.

### Q: What's the difference between smoothing ON and OFF?
**A:** 
- **ON:** Cursor movement is smooth and fluid, slight lag (~50ms)
- **OFF:** Cursor responds instantly but jerky/jittery

### Q: Why is blink detection disabled when looking down?
**A:** Looking down naturally closes eyes more. Without this, looking at bottom of screen would trigger false clicks constantly.

---

## Keyboard Shortcuts Summary

| Key | Function |
|-----|----------|
| **C** | Quick 9-point calibration |
| **F** | Full 21-point calibration |
| **D** | Delete calibration and start fresh |
| **S** | Toggle cursor control ON/OFF |
| **X** | Toggle smoothing ON/OFF |
| **Z** | Reset smoothing filters |
| **G** | Toggle raw gaze overlay |
| **+** or **=** | Increase gain (sensitivity) |
| **-** or **_** | Decrease gain (sensitivity) |
| **Q** | Quit and save |
| **ESC** | Force close (during calibration) |

---

## Control Panel Workflow

**Typical usage session:**

1. **Start:** `python enhanced_tracker.py`
2. **Calibrate:** 21-point calibration runs (if first time)
3. **Control panel opens:** Shows live feed and status
4. **Track:** Eyes control cursor automatically
5. **Adjust if needed:**
   - Gain too low? Press **+**
   - Cursor jumping? Press **Z**
   - Want to see raw gaze? Press **G**
6. **Recalibrate if accuracy drops:** Press **F**
7. **Quit:** Press **Q** (saves calibration and logs)

---

## Advanced Customization

### Modifying Calibration Grid

Edit `core/calibration_15point.py`, function `create_calibration_grid`:

**Current 21-point grid:**
```python
grid = [
    # Top row (y=0.05)
    (0.05, 0.05), (0.275, 0.05), (0.5, 0.05), (0.725, 0.05), (0.95, 0.05),
    # Upper-mid row (y=0.3)
    (0.1, 0.3), (0.5, 0.3), (0.9, 0.3),
    # Center row (y=0.5)
    (0.05, 0.5), (0.275, 0.5), (0.5, 0.5), (0.725, 0.5), (0.95, 0.5),
    # Lower-mid row (y=0.7)
    (0.1, 0.7), (0.5, 0.7), (0.9, 0.7),
    # Bottom row (y=0.95)
    (0.05, 0.95), (0.275, 0.95), (0.5, 0.95), (0.725, 0.95), (0.95, 0.95)
]
```

**Add more points:** Just append to grid list

**Change positions:** Modify (x, y) coordinates (0.0-1.0 range)

### Changing Edge Weights

Edit `core/calibration_15point.py`, function `prepare_training_data`:

**Current weights:**
```python
corner_indices = [0, 4, 16, 20]  # 9× weight
edge_indices = [1, 2, 3, 5, 7, 13, 15, 17, 18, 19]  # 5× weight
```

**Modify:**
```python
if idx in corner_indices:
    weight = 12  # Increase corner importance
elif idx in edge_indices:
    weight = 7   # Increase edge importance
```

### Adjusting Machine Learning

Edit `core/calibration_15point.py`, function `train_model`:

**Current:**
```python
poly = PolynomialFeatures(degree=3)
model = Ridge(alpha=0.01)
```

**Experiment:**
```python
# More complex model (slower but potentially more accurate)
poly = PolynomialFeatures(degree=4)
model = Ridge(alpha=0.005)

# Or simpler/faster model
poly = PolynomialFeatures(degree=2)
model = Ridge(alpha=0.1)
```

---

**Version:** 2.0 (Enhanced)  
**Author:** SHA Graduation Project Group 24  
**Supervisor:** Dr. Mohammed Hussien  
**Academic Year:** 2025/2026

For technical support, refer to diagnostic tools and analysis scripts in the `scripts/` folder.
