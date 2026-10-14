import os
import sys
import glob
import numpy as np

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import torch
import torchvision.models as models
from PIL import Image
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

BASE_DIR = r"e:\Rotor"
CROPPED_DIR = os.path.join(BASE_DIR, "dataset_cropped")
GOOD_DIR = os.path.join(CROPPED_DIR, "good")
BAD_DIR = os.path.join(CROPPED_DIR, "bad")

MODEL_DEEP_FILE = os.path.join(BASE_DIR, "trained_deep_model.pkl")

def main():
    good_files = sorted(glob.glob(os.path.join(GOOD_DIR, "*.jpeg")) + glob.glob(os.path.join(GOOD_DIR, "*.jpg")))
    bad_files = sorted(glob.glob(os.path.join(BAD_DIR, "*.jpeg")) + glob.glob(os.path.join(BAD_DIR, "*.jpg")))

    all_files = good_files + bad_files
    y = np.array([0] * len(good_files) + [1] * len(bad_files))
    
    print(f"Training on CROPPED WELD DATASET: {len(good_files)} Good, {len(bad_files)} Bad (Total: {len(all_files)})")

    # Load pretrained MobileNetV3
    print("Loading pretrained PyTorch MobileNetV3...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    weights = models.MobileNet_V3_Small_Weights.DEFAULT
    model = models.mobilenet_v3_small(weights=weights)
    preprocess = weights.transforms()
    model.classifier = torch.nn.Identity()
    model = model.to(device)
    model.eval()

    print("Extracting deep vision embeddings from cropped welds...")
    deep_features = []
    with torch.no_grad():
        for p in all_files:
            img = Image.open(p).convert("RGB")
            t_img = preprocess(img).unsqueeze(0).to(device)
            feat = model(t_img).squeeze().cpu().numpy()
            deep_features.append(feat)

    deep_features = np.array(deep_features)
    print(f"Deep feature matrix shape: {deep_features.shape}")

    # 5-Fold Stratified Cross-Validation
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    clf = LogisticRegression(max_iter=1000, C=1.0)
    
    fold_accs = []
    all_preds = []
    all_targets = []
    
    for train_idx, val_idx in skf.split(deep_features, y):
        X_tr, X_val = deep_features[train_idx], deep_features[val_idx]
        y_tr, y_val = y[train_idx], y[val_idx]
        clf.fit(X_tr, y_tr)
        preds = clf.predict(X_val)
        fold_accs.append(accuracy_score(y_val, preds))
        all_preds.extend(preds)
        all_targets.extend(y_val)

    mean_acc = np.mean(fold_accs) * 100
    cm = confusion_matrix(all_targets, all_preds)
    
    print("\n" + "="*50)
    print(f"🎯 5-FOLD CV ACCURACY ON CROPPED WELDS: {mean_acc:.1f}%")
    print(f"   True Positives (Defective caught): {cm[1][1]} / 54 ({(cm[1][1]/54)*100:.1f}%)")
    print(f"   True Negatives (Good passed):      {cm[0][0]} / 27 ({(cm[0][0]/27)*100:.1f}%)")
    print("="*50)

    # Train final production model on full dataset
    clf.fit(deep_features, y)
    joblib.dump(clf, MODEL_DEEP_FILE)
    print(f"\nSaved updated production model to: {MODEL_DEEP_FILE}")

if __name__ == "__main__":
    main()
