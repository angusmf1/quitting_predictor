#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re


# In[3]:


def capture_month_duration(duration):
    if duration == '':
        return 0
    
    else:
        pattern = r'(\w{3} \d{4}) - Present|(\d{4}) - Present|(\w{3} \d{4}) - (\w{3} \d{4})|(\d{4}) - (\w{3} \d{4})|(\d{4}) - (\d{4})|(\w{3} \d{4}) - (\d{4})'

        match = re.search(pattern, duration)
        if match:
            whole = match.group(0)
            start_date = match.group(1) or match.group(2) or match.group(3) or match.group(5) or match.group(7) or match.group(9)
            end_date = 'Dec 2022'  #Change to Present
            
            if 'Present' in whole:
                start_date = match.group(1) or match.group(2)
                end_year = 2022
                end_month = 12  #Change to Present
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
                            
        return 0
    

def month_to_number(month):
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
        'aot': '08'
    }
    return month_dict.get(month)


def get_jobduration(df_input, col):
    df = df_input
    
    # filling the null values with '' so things are not compared with NaN 
    df.fillna('', inplace = True)
    df1 = df.copy()
    # compute job duration
    job_duration = []
    lst = list(df[col])
    for duration in lst:
        job_duration.append(capture_month_duration(duration))
    
    df1[f'{col}_int'] = job_duration
    return df1


# In[ ]:




