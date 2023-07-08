#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:01:07 2023

@author: angus
"""

import pandas as pd
import re
import datetime


q_df = pd.read_csv('quitters_w_seniority.csv')
nq_df = pd.read_csv('nonquitters_w_seniority.csv')


#columns_to_drop = ['Unnamed: 0.1', 'Unnamed: 0']
#q_df = q_df.drop(columns_to_drop, axis=1)
#nq_df = nq_df.drop(columns_to_drop, axis=1)

# Calculate total working experience in months
q_df['total_experience'] = q_df[['time_duration_1', 'time_duration_2', 'time_duration_3', 'time_duration_4',
                             'time_duration_5', 'time_duration_6', 'time_duration_7', 'time_duration_8',
                             'time_duration_9', 'time_duration_10']].sum(axis=1)

nq_df['total_experience'] = nq_df[['time_duration_1', 'time_duration_2', 'time_duration_3', 'time_duration_4',
                             'time_duration_5', 'time_duration_6', 'time_duration_7', 'time_duration_8',
                             'time_duration_9', 'time_duration_10']].sum(axis=1)



def normalize_education_years(df):
    """Normalizes education years into YYYY-YYYY format.

    Args:
      df: The DataFrame containing the ed_time_duration columns.

    Returns:
      A new DataFrame with the normalized education years.
    """

    #pattern = r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b'
    pattern = r'[a-zA-Z]'
    
    # Create a function to normalize a single education year.
    def normalize_education_year(year):
        if year == 'Present':
            return str(datetime.datetime.now().year)
        elif year == '':
            return None
        elif (re.search(pattern, str(year))):
            return None
        else:
            return year

  # Loop through the rows in the DataFrame.
    for index, row in df.iterrows():
        # Normalize each education year.
        for col in ['ed_time_duration_1', 'ed_time_duration_2', 'ed_time_duration_3']:
            df.loc[index, col] = normalize_education_year(row[col])

    return df

q_df = normalize_education_years(q_df)
nq_df = normalize_education_years(nq_df)


def check_exp(q_df):

    # Extract graduation years
    q_df['grad_year_1'] = q_df['ed_time_duration_1'].str.split(' - ').str[1].astype(float)
    q_df['grad_year_2'] = q_df['ed_time_duration_2'].str.split(' - ').str[1].astype(float)
    q_df['grad_year_3'] = q_df['ed_time_duration_3'].str.split(' - ').str[1].astype(float)

    # Find the earliest valid graduation year
    valid_grad_years = q_df[['grad_year_1', 'grad_year_2', 'grad_year_3']].stack().dropna()
    if valid_grad_years.empty:
        # Handle case when all graduation years are missing or invalid
        q_df['exp check'] = 0
    else:
        earliest_grad_year = valid_grad_years.min()

        # Calculate number of months from earliest graduation year until now
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        months_since_graduation = (current_year - earliest_grad_year) * 12 + current_month

        # Compare with total_experience
        q_df['exp_check'] = q_df['total_experience'].apply(lambda x: 1 if x > months_since_graduation else 0)

        return q_df


def calculate_avg_work_exp(df):
    job_columns = ['time_duration_1', 'time_duration_2', 'time_duration_3', 'time_duration_4',
                   'time_duration_5', 'time_duration_6', 'time_duration_7', 'time_duration_8',
                   'time_duration_9', 'time_duration_10']
    df['num_jobs'] = df[job_columns].apply(lambda row: row.notnull().sum(), axis=1)
    df['avg_work_exp'] = df['total_experience'] / df['num_jobs']
    return df

q_df = check_exp(q_df)
nq_df = check_exp(nq_df)
q_df = calculate_avg_work_exp(q_df)
nq_df = calculate_avg_work_exp(nq_df)


print('# of Quitters failed check: ', sum(q_df['exp_check']==1))
print('# of NonQuitters failed check: ', sum(nq_df['exp_check']==1))

q_df = q_df.drop(['grad_year_1', 'grad_year_2', 'grad_year_3','num_jobs'], axis=1)
nq_df = nq_df.drop(['grad_year_1', 'grad_year_2', 'grad_year_3','num_jobs'], axis=1)


#write out files with 'total_experience and 'exp_check'
quitters_out = 'quitters_updated.csv'
q_df.to_csv(quitters_out, index=False)

nonquitters_out = 'nonquitters_updated.csv'
nq_df.to_csv(nonquitters_out, index=False)





