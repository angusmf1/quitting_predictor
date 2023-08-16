#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 15:03:14 2023

@author: angus
"""

import csv
import re
import time
from fuzzywuzzy import fuzz
import pandas as pd
import glob

def normalize_job_titles(filename):


    #############CHANGE INFORMATION BELOW THIS LINE#################

    # File name of the job titles to be normalized
    #file_name = '/Users/yuantian/Desktop/developerDB/quitter_vs_non_quitter/NonQuitters1.csv'
    file_name = filename

    # Library files
    find_library_name = 'find_lib.csv'
    title_lib = 'title_lib.csv'

    # Column name that you want normalized
    column_name = 'title_2'

    ##########################ABOVE HERE############################



    stopwords = ["staff"]

    def find_replace():
        df = pd.read_csv(file_name)
        lib = pd.read_csv(find_library_name)

        for row in lib['Words']:
            row = row.lower()
            find = row.split('|')[0]
            find = find.strip()

            replace = row.split('|')[1]
            replace = replace.strip()

            df[column_name] = df[column_name].str.lower().replace(find, replace, regex=True)
        # removes the stop words
        df[column_name] = df[column_name].astype(str) .apply(lambda x: ' '.join(word for word in x.split() if word not in stopwords))
        # removes company names
        df[column_name] = df[column_name].apply(lambda x: re.sub(r'\bat.+', '', x))
        
        #df.to_csv(file_name[:-4] + '_find_replaced.csv', index = False)
        
        return df[column_name]


    # Compares the result of the find/replace function OPTIONA
    def compare(column2):
        df1 = pd.read_csv(file_name)

        # Extract the column you want to compare
        column1 = df1[column_name].str.lower()
        # column2 = df2[column_name]

        # Compare the columns
        comparison_result = column1 != column2

        percentage_changed = (comparison_result.value_counts(normalize=True) * 100).round(2)
        print(percentage_changed)

        result_df = pd.DataFrame({
            'Original': column1,
            'Replaced': column2,
            'Changed?': comparison_result,
        })

        result_df.to_csv('comparison_result.csv', index=False)

        # # Get the frequency counts of column1
        # column1_counts = column1.value_counts().reset_index()
        # column1_counts.columns = ['Before Title', 'Before Freq']

        # # Sort the column1 counts by frequency in descending order
        # column1_counts = column1_counts.sort_values(by='Before Freq', ascending=False)

        # # Get the frequency counts of column2
        # column2_counts = column2.value_counts().reset_index()
        # column2_counts.columns = ['After Title', 'After Freq']

        # # Sort the column2 counts by frequency in descending order
        # column2_counts = column2_counts.sort_values(by='After Freq', ascending=False)

        # # Create a DataFrame with all four columns
        # before_after_freq = pd.DataFrame({
        #     'Before Title': column1_counts['Before Title'],
        #     'Before Freq': column1_counts['Before Freq'],
        #     'After Title': column2_counts['After Title'],
        #     'After Freq': column2_counts['After Freq']
        # })

        # # Save the before_after_freq DataFrame to a new CSV file
        # before_after_freq.to_csv('before-after-freq.csv', index=False)
        return



    # Find/replace changes library
    changes = {
        "seniority": "senior",
        "soft": "software",
        "eng": "engineer",
        "enig": "engineering",
        "deev": "development",
        "dev": "developer",
        "testing": "test",
        "cloudcloud": "cloud"
    }

    ## Fuzzy Matching helper Functions
    def remove_changes(title):
        for key, value in changes.items():
            if key in title:
                title = title.replace(key, value)

        # Dev ops title fix
        return title.replace("developerelopment", "development")


    important = ["seniority", "junior", "principal"]
    def important_titles(before, after):
        for imp in important:
            if imp in before and imp not in after:
                after = imp + " " + after
        return after


    def compare_titles_and_save(titles_before):
        titles_list = []

        with open(title_lib, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                title = row[0]
                titles_list.append(title)

        unchanged_titles = []
        with open(file_name, 'r') as term:
            temp = csv.DictReader(term)
            for row in temp:
                unchanged_titles.append(row[column_name])

        number = 0
        same = 0
        for i, title in enumerate(titles_before):
            if title in titles_list:
                same = same + 1
                unchanged_titles[i] = remove_changes(title)
            else:
                if "intern" in title:
                    same = same + 1
                    unchanged_titles[i] = remove_changes(title)
                else:
                    match = max(titles_list, key=lambda x: fuzz.token_set_ratio(title, x))
                    similarity_score = fuzz.partial_token_set_ratio(title, match)
                    if similarity_score >= 80:
                        number = number + 1
                        match = important_titles(title, match)
                        unchanged_titles[i] = remove_changes(match)
                    else:
                        unchanged_titles[i] = remove_changes(title)

        df = pd.read_csv(file_name)
        df[column_name] = unchanged_titles
        df.to_csv('updated_' + file_name, index=False)

        print(f"Percentage of titles changed: {float(number) / len(titles_before)} ")
        print(f"Percentage of titles already normalized: {float(same) / len(titles_before)}")
        print(f"Percentage of titles not changed: {1 - float(number) / len(titles_before) - float(same) / len(titles_before)}")


    # Output Function OPTIONAL
    def get_similarity(path, col1, col2, output_name):
        """
        Adds three columns, each representing the token_set, partio ratio and their mean
        Adds two more column representing the word-count between two columns
        """
        df = pd.read_csv(path)
        
        # filling the null values with '' so things are not compared with NaN 
        df.fillna('', inplace=True)

        # compute simple ratio
        match_token = []
        for i in range(len(df)):
            # lowering both columsn
            name1 = str(df[col1][i]).lower()
            name2 = str(df[col2][i]).lower()
            similarity = fuzz.ratio(name1, name2)
            match_token.append(similarity)
            
        # applying partial ratio
        match_partial = []
        for i in range(len(df)):
            # lowering both columsn
            name1 = str(df[col1][i]).lower()
            name2 = str(df[col2][i]).lower()
            similarity = fuzz.partial_ratio(name1, name2)
            match_partial.append(similarity)
            
        # applying token sort
        match_sort = []
        for i in range(len(df)):
            # lowering both columsn
            name1 = str(df[col1][i]).lower()
            name2 = str(df[col2][i]).lower()
            similarity = fuzz.token_sort_ratio(name1, name2)
            match_sort.append(similarity)
            
        # inserting the computed values
        df['simple_ratio'] = match_token
        df['partial_ratio'] = match_partial
        # df['similarity_token_sort_ratio'] = match_sort
        df['mean'] = df[['simple_ratio','partial_ratio']].mean(axis=1)
        # the word-counts
        df['count_col1'] = df[col1].apply(lambda x: len(str(x)))
        df['count_col2'] = df[col2].apply(lambda x: len(str(x)))
        
        df.to_csv(output_name, index=False)
        return

    __name__ == "__main__"
    if __name__ == "__main__":
        start = time.time()

        # Find/Replace function 
        column = find_replace()

        # Fuzzy Matching and saves to "norm_result.csv"
        compare_titles_and_save(column)

        # Timing
        print(time.time() - start)

        # If you want to compare the result from the find replace function run the below commented code
        # and change the column title in the 'compare' function
        # compare(column) 

        


        # Fuzzy Matching csv statistics

        # input_file = 'thefuzz_after.csv'
        # c1 = 'title_before'
        # c2 = 'title_after'
        # output_name = input_file.replace('.csv','') + '_output.csv'
        # get_similarity(input_file,c1,c2, output_name)



#normalize_job_titles('lifull_reg_212.csv')

datasets = ['updated_lifull_322_0.csv', 'updated_lifull_12.2022.csv', 'updated_lifull_419_M2.csv', 'updated_more_training_data.csv', 'updated_lifull_419M3.csv', 'updated_li_full_11_22.csv', 'updated_lifull_bing1_212.csv', 'updated_lifull_419M1.csv', 'updated_lifull_326-001.csv', 'updated_lifull_326-000.csv', 'updated_lifull_326-002.csv', 'updated_lifull_reg_212.csv', 'updated_lifull_bing2_212.csv', 'updated_lifull_303.csv', 'updated_lifull_1_2023.csv', 'updated_lifull_309_1.csv', 'updated_lifull_309_2_3.csv']


for i, file in enumerate(datasets):
    print('file number: ',i)
    normalize_job_titles(file)





