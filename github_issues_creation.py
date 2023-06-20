from github import Github
import random

#To use the github library above, it's necessary to have PyGitHub installed.

'''You need to complete with a personal token. Access your "Settings" on github > "developer settings" >
personal access tokens > fine-grained tokens > generate new token. You're going to need to set the permissions,
because the library uses the token to viabilize the issue creation  
'''
#token = "your_token_here"
#g = Github(token)

#Gets the repo
repo_name = "laurasskp/projetos"
repo = g.get_repo(repo_name)

#Creates a pool of options for the issues creation.
#Here, I used chat GPT to create more options of labels combo based on those I've previously created
title_options_1st_part = ['broken', 'unavailable', 'disordered', 'unformatted', 'erased']
title_options_2nd_part = ['page', 'button', 'slider', 'checkbox', 'dropdown']
title_options_clients = ['A', 'B', 'C']
labels_options_combo = [
    ['bug', 'urgent', 'Client - A', 'monitoring', 'effort 0-2', 'spent 3-5'],
    ['enhancement', 'monitoring', 'effort 30-40', 'spent > 40'],
    ['bug', 'urgent', 'Client B', 'monitoring', 'effort 0-2', 'spent 0-2'],
    ['enhancement', 'monitoring', 'effort 30-40', 'spent 30-40'],
    ['bug', 'Client - B', 'monitoring', 'effort 6-10', 'spent 11-20'],
    ['bug', 'Client - C', 'monitoring', 'effort 3-5', 'spent 3-5'],
    ['enhancement', 'urgent', 'Client - A', 'effort 6-10', 'spent 11-20'],
    ['enhancement', 'Client - B', 'effort 0-2', 'spent 0-2'],
    ['bug', 'Client - C', 'effort 11-20', 'spent 6-10'],
    ['enhancement', 'Client - A', 'monitoring', 'effort 11-20', 'spent 3-5'],
    ['bug', 'Client - B', 'effort > 40', 'spent 30-40'],
    ['enhancement', 'Client - C', 'monitoring', 'effort 0-2', 'spent 11-20'],
    ['bug', 'urgent', 'Client - A', 'effort 30-40', 'spent 30-40'],
    ['enhancement', 'monitoring', 'effort 3-5', 'spent 6-10'],
    ['bug', 'Client - B', 'effort 11-20', 'spent 6-10'],
    ['enhancement', 'urgent', 'Client - B', 'monitoring', 'effort > 40', 'spent 30-40'],
    ['bug', 'Client - A', 'effort 6-10', 'spent 11-20'],
    ['enhancement', 'Client - B', 'monitoring', 'effort 11-20', 'spent 3-5'],
    ['bug', 'Client - C', 'monitoring', 'effort 3-5', 'spent 11-20'],
    ['enhancement', 'Client - A', 'effort 30-40', 'spent 30-40']]

#Establishes the parts of the issue, assuring that if client 'A' is mentioned in the title, then
#The same client is present in the label
for item in range(len(labels_options_combo)):
    title_part_1 = random.choice(title_options_1st_part)
    title_part_2 = random.choice(title_options_2nd_part)
    client = random.choice(title_options_clients)
    
    title = f'[Client {client}] {title_part_1} {title_part_2}'
    
    # Finds the labels options for the selected client
    labels_options = None
    for options in labels_options_combo:
        if f'Client - {client}' in options:
            labels_options = options
            break
    
    if labels_options is None:
        continue  
    # Skips this iteration if {client} is not in the labels options, or is there's no client 

    labels = labels_options
    body = "Issue body"

    issue = repo.create_issue(title=title, body=body, labels=labels)
    print("Issue successfully created!")