from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd

# Read in food insecurity data
df = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/GA%20Fips.csv",
                 dtype={"FIPS": str})

import plotly.express as px

# Map that color coordinates counties across US by food insecurity %
fig = px.choropleth_mapbox(df, geojson=counties, locations='FIPS', color='Food Insecurity %',
                           color_continuous_scale="YlOrRd",
                           range_color=(0, 30),
                           mapbox_style="carto-positron",
                           zoom=5.75, center={"lat": 34.7490, "lon": -84.3880},
                           opacity=0.5,
                           labels={'# of Food Insecure Persons Overall (1 Year)': 'Total Food Insecure'}
                           )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Read in food distribution center data
gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/gadistcenters.csv')
gdf_fp = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/gafreshpoint.csv')

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

fig.show()