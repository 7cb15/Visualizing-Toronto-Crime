
#PROJECT: CRIME MAPPING I

#--------------------------------------------------#

#1) IMPORT LIBRARIES

import pandas as pd
import numpy as np
import folium as fol
from folium.plugins import MarkerCluster

#--------------------------------------------------#

#Iteration 1: Using a CSV file

df_crime = pd.read_csv('MCI_2014_to_2017.csv',sep=',',header=0) #import crime data

df_crime_sample = df_crime.sample(1000) #use a sample for testing purposes

MAP_COORDINATES = (df_crime_sample['Lat'].mean(), df_crime_sample['Long'].mean()) #centre the map at the average coordinates from the data set

print(df_crime_sample.head())

marker_colour = [] #create a marker colour column

for MCI in df_crime_sample['MCI']:
        if MCI == 'Assault':
            marker_colour.append('beige')
        elif MCI == 'Break and Enter':
             marker_colour.append('orange')
        elif MCI == 'Robbery':
             marker_colour.append('red')
        elif MCI == 'Auto Theft':
             marker_colour.append('darkred')   
        else:
            marker_colour.append('lightred')
  
print(np.count_nonzero(marker_colour)) #check list length
    
df_crime_sample['marker_colour'] = marker_colour #append to main DF

map = fol.Map(location=MAP_COORDINATES, tiles='cartodbpositron', zoom_start=11)  #Initialize map object

marker_cluster = MarkerCluster() #creates a cluster marker object so markers are aggregating when you zoom out in map

for lat, long, MCI, mark_col in zip(df_crime_sample['Lat'],df_crime_sample['Long'],df_crime_sample['MCI'],df_crime_sample['marker_colour']):
    fol.Marker(location=[lat,long],popup=(fol.Popup(MCI)),icon=fol.Icon(color=mark_col,icon_color='white')).add_to(marker_cluster)

marker_cluster.add_to(map)

fol.LayerControl().add_to(map) #adds a layer filter to the map, though this map has only one layer so this is for example purposes

map.save(outfile='crime_map_test.html')

