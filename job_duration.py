#!/usr/bin/env python
# coding: utf-8

"""
author: @Bill Tian
upload data: Jun 28, 2023

"""


import re
import pandas as pd
import numpy as np
import math




def capture_month_duration(duration):
    '''Capture start year/month and end year/month and calculate the duration in month'''
    
    if duration == '':
        return np.nan
    
    else:
        pattern = r'(\w{3} \d{4}) - Present|(\d{4}) - Present|(\w{3} \d{4}) - (\w{3} \d{4})|(\d{4}) - (\w{3} \d{4})|(\d{4}) - (\d{4})|(\w{3} \d{4}) - (\d{4})'

        match = re.search(pattern, duration)
        if match:
            whole = match.group(0)
            start_date = match.group(1) or match.group(2) or match.group(3) or match.group(5) or match.group(7) or match.group(9)
            end_date = 'Dec 2022'  #CHANGE TO PRESENT
            
            if 'Present' in whole:
                start_date = match.group(1) or match.group(2)
                end_year = 2022 #CHANGE TO PRESENT YEAR
                end_month = 12  #CHANGE TO PRESENT MONTH
                if len(start_date) != 4:                   
                    start_year = int(start_date.split()[1])
                    start_month = int(month_to_number(start_date.split()[0]))
                    
                else:
                    start_year = int(start_date[:4])
                    start_month = 6
                   
                if end_month < start_month:
                    duration_in_months = (end_year - start_year - 1)*12 + (12 - start_month + end_month)
                
                else:
                    duration_in_months = (end_year - start_year)*12 + (end_month - start_month)
                return duration_in_months
                    
            else:
                end_date = match.group(4) or match.group(6) or match.group(8) or match.group(10)
                
                if len(start_date) == 4:
                    start_month = 6
                    start_year = int(match.group(0)[:4])
                    if len(end_date) == 4:
                        end_month = 6
                        end_year = int(end_date[:4])
                    else:
                        end_year = int(end_date.split()[1])
                        end_month = int(month_to_number(end_date.split()[0]))
                    
                    if end_month < start_month:
                        duration_in_months = (end_year - start_year - 1)*12 + (12 - start_month + end_month)
                
                    else:
                        duration_in_months = (end_year - start_year)*12 + (end_month - start_month)
                    return duration_in_months
                
                else:
                    start_year = int(start_date.split()[1])
                    start_month = int(month_to_number(start_date.split()[0]))
                    
                    if len(end_date) == 4:
                        end_month = 6
                        end_year = int(end_date[:4])
                    else:
                        end_year = int(end_date.split()[1])
                        end_month = int(month_to_number(end_date.split()[0]))
                    
                    if end_month < start_month:
                        duration_in_months = (end_year - start_year - 1)*12 + (12 - start_month + end_month)
                
                    else:
                        duration_in_months = (end_year - start_year)*12 + (end_month - start_month)
                    return duration_in_months
                            
        return np.nan
    

def month_to_number(month):
    '''Word converted to number string'''
    month_dict = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12',
        'aot': '08', #<---Weird Month in the dataset
        'mai': '05' #<---Weird Month in the dataset
    }
    if month_dict.get(month) == None:
        return '06'
    return month_dict.get(month)


def get_jobduration(df_input, col):
    '''Return the list of converted duration for column 'col' '''
    
    df = df_input
    
    # compute job duration
    job_duration = []
    lst = list(df[col])
    for duration in lst:
        job_duration.append(capture_month_duration(duration))
    
    df[col] = job_duration
    return df

##Example:(for multiple columns)

#quit = pd.read_csv('Quitters.csv')
#target_columns = ['time_duration_1', 'time_duration_2', 'time_duration_3', 'time_duration_4',
 #                'time_duration_5', 'time_duration_6', 'time_duration_7', 'time_duration_8',
  #               'time_duration_9','time_duration_10']

##Fill Nan with ''

#new_quit = quit[['time_duration_1', 'time_duration_2', 'time_duration_3', 'time_duration_4',
 #                'time_duration_5', 'time_duration_6', 'time_duration_7', 'time_duration_8',
  #               'time_duration_9','time_duration_10']].fillna('')

##Following codes return a df with only columns time_duration_1 to 10 with work duration in month in each entry

#for c in target_columns:
 #   new_quit = get_jobduration(new_quit, c)

##replacing columns in original df

#for c in target_columns:
 #   quit[c] = new_quit[c]




