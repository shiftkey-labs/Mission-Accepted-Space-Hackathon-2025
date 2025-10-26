import rasterio
import matplotlib.pyplot as plt
import numpy as np
from rasterio.warp import reproject, Resampling
import os

# Read the temperature TIFF
with rasterio.open('slstr_sst.tiff') as src:
    temp_data = src.read(1)
    temp_transform = src.transform
    temp_crs = src.crs
    temp_shape = temp_data.shape
    
    print(f"Temperature data shape: {temp_shape}")
    print(f"Value range: {np.nanmin(temp_data)} - {np.nanmax(temp_data)}")

# Check if water mask exists, if not use simple threshold
if os.path.exists('water_mask.tiff'):
    print("Using water mask from water_mask.tiff")
    
    with rasterio.open('water_mask.tiff') as mask_src:
        # Reproject water mask to match temperature data
        water_mask = np.zeros(temp_shape, dtype=np.uint8)
        
        reproject(
            source=rasterio.band(mask_src, 1),
            destination=water_mask,
            src_transform=mask_src.transform,
            src_crs=mask_src.crs,
            dst_transform=temp_transform,
            dst_crs=temp_crs,
            resampling=Resampling.nearest
        )
        
        water_mask = water_mask > 0
else:
    print("No water mask found, using temperature threshold")
    # Fallback: simple threshold
    water_mask = (
        ~np.isnan(temp_data) &
        (temp_data > 285) &  # > 12°C
        (temp_data < 302)    # < 29°C
    )

# Apply mask to temperature data
masked_temp = np.ma.masked_where(~water_mask, temp_data)

# Convert to Celsius
masked_temp_celsius = masked_temp - 273.15

# Plot only masked temperature
plt.figure(figsize=(12, 10))
im = plt.imshow(masked_temp_celsius, cmap='RdYlBu_r', vmin=10, vmax=20)
plt.colorbar(im, label='Temperature (°C)')
plt.title('Lake Winnipeg Water Temperature - August 2022')
plt.tight_layout()
plt.show()

# Print statistics
valid_temps = masked_temp_celsius[~masked_temp_celsius.mask]
print(f"\nWater temperature statistics:")
print(f"Mean: {np.mean(valid_temps):.2f}°C")
print(f"Min: {np.min(valid_temps):.2f}°C")
print(f"Max: {np.max(valid_temps):.2f}°C")
print(f"Water pixels: {np.sum(water_mask)}")