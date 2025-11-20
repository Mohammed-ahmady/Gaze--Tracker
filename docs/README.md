# GazeAssist - Eye Tracking System
SHA Graduation Project Group 24 (2025/2026)

## Quick Start

### Run Eye Tracker
```powershell
python main.py
```

### Diagnose Eye Movement
```powershell
python scripts/diagnose_eye_movement.py
```

### Analyze Logs
```powershell
python scripts/deep_analysis.py
```

## Project Structure

- **main.py** - Main entry point (run this)
- **enhanced_tracker.py** - Core eye tracking system
- **calibration_system.py** - Calibration module
- **control_window.py** - GUI control panel
- **overlay.py** - Calibration overlay
- **integrated_eye_tracker.py** - Legacy tracker
- **core/** - Core tracking modules
- **ui/** - User interface components
- **scripts/** - Utility scripts (analysis, diagnostics)
- **docs/** - Documentation and guides
- **logs/** - Session logs and tracking data
- **data/** - Calibration data
- **config/** - Configuration files

## Documentation

See **docs/** folder for:
- Calibration guides
- Technical details
- Project proposals
- Improvements and enhancements

## Controls

- **C** - Toggle cursor control
- **F** - Toggle smoothing filter
- **D** - Delete calibration
- **S** - Save calibration
- **X** - Toggle smoothing on/off
- **G** - Toggle raw gaze overlay
- **Z** - Reset smoothing filters
- **+/-** - Adjust output gain
- **Q** - Quit and save

## Requirements

```powershell
pip install -r requirements.txt
```
