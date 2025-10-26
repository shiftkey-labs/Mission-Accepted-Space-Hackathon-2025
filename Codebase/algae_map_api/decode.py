import rasterio
import numpy as np
import matplotlib.pyplot as plt

# --- Load the Sentinel Hub TIFF ---
with rasterio.open("output.tif") as src:
    B02 = src.read(1).astype(float)  # Blue
    B03 = src.read(2).astype(float)  # Green
    B04 = src.read(3).astype(float)  # Red
    B08 = src.read(4).astype(float)  # NIR

# --- Compute NDWI (water detection) ---
ndwi = np.where((B03 + B08) == 0, np.nan, (B03 - B08) / (B03 + B08))

# --- Compute NDVI (vegetation/algae) ---
ndvi = np.where((B08 + B04) == 0, np.nan, (B08 - B04) / (B08 + B04))

# --- Mask water pixels ---
water_mask = ndwi > 0
ndvi_over_water = np.where(water_mask, ndvi, np.nan)

# --- Flip NDVI over water to highlight algae ---
ndvi_algae = np.where(water_mask, -ndvi_over_water, np.nan)

# --- Clip super high-end outliers ---
ndvi_water_values = ndvi_algae[~np.isnan(ndvi_algae)]
upper_clip = np.nanpercentile(ndvi_water_values, 99)  # clip top 1%
ndvi_algae_clipped = np.where(ndvi_algae > upper_clip, upper_clip, ndvi_algae)

# --- Adaptive thresholds for Low/Medium/High algae (using clipped values) ---
ndvi_values_clipped = ndvi_algae_clipped[~np.isnan(ndvi_algae_clipped)]
low_thresh = np.nanpercentile(ndvi_values_clipped, 60)
medium_thresh = np.nanpercentile(ndvi_values_clipped, 85)
high_thresh = np.nanpercentile(ndvi_values_clipped, 95)

# --- Classify algae severity ---
algae_severity = np.full_like(ndvi_algae_clipped, np.nan)
algae_severity = np.where((ndvi_algae_clipped >= low_thresh) & (ndvi_algae_clipped < medium_thresh), 1, algae_severity)
algae_severity = np.where((ndvi_algae_clipped >= medium_thresh) & (ndvi_algae_clipped < high_thresh), 2, algae_severity)
algae_severity = np.where(ndvi_algae_clipped >= high_thresh, 3, algae_severity)

# --- Visualization ---
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(ndwi, cmap='Blues')
plt.title("NDWI (Water Detection)")
plt.colorbar(shrink=0.7, label="NDWI")

plt.subplot(1, 3, 2)
plt.imshow(ndvi_algae_clipped, cmap='RdYlGn')
plt.title("Flipped NDVI (Algae Highlight, Clipped)")
plt.colorbar(shrink=0.7, label="NDVI-Algae")

plt.subplot(1, 3, 3)
severity_plot = plt.imshow(algae_severity, cmap='YlOrRd', vmin=0, vmax=3)
plt.title("Algae Bloom Severity")
cbar = plt.colorbar(severity_plot, shrink=0.7, ticks=[1, 2, 3])
cbar.ax.set_yticklabels(['Low', 'Medium', 'High'])
cbar.set_label("Severity")

plt.tight_layout()
plt.show()

# --- Save numeric results ---
np.savetxt("ndvi_algae_clipped.txt", ndvi_algae_clipped, fmt="%.4f")
np.savetxt("algae_severity.txt", np.nan_to_num(algae_severity, nan=0), fmt="%d")
# Add this line to maintain compatibility with combined_map.py:
np.savetxt("algae_mask.txt", np.nan_to_num(algae_severity, nan=0), fmt="%d")

print("✅ Algae bloom detection complete with outlier clipping and Low/Medium/High classification!")