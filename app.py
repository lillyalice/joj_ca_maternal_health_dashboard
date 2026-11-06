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
import os
from streamlit_echarts import st_echarts, Map, JsCode
from data_loader import load_snapshot_data, load_crime_data, get_variable_config
from time_series import render_time_series_tab
from community_insights import render_community_insights_tab

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
st.title('Maternal Health Disparities in California')

# subtitle; NOTE FOR LATER: Create an introduction to the dashboard (?)
st.sidebar.image(os.path.join(BASE_DIR, "jojLogo.png"), width="content")

st.sidebar.header("Map Controls", divider="gray")
# stores what label is selected by user to 'selected_var'
selected_var = st.sidebar.selectbox("Select a Variable:", [" "] + list(variables.keys()))

# creating the dashboard tabs; each tab's content lives in its own block below

# Creating the dashboard tabs
map_tab, ts_tab, eda_tab = st.tabs([
    "County Map",
    "Time Series",
    "Community Insights"
])

# TIME SERIES TAB
with ts_tab:
    render_time_series_tab()


# COMMUNITY INSIGHTS TAB
with eda_tab:
    render_community_insights_tab()


# COUNTY MAP TAB
with map_tab:

    # Show a message if the user hasn't selected a variable
    if selected_var == " ":
        st.info(
            "Select A Variable From The Sidebar To View It",
            icon="⚠️"
        )

    else:
        # Get the configuration for the selected variable
        var = variables[selected_var]

        # Determine whether the variable has a time dimension
        selected_year = None

        if var['has_time_dimension']:
            selected_year = st.sidebar.slider(
                "Select year:", 2016, 2024
            )

        # Prepare the data for the selected variable
        if var['has_time_dimension']:

            year_data = crime_df[
                crime_df['year'] == selected_year
            ][['FIPS', var['column'], 'COUNTY_NAME_SHORT']].copy()

            year_data['value'] = (
                year_data[var['column']] * var['scale_factor']
            )

            display_df = snapshot_df[
                ['FIPS', 'COUNTY_NAME_SHORT']
            ].merge(
                year_data[['FIPS', 'value']],
                on='FIPS',
                how='left'
            )

        else:
            display_df = snapshot_df.copy()

            display_df['value'] = (
                display_df[var['column']] * var['scale_factor']
            )

        # Convert county values into ECharts map data
        map_data = [
            {
                "name": row['COUNTY_NAME_SHORT'],
                "value": (
                    row['value']
                    if pd.notnull(row['value'])
                    else None
                )
            }
            for _, row in display_df.iterrows()
        ]

        # Format values for map tooltips
        if var['value_type'] == 'percent':
            value_fmt = "params.value.toFixed(1) + '%'"

        elif var['value_type'] == 'count':
            value_fmt = (
                "Math.round(params.value) + '"
                + var['suffix']
                + "'"
            )

        else:
            value_fmt = "params.value.toFixed(2)"

        tooltip_formatter = JsCode(
            "function (params) {"
            + "if (params.value == null) { "
            + "return params.name + ': Data Unavailable'; "
            + "}"
            + f"return params.name + ': ' + {value_fmt};"
            + "}"
        ).js_code

        # Display the map heading
        st.subheader(
            f"{selected_var} by County",
            divider="rainbow"
        )

        # ECharts configuration
        options = {
            "tooltip": {
                "trigger": "item",
                "formatter": tooltip_formatter
            },
            "toolbox": {
                "show": True,
                "left": "left",
                "top": "top",
                "feature": {
                    "dataView": {"readOnly": False},
                    "restore": {},
                    "saveAsImage": {}
                }
            },
            "visualMap": {
                "min": var['vis_min'],
                "max": var['vis_max'],
                "left": "left",
                "top": "bottom",
                "text": ["High", "Low"],
                "calculable": True,
                "inRange": {
                    "color": var['color_range']
                }
            },
            "series": [{
                "name": selected_var,
                "type": "map",
                "map": "CA_counties",
                "roam": True,
                "emphasis": {
                    "label": {"show": True}
                },
                "data": map_data
            }]
        }

        # Render the California map
        st_echarts(
            options=options,
            map=ca_map,
            height="600px"
        )

        # Display county and statewide statistics
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(
                "Fresno County",
                divider="gray"
            )

            fresno_rows = display_df[
                display_df['COUNTY_NAME_SHORT'] == 'Fresno'
            ]

            valid_ranked = display_df[
                display_df['value'].notnull()
            ].sort_values(
                'value',
                ascending=False
            ).reset_index(drop=True)

            if not fresno_rows.empty:
                fresno_row = fresno_rows.iloc[0]

                if pd.notnull(fresno_row['value']):
                    st.metric(
                        selected_var,
                        f"{fresno_row['value']:.2f}{var['suffix']}",
                        border=True
                    )

                    fresno_rank = (
                        valid_ranked[
                            valid_ranked['COUNTY_NAME_SHORT'] == 'Fresno'
                        ].index[0] + 1
                    )

                    st.metric(
                        "Statewide Rank",
                        f"#{fresno_rank} of {len(valid_ranked)}",
                        border=True
                    )

        with col2:
            st.subheader(
                "Statewide Context",
                divider="gray"
            )

            valid = display_df[
                display_df['value'].notnull()
            ]

            if len(valid) > 0:
                st.metric(
                    "Statewide Average",
                    f"{valid['value'].mean():.1f}{var['suffix']}",
                    border=True
                )

                st.metric(
                    "Highest",
                    f"{valid['value'].max():.1f}{var['suffix']}",
                    border=True
                )

                st.metric(
                    "Lowest",
                    f"{valid['value'].min():.1f}{var['suffix']}",
                    border=True
                )

        # Create the downloadable county table
        table_df = display_df[
            ['COUNTY_NAME_SHORT', 'value']
        ].copy()

        table_df.columns = [
            'County',
            selected_var
        ]

        table_df = table_df.sort_values(
            selected_var,
            ascending=False,
            na_position='last'
        )

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                selected_var: st.column_config.NumberColumn(
                    format="%.1f"
                )
            }
        )

        st.download_button(
            "Download this table as CSV",
            table_df.to_csv(index=False),
            file_name=(
                f"{selected_var.replace(' ', '_').replace('/', '_')}.csv"
            ),
            mime="text/csv"
        )
