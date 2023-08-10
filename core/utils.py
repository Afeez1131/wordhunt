import json
import time
from statistics import mean

import requests

LEARNER = '6d44627e-ca63-4211-94c4-cc0f3630489b'
SCHOOL_DICTIONARY = '041616a8-2cda-4483-b76c-f2e612a775da'
# word = 'legend'
BASE_URL_LEARNER = f'https://dictionaryapi.com/api/v3/references/learners/json/'
BASE_URL_SCHOOL = 'https://dictionaryapi.com/api/v3/references/sd4/json/'


def send_api_request(word):
    try:
        response = requests.get(f'{BASE_URL_SCHOOL}{word}?key={SCHOOL_DICTIONARY}')
        api_data = response.json()
        is_valid = isinstance(api_data[0], dict) and api_data[0].get("meta") is not None
        if is_valid:
            print('it is a valid english word')
            # d = api_data[0].get("def")
            # dd = d[0].get("sseq")
            # dd_len = len(dd)
            # for i in range(dd_len):
            #     print(dd[i][0], '\n\n')
        else:
            print('Not a valid english word..')
    except Exception as e:
        print(str(e))
