import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text

# Set UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"e:\Rotor"
CSV_PATH = os.path.join(BASE_DIR, "extracted_features_all.csv")
OUT_DIR = os.path.join(BASE_DIR, "analysis_output")
os.makedirs(OUT_DIR, exist_ok=True)

def load_data():
    # Read CSV manually or via numpy/custom to avoid pandas dependency issues if any
    import csv
    records = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            records.append(r)
            
    feature_names = [
        "void_area_pct", "slag_protrusion_pct", "circularity", "solidity",
        "aspect_ratio", "extent", "edge_density_pct", "glcm_contrast",
        "glcm_homogeneity", "glcm_energy", "glcm_entropy", "mean_saturation",
        "std_saturation", "mean_hue", "intensity_contrast_std"
    ]
    
    X = []
    y = []
    filenames = []
    for r in records:
        X.append([float(r[k]) for k in feature_names])
        y.append(0 if r["label"] == "good" else 1)
        filenames.append(r["filename"])
        
    return np.array(X), np.array(y), feature_names, filenames

def plot_correlation_heatmap(X, y, feature_names):
    # Include target label in correlation
    data = np.column_stack([X, y])
    names = [f.replace("_", " ").title() for f in feature_names] + ["Defect Status"]
    
    # Compute correlation matrix
    corr_matrix = np.corrcoef(data, rowvar=False)
    
    fig, ax = plt.subplots(figsize=(14, 12))
    cax = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    
    cbar = fig.colorbar(cax, shrink=0.8, pad=0.03)
    cbar.set_label("Pearson Correlation Coefficient (r)", fontsize=11, fontweight='bold')
    
    ax.set_xticks(range(len(names)))
    ax.set_yticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=9.5, fontweight='bold')
    ax.set_yticklabels(names, fontsize=9.5, fontweight='bold')
    
    # Annotate values
    for i in range(len(names)):
        for j in range(len(names)):
            val = corr_matrix[i, j]
            color = "white" if abs(val) > 0.55 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=8)
            
    plt.title("Pearson Feature Correlation Matrix: 15 Extracted Physical & Texture Descriptors\n(N=81 Cropped Rotor Welds)", 
              fontsize=14, fontweight='bold', pad=16)
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "feature_correlation_matrix.png")
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"Saved Correlation Heatmap to: {out_path}")
    return corr_matrix, names

def plot_pca_clusters(X, y, feature_names):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    var_exp = pca.explained_variance_ratio_ * 100
    print(f"PCA Variance Explained: PC1={var_exp[0]:.1f}%, PC2={var_exp[1]:.1f}%, Total={sum(var_exp):.1f}%")
    
    fig, ax = plt.subplots(figsize=(11, 8.5))
    
    # Plot Good vs Bad
    good_mask = (y == 0)
    bad_mask = (y == 1)
    
    ax.scatter(X_pca[good_mask, 0], X_pca[good_mask, 1], c='#2ea043', label=f'Good Welds (N={sum(good_mask)})',
               s=80, alpha=0.85, edgecolors='black', linewidth=1)
    ax.scatter(X_pca[bad_mask, 0], X_pca[bad_mask, 1], c='#f85149', label=f'Defective / Over-Melted (N={sum(bad_mask)})',
               s=80, alpha=0.85, edgecolors='black', linewidth=1)
    
    # Add 95% Confidence Ellipses
    def plot_ellipse(pts, color, label):
        cov = np.cov(pts, rowvar=False)
        mean = np.mean(pts, axis=0)
        vals, vecs = np.linalg.eigh(cov)
        order = vals.argsort()[::-1]
        vals, vecs = vals[order], vecs[:, order]
        theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
        w, h = 2 * 2.0 * np.sqrt(vals) # ~95% confidence
        ell = patches.Ellipse(xy=mean, width=w, height=h, angle=theta,
                              edgecolor=color, facecolor=color, alpha=0.15, linestyle='--', linewidth=2)
        ax.add_patch(ell)
        
    plot_ellipse(X_pca[good_mask], '#2ea043', 'Good Cluster (95% CI)')
    plot_ellipse(X_pca[bad_mask], '#f85149', 'Defective Cluster (95% CI)')
    
    # Add Feature Biplot Arrows (top 5 most influential features)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    norm_loadings = loadings / np.max(np.abs(loadings)) * 3.5 # scale for display
    
    magnitudes = np.linalg.norm(norm_loadings, axis=1)
    top_feat_idx = magnitudes.argsort()[::-1][:5]
    
    for idx in top_feat_idx:
        ax.arrow(0, 0, norm_loadings[idx, 0], norm_loadings[idx, 1],
                 head_width=0.15, head_length=0.2, color='#1e3a8a', alpha=0.75, linewidth=1.5)
        ax.text(norm_loadings[idx, 0] * 1.15, norm_loadings[idx, 1] * 1.15,
                feature_names[idx].replace("_", " ").title(),
                color='#1e3a8a', fontsize=9.5, fontweight='bold', ha='center', va='center')

    ax.set_xlabel(f"Principal Component 1 (PC1) — {var_exp[0]:.1f}% Variance Explained\n(Rim Geometry & Molten Runoff)", fontsize=11, fontweight='bold')
    ax.set_ylabel(f"Principal Component 2 (PC2) — {var_exp[1]:.1f}% Variance Explained\n(Surface Roughness & Texture Dispersion)", fontsize=11, fontweight='bold')
    ax.set_title("PCA 2D Dimensionality Reduction: Rotor Weld Defect Separation\n(15 Physical Features Projected to 2D)", fontsize=13, fontweight='bold', pad=14)
    
    ax.axhline(0, color='gray', linestyle=':', alpha=0.6)
    ax.axvline(0, color='gray', linestyle=':', alpha=0.6)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(loc='upper right', fontsize=10.5, framealpha=0.95)
    
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "pca_cluster_separation.png")
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"Saved PCA Cluster Plot to: {out_path}")
    
    return pca, X_pca

def plot_pca_loadings(pca, feature_names):
    # PC1 and PC2 feature loadings
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    names = [f.replace("_", " ").title() for f in feature_names]
    pc1_loadings = pca.components_[0]
    pc2_loadings = pca.components_[1]
    
    # Sort PC1
    idx1 = np.argsort(pc1_loadings)
    colors1 = ['#f85149' if val < 0 else '#2ea043' for val in pc1_loadings[idx1]]
    ax1.barh([names[i] for i in idx1], pc1_loadings[idx1], color=colors1)
    ax1.set_title("PC1 Feature Loadings (Dominant Defect Drivers)", fontsize=11, fontweight='bold')
    ax1.set_xlabel("Loading Coefficient", fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # Sort PC2
    idx2 = np.argsort(pc2_loadings)
    colors2 = ['#1f6feb' for _ in idx2]
    ax2.barh([names[i] for i in idx2], pc2_loadings[idx2], color=colors2)
    ax2.set_title("PC2 Feature Loadings (Secondary Texture Dynamics)", fontsize=11, fontweight='bold')
    ax2.set_xlabel("Loading Coefficient", fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    plt.suptitle("PCA Component Loadings: Measuring Feature Contribution to Variance", fontsize=13, fontweight='bold')
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "pca_feature_loadings.png")
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"Saved PCA Loadings Plot to: {out_path}")

def generate_decision_tree(X, y, feature_names):
    clean_names = [f.replace("_", " ").title() for f in feature_names]
    dt = DecisionTreeClassifier(max_depth=3, min_samples_leaf=3, random_state=42)
    dt.fit(X, y)
    
    acc = dt.score(X, y) * 100
    print(f"Explainable Decision Tree Accuracy: {acc:.1f}%")
    
    fig, ax = plt.subplots(figsize=(16, 8))
    plot_tree(
        dt,
        feature_names=clean_names,
        class_names=["GOOD (PASS)", "DEFECTIVE (REJECT)"],
        filled=True,
        rounded=True,
        fontsize=9,
        ax=ax
    )
    plt.title(f"Explainable Production Decision Tree: Automated Rule Induction (Accuracy: {acc:.1f}%)\nHuman-Readable Inspection Logic for Industrial Quality Assurance", 
              fontsize=13, fontweight='bold', pad=12)
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "explainable_decision_tree.png")
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"Saved Explainable Decision Tree to: {out_path}")
    
    tree_rules = export_text(dt, feature_names=clean_names)
    print("\n--- INDUCED FACTORY QUALITY RULES ---")
    print(tree_rules)
    with open(os.path.join(OUT_DIR, "quality_inspection_rules.txt"), "w", encoding="utf-8") as f:
        f.write(tree_rules)

def main():
    X, y, feature_names, filenames = load_data()
    print(f"Loaded {len(X)} samples with {len(feature_names)} features.")
    
    corr_matrix, names = plot_correlation_heatmap(X, y, feature_names)
    pca, X_pca = plot_pca_clusters(X, y, feature_names)
    plot_pca_loadings(pca, feature_names)
    generate_decision_tree(X, y, feature_names)

if __name__ == "__main__":
    main()
