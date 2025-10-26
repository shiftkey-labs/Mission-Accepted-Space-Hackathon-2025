import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing


def gen_geojson(path: Path, radius_km: float = 500) -> Path:
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
    if len(rows) == 0:
        return None

    xs, ys = rasterio.transform.xy(transform, rows, cols)
    points = [Point(x, y) for x, y in zip(xs, ys)]
    gdf = gpd.GeoDataFrame(geometry=points, crs=crs).to_crs(epsg=4326)
    out_geojson = path.with_suffix(".geojson")
    gdf.to_file(out_geojson, driver="GeoJSON")
    return out_geojson


def process_one(tif_file: Path, all_dir: Path, output_dir: Path, radius_km: float):
    try:
        geojson_path = gen_geojson(tif_file, radius_km)
        if geojson_path is None:
            return tif_file.name, "No data"
        rel_path = tif_file.relative_to(all_dir).with_suffix(".geojson")
        dest_path = output_dir / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(geojson_path, dest_path)
        return tif_file.name, str(dest_path.relative_to(output_dir))
    except Exception as e:
        return tif_file.name, f"❌ {e}"


def batch_gen_geojson(start_year: int, end_year: int, radius_km: float, max_workers: int = None):
    parent = Path(__file__).parent
    all_dir = parent / "all_source"
    output_dir = parent / "all_geo"
    output_dir.mkdir(parents=True, exist_ok=True)

    tif_files = []
    for year in range(start_year, end_year + 1):
        year_dir = all_dir / str(year)
        if year_dir.exists():
            tif_files += list(year_dir.rglob("*.tif"))

    if not tif_files:
        print("⚠️ No .tif files found.")
        return

    cpu_count = multiprocessing.cpu_count() if max_workers is None else max_workers
    print(f"🧩 Using {cpu_count} processes for {len(tif_files)} files")

    count = 0
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        futures = {executor.submit(process_one, f, all_dir, output_dir, radius_km): f for f in tif_files}
        for i, future in enumerate(as_completed(futures), 1):
            name, status = future.result()
            print(f"[{i}/{len(tif_files)}] {name} → {status}")
            if "❌" not in status and status != "No data":
                count += 1

    print(f"\n🎯 Done! Generated {count} GeoJSON files into: {output_dir}")


if __name__ == "__main__":
    batch_gen_geojson(1978, 2025, radius_km=200)
