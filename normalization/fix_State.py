#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 11:36:51 2023

@author: angus
"""

import glob
import pandas as pd
import numpy as np

training_files = glob.glob('datasets/*.csv')

files = []
for filename in training_files:
    data = pd.read_csv(filename)
    files.append(data)
    
output = pd.concat(files, ignore_index=True)

output.drop_duplicates(subset='Linkedin_url', keep='first', inplace=True)
print(output.shape)

print(np.sum(output['State'].isnull())/len(output))


## read in file to fix

raw = pd.read_csv('quitting_data2.csv')

print(raw.shape)

# Use the 'Linkedin_url' column as the primary key to merge the DataFrames and fill missing 'State' values
merged_df = raw.merge(output, on='Linkedin_url', how='left', suffixes=('', '_y'))

# Update the 'State' column in the 'raw' DataFrame with the non-null values from the 'output' DataFrame
merged_df['State'] = merged_df['State'].combine_first(merged_df['State_y'])

# Drop the unnecessary columns
merged_df.drop(columns=['State_y'], inplace=True)

# Assign the updated DataFrame back to the 'raw' DataFrame
raw = merged_df.copy()

print(np.sum(raw['State'].isnull())/len(output))

columns_to_drop = [
    'Summary_y', 'Skills_y', 'title_1_y',
    'company_1_y', 'time_duration_1_y', 'Job_Description_1_y', 'title_2_y',
    'company_2_y', 'time_duration_2_y', 'Job_Description_2_y', 'title_3_y',
    'company_3_y', 'time_duration_3_y', 'Job_Description_3_y', 'title_4_y',
    'company_4_y', 'time_duration_4_y', 'Job_Description_4_y', 'title_5_y',
    'company_5_y', 'time_duration_5_y', 'Job_Description_5_y', 'title_6_y',
    'company_6_y', 'time_duration_6_y', 'Job_Description_6_y', 'title_7_y',
    'company_7_y', 'time_duration_7_y', 'Job_Description_7_y', 'title_8_y',
    'company_8_y', 'time_duration_8_y', 'Job_Description_8_y', 'title_9_y',
    'company_9_y', 'time_duration_9_y', 'Job_Description_9_y', 'title_10_y',
    'company_10_y', 'time_duration_10_y', 'Job_Description_10_y', 'school_name_1_y',
    'ed_time_duration_1_y', 'degree_name_1_y', 'education_fos_1_y', 'school_name_2_y',
    'ed_time_duration_2_y', 'degree_name_2_y', 'education_fos_2_y', 'school_name_3_y',
    'ed_time_duration_3_y', 'degree_name_3_y', 'education_fos_3_y', 'school_name_4_y',
    'ed_time_duration_4_y', 'degree_name_4_y', 'education_fos_4_y', 'school_name_5_y',
    'ed_time_duration_5_y', 'degree_name_5_y', 'education_fos_5_y', 'school_name_6_y',
    'ed_time_duration_6_y', 'degree_name_6_y', 'education_fos_6_y', 'First Name_y',
    'Middle Name_y', 'Surname_y', 'City_y', 'Country_y', 'profile_url_y',
    'edu 4 activities_y', 'edu 5 activities_y',
    'edu 6 activities_y']

raw.drop(columns=columns_to_drop, inplace=True, axis=0)

print(raw.shape)

raw.to_csv('quitting_data3.csv', index=False)



