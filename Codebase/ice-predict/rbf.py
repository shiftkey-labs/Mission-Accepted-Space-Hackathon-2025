# ========================================
# Sea Ice Prediction - SpatioTemporal RBF Regression (train & save)
# Saves weights + metadata for later point-GeoJSON prediction
# ========================================

import os, glob, re
import numpy as np
import rasterio
from datetime import datetime
from tqdm import tqdm
import torch


DATA_ROOT = r"C:\Documents\NASA\ice-predict\data\all_source"
MODEL_DIR = r"C:\Documents\NASA\ice-predict\models"

YEAR_RANGE = (2015, 2025)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
os.makedirs(MODEL_DIR, exist_ok=True)

model_name = f"rbf_model_{YEAR_RANGE[0]}_{YEAR_RANGE[1]}_spatiotemporal.npz"
SAVE_MODEL = os.path.join(MODEL_DIR, model_name)

print(f"Using device: {DEVICE}")
print(f"Will save model to: {SAVE_MODEL}")


DATE_RE = re.compile(r"N_(\d{4})(\d{2})(\d{2})_extent_v4\.0\.tif$")
def parse_date(p):
    m = DATE_RE.search(os.path.basename(p))
    if not m:
        return None
    y, mth, d = map(int, m.groups())
    return datetime(y, mth, d)

def within_year_range(date):
    return YEAR_RANGE[0] <= date.year <= YEAR_RANGE[1]

files_all = sorted(glob.glob(os.path.join(DATA_ROOT, "**", "*.tif"), recursive=True),
                   key=lambda p: (parse_date(p) or datetime.min))
files = [f for f in files_all if parse_date(f) and within_year_range(parse_date(f))]

print(f"Total frames loaded: {len(files)} ({YEAR_RANGE[0]}–{YEAR_RANGE[1]})")
if len(files) == 0:
    raise RuntimeError("No TIFs found for the given YEAR_RANGE.")

with rasterio.open(files[0]) as src:
    H, W = src.height, src.width
    transform, crs = src.transform, src.crs


T = len(files)
ice_seq = np.zeros((T, H, W), np.float32)
land_mask = np.zeros((H, W), np.uint8)
border_mask = np.zeros((H, W), np.uint8)
dates = []

for t, f in enumerate(tqdm(files, desc="Loading .tif")):
    dt = parse_date(f)
    dates.append(dt)
    with rasterio.open(f) as src:
        arr = src.read(1)
    ice_seq[t] = (arr == 1).astype(np.float32)
    land_mask |= (arr == 254)
    border_mask |= (arr == 253)

valid_mask = (land_mask == 0) & (border_mask == 0)
print(f"Valid pixel ratio: {valid_mask.mean():.3f}")


years = np.array([d.year for d in dates], dtype=np.int32)
months = np.array([d.month for d in dates], dtype=np.int32)
# 归一化到 [0,1]
year_norm = (years - YEAR_RANGE[0]) / max(1, (YEAR_RANGE[1] - YEAR_RANGE[0]))
month_sin = np.sin(2 * np.pi * months / 12.0)
month_cos = np.cos(2 * np.pi * months / 12.0)
t_features = np.stack([year_norm, month_sin, month_cos], axis=1)
t = torch.tensor(t_features, dtype=torch.float32, device=DEVICE)   # (T,3)


def rbf_kernel(x1, x2, gamma):
    diff = x1[:, None, :] - x2[None, :, :]    # (T1,T2,3)
    dist2 = torch.sum(diff**2, dim=2)         # (T1,T2)
    return torch.exp(-gamma * dist2)


Y = ice_seq[:, valid_mask]   # (T, N_valid)
N_valid = Y.shape[1]
print(f"Training {N_valid} pixels, {T} timesteps")

alpha = 1e-2
gamma = 1.0 / (2 * (0.3 ** 2))
BATCH = 4000

K = rbf_kernel(t, t, gamma)                         # (T,T)
K_reg = K + alpha * torch.eye(T, device=DEVICE)     # (T,T)
K_inv = torch.linalg.inv(K_reg)                      # (T,T)

weights_all = np.zeros((N_valid, T), np.float32)

for i in tqdm(range(0, N_valid, BATCH), desc="Training SpatioTemporal RBF"):
    batch_Y = torch.from_numpy(Y[:, i:i+BATCH]).to(DEVICE).float()   # (T,B)
    w = K_inv @ batch_Y                                              # (T,B)
    weights_all[i:i+BATCH, :] = w.T.detach().cpu().numpy()


np.savez(
    SAVE_MODEL,
    weights=weights_all,
    alpha=alpha,
    gamma=gamma,
    valid_mask=valid_mask,
    years=years,
    months=months,
    H=np.int32(H),
    W=np.int32(W),
    transform=np.array([transform.a, transform.b, transform.c,
                        transform.d, transform.e, transform.f], dtype=np.float64),
    crs=str(crs)
)

print(f"Model saved to: {SAVE_MODEL}")
