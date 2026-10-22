import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

BASE_DIR = r"e:\Rotor"
OUTPUT_DIR = os.path.join(BASE_DIR, "analysis_output")
REPORT_ASSETS_DIR = os.path.join(OUTPUT_DIR, "report_assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_ASSETS_DIR, exist_ok=True)

# -------------------------------------------------------------
# Chart 1: Confusion Matrix, Dual-Model Comparison & Ablation
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=300)
plt.subplots_adjust(wspace=0.32)

# Subplot 1: Deep MobileNetV3 Confusion Matrix (N=81)
cm = np.array([[22, 5],
               [3, 51]])
total_samples = np.sum(cm) # 81

im = axes[0].imshow(cm, cmap='Blues', interpolation='nearest')
axes[0].set_title('Deep MobileNetV3 Confusion Matrix\n(5-Fold Stratified CV, N=81)', fontsize=12, fontweight='bold', pad=12, color='#0f172a')
tick_marks = np.arange(2)
axes[0].set_xticks(tick_marks)
axes[0].set_xticklabels(['Nominal (Pass)', 'Defect (Reject)'], fontsize=10, fontweight='bold')
axes[0].set_yticks(tick_marks)
axes[0].set_yticklabels(['Nominal (Pass)', 'Defect (Reject)'], fontsize=10, fontweight='bold')

for i in range(2):
    for j in range(2):
        val = cm[i, j]
        pct = (val / total_samples) * 100
        color = 'white' if val > 20 else '#0f172a'
        label = f"{val}\n({pct:.1f}%)"
        if i == 1 and j == 1:
            label += "\n[94.4% Recall]"
        elif i == 0 and j == 0:
            label += "\n[81.5% Spec]"
        axes[0].text(j, i, label, ha="center", va="center", color=color, fontsize=10, fontweight='bold')

axes[0].set_xlabel('Predicted Verdict', fontsize=11, fontweight='bold', labelpad=8)
axes[0].set_ylabel('True Industrial Label', fontsize=11, fontweight='bold', labelpad=8)
cbar = fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=9)

# Subplot 2: Dual-Model Performance Benchmarking (Random Forest REMOVED)
models = ['Explainable Decision Tree\n(White-Box 15 Features)', 'Deep MobileNetV3\n(Transfer Learning CNN)']
accs = [80.2, 90.2]
recalls = [85.2, 94.4]
f1s = [84.9, 92.7]

x = np.arange(len(models))
width = 0.24

rects1 = axes[1].bar(x - width, accs, width, label='5-Fold CV Acc', color='#3b82f6', edgecolor='#1e3a8a', linewidth=0.8)
rects2 = axes[1].bar(x, recalls, width, label='Defect Recall', color='#10b981', edgecolor='#065f46', linewidth=0.8)
rects3 = axes[1].bar(x + width, f1s, width, label='F1-Score (%)', color='#8b5cf6', edgecolor='#4c1d95', linewidth=0.8)

axes[1].set_ylabel('Score (%)', fontsize=11, fontweight='bold')
axes[1].set_title('Dual-Model Performance Benchmark\n(Cross-Validation on Cropped Rotors)', fontsize=12, fontweight='bold', pad=12, color='#0f172a')
axes[1].set_xticks(x)
axes[1].set_xticklabels(models, fontsize=9.5, fontweight='bold')
axes[1].set_ylim(60, 102)
axes[1].grid(axis='y', linestyle='--', alpha=0.5)
axes[1].legend(loc='lower right', frameon=True, fontsize=9)

for rects in [rects1, rects2, rects3]:
    for rect in rects:
        height = rect.get_height()
        axes[1].annotate(f'{height:.1f}%',
                         xy=(rect.get_x() + rect.get_width() / 2, height),
                         xytext=(0, 3), textcoords="offset points",
                         ha='center', va='bottom', fontsize=9, fontweight='bold')

# Subplot 3: Cropping Ablation Gain
stages = ['Uncropped\nRaw Capture', 'Saliency-Guided\nWeld-ROI Crop']
acc_abl = [74.1, 90.2]

color_gain = ['#94a3b8', '#0284c7']
bars_abl = axes[2].bar(stages, acc_abl, color=color_gain, width=0.55, edgecolor='#0f172a', linewidth=1)
axes[2].set_title('ROI Cropper Ablation Impact\n(Eliminating Shop Clutter)', fontsize=12, fontweight='bold', pad=12, color='#0f172a')
axes[2].set_ylabel('Accuracy (%)', fontsize=11, fontweight='bold')
axes[2].set_ylim(50, 102)
axes[2].grid(axis='y', linestyle='--', alpha=0.5)

axes[2].annotate('+16.1% Accuracy Boost\nSlashes Escapes 12 -> 3',
                 xy=(1, 90.2), xytext=(0.35, 76),
                 arrowprops=dict(facecolor='#10b981', shrink=0.08, width=2, headwidth=8),
                 fontsize=10, fontweight='bold', color='#065f46',
                 bbox=dict(boxstyle="round,pad=0.4", fc="#d1fae5", ec="#10b981", lw=1.2))

for bar, val in zip(bars_abl, acc_abl):
    axes[2].text(bar.get_x() + bar.get_width()/2, val + 1, f"{val:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()

chart1_path = os.path.join(OUTPUT_DIR, "confusion_matrix_and_metrics.png")
fig_asset_path = os.path.join(REPORT_ASSETS_DIR, "fig_confusion_matrix.png")
plt.savefig(chart1_path, dpi=300)
plt.savefig(fig_asset_path, dpi=300)
plt.close()
print(f"Generated: {chart1_path}")
print(f"Generated: {fig_asset_path}")

# -------------------------------------------------------------
# Chart 2: End-to-End Cyber-Physical Architecture Diagram
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 5.5), dpi=300)
ax.axis('off')

# Stage 1: Acquisition
rect1 = patches.FancyBboxPatch((0.02, 0.25), 0.20, 0.65, boxstyle="round,pad=0.03", fc="#eff6ff", ec="#2563eb", lw=2)
ax.add_patch(rect1)
ax.text(0.12, 0.82, "STAGE 1\nIMAGE INGESTION", ha="center", va="center", fontsize=11, fontweight="bold", color="#1e3a8a")
ax.text(0.12, 0.52, "• 81 Captures (4080x3060)\n• Axial Normal (0° View)\n• Oblique Profile (45° View)\n• Diffuse Ring LED (High CRI)\n• Mixed Shop Clutter\n• Operator Clothing (Denim)", ha="center", va="center", fontsize=9, color="#1e293b")

ax.annotate("", xy=(0.26, 0.57), xytext=(0.23, 0.57), arrowprops=dict(arrowstyle="->", lw=2.5, color="#2563eb"))

# Stage 2: Cropping Engine
rect2 = patches.FancyBboxPatch((0.27, 0.25), 0.22, 0.65, boxstyle="round,pad=0.03", fc="#f0fdf4", ec="#16a34a", lw=2)
ax.add_patch(rect2)
ax.text(0.38, 0.82, "STAGE 2\nSALIENCY CROPPING", ha="center", va="center", fontsize=11, fontweight="bold", color="#14532d")
ax.text(0.38, 0.52, "• Sobel Filter (Gx & Gy, 3x3)\n• G_mag Gradient Energy\n• Gaussian Texture Blur (σ=35)\n• 2D Radial Center-Prior\n• Otsu + Elliptical Closing\n• +65% Downward Expansion\n  (Preserves Molten Icicles)", ha="center", va="center", fontsize=9, color="#1e293b")

ax.annotate("", xy=(0.53, 0.57), xytext=(0.50, 0.57), arrowprops=dict(arrowstyle="->", lw=2.5, color="#16a34a"))

# Stage 3: Dual-Model AI Core (Random Forest removed)
rect3 = patches.FancyBboxPatch((0.54, 0.15), 0.24, 0.78, boxstyle="round,pad=0.03", fc="#faf5ff", ec="#9333ea", lw=2)
ax.add_patch(rect3)
ax.text(0.66, 0.86, "STAGE 3\nDUAL-MODEL AI ENGINE", ha="center", va="center", fontsize=11, fontweight="bold", color="#581c87")
ax.text(0.66, 0.51, "1. Deep MobileNetV3 Backbone\n   • 576-dim Latent Space\n   • 90.2% Acc | 94.4% Recall\n   • Primary Defect Hunter\n   • Latency: ~42.5 ms\n\n2. Auditable Decision Tree\n   • White-Box Gini Rules\n   • 15 Physical Features\n   • 80.2% Acc | 2.1 ms\n   • ISO 9001 Compliance", ha="center", va="center", fontsize=8.5, color="#1e293b")

ax.annotate("", xy=(0.82, 0.57), xytext=(0.79, 0.57), arrowprops=dict(arrowstyle="->", lw=2.5, color="#9333ea"))

# Stage 4: Industrial Output & Sorting
rect4 = patches.FancyBboxPatch((0.83, 0.20), 0.15, 0.72, boxstyle="round,pad=0.03", fc="#fff7ed", ec="#ea580c", lw=2)
ax.add_patch(rect4)
ax.text(0.905, 0.84, "STAGE 4\n3-TIER SORTING", ha="center", va="center", fontsize=11, fontweight="bold", color="#7c2d12")
ax.text(0.905, 0.52, "[Grade A: Pass]\n   Stator Assembly\n\n[Grade B: Rework]\n   Deburr & Buffing\n\n[Grade C: Scrap]\n   Immediate Recycle\n\n[ISO 9001 Cert]\n   QC-WELD-XXXX", ha="center", va="center", fontsize=8.5, color="#1e293b")

plt.tight_layout()
chart2_path = os.path.join(OUTPUT_DIR, "pipeline_workflow_diagram.png")
chart2_asset = os.path.join(REPORT_ASSETS_DIR, "fig_pipeline_arch.png")
plt.savefig(chart2_path, dpi=300)
plt.savefig(chart2_asset, dpi=300)
plt.close()
print(f"Generated: {chart2_path}")
print(f"Generated: {chart2_asset}")
