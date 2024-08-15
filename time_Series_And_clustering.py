# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 21:19:35 2024

@author: kapla
"""

import os
import zipfile
import numpy as np
import rasterio
from rasterio.enums import Resampling
from tslearn.clustering import TimeSeriesKMeans
import matplotlib.pyplot as plt
from glob import glob

# ZIP dosyasının yolu
zip_file_path = os.path.expanduser("~/Desktop/clipped_images_renamed.zip")
extracted_folder_path = os.path.expanduser("~/Desktop/clipped_images_renamed/")

# ZIP dosyasını çıkar
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path)

# Çıkarılan klasördeki TIFF dosyalarını listele
tiff_files = sorted(glob(os.path.join(extracted_folder_path, "*.tiff")))

# İlk dosyanın koordinat bilgilerini almak için örnek bir dosya aç
with rasterio.open(tiff_files[0]) as src:
    transform = src.transform
    crs = src.crs
    min_rows, min_cols = src.shape

# Yeniden boyutlandırılmış zaman serisi verilerini saklamak için bir dizi oluştur
resized_time_series_data = np.zeros((len(tiff_files), min_rows, min_cols))

# Her bir görüntüyü minimum boyutlara yeniden boyutlandır ve dizide sakla
for i, tiff_file in enumerate(tiff_files):
    with rasterio.open(tiff_file) as src:
        resized_image = src.read(
            out_shape=(1, min_rows, min_cols),
            resampling=Resampling.bilinear
        )
        resized_time_series_data[i, :, :] = resized_image[0]

# Nan değerlerini kontrol et ve ortalama ile doldur
resized_time_series_data = np.nan_to_num(resized_time_series_data, nan=np.nanmean(resized_time_series_data))

# Kümeleme için veriyi yeniden şekillendir (örnek sayısı, zaman serisi uzunluğu)
n_samples = resized_time_series_data.shape[1] * resized_time_series_data.shape[2]
data_for_clustering = resized_time_series_data.reshape((n_samples, resized_time_series_data.shape[0]))

# Zaman serisi verilerinin ortalama ve standart sapmasını hesapla
mean = np.mean(data_for_clustering, axis=1, keepdims=True)
std = np.std(data_for_clustering, axis=1, keepdims=True)

# Z-score normalizasyonu
normalized_data = (data_for_clustering - mean) / std

# TimeSeriesKMeans ile kümeleme işlemini gerçekleştir
n_clusters = 3  # Kümelerin sayısını ihtiyacına göre ayarlayabilirsin
kmeans = TimeSeriesKMeans(n_clusters=n_clusters, metric="euclidean", max_iter=10, random_state=0)
labels = kmeans.fit_predict(normalized_data)

# Kümelenme etiketlerini orijinal boyutlara geri şekillendir
labels_reshaped = labels.reshape((min_rows, min_cols))

# Küme merkezleri (normalize edilmiş)
cluster_centers = kmeans.cluster_centers_

# Orijinal sıcaklık verilerini geri dönüştürmek için küme merkezlerini yeniden ölçeklendir
cluster_centers_original = cluster_centers * std.mean(axis=0) + mean.mean(axis=0)

# Sıcaklık haritası için küme merkezlerinin ortalamalarını orijinal verilere göre hesapla
average_temperatures = np.mean(cluster_centers_original, axis=1)

# Soğuk olan kümeyi bul
cold_cluster_label = np.argmin(average_temperatures)

# Haritayı görselleştirin ve soğuk bölgeleri vurgulayın
plt.figure(figsize=(10, 8))

# Kümeleri sıcaklık değerlerine göre renklendir
temperature_map = np.zeros_like(labels_reshaped, dtype=float)
for i in range(n_clusters):
    temperature_map[labels_reshaped == i] = average_temperatures[i]

# Sıcaklık haritasını çiz
plt.title("Temperature Map with Cold Regions Highlighted")
temp_image = plt.imshow(temperature_map, cmap='coolwarm', extent=(transform[2], transform[2] + transform[0] * min_cols, transform[5] + transform[4] * min_rows, transform[5]))
plt.colorbar(temp_image, label="Average Temperature")

# Soğuk bölgeleri vurgulayın
cold_areas_mask = labels_reshaped == cold_cluster_label
plt.imshow(cold_areas_mask, cmap='Blues', alpha=0.5, extent=(transform[2], transform[2] + transform[0] * min_cols, transform[5] + transform[4] * min_rows, transform[5]))

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Soğuk bölgeleri temsil eden kümenin zaman serisini görselleştirme
plt.figure(figsize=(10, 4))
plt.plot(cluster_centers_original[cold_cluster_label], label="Cold Area (Tarla) Time Series", color='blue')
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.title("Time Series of Cold (Tarla) Areas")
plt.legend()
plt.show()
