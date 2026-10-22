import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image
import os

# Set fonts
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# 7.2 x 6.4 inches at 300 DPI - Single Panel: Physical Rotor Specimen on Inspection Stand
fig, ax_img = plt.subplots(1, 1, figsize=(7.2, 6.4), dpi=300)
ax_img.set_xlim(0, 100)
ax_img.set_ylim(0, 100)
ax_img.axis('off')

# Panel border
panel_box_b = FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=0.3,rounding_size=1.5",
                             facecolor="#FAFBFC", edgecolor="#CFD8DC", linewidth=1.5)
ax_img.add_patch(panel_box_b)

# Title banner
tbox_b = FancyBboxPatch((3, 91), 94, 6.5, boxstyle="round,pad=0.2,rounding_size=1.0",
                        facecolor="#0277BD", edgecolor="#01579B", linewidth=1.2)
ax_img.add_patch(tbox_b)
ax_img.text(50, 94.25, "PHYSICAL ROTOR SPECIMEN ON INSPECTION STAND",
            ha='center', va='center', color='white', fontsize=10, fontweight='bold')

# Load and embed the actual rotor photo
rotor_photo_path = 'images/WhatsApp Image 2026-09-17 at 23.10.08.jpeg'
if os.path.exists(rotor_photo_path):
    raw_img = Image.open(rotor_photo_path)
    w, h = raw_img.size
    cx, cy = w // 2, h // 2
    crop_w, crop_h = int(w * 0.72), int(h * 0.85)
    left = cx - crop_w // 2
    top = cy - crop_h // 2 + 50
    right = left + crop_w
    bottom = top + crop_h
    cropped_rotor = raw_img.crop((left, top, right, bottom))
    
    # Display in ax_img: x=4 to 96, y=6 to 88
    ax_img.imshow(cropped_rotor, extent=[4, 96, 6, 88], aspect='auto', zorder=2)
    
    # Engineering Annotations & Bounding Overlays
    weld_ann = FancyBboxPatch((18, 55), 64, 25, boxstyle="round,pad=0.2",
                              facecolor="none", edgecolor="#00E676", lw=2.2, linestyle="--", zorder=4)
    ax_img.add_patch(weld_ann)
    
    lbl1 = FancyBboxPatch((24, 76), 52, 6.5, boxstyle="round,pad=0.1",
                          facecolor=(0, 0, 0, 0.75), edgecolor="#00E676", lw=1.2, zorder=5)
    ax_img.add_patch(lbl1)
    ax_img.text(50, 79.25, "CIRCUMFERENTIAL WELD SEAM (FOV ROI)", ha='center', va='center',
               color='#00E676', fontsize=8.0, fontweight='bold', zorder=6)
    
    lbl2 = FancyBboxPatch((20, 20), 60, 6.5, boxstyle="round,pad=0.1",
                          facecolor=(0, 0, 0, 0.75), edgecolor="#29B6F6", lw=1.2, zorder=5)
    ax_img.add_patch(lbl2)
    ax_img.text(50, 23.25, "ROTOR CORE & CONDUCTIVE BARS (92.4 mm)", ha='center', va='center',
               color='#81D4FA', fontsize=8.0, fontweight='bold', zorder=6)
    
    lbl3 = FancyBboxPatch((14, 8), 72, 5.5, boxstyle="round,pad=0.1",
                          facecolor=(1, 1, 1, 0.9), edgecolor="#37474F", lw=1.0, zorder=5)
    ax_img.add_patch(lbl3)
    ax_img.text(50, 10.75, "Working Standoff: 300 mm | Illumination: Diffused 5500K LED",
               ha='center', va='center', color='#263238', fontsize=7.8, fontweight='bold', zorder=6)

plt.tight_layout()
output_fig_path = "analysis_output/report_assets/fig_experimental_setup.png"
os.makedirs(os.path.dirname(output_fig_path), exist_ok=True)
plt.savefig(output_fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Successfully generated single-panel experimental setup diagram: {output_fig_path}")
