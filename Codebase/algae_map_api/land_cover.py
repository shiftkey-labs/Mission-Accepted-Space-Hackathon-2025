from matplotlib.colors import ListedColormap
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# --- Load Sentinel-2 bands ---
with rasterio.open("output.tif") as src:
    B02 = src.read(1).astype(float)  # Blue
    B03 = src.read(2).astype(float)  # Green
    B04 = src.read(3).astype(float)  # Red
    B08 = src.read(4).astype(float)  # NIR
    B11 = src.read(5).astype(float)  # SWIR1
    B12 = src.read(6).astype(float)  # SWIR2

# --- Calculate spectral indices ---
# NDVI (vegetation)
ndvi = np.where((B08 + B04) == 0, np.nan, (B08 - B04) / (B08 + B04))

# NDWI (water)
ndwi = np.where((B03 + B08) == 0, np.nan, (B03 - B08) / (B03 + B08))

# NDBI (built-up areas)
ndbi = np.where((B11 + B08) == 0, np.nan, (B11 - B08) / (B11 + B08))

# --- Classify land cover ---
land_cover = np.zeros_like(ndvi, dtype=int)

# 1 = Water
land_cover[ndwi > 0] = 1

# 2 = Urban/Built-up (high NDBI, low NDVI)
land_cover[(ndbi > 0) & (ndvi < 0.3) & (ndwi <= 0)] = 2

# 3 = Bare soil (very low NDVI, not water)
land_cover[(ndvi >= 0) & (ndvi < 0.2) & (ndwi <= 0) & (ndbi <= 0)] = 3

# 4 = Cropland/Agriculture (moderate NDVI)
land_cover[(ndvi >= 0.2) & (ndvi < 0.6) & (ndwi <= 0)] = 4

# 5 = Forest/Dense vegetation (high NDVI)
land_cover[(ndvi >= 0.6) & (ndwi <= 0)] = 5

# --- Create agricultural mask (target for buffer strips) ---
agricultural_land = (land_cover == 4)

# --- Save outputs ---
np.save("land_cover.npy", land_cover)
np.save("agricultural_mask.npy", agricultural_land)

# --- Visualization ---
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Land cover classification with custom colors
colors = ['black', 'blue', 'gray', 'tan', 'yellow', 'darkgreen']
cmap = ListedColormap(colors)

im1 = axes[0].imshow(land_cover, cmap=cmap, vmin=0, vmax=5)
axes[0].set_title("Land Cover Classification", fontsize=14, fontweight='bold')
axes[0].set_xlabel("Pixel X")
axes[0].set_ylabel("Pixel Y")
cbar1 = plt.colorbar(im1, ax=axes[0], ticks=[0, 1, 2, 3, 4, 5], fraction=0.046)
cbar1.ax.set_yticklabels(['No Data', 'Water', 'Urban', 'Bare Soil', 'Cropland', 'Forest'])

# Agricultural land only
im2 = axes[1].imshow(agricultural_land, cmap='YlGn', vmin=0, vmax=1)
axes[1].set_title("Agricultural Land (Target for Buffer Strips)", fontsize=14, fontweight='bold')
axes[1].set_xlabel("Pixel X")
axes[1].set_ylabel("Pixel Y")
plt.colorbar(im2, ax=axes[1], label="Agricultural (1=Yes)", fraction=0.046)

plt.tight_layout()
plt.savefig("land_cover_classification.png", dpi=150, bbox_inches='tight')
plt.show()

# --- Statistics ---
total_pixels = land_cover.size
print("✅ Land cover classification complete!")
print(f"\nLand Cover Distribution:")
print(f"  Water:        {np.sum(land_cover == 1):,} pixels ({100*np.sum(land_cover == 1)/total_pixels:.1f}%)")
print(f"  Urban:        {np.sum(land_cover == 2):,} pixels ({100*np.sum(land_cover == 2)/total_pixels:.1f}%)")
print(f"  Bare Soil:    {np.sum(land_cover == 3):,} pixels ({100*np.sum(land_cover == 3)/total_pixels:.1f}%)")
print(f"  Cropland:     {np.sum(land_cover == 4):,} pixels ({100*np.sum(land_cover == 4)/total_pixels:.1f}%)")
print(f"  Forest:       {np.sum(land_cover == 5):,} pixels ({100*np.sum(land_cover == 5)/total_pixels:.1f}%)")
print(f"\n🎯 Agricultural land available for buffer strips: {np.sum(agricultural_land):,} pixels")