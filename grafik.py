# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:16:11 2024

@author: kapla
"""

import zipfile
import os
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from numpy.polynomial.polynomial import Polynomial

# Path to the uploaded zip file
zip_file_path = os.path.expanduser("~/Desktop/clipped_images_renamed.zip")
extracted_folder_path = os.path.expanduser("~/Desktop/clipped_images_renamed/")

# Extract the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path)

# List the files in the extracted folder
extracted_files = os.listdir(extracted_folder_path)
print(extracted_files)

# Navigating into the directory to see the TIFF files
tiff_files_path = os.path.join(extracted_folder_path, 'clipped_images_renamed')
tiff_files = os.listdir(tiff_files_path)
print(tiff_files)

# Prepare a list to store the average values and corresponding dates
data = []

# Process each TIFF file
for file_name in sorted(tiff_files):
    file_path = os.path.join(tiff_files_path, file_name)
    with rasterio.open(file_path) as src:
        array = src.read(1)
        # Calculate the mean, ignoring nan values
        mean_value = np.nanmean(array)
        
        # Extract the date from the filename (YYYYMMDD)
        date_str = file_name.split('_')[2][:8]
        # Check if it is day or night
        day_or_night = 'day' if 'day' in file_name else 'night'
        
        data.append((date_str, day_or_night, mean_value))

# Convert the list into a DataFrame
df = pd.DataFrame(data, columns=['Date', 'Day/Night', 'Mean Temperature'])

# Convert the Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

# Separate day and night data
day_data = df[(df['Day/Night'] == 'day') & (df['Mean Temperature'] > 290)]
night_data = df[(df['Day/Night'] == 'night') & (df['Mean Temperature'] > 277)]

frames = [day_data,night_data]
result = pd.concat(frames)

def moving_average(series, window_size):
    return series.rolling(window=window_size).mean()

# Apply moving average
window_size = 5  # You can adjust this window size
day_data['Smoothed Temperature'] = moving_average(day_data['Mean Temperature'], window_size)
night_data['Smoothed Temperature'] = moving_average(night_data['Mean Temperature'], window_size)

degree = 4  # You can change the degree to get a better fit
p_day = Polynomial.fit(day_data.index, day_data['Mean Temperature'], degree)
p_night = Polynomial.fit(night_data.index, night_data['Mean Temperature'], degree)

# Generate the polynomial values
day_fit = p_day(day_data.index)
night_fit = p_night(night_data.index)
# Plot the smoothed results
plt.figure(figsize=(14, 7))
plt.plot(day_data['Date'], day_data['Smoothed Temperature'], label='Smoothed Daytime Temperature', color='orange')
plt.plot(day_data['Date'], day_fit, label='Daytime Temperature Fit', color='red', linestyle='--')
plt.plot(night_data['Date'], night_data['Smoothed Temperature'], label='Smoothed Nighttime Temperature', color='blue')

plt.plot(night_data['Date'], night_fit, label='Nighttime Temperature Fit', color='purple', linestyle='--')
plt.title('Land Surface Temperature (LST) from April to September with Polynomial Fit')
plt.xlabel('Date')
plt.ylabel('Mean Temperature (°K)')
plt.legend()
plt.grid(True)
plt.show()



# Find max and min values and dates for day and night data
maxvalues_day = day_data['Mean Temperature'].max()
minvalues_day = day_data['Mean Temperature'].min()

maxvalues_night = night_data['Mean Temperature'].max()
minvalues_night = night_data['Mean Temperature'].min()

max_temp_day = result[result['Mean Temperature'] == maxvalues_day]['Date'].values[0]
min_temp_day = result[result['Mean Temperature'] == minvalues_day]['Date'].values[0]

max_temp_night = result[result['Mean Temperature'] == maxvalues_night]['Date'].values[0]
min_temp_night = result[result['Mean Temperature'] == minvalues_night]['Date'].values[0]

print(max_temp_day, maxvalues_day)
print(min_temp_day, minvalues_day)

print(max_temp_night, maxvalues_night)
print(min_temp_night, minvalues_night)