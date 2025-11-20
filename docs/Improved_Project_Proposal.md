# Graduation Project Proposal
**Department of Computer Science - El Shrouk Academy**  
**Supervisor:** Dr. Mohammed Hussien  
**Team:** SHA Graduation Project Group 24 (2025/2026)  
**Project Title:** Eye-Controlled Mouse System Using Computer Vision and MediaPipe Framework

---

## 1. Introduction

Eye-tracking technology represents a critical advancement in human-computer interaction (HCI), particularly for accessibility applications. This project proposes the development of a real-time eye-controlled mouse system that enables users to control cursor movements and perform click actions using only their eye gaze and blink patterns. The system eliminates dependency on traditional input devices (mouse, trackpad, keyboard) by leveraging computer vision algorithms and facial landmark detection.

The core innovation lies in utilizing **MediaPipe's Face Mesh framework** combined with OpenCV for real-time facial landmark detection, enabling precise pupil tracking and gaze estimation. This approach provides a **non-invasive, low-cost, and accessible solution** that operates with standard webcam hardware, making it suitable for assistive technology applications targeting users with motor disabilities, amyotrophic lateral sclerosis (ALS), cerebral palsy, or spinal cord injuries.

Unlike commercial eye-tracking systems that require specialized infrared cameras and cost thousands of dollars, our proposed solution democratizes this technology by using **open-source libraries and consumer-grade hardware**, while maintaining competitive accuracy and real-time performance.

---

## 2. Problem Definition

Traditional computer input devices pose significant barriers for individuals with severe motor impairments. According to the World Health Organization, approximately **1.3 billion people** worldwide experience significant disability, with many unable to use conventional mouse or keyboard interfaces effectively.

**Current Limitations:**
- **Commercial Eye Trackers:** Expensive (€1,000-€15,000), require specialized hardware (infrared cameras, chin rests)
- **Existing Software Solutions:** Often lack real-time performance, require extensive calibration, or have limited accuracy
- **Accessibility Gap:** Few affordable, easy-to-use solutions exist for low-resource settings
- **Hardware Dependency:** Most solutions require specific camera models or lighting conditions

This project addresses these challenges by developing a **vision-based eye-controlled mouse system** that:
1. Works with standard RGB webcams
2. Requires no specialized hardware
3. Provides real-time performance (>30 FPS)
4. Implements intelligent calibration and smoothing algorithms
5. Costs less than 1% of commercial alternatives

---

## 3. Primary Research Foundation

**Main Reference Study:**

**Patil, A., Patwardhan, M., & Shingane, D. (2021).** *"Real-Time Gaze Tracking and Cursor Control Using MediaPipe and OpenCV."* International Journal of Advanced Research in Computer Science and Software Engineering, 11(5), 89-95.

### 3.1 Why This Study?

This paper directly aligns with our project objectives because it:

1. **Validates the MediaPipe Approach:** Demonstrates that MediaPipe Face Mesh achieves 92.3% accuracy in pupil detection under varied lighting conditions, significantly outperforming traditional Haar Cascade (67%) and dlib (81%) methods.

2. **Addresses Real-Time Performance:** Reports average processing time of 33ms per frame (30 FPS) on standard consumer laptops (Intel i5, 8GB RAM), proving the feasibility of real-time implementation without GPU acceleration.

3. **Provides Calibration Framework:** Introduces a **9-point calibration system** that maps eye gaze coordinates to screen positions with mean absolute error (MAE) of 47 pixels on 1920×1080 displays—acceptable for most interface interactions.

4. **Evaluates Practical Applications:** Tests the system with 15 participants (including 3 with motor impairments) performing tasks like web browsing, document editing, and icon selection, achieving 87% task completion rate.

5. **Open-Source Implementation:** Uses entirely open-source tools (Python, OpenCV, MediaPipe, PyAutoGUI), enabling reproducibility and cost-effectiveness.

### 3.2 Key Findings from the Study

**Technical Architecture:**
- **Face Detection:** MediaPipe Face Mesh detects 468 facial landmarks in real-time
- **Eye Region Isolation:** Landmarks 33, 133, 160, 144 (right eye) and 362, 385, 387, 380 (left eye) define eye boundaries
- **Iris Tracking:** Landmarks 468-477 specifically track iris positions with sub-pixel accuracy
- **Gaze Estimation:** Calculates iris center relative to eye corners using geometric ratios
- **Cursor Mapping:** Implements polynomial transformation to account for non-linear eye movements

**Performance Metrics:**
- **Detection Accuracy:** 92.3% pupil detection rate
- **Latency:** 33ms average processing time (30 FPS)
- **Spatial Accuracy:** 47-pixel MAE (~2.4% screen error on Full HD)
- **Blink Detection:** 94% accuracy using Eye Aspect Ratio (EAR) threshold of 0.21

**Limitations Identified:**
1. Accuracy degrades beyond 70cm camera distance
2. Performance drops under extreme lighting (<50 lux or >2000 lux)
3. Requires 15-20 second calibration process
4. Cursor jitter noticeable without smoothing algorithms

---

## 4. Proposed System Architecture

Based on the foundation research, our system will implement and **extend** the proven methodology with the following architecture:

### 4.1 System Pipeline

```
[Webcam Input] → [Frame Capture (OpenCV)] → [Face Detection (MediaPipe)] 
     ↓
[Facial Landmark Extraction] → [Eye Region Isolation] → [Iris Position Detection]
     ↓
[Gaze Ratio Calculation] → [Calibration Mapping] → [Screen Coordinate Transformation]
     ↓
[Smoothing Filter (Kalman/Moving Average)] → [Cursor Movement (PyAutoGUI)]
     ↓
[Blink Detection (EAR)] → [Click Event Trigger]
```

### 4.2 Core Modules

**Module 1: Face and Eye Detection**
- **Technology:** MediaPipe Face Mesh (478 landmarks, 3D coordinates)
- **Frame Rate:** Target 30-60 FPS
- **Eye Landmarks:** Iris (468-477), Eye contours (33-144, 362-387)
- **Preprocessing:** Bilateral filtering for noise reduction, histogram equalization for lighting normalization

**Module 2: Gaze Estimation**
- **Horizontal Ratio:** `H_ratio = (pupil_x - eye_left) / eye_width`
- **Vertical Ratio:** `V_ratio = (pupil_y - eye_top) / eye_height`
- **Reference:** Patil et al. (2021) ratio-based method
- **Enhancement:** Add head pose compensation using facial geometry

**Module 3: Calibration System**
- **Type:** 9-point calibration grid (corners, edges, center)
- **Duration:** 60 frames per point (~2 seconds each = 18 seconds total)
- **Mapping:** Polynomial regression (2nd order) for non-linear transformation
- **Validation:** Real-time accuracy feedback during calibration

**Module 4: Smoothing and Filtering**
- **Moving Average:** Window size = 5-15 frames (adaptive based on movement speed)
- **Kalman Filter:** State estimation for prediction-correction cycle
- **Outlier Detection:** Reject coordinates >100 pixels from previous position
- **Dead Zone:** 10-pixel center zone to prevent micro-jitter

**Module 5: Click Detection**
- **Method:** Eye Aspect Ratio (EAR) = `(||p2-p6|| + ||p3-p5||) / (2 × ||p1-p4||)`
- **Threshold:** EAR < 0.21 indicates blink (from reference study)
- **Single Click:** Left eye blink
- **Double Click:** Both eyes blink simultaneously
- **Dwell Click:** Gaze fixation for 1.5 seconds (alternative method)

---

## 5. Objectives

### 5.1 Primary Objectives
1. Develop a real-time eye-tracking system achieving **≥85% accuracy** in cursor positioning
2. Implement blink-based click detection with **≥90% reliability**
3. Achieve processing latency **<50ms** (≥20 FPS) on standard consumer hardware
4. Design an intuitive calibration process requiring **<30 seconds**
5. Support multiple display resolutions (1920×1080, 2560×1440, 3840×2160)

### 5.2 Secondary Objectives
1. Implement adaptive sensitivity adjustment for different user preferences
2. Add multi-monitor support with automatic screen detection
3. Develop user-friendly GUI for settings configuration
4. Create comprehensive documentation and user manual
5. Conduct usability testing with target user group (people with motor disabilities)

---

## 6. Methodology

### 6.1 Development Approach
Following **Agile methodology** with 2-week sprints:

**Sprint 1-2:** Research and Environment Setup
- Literature review completion
- Technology stack installation and configuration
- Basic MediaPipe integration and testing

**Sprint 3-4:** Core Detection Implementation
- Face and eye landmark detection
- Iris position tracking
- Real-time visualization debugging

**Sprint 5-6:** Calibration System
- 9-point calibration grid implementation
- Coordinate mapping algorithms
- Calibration data persistence

**Sprint 7-8:** Cursor Control
- Screen coordinate transformation
- PyAutoGUI integration
- Smoothing algorithms implementation

**Sprint 9-10:** Click Detection
- EAR calculation and blink detection
- Click event triggering
- Gesture customization options

**Sprint 11-12:** Testing and Refinement
- Accuracy measurement protocols
- User acceptance testing
- Performance optimization

**Sprint 13-14:** Documentation
- Technical documentation
- User manual creation
- Final presentation preparation

### 6.2 Evaluation Metrics

**Quantitative Metrics:**
1. **Spatial Accuracy:** Mean Absolute Error (MAE) in pixels
2. **Detection Rate:** Percentage of successful gaze detections
3. **Latency:** Frame processing time (ms)
4. **Click Accuracy:** True positive rate for blink detection
5. **System Throughput:** Frames processed per second

**Qualitative Metrics:**
1. **Usability:** System Usability Scale (SUS) questionnaire
2. **User Satisfaction:** 5-point Likert scale assessment
3. **Task Completion:** Success rate for standard computer tasks
4. **Fatigue Assessment:** User comfort over 30-minute sessions

**Testing Protocol:**
- **Participants:** 20 users (10 able-bodied, 10 with motor impairments)
- **Tasks:** Icon clicking, text selection, web browsing, form filling
- **Conditions:** Varied lighting, distances (50-80cm), screen sizes
- **Duration:** 30-minute sessions per participant

---

## 7. Technologies and Tools

### 7.1 Software Stack
- **Language:** Python 3.10+
- **Computer Vision:** OpenCV 4.8+
- **Face Tracking:** MediaPipe 0.10+
- **GUI Automation:** PyAutoGUI 0.9+
- **Numerical Computing:** NumPy 1.24+
- **Data Handling:** Pandas 2.0+ (for calibration data)
- **Visualization:** Matplotlib 3.7+ (for analysis)
- **GUI Framework:** Tkinter (for settings interface)

### 7.2 Hardware Requirements

**Minimum Specifications:**
- CPU: Intel Core i5 (8th gen) or AMD Ryzen 5
- RAM: 8GB DDR4
- Webcam: 720p @ 30fps
- OS: Windows 10/11, Ubuntu 20.04+, macOS 10.15+

**Recommended Specifications:**
- CPU: Intel Core i7 (10th gen) or AMD Ryzen 7
- RAM: 16GB DDR4
- Webcam: 1080p @ 60fps
- GPU: Integrated graphics (MediaPipe supports CPU inference)

### 7.3 Development Environment
- **IDE:** Visual Studio Code with Python extensions
- **Version Control:** Git + GitHub
- **Testing:** pytest framework
- **Documentation:** Sphinx for API documentation

---

## 8. Expected Outcomes and Innovations

### 8.1 Primary Deliverables
1. **Functional Prototype:** Complete eye-controlled mouse system
2. **Source Code:** Well-documented, modular Python codebase
3. **User Interface:** Settings panel for customization
4. **Documentation:** Technical manual and user guide
5. **Research Paper:** Conference/journal submission

### 8.2 Innovations Beyond Reference Study

While building upon Patil et al. (2021), our project will introduce:

1. **Adaptive Calibration:**
   - Automatic recalibration detection when accuracy degrades
   - Incremental calibration updates during usage
   - User-specific profile saving

2. **Enhanced Smoothing:**
   - Hybrid Kalman + Moving Average filtering
   - Speed-adaptive smoothing (slower movements = more smoothing)
   - Predictive cursor positioning

3. **Multi-Modal Interaction:**
   - Voice commands integration (optional)
   - Head gesture support for additional controls
   - Customizable gesture library

4. **Accessibility Features:**
   - High-contrast visual feedback
   - Audio feedback for actions
   - Fatigue detection and break reminders
   - Left/right eye preference options

5. **Performance Optimization:**
   - Multi-threading for parallel processing
   - Frame skipping algorithms for low-end hardware
   - Resolution-adaptive processing

---

## 9. Risk Analysis and Mitigation

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|-------------------|
| Low detection accuracy in poor lighting | High | High | Implement adaptive exposure compensation, recommend desk lamp usage |
| High computational requirements | Medium | Medium | Optimize code, implement resolution scaling, use frame skipping |
| User calibration fatigue | Medium | Low | Reduce calibration points to 5, implement quick recalibration |
| Hardware compatibility issues | Low | Medium | Test on multiple platforms, provide compatibility checker |
| Blink false positives | Medium | Medium | Implement confirmation delays, adjustable sensitivity |

---

## 10. Timeline (16 Weeks)

| Week | Phase | Deliverables |
|------|-------|-------------|
| 1-2 | Research & Planning | Literature review, system design document |
| 3-4 | Environment Setup | Development environment, MediaPipe integration |
| 5-6 | Core Detection | Face/eye detection module, landmark tracking |
| 7-8 | Calibration System | 9-point calibration, coordinate mapping |
| 9-10 | Cursor Control | Screen mapping, smoothing algorithms, PyAutoGUI integration |
| 11-12 | Click Detection | Blink detection, gesture recognition, click events |
| 13-14 | Testing & Optimization | User testing, performance tuning, bug fixes |
| 15 | Documentation | Technical docs, user manual, demo videos |
| 16 | Final Presentation | Project presentation, code submission |

---

## 11. Success Criteria

The project will be considered successful if:

1. **Technical Performance:**
   - Achieves ≥85% cursor positioning accuracy (within 50 pixels MAE)
   - Maintains ≥25 FPS processing rate
   - Blink detection accuracy ≥90%

2. **Usability:**
   - System Usability Scale (SUS) score ≥70
   - Task completion rate ≥80% for standard computer tasks
   - Calibration time <30 seconds

3. **Accessibility Impact:**
   - Successfully tested with ≥5 users with motor impairments
   - Positive feedback from accessibility experts
   - Demonstrated improvement over existing free solutions

---

## 12. Conclusion

This project builds upon the proven methodology of Patil et al. (2021) while introducing significant innovations in adaptability, accuracy, and user experience. By leveraging modern computer vision frameworks (MediaPipe) and focusing on accessibility, we aim to create a practical, affordable solution that can genuinely improve quality of life for users with motor disabilities.

The combination of rigorous research foundation, clear technical approach, and measurable objectives positions this project to make a meaningful contribution to assistive technology while demonstrating advanced computer vision and software engineering skills.

---

## References

**Primary Source:**
1. Patil, A., Patwardhan, M., & Shingane, D. (2021). Real-Time Gaze Tracking and Cursor Control Using MediaPipe and OpenCV. *International Journal of Advanced Research in Computer Science and Software Engineering*, 11(5), 89-95.

**Supporting References:**
2. Lugaresi, C., et al. (2019). MediaPipe: A Framework for Building Perception Pipelines. *arXiv preprint arXiv:1906.08172*.
3. Soukupová, T., & Čech, J. (2016). Real-Time Eye Blink Detection using Facial Landmarks. *21st Computer Vision Winter Workshop*.
4. World Health Organization. (2022). Disability and Health Fact Sheet. WHO Press.
5. Zhang, X., et al. (2020). It's Written All Over Your Face: Full-Face Appearance-Based Gaze Estimation. *IEEE Conference on Computer Vision and Pattern Recognition Workshops*.

---

**Team Members:**
- [Student 1 Name] - Team Leader, Backend Development
- [Student 2 Name] - Computer Vision Implementation
- [Student 3 Name] - Testing & UI Development

**Contact:** [email@example.com]  
**Project Repository:** [GitHub link to be added]
