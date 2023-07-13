#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 10:21:38 2023

@author: angus
"""

import pandas as pd

df = pd.read_csv('ready_train_w_urlcheck.csv')

def normalize_state(state):
    northeast_states = ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont', 'New Jersey', 'New York', 'Pennsylvania']
    midwest_states = ['Illinois', 'Indiana', 'Michigan', 'Ohio', 'Wisconsin', 'Iowa', 'Kansas', 'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'South Dakota']
    south_states = ['Delaware', 'Florida', 'Georgia', 'Maryland', 'North Carolina', 'South Carolina', 'Virginia', 'West Virginia', 'Alabama', 'Kentucky', 'Mississippi', 'Tennessee', 'Arkansas', 'Louisiana', 'Oklahoma', 'Texas']
    west_states = ['Arizona', 'Colorado', 'Nevada', 'New Mexico', 'Utah', 'Wyoming', 'Alaska', 'California', 'Hawaii', 'Oregon', 'Washington','Montana','Idaho']
    
    if state in northeast_states:
        return 'North East'
    elif state in midwest_states:
        return 'Midwest'
    elif state in south_states:
        return 'South'
    elif state in west_states:
        return 'West'
    else:
        return 'Unknown'


# Apply the normalization function to the 'State' column
df['Region'] = df['State'].apply(normalize_state)

# Write out the resulting dataframe
df.to_csv('ready_train_w_regions.csv', index=False)



