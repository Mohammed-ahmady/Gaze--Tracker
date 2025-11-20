Enhanced Project Proposal — Eye-Controlled Mouse (Improved)
=============================================================

Summary
-------
This document builds on your Simplified Project Proposal and the current codebase, now explicitly using GazePointer_Journal.pdf as the primary reference [1]. It provides a richer, more technical proposal with diagrams and instructions for extracting images from both PDFs. It includes:

- Executive summary
- System architecture diagram (PlantUML + placeholder image)
- Calibration and runtime flowchart (PlantUML)
- Detailed module descriptions (camera, MediaPipe, calibration, mapping, smoothing, UI)
- Data formats and persistence
- Tests and evaluation plan
- Instructions to extract images from the attached PDF (automated script)

Primary figure placeholders (replace after extraction)
----------------------------------------------------
Use the script (extract_pdf_images.py) to extract embedded images from the PDFs into `extracted_images/<pdf-stem>/`. Then copy chosen images into `images/` and update the references below.

- [ ] images/figure_architecture.png  — (placeholder; candidate from: extracted_images/GazePointer_Journal/pageX_imgY.png)
- [ ] images/figure_calibration_examples.png — (placeholder; candidate from: extracted_images/GazePointer_Journal/pageX_imgY.png)
- [ ] images/figure_results.png — (placeholder; candidate from: extracted_images/GazePointer_Journal/pageX_imgY.png)

Executive summary
-----------------
The project implements an eye-controlled mouse using MediaPipe Face Mesh for landmark detection, OpenCV for video capture and preview, and PyAutoGUI for cursor control. The system prioritizes stability (smoothing filters), accuracy (multi-point calibration), and usability (transparent overlay calibration UI and keyboard controls). The integration improves on the original base by adding an always-on overlay, better feature engineering (eye-relative iris coordinates), and live-tunable smoothing/gain parameters.

System Architecture (high level)
--------------------------------
- Camera capture (OpenCV)
- Face & landmark detection (MediaPipe Face Mesh)
- Feature extraction (iris center, eye-relative ratios, nose tip)
- Calibration manager (multi-point collection, polynomial/RBF mapping, fallback)
- Mapping & cursor control (predict -> smoothing -> PyAutoGUI)
- UI & overlay (OpenCV preview + Tkinter transparent overlay)

See `architecture.puml` for a PlantUML diagram you can render. Aligns conceptually with [1], adapted to the current codebase.

Calibration & Runtime Flow
--------------------------
1. Start camera preview (control window)
2. If no calibration present: start calibration
   - Show overlay dots, collect N frames per point
   - Average measurements, build calibration dataset
   - Train models: polynomial (degree 2) + RBF backup
   - Save model and calibration JSON
3. Runtime loop:
   - Detect face and landmarks
   - Compute eye-relative features (ratio-based)
   - Predict screen coordinates using calibration mapping
   - Apply smoothing (Kalman + EMA)
   - Optionally scale movement by output_gain
   - Move mouse via PyAutoGUI

See `flow_calibration.puml` for the flowchart. Steps and nomenclature align with best practices described in [1], tailored to our implementation details.

Module breakdown
----------------
- integrated_eye_tracker.py — main integration and runtime control
- calibration_system.py — handles calibration grid, training, saving/loading, and prediction
- overlay.py — Tkinter-based transparent overlay for calibration dots
- control_window.py — OpenCV live preview + keyboard input

Data formats
------------
Calibration JSON contains:
- screen_width, screen_height
- calibration_points: list of points with screen coords and averaged eye features
- head_baseline_x/y
- calibration_error

Models: pickle file storing poly_features and Ridge models for X/Y, plus optional RBF functions.

Evaluation plan
---------------
- Quantitative: mean error (pixels), std error, max/min across calibration points
- Qualitative: user testing for ease of use, latency, and perceived accuracy
- Stress tests: varied lighting, head movement, different distances/angles

How to extract images from the original PDF
-------------------------------------------
1) Install requirements in your venv (recommended):

```powershell
# activate venv first if needed
pip install pymupdf
```

2) Run the script I added (works for one or multiple PDFs):

```powershell
python extract_pdf_images.py Simplified_Project_Proposal.pdf GazePointer_Journal.pdf
```

Images will be saved to `extracted_images/<pdf-stem>/` as PNG files. Copy ones you want into `images/` and update the markup in this document.

Files I added
--------------
- `enhanced_proposal.md` — this improved proposal with placeholders
- `extract_pdf_images.py` — simple script to extract images from PDF
- `architecture.puml` — PlantUML system architecture diagram
- `flow_calibration.puml` — PlantUML calibration flowchart

Next steps
----------
- Run `extract_pdf_images.py` and pick images to insert.
- Render PlantUML diagrams (or I can render them for you and add PNGs here if you want).
- I can also produce a PDF-ready version of `enhanced_proposal.md` with embedded images once you confirm which images to include.


Questions / options
-------------------
- Do you want me to automatically render the PlantUML files into PNG and embed them here? (I can create them locally if you allow me to run the necessary commands.)
- Do you want a polished PDF output of the proposal ready for submission?

References
----------
[1] GazePointer Journal (PDF provided by the author). Use this as the primary conceptual reference for calibration strategy, mapping choices, and evaluation methodology. Cite figures and tables with figure numbers (if present) once images are extracted.


