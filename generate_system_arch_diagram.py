import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set font to Times New Roman
plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['font.family'] = 'serif'

fig, ax = plt.subplots(figsize=(10.5, 4.2), dpi=300)
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 4.2)
ax.axis('off')

# Stage 1: Optical Acquisition (Blue theme) - Updated for Mobile Camera
# Stage 2: Saliency Cropping (Teal/Green theme)
# Stage 3: Feature & AI (Purple/Indigo theme)
# Stage 4: 3-Tier Sorting (Amber/Orange theme)

stages = [
    {
        'x': 0.25, 'w': 2.2, 'title': 'STAGE 1', 'sub': 'Image Acquisition',
        'color': '#EBF3FA', 'border': '#1F4E79',
        'items': [
            'Mobile Phone Camera',
            'Macro Weld Seam Capture',
            'Uniform Diffused Light',
            'High-Res Image (JPG/PNG)'
        ]
    },
    {
        'x': 2.85, 'w': 2.2, 'title': 'STAGE 2', 'sub': 'Weld ROI Cropping',
        'color': '#EAF7ED', 'border': '#2E7D32',
        'items': [
            'Dual-Axis Sobel Gradient',
            'Otsu Saliency Binarization',
            'Morphological Closure',
            'Droop Margin Inflation'
        ]
    },
    {
        'x': 5.45, 'w': 2.2, 'title': 'STAGE 3', 'sub': 'AI Defect Detection',
        'color': '#F3EDFA', 'border': '#6A1B9A',
        'items': [
            '15 Mathematical Descriptors',
            'GLCM Haralick Texture',
            'Explainable Decision Tree',
            'MobileNetV3 Deep Vision'
        ]
    },
    {
        'x': 8.05, 'w': 2.2, 'title': 'STAGE 4', 'sub': '3-Tier Industrial Output',
        'color': '#FFF5E6', 'border': '#E65100',
        'items': [
            'Tier 1: Accept (Pass)',
            'Tier 2: Rework (TIG Repair)',
            'Tier 3: Scrap (Reject)',
            'Web UI & ISO Certificate'
        ]
    }
]

for s in stages:
    # Outer box
    rect = patches.FancyBboxPatch(
        (s['x'], 0.35), s['w'], 3.5,
        boxstyle='round,pad=0.1,rounding_size=0.18',
        facecolor=s['color'], edgecolor=s['border'],
        linewidth=1.8
    )
    ax.add_patch(rect)

    # Header banner
    banner = patches.FancyBboxPatch(
        (s['x'], 3.1), s['w'], 0.75,
        boxstyle='round,pad=0.08,rounding_size=0.14',
        facecolor=s['border'], edgecolor=s['border'],
        linewidth=1
    )
    ax.add_patch(banner)

    # Header text
    ax.text(s['x'] + s['w']/2, 3.58, s['title'],
            color='white', fontsize=12, fontweight='bold', ha='center', va='center')
    ax.text(s['x'] + s['w']/2, 3.28, s['sub'],
            color='#E0E0E0', fontsize=10, fontstyle='italic', ha='center', va='center')

    # Content items
    start_y = 2.65
    for i, itm in enumerate(s['items']):
        y = start_y - i * 0.62
        ax.plot(s['x'] + 0.22, y, marker='o', color=s['border'], markersize=4.5)
        ax.text(s['x'] + 0.35, y, itm,
                color='#1A1A1A', fontsize=9.2, va='center', fontweight='medium')

# Connecting arrows between stages
arrow_props = dict(facecolor='#424242', edgecolor='#424242', width=2.5, headwidth=8.5, headlength=7.5)
for x_start in [2.50, 5.10, 7.70]:
    ax.annotate('', xy=(x_start + 0.30, 2.1), xytext=(x_start + 0.02, 2.1),
                arrowprops=arrow_props)

plt.tight_layout()
out_path = 'analysis_output/report_assets/fig_system_architecture_diagram.png'
plt.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close()
print('Successfully generated updated architecture diagram:', out_path)
