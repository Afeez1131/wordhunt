import json
import time
from statistics import mean

import requests

Learner = '6d44627e-ca63-4211-94c4-cc0f3630489b'
school_dictionary = '041616a8-2cda-4483-b76c-f2e612a775da'
word = 'legend'
base_url = f'https://dictionaryapi.com/api/v3/references/learners/json/'
base_url2 = 'https://dictionaryapi.com/api/v3/references/sd4/json/'
time_list = []
count = 5
start = time.monotonic()
response = requests.get(f'{base_url2}{word}?key={school_dictionary}')

print('response: ', response)
end = time.monotonic()
exec_time = end - start
time_list.append(exec_time)
print(f'The average execution time is {mean(time_list):.2f}')
print(sum(time_list)/ len(time_list))

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


# with open('resp.txt', 'a+') as file:
#     file.write(json.dumps(api_data[0].get("def"), indent=3))
# print(response.status_code)

# print(is_valid)
