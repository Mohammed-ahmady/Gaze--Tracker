# 🚀 Quick Installation Guide

Choose the installation method that works best for you:

---

## Method 1: Smart Installer ⭐ RECOMMENDED

**Works on any Python 3.7-3.12. Auto-detects your version and installs compatible packages.**

### Windows (PowerShell):
```powershell
# Check compatibility first
python check_compatibility.py

# If compatible, install everything
python install_smart.py

# Or use automated setup script
.\setup.ps1
```

### Linux/Mac (Bash):
```bash
# Check compatibility first
python3 check_compatibility.py

# If compatible, install everything
python3 install_smart.py

# Or use automated setup script
chmod +x setup.sh
./setup.sh
```

---

## Method 2: Manual Install

**If you know you have Python 3.9-3.12:**

```bash
# Version 1 (Basic)
cd version1
pip install -r requirements.txt
python main.py

# Version 2 (Advanced)
cd version2
pip install -r requirements.txt
python enhanced_tracker.py
```

---

## Method 3: Virtual Environment (Safest)

**Isolates GazeAssist from other Python projects:**

### Windows:
```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install
python install_smart.py

# Run
cd version1  # or version2
python main.py
```

### Linux/Mac:
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install
python install_smart.py

# Run
cd version1  # or version2
python main.py
```

---

## Method 4: Conda (Most Reliable)

**Best for data science users or complex environments:**

```bash
# Create environment with all dependencies
conda env create -f environment.yml

# Activate environment
conda activate gazeassist

# Run
python version1/main.py
# or
python version2/enhanced_tracker.py
```

---

## Method 5: Docker (True Cross-Platform)

**Works on any OS with Docker installed:**

```bash
# Build container
docker build -t gazeassist .

# Run with webcam access
# Linux:
docker run -it --device=/dev/video0 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    gazeassist python version1/main.py

# Windows (requires WSL2 + Docker Desktop):
docker run -it gazeassist python version1/main.py
```

---

## ⚠️ Troubleshooting

### "No matching distribution found for mediapipe"

**You have Python 3.13 or higher** - MediaPipe doesn't support it yet.

**Fix:**
1. Download Python 3.11 or 3.12: https://www.python.org/downloads/
2. Install to separate directory (e.g., `C:\Python312`)
3. Use that version:
   ```bash
   C:\Python312\python.exe check_compatibility.py
   C:\Python312\python.exe install_smart.py
   ```

### "ModuleNotFoundError" after installation

**Packages didn't install correctly.**

**Fix:**
```bash
# Verify installation
python -c "import cv2, mediapipe, numpy, pyautogui; print('OK')"

# If it fails, reinstall
python install_smart.py
```

### Camera not working

**Test camera first:**
```bash
python scripts/test_camera.py
```

---

## 🎯 Recommended Path for Beginners

1. **Check compatibility**: `python check_compatibility.py`
2. **Run setup script**: 
   - Windows: `.\setup.ps1`
   - Linux/Mac: `./setup.sh`
3. **Test camera**: `python scripts/test_camera.py`
4. **Run Version 1**: `python version1/main.py`

---

## 🎓 Recommended Path for Advanced Users

1. **Use Conda**: `conda env create -f environment.yml`
2. **Activate**: `conda activate gazeassist`
3. **Run Version 2**: `python version2/enhanced_tracker.py`

---

## Need More Help?

- **Installation issues**: See [version1/INSTALL.md](version1/INSTALL.md) or [version2/INSTALL.md](version2/INSTALL.md)
- **Usage help**: See [version1/MANUAL.md](version1/MANUAL.md) or [version2/MANUAL.md](version2/MANUAL.md)
- **GitHub Issues**: https://github.com/Mohammed-ahmady/Gaze--Tracker/issues
