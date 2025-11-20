"""
GazeAssist Compatibility Checker
Run this first to check if your Python version is compatible!
"""
import sys

def check_compatibility():
    """Check if current Python version is compatible with MediaPipe."""
    py_version = sys.version_info[:2]
    
    print("=" * 70)
    print(" " * 20 + "GazeAssist Compatibility Checker")
    print("=" * 70)
    print(f"\nYour Python Installation:")
    print(f"  Version: {sys.version}")
    print(f"  Executable: {sys.executable}")
    print(f"  Platform: {sys.platform}")
    
    # Check compatibility
    is_compatible = (py_version[0] == 3 and 7 <= py_version[1] <= 12)
    
    print(f"\n{'=' * 70}")
    
    if is_compatible:
        print(f"\n✅ SUCCESS! Your Python {py_version[0]}.{py_version[1]} IS COMPATIBLE!\n")
        print(f"MediaPipe supports Python 3.7 through 3.12")
        print(f"\n{'=' * 70}")
        print(f"\n📋 Next Steps:")
        print(f"\n  1️⃣  Install dependencies:")
        print(f"      python install_smart.py")
        print(f"\n  2️⃣  Choose your version:")
        print(f"      • Version 1 (Basic):    cd version1")
        print(f"      • Version 2 (Advanced): cd version2")
        print(f"\n  3️⃣  Run the program:")
        print(f"      python main.py              (Version 1)")
        print(f"      python enhanced_tracker.py   (Version 2)")
        print(f"\n{'=' * 70}\n")
        
    else:
        print(f"\n❌ INCOMPATIBLE! Python {py_version[0]}.{py_version[1]} is NOT supported!\n")
        print(f"MediaPipe requires Python 3.7 - 3.12")
        print(f"You have Python {py_version[0]}.{py_version[1]}")
        print(f"\n{'=' * 70}")
        print(f"\n🔧 How to Fix:")
        print(f"\n  Option 1: Install Python 3.11 or 3.12 (Recommended)")
        print(f"  ────────────────────────────────────────────────")
        print(f"  1. Download from: https://www.python.org/downloads/")
        print(f"  2. Install to a separate directory:")
        print(f"     Windows: C:\\Python312\\")
        print(f"     Linux/Mac: /usr/local/python312/")
        print(f"  3. Use that installation:")
        print(f"     C:\\Python312\\python.exe check_compatibility.py")
        print(f"     /usr/local/python312/bin/python3 check_compatibility.py")
        print(f"\n  Option 2: Use pyenv (Advanced)")
        print(f"  ────────────────────────────────────")
        print(f"  Windows: https://github.com/pyenv-win/pyenv-win")
        print(f"  Linux/Mac: https://github.com/pyenv/pyenv")
        print(f"  Then: pyenv install 3.12.0 && pyenv local 3.12.0")
        print(f"\n  Option 3: Use Virtual Environment with Correct Python")
        print(f"  ────────────────────────────────────────────────────")
        print(f"  IMPORTANT: You must FIRST install Python 3.12, THEN create venv with it!")
        print(f"  ")
        print(f"  Step 1: Install Python 3.12 to C:\\Python312\\")
        print(f"  Step 2: Create venv using that installation:")
        print(f"          C:\\Python312\\python.exe -m venv venv")
        print(f"  Step 3: Activate and use:")
        print(f"          .\\venv\\Scripts\\activate")
        print(f"          python install_smart.py")
        print(f"  ")
        print(f"  ⚠️  Creating venv with 'python -m venv venv' will use Python 3.13!")
        print(f"      This will NOT work. You must use the Python 3.12 executable.")
        print(f"\n{'=' * 70}\n")
        
        return False
    
    return True

if __name__ == "__main__":
    try:
        compatible = check_compatibility()
        sys.exit(0 if compatible else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
