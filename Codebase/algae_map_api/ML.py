import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from scipy.ndimage import distance_transform_edt

# --- Load data ---
elevation = np.load("elevation.npy")
slope = np.load("slope.npy")
land_cover = np.load("land_cover.npy")
agricultural_mask = np.load("agricultural_mask.npy")
algae_severity = np.loadtxt("algae_severity.txt")

# --- Create distance-to-algae map ---
# distance to nearest high-severity bloom (used as a feature)
dist_to_bloom = distance_transform_edt(algae_severity != 3)

# --- Flatten all arrays to feature vectors ---
X = np.column_stack([
    elevation.ravel(),
    slope.ravel(),
    land_cover.ravel(),
    agricultural_mask.ravel(),
    dist_to_bloom.ravel()
])

# --- Labels: algae severity (binary) ---
y = (algae_severity.ravel() == 3).astype(int)

# Filter out NaNs or irrelevant pixels
mask = ~np.isnan(X).any(axis=1)
X, y = X[mask], y[mask]

# --- Train-test split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train model ---
model = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42)
model.fit(X_train, y_train)

# --- Evaluate ---
print(classification_report(y_test, model.predict(X_test)))

# --- Predict across entire raster ---
y_pred = model.predict_proba(X)[:, 1]  # probability of bloom-prone
y_pred_map = np.full_like(algae_severity, np.nan, dtype=float)
y_pred_map.ravel()[mask] = y_pred

# --- Identify top potential vegetation zones ---
# High probability + agricultural + moderate slope (1–8°)
buffer_zones = (y_pred_map > 0.6) & agricultural_mask & (slope >= 1.7) & (slope <= 8.5)

# --- Visualization ---
plt.figure(figsize=(12, 10))
plt.imshow(slope, cmap='YlOrRd', alpha=0.5)
plt.imshow(y_pred_map, cmap='Blues', alpha=0.7)
plt.imshow(buffer_zones, cmap='Greens', alpha=0.6)
plt.title("Predicted Runoff Mitigation Zones")
plt.colorbar(label="Predicted Algae Risk Probability")
plt.savefig("predicted_vegetation_sites.png", dpi=200, bbox_inches='tight')
plt.show()
