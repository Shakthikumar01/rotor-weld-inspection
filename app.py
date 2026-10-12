import os
import json
import base64
import time
import random
import numpy as np
import cv2
import torch
import torchvision.models as models
from PIL import Image
from flask import Flask, render_template, jsonify, request, send_from_directory
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import confusion_matrix
import joblib

app = Flask(__name__, template_folder="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

LABELS_FILE = os.path.join(BASE_DIR, "dataset_labels.json")
MODEL_CV_FILE = os.path.join(BASE_DIR, "trained_cv_model.pkl")
MODEL_DEEP_FILE = os.path.join(BASE_DIR, "trained_deep_model.pkl")

# Initialize Pretrained MobileNetV3 Extractor
print("Initializing Pretrained Deep Vision Extractor...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
weights = models.MobileNet_V3_Small_Weights.DEFAULT
deep_model = models.mobilenet_v3_small(weights=weights)
preprocess = weights.transforms()
deep_model.classifier = torch.nn.Identity()
deep_model = deep_model.to(device)
deep_model.eval()

def load_labels():
    if os.path.exists(LABELS_FILE):
        try:
            with open(LABELS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_labels(labels):
    with open(LABELS_FILE, "w") as f:
        json.dump(labels, f, indent=2)

def extract_cv_features(img_path):
    bgr = cv2.imread(img_path)
    if bgr is None:
        return None, {}

    target_dim = 800
    h, w = bgr.shape[:2]
    scale = target_dim / max(h, w)
    resized = cv2.resize(bgr, (int(w * scale), int(h * scale)))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    total_pixels = resized.shape[0] * resized.shape[1]

    # 1. Edge & Contour features
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 40, 140)
    edge_density = float(np.sum(edges > 0) / total_pixels)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated_edges = cv2.dilate(edges, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    circularity = 0.0
    solidity = 0.0
    aspect_ratio = 1.0
    
    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        main_c = contours[0]
        area = cv2.contourArea(main_c)
        perimeter = cv2.arcLength(main_c, True)
        if perimeter > 0:
            circularity = float((4 * np.pi * area) / (perimeter ** 2))
        
        hull = cv2.convexHull(main_c)
        hull_area = cv2.contourArea(hull)
        if hull_area > 0:
            solidity = float(area / hull_area)
            
        x, y, cw, ch = cv2.boundingRect(main_c)
        aspect_ratio = float(cw / ch) if ch > 0 else 1.0

    # 2. Dark Cavity / Voids
    _, dark_cavities = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    dark_cavities = cv2.morphologyEx(dark_cavities, cv2.MORPH_OPEN, kernel)
    void_pct = float((np.sum(dark_cavities > 0) / total_pixels) * 100)

    # 3. Thermal Slag & Melt Discoloration
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    h_chan, s_chan, v_chan = cv2.split(hsv)
    _, slag_mask = cv2.threshold(s_chan, 110, 255, cv2.THRESH_BINARY)
    slag_mask = cv2.bitwise_and(slag_mask, cv2.threshold(v_chan, 70, 255, cv2.THRESH_BINARY)[1])
    slag_pct = float((np.sum(slag_mask > 0) / total_pixels) * 100)

    mean_sat = float(np.mean(s_chan))
    std_sat = float(np.std(s_chan))

    features = [
        round(void_pct, 3),
        round(slag_pct, 3),
        round(circularity, 4),
        round(solidity, 4),
        round(edge_density * 100, 3),
        round(mean_sat, 2),
        round(std_sat, 2),
        round(aspect_ratio, 3)
    ]

    metrics = {
        "void_pct": round(void_pct, 2),
        "slag_pct": round(slag_pct, 2),
        "circularity": round(circularity, 3),
        "solidity": round(solidity, 3),
        "edge_density": round(edge_density * 100, 2),
        "mean_sat": round(mean_sat, 1),
        "std_sat": round(std_sat, 1),
        "aspect_ratio": round(aspect_ratio, 2)
    }

    vis_contour = rgb.copy()
    if contours:
        cv2.drawContours(vis_contour, contours[:2], -1, (0, 255, 0), 3)

    vis_slag = rgb.copy()
    vis_slag[slag_mask > 0] = [255, 60, 0]

    vis_void = rgb.copy()
    vis_void[dark_cavities > 0] = [0, 160, 255]

    return features, {
        "metrics": metrics,
        "edge_b64": to_base64_jpeg(edges),
        "contour_b64": to_base64_jpeg(cv2.cvtColor(vis_contour, cv2.COLOR_RGB2BGR)),
        "slag_b64": to_base64_jpeg(cv2.cvtColor(vis_slag, cv2.COLOR_RGB2BGR)),
        "void_b64": to_base64_jpeg(cv2.cvtColor(vis_void, cv2.COLOR_RGB2BGR))
    }

def extract_deep_feature(img_path):
    img = Image.open(img_path).convert("RGB")
    t_img = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        feat = deep_model(t_img).squeeze().cpu().numpy()
    return feat

def to_base64_jpeg(img):
    _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return base64.b64encode(buf).decode("utf-8")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(IMG_DIR, filename)

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@app.route("/api/dataset")
def get_dataset():
    labels = load_labels()
    files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    ref_files = [f for f in ["good.jpeg", "bad.jpeg"] if f in files]
    other_files = [f for f in files if f not in ref_files]
    sorted_files = ref_files + sorted(other_files)

    data = [{"filename": f, "label": labels.get(f, None)} for f in sorted_files]
    good_cnt = sum(1 for d in data if d["label"] == "good")
    bad_cnt = sum(1 for d in data if d["label"] == "bad")
    unlabeled_cnt = sum(1 for d in data if d["label"] is None)

    return jsonify({
        "images": data,
        "total": len(data),
        "good": good_cnt,
        "bad": bad_cnt,
        "unlabeled": unlabeled_cnt
    })

@app.route("/api/label", methods=["POST"])
def set_label():
    req = request.json
    filename = req.get("filename")
    label = req.get("label")
    labels = load_labels()
    if label in ["good", "bad"]:
        labels[filename] = label
    elif filename in labels:
        del labels[filename]
    save_labels(labels)
    return jsonify({"status": "success", "filename": filename, "label": label})

@app.route("/api/analyze/<path:filename>")
def analyze_single(filename):
    img_path = os.path.join(IMG_DIR, filename)
    if not os.path.exists(img_path):
        return jsonify({"error": "File not found"}), 404
    _, analysis = extract_cv_features(img_path)
    return jsonify(analysis)

@app.route("/api/train", methods=["POST"])
def train_model():
    labels = load_labels()
    labeled_items = [(f, l) for f, l in labels.items() if l in ["good", "bad"]]
    
    if len(labeled_items) < 6:
        return jsonify({"error": "Please label at least 6 images before training."}), 400

    X_cv = []
    X_deep = []
    y = []

    for fname, label in labeled_items:
        p = os.path.join(IMG_DIR, fname)
        if os.path.exists(p):
            cv_f, _ = extract_cv_features(p)
            deep_f = extract_deep_feature(p)
            if cv_f is not None:
                X_cv.append(cv_f)
                X_deep.append(deep_f)
                y.append(1 if label == "bad" else 0)

    X_cv = np.array(X_cv)
    X_deep = np.array(X_deep)
    y = np.array(y)

    unique_classes, counts = np.unique(y, return_counts=True)
    if len(unique_classes) < 2:
        return jsonify({"error": "Need both good and bad samples to train."}), 400

    skf = StratifiedKFold(n_splits=min(5, min(counts)), shuffle=True, random_state=42)

    # 1. OpenCV Random Forest
    rf_cv = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    scores_cv = cross_val_score(rf_cv, X_cv, y, cv=skf)
    acc_cv = float(np.mean(scores_cv) * 100)
    rf_cv.fit(X_cv, y)
    joblib.dump(rf_cv, MODEL_CV_FILE)

    # 2. Deep Transfer Learning (Logistic / SVM)
    deep_clf = LogisticRegression(max_iter=1000, C=1.0)
    scores_deep = cross_val_score(deep_clf, X_deep, y, cv=skf)
    acc_deep = float(np.mean(scores_deep) * 100)
    deep_clf.fit(X_deep, y)
    joblib.dump(deep_clf, MODEL_DEEP_FILE)

    feature_names = [
        "Void Area %", "Slag / Melt %", "Circularity", "Solidity",
        "Edge Density", "Mean Saturation", "Std Saturation", "Aspect Ratio"
    ]
    importances = [round(float(imp), 4) for imp in rf_cv.feature_importances_]

    return jsonify({
        "status": "success",
        "samples_trained": len(y),
        "good_count": int(np.sum(y == 0)),
        "bad_count": int(np.sum(y == 1)),
        "cv_accuracy": round(acc_cv, 1),
        "deep_accuracy": round(acc_deep, 1),
        "feature_importances": dict(zip(feature_names, importances))
    })

@app.route("/api/inspect_upload", methods=["POST"])
def inspect_uploaded_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = f"inspect_{int(time.time())}_{file.filename}"
    save_path = os.path.join(UPLOAD_DIR, filename)
    file.save(save_path)

    # Run OpenCV analysis
    cv_feats, analysis = extract_cv_features(save_path)
    if cv_feats is None:
        return jsonify({"error": "Failed to process image"}), 400

    # Run Deep Feature Extraction
    deep_feats = extract_deep_feature(save_path)

    # Predict using trained models
    if os.path.exists(MODEL_DEEP_FILE):
        deep_clf = joblib.load(MODEL_DEEP_FILE)
        prob_bad = float(deep_clf.predict_proba([deep_feats])[0][1])
    else:
        # Fallback to CV heuristic
        prob_bad = 0.85 if (analysis["metrics"]["void_pct"] > 12.0 or analysis["metrics"]["slag_pct"] > 0.3) else 0.15

    is_bad = prob_bad >= 0.5
    verdict = "REJECT: DEFECTIVE WELD" if is_bad else "PASS: ACCEPTABLE WELD"
    confidence = round(prob_bad * 100 if is_bad else (1 - prob_bad) * 100, 1)

    # Generate Certificate Number
    cert_id = f"QC-ROTOR-{int(time.time())}-{random.randint(100, 999)}"

    return jsonify({
        "certificate_id": cert_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "filename": file.filename,
        "image_url": f"/uploads/{filename}",
        "verdict": verdict,
        "status": "REJECT" if is_bad else "PASS",
        "is_bad": bool(is_bad),
        "confidence": confidence,
        "metrics": analysis["metrics"],
        "overlays": {
            "contour": analysis["contour_b64"],
            "void": analysis["void_b64"],
            "slag": analysis["slag_b64"],
            "edge": analysis["edge_b64"]
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Rotor Inspection Web App on http://0.0.0.0:{port} ...")
    app.run(host="0.0.0.0", port=port, debug=False)
