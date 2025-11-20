# Eye Tracking System - Version 2 (Enhanced)

## Overview
Advanced eye-controlled mouse system with 21-point calibration, machine learning-based prediction, advanced smoothing, comprehensive logging, and professional control panel.

**Author:** SHA Graduation Project Group 24  
**Supervisor:** Dr. Mohammed Hussien  
**Academic Year:** 2025/2026

---

## Features

### Core Tracking
- ✅ **21-point calibration** with full screen coverage (edges + corners)
- ✅ **Machine Learning:** Ridge Regression with Polynomial Features (degree 3)
- ✅ **Advanced smoothing:** Deque-based + exponential + outlier detection
- ✅ **10 engineered features:** Left eye, right eye, average, difference, nose tip
- ✅ **Edge weighting:** 9× for corners, 5× for edges
- ✅ **Smart blink detection:** Disabled when looking down to prevent false triggers

### User Interface
- ✅ **Advanced Control Panel:** Real-time video, FPS, calibration status
- ✅ **Setup Wizard:** Interactive pre-calibration guide
- ✅ **Raw Gaze Overlay:** Debug view showing raw eye positions
- ✅ **Calibration Overlay:** Professional fullscreen calibration interface

### Analytics & Logging
- ✅ **Comprehensive session logging:** Every calibration and tracking frame
- ✅ **Training error metrics:** Saved with calibration data
- ✅ **Analysis tools:** Deep session analysis, eye movement diagnostics
- ✅ **Session management:** Organized logs by timestamp

### Advanced Controls
- ✅ **Adjustable gain:** Fine-tune cursor sensitivity (±)
- ✅ **Toggle smoothing:** Enable/disable on-the-fly (X)
- ✅ **Reset filters:** Clear smoothing history (Z)
- ✅ **Multiple calibration modes:** 9-point quick or 21-point full
- ✅ **Incremental calibration:** Add points without full recalibration

---

## Requirements

### Hardware
- **Webcam:** 720p or better (1080p recommended)
- **OS:** Windows 10/11, Linux, or Mac OS
- **RAM:** Minimum 8GB (16GB recommended)
- **CPU:** Multi-core processor recommended

### Software
- **Python:** 3.8 or higher (3.10 recommended)
- See `requirements.txt` for complete dependencies

---

## Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
python --version  # Should show Python 3.8+
python -c "import cv2, mediapipe, numpy, sklearn; print('All packages OK')"
```

### Step 3: (Optional) Configure Camera
Edit `enhanced_tracker.py` if you need to change camera index (default: 0)

---

## How to Use

### Quick Start
1. **Run the program:**
   ```bash
   python enhanced_tracker.py
   ```

2. **Setup Wizard (First Time):**
   - Follow on-screen instructions
   - Position yourself correctly
   - Test camera detection
   - Proceed to calibration

3. **21-Point Calibration:**
   - **BLACK SCREEN** appears with numbered red dots
   - Look at each dot as it turns red and is called out
   - Hold your gaze for 2 seconds per point
   - **CRITICAL:** Look at EXTREME positions - feel your eyes strain
   - 21 points cover: all corners, edges, and center

4. **Control Panel Opens:**
   - Live camera feed with tracking visualization
   - Real-time FPS and status indicators
   - Cursor control automatically enabled

5. **Using Eye Tracking:**
   - Eyes control the cursor
   - **Left eye blink** (right eye open) = Click
   - Blink detection disabled when looking at bottom 40% of screen

---

## Control Panel Commands

### Calibration
- **C:** Quick 9-point calibration
- **F:** Full 21-point calibration (recommended)
- **D:** Delete saved calibration and start fresh
- **R:** Add incremental calibration point

### Tracking Controls
- **S:** Toggle cursor control ON/OFF
- **X:** Toggle smoothing ON/OFF
- **Z:** Reset smoothing filters (clear history)
- **G:** Toggle raw gaze overlay (debug view)

### Sensitivity
- **+ or =:** Increase gain (more sensitive)
- **- or _:** Decrease gain (less sensitive)

### Exit
- **Q:** Quit and save calibration + logs

---

## Advanced Features

### Raw Gaze Overlay (G key)
- Shows raw eye position before smoothing
- Fullscreen overlay with green crosshair
- Trail shows recent positions
- Useful for debugging calibration issues

### Diagnostic Tools
Located in `scripts/` folder:

1. **Eye Movement Diagnostic:**
   ```bash
   python scripts/diagnose_eye_movement.py
   ```
   - Real-time visualization of eye detection
   - Shows vertical/horizontal movement ranges
   - Helps identify camera detection issues

2. **Deep Session Analysis:**
   ```bash
   python scripts/deep_analysis.py
   ```
   - Analyzes latest session logs
   - Shows training errors, eye movement ranges
   - Per-point calibration quality
   - Recommendations for improvement

3. **Log Analysis:**
   ```bash
   python scripts/analyze_logs.py
   ```
   - Session summary statistics
   - Tracking performance metrics

### Logging System
All sessions saved to `logs/session_YYYYMMDD_HHMMSS/`:
- `session.log` - All events and errors
- `calibration.json` - Calibration data and training errors
- `tracking.csv` - Every tracking frame (sampled)
- `analysis.txt` - Automatic analysis report

---

## Tips for Best Results

### Camera Setup
- **Position:** Eye level, 40-60 cm from face
- **Lighting:** Bright, even lighting on face (no backlighting)
- **Background:** Stable, non-moving background
- **Angle:** Camera perpendicular to face

### Calibration Best Practices
1. **Sit comfortably** in your normal working position
2. **Keep head STILL** - only move eyes
3. **Look DIRECTLY** at each point - not near it, AT it
4. **Move to EXTREMES:** Feel eye strain at corners/edges
5. **Wait for completion:** Don't rush, let each point finish
6. **Consistency:** Maintain same head position throughout

### Common Calibration Mistakes
❌ Moving head instead of eyes  
❌ Looking near the point instead of at it  
❌ Not moving eyes to extreme positions  
❌ Rushing through points  
❌ Poor lighting conditions  

✅ **Solution:** Run diagnostic tool first to verify camera detection

### Improving Accuracy
1. Run `python scripts/diagnose_eye_movement.py`
2. Verify vertical range > 0.4, horizontal > 0.5
3. If ranges low: adjust camera/lighting
4. Delete calibration (D key) and recalibrate with better technique
5. Use 21-point calibration for best coverage
6. Adjust gain (±) to fine-tune sensitivity

---

## Troubleshooting

### Problem: Training errors high (>50px)
**Solution:**
- Run diagnostic tool: `python scripts/diagnose_eye_movement.py`
- Check eye movement ranges (should be >0.4 vertical, >0.5 horizontal)
- Recalibrate with eyes at EXTREME positions
- Ensure good lighting and camera position

### Problem: Can't reach screen corners
**Solution:**
- During calibration, look BEYOND the dots at corners
- Feel your eyes strain to reach extremes
- Check diagnostic tool for movement range
- Adjust camera angle/distance

### Problem: Cursor jumps/unstable
**Solution:**
- Enable smoothing (X key if disabled)
- Reduce gain (- key)
- Reset filters (Z key)
- Check lighting consistency

### Problem: False click triggers
**Solution:**
- Blink detection already disabled when looking down
- Adjust `blink_threshold` in code if needed (lower = less sensitive)
- Try blinking more deliberately (left eye only)

### Problem: Low FPS (<20)
**Solution:**
- Close other applications
- Reduce camera resolution in code
- Disable raw gaze overlay (G key)
- Check CPU usage

### Problem: Calibration keeps failing
**Solution:**
1. Run setup wizard again
2. Verify camera detects face: check control panel video
3. Improve lighting
4. Move closer/farther from camera
5. Clean camera lens

---

## Technical Architecture

### Machine Learning Pipeline
```
Input Features (10D):
├── Left eye position (x, y)
├── Right eye position (x, y)
├── Average eye position (x, y)
├── Eye difference (Δx, Δy)
└── Nose tip position (x, y)
    ↓
Polynomial Features (degree=3)
    ↓
Ridge Regression (α=0.01)
    ↓
Screen Coordinates (x, y)
    ↓
Smoothing (deque, exponential, outlier detection)
    ↓
Cursor Movement
```

### Calibration System
- **Grid:** 21 points (5+3+5+3+5 rows at y=0.05, 0.3, 0.5, 0.7, 0.95)
- **Sampling:** 60 frames per point (2 seconds)
- **Edge Weighting:** Corners ×9, Edges ×5, Center ×1
- **Training:** Ridge with PolynomialFeatures degree 3
- **Validation:** Training error saved for analysis

### Smoothing Algorithm
```python
1. Deque buffer (7 frames)
2. Outlier detection (>200px movement rejected)
3. Moving average
4. Exponential smoothing (factor=0.5)
5. Gain adjustment (default=1.0)
```

### Performance Metrics
- **FPS:** 25-30 typical
- **Latency:** <30ms
- **Accuracy:** ±20-40px (after good calibration)
- **Training Error:** Target <40px both X and Y

---

## Project Structure
```
version2/
├── enhanced_tracker.py          # Main application
├── core/
│   ├── calibration_15point.py   # 21-point calibration + ML
│   └── eye_tracking_logger.py   # Logging system
├── ui/
│   ├── control_panel.py         # Advanced control panel
│   ├── setup_wizard.py          # Pre-calibration wizard
│   ├── overlay_window.py        # Calibration overlay
│   └── raw_gaze_overlay.py      # Raw gaze debug view
├── scripts/
│   ├── diagnose_eye_movement.py # Eye movement diagnostic
│   ├── deep_analysis.py         # Session analysis
│   └── analyze_logs.py          # Log statistics
├── logs/                        # Session logs (auto-generated)
├── calibration_15point.json     # Saved calibration (auto-generated)
├── calibration_15point.pkl      # Saved ML model (auto-generated)
├── README.md                    # This file
├── requirements.txt             # Dependencies
└── MANUAL.md                    # Detailed manual
```

---

## Known Limitations
- Requires consistent head position (±5cm tolerance)
- Sensitive to lighting changes
- Eye glasses may reduce accuracy by 10-20%
- Not suitable for very rapid movements
- Single user per session
- Training errors depend heavily on calibration technique

---

## Comparison: Version 1 vs Version 2

| Feature | Version 1 | Version 2 |
|---------|-----------|-----------|
| Calibration Points | 9 | 21 |
| Algorithm | Ratio mapping | Ridge Regression ML |
| Features | 2 (avg eye x/y) | 10 (eyes, nose, deltas) |
| Smoothing | Basic moving avg | Advanced multi-stage |
| UI | Debug window only | Control panel + overlays |
| Logging | None | Comprehensive |
| Analysis Tools | None | 3 diagnostic tools |
| Edge Accuracy | Poor | Excellent (edge weighting) |
| Typical Accuracy | ±50-80px | ±20-40px |
| Training Error | Unknown | Tracked and saved |

---

## Support & Analysis

### If Tracking Quality is Poor:
1. **Run diagnostic:** `python scripts/diagnose_eye_movement.py`
2. **Analyze session:** `python scripts/deep_analysis.py`
3. **Check logs:** `logs/session_YYYYMMDD_HHMMSS/analysis.txt`
4. **Recalibrate:** Use 'D' key in control panel

### For Development/Research:
- Session logs contain all raw data
- CSV format for easy analysis
- Training errors tracked per calibration
- Modify parameters in `calibration_15point.py`

---

## License
Academic project for SHA University - Group 24 (2025/2026)

**Supervisor:** Dr. Mohammed Hussien

---

## Credits
- **MediaPipe:** Google's face mesh solution
- **OpenCV:** Computer vision library
- **scikit-learn:** Machine learning algorithms
- **PyAutoGUI:** Cursor control
