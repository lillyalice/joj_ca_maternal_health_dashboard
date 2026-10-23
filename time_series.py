"""
time_series.py

This file builds the Time Series tab of the California Maternal Health
Disparities Dashboard. It is imported by app.py, and can also be run on
its own while developing with: streamlit run time_series.py

"""

# importing libraries

import streamlit as st


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

    # placeholder until the California and national (CDC) charts are added
    st.info("Time series charts are coming soon.", icon="📈")


# lets this file be run on its own for development; app.py imports the function instead
if __name__ == "__main__":
    st.set_page_config(page_title='Time Series Preview', layout="wide")
    render_time_series_tab()
