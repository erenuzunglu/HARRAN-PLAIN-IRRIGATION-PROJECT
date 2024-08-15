# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 12:24:48 2024

@author: kapla
"""

import rasterio
from rasterio.plot import show
import os

# Path 
desktop_path = os.path.expanduser("~/Desktop/SENTINEL3_2023_FINAL/2023/july/1/day")
file_name = "S3B_SL_2_LST____20230701T074456_20230701T074756_20230701T095104_0179_081_149_2340_PS2_O_NR_004re.tif"  # Replace with your actual file name
file_path = os.path.join(desktop_path, file_name)

# Exıstıng of File and Document
if os.path.exists(file_path):
    print(f"File found: {file_path}")
else:
    print(f"File not found: {file_path}")

# TIF file
try:
    with rasterio.open(file_path) as src:
        # Read the image data
        image_data = src.read()
        # Display the image
        show(src)
except rasterio.errors.RasterioIOError:
    print(f"File not found or unable to open: {file_path}")

