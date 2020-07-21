from stackapi import StackAPI
import json
from time import sleep
import os
import pandas as pd
from Data.apikey import access_token as apikey


def get_data(path, answer_id, question_id):
    try:
        question = SITE.fetch(f'questions/{question_id}', filter='withbody')
        print(question)
        with open(path + str(answer_id) + '.json', 'w', encoding='utf-8') as outfile:
            json.dump(question, outfile, ensure_ascii=False, indent=4)
        with open('Data/Raw/all_questions/' + str(question_id) + '.json', 'w', encoding='utf-8') as outfile:
            json.dump(question, outfile, ensure_ascii=False, indent=4)
    except:
        print("Something went wrong!\nUser:", user_id)
        with open("Data/Error/" + str(user_id) + '_' + str(answer_id) + ".txt", "w") as f:
            f.write("Something went wrong!")


SITE = StackAPI('stackoverflow', key=apikey)
users = os.listdir('Data/Raw/answers')
for user in users:
    user_id = user.split('.')[0]
    print(f"Collecting Data for User: {user_id}")
    path = 'Data/Raw/questions_of_answers/' + user_id + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    with open('Data/Raw/answers/' + user, encoding='utf-8') as json_file:
        answers = json.load(json_file)
    ls = os.listdir(path)
    for item in answers['items']:
        print("Ans ID:", item['answer_id'])
        allques = os.listdir('Data/Raw/all_questions/')
        if str(item['answer_id']) + '.json' not in ls:
            if str(item['question_id']) + '.json' not in allques:
                get_data(path, item['answer_id'], item['question_id'])
            else:
                with open('Data/Raw/all_questions/' + str(item['question_id']) + '.json',
                          encoding='utf-8') as json_file:
                    data = json.load(json_file)
                with open('Data/Raw/questions_of_answers/' + str(item['answer_id']) + '.json', 'w',
                          encoding='utf-8') as outfile:
                    json.dump(data, outfile, ensure_ascii=False, indent=4)
                print("From previous save!!!")
        else:
            print('Already Collected!')
