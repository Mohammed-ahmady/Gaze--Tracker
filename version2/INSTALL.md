# Installation Guide - Version 2

## ⚠️ IMPORTANT: Python Version Requirement

**This project requires Python 3.9, 3.10, 3.11, or 3.12**

**❌ Python 3.13+ is NOT supported** because MediaPipe (the eye tracking library) doesn't support it yet.

---

## Step 1: Check Your Python Version

```bash
python --version
```

### If you have Python 3.13:

You need to install an older Python version. Here are your options:

#### Option A: Download Python 3.12 (Recommended)
1. Go to https://www.python.org/downloads/
2. Download **Python 3.12.x** (latest 3.12 version)
3. During installation, check "Add Python 3.12 to PATH"
4. Install to a different directory (e.g., `C:\Python312\`)

#### Option B: Use pyenv (Advanced)
Install Python version manager to switch between versions easily.

---

## Step 2: Install Dependencies

Once you have the correct Python version:

```bash
# Make sure you're using Python 3.9-3.12
python --version

# Install required packages
pip install -r requirements.txt
```

### If you get "No matching distribution found for mediapipe":
This means you're still using Python 3.13 or another incompatible version.

**Solution:**
```bash
# Use specific Python installation
C:\Python312\python.exe -m pip install -r requirements.txt

# Or if you have multiple Python versions
py -3.12 -m pip install -r requirements.txt
```

---

## Step 3: Run the Program

```bash
# Using the correct Python version
python enhanced_tracker.py

# Or specify the Python installation
C:\Python312\python.exe enhanced_tracker.py
# Or
py -3.12 enhanced_tracker.py
```

---

## Common Installation Issues

### Error: "No module named 'mediapipe'"
**Cause:** Wrong Python version (3.13+) or packages not installed

**Fix:**
```bash
# Check Python version first
python --version

# If it shows 3.13, use a different Python installation
C:\Python312\python.exe -m pip install -r requirements.txt
C:\Python312\python.exe enhanced_tracker.py
```

### Error: "ModuleNotFoundError: No module named 'sklearn'"
**Fix:**
```bash
pip install scikit-learn
```

### Error: "No module named 'tkinter'"
**Cause:** tkinter not included with your Python installation

**Fix:**
- Windows: Reinstall Python and check "tcl/tk and IDLE" during installation
- Linux: `sudo apt-get install python3-tk`

---

## Quick Start for Different Devices

### On a fresh Windows machine:

1. **Download Python 3.12**: https://www.python.org/downloads/release/python-3120/
2. **Install Python** (check "Add to PATH" and "tcl/tk and IDLE")
3. **Download this project** from GitHub
4. **Open PowerShell** in the `version2` folder
5. **Run:**
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python enhanced_tracker.py
   ```

---

## Verifying Installation

Run this to verify all packages are installed correctly:

```bash
python -c "import cv2, mediapipe, numpy, sklearn, pyautogui; print('All packages installed successfully!')"
```

If you see "All packages installed successfully!" - you're ready to go! 🎉

---

## Virtual Environment (Recommended for Advanced Users)

To avoid conflicts with other Python projects:

```bash
# Create virtual environment with Python 3.12
py -3.12 -m venv venv

# Activate it
.\venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run the program
python enhanced_tracker.py
```

---

## Still Having Issues?

1. Make sure you're using **Python 3.9-3.12** (NOT 3.13+)
2. Update pip: `python -m pip install --upgrade pip`
3. Install Visual C++ redistributables: https://aka.ms/vs/17/release/vc_redist.x64.exe
4. Try installing packages one by one:
   ```bash
   pip install opencv-python
   pip install mediapipe
   pip install numpy
   pip install scikit-learn
   pip install scipy
   pip install pyautogui
   pip install Pillow
   ```
5. Check the main README.md troubleshooting section
