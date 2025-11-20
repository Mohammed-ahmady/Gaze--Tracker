# Enhanced Eye Tracking System - Project Structure

## 📁 Project Organization

```
GazeAssistsudo/
│
├── core/                          # Core calibration systems
│   ├── __init__.py
│   └── calibration_15point.py    # 15-point calibration system
│
├── ui/                            # User interface components
│   ├── __init__.py
│   ├── control_panel.py          # Advanced control panel with GUI
│   └── overlay_window.py         # Calibration overlay window
│
├── enhanced_tracker.py            # Main tracker with 15-point calibration
├── main.py                        # Original eye tracker
├── integrated_eye_tracker.py     # Advanced integrated tracker
├── calibration_system.py         # Original calibration system
├── control_window.py             # Simple control window
└── overlay.py                     # Simple overlay
```

## 🎯 15-Point Calibration Grid

The new system uses an enhanced 15-point calibration grid for better accuracy:

```
1  2  3  4  5     (Top row - 5 points)
   6  7  8        (Upper middle - 3 points)
9  10 11 12 13    (Center row - 5 points)
   14 15          (Lower middle - 2 points)
```

This provides:
- **Better horizontal coverage** with 5 points on key rows
- **Enhanced center tracking** with additional mid-row points
- **Improved accuracy** across the entire screen

## 🚀 Running the Enhanced System

### Quick Start

```bash
python enhanced_tracker.py
```

### Features

1. **Advanced Control Panel**
   - Real-time video preview
   - System status monitoring
   - Button controls for all functions
   - Live FPS, face detection, and cursor position display

2. **15-Point Calibration**
   - Press `C` for 9-point calibration (quick)
   - Press `F` for 15-point calibration (precise)
   - Visual overlay during calibration
   - Progress indicators and completion percentage

3. **System Controls**
   - `S` - Toggle cursor control on/off
   - `X` - Toggle smoothing
   - `Z` - Reset smoothing filters
   - `+/-` - Adjust gain (sensitivity)
   - `R` - Add single calibration point
   - `D` - Delete calibration and restart
   - `Q` - Quit and save

## 📊 Control Panel Features

### Status Display
- **Mode**: Current operation mode (Tracking/Calibration)
- **FPS**: Real-time frames per second
- **Face Detection**: ✓ Detected or ✗ No Face
- **Calibration Status**: ✓ Calibrated or ✗ Not Calibrated
- **Cursor Control**: ON/OFF status
- **Smoothing**: ON/OFF status
- **Gain**: Current sensitivity multiplier
- **Cursor Position**: Real-time cursor coordinates

### Control Buttons
- Color-coded buttons for easy identification
- Green: Primary actions (9-point calibration)
- Blue: Advanced actions (15-point calibration)
- Orange: Additional features (add point)
- Red: Destructive actions (delete calibration)
- Purple/Cyan: System toggles

## 🔧 Technical Details

### Calibration System (`core/calibration_15point.py`)
- **Polynomial regression** with Ridge regularization
- **6 features**: Left eye (2), Right eye (2), Nose (2)
- **Smoothing buffer** for stable cursor movement
- **Adjustable gain** for sensitivity control
- **Save/Load** calibration data persistence

### Control Panel (`ui/control_panel.py`)
- **Tkinter-based GUI** with modern styling
- **Threading** for smooth UI updates
- **Real-time video preview** with 480x360 display
- **Command queue** system for reliable control
- **Status monitoring** with color-coded indicators

### Overlay Window (`ui/overlay_window.py`)
- **Fullscreen transparent overlay** (85% opacity)
- **Animated calibration points** with pulsing effect
- **Progress rings** showing completion percentage
- **Point numbering** and status indicators
- **ESC to cancel** functionality

## 📦 Dependencies

```
opencv-python
mediapipe
pyautogui
numpy
scikit-learn
Pillow
tkinter (included with Python)
```

## 🎓 Project Information

- **Group**: SHA Graduation Project Group 24
- **Academic Year**: 2025/2026
- **Supervisor**: Dr. Mohammed Hussien

## 🔄 Upgrade Path

If you're using the old system:

1. **From `main.py`**: Basic 9-point calibration, simple controls
2. **From `integrated_eye_tracker.py`**: Advanced calibration with control window
3. **To `enhanced_tracker.py`**: Full GUI, 15-point calibration, organized structure

## 📝 Notes

- Calibration files are saved separately for 9-point and 15-point systems
- The control panel runs in a separate thread for responsiveness
- All components are modular and can be used independently
- The system automatically falls back to simple mapping if calibration fails

## 🐛 Troubleshooting

**Control panel not appearing?**
- Check if tkinter is installed: `python -m tkinter`
- Ensure threading is not blocked by antivirus

**Calibration overlay not showing?**
- May require administrator privileges on some systems
- Check if fullscreen windows are allowed

**Low FPS?**
- Reduce camera resolution in enhanced_tracker.py
- Disable smoothing temporarily
- Check CPU usage

## 🎯 Best Practices

1. **Calibration**:
   - Use 9-point for quick setup
   - Use 15-point for maximum accuracy
   - Recalibrate if you move your head position

2. **Usage**:
   - Keep head relatively still
   - Ensure good lighting on your face
   - Adjust gain if cursor is too sensitive or sluggish

3. **Performance**:
   - Close other applications using the camera
   - Reduce window size if experiencing lag
   - Use smoothing for stable cursor movement
