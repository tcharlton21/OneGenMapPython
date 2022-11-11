from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/Food%20Insecure%25.csv",
                 dtype={"FIPS": str})

import plotly.express as px

fig = px.choropleth_mapbox(df, geojson=counties, locations='FIPS', color='Food Insecurity %',
                           color_continuous_scale="YlOrRd",
                           range_color=(0, 30),
                           mapbox_style="carto-positron",
                           zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'# of Food Insecure Persons Overall (1 Year)': 'Total Food Insecure'}
                           )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()
