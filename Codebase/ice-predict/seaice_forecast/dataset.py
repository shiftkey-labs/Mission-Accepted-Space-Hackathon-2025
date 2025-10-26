# seaice_forecast/dataset.py
import numpy as np, torch, rasterio
from datetime import datetime
from torch.utils.data import Dataset
import re, os
from pathlib import Path

DATE_RE = re.compile(r"N_(\d{4})(\d{2})(\d{2})_extent_v4\.0\.tif$")

def parse_date(p):
    m = DATE_RE.search(os.path.basename(p))
    if not m:
        return None
    y, mth, d = map(int, m.groups())
    return datetime(y, mth, d)

class SeaIceDataset(Dataset):
    def __init__(self, root_dir, seq_len=6, radius_km=200, years_range=(2020,2025)):
        self.root_dir = Path(root_dir)
        self.seq_len = seq_len
        self.radius_km = radius_km
        self.years_range = years_range

        files = sorted(self.root_dir.rglob("*.tif"), key=lambda p: parse_date(p))
        pairs = []
        for f in files:
            dt = parse_date(f)
            if dt and (self.years_range[0] <= dt.year <= self.years_range[1]):
                pairs.append((dt, f))

        self.files = [f for _, f in pairs]
        self.dates = [dt for dt, _ in pairs]
        self.indices = list(range(seq_len, len(self.files)))

        with rasterio.open(self.files[0]) as src:
            h, w = src.height, src.width
            transform = src.transform
        cols, rows = np.meshgrid(np.arange(w), np.arange(h))
        xs = transform.c + cols * transform.a + rows * transform.b
        ys = transform.f + cols * transform.d + rows * transform.e
        self.dist_km = np.sqrt(xs**2 + ys**2) / 1000

    def __len__(self):
        return len(self.indices)

    def _read_mask(self, path: Path):
        with rasterio.open(path) as src:
            arr = src.read(1)
        mask = (arr == 1).astype(np.float32)
        mask[self.dist_km < self.radius_km] = 0
        return mask

    def __getitem__(self, idx):
        t = self.indices[idx]
        seq_files = self.files[t - self.seq_len : t]
        target_file = self.files[t]
        seq = np.stack([self._read_mask(f) for f in seq_files], axis=0)
        target = self._read_mask(target_file)

        months = np.array([parse_date(f).month for f in seq_files], dtype=np.float32)
        month_sin = np.sin(2 * np.pi * months / 12)
        month_cos = np.cos(2 * np.pi * months / 12)
        month_sin = month_sin.reshape(-1, 1, 1) * np.ones_like(seq)
        month_cos = month_cos.reshape(-1, 1, 1) * np.ones_like(seq)

        seq = np.stack([seq, month_sin, month_cos], axis=1)  # (seq, 3, H, W)

        X = torch.tensor(seq).float()  # (seq, 2, H, W)
        y = torch.tensor(target).unsqueeze(0)
        return X, y
