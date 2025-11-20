# 📋 GazeAssist - Quick Reference Card

## 🚀 Installation (One Command!)

```bash
python check_compatibility.py  # Check if your Python works
python install_smart.py        # Install everything automatically
```

**Or use setup script:**
- Windows: `.\setup.ps1`
- Linux/Mac: `./setup.sh`

---

## ✅ What Python Versions Work?

| Version | Status | Notes |
|---------|--------|-------|
| 3.7 | ✅ Works | MediaPipe 0.8.11 |
| 3.8 | ✅ Works | MediaPipe 0.10.0 |
| 3.9 | ✅ Works | MediaPipe 0.10.8 |
| 3.10 | ✅ Works | MediaPipe 0.10.9 |
| 3.11 | ✅ Works | MediaPipe 0.10.9 |
| 3.12 | ✅ Works | MediaPipe 0.10.9 |
| 3.13+ | ❌ NO | Not supported yet |

---

## 🎮 Running the Program

### Version 1 (Basic - 9 points, voice guidance):
```bash
cd version1
python main.py
```

### Version 2 (Advanced - 21 points, ML, control panel):
```bash
cd version2
python enhanced_tracker.py
```

---

## 🎯 Keyboard Controls

| Key | Action |
|-----|--------|
| **C** | Toggle cursor control ON/OFF |
| **D** | Delete calibration and recalibrate |
| **S** | Save current calibration |
| **Q** | Quit and save logs |
| **F** | Toggle smoothing (V2 only) |
| **G** | Toggle raw gaze overlay (V2 only) |

---

## 🔧 Diagnostic Tools

```bash
# Test camera
python scripts/test_camera.py

# Test eye movement detection
python scripts/diagnose_eye_movement.py

# Analyze session logs (V2 only)
python scripts/deep_analysis.py
```

---

## ⚠️ Common Issues

### "No matching distribution found for mediapipe"
**→ You have Python 3.13 - it's not supported yet**

**Fix:** Install Python 3.12 and use it:
```bash
C:\Python312\python.exe check_compatibility.py
C:\Python312\python.exe install_smart.py
```

### Poor tracking accuracy
1. Run diagnostic: `python scripts/diagnose_eye_movement.py`
2. Check ranges (need >0.4 vertical, >0.5 horizontal)
3. Improve lighting and camera position
4. Look at EXTREME edges during calibration

### Camera not detected
```bash
# Test camera first
python scripts/test_camera.py

# Check permissions
# Windows: Settings > Privacy > Camera
```

---

## 📦 Alternative Installation Methods

### Virtual Environment (Isolated):
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
python install_smart.py
```

### Conda (Most Reliable):
```bash
conda env create -f environment.yml
conda activate gazeassist
```

### Docker (Cross-Platform):
```bash
docker build -t gazeassist .
docker run -it gazeassist
```

---

## 📚 Documentation

- **Installation**: [QUICK_INSTALL.md](QUICK_INSTALL.md)
- **Version 1**: [version1/README.md](version1/README.md) | [version1/MANUAL.md](version1/MANUAL.md)
- **Version 2**: [version2/README.md](version2/README.md) | [version2/MANUAL.md](version2/MANUAL.md)

---

## 🆘 Getting Help

1. Check compatibility: `python check_compatibility.py`
2. Read error messages carefully
3. See [QUICK_INSTALL.md](QUICK_INSTALL.md) for detailed troubleshooting
4. GitHub Issues: https://github.com/Mohammed-ahmady/Gaze--Tracker/issues

---

**Ready? Start here:** `python check_compatibility.py` 🚀
