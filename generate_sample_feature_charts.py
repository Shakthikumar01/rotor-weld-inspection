import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# Set publication style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'cm'

BASE_DIR = r"e:\Rotor"
CSV_PATH = os.path.join(BASE_DIR, "extracted_features_all.csv")
OUT_DIR = os.path.join(BASE_DIR, "analysis_output", "report_assets")
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load data
records = []
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        records.append(r)

feature_names = [
    'void_area_pct', 'slag_protrusion_pct', 'circularity', 'solidity',
    'aspect_ratio', 'extent', 'edge_density_pct', 'glcm_contrast',
    'glcm_homogeneity', 'glcm_energy', 'glcm_entropy', 'mean_saturation',
    'std_saturation', 'mean_hue', 'intensity_contrast_std'
]

display_names = {
    'void_area_pct': 'Void Area %',
    'slag_protrusion_pct': 'Slag Protrusion %',
    'circularity': 'Circularity',
    'solidity': 'Convex Solidity',
    'aspect_ratio': 'Aspect Ratio',
    'extent': 'Bounding Extent',
    'edge_density_pct': 'Sobel Edge Density %',
    'glcm_contrast': 'GLCM Contrast',
    'glcm_homogeneity': 'GLCM Homogeneity',
    'glcm_energy': 'GLCM Energy',
    'glcm_entropy': 'GLCM Entropy',
    'mean_saturation': 'Mean Saturation (HSV)',
    'std_saturation': 'Std Dev Saturation (HSV)',
    'mean_hue': 'Mean Hue (HSV)',
    'intensity_contrast_std': 'Intensity Contrast Std'
}

X = np.array([[float(r[k]) for k in feature_names] for r in records])
y = np.array([0 if r['label'] == 'good' else 1 for r in records])

# Train Random Forest to get Gini importance
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)
importances = rf.feature_importances_

# Sort by importance
sorted_idx = np.argsort(importances)
sorted_names = [display_names[feature_names[i]] for i in sorted_idx]
sorted_vals = importances[sorted_idx] * 100

# ----------------------------------------------------
# FIGURE 5.3: Sample Feature Importance Ranking
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=300)

# Colors based on category: Geometric, Texture, Color/Intensity
colors = []
for name in sorted_names:
    if any(k in name for k in ['Void', 'Slag', 'Circularity', 'Solidity', 'Aspect', 'Extent']):
        colors.append('#1976D2') # Blue: Geometric/Morphological
    elif 'GLCM' in name or 'Edge' in name:
        colors.append('#388E3C') # Green: Texture
    else:
        colors.append('#E65100') # Orange: Intensity/Color

bars = ax.barh(range(len(sorted_names)), sorted_vals, color=colors, edgecolor='#263238', height=0.72, zorder=3)

# Add value labels on bars
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.25, bar.get_y() + bar.get_height()/2, f"{w:.1f}%",
            va='center', ha='left', fontsize=8.0, fontweight='bold', color='#263238')

ax.set_yticks(range(len(sorted_names)))
ax.set_yticklabels(sorted_names, fontsize=8.5, fontweight='bold', color='#1A237E')
ax.set_xlabel('Predictive Gini Feature Importance Score (%)', fontsize=9.5, fontweight='bold', color='#263238')
ax.set_title('Supervised Feature Importance Ranking Across 15 Sample Descriptors (Zero PCA)', fontsize=10.5, fontweight='bold', color='#0D47A1', pad=8)
ax.set_xlim(0, max(sorted_vals) + 3.2)
ax.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)

# Custom legend for categories
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#1976D2', edgecolor='#263238', label='Morphological / Geometric'),
    Patch(facecolor='#388E3C', edgecolor='#263238', label='GLCM Texture Descriptors'),
    Patch(facecolor='#E65100', edgecolor='#263238', label='Color / Intensity Moments')
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8.0, framealpha=0.92)

plt.tight_layout()
fig_53_path = os.path.join(OUT_DIR, "fig_sample_feature_importance.png")
fig.savefig(fig_53_path, dpi=300)
plt.close(fig)
print(f"Generated Figure 5.3: {fig_53_path}")

# ----------------------------------------------------
# FIGURE 5.4: Top 4 Sample Feature Distribution (Sound vs Defective)
# ----------------------------------------------------
top_4_keys = ['std_saturation', 'void_area_pct', 'slag_protrusion_pct', 'solidity']
top_4_titles = [
    '(a) Std Dev Saturation (HSV)',
    '(b) Void Area Percentage (%)',
    '(c) Slag Protrusion Percentage (%)',
    '(d) Convex Solidity Ratio'
]

fig, axes = plt.subplots(1, 4, figsize=(10.5, 3.6), dpi=300)

for idx, key in enumerate(top_4_keys):
    ax = axes[idx]
    col_idx = feature_names.index(key)
    sound_vals = X[y == 0, col_idx]
    defective_vals = X[y == 1, col_idx]
    
    # Boxplot
    bp = ax.boxplot([sound_vals, defective_vals], patch_artist=True, widths=0.55,
                    medianprops=dict(color='black', linewidth=1.5),
                    whiskerprops=dict(color='#37474F', linewidth=1.2),
                    capprops=dict(color='#37474F', linewidth=1.2))
    
    bp['boxes'][0].set(facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.3) # Green for Sound
    bp['boxes'][1].set(facecolor='#FFCDD2', edgecolor='#C62828', linewidth=1.3) # Red for Defective
    
    # Scatter points with jitter
    np.random.seed(42)
    jitter_s = np.random.normal(0, 0.04, size=len(sound_vals))
    jitter_d = np.random.normal(0, 0.04, size=len(defective_vals))
    ax.scatter(np.ones_like(sound_vals) + jitter_s, sound_vals, color='#1B5E20', alpha=0.65, s=18, zorder=4)
    ax.scatter(np.ones_like(defective_vals)*2 + jitter_d, defective_vals, color='#B71C1C', alpha=0.65, s=18, zorder=4)
    
    ax.set_xticklabels(['Sound\n(n=54)', 'Defective\n(n=27)'], fontsize=8.5, fontweight='bold')
    ax.set_title(top_4_titles[idx], fontsize=9.0, fontweight='bold', color='#1A237E', pad=6)
    ax.grid(axis='y', linestyle=':', alpha=0.6)

plt.suptitle('Primary Sample Feature Distribution Comparison Across Sound and Defective Rotors',
             fontsize=10.5, fontweight='bold', color='#0D47A1', y=1.02)
plt.tight_layout()
fig_54_path = os.path.join(OUT_DIR, "fig_sample_feature_distributions.png")
fig.savefig(fig_54_path, dpi=300)
plt.close(fig)
print(f"Generated Figure 5.4: {fig_54_path}")
