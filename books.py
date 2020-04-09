import requests
import json
from pprint import pprint

main_link = 'https://www.goodreads.com/book/show.xml'
params = {
            'id': 33917,
            'key':'gIRxQgOU164vDWb63NlnA',
            'text_only': 'false',
            'rating': 'false'}
response = requests.get(main_link,params=params)
data = response.text
pprint(data)
with open('books.json', 'w') as f:
    json.dump(data, f)