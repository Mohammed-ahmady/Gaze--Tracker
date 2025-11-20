"""Deep Analysis of Latest Eye Tracking Session"""
import json
import csv
import numpy as np
from pathlib import Path

def analyze_latest_session():
    # Find latest session
    logs_dir = Path('logs')
    sessions = sorted([d for d in logs_dir.iterdir() if d.is_dir()], 
                     key=lambda x: x.name, reverse=True)
    
    if not sessions:
        print("No sessions found!")
        return
    
    session = sessions[0]
    print(f"\n{'='*80}")
    print(f"DEEP ANALYSIS - Session: {session.name}")
    print(f"{'='*80}\n")
    
    # Load calibration data
    try:
        cal_saved = json.load(open('calibration_15point.json'))
        
        print("📊 CALIBRATION QUALITY")
        print("="*80)
        
        error_x = cal_saved.get('training_error_x', 0)
        error_y = cal_saved.get('training_error_y', 0)
        
        print(f"\n🎯 Model Training Errors:")
        print(f"   X Error: {error_x:.2f} pixels ", end="")
        if error_x < 30:
            print("✅ EXCELLENT")
        elif error_x < 40:
            print("✓ Good")
        elif error_x < 60:
            print("⚠️ Moderate")
        else:
            print("❌ POOR")
            
        print(f"   Y Error: {error_y:.2f} pixels ", end="")
        if error_y < 30:
            print("✅ EXCELLENT")
        elif error_y < 40:
            print("✓ Good")
        elif error_y < 60:
            print("⚠️ Moderate")
        else:
            print("❌ POOR")
        
        print(f"\n   Total Samples: {len(cal_saved.get('samples', []))}")
        
        # Analyze eye movement during calibration
        samples = cal_saved.get('samples', [])
        if samples:
            # Top row (0-4), Center row (8-12), Bottom row (16-20)
            top = [s for s in samples if s['point_idx'] in [0,1,2,3,4]]
            center = [s for s in samples if s['point_idx'] in [8,9,10,11,12]]
            bottom = [s for s in samples if s['point_idx'] in [16,17,18,19,20]]
            
            # Left edge (0,6,9,14,17), Right edge (4,8,12,16,20)
            left_edge = [s for s in samples if s['point_idx'] in [0,6,9,14,17]]
            right_edge = [s for s in samples if s['point_idx'] in [4,8,12,16,20]]
            
            # Calculate averages
            top_y = np.mean([s['left_eye'][1] for s in top])
            center_y = np.mean([s['left_eye'][1] for s in center])
            bottom_y = np.mean([s['left_eye'][1] for s in bottom])
            
            left_x = np.mean([s['left_eye'][0] for s in left_edge])
            right_x = np.mean([s['left_eye'][0] for s in right_edge])
            
            vertical_range = bottom_y - top_y
            horizontal_range = right_x - left_x
            
            print(f"\n👁️ Eye Movement Analysis:")
            print(f"\n   VERTICAL (Up/Down):")
            print(f"      Top points:    {top_y:.4f}")
            print(f"      Center points: {center_y:.4f}")
            print(f"      Bottom points: {bottom_y:.4f}")
            print(f"      Range:         {vertical_range:.4f} ", end="")
            
            if vertical_range > 0.4:
                print("✅ EXCELLENT - Good vertical coverage")
            elif vertical_range > 0.3:
                print("✓ Good - Decent vertical movement")
            elif vertical_range > 0.2:
                print("⚠️ MODERATE - Limited vertical movement")
            else:
                print("❌ CRITICAL - NOT looking up/down!")
            
            print(f"\n   HORIZONTAL (Left/Right):")
            print(f"      Left points:   {left_x:.4f}")
            print(f"      Right points:  {right_x:.4f}")
            print(f"      Range:         {horizontal_range:.4f} ", end="")
            
            if horizontal_range > 0.5:
                print("✅ EXCELLENT - Good horizontal coverage")
            elif horizontal_range > 0.3:
                print("✓ Good - Decent horizontal movement")
            elif horizontal_range > 0.2:
                print("⚠️ MODERATE - Limited horizontal movement")
            else:
                print("❌ CRITICAL - NOT looking left/right!")
            
            # Overall ranges
            all_x = [s['left_eye'][0] for s in samples]
            all_y = [s['left_eye'][1] for s in samples]
            
            print(f"\n   OVERALL EYE POSITION COVERAGE:")
            print(f"      X: {min(all_x):.4f} to {max(all_x):.4f} (span: {max(all_x)-min(all_x):.4f})")
            print(f"      Y: {min(all_y):.4f} to {max(all_y):.4f} (span: {max(all_y)-min(all_y):.4f})")
            
            # Per-point stability
            print(f"\n📈 Per-Point Stability (High variance = eyes wandering):")
            print(f"   {'Point':<8} {'Position':<18} {'L_X_std':<10} {'L_Y_std':<10} {'Status'}")
            print(f"   {'-'*70}")
            
            unstable_points = []
            for i in range(21):
                point_samples = [s for s in samples if s['point_idx'] == i]
                if point_samples:
                    left_x_vals = [s['left_eye'][0] for s in point_samples]
                    left_y_vals = [s['left_eye'][1] for s in point_samples]
                    std_x = np.std(left_x_vals)
                    std_y = np.std(left_y_vals)
                    
                    screen_x = point_samples[0]['screen_x']
                    screen_y = point_samples[0]['screen_y']
                    pos = f"({screen_x},{screen_y})"
                    
                    if std_x < 0.02 and std_y < 0.02:
                        status = "✅ Stable"
                    elif std_x < 0.03 and std_y < 0.03:
                        status = "✓ Good"
                    elif std_x < 0.04 and std_y < 0.04:
                        status = "⚠️ Moderate"
                        unstable_points.append((i+1, pos, std_x, std_y))
                    else:
                        status = "❌ Unstable"
                        unstable_points.append((i+1, pos, std_x, std_y))
                    
                    print(f"   {i+1:<8} {pos:<18} {std_x:<10.4f} {std_y:<10.4f} {status}")
            
            if unstable_points:
                print(f"\n   ⚠️ Problem Points (eyes were moving/not looking steadily):")
                for pt, pos, std_x, std_y in unstable_points:
                    print(f"      Point {pt} at {pos}: X_std={std_x:.4f}, Y_std={std_y:.4f}")
    
    except FileNotFoundError:
        print("❌ No calibration_15point.json found")
    
    # Analyze tracking data
    print(f"\n\n📊 TRACKING PERFORMANCE")
    print("="*80)
    
    tracking_file = session / 'tracking.csv'
    if tracking_file.exists() and tracking_file.stat().st_size > 0:
        with open(tracking_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"\n   Total Frames Logged: {len(rows)}")
        
        if rows:
            cursor_x = [float(r['cursor_x']) for r in rows]
            cursor_y = [float(r['cursor_y']) for r in rows]
            eye_x = [float(r['avg_eye_x']) for r in rows]
            eye_y = [float(r['avg_eye_y']) for r in rows]
            
            print(f"\n   🖱️ Cursor Movement During Tracking:")
            print(f"      X: {min(cursor_x):.0f} to {max(cursor_x):.0f} px (range: {max(cursor_x)-min(cursor_x):.0f}px)")
            print(f"      Y: {min(cursor_y):.0f} to {max(cursor_y):.0f} px (range: {max(cursor_y)-min(cursor_y):.0f}px)")
            
            if max(cursor_x) - min(cursor_x) < 500:
                print(f"      ⚠️ Limited horizontal cursor movement")
            if max(cursor_y) - min(cursor_y) < 300:
                print(f"      ⚠️ Limited vertical cursor movement")
            
            print(f"\n   👁️ Eye Movement During Tracking:")
            print(f"      X: {min(eye_x):.4f} to {max(eye_x):.4f} (range: {max(eye_x)-min(eye_x):.4f})")
            print(f"      Y: {min(eye_y):.4f} to {max(eye_y):.4f} (range: {max(eye_y)-min(eye_y):.4f})")
        else:
            print("   ⚠️ No tracking frames logged (file is empty)")
    else:
        print("   ⚠️ No tracking data - cursor was likely disabled or no tracking occurred")
    
    # Final diagnosis
    print(f"\n\n🔍 DIAGNOSIS & RECOMMENDATIONS")
    print("="*80)
    
    if cal_saved:
        error_x = cal_saved.get('training_error_x', 0)
        error_y = cal_saved.get('training_error_y', 0)
        samples = cal_saved.get('samples', [])
        
        if samples:
            top = [s for s in samples if s['point_idx'] in [0,1,2,3,4]]
            bottom = [s for s in samples if s['point_idx'] in [16,17,18,19,20]]
            top_y = np.mean([s['left_eye'][1] for s in top])
            bottom_y = np.mean([s['left_eye'][1] for s in bottom])
            vertical_range = bottom_y - top_y
            
            print(f"\n🎯 PRIMARY ISSUES:")
            
            if error_x > 60 or error_y > 60:
                print(f"\n   ❌ HIGH TRAINING ERRORS")
                print(f"      X: {error_x:.1f}px, Y: {error_y:.1f}px")
                print(f"      Model could not learn accurate mapping")
                print(f"      Root cause: Eye positions don't correlate with screen positions")
            
            if vertical_range < 0.2:
                print(f"\n   ❌ CRITICAL: INSUFFICIENT VERTICAL EYE MOVEMENT")
                print(f"      Range: {vertical_range:.3f} (need > 0.4)")
                print(f"      Top avg: {top_y:.3f}, Bottom avg: {bottom_y:.3f}")
                print(f"      Difference: only {vertical_range:.3f}")
                print(f"      ")
                print(f"      YOU ARE NOT LOOKING UP/DOWN AT THE CALIBRATION POINTS!")
                print(f"      Your eyes stayed in a narrow vertical range during calibration")
            elif vertical_range < 0.35:
                print(f"\n   ⚠️ LIMITED VERTICAL EYE MOVEMENT")
                print(f"      Range: {vertical_range:.3f} (should be > 0.4 for best results)")
                print(f"      Try to look MORE up/down at top and bottom points")
            
            if error_y > error_x * 1.5:
                print(f"\n   ⚠️ VERTICAL ERROR >> HORIZONTAL ERROR")
                print(f"      This confirms you're not looking at vertical points properly")
            
            print(f"\n✅ SOLUTIONS:")
            print(f"   1. Delete calibration: Remove-Item calibration_15point.*")
            print(f"   2. Position yourself comfortably, head stable")
            print(f"   3. During calibration:")
            print(f"      - MOVE YOUR EYES to actually LOOK AT each red circle")
            print(f"      - For TOP points: Look UP with your eyes (feel your eyes looking up)")
            print(f"      - For BOTTOM points: Look DOWN with your eyes (feel your eyes looking down)")
            print(f"      - For corners: Move eyes to EXTREME positions")
            print(f"      - Keep HEAD perfectly still, only EYES move")
            print(f"   4. After calibration, enable cursor (press 'C') and test for 1-2 minutes")
            print(f"   5. Press Q to exit and analyze results")
            
            if error_x < 40 and error_y < 40 and vertical_range > 0.35:
                print(f"\n   ✅ CALIBRATION LOOKS GOOD!")
                print(f"      Training errors are acceptable")
                print(f"      Eye movement ranges are good")
                print(f"      Tracking should work well")
    
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    analyze_latest_session()
