import os
import json
import base64
import time
import random
import glob
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
CROPPED_DIR = os.path.join(BASE_DIR, "dataset_cropped")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(CROPPED_DIR, "good"), exist_ok=True)
os.makedirs(os.path.join(CROPPED_DIR, "bad"), exist_ok=True)

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

def crop_weld_roi(bgr):
    """Isolates the upper welded region and dripping slag, eliminating background & cylinder core."""
    if bgr is None:
        return None
    h, w = bgr.shape[:2]
    target_dim = 1000
    scale = target_dim / max(h, w)
    resized = cv2.resize(bgr, (int(w * scale), int(h * scale)))
    rh, rw = resized.shape[:2]

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(sobelx, sobely)
    mag = np.clip(mag, 0, 255).astype(np.uint8)
    texture = cv2.GaussianBlur(mag, (35, 35), 0)

    cy, cx = rh / 2.0, rw / 2.0
    y_coords, x_coords = np.indices((rh, rw))
    dist_from_center = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    max_dist = np.sqrt(cx**2 + cy**2)
    center_weight = 1.0 - 0.4 * (dist_from_center / max_dist)
    saliency = (texture.astype(np.float32) * center_weight).astype(np.uint8)

    _, thresh = cv2.threshold(saliency, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        rx, ry, rw_box, rh_box = int(rw*0.1), int(rh*0.05), int(rw*0.8), int(rh*0.8)
    else:
        best_c = max(contours, key=cv2.contourArea)
        rx, ry, rw_box, rh_box = cv2.boundingRect(best_c)

    aspect = rw_box / float(rh_box)
    if 0.75 < aspect < 1.3 and ry > rh * 0.04 and (ry + rh_box) < rh * 0.96:
        m = int(min(rw_box, rh_box) * 0.05)
        x1, y1 = max(0, rx - m), max(0, ry - m)
        x2, y2 = min(rw, rx + rw_box + m), min(rh, ry + rh_box + m)
    else:
        m_x = int(rw_box * 0.08)
        x1 = max(0, rx - m_x)
        x2 = min(rw, rx + rw_box + m_x)
        y1 = max(0, ry - int(rh_box * 0.05))
        y2 = min(rh, ry + int(rh_box * 0.65))

    inv_scale = 1.0 / scale
    ox1 = max(0, int(x1 * inv_scale))
    oy1 = max(0, int(y1 * inv_scale))
    ox2 = min(w, int(x2 * inv_scale))
    oy2 = min(h, int(y2 * inv_scale))

    if (ox2 - ox1) < 100 or (oy2 - oy1) < 100:
        return bgr
    return bgr[oy1:oy2, ox1:ox2]

def extract_cv_features(img_input, is_already_cropped=False):
    if isinstance(img_input, str):
        bgr = cv2.imread(img_input)
    else:
        bgr = img_input

    if bgr is None:
        return None, {}

    # If full raw image, crop strictly to weld ROI
    weld_roi = bgr if is_already_cropped else crop_weld_roi(bgr)

    target_dim = 800
    h, w = weld_roi.shape[:2]
    scale = target_dim / max(h, w)
    resized = cv2.resize(weld_roi, (int(w * scale), int(h * scale)))
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

    circularity, solidity, aspect_ratio = 0.0, 0.0, 1.0
    if contours:
        main_c = max(contours, key=cv2.contourArea)
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

    # 2. Voids / Missing Fusion
    _, dark_cavities = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    dark_cavities = cv2.morphologyEx(dark_cavities, cv2.MORPH_OPEN, kernel)
    void_pct = float((np.sum(dark_cavities > 0) / total_pixels) * 100)

    # 3. Slag & Thermal Melt Discoloration
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    h_chan, s_chan, v_chan = cv2.split(hsv)
    _, slag_mask = cv2.threshold(s_chan, 110, 255, cv2.THRESH_BINARY)
    slag_mask = cv2.bitwise_and(slag_mask, cv2.threshold(v_chan, 70, 255, cv2.THRESH_BINARY)[1])
    slag_pct = float((np.sum(slag_mask > 0) / total_pixels) * 100)

    features = [
        round(void_pct, 3), round(slag_pct, 3), round(circularity, 4),
        round(solidity, 4), round(edge_density * 100, 3),
        round(float(np.mean(s_chan)), 2), round(float(np.std(s_chan)), 2), round(aspect_ratio, 3)
    ]

    metrics = {
        "void_pct": round(void_pct, 2),
        "slag_pct": round(slag_pct, 2),
        "circularity": round(circularity, 3),
        "solidity": round(solidity, 3),
        "edge_density": round(edge_density * 100, 2),
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
        "cropped_weld_b64": to_base64_jpeg(cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)),
        "edge_b64": to_base64_jpeg(edges),
        "contour_b64": to_base64_jpeg(cv2.cvtColor(vis_contour, cv2.COLOR_RGB2BGR)),
        "slag_b64": to_base64_jpeg(cv2.cvtColor(vis_slag, cv2.COLOR_RGB2BGR)),
        "void_b64": to_base64_jpeg(cv2.cvtColor(vis_void, cv2.COLOR_RGB2BGR))
    }

def extract_deep_feature(img_input, is_already_cropped=False):
    if isinstance(img_input, str):
        bgr = cv2.imread(img_input)
    else:
        bgr = img_input

    weld_roi = bgr if is_already_cropped else crop_weld_roi(bgr)
    rgb = cv2.cvtColor(weld_roi, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    t_img = preprocess(pil_img).unsqueeze(0).to(device)
    with torch.no_grad():
        feat = deep_model(t_img).squeeze().cpu().numpy()
    return feat

def to_base64_jpeg(img):
    _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf).decode("utf-8")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/images/<path:filename>")
def serve_image(filename):
    # Serve cropped weld image if available, otherwise original
    if filename.startswith("good"):
        p = os.path.join(CROPPED_DIR, "good", filename)
    elif filename.startswith("bad"):
        p = os.path.join(CROPPED_DIR, "bad", filename)
    else:
        p = os.path.join(BASE_DIR, "images", filename)
        
    if os.path.exists(p):
        return send_from_directory(os.path.dirname(p), os.path.basename(p))
    return send_from_directory(os.path.join(BASE_DIR, "images"), filename)

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@app.route("/api/dataset")
def get_dataset():
    good_files = sorted(os.listdir(os.path.join(CROPPED_DIR, "good")))
    bad_files = sorted(os.listdir(os.path.join(CROPPED_DIR, "bad")))

    data = [{"filename": f, "label": "good"} for f in good_files] + \
           [{"filename": f, "label": "bad"} for f in bad_files]

    return jsonify({
        "images": data,
        "total": len(data),
        "good": len(good_files),
        "bad": len(bad_files)
    })

@app.route("/api/analyze/<path:filename>")
def analyze_single(filename):
    if filename.startswith("good"):
        p = os.path.join(CROPPED_DIR, "good", filename)
    elif filename.startswith("bad"):
        p = os.path.join(CROPPED_DIR, "bad", filename)
    else:
        p = os.path.join(BASE_DIR, "images", filename)

    if not os.path.exists(p):
        return jsonify({"error": "File not found"}), 404
    _, analysis = extract_cv_features(p, is_already_cropped=True)
    return jsonify(analysis)

@app.route("/api/train", methods=["POST"])
def train_model():
    good_files = sorted(glob.glob(os.path.join(CROPPED_DIR, "good", "*.*")))
    bad_files = sorted(glob.glob(os.path.join(CROPPED_DIR, "bad", "*.*")))
    all_files = good_files + bad_files
    y = np.array([0] * len(good_files) + [1] * len(bad_files))

    X_cv = []
    X_deep = []
    for p in all_files:
        cv_f, _ = extract_cv_features(p, is_already_cropped=True)
        deep_f = extract_deep_feature(p, is_already_cropped=True)
        X_cv.append(cv_f)
        X_deep.append(deep_f)

    X_cv = np.array(X_cv)
    X_deep = np.array(X_deep)

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # 1. OpenCV Random Forest
    rf_cv = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    scores_cv = cross_val_score(rf_cv, X_cv, y, cv=skf)
    acc_cv = float(np.mean(scores_cv) * 100)
    rf_cv.fit(X_cv, y)
    joblib.dump(rf_cv, MODEL_CV_FILE)

    # 2. Deep Transfer Learning
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
        "good_count": len(good_files),
        "bad_count": len(bad_files),
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

    raw_bgr = cv2.imread(save_path)
    # Crop to weld region strictly
    cropped_weld = crop_weld_roi(raw_bgr)
    cropped_filename = f"crop_{filename}"
    cropped_path = os.path.join(UPLOAD_DIR, cropped_filename)
    cv2.imwrite(cropped_path, cropped_weld)

    # Extract features strictly on cropped weld
    cv_feats, analysis = extract_cv_features(cropped_weld, is_already_cropped=True)
    deep_feats = extract_deep_feature(cropped_weld, is_already_cropped=True)

    if os.path.exists(MODEL_DEEP_FILE):
        deep_clf = joblib.load(MODEL_DEEP_FILE)
        prob_bad = float(deep_clf.predict_proba([deep_feats])[0][1])
    else:
        prob_bad = 0.85 if (analysis["metrics"]["void_pct"] > 14.0 or analysis["metrics"]["slag_pct"] > 0.5) else 0.15

    is_bad = prob_bad >= 0.5
    verdict = "REJECT: DEFECTIVE WELD" if is_bad else "PASS: ACCEPTABLE WELD"
    confidence = round(prob_bad * 100 if is_bad else (1 - prob_bad) * 100, 1)

    cert_id = f"QC-WELD-{int(time.time())}-{random.randint(100, 999)}"

    return jsonify({
        "certificate_id": cert_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "filename": file.filename,
        "raw_image_url": f"/uploads/{filename}",
        "weld_crop_url": f"/uploads/{cropped_filename}",
        "verdict": verdict,
        "status": "REJECT" if is_bad else "PASS",
        "is_bad": bool(is_bad),
        "confidence": confidence,
        "metrics": analysis["metrics"],
        "overlays": {
            "cropped_weld": analysis["cropped_weld_b64"],
            "contour": analysis["contour_b64"],
            "void": analysis["void_b64"],
            "slag": analysis["slag_b64"],
            "edge": analysis["edge_b64"]
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Rotor Weld Inspection Studio on http://0.0.0.0:{port} ...")
    app.run(host="0.0.0.0", port=port, debug=False)
