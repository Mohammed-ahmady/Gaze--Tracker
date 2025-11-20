"""
GazeAssist Smart Installer
Automatically detects your Python version and installs compatible packages
"""
import sys
import subprocess
import os

def get_python_version():
    """Get current Python version as tuple (major, minor)."""
    return sys.version_info[:2]

def run_pip_command(args):
    """Run pip command and handle errors."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip"] + args)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def install_packages():
    """Install packages based on Python version."""
    py_version = get_python_version()
    
    print("=" * 70)
    print(" " * 25 + "GazeAssist Smart Installer")
    print("=" * 70)
    print(f"\n📌 Detected Python {py_version[0]}.{py_version[1]}")
    print(f"   Location: {sys.executable}")
    
    # MediaPipe compatibility matrix
    # Based on official MediaPipe PyPI releases
    mediapipe_versions = {
        (3, 7): "0.8.11",
        (3, 8): "0.10.0",
        (3, 9): "0.10.8",
        (3, 10): "0.10.9",
        (3, 11): "0.10.9",
        (3, 12): "0.10.9",
    }
    
    # Check if Python version is supported
    if py_version not in mediapipe_versions:
        print(f"\n{'=' * 70}")
        print(f"\n❌ Python {py_version[0]}.{py_version[1]} is NOT supported by MediaPipe!")
        print(f"\n✅ Supported Python versions: 3.7 - 3.12")
        print(f"\n🔧 Please install Python 3.11 or 3.12 (recommended)")
        print(f"   Download from: https://www.python.org/downloads/")
        print(f"\n{'=' * 70}\n")
        sys.exit(1)
    
    print(f"\n{'=' * 70}")
    print(f"\n✅ Python {py_version[0]}.{py_version[1]} is compatible!")
    print(f"\n{'=' * 70}\n")
    
    # Get MediaPipe version for this Python
    mediapipe_version = mediapipe_versions[py_version]
    
    print(f"📦 Installing packages...\n")
    
    # Upgrade pip first
    print(f"⏳ Upgrading pip...")
    if run_pip_command(["install", "--upgrade", "pip"]):
        print(f"✅ pip upgraded\n")
    else:
        print(f"⚠️  Warning: Could not upgrade pip (continuing anyway)\n")
    
    # Package list with version constraints
    packages = [
        ("MediaPipe", f"mediapipe=={mediapipe_version}"),
        ("OpenCV", "opencv-python>=4.5.0"),
        ("NumPy", "numpy>=1.19.0,<2.0.0"),
        ("PyAutoGUI", "pyautogui>=0.9.50"),
        ("scikit-learn", "scikit-learn>=0.24.0"),
        ("SciPy", "scipy>=1.7.0"),
        ("Pillow", "Pillow>=8.0.0"),
        ("pyttsx3", "pyttsx3>=2.90"),
    ]
    
    failed_packages = []
    
    for name, package in packages:
        print(f"⏳ Installing {name}...")
        if run_pip_command(["install", package]):
            print(f"✅ {name} installed successfully\n")
        else:
            print(f"❌ Failed to install {name}\n")
            failed_packages.append(name)
    
    # Summary
    print("=" * 70)
    if not failed_packages:
        print(f"\n🎉 Installation Complete! All packages installed successfully.\n")
        print(f"{'=' * 70}\n")
        print(f"📋 Next Steps:\n")
        print(f"  Choose your version:\n")
        print(f"  📂 Version 1 (Basic Eye Tracker):")
        print(f"     cd version1")
        print(f"     python main.py\n")
        print(f"  📂 Version 2 (Advanced Eye Tracker):")
        print(f"     cd version2")
        print(f"     python enhanced_tracker.py\n")
        print(f"  🔍 Test your camera first:")
        print(f"     python scripts/test_camera.py\n")
        print(f"  🧪 Check eye movement detection:")
        print(f"     python scripts/diagnose_eye_movement.py\n")
        print(f"{'=' * 70}\n")
    else:
        print(f"\n⚠️  Installation completed with warnings!\n")
        print(f"Failed packages: {', '.join(failed_packages)}\n")
        print(f"{'=' * 70}\n")
        print(f"🔧 Troubleshooting:\n")
        print(f"  1. Update pip: python -m pip install --upgrade pip")
        print(f"  2. Install Visual C++ redistributables (Windows):")
        print(f"     https://aka.ms/vs/17/release/vc_redist.x64.exe")
        print(f"  3. Try installing failed packages manually:")
        for package_name in failed_packages:
            matching = [p for n, p in packages if n == package_name]
            if matching:
                print(f"     pip install {matching[0]}")
        print(f"\n{'=' * 70}\n")

def verify_installation():
    """Verify that critical packages are installed."""
    print(f"\n{'=' * 70}")
    print(f"\n🔍 Verifying installation...\n")
    
    critical_modules = [
        ("cv2", "OpenCV"),
        ("mediapipe", "MediaPipe"),
        ("numpy", "NumPy"),
        ("pyautogui", "PyAutoGUI"),
    ]
    
    all_ok = True
    for module_name, display_name in critical_modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name} - OK")
        except ImportError:
            print(f"❌ {display_name} - MISSING!")
            all_ok = False
    
    print(f"\n{'=' * 70}\n")
    
    if all_ok:
        print(f"✅ All critical packages are installed correctly!\n")
        print(f"You're ready to run GazeAssist! 🎉\n")
    else:
        print(f"⚠️  Some packages are missing. Please run installation again or install manually.\n")
    
    return all_ok

if __name__ == "__main__":
    try:
        install_packages()
        verify_installation()
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Installation cancelled by user.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        print(f"Please report this issue on GitHub:")
        print(f"https://github.com/Mohammed-ahmady/Gaze--Tracker/issues\n")
        sys.exit(1)
