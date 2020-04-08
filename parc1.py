import requests
import json
from pprint import pprint

profile = 'mikebryant'
main_link = 'https://api.github.com/users/' + profile + '/repos'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
response = requests.get(main_link,headers=headers)
data = json.loads(response.content)
print('Репозитории пользователя ' + profile + ' ' + str(len(data)) + ':')
for i in range(len(data)):
    print(data[i]['name'])