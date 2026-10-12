import os
import shutil
import json

BASE_DIR = r"e:\Rotor"
IMG_DIR = os.path.join(BASE_DIR, "images")
LABELS_FILE = os.path.join(BASE_DIR, "dataset_labels.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "dataset")

GOOD_DIR = os.path.join(OUTPUT_DIR, "good")
BAD_DIR = os.path.join(OUTPUT_DIR, "bad")

os.makedirs(GOOD_DIR, exist_ok=True)
os.makedirs(BAD_DIR, exist_ok=True)

with open(LABELS_FILE, "r") as f:
    labels = json.load(f)

# Group files
good_files = []
bad_files = []

for fn, lbl in labels.items():
    src_path = os.path.join(IMG_DIR, fn)
    if os.path.exists(src_path):
        if lbl == "good":
            good_files.append((fn, src_path))
        elif lbl == "bad":
            bad_files.append((fn, src_path))

# Sort so original good.jpeg and bad.jpeg are first, then chronological
def sort_key(item):
    fn = item[0]
    if fn in ["good.jpeg", "bad.jpeg"]:
        return "0_" + fn
    return "1_" + fn

good_files.sort(key=sort_key)
bad_files.sort(key=sort_key)

mapping = {}

# Copy good images
for idx, (orig_name, src_path) in enumerate(good_files, 1):
    ext = os.path.splitext(orig_name)[1].lower()
    new_name = f"good{idx}{ext}"
    dst_path = os.path.join(GOOD_DIR, new_name)
    shutil.copy2(src_path, dst_path)
    mapping[new_name] = {
        "class": "good",
        "original_filename": orig_name,
        "path": dst_path
    }

# Copy bad images
for idx, (orig_name, src_path) in enumerate(bad_files, 1):
    ext = os.path.splitext(orig_name)[1].lower()
    new_name = f"bad{idx}{ext}"
    dst_path = os.path.join(BAD_DIR, new_name)
    shutil.copy2(src_path, dst_path)
    mapping[new_name] = {
        "class": "bad",
        "original_filename": orig_name,
        "path": dst_path
    }

# Save mapping file
mapping_file = os.path.join(OUTPUT_DIR, "dataset_mapping.json")
with open(mapping_file, "w") as f:
    json.dump(mapping, f, indent=2)

print(f"Successfully organized {len(good_files)} good images into: {GOOD_DIR}")
print(f"Successfully organized {len(bad_files)} bad images into: {BAD_DIR}")
print(f"Mapping saved to: {mapping_file}")
