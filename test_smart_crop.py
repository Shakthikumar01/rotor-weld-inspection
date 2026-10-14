import os
import cv2
import numpy as np

def detect_rotor_smart(img_path):
    bgr = cv2.imread(img_path)
    if bgr is None:
        return None, None
        
    h, w = bgr.shape[:2]
    # Resize to standard working resolution
    target_dim = 1000
    scale = target_dim / max(h, w)
    resized = cv2.resize(bgr, (int(w * scale), int(h * scale)))
    rh, rw = resized.shape[:2]
    
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    # 1. Edge & Texture Saliency Map
    # The rotor has intense texture (laminations, weld bead, copper bars, teeth)
    # Background (pants, table) has low texture
    sobelx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(sobelx, sobely)
    mag = np.clip(mag, 0, 255).astype(np.uint8)
    
    # Smooth texture map
    texture = cv2.GaussianBlur(mag, (31, 31), 0)
    
    # Distance to center prior (rotors are mostly centered in photo)
    cy, cx = rh / 2.0, rw / 2.0
    y_coords, x_coords = np.indices((rh, rw))
    dist_from_center = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    max_dist = np.sqrt(cx**2 + cy**2)
    center_weight = 1.0 - 0.5 * (dist_from_center / max_dist)
    
    saliency = (texture.astype(np.float32) * center_weight).astype(np.uint8)
    
    # Threshold saliency
    _, thresh = cv2.threshold(saliency, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        rx, ry, rw_box, rh_box = int(rw*0.15), int(rh*0.1), int(rw*0.7), int(rh*0.8)
    else:
        # Score contours by area * central closeness
        best_c = None
        best_score = -1
        for c in contours:
            area = cv2.contourArea(c)
            if area < (rw * rh * 0.05): # Ignore small noise
                continue
            M = cv2.moments(c)
            if M["m00"] > 0:
                mcx, mcy = M["m10"] / M["m00"], M["m01"] / M["m00"]
                d = np.sqrt((mcx - cx)**2 + (mcy - cy)**2)
                score = area * (1.0 - (d / max_dist))
                if score > best_score:
                    best_score = score
                    best_c = c
                    
        if best_c is not None:
            rx, ry, rw_box, rh_box = cv2.boundingRect(best_c)
        else:
            rx, ry, rw_box, rh_box = int(rw*0.15), int(rh*0.1), int(rw*0.7), int(rh*0.8)
            
    # Check if Top-down view vs Angled view
    aspect = rw_box / float(rh_box)
    
    # For Top-down circular rotor:
    if 0.8 < aspect < 1.25 and ry > rh * 0.05 and (ry + rh_box) < rh * 0.95:
        margin = int(min(rw_box, rh_box) * 0.05)
        x1 = max(0, rx - margin)
        y1 = max(0, ry - margin)
        x2 = min(rw, rx + rw_box + margin)
        y2 = min(rh, ry + rh_box + margin)
    else:
        # Angled view: The weld is the top ~45% of the rotor cylinder
        margin_x = int(rw_box * 0.05)
        x1 = max(0, rx - margin_x)
        x2 = min(rw, rx + rw_box + margin_x)
        y1 = max(0, ry - int(rh_box * 0.03))
        # Top 45% of the rotor bounds captures weld ring + dripping molten slag
        y2 = min(rh, ry + int(rh_box * 0.45))
        
    crop = resized[y1:y2, x1:x2]
    
    vis = resized.copy()
    cv2.rectangle(vis, (rx, ry), (rx+rw_box, ry+rh_box), (255, 255, 0), 2) # full rotor box in yellow
    cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 4) # weld crop in green
    
    return crop, vis

def main():
    test_files = [
        ("dataset/good/good1.jpeg", "good1"),
        ("dataset/good/good2.jpeg", "good2"),
        ("dataset/bad/bad1.jpeg", "bad1"),
        ("dataset/bad/bad2.jpeg", "bad2")
    ]
    
    out_dir = r"e:\Rotor\analysis_output\smart_crops"
    os.makedirs(out_dir, exist_ok=True)
    
    for rel_path, tag in test_files:
        p = os.path.join(r"e:\Rotor", rel_path)
        crop, vis = detect_rotor_smart(p)
        if crop is not None:
            cv2.imwrite(os.path.join(out_dir, f"{tag}_smart_box.jpg"), vis)
            cv2.imwrite(os.path.join(out_dir, f"{tag}_smart_crop.jpg"), crop)
            print(f"Smart processed {tag}: Crop shape {crop.shape}")

if __name__ == "__main__":
    main()
