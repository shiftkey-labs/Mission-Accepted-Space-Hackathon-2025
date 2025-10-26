import rasterio
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

# --- Load DEM ---
with rasterio.open("elevation.tif") as src:
    elevation = src.read(1).astype(float)
    transform = src.transform
    crs = src.crs

# --- Calculate Slope (in degrees) ---
# Compute gradient in x and y directions
dx = 30  # Copernicus DEM resolution in meters
dy = 30

gradient_x = ndimage.sobel(elevation, axis=1) / (8 * dx)
gradient_y = ndimage.sobel(elevation, axis=0) / (8 * dy)

# Slope = arctan(sqrt(dx^2 + dy^2))
slope = np.degrees(np.arctan(np.sqrt(gradient_x**2 + gradient_y**2)))

# --- Calculate Flow Direction & Accumulation (simplified) ---
# Flow direction using D8 algorithm (8 directions)
def calculate_flow_direction(dem):
    """Simple D8 flow direction"""
    rows, cols = dem.shape
    flow_dir = np.zeros_like(dem, dtype=int)
    
    # Direction encoding: 1=E, 2=SE, 4=S, 8=SW, 16=W, 32=NW, 64=N, 128=NE
    directions = [
        (0, 1, 1),    # East
        (1, 1, 2),    # Southeast
        (1, 0, 4),    # South
        (1, -1, 8),   # Southwest
        (0, -1, 16),  # West
        (-1, -1, 32), # Northwest
        (-1, 0, 64),  # North
        (-1, 1, 128)  # Northeast
    ]
    
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if np.isnan(dem[i, j]):
                continue
            
            max_slope = -np.inf
            flow_direction = 0
            
            for di, dj, code in directions:
                neighbor = dem[i+di, j+dj]
                if not np.isnan(neighbor):
                    slope_to_neighbor = (dem[i, j] - neighbor)
                    if slope_to_neighbor > max_slope:
                        max_slope = slope_to_neighbor
                        flow_direction = code
            
            flow_dir[i, j] = flow_direction
    
    return flow_dir

flow_direction = calculate_flow_direction(elevation)

print("✅ Terrain analysis complete!")
print(f"Elevation range: {np.nanmin(elevation):.1f}m to {np.nanmax(elevation):.1f}m")
print(f"Slope range: {np.nanmin(slope):.1f}° to {np.nanmax(slope):.1f}°")

# Save outputs for next step
np.save("elevation.npy", elevation)
np.save("slope.npy", slope)
np.save("flow_direction.npy", flow_direction)

# --- Visualization ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].imshow(elevation, cmap='terrain')
axes[0].set_title("Elevation (DEM)")
axes[0].set_xlabel("Pixel X")
axes[0].set_ylabel("Pixel Y")
plt.colorbar(axes[0].images[0], ax=axes[0], label="Elevation (m)")

axes[1].imshow(slope, cmap='YlOrRd', vmin=0, vmax=15)
axes[1].set_title("Slope (degrees)")
axes[1].set_xlabel("Pixel X")
axes[1].set_ylabel("Pixel Y")
plt.colorbar(axes[1].images[0], ax=axes[1], label="Slope (°)")

plt.tight_layout()
plt.savefig("terrain_analysis.png", dpi=150)
plt.show()