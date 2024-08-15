# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 15:17:56 2024

@author: kapla
"""

import zipfile
import os
import rasterio
from rasterio.windows import Window

# ZIP dosyasının ve çıkartılacak klasörün yollarını belirleyin
zip_file_path = os.path.expanduser("~/Desktop/clipped_images_renamed.zip")
extracted_folder_path = os.path.expanduser("~/Desktop/clipped_images_renamed/")
os.makedirs(extracted_folder_path, exist_ok=True)

# ZIP dosyasını çıkartın
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path)

# Belirlediğiniz koordinatları girin
minx, miny, maxx, maxy = (39.8309, 36.7852, 39.8534, 36.8064)

# Yeni TIFF dosyalarının kaydedileceği yol
output_folder_path = os.path.join(os.path.expanduser("~"), "Desktop/SENTINEL3_2023_FINAL/2023/ceylanpinar_area6_clipped_pixels")
os.makedirs(output_folder_path, exist_ok=True)

# Çıkarılan dosyalar arasında TIFF dosyalarını bulun ve işleyin
for root, dirs, files in os.walk(extracted_folder_path):
    for file in files:
        if file.endswith('.tiff'):
            tiff_path = os.path.join(root, file)
            
            # Her TIFF dosyasını açın ve kesip kaydedin
            with rasterio.open(tiff_path) as src:
                # Koordinatları piksel koordinatlarına dönüştürün
                row_start, col_start = src.index(minx, maxy)
                row_stop, col_stop = src.index(maxx, miny)

                # Pencereyi oluşturun
                window = Window(col_off=col_start, row_off=row_start, width=col_stop - col_start, height=row_stop - row_start)

                # Pencereyi kullanarak veriyi okuyun
                clipped_image = src.read(window=window)

                # Yeni bir transform oluşturun
                new_transform = src.window_transform(window)

                # Yeni TIFF dosyasını oluşturun ve kesilen kısmı yazın
                out_meta = src.meta.copy()
                out_meta.update({
                    "driver": "GTiff",
                    "height": window.height,
                    "width": window.width,
                    "transform": new_transform,
                    "crs": src.crs
                })

                # Orijinal dosya adını kullanarak dosyayı kaydedin
                output_file_path = os.path.join(output_folder_path, file)
                with rasterio.open(output_file_path, 'w', **out_meta) as dest:
                    dest.write(clipped_image)

print(f"Tüm TIFF dosyaları '{output_folder_path}' klasörüne kesildi ve kaydedildi.")