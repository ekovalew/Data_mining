import requests
import json
from pprint import pprint

profile = 'mikebryant'
main_link = 'https://api.github.com/users/' + profile + '/repos'
params = {'per_page':1000}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
response = requests.get(main_link,headers=headers,params=params)
data = json.loads(response.content)
with open('parc_github.json', 'w') as f:
    json.dump(data, f)
print('Репозитории пользователя ' + profile + ' ' + str(len(data)) + ':')
for i in range(len(data)):
    print(data[i]['name'])