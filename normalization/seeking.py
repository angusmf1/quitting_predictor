#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 11:42:23 2023

@author: angus
"""

import pandas as pd
import numpy as np

# Step 2: Read the CSV file into a DataFrame
df = pd.read_csv('quitting_data.csv')

# Step 3: Define a function to check for the keywords
def check_keywords(text):
    keywords = ['seeking', 'looking', 'open', 'available', 'transitioning']
    return 1 if any(keyword in text.lower() for keyword in keywords) else 0

# Step 4: Apply the function to create the 'Seeking' column with 1 or 0
df['Seeking'] = df[['Summary', 'Skills', 'title_1']].apply(lambda row: check_keywords(' '.join(map(str, row))), axis=1)

# Now, your DataFrame 'df' contains a new column 'Seeking' with 1 or 0 based on the presence of the keywords.

ratio = np.sum(df['Seeking']==1)/len(df['Seeking'])

print('% Seeking: ',ratio)

df.to_csv('quitting_data2.csv', index=False)