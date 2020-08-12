import pandas as pd
from collections import Counter
import json

df = pd.read_csv('Data/users_clean_texts.csv')
users = [str(_) for _ in list(df.user_id)]
datas = []

for user in users:
    with open('Data/Raw/answers/' + user + '.json', encoding='utf-8') as json_file:
        ans_data = json.load(json_file)
    try:
        with open('Data/Raw/questions/' + user + '.json', encoding='utf-8') as json_file:
            qus_data = json.load(json_file)
    except:
        qus_data['items'] = []

    reputation = ans_data['items'][0]['owner']['reputation']
    name = ans_data['items'][0]['owner']['display_name']
    ans_count = len(ans_data['items'])
    qus_count = len(qus_data['items'])
    word_count = list(df[df['user_id'] == int(user)].word_count)[0]
    '''print(f"Name: {name}\nAnswers Count: {ans_count}\n"
          f"Questions Count: {qus_count}\nReputation: {reputation}"
          f"\nWord Count: {word_count}")'''

    tags = []
    for item in qus_data['items']:
        for tag in item['tags']:
            tags.append(tag)

    top_tags = Counter(tags).most_common(10)
    tags_ques = [i[0] for i in top_tags]

    #print(f"Most Frequent 10 tags From Questions: {tags_ques}")

    tags = []
    duplicate_check = dict()
    for item in ans_data['items']:
        if not duplicate_check.get(str(item['question_id'])):
            duplicate_check[str(item['question_id'])] = "done"
            with open('Data/Raw/all_questions/' + str(item['question_id']) + '.json', encoding='utf-8') as json_file:
                tq = json.load(json_file)
            try:
                if 'items' in tq:
                    if len(tq['items']) > 0:
                        for tag in tq['items'][0]['tags']:
                            tags.append(tag)
                else:
                    for tag in tq['tags']:
                        tags.append(tag)
            except:
                print(tq)

    top_tags = Counter(tags).most_common(10)
    tags_ans = [i[0] for i in top_tags]

    #print(f"Most Frequent 10 tags From Answers: {tags_ans}")

    with open('Data/Raw/Personality_Data/' + user + '.json', encoding='utf-8') as json_file:
        pdata = json.load(json_file)

    tmp = []
    for p in pdata['personality']:
        #print(p['name'], " : ", p['percentile'])
        tmp.append(p['percentile'])

    arr = [user, name, ans_count, qus_count, reputation, word_count, tags_ans, tags_ques]
    for t in tmp:
        arr.append(t)
    datas.append(arr)

tf = pd.DataFrame(datas, columns=['id', 'name', 'answer_count', 'question_count',
                                  'reputation', 'word_count', 'top_tags_question', 'top_tags_answers',
                                  'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'emotional range'])
tf.to_csv('Data/sample_dataset.csv', index=False, encoding='utf-8')
