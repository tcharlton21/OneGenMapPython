# import plotly.figure_factory as ff
#
# import numpy as np
# import pandas as pd
#
# df_sample = pd.read_csv('https://raw.githubusercontent.com/tcharlton21/OneGenAwayMap/main/countydata.csv')
# df_sample_r = df_sample[df_sample['State'] == 'TN']
# df_sample['FIPS'] = df_sample['FIPS'].apply(lambda x: str(x).zfill(1))
#
# df_sample['# of Food Insecure Persons Overall (1 Year)'] = df_sample[
#     '# of Food Insecure Persons Overall (1 Year)'].str.replace(',', '')
#
# colorscale = [
#     'rgb(193, 193, 193)',
#     'rgb(239,239,239)',
#     'rgb(195, 196, 222)',
#     'rgb(144,148,194)',
#     'rgb(101,104,168)',
#     'rgb(65, 53, 132)'
# ]
# fips = df_sample['FIPS'].tolist()
# values = df_sample['# of Food Insecure Persons Overall (1 Year)'].astype(float).tolist()
# endpts = list(np.mgrid[min(values):max(values):4j])
#
# fig = ff.create_choropleth(
#
#     fips=fips, values=values, scope=['TN'], show_state_data=True,
#     binning_endpoints=[5000, 25000, 50000, 100000, 500000], colorscale=colorscale,
#     county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
#     title='USA by Food Insecurity',
#     legend_title='# of food insecure'
# )
#
# fig.layout.template = None
# fig.show()
