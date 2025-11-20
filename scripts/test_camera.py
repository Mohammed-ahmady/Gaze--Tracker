"""
Quick Camera Diagnostic Tool
Test if your camera is working before running the eye tracker.
"""

import cv2
import sys


def test_camera_detailed():
    """Detailed camera test with multiple backends."""
    print("="*60)
    print("CAMERA DIAGNOSTIC TOOL")
    print("="*60)
    
    backends = [
        (cv2.CAP_DSHOW, "DirectShow (Windows)"),
        (cv2.CAP_MSMF, "Media Foundation (Windows)"),
        (cv2.CAP_ANY, "Auto-detect"),
    ]
    
    print("\nTesting different camera backends...\n")
    
    working_backend = None
    
    for backend_id, backend_name in backends:
        print(f"Testing {backend_name}...")
        try:
            cap = cv2.VideoCapture(0, backend_id)
            
            if cap.isOpened():
                ret, frame = cap.read()
                
                if ret and frame is not None:
                    height, width = frame.shape[:2]
                    print(f"  ✓ SUCCESS! Camera resolution: {width}x{height}")
                    
                    if working_backend is None:
                        working_backend = (backend_id, backend_name)
                    
                    # Show a preview for 3 seconds
                    print(f"  → Showing preview window (press any key to continue)...")
                    cv2.imshow(f"Camera Test - {backend_name}", frame)
                    cv2.waitKey(3000)  # Show for 3 seconds
                    cv2.destroyAllWindows()
                else:
                    print(f"  ✗ FAILED: Camera opened but cannot read frames")
                
                cap.release()
            else:
                print(f"  ✗ FAILED: Cannot open camera")
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
        
        print()
    
    print("="*60)
    
    if working_backend:
        print("RESULT: Camera is WORKING! ✓")
        print(f"Best backend: {working_backend[1]}")
        print("\nYou can now run the eye tracker:")
        print("  python integrated_eye_tracker.py")
    else:
        print("RESULT: Camera is NOT WORKING! ✗")
        print("\nPossible solutions:")
        print("  1. CHECK HARDWARE:")
        print("     - Is your camera physically connected?")
        print("     - Does the camera LED light turn on?")
        print("     - Try using the Camera app (Windows + type 'Camera')")
        print()
        print("  2. CHECK PERMISSIONS:")
        print("     - Open Windows Settings")
        print("     - Go to Privacy & Security > Camera")
        print("     - Enable 'Camera access' and 'Let apps access your camera'")
        print("     - Allow 'Desktop apps' to access your camera")
        print()
        print("  3. CHECK FOR CONFLICTS:")
        print("     - Close ALL apps that might use the camera:")
        print("       Teams, Zoom, Skype, Discord, OBS, etc.")
        print("     - Check Task Manager for any camera processes")
        print()
        print("  4. UPDATE DRIVERS:")
        print("     - Open Device Manager")
        print("     - Find 'Cameras' or 'Imaging devices'")
        print("     - Right-click your camera > Update driver")
        print()
        print("  5. RESTART:")
        print("     - Sometimes a simple restart fixes camera issues")
    
    print("="*60)
    
    return working_backend is not None


if __name__ == "__main__":
    try:
        success = test_camera_detailed()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
