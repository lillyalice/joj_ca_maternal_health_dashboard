"""
build_time_series_data.py

One-off script that trims the raw source files used by the Time Series tab
into the small CSVs saved in data/time_series/. The raw files are not
committed; re-run this only if the source data changes.

Run in terminal with: python scripts/build_time_series_data.py <path to CDPH births CSV>

"""

# importing libraries

import os
import sys
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CA_DIR = os.path.join(BASE_DIR, 'data', 'time_series', 'california')


def build_ca_births(cdph_path):
    """ trims the CDPH Live Birth Profiles by County file

    Keeps residence-based counts for 2014-2024, for total births and births
    to Black parents, matching the filtering in the CA DHCS notebook.
    Suppressed cells are kept as blanks so the dashboard can label them.

    Parameters
    ----------
    cdph_path : str
        path to 20260319_births_final_county_year_sup.csv

    Returns
    -------
    None. Writes ca_births_by_county.csv.
    """

    df = pd.read_csv(cdph_path, dtype={'Annotation_Code': str})

    # residence = where the parent lives, not where the birth happened
    df = df[(df['Geography_Type'] == 'Residence') & (df['Year'].between(2014, 2024))]

    total = df[df['Strata'] == 'Total Population']
    black = df[(df['Strata'] == "Parent Giving Birth's Race-Ethnicity") & (df['Strata_Name'] == 'Black')]

    out = total[['Year', 'County', 'Count']].rename(columns={'Count': 'total_births'}).merge(
        black[['Year', 'County', 'Count']].rename(columns={'Count': 'black_births'}),
        on=['Year', 'County'], how='left'
    )
    out = out.rename(columns={'Year': 'year', 'County': 'COUNTY_NAME_SHORT'})
    out = out.sort_values(['COUNTY_NAME_SHORT', 'year'])

    # whole-number counts; suppressed cells stay blank
    out[['total_births', 'black_births']] = out[['total_births', 'black_births']].astype('Int64')

    os.makedirs(CA_DIR, exist_ok=True)
    out.to_csv(os.path.join(CA_DIR, 'ca_births_by_county.csv'), index=False)
    print(f"wrote {len(out)} rows to ca_births_by_county.csv")


if __name__ == '__main__':
    build_ca_births(sys.argv[1])
