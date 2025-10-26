# ========================================
# FastAPI - Predict Sea Ice GeoJSON (Point-based)
# ========================================

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import numpy as np
import torch
import rasterio
from datetime import datetime
from shapely.geometry import Point
import geopandas as gpd
import json
import os

# ---------------------- Configuration ----------------------
MODEL_PATH = r"C:\Documents\NASA\ice-predict\models\rbf_model_2015_2025_spatiotemporal.npz"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {DEVICE}")
print(f"Loading model: {MODEL_PATH}")

# ---------------------- Preload Model ----------------------
data = np.load(MODEL_PATH, allow_pickle=True)
weights = torch.from_numpy(data["weights"]).to(DEVICE).float()   # (N_valid, T)
valid_mask = data["valid_mask"].astype(bool)                     # (H, W)
years = data["years"]
months = data["months"]
alpha = float(data["alpha"])
gamma = float(data["gamma"])
H, W = int(data["H"]), int(data["W"])

A, B, C, D, E, F = data["transform"].tolist()
transform = rasterio.Affine(A, B, C, D, E, F)
crs = rasterio.crs.CRS.from_string(str(data["crs"]))

year_norm = (years - years.min()) / max(1, (years.max() - years.min()))
month_sin = np.sin(2 * np.pi * months / 12.0)
month_cos = np.cos(2 * np.pi * months / 12.0)
t_features = np.stack([year_norm, month_sin, month_cos], axis=1)
t = torch.tensor(t_features, dtype=torch.float32, device=DEVICE)

# ---------------------- RBF Kernel ----------------------
def rbf_kernel(x1, x2, gamma):
    diff = x1[:, None, :] - x2[None, :, :]
    dist2 = torch.sum(diff ** 2, dim=2)
    return torch.exp(-gamma * dist2)

# ---------------------- Initialize FastAPI ----------------------
app = FastAPI(title="Sea Ice Predictor API", version="1.0")


@app.get("/")
def root():
    return {"message": "Sea Ice Prediction API is running."}


# ---------------------- Prediction Endpoint ----------------------
@app.get("/predict")
def predict_sea_ice(
    year: int = Query(..., ge=1979, le=2100, description="Year to predict"),
    month: int = Query(..., ge=1, le=12, description="Month to predict"),
    thresh: float = Query(0.5, ge=0.0, le=1.0, description="Threshold for ice probability"),
    radius_km: float = Query(200.0, ge=0.0, description="Exclude points within this distance (km) from the pole")
):
    """
    Predict sea ice extent for a given year and month.
    Returns a GeoJSON FeatureCollection of Point geometries (ice pixels).
    """

    FUTURE_DATE = datetime(year, month, 1)

    # Construct time feature for the given date
    year_norm_next = (FUTURE_DATE.year - years.min()) / max(1, (years.max() - years.min()))
    month_sin_next = np.sin(2 * np.pi * FUTURE_DATE.month / 12.0)
    month_cos_next = np.cos(2 * np.pi * FUTURE_DATE.month / 12.0)
    t_next = torch.tensor([[year_norm_next, month_sin_next, month_cos_next]],
                          dtype=torch.float32, device=DEVICE)

    # Predict using RBF kernel
    k_star = rbf_kernel(t, t_next, gamma)
    preds = (weights @ k_star).squeeze(-1).detach().cpu().numpy()
    preds = np.clip(preds, 0, 1)

    # Fill predicted probability map
    pred_prob = np.zeros((H, W), dtype=np.float32)
    pred_prob[valid_mask] = preds
    ice_mask_bin = pred_prob >= thresh
    ice_mask_bin &= valid_mask

    # Compute distance from pole and remove near-pole pixels
    cols, rows = np.meshgrid(np.arange(W), np.arange(H))
    xs = transform.c + cols * transform.a + rows * transform.b
    ys = transform.f + cols * transform.d + rows * transform.e
    dist_km = np.sqrt(xs**2 + ys**2) / 1000.0
    ice_mask_bin &= (dist_km > radius_km)

    # Convert ice pixels to Point geometries
    rr, cc = np.where(ice_mask_bin)
    xs_center, ys_center = rasterio.transform.xy(transform, rr, cc)
    points = [Point(x, y) for x, y in zip(xs_center, ys_center)]

    # Build GeoDataFrame and convert to WGS84
    gdf = gpd.GeoDataFrame(
        {
            "date": FUTURE_DATE.strftime("%Y-%m-%d"),
            "pred_prob": pred_prob[rr, cc].astype(float)
        },
        geometry=points,
        crs=crs
    ).to_crs(epsg=4326)

    # Return GeoJSON as response
    geojson_dict = json.loads(gdf.to_json())
    print(f"Generated {len(points)} ice points for {FUTURE_DATE:%Y-%m}")
    return JSONResponse(content=geojson_dict)
