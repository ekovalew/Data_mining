from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacansy312']
collection = db.hhru
#collection.delete_many({})
#db.vacansies.deleteMany()

def vac_salary():
    vac = collection.find({'site': 'superjob.ru'})
    return vac
for vac1 in vac_salary():
    n += 1
    print(vac1)
