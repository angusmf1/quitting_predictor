#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 12:48:04 2023

@author: angus
"""
import pandas as pd

# Function to classify the education level based on the school name and degree name
def classify_education_level(school_name, degree_name):
    school_name = str(school_name)
    degree_name = str(degree_name)
    
    if any(keyword in degree_name.lower() for keyword in ['phd', 'doctor', 'ph.d']) or any(keyword in school_name.lower() for keyword in ['phd', 'doctor', 'ph.d']):
        return 'PhD'
    elif any(keyword in degree_name.lower() for keyword in ['master', 'ms', 'me', 'm.','postgraduate', 'post']) or any(keyword in school_name.lower() for keyword in ['master', 'ms', 'm.','postgraduate', 'post']): 
        return "Master's"
    elif any(keyword in degree_name.lower() for keyword in ['bachelor', 'ba', 'bs','be','bfa','b.','b tech','b-tech','b sc', 'computer','engineering']) or any(keyword in school_name.lower() for keyword in ['bachelor','ba', 'bs','bfa','b.','b tech','b-tech','b sc',' be ']): 
        return "Bachelor's"
    elif any(keyword in degree_name.lower() for keyword in ['associate', 'a.','aas']) or any(keyword in school_name.lower() for keyword in ['associate', ' as', 'a.','aas']): 
        return "Associate's"
    elif any(keyword in degree_name.lower() for keyword in ['university','college', 'universidad','universit','tec','uc','undergraduate','military academy']) or any(keyword in school_name.lower() for keyword in ['university','college', 'universidad','universit','tec','uc','undergraduate','military academy']): 
        return "Bachelor's minus"
    elif 'NA' in degree_name or 'NA' in school_name:
        return 'NA'
    else:
        return 'Other'


# Function to rank the education levels
def rank_education_level(education_levels):
    ranking_order = ['NA', 'Other', "Bachelor's minus", "Associate's", "Bachelor's", "Master's", 'PhD']
    max_rank = -1
    max_level = 'NA'

    for level in education_levels:
        rank = ranking_order.index(level)
        if rank > max_rank:
            max_rank = rank
            max_level = level

    return max_level


# Iterate through every row in dataframe and call classify_education_level and rank_education_level
# takes a dataframe for an input, then adds 'education level' column
def normalize_edu(df):
    
    # Create a new column 'education level' in the DataFrame
    df['education level'] = ''
    df['school_name_1'] = df['school_name_1'].fillna('NA')
    df['degree_name_1'] = df['degree_name_1'].fillna('NA')

    # Iterate over each row and normalize education data
    for index, row in df.iterrows():
        education_levels = []

        for i in range(1, 4):
            school_name = row['school_name_' + str(i)]
            degree_name = row['degree_name_' + str(i)]
            if pd.notnull(degree_name) or pd.notnull(school_name):
                education_level = classify_education_level(school_name, degree_name)
                education_levels.append(education_level)

        if len(education_levels) > 0:
            max_level = rank_education_level(education_levels)
            if max_level == "Bachelor's minus":
                max_level = "Bachelor's"

            df.at[index, 'education level'] = max_level
           

# Prints out the edu normalization metrics 
def stats(df):
    print("PhD:         ",sum(df['education level']=="PhD"))
    print("Master's:    ",sum(df['education level']=="Master's"))
    print("Bachelor's:  ",sum(df['education level']=="Bachelor's"))
    print("Associate's: ",sum(df['education level']=="Associate's"))
    print("Other:       ",sum(df['education level']=="Other"))
    print("NA:          ",sum(df['education level']=="NA"))
    
    
    
    
### Example on how to run ###

#filename = 'Quitters combined.csv'
#q_df = pd.read_csv(filename)    

#normalize_edu(q_df)
#stats(q_df)
    
### Write out file with normalized data ###

#quitters_final = 'Quitters.csv'
#q_df.to_csv(quitters_final, index=False)    
    
    
    
    