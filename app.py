"""
app.py

This file creates the California Maternal Health Disparities Dashboard
using ECharts.

Run in terminal with: streamlit run app.py

"""

# importing libraries

import streamlit as st
import pandas as pd
import requests
from streamlit_echarts import st_echarts, Map, JsCode
from data_loader import load_snapshot_data, load_crime_data, get_variable_config

# setting up page configurations
st.set_page_config(page_title='California Maternal Health Dashboard', layout="wide")

# caches loaded snapshot and crime  data for ease of access
@st.cache_data
def get_snapshot_data():
    return load_snapshot_data()

@st.cache_data
def get_crime_data():
    return load_crime_data()

# cacheing california geoJSON data

@st.cache_data
def get_ca_geojson(_fips_to_name):

    # public county boundary file
    url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"

    # downloads the file and parses it from raw text into a dictionary structure
    geojson = requests.get(url).json()
    geojson['features'] = [f for f in geojson['features'] if f['id'].startswith('06')] # California's state code is 06; discards every other county
    for feature in geojson['features']:
        fips = feature['id'] # grabs the shape's FIPS code if in California
        feature['properties']['name'] = _fips_to_name.get(fips, fips)
    return geojson

# calling functions; the outputs will be stored in the three specified variables

snapshot_df = get_snapshot_data()
crime_df = get_crime_data()
variables = get_variable_config()

# pairing the FIPS and county name together and placing them into a dictionary

fips_to_name = dict(zip(snapshot_df['FIPS'], snapshot_df['COUNTY_NAME_SHORT']))

# pulling the geojson from these pairs and wrapping then in EChart's Map object
geojson = get_ca_geojson(fips_to_name)
ca_map = Map(map_name="CA_counties", geo_json=geojson)

##################################
# BEGINNING OF DASHBOARD CREATION
##################################

# large heading at the top of the page
st.title('Maternal Health Disparities in California', text_alignment='center')

# subtitle; NOTE FOR LATER: Create an introduction to the dashboard (?)
st.sidebar.image("/Users/lilly/Downloads/jojLogo.png", width="content")

st.sidebar.header("Map Controls", divider="gray")
# stores what label is selected by user to 'selected_var'
selected_var = st.sidebar.selectbox("Select a Variable:", [" "] + list(variables.keys()))

# if there is no variable chosen then an info box is shown prompting the user to select a variable
if selected_var == " ":
    st.info("Select a variable from the sidebar to view it on the map.", icon='⚠️', title="Select A Variable From The Sidebar To View It On The Map")
    st.stop()

# looks up the settings dictionary for which variable was picked using its label as the dictionary key
var = variables[selected_var]

# starts selected_year at None unless it has a time dimension
# if 'has_time_dimension' is true, then it renders a slider
selected_year = None
if var['has_time_dimension']:
    selected_year = st.sidebar.slider("Select year:", 2016, 2024)

# filters columns to those specifically crime data; the only data in the dashboard that has a time dimension
if var['has_time_dimension']:
    year_data = crime_df[
        (crime_df['year'] == selected_year)
    ][['FIPS', var['column'], 'COUNTY_NAME_SHORT']].copy()

#    creating a new 'value' column by its scale factor
    year_data['value'] = year_data[var['column']] * var['scale_factor']

    year_data.head(20)

# creating a new dataframe that merges scaled data from each year onto FIPS and COUNTY_NAME_SHORT
# FOR DATA WITH A TIME DIMENSION
    display_df = snapshot_df[['FIPS', 'COUNTY_NAME_SHORT']].merge(
        year_data[['FIPS', 'value']], on='FIPS', how='left'
    )
else: 
# FOR DATA WITHOUT A TIME DIMENSION
    display_df = snapshot_df.copy()
    display_df['value'] = display_df[var['column']] * var['scale_factor']

# for each row of the dataset builds a dictionary containing the name of the county and the value; if null returns nothing
map_data = [
        {"name": row['COUNTY_NAME_SHORT'], "value": row['value'] if pd.notnull(row['value']) else None}
        for _, row in display_df.iterrows()
]


if var['value_type'] == 'percent':
    value_fmt = "params.value.toFixed(1) + '%'"
elif var['value_type'] == 'count':
    value_fmt = "Math.round(params.value) + '" + var['suffix'] + "'"
else:
    value_fmt = "params.value.toFixed(2)"


tooltip_formatter = JsCode(
    "function (params) {"
    + "if (params.value == null) { return params.name + ': Data Unavailable'; }"
    + f"return params.name + ': ' + {value_fmt};"
    + "}"
).js_code

# creates a subheader that displays what variable is being displayed by county on the map
st.subheader(f"{selected_var} by County", text_alignment="center", divider="grey")

# EChart configuration
options = {
    "tooltip": {"trigger": "item", "formatter": tooltip_formatter},
    "toolbox": {
        "show": True, "left": "left", "top": "top",
        "feature": {"dataView": {"readOnly": False}, "restore": {}, "saveAsImage": {}},
    },
    "visualMap": {
        "min": var['vis_min'], "max": var['vis_max'],
        "left": "left", "top": "bottom",
        "text": ["High", "Low"], "calculable": True,
        "inRange": {"color": var['color_range']},
    },
    "series": [{
        "name": selected_var, "type": "map", "map": "CA_counties",
        "roam": True, "emphasis": {"label": {"show": True}},
        "data": map_data,
    }],
}

st_echarts(options=options, map=ca_map, height="600px")

# creating two columns to display below the map
col1, col2 = st.columns(2)

with col1:
    st.subheader('Fresno County', divider="gray")
    fresno_row = display_df[display_df['COUNTY_NAME_SHORT'] == 'Fresno'].iloc[0]
    valid = display_df[display_df['value'].notnull()].sort_values('value', ascending=False).reset_index(drop=True)
    if pd.notnull(fresno_row['value']):
        st.metric(selected_var, f"{fresno_row['value']:.2f}{var['suffix']}", border=True)
        fresno_rank = valid[valid['COUNTY_NAME_SHORT'] == 'Fresno'].index[0] + 1
        st.metric("Statewide Rank", f"#{fresno_rank} of {len(valid)}", border=True)

with col2:
    st.subheader("Statewide Context", divider="gray")
    valid = display_df[display_df['value'].notnull()]
    if len(valid) > 0:
        st.metric("Statewide Average", f"{valid['value'].mean():.1f}{var['suffix']}", border=True)
        st.metric("Highest", f"{valid['value'].max():.1f}{var['suffix']}", border=True)
        st.metric("Lowest", f"{valid['value'].min():.1f}{var['suffix']}", border=True)

table_df = display_df[['COUNTY_NAME_SHORT', 'value']].copy()
table_df.columns = ['County', selected_var]
table_df = table_df.sort_values(selected_var, ascending=False, na_position='last')    
    
st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        selected_var: st.column_config.NumberColumn(format="%.1f")
    }
)

st.download_button(
    "Download this table as CSV",
    table_df.to_csv(index=False),
    file_name=f"{selected_var.replace(' ', '_').replace('/', '_')}.csv",
    mime="text/csv",
)

#st.caption("Data sources: CDC WONDER Natality (2016-2024), U.S. Census ACS 5-Year Estimates (2024), "
           #"CalEnviroScreen 5.0, CA DOJ crime statistics (2016-2024), Census Population Estimates Program. "
           #"Rates for small counties are regionally smoothed to improve reliability.")