import os
import cv2
import numpy as np

def crop_weld_region_robust(bgr):
    h, w = bgr.shape[:2]
    target_dim = 1000
    scale = target_dim / max(h, w)
    resized = cv2.resize(bgr, (int(w * scale), int(h * scale)))
    rh, rw = resized.shape[:2]
    
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    # Texture map
    sobelx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(sobelx, sobely)
    mag = np.clip(mag, 0, 255).astype(np.uint8)
    texture = cv2.GaussianBlur(mag, (35, 35), 0)
    
    cy, cx = rh / 2.0, rw / 2.0
    y_coords, x_coords = np.indices((rh, rw))
    dist_from_center = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    max_dist = np.sqrt(cx**2 + cy**2)
    center_weight = 1.0 - 0.4 * (dist_from_center / max_dist)
    saliency = (texture.astype(np.float32) * center_weight).astype(np.uint8)
    
    _, thresh = cv2.threshold(saliency, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        rx, ry, rw_box, rh_box = int(rw*0.15), int(rh*0.1), int(rw*0.7), int(rh*0.8)
    else:
        best_c = max(contours, key=cv2.contourArea)
        rx, ry, rw_box, rh_box = cv2.boundingRect(best_c)
        
    aspect = rw_box / float(rh_box)
    
    # If Top-Down axial shot:
    if 0.75 < aspect < 1.3 and ry > rh * 0.04 and (ry + rh_box) < rh * 0.96:
        m = int(min(rw_box, rh_box) * 0.05)
        x1 = max(0, rx - m)
        y1 = max(0, ry - m)
        x2 = min(rw, rx + rw_box + m)
        y2 = min(rh, ry + rh_box + m)
    else:
        # Angled / Isometric shot:
        # Weld is the top portion, but molten dripping metal can run down the upper cylinder
        # We capture the full width of the rotor, from top of the rim down to 65% of the rotor height
        m_x = int(rw_box * 0.08)
        x1 = max(0, rx - m_x)
        x2 = min(rw, rx + rw_box + m_x)
        y1 = max(0, ry - int(rh_box * 0.05))
        # 60% of rotor height ensures weld ring, joint teeth, AND all molten dripping metal are captured!
        y2 = min(rh, ry + int(rh_box * 0.65))
        
    # Scale crop back to original image resolution coordinates
    inv_scale = 1.0 / scale
    ox1 = int(x1 * inv_scale)
    oy1 = int(y1 * inv_scale)
    ox2 = int(x2 * inv_scale)
    oy2 = int(y2 * inv_scale)
    
    crop = bgr[oy1:oy2, ox1:ox2]
    return crop, (ox1, oy1, ox2, oy2)

# Test on bad1 specifically
bgr = cv2.imread(r"e:\Rotor\dataset\bad\bad1.jpeg")
crop, coords = crop_weld_region_robust(bgr)
cv2.imwrite(r"e:\Rotor\analysis_output\smart_crops\bad1_full_drip_crop.jpg", crop)
print("Saved bad1 full drip crop. Size:", crop.shape)
