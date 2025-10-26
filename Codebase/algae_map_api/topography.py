import rasterio
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from matplotlib.colors import LinearSegmentedColormap

# --- Load DEM ---
with rasterio.open("elevation.tif") as src:
    elevation = src.read(1).astype(float)
    transform = src.transform
    crs = src.crs

# Handle invalid values
elevation[elevation <= -1000] = np.nan

# Smooth slightly for clean contours
elevation_smooth = ndimage.gaussian_filter(elevation, sigma=1)

# --- Flip vertically so north is up ---
elev_flipped = np.flipud(elevation_smooth)

# --- Define contour levels ---
n_levels = 40
min_elev, max_elev = np.nanmin(elev_flipped), np.nanmax(elev_flipped)
levels = np.linspace(min_elev, max_elev, n_levels)

# --- Create custom monotone colormap ---
# Example: light tan → dark brown (terrain-style)
colors = ["#f3e9d2", "#c0a16b", "#7a5a2a"]  # light → dark
mono_cmap = LinearSegmentedColormap.from_list("mono_terrain", colors)

plt.figure(figsize=(10, 8))

# --- Filled contours with monotone gradient ---
contourf = plt.contourf(
    elev_flipped,
    levels=levels,
    cmap=mono_cmap,
    alpha=1.0
)

# --- Thin contour lines for definition ---
contour_lines = plt.contour(
    elev_flipped,
    levels=levels,
    colors="black",
    linewidths=0.4,
    alpha=0.4
)

plt.title("Monotone Topographic Map")
plt.xlabel("Pixel X")
plt.ylabel("Pixel Y")
plt.gca().set_aspect("equal", adjustable="box")

plt.colorbar(contourf, label="Elevation (m)")
plt.tight_layout()
plt.savefig("topography_monotone.png", dpi=300, bbox_inches="tight")
plt.show()
