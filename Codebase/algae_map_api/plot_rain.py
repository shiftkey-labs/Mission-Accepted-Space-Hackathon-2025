import zipfile
import xarray as xr
import matplotlib.pyplot as plt

zip_path = "April2024_precip.nc"
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall("April2024_precip")  # extract to a folder

# Path to the real .nc file
nc_path = "April2024_precip/data_stream-mnth.nc"

# Open the dataset
ds = xr.open_dataset(nc_path, engine='netcdf4')
print(ds)

# Select first (and only) timestep along valid_time
precip = ds['tp'].isel(valid_time=0)

# Plot
plt.figure(figsize=(8,6))
(precip*1000).plot(cmap='Blues')  # in mm
plt.title("Total Precipitation April 2024 [mm]")
plt.show()