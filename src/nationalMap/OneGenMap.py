from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd

# Read in food insecurity data
df = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/2020FoodInsecure3.csv",
                 dtype={"FIPS": str})

import plotly.express as px

# Map that color coordinates counties across US by food insecurity %
fig = px.choropleth_mapbox(df, geojson=counties, locations='FIPS', color='Normalized%',
                           color_continuous_scale="YlOrRd",
                           range_color=(0, 1),
                           mapbox_style="carto-positron",
                           zoom=5.75, center={"lat": 34.7490, "lon": -84.3880},
                           opacity=0.5,
                           labels={'# of Food Insecure Persons Overall (1 Year)': 'Total Food Insecure'}
                           )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Read in food distribution center data
gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/distcenters.csv')
gdf_fp = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/freshptdiscenters.csv')

# Adds dots of distribution centers on top of mapbox
fig.add_scattermapbox(
    lon=gdf['Longitude'],
    lat = gdf['Latitude'],
    mode = 'markers',
    marker_size=12,
    text = gdf['Center Name'],
    marker_color = 'rgb(65, 105, 225)'
)

fig.add_scattermapbox(
    lon=gdf_fp['Longitude'],
    lat = gdf_fp['Latitude'],
    mode = 'markers',
    marker_size=12,
    text = gdf_fp['Center Name'],
    marker_color = 'rgb(42, 188, 0)'
)

# Read in warehouse data
whd = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/warehouselocs.csv')

# Add warehouse points

fig.add_scattermapbox(
    lon=whd['Longitude'],
    lat = whd['Latitude'],
    mode = 'markers',
    marker_size=12,
    text = "One Generation Away Warehouse",
    marker_color = 'rgb(171, 0, 252)'
)



fig.show()