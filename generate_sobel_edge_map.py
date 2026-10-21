import cv2
import numpy as np
import matplotlib.pyplot as plt

# Set Times New Roman font
plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['font.family'] = 'serif'

# Load the weld specimen (bad1_crop or clean crop)
# Let's load bad1_crop which has a molten droop defect, or weld seam crop
img_bgr = cv2.imread('analysis_output/crop_samples/bad1_crop.jpg')
if img_bgr is None:
    img_bgr = cv2.imread('analysis_output/report_assets/fig_weld_seam_crop.jpg')

# Convert to RGB and Grayscale
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur slightly to reduce sensor noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Compute Sobel gradients
gx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
gy = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)

# Absolute gradients normalized to 0-255
abs_gx = cv2.convertScaleAbs(gx)
abs_gy = cv2.convertScaleAbs(gy)

# Gradient magnitude M = sqrt(gx^2 + gy^2)
mag = np.sqrt(gx**2 + gy**2)
mag_norm = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# Otsu optimal binarization
_, otsu_thresh = cv2.threshold(mag_norm, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Morphological closing
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
closed = cv2.morphologyEx(otsu_thresh, cv2.MORPH_CLOSE, kernel)

# Create 2x3 publication figure
fig, axes = plt.subplots(2, 3, figsize=(10.5, 4.2), dpi=300)

# (a) Input Grayscale
axes[0, 0].imshow(gray, cmap='gray')
axes[0, 0].set_title('(a) Input Luminance Channel $I(x, y)$', fontsize=9.5, fontweight='bold', pad=4)
axes[0, 0].axis('off')

# (b) Horizontal Gradient Gx
axes[0, 1].imshow(abs_gx, cmap='bone')
axes[0, 1].set_title('(b) Horizontal Sobel Gradient $|G_x|$', fontsize=9.5, fontweight='bold', pad=4)
axes[0, 1].axis('off')

# (c) Vertical Gradient Gy
axes[0, 2].imshow(abs_gy, cmap='bone')
axes[0, 2].set_title('(c) Vertical Sobel Gradient $|G_y|$', fontsize=9.5, fontweight='bold', pad=4)
axes[0, 2].axis('off')

# (d) Gradient Magnitude M(x, y)
im_mag = axes[1, 0].imshow(mag_norm, cmap='inferno')
axes[1, 0].set_title(r'(d) Gradient Energy Map $M = \sqrt{G_x^2 + G_y^2}$', fontsize=9.5, fontweight='bold', pad=4)
axes[1, 0].axis('off')

# (e) Otsu Saliency Binarization
axes[1, 1].imshow(otsu_thresh, cmap='gray')
axes[1, 1].set_title('(e) Otsu Saliency Binarization', fontsize=9.5, fontweight='bold', pad=4)
axes[1, 1].axis('off')

# (f) Morphological Closing & Contour Seam
# Find contours and draw on RGB
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_img = img_rgb.copy()
cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
axes[1, 2].imshow(contour_img)
axes[1, 2].set_title('(f) Morphological Seam Boundary', fontsize=9.5, fontweight='bold', pad=4)
axes[1, 2].axis('off')

plt.tight_layout(pad=1.0)
out_fig41 = 'analysis_output/report_assets/fig_sobel_edge_map.png'
plt.savefig(out_fig41, dpi=300, bbox_inches='tight')
plt.close()
print("Successfully generated true Sobel edge detection map:", out_fig41)
