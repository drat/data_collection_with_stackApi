from stackapi import StackAPI
import json
from time import sleep
import os
import pandas as pd
from Data.apikey import access_token as apikey


def get_data(path, answer_id, question_id):
    global check_all_ques
    try:
        question = SITE.fetch(f'questions/{question_id}', filter='withbody')
        #print(question['items'][0]['tags'])
        check_all_ques.append(str(question_id) + '.json')
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


SITE = StackAPI('stackoverflow', key=apikey)
users = os.listdir('Data/Raw/answers')
users.sort()
df = pd.read_csv('Data/user_list.csv')
accepted_users = [str(x) for x in list(df.user_id)]
ok = True
check_all_ques = []

for user in users[171:]:
    user_id = user.split('.')[0]
    if user_id in accepted_users:
        check_all_ques = os.listdir('Data/Raw/all_questions/')
        print(f"Collecting Data for User: {user_id}")
        path = 'Data/Raw/questions_of_answers/' + user_id + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        with open('Data/Raw/answers/' + user, encoding='utf-8') as json_file:
            answers = json.load(json_file)
        ls = os.listdir(path)
        for item in answers['items']:
            #allques = os.listdir('Data/Raw/all_questions/')
            if str(item['answer_id']) + '.json' not in ls:
                if str(item['question_id']) + '.json' not in check_all_ques:
                    ok = get_data(path, item['answer_id'], item['question_id'])
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
