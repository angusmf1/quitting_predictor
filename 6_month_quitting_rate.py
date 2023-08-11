import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
author: @Bill Tian
upload data: Aug 11, 2023

"""


df = pd.read_csv('Cleaned_Combined_Data.csv')
time_df = df[['time_duration_2', 'time_duration_3', 'time_duration_4', 'time_duration_5', 'time_duration_6']]

total_buckets = {'2014-Jan-June': 0, '2014-July-Dec': 0,'2015-Jan-June': 0, '2015-July-Dec': 0,
                 '2016-Jan-June': 0, '2016-July-Dec': 0, '2017-Jan-June': 0, '2017-July-Dec': 0, 
                 '2018-Jan-June': 0, '2018-July-Dec': 0,'2019-Jan-June': 0,'2019-July-Dec': 0,
                 '2020-Jan-June': 0,'2020-July-Dec': 0,'2021-Jan-June': 0,'2021-July-Dec': 0,
                 '2022-Jan-June': 0,'2022-July-Dec': 0}

quitting_buckets = {'2014-Jan-June': 0, '2014-July-Dec': 0,'2015-Jan-June': 0, '2015-July-Dec': 0,
                 '2016-Jan-June': 0, '2016-July-Dec': 0, '2017-Jan-June': 0, '2017-July-Dec': 0, 
                 '2018-Jan-June': 0, '2018-July-Dec': 0,'2019-Jan-June': 0,'2019-July-Dec': 0,
                 '2020-Jan-June': 0,'2020-July-Dec': 0,'2021-Jan-June': 0,'2021-July-Dec': 0,
                 '2022-Jan-June': 0,'2022-July-Dec': 0}

def filter_dataframe(dataframe):
"""Filter out incorrect format work duration and return a correct-formatted dataframe"""
    filtered_rows = []

    for index, row in dataframe.iterrows():
        valid = True

        for column in dataframe.columns:
            value = row[column]

            if pd.isna(value):  # Keep NaN values
                continue

            if not isinstance(value, str):
                valid = False
                break

            if len(value) != 19:
                valid = False
                break

        if valid:
            filtered_rows.append(index)

    return dataframe.loc[filtered_rows]

def update_quitting_bucket(year, df):
"""Update a quitting bucket, year:int, df:dataframe"""

    for column in df.columns:
        for item in df[column]:
            if pd.isna(item):
                continue
            
            else:
                start = item.split('-')[0]
                end = item.split('-')[1]
            
                end_year = end.split()[1]
                end_month = end.split()[0]
                if end_year == year:
                    if end_month == 'Jan' or end_month == 'Feb' or end_month == 'Mar' or end_month == 'Apr' or end_month == 'May' or end_month == 'Jun':
                        quitting_buckets[year + '-Jan-June'] += 1
                        
                    else:
                        quitting_buckets[year + '-July-Dec'] += 1

def update_total_bucket(year, df):
"""Update a total bucket, year:int, df:dataframe"""
    
    for column in df.columns:
        for item in df[column]:
            if pd.isna(item):
                continue
            
            else:
                start = item.split('-')[0]
                end = item.split('-')[1]
            
                start_year = start.split()[1]
                start_month = start.split()[0]
                
                end_year = end.split()[1]
                end_month = end.split()[0]
                if start_year == year and end_year == year:
                    if end_month == 'Jan' or end_month == 'Feb' or end_month == 'Mar' or end_month == 'Apr' or end_month == 'May' or end_month == 'Jun':
                        total_buckets[year + '-Jan-June'] += 1
                        
                    else:
                        total_buckets[year + '-July-Dec'] += 1
                        
                elif start_year == year and int(end_year) >  int(year):
                    if end_month == 'Jan' or end_month == 'Feb' or end_month == 'Mar' or end_month == 'Apr' or end_month == 'May' or end_month == 'Jun':
                        total_buckets[year + '-Jan-June'] += 1
                    else:
                        total_buckets[year + '-Jan-June'] += 1
                        total_buckets[year + '-July-Dec'] += 1
                    
                elif int(start_year) < int(year) and int(end_year) > int(year):
                    total_buckets[year + '-Jan-June'] += 1
                    total_buckets[year + '-July-Dec'] += 1
                    
                elif int(start_year) < int(year) and end_year == year:
                    if end_month == 'Jan' or end_month == 'Feb' or end_month == 'Mar' or end_month == 'Apr' or end_month == 'May' or end_month == 'Jun':
                        total_buckets[year + '-Jan-June'] += 1
                        
                    else:
                        total_buckets[year + '-July-Dec'] += 1
                elif int(start_year) < int(year) and int(end_year) < int(year):
                    continue


original = filter_dataframe(time_df)

update_quitting_bucket('2014', original)
update_quitting_bucket('2015', original)
update_quitting_bucket('2016', original)
update_quitting_bucket('2017', original)
update_quitting_bucket('2018', original)
update_quitting_bucket('2019', original)
update_quitting_bucket('2020', original)
update_quitting_bucket('2021', original)
update_quitting_bucket('2022', original)


update_total_bucket('2014', original)
update_total_bucket('2015', original)
update_total_bucket('2016', original)
update_total_bucket('2017', original)
update_total_bucket('2018', original)
update_total_bucket('2019', original)
update_total_bucket('2020', original)
update_total_bucket('2021', original)
update_total_bucket('2022', original)

x_name = ['2014-Jan-June','2014-July-Dec','2015-Jan-June','2015-July-Dec',
          '2016-Jan-June','2016-July-Dec','2017-Jan-June','2017-July-Dec',
          '2018-Jan-June','2018-July-Dec','2019-Jan-June','2019-July-Dec',
          '2020-Jan-June','2020-July-Dec','2021-Jan-June','2021-July-Dec',
          '2022-Jan-June','2022-July-Dec']

        
quitting_rate = [quitting_buckets['2014-Jan-June'] / total_buckets['2014-Jan-June'], quitting_buckets['2014-July-Dec'] / total_buckets['2014-July-Dec'],
                 quitting_buckets['2015-Jan-June'] / total_buckets['2015-Jan-June'], quitting_buckets['2015-July-Dec'] / total_buckets['2015-July-Dec'],
                 quitting_buckets['2016-Jan-June'] / total_buckets['2016-Jan-June'], quitting_buckets['2016-July-Dec'] / total_buckets['2016-July-Dec'],
                 quitting_buckets['2017-Jan-June'] / total_buckets['2017-Jan-June'], quitting_buckets['2017-July-Dec'] / total_buckets['2017-July-Dec'],
                 quitting_buckets['2018-Jan-June'] / total_buckets['2018-Jan-June'], quitting_buckets['2018-July-Dec'] / total_buckets['2018-July-Dec'],
                 quitting_buckets['2019-Jan-June'] / total_buckets['2019-Jan-June'], quitting_buckets['2019-July-Dec'] / total_buckets['2019-July-Dec'],
                 quitting_buckets['2020-Jan-June'] / total_buckets['2020-Jan-June'], quitting_buckets['2020-July-Dec'] / total_buckets['2020-July-Dec'],
                 quitting_buckets['2021-Jan-June'] / total_buckets['2021-Jan-June'], quitting_buckets['2021-July-Dec'] / total_buckets['2021-July-Dec'],
                 quitting_buckets['2022-Jan-June'] / total_buckets['2022-Jan-June'], quitting_buckets['2022-July-Dec'] / total_buckets['2022-July-Dec'],]


#table = pd.DataFrame({"quitting count":list(quitting_buckets.values()), "total count":list(total_buckets.values()) , "quitting rate": quitting_rate} ,index = x_name)


#Graph
"""plt.figure(figsize=(10, 6))
plt.plot(x_name, quitting_rate, marker='o')

plt.title('6 month quitting rate')
plt.xlabel('Time Period')
plt.ylabel('quitting rate')

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()"""