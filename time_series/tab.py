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
from time_series.charts.medi_cal_hypertension import render_medi_cal_hypertension_chart


# caches loaded births data for ease of access
@st.cache_data
def get_ca_births_by_age():
    return load_ca_births_by_age()


# caches Medi-Cal diagnosis rates for ease of access
@st.cache_data
def get_medi_cal_rates():
    return load_medi_cal_rates()

# places a user can compare, in the order shown in the Where row
PLACES = ["Fresno County", "California", "United States"]

# each topic lists, for every place that has data, the views (charts) available there.
# A place left out of a topic is shown greyed out in the Where row.
TOPICS = {
    "Maternal age": {
        "Fresno County": ["Age mix"],
        "California": ["Age mix"],
    },
    "Hypertension and diabetes": {
        "California": ["Diagnosis rates", "Medi-Cal only", "Medi-Cal vs. private insurance"],
    },
}

# why a place is greyed out, shown when hovering over it
UNAVAILABLE_REASON = {
    "Fresno County": "No Fresno County data for this topic; the source data is statewide only.",
    "California": "No California data for this topic.",
    "United States": "National (CDC) charts for this topic are coming next.",
}


def render_chart(topic, place, view):
    """ draws the chart for one topic, place and view, with its data notes

    Parameters
    ----------
    topic : str
        a key of TOPICS
    place : str
        one of PLACES that has data for the topic
    view : str
        one of the views listed for that topic and place

    Returns
    -------
    None.
    """

    if topic == "Maternal age":
        area = 'Fresno' if place == "Fresno County" else 'California'
        render_generational_shift_chart(get_ca_births_by_age(), area, place)

        st.caption("Data source: CDPH Live Birth Profiles by County (2014-2024), by county of residence. "
                   "CDPH reports births by age and by race separately, so age brackets include mothers of all races.")
        if area == 'California':
            st.caption("Statewide figures are the sum of all 58 counties. CDPH suppresses small counts in some "
                       "rural counties, so these totals are slightly low.")

    elif topic == "Hypertension and diabetes":
        rates = get_medi_cal_rates()
        if view == "Diagnosis rates":
            render_comorbidities_chart(rates)
        else:
            render_medi_cal_hypertension_chart(rates, compare_private=(view == "Medi-Cal vs. private insurance"))

        st.caption("Data source: DHCS Medi-Cal Birth Statistics (2014-2023), California resident hospital births. "
                   "Data is available statewide only.")


def render_time_series_tab():
    """ renders the contents of the Time Series tab

    The tab is organized by topic. A Where row (Fresno County, California,
    United States) appears for every topic, with places that have no data
    greyed out, and a View row appears when a topic and place have more than
    one chart. Controls live inside the tab rather than the sidebar, because
    the sidebar is shared with the County Map tab.

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """

    # creates a subheader for the tab
    st.subheader("Maternal Health Trends Over Time", divider="rainbow")

    # topic picker; pills are click-only. Clicking the selected pill again would leave nothing
    # selected, so the last topic is saved and handed back to the widget on every run. This keeps
    # one topic selected on older Streamlit versions that don't have pills(required=True).
    def remember_topic():
        if st.session_state["ts_topic"] is not None:
            st.session_state["ts_topic_pref"] = st.session_state["ts_topic"]

    st.session_state["ts_topic"] = st.session_state.get("ts_topic_pref", list(TOPICS)[0])
    topic = st.pills("Choose a topic:", list(TOPICS), key="ts_topic", on_change=remember_topic)
    places_with_data = TOPICS[topic]

    # remembers the place the user last clicked (Fresno County to start); when this topic has no
    # data there, shows the first place it does cover without forgetting the user's choice
    preferred = st.session_state.setdefault("ts_where", PLACES[0])
    place = preferred if preferred in places_with_data else next(p for p in PLACES if p in places_with_data)

    # Where row: one button per place, greyed out (with a reason on hover) when there's no data
    st.markdown("<p style='font-size:14px;margin-bottom:0'>Where:</p>", unsafe_allow_html=True)
    with st.container(horizontal=True):
        for p in PLACES:
            available = p in places_with_data
            if st.button(p, key=f"ts_where_{p}", type="primary" if p == place else "secondary",
                         disabled=not available, help=None if available else UNAVAILABLE_REASON[p]):
                st.session_state["ts_where"] = p
                st.rerun()

    # View row: only filled when there's more than one chart here; the empty slot keeps the chart
    # at the same spot on the page so switching doesn't jump back to the top
    views = places_with_data[place]
    view_slot = st.empty()
    view = views[0]
    if len(views) > 1:
        # the chosen view is saved per topic and place when it changes, and handed back to the
        # widget on every run, so the highlighted pill still matches the chart after switching
        # topics (Streamlit forgets a widget's value while it's off the page). Clicking the
        # selected pill again is ignored, so one view always stays selected.
        widget_key = f"ts_view_{topic}_{place}"
        pref_key = f"{widget_key}_pref"

        def remember_view():
            if st.session_state[widget_key] is not None:
                st.session_state[pref_key] = st.session_state[widget_key]

        st.session_state[widget_key] = st.session_state.get(pref_key, views[0])
        view = view_slot.pills("View:", views, key=widget_key, on_change=remember_view)

    render_chart(topic, place, view)


