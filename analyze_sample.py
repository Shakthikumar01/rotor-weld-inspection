import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

GOOD_PATH = r"e:\Rotor\images\good.jpeg"
BAD_PATH = r"e:\Rotor\images\bad.jpeg"
OUTPUT_DIR = r"e:\Rotor\analysis_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def analyze_rotor_image(img_path, label_name):
    # Load image
    bgr = cv2.imread(img_path)
    if bgr is None:
        print(f"Error loading {img_path}")
        return None
    
    # Resize for consistent processing while preserving aspect ratio
    target_dim = 800
    h, w = bgr.shape[:2]
    scale = target_dim / max(h, w)
    resized = cv2.resize(bgr, (int(w * scale), int(h * scale)))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # 1. Edge & Contour Irregularity (Canny + Morphology)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated_edges = cv2.dilate(edges, kernel, iterations=2)

    # 2. Void / Dark Cavity Extraction (thresholding dark crevices in weld zone)
    # Welded cavities & exposed bars create high contrast dark pockets
    _, dark_cavities = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    # Remove small noise
    dark_cavities = cv2.morphologyEx(dark_cavities, cv2.MORPH_OPEN, kernel)

    # 3. Thermal Oxidation / Burn Discoloration (HSV analysis)
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    # Severe molten copper/slag discoloration has distinct warm/burn hue or low saturation
    h_channel, s_channel, v_channel = cv2.split(hsv)
    # Detect high saturation burn/slag marks
    _, slag_mask = cv2.threshold(s_channel, 110, 255, cv2.THRESH_BINARY)
    slag_mask = cv2.bitwise_and(slag_mask, cv2.threshold(v_channel, 70, 255, cv2.THRESH_BINARY)[1])

    # 4. Contour Roughness / Projection Analysis (dripping metal)
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_vis = rgb.copy()
    total_contour_area = 0
    max_contour_perimeter = 0
    
    if contours:
        # Sort by area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        # Main outer boundary
        main_contour = contours[0]
        area = cv2.contourArea(main_contour)
        perimeter = cv2.arcLength(main_contour, True)
        # Circularity metric: 4 * pi * Area / (Perimeter^2) -> 1.0 for perfect circle
        circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
        cv2.drawContours(contour_vis, contours[:3], -1, (255, 0, 0), 2)
    else:
        circularity = 0
        area = 0
        perimeter = 0

    # Defect intensity metric calculation
    void_pixel_count = cv2.countNonZero(dark_cavities)
    slag_pixel_count = cv2.countNonZero(slag_mask)
    total_pixels = resized.shape[0] * resized.shape[1]
    
    void_pct = (void_pixel_count / total_pixels) * 100
    slag_pct = (slag_pixel_count / total_pixels) * 100

    metrics = {
        "label": label_name,
        "circularity_smoothness": round(circularity, 4),
        "void_area_pct": round(void_pct, 2),
        "thermal_slag_pct": round(slag_pct, 2)
    }

    return {
        "rgb": rgb,
        "edges": edges,
        "dark_cavities": dark_cavities,
        "slag_mask": slag_mask,
        "contour_vis": contour_vis,
        "metrics": metrics
    }

def main():
    good_res = analyze_rotor_image(GOOD_PATH, "GOOD WELD")
    bad_res = analyze_rotor_image(BAD_PATH, "DEFECTIVE (OVER-MELTED)")

    if not good_res or not bad_res:
        print("Failed to analyze one of the images.")
        return

    print("--- COMPUTED IMAGE ANALYSIS METRICS ---")
    print(f"GOOD SAMPLE: {good_res['metrics']}")
    print(f"BAD SAMPLE : {bad_res['metrics']}")

    # Create visual comparison figure
    fig, axes = plt.subplots(2, 4, figsize=(18, 9))
    
    # Good row
    axes[0, 0].imshow(good_res['rgb'])
    axes[0, 0].set_title(f"GOOD: Original\n(Circularity: {good_res['metrics']['circularity_smoothness']})", fontsize=11, fontweight='bold', color='green')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(good_res['contour_vis'])
    axes[0, 1].set_title("GOOD: Outer Contour/Rim", fontsize=11)
    axes[0, 1].axis('off')

    axes[0, 2].imshow(good_res['dark_cavities'], cmap='gray')
    axes[0, 2].set_title(f"GOOD: Dark Crevices/Voids\n({good_res['metrics']['void_area_pct']}%)", fontsize=11)
    axes[0, 2].axis('off')

    axes[0, 3].imshow(good_res['slag_mask'], cmap='magma')
    axes[0, 3].set_title(f"GOOD: Thermal Slag Mask\n({good_res['metrics']['thermal_slag_pct']}%)", fontsize=11)
    axes[0, 3].axis('off')

    # Bad row
    axes[1, 0].imshow(bad_res['rgb'])
    axes[1, 0].set_title(f"DEFECTIVE: Original\n(Circularity: {bad_res['metrics']['circularity_smoothness']})", fontsize=11, fontweight='bold', color='red')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(bad_res['contour_vis'])
    axes[1, 1].set_title("DEFECTIVE: Dripping Molten Edge", fontsize=11)
    axes[1, 1].axis('off')

    axes[1, 2].imshow(bad_res['dark_cavities'], cmap='gray')
    axes[1, 2].set_title(f"DEFECTIVE: Deep Cavity/Voids\n({bad_res['metrics']['void_area_pct']}%)", fontsize=11)
    axes[1, 2].axis('off')

    axes[1, 3].imshow(bad_res['slag_mask'], cmap='magma')
    axes[1, 3].set_title(f"DEFECTIVE: Severe Slag & Melt Mask\n({bad_res['metrics']['thermal_slag_pct']}%)", fontsize=11)
    axes[1, 3].axis('off')

    plt.tight_layout()
    out_img = os.path.join(OUTPUT_DIR, "weld_comparison_analysis.png")
    plt.savefig(out_img, dpi=200)
    plt.close()
    print(f"\nAnalysis comparison visual saved to: {out_img}")

if __name__ == "__main__":
    main()

