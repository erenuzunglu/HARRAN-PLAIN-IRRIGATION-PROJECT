# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 19:11:17 2024

@author: kapla
"""

import os
import zipfile
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image

# Path to the uploaded zip file
zip_file_path = os.path.expanduser("~/Desktop/ceylanpinar_area1_clipped_pixels.zip")
extracted_folder_path = os.path.expanduser("~/Desktop/ceylanpinar_area1_clipped_pixels/")

# Extract the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path)

# List the files in the extracted folder
extracted_files = os.listdir(extracted_folder_path)
print(extracted_files)

# Navigating into the directory to see the TIFF files
tiff_files_path = os.path.join(extracted_folder_path, 'ceylanpinar_area1_clipped_pixels')
tiff_files = os.listdir(tiff_files_path)
print(tiff_files)

# Initialize lists for dates and average pixel values
dates = []
avg_pixels = []

# Iterate over each TIFF file in the directory
for file in tiff_files:
    # Extract the date from the file name (e.g., "clipped_image_20230401.tiff")
    # Assume the date is the last part of the filename before the extension
    date_str = file.split('_')[-1].split('.')[0].strip()
    
    try:
        date = datetime.strptime(date_str, '%Y%m%d')
    except ValueError:
        print(f"Error parsing date from file name: {file}")
        continue
    
    # Open the image and calculate the average pixel value
    image_path = os.path.join(tiff_files_path, file)
    image = Image.open(image_path)
    image_array = np.array(image)
    avg_pixel = np.mean(image_array)
    
    # Only include values where the Kelvin value is 290 or higher
    if avg_pixel >= 290:
        dates.append(date)
        avg_pixels.append(avg_pixel)

# If there are valid dates and pixel values, plot the graph
if dates and avg_pixels:
    dates, avg_pixels = zip(*sorted(zip(dates, avg_pixels)))
    
    # Convert dates to numerical values for polynomial fitting
    date_nums = np.array([date.toordinal() for date in dates])
    avg_pixels = np.array(avg_pixels)
    
    # Fit a 4th-degree polynomial to the data
    poly_coeff = np.polyfit(date_nums, avg_pixels, 4)
    poly = np.poly1d(poly_coeff)
    poly_fit = poly(date_nums)
    
    # Plot the original data and the polynomial fit
    plt.figure(figsize=(10, 6))
    #plt.plot(dates, avg_pixels, marker='o', label='Original Data')
    plt.plot(dates, poly_fit, color='red', linestyle='--', label='4th Degree Polynomial Fit')
    plt.xlabel('Date')
    plt.ylabel('Average Pixel Value')
    plt.title('Smoothed Pixel Values with 4th Degree Polynomial')
    plt.grid(True)
    plt.legend()
    plt.show()
else:
    print("No data above 290K to plot.")


