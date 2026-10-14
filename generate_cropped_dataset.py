import os
import glob
import cv2
import numpy as np

BASE_DIR = r"e:\Rotor"
SRC_DATASET = os.path.join(BASE_DIR, "dataset")
OUT_DATASET = os.path.join(BASE_DIR, "dataset_cropped")

GOOD_SRC = os.path.join(SRC_DATASET, "good")
BAD_SRC = os.path.join(SRC_DATASET, "bad")

GOOD_OUT = os.path.join(OUT_DATASET, "good")
BAD_OUT = os.path.join(OUT_DATASET, "bad")

os.makedirs(GOOD_OUT, exist_ok=True)
os.makedirs(BAD_OUT, exist_ok=True)

def crop_weld_roi(bgr):
    if bgr is None:
        return None
    h, w = bgr.shape[:2]
    target_dim = 1000
    scale = target_dim / max(h, w)
    resized = cv2.resize(bgr, (int(w * scale), int(h * scale)))
    rh, rw = resized.shape[:2]
    
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    # 1. Texture Saliency Map
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
        rx, ry, rw_box, rh_box = int(rw*0.1), int(rh*0.05), int(rw*0.8), int(rh*0.8)
    else:
        best_c = max(contours, key=cv2.contourArea)
        rx, ry, rw_box, rh_box = cv2.boundingRect(best_c)
        
    aspect = rw_box / float(rh_box)
    
    # Check if Top-Down axial view:
    if 0.75 < aspect < 1.3 and ry > rh * 0.04 and (ry + rh_box) < rh * 0.96:
        m = int(min(rw_box, rh_box) * 0.05)
        x1 = max(0, rx - m)
        y1 = max(0, ry - m)
        x2 = min(rw, rx + rw_box + m)
        y2 = min(rh, ry + rh_box + m)
    else:
        # Angled/Isometric view:
        # The welded zone comprises the end ring, rotor bar brazed joints, and any dripping slag
        # Capture from the top edge down to ~65% of the rotor bounds
        m_x = int(rw_box * 0.08)
        x1 = max(0, rx - m_x)
        x2 = min(rw, rx + rw_box + m_x)
        y1 = max(0, ry - int(rh_box * 0.05))
        y2 = min(rh, ry + int(rh_box * 0.65))
        
    inv_scale = 1.0 / scale
    ox1 = max(0, int(x1 * inv_scale))
    oy1 = max(0, int(y1 * inv_scale))
    ox2 = min(w, int(x2 * inv_scale))
    oy2 = min(h, int(y2 * inv_scale))
    
    # Ensure minimum valid size
    if (ox2 - ox1) < 100 or (oy2 - oy1) < 100:
        return bgr
        
    return bgr[oy1:oy2, ox1:ox2]

def process_folder(src_folder, dst_folder, class_label):
    files = sorted(glob.glob(os.path.join(src_folder, "*.jpeg")) + glob.glob(os.path.join(src_folder, "*.jpg")))
    print(f"Processing {len(files)} {class_label} images...")
    count = 0
    for f in files:
        bgr = cv2.imread(f)
        if bgr is not None:
            cropped = crop_weld_roi(bgr)
            out_path = os.path.join(dst_folder, os.path.basename(f))
            cv2.imwrite(out_path, cropped, [cv2.IMWRITE_JPEG_QUALITY, 95])
            count += 1
    print(f"Finished {class_label}: {count} images cropped and saved.")

if __name__ == "__main__":
    process_folder(GOOD_SRC, GOOD_OUT, "GOOD")
    process_folder(BAD_SRC, BAD_OUT, "BAD")
    print(f"\nAll cropped images successfully saved to:\n  - {GOOD_OUT}\n  - {BAD_OUT}")
