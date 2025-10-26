import rasterio
import numpy as np
from PIL import Image
from pathlib import Path

def showIce(tif_path: str):
    path = Path(tif_path)

    with rasterio.open(path) as src:
        data = src.read(1)

    ice_mask = (data == 1).astype(np.uint8) * 255

    out_path = path.with_name(f"{path.stem}_ice_only.png")
    img = Image.fromarray(ice_mask, mode="L")
    img.save(out_path)

    return out_path

if __name__ == "__main__":
    showIce("N_19781026_extent_v4.0.tif")
