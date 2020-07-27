from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import os
from Data.apikey import ibm_key as api_key
import pandas as pd

authenticator = IAMAuthenticator(api_key)
personality_insights = PersonalityInsightsV3(
    version='2017-10-13',
    authenticator=authenticator
)

personality_insights.set_service_url('https://api.us-south.personality-insights.watson.cloud.ibm.com/instances/66b10b97-021d-47ae-b5c2-fec4f691fc69')

df = pd.read_csv('Data/users_texts.csv')
for index, row in df.iterrows():
    user = row['user_id']
    personality_path = 'Data/Raw/Personality_Data/'
    ls = os.listdir(personality_path)

    if not os.path.exists(personality_path + str(user) + '.json'):
        print("Collecting data of user:", user)
        profile = personality_insights.profile(row['text'], content_type='text/plain', accept_language='en',
                                               accept='application/json').get_result()
        with open(personality_path + str(user) + '.json', 'w', encoding='utf-8') as outfile:
            json.dump(profile, outfile, ensure_ascii=False, indent=4)
    else:
        print("Already collected!")
