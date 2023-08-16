#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:36:56 2023

@author: angus
"""

import pandas as pd
import numpy as np
import re

data = pd.read_csv('ready_train.csv').drop(['Unnamed: 0.1','Unnamed: 0'], axis=1)


def has_custom_url(linkedin_url):
    pattern = '(?=.*-.*-)(.*(?:\d.*?){5})$'
    match = re.match(pattern, linkedin_url)
    return 0 if match else 1


def check_hyphens(linkedin_url):
    pattern = '.*-.*-.*-.*-'
    return bool(re.match(pattern, linkedin_url))


# Apply custom URL check to 'profile_url' column and create a new 'custom_url' column
data['custom_url'] = data['profile_url'].apply(has_custom_url)

check = []
for i,url in enumerate(data.profile_url.items()):
    if check_hyphens(str(url)) == True:
        check.append(i)
        #print(i, url)
    
data.loc[check, 'custom_url'] = 1

print('total custom urls: ',np.sum(data.custom_url==1))

#write out results
data.to_csv('ready_train_w_urlcheck.csv', index=False)

