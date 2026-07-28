"""
data_loader.py

This file loads two county_level datasets containing various 
indicators of Maternal health alongside other socioeconomic and 
enviormental factors. It also defines the dashboard's dropdown menu
options.

"""
# importing libraries

import pandas as pd
import os 

# setting base directory 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# defining a function 'load_snapshot_data()' to read in our datasets

def load_snapshot_data():
    """ loads snapshot data; data that does not contain time variables
    
    This function loads in snapshot data -- data that does not contain 
    time dependent variables -- to display on the dashboard

    Parameters
    ----------
    None. 

    Returns
    -------
    Returns a finished dataframe (df) with the changes made.
    """

    # loading in our snapshot dataset containing all chosen variables;
    # forces the 'fips' column to ensure it is read in as a string and does not become and integer
    df = pd.read_csv(os.path.join(BASE_DIR, 'dashboard_master.csv'), dtype={'fips': str})

    # renaming columns for consistency across datasets
    df = df.rename(columns={
        'fips': 'FIPS', # this column is capitalized in our crime dataset
        'county_name_short' : 'COUNTY_NAME_SHORT',
        'county_name_full' : 'COUNTY_NAME_FULL'
    })

    # selecting the FIPS (Federal Information Processing Standards) --
    # which are geographic location codes used by the federal government --
    # column from the dataset and forcing every value to a string and pads each
    # value with leading zeros until it is 5 characters long. (ex: "6001" to "06001")

    df['FIPS'] = df['FIPS'].astype(str).str.zfill(5)
    return df

def load_crime_data():
    """ loads crime data which containts yearly rates of violent crime
        
        This dataset contains yearly rates of violent crime
        with regional shrinkage smoothed rates; One row per county per year
    
        Parameters
        ----------
        None.

        Returns
        -------
        Returns standardized crime dataset.
        """

    # loading in dataset
    crime = pd.read_csv(os.path.join(BASE_DIR, 'ca_violent_crime_final.csv'), dtype={'FIPS': str})

    # selecting the FIPS (Federal Information Processing Standards) --
    # which are geographic location codes used by the federal government --
    # column from the dataset and forcing every value to a string and pads each
    # value with leading zeros until it is 5 characters long. (ex: "6001" to "06001")
    crime['FIPS'] = crime['FIPS'].astype(str).str.zfill(5)

    # removing Unnamed column; if column does not exist do not raise error
    crime = crime.drop(columns=['Unnamed: 0'], errors='ignore')

    # converting 'year', 'crime_rate', and 'crime_rate_smoothed' to numeric dtype;
    # anything that cannot become a number becomes NaN
    crime['year'] = pd.to_numeric(crime['year'], errors='coerce')
    crime['crime_rate'] = pd.to_numeric(crime['crime_rate'], errors='coerce')
    crime['crime_rate_smoothed'] = pd.to_numeric(crime['crime_rate_smoothed'], errors='coerce')

    # renaming crime columns for consistency
    crime = crime.rename(columns={'county_name': 'COUNTY_NAME_SHORT'})

    # returning crime dataset
    return crime

"""
Here is where we define and configure the variables that will be displayed
on the dashboard. 
"""

def get_variable_config():
    """ loads crime data which containts yearly rates of violent crime
            
    This dataset contains yearly rates of violent crime
    with regional shrinkage smoothed rates; One row per county per year
        
    Parameters
    ----------
    None.
    
    Returns
    -------
    Returns standardized crime dataset.
    """
    # returning a dictionary that contains what will be included
    # in the dropdown menu on the dashboard

    return {
        'Preterm Birth Rate': {
        # settings for the 'Preterm Birth Rate specifically; the scale factor (100)
        # maps the a decimal to its smoothed representation (ex: 0.097 to 9.7)
        'column' : 'preterm_rate_smoothed', 'scale_factor': 100,
        # this variable doesn't need a year slide because it is a single snapshot
        # '%' is appened after the number when displayed
        'has_time_dimension' : False, 'suffix' : '%', 'value_type': 'percent',
        # list that decides the defininf low and high ends of the maps color scale
        'color_range' : ["#94839C",'#2E183F'], 'vis_min' :  7, 'vis_max' : 10,
        },

        # poverty rate variable
        'Poverty Rate': {
            'column': 'poverty_rate_overall', 'scale_factor': 1,
            'has_time_dimension': False, 'suffix': '%', 'value_type': 'percent',
            'color_range': ["#94839C",'#2E183F'], 'vis_min': 6, 'vis_max': 30,
        },

        # percentage of low birth weight
        'Low Birth Weight Rate': {
            'column': 'low_birth_weight_pct', 'scale_factor': 1,
            'has_time_dimension': False, 'suffix': '%', 'value_type': 'percent',
            'color_range': ["#94839C",'#2E183F'], 'vis_min': 3, 'vis_max': 10,
        },

        'Diabetes Prevalence': {
            'column': 'diabetes_prevalence', 'scale_factor': 1,
            'has_time_dimension': False, 'suffix': '%', 'value_type': 'percent',
            'color_range': ["#94839C",'#2E183F'], 'vis_min': 9, 'vis_max': 16,
        },

        'Cardiovascular Disease Rate': {
            'column': 'cvd_rate', 'scale_factor': 1,
            'has_time_dimension': False, 'suffix': ' per 10,000', 'value_type': 'count',
            'color_range': ["#94839C",'#2E183F'], 'vis_min': 0, 'vis_max': 30,
        },

        'Violent Crime Rate': {
            'column': 'crime_rate_smoothed', 'scale_factor': 1,
            'has_time_dimension': True, 'suffix': ' per 100k', 'value_type': 'count',
            'color_range': ["#94839C", '#2E183F'], 'vis_min': 150, 'vis_max': 1000,
        }
    }

