from stackapi import StackAPI
import json
from time import sleep
import os
import pandas as pd
from Data.apikey import access_token as apikey


def get_data(user_id):
    try:
        print(user, ":", end=" ")
        answers = SITE.fetch(f'users/{user}/answers', filter='withbody')
        print(len(answers['items']))
        if len(answers['items']) > 0:
            with open('Data/Raw/answers/' + str(user) + '.json', 'w', encoding='utf-8') as outfile:
                json.dump(answers, outfile, ensure_ascii=False, indent=4)
    except:
        print("Something went wrong!\nUser:", user_id)
        with open("Data/Error/" + user_id + ".txt", "w") as f:
            f.write("Something went wrong!")


SITE = StackAPI('stackoverflow', key=apikey)
df = pd.read_csv("Data/Stack_Twitter.csv", encoding='unicode_escape')
users = [userid.split('/')[2] for userid in list(df.STACK_ID)]
ls = [file.split('.')[0] for file in os.listdir('Data/Raw/answers/')]

for user in users:
    if user not in ls:
        print("Collecting Data of user:", user)
        get_data(user)
    else:
        print("Already collected!")

