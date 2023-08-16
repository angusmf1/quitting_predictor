import pandas as pd
import numpy as np

"""
author: @Bill Tian
upload data: Jun 28, 2023
updated: Jul 11, 2023

"""

def check_seniority(input_df, col):
    df = input_df
    df[col] = df[col].fillna('')
    lst = list(df[col])
    level = []
    for t in lst:
        if t == '':
            level.append(np.nan)
        elif any(keyword in t for keyword in ['junior']):
            level.append('Junior')
        elif any(keyword in t for keyword in ['founder', 'chief', 'ceo', 'cto', 'owner','vice president', 'director']):
            level.append('Management')
        elif any(keyword in t for keyword in ['senior', 'lead','chief','principal']):
            level.append('Senior')
        elif any(keyword in t for keyword in ['intern', 'student']):
            level.append('Intern')
        else:
            level.append('Regular')
            
    return level

##Example:

#df_quit = pd.read_csv('Quitters1.csv')
#seniority_lst_quit = check_seniority(df_quit, 'title_1')
#df_quit['Seniority'] = seniority_lst_quit

