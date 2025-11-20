# Eye Tracking System - Comprehensive Logging Guide

## Overview

The system now includes comprehensive logging to diagnose calibration and tracking issues. All data is saved to the `logs/` directory with a unique session timestamp.

## How to Use

### 1. Delete Old Calibration (Important!)

Before starting, delete the old calibration files to ensure you start fresh:

```powershell
Remove-Item calibration_15point.json, calibration_15point.pkl -ErrorAction SilentlyContinue
```

### 2. Run the Eye Tracker

```powershell
python enhanced_tracker.py
```

### 3. Complete Calibration Carefully

**CRITICAL**: During calibration, you MUST actually look at each calibration point!

- When a red circle appears, **move your eyes** to look directly at it
- Keep your head still, only move your eyes
- Wait until the circle turns green and moves to the next point
- Don't just stare at the center - this is the #1 cause of poor vertical/corner tracking

### 4. Use the System for 1-2 Minutes

After calibration, move your eyes around to test:
- Top corners
- Bottom corners
- Vertical movements (top to bottom)
- Horizontal movements (left to right)

### 5. Exit and Check Logs

Press **Q** to exit. This will:
- Save all calibration data
- Generate tracking logs
- Create analysis report
- Close the system cleanly

## Log Files Generated

All files are in `logs/session_YYYYMMDD_HHMMSS/`:

### 1. `session.log` - Main Event Log
- System information (screen resolution, camera settings)
- Calibration events (start, points, completion)
- Training errors (X and Y pixel errors)
- General events and errors

### 2. `calibration.json` - Raw Calibration Data
```json
{
  "session_id": "...",
  "start_time": "...",
  "num_points": 21,
  "frames_per_point": 60,
  "points": [
    {
      "point_index": 0,
      "screen_x": 96,
      "screen_y": 54,
      "samples": [
        {
          "timestamp": "...",
          "left_eye": [0.45, 0.32],
          "right_eye": [0.55, 0.33],
          "nose": [0.50, 0.45]
        },
        ...60 samples...
      ]
    },
    ...21 points...
  ]
}
```

### 3. `tracking.csv` - Every Frame Logged
CSV with all tracking data for analysis in Excel/Python:

| Column | Description |
|--------|-------------|
| timestamp | ISO timestamp of frame |
| frame_count | Frame number |
| left_eye_x, left_eye_y | Left eye iris position (0-1) |
| right_eye_x, right_eye_y | Right eye iris position (0-1) |
| avg_eye_x, avg_eye_y | Average eye position |
| nose_x, nose_y | Nose tip position |
| predicted_x, predicted_y | Raw model prediction (pixels) |
| smoothed_x, smoothed_y | After smoothing (pixels) |
| cursor_x, cursor_y | Final cursor position (pixels) |
| face_detected | True/False |
| left_ear, right_ear | Eye Aspect Ratio (blink detection) |
| blink_detected | True/False |
| smoothing_enabled | True/False |
| gain | Output gain multiplier |
| mode | Tracking/Calibration |

### 4. `errors.log` - Error Messages
All errors and exceptions during the session.

### 5. `analysis.txt` - Automated Analysis & Recommendations

Example:
```
Eye Tracking Session Analysis
Session: 20240101_120000

CALIBRATION SUMMARY
- Points: 21
- Training Error X: 45.2 px
- Training Error Y: 78.5 px

TRACKING SUMMARY
- Total Frames: 1234
- Face Detection Rate: 98.5%
- Avg Smoothing Applied: Yes

CALIBRATION QUALITY ANALYSIS
⚠️ WARNING: High vertical error (78.5px > 50px threshold)
  This suggests poor calibration technique. Common causes:
  - Not actually looking at vertical calibration points
  - Only looking at center/horizontal points
  - Head movement during calibration

RECOMMENDATIONS
1. Recalibrate and ensure you LOOK AT each point
2. Pay special attention to top/bottom points
3. Keep head very still during calibration
4. Focus eyes on the red circle, not the center
```

## Analyzing the Data

### Quick Check: Read `analysis.txt`

This tells you immediately what's wrong:
- **High X/Y errors (>50px)**: Poor calibration - user not looking at points
- **High Y error only**: Not looking at vertical points (top/bottom)
- **Low errors but poor tracking**: Model issue (very rare with current setup)

### Detailed Analysis: Use `tracking.csv`

Import into Excel or Python:

```python
import pandas as pd

# Load tracking data
df = pd.read_csv('logs/session_YYYYMMDD_HHMMSS/tracking.csv')

# Check eye movement ranges
print("Eye X range:", df['avg_eye_x'].min(), "to", df['avg_eye_x'].max())
print("Eye Y range:", df['avg_eye_y'].min(), "to", df['avg_eye_y'].max())

# If ranges are narrow (e.g., 0.3-0.7), you're not moving eyes enough!
# Should be close to 0.0-1.0 for full coverage

# Plot cursor vs eye position
import matplotlib.pyplot as plt
plt.scatter(df['avg_eye_x'], df['cursor_x'])
plt.xlabel('Eye X')
plt.ylabel('Cursor X')
plt.show()
```

### Detailed Calibration Check: Use `calibration.json`

```python
import json

with open('logs/session_YYYYMMDD_HHMMSS/calibration.json', 'r') as f:
    cal = json.load(f)

# Check per-point variability
for point in cal['points']:
    samples = point['samples']
    left_eyes = [s['left_eye'] for s in samples]
    
    # Calculate standard deviation
    import numpy as np
    std_x = np.std([e[0] for e in left_eyes])
    std_y = np.std([e[1] for e in left_eyes])
    
    print(f"Point {point['point_index']} at ({point['screen_x']}, {point['screen_y']})")
    print(f"  Eye position std: X={std_x:.3f}, Y={std_y:.3f}")
    # High std (>0.05) = eyes moving around, not looking at point!
```

## Common Issues & What Logs Show

### Issue: Cursor doesn't move vertically
**Log Evidence:**
- `analysis.txt`: High Y error, low X error
- `calibration.json`: Top/bottom points have same eye_y values as center
- **Cause**: User staring at center, not looking up/down at calibration points

### Issue: Corners unreachable
**Log Evidence:**
- `analysis.txt`: High overall errors
- `calibration.json`: Corner points (0, 4, 16, 20) have high variability
- **Cause**: Not looking at corners during calibration

### Issue: Cursor shaky/jittery
**Log Evidence:**
- `tracking.csv`: predicted_x/y jumping around
- `tracking.csv`: smoothed_x/y still jumping
- **Cause**: Camera/lighting issues, not calibration

### Issue: Cursor slow to respond
**Log Evidence:**
- `tracking.csv`: Large difference between predicted and smoothed
- **Solution**: Press X to toggle smoothing, or adjust parameters

## Session Workflow

1. **Delete old calibration**
2. **Run tracker**: `python enhanced_tracker.py`
3. **Setup wizard**: Follow positioning guide
4. **Calibrate carefully**: LOOK AT EACH POINT!
5. **Test tracking**: Move eyes to all screen areas
6. **Exit**: Press Q
7. **Check logs**: Read `analysis.txt` first
8. **If issues**: Analyze CSV/JSON for root cause
9. **Recalibrate**: Use insights from logs to improve technique

## What Makes Good Calibration?

**Good calibration logs show:**
- Training errors: X < 30px, Y < 30px
- Per-point std: < 0.03 for both X and Y
- Eye position ranges: 0.1-0.9 for both axes
- Face detection: > 95% during calibration

**Bad calibration logs show:**
- Training errors: > 50px
- Per-point std: > 0.05 (eyes wandering)
- Eye position ranges: 0.4-0.6 (not moving eyes)
- High variability on edge points (not looking)

## Tips for Best Results

1. **Environment**:
   - Good lighting (front-lit, not backlit)
   - Stable head position (40-80cm from camera)
   - Minimize reflections on glasses

2. **Calibration Technique**:
   - Actually move your EYES to each point
   - Keep head completely still
   - Wait for green circle before looking away
   - Don't rush - accuracy > speed

3. **Verification**:
   - After calibration, test all corners
   - If corners/edges don't work, recalibrate
   - Use raw gaze overlay (press G) to see actual eye detection

4. **Using Logs**:
   - Always check `analysis.txt` first
   - If errors > 50px, always recalibrate
   - Use CSV for detailed diagnosis
   - Compare multiple sessions to see improvement

## Troubleshooting with Logs

**Q: How do I know if calibration was good?**
A: Check `analysis.txt` - if training errors < 40px for both X and Y, it's good.

**Q: Vertical tracking is bad but errors look OK?**
A: Check `calibration.json` - compare eye_y values for top (points 0-4) vs bottom (points 16-20) vs center (points 8-12). They should be very different.

**Q: Cursor doesn't reach corners?**
A: Check corner calibration points (0, 4, 16, 20) in `calibration.json` - high std or similar eye positions to center points = didn't look at corners.

**Q: How do I analyze smoothing effects?**
A: In `tracking.csv`, compare predicted_x/y to smoothed_x/y. Large differences = aggressive smoothing.

---

**Remember**: Good tracking requires good calibration. The logs will tell you exactly what went wrong!
