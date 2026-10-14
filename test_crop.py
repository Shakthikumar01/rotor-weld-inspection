import os
import cv2
import numpy as np

OUTPUT_DIR = r"e:\Rotor\analysis_output\crop_samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def detect_and_crop_weld_roi(img_path):
    bgr = cv2.imread(img_path)
    if bgr is None:
        return None, None
        
    h, w = bgr.shape[:2]
    # Resize to standard working resolution
    target_max = 1200
    scale = target_max / max(h, w)
    resized = cv2.resize(bgr, (int(w * scale), int(h * scale)))
    rh, rw = resized.shape[:2]
    
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # 1. Detect Rotor Object from background
    # Background is bright table or shadows; rotor is dark metal core / metallic end ring
    # Otsu or adaptive threshold
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Clean up mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Fallback bounding box if contour detection fails
    if not contours:
        rx, ry, rw_box, rh_box = int(rw * 0.1), int(rh * 0.05), int(rw * 0.8), int(rh * 0.5)
    else:
        # Find largest contour representing the rotor
        largest = max(contours, key=cv2.contourArea)
        rx, ry, rw_box, rh_box = cv2.boundingRect(largest)
    
    # Distinguish Top-Down vs Angled/Side View:
    aspect = rw_box / float(rh_box)
    
    if aspect > 0.85 and aspect < 1.15 and ry > rh * 0.05 and (ry + rh_box) < rh * 0.95:
        # Top-down circular rotor: The whole circular face IS the welded ring
        # Add small margin
        margin = int(min(rw_box, rh_box) * 0.05)
        x1 = max(0, rx - margin)
        y1 = max(0, ry - margin)
        x2 = min(rw, rx + rw_box + margin)
        y2 = min(rh, ry + rh_box + margin)
        view_type = "Top-down Circular"
    else:
        # Angled/Isometric rotor:
        # The weld is situated strictly at the UPPER section of the rotor cylinder (top 45-50% of the rotor height)
        # We crop from the very top of the rotor down to where the weld & dripping slag end (~45% of rotor height)
        margin_x = int(rw_box * 0.06)
        x1 = max(0, rx - margin_x)
        x2 = min(rw, rx + rw_box + margin_x)
        y1 = max(0, ry - int(rh_box * 0.04))
        # Top ~48% of rotor height captures weld ring + any dripping slag down the upper side
        weld_h = int(rh_box * 0.50)
        y2 = min(rh, ry + weld_h)
        view_type = "Angled Side-View (Top Weld Region)"
        
    crop = resized[y1:y2, x1:x2]
    
    # Create visualization
    vis = resized.copy()
    cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 4)
    cv2.putText(vis, f"WELD ROI: {view_type}", (x1, max(30, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
    return crop, vis

def main():
    test_files = [
        ("dataset/good/good1.jpeg", "good1"),
        ("dataset/good/good2.jpeg", "good2"),
        ("dataset/good/good5.jpeg", "good5"),
        ("dataset/bad/bad1.jpeg", "bad1"),
        ("dataset/bad/bad2.jpeg", "bad2"),
        ("dataset/bad/bad3.jpeg", "bad3")
    ]
    
    for rel_path, tag in test_files:
        p = os.path.join(r"e:\Rotor", rel_path)
        if os.path.exists(p):
            crop, vis = detect_and_crop_weld_roi(p)
            if crop is not None:
                cv2.imwrite(os.path.join(OUTPUT_DIR, f"{tag}_crop.jpg"), crop)
                cv2.imwrite(os.path.join(OUTPUT_DIR, f"{tag}_box.jpg"), vis)
                print(f"Processed {tag}: Crop shape {crop.shape}")

if __name__ == "__main__":
    main()
