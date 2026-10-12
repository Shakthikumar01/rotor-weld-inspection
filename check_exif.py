import os
from PIL import Image
from PIL.ExifTags import TAGS

img_dir = r"e:\Rotor\images"
files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg'))][:10]

for f in files:
    p = os.path.join(img_dir, f)
    img = Image.open(p)
    exif_data = img._getexif()
    print(f"\nFile: {f}")
    if exif_data:
        exif = {TAGS.get(k, k): v for k, v in exif_data.items()}
        print("DateTimeOriginal:", exif.get('DateTimeOriginal'))
        print("DateTime:", exif.get('DateTime'))
    else:
        print("No EXIF data found (WhatsApp compression strips EXIF metadata).")
