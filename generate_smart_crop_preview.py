import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set font
plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['font.family'] = 'serif'

# Load good and bad samples
good_box = cv2.imread('analysis_output/crop_samples/good1_box.jpg')
good_crop = cv2.imread('analysis_output/crop_samples/good1_crop.jpg')
bad_box = cv2.imread('analysis_output/crop_samples/bad1_box.jpg')
bad_crop = cv2.imread('analysis_output/crop_samples/bad1_crop.jpg')

# Convert to RGB
good_box_rgb = cv2.cvtColor(good_box, cv2.COLOR_BGR2RGB)
good_crop_rgb = cv2.cvtColor(good_crop, cv2.COLOR_BGR2RGB)
bad_box_rgb = cv2.cvtColor(bad_box, cv2.COLOR_BGR2RGB)
bad_crop_rgb = cv2.cvtColor(bad_crop, cv2.COLOR_BGR2RGB)

# For good_box_rgb (shape 1200, 900), crop a balanced landscape view centered on the rotor
h_gb, w_gb, _ = good_box_rgb.shape
# Crop around the rotor center
good_box_crop = good_box_rgb[int(h_gb*0.15):int(h_gb*0.85), :]

# For bad_box_rgb (shape 900, 1200), it's already landscape
h_bb, w_bb, _ = bad_box_rgb.shape
bad_box_crop = bad_box_rgb[int(h_bb*0.1):int(h_bb*0.9), :]

fig, axes = plt.subplots(2, 2, figsize=(10.5, 4.6), dpi=300)

# (a) Sound Rotor Bounding Box
axes[0, 0].imshow(good_box_crop)
axes[0, 0].set_title('(a) Sound Rotor: Detected Bounding Box [Specimen G-01]',
                     fontsize=9.5, fontweight='bold', pad=4, color='#1F4E79')
axes[0, 0].axis('off')

# (b) Sound Rotor Cropped Seam ROI
axes[0, 1].imshow(good_crop_rgb)
axes[0, 1].set_title('(b) Sound Rotor: Extracted Weld Seam ROI [Uniform Bead]',
                     fontsize=9.5, fontweight='bold', pad=4, color='#1F4E79')
axes[0, 1].axis('off')

# (c) Defective Rotor Bounding Box
axes[1, 0].imshow(bad_box_crop)
axes[1, 0].set_title('(c) Defective Rotor: Adaptive Inflation Box [Specimen D-01]',
                     fontsize=9.5, fontweight='bold', pad=4, color='#B71C1C')
axes[1, 0].axis('off')

# (d) Defective Rotor Cropped Seam ROI
axes[1, 1].imshow(bad_crop_rgb)
axes[1, 1].set_title('(d) Defective Rotor: Preserved Molten Droop ROI',
                     fontsize=9.5, fontweight='bold', pad=4, color='#B71C1C')
axes[1, 1].axis('off')

plt.tight_layout(pad=1.0)
out_smart = 'analysis_output/report_assets/fig_smart_crop_preview.png'
plt.savefig(out_smart, dpi=300, bbox_inches='tight')
plt.close()
print("Successfully generated clean smart crop preview:", out_smart)
