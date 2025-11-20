# Technical Details - Eye Tracking System

## What Filters Are Used?

### 1. **Smoothing Filter (Toggle with 'X' key)**
The smoothing filter stabilizes cursor movement using **3 techniques**:

#### A) **Moving Average Filter**
- **Buffer Size:** 7 frames
- **How it works:** Keeps the last 7 cursor positions and averages them
- **Effect:** Reduces jitter and shaky movements
- **Example:** If positions are [100, 102, 98, 101, 99, 103, 100], average = 100.4

#### B) **Exponential Smoothing**
- **Smooth Factor:** 0.5 (50/50 blend)
- **Formula:** `new_position = 0.5 × current + 0.5 × previous`
- **Effect:** Prevents sudden jumps while keeping responsiveness
- **Why 0.5?** Balance between speed (1.0 = no smoothing) and stability (0.1 = very slow)

#### C) **Outlier Detection**
- **Threshold:** 200 pixels
- **How it works:** If cursor tries to jump more than 200px, it's damped to 50/50 blend
- **Effect:** Prevents wild jumps from tracking errors
- **Formula:** If jump > 200px: `position = 0.5 × old + 0.5 × new`

### 2. **Vertical Bias Compensation**
- **Purpose:** Help reach bottom of screen
- **How it works:** When looking below center, adds up to 50px boost
- **Formula:** `boost = (distance_from_center / screen_half_height) × 50px`
- **Effect:** Easier to reach taskbar and bottom UI elements

### 3. **Polynomial Regression (Machine Learning)**
- **Model:** Ridge Regression with Polynomial Features (degree=2)
- **Features:** 10 inputs transformed into 66 polynomial combinations
- **Regularization (alpha):** 0.1 (low = tight fit to calibration)
- **Purpose:** Maps eye position → screen coordinates with non-linear accuracy

---

## What Is Gain Used For?

**Gain** = Cursor sensitivity multiplier (adjustable with '+' and '-' keys)

### How Gain Works:
```
final_position = center + (predicted_position - center) × gain
```

### Examples:
- **Gain = 1.0** (default): Normal 1:1 mapping
- **Gain = 1.5**: Eye movement amplified 1.5x (move less, cursor moves more)
- **Gain = 0.8**: Eye movement reduced (move more, cursor moves less)

### Use Cases:
- **Increase gain (1.2-1.5):** If you struggle to reach screen edges
- **Decrease gain (0.7-0.9):** If cursor moves too much/overshoots
- **Range:** 0.5 to 2.0

### Formula Breakdown:
1. Calculate distance from screen center: `offset = predicted - center`
2. Multiply by gain: `scaled_offset = offset × gain`
3. Add back to center: `final = center + scaled_offset`

**Effect:** Larger gain = more sensitive = smaller eye movements needed

---

## Blink Detection (NEW!)

### Left-Eye Click
- **Trigger:** Close LEFT eye only (RIGHT eye stays open)
- **Threshold:** Eye Aspect Ratio (EAR) < 0.2
- **Cooldown:** 0.5 seconds between clicks
- **Purpose:** Click without hands

### How EAR Works:
```
EAR = (vertical_1 + vertical_2) / (2 × horizontal)
```
- Open eye: EAR ≈ 0.3-0.4
- Closed eye: EAR < 0.2

---

## Performance Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| Smooth Window | 7 frames | Balance speed/stability |
| Smooth Factor | 0.5 | 50% new + 50% old |
| Outlier Threshold | 200 px | Detect tracking errors |
| Blink Threshold | 0.2 EAR | Detect eye closure |
| Calibration Samples | 60 frames/point | Stable averaging |
| Polynomial Degree | 2 | Non-linear mapping |
| Ridge Alpha | 0.1 | Low regularization |

---

## Calibration Features (10 total)

The system uses **10 engineered features** for accurate prediction:

1. **Left Eye X** - Horizontal iris position in left eye
2. **Left Eye Y** - Vertical iris position in left eye
3. **Right Eye X** - Horizontal iris position in right eye
4. **Right Eye Y** - Vertical iris position in right eye
5. **Average Eye X** - Mean of both eyes (main gaze indicator)
6. **Average Eye Y** - Mean of both eyes (main gaze indicator)
7. **Eye Diff X** - Right - Left horizontal (head angle compensation)
8. **Eye Diff Y** - Right - Left vertical (head tilt compensation)
9. **Nose X** - Head position horizontal
10. **Nose Y** - Head position vertical

These 10 features are transformed into **66 polynomial features** (combinations like X², Y², X×Y, etc.)

---

## Filter Performance

### With Smoothing ON:
- ✅ Stable cursor (no shaking)
- ✅ Smooth movement
- ⚠️ ~50ms delay (acceptable for UI navigation)
- 🎯 Best for: General use, clicking, browsing

### With Smoothing OFF:
- ✅ Instant response (0 delay)
- ❌ Shaky/jittery cursor
- 🎯 Best for: Testing, debugging, seeing raw tracking

---

## Quick Reference

| Command | Action | Effect |
|---------|--------|--------|
| **X** | Toggle smoothing | ON = stable, OFF = fast but shaky |
| **+** | Increase gain | More sensitive (easier edges) |
| **-** | Decrease gain | Less sensitive (more control) |
| **Z** | Reset filters | Clear smoothing buffers |
| **D** | Delete calibration | Start fresh calibration |
| **Blink Left** | Click | Close left eye only |

---

## Troubleshooting

**Problem:** Cursor too slow/laggy  
**Solution:** Press 'X' to turn smoothing OFF, or reduce smooth_window in code

**Problem:** Can't reach screen edges  
**Solution:** Press '+' to increase gain to 1.2-1.5

**Problem:** Cursor overshoots/too sensitive  
**Solution:** Press '-' to decrease gain to 0.8-0.9

**Problem:** Cursor shakes too much  
**Solution:** Press 'X' to turn smoothing ON, or press 'D' to recalibrate

**Problem:** Bottom screen hard to reach  
**Solution:** Vertical bias compensation now adds 50px boost when looking down

**Problem:** Blink not working  
**Solution:** Close ONLY left eye (keep right eye open), wait 0.5s between blinks
