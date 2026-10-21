import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set font family to Times New Roman
plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['font.family'] = 'serif'

fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 4.8)
ax.axis('off')

# Background canvas subtle fill
bg = patches.Rectangle((0, 0), 10.5, 4.8, facecolor='#FAFAFA', edgecolor='none')
ax.add_patch(bg)

# =========================================================================
# HELPER FUNCTIONS TO DRAW LOGOS
# =========================================================================

def draw_matlab_logo(ax, cx, cy, radius=0.35):
    # Circular base
    circ = patches.Circle((cx, cy), radius, facecolor='#D9531E', edgecolor='#B03A0E', linewidth=1.5, zorder=3)
    ax.add_patch(circ)
    # 3D Membrane mesh representation
    t = np.linspace(-np.pi, np.pi, 25)
    for i, shift in enumerate([-0.12, 0.0, 0.12]):
        x_mesh = cx + (radius * 0.7) * (t / np.pi)
        y_mesh = cy + shift + 0.12 * np.cos(1.8 * t) * np.exp(-0.4 * (t**2))
        ax.plot(x_mesh, y_mesh, color='white', lw=1.3 - 0.2*abs(i-1), zorder=4)
    # Lobe peaks
    ax.plot([cx - 0.12, cx, cx + 0.12], [cy + 0.14, cy + 0.02, cy + 0.14], 'o', color='#FFF0E6', markersize=3, zorder=5)

def draw_python_logo(ax, cx, cy, radius=0.35):
    # Circular base
    circ = patches.Circle((cx, cy), radius, facecolor='#306998', edgecolor='#1F4565', linewidth=1.5, zorder=3)
    ax.add_patch(circ)
    # Top blue half
    top_box = patches.FancyBboxPatch((cx - 0.18, cy - 0.02), 0.24, 0.20,
                                     boxstyle='round,pad=0.03,rounding_size=0.06',
                                     facecolor='#3776AB', edgecolor='white', lw=0.8, zorder=4)
    ax.add_patch(top_box)
    ax.plot(cx - 0.09, cy + 0.11, 'o', color='white', markersize=2.5, zorder=5)
    # Bottom yellow half
    bot_box = patches.FancyBboxPatch((cx - 0.06, cy - 0.18), 0.24, 0.20,
                                     boxstyle='round,pad=0.03,rounding_size=0.06',
                                     facecolor='#FFD43B', edgecolor='#3776AB', lw=0.8, zorder=4)
    ax.add_patch(bot_box)
    ax.plot(cx + 0.09, cy - 0.11, 'o', color='#3776AB', markersize=2.5, zorder=5)

def draw_opencv_logo(ax, cx, cy, r=0.18):
    # Three interlocking rings (Red top, Green bottom-left, Blue bottom-right)
    colors_cv = ['#EE2C2C', '#00CD00', '#1C86EE']
    angles = [90, 210, 330]
    dist = r * 0.75
    for c, ang in zip(colors_cv, angles):
        rad = np.radians(ang)
        ox = cx + dist * np.cos(rad)
        oy = cy + dist * np.sin(rad)
        w = patches.Wedge((ox, oy), r*0.65, 0, 360, width=r*0.25, facecolor=c, edgecolor='none', zorder=4)
        ax.add_patch(w)

def draw_pytorch_logo(ax, cx, cy, r=0.18):
    # PyTorch flame
    circ = patches.Circle((cx, cy), r*1.1, facecolor='#FFF3EE', edgecolor='#EE4C2C', lw=1, zorder=3)
    ax.add_patch(circ)
    # Flame polygon
    flame_pts = [
        [cx, cy + r*0.8],
        [cx + r*0.5, cy + r*0.3],
        [cx + r*0.6, cy - r*0.4],
        [cx, cy - r*0.7],
        [cx - r*0.6, cy - r*0.4],
        [cx - r*0.5, cy + r*0.3]
    ]
    flame = patches.Polygon(flame_pts, closed=True, facecolor='#EE4C2C', edgecolor='none', zorder=4)
    ax.add_patch(flame)
    ax.plot(cx, cy - r*0.2, 'o', color='white', markersize=3.5, zorder=5)

def draw_sklearn_logo(ax, cx, cy, r=0.18):
    # Scikit-learn badge
    poly = patches.RegularPolygon((cx, cy), numVertices=6, radius=r*1.1,
                                  facecolor='#F89939', edgecolor='#2B7BB9', lw=1.2, zorder=3)
    ax.add_patch(poly)
    ax.text(cx, cy, 'sk', color='white', fontsize=8, fontweight='bold', ha='center', va='center', zorder=4)

def draw_web_logo(ax, cx, cy, r=0.18):
    circ = patches.Circle((cx, cy), r*1.1, facecolor='#E34F26', edgecolor='#C53B15', lw=1, zorder=3)
    ax.add_patch(circ)
    ax.text(cx, cy, 'UI', color='white', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=4)


# =========================================================================
# LEFT CARD: MATLAB ONLINE R2024b (EXPLORATORY ANALYSIS)
# =========================================================================
left_x = 0.35
left_w = 4.6
left_h = 3.9
left_y = 0.55

# Outer container
box_matlab = patches.FancyBboxPatch(
    (left_x, left_y), left_w, left_h,
    boxstyle='round,pad=0.1,rounding_size=0.18',
    facecolor='#FFFFFF', edgecolor='#D9531E', linewidth=1.8, zorder=2
)
ax.add_patch(box_matlab)

# Top Banner
banner_matlab = patches.FancyBboxPatch(
    (left_x, left_y + left_h - 0.72), left_w, 0.72,
    boxstyle='round,pad=0.08,rounding_size=0.14',
    facecolor='#D9531E', edgecolor='#D9531E', linewidth=1, zorder=2
)
ax.add_patch(banner_matlab)

# MATLAB Logo
draw_matlab_logo(ax, left_x + 0.45, left_y + left_h - 0.36, radius=0.28)

# Banner Text
ax.text(left_x + 0.90, left_y + left_h - 0.24, 'MATLAB Online (R2024b)',
        color='white', fontsize=12, fontweight='bold', va='center', zorder=3)
ax.text(left_x + 0.90, left_y + left_h - 0.50, 'Exploratory Signal Profiling & Statistical Validation',
        color='#FFE6DD', fontsize=9, fontstyle='italic', va='center', zorder=3)

# Subcard 1: Intensity Profiling
c1_y = left_y + 2.15
card_p1 = patches.FancyBboxPatch((left_x + 0.2, c1_y), left_w - 0.4, 0.88,
                                 boxstyle='round,pad=0.05,rounding_size=0.1',
                                 facecolor='#FFF7F4', edgecolor='#F0B298', lw=1, zorder=3)
ax.add_patch(card_p1)
ax.text(left_x + 0.35, c1_y + 0.65, '1. Spatial Intensity Sweep & Variation Profiles',
        fontsize=9.8, fontweight='bold', color='#B03A0E', zorder=4)
ax.text(left_x + 0.35, c1_y + 0.40, '• Row-wise & column-wise mean pixel intensity vectors',
        fontsize=8.5, color='#333333', zorder=4)
ax.text(left_x + 0.35, c1_y + 0.18, '• Standard deviation profile tracking surface anomalies',
        fontsize=8.5, color='#333333', zorder=4)

# Subcard 2: Statistical Moments
c2_y = left_y + 1.12
card_p2 = patches.FancyBboxPatch((left_x + 0.2, c2_y), left_w - 0.4, 0.88,
                                 boxstyle='round,pad=0.05,rounding_size=0.1',
                                 facecolor='#FFF7F4', edgecolor='#F0B298', lw=1, zorder=3)
ax.add_patch(card_p2)
ax.text(left_x + 0.35, c2_y + 0.65, '2. Statistical Moments & Histogram Distribution',
        fontsize=9.8, fontweight='bold', color='#B03A0E', zorder=4)
ax.text(left_x + 0.35, c2_y + 0.40, '• Global moments: Mean, Variance, Skewness, Kurtosis',
        fontsize=8.5, color='#333333', zorder=4)
ax.text(left_x + 0.35, c2_y + 0.18, '• Multimodal histograms identifying good vs. defect welds',
        fontsize=8.5, color='#333333', zorder=4)

# Subcard 3: Data Export
c3_y = left_y + 0.15
card_p3 = patches.FancyBboxPatch((left_x + 0.2, c3_y), left_w - 0.4, 0.84,
                                 boxstyle='round,pad=0.05,rounding_size=0.1',
                                 facecolor='#FFF7F4', edgecolor='#F0B298', lw=1, zorder=3)
ax.add_patch(card_p3)
ax.text(left_x + 0.35, c3_y + 0.61, '3. Tabular Dataset Export for AI Pipelines',
        fontsize=9.8, fontweight='bold', color='#B03A0E', zorder=4)
ax.text(left_x + 0.35, c3_y + 0.38, '• Exported badrotor_pixel_data.xlsx & goodrotor statistics',
        fontsize=8.5, color='#333333', zorder=4)
ax.text(left_x + 0.35, c3_y + 0.16, '• Establishes baseline physical thresholds for ML models',
        fontsize=8.5, color='#333333', zorder=4)


# =========================================================================
# RIGHT CARD: PYTHON 3.10+ PRODUCTION PIPELINE
# =========================================================================
right_x = 5.55
right_w = 4.6
right_h = 3.9
right_y = 0.55

# Outer container
box_python = patches.FancyBboxPatch(
    (right_x, right_y), right_w, right_h,
    boxstyle='round,pad=0.1,rounding_size=0.18',
    facecolor='#FFFFFF', edgecolor='#1F4E79', linewidth=1.8, zorder=2
)
ax.add_patch(box_python)

# Top Banner
banner_python = patches.FancyBboxPatch(
    (right_x, right_y + right_h - 0.72), right_w, 0.72,
    boxstyle='round,pad=0.08,rounding_size=0.14',
    facecolor='#1F4E79', edgecolor='#1F4E79', linewidth=1, zorder=2
)
ax.add_patch(banner_python)

# Python Logo
draw_python_logo(ax, right_x + 0.45, right_y + right_h - 0.36, radius=0.28)

# Banner Text
ax.text(right_x + 0.90, right_y + right_h - 0.24, 'Python 3.10+ Production Pipeline',
        color='white', fontsize=12, fontweight='bold', va='center', zorder=3)
ax.text(right_x + 0.90, right_y + right_h - 0.50, 'Automated Vision Preprocessing & AI Inference',
        color='#D6E4F0', fontsize=9, fontstyle='italic', va='center', zorder=3)

# 4 Modular Mini-Cards inside Python Pipeline

# Mini-Card 1: OpenCV
m1_y = right_y + 2.30
m1 = patches.FancyBboxPatch((right_x + 0.2, m1_y), right_w - 0.4, 0.72,
                            boxstyle='round,pad=0.04,rounding_size=0.08',
                            facecolor='#F4F8FC', edgecolor='#BFD7EA', lw=1, zorder=3)
ax.add_patch(m1)
draw_opencv_logo(ax, right_x + 0.45, m1_y + 0.36, r=0.18)
ax.text(right_x + 0.75, m1_y + 0.48, 'OpenCV (cv2 4.10) - Preprocessing & Cropping',
        fontsize=9.2, fontweight='bold', color='#1F4E79', zorder=4)
ax.text(right_x + 0.75, m1_y + 0.20, '• Sobel edge filtering, Otsu binarization, droop padding',
        fontsize=8.2, color='#333333', zorder=4)

# Mini-Card 2: Scikit-Learn & Scikit-Image
m2_y = right_y + 1.52
m2 = patches.FancyBboxPatch((right_x + 0.2, m2_y), right_w - 0.4, 0.72,
                            boxstyle='round,pad=0.04,rounding_size=0.08',
                            facecolor='#F4F8FC', edgecolor='#BFD7EA', lw=1, zorder=3)
ax.add_patch(m2)
draw_sklearn_logo(ax, right_x + 0.45, m2_y + 0.36, r=0.18)
ax.text(right_x + 0.75, m2_y + 0.48, 'Scikit-Learn & Scikit-Image - Feature Extraction',
        fontsize=9.2, fontweight='bold', color='#1F4E79', zorder=4)
ax.text(right_x + 0.75, m2_y + 0.20, '• 15 physical descriptors, GLCM texture, 2D PCA, DT & RF',
        fontsize=8.2, color='#333333', zorder=4)

# Mini-Card 3: PyTorch Deep Learning
m3_y = right_y + 0.74
m3 = patches.FancyBboxPatch((right_x + 0.2, m3_y), right_w - 0.4, 0.72,
                            boxstyle='round,pad=0.04,rounding_size=0.08',
                            facecolor='#F4F8FC', edgecolor='#BFD7EA', lw=1, zorder=3)
ax.add_patch(m3)
draw_pytorch_logo(ax, right_x + 0.45, m3_y + 0.36, r=0.18)
ax.text(right_x + 0.75, m3_y + 0.48, 'PyTorch (2.4.1) - MobileNetV3 Deep Vision',
        fontsize=9.2, fontweight='bold', color='#1F4E79', zorder=4)
ax.text(right_x + 0.75, m3_y + 0.20, '• Lightweight CNN transfer learning & fast tensor inference',
        fontsize=8.2, color='#333333', zorder=4)

# Mini-Card 4: Web UI & Automated Reporting
m4_y = right_y + 0.06
m4 = patches.FancyBboxPatch((right_x + 0.2, m4_y), right_w - 0.4, 0.62,
                            boxstyle='round,pad=0.04,rounding_size=0.08',
                            facecolor='#F4F8FC', edgecolor='#BFD7EA', lw=1, zorder=3)
ax.add_patch(m4)
draw_web_logo(ax, right_x + 0.45, m4_y + 0.31, r=0.16)
ax.text(right_x + 0.75, m4_y + 0.42, 'Web Inspection UI & ReportLab / python-docx',
        fontsize=9.2, fontweight='bold', color='#1F4E79', zorder=4)
ax.text(right_x + 0.75, m4_y + 0.16, '• Real-time HTML5 UI & automated ISO 9001 certificates',
        fontsize=8.2, color='#333333', zorder=4)

# =========================================================================
# CENTRAL INTERFACE CONNECTOR ARROWS
# =========================================================================
arrow_conn = patches.FancyArrowPatch(
    (left_x + left_w, 2.5), (right_x, 2.5),
    connectionstyle="arc3,rad=0.0", color='#555555',
    arrowstyle="<|-|>", mutation_scale=15, lw=2.2, zorder=5
)
ax.add_patch(arrow_conn)

badge_data = patches.FancyBboxPatch((4.85, 2.22), 0.80, 0.56,
                                    boxstyle='round,pad=0.03,rounding_size=0.08',
                                    facecolor='#333333', edgecolor='white', lw=1, zorder=6)
ax.add_patch(badge_data)
ax.text(5.25, 2.57, 'DATA', color='white', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=7)
ax.text(5.25, 2.38, 'EXCHANGE', color='#FFE082', fontsize=6.8, fontweight='bold', ha='center', va='center', zorder=7)

# Bottom workflow strip
strip = patches.FancyBboxPatch((0.35, 0.08), 9.8, 0.38,
                               boxstyle='round,pad=0.03,rounding_size=0.08',
                               facecolor='#E8ECEF', edgecolor='#BAC5CF', lw=1, zorder=2)
ax.add_patch(strip)
ax.text(5.25, 0.27,
        'Workflow: Mobile Photo Ingestion  ->  MATLAB Signal Profiling  ->  OpenCV Smart ROI Crop  ->  AI Tri-Model Inference  ->  3-Tier Web Output',
        fontsize=8.5, color='#2C3E50', fontweight='bold', ha='center', va='center', zorder=3)

plt.tight_layout()
out_file = 'analysis_output/report_assets/fig_software_stack_diagram.png'
plt.savefig(out_file, dpi=300, bbox_inches='tight')
plt.close()
print("Successfully generated software stack diagram:", out_file)
