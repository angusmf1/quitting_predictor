import numpy as np
import pandas as pd
from tsfresh import extract_features


"""
***Need dataFrames that contains both original duration in string and duration converted in float: 
df

"""



def get_start_year(time_duration):
    """Find the start year in the duration"""
    if pd.notnull(time_duration):
        parts = time_duration.split('-')
        if len(parts) == 2 and len(parts[0].split()) == 2:
            try:
                return pd.to_datetime(parts[0]).year
            except ValueError:
                pass 
        if len(parts) == 2 and len(parts[0].split()) == 1:
            try:
                return pd.to_datetime(parts[0]).year
            except ValueError:
                pass
    return None


def find_min_start_year(row):
    """Find the minimum start year among all the values in the list"""
    non_null_years = [get_start_year(cell) for cell in row]
    non_null_years = [year for year in non_null_years if year is not None]
    if non_null_years:
        return min(non_null_years)
    return None


def start_year(df):
    """Create a column for first job start year"""

    df_name = df.reset_index().rename(columns = {'index':'Name'})
    
    df_dura = df_name[['time_duration_1', 'time_duration_2', 'time_duration_3', 'time_duration_4',
        'time_duration_5', 'time_duration_6', 'time_duration_7', 'time_duration_8', 'time_duration_9',
        'time_duration_10']]
    
    df_name['first_job_start_year'] = df_dura.apply(lambda row: find_min_start_year(row), axis=1)
    
    return df_name

#df_test = start_year(df)


def df_melt(df):
    """convert the DataFrame into ts format"""

    # List of columns you want to keep as id_vars
    id_vars = ['first_job_start_year', 'Name']

    # List of columns you want to melt for time_duration
    value_vars_duration = [f'time_duration_{i}' for i in range(1, 11)]

    # List of columns you want to melt for time_duration_int
    value_vars_duration_int = [f'time_duration_{i}_int' for i in range(1, 11)]

    # Melt the DataFrame for time_duration
    df_noint = pd.melt(df, id_vars=id_vars, value_vars=value_vars_duration, var_name='variable', value_name='time_duration')

    # Melt the DataFrame for time_duration_int
    df_int = pd.melt(df, id_vars=id_vars, value_vars=value_vars_duration_int, var_name='variable', value_name='time_duration_int')

    # Merge the two melted DataFrames based on the 'variable' column
    df_noint['time_duration_int'] = df_int['time_duration_int']

    # Drop rows with NaN in the time_duration column
    df_noint = df_noint.dropna(subset=['time_duration'])
    
    # Sort by 'Name', 'first_job_start_year', and 'time_duration' to prepare for the time series data
    df_noint = df_noint.sort_values(by=['Name', 'first_job_start_year', 'time_duration'])
    
    df_noint.reset_index(drop=True, inplace=True)
    
    return df_noint



#df_melted = df_melt(df_test)


def calculate_time_since_first_job(row):
    """Calculate the time since the first job for each row"""

    duration_str = row['time_duration']
    print(duration_str)
    if 'Present' in duration_str:
        if pd.notnull(row['first_job_start_year']):
            return pd.to_datetime('now').year - int(row['first_job_start_year'])
        else:
            return None
    elif len(duration_str.split('-')) == 2:
        # Split the duration string by '-' and take the second part as the start year
        start_year = duration_str.split('-')[1].strip()[-4:]
        if start_year.isdigit() and pd.notnull(row['first_job_start_year']):
            # Convert the start_year to an integer if it is a valid digit
            start_year = int(start_year)
            return start_year - int(row['first_job_start_year'])
        else:
            # Handle cases where the start year is not a valid digit or first_job_start_year is NaN
            return None
        
    elif len(duration_str.split('-')) == 3:
        if duration_str.split('-')[1].strip()[:4].isdigit():
            start_year = duration_str.split('-')[1].strip()[:4]
            start_year = int(start_year)
            return start_year - int(row['first_job_start_year'])
        else:
            return None
    else:
        start_year = duration_str.split('-')[0][:4]
        if start_year.isdigit() and pd.notnull(row['first_job_start_year']):
            start_year = int(start_year)
            return start_year - int(row['first_job_start_year'])
        else:
            return None



#df_melted['time'] = df_melted.apply(calculate_time_since_first_job, axis=1)

###""Change Column Names"""

#df_ts = df_melted[['Name', 'time', 'time_duration_int']].rename(columns = {'Name':"id", 'time':'years since first job', 'time_duration_int':'work duration in months'})

#df_ts.fillna({'years since first job':0, 'work duration in months': 0}, inplace=True)



"""Run tsfresh"""

#extracted_features = extract_features(df_ts, column_id="id", column_sort="years since first job")