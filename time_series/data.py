"""
time_series/data.py

This file loads the datasets used by the Time Series tab. The CSVs in
data/time_series/ are small trimmed copies of the raw source files, made
with scripts/build_time_series_data.py.

"""

# importing libraries

import pandas as pd
import os

# setting base directory (the project folder, one level above this package)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CA_DIR = os.path.join(BASE_DIR, 'data', 'time_series', 'california')

# adult age brackets in display order, with the labels used in the chart legend
# (kept the same as the CA DHCS notebook's legend)
AGE_LABELS = {
    '20-24 years': '20-24 years', '25-29 years': '25-29 years', '30-34 years': '30-34 years',
    '35-39 years': '35-39 years', '40-44 years': '40-44 years', '45 years and over': '45 years and over',
}


def load_ca_births_by_age():
    """ loads yearly California births by parent's age bracket

    This dataset comes from CDPH Live Birth Profiles by County (2014-2024),
    by county of residence, for adult age brackets (20+). CDPH reports age
    and race separately, so these counts cover mothers of all races. Small
    counts are suppressed by CDPH and are left as NaN.

    Parameters
    ----------
    None.

    Returns
    -------
    Returns births dataframe with statewide rows labeled 'California' and
    a 'pct' column (% of that year's adult births in the area).
    """

    # loading in dataset; county names match COUNTY_NAME_SHORT in the map data
    births = pd.read_csv(os.path.join(CA_DIR, 'ca_births_by_age.csv'))

    # statewide totals are the sum of all counties; suppressed small-county
    # cells are skipped, so these slightly undercount
    statewide = births.groupby(['year', 'age_group'], as_index=False)['births'].sum()
    statewide['COUNTY_NAME_SHORT'] = 'California'
    births = pd.concat([births, statewide], ignore_index=True)

    # percentage of each year's adult births falling in each age bracket
    year_totals = births.groupby(['COUNTY_NAME_SHORT', 'year'])['births'].transform('sum')
    births['pct'] = births['births'] / year_totals * 100

    births['age_label'] = births['age_group'].map(AGE_LABELS)

    return births


def load_medi_cal_rates():
    """ loads yearly diagnosis rates for African American mothers by payer

    This dataset comes from DHCS Medi-Cal Birth Statistics (2014-2023),
    California resident hospital births. It is statewide only. Rates are
    diagnoses out of births with a known status (unknowns are excluded),
    matching the CA DHCS notebook.

    Parameters
    ----------
    None.

    Returns
    -------
    Returns one row per year and payer with 'births', 'medi_cal_share'
    (that payer's % of the year's births; read it on the Medi-Cal rows),
    'hypertension_rate' and 'diabetes_rate' columns (%).
    """

    births = pd.read_csv(os.path.join(CA_DIR, 'medi_cal_births_african_american.csv'))

    # one column per birth characteristic, e.g. 'Hypertension Diagnosis'
    wide = births.pivot_table(index=['year', 'payer'], columns='characteristic',
                              values='births', aggfunc='sum').reset_index()

    wide['hypertension_rate'] = wide['Hypertension Diagnosis'] / (
        wide['Hypertension Diagnosis'] + wide['No Hypertension Diagnosis']) * 100
    wide['diabetes_rate'] = wide['Diabetes Diagnosis'] / (
        wide['Diabetes Diagnosis'] + wide['No Diabetes Diagnosis']) * 100

    # each birth is listed once under every grouper, so births per payer are counted within
    # one grouper only; Medi-Cal's share of all births to African American mothers that year
    payer_births = births[births['grouper'] == 'Hypertension Status'].groupby(
        ['year', 'payer'], as_index=False)['births'].sum()
    wide = wide.merge(payer_births, on=['year', 'payer'])
    wide['medi_cal_share'] = wide.groupby('year')['births'].transform(
        lambda b: b / b.sum() * 100)

    return wide[['year', 'payer', 'births', 'medi_cal_share', 'hypertension_rate', 'diabetes_rate']]
