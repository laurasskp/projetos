import pandas as pd
import numpy as np
import datetime
import os

#Establishes the current date as part of the archive name
current_date = datetime.datetime.now().strftime("%Y_%m_%d")
filename = f"issues_{current_date}.json"

#Here, you need to fill with: 1st row limit; 2nd repo; 3rd issues' items you want to extract
#Remeber to pass the path where you want to save on, or to navigate to it before run this script
#os.system(f"gh issue list -s all --limit {1s} -R {2nd}/{2nd} -- {3rd} json number,title,closed,author,createdAt,closedAt,assignees,labels,projectCards > ./{filename}")

#Reads the json file 
df = pd.read_json(f"{filename}")

#Searches for issue type in labels
df.loc[:,'bug'] = df.labels.apply(lambda x: ['bug' for item in x if item['name'] == 'bug'][0] if any(item['name'] == 'bug' for item in x) else None)
df.loc[:,'enhancement'] = df.labels.apply(lambda x: ['enhancement' for item in x if item['name'] == 'enhancement'][0] if any(item['name'] == 'enhancement' for item in x) else None)
df.loc[:,'urgent'] = df.labels.apply(lambda x: ['urgent' for item in x if item['name'] == 'urgent'][0] if any(item['name'] == 'urgent' for item in x) else None)

#Searches for assignee info. If more than 1, brings them all separated with comma
df.loc[:,'assignee_login'] = df.assignees.apply(lambda x: ', '.join([item['login'] for item in x]) if any(item['login']for item in x) else None)
df.loc[:,'assignee_name'] = df.assignees.apply(lambda x: ', '.join([item['name'] for item in x]) if any(item['name'] for item in x) else None)

#Issue's author
df['login_autor'] = df['author'].apply(lambda x: x['login'])

#Issue's client (requester)
df.loc[:, 'client'] = df.labels.apply(lambda x: ', '.join([item['name'].split('- ')[1] for item in x if 'Client - ' in item['name']]) if any('Client -' in item['name'] for item in x) else None)

#Spent: the time in hours spent on an issue. Brings the biggest in the interval
df.loc[:, 'spent'] = df.labels.apply(lambda x: [item['name'].split('-')[1] for item in x if 'spent' in item['name']][0] if any('spent' in item['name'] for item in x) else None)

#Effort: the time in hours estimated for an issue. Brings the biggest in the interval
df.loc[:, 'effort'] = df.labels.apply(lambda x: [item['name'].split('-')[1] if '-' in item['name'] else item['name'].split('>')[1] for item in x if 'effort' in item['name']][0] if any('effort' in item['name'] for item in x) else None)

#Type conversion
df['closedAt'] = pd.to_datetime(df['closedAt'])
df['createdAt'] = pd.to_datetime(df['createdAt'])

#Monitoring: informs if an issue problem was found by the team. When absent: it was found by a client (external_report) 
df.loc[:,'monitoring'] = df.labels.apply(lambda x: ['monitoring' for item in x if item['name'] == 'monitoring'][0] if any(item['name'] == 'monitoring' for item in x) else 'external_report')

#Fix cases that title has extra spaces
def title_fix(row):
    title = str(row['title'])
    return " ".join(title.split())

#Issue's title
df['title'] = df.apply(title_fix, axis=1)

#Lowest effort in the interval
df.loc[:, 'effort_min'] = df.labels.apply(lambda x: [item['name'].split(' ')[1].split('-')[0] if '-' in item['name'] else item['name'].split('>')[1] for item in x if 'effort' in item['name']][0] if any('effort' in item['name'] for item in x) else None)

#Type conversion
df.spent = pd.to_numeric(df.spent)
df.effort = pd.to_numeric(df.effort)

#Dropping other columns
df = df.drop(columns=['assignees', 'labels', 'projectCards', 'author'])

#Saving the date as a csv file with sep = ';'
df.to_csv('issues_info.csv', sep =';' ,index = False)