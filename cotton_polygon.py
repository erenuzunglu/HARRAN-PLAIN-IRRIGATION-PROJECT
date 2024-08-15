# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 14:26:35 2024

@author: kapla
"""

import geopandas



harran = geopandas.read_file('harran_2022.shp')

#harran.plot()



cotton = harran[harran['CROP_NAME'].isin(['cotton'])]
cotton.plot()

cotton['area'] = cotton.geometry.area


cotton_areas = cotton[['fid', 'area']]
maxvalue = cotton_areas['area'].max()
minvalue= cotton_areas['area'].min()




for index, row in cotton_areas.iterrows():
    f"ID: {row['fid']}, Alan: {row['area']} metrekare"
    
#cotton_areas.to_csv('cotton_areas.csv', index=False)

sorted_df = cotton_areas.sort_values(by='area')

max_area_field = cotton_areas[cotton_areas['area'] == maxvalue]['fid'].values[0]
min_area_field = cotton_areas[cotton_areas['area'] == minvalue]['fid'].values[0]


print(maxvalue,'metrekare',max_area_field)
print(minvalue,'metrekare',min_area_field)
print(sorted_df)

