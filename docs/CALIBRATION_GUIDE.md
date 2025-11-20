# Calibration Tips for Best Accuracy

## 🎯 Current Improvements

### What's Been Enhanced:
1. **Polynomial Degree 3** - Better vertical and non-linear mapping
2. **Edge Weighting** - Corners/edges get 9x more emphasis during training
3. **21 Calibration Points** - Full screen coverage including all corners
4. **Very Low Regularization** (alpha=0.01) - Model fits tightly to your data
5. **10 Features** - Advanced eye tracking with head compensation

---

## ✅ How to Get Perfect Calibration

### Before Calibration:
1. **Delete old calibration files:**
   ```powershell
   Remove-Item calibration_15point.*
   ```

2. **Run setup wizard** - DON'T SKIP!
   - Distance: 50-60cm (arm's length)
   - Face centered
   - Head straight
   - Good lighting on your face

### During Calibration:
1. **Follow each dot PRECISELY**
   - Look DIRECTLY at the center of the red dot
   - Don't just glance - FOCUS on it
   - Keep your head STILL (only move eyes)

2. **Corners are CRITICAL**
   - Points 1, 5, 17, 21 are the 4 corners
   - Really LOOK at these - they get 9x weight
   - Don't approximate - FOCUS hard

3. **Top and Bottom Rows**
   - Points 1-5: Top edge
   - Points 17-21: Bottom edge  
   - These fix vertical tracking

4. **Stay Still**
   - Don't move head between points
   - Same distance throughout
   - Maintain posture

### After Calibration:
1. **Check error message:**
   - X error should be < 30px
   - Y error should be < 30px
   - If higher → Recalibrate (press 'D')

2. **Test all areas:**
   - Move cursor to all 4 corners
   - Test top edge
   - Test bottom edge
   - Test center

3. **Adjust if needed:**
   - Press '+' to increase gain if can't reach edges
   - Press '-' to decrease if overshooting

---

## 🔧 Calibration Grid Layout

```
1       2       3       4       5          ← Top edge (y=5%)
    6       7       8                      ← Upper-mid (y=30%)
9       10      11      12      13         ← Center (y=50%)
    14      15      16                     ← Lower-mid (y=70%)
17      18      19      20      21         ← Bottom edge (y=95%)
```

**Critical points for corners:**
- Point 1: Top-left corner
- Point 5: Top-right corner
- Point 17: Bottom-left corner
- Point 21: Bottom-right corner

**Critical points for vertical:**
- Points 1, 2, 3, 4, 5: Top edge
- Points 17, 18, 19, 20, 21: Bottom edge

---

## 🐛 Common Issues & Fixes

### "Left/Right works but Up/Down sucks"
**Cause:** Not focusing on top/bottom edge points  
**Fix:**  
- Recalibrate (press 'D')
- When you see points 1-5 (top row) - REALLY look at them
- When you see points 17-21 (bottom row) - REALLY look at them
- Don't estimate - your eyes must actually move there

### "Corners not even close"
**Cause:** Not looking at extreme corners during calibration  
**Fix:**
- Recalibrate (press 'D')
- Points 1, 5, 17, 21 are corners
- Move your EYES to the corner (not just glance)
- These points have 9x weight now - they matter most!

### "Everything is offset"
**Cause:** Head moved during calibration  
**Fix:**
- Keep head PERFECTLY STILL
- Use headrest or stable chair
- Only move EYES, not HEAD

### "Model says high error (>50px)"
**Cause:** Inconsistent calibration  
**Fix:**
- You may have moved during calibration
- Lighting changed
- Press 'D' and recalibrate more carefully

---

## 📊 Technical Details

### Edge Weighting Formula:
```python
distance_from_center = sqrt((x - 0.5)² + (y - 0.5)²)
weight = 1.0 + distance_from_center * 8.0

# Center point: weight = 1.0
# Edge point: weight ≈ 5.0
# Corner point: weight ≈ 9.0
```

### Polynomial Features:
- **Degree 3** creates 286 polynomial combinations
- Captures complex non-linear eye-to-screen mapping
- Better for vertical movement (looking up/down)

### Sample Averaging:
- 60 frames per calibration point
- All 60 frames averaged to 1 stable point
- Reduces noise and jitter
- Total: 21 points × 60 frames = 1260 samples → 21 averaged points

---

## 💡 Pro Tips

### For Best Vertical Tracking:
1. During calibration, MOVE YOUR EYES vertically
2. Don't tilt head up/down - move EYES
3. Focus on top row (1-5) and bottom row (17-21)
4. The model learns from YOUR eye movement

### For Best Corner Accuracy:
1. Corner points (1, 5, 17, 21) have 9x importance
2. Actually move your eyes to the EXTREME corner
3. Don't just glance - LOOK at it for all 60 frames
4. Keep head centered while eyes go to corner

### For Consistent Results:
1. Same chair height every time
2. Same distance (50-60cm)
3. Same lighting
4. Same head position
5. Save calibration after getting good results

---

## 🎮 Quick Calibration Workflow

```
1. Delete old calibration
   → powershell: Remove-Item calibration_15point.*

2. Run enhanced_tracker.py
   → Setup wizard appears

3. Position yourself (follow guides)
   → Press SPACE when all checks pass

4. Calibration starts (21 points)
   → FOCUS on each dot
   → Especially corners and edges
   → Keep head STILL

5. Check error message
   → Should be < 30px for X and Y
   → If not, press 'D' and try again

6. Test cursor
   → Try all 4 corners
   → Try top and bottom edges
   → Press 'G' to see raw gaze overlay

7. Adjust gain if needed
   → '+' for more sensitivity
   → '-' for less sensitivity

8. Done! 
   → Press 'Q' to save and quit
```

---

## Expected Results

After proper calibration:
- ✅ Cursor reaches all 4 corners
- ✅ Top edge accessible  
- ✅ Bottom edge accessible
- ✅ Smooth vertical movement
- ✅ Smooth horizontal movement
- ✅ Error < 30px in X and Y
- ✅ Raw gaze overlay matches cursor position

If you're not getting these results, **recalibrate more carefully** focusing on the corner and edge points!
