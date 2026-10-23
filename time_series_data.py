"""
time_series_data.py

This file loads the datasets used by the Time Series tab. The CSVs in
data/time_series/ are small trimmed copies of the raw source files, made
with scripts/build_time_series_data.py.

"""

# importing libraries

import pandas as pd
import os

# setting base directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CA_DIR = os.path.join(BASE_DIR, 'data', 'time_series', 'california')


def load_ca_births():
    """ loads yearly California births by county

    This dataset comes from CDPH Live Birth Profiles by County (2014-2024),
    by county of residence. One row per county per year, with total births
    and births to Black parents. Small counts are suppressed by CDPH and
    are left as NaN.

    Parameters
    ----------
    None.

    Returns
    -------
    Returns births dataframe with a 'black_share' column (% of all births).
    """

    # loading in dataset; county names match COUNTY_NAME_SHORT in the map data
    births = pd.read_csv(os.path.join(CA_DIR, 'ca_births_by_county.csv'))

    # share of all births in that county and year that were to Black parents
    births['black_share'] = births['black_births'] / births['total_births'] * 100

    return births
