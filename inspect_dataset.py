import os
import re
from datetime import datetime
import cv2
import numpy as np

IMG_DIR = r"e:\Rotor\images"

def parse_time_from_name(filename):
    # Pattern like: WhatsApp Image 2026-09-17 at 23.10.08.jpeg or with (1)
    match = re.search(r"(\d{4}-\d{2}-\d{2}) at (\d{2})\.(\d{2})\.(\d{2})", filename)
    if match:
        date_str, h, m, s = match.groups()
        time_str = f"{date_str} {h}:{m}:{s}"
        try:
            return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except:
            return None
    return None

def main():
    if not os.path.exists(IMG_DIR):
        print(f"Directory {IMG_DIR} does not exist.")
        return

    files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Total images found: {len(files)}")

    timed_files = []
    other_files = []

    for f in files:
        dt = parse_time_from_name(f)
        path = os.path.join(IMG_DIR, f)
        if dt:
            timed_files.append((dt, f, path))
        else:
            other_files.append((f, path))

    # Sort timed files chronologically
    timed_files.sort(key=lambda x: x[0])

    print(f"\nImages with timestamps: {len(timed_files)}")
    print(f"Other images (e.g. good.jpeg, bad.jpeg): {len(other_files)} {[f[0] for f in other_files]}")

    # Cluster by time difference (e.g., gap > 25 seconds indicates switching to a new rotor)
    clusters = []
    current_cluster = []
    threshold_seconds = 25

    for i, (dt, f, path) in enumerate(timed_files):
        if not current_cluster:
            current_cluster.append((dt, f, path))
        else:
            prev_dt = current_cluster[-1][0]
            delta = (dt - prev_dt).total_seconds()
            if delta <= threshold_seconds:
                current_cluster.append((dt, f, path))
            else:
                clusters.append(current_cluster)
                current_cluster = [(dt, f, path)]
    if current_cluster:
        clusters.append(current_cluster)

    print(f"\n--- Estimated Physical Rotors by Timestamp Clustering (Gap > {threshold_seconds}s) ---")
    print(f"Total estimated rotors from sequential shots: {len(clusters)}")
    for idx, c in enumerate(clusters, 1):
        start_t = c[0][0].strftime("%H:%M:%S")
        end_t = c[-1][0].strftime("%H:%M:%S")
        print(f"Rotor {idx:02d}: {len(c)} shots (from {start_t} to {end_t}) -> e.g. {c[0][1]}")

    # Inspect image resolution sample
    sample_img = cv2.imread(timed_files[0][2]) if timed_files else None
    if sample_img is not None:
        h, w, c = sample_img.shape
        print(f"\nSample image resolution: {w}x{h} (channels: {c})")

if __name__ == "__main__":
    main()
