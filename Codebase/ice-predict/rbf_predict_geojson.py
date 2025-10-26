# ========================================
# Predict future sea-ice points GeoJSON from saved RBF model
# - Output GeoJSON has Point features (pixel centers)
# - File name matches NSIDC style: N_YYYYMM01_extent_v4.0.geojson
# - Optional: drop points within radius_km of the pole (EPSG:3411 meters)
# ========================================

import os, json
import numpy as np
import torch
import rasterio
from datetime import datetime
from shapely.geometry import Point
import geopandas as gpd
from tqdm import tqdm

MODEL_PATH = r"C:\Documents\NASA\ice-predict\models\rbf_model_2015_2025_spatiotemporal.npz"
PRED_DIR = r"C:\Documents\NASA\ice-predict\predictions"

FUTURE_DATE = datetime(2026, 8, 1)

THRESH = 0.5
RADIUS_KM = 200.0

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
os.makedirs(PRED_DIR, exist_ok=True)

pred_name = f"N_{FUTURE_DATE.year}{FUTURE_DATE.month:02d}{FUTURE_DATE.day:02d}_extent_v4.0.geojson"
SAVE_GEOJSON = os.path.join(PRED_DIR, pred_name)

print(f"Using device: {DEVICE}")
print(f"Loading model: {MODEL_PATH}")
print(f"Output: {SAVE_GEOJSON}")

data = np.load(MODEL_PATH, allow_pickle=True)
weights = torch.from_numpy(data["weights"]).to(DEVICE).float()   # (N_valid,T)
valid_mask = data["valid_mask"].astype(bool)                     # (H,W)
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
t = torch.tensor(t_features, dtype=torch.float32, device=DEVICE)     # (T,3)

year_norm_next = (FUTURE_DATE.year - years.min()) / max(1, (years.max() - years.min()))
month_sin_next = np.sin(2 * np.pi * FUTURE_DATE.month / 12.0)
month_cos_next = np.cos(2 * np.pi * FUTURE_DATE.month / 12.0)
t_next = torch.tensor([[year_norm_next, month_sin_next, month_cos_next]],
                      dtype=torch.float32, device=DEVICE)             # (1,3)

# ---------------------- RBF Kernel ----------------------
def rbf_kernel(x1, x2, gamma):
    diff = x1[:, None, :] - x2[None, :, :]
    dist2 = torch.sum(diff ** 2, dim=2)
    return torch.exp(-gamma * dist2)

T = t.shape[0]
k_star = rbf_kernel(t, t_next, gamma)                       # (T,1)
preds = (weights @ k_star).squeeze(-1).detach().cpu().numpy()  # (N_valid,)
preds = np.clip(preds, 0, 1)

pred_prob = np.zeros((H, W), dtype=np.float32)
pred_prob[valid_mask] = preds

ice_mask_bin = pred_prob >= THRESH
ice_mask_bin &= valid_mask

cols, rows = np.meshgrid(np.arange(W), np.arange(H))
xs = transform.c + cols * transform.a + rows * transform.b
ys = transform.f + cols * transform.d + rows * transform.e
dist_km = np.sqrt(xs**2 + ys**2) / 1000.0
ice_mask_bin &= (dist_km > RADIUS_KM)


rr, cc = np.where(ice_mask_bin)
xs_center, ys_center = rasterio.transform.xy(transform, rr, cc)
points = [Point(x, y) for x, y in zip(xs_center, ys_center)]

gdf = gpd.GeoDataFrame(
    {
        "date": FUTURE_DATE.strftime("%Y-%m-%d"),
        "pred_prob": pred_prob[rr, cc].astype(float)
    },
    geometry=points,
    crs=crs
).to_crs(epsg=4326)

gdf.to_file(SAVE_GEOJSON, driver="GeoJSON")
print(f"Saved Point GeoJSON: {SAVE_GEOJSON}")
print(f"Points: {len(gdf)}  |  THRESH={THRESH}  |  RADIUS_KM={RADIUS_KM}")
