from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import string
import os
from Data.apikey import ibm_key as api_key


def clean_text(text):
    import re
    clean = re.compile('<pre>([\s\S]*?)</pre>')
    text = re.sub(clean, '', text)
    clean = re.compile('<code>([\s\S]*?)</code>')
    text = re.sub(clean, '', text)
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = text.split()
    table = str.maketrans('', '', string.punctuation)
    res = [w.translate(table) for w in text]
    return ' '.join(res)


authenticator = IAMAuthenticator(api_key)
personality_insights = PersonalityInsightsV3(
    version='2017-10-13',
    authenticator=authenticator
)

personality_insights.set_service_url('https://api.us-south.personality-insights.watson.cloud.ibm.com/instances/66b10b97-021d-47ae-b5c2-fec4f691fc69')

users = os.listdir('Data/Raw/answers')
users.sort()
for user in users:
    user_texts = ""
    print(user)

    personality_path = 'Data/Raw/Personality_Data/'
    ls = os.listdir(personality_path)

    if not os.path.exists(personality_path + user):
        print("Collecting data of user:", user.split('.')[0])
        with open('Data/Raw/answers/' + user, encoding='utf-8') as json_file:
            answers = json.load(json_file)
        for item in answers['items']:
            user_texts += clean_text(item['body'])

        q_path = 'Data/Raw/questions/' + user
        if os.path.exists(q_path):
            with open(q_path, encoding='utf-8') as json_file:
                questions = json.load(json_file)
            for item in questions['items']:
                user_texts += clean_text(item['body'])

        profile = personality_insights.profile(user_texts, content_type='text/plain', accept_language='en',
                                               accept='application/json').get_result()
        with open('Data/Raw/Personality_Data/' + user, 'w', encoding='utf-8') as outfile:
            json.dump(profile, outfile, ensure_ascii=False, indent=4)
    else:
        print("Already collected!")
