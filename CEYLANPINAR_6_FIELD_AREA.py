# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 19:16:10 2024

@author: kapla
"""

import os
import zipfile
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image

# Zip file paths (replace these with the actual paths)
zip_file_paths = [
    "~/Desktop/ceylanpinar_area1_clipped_pixels.zip",
    "~/Desktop/ceylanpinar_area2_clipped_pixels.zip",
    "~/Desktop/ceylanpinar_area3_clipped_pixels.zip",
    "~/Desktop/ceylanpinar_area4_clipped_pixels.zip",
    "~/Desktop/ceylanpinar_area5_clipped_pixels.zip",
    "~/Desktop/ceylanpinar_area6_clipped_pixels.zip"
]

# Initialize a plot
plt.figure(figsize=(14, 8))

# Process each zip file
for zip_file_path in zip_file_paths:
    zip_file_path = os.path.expanduser(zip_file_path)
    extracted_folder_path = zip_file_path.replace('.zip', '')

    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder_path)

    # List the files in the extracted folder
    tiff_files_path = os.path.join(extracted_folder_path, os.path.basename(extracted_folder_path))
    tiff_files = os.listdir(tiff_files_path)

    # Initialize lists for dates and average pixel values
    dates = []
    avg_pixels = []

    # Iterate over each TIFF file in the directory
    for file in tiff_files:
        # Extract the date from the file name
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
        plt.plot(dates, poly_fit, linestyle='--', label=os.path.basename(zip_file_path))

# Finalize the plot
plt.xlabel('Date')
plt.ylabel('Average Pixel Value')
plt.title('Smoothed Pixel Values with 4th Degree Polynomial (All Areas)')
plt.grid(True)
plt.legend()
plt.show()
