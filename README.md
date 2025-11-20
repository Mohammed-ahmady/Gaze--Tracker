# 👁️ GazeAssist - Eye Tracking Cursor Control System

**SHA Graduation Project Group 24 (2025/2026)**

Control your computer cursor using only your eyes! This project provides two versions of an eye tracking system built with MediaPipe and machine learning.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.8-green.svg)](https://mediapipe.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📦 What's Inside?

This repository contains **two complete versions** of the eye tracking system:

> **⚠️ IMPORTANT:** Requires **Python 3.9, 3.10, 3.11, or 3.12** (NOT Python 3.13+)  
> MediaPipe doesn't support Python 3.13 yet. See installation guides below.

### **Version 1 - Basic Eye Tracker** 🎯
- Simple 9-point calibration
- Ratio-based gaze mapping
- Voice guidance during calibration
- Perfect for beginners and quick setup
- **➡️ [Go to Version 1](./version1/)** | **[Installation Guide](./version1/INSTALL.md)**

### **Version 2 - Advanced Eye Tracker** 🚀
- ML-powered 21-point calibration
- Polynomial regression for accurate tracking
- Advanced control panel with live adjustments
- Comprehensive logging and diagnostics
- Real-time performance monitoring
- **➡️ [Go to Version 2](./version2/)** | **[Installation Guide](./version2/INSTALL.md)**

---

## 🚀 Quick Start

### Method 1: Smart Installer ⭐ RECOMMENDED

**One command install - works with Python 3.7-3.12:**

```bash
# 1. Clone the repository
git clone https://github.com/Mohammed-ahmady/Gaze--Tracker.git
cd Gaze--Tracker

# 2. Check if your Python is compatible
python check_compatibility.py

# 3. Install everything automatically
python install_smart.py

# 4. Run your chosen version
python version1/main.py              # Basic version
python version2/enhanced_tracker.py   # Advanced version
```

**Or use the automated setup script:**
- **Windows**: `.\setup.ps1`
- **Linux/Mac**: `chmod +x setup.sh && ./setup.sh`

### Method 2: Manual Install

**If you have Python 3.9-3.12:**

```bash
cd version1  # or version2
pip install -r requirements.txt
python main.py  # or enhanced_tracker.py
```

### Method 3: Conda (Most Reliable)

```bash
conda env create -f environment.yml
conda activate gazeassist
python version1/main.py
```

### Method 4: Docker (Cross-Platform)

```bash
docker build -t gazeassist .
docker run -it gazeassist python version1/main.py
```

**📖 Full installation guide:** [QUICK_INSTALL.md](./QUICK_INSTALL.md)

---

### ⚠️ Prerequisites
- **Python 3.7-3.12** (NOT 3.13+) - MediaPipe limitation
- **Webcam** (720p or better recommended)
- **Windows 10/11, Linux, or macOS**

> **Have Python 3.13?** The smart installer will detect this and show you how to fix it.

3. **Follow the on-screen setup wizard**
   - Position your camera at eye level
   - Ensure good lighting
   - Complete calibration
   - Start tracking!

---

## 📖 Documentation

Each version has complete documentation:

- **🚀 [Quick Installation Guide](./QUICK_INSTALL.md)** - All installation methods
- **[Version 1 README](./version1/README.md)** - Features, installation, usage
- **[Version 1 INSTALL](./version1/INSTALL.md)** - Detailed installation troubleshooting
- **[Version 1 MANUAL](./version1/MANUAL.md)** - Complete user guide
- **[Version 2 README](./version2/README.md)** - Features, installation, usage  
- **[Version 2 INSTALL](./version2/INSTALL.md)** - Detailed installation troubleshooting
- **[Version 2 MANUAL](./version2/MANUAL.md)** - Comprehensive manual with advanced features

---

## 🛠️ Diagnostic Tools

Both versions include diagnostic tools in the `scripts/` directory:

### Test Eye Movement Detection
```bash
python scripts/diagnose_eye_movement.py
```
Verify your camera can detect full eye movement range before calibration.

### Analyze Tracking Sessions (Version 2 only)
```bash
python scripts/deep_analysis.py
```
Get detailed analysis of calibration quality and tracking performance.

---

## 🎮 Basic Controls

| Key | Action |
|-----|--------|
| **C** | Toggle cursor control ON/OFF |
| **F** | Toggle smoothing filter (Version 2) |
| **D** | Delete calibration and recalibrate |
| **S** | Save current calibration |
| **X** | Toggle smoothing ON/OFF |
| **G** | Toggle raw gaze overlay (Version 2) |
| **Z** | Reset smoothing filters (Version 2) |
| **+/-** | Adjust output gain (Version 2) |
| **Q** | Quit and save logs |

---

## 📁 Project Structure

```
Gaze--Tracker/
│
├── version1/                 # 🎯 Basic Eye Tracker
│   ├── main.py                   # Main program
│   ├── README.md                 # Features & quick start
│   ├── MANUAL.md                 # Detailed user guide
│   └── requirements.txt          # Dependencies
│
├── version2/                 # 🚀 Advanced Eye Tracker
│   ├── enhanced_tracker.py       # Main program
│   ├── core/                     # Core tracking modules
│   │   ├── calibration_15point.py
│   │   └── eye_tracking_logger.py
│   ├── ui/                       # User interface
│   │   ├── control_panel.py
│   │   ├── overlay_window.py
│   │   ├── setup_wizard.py
│   │   └── raw_gaze_overlay.py
│   ├── README.md                 # Features & quick start
│   ├── MANUAL.md                 # Comprehensive manual
│   └── requirements.txt          # Dependencies
│
├── scripts/                  # 🛠️ Diagnostic Tools
│   ├── diagnose_eye_movement.py  # Test eye detection
│   ├── deep_analysis.py          # Session analyzer
│   ├── analyze_logs.py           # Log analyzer
│   └── test_camera.py            # Camera test
│
├── docs/                     # 📚 Documentation & Research
│   ├── CALIBRATION_GUIDE.md
│   ├── LOGGING_COMPLETE.md
│   └── ...project proposals & PDFs
│
├── logs/                     # 📊 Auto-generated session logs
├── data/                     # 💾 Calibration data storage
├── config/                   # ⚙️ Configuration files
└── legacy/                   # 📦 Old versions (archived)
```

---

## 🎯 Which Version Should I Use?

| Feature | Version 1 | Version 2 |
|---------|-----------|-----------|
| Setup Difficulty | ⭐ Easy | ⭐⭐ Moderate |
| Calibration Points | 9 points | 21 points |
| Tracking Method | Ratio-based | ML-powered |
| Accuracy | Good | Excellent |
| Voice Guidance | ✅ Yes | ❌ No |
| Control Panel | ❌ No | ✅ Yes |
| Session Logging | ❌ Basic | ✅ Comprehensive |
| Diagnostics | ❌ No | ✅ Yes |
| Best For | Quick testing | Production use |

**Recommendation:** Start with Version 1 to test if eye tracking works for you, then upgrade to Version 2 for better accuracy and features.

---

## 🔧 Troubleshooting

### Camera Issues
- Ensure webcam is connected and working
- Run `python scripts/test_camera.py` to verify
- Check camera permissions in Windows settings

### Poor Tracking Accuracy
1. Run diagnostic: `python scripts/diagnose_eye_movement.py`
2. Verify eye movement ranges are >0.4 vertical and >0.5 horizontal
3. If ranges are low:
   - Improve lighting (bright, even, no glare)
   - Adjust camera position (eye level, 50-70cm away)
   - Clean camera lens
4. During calibration, look at EXTREME edges of each dot

### Installation Issues
- Use Python 3.9 or higher: `python --version`
- Update pip: `python -m pip install --upgrade pip`
- Install Visual C++ redistributables (for MediaPipe)

### ⚠️ Error: "No matching distribution found for mediapipe"
**You're using Python 3.13** - MediaPipe doesn't support it yet.

**Fix:** Install and use Python 3.12:
1. Download from https://www.python.org/downloads/release/python-3120/
2. Install to `C:\Python312\`
3. Use that version:
   ```bash
   C:\Python312\python.exe -m pip install -r requirements.txt
   C:\Python312\python.exe main.py
   ```

See detailed installation guides:
- **[Version 1 Installation Guide](./version1/INSTALL.md)**
- **[Version 2 Installation Guide](./version2/INSTALL.md)**

For detailed troubleshooting, see the MANUAL.md files in each version folder.

---

## 📊 Features Comparison

### Version 1 Features
- ✅ Simple 9-point calibration
- ✅ Voice-guided setup (pyttsx3)
- ✅ Basic gaze tracking
- ✅ Cursor control
- ✅ Minimal dependencies
- ✅ Fast startup

### Version 2 Features
- ✅ Advanced 21-point calibration
- ✅ Machine learning (Ridge Regression + Polynomial Features)
- ✅ Edge-weighted calibration (9× corners, 5× edges)
- ✅ Real-time control panel
- ✅ Comprehensive session logging
- ✅ Tracking analysis tools
- ✅ Multi-stage smoothing (deque + exponential + outlier detection)
- ✅ Raw gaze overlay
- ✅ Setup wizard
- ✅ Training error metrics
- ✅ Performance monitoring

---

## 🤝 Contributing

This is a graduation project, but we welcome:
- Bug reports
- Feature suggestions
- Documentation improvements
- Testing feedback

Please open an issue to discuss before submitting pull requests.

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👥 Authors

**SHA Graduation Project - Group 24 (2025/2026)**

---

## 🙏 Acknowledgments

- **MediaPipe** for face mesh and iris tracking
- **OpenCV** for computer vision utilities
- **scikit-learn** for machine learning models
- Research papers in `docs/` folder for theoretical foundation

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Mohammed-ahmady/Gaze--Tracker/issues)
- **Documentation:** See `docs/` folder
- **Version 1 Manual:** [version1/MANUAL.md](./version1/MANUAL.md)
- **Version 2 Manual:** [version2/MANUAL.md](./version2/MANUAL.md)

---

## 🚦 Getting Started Checklist

- [ ] **Clone repository**: `git clone https://github.com/Mohammed-ahmady/Gaze--Tracker.git`
- [ ] **Check Python compatibility**: `python check_compatibility.py`
- [ ] **Install packages**: `python install_smart.py` (or use `setup.ps1`/`setup.sh`)
- [ ] **Test camera**: `python scripts/test_camera.py`
- [ ] **Test eye detection**: `python scripts/diagnose_eye_movement.py`
- [ ] **Setup environment**: Good lighting, camera at eye level (50-70cm away)
- [ ] **Choose version**: Version 1 (simple) or Version 2 (advanced)
- [ ] **Read the manual**: [version1/MANUAL.md](./version1/MANUAL.md) or [version2/MANUAL.md](./version2/MANUAL.md)
- [ ] **Run calibration**: Follow on-screen instructions carefully
- [ ] **Start tracking**: Press 'C' to enable cursor control!

---

**Ready to control your cursor with your eyes? Pick a version and get started! 👁️🖱️**
   - Check vertical/horizontal ranges (> 0.4 and > 0.5)
   - Read recommendations

### Calibration Tips

✅ **DO:**
- Keep head completely still
- Move ONLY your eyes
- Look directly AT each red circle
- Feel your eyes strain to extreme positions
- Wait for green before moving eyes

❌ **DON'T:**
- Move your head
- Just glance at points
- Rush through calibration
- Look near the points instead of AT them

---

## 📈 Features

- **21-point calibration** with edge weighting
- **Polynomial regression** (degree 3) for accurate mapping
- **10 engineered features** for enhanced accuracy
- **Advanced smoothing** with outlier detection
- **Blink detection** for clicking (left eye wink)
- **Smart blink disable** when looking down
- **Setup wizard** for optimal positioning
- **Raw gaze overlay** for debugging
- **Comprehensive logging** for analysis
- **Real-time control panel** with live preview

---

## 📊 System Requirements

- Python 3.8+
- Webcam (640x480 minimum)
- Windows 10/11 (PowerShell)
- Good lighting conditions
- 50-70cm from camera

### Python Packages
- mediapipe
- opencv-python
- numpy
- scikit-learn
- pyautogui
- tkinter (usually included)

---

## 📝 Logging & Analysis

All sessions are automatically logged to `logs/session_YYYYMMDD_HHMMSS/`:

- `session.log` - Main events, calibration info, training errors
- `calibration.json` - All calibration samples (21 points × 60 frames)
- `tracking.csv` - Every 10th tracking frame with eye/cursor positions
- `errors.log` - Any errors that occurred
- `analysis.txt` - Auto-generated analysis with recommendations

To analyze latest session:
```powershell
python scripts/deep_analysis.py
```

---

## 🎓 Academic Context

**Project:** Eye Tracking for Computer Cursor Control  
**Institution:** SHA University  
**Group:** 24  
**Year:** 2025/2026  
**Supervisor:** Dr. Mohammed Hussien

---

## 📚 Documentation

See `docs/` folder for:
- `QUICK_START.md` - Getting started guide
- `CALIBRATION_GUIDE.md` - Detailed calibration instructions
- `ADVANCED_CALIBRATION_GUIDE.md` - Advanced techniques
- `LOGGING_COMPLETE.md` - Logging system documentation
- `TECHNICAL_DETAILS.md` - Technical implementation details
- Project proposals and references

---

## 🐛 Known Issues & Solutions

### Issue: "Vertical tracking doesn't work"
**Cause:** Not moving eyes up/down during calibration  
**Solution:** Use diagnostic tool, then recalibrate with EXTREME eye movements

### Issue: "Cursor is shaky"
**Cause:** Too much smoothing or camera issues  
**Solution:** Press 'X' to toggle smoothing, improve lighting

### Issue: "Can't reach screen corners"
**Cause:** Limited eye movement during calibration  
**Solution:** Recalibrate, move eyes to EXTREME positions at corner points

### Issue: "Blink triggers when looking down"
**Cause:** Eye aspect ratio drops when squinting  
**Solution:** Smart blink disable is enabled (automatic)

---

## 🔬 Technical Details

- **Face Detection:** MediaPipe Face Mesh (468 landmarks + iris)
- **Eye Tracking:** Iris relative to eye boundaries
- **ML Model:** Ridge Regression with PolynomialFeatures (degree=3, alpha=0.01)
- **Features:** Left eye (2), Right eye (2), Avg eye (2), Eye diff (2), Nose (2)
- **Smoothing:** Deque-based (7 frames) + exponential (0.5) + outlier detection (200px)
- **Calibration:** 21 points with edge weighting (9x corners, 5x edges)
- **Blink Detection:** EAR < 0.15 (disabled when looking down)

---

## 📞 Support

For issues:
1. Run diagnostics: `python scripts/diagnose_eye_movement.py`
2. Analyze logs: `python scripts/deep_analysis.py`
3. Check `logs/latest/analysis.txt` for recommendations
4. Review `docs/TROUBLESHOOTING.md`

---

**Made with 👁️ by SHA Group 24**
