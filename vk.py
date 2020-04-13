import requests
import json
from pprint import pprint

main_link = 'https://oauth.vk.com/authorize?client_id=7398414&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52'
response = requests.get(main_link)
url = response.url
print(url)