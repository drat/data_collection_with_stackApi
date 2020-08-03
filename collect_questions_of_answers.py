from stackapi import StackAPI
import json
from time import sleep
import os
import requests
import pandas as pd
from random import choice
from Data.apikey import access_token as apikey

proxies = []
SITE = StackAPI('stackoverflow')


def init():
    global SITE
    SITE = StackAPI('stackoverflow', key=apikey)


def get_data(path, answer_id, question_id):
    global check_all_ques
    global proxies
    global SITE
    try:
        question = SITE.fetch(f'questions/{question_id}', filter='withbody')
        #print(question['items'][0]['tags'])
        check_all_ques[str(question_id)] = 'Data/Raw/all_questions/' + str(question_id) + '.json'
        with open(path + str(answer_id) + '.json', 'w', encoding='utf-8') as outfile:
            json.dump(question, outfile, ensure_ascii=False, indent=4)
        with open('Data/Raw/all_questions/' + str(question_id) + '.json', 'w', encoding='utf-8') as outfile:
            json.dump(question, outfile, ensure_ascii=False, indent=4)
        return True
    except:
        print("Something went wrong!\nUser:", user_id)
        with open("Data/Error/" + str(user_id) + '_' + str(answer_id) + ".txt", "w") as f:
            f.write("Something went wrong!")
        return False


init()
users = os.listdir('Data/Raw/answers')
users.sort()
df = pd.read_csv('Data/user_list.csv')
accepted_users = [str(x) for x in list(df.user_id)]
ok = True
check_all_ques = dict()
q_path = 'Data/Raw/all_questions/'
q_list = os.listdir(q_path)
for i in q_list:
    x = str(i.split('.')[0])
    check_all_ques[x] = q_path + i

total_cnt = 0
api_call_cnt = 0
index = 0

for user in users:
    user_id = user.split('.')[0]
    if user_id in accepted_users:
        print(f"#Index: {index} ---> Collecting Data for User: {user_id}")
        print(f"Total: {total_cnt} >--< API Calls: {api_call_cnt}")
        index += 1
        path = 'Data/Raw/questions_of_answers/' + user_id + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        with open('Data/Raw/answers/' + user, encoding='utf-8') as json_file:
            answers = json.load(json_file)
        ls = os.listdir(path)
        for item in answers['items']:
            if str(item['answer_id']) + '.json' not in ls:
                total_cnt += 1
                if not check_all_ques.get(str(item['question_id'])):
                    ok = get_data(path, item['answer_id'], item['question_id'])
                    api_call_cnt += 1
                else:
                    with open('Data/Raw/all_questions/' + str(item['question_id']) + '.json',
                              encoding='utf-8') as json_file:
                        data = json.load(json_file)
                    with open(path + str(item['answer_id']) + '.json', 'w',
                              encoding='utf-8') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=4)
                    print("From previous save!!!")
            if not ok:
                break
        if not ok:
            break

print(f"Total: {total_cnt}\nAPI Calls: {api_call_cnt}")
