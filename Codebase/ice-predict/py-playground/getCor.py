import rasterio
import numpy as np
from PIL import Image
from pathlib import Path

path = Path("N_19781026_extent_v4.0.tif")

with rasterio.open(path) as src:
    print("Driver:", src.driver)
    print("CRS:", src.crs)
    print("Width, Height:", src.width, src.height)
    print("Count:", src.count)
    print("Dtype:", src.dtypes[0])
    print("Bounds:", src.bounds)
    print("Transform:", src.transform)
    print("Metadata:", src.meta)

with rasterio.open(path) as src:
    data = src.read(1)
    cmap = src.colormap(1)

used = np.unique(data)
print("Used values:", used)
print("Used colors:")
for v in used:
    print(f"{v}: {cmap[v]}")

# --- Separate four classes and export ---
out_dir = Path(".")
classes = {
    0: "ocean",
    1: "ice",
    253: "nodata",
    254: "land"
}

for v, name in classes.items():
    mask = (data == v).astype(np.uint8) * 255
    img = Image.fromarray(mask, mode="L")
    out_path = out_dir / f"{path.stem}_{name}.png"
    img.save(out_path)
    print(f"Saved: {out_path}")

# --- Count number of ice pixels ---
ice_pixels = np.sum(data == 1)
print(f"Total ice pixels: {ice_pixels}")
