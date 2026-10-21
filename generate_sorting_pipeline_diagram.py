import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Set font family
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# Figure canvas with generous dimensions
fig, ax = plt.subplots(figsize=(14.2, 7.8), dpi=300)
ax.set_xlim(0, 142)
ax.set_ylim(0, 78)
ax.axis('off')

# Title Banner
title_box = FancyBboxPatch((4, 69), 134, 6.8, boxstyle="round,pad=0.4",
                           facecolor="#1F4E79", edgecolor="#0F2E4A", linewidth=1.5)
ax.add_patch(title_box)
ax.text(71, 72.4, "AUTOMATED 3-TIER INDUSTRIAL SORTING & ISO COMPLIANCE PIPELINE",
        ha='center', va='center', color='white', fontsize=13, fontweight='bold')

def draw_rounded_card(ax, x, y, w, h, bg_color, border_color, title, items, title_color="white", title_bg=None, rad=1.5):
    # Main outer card
    box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.2,rounding_size={rad}",
                         facecolor=bg_color, edgecolor=border_color, linewidth=1.5, zorder=2)
    ax.add_patch(box)
    
    # Title bar
    th = 4.4
    if title_bg:
        tbox = FancyBboxPatch((x, y + h - th), w, th, boxstyle=f"round,pad=0.2,rounding_size={rad}",
                              facecolor=title_bg, edgecolor=border_color, linewidth=1.2, zorder=3)
        ax.add_patch(tbox)
        # Rect to square the lower corners of the title header
        rect = patches.Rectangle((x, y + h - th), w, 2.0, facecolor=title_bg, edgecolor=title_bg, zorder=3)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - (th/2), title, ha='center', va='center', color=title_color,
                fontsize=9.6, fontweight='bold', zorder=4)
    else:
        ax.text(x + w/2, y + h - 2.5, title, ha='center', va='center', color=title_color,
                fontsize=9.6, fontweight='bold', zorder=4)
        
    # Content rendering
    start_y = y + h - th - 2.5 if title_bg else y + h - 4.5
    for i, line in enumerate(items):
        cur_y = start_y - (i * 2.3)
        is_heading = line.startswith("•") or line.startswith("RULE:") or line.startswith("ACTION:")
        weight = 'bold' if is_heading else 'normal'
        col = '#102A43' if is_heading else '#334E68'
        ax.text(x + 1.8, cur_y, line, ha='left', va='center', color=col,
                fontsize=8.3, fontweight=weight, zorder=4)

def draw_arrow(ax, x1, y1, x2, y2, color="#455A64", style='->', lw=2.0, connectionstyle="arc3,rad=0"):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle=style, mutation_scale=15,
                            color=color, linewidth=lw,
                            connectionstyle=connectionstyle, zorder=6)
    ax.add_patch(arrow)

# -------------------------------------------------------------------------
# COLUMN 1: IMAGE PROCESSING & AI PIPELINE (x=4 to 33, w=29)
# -------------------------------------------------------------------------
# Step 1: Weld Acquisition & Saliency Cropping
draw_rounded_card(
    ax, 4, 46.5, 29, 19.5, "#F8F9FA", "#37474F",
    "1. WELD ACQUISITION & CROPPING",
    ["• Mobile / Optical Camera Image",
     "• Saliency Sobel Gradient Filter",
     "• Adaptive Annular ROI Bounding",
     "• +25% Droop Expansion Buffer",
     "  (Preserves molten anomalies",
     "   without edge boundary clipping)"],
    title_bg="#37474F"
)

# Step 2: Dual AI Inference & Arbitration Engine
draw_rounded_card(
    ax, 4, 4, 29, 38.5, "#F0F4F8", "#1565C0",
    "2. AI INFERENCE & ARBITRATION",
    ["• Mathematical Feature Engine:",
     "  15 Visual Descriptors (Table 4.4)",
     "  Solidity, GLCM Entropy, Mean Intensity",
     "• Embedded Decision Tree Logic:",
     "  Real-time if-else decision rules",
     "• Deep Learning Vision Engine:",
     "  MobileNetV3-Small (Raw Pixels)",
     "  Convolutional feature validation",
     "• Consensus Arbitration Logic:",
     "  Solidity Cutoff: 0.842",
     "  Entropy Cutoff: 4.621",
     "  Mean Intensity Cutoff: 118.4",
     "• Automatic Tier Dispatcher"],
    title_bg="#1565C0"
)

# Arrow from Acquisition to AI Engine
draw_arrow(ax, 18.5, 46.5, 18.5, 42.5, color="#37474F", lw=2.2)

# -------------------------------------------------------------------------
# COLUMN 2: INDUSTRIAL 3-TIER SORTING ACTUATION (x=39 to 90, w=51)
# -------------------------------------------------------------------------
# Tier 1: Accept
draw_rounded_card(
    ax, 39, 47.5, 51, 18.5, "#E8F5E9", "#2E7D32",
    "TIER 1: ACCEPT  [GREEN BEACON / CONTINUOUS RUN]",
    ["RULE: Solidity >= 0.84 & Mean Intensity >= 118.4 & Low Entropy",
     "• Defect Severity: ZERO / NEGLIGIBLE (Uniform fusion seam)",
     "• Tower Signal: Digital Pin Out -> Green Beacon Active",
     "• Shop-Floor Routing Action:",
     "  Direct pass to Rotor Dynamic Balancing & Final Motor Assembly"],
    title_bg="#2E7D32"
)

# Tier 2: Rework
draw_rounded_card(
    ax, 39, 25.5, 51, 18.5, "#FFF3E0", "#E65100",
    "TIER 2: REWORK  [AMBER BEACON / DEFLECTION GATE]",
    ["RULE: Solidity <= 0.84 & GLCM Entropy <= 4.62 (Cold Lap / Oxidation)",
     "• Defect Severity: MARGINAL (Repairable surface flaw / incomplete fill)",
     "• Tower Signal: Digital Pin Out -> Amber Beacon Active",
     "• Shop-Floor Routing Action:",
     "  Pneumatic gate diverts rotor to Secondary Manual TIG Touch-up Bay"],
    title_bg="#E65100"
)

# Tier 3: Scrap
draw_rounded_card(
    ax, 39, 3.5, 51, 18.5, "#FFEBEE", "#C62828",
    "TIER 3: SCRAP  [RED BEACON / EMERGENCY SIREN]",
    ["RULE: Solidity <= 0.84 & GLCM Entropy > 4.62 (Molten Droop / Porosity)",
     "• Defect Severity: FATAL (Severe unbalance risk, irreversible metal void)",
     "• Tower Signal: Digital Pin Out -> Red Beacon + Buzzer Pulse",
     "• Shop-Floor Routing Action:",
     "  Eject immediately via drop-chute to Metal Recovery & Recycling Bin"],
    title_bg="#C62828"
)

# Clear non-overlapping arrows from Column 1 AI Engine into 3 Tiers
draw_arrow(ax, 33, 33.0, 39, 56.5, color="#2E7D32", connectionstyle="arc3,rad=-0.12", lw=2.2)
draw_arrow(ax, 33, 23.0, 39, 34.5, color="#E65100", connectionstyle="arc3,rad=-0.05", lw=2.2)
draw_arrow(ax, 33, 13.0, 39, 12.5, color="#C62828", connectionstyle="arc3,rad=0.04", lw=2.2)

# -------------------------------------------------------------------------
# COLUMN 3: AUTOMATED REPORTING & AUDIT TRAIL (x=96 to 138, w=42)
# -------------------------------------------------------------------------
# Real-Time Web Dashboard
draw_rounded_card(
    ax, 96, 37.5, 42, 28.5, "#EDE7F6", "#512DA8",
    "REAL-TIME WEB INSPECTION DASHBOARD",
    ["• Live Visual Feedback:",
     "  HTML5 Canvas with Bounding Box Overlay",
     "  Color-coded: Green (Accept) / Amber / Red",
     "• Real-Time Telemetry Readouts:",
     "  Solidity, GLCM Entropy, Mean Intensity",
     "  Inference Latency: 48.2 ms (Real-time speed)",
     "• Dual-Model Consensus Readout:",
     "  Decision Tree & MobileNetV3 Verification",
     "• Operator Controls:",
     "  One-click Batch PDF Download, Live Refresh"],
    title_bg="#512DA8"
)

# ISO 9001:2015 Audit Certificate
draw_rounded_card(
    ax, 96, 3.5, 42, 30.5, "#E0F2F1", "#00695C",
    "ISO 9001:2015 AUDIT CERTIFICATE ENGINE",
    ["• Automated PDF Report Generation:",
     "  Formatted inspection certificates for shop audit",
     "  Captures Timestamp, Specimen ID, Operator",
     "• Cryptographic Traceability:",
     "  SHA-256 Digital Fingerprint Hash",
     "  Guarantees zero post-inspection record tampering",
     "• Quality Compliance:",
     "  Full conformity with lean manufacturing standards",
     "  Eliminates manual paper logs from factory floor"],
    title_bg="#00695C"
)

# Connectors from 3 Tiers into Reporting Pipeline
draw_arrow(ax, 90, 56.5, 96, 56.5, color="#2E7D32", lw=2.0)
draw_arrow(ax, 90, 34.5, 96, 43.0, color="#E65100", lw=2.0)
draw_arrow(ax, 90, 12.5, 96, 17.0, color="#C62828", lw=2.0)

# Connector from Dashboard to Certificate
draw_arrow(ax, 117, 37.5, 117, 34.0, color="#00695C", lw=2.0)

plt.tight_layout()
output_path = "analysis_output/report_assets/fig_sorting_and_reporting_pipeline.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Successfully generated {output_path}")
