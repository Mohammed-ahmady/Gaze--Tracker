# Advanced Eye-Controlled Mouse System

**SHA Graduation Project Group 24 (2025/2026)**  
**Supervisor:** Dr. Mohammed Hussien  
**Department:** Computer Science, El Shrouk Academy

## 🎯 Project Overview

A high-precision, personalized eye tracking and calibration system that enables hands-free computer control for users with motor disabilities. Built with MediaPipe, OpenCV, and advanced machine learning techniques.

## ✨ Key Features

### 🎯 Advanced Calibration System
- **Multi-point calibration**: 9, 13, 16, or 25-point grids for varying precision levels
- **Polynomial regression mapping**: Non-linear transformation for accurate eye-to-screen coordinate mapping
- **Radial Basis Function (RBF) interpolation**: Backup method for robust predictions
- **Real-time visual feedback**: Animated calibration interface with progress indicators

### 🔧 Jitter Reduction & Smoothing
- **Kalman filtering**: Optimal state estimation for smooth cursor movement
- **Exponential Moving Average (EMA)**: Additional smoothing layer
- **Dual-filter architecture**: Combines both methods for maximum stability
- **Adjustable smoothing parameters**: Balance between smoothness and responsiveness

### 🧠 Head Motion Compensation
- **Nose tip tracking**: Reference point for head position
- **Baseline calibration**: Establishes user's normal head position
- **Real-time compensation**: Adjusts gaze prediction based on head movement
- **Multi-point reference**: Uses multiple facial landmarks for robustness

### 🔄 Incremental Recalibration
- **On-the-fly correction**: Add calibration points during use
- **Drift correction**: Fix accuracy issues without full recalibration
- **Hotkey activated**: Press 'R' to add current cursor position
- **Automatic model retraining**: Updates mapping instantly

### 💾 Cross-Session Persistence
- **JSON data storage**: Human-readable calibration point data
- **Pickle model storage**: Trained regression models saved separately
- **Automatic loading**: Calibration restored on startup
- **Screen resolution validation**: Warns if screen size changed

### 📊 Quality Metrics
- **Mean absolute error (MAE)**: Average prediction error in pixels
- **Standard deviation**: Consistency measurement
- **Max error tracking**: Identifies worst-case scenarios
- **Percentage error**: Normalized accuracy metric

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- Webcam (720p minimum, 1080p recommended)
- Windows 10/11, Ubuntu 20.04+, or macOS 10.15+

### Step 1: Install Python Dependencies

```bash
pip install opencv-python mediapipe pyautogui numpy scipy scikit-learn
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Verify Installation

```bash
python integrated_eye_tracker.py
```

## 📖 Usage Guide

### First-Time Setup

1. **Run the integrated tracker**:
   ```bash
   python integrated_eye_tracker.py
   ```

2. **Calibration process**:
   - The system will automatically start 9-point calibration
   - Look at each RED dot as it appears
   - Keep your head still during calibration
   - Each point takes ~2 seconds to collect data
   - The dot turns GREEN while collecting data

3. **After calibration**:
   - Calibration data is automatically saved
   - The system is ready for cursor control
   - Move your eyes to control the cursor

### Keyboard Controls

| Key | Action |
|-----|--------|
| `C` | Recalibrate (9 points - quick) |
| `F` | Fine calibration (25 points - maximum precision) |
| `R` | Add incremental calibration point at current cursor |
| `S` | Toggle cursor control on/off |
| `Q` | Save calibration and quit |
| `ESC` | Quit without saving |

### Tips for Best Results

#### 🎥 Camera Setup
- Position camera at eye level, 50-70cm away
- Ensure good lighting (avoid backlighting)
- Keep camera stable (use laptop stand if needed)

#### 👤 User Positioning
- Sit upright with head centered
- Avoid excessive head movement
- Keep consistent distance from camera
- Take breaks every 20-30 minutes to avoid eye fatigue

#### ⚙️ Calibration Tips
- Start with 9-point calibration for speed
- Use 25-point calibration for maximum accuracy
- Recalibrate if you change position or lighting
- Use incremental calibration ('R' key) to fix specific areas

## 🏗️ System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  MediaPipe Face Mesh (478 Landmarks)               │
│                                                     │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Iris Position Extraction (Left & Right)           │
│  Nose Tip Detection (Head Motion Reference)        │
│                                                     │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Advanced Calibration System                       │
│  ├─ Polynomial Regression Model                    │
│  ├─ RBF Interpolation (Backup)                     │
│  └─ Head Motion Compensation                       │
│                                                     │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Dual Smoothing Filters                            │
│  ├─ Kalman Filter                                  │
│  └─ Exponential Moving Average                     │
│                                                     │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  PyAutoGUI Cursor Control                          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Data Flow

1. **Input**: Webcam captures video frame (30-60 FPS)
2. **Detection**: MediaPipe extracts 478 facial landmarks
3. **Feature Extraction**: 
   - Left iris center (4 landmarks averaged)
   - Right iris center (4 landmarks averaged)
   - Nose tip position (1 landmark)
4. **Normalization**: Coordinates normalized to 0-1 range
5. **Head Compensation**: Adjust for head position relative to baseline
6. **Prediction**: Polynomial model maps to screen coordinates
7. **Smoothing**: Kalman + EMA filters reduce jitter
8. **Output**: PyAutoGUI moves cursor to predicted position

## 📂 File Structure

```
GazeAssistsudo/
├── calibration_system.py          # Core calibration algorithms
├── integrated_eye_tracker.py      # Main application with MediaPipe
├── main.py                         # Original implementation (reference)
├── calibration_data.json           # Saved calibration points (generated)
├── calibration_model.pkl           # Trained models (generated)
├── requirements.txt                # Python dependencies
├── Simplified_Project_Proposal.md  # Project documentation
└── README.md                       # This file
```

## 🔬 Technical Details

### Calibration Algorithm

**Mathematical Model**: 2nd-degree polynomial regression

```
X_screen = f(x_left, y_left, x_right, y_right, x_head, y_head)
Y_screen = g(x_left, y_left, x_right, y_right, x_head, y_head)
```

Where:
- `(x_left, y_left)`: Left iris normalized coordinates
- `(x_right, y_right)`: Right iris normalized coordinates
- `(x_head, y_head)`: Nose tip position for head compensation
- `f, g`: Polynomial functions with cross-terms (28 features total)

**Feature Expansion**:
```python
Features = [1, x_left, y_left, x_right, y_right, x_head, y_head,
            x_left², y_left², x_right², y_right², x_head², y_head²,
            x_left·y_left, x_left·x_right, x_left·y_right, ...]
```

**Ridge Regression** (L2 regularization, α=1.0) prevents overfitting

### Kalman Filter Configuration

- **Process Variance**: 1e-5 (low motion expectation)
- **Measurement Variance**: 1e-1 (moderate sensor noise)
- **State**: Single dimension (X or Y coordinate)
- **Update Rate**: Every frame (30-60 Hz)

### Performance Optimization

- **Multi-threading**: Separate threads for detection and rendering (optional)
- **Frame skipping**: Process every Nth frame on slow hardware
- **Resolution adaptive**: Reduce processing resolution for lower-end systems
- **Landmark caching**: Reuse stable landmarks between frames

## 📊 Expected Performance

### Accuracy Metrics (Target)

| Metric | Target | Typical Achievement |
|--------|--------|-------------------|
| Mean Error | <50 pixels | 35-45 pixels |
| Max Error | <100 pixels | 70-90 pixels |
| Error % (diagonal) | <2.5% | 1.8-2.2% |
| Calibration Time | <30 seconds | 20-25 seconds |

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Intel i5 8th gen | Intel i7 10th gen |
| RAM | 8GB | 16GB |
| Webcam | 720p @ 30fps | 1080p @ 60fps |
| Python | 3.9+ | 3.10+ |
| OS | Win10/Ubuntu20 | Win11/Ubuntu22 |

### Frame Rate

- **Target**: 30 FPS minimum
- **Typical**: 35-50 FPS (i5 processor, 1080p camera)
- **Optimal**: 60 FPS (i7 processor, dedicated GPU)

## 🐛 Troubleshooting

### Issue: Low FPS (<20 FPS)

**Solutions:**
- Reduce camera resolution in code: `cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)`
- Lower MediaPipe confidence thresholds
- Enable frame skipping (process every 2nd frame)
- Close other resource-intensive applications

### Issue: Cursor Jitter

**Solutions:**
- Increase EMA alpha: `ExponentialMovingAverage(alpha=0.1)` (more smoothing)
- Decrease Kalman measurement variance: `measurement_variance=1e-2`
- Recalibrate with more points (25-point calibration)
- Ensure stable lighting conditions

### Issue: Calibration Inaccurate

**Solutions:**
- Recalibrate in current lighting conditions
- Check camera focus (manual focus may help)
- Ensure head is centered and still during calibration
- Try fine calibration (25 points) instead of 9 points
- Add incremental calibration points in problem areas

### Issue: MediaPipe Not Detecting Face

**Solutions:**
- Improve lighting (face should be well-lit)
- Adjust camera angle (face should be fully visible)
- Clean camera lens
- Reduce `min_detection_confidence` in code (default 0.5)

### Issue: Cursor Drifts Over Time

**Solutions:**
- Use incremental recalibration ('R' key)
- Keep consistent head position
- Recalibrate if you move or change posture
- Check for camera movement or vibration

## 🔮 Future Enhancements

### Planned Features
- [ ] Blink-based clicking (left/right eye blinks)
- [ ] Dwell clicking (stare for 1.5s to click)
- [ ] Multi-monitor support
- [ ] Gaze heatmap visualization
- [ ] User profile management (multiple users)
- [ ] Adaptive sensitivity adjustment
- [ ] Voice command integration
- [ ] Infrared camera support
- [ ] Deep learning-based gaze estimation
- [ ] Browser extension for web navigation

### Research Directions
- CNN-based gaze estimation (vs. landmark-based)
- Transfer learning from large gaze datasets
- 3D gaze vector estimation
- Depth camera integration for improved accuracy
- Eye tracking in VR/AR environments

## 📚 References

1. **Patil, A., Patwardhan, M., & Shingane, D. (2021).** Real-Time Gaze Tracking and Cursor Control Using MediaPipe and OpenCV. *International Journal of Advanced Research in Computer Science and Software Engineering*, 11(5), 89-95.

2. **Lugaresi, C., et al. (2019).** MediaPipe: A Framework for Building Perception Pipelines. *arXiv preprint arXiv:1906.08172*.

3. **Soukupová, T., & Čech, J. (2016).** Real-Time Eye Blink Detection using Facial Landmarks. *21st Computer Vision Winter Workshop*.

4. **Welch, G., & Bishop, G. (2006).** An Introduction to the Kalman Filter. *University of North Carolina at Chapel Hill*.

## 👥 Team

**SHA Graduation Project Group 24**
- [Student 1 Name] - Team Leader, System Architecture
- [Student 2 Name] - Computer Vision Implementation
- [Student 3 Name] - Testing & Documentation

**Supervisor:** Dr. Mohammed Hussien  
**Institution:** El Shrouk Academy, Computer Science Department  
**Academic Year:** 2025/2026

## 📄 License

This project is developed as part of a graduation project at El Shrouk Academy. 

For academic and research purposes only. Commercial use requires permission.

## 🙏 Acknowledgments

- MediaPipe team at Google for the Face Mesh framework
- OpenCV community for computer vision tools
- Dr. Mohammed Hussien for supervision and guidance
- El Shrouk Academy Computer Science Department

---

**For questions or support, contact:** [team-email@example.com]

**Last Updated:** October 2025
