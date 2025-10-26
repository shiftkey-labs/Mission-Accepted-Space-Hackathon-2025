import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# --- Load data ---
# From terrain analysis
elevation = np.load("elevation.npy")
slope = np.load("slope.npy")

# From algae detection - now with severity levels
algae_severity = np.loadtxt("algae_severity.txt")
# Convert 0s to NaN for transparency
algae_severity_display = np.where(algae_severity > 0, algae_severity, np.nan)

# From land cover
land_cover = np.load("land_cover.npy")
agricultural_mask = np.load("agricultural_mask.npy")

# --- Create a focused overlay map ---
fig, ax = plt.subplots(figsize=(12, 10))

# Base layer: Slope
im = ax.imshow(slope, cmap='YlOrRd', vmin=0, vmax=15, alpha=0.7)

# Overlay: Agricultural land (highlight where buffer strips can go)
ag_display = np.where(agricultural_mask, 1, np.nan)
ax.imshow(ag_display, cmap='Oranges', alpha=0.6, vmin=0, vmax=1, interpolation='nearest')

# Overlay: Algae blooms with severity levels (Low=1, Medium=2, High=3)
# Use a custom colormap for severity levels
severity_colors = ['lightgreen', 'green', 'darkgreen']
severity_cmap = ListedColormap(severity_colors)
algae_overlay = ax.imshow(algae_severity_display, cmap=severity_cmap, alpha=0.7, 
                          vmin=1, vmax=3, interpolation='nearest')

# Add contour lines for elevation context
contours = ax.contour(elevation, levels=10, colors='black', alpha=0.3, linewidths=0.5)
ax.clabel(contours, inline=True, fontsize=8, fmt='%d m')

ax.set_title("Buffer Strip Site Selection: Slope, Agricultural Land, & Algae Bloom Severity", 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel("Pixel X", fontsize=12)
ax.set_ylabel("Pixel Y", fontsize=12)

# Create custom legend with severity levels
legend_elements = [
    Patch(facecolor='lightgreen', alpha=0.7, label='Low Algae Severity'),
    Patch(facecolor='green', alpha=0.7, label='Medium Algae Severity'),
    Patch(facecolor='darkgreen', alpha=0.7, label='High Algae Severity'),
    Patch(facecolor='saddlebrown', alpha=0.5, label='Agricultural Land'),
    Patch(facecolor='red', alpha=0.7, label='High Slope Areas'),
    Patch(facecolor='yellow', alpha=0.7, label='Moderate Slope'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

# Colorbars
cbar_slope = plt.colorbar(im, ax=ax, label="Slope (degrees)", 
                          fraction=0.046, pad=0.04)
cbar_slope.set_label("Slope (°)", fontsize=11)

plt.savefig("integrated_algae_slope_landcover_map.png", dpi=200, bbox_inches='tight')
plt.show()

print("✅ Combined visualization complete!")
print(f"\nAlgae Severity Distribution:")
print(f"  Low severity pixels:    {np.sum(algae_severity == 1):,}")
print(f"  Medium severity pixels: {np.sum(algae_severity == 2):,}")
print(f"  High severity pixels:   {np.sum(algae_severity == 3):,}")
print(f"  Total algae pixels:     {np.sum(algae_severity > 0):,}")
print(f"\nAgricultural land pixels: {np.sum(agricultural_mask):,}")
print(f"High slope areas (>8°): {np.sum(slope > 8):,}")
print(f"Prime buffer sites (ag land + suitable slope 3-15%): {np.sum(agricultural_mask & (slope >= 1.7) & (slope <= 8.5)):,}")
print(f"\nHigh severity algae in high slope areas: {np.sum((algae_severity == 3) & (slope > 8)):,}")