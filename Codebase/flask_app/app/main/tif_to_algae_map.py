"""
Utilities to convert Sentinel Hub TIFFs into algae-detection outputs.

This module provides two entry points:

- `bytes_to_algae_png(tiff_bytes)` — convert TIFF bytes (in-memory) to PNG
  bytes containing a 1x3 plot (NDWI, NDVI over water, algae mask). This is
  useful when you already have the TIFF bytes (e.g. from an HTTP response).

- `process_tiff_file(input_path="output.tif")` — file-based utility that
  reads a local TIFF (default `output.tif`), computes NDWI/NDVI/algae mask,
  saves numeric outputs (`ndvi_water.txt`, `algae_mask.txt`) and writes a
  PNG visualization (`algae_detection.png`). It also displays the plots if
  running in an interactive environment.

Both implementations use the same index calculations and thresholds. The
algae mask follows the user's provided threshold: `ndvi_over_water < -0.35`.
"""

from io import BytesIO
from typing import Optional

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import rasterio
from rasterio.io import MemoryFile
import logging
import os

logger = logging.getLogger(__name__)


def _compute_indices(B02: np.ndarray, B03: np.ndarray, B04: np.ndarray, B08: np.ndarray):
	"""Compute NDWI, NDVI, water mask, NDVI over water, and algae mask.

	Returns a tuple: (ndwi, ndvi_over_water, algae_mask)
	"""
	# Ensure float type
	B02 = B02.astype(float)
	B03 = B03.astype(float)
	B04 = B04.astype(float)
	B08 = B08.astype(float)

	# NDWI
	ndwi = np.where((B03 + B08) == 0, np.nan, (B03 - B08) / (B03 + B08))

	# NDVI
	ndvi = np.where((B08 + B04) == 0, np.nan, (B08 - B04) / (B08 + B04))

	# Mask out non-water
	water_mask = ndwi > 0
	ndvi_over_water = np.where(water_mask, ndvi, np.nan)

	# Algae mask per user code
	algae_mask = np.where((ndvi_over_water < -0.35), 1, np.nan)

	return ndwi, ndvi_over_water, algae_mask


def bytes_to_algae_png(tiff_bytes: bytes, dpi: int = 100) -> bytes:
	"""Convert TIFF bytes (multiband) to PNG bytes containing the algae plots.

	Expects the TIFF to contain bands in the order: B02, B03, B04, B08, ...
	(matching the evalscript used in the controller). Bands are 1-indexed in
	rasterio (we read bands 1..4 for Blue, Green, Red, NIR).
	"""
	if not tiff_bytes:
		raise ValueError("Empty TIFF bytes provided")

	with MemoryFile(tiff_bytes) as mem:
		with mem.open() as src:
			count = src.count
			if count < 4:
				raise ValueError(f"Expected >=4 bands in TIFF, found {count}")

			B02 = src.read(1).astype(float)  # Blue
			B03 = src.read(2).astype(float)  # Green
			B04 = src.read(3).astype(float)  # Red
			B08 = src.read(4).astype(float)  # NIR

	ndwi, ndvi_over_water, algae_mask = _compute_indices(B02, B03, B04, B08)

	# Create figure
	fig, axes = plt.subplots(1, 3, figsize=(12, 5), dpi=dpi)
	ax = axes[0]
	im0 = ax.imshow(ndwi, cmap='Blues')
	ax.set_title("NDWI (Water Detection)")
	plt.colorbar(im0, ax=ax, shrink=0.7, label="NDWI")

	ax = axes[1]
	im1 = ax.imshow(ndvi_over_water, cmap='RdYlGn')
	ax.set_title("NDVI (Over Water)")
	plt.colorbar(im1, ax=ax, shrink=0.7, label="NDVI")

	ax = axes[2]
	im2 = ax.imshow(algae_mask, cmap='Greens')
	ax.set_title("Potential Algae Blooms")
	plt.colorbar(im2, ax=ax, shrink=0.7, label="Detected Algae")

	plt.tight_layout()

	buf = BytesIO()
	fig.savefig(buf, format='png', bbox_inches='tight')
	plt.close(fig)
	buf.seek(0)
	png_bytes = buf.getvalue()
	buf.close()

	return png_bytes


def process_tiff_file(
	input_path: str = "output.tif",
	png_output: str = "algae_detection.png",
	ndvi_output: str = "ndvi_water.txt",
	algae_output: str = "algae_mask.txt",
	show_plot: bool = True,
	dpi: int = 100
):
	"""Read a TIFF file from disk, compute indices, save numeric outputs and PNG.

	This keeps the same input/output names/behaviour as your provided script.
	"""
	if not os.path.exists(input_path):
		raise FileNotFoundError(f"Input TIFF not found: {input_path}")

	with rasterio.open(input_path) as src:
		count = src.count
		if count < 4:
			raise ValueError(f"Expected >=4 bands in TIFF, found {count}")

		B02 = src.read(1).astype(float)
		B03 = src.read(2).astype(float)
		B04 = src.read(3).astype(float)
		B08 = src.read(4).astype(float)

	ndwi, ndvi_over_water, algae_mask = _compute_indices(B02, B03, B04, B08)

	# Save numeric outputs (matching user's original file names and formats)
	np.savetxt(ndvi_output, ndvi_over_water, fmt="%.4f")
	np.savetxt(algae_output, np.nan_to_num(algae_mask, nan=0), fmt="%d")

	# Plot and save PNG
	fig, axes = plt.subplots(1, 3, figsize=(12, 8), dpi=dpi)

	ax = axes[0]
	im0 = ax.imshow(ndwi, cmap='Blues')
	ax.set_title("NDWI (Water Detection)")
	plt.colorbar(im0, ax=ax, shrink=0.7, label="NDWI")

	ax = axes[1]
	im1 = ax.imshow(ndvi_over_water, cmap='RdYlGn')
	ax.set_title("NDVI (Over Water)")
	plt.colorbar(im1, ax=ax, shrink=0.7, label="NDVI")

	ax = axes[2]
	im2 = ax.imshow(algae_mask, cmap='Greens')
	ax.set_title("Potential Algae Blooms")
	plt.colorbar(im2, ax=ax, shrink=0.7, label="Detected Algae")

	plt.tight_layout()
	fig.savefig(png_output, bbox_inches='tight')

	if show_plot:
		plt.show()
	else:
		plt.close(fig)

	logger.info(f"Saved PNG visualization to {png_output}")
	logger.info(f"Saved NDVI over water to {ndvi_output}")
	logger.info(f"Saved algae mask to {algae_output}")

	# Return arrays for further processing if caller wants them
	return ndwi, ndvi_over_water, algae_mask


if __name__ == "__main__":
	import argparse
	logging.basicConfig(level=logging.INFO)

	parser = argparse.ArgumentParser(description="Process a Sentinel Hub TIFF for algae detection")
	parser.add_argument("--input", "-i", default="output.tif", help="Input TIFF file path")
	parser.add_argument("--png", default="algae_detection.png", help="PNG output path")
	parser.add_argument("--ndvi", default="ndvi_water.txt", help="NDVI numeric output path")
	parser.add_argument("--algae", default="algae_mask.txt", help="Algae mask numeric output path")
	parser.add_argument("--no-show", dest="show", action="store_false", help="Do not display plots")
	args = parser.parse_args()

	try:
		process_tiff_file(
			input_path=args.input,
			png_output=args.png,
			ndvi_output=args.ndvi,
			algae_output=args.algae,
			show_plot=args.show
		)
		print("✅ Algae bloom detection complete!")
	except Exception as e:
		print(f"❌ Error: {e}")
