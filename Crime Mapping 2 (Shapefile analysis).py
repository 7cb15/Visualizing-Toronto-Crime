#PROJECT: CRIME MAPPING II

#--------------------------------------------------#

#1) IMPORT LIBRARIES

import pandas as pd
import numpy as np
import folium as fol
from shapely.geometry import Point
from shapely.geometry import shape
import geopandas as gpd

#--------------------------------------------------#

#2) Data Processing

df_crime = pd.read_csv('MCI_2014_to_2017.csv',sep=',',header=0) #import crime data

df_crime_sample = df_crime.sample(5000) #use a sample for testing purposes

#First create a GeoSeries of crime locations by converting coordinates to Shapely geometry objects
#Specify the coordinate system ESPG4326 which represents the standard WGS84 coordinate system

crime_geo = gpd.GeoSeries(df_crime_sample.apply(lambda z: Point(z['X'], z['Y']), 1),crs={'init': 'epsg:4326'})

#Create a geodataframe from the pandas dataframe and the geoseries of shapely geometry objects
crime = gpd.GeoDataFrame(df_crime_sample.drop(['X', 'Y'], 1), geometry=crime_geo)
print(crime.head())

tracts = gpd.read_file('POLICE_DIVISION_WGS84.shp').set_index('AREA_NAME') #reads police boundary shapefile into a GeoPandasDF. Polygon format.

print(tracts.tail()) #make sure output is in polygon not point format

#join the police boundary data and the crime stats

#Generate Counts of Major Crimes by Police Division:

#Spatially join crime counts with police boundaries (after projecting) and then group by division/police area
tract_counts = gpd.tools.sjoin(crime.to_crs(tracts.crs), tracts.reset_index()).groupby('AREA_NAME').size()

print(tract_counts.head())

#calculate the sq km of each polygon in tracts:

tracts['MCIpersqmi'] = (tract_counts/ tracts["geometry"].to_crs({'init': 'epsg:3395'}).map(lambda p: p.area / 10**6 / 2)).fillna(0)

tracts = tracts.reset_index()
print(tracts['MCIpersqmi'].head())

#--------------------------------------------------#

#3) Creating the Map 

MAP_COORDINATES = (df_crime_sample['Lat'].mean(), df_crime_sample['Long'].mean()) #centre the map at the average coordinates from the data set

crime_map = fol.Map(location=MAP_COORDINATES, tiles='Mapbox Bright', zoom_start=11)  #Initialize map object


with open('tracts1.json', 'w') as f:
    f.write(tracts.to_json())

tracts_json = open('tracts1.json', 'r')

# Add the color for the chloropleth:
crime_map.choropleth(
 geo_data=tracts,
 name='choropleth',
 data=tracts,
 columns=['AREA_NAME', 'MCIpersqmi'],
 key_on='tracts.AREA_NAME',
 fill_color='YlGn',
 fill_opacity=0.7,
 line_opacity=0.2,
 legend_name='MCIpersqmi'
)


fol.LayerControl().add_to(crime_map) 

map.save(outfile='crime_map_test2.html')

