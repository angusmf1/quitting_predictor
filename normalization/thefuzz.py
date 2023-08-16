import csv
import re
import time
from fuzzywuzzy import fuzz
import pandas as pd 

#############CHANGE INFORMATION BELOW THIS LINE#################

# File name of the job titles to be normalized
file_name = '/Users/yuantian/Desktop/developerDB/quitter_vs_non_quitter/NonQuitters1.csv'

# Library files
find_library_name = '/Users/yuantian/Desktop/developerDB/JT-Norm-6-15/find_lib.csv'
title_lib = '/Users/yuantian/Desktop/developerDB/JT-Norm-6-15/title_lib.csv'

# Column name that you want normalized
column_name = 'title_5'

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
    #df.to_csv(file_name[:-4] + 'find_replaced.csv', index = False)
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



## Fuzzy matching
def compare_titles_and_save(titles_before):
    # Read the title_lib
    # Initialize an empty list to store the titles
    titles_list = []

    # Open the CSV title list file
    with open(title_lib, 'r') as file:
        reader = csv.reader(file)
        # Iterate over each row in the CSV file
        for row in reader:
            # Assuming the title is in the first column (index 0)
            title = row[0]
            
            # Append the title to the list
            titles_list.append(title)

    # Original Title
    unchanged_titles = []
    with open(file_name, 'r') as term:
        temp = csv.DictReader(term)
        for row in temp:
            unchanged_titles.append(row[column_name])


    # Compare each title against the list and find the most similar title
    titles_after = []
    number = 0
    same = 0
    for title in titles_before:
        if title in titles_list:
            same = same + 1
            titles_after.append(remove_changes(title))
            continue
            
        else:
            if "intern" in title:
                same = same + 1
                titles_after.append(remove_changes(title))
                continue
            # match = max(titles_list, key=lambda x: fuzz.partial_ratio(title, x))
            match = max(titles_list, key=lambda x: fuzz.token_set_ratio(title, x))
            # sort = max(titles_list, key=lambda x: fuzz.partial_token_sort_ratio(title,x))

            # best_match = max(fuzz.partial_token_set_ratio(title, stete), fuzz.partial_token_sort_ratio(title,sort))
            similarity_score = fuzz.partial_token_set_ratio(title, match)
            if similarity_score >= 80:
                number = number + 1
                match = important_titles(title, match)
                titles_after.append(remove_changes(match))
                # print(f"Match: {best_match}")
            else:
                # print("No Match")
                titles_after.append(remove_changes(title))

    # Save the before and after titles to a new CSV file
    with open('norm_result.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['title_before', 'title_after'])
        writer.writerows(zip(unchanged_titles, titles_after))
        # writer.writerows(zip(titles_before, titles_after))

    print(f"Percentage of titles changed: {float(number) / len(titles_before)} ")
    print(f"Percentage of titles already normalized: {float(same) / len(titles_before)}")
    print(f"Percentage of titles not changed: { 1 - float(number) / len(titles_before) - float(same) / len(titles_before)}")


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
