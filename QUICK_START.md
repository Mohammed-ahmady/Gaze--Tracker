# 🎯 Enhanced Eye Tracking System - Quick Start Guide

## ✨ What's New

### 1. **Organized Project Structure**
```
✅ core/          - Calibration systems (separated)
✅ ui/            - Control panel & overlay (separated)
✅ enhanced_tracker.py - Main entry point
```

### 2. **15-Point Calibration System**
- **9 original points** (corners, edges, center)
- **6 new horizontal points** for better left-right tracking
- **Total: 15 points** for maximum accuracy

Grid layout:
```
●  ●  ●  ●  ●     (5 points - top)
   ●  ●  ●        (3 points - upper mid)
●  ●  ●  ●  ●     (5 points - center)
   ●  ●           (2 points - lower mid)
```

### 3. **Advanced Control Panel**
Full GUI with:
- 📹 **Live video preview**
- 📊 **Real-time status** (FPS, face detection, calibration)
- 🎛️ **Button controls** (no need to remember keys!)
- 🎨 **Color-coded interface** (green, blue, orange, red)

## 🚀 How to Run

```bash
python enhanced_tracker.py
```

That's it! The control panel will open automatically.

## 🎮 Controls

### Calibration
| Button | Function | When to Use |
|--------|----------|-------------|
| 9-Point (C) | Quick calibration | Fast setup, testing |
| 15-Point (F) | Precise calibration | Maximum accuracy |
| Add Point (R) | Single point | Fine-tune specific areas |
| Delete (D) | Reset calibration | Start fresh |

### System
| Button | Function | Effect |
|--------|----------|--------|
| Toggle Cursor (S) | Pause/Resume | Stop cursor movement temporarily |
| Toggle Smoothing (X) | Smooth on/off | More stable vs. more responsive |
| Reset Filters (Z) | Clear buffers | Fix stuck/laggy cursor |
| Gain +/- | Adjust sensitivity | Fine-tune cursor speed |
| Quit (Q) | Exit & save | Close application |

## 📊 Status Indicators

### Green ✅ = Good
- Face detected
- Calibrated
- Cursor control ON

### Red ❌ = Issue
- No face detected
- Not calibrated
- Cursor control OFF

### Orange ⚠️ = Warning
- Low FPS
- Needs calibration

## 🎯 Usage Tips

### For Best Results:
1. **Lighting**: Face should be well-lit
2. **Position**: Head 50-70cm from camera
3. **Calibration**: Use 15-point for first time
4. **Recalibrate**: If you move your head position

### Troubleshooting:
- **Cursor too fast?** → Decrease gain with `-` button
- **Cursor too slow?** → Increase gain with `+` button
- **Cursor jittery?** → Enable smoothing with `X` button
- **Cursor stuck?** → Press `Z` to reset filters

## 📁 File Structure

### Created Files
1. **`core/calibration_15point.py`** - 15-point calibration engine
2. **`ui/control_panel.py`** - Advanced GUI control panel
3. **`ui/overlay_window.py`** - Calibration overlay display
4. **`enhanced_tracker.py`** - Main application

### Existing Files (Preserved)
- `main.py` - Original basic tracker
- `integrated_eye_tracker.py` - Advanced tracker
- `calibration_system.py` - Original calibration
- `control_window.py` - Simple control window
- `overlay.py` - Simple overlay

## 🔄 Comparison

| Feature | main.py | integrated_eye_tracker.py | enhanced_tracker.py |
|---------|---------|---------------------------|---------------------|
| Calibration Points | 9 | 9 or 25 | 9 or 15 |
| Control Interface | Keyboard only | Simple window | Full GUI panel |
| Code Organization | Single file | Few files | Organized folders |
| Overlay | ❌ | ✅ | ✅ Enhanced |
| Status Display | Console | Text overlay | GUI panel |
| Button Controls | ❌ | ❌ | ✅ |
| Real-time Preview | ❌ | ✅ | ✅ Better |

## 🎓 Project Details

- **Group**: SHA Graduation Project Group 24
- **Year**: 2025/2026
- **Supervisor**: Dr. Mohammed Hussien
- **Features**: 15-point calibration, organized structure, advanced GUI

## ⚡ Quick Commands

```bash
# Run enhanced system (recommended)
python enhanced_tracker.py

# Run original system
python main.py

# Run integrated system
python integrated_eye_tracker.py
```

## 💡 Pro Tips

1. **First time users**: Start with 9-point, then try 15-point
2. **Frequent users**: 15-point calibration lasts for session
3. **Presentations**: Use 15-point for smoothest experience
4. **Development**: Folders make it easy to modify components

## ✅ What You Asked For - Delivered!

✅ **Full control window** - Advanced GUI with buttons and status
✅ **Separated code** - Organized into `core/` and `ui/` folders
✅ **15 calibration points** - Enhanced with horizontal mid-points
✅ **Clean structure** - Easy to understand and modify

Enjoy your enhanced eye tracking system! 🎉
