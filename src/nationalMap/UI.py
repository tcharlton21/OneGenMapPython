import dash
from dash import dcc
from dash import html
from urllib.request import urlopen
import json
import pandas as pd
import plotly.graph_objects as go
import numpy as np

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Create the Dash app
app = dash.Dash(__name__)

dropdown_options = [
    {'label': 'National', 'value': 'NAT'},
    {'label': 'Alabama', 'value': 'AL'},
    {'label': 'Arkansas', 'value': 'AR'},
    {'label': 'Florida', 'value': 'FL'},
    {'label': 'Georgia', 'value': 'GA'},
    {'label': 'Louisiana', 'value': 'LA'},
    {'label': 'North Carolina', 'value': 'NC'},
    {'label': 'South Carolina', 'value': 'SC'},
    {'label': 'Tennessee', 'value': 'TN'}
]

# Define the layout
app.layout = html.Div([
    # Create the dropdown
    dcc.Dropdown(
        id='map-dropdown',
        options=dropdown_options,
        value='NAT',
        clearable=False,
    # Create the map container
    ), dcc.Graph(
        id='map-container',
        style={'height': '650px', 'width': '1400px'}
    )
], style={'width': '80%', 'margin': 'auto', 'padding': '10px', 'margin-right': '300px'})

# Define the callback function
@app.callback(
    dash.dependencies.Output('map-container', 'figure'),
    [dash.dependencies.Input('map-dropdown', 'value')]
)
def update_map(selected_map):
    if selected_map == 'NAT':
        # Get the appropriate data and layout for the selected map
        # Read in food insecurity data
        df1 = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/2020FoodInsecure4.csv",
                          dtype={"FIPS": str})

        # Read in distance data
        df2 = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/OneGenData4.csv",
                          dtype={"FIPS": str})
        df_weights = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/Weightings.csv")

        df_names = pd.read_csv(
            "https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/us_county_latlng2.csv")

        # Merge the data
        df_names['FIPS'] = df_names['fips_code'].astype(str)
        df_dist = df2.merge(df_names, on='FIPS')

        # Merge the dataframes based on the FIPS code column
        df_merged = df1.merge(df_dist, on='FIPS')

        df = df1.merge(df2, on='FIPS')
        fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df['FIPS'], z=df_weights['50% Each'],
                                            colorscale='YlOrRd', zmin=0, zmax=1,
                                            marker_opacity=0.5,
                                            hovertemplate='%{customdata[0]}<br> %{customdata[1]}<br>'))  # Update hovertemplate))

        # Add custom data to the trace for the county name
        # Essentially hides all other stuff and just says the county name + the stats we want to show
        # Merge the distance data with the county names

        # Add custom data to the trace for the county name and relevant columns from the merged dataframe
        fig.data[0].customdata = np.stack((df_merged['FIPS'], df_merged['name'], df_merged['%_x']), axis=-1)
        fig.update_traces(
            hovertemplate='<br>'.join(['County: %{customdata[1]}', 'Food Insecurity %: %{customdata[2]:.2f}'])
        )
        fig.update_traces(hoverlabel={"namelength": 0})

        # Define the slider steps
        slider_steps = []
        for i, column in enumerate(
                ['Distance ', '90% Distance', '70% Distance', '50% Each', '70% Food Insecurity', '90% Food Insecurity',
                 'Food Insecurity %']):
            slider_step = {'args': [
                {'z': [df_weights[column].values]},  # update the z data
                {'title': f'{column}'}  # update the title
            ],
                'label': column,
                'method': 'update'
            }
            slider_steps.append(slider_step)

        sliders = [{
            'active': 3,
            'currentvalue':
                {
                    'prefix': 'Weighting: ',
                    'font': {'size': 16,
                             'color': 'black',
                             }},
            'pad': {'t': 50},
            'len': .9,
            'x': 0.02,
            'y': 0.2,
            'steps': slider_steps}]

        # Update the figure layout with the slider
        fig.update_layout(mapbox_style="carto-positron",
                          mapbox_zoom=5.75,
                          mapbox_center={"lat": 34.7490, "lon": -84.3880},
                          margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          updatemenus=[dict(type='buttons', showactive=False)],
                          showlegend=False)

        # update the layout with the slider
        fig.update_layout(sliders=sliders)

        # Read in food distribution center data
        gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/distcenters.csv')
        gdf_fp = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/freshptdiscenters.csv')
        # Adds dots of distribution centers on top of mapbox
        fig.add_scattermapbox(
            lon=gdf['Longitude'],
            lat=gdf['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf['Center Name'],
            marker_color='rgb(65, 105, 225)'
        )

        fig.add_scattermapbox(
            lon=gdf_fp['Longitude'],
            lat=gdf_fp['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf_fp['Center Name'],
            marker_color='rgb(42, 188, 0)'
        )

        # Read in warehouse data
        whd = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/warehouselocs.csv')

        # Add warehouse points

        fig.add_scattermapbox(
            lon=whd['Longitude'],
            lat=whd['Latitude'],
            mode='markers',
            marker_size=12,
            text="One Generation Away Warehouse",
            marker_color='rgb(171, 0, 252)'
        )
    elif selected_map == 'AL':
        dfBama = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/AL%20Fips.csv",
                             dtype={"FIPS": str})
        import plotly.express as px
        fig = px.choropleth_mapbox(dfBama, geojson=counties, locations='FIPS', color='Food Insecurity %',
                                   color_continuous_scale="YlOrRd",
                                   range_color=(0, 30),
                                   mapbox_style="carto-positron",
                                   zoom=5.75, center={"lat": 32.12, "lon": -86.90},
                                   opacity=0.5,
                                   labels={'# of Food Insecure Persons Overall (1 Year)': 'Total Food Insecure'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        # Read in food distribution center data
        gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/aldistcenters.csv')

        # Adds dots of distribution centers on top of mapbox
        fig.add_scattermapbox(
            lon=gdf['Longitude'],
            lat=gdf['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf['Center Name'],
            marker_color='rgb(65, 105, 225)'
        )
    elif selected_map == 'AR':
        # Read in food insecurity data
        df = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/AR%20Fips.csv",
                         dtype={"FIPS": str})

        import plotly.express as px

        # Map that color coordinates counties across US by food insecurity %
        fig = px.choropleth_mapbox(df, geojson=counties, locations='FIPS', color='Food Insecurity %',
                                   color_continuous_scale="YlOrRd",
                                   range_color=(0, 30),
                                   mapbox_style="carto-positron",
                                   zoom=5.75, center={"lat": 34.56, "lon": -92.29},
                                   opacity=0.5,
                                   labels={'# of Food Insecure Persons Overall (1 Year)': 'Total Food Insecure'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        # Read in food distribution center data
        gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/ardistcenters.csv')

        # Adds dots of distribution centers on top of mapbox
        fig.add_scattermapbox(
            lon=gdf['Longitude'],
            lat=gdf['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf['Center Name'],
            marker_color='rgb(65, 105, 225)'
        )
    elif selected_map == 'FL':
        # Read in food insecurity data
        df = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/FL%20Fips.csv",
                         dtype={"FIPS": str})

        import plotly.express as px

        # Map that color coordinates counties across US by food insecurity %
        fig = px.choropleth_mapbox(df, geojson=counties, locations='FIPS', color='Food Insecurity %',
                                   color_continuous_scale="YlOrRd",
                                   range_color=(0, 30),
                                   mapbox_style="carto-positron",
                                   zoom=5.75, center={"lat": 27.66, "lon": -81.52},
                                   opacity=0.5,
                                   labels={'# of Food Insecure Persons Overall (1 Year)': 'Total Food Insecure'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        # Read in food distribution center data
        gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/fldistcenters.csv')
        gdf_fp = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/flfreshpoint.csv')

        # Adds dots of distribution centers on top of mapbox
        fig.add_scattermapbox(
            lon=gdf['Longitude'],
            lat=gdf['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf['Center Name'],
            marker_color='rgb(65, 105, 225)',
            showlegend=False
        )

        fig.add_scattermapbox(
            lon=gdf_fp['Longitude'],
            lat=gdf_fp['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf_fp['Center Name'],
            marker_color='rgb(42, 188, 0)',
            showlegend=False
        )
    elif selected_map == 'GA':
        # Read in food insecurity data
        df = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/GA%20Fips.csv",
                         dtype={"FIPS": str})

        import plotly.express as px

        # Map that color coordinates counties across US by food insecurity %
        fig = px.choropleth_mapbox(df, geojson=counties, locations='FIPS', color='Food Insecurity %',
                                   color_continuous_scale="YlOrRd",
                                   range_color=(0, 30),
                                   mapbox_style="carto-positron",
                                   zoom=5.75, center={"lat": 32.17, "lon": -82.9},
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
            lat=gdf['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf['Center Name'],
            marker_color='rgb(65, 105, 225)',
            showlegend=False
        )

        fig.add_scattermapbox(
            lon=gdf_fp['Longitude'],
            lat=gdf_fp['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf_fp['Center Name'],
            marker_color='rgb(42, 188, 0)',
            showlegend=False
        )
    elif selected_map == 'LA':
        # Map that color coordinates counties across US by food insecurity %
        import plotly.express as px
        # Read in food insecurity data
        df = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/LA%20Fips.csv",
                         dtype={"FIPS": str})

        fig = px.choropleth_mapbox(df, geojson=counties, locations='FIPS', color='Food Insecurity %',
                                   color_continuous_scale="YlOrRd",
                                   range_color=(0, 30),
                                   mapbox_style="carto-positron",
                                   zoom=5.75, center={"lat": 30.39, "lon": -92.32},
                                   opacity=0.5,
                                   labels={'# of Food Insecure Persons Overall (1 Year)': 'Total Food Insecure'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        # Read in food distribution center data
        gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/ladistcenters.csv')

        # Adds dots of distribution centers on top of mapbox
        fig.add_scattermapbox(
            lon=gdf['Longitude'],
            lat=gdf['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf['Center Name'],
            marker_color='rgb(65, 105, 225)'
        )
    elif selected_map == 'NC':
        # Read in food insecurity data
        df = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/NC%20Fips.csv",
                         dtype={"FIPS": str})

        import plotly.express as px

        # Map that color coordinates counties across US by food insecurity %
        fig = px.choropleth_mapbox(df, geojson=counties, locations='FIPS', color='Food Insecurity %',
                                   color_continuous_scale="YlOrRd",
                                   range_color=(0, 30),
                                   mapbox_style="carto-positron",
                                   zoom=5.75, center={"lat": 35.76, "lon": -79.02},
                                   opacity=0.5,
                                   labels={'# of Food Insecure Persons Overall (1 Year)': 'Total Food Insecure'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        # Read in food distribution center data
        gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/ncdistcenters.csv')
        gdf_fp = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/ncfreshpoint.csv')

        # Adds dots of distribution centers on top of mapbox
        fig.add_scattermapbox(
            lon=gdf['Longitude'],
            lat=gdf['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf['Center Name'],
            marker_color='rgb(65, 105, 225)',
            showlegend=False
        )

        fig.add_scattermapbox(
            lon=gdf_fp['Longitude'],
            lat=gdf_fp['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf_fp['Center Name'],
            marker_color='rgb(42, 188, 0)',
            showlegend=False
        )
    elif selected_map == 'SC':
        # Read in food insecurity data
        df = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/SC%20Fips.csv",
                         dtype={"FIPS": str})

        import plotly.express as px

        # Map that color coordinates counties across US by food insecurity %
        fig = px.choropleth_mapbox(df, geojson=counties, locations='FIPS', color='Food Insecurity %',
                                   color_continuous_scale="YlOrRd",
                                   range_color=(0, 30),
                                   mapbox_style="carto-positron",
                                   zoom=5.75, center={"lat": 33.84, "lon": -81.163},
                                   opacity=0.5,
                                   labels={'# of Food Insecure Persons Overall (1 Year)': 'Total Food Insecure'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        # Read in food distribution center data
        gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/scdistcenters.csv')

        # Adds dots of distribution centers on top of mapbox
        fig.add_scattermapbox(
            lon=gdf['Longitude'],
            lat=gdf['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf['Center Name'],
            marker_color='rgb(65, 105, 225)'
        )
    elif selected_map == 'TN':
        # Read in food insecurity data
        df = pd.read_csv("https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/TN%20Fips.csv",
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
        gdf = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/tndistcenters.csv')
        gdf_fp = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenMapPython/main/tnfreshpoint.csv')

        # Adds dots of distribution centers on top of mapbox
        fig.add_scattermapbox(
            lon=gdf['Longitude'],
            lat=gdf['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf['Center Name'],
            marker_color='rgb(65, 105, 225)',
            showlegend=False
        )

        fig.add_scattermapbox(
            lon=gdf_fp['Longitude'],
            lat=gdf_fp['Latitude'],
            mode='markers',
            marker_size=12,
            text=gdf_fp['Center Name'],
            marker_color='rgb(42, 188, 0)',
            showlegend=False
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

