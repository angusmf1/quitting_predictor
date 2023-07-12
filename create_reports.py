#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:30:59 2023

@author: angus
"""

### Pandas Profile Report ###

import pandas as pd
from ydata_profiling import ProfileReport


# read in csv file
data = pd.read_csv('ready_train_w_urlcheck.csv')


# run pandas profile and write out report
profile = ProfileReport(data)
profile.to_file(output_file='Pandas Profile Report 12 July.html')





