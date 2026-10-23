"""
build_time_series_data.py

One-off script that trims the raw source files used by the Time Series tab
into the small CSVs saved in data/time_series/. The raw files are not
committed; re-run this only if the source data changes.

Run in terminal with:
python scripts/build_time_series_data.py <path to CDPH births CSV> <path to DHCS t10 CSV>

"""

# importing libraries

import os
import sys
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CA_DIR = os.path.join(BASE_DIR, 'data', 'time_series', 'california')

# adult age brackets used in the CA DHCS notebook's Generational Shift chart
ADULT_AGES = ['20-24 years', '25-29 years', '30-34 years', '35-39 years', '40-44 years', '45 years and over']


def build_ca_births_by_age(cdph_path):
    """ trims the CDPH Live Birth Profiles by County file to adult age brackets

    Keeps residence-based counts for 2014-2024 by parent's age bracket,
    matching the filtering in the CA DHCS notebook. CDPH reports age and
    race separately, so these counts cover mothers of all races.
    Suppressed cells are kept as blanks so the dashboard can label them.

    Parameters
    ----------
    cdph_path : str
        path to 20260319_births_final_county_year_sup.csv

    Returns
    -------
    None. Writes ca_births_by_age.csv.
    """

    df = pd.read_csv(cdph_path, dtype={'Annotation_Code': str})

    # residence = where the parent lives, not where the birth happened
    df = df[(df['Geography_Type'] == 'Residence') & (df['Year'].between(2014, 2024))]
    df = df[(df['Strata'] == "Parent Giving Birth's Age") & (df['Strata_Name'].isin(ADULT_AGES))]

    out = df[['Year', 'County', 'Strata_Name', 'Count']].rename(columns={
        'Year': 'year', 'County': 'COUNTY_NAME_SHORT', 'Strata_Name': 'age_group', 'Count': 'births'
    })
    out = out.sort_values(['COUNTY_NAME_SHORT', 'year', 'age_group'])

    # whole-number counts; suppressed cells stay blank
    out['births'] = out['births'].astype('Int64')

    os.makedirs(CA_DIR, exist_ok=True)
    out.to_csv(os.path.join(CA_DIR, 'ca_births_by_age.csv'), index=False)
    print(f"wrote {len(out)} rows to ca_births_by_age.csv")


def build_medi_cal_births(t10_path):
    """ trims the DHCS Medi-Cal Birth Statistics table (t10) to African American births

    Keeps 2014-2023 rows for African American mothers, both payers and all
    groupers, matching the filtering in the CA DHCS notebook. Each birth is
    listed once under every grouper (diabetes, hypertension, smoking,
    substance use), so totals must be taken within a single grouper.

    Parameters
    ----------
    t10_path : str
        path to t10_detailedtables_2007-2023.csv

    Returns
    -------
    None. Writes medi_cal_births_african_american.csv.
    """

    df = pd.read_csv(t10_path, encoding='latin1')

    # removing the hidden BOM character and stray spaces from column names
    df.columns = df.columns.str.replace('ï»¿', '').str.strip()

    df = df[(df['Maternal Race/Ethnicity'] == 'African American') & (df['Calendar Year'] >= 2014)]

    out = df[['Calendar Year', 'Payer', 'Grouper', 'Birth Characteristic', 'Number of Births']].rename(columns={
        'Calendar Year': 'year', 'Payer': 'payer', 'Grouper': 'grouper',
        'Birth Characteristic': 'characteristic', 'Number of Births': 'births'
    })
    out['births'] = out['births'].astype('Int64')

    os.makedirs(CA_DIR, exist_ok=True)
    out.to_csv(os.path.join(CA_DIR, 'medi_cal_births_african_american.csv'), index=False)
    print(f"wrote {len(out)} rows to medi_cal_births_african_american.csv")


if __name__ == '__main__':
    build_ca_births_by_age(sys.argv[1])
    build_medi_cal_births(sys.argv[2])
