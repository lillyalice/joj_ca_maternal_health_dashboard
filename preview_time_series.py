"""
preview_time_series.py

Runs only the Time Series tab, for development.

Run in terminal with: streamlit run preview_time_series.py

"""

# importing libraries

import streamlit as st
from time_series import render_time_series_tab

st.set_page_config(page_title='Time Series Preview', layout="wide")
render_time_series_tab()
