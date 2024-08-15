# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 15:12:11 2024

@author: kapla
"""

import zipfile
import os
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from numpy.polynomial.polynomial import Polynomial

from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# Path to the uploaded zip file
zip_file_path = os.path.expanduser("~/Desktop/clipped_pixels.zip")
extracted_folder_path = os.path.expanduser("~/Desktop/clipped_pixels/")

# Extract the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path)

# List the files in the extracted folder
extracted_files = os.listdir(extracted_folder_path)
print(extracted_files)

# Navigating into the directory to see the TIFF files
tiff_files_path = os.path.join(extracted_folder_path, 'clipped_pixels')
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

scaler = MinMaxScaler()
day_data['Normalized Temperature'] = scaler.fit_transform(day_data[['Mean Temperature']])


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
p_day = Polynomial.fit(day_data.index, day_data['Normalized Temperature'], degree)
p_day_all = Polynomial.fit(day_data.index, day_data['Mean Temperature'], degree)
p_night = Polynomial.fit(night_data.index, night_data['Mean Temperature'], degree)




# Path to the uploaded zip file
zip_file_path_m = os.path.expanduser("~/Desktop/maxfield_pixel.zip")
extracted_folder_path_m = os.path.expanduser("~/Desktop/maxfield_pixel/")

# Extract the zip file
with zipfile.ZipFile(zip_file_path_m, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path_m)

# List the files in the extracted folder
extracted_files_m = os.listdir(extracted_folder_path_m)
print(extracted_files_m)

# Navigating into the directory to see the TIFF files
tiff_files_path_m = os.path.join(extracted_folder_path_m, 'maxfield_pixel')
tiff_files_m = os.listdir(tiff_files_path_m)
print(tiff_files_m)

# Prepare a list to store the average values and corresponding dates
data_m = []

# Process each TIFF file
for file_name_m in sorted(tiff_files_m):
    file_path_m = os.path.join(tiff_files_path_m, file_name_m)
    with rasterio.open(file_path_m) as src:
        array_m = src.read(1)
        # Calculate the mean, ignoring nan values
        mean_value_m = np.nanmean(array_m)
        
        # Extract the date from the filename (YYYYMMDD)
        date_str_m = file_name_m.split('_')[2][:8]
        # Check if it is day or night
        day_or_night_m = 'day' if 'day' in file_name_m else 'night'
        
        data_m.append((date_str_m, day_or_night_m, mean_value_m))

# Convert the list into a DataFrame
df_m = pd.DataFrame(data_m, columns=['Date', 'Day/Night', 'Mean Temperature'])

# Convert the Date column to datetime format
df_m['Date'] = pd.to_datetime(df_m['Date'], format='%Y%m%d')

# Separate day and night data
day_data_m = df_m[(df_m['Day/Night'] == 'day') & (df_m['Mean Temperature'] > 290)]

scaler = MinMaxScaler()
day_data_m['Normalized Temperature'] = scaler.fit_transform(day_data_m[['Mean Temperature']])


night_data_m = df_m[(df_m['Day/Night'] == 'night') & (df_m['Mean Temperature'] > 277)]

frames_m = [day_data_m,night_data_m]
result = pd.concat(frames_m)

zip_file_path_ms = os.path.expanduser("~/Desktop/second_maxfield_pixel.zip")
extracted_folder_path_ms = os.path.expanduser("~/Desktop/second_maxfield_pixel/")

# Extract the zip file
with zipfile.ZipFile(zip_file_path_ms, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path_ms)

# List the files in the extracted folder
extracted_files_ms = os.listdir(extracted_folder_path_ms)
print(extracted_files_ms)

# Navigating into the directory to see the TIFF files
tiff_files_path_ms = os.path.join(extracted_folder_path_ms, 'second_max_pixels')
tiff_files_ms = os.listdir(tiff_files_path_ms)
print(tiff_files_ms)

# Prepare a list to store the average values and corresponding dates
data_ms = []

# Process each TIFF file
for file_name_ms in sorted(tiff_files_ms):
    file_path_ms = os.path.join(tiff_files_path_ms, file_name_ms)
    with rasterio.open(file_path_ms) as src:
        array_ms = src.read(1)
        # Calculate the mean, ignoring nan values
        mean_value_ms = np.nanmean(array_ms)
        
        # Extract the date from the filename (YYYYMMDD)
        date_str_ms = file_name_ms.split('_')[2][:8]
        # Check if it is day or night
        day_or_night_ms = 'day' if 'day' in file_name_ms else 'night'
        
        data_ms.append((date_str_ms, day_or_night_ms, mean_value_ms))

# Convert the list into a DataFrame
df_ms = pd.DataFrame(data_ms, columns=['Date', 'Day/Night', 'Mean Temperature'])

# Convert the Date column to datetime format
df_ms['Date'] = pd.to_datetime(df_ms['Date'], format='%Y%m%d')

# Separate day and night data
day_data_ms = df_ms[(df_ms['Day/Night'] == 'day') & (df_ms['Mean Temperature'] > 290)]

scaler = MinMaxScaler()
day_data_ms['Normalized Temperature'] = scaler.fit_transform(day_data_ms[['Mean Temperature']])


night_data_ms = df_ms[(df_ms['Day/Night'] == 'night') & (df_ms['Mean Temperature'] > 277)]

frames_ms = [day_data_ms,day_data_m]
result_ms = pd.concat(frames_ms)




def moving_average(series_m, window_size_m):
    return series_m.rolling(window=window_size_m).mean()

# Apply moving average
window_size_m = 5  # You can adjust this window size
day_data_m['Smoothed Temperature'] = moving_average(day_data_m['Mean Temperature'], window_size_m)
night_data_m['Smoothed Temperature'] = moving_average(night_data_m['Mean Temperature'], window_size_m)

degree_m = 4  # You can change the degree to get a better fit
p_day_m = Polynomial.fit(day_data_m.index, day_data_m['Normalized Temperature'], degree_m)
p_day_all_m = Polynomial.fit(day_data_m.index, day_data_m['Mean Temperature'], degree_m)
p_night_m = Polynomial.fit(night_data_m.index, night_data_m['Mean Temperature'], degree_m)

# Generate the polynomial values
day_fit = p_day(day_data['Normalized Temperature'].index)

day_fit_all = p_day_all_m(day_data_m['Mean Temperature'].index)
night_fit = p_night(night_data.index)
# Plot the smoothed results
fig, ax1 = plt.subplots(figsize=(14, 7))

ax1.plot(day_data['Date'], day_fit, label='Daytime Temperature for the Biggest Crop Field', color='red', linestyle='--')

ndvi_data = pd.read_excel('HARRAN_NDVI.xlsx')
ndvi_data['Date'] = pd.to_datetime(ndvi_data['Date'])

# Plot NDVI values
ax1.plot(ndvi_data['Date'], ndvi_data['NDVI'], label='NDVI', color='green')

# Setting labels and title
ax1.set_title('Land Surface Temperature (LST) from April to September with Polynomial Fit')
ax1.set_xlabel('Date')
ax1.set_ylabel('NDVI / Normalized Temperature')

# Create a secondary y-axis to display the Mean Temperature
ax2 = ax1.twinx()
ax2.plot(day_data_m['Date'], day_fit_all, color='orange', alpha=0.6, label='Mean Temperature for All Area')

ax2.set_ylabel('Mean Temperature (°K)', color='orange')

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

ax1.grid(True)
plt.show()

result.to_excel('TEMPERATURE_RESULT.xlsx', index=False)

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