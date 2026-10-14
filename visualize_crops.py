import os
import cv2
import matplotlib.pyplot as plt

OUTPUT_DIR = r"e:\Rotor\analysis_output\crop_samples"
samples = ["good1", "good2", "bad1", "bad2"]

fig, axes = plt.subplots(4, 2, figsize=(10, 16))

for idx, s in enumerate(samples):
    box_p = os.path.join(OUTPUT_DIR, f"{s}_box.jpg")
    crop_p = os.path.join(OUTPUT_DIR, f"{s}_crop.jpg")
    
    if os.path.exists(box_p) and os.path.exists(crop_p):
        box_img = cv2.cvtColor(cv2.imread(box_p), cv2.COLOR_BGR2RGB)
        crop_img = cv2.cvtColor(cv2.imread(crop_p), cv2.COLOR_BGR2RGB)
        
        axes[idx, 0].imshow(box_img)
        axes[idx, 0].set_title(f"{s.upper()}: Detected Weld Bounding Box", fontsize=10, fontweight='bold')
        axes[idx, 0].axis('off')
        
        axes[idx, 1].imshow(crop_img)
        axes[idx, 1].set_title(f"{s.upper()}: Extracted Weld ROI Crop", fontsize=10, fontweight='bold', color='green' if 'good' in s else 'red')
        axes[idx, 1].axis('off')

plt.tight_layout()
preview_path = os.path.join(OUTPUT_DIR, "weld_crop_preview.png")
plt.savefig(preview_path, dpi=180)
plt.close()
print("Saved preview to:", preview_path)
