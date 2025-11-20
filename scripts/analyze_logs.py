"""
Eye Tracking Log Analyzer
=========================
Analyze calibration and tracking logs to diagnose issues.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
import sys


def analyze_calibration(log_dir):
    """Analyze calibration quality."""
    cal_file = Path(log_dir) / 'calibration.json'
    
    if not cal_file.exists():
        print("❌ No calibration.json found")
        return
    
    with open(cal_file, 'r') as f:
        cal = json.load(f)
    
    print("\n" + "="*60)
    print("CALIBRATION ANALYSIS")
    print("="*60)
    
    print(f"\nSession: {cal['session_id']}")
    print(f"Points: {cal['num_points']}")
    print(f"Samples per point: {cal['frames_per_point']}")
    
    # Per-point analysis
    print("\nPER-POINT VARIABILITY:")
    print(f"{'Point':<8} {'Position':<20} {'Eye X Std':<12} {'Eye Y Std':<12} {'Status'}")
    print("-" * 70)
    
    high_var_points = []
    
    for point in cal['points']:
        idx = point['point_index']
        pos = f"({point['screen_x']}, {point['screen_y']})"
        samples = point['samples']
        
        # Calculate average eye position
        left_eyes = np.array([s['left_eye'] for s in samples])
        right_eyes = np.array([s['right_eye'] for s in samples])
        avg_eyes = (left_eyes + right_eyes) / 2
        
        std_x = np.std(avg_eyes[:, 0])
        std_y = np.std(avg_eyes[:, 1])
        
        # Determine point location
        x_pos = point['screen_x']
        y_pos = point['screen_y']
        location = ""
        if x_pos < 500 and y_pos < 300:
            location = "Top-Left"
        elif x_pos > 1400 and y_pos < 300:
            location = "Top-Right"
        elif x_pos < 500 and y_pos > 780:
            location = "Bottom-Left"
        elif x_pos > 1400 and y_pos > 780:
            location = "Bottom-Right"
        elif y_pos < 300:
            location = "Top"
        elif y_pos > 780:
            location = "Bottom"
        else:
            location = "Center"
        
        status = "✓ Good"
        if std_x > 0.05 or std_y > 0.05:
            status = "⚠️  High variance"
            high_var_points.append((idx, location, std_x, std_y))
        
        print(f"{idx:<8} {pos:<20} {std_x:<12.4f} {std_y:<12.4f} {status}")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if high_var_points:
        print(f"\n⚠️  {len(high_var_points)} points with high variability:")
        for idx, loc, std_x, std_y in high_var_points:
            print(f"   Point {idx} ({loc}): X_std={std_x:.4f}, Y_std={std_y:.4f}")
        print("\n💡 This suggests eyes were not steadily looking at these points!")
    else:
        print("\n✓ All points have good stability (low variance)")
    
    # Check eye movement range
    all_samples = []
    for point in cal['points']:
        for sample in point['samples']:
            left = sample['left_eye']
            right = sample['right_eye']
            avg = [(left[0] + right[0])/2, (left[1] + right[1])/2]
            all_samples.append(avg)
    
    all_samples = np.array(all_samples)
    x_range = (all_samples[:, 0].min(), all_samples[:, 0].max())
    y_range = (all_samples[:, 1].min(), all_samples[:, 1].max())
    
    print(f"\nEye Position Ranges:")
    print(f"  X: {x_range[0]:.3f} to {x_range[1]:.3f} (range: {x_range[1]-x_range[0]:.3f})")
    print(f"  Y: {y_range[0]:.3f} to {y_range[1]:.3f} (range: {y_range[1]-y_range[0]:.3f})")
    
    if x_range[1] - x_range[0] < 0.5:
        print("  ⚠️  Narrow horizontal range - eyes not moving left/right enough!")
    if y_range[1] - y_range[0] < 0.5:
        print("  ⚠️  Narrow vertical range - eyes not moving up/down enough!")
    
    # Compare top vs bottom points
    top_points = [p for p in cal['points'] if p['screen_y'] < 300]
    bottom_points = [p for p in cal['points'] if p['screen_y'] > 780]
    
    if top_points and bottom_points:
        top_avg_y = np.mean([
            np.mean([(s['left_eye'][1] + s['right_eye'][1])/2 for s in p['samples']])
            for p in top_points
        ])
        bottom_avg_y = np.mean([
            np.mean([(s['left_eye'][1] + s['right_eye'][1])/2 for s in p['samples']])
            for p in bottom_points
        ])
        
        y_diff = bottom_avg_y - top_avg_y
        print(f"\nVertical Calibration Check:")
        print(f"  Top points avg eye_y: {top_avg_y:.3f}")
        print(f"  Bottom points avg eye_y: {bottom_avg_y:.3f}")
        print(f"  Difference: {y_diff:.3f}")
        
        if y_diff < 0.2:
            print("  ❌ CRITICAL: Very small difference!")
            print("     You were NOT looking up/down at calibration points!")
            print("     This is why vertical tracking doesn't work!")
        elif y_diff < 0.4:
            print("  ⚠️  Small difference - limited vertical eye movement")
        else:
            print("  ✓ Good vertical eye movement")


def analyze_tracking(log_dir):
    """Analyze tracking performance."""
    csv_file = Path(log_dir) / 'tracking.csv'
    
    if not csv_file.exists():
        print("\n❌ No tracking.csv found")
        return
    
    df = pd.read_csv(csv_file)
    
    print("\n" + "="*60)
    print("TRACKING ANALYSIS")
    print("="*60)
    
    print(f"\nTotal Frames: {len(df)}")
    print(f"Face Detection Rate: {df['face_detected'].sum() / len(df) * 100:.1f}%")
    
    # Eye movement during tracking
    print(f"\nEye Movement Ranges (during tracking):")
    print(f"  X: {df['avg_eye_x'].min():.3f} to {df['avg_eye_x'].max():.3f} "
          f"(range: {df['avg_eye_x'].max() - df['avg_eye_x'].min():.3f})")
    print(f"  Y: {df['avg_eye_y'].min():.3f} to {df['avg_eye_y'].max():.3f} "
          f"(range: {df['avg_eye_y'].max() - df['avg_eye_y'].min():.3f})")
    
    # Cursor movement
    print(f"\nCursor Movement Ranges:")
    print(f"  X: {df['cursor_x'].min():.0f} to {df['cursor_x'].max():.0f}")
    print(f"  Y: {df['cursor_y'].min():.0f} to {df['cursor_y'].max():.0f}")
    
    # Smoothing effect
    if 'predicted_x' in df.columns and 'smoothed_x' in df.columns:
        avg_smooth_diff_x = np.abs(df['predicted_x'] - df['smoothed_x']).mean()
        avg_smooth_diff_y = np.abs(df['predicted_y'] - df['smoothed_y']).mean()
        print(f"\nSmoothing Effect (avg difference):")
        print(f"  X: {avg_smooth_diff_x:.1f} pixels")
        print(f"  Y: {avg_smooth_diff_y:.1f} pixels")
    
    # Blink detection
    if 'blink_detected' in df.columns:
        blinks = df['blink_detected'].sum()
        print(f"\nBlinks Detected: {blinks}")


def main():
    if len(sys.argv) > 1:
        log_dir = sys.argv[1]
    else:
        # Find most recent log directory
        logs_path = Path('logs')
        if not logs_path.exists():
            print("❌ No logs directory found")
            return
        
        log_dirs = sorted(logs_path.glob('session_*'), key=lambda p: p.stat().st_mtime, reverse=True)
        if not log_dirs:
            print("❌ No session logs found")
            return
        
        log_dir = log_dirs[0]
    
    print(f"\nAnalyzing: {log_dir}")
    
    analyze_calibration(log_dir)
    analyze_tracking(log_dir)
    
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    print("""
If you see:
- High point variability (std > 0.05): Eyes were moving during calibration
- Narrow eye ranges (< 0.5): Not looking at all screen areas
- Small top-bottom difference (< 0.2): NOT looking up/down - RECALIBRATE!
- High smoothing differences: Try toggling smoothing (X key)

For good calibration:
- Actually LOOK AT each calibration point with your eyes
- Keep head still, only move eyes
- Eye X/Y ranges should be 0.8+ for full coverage
- Top-bottom difference should be 0.4+
""")


if __name__ == '__main__':
    main()
