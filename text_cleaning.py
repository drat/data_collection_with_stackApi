import json
import os
import pandas as pd
import re
from cleantext import clean
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer


def get_clean_text(text):
    tmp = re.compile('<pre>([\s\S]*?)</pre>')
    text = re.sub(tmp, ' ', text)
    tmp = re.compile('<code>([\s\S]*?)</code>')
    text = re.sub(tmp, ' ', text)
    tmp = re.compile('<.*?>')
    text = re.sub(tmp, ' ', text)
    text = ' '.join(text.split())
    text = clean(text,
                 fix_unicode=True,  # fix various unicode errors
                 to_ascii=True,  # transliterate to closest ASCII representation
                 lower=True,  # lowercase text
                 no_line_breaks=True,  # fully strip line breaks as opposed to only normalizing them
                 no_urls=True,  # replace all URLs with a special token
                 no_emails=True,  # replace all email addresses with a special token
                 no_phone_numbers=True,  # replace all phone numbers with a special token
                 no_numbers=True,  # replace all numbers with a special token
                 no_digits=False,  # replace all digits with a special token
                 no_currency_symbols=False,  # replace all currency symbols with a special token
                 no_punct=True,  # fully remove punctuation
                 replace_with_url=" ",
                 replace_with_email=" ",
                 replace_with_phone_number=" ",
                 replace_with_number=" ",
                 replace_with_digit="0",
                 replace_with_currency_symbol="<CUR>",
                 lang="en"  # set to 'de' for German special handling
                 )
    tokenized_text = word_tokenize(text)
    wordnet = WordNetLemmatizer()
    ret = []
    for w in tokenized_text:
        tmp = wordnet.lemmatize(w)
        if len(tmp) <= 15:
            ret.append(tmp)
    text = ' '.join(ret)
    return text


df = pd.read_csv('Data/user_list.csv')
users = list(df.user_id)
users.sort()
arr = []

for user in users:
    user_texts = ""

    with open('Data/Raw/answers/' + str(user) + '.json', encoding='utf-8') as json_file:
        answers = json.load(json_file)
    for item in answers['items']:
        user_texts += ' ' + item['body']

    q_path = 'Data/Raw/questions/' + str(user) + '.json'
    if os.path.exists(q_path):
        with open(q_path, encoding='utf-8') as json_file:
            questions = json.load(json_file)
        for item in questions['items']:
            user_texts += ' ' + item['body']
    user_texts = get_clean_text(user_texts)
    #print([user, len(user_texts), user_texts])
    arr.append([user, len(user_texts), user_texts])

tf = pd.DataFrame(arr, columns=['user_id', 'word_count', 'text'])
tf.to_csv('Data/users_texts.csv', index=False, encoding='utf-8')
