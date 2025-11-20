# Eye Tracking System - Version 1 (Basic)

## Overview
Simple eye-controlled mouse using computer vision. This is the basic version with 9-point calibration and straightforward eye tracking functionality.

**Author:** SHA Graduation Project Group 24  
**Supervisor:** Dr. Mohammed Hussien  
**Academic Year:** 2025/2026

---

## Features
- ✅ Eye movement tracking for mouse control
- ✅ Blink detection for mouse clicks
- ✅ Smooth cursor movement with moving average
- ✅ 9-point auto-calibration
- ✅ Screen size adaptation
- ✅ Debug visualization
- ✅ Text-to-speech calibration guidance

---

## Requirements

### Hardware
- Webcam (internal or external)
- Windows/Linux/Mac OS
- Minimum 4GB RAM

### Software
- Python 3.8 or higher
- See `requirements.txt` for Python packages

---

## Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
python --version  # Should show Python 3.8+
```

---

## How to Use

### Quick Start
1. **Run the program:**
   ```bash
   python main.py
   ```

2. **Calibration Process:**
   - The program will automatically start calibration
   - Voice guidance will tell you where to look
   - Follow the numbered red dots (1-9) on screen
   - Look at each point for 2 seconds until it moves to the next
   - Keep your head still and only move your eyes

3. **After Calibration:**
   - Your eyes now control the mouse cursor
   - Blink your **left eye only** to click
   - Close **both eyes for 1 second** to exit the program

### Controls During Tracking
- **Left eye blink:** Mouse click
- **Both eyes closed (1 sec):** Exit program
- **3 rapid blinks:** Toggle debug window (fullscreen/normal)
- **ESC key:** Force exit

---

## Tips for Best Performance

### Camera Position
- Place camera at eye level
- Maintain 30-50 cm distance from screen
- Ensure good lighting (avoid backlighting)
- Keep face centered in camera view

### Calibration Tips
- Sit comfortably in your normal position
- Keep head still during calibration
- Move ONLY your eyes to look at each point
- Look directly at the center of each red dot
- Don't rush - let each point complete

### Tracking Tips
- Keep head relatively still
- Make deliberate eye movements
- If cursor drifts, close and restart the program
- Recalibrate if accuracy decreases

---

## Troubleshooting

### Problem: Cursor is shaky
**Solution:** Adjust the `smooth_window` parameter in code (default: 15)

### Problem: Can't reach screen edges
**Solution:** During calibration, look at the EXTREME corners - move eyes as far as possible

### Problem: Blink detection too sensitive
**Solution:** Adjust `blink_threshold` in code (lower = require more closed eye, default: 0.2)

### Problem: Camera not detected
**Solution:** 
- Check camera permissions
- Try different camera index (change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`)

### Problem: Low FPS/lag
**Solution:**
- Close other applications
- Reduce `smooth_window` value
- Ensure good lighting (reduces processing)

---

## Technical Details

### Algorithm
- **Face Detection:** MediaPipe Face Mesh (468 landmarks + iris tracking)
- **Eye Tracking:** Iris position within eye boundaries
- **Smoothing:** Moving average (15-frame window) + exponential smoothing
- **Calibration:** 9-point grid mapping with ratio-based transformation
- **Blink Detection:** Eye Aspect Ratio (EAR) method

### Coordinate System
- Horizontal: 0.0 (left) → 1.0 (right)
- Vertical: 0.0 (top) → 1.0 (bottom)
- Screen mapping uses calibrated ratios with sensitivity adjustment

### Performance
- **FPS:** 25-30 (typical)
- **Latency:** <50ms
- **Accuracy:** ±50px (after good calibration)

---

## File Structure
```
version1/
├── main.py              # Main program
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── MANUAL.md           # Detailed user manual
```

---

## Known Limitations
- Requires consistent head position
- Lighting affects accuracy
- Eye glasses may reduce precision
- Not suitable for rapid/gaming applications
- Single user at a time

---


## License
Academic project for SHA University - Group 24 (2025/2026)

**Note:** This is Version 1 (Basic). For advanced features, see Version 2.
