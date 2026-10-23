"""
time_series/tab.py

This file builds the Time Series tab of the California Maternal Health
Disparities Dashboard: the chart picker and the controls around each chart.
Each chart lives in its own file in time_series/charts/. The charts are
interactive versions of the matplotlib charts from Mali's CA DHCS and CDC
maternal health notebooks, keeping their titles.

"""

# importing libraries

import streamlit as st
from time_series.data import load_ca_births_by_age, load_medi_cal_rates
from time_series.charts.generational_shift import render_generational_shift_chart
from time_series.charts.comorbidities import render_comorbidities_chart
from time_series.charts.payer import render_payer_chart


# caches loaded births data for ease of access
@st.cache_data
def get_ca_births_by_age():
    return load_ca_births_by_age()


# caches Medi-Cal diagnosis rates for ease of access
@st.cache_data
def get_medi_cal_rates():
    return load_medi_cal_rates()

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

    # creates a subheader for the tab
    st.subheader("Maternal Health Trends Over Time", divider="rainbow")

    # chart picker; each option is one chart from Mali's notebooks. Pills are click-only
    # (no text box) and required=True keeps one chart selected at all times
    chart_options = [
        "The Generational Shift (age of mothers)",
        "Escalation of Chronic Comorbidities (Medi-Cal)",
        "Structural Layering of Maternal Risk (Medi-Cal vs. private)",
    ]
    chart = st.pills("Choose a chart:", chart_options, default=chart_options[0], required=True, key="ts_chart")

    if chart.startswith("The Generational Shift"):
        births = get_ca_births_by_age()

        # the dashboard's stakeholder is based in Fresno, so the tab compares Fresno with the state
        area_label = st.radio("Show:", ["Fresno County", "California"], horizontal=True, key="ts_area")
        area = 'Fresno' if area_label == "Fresno County" else 'California'

        render_generational_shift_chart(births, area, area_label)

        st.caption("Data source: CDPH Live Birth Profiles by County (2014-2024), by county of residence. "
                   "CDPH reports births by age and by race separately, so age brackets include mothers of all races.")
        if area == 'California':
            st.caption("Statewide figures are the sum of all 58 counties. CDPH suppresses small counts in some "
                       "rural counties, so these totals are slightly low.")

    elif chart.startswith("Structural Layering"):
        # the notebook has two versions of this chart; this control sits in the same spot as the
        # Fresno / California option so the page layout stays steady when switching charts
        view = st.radio("Show:", ["Medi-Cal only", "Medi-Cal vs. private insurance"], horizontal=True,
                        key="ts_payer_view", help="This chart's data is available statewide only.")

        render_payer_chart(get_medi_cal_rates(), compare_private=(view != "Medi-Cal only"))

        st.caption("Data source: DHCS Medi-Cal Birth Statistics (2014-2023), California resident hospital births. "
                   "Data is available statewide only.")

    else:
        # same control in the same spot as the Generational Shift chart (keeps the page layout steady),
        # locked to California because this data is statewide only
        st.radio("Show:", ["Fresno County", "California"], index=1, horizontal=True, disabled=True,
                 key="ts_area_statewide", help="This chart's data is available statewide only.")

        render_comorbidities_chart(get_medi_cal_rates())

        st.caption("Data source: DHCS Medi-Cal Birth Statistics (2014-2023), California resident hospital births. "
                   "Diagnosis data is available statewide only.")
