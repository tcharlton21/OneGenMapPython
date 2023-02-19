from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Read in food insecurity data
df1 = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/2020FoodInsecure4.csv",
                 dtype={"FIPS": str})

# Read in distance data
df2 = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/OneGenData4.csv",
                 dtype={"FIPS": str})
df_weights = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/Weightings.csv")

df_names = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/us_county_latlng2.csv")

# Read in food distribution center data
gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/distcenters.csv')
gdf_fp = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/freshptdiscenters.csv')

# Read in warehouse data
whd = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/warehouselocs.csv')

# Merge the data
df_names['FIPS'] = df_names['fips_code'].astype(str)
df_dist = df2.merge(df_names, on='FIPS')

# Merge the dataframes based on the FIPS code column
df_merged = df1.merge(df_dist, on='FIPS')

df = df1.merge(df2, on='FIPS')

# print(df_merged.columns)

# create the choropleth map with default weighting
fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df['FIPS'], z=df_weights['50% Each'],
                                     colorscale='YlOrRd', zmin=0, zmax=1,
                                     marker_opacity=0.5, hovertemplate='%{customdata[0]}<br> %{customdata[1]}<br>')) # Update hovertemplate))

# Add custom data to the trace for the county name
#Essentially hides all other stuff and just says the county name + the stats we want to show
# Merge the distance data with the county names


# Add custom data to the trace for the county name and relevant columns from the merged dataframe
fig.data[0].customdata = np.stack((df_merged['FIPS'], df_merged['name'], df_merged['%_x']), axis=-1)
fig.update_traces(
    hovertemplate='<br>'.join([        'County: %{customdata[1]}',        'Food Insecurity %: %{customdata[2]:.2f}'])
)
fig.update_traces(hoverlabel={"namelength": 0})



# Define the slider steps
slider_steps = []
for i, column in enumerate(['Distance ','10% Food Insecurity', '30% Food Insecurity', '50% Each', '70% Distance', '90% Distance', 'Food Insecurity %']):
    slider_step = {'args': [
        {'z': [df_weights[column].values]},  # update the z data
        {'title': f'{column}'}  # update the title
    ],
        'label': column,
        'method': 'update'
    }
    slider_steps.append(slider_step)


# Define the slider
sliders = [{'active': 3,
            'currentvalue': {'prefix': 'Weighting: '},
            'steps': slider_steps
            }]

# Update the figure layout with the slider
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=5.75,
                  mapbox_center={"lat": 34.7490, "lon": -84.3880},
                  margin={"r": 0, "t": 0, "l": 0, "b": 0},
                  updatemenus=[dict(type='buttons', showactive=False)])

# update the layout with the slider
fig.update_layout(sliders=sliders)

#Last - add distribution center and warehouse points on

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



