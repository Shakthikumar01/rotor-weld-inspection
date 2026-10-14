import os
import glob
import json
import csv
import numpy as np
import cv2
import matplotlib.pyplot as plt

BASE_DIR = r"e:\Rotor"
DATASET_DIR = os.path.join(BASE_DIR, "dataset_cropped")
GOOD_DIR = os.path.join(DATASET_DIR, "good")
BAD_DIR = os.path.join(DATASET_DIR, "bad")
OUTPUT_CSV = os.path.join(BASE_DIR, "extracted_features_all.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "analysis_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def compute_glcm_features(gray_img):
    # Quantize to 16 gray levels for fast, robust co-occurrence
    quantized = (gray_img // 16).astype(np.uint8)
    h, w = quantized.shape
    
    # Horizontal neighbor pairs (dx=1, dy=0)
    left = quantized[:, :-1].ravel()
    right = quantized[:, 1:].ravel()
    
    # 16x16 GLCM matrix
    glcm = np.zeros((16, 16), dtype=np.float64)
    np.add.at(glcm, (left, right), 1)
    
    total = np.sum(glcm)
    if total > 0:
        glcm /= total
    
    # Indices
    i_idx, j_idx = np.indices((16, 16))
    
    contrast = float(np.sum(glcm * ((i_idx - j_idx) ** 2)))
    homogeneity = float(np.sum(glcm / (1.0 + np.abs(i_idx - j_idx))))
    energy = float(np.sum(glcm ** 2))
    entropy = float(-np.sum(glcm * np.log2(glcm + 1e-12)))
    
    return contrast, homogeneity, energy, entropy

def extract_features_single(img_path, label):
    bgr = cv2.imread(img_path)
    if bgr is None:
        return None
        
    target_dim = 800
    h, w = bgr.shape[:2]
    scale = target_dim / max(h, w)
    resized = cv2.resize(bgr, (int(w * scale), int(h * scale)))
    total_pixels = resized.shape[0] * resized.shape[1]

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

    # 1. Edge & Morphology
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 40, 140)
    edge_density = float(np.sum(edges > 0) / total_pixels) * 100

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated_edges = cv2.dilate(edges, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    circularity = 0.0
    solidity = 0.0
    aspect_ratio = 1.0
    extent = 0.0

    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        main_c = contours[0]
        area = cv2.contourArea(main_c)
        perimeter = cv2.arcLength(main_c, True)
        if perimeter > 0:
            circularity = float((4 * np.pi * area) / (perimeter ** 2))

        hull = cv2.convexHull(main_c)
        hull_area = cv2.contourArea(hull)
        if hull_area > 0:
            solidity = float(area / hull_area)

        x, y, cw, ch = cv2.boundingRect(main_c)
        aspect_ratio = float(cw / ch) if ch > 0 else 1.0
        extent = float(area / (cw * ch)) if (cw * ch) > 0 else 0.0

    # 2. Defect Segmentation: Dark Cavity / Voids
    _, dark_cavities = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    dark_cavities = cv2.morphologyEx(dark_cavities, cv2.MORPH_OPEN, kernel)
    void_pct = float(np.sum(dark_cavities > 0) / total_pixels) * 100

    # 3. Defect Segmentation: Thermal Molten Slag & Heat Tint
    h_chan, s_chan, v_chan = cv2.split(hsv)
    _, slag_mask = cv2.threshold(s_chan, 110, 255, cv2.THRESH_BINARY)
    slag_mask = cv2.bitwise_and(slag_mask, cv2.threshold(v_chan, 70, 255, cv2.THRESH_BINARY)[1])
    slag_pct = float(np.sum(slag_mask > 0) / total_pixels) * 100

    # 4. Color Statistics
    mean_hue = float(np.mean(h_chan))
    mean_sat = float(np.mean(s_chan))
    std_sat = float(np.std(s_chan))
    mean_val = float(np.mean(v_chan))
    std_val = float(np.std(v_chan))

    # 5. Texture (GLCM)
    contrast, homogeneity, energy, entropy = compute_glcm_features(gray)

    return {
        "filename": os.path.basename(img_path),
        "label": label,
        "void_area_pct": round(void_pct, 3),
        "slag_protrusion_pct": round(slag_pct, 3),
        "circularity": round(circularity, 4),
        "solidity": round(solidity, 4),
        "aspect_ratio": round(aspect_ratio, 3),
        "extent": round(extent, 3),
        "edge_density_pct": round(edge_density, 3),
        "glcm_contrast": round(contrast, 3),
        "glcm_homogeneity": round(homogeneity, 4),
        "glcm_energy": round(energy, 4),
        "glcm_entropy": round(entropy, 3),
        "mean_saturation": round(mean_sat, 2),
        "std_saturation": round(std_sat, 2),
        "mean_hue": round(mean_hue, 2),
        "intensity_contrast_std": round(std_val, 2)
    }

def main():
    good_paths = sorted(glob.glob(os.path.join(GOOD_DIR, "*.jpeg")) + glob.glob(os.path.join(GOOD_DIR, "*.jpg")))
    bad_paths = sorted(glob.glob(os.path.join(BAD_DIR, "*.jpeg")) + glob.glob(os.path.join(BAD_DIR, "*.jpg")))

    print(f"Extracting features from {len(good_paths)} Good and {len(bad_paths)} Bad rotor images...")

    records = []
    for p in good_paths:
        f = extract_features_single(p, "good")
        if f: records.append(f)

    for p in bad_paths:
        f = extract_features_single(p, "bad")
        if f: records.append(f)

    # Save to CSV
    fieldnames = list(records[0].keys())
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"\nSaved {len(records)} extracted feature records to: {OUTPUT_CSV}")

    # Compute Statistical Comparison: Good vs Bad
    good_records = [r for r in records if r["label"] == "good"]
    bad_records = [r for r in records if r["label"] == "bad"]

    numeric_keys = [k for k in fieldnames if k not in ["filename", "label"]]
    
    print("\n--- STATISTICAL COMPARISON: GOOD vs DEFECTIVE (MEANS) ---")
    print(f"{'Feature Name':<25} | {'Good Mean':<12} | {'Bad Mean':<12} | {'Difference':<12}")
    print("-" * 68)

    diffs = {}
    for k in numeric_keys:
        g_vals = [r[k] for r in good_records]
        b_vals = [r[k] for r in bad_records]
        g_mean = np.mean(g_vals)
        b_mean = np.mean(b_vals)
        diff_pct = ((b_mean - g_mean) / (g_mean + 1e-6)) * 100
        diffs[k] = (g_mean, b_mean, diff_pct)
        print(f"{k:<25} | {g_mean:<12.3f} | {b_mean:<12.3f} | {diff_pct:>+10.1f}%")

    # Plot Boxplots for Top Discriminating Features
    top_features = ["void_area_pct", "slag_protrusion_pct", "solidity", "circularity", "glcm_contrast", "edge_density_pct"]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    axes = axes.flatten()

    for idx, feat in enumerate(top_features):
        g_data = [r[feat] for r in good_records]
        b_data = [r[feat] for r in bad_records]
        
        box = axes[idx].boxplot([g_data, b_data], patch_artist=True, tick_labels=["Good Welds", "Defective"])
        colors = ['#2ea043', '#f85149']
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        axes[idx].set_title(feat.replace("_", " ").title(), fontsize=12, fontweight='bold')
        axes[idx].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Statistical Feature Distribution: Good vs Defective Rotor Welds (N=81)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    chart_path = os.path.join(OUTPUT_DIR, "feature_distribution_comparison.png")
    plt.savefig(chart_path, dpi=200)
    plt.close()
    print(f"\nFeature distribution comparison plot saved to: {chart_path}")

if __name__ == "__main__":
    main()
