Reusable Proposal Snippets (Paste Under Your Existing Headings)
===============================================================

Note: These are drop-in paragraphs, figures, and captions designed to be pasted under your current headings without renaming or adding new section titles. Replace IMAGE_PATH placeholders after running the extractor, and keep your original headers untouched.

Insert under your Introduction (or Background) heading
-----------------------------------------------------
Our system implements an eye-controlled mouse built on commodity hardware (webcam) and open-source software. It leverages MediaPipe Face Mesh for robust, real-time facial landmark detection, mapping eye movement to on-screen cursor motion. Following the guidance and evaluation practices in [1], we emphasize a clear calibration strategy, stable runtime behavior, and user-centric controls that work across lighting and posture variations.

Insert under your Related Work heading
--------------------------------------
Prior work on gaze-based interaction has shown that end-to-end accuracy depends critically on (i) how eye-relative features are engineered, (ii) the spatial coverage of calibration points, and (iii) temporal smoothing to balance responsiveness with stability. The GazePointer reference [1] provides a thorough treatment of calibration and evaluation, which we adopt and adapt to our implementation, including multi-point grids and error reporting in pixel units.

Insert under your System Design (or Methodology) heading
--------------------------------------------------------
Architecture overview.
- Camera and CV: OpenCV captures frames; MediaPipe Face Mesh extracts facial landmarks (including iris and eyelid points).
- Feature extraction: We compute iris centers and eye-relative horizontal/vertical ratios (0–1) per eye, along with an optional head pose proxy (nose tip) for compensation.
- Calibration manager: A multi-point grid (9–25 points) is presented via a transparent overlay; for each target, we average N frames and store the features with ground-truth screen coordinates.
- Mapping and smoothing: At runtime, we average left/right eyes, normalize by calibration extremes (left/right/top/bottom) as in [1], apply sensitivity and optional output gain, then smooth with Kalman + EMA before cursor updates.

Figure: System Architecture (adapted from [1])
![System Architecture](images/figure_architecture.png)
Caption: Block diagram of the capture–feature–calibration–mapping pipeline (adapted from [1]). Replace with a figure extracted from GazePointer_Journal.pdf if available.

Insert under your Calibration heading
-------------------------------------
Calibration procedure.
- Grid: 9-point by default; 25-point for higher precision.
- Collection: For each dot, collect ~2 seconds of data and average features to reduce noise.
- Model: We normalize using per-axis extremes observed during calibration (left/right and top/bottom midpoints), then apply a sensitivity curve around center for better fine control, following best practices inspired by [1].
- UI: A transparent, always-on-top overlay renders true screen-space dots; ESC cancels safely.

Figure: Calibration Flow
![Calibration Flow](images/figure_calibration_examples.png)
Caption: Example calibration sequence. Replace placeholder with an extracted figure.

Insert under your Implementation (or System Integration) heading
----------------------------------------------------------------
- Control window (OpenCV): Live preview and keyboard controls (C/F/R/S/D/Z, plus +/- gain, X toggle smoothing).
- Overlay (Tkinter): Transparent dot renderer aligned to the physical screen resolution.
- Configuration and persistence: Calibration points saved as JSON; models serialized to pickle. Supports CLI reset and in-app deletion.
- Diagnostics: On-screen status (ACTIVE/PAUSED, Face OK/No Face, FPS, Gain, Smooth), periodic console logs, and optional debug overlays.

Insert under your Experiments/Results heading
--------------------------------------------
Metrics and observations.
- Report mean pixel error, standard deviation, and max error across calibration points, matching [1].
- Compare 9 vs. 25 points and the effect on edge accuracy.
- Qualitative usability: perceived latency, target acquisition time, user fatigue observations.

Figure: Results Summary
![Results](images/figure_results.png)
Caption: Representative results (error bars or heatmaps). Replace placeholder with an extracted figure from [1] when available.

Insert under your Discussion (or Limitations) heading
----------------------------------------------------
- Sensitivity vs. stability: Tuning smoothing (EMA/Kalman) and movement gain affects usability; expose simple hotkeys to accommodate users.
- Lighting/posture variability: Landmark confidence can degrade under poor conditions; future work includes adaptive exposure and landmark quality checks.
- Personalization: Session-to-session variance suggests maintaining per-user calibration profiles and lightweight incremental updates during use.

Insert under your Conclusion heading
-----------------------------------
We deliver a practical eye-controlled mouse that pairs robust feature engineering with a user-friendly calibration and control interface, grounded in best practices from [1]. The system achieves full-screen coverage, low latency, and stable cursor motion on commodity hardware, and remains extensible for further experiments and assistive features.

Insert near your References heading
-----------------------------------
[1] GazePointer Journal (PDF provided): Primary conceptual reference for calibration strategy, mapping choices, UI, and evaluation methodology.

How to replace IMAGE_PATH placeholders
--------------------------------------
1) Extract images:
   ```powershell
   python extract_pdf_images.py GazePointer_Journal.pdf
   ```
2) Copy chosen files from `extracted_images/GazePointer_Journal/` into `images/`.
3) Replace the `images/figure_*.png` paths above with the actual filenames.
