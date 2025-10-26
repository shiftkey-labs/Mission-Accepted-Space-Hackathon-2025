import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
import shutil

def genGeojson(path: str, radius_km: float = 500) -> Path:
    path = Path(path)
    with rasterio.open(path) as src:
        data = src.read(1)
        transform = src.transform
        crs = src.crs

    height, width = data.shape
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    xs = transform.c + cols * transform.a + rows * transform.b
    ys = transform.f + cols * transform.d + rows * transform.e
    dist_km = np.sqrt(xs**2 + ys**2) / 1000

    mask = (data == 1) & (dist_km > radius_km)
    rows, cols = np.where(mask)
    xs, ys = rasterio.transform.xy(transform, rows, cols)
    points = [Point(x, y) for x, y in zip(xs, ys)]

    gdf = gpd.GeoDataFrame(geometry=points, crs=crs).to_crs(epsg=4326)
    out_geojson = path.with_suffix(".geojson")
    gdf.to_file(out_geojson, driver="GeoJSON")
    return out_geojson


def batch_gen_geojson(start_year: int, end_year: int, radius_km: float = 500):
    parent = Path(__file__).parent
    downloads_dir = parent
    all_dir = downloads_dir / "all_source"
    output_dir = downloads_dir / "all_geo"
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for year in range(start_year, end_year + 1):
        year_dir = all_dir / str(year)
        if not year_dir.exists():
            continue

        tif_files = list(year_dir.rglob("*.tif"))
        for tif_file in tif_files:
            geojson_path = genGeojson(tif_file, radius_km=radius_km)
            rel_path = tif_file.relative_to(all_dir).with_suffix(".geojson")
            dest_path = output_dir / rel_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(geojson_path, dest_path)
            count += 1
            print(f"{tif_file.name} → {dest_path.relative_to(output_dir)}")

    print(f"\n🎯 Done! Generated {count} GeoJSON files into: {output_dir}")


if __name__ == "__main__":
    batch_gen_geojson(1978, 2025, radius_km=200)
