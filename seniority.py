import pandas as pd
import numpy as np



def seniority_checker(title_1, title_2 , duration_1, duration_2):
    '''Identity seniority and return a string'''
  
    title1 = title_1.lower()
    title2 = title_2.lower()
    
    if title1 == '':
        return np.nan
    elif any(keyword in title1 for keyword in ['senior', 'staff', 'lead', 'founder', 'chief', 'sr.', 'ceo', 'cto','principal', 'owner' ]):
        return 'Senior'
    elif any(keyword in title1 for keyword in ['intern', 'student']):
        return 'Intern'
    elif title1 == title2:    # The idea is that if a user work in the same job title/position in two different companies, experience added up
        if duration_1 + duration_2 >= 36:   
            return 'Middle'
        elif 12 <= (duration_1 + duration_2) < 36:
            return 'Junior'
        else:
            return 'Entry'
    else:
        if duration_1 >= 36:
            return 'Middle'
        elif 12 <= duration_1 < 36:
            return 'Junior'
        else:
            return 'Entry'
        
    
    
def grouping_seniority(input_df):
    '''Check seniority for each row'''
  
    df = input_df.copy()
    lst = []
    df['title_1'] = df['title_1'].fillna('')
    df['title_2'] = df['title_2'].fillna('')
    
    for i in range(len(df)):
    
        lst.append(seniority_checker(df['title_1'][i], df['title_2'][i] , df['time_duration_1'][i], df['time_duration_2'][i]))
    return lst

##Example:

#df_quit = pd.read_csv('Quitters1.csv')
#seniority_lst_quit = grouping_seniority(df_quit)
#df_quit['Seniority'] = seniority_lst_quit

