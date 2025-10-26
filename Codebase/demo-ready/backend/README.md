# NASA Ice Backend

Light-weight FastAPI service that exposes two endpoints used by the frontend
under the `/api` prefix:

- `GET /api/ice_extent` – converts GeoTIFF sea-ice rasters into GeoJSON
- `POST /api/route_prediction` – placeholder that returns a straight line between two coordinates

## Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # customise host/port or dataset path as needed
python app.py
```

## Datasets

Place raw GeoTIFF files below `backend/datasets/`.  The filename should contain
the acquisition date in `YYYYMMDD` form (e.g. `N_19781026_extent_v4.0.tif`).
You can configure an alternate root via the `ICE_DATASET_DIR` environment
variable set in `.env`.

## Configuration

The server reads settings from environment variables (loaded via `.env`):

- `BACKEND_HOST` / `BACKEND_PORT` control the uvicorn bind address (defaults to `0.0.0.0:5000`).
- `API_PREFIX` allows changing the routing prefix (defaults to `/api`).
- `ICE_DATASET_DIR` overrides the GeoTIFF dataset directory if you keep files elsewhere.

Copy `.env.example` to `.env` and tweak values before launching the server if you need
non-default settings.

## `/ice_extent`

Converts a single raster into a GeoJSON FeatureCollection using `rasterio` and
`geopandas`.  Query parameters:

- `date` (required) – formatted as `YYYY-MM-DD`
- `radius_km` (optional) – defaults to `500`, controls the radial mask used when
  selecting ice pixels

Example:

```
GET /api/ice_extent?date=1978-10-26&radius_km=400
```

The response includes the GeoJSON features plus metadata about the source file:

```json
{
  "date": "1978-10-26",
  "feature_collection": { "...": "..." },
  "radius_km": 400.0,
  "source": "/absolute/path/to/datasets/1978/10_Oct/N_19781026_extent_v4.0.tif"
}
```

Results are cached in-memory keyed by file path and radius for faster repeated
requests.

## `/route_prediction`

Accepts JSON payload:

```json
{
  "start": [-93.0, 60.0],
  "end": [-90.0, 65.0]
}
```

and returns a stubbed `LineString` FeatureCollection.  Swap the implementation
with the ML-generated routes when they are available.
