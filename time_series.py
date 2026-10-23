"""
time_series.py

This file builds the Time Series tab of the California Maternal Health
Disparities Dashboard. It is imported by app.py, and can also be run on
its own while developing with: streamlit run time_series.py

"""

# importing libraries

import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts, JsCode
from time_series_data import load_ca_births

# colors matching the map's color range
PLUM_DARK = '#2E183F'
PLUM_LIGHT = '#94839C'


# caches loaded births data for ease of access
@st.cache_data
def get_ca_births():
    return load_ca_births()


def render_ca_births_chart(births, county):
    """ draws Black births and their share of all births for one county

    Parameters
    ----------
    births : DataFrame
        output of load_ca_births()
    county : str
        county name to plot

    Returns
    -------
    None.
    """

    county_df = births[births['COUNTY_NAME_SHORT'] == county].sort_values('year')

    # suppressed cells become None so ECharts leaves a gap instead of plotting zero
    def to_list(col, digits):
        return [round(v, digits) if pd.notnull(v) else None for v in county_df[col]]

    black_births = to_list('black_births', 0)
    black_share = to_list('black_share', 1)

    # tooltip shows both values for the hovered year, or 'Data Unavailable' when suppressed
    tooltip_formatter = JsCode(
        "function (params) {"
        + "var out = params[0].axisValue;"
        + "params.forEach(function (p) {"
        + "var v = (p.value == null) ? 'Data Unavailable'"
        + " : (p.seriesIndex == 1 ? p.value.toFixed(1) + '%' : Math.round(p.value).toLocaleString());"
        + "out += '<br/>' + p.marker + p.seriesName + ': ' + v;"
        + "});"
        + "return out;"
        + "}"
    ).js_code

    # EChart configuration; bars for counts on the left axis, line for share on the right axis
    options = {
        "tooltip": {"trigger": "axis", "formatter": tooltip_formatter},
        "legend": {"data": ["Black births", "Share of all births"], "top": "top"},
        "toolbox": {
            "show": True, "left": "left", "top": "top",
            "feature": {"dataView": {"readOnly": True}, "saveAsImage": {}},
        },
        "grid": {"left": 60, "right": 60, "top": 80, "bottom": 40},
        "xAxis": {"type": "category", "data": [str(y) for y in county_df['year']]},
        "yAxis": [
            {"type": "value", "name": "Births", "minInterval": 1},
            {"type": "value", "name": "% of births", "axisLabel": {"formatter": "{value}%"},
             "splitLine": {"show": False}},
        ],
        "series": [
            {"name": "Black births", "type": "bar", "data": black_births,
             "itemStyle": {"color": PLUM_LIGHT}},
            {"name": "Share of all births", "type": "line", "yAxisIndex": 1, "data": black_share,
             "connectNulls": False, "symbolSize": 7,
             "lineStyle": {"width": 3, "color": PLUM_DARK}, "itemStyle": {"color": PLUM_DARK}},
        ],
    }

    st_echarts(options=options, height="420px", key=f"ca_births_{county}")

    # notes which years are hidden so a gap isn't mistaken for zero
    suppressed = county_df.loc[county_df['black_births'].isna(), 'year'].tolist()
    if suppressed:
        st.caption(
            f"Data unavailable for {', '.join(str(y) for y in suppressed)}: "
            "CDPH suppresses small counts to protect privacy."
        )


def render_time_series_tab():
    """ renders the contents of the Time Series tab

    This function draws everything inside the Time Series tab. Controls for
    this tab live inside the tab itself rather than the sidebar, because the
    sidebar is shared with the County Map tab.

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """

    births = get_ca_births()

    # creates a subheader for the tab
    st.subheader("Black Births in California Over Time", divider="rainbow")

    # county picker; defaults to Fresno to match the map tab's county cards
    counties = sorted(births['COUNTY_NAME_SHORT'].unique())
    county = st.selectbox("Select a County:", counties, index=counties.index('Fresno'), key="ts_county")

    render_ca_births_chart(births, county)

    st.caption("Data source: CDPH Live Birth Profiles by County (2014-2024), by county of residence.")


# lets this file be run on its own for development; app.py imports the function instead
if __name__ == "__main__":
    st.set_page_config(page_title='Time Series Preview', layout="wide")
    render_time_series_tab()
