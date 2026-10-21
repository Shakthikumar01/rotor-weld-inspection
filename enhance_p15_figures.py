import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load the raw image
raw_bgr = cv2.imread('analysis_output/report_assets/fig_rotor_specimen_raw.jpg')
raw_rgb = cv2.cvtColor(raw_bgr, cv2.COLOR_BGR2RGB)
h_raw, w_raw, _ = raw_rgb.shape

# The rotor center is approximately at (cx=393, cy=535)
# In raw_rgb (H=1000, W=750), the rotor diameter is about 550 pixels.
# Let's crop a clean, balanced 4:3 landscape window around the rotor:
# Target width = 750 (full width), target height = 562 (750 * 3 / 4)
# Center cy = 535 -> y_start = 535 - 281 = 254, y_end = 254 + 562 = 816
y_start = max(0, 535 - 281)
y_end = min(h_raw, y_start + 562)
crop_raw = raw_rgb[y_start:y_end, 0:w_raw]

# Create Figure 3.2: High quality annotated view with 1:1 circular proportions
plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['font.family'] = 'serif'

fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
ax.imshow(crop_raw)
ax.axis('off')

# Add clean engineering annotations
# Outer bounding box overlay
box_y0 = 258 - y_start
box_y1 = 813 - y_start
box_x0 = 122
box_x1 = 665

# Draw clean styled bounding box
rect = patches.Rectangle((box_x0, box_y0), box_x1 - box_x0, box_y1 - box_y0,
                         linewidth=2.2, edgecolor='#00E676', facecolor='none')
ax.add_patch(rect)

# Top badge on box
badge = patches.FancyBboxPatch((box_x0 + 8, box_y0 + 8), 240, 28,
                               boxstyle='round,pad=2,rounding_size=4',
                               facecolor='#004D40', edgecolor='#00E676', lw=1.2, alpha=0.9)
ax.add_patch(badge)
ax.text(box_x0 + 128, box_y0 + 22, 'Adaptive Weld Seam ROI [543 x 555 px]',
        color='#FFFFFF', fontsize=8.5, fontweight='bold', ha='center', va='center')

# Margin padding indicator
ax.text(box_x1 - 10, box_y1 - 12, '+15 px Margin Inflation',
        color='#00E676', fontsize=8, fontweight='bold', ha='right', va='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#004D40', edgecolor='#00E676', lw=1, alpha=0.85))

# Header overlay badge
top_badge = patches.FancyBboxPatch((15, 15), 235, 26,
                                   boxstyle='round,pad=2,rounding_size=4',
                                   facecolor='#1A237E', edgecolor='white', lw=1, alpha=0.9)
ax.add_patch(top_badge)
ax.text(132, 28, 'Mobile Camera Optical Acquisition',
        color='white', fontsize=8.5, fontweight='bold', ha='center', va='center')

plt.tight_layout(pad=0.2)
out_fig32 = 'analysis_output/report_assets/fig_rotor_specimen_raw.jpg'
plt.savefig(out_fig32, dpi=300, bbox_inches='tight')
plt.close()
print("Successfully generated updated Fig 3.2:", out_fig32)


# -------------------------------------------------------------------------
# Figure 3.3: Isolated annular weld seam ROI with circular 1:1 true geometry
# -------------------------------------------------------------------------
crop_bgr = cv2.imread('analysis_output/report_assets/fig_weld_seam_crop.jpg')
crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
h_c, w_c, _ = crop_rgb.shape

fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
# Neutral light gray background
ax.set_facecolor('#F8F9FA')
# Show cropped rotor in center
pad_x = (int(h_c * 4 / 3) - w_c) // 2
padded_crop = cv2.copyMakeBorder(crop_rgb, 20, 20, pad_x + 20, pad_x + 20,
                                 cv2.BORDER_CONSTANT, value=[245, 247, 250])
ax.imshow(padded_crop)
ax.axis('off')

# Feature callout annotations on the weld seam
# 1. Molten droop anomaly callout (bottom right area)
ax.annotate('Molten Droop Defect\n(Margin Preserved)',
            xy=(pad_x + 20 + 440, 20 + 380),
            xytext=(pad_x + 20 + 510, 20 + 480),
            arrowprops=dict(facecolor='#D50000', edgecolor='white', width=1.5, headwidth=6, lw=0.8),
            fontsize=8.5, fontweight='bold', color='#D50000',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFEBEE', edgecolor='#D50000', lw=1))

# 2. Weld seam circumferential zone (top left)
ax.annotate('Copper Weld Bead Seam\n(Contour Profile)',
            xy=(pad_x + 20 + 130, 20 + 150),
            xytext=(pad_x + 20 + 20, 20 + 70),
            arrowprops=dict(facecolor='#1565C0', edgecolor='white', width=1.5, headwidth=6, lw=0.8),
            fontsize=8.5, fontweight='bold', color='#1565C0',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#E3F2FD', edgecolor='#1565C0', lw=1))

# 3. Inner core suppressed region
ax.annotate('Inner Core Iron\n(Suppressed Region)',
            xy=(pad_x + 20 + 280, 20 + 280),
            xytext=(pad_x + 20 + 200, 20 + 480),
            arrowprops=dict(facecolor='#424242', edgecolor='white', width=1.5, headwidth=6, lw=0.8),
            fontsize=8.5, fontweight='bold', color='#424242',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#EEEEEE', edgecolor='#424242', lw=1))

# Top title badge
top_badge2 = patches.FancyBboxPatch((15, 15), 235, 26,
                                    boxstyle='round,pad=2,rounding_size=4',
                                    facecolor='#2E7D32', edgecolor='white', lw=1, alpha=0.9)
ax.add_patch(top_badge2)
ax.text(132, 28, 'Isolated Annular Weld Seam ROI',
        color='white', fontsize=8.5, fontweight='bold', ha='center', va='center')

plt.tight_layout(pad=0.2)
out_fig33 = 'analysis_output/report_assets/fig_weld_seam_crop.jpg'
plt.savefig(out_fig33, dpi=300, bbox_inches='tight')
plt.close()
print("Successfully generated updated Fig 3.3:", out_fig33)
