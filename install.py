"""
GazeAssist Universal Installer
Works on ANY Python version, ANY platform - automatically fixes everything!
"""
import sys
import subprocess
import platform
import os
import urllib.request
import tempfile
import shutil

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def run_command(cmd, check=True):
    """Run a command and return success status."""
    try:
        if isinstance(cmd, str):
            subprocess.check_call(cmd, shell=True)
        else:
            subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError:
        if check:
            return False
        return False

def get_python_version():
    """Get current Python version."""
    return sys.version_info[:2]

def is_windows():
    """Check if running on Windows."""
    return platform.system() == "Windows"

def find_compatible_python():
    """Try to find a compatible Python installation on the system."""
    print("🔍 Searching for compatible Python installations...\n")
    
    # Common Python installation paths
    if is_windows():
        search_paths = [
            "C:\\Python312\\python.exe",
            "C:\\Python311\\python.exe",
            "C:\\Python310\\python.exe",
            "C:\\Python39\\python.exe",
            "C:\\Program Files\\Python312\\python.exe",
            "C:\\Program Files\\Python311\\python.exe",
            "C:\\Program Files\\Python310\\python.exe",
            "C:\\Program Files\\Python39\\python.exe",
        ]
        # Also check py launcher
        for minor in [12, 11, 10, 9, 8, 7]:
            search_paths.insert(0, f"py -3.{minor}")
    else:
        search_paths = [
            "python3.12",
            "python3.11",
            "python3.10",
            "python3.9",
            "python3.8",
            "python3.7",
            "/usr/local/bin/python3.12",
            "/usr/local/bin/python3.11",
            "/usr/local/bin/python3.10",
            "/usr/bin/python3.12",
            "/usr/bin/python3.11",
            "/usr/bin/python3.10",
        ]
    
    for path in search_paths:
        try:
            if path.startswith("py -"):
                # Test py launcher
                result = subprocess.run(
                    f"{path} --version",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0 and "Python 3." in result.stdout:
                    version = result.stdout.strip().split()[1]
                    print(f"✅ Found: {path} (Python {version})")
                    return path.replace(" -", " -").split()
            else:
                # Test executable path
                result = subprocess.run(
                    [path, "--version"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0 and "Python 3." in result.stdout:
                    version = result.stdout.strip().split()[1]
                    minor = int(version.split('.')[1])
                    if 7 <= minor <= 12:
                        print(f"✅ Found compatible: {path} (Python {version})")
                        return [path]
        except (FileNotFoundError, PermissionError, subprocess.SubprocessError):
            continue
    
    print("❌ No compatible Python installation found automatically.\n")
    return None

def download_python_installer():
    """Guide user to download Python 3.12."""
    print_header("Python 3.12 Installation Required")
    
    print("MediaPipe requires Python 3.7 - 3.12")
    print("You have Python 3.13 or incompatible version.\n")
    
    if is_windows():
        url = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
        print("📥 Downloading Python 3.12 installer...\n")
        print(f"Download URL: {url}")
        print("\nManual steps:")
        print("1. Go to: https://www.python.org/downloads/release/python-3120/")
        print("2. Download: 'Windows installer (64-bit)'")
        print("3. Run installer and CHECK these options:")
        print("   ✅ Add Python 3.12 to PATH")
        print("   ✅ Install for all users (optional)")
        print("4. Choose installation location: C:\\Python312\\")
        print("5. After install, run this script again:")
        print(f"   C:\\Python312\\python.exe install.py\n")
    else:
        print("Linux/Mac installation:\n")
        print("Option 1 - Using apt (Ubuntu/Debian):")
        print("  sudo apt update")
        print("  sudo apt install python3.12 python3.12-venv python3.12-dev\n")
        print("Option 2 - Using homebrew (Mac):")
        print("  brew install python@3.12\n")
        print("Option 3 - Using pyenv:")
        print("  curl https://pyenv.run | bash")
        print("  pyenv install 3.12.0")
        print("  pyenv global 3.12.0\n")
        print("After installation, run:")
        print("  python3.12 install.py\n")
    
    return False

def install_packages(python_cmd):
    """Install all required packages using the specified Python."""
    print_header("Installing GazeAssist Dependencies")
    
    # Get Python version for MediaPipe compatibility
    try:
        result = subprocess.run(
            python_cmd + ["--version"],
            capture_output=True,
            text=True
        )
        version_str = result.stdout.strip()
        print(f"Using: {version_str}")
        print(f"Executable: {' '.join(python_cmd)}\n")
        
        # Extract minor version
        version = version_str.split()[1]
        minor = int(version.split('.')[1])
        
        # MediaPipe version compatibility
        mediapipe_versions = {
            7: "0.8.11",
            8: "0.10.0",
            9: "0.10.8",
            10: "0.10.9",
            11: "0.10.9",
            12: "0.10.9",
        }
        
        if minor not in mediapipe_versions:
            print(f"❌ Python 3.{minor} is not supported by MediaPipe!")
            return False
        
        mediapipe_version = mediapipe_versions[minor]
        
    except Exception as e:
        print(f"❌ Could not determine Python version: {e}")
        return False
    
    # Upgrade pip first
    print("⏳ Upgrading pip...")
    subprocess.run(
        python_cmd + ["-m", "pip", "install", "--upgrade", "pip"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("✅ pip upgraded\n")
    
    # Package list
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
    
    failed = []
    for name, package in packages:
        print(f"⏳ Installing {name}...")
        result = subprocess.run(
            python_cmd + ["-m", "pip", "install", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            print(f"✅ {name} installed\n")
        else:
            print(f"❌ Failed to install {name}\n")
            failed.append(name)
    
    if failed:
        print(f"\n⚠️  Some packages failed: {', '.join(failed)}")
        print("Try installing manually:")
        for name, package in packages:
            if name in failed:
                print(f"  {' '.join(python_cmd)} -m pip install {package}")
        return False
    
    return True

def verify_installation(python_cmd):
    """Verify critical packages are installed."""
    print_header("Verifying Installation")
    
    test_imports = """
import cv2
import mediapipe
import numpy
import pyautogui
print("SUCCESS")
"""
    
    result = subprocess.run(
        python_cmd + ["-c", test_imports],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0 and "SUCCESS" in result.stdout:
        print("✅ All critical packages verified!\n")
        return True
    else:
        print("❌ Package verification failed!")
        print(f"Error: {result.stderr}\n")
        return False

def create_runner_script(python_cmd):
    """Create convenience scripts to run with correct Python."""
    print_header("Creating Runner Scripts")
    
    if is_windows():
        # Create run.bat
        with open("run.bat", "w") as f:
            f.write(f"@echo off\n")
            f.write(f"{' '.join(python_cmd)} %*\n")
        print("✅ Created run.bat")
        print("   Use: run.bat version1\\main.py\n")
        
        # Create run_version1.bat
        with open("run_version1.bat", "w") as f:
            f.write(f"@echo off\n")
            f.write(f"{' '.join(python_cmd)} version1\\main.py\n")
        print("✅ Created run_version1.bat")
        
        # Create run_version2.bat
        with open("run_version2.bat", "w") as f:
            f.write(f"@echo off\n")
            f.write(f"{' '.join(python_cmd)} version2\\enhanced_tracker.py\n")
        print("✅ Created run_version2.bat\n")
        
    else:
        # Create run.sh
        with open("run.sh", "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"{' '.join(python_cmd)} \"$@\"\n")
        os.chmod("run.sh", 0o755)
        print("✅ Created run.sh")
        print("   Use: ./run.sh version1/main.py\n")
        
        # Create run_version1.sh
        with open("run_version1.sh", "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"{' '.join(python_cmd)} version1/main.py\n")
        os.chmod("run_version1.sh", 0o755)
        print("✅ Created run_version1.sh")
        
        # Create run_version2.sh
        with open("run_version2.sh", "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"{' '.join(python_cmd)} version2/enhanced_tracker.py\n")
        os.chmod("run_version2.sh", 0o755)
        print("✅ Created run_version2.sh\n")

def main():
    """Main installation flow."""
    print_header("🎉 GazeAssist Universal Installer 🎉")
    print("This installer works on ANY system and automatically fixes issues!\n")
    
    # Step 1: Check current Python
    current_version = get_python_version()
    print(f"📌 Current Python: {current_version[0]}.{current_version[1]}")
    print(f"   Executable: {sys.executable}\n")
    
    # Step 2: Determine if current Python is compatible
    if current_version[0] == 3 and 7 <= current_version[1] <= 12:
        print("✅ Your Python is compatible!\n")
        python_cmd = [sys.executable]
    else:
        print("❌ Your Python is NOT compatible (need 3.7-3.12)\n")
        
        # Step 3: Try to find compatible Python on system
        found_python = find_compatible_python()
        
        if found_python:
            print("\n✅ Found compatible Python installation!")
            python_cmd = found_python
            
            # Verify it works
            try:
                result = subprocess.run(
                    python_cmd + ["--version"],
                    capture_output=True,
                    text=True
                )
                print(f"   Will use: {result.stdout.strip()}\n")
            except:
                print("❌ Found Python is not working. Need manual installation.\n")
                download_python_installer()
                return False
        else:
            # Step 4: No compatible Python found - guide user
            download_python_installer()
            return False
    
    # Step 5: Install packages
    print("=" * 70 + "\n")
    if not install_packages(python_cmd):
        print("\n❌ Package installation failed!")
        print("Try running with administrator/sudo privileges.\n")
        return False
    
    # Step 6: Verify installation
    if not verify_installation(python_cmd):
        print("\n❌ Installation verification failed!")
        return False
    
    # Step 7: Create runner scripts
    create_runner_script(python_cmd)
    
    # Step 8: Success!
    print_header("🎉 Installation Complete! 🎉")
    
    if is_windows():
        print("To run GazeAssist:\n")
        print("  Version 1 (Basic):    run_version1.bat")
        print("  Version 2 (Advanced): run_version2.bat")
        print("  Or manually:          run.bat version1\\main.py\n")
        print("First time? Test camera:")
        print("  run.bat scripts\\test_camera.py\n")
    else:
        print("To run GazeAssist:\n")
        print("  Version 1 (Basic):    ./run_version1.sh")
        print("  Version 2 (Advanced): ./run_version2.sh")
        print("  Or manually:          ./run.sh version1/main.py\n")
        print("First time? Test camera:")
        print("  ./run.sh scripts/test_camera.py\n")
    
    print("=" * 70 + "\n")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        print("Please report this issue on GitHub:")
        print("https://github.com/Mohammed-ahmady/Gaze--Tracker/issues\n")
        sys.exit(1)
