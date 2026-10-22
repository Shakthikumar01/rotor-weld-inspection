import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon
from PIL import Image
import numpy as np
import os

# Set fonts
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# 14.0 x 6.4 inches at 300 DPI
fig, (ax_sch, ax_img) = plt.subplots(1, 2, figsize=(14.0, 6.4), dpi=300,
                                     gridspec_kw={'width_ratios': [1.15, 1.0]})

# =========================================================================
# LEFT PANEL (a): SCHEMATIC OF PHYSICAL TEST BENCH & EDGE WORKSTATION
# =========================================================================
ax_sch.set_xlim(0, 100)
ax_sch.set_ylim(0, 100)
ax_sch.axis('off')

# Panel border
panel_box_a = FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=0.3,rounding_size=1.5",
                             facecolor="#FAFBFC", edgecolor="#CFD8DC", linewidth=1.5)
ax_sch.add_patch(panel_box_a)

# Title banner
tbox_a = FancyBboxPatch((3, 91), 94, 6.5, boxstyle="round,pad=0.2,rounding_size=1.0",
                        facecolor="#1F4E79", edgecolor="#0F2E4A", linewidth=1.2)
ax_sch.add_patch(tbox_a)
ax_sch.text(50, 94.25, "(a) TEST BENCH SCHEMATIC & HARDWARE ARCHITECTURE",
            ha='center', va='center', color='white', fontsize=10, fontweight='bold')

# 1. Physical Bench Table Surface
bench = FancyBboxPatch((6, 12), 48, 4.5, boxstyle="square,pad=0",
                       facecolor="#546E7A", edgecolor="#37474F", linewidth=1.5, zorder=3)
ax_sch.add_patch(bench)
bench_leg1 = Rectangle((10, 2), 4, 10, facecolor="#78909C", edgecolor="#37474F", lw=1.2, zorder=2)
bench_leg2 = Rectangle((46, 2), 4, 10, facecolor="#78909C", edgecolor="#37474F", lw=1.2, zorder=2)
ax_sch.add_patch(bench_leg1)
ax_sch.add_patch(bench_leg2)
ax_sch.text(30, 8, "Vibration-Damped Inspection Bench", ha='center', va='center', fontsize=7.2, color='#37474F', fontweight='bold')

# 2. Vertical Mounting Boom Stand
stand_base = Rectangle((8, 16.5), 10, 3.5, facecolor="#37474F", edgecolor="#212121", lw=1.2, zorder=4)
stand_pole = Rectangle((11.5, 20), 3, 62, facecolor="#90A4AE", edgecolor="#37474F", lw=1.2, zorder=3)
stand_arm = Rectangle((11.5, 78), 22, 3.5, facecolor="#90A4AE", edgecolor="#37474F", lw=1.2, zorder=3)
ax_sch.add_patch(stand_base)
ax_sch.add_patch(stand_pole)
ax_sch.add_patch(stand_arm)

# 3. Mobile Camera & Ring LED Array
cam_body = FancyBboxPatch((28, 72), 12, 6, boxstyle="round,pad=0.2",
                          facecolor="#263238", edgecolor="#000000", lw=1.4, zorder=5)
ax_sch.add_patch(cam_body)
lens = Circle((34, 72), 2.2, facecolor="#1565C0", edgecolor="#90CAF9", lw=1.2, zorder=6)
ax_sch.add_patch(lens)
ring_light = FancyBboxPatch((25, 70.5), 18, 2.2, boxstyle="round,pad=0.1",
                            facecolor="#FFF9C4", edgecolor="#FBC02D", lw=1.2, zorder=5)
ax_sch.add_patch(ring_light)

ax_sch.text(34, 82.5, "Mobile Optical Camera", ha='center', va='center', fontsize=8.0, fontweight='bold', color='#1A237E')
ax_sch.text(34, 79.5, "(48 MP Sensor, f/1.8 Aperture)", ha='center', va='center', fontsize=6.8, color='#37474F')
ax_sch.text(25, 67.5, "5500K Diffused Ring LED Array", ha='left', va='center', fontsize=7.0, color='#E65100', fontweight='bold')

# Optical Illumination Cone (diffused daylight)
cone_poly = Polygon([[30, 70.5], [38, 70.5], [44, 30], [24, 30]], closed=True,
                    facecolor="#FFFDE7", edgecolor="#FDD835", linestyle="--", alpha=0.45, zorder=2)
ax_sch.add_patch(cone_poly)

# Standoff Distance Indicator (300 mm)
arrow_dist = FancyArrowPatch((21, 71), (21, 31), arrowstyle='<->', mutation_scale=12,
                             color="#D32F2F", linewidth=1.5, zorder=6)
ax_sch.add_patch(arrow_dist)
ax_sch.text(19, 51, "h = 300 mm\n(Calibrated Standoff)", ha='right', va='center', fontsize=7.2, color='#C62828', fontweight='bold')

# 4. Rotor Specimen on V-block Stage
v_fixture = Polygon([[26, 16.5], [42, 16.5], [44, 23], [37, 19], [31, 19], [24, 23]], closed=True,
                    facecolor="#455A64", edgecolor="#263238", lw=1.2, zorder=4)
ax_sch.add_patch(v_fixture)

# Rotor core & weld seam
rotor_body = Rectangle((27, 21), 14, 10, facecolor="#78909C", edgecolor="#37474F", lw=1.2, zorder=5)
ax_sch.add_patch(rotor_body)
weld_ring = FancyBboxPatch((26.5, 29), 15, 2.8, boxstyle="round,pad=0.1",
                           facecolor="#FFB74D", edgecolor="#E65100", lw=1.4, zorder=6)
ax_sch.add_patch(weld_ring)
ax_sch.text(34, 25.5, "Induction Rotor", ha='center', va='center', fontsize=7.5, color='#FFFFFF', fontweight='bold', zorder=7)
ax_sch.text(34, 34, "End-Ring Weld Seam", ha='center', va='center', fontsize=7.5, color='#E65100', fontweight='bold', zorder=7)

# 5. Edge Processing Workstation (Right side of Left Panel: x=58 to 96)
ws_box = FancyBboxPatch((58, 48), 38, 39, boxstyle="round,pad=0.2,rounding_size=1.2",
                        facecolor="#FFFFFF", edgecolor="#1565C0", linewidth=1.4, zorder=4)
ax_sch.add_patch(ws_box)
# header
ws_hdr = FancyBboxPatch((58, 83), 38, 4, boxstyle="round,pad=0.1,rounding_size=1.0",
                        facecolor="#1565C0", edgecolor="#1565C0", zorder=5)
ax_sch.add_patch(ws_hdr)
ax_sch.text(77, 85, "EDGE COMPUTING WORKSTATION", ha='center', va='center', color='white', fontsize=7.8, fontweight='bold', zorder=6)

ws_items = [
    "• Host: Industrial Laptop / PC",
    "• Server: Python Flask (Async)",
    "• Cropper: Saliency Sobel Filter",
    "• Features: 15 Descriptors (Tab 4.4)",
    "• Dual AI: Decision Tree + CNN",
    "• Inference Speed: 48.2 ms (Live)",
    "• Traceability: SHA-256 PDF Cert"
]
for idx_w, item in enumerate(ws_items):
    ax_sch.text(60, 79 - (idx_w * 4.2), item, ha='left', va='center', color='#102A43', fontsize=7.1, zorder=6)

# Data link arrow from Camera to Workstation
link_arrow = FancyArrowPatch((40, 76), (58, 76), arrowstyle='->', mutation_scale=14,
                             color="#1565C0", linewidth=2.0, zorder=6)
ax_sch.add_patch(link_arrow)
ax_sch.text(49, 78.5, "USB-C / Wi-Fi", ha='center', va='center', fontsize=7.2, color='#1565C0', fontweight='bold')

# 6. Industrial 3-Tier Actuation Tower Lamp
tl_box = FancyBboxPatch((58, 8), 38, 34, boxstyle="round,pad=0.2,rounding_size=1.2",
                        facecolor="#FFFFFF", edgecolor="#2E7D32", linewidth=1.4, zorder=4)
ax_sch.add_patch(tl_box)
tl_hdr = FancyBboxPatch((58, 38), 38, 4, boxstyle="round,pad=0.1,rounding_size=1.0",
                        facecolor="#2E7D32", edgecolor="#2E7D32", zorder=5)
ax_sch.add_patch(tl_hdr)
ax_sch.text(77, 40, "SHOP-FLOOR 3-TIER ACTUATION", ha='center', va='center', color='white', fontsize=7.8, fontweight='bold', zorder=6)

# 3 Tower Lights
g_lamp = Circle((63, 31), 2.8, facecolor="#4CAF50", edgecolor="#1B5E20", lw=1.2, zorder=6)
a_lamp = Circle((63, 23), 2.8, facecolor="#FFA726", edgecolor="#E65100", lw=1.2, zorder=6)
r_lamp = Circle((63, 15), 2.8, facecolor="#EF5350", edgecolor="#B71C1C", lw=1.2, zorder=6)
ax_sch.add_patch(g_lamp)
ax_sch.add_patch(a_lamp)
ax_sch.add_patch(r_lamp)

ax_sch.text(68, 31, "TIER 1: ACCEPT [Green Lamp]\n-> Forward to Rotor Balancing", ha='left', va='center', fontsize=6.8, color='#1B5E20', fontweight='bold', zorder=6)
ax_sch.text(68, 23, "TIER 2: REWORK [Amber Lamp]\n-> Divert to TIG Touch-up Bay", ha='left', va='center', fontsize=6.8, color='#E65100', fontweight='bold', zorder=6)
ax_sch.text(68, 15, "TIER 3: SCRAP [Red Beacon]\n-> Eject into Recycling Bin", ha='left', va='center', fontsize=6.8, color='#B71C1C', fontweight='bold', zorder=6)

# Control link arrow from Workstation to Tower
ctl_arrow = FancyArrowPatch((77, 48), (77, 42), arrowstyle='->', mutation_scale=12,
                            color="#2E7D32", linewidth=2.0, zorder=6)
ax_sch.add_patch(ctl_arrow)


# =========================================================================
# RIGHT PANEL (b): REAL OPTICAL PHOTOGRAPH OF ROTOR ON TEST BENCH
# =========================================================================
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
ax_img.text(50, 94.25, "(b) PHYSICAL ROTOR SPECIMEN ON INSPECTION STAND",
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
    # Annotation 1: Circumferential End-Ring Weld Seam
    weld_ann = FancyBboxPatch((18, 55), 64, 25, boxstyle="round,pad=0.2",
                              facecolor="none", edgecolor="#00E676", lw=2.2, linestyle="--", zorder=4)
    ax_img.add_patch(weld_ann)
    
    lbl1 = FancyBboxPatch((24, 76), 52, 6.5, boxstyle="round,pad=0.1",
                          facecolor=(0, 0, 0, 0.75), edgecolor="#00E676", lw=1.2, zorder=5)
    ax_img.add_patch(lbl1)
    ax_img.text(50, 79.25, "CIRCUMFERENTIAL WELD SEAM (FOV ROI)", ha='center', va='center',
               color='#00E676', fontsize=7.5, fontweight='bold', zorder=6)
    
    # Annotation 2: Conductive Bars / Laminations
    lbl2 = FancyBboxPatch((20, 20), 60, 6.5, boxstyle="round,pad=0.1",
                          facecolor=(0, 0, 0, 0.75), edgecolor="#29B6F6", lw=1.2, zorder=5)
    ax_img.add_patch(lbl2)
    ax_img.text(50, 23.25, "ROTOR CORE & CONDUCTIVE BARS (92.4 mm)", ha='center', va='center',
               color='#81D4FA', fontsize=7.5, fontweight='bold', zorder=6)
    
    # Annotation 3: Calibration tag at bottom
    lbl3 = FancyBboxPatch((14, 8), 72, 5.5, boxstyle="round,pad=0.1",
                          facecolor=(1, 1, 1, 0.9), edgecolor="#37474F", lw=1.0, zorder=5)
    ax_img.add_patch(lbl3)
    ax_img.text(50, 10.75, "Working Standoff: 300 mm | Illumination: Diffused 5500K LED",
               ha='center', va='center', color='#263238', fontsize=7.2, fontweight='bold', zorder=6)

plt.tight_layout()
output_fig_path = "analysis_output/report_assets/fig_experimental_setup.png"
os.makedirs(os.path.dirname(output_fig_path), exist_ok=True)
plt.savefig(output_fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Successfully generated dual-panel experimental setup diagram: {output_fig_path}")
