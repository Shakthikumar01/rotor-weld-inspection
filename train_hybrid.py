import os
import json
import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

LABELS_FILE = r"e:\Rotor\dataset_labels.json"
IMG_DIR = r"e:\Rotor\images"

def main():
    with open(LABELS_FILE, "r") as f:
        labels = json.load(f)

    # Prepare dataset
    fnames = []
    y = []
    for fn, l in labels.items():
        if l in ["good", "bad"]:
            p = os.path.join(IMG_DIR, fn)
            if os.path.exists(p):
                fnames.append(fn)
                y.append(0 if l == "good" else 1)

    y = np.array(y)
    print(f"Loaded {len(fnames)} images. Good: {sum(y==0)}, Bad: {sum(y==1)}")

    # Load pretrained model
    print("Loading pretrained MobileNetV3 / ResNet-18...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Use MobileNetV3-Small for lightweight, fast extraction
    try:
        weights = models.MobileNet_V3_Small_Weights.DEFAULT
        model = models.mobilenet_v3_small(weights=weights)
        preprocess = weights.transforms()
    except Exception as e:
        print("Falling back to ResNet18:", e)
        weights = models.ResNet18_Weights.DEFAULT
        model = models.resnet18(weights=weights)
        preprocess = weights.transforms()

    # Feature extractor (remove final classifier)
    if hasattr(model, 'classifier'):
        model.classifier = torch.nn.Identity()
    elif hasattr(model, 'fc'):
        model.fc = torch.nn.Identity()

    model = model.to(device)
    model.eval()

    print("Extracting deep vision features for all 81 images...")
    deep_features = []
    with torch.no_grad():
        for fn in fnames:
            p = os.path.join(IMG_DIR, fn)
            img = Image.open(p).convert("RGB")
            t_img = preprocess(img).unsqueeze(0).to(device)
            feat = model(t_img).squeeze().cpu().numpy()
            deep_features.append(feat)

    deep_features = np.array(deep_features)
    print(f"Deep feature matrix shape: {deep_features.shape}")

    # Evaluate using 5-Fold Stratified Cross Validation
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    classifiers = {
        "Logistic Regression (L2)": LogisticRegression(max_iter=1000, C=1.0),
        "Support Vector Machine (RBF)": SVC(C=2.0, kernel='rbf', probability=True),
        "Random Forest (Deep Features)": RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    }

    print("\n--- 5-FOLD CROSS-VALIDATION RESULTS (PRETRAINED DEEP FEATURES) ---")
    for name, clf in classifiers.items():
        fold_accs = []
        all_preds = []
        all_targets = []
        for train_idx, val_idx in skf.split(deep_features, y):
            X_tr, X_val = deep_features[train_idx], deep_features[val_idx]
            y_tr, y_val = y[train_idx], y[val_idx]

            clf.fit(X_tr, y_tr)
            preds = clf.predict(X_val)
            acc = accuracy_score(y_val, preds)
            fold_accs.append(acc)
            all_preds.extend(preds)
            all_targets.extend(y_val)

        mean_acc = np.mean(fold_accs) * 100
        print(f"\nModel: {name}")
        print(f"  CV Accuracy: {mean_acc:.1f}%")
        print("  Confusion Matrix:")
        cm = confusion_matrix(all_targets, all_preds)
        print(f"    [[TN (Good as Good)={cm[0][0]}, FP (Good as Bad)={cm[0][1]}],")
        print(f"     [FN (Bad as Good) ={cm[1][0]}, TP (Bad as Bad) ={cm[1][1]}]]")

if __name__ == "__main__":
    main()
